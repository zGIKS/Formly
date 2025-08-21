from pydantic import BaseModel, Field
from typing import List, Optional

class OptionDTO(BaseModel):
    id: str
    text: str
    image: Optional[str]
    score: int = 0

class QuestionCreateDTO(BaseModel):
    form_id: str
    text: str
    type: str = Field(..., regex='^(MULTIPLE_CHOICE|CHECKBOXES|TEXT)$')
    image: Optional[str]
    options: Optional[List[OptionDTO]]

    class Config:
        orm_mode = True
