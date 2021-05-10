'''
This files takes in a .puz file and MODE flag 
FORMAT python solver.py <input_file> <output_file> <mode> 
'''

from samplePuzzle import SampleCrossword
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


def AC3(cons, doms, arcl):
    print("\nAC3: doms:{}, cons: {}".format(doms, cons))
    # initilize arc Queue, contains all arcs in csp
    arcQ = deque(arcl)
    # while arc Queue is not empty
    while arcQ:
        # pop an arc tail -> head from queue
        t, h = arcQ.popleft()
        # prune domain of tail  based on head's domain
        removed = False
        print("t: {} -> h: {}, old t d: {}".format(t, h, doms[t[0]]))
        overlap = [w[h[1]] for w in doms[h[0]]]
        print(f"\th d: {doms[h[0]]}, {overlap}")
        # for each value in tail's domain
        for x in doms[t[0]]:
            c = x[t[1]]
            print(f"for t value {x}, c={c}, {c not in overlap}")
            # removed value if there is no value in head's domain that satisfy cons
            # if doms[h] == [x]: # if x in doms[h] and len(doms[h]) == 1:
            #     doms[t].remove(x)
            #     removed = True
            if c not in overlap:
                doms[t[0]].remove(x)
                removed = True
        # if domain of tail is pruned
        if removed:
            print("\t removed?: {}, t: {}, new d: {}".format(
                removed, t, doms[t[0]]))
            # if domain of t is empty (all values are inconsistent), return False
            if len(doms[t[0]]) == 0:
                return False
            print(f"cons at index {t[0]}: {cons[t[0]]}\narcQ: {arcQ}")
            # add all arc n -> t to the queue if not already and n != h
            for n in cons[t[0]]:
                print("n, h: ", n, h, ((n[0], n[1]) not in arcQ), (n[0] != h))
                if (n[0], n[1]) not in arcQ and n[0] != h:
                    print(f"added {(n[0], n[1])}")
                    arcQ.append((n[0], n[1]))
    return True

# DFS-B with variable, value ordering + AC3 for constraint propagation.


def improved_DFSB(assignment, constraints, domains, arclist):
    print("\nCurrent assignment: ", assignment)
    print(constraints, domains, arclist)
    # if assignment is complete, return the assignment
    if None not in assignment:
        return assignment
    # call AC3 on given csp to do constrain propagation; if inconsistent detected, return False
    if AC3(constraints, domains, arclist) == False:
        return False
    # print("domains after AC3: ", domains)
    global exploredCount  # global counter for explored states
    exploredCount += 1
    # select most constrained unassigned variable:
    #   the one w/ min remaining values, if tie occurs pick the one w/ most neighbors
    index = [i for i in range(len(domains)) if assignment[i] == None]
    remaining = [len(domains[i]) for i in index]
    print("index, remaining: ", index, remaining)
    minRe = min(remaining)
    print("index, remaining, minRe: ", index, remaining, minRe)
    if remaining.count(minRe) == 1:  # only one remaining value or no tie, or minRe==1
        var = index[remaining.index(minRe)]
    else:  # multiple var w/ same # of remaining values
        index2 = [index[i] for i in range(len(index)) if remaining[i] == minRe]
        nei = [len(constraints[i]) for i in index2]
        print("find the one w/ most nei:", nei)
        var = index2[nei.index(max(nei))]
    print("var: ", var)
    # perform ordering values: order value by reduceCount
    valueQ = PriorityQueue()
    reduceCount = 0  # count # of values rules out by given v in the remaining variable
    for v in domains[var]:
        #     for n in constraints[var]: # for each neighbor
        #         if assignment[n] == -1 and v in domains[n]:  # if it has not assign color and v in its domain
        #             reduceCount += 1
        valueQ.put((reduceCount, v))  # add that value with its reduceCount
    #     reduceCount = 0
    print("valueQ: {}".format(valueQ.queue))
    # pop each value in domain of selected variable, Least constraining value first
    while not valueQ.empty():
        v = valueQ.get()[1]
        # if value is consistent with problem constraints, not same as neighbor's color
        print(f"value: {v}, cons: {constraints[var]}")
        consistent = True
        for i in constraints[var]:
            [pos, ind], [pos2, ind2] = i
            print(i, pos, ind, pos2, ind2,
                  assignment[pos], assignment[pos2], v)
            if assignment[pos] != None and v != None:
                print(assignment[pos][ind], v[ind2])
                if assignment[pos][ind] != v[ind2]:
                    consistent = False
                break
        print(consistent)
        if consistent:
            # if v not in [ assignment[i] for i in constraints[var] ]:
            # add assignment[var]=v, domains[var] = [v], call DFSB on given assignment
            # print("\tvar: {}, v: {}".format(var, v))
            old_domain = copy.deepcopy(domains)
            domains[var] = [v]
            assignment[var] = v
            # forward checking
            for nei in constraints[var]:
                [pos, ind], [pos2, ind2] = nei
                c = assignment[var][ind2]
                print("nei, domain before:", nei, domains[pos])
                for w in domains[pos]:
                    if w[ind] != c:
                        domains[pos].remove(w)
                print(
                    f"after assign {assignment[var]}, {c}; domain at {pos}: {domains[pos]}")
                # if v in domains[nei]: domains[nei].remove(v)
            res = improved_DFSB(assignment, constraints, domains, arclist)
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
        # s = ""
        # for j in i:
        #     s += j
        # print(s)


