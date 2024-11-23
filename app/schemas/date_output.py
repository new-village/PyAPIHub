from pydantic import BaseModel

class DateOutput(BaseModel):
    date_str: str
