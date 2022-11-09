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

load_dotenv()

app = FastAPI(
    title="API for AI Market",
    description="",
    version="1.0",
    docs_url='/docs',
    openapi_url='/openapi.json', # This line solved my issue, in my case it was a lambda function
    redoc_url='/redoc'
)


def __init__(self, no_gui=False, proxy=None):
        executable = ''
        if platform.system() == 'Windows':
            print('Detected OS : Windows')
            executable = './chromedriver/chromedriver_win.exe'
        elif platform.system() == 'Linux':
            print('Detected OS : Linux')
            executable = './chromedriver/chromedriver_linux'
        elif platform.system() == 'Darwin':
            print('Detected OS : Mac')
            executable = './chromedriver/chromedriver_mac'
        else:
            raise OSError('Unknown OS Type')

        if not osp.exists(executable):
            raise FileNotFoundError('Chromedriver file should be placed at {}'.format(executable))

        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        if no_gui:
            chrome_options.add_argument('--headless')
        if proxy:
            chrome_options.add_argument("--proxy-server={}".format(proxy))
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

        browser_version = 'Failed to detect version'
        chromedriver_version = 'Failed to detect version'
        major_version_different = False

        if 'browserVersion' in self.browser.capabilities:
            browser_version = str(self.browser.capabilities['browserVersion'])

        if 'chrome' in self.browser.capabilities:
            if 'chromedriverVersion' in self.browser.capabilities['chrome']:
                chromedriver_version = str(self.browser.capabilities['chrome']['chromedriverVersion']).split(' ')[0]

        if browser_version.split('.')[0] != chromedriver_version.split('.')[0]:
            major_version_different = True







@app.post("/naver")
async def naver(label: str = Form(description='label text')
                ):
    """Crawl Image From Naver.com (~ 400 image)

    Args:
        label (str, optional): _description_. Defaults to Form(description='label text').

    Returns:
        _type_: _description_ 
    """
    collect = CollectLinks(no_gui=True, proxy=False)
    links = collect.naver(keyword=label,add_url='&face=1')
    res = {
        'data': links
    }
    return res

@app.post("/flickr")
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
    collect = CollectLinks(no_gui=True, proxy=False)
    links = collect.flickr(keyword=label,page=page,add_url='')
    res = {
        'data': links
    }
    return res


@app.post("/pexels")
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
    collect = CollectLinks(no_gui=True, proxy=False)
    links = collect.pexels(keyword=label,page=page,add_url='')
    res = {
        'data': links
    }
    print(len(links))
    return res