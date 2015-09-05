from commonSettings import *
from commonFunctions import getParsedHTML, getText, dumpData, csvWriter, load
from string import ascii_uppercase
def getURL(i):
    return moneycontrolURL + '/india/stockmarket/pricechartquote/' + i


def removeSemicolon(x):
    return x.strip(';')

def getSymbolFromMCurl(url):
    try:
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
    except:
        return None

def updateSymbols():
    DATA = []
    data = []
    INDEX = {}
    counter = 0
    alphabets = list(ascii_uppercase)
    alphabets.append('others')
    for i in alphabets:#26 alphabets and one where stocks start with numeral
        try:
            print 'updating from page '+i+ ' out of z'
            parsedHTML = getParsedHTML(getURL(i))
            table = parsedHTML.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['bl_12'])
            size = len(table)
            tempInsert = {}
            for j in range(1,size): #0 is for header
                try:
                    print i, j,'out of',size
                    row = table[j]
                    name = getText(row)
                    if name == '':
                        continue
                    mcURL = str(row['href'].encode('UTF-8'))
                    mcURLsplit = mcURL.split('/')
                    symbol = getSymbolFromMCurl(mcURL)
                    if symbol == None:
                        continue
                    nse,bse = symbol
                    DATA.append([name, nse, bse])
                    data.append([name, nse, bse])
                    DATA[counter].extend(mcURLsplit[-3:])
                    DATA[counter].append(mcURL)
                    if nse != "":
                        tempInsert[nse] = counter
                    if bse != "":
                        tempInsert[bse] = counter
                    tempInsert[mcURL] = counter
                    counter = counter + 1
                except:
                    print 'except 1'

            INSERT = INSERT.update(tempInsert)
        except:
            print 'except 2'

            #0 is the name, 1 is NSE symbol, 2 is BSE symbol
    dumpData(DATA, 'data/symbolsMCupdated.p')
    dumpData(INDEX,'data/index.p')
    dumpData(data,'data/symbols.p')

def searchSymbol(symbol):
    driver = webdriver.Chrome()
    time.sleep(2)
    driver.get("http://www.moneycontrol.com/")
    time.sleep(2)
    if len(symbol)<2:
        return []
    while True:
        id = driver.find_elements_by_id("search_str")
        if len(id)>0:
            id[0].send_keys(symbol)
            id[0].submit()
            break
        else: time.sleep(2)
    mcURL = str(driver.current_url.encode('UTF-8'))
    output = []
    if mcURL.startswith('http://www.moneycontrol.com/india/stockpricequote/'):
            mcURLsplit = mcURL.split('/')
            mcSymbol = mcURLsplit[-1]
            mcName = mcURLsplit[-2]
            mcSector = mcURLsplit[-3]
            output = [mcSector, mcName, mcSymbol,mcURL]
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
                            output = [mcSector, mcName, mcSymbol,mcURL]
                            exitFlag = True
                            break
                if exitFlag:
                    break
        except:
            driver.close()
            return
    driver.close()
    return output





def insertSymbolinDatabase(symbol):
    index = load('data/index.p')
    try:
        print index[symbol]
        print symbol + 'is already in our database'
    except:
        result = searchSymbol(symbol)
        if result == []:
            print 'symbol not found'
            return
        nse,bse = getSymbolFromMCurl(result[-1])
        symbols = load('data/symbols.p')
        data = load('data/symbolsMCupdated.p')
        l = len(data)
        symbols.append(['',nse,bse])
        data.append(['',nse,bse])
        data[-1].extend(result)
        if nse != "":
            index[nse] = l
        if bse != "":
            index[bse] = l
        dumpData(index, 'data/index.p')
        dumpData(symbols, 'data/symbols.p')
        dumpData(data, 'data/symbolsMCupdated.p')
        return True

#get all the stock symbols and save the data in data folder
def main():
    #updateSymbols()
    #getMCSymbols()
    #improveMCsearchForPreiousFails()
    updateSymbols()
    from download_financial_data import downloadFinancialData
    downloadFinancialData()

if __name__ == "__main__":
    main()
