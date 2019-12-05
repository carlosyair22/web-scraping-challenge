from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests

def mars_news():
    #Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text; return both
    news_url="https://mars.nasa.gov/news/"
    response=requests.get(news_url)
    soup=BeautifulSoup(response.text,'html.parser')
    result=soup.find_all('div',class_='slide')[0]
    news_title=result.find('div',class_='content_title').a.text
    news_paragraph=result.find('div',class_='rollover_description_inner').text
    return news_title, news_paragraph

def scrape_image(browser):
    #Use splinter to navigate the site and find the image url for the current Featured Mars Image. Return the url
    url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    browser.click_link_by_partial_text('FULL IMAGE')
    while browser.is_text_present("more info")==False:
        html=browser.html
        soup = BeautifulSoup(html, 'html.parser')
    else:
        browser.click_link_by_partial_text("more info")
        html=browser.html
        soup = BeautifulSoup(html, 'html.parser')
        partial_url=soup.find('img',class_="main_image").get('src')
        featured_image_url=f"https://www.jpl.nasa.gov{partial_url}"
        return featured_image_url

def scrape_twitter(browser):
    #Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. Return the weather report 
    url="https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    tweet=soup.find('div',attrs={"class":"tweet","data-name": "Mars Weather"})
    tweet_text=tweet.find('p')
    mars_weather=tweet_text.get_text()
    return mars_weather

def scrape_facts():
    # Use Read HTML method to load the table into a dataframe. Select the fist table and return it
    mars_fact_df=pd.read_html('https://space-facts.com/mars/')[0]
    mars_fact_df.columns=["Measure", "Value"]
    return mars_fact_df.to_html()

def scrape_hemispheres(browser):
    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    hemisphere_list=[]
    hemisphere_names=['Cerberus','Schiaparelli','Syrtis','Valles']
    for hemi in hemisphere_names:
        hemisphere={}
        browser.visit(url)
        browser.click_link_by_partial_text(hemi)
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
        sample = browser.find_link_by_text("Sample").first
        hemisphere["url"] = sample['href']
        hemisphere['title']=soup.find('h2',class_="title").text
        hemisphere_list.append(hemisphere)
    return hemisphere_list

def scrape_all():
    news_title, news_paragraph = mars_news()
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    featured_image_url=scrape_image(browser)
    weather_tweet=scrape_twitter(browser)
    mars_facts=scrape_facts()
    hemisphere_list=scrape_hemispheres(browser)
    mars={
        "news_title":news_title,
        "news_paragraph":news_paragraph,
        "featured_image_url":featured_image_url,
        "weather_tweet":weather_tweet,
        "mars_facts":mars_facts,
        "hemisphere_list":hemisphere_list
    }
    print("------------------------------FIN")
    browser.quit()
    return mars