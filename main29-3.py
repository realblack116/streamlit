import streamlit as st
import datetime
import pyupbit

d = st.date_input( # 날짜 선택 부분
    "날짜를 선택하세요",
    datetime.date.today())

st.write('비트코인 1일 차트') # 제목

ticker = 'KRW-BTC' # 코인 종류
interval = 'minute60'# 1시간마다 기록하는 데이터
to = str(d + datetime.timedelta(days=1)) # ~까지의 데이터
count = 24
price_now = pyupbit.get_ohlcv(ticker=ticker,interval=interval,to=to,count=count) # 가격 데이터 가져오기

st.line_chart(price_now.close) # 그래프 그리기