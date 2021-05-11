import numpy as np
import copy


class Word:
    ''' 
    __init__ function for Word 
    number = number in the crossword puzzle 
    orientation = 0 for down/vertival, 1 for across/horizontal
    length = length of word 
    start = [x,y] where word start on the grid 
    word = word
    clue = clue for the word 
    constraints = constraints on this word 
    domain = list of words 
    possible_words = list of possible solutions 
    '''

    def __init__(self, number, length, orientation, start, clue, domain=None,  constraints=None):
        self.number = number
        self.temp = -1
        self.orientation = orientation
        self.length = length
        self.start = start
        self.word = None
        self.clue = clue
        self.constraints = [] if constraints is None else constraints
        self.domain = [] if domain is None else domain

    ''' 
    is_valid checks if a word if valid given the current partial solution 
    input: word (string) 
    output: boolean value for succtess status 
    '''

    def is_valid(self, word):
        if len(word) != self.length:
            return False

        # Check if any constraints are violated
        for constraint in self.constraints:
            index = constraint[1]
            if constraint[0].word is None:
                continue
            if word[index] != constraint[0].word[index]:
                return False

        self.word = word
        return True

    def __repr__(self):
        string = {'number': self.number,
                  'length': self.length,
                  'orientation': "across" if self.orientation == 1 else "down",
                  'start': str(self.start),
                  # 'clue' : self.clue,
                  'word': self.word}
        # return str(string )
        orientation = " across" if self.orientation == 1 else " down"

        return str(self.number) + " " + orientation
        return str(string)

    def __eq__(self, word):
        return self.number == word.number and self.orientation == word.orientation

    def __gt__(self, word):
        if self.number == word.number:
            return self.orientation > word.orientation  # Vertrical first
        return self.number > word.number


class Crossword:
    '''
    __init__ function for Crossword 
    input: 
        grid (array) = crossword 
        words_across (dictionary) = key: number and value: Word object 
        words_down (dictionary) = key: number and value: Word object 
    '''

    def __init__(self, vert_dim, hor_dim, grid=None, words=None, constraints=None):
        if grid is None:
            self.grid = [['-' for j in range(hor_dim)]
                         for i in range(vert_dim)]
        else:
            self.grid = copy.deepcopy(grid)

        self.vert_dim = vert_dim
        self.hor_dim = hor_dim
        self.word_list = [] if words is None else words
        self.constraints = [] if constraints is None else constraints

    ''' 
    is_solution checks if the crossword is solved 
    output: boolean 
    '''

    def is_solution(self):
        for value in self.words.values():
            for word in value:
                if word.word is None:
                    return False

        return True

    '''
    blank_words returns a list of words that does not have a solution 
    output: list 
    '''

    def blank_words(self):
        words = []
        for value in self.words.values():
            for word in value:
                if word.word is None:
                    words.append(word)
        return word

    # def add_solution_dict(self, number, orientation, solution):
        # word = self.word_list[number][orientation]
        # if word.is_valid(solution):
        # word.word = solution
        # word.domain = [solution]
        # return True
        # return False

    '''
    Updates Crossword with solution for a word 
    input: index (integer), solution (string) 
    output: boolean value for success status 
    '''

    def add_solution(self, index, solution):
        word = self.word_list[index]
        if word.is_valid(solution):
            word.word = solution
            word.domain = [solution]
            return True
        return False

    '''
    Returns the grid as an array 
    '''

    def return_grid(self):
        grid = copy.deepcopy(self.grid)
        for word in self.word_list:
            if word.word is not None:
                x = word.start[0]
                y = word.start[1]
                dim = word.orientation
                ind = 0

                while ind < word.length:
                    grid[x, y] = word.word[ind]
                    ind += 1
                    if dim == 0:
                        x += 1
                    else:
                        y += 1
        return grid

    def __repr__(self):
        return str(self.return_grid()) + "\n" + str(self.word_list)
