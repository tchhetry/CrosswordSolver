'''
This files takes in a .puz file and MODE flag 
FORMAT python solver.py <input_file> <output_file> <mode> 
'''

from samplePuzzle import SampleCrossword, SampleCrosswordTxt
import sys
from datetime import datetime
from queue import PriorityQueue
from collections import deque
import copy
import random

from Parser import Parser

# This should run in two modes. a) Plain DFS-B and
#   b) DFS-B with variable, value ordering + AC3 for constraint propagation.

exploredCount = 0  # global counter for explored states

# Plain DFS-B


def DFSB(assignment, constraints, domains, debug):
    print("\nCurrent assignment: ", assignment)
    # if assignment is complete, return the assignment
    if None not in assignment:
        return assignment
    global exploredCount  # global counter for explored states
    exploredCount += 1
    # select first unassigned variable
    var = assignment.index(None)
    if debug:
        print("var", var)
    # for each value in domain of selected variable
    for v in domains[var]:
        # if value is consistent with problem constraints
        # if v not in [ assignment[i] for i in constraints[var] ]:
        consistent = True
        for i in constraints[var]:
            [pos, ind], [pos2, ind2] = i
            if debug:
                print(i, pos, ind, pos2, ind2,
                      assignment[pos], assignment[pos2], v)
            if assignment[pos] != None and v != None:
                if assignment[pos][ind] != v[ind2]:
                    consistent = False
                break
        if debug:
            print(f"For v = {v}, consistent: {consistent}")
        if consistent:
            # add var=value to assignment, call DFSB on given assignment
            assignment[var] = v
            res = DFSB(assignment, constraints, domains)
            # if result is not false, return result
            if res != False:
                return res
            # otherwise remove var=value from assignment
            if debug:
                print(f"recover from assignment[{var}]={assignment[var]}")
            assignment[var] = None
    return False


def AC3(cons, doms, arcl, debug):
    if debug:
        print("\nAC3: doms:{}, cons: {}".format(doms, cons))
    # initilize arc Queue, contains all arcs in csp
    arcQ = deque(arcl)
    # while arc Queue is not empty
    while arcQ:
        # pop an arc tail -> head from queue
        t, h = arcQ.popleft()
        # prune domain of tail  based on head's domain
        removed = False
        if debug:
            print("t: {} -> h: {}, old t d: {}".format(t, h, doms[t[0]]))

        overlap = [w[h[1]] for w in doms[h[0]]]

        if debug:
            print(f"\th d: {doms[h[0]]}, {overlap}")
        # for each value in tail's domain
        for x in doms[t[0]]:
            c = x[t[1]]
            if debug:
                print(f"for t value {x}, c={c}, {c not in overlap}")
            # removed value if there is no value in head's domain that satisfy cons
            if c not in overlap:
                doms[t[0]].remove(x)
                removed = True
        # if domain of tail is pruned
        if removed:
            if debug:
                print("\t removed?: {}, t: {}, new d: {}".format(
                    removed, t, doms[t[0]]))
            # if domain of t is empty (all values are inconsistent), return False
            if len(doms[t[0]]) == 0:
                return False
            if debug:
                print(f"cons at index {t[0]}: {cons[t[0]]}\narcQ: {arcQ}")
            # add all arc n -> t to the queue if not already and n != h
            for n in cons[t[0]]:
                if debug:
                    print("n, h: ", n, h,
                          ((n[0], n[1]) not in arcQ), (n[0] != h))
                if (n[0], n[1]) not in arcQ and n[0] != h:
                    if debug:
                        print(f"added {(n[0], n[1])}")
                    arcQ.append((n[0], n[1]))
    return True


# DFS-B with variable, value ordering + AC3 for constraint propagation.
def improved_DFSB(assignment, constraints, domains, arclist, debug):
    print("\nCurrent assignment: ", assignment)
    if debug:
        print(constraints, domains, arclist)
    # if assignment is complete, return the assignment
    if None not in assignment:
        return assignment
    lengths = [len(domains[i]) for i in range(len(domains))]
    if debug:
        print("lengths: ", lengths)
    # call AC3 on given csp to do constrain propagation if some domain length is more than 1;
    #   if inconsistent detected, return False
    if(sum(lengths) != len(lengths)):
        if AC3(constraints, domains, arclist, debug) == False:
            return False
        if debug:
            print("domains after AC3: ", domains)
    global exploredCount  # global counter for explored states
    exploredCount += 1
    # select most constrained unassigned variable:
    #   the one w/ min remaining values, if tie occurs pick the one w/ most neighbors
    index = [i for i in range(len(domains)) if assignment[i] == None]
    remaining = [len(domains[i]) for i in index]
    minRe = min(remaining)
    if debug:
        print("index, remaining, minRe: ", index, remaining, minRe)
    if remaining.count(minRe) == 1:  # only one remaining value or no tie, or minRe==1
        var = index[remaining.index(minRe)]
    else:  # multiple var w/ same # of remaining values
        index2 = [index[i] for i in range(len(index)) if remaining[i] == minRe]
        nei = [len(constraints[i]) for i in index2]
        if debug:
            print("find the one w/ most nei:", nei)
        var = index2[nei.index(max(nei))]
    # perform ordering values: order value by reduceCount
    valueQ = PriorityQueue()
    if len(domains[var]) != 1:  # if more than 1 possible word
        reduceCount = 0  # count num of values rules out by given v in the remaining variable
        for v in domains[var]:
            for n in constraints[var]:  # for each neighbor
                if assignment[n[0][0]] == None:  # if it has not assign word
                    rule_out = [1 for w in domains[n[0][0]]
                                if (v[n[1][1]] != w[n[0][1]])]
                    if debug:
                        print(f"v: {v}, rule_out: {rule_out}")
                    reduceCount += len(rule_out)
            valueQ.put((reduceCount, v))  # add that value with its reduceCount
            reduceCount = 0
    else:
        valueQ.put((0, domains[var][0]))
    if debug:
        print("var: {}, valueQ: {}".format(var, valueQ.queue))
    # pop each value in domain of selected variable, Least constraining value first
    while not valueQ.empty():
        v = valueQ.get()[1]
        # if value is consistent with problem constraints, not same as neighbor's color
        if debug:
            print(f"value: {v}, cons: {constraints[var]}")
        consistent = True
        for i in constraints[var]:
            [pos, ind], [pos2, ind2] = i
            if debug:
                print(i, pos, ind, pos2, ind2,
                      assignment[pos], assignment[pos2], v)
            if assignment[pos] != None and v != None:
                if debug:
                    print(assignment[pos][ind], v[ind2])
                if assignment[pos][ind] != v[ind2]:
                    consistent = False
                break
        print(f"For v = {v}, consistent: {consistent}")
        if consistent:
            # add assignment[var]=v, domains[var] = [v], call DFSB on given assignment
            # print("\tvar: {}, v: {}".format(var, v))
            old_domain = copy.deepcopy(domains)
            domains[var] = [v]
            assignment[var] = v
            # forward checking
            for nei in constraints[var]:
                [pos, ind], [pos2, ind2] = nei
                # if possible word is more than 1 and assignment has not done yet
                if len(domains[pos]) != 1 and assignment[pos] == None:
                    c = assignment[var][ind2]
                    if debug:
                        print("nei, domain before:", nei, domains[pos])
                    for w in domains[pos]:
                        if w[ind] != c:
                            domains[pos].remove(w)
                    if debug:
                        print(
                            f"after assign {assignment[var]}, {c}; domain at {pos}: {domains[pos]}")
            res = improved_DFSB(assignment, constraints,
                                domains, arclist, debug)
            # if result is not false, return result
            if res != False:
                return res
            # otherwise recover the old domain and assignment
            print("\tIn otherwise, recover domain ")
            assignment[var] = -1
            domains = old_domain
    return False


