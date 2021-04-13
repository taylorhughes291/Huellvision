import csv

from lxml import html
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


URL = 'https://blogs.chapman.edu/huell-howser-archives/1991/01/10/preserving-the-past-californias-gold-207/'
fields = ['ID', 'URL', 'episodeType', 'episodeName', 'episodeDate', 'episodeTags', 'videoSource']


filename = "huellArchives.csv"




driver = webdriver.Chrome('/Applications/Utilities/chromedriver')
rows = []
nextPage = "1"
ID = 0

#The for loop will begin here using i as the index. Possibly while loop.
while len(nextPage) > 0:
#for x in range(0,3):

    ID = ID + 1

    driver.get(URL)

    episodeType = driver.find_elements_by_xpath('//a[@rel="category tag"]')
    episodeType = episodeType[0].text
    episodeName = driver.find_elements_by_xpath('//h1[contains(@class, "entry-title")]')
    episodeName = episodeName[0].text
    episodeDate = driver.find_elements_by_xpath('//time[contains(@class, "entry-date")]')[0]

    episodeDate = episodeDate.get_attribute('datetime')
    episodeTags = driver.find_elements_by_xpath('//span[contains(@class, "tags-links")]/a')
    for y in range(0, len(episodeTags)):
        episodeTags[y] = episodeTags[y].text

    
    nextPage = driver.find_elements_by_xpath('//a[@rel="next"]')
    if len(nextPage) > 0:
        nextPage = nextPage[0].get_attribute('href')

    iframe = driver.find_elements_by_tag_name("iframe")
    
    driver.switch_to.frame(iframe[0])
    if len(driver.find_elements_by_xpath('//video')) == 0:
        driver.switch_to.default_content()
        driver.switch_to.frame(iframe[1])        
    videoSource = driver.find_elements_by_xpath('//video')
    if len(videoSource) > 0:
        videoSource = videoSource[0].get_attribute('src')

    row = [
        ID,
        URL,
        episodeType,
        episodeName,
        episodeDate,
        episodeTags,
        videoSource
        ]

    rows.append(row)



    URL = nextPage


with open("huellArchives.csv", "w", encoding="utf-8-sig") as file:
    csv.writer(file).writerow(fields)
    csv.writer(file).writerows(rows)


