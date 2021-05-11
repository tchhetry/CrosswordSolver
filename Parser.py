'''
This file takes a .puz file and parses the content into a Crossword object 
If no argument is given, 'che20200110.puz' is used 
'''

import puz
from Puzzle import Crossword, Word
import getDomain
import numpy as np


class Parser():
    def __init__(self):
        self.p = None
        self.word_indices = {}
        self.crossword = None

    def parse(self, file='che20200110.puz'):
        self.p = puz.read(file)
        grid = self.create_grid()
        self.crossword = Crossword(self.p.width, self.p.height, grid)
        self.add_words_to_crossword()
        self.add_constraints_to_words()
        self.add_constraints_to_crossowrd()

        self.add_domains_to_words()
        return self.crossword

    ''' 
    Add Words to the crossword puzzle 
    '''

    def get_start(self, clue):
        cell = clue['cell']
        x = cell//self.p.width
        y = cell - (x*self.p.width)
        return [x, y]

    def add_indices(self, x, y, word):
        i = x
        j = y
        ind = 0
        while ind < word.length:
            try:
                self.word_indices[(i, j)].append([word, ind])
            except:
                self.word_indices[(i, j)] = [[word, ind]]
            if word.orientation == 0:
                i += 1
            else:
                j += 1
            ind += 1

    def add_words_to_crossword(self):
        numbering = self.p.clue_numbering()
        for clue in numbering.across:
            x, y = self.get_start(clue)
            word = Word(clue['num'], clue['len'], 1, [x, y], clue['clue'])

            self.add_indices(x, y, word)
            self.crossword.word_list.append(word)

        for clue in numbering.down:
            x, y = self.get_start(clue)

            word = Word(clue['num'], clue['len'], 0, [x, y], clue['clue'])
            self.add_indices(x, y, word)
            self.crossword.word_list.append(word)

    '''
    Add Constraints to each word 
    '''

    def add_constraints_to_words(self):
        for key, value in self.word_indices.items():
            for i in range(len(value)-1):
                for j in range(i+1, len(value)):
                    value[i][0].constraints.append(
                            [value[j][0], value[j][1], value[i][1]])
                    value[j][0].constraints.append(
                            [value[i][0], value[i][1], value[j][1]])

    '''
    Add all constraints to the crossword 
    '''

    def add_constraints_to_crossowrd(self):
        constraints = []

        for i in range(len(self.crossword.word_list)):
            row = []
            word = self.crossword.word_list[i]
            for nei in word.constraints:
                pos = self.crossword.word_list.index(nei[0])
                ind = nei[1]
                row.append([[pos, ind], [i, nei[2]]])
            constraints.append(row)
        self.crossword.constraints = constraints

    '''
    Create grid for the Crossword puzzle: 
    _ for black space 
    * for word space 
    '''

    def create_grid(self):
        grid = []
        for i in range(self.p.height):
            start = i * self.p.width
            row = ['*' if c ==
                   '-' else '_' for c in self.p.fill[start:start + self.p.width]]
            grid.append(row)
        return np.array(grid)

    '''
    BERT to get domain 
    '''

    def add_domains_to_words(self):
        print("Getting Domain")
        for word in self.crossword.word_list:
            domain = getDomain.wordplaysCand(word.clue, word.length)
            word.domain = domain
        print("Complete")

# parser = Parser()
# parser.parse()

# solution = parser.p.solution
# width = parser.p.width
# ind = 0
# while ind < len(solution):
#     print(solution[ind:ind+width])
#     ind += width
