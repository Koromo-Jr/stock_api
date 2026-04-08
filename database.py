from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. 買一塊建地 (建立 SQLite 資料庫檔案，檔名叫 stock.db)
SQLALCHEMY_DATABASE_URL = "sqlite:///./stock.db"

# 2. 請一個地基工程師 (Engine)
# connect_args={"check_same_thread": False} 這是 SQLite 專屬的防呆機制，照抄就好！
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. 建立一個「會議室」(SessionLocal)，以後我們 API 要拿資料、存資料，都要透過這個會議室
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 準備好建築藍圖的底稿 (Base)，我們等下設計的資料表都要繼承它
Base = declarative_base()