from commonSettings import *
from commonFunctions import getParsedHTML, getText, dumpData

def load(file):
    return pickle.load(open(file,'rb'))

StockSymbols = load('data/symbolsMCupdated.p')
Indexes = load('data/index.p')

def getCurrentAnd52WeekHighLow(url):
    try:
        parsedHTML = getParsedHTML(url)
        curr = float(getText(parsedHTML.findAll(attrs = {"class":"FL PR5 rD_30"})[-1]))
        high = parsedHTML.find(attrs={"id":"n_52high"})
        low = parsedHTML.find(attrs={"id":"n_52low"})
        if high == "":
            high = parsedHTML.find(attrs={"id":"b_52high"})
            low = parsedHTML.find(attrs={"id":"b_52low"})
        if high == "":
            return None
        return(curr, float(high), float(low))
    except:
        print "error in getting low high for ", url


#find all the stocks whose current prices are in 52 weeks high zone (not more than 10% from 52 week high)
def 52weeksHighZone():
    l = len(StockSymbols)
    for i in range(l):
        if len(StockSymbols[i])> 3 and StockSymbols[i][-1].startswith("http://www.moneycontrol.com/india/stockpricequote/"):
            url = StockSymbols[-1]
            currHighLow = getCurrentAnd52WeekHighLow(url)
            if currHighLow  is None:
                continue;
            curr, high,low = currHighLow
            diff = (high - curr)/(high - low)*100
            if diff < 10:
                print low, high, curr, StockSymbols[:3]


def is52WeekHigh(symbol):
    try:
        index = Indexes[symbol]
        StockSymbols[index][-1]
        currHighLow = getCurrentAnd52WeekHighLow(url)
        if currHighLow  is None:
            print "could not get low high, might not be trading currently"
        curr, high,low = currHighLow
        diff = (high - curr)/(high - low)*100
        if diff < 10:
            return True
        return False

    except:
        print "Symbol not found"
        return False

