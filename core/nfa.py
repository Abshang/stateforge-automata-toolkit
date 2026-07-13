from dataclasses import dataclass, field
from typing import Dict, Set
from core.automata import Automata

EPSILON = "ε"


@dataclass
class NFASimulationResult:
    """Result of running a string on the NFA."""
    accepted: bool
    final_states: Set[str]

    def __str__(self) -> str:
        verdict = "ACCEPT" if self.accepted else "REJECT"
        return (
            f"Result       : {verdict}\n"
            f"Final states : {sorted(self.final_states)}"
        )


class NFA(Automata):
    """
    Nondeterministic Finite Automaton.
    transitions[state][symbol] → set of target states.
    Epsilon transitions use the EPSILON constant.
    """

    def __init__(
        self,
        states: Set[str],
        alphabet: Set[str],
        transitions: Dict[str, Dict[str, Set[str]]],
        start: str,
        accept: Set[str],
    ) -> None:
        self.transitions = transitions
        # Pass alphabet without epsilon to base — ε is not a real input symbol
        super().__init__(states, alphabet - {EPSILON}, start, accept)
        self._validate_transitions()

    def _validate_transitions(self) -> None:
        """Check that all states and symbols in the table are declared."""
        for state, mapping in self.transitions.items():
            if state not in self.states:
                raise ValueError(
                    f"Transition table contains undeclared state '{state}'."
                )
            for symbol, targets in mapping.items():
                if symbol != EPSILON and symbol not in self.alphabet:
                    raise ValueError(
                        f"Transition uses undeclared symbol '{symbol}' at state '{state}'."
                    )
                for target in targets:
                    if target not in self.states:
                        raise ValueError(
                            f"Transition δ({state}, {symbol}) → '{target}' is not a valid state."
                        )

    def epsilon_closure(self, states: Set[str]) -> Set[str]:
        """Return all states reachable from given states via ε-transitions only."""
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            for target in self.transitions.get(state, {}).get(EPSILON, set()):
                if target not in closure:
                    closure.add(target)
                    stack.append(target)

        return closure

    def move(self, states: Set[str], symbol: str) -> Set[str]:
        """Return all states reachable from given states on symbol (without ε)."""
        result: Set[str] = set()
        for state in states:
            result |= self.transitions.get(state, {}).get(symbol, set())
        return result

    def run(self, input_string: str) -> NFASimulationResult:
        """
        Simulate NFA on input_string.
        At each step: move on symbol → apply ε-closure.
        Empty current set means no path survives (reject early).
        """
        current = self.epsilon_closure({self.start})

        for symbol in input_string:
            if symbol not in self.alphabet:
                raise ValueError(
                    f"Symbol '{symbol}' is not in the alphabet {self.alphabet}."
                )
            current = self.epsilon_closure(self.move(current, symbol))

            # No active states — no path can lead to accept
            if not current:
                return NFASimulationResult(accepted=False, final_states=set())

        return NFASimulationResult(
            accepted=bool(current & self.accept),
            final_states=current,
        )

    def __repr__(self) -> str:
        return (
            f"NFA(states={sorted(self.states)}, "
            f"alphabet={sorted(self.alphabet)}, "
            f"start='{self.start}', "
            f"accept={sorted(self.accept)})"
        )