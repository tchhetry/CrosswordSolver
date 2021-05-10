from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import sys

link = "https://www.wordplays.com/crossword-solver/"
if sys.platform == "darwin":
    chrome = "./chromedrivermac"
elif sys.platform == "win32" or sys.platform == "cygwin":
    chrome = "./chromedriver.exe"
else:
    chrome = "./chromedriverlinux"

def wordplaysCand(clue):
    answers = []
    options = Options()
    options.headless = True
    linkClue = clue.replace(" ", "-")
    driver = webdriver.Chrome(chrome, options = options)
    driver.get(link+linkClue)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(soup)
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

print(wordplaysCand("haha"))
