from commonSettings import *
from commonFunctions import getParsedHTML, getText, dumpData, csvWriter

base_url = "http://www.stockfry.com/"

def getURL(i):
    return base_url + '/Report_New.asp?id=StockList&a=' + str(101+i)


def removeSemicolon(x):
    return x.strip(';')


def updateSymbols():
    DATA = []
    INDEX = {}
    counter = 0
    for i in range(27):#26 alphabets and one where stocks start with numeral
        print 'updating from page '+str(i+1)+ ' out of 27'
        parsedHTML = getParsedHTML(getURL(i))
        table = parsedHTML.findAll('table')[19].findAll('tr')
        size = len(table)
        for j in range(1,size): #0 is for header
            row = table[j]
            contents = map(getText,row.findAll('td'))
            print contents
            if contents[2] == "000000":
                contents[2] = ""
            DATA.append(contents)
            if contents[1] != "":
                INDEX[contents[1]] = counter
            if contents[2] != "":
                INDEX[contents[2]] = counter
            counter = counter + 1
            #0 is the name, 1 is NSE symbol, 2 is BSE symbol
    dumpData(DATA, 'data/symbols.p')
    dumpData(INDEX,'data/index.p')


def verify(url, symbol):
    parsedHTML = getParsedHTML(url)
    info = getText(parsedHTML.find(attrs={"class":"FL gry10"}))
    info = info.replace(' ','').split('|')
    #print symbol, url
    if info[0] == symbol or info[1] == symbol:
        return True
    return False

def getSymbolFromMCurl(url):
    parsedHTML = getParsedHTML(url)
    info = getText(parsedHTML.find(attrs={"class":"FL gry10"}))
    info = info.replace(' ','').split('|')
    bse = ""
    if len(info[0])>4:
        bse = info[0][4:]
    nse = ""
    if len(info[1])>4:
        nse = info[1][4:]
    return (nse,bse)

def updateAllSymbols():
    symbols = load('data/symbols.p')
    data = load('data/symbolsMCupdated.p')
    index = load('data/index.p')
    l = len(data)
    for i in range(l):
        print i,l
        if data[i][-1].startswith('http://www.moneycontrol.com/india/stockpricequote/'):
            symbol = getSymbolFromMCurl(data[i][-1])
            if symbols[i][1] != "":
                index[symbols[i][1]] = -1
            if symbols[i][2] != "":
                index[symbols[i][2]] = -1
            symbols[i][1] = symbol[0]
            symbols[i][2] = symbol[1]
            index[symbol[0]] = i
            index[symbol[1]] = i
            data[i][1] = symbol[0]
            data[i][2] = symbol[1]
    dumpData(data, 'data/symbolsMCupdated.p')
    dumpData(symbols, 'data/symbols.p')
    dumpData(index, 'data/index.p')

def getMCSymbols():
    data = pickle.load(open('data/symbols.p','rb'))
    l = len(data)
    driver = webdriver.Chrome()
    time.sleep(2)
    driver.get("http://www.moneycontrol.com/")

    for j in range(l):
        try:
            time.sleep(2)
            i = data[j]
            symbol = i[2]
            if i[2] == '':#take either of NSE or BSE
                symbol = i[1]
            print symbol
            while True:
                id = driver.find_elements_by_id("search_str")
                if len(id)>0:
                    id[0].send_keys(symbol)
                    id[0].submit()
                    break
                else: time.sleep(2)
            mcURL = str(driver.current_url.encode('UTF-8'))
            try:
                mcURLsplit = mcURL.split('/')
                mcSymbol = mcURLsplit[-1]
                mcName = mcURLsplit[-2]
                mcSector = mcURLsplit[-3]

                #parsedHTML = getParsedHTML(mcURL)
                #name = getText(parsedHTML.find(attrs = {"class":"b_42 PT5"}))
                #info = getText(parsedHTML.findAll(attrs={"class":"FL gry10"})[0])

                data[j].extend(mcURLsplit[-3:])
                data[j].append(mcURL)
                print data[j]
            except:
                print "Error in getting Moneycontrol symbols for ",symbol
                print mcURL
        except:
            print "error in ",data[j]
    dumpData(data, 'data/symbolsMCupdated.p')


def improveMCsearchForPreiousFails():
    data = load('data/symbolsMCupdated.p')
    l = len(data)
    driver = webdriver.Chrome()
    time.sleep(2)
    driver.get("http://www.moneycontrol.com/")
    for i in range(l):
        if len(data[i]) <4:
            print data
            print 'Error'
            return
        elif data[i][-1].startswith('http://www.moneycontrol.com/india/stockpricequote/'):
            continue
        else:
            symbol = (data[i][1],data[i][2])
            j = 0
            for j in range(2):
                if len(symbol[j])<2:
                    continue
                while True:
                    id = driver.find_elements_by_id("search_str")
                    if len(id)>0:
                        id[0].send_keys(symbol[j])
                        id[0].submit()
                        break
                    else: time.sleep(2)
                mcURL = str(driver.current_url.encode('UTF-8'))
                if mcURL.startswith('http://www.moneycontrol.com/india/stockpricequote/'):
                    mcURLsplit = mcURL.split('/')
                    mcSymbol = mcURLsplit[-1]
                    mcName = mcURLsplit[-2]
                    mcSector = mcURLsplit[-3]
                    data[i][3] = mcSector
                    data[i][4] = mcName
                    data[i][5] = mcSymbol
                    data[i][6] = mcURL
                else:
                    parsedHTML = getParsedHTML(driver.current_url)
                    table = parsedHTML.find(attrs={'class':'srch_tbl'}).findAll('tr')
                    try:
                        for row in table:
                            entry = row.findAll('td')[1]
                            entry = getText(entry).split(' ')
                            exitFlag = False
                            for k in entry:
                                if len(k)>0 and k[0] == ':':
                                    if k[1:] == symbol[j]:
                                        mcURL = str(row.find('td').a['href'].encode('UTF-8'))
                                        mcURLsplit = mcURL.split('/')
                                        mcSymbol = mcURLsplit[-1]
                                        mcName = mcURLsplit[-2]
                                        mcSector = mcURLsplit[-3]
                                        data[i][3] = mcSector
                                        data[i][4] = mcName
                                        data[i][5] = mcSymbol
                                        data[i][6] = mcURL
                                        exitFlag = True
                                        break
                            if exitFlag:
                                break
                    except:
                        pass
            print symbol, data[i][-1]
    dumpData(data, 'data/symbolsMCupdated.p')

def getMCSymbolsUpdated()
    getMCSymbols()
    improveMCsearchForPreiousFails()

#get all the stock symbols and save the data in data folder
def main():
    #updateSymbols()
    #getMCSymbols()
    #improveMCsearchForPreiousFails()
    updateAllSymbols()

if __name__ == "__main__":
    main()
