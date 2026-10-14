# Week 03 — Tool Calling for AEM Diagnostics

An AEM diagnostic assistant that can **ask for runtime evidence**. The model requests a
read-only lookup, the application runs it, and the model answers from the result. One
explicit round trip, no agent framework.

```
contracts.py       BundleStatus / ComponentStatus (tool results), BundleStatusArgs /
                   ComponentStatusArgs (tool arguments), the two FunctionToolParam dicts
tools.py           get_bundle_status, get_component_status over deterministic mock data
tool_registry.py   REGISTRY (name -> (args model, callable)) and dispatch(name, arguments)
runner.py          ask(question) -> str: the full model -> tool -> model round trip
test_failures.py   Part E: the three offline rejections and the two live cases
```

Run (from this directory):

```zsh
uv run runner.py          # the translation-bundle diagnosis
uv run test_failures.py   # failure exercises; the last two cases call the API
```

`OPENAI_API_KEY` comes from the environment and appears nowhere in the source.

---

## The model does not call your function

"The LLM calls my Python function" is the sentence to unlearn this week. The model never
executes anything. It emits a `function_call` item: a tool **name**, a JSON string of
**arguments**, and a **`call_id`**. Everything after that is ordinary application code:

```
question ──> model (with tool definitions)
                │
                ▼
        function_call(name, arguments, call_id)      ← a proposal, nothing has run
                │
                ▼
        dispatch(name, arguments)                     ← allowlist, validate, execute
                │
                ▼
        function_call_output(call_id, output)         ← serialized result, or an error
                │
                ▼
        model ──> final answer
```

`runner.py` is that diagram in forty lines. The first `responses.create` returns the
proposals; the loop turns each one into a `function_call_output` whose `call_id` matches;
the second `responses.create` receives the whole accumulated history and produces the
answer. Two details matter more than they look:

- **`input_items += response.output`** keeps the model's own items, including its
  reasoning item, in the history. The follow-up call is a continuation, not a fresh
  question with results pasted in.
- **Every `call_id` needs an output.** If a tool fails and nothing is appended for its
  `call_id`, the second call is rejected by the API. This is why the error path in the
  loop *appends* rather than *raises*.

The boundary this creates is the point of the week. The model proposes; the application
decides whether the proposal is allowed, executes it, and chooses what the model gets to
see. Authentication, authorization, timeouts, logging and side effects all live on the
application side of that line, where they can be tested and audited.

## Structured output versus function calling

Week 2 constrained the *shape of the answer*: the model's final text had to decode into
an `AemDiagnostic`. Week 3 constrains the *shape of a request*: when the model wants
data, the request it emits has to decode into `BundleStatusArgs` or
`ComponentStatusArgs`.

Same mechanism, strict JSON Schema decoding, pointed in opposite directions. Structured
output is the model talking to the caller. Function calling is the model talking to the
application mid-flight, and the application talking back. The round trip is what makes it
different: a structured-output call has one response, a tool call has at least two, and
the history between them is state your code owns.

## What each field of the contract does

| Piece | What it does | Where it is in this project |
| --- | --- | --- |
| `name` | The key the application dispatches on. Not an instruction to run anything. | `"get_bundle_status"` in `contracts.py`, matched in `REGISTRY` |
| `description` | The only thing the model has to decide *when* to use the tool. | Three-sentence pattern: what it looks up, what comes back, when to prefer it over the other tool |
| `parameters` | JSON Schema for the arguments. | `BundleStatusArgs.model_json_schema()`: one declaration feeds the schema and the validator |
| `strict: True` | The decoder refuses argument JSON that violates the schema. | Requires `additionalProperties: false`, which `ConfigDict(extra="forbid")` emits |
| `call_id` | Correlates a request with its result across the two API calls. | Copied verbatim from the `function_call` item into the `function_call_output` |
| `function_call_output` | The application's reply to one `call_id`. A string, so JSON is serialized by hand. | `result.model_dump_json()`, or `json.dumps({"error": ...})` |

