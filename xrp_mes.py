import time
import pyupbit
import datetime
import requests
import json

access = "w40NyLOUuaWMVQu2Ij4Pd3vJNCItU3QwQ4Wgl3CR"
secret = "7qewsv3iebKqqZyh2dDx1myxg61sk63OE6FqT2Fh"
webhook_url = "https://discordapp.com/api/webhooks/1205022458265079818/X9hl7WmShq1G4ybUGHGjHbHmAtZUK6UMkPhesev8qaXvKMMmoSjinFPypG4J0-PJu3_8"

def calculate_macd(df, short_window=12, long_window=26, signal_window=9):
    """MACD 지표 계산"""
    df['EMA_short'] = df['close'].ewm(span=short_window, min_periods=1).mean()
    df['EMA_long'] = df['close'].ewm(span=long_window, min_periods=1).mean()
    df['MACD'] = df['EMA_short'] - df['EMA_long']
    df['Signal_Line'] = df['MACD'].ewm(span=signal_window, min_periods=1).mean()

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

def send_discord_message(content):
    """Discord로 메시지 보내기"""
    data = {
        "content": content
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    if response.status_code != 204:
        print("Failed to send message to Discord")

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        df = pyupbit.get_ohlcv("KRW-XRP", interval="minute30", count=100) # 30분 봉 데이터 가져오기
        calculate_macd(df) # MACD 계산
        
        if df['MACD'].iloc[-1] > df['Signal_Line'].iloc[-1] and df['MACD'].iloc[-2] <= df['Signal_Line'].iloc[-2]:
            krw = get_balance("KRW")
            if krw > 5000:
                upbit.buy_market_order("KRW-XRP", krw*0.9995)
                send_discord_message("매수 주문이 실행되었습니다.")
        elif df['MACD'].iloc[-1] < df['Signal_Line'].iloc[-1] and df['MACD'].iloc[-2] >= df['Signal_Line'].iloc[-2]:
            xrp = get_balance("XRP")
            if xrp > 10:
                upbit.sell_market_order("KRW-XRP", xrp*0.9995)
                send_discord_message("매도 주문이 실행되었습니다.")
                
        time.sleep(1)
    except Exception as e:
        error_message = f"에러 발생: {str(e)}"
        print(error_message)
        send_discord_message(error_message)
        time.sleep(1)