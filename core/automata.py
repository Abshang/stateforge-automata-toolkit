from abc import ABC, abstractmethod
from typing import Set


class Automata(ABC):
    """Abstract base for all finite automata types."""

    def __init__(
        self,
        states: Set[str],
        alphabet: Set[str],
        start: str,
        accept: Set[str],
    ) -> None:
        self.states = states
        self.alphabet = alphabet
        self.start = start
        self.accept = accept
        self._validate()

    def _validate(self) -> None:
        """Check structural consistency of the automaton definition."""
        if not self.states:
            raise ValueError("State set cannot be empty.")
        if not self.alphabet:
            raise ValueError("Alphabet cannot be empty.")
        if self.start not in self.states:
            raise ValueError(f"Start state '{self.start}' is not in states.")
        invalid_accept = self.accept - self.states
        if invalid_accept:
            raise ValueError(f"Accept states not in states: {invalid_accept}")

    @abstractmethod
    def run(self, input_string: str) -> object:
        """Simulate automaton on input_string and return result."""
        pass

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"states={sorted(self.states)}, "
            f"alphabet={sorted(self.alphabet)}, "
            f"start='{self.start}', "
            f"accept={sorted(self.accept)})"
        )