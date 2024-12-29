from graphviz import Digraph
import json
# from itertools import product
# from collections import defaultdict, deque
# import re


# TODO исправить ошибки в сохранении автомата
class DFSA:
    def __init__(self, alphabet={}, states={'0'}, start_state='0', accepting_states={'0'}, stated_transitions={}):
        self.states = states
        self.stated_transitions = stated_transitions  # {from_state: {char: to_states={}}} - Состояния с переходами
        self.start_state = start_state  # Начальное состояние
        self.accepting_states = accepting_states  # set Набор принимающих состояний
        self.alphabet = alphabet  # set

    def visualize(self):
        dot = Digraph()
        # Костыль для исправления фантомного бага
        added_edges = set()
        # Все узлы
        for state in self.stated_transitions.keys():
            cur_shape = "doublecircle" if state in self.accepting_states else "circle"
            dot.node(str(state), shape=cur_shape)

        # Указатель на стартовое
        dot.node('start', shape='none')
        dot.edge('start', str(self.start_state))

        for state, transitions in self.stated_transitions.items():
            for char, target in transitions.items():
                cur_edge = (str(state), str(target), char)
                if cur_edge not in added_edges:
                    dot.edge(str(state), str(target), label=char)
                    added_edges.add(cur_edge)
        return dot

    # dfsa.txt output format:
    #
    # a, b              ->  alphabet
    # q0, q1, q2        ->  states
    # q0                -> start state
    # q2, q1            -> final states
    # q0, a, q1         ->  transitions from 'q0' with 'a' to 'q1'
    # q0, b, q2         -> etc.
    # q1, a, q2
    # q2, b, q0
    def write_txt(self, file_path):
        with open(file_path, 'w') as file:
            file.write(','.join(self.alphabet) + '\n')
            file.write(','.join(self.states) + '\n')
            file.write(self.start_state + '\n')
            file.write(','.join(self.accepting_states) + '\n')
            print(self.stated_transitions)
            for from_state, transitions in self.stated_transitions.items():
                for char, to_states in transitions.items():
                    file.write(f"{from_state},{char},{to_states}\n")

    # dfsa.json output format:
    #
    # {
    #     "states": ["q0", "q1", "q2"],
    #     "alphabet": ["a", "b"],
    #     "start": "q0",
    #     "accepting": ["q2"],
    #     "transitions": {
    #         "q0": {
    #             "a": ["q1"],
    #             "b": ["q2"]
    #         },
    #         "q1": {
    #             "a": ["q2"]
    #         },
    #         "q2": {
    #             "b": ["q0"]
    #         }
    #     }
    # }
    def write_json(self, file_path):
        # print(self.stated_transitions)
        with open(file_path, 'w') as file:
            json.dump({
                'alphabet': list(self.alphabet),
                'states': list(self.states),
                'start': self.start_state,
                'accepting': list(self.accepting_states),
                'transitions': {
                    state: {char: [to_states] for char, to_states in transitions.items()}
                    for state, transitions in self.stated_transitions.items()
                }
            }, file, indent=4
            )