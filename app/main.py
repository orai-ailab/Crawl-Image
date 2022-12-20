"""
Copyright 2022 hoangks5

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException, StaleElementReferenceException
import platform
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os.path as osp
from pexels_api import API
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Form
load_dotenv()
app = FastAPI(
    title="API Crawl",
    description="",
    version="1.0",
    docs_url='/crawl/docs',
    openapi_url='/openapi.json', # This line solved my issue, in my case it was a lambda function
    redoc_url='/crawl/redoc'
)

def create_browser(no_gui=False, proxy=None):
        
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        if no_gui:
            chrome_options.add_argument('--headless')
        if proxy:
            chrome_options.add_argument("--proxy-server={}".format(proxy))
        browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

        browser_version = 'Failed to detect version'
        chromedriver_version = 'Failed to detect version'
        major_version_different = False

        if 'browserVersion' in browser.capabilities:
            browser_version = str(browser.capabilities['browserVersion'])

        if 'chrome' in browser.capabilities:
            if 'chromedriverVersion' in browser.capabilities['chrome']:
                chromedriver_version = str(browser.capabilities['chrome']['chromedriverVersion']).split(' ')[0]

        if browser_version.split('.')[0] != chromedriver_version.split('.')[0]:
            major_version_different = True
        print('_________________________________')
        print('Current web-browser version:\t{}'.format(browser_version))
        print('Current chrome-driver version:\t{}'.format(chromedriver_version))
        if major_version_different:
            print('warning: Version different')
            print(
                'Download correct version at "http://chromedriver.chromium.org/downloads" and place in "./chromedriver"')
        print('_________________________________')
        return browser
    
    
def get_scroll(self):
        pos = self.browser.execute_script("return window.pageYOffset;")
        return pos

def wait_and_click(self, xpath):
    #  Sometimes click fails unreasonably. So tries to click at all cost.
    try:
        w = WebDriverWait(self.browser, 15)
        elem = w.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        elem.click()
        self.highlight(elem)
    except Exception as e:
        print('Click time out - {}'.format(xpath))
        print('Refreshing browser...')
        self.browser.refresh()
        time.sleep(2)
        return self.wait_and_click(xpath)

    return elem

def highlight(self, element):
    self.browser.execute_script("arguments[0].setAttribute('style', arguments[1]);", element,
                                "background: yellow; border: 2px solid red;")


def remove_duplicates(_list):
    return list(dict.fromkeys(_list))


def naver_(browser, keyword, add_url=""):
    browser.get(
        "https://search.naver.com/search.naver?where=image&sm=tab_jum&query={}{}".format(keyword, add_url))

    time.sleep(1)
    links = []
    
    
    print('Scrolling down')
    elem = browser.find_element(By.TAG_NAME, "body")

    for i in range(60):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)

    imgs = browser.find_elements(By.XPATH,
                                    '//div[@class="photo_bx api_ani_send _photoBox"]//img[@class="_image _listImage"]')

    print('Scraping links')

    

    for img in imgs:
        try:
            src = img.get_attribute("src")
            if src[0] != 'd':
                links.append(src)
        except Exception as e:
            print('[Exception occurred while collecting links from naver] {}'.format(e))

    links = remove_duplicates(links)

    print('Collect links done. Site: {}, Keyword: {}, Total: {}'.format('naver', keyword, len(links)))
    browser.close()
    print(len(links))
    return links

    

    

def flickr_(browser, keyword, page, add_url=""):
    links = []
    for i in range(page):
        browser.get(
            "https://flickr.com/search/?text="+keyword+"&view_all="+str(page)+add_url)

        time.sleep(1)
        print('Scrolling down') 

        elem = browser.find_element(By.TAG_NAME, "body")

        for i in range(60):
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)

        imgs = browser.find_elements(By.XPATH,
                                        '//*[@class="photo-list-photo-container"]/img')

        print('Scraping links')
        for img in imgs:
            try:
                src = img.get_attribute("src")
                if src[0] != 'd':
                    links.append(src)
            except Exception as e:
                print('[Exception occurred while collecting links from naver] {}'.format(e))

    links = remove_duplicates(links)
    print('Collect links done. Site: {}, Keyword: {}, Total: {}'.format('naver', keyword, len(links)))
    browser.close()
    return links


def pexels_(keyword, page):
    PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
    api = API(PEXELS_API_KEY)
    links = []

    for i in range(1, page, 1):
        api.search(keyword, page=i, results_per_page=80)
        photos = api.get_entries()
        for photo in photos:
            links.append(photo.original)
    links = remove_duplicates(links)
    return links






@app.post("/crawl/naver")
async def naver(label: str = Form(description='label text')
                ):
    """Crawl Image From Naver.com (~ 400 image)

    Args:
        label (str, optional): _description_. Defaults to Form(description='label text').

    Returns:
        _type_: _description_ 
    """
    browser = create_browser(no_gui=True, proxy=False)
    links = naver_(browser=browser,keyword=label,add_url='&face=1')
    res = {
        'data': links
    }
    return res

@app.post("/crawl/flickr")
async def flickr(label: str = Form(description='label text'),
                 page: int = Form(description='1 page =~ 200-300 image')
                ):
    """Crawl Image From Flickr.com

    Args:
        label (str, optional): _description_. Defaults to Form(description='label text').
        page (int, optional): _description_. Defaults to Form(description='number page').

    Returns:
        _type_: _description_
    """
    browser = create_browser(no_gui=True, proxy=False)
    links = flickr_(browser=browser,keyword=label,page=page,add_url='')
    res = {
        'data': links
    }
    return res


@app.post("/crawl/pexels")
async def pexels(label: str = Form(description='label text'),
                 page: int = Form(description='1 page =~ 80 image')
                ):
    """Crawl Image From Pexels.com

    Args:
        label (str, optional): _description_. Defaults to Form(description='label text').
        page (int, optional): _description_. Defaults to Form(description='number page').

    Returns:
        _type_: _description_
    """
    links = pexels_(keyword=label,page=page)
    res = {
        'data': links
    }
    return res