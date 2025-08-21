from pydantic import BaseModel, EmailStr

class LoginDTO(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
