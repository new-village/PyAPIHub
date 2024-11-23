from pydantic import BaseModel

class DateInput(BaseModel):
    date_str: str
