from commonSettings import *
def getHTML(url):
    sock = urllib.urlopen(url)
    htmlSource = sock.read()
    sock.close()
    return htmlSource

def getParsedHTML(url):
    htmlSource = getHTML(url)
    try:
        return BeautifulSoup(htmlSource, 'html.parser')
    except:
        return BeautifulSoup(htmlSource, 'lxml')

def getParsedSoupFromHTML(htmlSource):
    try:
        return BeautifulSoup(htmlSource, 'html.parser')
    except:
        return BeautifulSoup(htmlSource, 'lxml')

#get the text from the parsed object
def getText(soup):
    return str(soup.get_text().encode('UTF-8'))

def dumpData(data, file):
    pickle.dump(data, open(file,'wb'))

def csvWriter(file, fieldnames):
    f = open(file,'w')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    return writer

def load(file):
    return pickle.load(open(file,'rb'))

def write(file, content):
    f = open(file,'w')
    f.write(content)
    f.close()

def getEmptyFinancialDataDict():
    out={}
    out['month'] = []
    out['Net Sales/Income from operations'] = []
    out['Other Operating Income'] = []
    out['Total Income From Operations'] = []
    out['EXPENDITURE'] = []
    out['Consumption of Raw Materials'] = []
    out['Purchase of Traded Goods'] = []
    out['Increase/Decrease in Stocks'] = []
    out['Power & Fuel'] = []
    out['Employees Cost'] = []
    out['Depreciation'] = []
    out['Excise Duty'] = []
    out['Admin. And Selling Expenses'] = []
    out['R & D Expenses'] = []
    out['Provisions And Contingencies'] = []
    out['Exp. Capitalised'] = []
    out['Other Expenses'] = []
    out['P/L Before Other Inc. , Int., Excpt. Items & Tax'] = []
    out['Other Income'] = []
    out['P/L Before Int., Excpt. Items & Tax'] = []
    out['Interest'] = []
    out['P/L Before Exceptional Items & Tax'] = []
    out['Exceptional Items'] = []
    out['P/L Before Tax'] = []
    out['Tax'] = []
    out['P/L After Tax from Ordinary Activities'] = []
    out['Prior Year Adjustments'] = []
    out['Extra Ordinary Items'] = []
    out['Net Profit/(Loss) For the Period'] = []
    out['Equity Share Capital'] = []
    out['Reserves Excluding Revaluation Reserves'] = []
    out['Equity Dividend Rate (%)'] = []
    out['EPS Before Extra Ordinary'] = {}
    out['EPS Before Extra Ordinary']['Basic EPS'] = []
    out['EPS Before Extra Ordinary']['Diluted EPS'] = []
    out['EPS After Extra Ordinary'] = {}
    out['EPS After Extra Ordinary']['Basic EPS'] = []
    out['EPS After Extra Ordinary']['Diluted EPS'] = []
    out['Public Share Holding'] = []
    out['No Of Shares (Crores)'] = []
    out['Share Holding (%)'] = []
    out['Promoters and Promoter Group Shareholding'] = []
    out['a) Pledged/Encumbered'] = {}
    out['a) Pledged/Encumbered']['- Number of shares (Crores)'] = []
    out['a) Pledged/Encumbered']['- Per. of shares (as a % of the total sh. of prom. and promoter group)'] = []
    out['a) Pledged/Encumbered']['- Per. of shares (as a % of the total Share Cap. of the company)'] = []

    out['b) Non-encumbered'] = {}
    out['Notes'] = []
    out['Source :  Dion Global Solutions Limited '] = []
    out['b) Non-encumbered']['- Number of shares (Crores)'] = []
    out['b) Non-encumbered']['- Per. of shares (as a % of the total sh. of prom. and promoter group)'] = []
    out['b) Non-encumbered']['- Per. of shares (as a % of the total Share Cap. of the company)'] = []
    out['Interest Earned'] = {}
    out['Interest Earned']['(a) Int. /Disc. on Adv/Bills'] = []
    out['Interest Earned']['(b) Income on Investment'] = []
    out['Interest Earned']['(c) Int. on balances With RBI'] = []
    out['Interest Earned']['(d) Others'] = []

    out['Interest Expended'] = []
    out['Operating Profit before Provisions and contingencies'] = []
    return out

if __name__ == "__main__":
    pass
