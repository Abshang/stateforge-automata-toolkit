import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, request, jsonify, send_from_directory
from core.dfa import DFA
from core.nfa import NFA
from core.converter import nfa_to_dfa
from core.minimizer import minimize

app = Flask(__name__, static_folder='../ui')


@app.route('/')
def index():
    return send_from_directory('../ui', 'index.html')


@app.route('/api/dfa/simulate', methods=['POST'])
def dfa_simulate():
    try:
        data = request.get_json()
        dfa = DFA(
            states=set(data['states']),
            alphabet=set(data['alphabet']),
            transitions=data['transitions'],
            start=data['start'],
            accept=set(data['accept']),
        )
        result = dfa.run(data['input'])
        return jsonify({
            'accepted': result.accepted,
            'final_state': result.final_state,
            'steps': [
                {'state': s.state, 'symbol': s.symbol, 'next_state': s.next_state}
                for s in result.steps
            ],
        })
    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/nfa/convert', methods=['POST'])
def nfa_convert():
    try:
        data = request.get_json()
        raw = data['transitions']
        transitions = {
            state: {symbol: set(targets) for symbol, targets in mapping.items()}
            for state, mapping in raw.items()
        }
        nfa = NFA(
            states=set(data['states']),
            alphabet=set(data['alphabet']),
            transitions=transitions,
            start=data['start'],
            accept=set(data['accept']),
        )
        result = nfa_to_dfa(nfa)
        dfa = result.dfa
        return jsonify({
            'states': sorted(dfa.states),
            'start': dfa.start,
            'accept': sorted(dfa.accept),
            'alphabet': sorted(dfa.alphabet),
            'transitions': {
                s: {sym: dfa.transitions[s][sym] for sym in sorted(dfa.alphabet)}
                for s in sorted(dfa.states)
            },
            'state_map': {
                name: sorted(subset)
                for name, subset in result.state_map.items()
            },
        })
    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/nfa/simulate', methods=['POST'])
def nfa_simulate():
    try:
        data = request.get_json()
        raw = data['transitions']
        transitions = {
            state: {symbol: set(targets) for symbol, targets in mapping.items()}
            for state, mapping in raw.items()
        }
        nfa = NFA(
            states=set(data['states']),
            alphabet=set(data['alphabet']),
            transitions=transitions,
            start=data['start'],
            accept=set(data['accept']),
        )
        result = nfa.run(data['input'])
        return jsonify({
            'accepted': result.accepted,
            'final_states': sorted(result.final_states),
        })
    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/dfa/minimize', methods=['POST'])
def dfa_minimize():
    try:
        data = request.get_json()
        dfa = DFA(
            states=set(data['states']),
            alphabet=set(data['alphabet']),
            transitions=data['transitions'],
            start=data['start'],
            accept=set(data['accept']),
        )
        result = minimize(dfa)
        mdfa = result.dfa
        return jsonify({
            'original_count': result.original_state_count,
            'minimized_count': len(mdfa.states),
            'states': sorted(mdfa.states),
            'start': mdfa.start,
            'accept': sorted(mdfa.accept),
            'alphabet': sorted(mdfa.alphabet),
            'transitions': {
                s: {sym: mdfa.transitions[s][sym] for sym in sorted(mdfa.alphabet)}
                for s in sorted(mdfa.states)
            },
            'partition_map': result.partition_map,
        })
    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)