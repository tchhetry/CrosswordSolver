from bs4 import BeautifulSoup
from selenium import webdriver
import requests

# link = "https://www.wordplays.com/crossword-solver/"
# link = "https://crossword-solver.io/clue/Cover-your-face/pattern/____/?s=1"
link = "https://crossword-solver.io"

def wordplaysCand(clue, length):
    answers = []
    linkClue = clue.replace(" ", "-")
    url = link + '/clue/' + clue + '/pattern/' + '_'*length + '/?s=1'
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, features="html.parser")

    rows = soup.find_all("tr")
    if rows != None:
        for r in rows:
            word = r.find_all("td")
            if len(word) > 1:
                answers.append(word[1].text.replace("\n", ""))
    return answers

# domain = wordplaysCand("Cover Your Face", 4) # Something sweet
# print("domain", domain)