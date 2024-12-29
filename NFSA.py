from graphviz import Digraph
import json
# from itertools import product
# from collections import defaultdict, deque
import re


# NSFWSA
class NFSA:
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
            for char, targets in transitions.items():
                for target in targets:
                    cur_edge = (str(state), str(target), char)
                    if cur_edge not in added_edges:
                        if state != target:
                            dot.edge(str(state), str(target), label=char)
                        else:
                            dot.edge(str(state), str(state), label=char)
                        added_edges.add(cur_edge)
        return dot

    # nfsa.json format:
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
    @staticmethod
    def read_json(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return NFSA(
            alphabet=set(data['alphabet']),
            states=set(data['states']),
            start_state=data['start'],
            accepting_states=set(data['accepting']),
            stated_transitions={
                state: {char: list(to_states) for char, to_states in transitions.items()}
                for state, transitions in data['transitions'].items()
            }
        )

    # nfsa.txt format:
    #
    # a, b              ->  alphabet
    # q0, q1, q2        ->  states
    # q0                -> start state
    # q2, q1            -> final states
    # q0, a, q1, q2     ->  transitions from 'q0' with 'a' to 'q1' and 'q2'
    # q0, b, q2         -> etc.
    # q1, a, q2
    # q2, b, q0
    @staticmethod
    def read_txt(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        alphabet = set([c for c in re.split(r'[,\s]+', lines[0]) if c])
        states = set([c for c in re.split(r'[,\s]+', lines[1]) if c])
        start_state = lines[2].strip()
        accepting_states = set([c for c in re.split(r'[,\s]+', lines[3]) if c])
        transitions = {}
        for line in lines[4:]:
            from_state, char, *to_states = [c for c in re.split(r'[,\s]+', line) if c]
            if from_state not in transitions:
                transitions[from_state] = {}
            transitions[from_state][char] = list(to_states)

        # print(alphabet)
        # print(states)
        # print(start_state)
        # print(accepting_states)
        # print(transitions)
        return NFSA(alphabet, states, start_state, accepting_states, transitions)