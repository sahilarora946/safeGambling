from commonSettings import *
from commonFunctions import getParsedHTML, getText, dumpData, csvWriter, load, getHTML

StockSymbols = load('data/symbolsMCupdated.p')
Indexes = load('data/index.p')
nSymbols = len(StockSymbols)
def saveFinancialData(data, index):
    directory = 'data/financials/'+str(index)+'/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    dumpData(data[0], directory+'annualFinancialData.p')
    dumpData(data[1], directory+'quarterFinancialData1.p')
    dumpData(data[2], directory+'quarterFinancialData2.p')


def download_and_save_fin_data_from_symbol(symbol):
    try:
        index = Indexes[symbol]
        url = StockSymbols[index][-1]
        data = download_fin_data_from_URL(url)
        saveFinancialData(data, index)
    except:
        print 'Symbol not found'

def download_fin_data_from_URL(url, driver = ""):
    if url.startswith('http://www.moneycontrol.com/india/stockpricequote/'):
        mcURLsplit = url.split('/')
        mcSymbol = mcURLsplit[-1]
        mcName = mcURLsplit[-2]
        mcSector = mcURLsplit[-3]
        annualFinancialURL = moneycontrolURL+'financials/'+mcName+'/results/yearly/'+mcSymbol+'#'+mcSymbol
        quarterlyFinancialURL = moneycontrolURL+'financials/'+mcName+'/results/quarterly-results/'+mcSymbol+'#'+mcSymbol
        annualDataHTML = getHTML(annualFinancialURL)

        closeDriver = False
        if driver == "":
            driver = webdriver.Chrome()
            time.sleep(2)
            closeDriver = True
        driver.get(quarterlyFinancialURL)
        quarterDataHTML1 = ""
        quarterDataHTML2 = ""
        while True:
            quarterDataHTML1 = driver.page_source
            if quarterDataHTML1.find('Basic EPS') != -1 or quarterDataHTML1.find('Data Not Available for Quarterly Results')!= -1:
                break
            time.sleep(0.5)
        time.sleep(2)
        l = driver.find_elements_by_class_name("prevnext")
        if len(l) > 0:
            l[-1].click()
            time.sleep(2)
            while True:
                quarterDataHTML2 = driver.page_source
                if quarterDataHTML2 != quarterDataHTML1 and (quarterDataHTML2.find('Basic EPS') != -1 or quarterDataHTML2.find('Data Not Available for Quarterly Results')!= -1):
                    break
                time.sleep(1)
            if closeDriver:
                driver.close()
        return (annualDataHTML, quarterDataHTML1, quarterDataHTML2)

    else:
        print 'invalid url'
        return None

def download_annual_data_from_URL(url,index):
    try:
        if url.startswith('http://www.moneycontrol.com/india/stockpricequote/'):
            mcURLsplit = url.split('/')
            mcSymbol = mcURLsplit[-1]
            mcName = mcURLsplit[-2]
            annualFinancialURL = moneycontrolURL+'financials/'+mcName+'/results/yearly/'+mcSymbol+'#'+mcSymbol
            annualDataHTML = getHTML(annualFinancialURL)
            directory = 'data/financials/'+str(index)+'/'
            if not os.path.exists(directory):
                os.makedirs(directory)
            dumpData(annualDataHTML, directory+'annualFinancialData.p')
    except:
        print 'error'

def downloadAnnualData(a,b):
    for i in range(a,b):
        print i,nSymbols
        data = download_annual_data_from_URL(StockSymbols[i][-1], i)

def download_split_data_from_URL(url,index):
    try:
        if url.startswith('http://www.moneycontrol.com/india/stockpricequote/'):
            mcURLsplit = url.split('/')
            mcSymbol = mcURLsplit[-1]
            mcName = mcURLsplit[-2]
            annualFinancialURL = moneycontrolURL+'company-facts/'+mcName+'/splits/'+mcSymbol+'#'+mcSymbol
            annualDataHTML = getHTML(annualFinancialURL)
            directory = 'data/financials/'+str(index)+'/'
            if not os.path.exists(directory):
                os.makedirs(directory)
            dumpData(annualDataHTML, directory+'splits.p')
    except:
        print 'error'

def downloadSplitData(a,b):
    for i in range(a,b):
        print i,nSymbols
        data = download_split_data_from_URL(StockSymbols[i][-1], i)

def download_other_fin_data_from_URL(url,index):
    try:
        if url.startswith('http://www.moneycontrol.com/india/stockpricequote/'):
            mcURLsplit = url.split('/')
            mcSymbol = mcURLsplit[-1]
            mcName = mcURLsplit[-2]
            annualFinancialURL = moneycontrolURL+'financials/'+mcName+'/balance-sheet/'+mcSymbol+'#'+mcSymbol
            annualDataHTML = getHTML(annualFinancialURL)
            directory = 'data/financials/'+str(index)+'/'
            if not os.path.exists(directory):
                os.makedirs(directory)
            dumpData(annualDataHTML, directory+'balanceSheet.p')
            annualFinancialURL = moneycontrolURL+'financials/'+mcName+'/cash-flow/'+mcSymbol+'#'+mcSymbol
            annualDataHTML = getHTML(annualFinancialURL)
            directory = 'data/financials/'+str(index)+'/'
            if not os.path.exists(directory):
                os.makedirs(directory)
            dumpData(annualDataHTML, directory+'cash_flow.p')
            annualFinancialURL = moneycontrolURL+'financials/'+mcName+'/ratios/'+mcSymbol+'#'+mcSymbol
            annualDataHTML = getHTML(annualFinancialURL)
            directory = 'data/financials/'+str(index)+'/'
            if not os.path.exists(directory):
                os.makedirs(directory)
            dumpData(annualDataHTML, directory+'ratios.p')
            annualFinancialURL = moneycontrolURL+'financials/'+mcName+'/profit-loss/'+mcSymbol+'#'+mcSymbol
            annualDataHTML = getHTML(annualFinancialURL)
            directory = 'data/financials/'+str(index)+'/'
            if not os.path.exists(directory):
                os.makedirs(directory)
            dumpData(annualDataHTML, directory+'profit_loss.p')
            annualFinancialURL = moneycontrolURL+'financials/'+mcName+'/capital-structure/'+mcSymbol+'#'+mcSymbol
            annualDataHTML = getHTML(annualFinancialURL)
            directory = 'data/financials/'+str(index)+'/'
            if not os.path.exists(directory):
                os.makedirs(directory)
            dumpData(annualDataHTML, directory+'capital_structure.p')
    except:
        print 'error'

def downloadOtherFinancialData(a,b):
    for i in range(a,b):
        print i,nSymbols
        data = download_other_fin_data_from_URL(StockSymbols[i][-1], i)

def downloadFinancialData():
    driver = webdriver.Chrome()
    time.sleep(2)
    for i in range(0,nSymbols):
        print i,nSymbols
        data = download_fin_data_from_URL(StockSymbols[i][-1], driver)
        if data is not None:
            saveFinancialData(data, i)
    driver.close()


if __name__ == "__main__":
    downloadSplitData(6000,7630)
    #downloadAnnualData()
    #download_and_save_fin_data_from_symbol()
