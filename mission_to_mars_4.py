#!/usr/bin/env python
# coding: utf-8

# In[1]:


from splinter import Browser
import pymongo
from bs4 import BeautifulSoup as bs


# In[2]:

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=True)


def scrape():


    browser = init_browser()
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

     # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the first div 
    news = soup.find("div", class_="list_text")

    # Get the headline
    title = news.find("a").text

    # Get the body
    body = news.find("div", class_="article_teaser_body").text
    
    
    browser.quit()


    browser = init_browser()
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

     # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    results = soup.find("footer")

    # Get the first div 
    relative_path = results.find("a")["data-fancybox-href"]

    # Get the img
    featured_image_url = "https://www.jpl.nasa.gov" + relative_path
    
       
    browser.quit()


    browser = init_browser()
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

     # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    
      
   
    browser.quit()


    def facts():
        import pandas as pd
        url = "https://space-facts.com/mars/"

        tables = pd.read_html(url)
        facts_df= tables[0]
        facts_df.columns = ["description", "value"]
        facts_df.set_index("description", inplace = True)
    
        return facts_df.to_html(classes="table table-striped")

    browser = init_browser()
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)


        
    html = browser.html
    soup = bs(html, "html.parser")
    hemisphere_image_urls = []
    
    results = soup.find_all("div", class_="description")
    for result in results:
        title = result.find("a").text
        href = result.find("a")["href"]
        browser.quit()
        browser = init_browser()
        browser.visit("https://astrogeology.usgs.gov"+href)
        html = browser.html
        soup_2 = bs(html, "html.parser")
        results_2 = soup_2.find_all("div", class_="downloads")
        for results in results_2:
            image_url = results.find("li")
            url = image_url.find("a")["href"]
            hemisphere_image_urls.append({"title":title, "image_url":url})  
           
   
    browser.quit()


    mars_data = {
        "title": title,
        "body": body,
        "feat_img": featured_image_url, 
        "weather": weather, 
        "facts": facts(),
        "hemisphere_urls": hemisphere_image_urls
    }


    return mars_data


# In[ ]:




