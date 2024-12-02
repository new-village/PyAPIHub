# main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api.endpoints import jpdate, keiba

app = FastAPI(
    title="Keiba Scraper API",
    description="This API provides a web interface to test the input and output functionalities of the Python libraries developed by new-village.",
    version="1.0.0"
)

# ルーターをインクルード
app.include_router(jpdate.router, prefix="/api/jpdate", tags=["jpdate"])
app.include_router(keiba.router, prefix="/api/keiba", tags=["Keiba"])

# ルートエンドポイント（オプション）
@app.get("/")
def read_root():
    return {"message": "Welcome to my API"}
