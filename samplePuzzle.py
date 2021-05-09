from Puzzle import Crossword, Word
import numpy as np
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

        # Instantiate words
        trick = Word(1, 5, 0, [0, 4], "The opposite of treat", [
                     "trick", "candy"])
        monster = Word(2, 7, 0, [2, 6], "Goes bump in the night", [
                       'pumpkin', 'monster', 'lantern'])
        pirate = Word(4, 6, 0, [4, 0], "Sails the seven seas", [
                      "pirate"])
        candy = Word(5, 5, 0, [5, 8], "Something sweet", ["trick", "candy"])
        mask = Word(6, 4, 0, [6, 3], "Cover your face", ["mask", "lent"])
        owl = Word(3, 3, 1, [3, 6], "Gives a hoot", ["owl", "wow"])
        pumpkin = Word(4, 7, 1, [4, 0], "Something orange and round", [
                       'pumpkin', 'monster', 'lantern'])
        lantern = Word(7, 7, 1, [7, 2], "Lights the night", [
                       'pumpkin', 'monster', 'lantern'])

        words = {}

        # Add constraints
        words_list = [trick, monster, owl,
                      pirate, pumpkin, candy, lantern, mask]

        for word in words_list:
            words = self.add_to_words(word, words)

        for key, value in words.items():
            for i in range(len(value)-1):
                for j in range(i+1, len(value)):

                    value[i][0].constraints.append(
                        [value[j][0], value[j][1], value[i][1]])
                    value[j][0].constraints.append(
                        [value[i][0], value[i][1], value[j][1]])

        # Add to crossword constraints
        constraints = []
        for i in range(len(words_list)):
            row = []
            word = words_list[i]
            for nei in word.constraints:
                pos = words_list.index(nei[0])
                ind = nei[1]
                row.append([[pos, ind], [i, nei[2]]])
            constraints.append(row)

        super().__init__(9, 10, grid, words_list, constraints)

    def add_to_words(self, word, words):
        i = word.start[0]
        j = word.start[1]
        ind = 0
        while ind < word.length:
            try:
                words[(i, j)].append([word, ind])
            except:
                words[(i, j)] = [[word, ind]]
            if word.orientation == 0:
                i += 1
            else:
                j += 1
            ind += 1
        return words


sample = SampleCrossword()
# print(sample)
# print(sample.word_list)
# print("For word OWL")
# word = sample.word_list[0]

# print(word.domain)
# print(word.constraints)
# sample.add_solution(0, "owl")
# print(word.word)
# print(sample.return_grid())
