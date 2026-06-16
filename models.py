from pydantic import BaseModel
from typing import Optional

class Quote(BaseModel):
    Quote_id: str
    Quote_number: str
    Customer_Id: str
    Vehicle_id: str
    description_Q: Optional[str] = None
    created_by: Optional[str] = None