import puz 
from Puzzle import Crossword
import sys 

file = 'che20200110.puz' 


args = sys.argv 
if len(args) == 2: 
    file = args[1] 
    
p = puz.read(file)

grid = []         

for i in range(p.height):
    start = i * p.width
    row = [c for c in p.fill[start:start + p.width]]
    grid.append(row)

crossword = Crossword(p.width, p.height, grid)
print(crossword)