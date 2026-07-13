from dataclasses import dataclass, field
from typing import Dict, FrozenSet, Set
from core.nfa import NFA
from core.dfa import DFA


@dataclass
class ConversionResult:
    """
    Holds the converted DFA and the mapping used to build it.
    state_map: frozenset of NFA states → DFA state name.
    Useful for tracing which DFA state came from which NFA states.
    """
    dfa: DFA
    state_map: Dict[str, FrozenSet[str]] = field(default_factory=dict)

    def __str__(self) -> str:
        lines = ["=== NFA → DFA Conversion ==="]
        lines.append(f"DFA start  : {self.dfa.start}")
        lines.append(f"DFA accept : {sorted(self.dfa.accept)}")
        lines.append("\nState mapping (DFA ← NFA subsets):")
        for name, subset in sorted(self.state_map.items()):
            marker = " *" if name in self.dfa.accept else ""
            lines.append(f"  {name:<30} ← {sorted(subset)}{marker}")
        lines.append("\nTransition table:")
        symbols = sorted(self.dfa.alphabet)
        header = f"  {'State':<30}" + "".join(f"{s:<20}" for s in symbols)
        lines.append(header)
        lines.append("  " + "-" * (len(header) - 2))
        for state in sorted(self.dfa.states):
            row = f"  {state:<30}"
            for symbol in symbols:
                row += f"{self.dfa.transitions[state][symbol]:<20}"
            lines.append(row)
        return "\n".join(lines)


def nfa_to_dfa(nfa: NFA) -> ConversionResult:
    """
    Convert NFA to equivalent DFA using Subset Construction.
    Each DFA state is a frozenset of NFA states (a subset of Q).
    Dead state (∅) is added only when reachable.
    """
    start_closure = frozenset(nfa.epsilon_closure({nfa.start}))

    # frozenset of NFA states → DFA state label
    subset_to_name: Dict[FrozenSet[str], str] = {start_closure: _label(start_closure)}
    dfa_transitions: Dict[str, Dict[str, str]] = {}

    unprocessed = [start_closure]

    while unprocessed:
        current_subset = unprocessed.pop()
        current_name = subset_to_name[current_subset]
        dfa_transitions[current_name] = {}

        for symbol in sorted(nfa.alphabet):
            next_subset = frozenset(
                nfa.epsilon_closure(nfa.move(set(current_subset), symbol))
            )

            if next_subset not in subset_to_name:
                subset_to_name[next_subset] = _label(next_subset)
                unprocessed.append(next_subset)

            dfa_transitions[current_name][symbol] = subset_to_name[next_subset]

    dfa_states = set(subset_to_name.values())
    dfa_start = subset_to_name[start_closure]

    # DFA state is accepting if it contains at least one NFA accept state
    dfa_accept = {
        name
        for subset, name in subset_to_name.items()
        if subset & nfa.accept
    }

    dfa = DFA(
        states=dfa_states,
        alphabet=set(nfa.alphabet),
        transitions=dfa_transitions,
        start=dfa_start,
        accept=dfa_accept,
    )

    # Invert map: DFA name → NFA subset (for ConversionResult)
    name_to_subset = {name: subset for subset, name in subset_to_name.items()}

    return ConversionResult(dfa=dfa, state_map=name_to_subset)


def _label(state_set: FrozenSet[str]) -> str:
    """Readable label for a DFA state derived from a subset of NFA states."""
    if not state_set:
        return "∅"
    return "{" + ",".join(sorted(state_set)) + "}"