import json
from openai import OpenAI

from contracts import GET_BUNDLE_STATUS_TOOL, GET_COMPONENT_STATUS_TOOL
from tool_registry import dispatch

client = OpenAI()

TOOLS = [GET_BUNDLE_STATUS_TOOL, GET_COMPONENT_STATUS_TOOL]

# system prompt
INSTRUCTIONS = (
    "You are an AEM diagnostic assistant. When the question concerns the runtime "
    "state of a specific bundle or component, use the available tools and base "
    "your answer only on their results. For general or conceptual questions, "
    "answer directly from your knowledge without calling any tool."
)

# user prompt
QUESTION = (
    "Why is com.acme.translation.core not working? Check its bundle and the "
    "translation scheduler component if necessary."
)

def ask(question: str) -> str:
    input_items = [{"role": "user", "content": question}]

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
        print(f"[tool] {item.name}({item.arguments})")
        try:
            output = dispatch(item.name, item.arguments).model_dump_json()
        except Exception as e:
            output = json.dumps({"error": f"{type(e).__name__}: {e}"})

        input_items.append({
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": output,
        })

    final = client.responses.create(
        model="gpt-5.6-luna",
        instructions=INSTRUCTIONS,
        input=input_items,
        tools=TOOLS
    )

    if any(item.type == "function_call" for item in final.output):
        raise RuntimeError("Model asked for more tool calls; only one round trip is supported")

    return final.output_text


if __name__ == "__main__":
    print(ask(QUESTION))
