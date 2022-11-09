from fastapi import FastAPI, Form


app = FastAPI(
    title="API for AI Market",
    description="",
    version="1.0",
    docs_url='/docs',
    openapi_url='/openapi.json', # This line solved my issue, in my case it was a lambda function
    redoc_url='/redoc'
)

@app.post("/naver")
async def naver(label: str = Form(description='label text')):
    url = "https://gateway.ipfs.airight.io/ipfs/"+input_source_hash
    writer = PdfFileWriter()
    remoteFile = urlopen(Request(url)).read()
    memoryFile = io.BytesIO(remoteFile)
    pdfFile = PdfFileReader(memoryFile)
    for pageNum in range(pdfFile.getNumPages()):
        currentPage = pdfFile.getPage(pageNum)
        writer.addPage(currentPage)
    fileNamePdf = secrets.token_hex(16)+'.pdf'
    outputStream = open(fileNamePdf, "wb")
    writer.write(fileNamePdf)
    outputStream.close()
    pdfFile = open(fileNamePdf, 'rb')
    pdfreader = PyPDF2.PdfFileReader(pdfFile)
    pageObj = ""
    for page in pdfreader.pages:
        pageObj += page.extractText() + "\n"
    fileName = secrets.token_hex(16)+'.txt'
    f = open(fileName, 'w')
    f.write(pageObj)
    f.close()
    url = 'http://128.199.70.52:5001/api/v0/add'
    files = {'file': open(fileName, 'rb')}
    response = requests.post(url, files=files)
    os.remove(fileName)
    os.remove(fileNamePdf)
    return response.json() 