#!/usr/bin/env python3
"""Test with SPY - more reliable options data"""

import time
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

class SPYTest(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        
    def connectAck(self):
        print("✅ Connected!")
        
    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=""):
        print(f"ℹ️  {errorCode}: {errorString}")
    
    def nextValidId(self, orderId):
        print("🔍 Testing SPY stock data...")
        spy = Contract()
        spy.symbol = "SPY"
        spy.secType = "STK"
        spy.exchange = "SMART"
        spy.currency = "USD"
        
        self.reqMktData(1, spy, "", False, False, [])
        
    def tickPrice(self, reqId, tickType, price, attrib):
        if tickType == 4:  # Last price
            print(f"💰 SPY Price: ${price}")
            print("✅ Basic connection works!")
            self.disconnect()

app = SPYTest()
app.connect("127.0.0.1", 4001, clientId=1)
app.run()