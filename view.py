# Display Current Price
while True :
    now = datetime.datetime.now()
    # 매도 시도
    if now.hour == 8 and now.minute == 49 and 50 <= now.second <= 59:
        if op_mode is True and hold is True :
            eth_balance = upbit.get_balance("KRW-BTC")
            upbit.sell_market_order("KRW-BTC", eth_balance)
            logging.debug("매도 : "+ str(eth_balance))
            hold = False
        op_mode = False
        time.sleep(10)
        
    # 09시 목표가 갱신 # 09:00 후로 설정, upbit 기준 09시에 목표값이 갱신됨
    if now.hour == 9 and now.minute == 0 and (20<=now.second <= 30) :
        target = cal_target("KRW-BTC")
        print("목표가 :", target)
        op_mode = True 
    # 현재가 확인
    cur_price = pyupbit.get_current_price("KRW-BTC")
    
    # 매초마다 조건을 확인한 후 매수 시도
    print(now,cur_price)
    if op_mode is True and cur_price >= target and hold is False :
        buy_price = 1000000
        # 매수
        balance = upbit.get_balance(ticker="KRW")
        upbit.buy_market_order('KRW-BTC', buy_price)
        logging.debug("매수 : "+ str(buy_price))
        hold = True 
        
    print(f"현재 시간: {now} 목표가: {target} 현재가: {cur_price} 보유상태: {hold} 동작상태: {op_mode}")
    time.sleep(1)

# #%%
# # [BTC order]
# # # print(upbit.buy_limit_order("KRW-BTC", 41840000, 1)) #입력 금액에 BTC 1개 매수
# # # print(upbit.sell_limit_order("KRW-BTC", 50000000, 1)) #입력 금액에 BTC 1개 매도
# print(upbit.buy_market_order("KRW-BTC", 0)) #BTC 10,000원어치 시장가 매수
# # # print(upbit.sell_market_order("KRW-BTC", 1))  #BTC 1개 시장가매도
# 
# # [XRP order]
# # # print(upbit.buy_limit_order("KRW-XRP", 500, 20)) #500원에 리플20개 매수
# # # print(upbit.sell_limit_order("KRW-XRP", 500, 20)) #500원에 리플20개 매도
# # print(upbit.buy_market_order("KRW-XRP", 10000)) #리플 10000원어치 시장가 매수
# # # print(upbit.sell_market_order("KRW-XRP", 30))  #리플 30개 시장가매도
# 
# #시장가 매수 매도는 매수할때는 원화, 매도할때는 매도수량 값을 넘깁니다.
# # ret = upbit.buy_limit_order("KRW-XRP", 100, 20)    # Buy
# # ret = upbit.sell_limit_order("KRW-XRP", 1000, 10)  # Sell
# # print(ret)
# 
# # [order cnacle]
# # uuid = ret['uuid'] # 주문번호 얻기
# # print(uuid)
# # ret = upbit.cancel_order(uuid) # 주문 취소
# # print(ret)
