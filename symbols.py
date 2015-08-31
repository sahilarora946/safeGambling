from common import *
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

#get all the stock symbols and save the data in data folder
def main():
    updateSymbols()
    getMCSymbols()

if __name__ == "__main__":
    main()
