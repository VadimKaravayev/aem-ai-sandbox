from enum import Enum

from pydantic import BaseModel


class BundleState(str, Enum):
    INSTALLED = "INSTALLED"
    RESOLVED = "RESOLVED"
    ACTIVE = "ACTIVE"

class BundleStatus(BaseModel):
    symbolic_name: str
    state: BundleState
    version: str
    import_problems: list[str]

class ComponentState(str, Enum):
    ACTIVE = "ACTIVE"
    SATISFIED = "SATISFIED"
    UNSATISFIED_REFERENCE = "UNSATISFIED_REFERENCE"

class ComponentStatus(BaseModel):
    name: str
    state: ComponentState
    unsatisfied_references: list[str]


GET_BUNDLE_STATUS_TOOL = {
    "type": "function",
    "name": "get_bundle_status",
    "description": (
        "Look up the runtime status of one OSGI bundle in the AEM instance. "
        "Returns its state (ACTIVE, RESOLVED or INSTALLED), version, and any "
        "unresolved Import-Package problems. Use it when a bundle may not be "
        "running or when a component's dependency may come from a broken bundle"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "symbolic_name": {
                "type": "string",
                "description": "Bundle symbolic name, e.g. com.acme.translation.core"
            }
        },
        "required": ["symbolic_name"],
        "additionalProperties": False,
    },
    "strict": True
}
