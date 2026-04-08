from fastapi import FastAPI, HTTPException, Depends
import yfinance as yf
from sqlalchemy.orm import Session
import models, database

# 建立 FastAPI 總機
app = FastAPI()

# 在啟動時建立資料表 (這行很重要，它是幫你在 SQLite 裡蓋房子的動作)
models.Base.metadata.create_all(bind=database.engine)

# 取得資料庫連線的小工具 (Dependency Injection)
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 功能 1：抓取最新報價 ---
@app.get("/quote/{ticker}")
def get_stock_quote(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        # 【修正點】改抓 period="5d"，確保我們一定拿得到「昨天」的收盤價
        hist = stock.history(period="5d")
        
        if hist.empty or len(hist) < 2:
            raise HTTPException(status_code=404, detail=f"找不到代碼或歷史資料不足：{ticker}")
            
        latest_price = hist['Close'].iloc[-1]
        open_price = hist['Open'].iloc[-1]
        yesterday_price = hist['Close'].iloc[-2] # 拿倒數第二筆，就是昨收
        change_percent = ((latest_price - yesterday_price) / yesterday_price) * 100

        return {
            "stock_symbol": ticker.upper(),
            "open_price": round(open_price, 2),
            "latest_price": round(latest_price, 2),
            "change_percent": f"{round(change_percent, 2)}%",
            "message": "這是您要的最新報價！"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"伺服器錯誤：{str(e)}")

# --- 功能 2：新增到自選清單 (POST) ---
@app.post("/watchlist/{ticker}")
def add_to_watchlist(ticker: str, db: Session = Depends(get_db)):
    # 統一轉大寫，避免 2330.tw 和 2330.TW 被判定成不同股票
    ticker_upper = ticker.upper()
    
    # 防呆：檢查是否重複
    exists = db.query(models.Watchlist).filter(models.Watchlist.ticker == ticker_upper).first()
    if exists:
        raise HTTPException(status_code=400, detail="這檔股票已經在清單中囉！")
    
    # 存入資料庫
    new_stock = models.Watchlist(ticker=ticker_upper)
    db.add(new_stock)
    db.commit()
    
    return {"message": f"成功將 {ticker_upper} 加入自選清單！"}