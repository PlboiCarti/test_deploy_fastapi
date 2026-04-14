# Connecting
from sqlalchemy import create_engine
# Declare a mapping
from sqlalchemy.ext.declarative import declarative_base
# Creating a Session
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///./blog.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread" : False}
    # Đây là cấu hình quan trọng khi dùng SQLite. Mặc định, SQLite chỉ cho phép một luồng (thread) truy cập để đảm bảo an toàn. Tuy nhiên, trong các web framework như FastAPI, nhiều luồng có thể cùng xử lý một yêu cầu, nên ta cần tắt kiểm tra này để tránh lỗi.
)

SessionLocal = sessionmaker(bind = engine, autocommit = False, autoflush=False)
# ---> Tạo các phiên làm việc với CSDL
# autocommit = False --> Ngăn việc tự động lưu thay đổi. Bạn phải gọi db.commit() một cách thủ công. Điều này giúp bạn kiểm soát giao dịch (transaction) tốt hơn—nếu có lỗi xảy ra, bạn có thể rollback lại toàn bộ.
# autoflush=False --> Ngăn việc tự động đẩy dữ liệu lên DB trước khi bạn gửi truy vấn. Điều này giúp tối ưu hiệu suất và kiểm soát dữ liệu chờ xử lý.

Base = declarative_base() # Tất cả các Model (các lớp đại diện cho bảng trong database) mà bạn tạo sau này sẽ phải kế thừa từ Base này.

def get_db():
    db = SessionLocal() # Bước 1: Mở cửa (Tạo kết nối)
    try:
        yield db # Bước 2: "Cho mượn" kết nối và TẠM DỪNG tại đây

        # --- Lúc này FastAPI sẽ lấy 'db' để đi chạy các hàm @app.post hoặc @app.get của bạn ---
    finally:
        db.close() # Bước 3: Sau khi API chạy xong, hàm quay lại đây và Đóng cửa