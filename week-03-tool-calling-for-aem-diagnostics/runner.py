import json
from openai import OpenAI

from contracts import GET_BUNDLE_STATUS_TOOL, GET_COMPONENT_STATUS_TOOL
from tools import get_bundle_status, get_component_status

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
    args = json.loads(item.arguments)

    if item.name == "get_bundle_status":
        result = get_bundle_status(args["symbolic_name"])
    elif item.name == "get_component_status":
        result = get_component_status(args["component_name"])
    else:
        raise ValueError(f"Unknown tool {item.name}")
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

print(final.output_text)
