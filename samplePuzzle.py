from Puzzle import Crossword, Word
import numpy as np
import copy
'''
Sample Crossword Puzzle Object
'''

from english_words import english_words_lower_set

english_dic = {}

for word in english_words_lower_set:
    try:
        english_dic[len(word)].append(word)
    except:
        english_dic[len(word)] = [word]


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
                      pirate, pumpkin, candy, mask, lantern]

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


class SampleCrosswordTxt(Crossword):
    def __init__(self, file):
        with open(file, 'r') as f:
            lines = f.readlines()

            use_eng_dom = 0
            words = lines[0].strip().split(", ")
            dim = lines[1].split(',')
            vert = int(dim[0])
            hor = int(dim[0])
            dictionary = {}

            for word in words:
                try:
                    dictionary[len(word)].append(word)
                except:
                    dictionary[len(word)] = [word]
            i = 3
            line = lines[i]
            across = []
            while line != "\n":
                across.append(line)
                i += 1
                line = lines[i]

            i += 2
            line = lines[i]
            down = []
            while line != "\n":
                down.append(line)
                i += 1
                line = lines[i]

            # Process across
            words_list = []

            for val in across:
                num = int(val.split('.')[0])
                s = val.split(' ')
                x = int(s[1][1:-1])
                y = int(s[2][:-1])
                length = int(s[3][:-1])
                orientation = 1
                clue = ' '.join(s[4:])[:-1]

                if use_eng_dom == 0:
                    words_list.append(Word(num, length, orientation, [
                        x, y], clue, copy.deepcopy(dictionary[length])))
                else:
                    words_list.append(Word(num, length, orientation, [
                        x, y], clue, copy.deepcopy(english_dic[length])))
            for val in down:
                num = int(val.split('.')[0])
                s = val.split(' ')
                x = int(s[1][1:-1])
                y = int(s[2][:-1])
                length = int(s[3][:-1])
                orientation = 0
                clue = ' '.join(s[4:])[:-1]

                if use_eng_dom == 0:
                    words_list.append(Word(num, length, orientation, [
                        x, y], clue, copy.deepcopy(dictionary[length])))
                else:
                    words_list.append(Word(num, length, orientation, [
                        x, y], clue, copy.deepcopy(english_dic[length])))

            words_list = sorted(words_list)
            words = {}
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

        super().__init__(vert, hor, self.create_grid(
            hor, vert, words), words_list, constraints)

    def add_to_words(self, word, words):
        i = word.start[0]
        j = word.start[1]
        ind = 0
        while ind < word.length:
            try:
                words[(i, j)].append([word, ind])
            except:
                words[(i, j)] = [[word, ind]]
            if word.orientation == 0:  # Vertical then increment i
                i += 1
            else:
                j += 1
            ind += 1
        return words

    def create_grid(self, width, height, word_list):
        grid = [["_" for j in range(width)] for i in range(height)]

        for key in word_list.keys():
            grid[key[0]][key[1]] = "*"

        return np.array(grid)
# file = 'simpleP/p2.txt'
# sample = SampleCrosswordTxt(file)
# print(sample.word_list)
# # for word in sample.word_list:
# #     print(word.number)
# #     print(word.constraints)

# for c in sample.constraints:
#     print(c)