The descriptions are worth a note. The tools do not receive credentials, instance URLs,
or anything the application already knows. The model gets a *name* for a lookup; the
application decides what that name is bound to. The same `get_bundle_status` contract can
later sit over mock data, Jolokia/JMX on a 6.5 instance, or the AEMaaCS Developer
Console's status dumps, without the model noticing.

## Why tool arguments are untrusted input, even with a strict schema

Strict mode guarantees that the argument JSON *parses* against the schema: the right
keys, the right types, no extras. It guarantees nothing about the *values*. The model
chooses them, and the model is a text generator with the user's question in its context.
A symbolic name can be anything the user typed, anything the model guessed, or anything
an earlier tool result contained.

So `dispatch` validates again, on the application side, with the same Pydantic model that
generated the schema:

```python
args = args_model.model_validate_json(arguments)
return func(**args.model_dump())
```

The `**` unpacking is safe *only because the line above it ran*. `extra="forbid"` means no
key reaches the function that was not declared on the args model, so a hallucinated
`force=True` or `instance_url=...` is rejected before it can be passed as a keyword. The
first part of `test_failures.py` shows what that looks like when it fires: a payload with
`name` instead of `symbolic_name` produces one `ValidationError` carrying **both**
problems, the extra field and the missing one.

Two tool implementations in this project treat their argument as a lookup key into a
dict. A real backend would treat it as a query parameter, a JMX object name, or a URL
path segment, which is exactly where unvalidated, unescaped values do damage.

## The registry: an allowlist, not a lookup

```python
REGISTRY: dict[str, tuple[type[BaseModel], Callable]] = {
    "get_bundle_status": (BundleStatusArgs, get_bundle_status),
    "get_component_status": (ComponentStatusArgs, get_component_status),
}
```

The model emits a string. The only thing that string is ever used for is a `dict.get`
against this mapping. A name that is not a key raises `KeyError` and nothing runs: the
registry **fails closed**.

What this replaces is any form of "take the name and find something to call":
`eval(name)`, `globals()[name]`, `getattr(module, name)`, `importlib.import_module`. All
of them turn a model-produced string into code selection, and the set of things they can
reach is "whatever is importable", not "the two functions we advertised". The registry
makes the set of callable things a literal in the source, reviewable in a diff, and
identical to the set of tools the model was told about.

The registry is also where authorization will live. A tool entry is the natural place to
attach "read-only", "requires role X", "allowed on this environment". The model does not
get a vote on any of that.

## Failure exercises

`test_failures.py` covers the four cases Part E asks for. The first three run against
`dispatch` directly, offline, and assert the *specific* exception, which proves the
failures are distinguishable before the runner flattens them into an error payload:

| Case | Input | Result |
| --- | --- | --- |
| Unknown tool | `restart_bundle` | `KeyError: 'Unknown tool: restart_bundle'` |
| Invalid arguments | `{"name": "com.acme.core"}` to `get_bundle_status` | `ValidationError`, 2 errors: `extra_forbidden` on `name`, `missing` on `symbolic_name` |
| Tool raises | `com.acme.nonexistent` | `LookupError: Bundle not found com.acme.nonexistent` |

(The `KeyError` text is quoted because `KeyError` reprs its argument. Cosmetic, but it is
what the model will see in the error payload.)

The last two cases go through `ask()` and the real model.

**Tool raises, end to end.** The runner catches the `LookupError` and sends
`{"error": "LookupError: Bundle not found com.acme.nonexistent"}` as the
`function_call_output`. The model answered:

> Bundle `com.acme.nonexistent` was not found, so its runtime state cannot be determined.

No traceback, no invented status. The error is returned to the model as *data*, and the
model decides what to tell the user. Catching broad `Exception` is deliberate at this one
point: it is the boundary between application and model, and a tool failure must never
take the process down with a `call_id` left unanswered. Inside `dispatch` the exceptions
stay specific.

**No tool needed.** This case did not pass on the first run, and the reason is the most
useful finding of the week. The original instructions said:

