from fastapi import FastAPI
from fastapi.responses import RedirectResponse  # RedirectResponseをインポート
from app.api.endpoints import jpdate

app = FastAPI(
    title="PyAPIHub",
    description="This API provides a web interface to test the input and output functionalities of the Python libraries developed by new-village.",
    version="1.0.0"
)

app.include_router(jpdate.router)

@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")  # RedirectResponseを正しく使用
