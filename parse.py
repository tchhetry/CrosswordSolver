'''
This file takes a .puz file and parses the content into a Crossword object 
If no argument is given, 'che20200110.puz' is used 
'''

import puz
from Puzzle import Crossword, Word
import sys
import numpy as np

file = 'che20200110.puz'


args = sys.argv
if len(args) == 2:
    file = args[1]

p = puz.read(file)


''' 
Add Words to the crossword puzzle 
'''


def get_start(clue):
    cell = clue['cell']
    x = cell//p.width
    y = cell - (x*p.width)
    return [x, y]


def add_indices(x, y, word):
    global word_indices
    i = x
    j = y
    ind = 0
    while ind < word.length:
        try:
            word_indices[(i, j)].append(word)
        except:
            word_indices[(i, j)] = [word]
        if word.orientation == 0:
            i += 1
        else:
            j += 1
        ind += 1


def add_words_to_crossword():
    global crossword
    global p
    numbering = p.clue_numbering()
    for clue in numbering.across:
        x, y = get_start(clue)
        word = Word(clue['num'], clue['len'], 1, [x, y], clue['clue'])

        add_indices(x, y, word)
        crossword.word_list.append(word)

    for clue in numbering.down:
        x, y = get_start(clue)

        word = Word(clue['num'], clue['len'], 0, [x, y], clue['clue'])
        add_indices(x, y, word)
        crossword.word_list.append(word)


def add_constraints_to_words():
    '''
    Add Constraints 
    '''
    global word_indices
    for key, value in word_indices.items():
        for i in range(len(value)-1):
            word = value[i]
            for j in range(i+1, len(value)):
                word.constraints.append([value[j], key])
                value[j].constraints.append([word, key])


def add_constraints_to_crossowrd():
    global word_indices
    constraints = []


'''
Create grid for the Crossword puzzle: 
_ for black space 
* for word space 
'''
grid = []
word_indices = {}
for i in range(p.height):
    start = i * p.width
    row = ['*' if c == '-' else '_' for c in p.fill[start:start + p.width]]
    grid.append(row)

grid = np.array(grid)
crossword = Crossword(p.width, p.height, grid)
add_words_to_crossword()
add_constraints_to_words()

print(word_indices)

'''
BERT to get domain 
'''