> Use the available tools to gather runtime evidence before answering. Base your answer
> only on tool results.

Given "What is the difference between an OSGi bundle being INSTALLED and RESOLVED?", the
model obeyed that literally. Across two runs of the same code it failed two different
ways:

1. It **invented an argument** to have something to look up, called
   `get_bundle_status({"symbolic_name": "com.adobe.granite.workflow.core"})`, received a
   `LookupError` payload, and asked for *another* tool call, which hit the runner's
   one-round-trip guard.
2. It made no tool call but **refused to answer**: "Please provide the bundle's symbolic
   name. I need to check its runtime status before answering."

The fix was not in the tools, the schemas, or the registry. It was one sentence in
`INSTRUCTIONS`: tools are for questions about the runtime state of a specific bundle or
component; general or conceptual questions are answered directly. After that change the
same question produced a correct INSTALLED/RESOLVED explanation with no `[tool]` log
line. Schemas decide *how* a tool is called. Instructions decide *whether*.

## Other observations from the model's behaviour

- **Examples in argument descriptions become guesses.** `ComponentStatusArgs` describes
  its field with an example FQCN. On the main question, which only says "the translation
  scheduler component", the model produced that exact FQCN. It was the right one here
  because the mock data was built around it. On a real instance an example in a
  description is a value the model will reach for when it does not know the answer.
- **The final answer goes beyond the tool results.** The model summarised the evidence
  faithfully and then added that the API bundle is "missing, inactive, or exports an
  incompatible version". No tool result says that. It is a reasonable inference from an
  unresolved `Import-Package` range, but it is inference, and the instruction "base your
  answer only on tool results" did not stop it.
- **Remediation comes from general knowledge.** "Resolve that API bundle/version
  dependency, then restart or refresh" is textbook OSGi advice. The tools are read-only
  and said nothing about fixes. Useful, but it is the model's training, not the
  instance's state.
- **The same prompt does not behave the same twice.** The two failure modes above came
  from identical code and instructions. A single successful run proves nothing about a
  tool-use policy; it has to be checked repeatedly, which is what the Week 4 evaluation
  suite is for.
- **Correlation across tools works.** Given an INSTALLED bundle with an unresolved import
  of `com.acme.translation.api` and a component with an unsatisfied `TranslationService`
  reference from that package, the model connected the two as one root cause. That is the
  behaviour the whole design exists to produce: deterministic code supplies facts, the
  model supplies the explanation.

## The same design in Java, on an OSGi runtime

If the orchestration lived inside AEM, or in a Java service beside it, the chain is the
same five steps with the same owner for each: **tool definition/DTO → allowlisted
registry → validated arguments → OSGi diagnostic service → structured result → model**.

**Tool definition and argument DTO.** A record per tool's arguments, with Bean Validation
for the per-field rules and Jackson set to reject unknown properties, the
`extra="forbid"` equivalent. Plain Jackson does that by default, but Spring Boot and most
framework-managed `ObjectMapper`s turn it off, so pin it explicitly:

```java
@JsonIgnoreProperties(ignoreUnknown = false)
public record BundleStatusArgs(@NotBlank String symbolicName) {}

public record BundleStatus(String symbolicName, BundleState state, String version,
                           List<String> importProblems) {}
```

The JSON Schema advertised to the model is generated from the record (or written once
beside it); either way the DTO is the single source of truth, as the Pydantic args model
is here.

**Allowlisted registry.** A typed interface and an explicit map. The model's string is a
map key and nothing else:

```java
public interface DiagnosticTool<A, R> {
    Class<A> argsType();
    R execute(A args);
}

private final Map<String, DiagnosticTool<?, ?>> registry = Map.of(
    "get_bundle_status",    bundleStatusTool,
    "get_component_status", componentStatusTool);

ToolResult dispatch(String name, String argumentsJson) {
    DiagnosticTool<?, ?> tool = registry.get(name);
    if (tool == null) {
        return ToolResult.error("Unknown tool: " + name);   // fails closed
    }
    return run(tool, argumentsJson);
}
```

