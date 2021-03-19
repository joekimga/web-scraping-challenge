from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests
import pymongo
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def mars_scrape():

    browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # news_title = soup.title.text.find('a', .content_title)
    # news_paragraph = soup.body.find('p', .article_teaser_body)
    element = soup.select_one('ul.item_list li.slide')

    news_title = element.find('div', class_="content_title").get_text()
    # news_title

    news_paragraph = element.find('div', class_="article_teaser_body").get_text()
    # news_paragraph

    mars_data = {
        "news_article": news_title,
        "news_paragraph": news_paragraph,
        }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data


    # html = browser.html
    # soup = bs(html, "html.parser")






    # news = soup.find_all('div', class_="image_and_description_container")



    # featured_image_url = ('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + href)




