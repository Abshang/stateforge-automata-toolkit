from dataclasses import dataclass, field
from typing import Dict, FrozenSet, List, Set
from core.dfa import DFA


@dataclass
class MinimizationResult:
    """
    Holds the minimized DFA and partition info for tracing.
    partition_map: original state → minimized state name.
    """
    dfa: DFA
    partition_map: Dict[str, str] = field(default_factory=dict)
    original_state_count: int = 0

    def __str__(self) -> str:
        reduced = len(set(self.partition_map.values()))
        lines = [
            "=== DFA Minimization (Hopcroft's Algorithm) ===",
            f"States before : {self.original_state_count}",
            f"States after  : {reduced}",
            "",
            "State merges (original → minimized):",
        ]
        for original, minimized in sorted(self.partition_map.items()):
            marker = " *" if minimized in self.dfa.accept else ""
            lines.append(f"  {original:<15} → {minimized}{marker}")
        lines.append("")
        lines.append("Minimized transition table:")
        symbols = sorted(self.dfa.alphabet)
        header = f"  {'State':<20}" + "".join(f"{s:<15}" for s in symbols)
        lines.append(header)
        lines.append("  " + "-" * (len(header) - 2))
        for state in sorted(self.dfa.states):
            row = f"  {state:<20}"
            for symbol in symbols:
                row += f"{self.dfa.transitions[state][symbol]:<15}"
            lines.append(row)
        return "\n".join(lines)


def minimize(dfa: DFA) -> MinimizationResult:
    """
    Minimize a DFA using Hopcroft's algorithm.
    Unreachable states are removed before partitioning.
    """
    reachable = _reachable_states(dfa)
    accept = dfa.accept & reachable
    non_accept = reachable - accept

    # Initial partition: accept vs non-accept
    # Filter out empty sets — e.g. if all states are accepting
    partitions: List[FrozenSet[str]] = [
        p for p in [frozenset(accept), frozenset(non_accept)] if p
    ]
    worklist: List[FrozenSet[str]] = list(partitions)

    while worklist:
        splitter = worklist.pop()

        for symbol in dfa.alphabet:
            # States that transition into the splitter on this symbol
            predecessors = frozenset(
                s for s in reachable
                if dfa.transitions[s][symbol] in splitter
            )

            next_partitions: List[FrozenSet[str]] = []
            for group in partitions:
                inside = group & predecessors
                outside = group - predecessors

                if inside and outside:
                    # This group is split by the splitter
                    next_partitions.extend([inside, outside])
                    if group in worklist:
                        worklist.remove(group)
                        worklist.extend([inside, outside])
                    else:
                        # Add the smaller half to worklist (Hopcroft's optimization)
                        worklist.append(inside if len(inside) <= len(outside) else outside)
                else:
                    next_partitions.append(group)

            partitions = next_partitions

    return _build_minimized_dfa(dfa, partitions)


def _reachable_states(dfa: DFA) -> Set[str]:
    """BFS from start state to find all reachable states."""
    visited: Set[str] = set()
    queue = [dfa.start]

    while queue:
        state = queue.pop()
        if state in visited:
            continue
        visited.add(state)
        for symbol in dfa.alphabet:
            queue.append(dfa.transitions[state][symbol])

    return visited


def _build_minimized_dfa(
    dfa: DFA,
    partitions: List[FrozenSet[str]],
) -> MinimizationResult:
    """Build a new DFA from the final partitions."""

    # Map each original state to its partition representative (sorted first element)
    state_to_rep: Dict[str, str] = {}
    for group in partitions:
        rep = sorted(group)[0]
        for state in group:
            state_to_rep[state] = rep

    new_states = set(state_to_rep.values())
    new_start = state_to_rep[dfa.start]
    new_accept = {state_to_rep[s] for s in dfa.accept if s in state_to_rep}

    new_transitions: Dict[str, Dict[str, str]] = {}
    for group in partitions:
        rep = state_to_rep[sorted(group)[0]]
        new_transitions[rep] = {}
        for symbol in dfa.alphabet:
            target = dfa.transitions[rep][symbol]
            new_transitions[rep][symbol] = state_to_rep[target]

    minimized = DFA(
        states=new_states,
        alphabet=set(dfa.alphabet),
        transitions=new_transitions,
        start=new_start,
        accept=new_accept,
    )

    return MinimizationResult(
        dfa=minimized,
        partition_map=state_to_rep,
        original_state_count=len(dfa.states),
    )