from NFSA import *
from DFSA import *

nfa_example_1 = NFSA(
            {'0', '1'},
            {'A', 'B'},
            'A',
            {'B'},
            {
                'A': {'0': ['A', 'B']},
                'B': {'1': ['B']}
            }
        )
nfa_example_2 = NFSA(
            {'a', 'b'},
            {'s0', 's1', 's2'},
            's0',
            {'s2'},
            {
                's0': {'a': ['s0', 's1'], 'b': ['s0']},
                's1': {'a': ['s2']},
                's2': {'b': ['s2']},
            }
        )

nfa_example_3 = NFSA(
            {'0', '1', '2'},
            {'state1', 'state2', 'state3'},
            'state1',
            {'state2'},
            {
                'state1': {'1': ['state2', 'state3']},
                'state2': {'2': ['state2', 'state3']},
                'state3': {'0': ['state3', 'state1']},
            }
        )