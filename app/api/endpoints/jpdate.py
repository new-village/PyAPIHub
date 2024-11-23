from fastapi import APIRouter, HTTPException
from app.models.date_input import DateInput
from app.schemas.date_output import DateOutput
from jpdatetime import jpdatetime

router = APIRouter(prefix="/jpdate", tags=["jpdate"])

@router.post("/strptime", response_model=DateOutput)
async def strptime(date_input: DateInput):
    try:
        # 和暦の日付文字列をパース
        date_obj = jpdatetime.strptime(date_input.date_str, "%G年%m月%d日")
        # 西暦の日付文字列に変換
        return {"date_str": date_obj.strftime("%Y-%m-%d")}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Japanese date format")

@router.post("/strftime", response_model=DateOutput)
async def strftime(date_input: DateInput):
    try:
        # 西暦の日付文字列をパース
        date_obj = jpdatetime.strptime(date_input.date_str, "%Y-%m-%d")
        # 和暦の日付文字列に変換
        return {"date_str": date_obj.strftime("%-G年%m月%d日")}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Gregorian date format")
