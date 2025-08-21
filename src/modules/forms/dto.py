from pydantic import BaseModel, Field
from typing import Optional, List

class FormCreateDTO(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str]
    font_family: Optional[str]
    background_image: Optional[str]
    slug: Optional[str]
    score_ranges: Optional[List[dict]]  # [{'min':0,'max':5,'message':'...'}]

    class Config:
        orm_mode = True
