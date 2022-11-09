from fastapi import FastAPI, Form
import co

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
    main.AutoCrawler((skip_already_exist=_skip, n_threads=_threads,
                          do_flickr=_flickr, do_naver=_naver,do_pexels=_pexels, full_resolution=_full,
                          face=_face, no_gui=_no_gui, limit=_limit, proxy_list=_proxy_list))
    