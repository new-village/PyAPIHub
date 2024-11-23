from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from jpdatetime import jpdatetime

app = FastAPI(
    title="PyAPIHub",
    description="This API provides a web interface to test the input and output functionalities of the Python libraries developed by new-village.",
    version="1.0.0"
)

class DateInput(BaseModel):
    date_str: str

@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.post("/jpdate/strptime")
async def strptime(date_input: DateInput):
    try:
        # 和暦の日付文字列をパース
        date_obj = jpdatetime.strptime(date_input.date_str, "%G年%m月%d日")
        # 西暦の日付文字列に変換
        return {"gregorian_date": date_obj.strftime("%Y-%m-%d")}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Japanese date format")

@app.post("/jpdate/strftime")
async def strftime(date_input: DateInput):
    try:
        # 西暦の日付文字列をパース
        date_obj = jpdatetime.strptime(date_input.date_str, "%Y-%m-%d")
        # 和暦の日付文字列に変換
        return {"japanese_date": date_obj.strftime("%G年%m月%d日")}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Gregorian date format")
