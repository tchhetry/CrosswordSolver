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
        self.fill = fill #np.array(['*' for i in range(length)])
        self.clue = clue 
        if possible_words is None: 
            self.possible_words = [] 
        else: 
            self.possible_words = possible_words
    
    ''' 
    Check if word is valid given the current partial solution 
    '''
    def is_valid(self, word): 
        if len(word) != self.length: 
            return False 
            
        for i in range(self.length): 
            if self.fill[i] != "*" and word[i] != self.fill[i]: 
                return False 
        return True 
        
    '''
    Returns true if the word is valid and updates Word 
    Returns false otherwise 
    '''
    def fill_word(self, word): 
        if not self.is_valid(word): 
            return False 
        self.word = word 
        # for i in range(self.length):
            # self.fill[i] = word[i] 
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
    grid = array of crossword 
    words_across = dictionary where key = number and value = Word object 
    words_down = dictionary where key = number and value = Word object 
    '''
    def __init__(self, vert_dim, hor_dim, grid = None): 
        if grid is None: 
            self.grid = [['-' for j in range(hor_dim)] for i in range(vert_dim)]
        else: 
            self.grid = copy.deepcopy(grid)
        self.words_across = {}
        self.words_down = {}
    
    ''' 
    Returns true if all the words are filled out, False otherwise 
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
    Returns list of across words that has no solution yet 
    '''
    def across_blank(self): 
        words = [] 
        for word in self.words_across: 
            if word.word is None: 
                words.append(word) 
        return words 
    
    '''
    Returns list of down words that has no solution yet 
    
    '''
    def down_blank(self): 
        words = [] 
        for word in self.words_down: 
            if word.word is None: 
                words.append(word) 
        return words 
    
    '''
    Add solution and update grid 
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
                word.fill_word(solution)
                # Update grid 
                i = word.start[0]
                j = word.start[1]
                for offset in range(word.length): 
                    self.grid[i+offset,j] = word.word[i]
                return True 
        return False 
    
    ''' 
    Update grid and words with new grid (NOTE: 'grid' should be a deepcopy) 
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