import sys
from iohandler.parser import load_dfa, load_nfa
from core.converter import nfa_to_dfa
from core.minimizer import minimize


def run_dfa(path: str, input_string: str) -> None:
    """Load DFA from file and simulate on input_string."""
    dfa = load_dfa(path)
    result = dfa.run(input_string)
    print(f"\nInput  : '{input_string}'")
    print(result)
    print()


def run_nfa(path: str, input_string: str) -> None:
    """Load NFA from file and simulate on input_string."""
    nfa = load_nfa(path)
    result = nfa.run(input_string)
    print(f"\nInput  : '{input_string}'")
    print(result)
    print()


def run_convert(path: str) -> None:
    """Load NFA from file, convert to DFA, and print the result."""
    nfa = load_nfa(path)
    result = nfa_to_dfa(nfa)
    print()
    print(result)
    print()


def run_minimize(path: str) -> None:
    """Load DFA from file, minimize it, and print the result."""
    dfa = load_dfa(path)
    result = minimize(dfa)
    print()
    print(result)
    print()


def _usage() -> None:
    print("Usage:")
    print("  python main.py dfa      <json_path> <input_string>")
    print("  python main.py nfa      <json_path> <input_string>")
    print("  python main.py convert  <nfa_json_path>")
    print("  python main.py minimize <dfa_json_path>")


def main() -> None:
    if len(sys.argv) < 2:
        _usage()
        sys.exit(1)

    mode = sys.argv[1]

    try:
        if mode == "dfa":
            if len(sys.argv) < 4:
                print("Error: 'dfa' mode requires <json_path> and <input_string>.")
                sys.exit(1)
            run_dfa(sys.argv[2], sys.argv[3])

        elif mode == "nfa":
            if len(sys.argv) < 4:
                print("Error: 'nfa' mode requires <json_path> and <input_string>.")
                sys.exit(1)
            run_nfa(sys.argv[2], sys.argv[3])

        elif mode == "convert":
            if len(sys.argv) < 3:
                print("Error: 'convert' mode requires <nfa_json_path>.")
                sys.exit(1)
            run_convert(sys.argv[2])

        elif mode == "minimize":
            if len(sys.argv) < 3:
                print("Error: 'minimize' mode requires <dfa_json_path>.")
                sys.exit(1)
            run_minimize(sys.argv[2])

        else:
            print(f"Unknown mode: '{mode}'.")
            _usage()
            sys.exit(1)

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()