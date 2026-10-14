from pydantic import ValidationError

from runner import ask
from tool_registry import dispatch

def expect(label: str, exc_type: type[Exception], name: str, arguments: str) -> None:
    try:
        dispatch(name, arguments)
    except exc_type as e:
        print(f"[ok] {label}: {type(e).__name__}: {e}")
    else:
        raise AssertionError(f"{label}: expected {exc_type.__name__}, got a result")

expect("unknown tool", KeyError, "restart_bundle", '{"symbolic_name": "com.acme.core"}')
expect("invalid arguments", ValidationError, "get_bundle_status", '{"name": "com.acme.core"}')
expect("tool raises", LookupError, "get_bundle_status", '{"symbolic_name": "com.acme.nonexistent"}')

print("\n--- tool raises, end to end ---")
print(ask("What state is bundle com.acme.nonexistent in?"))

print("\n--- no tool needed ---")
print(ask("What is the difference between an OSGi bundle being INSTALLED and RESOLVED?"))