def buildBoard(n, pos):
    board = [['-' for j in range(n)] for i in range(n)]
    constraints = [[] for i in range(len(pos))]
    for i in range(n):
        row = []
    # printBoard(board)
    for i in range(len(pos)):
        x, y, d, l = pos[i]
        print("x, y, d, l: ", x, y, d, l)
        if d == 0:  # vertical
            for j in range(l):  # go down
                if(board[x+j][y] == '*'):  # intersect
                    # printBoard(board)
                    a = 0
                    while(board[x+j][y-a-1] == '*'):
                        a += 1
                    for p in range(len(pos)):
                        if (pos[p][0] == x+j and pos[p][1] == y-a and pos[p][2] == 1):
                            constraints[i].append([[p, a], [i, j]])
                            constraints[p].append([[i, j], [p, a]])
                            break
                    # c = [ p for p in range(len(pos)) if (pos[p][0]==x-a and pos[p][1]==y+j and pos[p][2]==0) ]
                    # print("a: ", a, j, x+j, y-a, [p, a, j], [i, j, a], "c: ", constraints)
                board[x+j][y] = '*'
        else:  # horizontal
            for j in range(l):  # go right
                if(board[x][y+j] == '*'):  # intersect
                    # printBoard(board)
                    a = 0
                    while(board[x-a-1][y+j] == '*'):
                        a += 1
                    for p in range(len(pos)):
                        if (pos[p][0] == x-a and pos[p][1] == y+j and pos[p][2] == 0):
                            constraints[i].append([[p, a], [i, j]])
                            constraints[p].append([[i, j], [p, a]])
                            break
                    # print("a: ", a, j, x-a, y+j, [p, a, j], [i, j, a], "c: ", constraints)
                board[x][y+j] = '*'
    printBoard(board)
    return board, constraints


def printBoard(board):
    for i in board:
        print(i)


if __name__ == '__main__':
    print(sys.argv, len(sys.argv), sys.argv[0])
    debug = 0
    # Get Crossword CSP
    args = sys.argv

    if len(args) != 3:
        print('Error: invalid arguments!')
        print('Usage: python3 solver.py <INPUT FILE> <OUTPUT FILE> <MODE FLAG>. \n')
        exit(-1)
    file = args[1]

    if file[-4:] == ".txt":
        crossword = SampleCrosswordTxt(file)
    else:
        parser = Parser()
        crossword = parser.parse(file)
    hints = [word.clue for word in crossword.word_list]
    word_ass = [None for i in range(len(hints))]
    word_domains = [word.domain for word in crossword.word_list]

    cons = crossword.constraints

    arclist = []

    for i in range(len(crossword.word_list)):
        print(i, ":", crossword.word_list[i])

    for i in range(len(cons)):
        print(f"cons at {i}: {cons[i]}")
        for j in cons[i]:
            arclist.append((j[1], j[0]))
    print("arclist: ", arclist)

    for i in range(len(cons)):
        print(f"{i}: {hints[i]}, \t{word_domains[i]}, \t{cons[i]}")
    print(
        f"word_ass: {word_ass} \ncons: {cons} \nword_domains: {word_domains}")
    debug = True  # True, False
    start_time = datetime.now()
    solution = improved_DFSB(word_ass, cons, word_domains, arclist, debug)
    time_elapsed = datetime.now() - start_time
    print("solution: ", solution)

    if solution is not False:
        for i in range(len(solution)):
            crossword.word_list[i].word = solution[i]

    print(crossword.return_grid())

    # Output solution into text file
    output_file = args[2]
    if solution is not False:
        with open(output_file, 'w') as f:
            f.write(str(crossword.return_grid()))
