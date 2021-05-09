from Puzzle import Crossword, Word 

'''
Sample Crossword Puzzle Object 
'''

class SampleCrossword(Crossword): 
    def __init__(self): 
        grid = np.array([
            ['_', '_', '_', '_', '*', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '*', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '*', '_', '*', '_', '_'],
            ['_', '_', '_', '_', '*', '_', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '_', '_'],
            ['*', '_', '_', '_', '_', '_', '*', '_', '*'],
            ['*', '_', '_', '*', '_', '_', '*', '_', '*'],
            ['*', '_', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '_', '_', '*', '_', '_', '*', '_', '*'],
            ['*', '_', '_', '*', '_', '_', '_', '_', '*']]) 
            
       
        trick = Word(1, 5, 0, [0,4], "The opposite of treat" , grid[0:5,4])
        monster = Word(2, 7, 0, [2,6], "Goes bump in the night" , grid[2:9,6])
        pirate = Word(4, 6, 0, [4,0], "Sails the seven seas" , grid[4:10,0])
        candy = Word(5, 5, 0, [5,8], "Something sweet" , grid[5:10,8])
        mask = Word(6, 4, 0, [6,3], "Cover your face" , grid[6:10,3])
        owl = Word(3, 3, 1, [3,6], "Gives a hoot" , grid[3,6:9])
        pumpkin = Word(4, 7, 1, [4,0], "Something orange and round" , grid[4,0:7])
        lantern = Word(7, 7, 1, [7,2], "Lights the night" , grid[7,2:9])
        words_across = {
            3: owl, 4: pumpkin, 7: lantern
        }

        words_down = {
            1: trick, 2:monster, 4: pirate, 5: candy, 6: mask 
        }
        super().__init__(9,10,grid, words_across, words_down)
            
