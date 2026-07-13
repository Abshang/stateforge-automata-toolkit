# StateForge

A modular Python toolkit for simulating, converting, and minimizing finite automata.

StateForge supports DFA and NFA simulation, epsilon transitions, NFA-to-DFA conversion, DFA minimization, command-line execution, and an interactive web interface.

## Features

* DFA simulation with step-by-step execution trace
* NFA simulation with epsilon-closure support
* NFA to DFA conversion using Subset Construction
* DFA minimization using Hopcroft’s algorithm
* JSON-based automata definitions
* Input validation with readable error messages
* Command-line interface
* Flask REST API
* Interactive web interface
* Example DFA and NFA definitions

## Project Structure

```text
stateforge-automata-toolkit/
├── core/
│   ├── automata.py
│   ├── dfa.py
│   ├── nfa.py
│   ├── converter.py
│   └── minimizer.py
├── iohandler/
│   ├── parser.py
│   └── validator.py
├── api/
│   └── app.py
├── ui/
│   └── index.html
├── examples/
├── main.py
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/Abshang/stateforge-automata-toolkit.git
cd stateforge-automata-toolkit
pip install -r requirements.txt
```

## Command-Line Usage

### Simulate a DFA

```bash
python main.py dfa examples/dfa_ends_with_ab.json abab
```

### Simulate an NFA

```bash
python main.py nfa examples/nfa_starts_a_or_ends_b.json aba
```

### Convert an NFA to a DFA

```bash
python main.py convert examples/nfa_epsilon_even_a_or_even_b.json
```

### Minimize a DFA

```bash
python main.py minimize examples/dfa_ends_with_ab.json
```

## Web Interface

Start the Flask application:

```bash
python api/app.py
```

Then open:

```text
http://localhost:5000
```

The web interface provides four main tools:

* DFA Simulator
* NFA Simulator
* NFA to DFA Converter
* DFA Minimizer

## Algorithms

| Operation        | Algorithm                                  | Complexity   |   |    |   |    |
| ---------------- | ------------------------------------------ | ------------ | - | -- | - | -- |
| DFA Simulation   | Direct transition processing               | `O(          | w | )` |   |    |
| NFA Simulation   | Active-state tracking with epsilon closure | `O(          | w | ×  | Q | )` |
| NFA to DFA       | Subset Construction                        | `O(2^        | Q | ×  | Σ | )` |
| DFA Minimization | Hopcroft’s Algorithm                       | `O(n log n × | Σ | )` |   |    |

## Technologies

* Python 3
* Flask
* HTML
* CSS
* JavaScript
* JSON

## Academic Context

Developed as a course project for **Foundations of Computation Theory** at Ferdowsi University of Mashhad.

**Instructor:** Dr. Tabasi

**Team Members:**

* Fatemeh Abshang
* Parsa Daroudi

**Semester:** Spring 1404
