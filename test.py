import pyupbit

access = "w40NyLOUuaWMVQu2Ij4Pd3vJNCItU3QwQ4Wgl3CR"          # 본인 값으로 변경
secret = "7qewsv3iebKqqZyh2dDx1myxg61sk63OE6FqT2Fh"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print("KRW-BORA :",upbit.get_balance("KRW-BORA"))     # KRW-BORA 조회
print("KRW : ",upbit.get_balance("KRW"))         # 보유 현금 조회