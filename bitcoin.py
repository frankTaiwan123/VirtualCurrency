# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time

def testfile():
	try:
		asset=open(".\\asset.txt","r+",encoding="utf-8")
	except FileNotFoundError:
		print("建立資產表中...")
		asset=open(".\\asset.txt","w")
		for i in coins:
			asset.writelines(i+": 0\n")
		asset.writelines("balance: 0")
	asset.close()

def prompt():
	print("輸入1購入貨幣")
	print("輸入2售出貨幣")
	print("輸入3查詢貨幣價格")
	print("輸入4查詢交易紀錄")
	print("輸入5查詢盈餘")
	print("輸入0結束程式(記錄將保存)")

def coincode():
	while(True):
		print("目前支援的貨幣: ",end="")
		for i in coins:
			print(i,end=" ")
		print()
		code=input("輸入貨幣代碼(大小寫有別): ")
		if(code in coins):
			break
		else:
			print("目前不支援此貨幣，請重新輸入\n")
	return code

def getamount():
	while(True):
		try:
			amount=float(input("輸入數量: "))
			if(amount>0):
				break
			else:
				print("請輸入大於0的數量")
		except ValueError:
			print("請輸入數字")
	return amount

class coin:
	def buy(code,amount,value):
		global asset
		global records
		try:
			asset=open(".\\asset.txt","r",encoding="utf-8")
			assetlist=asset.readlines()
			asset.close()
			
			asset=open(".\\asset.txt","w",encoding="utf-8")
			index=coins.index(code)
			add=float(assetlist[index].strip().replace(code+": ",""))+amount
			assetlist[index]=code+": "+str(add)+"\n"
			balance=float(assetlist[-1].strip().replace("balance: ",""))-amount*value
			assetlist[-1]="balance: "+str(balance)
			asset.seek(0,0)
			for i in assetlist:
				asset.writelines(i)
			
			records=open(".\\record.txt","a+",encoding="utf-8")
			nowtime=time.strftime("%Y-%m-%d %H:%M:%S")
			records.writelines(nowtime+" buy "+code+" "+str(amount)+" at $"+str(value)+"\n")
			print("交易完成\n")
			asset.close()
			records.close()
		except FileNotFoundError:
			print("檔案消失，請重新啟動程式\n")
	def sale(code,amount,value):
		global asset
		global records
		try:
			asset=open(".\\asset.txt","r+",encoding="utf-8")
			assetlist=asset.readlines()
			asset.close()
			
			asset=open(".\\asset.txt","w",encoding="utf-8")
			index=coins.index(code)
			minus=float(assetlist[index].strip().replace(code+": ",""))-amount
			if(minus<0):
				print("數量不足，您只有%f個%s"%(minus+amount, code))
				print("交易失敗\n")
			else:
				assetlist[index]=code+": "+str(minus)+"\n"
				balance=float(assetlist[-1].strip().replace("balance: ",""))+amount*value
				assetlist[-1]="balance: "+str(balance)
				asset.seek(0,0)
				for i in assetlist:
					asset.writelines(i)
				records=open(".\\record.txt","a+",encoding="utf-8")
				nowtime=time.strftime("%Y-%m-%d %H:%M:%S")
				records.writelines(nowtime+" sale "+code+" "+str(amount)+" at $"+str(value)+"\n")
				print("交易完成\n")
				records.close()
			asset.close()
		except FileNotFoundError:
			print("檔案消失，請重新啟動程式\n")
	def getvalue(code):
		url="https://crypto.cnyes.com/"+code+"/24h"
		try:
			res=requests.get(url)
		except:
			return -1.0
		bs=BeautifulSoup(res.content,"html.parser")
		lastprice=bs.find("div","last-price")
		price=lastprice.find("span","big-num").text+lastprice.find("span","small-num").text
		price=price.replace(",","")
		return float(price)

class account:
	def record():
		try:
			global records
			records=open(".\\record.txt","r",encoding="utf-8")
			recordlist=records.readlines()
			if(len(recordlist)==0):
				print("無紀錄\n")
			else:
				print("紀錄如下：")
				for i in recordlist:
					print(i.strip())
				print()
		except FileNotFoundError:
			print("無紀錄\n")
		records.close()
	def getmoney():
		global asset
		asset=open(".\\asset.txt","r",encoding="utf-8")
		assetlist=asset.readlines()
		print("目前盈餘為:　"+assetlist[-1].replace("balance: ","").strip()+"元\n")
		asset.close()

coins=["BTC", "ETH", "XRP", "BCH", "EOS", "XLM", "LTC", "USDT", "BSV", "TRX"]
records=open(".\\record.txt","a+",encoding="utf-8")
records.close()
testfile()

while(True):
	while(True):
		prompt()
		try:
			choice=int(input("輸入: "))
			break
		except ValueError:
			print("請輸入數字\n")
			
	if(choice==0):
		break
	elif(choice==1):
		code=coincode()
		
		value=coin.getvalue(code)
		if(value<0):
			print("連線異常，無法取得貨幣價格")
			buy="N"
		else:
			print("目前%s的價格為%.3f元"%(code,value))
			buy=input("確認要購買(Y/N)？")
		if(buy.upper()=="Y"):
			amount=getamount()
			coin.buy(code,amount,value)
		else:
			print("交易取消\n")
		
	elif(choice==2):
		code=coincode()
		value=coin.getvalue(code)
		if(value<0):
			print("連線異常，無法取得貨幣價格")
			sale="N"
		else:
			print("目前%s的價格為%.3f元"%(code,value))
			sale=input("確認要販賣(Y/N)？")
		if(sale.upper()=="Y"):
			amount=getamount()
			coin.sale(code,amount,value)
		else:
			print("交易取消\n")
		
	elif(choice==3):
		code=coincode()
		value=coin.getvalue(code)
		if(value<0):
			print("連線異常，無法取得貨幣價格\n")
		else:
			print("%s的價格為%.3f元\n"%(code,value))
		
	elif(choice==4):
		account.record()
		
	elif(choice==5):
		account.getmoney()
		
	else:
		print("輸入代碼錯誤\n")

print("程式即將關閉，歡迎再度使用")