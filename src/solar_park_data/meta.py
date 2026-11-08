from __future__ import annotations

import functools
from typing import Any, Callable, TypeVar, cast, overload

F = TypeVar("F", bound=Callable[..., Any])


def needs_client(name: str, attr: str) -> Callable[[F], F]:
    def decorator(f: F) -> F:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            self = args[0]
            client = getattr(self, attr, None)
            if client is None:
                raise RuntimeError(f"{name} client not set")
            return f(*args, **kwargs)

        return cast(F, wrapper)

    return decorator


@overload
def needs_influx(f: F, /, *, attr: str = "influx_client") -> F: ...


@overload
def needs_influx(
    f: None = None, /, *, attr: str = "influx_client"
) -> Callable[[F], F]: ...


def needs_influx(
    f: F | None = None, /, *, attr: str = "influx_client"
) -> F | Callable[[F], F]:
    decorator = needs_client("influx", attr)

    if f is None:
        return decorator

    return decorator(f)


@overload
def needs_s3(f: F, /, *, attr: str = "s3_client") -> F: ...


@overload
def needs_s3(f: None = None, /, *, attr: str = "aws_client") -> Callable[[F], F]: ...


def needs_s3(f: F | None = None, /, *, attr: str = "s3_client") -> F | Callable[[F], F]:
    decorator = needs_client("s3", attr)

    if f is None:
        return decorator

    return decorator(f)
