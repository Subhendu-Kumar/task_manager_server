from pydantic import BaseModel, EmailStr


class SignupUser(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginUser(BaseModel):
    email: EmailStr
    password: str
