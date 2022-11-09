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
    """Crawl Image From Naver (~ 400 image)

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
async def flickr(label: str = Form(description='label text')
                ):
    """Crawl Image From Naver (~ 400 image)

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