import json

from openai.lib._pydantic import to_strict_json_schema

from contracts import AemDiagnostic

print(json.dumps(to_strict_json_schema(AemDiagnostic), indent=2))
