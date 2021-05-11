# CrosswordSolver
Our CSE 352 final project, a crossword puzzle solver that uses machine learning

To run: 
> python solver.py <input_file> <output_file> 

Note: Input file can be of .txt or .puz 

In case of .txt file, format should be of: 
list of word bank 
vert_dim,hor_dim 
Across
<number>. (x, y, length) <Hint>

Down
<number>. (x, y, length) <Hint>


Dependencies: 
> pip install english_words 
> pip install beautiful_soup 
> pip install selium 