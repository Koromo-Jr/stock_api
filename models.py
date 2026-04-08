from sqlalchemy import Column, Integer, String, DateTime
import datetime
from database import Base # 把剛剛 database.py 裡面的底稿拿過來用

# 定義我們的第一張資料表：Watchlist (自選股清單)
class Watchlist(Base):
    # __tablename__ 就是這張表在資料庫裡面的真實名稱
    __tablename__ = "watchlist"

    # 開始設定欄位 (就像 Excel 的直行)
    
    # 第 1 欄：身分證字號 (主鍵)，每一筆資料都會有獨一無二的號碼 (1, 2, 3...)
    id = Column(Integer, primary_key=True, index=True)
    
    # 第 2 欄：股票代碼 (例如 NVDA, 2330.TW)
    # unique=True 是一個超棒的防呆：防止你不小心把同一檔股票加進清單兩次！
    ticker = Column(String, unique=True, index=True)
    
    # 第 3 欄：加入清單的時間
    # default=datetime.datetime.utcnow 會讓系統自動幫你填上當下的時間，不用自己寫！
    added_at = Column(DateTime, default=datetime.datetime.utcnow)