import os
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import time


def scrape():
    # create dictionary to atore all data
    mars_data_dict = {}

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    # parse html page using Beautiful Soup
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    time.sleep(2)

    # locate latest news title and paragraph, and set variable
    news_title = soup.find('div', class_='content_title').text.strip()
    news_parag = soup.find('div', class_='rollover_description_inner').text.strip()
    mars_data_dict['news_title'] = news_title
    mars_data_dict['news_parag'] = news_parag

    # find featured image and saved it as a variable
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA19334_ip.jpg'
    mars_data_dict['featured_image_url'] = featured_image_url

    # mars weather from twitter
    url_twt = 'https://twitter.com/marswxreport?lang=en'
    responded = requests.get(url_twt)
    soups = bs(responded.text, 'lxml')
    # scrape the latest Mars weather tweet and Save is as a variable called mars_weather.
    wea_tweet = soups.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[3].text
    mars_data_dict['weather_tweet'] = wea_tweet

    #mars facts
    # scrape the table containing facts
    table = pd.read_html('https://space-facts.com/mars/')[0]
    # rename columns
    facts_table = table.rename(columns={table.columns[0]: "Facts"}).rename(columns={table.columns[1]: "Results"})
    mars_data_dict['facts_table'] = facts_table

    #mars hemispheres
    murl = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    response_h = requests.get(murl)
    soup_h = bs(response_h.text, 'lxml')
    time.sleep(2)
    # scrapped Hemisphere's title containing Hemp's name
    titles = soup_h.find_all('h3')

    titles_list = []

    # loop thorugh iterable list, abstract text value and appended each to new list
    for title in titles:
        titles_list.append(title.text)

    # hardcoded img urls, I am not using splinter for obvious reasons
    img_url = ['https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg',
               'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg',
               'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg',
               'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg']

    # saved key-value pairs in a list of dictionaries
    dict_mars = []
    for x in range(0, 4):
        dict_mars.append({'title': titles_list[x], 'imgurl': img_url[x]})

    mars_data_dict['dict_mars'] = dict_mars






    return mars_data_dict






