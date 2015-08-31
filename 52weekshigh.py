from commonSettings import *
from commonFunctions import getParsedHTML, getText, dumpData, csvWriter, load



StockSymbols = load('data/symbolsMCupdated.p')
Indexes = load('data/index.p')

def getCurrentAnd52WeekHighLow(url):
    try:
        parsedHTML = getParsedHTML(url)
        curr = parsedHTML.findAll(attrs={"class":"FL PR5 gD_30"})
        curr.extend(parsedHTML.findAll(attrs={"class":"FL PR5 rD_30"}))
        curr.extend(parsedHTML.findAll(attrs={"class":"FL PR5 bD_30"}))
        curr = float(getText(curr[-1]))
        high = parsedHTML.find(attrs={"id":"n_52high"})
        low = parsedHTML.find(attrs={"id":"n_52low"})
        if high == None:
            high = parsedHTML.find(attrs={"id":"b_52high"})
            low = parsedHTML.find(attrs={"id":"b_52low"})
        if high == None:
            return None
        high = getText(high)
        low = getText(low)
        return(curr, float(high), float(low))
    except:
        #print "error in getting low high for ", url
        pass


#find all the stocks whose current prices are in 52 weeks high zone (not more than 10% from 52 week high)
def _52weeksHighZone():
    l = len(StockSymbols)
    writer = csvWriter('data/52weeksHigh.csv',['symbol','low','high','curr'])

    for i in range(l):
        if len(StockSymbols[i])> 3 and StockSymbols[i][-1].startswith("http://www.moneycontrol.com/india/stockpricequote/"):
            url = StockSymbols[i][-1]
            currHighLow = getCurrentAnd52WeekHighLow(url)
            if currHighLow  is None:
                continue;
            curr, high,low = currHighLow
            diff = (high - curr)/(high)*100
            if diff < 20:
                print low, high, curr, StockSymbols[i][:3]
                writer.writerow({'symbol':str(StockSymbols[i][:3]), 'low':low,'high':high,'curr':curr})


def is52WeekHigh(symbol):
    try:
        index = Indexes[symbol]
        StockSymbols[index][-1]
        currHighLow = getCurrentAnd52WeekHighLow(url)
        if currHighLow  is None:
            print "could not get low high, might not be trading currently"
        curr, high,low = currHighLow
        diff = (high - curr)/(high)*100
        if diff < 20:
            return True
        return False

    except:
        print "Symbol not found"
        return False

def main():
    _52weeksHighZone()

if __name__ == "__main__":
    main()
