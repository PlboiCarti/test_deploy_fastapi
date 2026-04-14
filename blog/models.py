# Model là cách dữ liệu nằm trong Database
from sqlalchemy import Column, Integer, String, ForeignKey
from blog.database import Base

from sqlalchemy.orm import relationship

# Define Model
class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key = True,index = True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship('User', back_populates='blogs')
    # back_populates='blogs' --> thiết lập mối quan hệ hai chiều (Bidirectional Relationship) giữa hai Class (hai bảng).


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key= True, index = True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    blogs = relationship('Blog', back_populates='creator')