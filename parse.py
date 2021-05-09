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
Create grid for the Crossword puzzle: 
_ for black space 
* for word space 
'''
grid = []         

for i in range(p.height):
    start = i * p.width
    row = ['*' if c == '-' else '_' for c in p.fill[start:start + p.width]]
    grid.append(row)

grid = np.array(grid)
crossword = Crossword(p.width, p.height, grid)


numbering = p.clue_numbering()

''' 
Add Words to the crossword puzzle 
'''
for clue in numbering.across:
    cell = clue['cell'] 
    x = cell//p.width 
    y = cell - (x*p.width)
 
    word = Word(clue['num'], clue['len'], 1, [x,y], clue['clue'], crossword.grid[x,y:y+clue['len']])
    crossword.words_across[clue['num']] = word  

for clue in numbering.down:
    cell = clue['cell'] 
    x = cell//p.width 
    y = cell - (x*p.width)
  
    word = Word(clue['num'], clue['len'], 0, [x,y], clue['clue'], crossword.grid[x:x+clue['len'],y])
    crossword.words_down[clue['num']] = word   

