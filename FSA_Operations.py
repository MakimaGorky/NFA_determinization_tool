from NFSA import *
from DFSA import *
from collections import deque


class FSA_Operations:
    @staticmethod
    def determinization(nfa):
        """Классический алгоритм детерминизации НКА."""

        # for reasons 🙄🙄🙄
        def frozenset_to_name(frznst):
            return ''.join(elem for elem in sorted(frznst))

        start_state = frozenset([nfa.start_state])
        start_state_ind = frozenset_to_name(start_state)  # for reasons

        dfa_states = set()
        dfa_transitions = {}
        dfa_accepting_states = set()

        queue = deque([start_state])
        dfa_states.add(start_state_ind)

        while queue:
            current_state = queue.popleft()
            current_state_ind = frozenset_to_name(current_state)
            dfa_transitions[current_state_ind] = {}

            # State acceptance handling
            if any(state in nfa.accepting_states for state in current_state):
                dfa_accepting_states.add(current_state_ind)

            for symbol in nfa.alphabet:
                next_state = set()

                # 🍔                                         ⚾        🦅           🍟
                # 🍔          🎢🤠🧤                                   💰     💵    🍟
                # United States of Current State 🏈 👋 🤠 👉 {🍔🍟🥤} 🌎    🗽 🗽   🍟
                for nfa_state in current_state:
                    if symbol in nfa.stated_transitions[nfa_state]: #nfa.stated_transitions.get(nfa_state, {}):
                        # next_state.update(transitions[nfa_state])
                        next_state.update(nfa.stated_transitions.get(nfa_state, {}).get(symbol, set()))

                next_state = frozenset(next_state)
                next_state_ind = frozenset_to_name(next_state)

                # enqueueng
                if next_state_ind not in dfa_states and len(next_state) != 0:
                    dfa_states.add(next_state_ind)
                    if next_state != current_state:
                        queue.append(next_state)

                if len(next_state) != 0:
                    dfa_transitions[current_state_ind][symbol] = next_state_ind
        # print(dfa_transitions)
        return DFSA(nfa.alphabet, dfa_states, start_state_ind, dfa_accepting_states, dfa_transitions)