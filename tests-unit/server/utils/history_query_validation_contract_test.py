from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
HELPER = ROOT / "api_server" / "utils" / "query_params.py"
SERVER = ROOT / "server.py"


def test_history_query_parser_rejects_invalid_integer_values() -> None:
    assert HELPER.exists(), "history query parser helper is not implemented"
    spec = importlib.util.spec_from_file_location("history_query_params", HELPER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    with pytest.raises(ValueError, match="max_items must be an integer"):
        module.parse_optional_int_query_param(
            {"max_items": "not-an-integer"}, "max_items"
        )


def test_history_route_converts_invalid_query_values_to_http_400() -> None:
    source = SERVER.read_text(encoding="utf-8")

    assert 'parse_optional_int_query_param(query, "max_items")' in source
    assert 'parse_optional_int_query_param(query, "offset")' in source
    assert 'except ValueError as exc:' in source
    assert 'web.json_response({"error": str(exc)}, status=400)' in source
