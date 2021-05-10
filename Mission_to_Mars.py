

# Imports 
from splinter import Browser
from bs4 import BeautifulSoup as soup 
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 
import datetime as dt 


def scrape_all():
    # executable path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data 


def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the webpage
    browser.is_element_not_present_by_css('div.list_text', wait_time=1)
    # setting up html parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')
        # finding and saving the news articles title
        news_title = slide_elem.find('div', class_='content_title').get_text()       
        # finding and saving article summary paragraph
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p


def featured_image(browser):
    # URL for image
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Finding the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # adding base URL to cereate and an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    df.columns = ['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    return df.to_html(classes="table table-striped")

if __name__ == "__main__":
    print(scrape_all())

    








