from collections.abc import Callable

from pydantic import BaseModel

from contracts import BundleStatusArgs, ComponentStatusArgs
from tools import get_bundle_status, get_component_status

REGISTRY: dict[str, tuple[type[BaseModel], Callable]] = {
    "get_bundle_status": (BundleStatusArgs, get_bundle_status),
    "get_component_status": (ComponentStatusArgs, get_component_status)
}


def dispatch(name: str, arguments: str) -> BaseModel:
    spec = REGISTRY.get(name)
    if spec is None:
        raise KeyError(f"Unknown tool: {name}")
    args_model, func = spec
    args = args_model.model_validate_json(arguments)
    return func(**args.model_dump())
