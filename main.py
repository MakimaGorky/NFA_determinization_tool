from App import *

# ind = 1
# nfa_1 = NFSA.read_txt('nfa/nfa_0.txt')
# nfa_2 = Demo.nfa_example_3
#
#
# dot = nfa_1.visualize()
# dot.render(f'NFA_1{ind}', format='png', cleanup=True)
#
# dot = nfa_2.visualize()
# dot.render(f'NFA_2{ind}', format='png', cleanup=True)
#
#
# dfa_1_result = FSA_Operations.determinization(nfa_1)
#
# dfa_2_result = FSA_Operations.determinization(nfa_2)
#
#
# dfa_1_result.write_txt(f'dfa_1{ind}.txt')
# dfa_2_result.write_json(f'dfa_2{ind}.json')
#
# dot = dfa_1_result.visualize()
# dot.render(f'DFA_1{ind}', format='png', cleanup=True)
#
# dot = dfa_2_result.visualize()
# dot.render(f'DFA_2{ind}', format='png', cleanup=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = AutomataApp(root)
    root.mainloop()
