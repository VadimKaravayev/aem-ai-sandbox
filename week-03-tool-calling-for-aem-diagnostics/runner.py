from openai import OpenAI

from contracts import GET_BUNDLE_STATUS_TOOL, GET_COMPONENT_STATUS_TOOL
from tool_registry import dispatch

client = OpenAI()

TOOLS = [GET_BUNDLE_STATUS_TOOL, GET_COMPONENT_STATUS_TOOL]

# system prompt
INSTRUCTIONS = (
    "You are an AEM diagnostic assistant. Use the available tools to gather "
    "runtime evidence before answering. Base your answer only on tool results."
)

# user prompt
QUESTION = (
    "Why is com.acme.translation.core not working? Check its bundle and the "
    "translation scheduler component if necessary."
)

input_items = [{"role": "user", "content": QUESTION}]

response = client.responses.create(
    model="gpt-5.6-luna",
    instructions=INSTRUCTIONS,
    input=input_items,
    tools=TOOLS
)

input_items += response.output

for item in response.output:
    if item.type != "function_call":
        continue

    result = dispatch(item.name, item.arguments)

    input_items.append({
        "type": "function_call_output",
        "call_id": item.call_id,
        "output": result.model_dump_json(),
    })

final = client.responses.create(
    model="gpt-5.6-luna",
    instructions=INSTRUCTIONS,
    input=input_items,
    tools=TOOLS
)

if any(item.type == "function_call" for item in final.output):
    raise RuntimeError("Model asked for more tool calls; only one round trip is supported")

print(final.output_text)
