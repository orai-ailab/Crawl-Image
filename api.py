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
async def naver(label: str = Form(description='label text'),
                page: int = Form(description='Page crawl (1 page about 80 image)')
                ):
    collect = CollectLinks(no_gui=True, proxy=False)
    links = collect.naver(keyword=label,add_url='&face=1')
    res = {
        'data': links
    }
    return res
     