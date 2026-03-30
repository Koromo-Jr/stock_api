from fastapi import FastAPI, HTTPException
import yfinance as yf

# 建立 FastAPI 總機
app = FastAPI()

@app.get("/quote/{ticker}")
def get_stock_quote(ticker: str):
    try:
        # 1. 召喚 yfinance 小幫手
        stock = yf.Ticker(ticker)
        
        # 2. 抓取最近 1 天的歷史交易資料
        hist = stock.history(period="1d")

        # 這就是工程師的透視眼
        print("\n=== 這是跑腿小弟帶回來的真實資料 ===")
        print(hist)
        print("====================================\n")
        
        # 3. 防呆機制：如果抓回來的資料是空的
        if hist.empty:
            raise HTTPException(status_code=404, detail=f"找不到代碼：{ticker}。台股請記得加上 .TW 或 .TWO 喔！")
            
        # 4. 抽出最新收盤價
        # iloc 的全名是 Index Location（索引定位），意思是「我要指定第幾『橫列 (Row)』」
        # [-1]就是倒數第一個的意思(最後一個)

        # 1. 最新收盤價 (倒數第一筆)
        latest_price = hist['Close'].iloc[-1]
        # 2. 今日開盤價 (倒數第一筆)
        open_price = hist['Open'].iloc[-1]
        # 3. 昨天的收盤價 (倒數第二筆！用 -2 來定位)
        yesterday_price = hist['Close'].iloc[-2]
        # 4. 計算漲跌幅：(今天收盤 - 昨天收盤) / 昨天收盤 * 100
        change_percent = ((latest_price - yesterday_price) / yesterday_price) * 100

        return {
            "stock_symbol": ticker.upper(),
            "open_price": round(open_price, 2),
            "latest_price": round(latest_price, 2),
            "change_percent": f"{round(change_percent, 2)}%", # 加上 % 符號讓它更直覺
            "message": "這是您要的最新報價！"
        }
        
    except HTTPException:
        # 如果是我們自己發出的 404 找不到代碼錯誤，就直接往外丟
        raise
    except Exception as e:
        # 萬一 Yahoo Finance 網路斷線或發生其他未知的錯誤，我們會優雅地擋下來
        raise HTTPException(status_code=500, detail=f"抓取資料時發生異常，可能是網路連線問題。錯誤細節：{str(e)}")