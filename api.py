from fastapi import FastAPI, Form
from collect_links import CollectLinks
import json

app = FastAPI(
    title="API for AI Market",
    description="",
    version="1.0",
    docs_url='/docs',
    openapi_url='/openapi.json', # This line solved my issue, in my case it was a lambda function
    redoc_url='/redoc'
)

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