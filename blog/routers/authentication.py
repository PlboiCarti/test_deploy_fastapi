from fastapi import APIRouter, Depends, HTTPException, status
from blog import schemas, models, token
from blog.database import get_db
from blog.hashing import Hash
from sqlalchemy.orm import Session
from blog.schemas import Token

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)

# @router.post('/login')
# def login(request:schemas.Login, db:Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.email == request.username).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"Invalid Credentials")
    
#     if not Hash.verify(user.password, request.password):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'Incorrect Password')
    
#     # generate a JWT and return 
#     access_token = token.create_access_token(data={"sub": user.email})
#     return Token(access_token=access_token, token_type="bearer")
#     # # data={"sub": user.email} --> Dùng để xác định thực thể mà token này đại diện (thường là User ID hoặc Email).
#     # # Khi server nhận lại token này từ người dùng trong các request sau, nó sẽ giải mã token, nhìn vào trường sub để biết "À, người đang gửi request này chính là user có email này".

# ================================================================================================
"""
Theo tiêu chuẩn OAuth2, khi bạn điền username và password vào bảng "Authorized", Swagger sẽ gửi 
một yêu cầu POST tới URL /login với dữ liệu ở dạng Form Data (giống như gửi một cái 
form HTML truyền thống).
 --> schemas.Login là một Pydantic model, FastAPI sẽ mặc định đợi một dữ liệu dạng JSON.
 --> request: OAuth2PasswordRequestForm = Depends() thay vì request:schemas.Login
"""
@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Invalid Credentials")
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Incorrect Password')
    
    # generate a JWT and return 
    access_token = token.create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")
    # # data={"sub": user.email} --> Dùng để xác định thực thể mà token này đại diện (thường là User ID hoặc Email).
    # # Khi server nhận lại token này từ người dùng trong các request sau, nó sẽ giải mã token, nhìn vào trường sub để biết "À, người đang gửi request này chính là user có email này".