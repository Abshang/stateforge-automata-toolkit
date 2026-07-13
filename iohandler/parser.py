import json
from pathlib import Path
from typing import Any, Dict
from core.dfa import DFA
from core.nfa import NFA
from io.validator import validate_dfa, validate_nfa


def load_dfa(path: str) -> DFA:
    """Load, validate, and parse a DFA from a JSON file."""
    data = _load_json(path)
    validate_dfa(data)
    return _parse_dfa(data)


def load_nfa(path: str) -> NFA:
    """Load, validate, and parse an NFA from a JSON file."""
    data = _load_json(path)
    validate_nfa(data)
    return _parse_nfa(data)


def _load_json(path: str) -> Dict[str, Any]:
    """Read and decode a JSON file. Raises clear errors on missing or malformed files."""
    file = Path(path)
    if not file.exists():
        raise FileNotFoundError(f"File not found: '{path}'.")
    try:
        with file.open(encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in '{path}': {e}.")


def _parse_dfa(data: Dict[str, Any]) -> DFA:
    """Build a DFA object from a validated JSON dict."""
    return DFA(
        states=set(data["states"]),
        alphabet=set(data["alphabet"]),
        transitions={
            state: dict(mapping)
            for state, mapping in data["transitions"].items()
        },
        start=data["start"],
        accept=set(data["accept"]),
    )


def _parse_nfa(data: Dict[str, Any]) -> NFA:
    """Build an NFA object from a validated JSON dict."""
    transitions: Dict[str, Dict[str, set]] = {}
    for state, mapping in data["transitions"].items():
        transitions[state] = {
            symbol: set(targets)
            for symbol, targets in mapping.items()
        }
    return NFA(
        states=set(data["states"]),
        alphabet=set(data["alphabet"]),
        transitions=transitions,
        start=data["start"],
        accept=set(data["accept"]),
    )