from enum import Enum

from openai.types.responses import FunctionToolParam
from pydantic import BaseModel, ConfigDict, Field


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

class BundleStatusArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    symbolic_name: str = Field(description="Bundle symbolic name, e.g. com.acme.translation.core")

class ComponentStatusArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    component_name: str = Field(description="Fully qualified DS component name, e.g. 'com.acme.translation.core.scheduler.TranslationSchedulerJob'")

GET_BUNDLE_STATUS_TOOL: FunctionToolParam = {
    "type": "function",
    "name": "get_bundle_status",
    "description": (
        "Look up the runtime status of one OSGi bundle in the AEM instance. "
        "Returns its state (ACTIVE, RESOLVED or INSTALLED), version, and any "
        "unresolved Import-Package problems. Use it when a bundle may not be "
        "running or when a component's dependency may come from a broken bundle"
    ),
    "parameters": BundleStatusArgs.model_json_schema(),
    "strict": True
}

GET_COMPONENT_STATUS_TOOL: FunctionToolParam = {
    "type": "function",
    "name": "get_component_status",
    "description": (
        "Look up the runtime status of one OSGi Declarative Services (DS) component "
        "in the AEM instance. Returns its state (ACTIVE, SATISFIED or "
        "UNSATISFIED_REFERENCE) and the list of references it cannot satisfy. "
        "Use it when a service is missing, a job is not running, or a component "
        "is reported as unsatisfied, even if its bundle is ACTIVE."
    ),
    "parameters": ComponentStatusArgs.model_json_schema(),
    "strict": True
}
