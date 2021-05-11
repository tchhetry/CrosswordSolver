import os
import sys
from datetime import datetime 
import numpy as np

from samplePuzzle import SampleCrossword, SampleCrosswordTxt
from Parser import Parser
from solver 

def run_dfsb(file, debug):
    solver.exploredCount = 0
    crossword = SampleCrosswordTxt(file)
    hints = [word.clue for word in crossword.word_list]
    word_ass = [None for i in range(len(hints))]
    word_domains = [word.domain for word in crossword.word_list]
    cons = crossword.constraints

    arclist = []
    for i in range(len(cons)):
        print(f"cons at {i}: {cons[i]}")
        for j in cons[i]:
            arclist.append((j[1], j[0]))
    print("arclist: ", arclist)

    for i in range(len(cons)):
        print(f"{i}: {hints[i]}, \t{word_domains[i]}, \t{cons[i]}")
    start_time = datetime.now()
    solution = solver.improved_DFSB(word_ass, cons, word_domains, arclist, debug)
    time_elapsed = datetime.now() - start_time
    print("solution: ", solution)

    return solution, time_elapsed, solver.exploredCount

if __name__ == '__main__':
    print("----- starting compute performance table. ----- \n")

    simpleP_list = os.listdir(path="simpleP")
    puzzle_list = os.listdir(path="puzzles")

    print(simpleP_list, puzzle_list)

    state, time = [], []
    for s in simpleP_list:
        path = "simpleP" + s
        sol, time, state = run_dfsb(path)
        state.append(solver.exploredCount)
        time.append(float(time.total_seconds()))