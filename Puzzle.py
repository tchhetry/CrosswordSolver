'''
This file contains the Word and Crossword object 
'''

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
    fill = array of word length. Used to keep track of partial solution 
    clue = clue for the word 
    possible_words = list of possible solutions 
    '''
    def __init__(self, number, length, orientation, start, clue, fill, possible_words = None): 
        self.number = number 
        self.orientation = orientation 
        self.length = length 
        self.start = start  
        self.word = None 
        self.fill = fill
        self.clue = clue 
        if possible_words is None: 
            self.possible_words = [] 
        else: 
            self.possible_words = possible_words
    
    ''' 
    is_valid checks if a word if valid given the current partial solution 
    input: word (string) 
    output: boolean 
    '''
    def is_valid(self, word): 
        if len(word) != self.length: 
            return False 
        print(self.number, self.fill)    
        for i in range(self.length): 
            
            if self.fill[i] != "*" and word[i] != self.fill[i]: 
                return False 
        return True 
        
    '''
    fill_word updates self.word 
    input: word (string) 
    output: boolean 
    '''
    def fill_word(self, word): 
        if not self.is_valid(word): 
            return False 
            
        self.word = word 
        return True 
    
    
    def __repr__(self): 
        string = {'number': self.number, 
            'length' : self.length,
            'orientation' : "across" if self.orientation == 1 else "down",
            'start' : str(self.start), 
            'clue' : self.clue,
            'partial_word' : self.fill,
            'word' : self.word}
        return str(string )
        
class Crossword: 
    '''
    __init__ function for Crossword 
    input: 
        grid (array) = crossword 
        words_across (dictionary) = key: number and value: Word object 
        words_down (dictionary) = key: number and value: Word object 
    '''
    def __init__(self, vert_dim, hor_dim, grid = None, words_across = None, words_down = None): 
        if grid is None: 
            self.grid = [['-' for j in range(hor_dim)] for i in range(vert_dim)]
        else: 
            self.grid = copy.deepcopy(grid)
            
        
        self.words_across = words_across if words_across is not None else {} 
        self.words_down = words_down if words_down is not None else {} 
    
    ''' 
    is_solution checks if the crossword is solved 
    output: boolean 
    '''
    def is_solution(self): 
        
        for word in self.words_across: 
            if word.word is None: 
                return False 
        
        for word in self.words_down: 
            if word.word is None:   
                return False 
                
        return True 
    
    '''
    across_blank returns a list of horizontal words that does not have a solution 
    output: list 
    '''
    def across_blank(self): 
        words = [] 
        for word in self.words_across: 
            if word.word is None: 
                words.append(word) 
        return words 
    
    '''
    across_down returns a list of vertical words that does not have a solution 
    output: list 
    '''
    def down_blank(self): 
        words = [] 
        for word in self.words_down: 
            if word.word is None: 
                words.append(word) 
        return words 
    
    '''
    add_solution updates the grid and corresponding word with the solution 
    input: 
        number (integer): number associated with the word 
        orientation (integer): 0 for vertical/down, 1 for horizontal/across 
        solution (string): given solution 
    output: boolean for success status 
    '''
    def add_solution(self, number, orientation, solution): 
        if orientation == 1: # Horizontal/across 
            word = self.words_across[number]
            if word.is_valid(solution): 
            
                word.fill_word(solution)
                # Update grid 
                i = word.start[0]
                j = word.start[1]
                for offset in range(word.length): 
                    self.grid[i, j+offset] = word.word[offset]
                return True 
            
        else: # Vertical/Down 
            word = self.words_down[number] 
            if word.is_valid(solution): 
                print(solution, "VALID")
                word.fill_word(solution)
                # Update grid 
                i = word.start[0]
                j = word.start[1]
                for offset in range(word.length): 
                    self.grid[i+offset,j] = word.word[offset]
                return True 
        return False 
    
    ''' 
    update_grid updates the grid and corresponding words 
    input: grid (array) = new grid status 
        NOTE: grid should be a deepcopy 
    '''
    def update_grid(self, grid): 
        for word in (list(self.words_across.values()) + list(self.words_down.values())): 
            i = word.start[0]
            j = word.start[1]
            self.grid[i,j] = grid[i,j]
            if word.orientation == 1: # Across 
                if not np.array_equal(word.fill, grid[i, j:j+word.length]): 
                    word.word = None 
            else: 
                if not np.array_equal(word.fill, grid[i:word.length, j]): 
                    word.word = None 
        
        
    def __repr__(self): 
        string = "" 
        for row in self.grid: 
            string += (str(row) +'\n')
        return string 