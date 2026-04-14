# Schema là cách dữ liệu "giao tiếp" với người dùng qua API.

from pydantic import BaseModel
from typing import List

class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    class Config():
        from_attributes = True
    
class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    name:str
    email:str
    blogs:List[Blog] = []

    class Config():
        from_attributes = True

# Tạo 1 response model chỉ kế thừa title và body của Blog mà ko hiển thị index
# --> Được áp dụng cho việc không muốn trả về những dữ liệu nhạy cảm cho backend
class ShowBlog(BaseModel):
    title:str
    body:str
    creator: ShowUser
    
    class Config():
        from_attributes = True
        """ 
        from_attributes = True --> cho phép Pydantic đọc được dữ liệu từ các 
                                Object (đối tượng) thay vì chỉ đọc được Dictionary.
        """

class Login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None