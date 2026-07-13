from dataclasses import dataclass, field
from typing import Dict, List, Set
from core.automata import Automata


@dataclass
class SimulationStep:
    """Single transition step during DFA execution."""
    state: str
    symbol: str
    next_state: str


@dataclass
class SimulationResult:
    """Complete result of running a string on the DFA."""
    accepted: bool
    final_state: str
    steps: List[SimulationStep] = field(default_factory=list)

    def __str__(self) -> str:
        verdict = "ACCEPT" if self.accepted else "REJECT"
        lines = [f"Result : {verdict}", f"Final  : {self.final_state}", "Trace  :"]
        if self.steps:
            for s in self.steps:
                lines.append(f"  δ({s.state}, {s.symbol}) → {s.next_state}")
        else:
            lines.append("  (empty string — no transitions taken)")
        return "\n".join(lines)


class DFA(Automata):
    """Deterministic Finite Automaton."""

    def __init__(
        self,
        states: Set[str],
        alphabet: Set[str],
        transitions: Dict[str, Dict[str, str]],
        start: str,
        accept: Set[str],
    ) -> None:
        self.transitions = transitions
        super().__init__(states, alphabet, start, accept)
        self._validate_transitions()

    def _validate_transitions(self) -> None:
        """
        Ensure transition function is total:
        every (state, symbol) pair must have exactly one target in states.
        """
        for state in self.states:
            for symbol in self.alphabet:
                target = self.transitions.get(state, {}).get(symbol)
                if target is None:
                    raise ValueError(
                        f"Missing transition: δ({state}, {symbol}) is undefined."
                    )
                if target not in self.states:
                    raise ValueError(
                        f"δ({state}, {symbol}) → '{target}' is not a valid state."
                    )

        # Catch states in transition table that are not declared
        for state, mapping in self.transitions.items():
            if state not in self.states:
                raise ValueError(
                    f"Transition table contains undeclared state '{state}'."
                )

    def step(self, state: str, symbol: str) -> str:
        """Return next state for a given (state, symbol) pair."""
        return self.transitions[state][symbol]

    def run(self, input_string: str) -> SimulationResult:
        """
        Simulate DFA on input_string left to right.
        Empty string is valid — stays at start state.
        """
        current = self.start
        steps: List[SimulationStep] = []

        for symbol in input_string:
            if symbol not in self.alphabet:
                raise ValueError(
                    f"Symbol '{symbol}' is not in the alphabet {self.alphabet}."
                )
            next_state = self.step(current, symbol)
            steps.append(SimulationStep(current, symbol, next_state))
            current = next_state

        return SimulationResult(
            accepted=current in self.accept,
            final_state=current,
            steps=steps,
        )

    def __repr__(self) -> str:
        return (
            f"DFA(states={sorted(self.states)}, "
            f"alphabet={sorted(self.alphabet)}, "
            f"start='{self.start}', "
            f"accept={sorted(self.accept)}, "
            f"transitions={self.transitions})"
        )