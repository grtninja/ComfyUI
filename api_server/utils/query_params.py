"""Helpers for validating optional HTTP query parameters."""

from collections.abc import Mapping


def parse_optional_int_query_param(
    query: Mapping[str, str], name: str
) -> int | None:
    """Return an optional integer query value or raise a stable validation error."""

    value = query.get(name)
    if value is None:
        return None

    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be an integer") from exc
