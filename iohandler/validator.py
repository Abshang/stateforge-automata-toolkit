from typing import Any, Dict

_DFA_FIELDS = {"states", "alphabet", "start", "accept", "transitions"}
_NFA_FIELDS = {"states", "alphabet", "start", "accept", "transitions"}


def validate_dfa(data: Any) -> None:
    """
    Validate raw JSON dict for DFA before parsing.
    Raises ValueError with a clear message on any structural issue.
    """
    _check_type(data, dict, "DFA definition")
    _check_required_fields(data, _DFA_FIELDS)

    _check_non_empty_list(data["states"], "states")
    _check_non_empty_list(data["alphabet"], "alphabet")
    _check_string(data["start"], "start")
    _check_list_of_strings(data["states"], "states")
    _check_list_of_strings(data["alphabet"], "alphabet")
    _check_list_of_strings(data["accept"], "accept")
    _check_type(data["transitions"], dict, "transitions")

    for state, mapping in data["transitions"].items():
        _check_type(mapping, dict, f"transitions['{state}']")
        for symbol, target in mapping.items():
            if not isinstance(target, str):
                raise ValueError(
                    f"DFA transition δ({state}, {symbol}) must be a string, got {type(target).__name__}."
                )


def validate_nfa(data: Any) -> None:
    """
    Validate raw JSON dict for NFA before parsing.
    Raises ValueError with a clear message on any structural issue.
    """
    _check_type(data, dict, "NFA definition")
    _check_required_fields(data, _NFA_FIELDS)

    _check_non_empty_list(data["states"], "states")
    _check_non_empty_list(data["alphabet"], "alphabet")
    _check_string(data["start"], "start")
    _check_list_of_strings(data["states"], "states")
    _check_list_of_strings(data["alphabet"], "alphabet")
    _check_list_of_strings(data["accept"], "accept")
    _check_type(data["transitions"], dict, "transitions")

    for state, mapping in data["transitions"].items():
        _check_type(mapping, dict, f"transitions['{state}']")
        for symbol, targets in mapping.items():
            if not isinstance(targets, list):
                raise ValueError(
                    f"NFA transition δ({state}, {symbol}) must be a list, got {type(targets).__name__}."
                )
            for t in targets:
                if not isinstance(t, str):
                    raise ValueError(
                        f"NFA transition δ({state}, {symbol}) contains non-string target: {t!r}."
                    )


def _check_type(value: Any, expected: type, field: str) -> None:
    if not isinstance(value, expected):
        raise ValueError(
            f"'{field}' must be {expected.__name__}, got {type(value).__name__}."
        )


def _check_required_fields(data: Dict, fields: set) -> None:
    missing = fields - data.keys()
    if missing:
        raise ValueError(f"Missing required fields: {sorted(missing)}.")


def _check_string(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"'{field}' must be a non-empty string.")


def _check_non_empty_list(value: Any, field: str) -> None:
    if not isinstance(value, list) or len(value) == 0:
        raise ValueError(f"'{field}' must be a non-empty list.")


def _check_list_of_strings(value: list, field: str) -> None:
    for item in value:
        if not isinstance(item, str):
            raise ValueError(
                f"'{field}' must contain only strings, got {type(item).__name__}: {item!r}."
            )