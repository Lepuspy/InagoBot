#-*-coding:utf-8-*-
import numbers
#pip install が必要なモジュール
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

"""InagoFlyer Sell & Buy Volume 取得モジュール"""


__author__ = "Lepus <Twitter @lepus_py>"
__version__ = "3.0"
__date__    = "2018/05/25"






class InagoFlyer:
		
	def __init__(self):
		#chrome.exe を同じディレクトリへ置くこと
		self.NowAvg = 20
		self.BuyVolume = 0
		self.SellVolume = 0	
		self.Merit = None
		self.__AvgTime = 20
		self.__Threshold = 0
		self.__Difference = 0
		options = Options()
		#ヘッドレスモード等オプション設定
		options.add_argument('--headless')
		options.add_argument('--disable-gpu')
		options.add_argument('--ignore-certificate-errors')
		options.add_argument('--allow-running-insecure-content')
		self.Driver = webdriver.Chrome(chrome_options=options)
		self.__Connection()

	@property
	def AvgTime(self):
		return self.__AvgTime
	@AvgTime.setter
	def AvgTime(self, val):
		self.__AvgChange(val)

	@property
	def Threshold(self):
		return self.__Threshold
	@Threshold.setter	
	def Threshold(self, val):
		self.__Threshold = int(val)

	@property
	def Difference(self):
		return self.__Difference
	@Difference.setter
	def Difference(self, val):
		self.__Difference = int(val)
	
	def __AvgChange(self, AvgTime):
		"""
		Action:
			Buy & Sellボリュームの平均秒数変更

		Parameters:
			AvgTime: Number
				floatで指定されても整数に直す

		Raises:
			ValueError:
				AvgTime が 10 ～ 60 の範囲外で設定された
			TypeError:
				AvgTime が 文字で入力された

		"""
		if isinstance(AvgTime, numbers.Number):
			AvgTime = int(AvgTime)
			if self.NowAvg != AvgTime:
				if 10 <= AvgTime <= 60:
					bs_ave = self.Driver.find_element_by_id("measurementTime")
					bs_ave.clear()
					bs_ave.send_keys(AvgTime)
					print("イナゴ平均秒数を変更しました 平均{}秒".format(AvgTime))
					self.NowAvg = AvgTime
				else:
					raise ValueError("現在 平均{}秒\n10-60の間に設定して下さい".format(self.Now))	
		else:
			raise TypeError("AvgTimeは数値で指定して下さい")

	def VolumeGet(self):
		"""
		Action:
			InagoFlyerのSell & Buy Volume取得
			約0.88秒毎に更新?
		
		Parameters:
			Threshold: Number
				指定値以下のVolume の場合 Merit を "Volume is Low" とする
			Difference: Number
				Sell Buy Volume の差が指定値以下の場合 "Even" とする
		
		Raises:
			TypeError:
				引数が数値以外で設定された
		"""

		while True:
			self.SellVolume = float(self.Driver.find_element_by_id("sellVolumePerMeasurementTime").text)

			self.BuyVolume = float(self.Driver.find_element_by_id("buyVolumePerMeasurementTime").text)

			if self.BuyVolume < self.Threshold and self.SellVolume < self.Threshold:
				self.Merit = "Volume is Low"

			elif abs(self.BuyVolume - self.SellVolume) < self.Difference:
				self.Merit = "Even"

			elif self.BuyVolume > self.SellVolume:
				self.Merit = "Buy"

			elif self.BuyVolume < self.SellVolume:
				self.Merit = "Sell"

			yield {"Sell":self.SellVolume,"Buy":self.BuyVolume,"Merit":self.Merit}


	def __Connection(self):
		"""
		Action:
			InagoFlyerに接続する
		
		Raises:
			RuntimeError:
				InagoFlyer接続失敗
				サウンドミュート失敗
		"""

		try:
			self.Driver.get("https://inagoflyer.appspot.com/btcmac")
		except:
			raise RuntimeError("Inago Flyer に接続できません")
		#音をミュートに
		try:
			volume=self.Driver.find_element_by_id('sound')
			volume.click()
		except:
			raise RuntimeError("音をミュートに出d来ません")

if __name__ == '__main__':
	import time
	inago = InagoFlyer()
	for vol in inago.VolumeGet():
		print(vol)
		time.sleep(1)

	