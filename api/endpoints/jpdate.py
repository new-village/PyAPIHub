# api/endpoints/jpdate.py
from fastapi import APIRouter, HTTPException
from jpdatetime import jpdatetime

router = APIRouter()

@router.get("/strptime/{jp_date}")
async def strptime(jp_date: str):    
    try:
        # 和暦の日付文字列をパース
        date_obj = jpdatetime.strptime(jp_date, "%G年%m月%d日")
        # 西暦の日付文字列に変換
        return {"date_str": date_obj.strftime("%Y-%m-%d")}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Japanese date format")
    except Exception:
        # その他の予期しないエラー
        raise HTTPException(status_code=500, detail="Internal Server Error.")

@router.get("/strftime/{iso_date}")
async def strftime(iso_date: str):    
    try:
        # 西暦の日付文字列をパース
        date_obj = jpdatetime.strptime(iso_date, "%Y-%m-%d")
        # 和暦の日付文字列に変換
        return {"date_str": date_obj.strftime("%-G年%m月%d日")}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Gregorian date format")
    except Exception as e:
        print(e)
        # その他の予期しないエラー
        raise HTTPException(status_code=500, detail="Internal Server Error.")
