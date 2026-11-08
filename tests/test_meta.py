import inspect
from types import SimpleNamespace

import pytest

from solar_park_data.meta import needs_influx


@needs_influx
def direct_decorator(self, value: int = 1) -> str:
    """Function decorated without arguments."""
    return str(value)


@needs_influx()
def empty_parens_decorator(self, value: int = 1) -> str:
    """Function decorated with empty parentheses."""
    return str(value)


@needs_influx(attr="custom_client")
def configured_decorator(self, value: int = 1) -> str:
    """Function decorated with a custom client attribute."""
    return str(value)


@pytest.mark.parametrize(
    "function,name,docstring",
    [
        (
            direct_decorator,
            "direct_decorator",
            "Function decorated without arguments.",
        ),
        (
            empty_parens_decorator,
            "empty_parens_decorator",
            "Function decorated with empty parentheses.",
        ),
        (
            configured_decorator,
            "configured_decorator",
            "Function decorated with a custom client attribute.",
        ),
    ],
)
def test_needs_influx_preserves_function_metadata(function, name, docstring):
    assert function.__name__ == name
    assert function.__doc__ == docstring
    assert function.__annotations__ == {"value": int, "return": str}
    assert str(inspect.signature(function)) == "(self, value: int = 1) -> str"
    assert function.__wrapped__.__name__ == name


@pytest.mark.parametrize(
    "function,client_attribute",
    [
        (direct_decorator, "influx_client"),
        (empty_parens_decorator, "influx_client"),
        (configured_decorator, "custom_client"),
    ],
)
def test_needs_influx_calls_function_when_client_is_set(function, client_attribute):
    instance = SimpleNamespace(**{client_attribute: object()})

    assert function(instance, 42) == "42"


def test_needs_influx_rejects_missing_client():
    with pytest.raises(RuntimeError, match="influx client not set"):
        direct_decorator(SimpleNamespace())