if __name__ == '__main__':
    print(sys.argv, len(sys.argv), sys.argv[0])
    # if len(sys.argv) != 4:
    #     print('Error: invalid arguments!')
    #     # Usage: python dfsb.py <INPUT FILE> <OUTPUT FILE> <MODE FLAG>.
    #     # <MODE FLAG> can be either 0 (plain DFS-B) or 1 (improved DFS-B).
    #     print('Usage: python3 dfsb.py <INPUT FILE> <OUTPUT FILE> <MODE FLAG>. \n')
    #     exit(-1)

    n = 10
    words = ["trick", "pumpkin", "monster", "owl",
             "pirate", "mask", "lantern", "candy", "lent", "wow"]
    hints = ["The opposite of treat", "Goes bunp in the night", "Givens a hoot",
             "Sails the seven seas", "Something orange and around", "Something sweet",
             "Cover your face", "Lights the night"]
    # # (x, y, dimension, length), 0 -> vertical & 1 -> horizontal
    # # positions = [(0, 4, 0, 5), (2, 6, 0, 7), (3, 6, 1, 3), (4, 0, 0, 6), (4, 0, 1, 7),
    # #     (5, 8, 0, 5), (6, 3, 0, 4), (7, 2, 1, 7)]

    # positions = [(0, 4, 0, 5), (2, 6, 0, 7), (3, 6, 1, 3), (4, 0, 0, 6), (4, 0, 1, 7),
    #              (5, 8, 0, 5), (7, 2, 1, 7), (6, 3, 0, 4)]
    # word_list = [{}]
    # word_ass = [None for i in range(len(hints))]
    # word_domains = [[w for w in words if len(
    #     w) == positions[i][3]] for i in range(len(hints))]
    # print("word domains", word_domains)
    # b, cons = buildBoard(n, positions)
    # for c in cons:
    #     print(c)
    # printBoard(b)
    # random.shuffle(words)
    # print("words: ", words, len(hints))
    # for c in cons:
    #     print(c)
    # for d in word_domains:
    #     print(d)

    # ADDED TO TEST STRUCTURE
    sample = SampleCrossword()
    hints = [word.clue for word in sample.word_list]

    word_ass = [None for i in range(len(hints))]
    word_domains = [word.domain for word in sample.word_list]

    print(word_domains)

    cons = sample.constraints
    for c in cons:
        print(c)
    # for c in cons:
    #     print(c)
    # for d in word_domains:
    #     print(d)

    '''
    # Get Crossword CSP 
    args = sys.argv 
    if len(args) != 4:
        print('Error: invalid arguments!')
        Usage: python solver.py <INPUT FILE> <OUTPUT FILE> <MODE FLAG>.
        <MODE FLAG> can be either 0 (plain DFS-B) or 1 (improved DFS-B).
        print('Usage: python3 dfsb.py <INPUT FILE> <OUTPUT FILE> <MODE FLAG>. \n')
        exit(-1)
    file = args[1]
    parser = Parse() 
    crossword = parser.parse(file)
    hints = [word.clue for word in crossword.word_list]
    word_ass = [None for i in range(len(hints))]
    word_domains = [word.domain for word in sample.word_list]
    cons = crossword.constraints 
    '''

    arclist = []
    print(cons)
    for i in range(len(cons)):
        print(f"cons at {i}: {cons[i]}")
        for j in cons[i]:
            print("j", (i, j), j[1], j[0])
            arclist.append((j[1], j[0]))  # arcQ.put((i, j))
    print("arclist: ", arclist)

    print(word_ass, cons, word_domains)
    solution = improved_DFSB(word_ass, cons, word_domains, arclist)
    print("solution: ", solution)
    for i in range(len(solution)):
        sample.word_list[i].word = solution[i]

    print(sample.return_grid())
    # n, color_ass, neighbors, k = readInput(sys.argv[1])
    if(True and False):
        print("if")
        arclist = []  # arcQ = Queue(maxsize=0)
        for i in range(len(cons)):
            for j in cons[i]:
                arclist.append((i, j))  # arcQ.put((i, j))
        print("len of arclist", len(arclist))
        start_time = datetime.now()
        # improved_DFSB(assignment, constraints, domains, arclist):
        solution = improved_DFSB(word_ass, cons, word_domains, arclist)
        time_elapsed = datetime.now() - start_time
        print()
