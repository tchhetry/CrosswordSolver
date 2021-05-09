class Word: 
    def __init__(self, number, length, orientation, start, clue, possible_words = None): 
        self.number = number 
        self.orientation = orientation 
        self.length = length 
        self.start = start  
        self.solution = None 
        self.clue = clue 
        if possible_words is None: 
            self.possible_words = [] 
        else: 
            self.possible_words = possible_words

class Crossword: 
    def __init__(self, vert_dim, hor_dim, grid = None): 
        if grid is None: 
            self.grid = [['-' for j in range(hor_dim)] for i in range(vert_dim)]
        else: 
            self.grid = grid 
        self.words_across = {}
        self.words_down = {} 
        
    def add_across(self, number, word): 
        self.words_across[number] = word 
        
    def add_down(self, number, word): 
        self.words_down[number] = word 
    
    def __str__(self): 
        string = "" 
        for row in self.grid: 
            string += (str(row) +'\n')
        return string 