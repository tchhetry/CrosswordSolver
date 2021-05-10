from bs4 import BeautifulSoup
from selenium import webdriver
import requests

link = "https://www.wordplays.com/crossword-solver/"

def wordplaysCand(clue):
    answers = []
    linkClue = clue.replace(" ", "-")
    driver = webdriver.Safari()
    driver.get(link+linkClue)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    odds = soup.find_all("tr", {"class" : "odd"})
    evens = soup.find_all("tr", {"class" : "even"})
    if odds != None:
        for odd in odds:
            word = odd.find_all("td")
            if len(word) > 1:
                answers.append(word[1].text)
    if evens != None:
        for even in evens:
            word = even.find_all("td")
            if len(word) > 1:
                answers.append(word[1].text)
    return answers
