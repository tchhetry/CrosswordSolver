import os
import sys
from datetime import datetime 
import numpy as np

from samplePuzzle import SampleCrossword, SampleCrosswordTxt
from Parser import Parser
import solver 

def run_dfsb(crossword, debug):
    solver.exploredCount = 0

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

def run_files(file_list, prePath, type):
    solution, state, time = [], [], []
    for s in file_list:
        path = prePath + s
        cw = SampleCrosswordTxt(path) if type=="txt" else Parser().parse(path)
        sol, time, state = run_dfsb(cw)
        solution.append(0 if sol==False else 1)
        state.append(solver.exploredCount)
        time.append(float(time.total_seconds()))
    solution, state, time = np.array(solution), np.array(state), np.array(time)
    stateM, stateSD, timeM, timeSD = np.mean(state), np.std(state), np.mean(time), np.std(time)
    print("improved DFS-B on {}: # of states explored: {} +- {}, time: {} +- {}. \n".format(path, stateM, 
            stateSD, timeM, timeSD))
    print(f"\t solution: {solution}")


if __name__ == '__main__':
    print("----- starting compute performance table. ----- \n")

    simpleP_list = os.listdir(path="simpleP")
    puzzle_list = os.listdir(path="puzzles")

    print(simpleP_list, puzzle_list)

    run_files(file_list=simpleP_list, prePath="simpleP", type="txt")
    run_files(file_list=puzzle_list, prePath="puzzles", type="puz")

