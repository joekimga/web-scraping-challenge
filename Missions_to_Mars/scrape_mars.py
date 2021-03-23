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

    # image_path = soup.find_all('img', class_="grey-mars")[0]["src"]

    # mars_img = url + image_path

    # mars_data = {
    #     # "mars_img": mars_img,
    #     "news_article": news_title,
    #     "news_paragraph": news_paragraph,
    #     }

#############  FEATURED MARS IMAGE  ##########

    # browser = init_browser()

    url_image = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url_image)

    time.sleep(1)   

    image_button = browser.find_by_css("button.btn.btn-outline-light")
    image_button.click()

    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, "html.parser")
    # soup = BeautifulSoup(html, "html.parser")

    image_link = jpl_soup.select_one("div.fancybox-inner img").get('src')

    jpl_image = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image_link}'
 
########################  MARS TABLE   ############################
    mars_db = pd.read_html("https://space-facts.com/mars/")[0]
    mars_db

    mars_db.columns=["Mars Description", "Values"]
    mars_db = mars_db.set_index("Mars Description")
    mars_db

    #mars_db.to_html("mars.html") 
    mars_variable = mars_db.to_html()

############## Mars Hemisphere  #######

    astro_base_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(astro_base_url)

    hemisphere_image_urls=[]
    mars_classes = browser.find_by_css('img.thumb')

    for i in range(len(mars_classes)):
    
        visual_images = {}
        browser.find_by_css("img.thumb")[i].click()
        visual_images['title'] = browser.find_by_css("h2.title").text
#     response = requests.get(classes)
#     soup = BeautifulSoup(response.text,'html.parser')
    
#     base_url = "https://astrogeology.usgs.gov/"
        button_sample = browser.find_by_text("Sample")
        button_sample.click()

        visual_images['img_url'] = button_sample["href"]
        #image_path = base_url + image_path
        hemisphere_image_urls.append(visual_images)
        browser.back()

    ############ Dictionary to store variable data
    mars_data = {
        "jpl_image": jpl_image,
        "news_article": news_title,
        "news_paragraph": news_paragraph,
        "mars_variable": mars_variable,
        "hemisphere_image_urls": hemisphere_image_urls
        }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data







