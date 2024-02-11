import time
import pyupbit
import datetime

access = "w40NyLOUuaWMVQu2Ij4Pd3vJNCItU3QwQ4Wgl3CR"
secret = "7qewsv3iebKqqZyh2dDx1myxg61sk63OE6FqT2Fh"

def calculate_macd(df, short_window=12, long_window=26, signal_window=9):
    """MACD 지표 계산"""
    df['EMA_short'] = df['trade_price'].ewm(span=short_window, min_periods=1).mean()
    df['EMA_long'] = df['trade_price'].ewm(span=long_window, min_periods=1).mean()
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

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        df = pyupbit.get_ohlcv("KRW-XRP", interval="minute1", count=100) # 1분 봉 데이터 가져오기
        calculate_macd(df) # MACD 계산
        
        if df['MACD'].iloc[-1] > df['Signal_Line'].iloc[-1] and df['MACD'].iloc[-2] <= df['Signal_Line'].iloc[-2]:
            krw = get_balance("KRW")
            if krw > 5000:
                upbit.buy_market_order("KRW-XRP", krw*0.9995)
        elif df['MACD'].iloc[-1] < df['Signal_Line'].iloc[-1] and df['MACD'].iloc[-2] >= df['Signal_Line'].iloc[-2]:
            xrp = get_balance("XRP")
            if xrp > 0.01:
                upbit.sell_market_order("KRW-XRP", xrp*0.9995)
                
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)