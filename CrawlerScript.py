# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 10:56:53 2023

@author: A20176
"""
import requests
import json
import numpy as np
import csv
import pandas as pd


stockTuple = []
stockCodeList = []
stringlist = []
textCodeList = []

# =============================================================================
# List clear
# =============================================================================
def clearList():
    stockTuple.clear()
    stockCodeList.clear()
    stringlist.clear()
    textCodeList.clear()

# =============================================================================
# read codes from file
# =============================================================================
def initCrawler():
    clearList()      
    readCodeFile("D:\PythonScripts\StockCodes.txt")

def readCodeFile(filename):
    f = open(filename, 'r')

    textCodeList.clear()
    
    for line in f:
        textCodeList.append(int(line))
    
    f.close()

# =============================================================================
# Main Crawler Engine
# =============================================================================
def crawlStock(code, addToList):
    
    strURL = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_" + code + ".tw"
    
    res = requests.get(strURL)

    jsonRes = res.json()

    # print(jsonRes)

    msgArray        = jsonRes['msgArray']    
    sysDate         = jsonRes['queryTime']

    stockName       = msgArray[0]['n']
    stockCode       = msgArray[0]['ch']
    sellPrice       = msgArray[0]['a']
    sellCount       = msgArray[0]['f']
    buyPrice        = msgArray[0]['b']
    buyCount        = msgArray[0]['g']
    openPrice       = msgArray[0]['o']
    lowestPrice     = msgArray[0]['l']
    highestPrice    = msgArray[0]['h']
    totalTransVol   = msgArray[0]['v']
    totalTrans      = msgArray[0]['s']
    yesterdayPrice  = msgArray[0]['y']
    closingPrice    = msgArray[0]['z']
    currentPrice    = msgArray[0]['z']
    currentTransVol = msgArray[0]['tv']
    ara             = msgArray[0]['u']
    arb             = msgArray[0]['w']

    sellPriceList   = np.float_(list(filter(None, sellPrice.split('_'))))
    buyPriceList    = np.float_(list(filter(None, buyPrice.split('_'))))
    sellCountList   = np.int_(list(filter(None, sellCount.split('_'))))
    buyCountList    = np.int_(list(filter(None, buyCount.split('_'))))
    
    textList = []
    
    title = "Date " + sysDate['sysDate']  + " " + sysDate['sysTime']
    textList.append( "Stock: " + stockName + "[ " + stockCode + " ]")
    textList.append( "- Sell Price: "    + str(sellPriceList))
    textList.append( "- Sell Volume: "   + str(sellCountList))
    textList.append( "- Buy Price: "     + str(buyPriceList))
    textList.append( "- Buy Volume: "    + str(buyCountList))
    textList.append( "- Current: "       + currentPrice)
    textList.append( "- Current Vol: "   + currentTransVol)
    textList.append( "- Open: "          + openPrice)
    textList.append( "- Close: "         + closingPrice)
    textList.append( "- Low: "           + lowestPrice)
    textList.append( "- High: "          + highestPrice)
    textList.append( "- Total Vol: "     + totalTransVol)    
    textList.append( "- Closing (d-1): " + yesterdayPrice)
    
    tupleVal = []
    tupleVal.append(sysDate['sysDate'])
    tupleVal.append(sysDate['sysTime'])
    tupleVal.append(stockName)
    tupleVal.append(stockCode)
    tupleVal.append(openPrice)
    tupleVal.append(closingPrice)
    tupleVal.append(lowestPrice)
    tupleVal.append(highestPrice)
    tupleVal.append(totalTransVol)
    
    for text in textList:
        print(text)
            
    if addToList == True:
       stockTuple.append(msgArray)

def writeCsv(filename):
    f = open(filename, 'a')

    # create the csv writer
    writer = csv.writer(f)
    
    # write a row to the csv file
    for element in stockTuple:   
        val1 = element[0]['d'] .split(',')        
        val1 += element[0]['t'] .split(',')        
        val1 += element[0]['n'] .split(',')        
        val1 += element[0]['ch'] .split(',')        
        val1 += element[0]['o'] .split(',')        
        val1 += element[0]['z'] .split(',')  
        val1 += element[0]['v'] .split(',')  
        writer.writerow(val1)

    # close the file
    f.close()

# =============================================================================
# get historical data
# =============================================================================
def Get_StockPrice(Symbol, Date):

    url = f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={Date}&stockNo={Symbol}'

    data = requests.get(url).text
    json_data = json.loads(data)

    Stock_data = json_data['data']

    StockPrice = pd.DataFrame(Stock_data, columns = ['Date','Volume','Volume_Cash','Open','High','Low','Close','Change','Order'])

    StockPrice['Date'] = StockPrice['Date'].str.replace('/','').astype(int) + 19110000
    StockPrice['Date'] = pd.to_datetime(StockPrice['Date'].astype(str))
    StockPrice['Volume'] = StockPrice['Volume'].str.replace(',','').astype(float)/1000
    StockPrice['Volume_Cash'] = StockPrice['Volume_Cash'].str.replace(',','').astype(float)
    StockPrice['Order'] = StockPrice['Order'].str.replace(',','').astype(float)

    StockPrice['Open'] = StockPrice['Open'].str.replace(',','').astype(float)
    StockPrice['High'] = StockPrice['High'].str.replace(',','').astype(float)
    StockPrice['Low'] = StockPrice['Low'].str.replace(',','').astype(float)
    StockPrice['Close'] = StockPrice['Close'].str.replace(',','').astype(float)

    StockPrice = StockPrice.set_index('Date', drop = True)


    StockPrice = StockPrice[['Open','High','Low','Close','Volume']]
    print(StockPrice)
    return StockPrice

# =============================================================================
# main program
# =============================================================================

if __name__ == '__main__':
    initCrawler()   
     
    for code in textCodeList:        
        stockCodeList.append(str(code))        
        
    #crawler loop
    for code in stockCodeList:    
        crawlStock(code, True)   
        print("")    
    
    # stockCodeList.append("2330")
    # stockCodeList.append("2359")
    # stockCodeList.append("2492")
    # stockCodeList.append("2603")
    # stockCodeList.append("2609")
    # stockCodeList.append("2615")
    # stockCodeList.append("3037")
    # stockCodeList.append("3406")
    
    # data = Get_StockPrice('2317','20200921')
    # writeCsv("D:\PythonScripts\Stock\StockRecord.csv")
