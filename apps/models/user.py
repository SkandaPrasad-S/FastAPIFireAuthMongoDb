from pydantic import BaseModel

class UserRegister(BaseModel):
    user_fullname: str
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "fullname" : "samplegoal",
                "email": "sample@gmail.com",
                "password": "samplepass123"
            }
        }

class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "sample@gmail.com",
                "password": "samplepass123"
            }
        }
