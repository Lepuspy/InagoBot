#-*-coding:utf-8-*-
import pybitflyer
from inago import InagoFlyer

inago = InagoFlyer()


# ユーザー定義
#--------------------------------#
AVG = 20		# 平均取得秒数 
LOW = 30		# 不足しきい値
TIE = 30		# 引き分け判定しきい値
Position = 0	# 初期ポジション指定(0: No, 1: Buy, -1: Sell)
LOT = 0.01 		# 1回のトレード枚数


KEY = ""		# APIキー
SECRET = ""		# APIシークレットキー
# BitFlyerの場合 (FX_BTC_JPY or BTC_JPY)
Pair = "FX_BTC_JPY" 
#--------------------------------#

# 変数初期化
Merit = None
api = pybitflyer.API(api_key=KEY, api_secret=SECRET)


def Market(side):
    global Position
    ret = api.sendchildorder(product_code=Pair,
                        child_order_type="MARKET",
                        side=side,
                        size=LOT,
                        minute_to_expire=10000,
                        time_in_force="GTC"
                        )
    if "child_order_acceptance_id" in ret:
        Position += 1 if Merit == "Buy" else -1
        print(ret["child_order_acceptance_id"])
    else:
        print(ret)
    return ret


# メインループ
for volume in inago.VolumeGet():
    # 売買勢力が変わった場合
    if volume["Merit"] != Merit:
        Merit = volume["Merit"]
        # 売買勢力が買いor売り
        if Merit in ["Buy","Sell"]:
            # ポジションを現在持っているならドテン
            if Position != 0:
                Market(Merit.upper())
            Market(Merit.upper())
        print(Merit)
