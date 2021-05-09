class Word: 
    ''' 
    __init__ function for Word 
    number = number in the crossword puzzle 
    length = length of word 
    start = [x,y] where word start on the grid 
    word = word
    fill = array of word length. Used to keep track of partial solution 
    fill_prev = Keep track of previous state of fill 
    clue = clue for the word 
    possible_words = list of possible solutions 
    '''
    def __init__(self, number, length, orientation, start, clue, possible_words = None): 
        self.number = number 
        self.orientation = orientation 
        self.length = length 
        self.start = start  
        self.word = None 
        self.fill = ['*' for i in range(length)]
        self.fill_prev = self.fill
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
            if self.fill != "*" and word[i] != self.fill[i]: 
                return False 
        return True 
    
    '''
    Returns true if the word is valid and updates Word 
    Returns false otherwise 
    '''
    def fill_word(self, word): 
        if not is_valued(word): 
            return False 
        self.word = word 
        for i in range(self.length):
            self.fill[i] = word[i] 
        return True 
    
    
    def __repr__(self): 
        string = {'number': self.number, 
            'length' : self.length,
            'orientation' : "across" if self.orientation == 0 else "down",
            'start' : str(self.start), 
            'clue' : self.clue,
            'word' : self.fill}
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
            self.grid = grid 
        self.words_across = []
        self.words_down = []
    
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
    Remove a solution and update the grid and Words 
    '''
    def remove_solution(self, number, orientation): 
        pass 
        
    def update_grid(self): 
        pass 
        
    def __repr__(self): 
        string = "" 
        for row in self.grid: 
            string += (str(row) +'\n')
        return string 