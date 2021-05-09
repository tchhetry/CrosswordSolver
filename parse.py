import puz 
from Puzzle import Crossword, Word 
import sys 

file = 'che20200110.puz' 


args = sys.argv 
if len(args) == 2: 
    file = args[1] 
    
p = puz.read(file)


'''
Create grid for the Crossword puzzle: 
_ for black space 
* for word space 
'''
grid = []         

for i in range(p.height):
    start = i * p.width
    row = ['*' if c == '-' else '_' for c in p.fill[start:start + p.width]]
    grid.append(row)

crossword = Crossword(p.width, p.height, grid)


numbering = p.clue_numbering()

''' 
Add Words to the crossword puzzle 
'''
for clue in numbering.across:
    cell = clue['cell'] 
    x = cell//p.width 
    y = cell - (x*p.width)
 
    word = Word(clue['num'], clue['len'], 0, [x,y], clue['clue'])
    crossword.words_across.append(word) 

for clue in numbering.down:
    cell = clue['cell'] 
    x = cell//p.width 
    y = cell - (x*p.width)
  
    word = Word(clue['num'], clue['len'], 0, [x,y], clue['clue'])
    crossword.words_down.append(word)     