No `Class.forName(name)`, no `bundleContext.getServiceReference(name)`, no reflection
over method names. The map is the allowlist and the authorization point.

**Validated arguments.** `ObjectMapper.readValue(json, tool.argsType())`, then
`Validator.validate(args)`; a non-empty violation set becomes a controlled tool error.
Unlike Pydantic, the invalid object does briefly exist between those two calls, so the
validator call is not optional. A compact constructor that throws closes that gap for
invariants the type must never violate.

**OSGi diagnostic service.** The tool implementation is a DS component holding
`@Reference` injections to exactly the runtime services it needs, and nothing else:

```java
@Component(service = DiagnosticTool.class)
public class BundleStatusTool implements DiagnosticTool<BundleStatusArgs, BundleStatus> {

    private BundleContext bundleContext;

    @Activate
    void activate(BundleContext ctx) { this.bundleContext = ctx; }

    public BundleStatus execute(BundleStatusArgs args) {
        return Arrays.stream(bundleContext.getBundles())
            .filter(b -> args.symbolicName().equals(b.getSymbolicName()))
            .findFirst()
            .map(this::toStatus)
            .orElseThrow(() -> new NoSuchElementException("Bundle not found " + args.symbolicName()));
    }
}
```

`Bundle.getState()` gives the integer constant to map onto the `BundleState` enum. The
unresolved-import list is not on the standard `Bundle` API; it comes from the
`BundleException` message when a start is attempted, or from the framework's resolver
report, which is why the web console and the AEMaaCS Developer Console are the practical
sources for it. Component status comes from `ServiceComponentRuntime`:
`getComponentDescriptionDTOs()` filtered by name, then
`getComponentConfigurationDTOs(...)`, whose `state` and `unsatisfiedReferences` map
directly onto `ComponentStatus`. On AEMaaCS, where there is no Felix console and no JMX,
the same tool would instead call the Developer Console's status-dump endpoints, with the
same `BundleStatus` contract on the way out.

**Structured result → model.** The record is serialized with Jackson and returned as the
`function_call_output` string for the matching `call_id`. Exceptions thrown by the tool
are caught at the dispatcher and serialized as `{"error": ...}`, never propagated to the
request thread and never left as an unanswered `call_id`.

### Why an LLM must not invoke arbitrary OSGi services

The OSGi service registry *is* the platform. `SlingRepository` with a service-user
session, `ResourceResolverFactory`, `Replicator`, `JobManager`, `ConfigurationAdmin`,
`UserManager`, the bundle lifecycle itself. There is no authorization layer between a
`getServiceReference` call and the service: whoever holds a `BundleContext` can obtain
and call anything registered. If a model-produced string selects the service, or the
method, the model has been handed that `BundleContext`. A hallucinated or injected tool
name such as `replicate`, `delete_path`, or `stop_bundle` would be one map miss away
from running with the diagnostic component's service-user permissions, which in practice
are often far broader than "read bundle state".

The allowlisted registry inverts that. The set of things the model can cause to run is
two read-only lookups, declared in source, each with a typed argument DTO and a typed
result. Adding a third tool is a code change with a review, not a new string the model
happened to produce. That is also why the tool contract is narrow on purpose: a tool that
takes a service name and a method name would be a reflection endpoint with extra steps,
and would reintroduce exactly the problem the registry exists to prevent.

The rule generalises past OSGi. Any runtime where a name resolves to executable
capability, a Spring context, a JNDI tree, a REST gateway with a path parameter, has the
same property: the model may *propose* a name, the application *selects* from a closed
set.

## What this becomes next

`runner.py` supports one round trip and raises if the model asks for more. Week 4 turns
that `RuntimeError` into a bounded loop with a step limit and token accounting, and the
"no tool needed" case above becomes the first entry in an evaluation suite that runs it
more than once. The registry, the args models and the error payload do not change. The
loop is built around them.
