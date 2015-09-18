from commonSettings import *
from commonFunctions import getParsedHTML, getText, dumpData, csvWriter, load, getParsedSoupFromHTML, write, getEmptyFinancialDataDict
import getpass


def stripNewLine(x):
    return x.strip('\n')
def processDict(lines):
    map(stripNewLine, lines)
    DictData = getEmptyFinancialDataDict()
    i = 0
    try:
        while True:
            mon = lines[i].split(' ')[0]
            if month[mon] == 1:
                DictData['month'].append(lines[i])
                i = i+1
    except:
        if i == 0:
            return None
    months = i
    while i < len(lines):
        if lines[i] == '':
            i = i+1
        elif lines[i] == 'EPS Before Extra Ordinary':
            i = i+1
            while lines[i] == '':
                i=i+1
            for j in range(i+1, i+1+months):
                DictData['EPS Before Extra Ordinary']['Basic EPS'].append(lines[j])
            i = i +1+months
            while lines[i] == '':
                i=i+1
            for j in range(i+1, i+1+months):
                DictData['EPS Before Extra Ordinary']['Diluted EPS'].append(lines[j])
            i = i+1+months
        elif lines[i] == 'EPS After Extra Ordinary':
            i = i+1
            while lines[i] == '':
                i=i+1
            for j in range(i+1, i+1+months):
                DictData['EPS After Extra Ordinary']['Basic EPS'].append(lines[j])
            i = i +1+months
            while lines[i] == '':
                i=i+1
            for j in range(i+1, i+1+months):
                DictData['EPS After Extra Ordinary']['Diluted EPS'].append(lines[j])
            i = i+1+months
        elif lines[i] == 'a) Pledged/Encumbered':
            i = i+1
            while lines[i] == '':
                i=i+1
            for j in range(i+1, i+1+months):
                DictData['a) Pledged/Encumbered']['- Number of shares (Crores)'].append(lines[j])
            i = i +1+months
            while lines[i] == '':
                i=i+1
            for j in range(i+1, i+1+months):
                DictData['a) Pledged/Encumbered']['- Per. of shares (as a % of the total sh. of prom. and promoter group)'].append(lines[j])
            i = i +1+months
            while lines[i] == '':
                i=i+1
            for j in range(i+1, i+1+months):
                DictData['a) Pledged/Encumbered']['- Per. of shares (as a % of the total Share Cap. of the company)'].append(lines[j])
            i = i+1+months
        elif lines[i] == 'b) Non-encumbered':
            i = i+1
            while lines[i] == '':
                i=i+1
            for j in range(i+1, i+1+months):
                DictData['b) Non-encumbered']['- Number of shares (Crores)'].append(lines[j])
            i = i +1+months
            while lines[i] == '':
                i=i+1
            for j in range(i+1, i+1+months):
                DictData['b) Non-encumbered']['- Per. of shares (as a % of the total sh. of prom. and promoter group)'].append(lines[j])
            i = i +1+months
            while lines[i] == '':
                i=i+1
            for j in range(i+1, i+1+months):
                DictData['b) Non-encumbered']['- Per. of shares (as a % of the total Share Cap. of the company)'].append(lines[j])
            i = i+1+months
        elif lines[i] == 'Interest Earned':
            i = i+1
            while lines[i] == '':
                i=i+1
            for j in range(i+1, i+1+months):
                DictData['Interest Earned']['(a) Int. /Disc. on Adv/Bills'].append(lines[j])
            i = i +1+months
            while lines[i] == '':
                i=i+1
            for j in range(i+1, i+1+months):
                DictData['Interest Earned']['(b) Income on Investment'].append(lines[j])
            i = i +1+months
            while lines[i] == '':
                i=i+1
            for j in range(i+1, i+1+months):
                DictData['Interest Earned']['(c) Int. on balances With RBI'].append(lines[j])
            i = i +1+months
            while lines[i] == '':
                i=i+1
            for j in range(i+1, i+1+months):
                DictData['Interest Earned']['(d) Others'].append(lines[j])
            i = i+1+monthsi
        elif lines[i] == 'ANALYTICAL RATIOS':
            i = i+2+months+1+months + 1 + months
        elif lines[i] == 'NPA Ratios :':
            i = i+2+months+1+months + 1 + months+ 1 + months+ 1 + months
        elif lines[i] == 'EXPENDITURE' or lines[i] == 'Promoters and Promoter Group Shareholding' or lines[i] == 'Notes' or lines[i] == 'Source :  Dion Global Solutions Limited ' or lines[i] == 'Public Share Holding':
            i = i+1
        else:
            for j in range(i+1, i+1+months):
                DictData[lines[i]].append(lines[j])
            i = i +1+months
    return DictData

def processAndDump(html, file):
    parsedData = getParsedSoupFromHTML(html)
    tables = parsedData.findAll('table')
    l = len(tables)
    for i in range(l-1,-1,-1):
        data = getText(tables[i]).strip('\n')
        if data == '':
            continue
        lines = data.split('\n')
        #print lines[0]
        if lines[0].startswith('Data Not Available'):
            data = ""
            write(file, data)
            return None
        else:
            try:
                if month[lines[0][:3]] == 1:
                    write(file, data)
                    return processDict(lines)
            except:
                continue
    return None


def saveAnnualDict(index):
    DIR = 'data/financials/'+str(index)+'/'
    annualData = load(DIR +'annualFinancialData.p')
    DictData = processAndDump(annualData,DIR+'annualData.txt')
    if DictData is not None:
        DictData['index'] = index
    dumpData(DictData, DIR + 'annualDict.p')

def combine(prev, next):
    if next is None:
        return prev
    a = prev.keys()
    i = 0
    while i < len(a):
        key = a[i]
        if type(prev[key]) == list:
            prev[key].extend(next[key])
        elif type(prev[key]) == dict:
            c = prev[key].keys()
            j = 0
            while j < len(c):
                key1 = c[j]
                prev[key][key1].extend(next[key][key1])
                j = j+1
        elif type(prev[key]) == int:
            pass
        else:
            print ERROR
        i = i + 1
    return prev

def saveQuarterDict(index):
    DIR = 'data/financials/'+str(index)+'/'
    quarterData1 = load(DIR +'quarterFinancialData1.p')
    DictData1 = processAndDump(quarterData1,DIR+'quarterData1.txt')
    if DictData1 is None:
        return
    quarterData2 = load(DIR +'quarterFinancialData2.p')
    DictData2 = processAndDump(quarterData2,DIR+'quarterData2.txt')
    DictData = combine(DictData1, DictData2)
    if DictData is not None:
        DictData['index'] = index
    dumpData(DictData, DIR+'quarterDict.p')

def saveOnlyRelevantTableDataOfIndex(index):
    saveAnnualDict(index)
    saveQuarterDict(index)

nSymbols = 7630
def saveOnlyRelevantTableData(a,b):
    for i in range(a,b):
        print i,nSymbols
        saveOnlyRelevantTableDataOfIndex(i)

def updateDicts(a,b):
    for index in range(a,b):
        print index,7630
        DIR = 'data/financials/'+str(index)+'/'
        try:
            annual = load(DIR+'annualDict.p')
            if annual is not None:
                annual['index'] = index
                dumpData(annual, 'annualDict.p')
        except:
            pass
        try:
            quarter = load(DIR+'quarterDict.p')
            if quarter is not None:
                quarter['index'] = index
                dumpData(quarter, 'quarterDict.p')
        except:
            pass



def format(x,y):
    return repr(x).ljust(y)

def comparator(x,y):
    if x[1][1] < y[1][1]:
        return -1
    elif x[1][1] > y[1][1]:
        return 1
    return 0
class filtering:
    def round(x):
        return int((x * 100) + 0.5) / 100.0

    def __init__(self):
        self.completeFinancialData = {}
        self.filteredFinancialData = {}
        self.stockSymbols = load('data/symbolsMCupdated.p')
        self.indexes = load('data/index.p')
        self.nSymbols = len(self.stockSymbols)
        self.epsQuarterThreshold = 20
        self.epsAnnualThreshold = 20
        self.salesThreshold = 25
        self.filters = [self.epsQuarterFilter, self.salesQuarterFilter, self.ATPMfilter, self.epsAnnualFilter, self.eps2QuarterFilter]
        self.filterCount = 5
        self.excludeSymbolList  = load('data/excludeSymbols.p')

    def email(self,fileToSend):
        emailfrom = "sahilarora946@gmail.com"
        emailto = "sahilarora946@gmail.com"
        username = "sahilarora946"

        password = getpass.getpass('Password:')

        msg = MIMEMultipart()
        msg["From"] = emailfrom
        msg["To"] = emailto
        msg["Subject"] = raw_input("enter the message you want as subject")
        msg.preamble = "Rock&Roll"

        ctype, encoding = mimetypes.guess_type(fileToSend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        if maintype == "text":
            fp = open(fileToSend)
            # Note: we should handle calculating the charset
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "image":
            fp = open(fileToSend, "rb")
            attachment = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "audio":
            fp = open(fileToSend, "rb")
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(fileToSend, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
        msg.attach(attachment)

        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(username,password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()
    def getParsedFinancialData(self,index):
        '''DIR = 'data/financials/'+str(index)+'/'
        annualData = load(DIR+'annualDict.p')
        if annualData == None:
            return {}
        output = {}
        output['Year'] = annualData['month']
        output['Annual EPS'] = annualData['EPS Before Extra Ordinary']['Basic EPS']
        output['Net Annual Sales'] = annualData['Net Sales/Income from operations']
        '''
        try:
            DIR = 'data/financials/'+str(index)+'/'
            return ((load(DIR+'annualDict.p'), load(DIR+'quarterDict.p')),0)
        except:
            return (None,0)
    def getAllParsedFinancialData(self):
        for i in range(0,self.nSymbols):
            self.completeFinancialData[i] = self.getParsedFinancialData(i)
        self.filteredFinancialData = self.completeFinancialData

    def salesGrowth(self,sales,month):
        if len(sales) < 5:
            return [-1]
        if sales[0] == '--' or sales[1] == '--':
            return [-1]
        for i in range(len(sales)):
            if sales[i] != '--':
                sales[i] = sales[i].replace(',','')
        if float(sales[1]) == 0.0:
            return [-1]

        i = 0
        salesGrowthList = []
        while i+4 < len(sales):
            if sales[i]=='--':
                break
            flag = False
            for j in range(i+1,i+5):
                if month[i].split(' ')[0] == month[j].split(' ')[0]:
                    if sales[j] == '--':
                        break
                    if float(sales[j]) != 0:
                        salesGrowthList.append((float(sales[i]) - float(sales[j]))/abs(float(sales[j]))*100)
                    else:
                        if float(sales[i]) < 0:
                            salesGrowthList.append(-100000)
                        elif float(sales[j]) > 0:
                            salesGrowthList.append(100000)
                    flag = True
                    break

            if flag is False:
                break
            i = i+1
        return map(round,salesGrowthList)

    def salesQuarterFilter(self,(annual,quarter)):
        sales = quarter['Net Sales/Income from operations']
        month = quarter['month']
        saleGrowthList =  self.salesGrowth(sales,month)
        if len(saleGrowthList) < 1 or saleGrowthList[0] < self.salesThreshold:
            return False
        return True

    def calculateEpsLastYearChange(self,eps,month):
        for i in range(len(eps)):
            eps[i] = eps[i].replace(',','')
        if len(eps) < 5 or eps[0]=='--' or float(eps[0]) < 0.0:
            return []
        epsPerChangeQ = []
        i = 0
        #print month
        while i+4 < len(eps):
            if eps[i] == '--':
                break
            flag = False
            for j in range(i+1,i+5):
                if month[i].split(' ')[0] == month[j].split(' ')[0]:
                    if eps[j] == '--':
                        break
                    if float(eps[j]) != 0:
                        epsPerChangeQ.append((float(eps[i]) - float(eps[j]))/abs(float(eps[j]))*100)
                    else:
                        if float(eps[i]) < 0:
                            epsPerChangeQ.append(-100000)
                        elif float(eps[i]) > 0:
                            epsPerChangeQ.append(100000)
                    flag = True
                    break

            if flag is False:
                break
            i = i+1
        return map(round, epsPerChangeQ)


    def epsQuarterFilter(self,(annual,quarter)):
        if quarter == None:
            return False
        eps = quarter['EPS Before Extra Ordinary']['Basic EPS']
        month = quarter['month']
        for i in range(len(eps)):
            eps[i] = eps[i].replace(',','')
        if len(eps) < 5 or eps[0]=='--' or float(eps[0]) < 0.0:
            return False
        epsPerChangeQ = self.calculateEpsLastYearChange(eps,month)
        if len(epsPerChangeQ) < 1 or epsPerChangeQ[0] < self.epsQuarterThreshold:
            return False
        return True

    def eps2QuarterFilter(self,(annual,quarter)):
        if quarter == None:
            return False
        eps = quarter['EPS Before Extra Ordinary']['Basic EPS']
        month = quarter['month']
        for i in range(len(eps)):
            eps[i] = eps[i].replace(',','')
        if len(eps) < 6 or eps[0]=='--' or float(eps[0]) < 0.0:
            return False
        epsPerChangeQ = self.calculateEpsLastYearChange(eps,month)
        if len(epsPerChangeQ) < 2 or epsPerChangeQ[0] < self.epsQuarterThreshold or epsPerChangeQ[1] < self.epsQuarterThreshold:
            return False
        return True

    def calculateEpsAnnualChange(self,eps,year):
        for i in range(len(eps)):
            eps[i] = eps[i].replace(',','')
        if len(eps) < 3 or eps[0]=='--' or float(eps[0]) < 0.0:
            return []
        epsPerChangeA = []
        i = 0
        #print month
        while i+1 < len(eps):
            if eps[i] == '--':
                break
            j = i+1
            if eps[j] == '--':
                break
            if float(eps[j]) != 0:
                epsPerChangeA.append((float(eps[i]) - float(eps[j]))/abs(float(eps[j]))*100)
            else:
                if float(eps[j]) < 0:
                    epsPerChangeA.append(-100000)
                elif float(eps[j]) > 0:
                    epsPerChangeA.append(100000)
            i = i+1
        return map(round, epsPerChangeA)

    def epsAnnualFilter(self,(annual,quarter)):
        if annual == None:
            return False
        eps = annual['EPS Before Extra Ordinary']['Basic EPS']
        year = annual['month']
        for i in range(len(eps)):
            eps[i] = eps[i].replace(',','')
        if len(eps) < 3 or eps[0]=='--' or float(eps[0]) < 0.0:
            return False
        epsPerChangeA = self.calculateEpsAnnualChange(eps,year)
        if len(epsPerChangeA) < 2 or epsPerChangeA[0] < self.epsAnnualThreshold or epsPerChangeA[1] < self.epsAnnualThreshold:
            return False
        return True




    def afterTaxProfitMargin(self,profit, sales):
        if len(profit) ==0 or len(sales) ==0:
            return []
        ATPM = []
        for i in range(len(sales)):
            if sales[i] != '--':
                sales[i] = sales[i].replace(',','')

        for i in range(len(profit)):
            if profit[i] != '--':
                profit[i] = profit[i].replace(',','')
        i = 0
        while i <len(profit):
            if profit[i] == '--' or sales[i] =='--' or float(sales[i])==0:
                break
            ATPM.append(float(profit[i])/float(sales[i])*100)
            i = i+1
        return map(round, ATPM)

    def ATPMfilter(self,(annual, quarter)):
        sales = quarter['Net Sales/Income from operations']
        profit = quarter['Net Profit/(Loss) For the Period']
        ATPM  = self.afterTaxProfitMargin(profit, sales)
        if ATPM == []:
            return False
        l = len(ATPM)
        t = int(30*l/100)
        currentATPM = ATPM[0]
        ATPM.sort()
        for i in range(l-t,l):
            if ATPM[i] == currentATPM:
                return True
        return False

    def writeNotes(self,index):
        DIR = 'data/financials/'+str(index)+'/'
        f = open(DIR+'notes.txt','a')
        f.write(time.strftime("%c"))
        f.write('\n')
        print "Enter your notes"
        while True:
            msg = raw_input()
            if msg == '#':
                f.write('\n\n')
                break
            f.write(msg+'\n')

    def writeNotesForSymbol(self, symbol):
        try:
            self.writeNotes(self.indexes[symbol])
        except:
            print 'Symbol not found'

    def excludeSymbol(self, symbol):
        try:
            self.excludeSymbolList.append(self.indexes[symbol])
            dumpData(self.excludeSymbolList, 'data/excludeSymbols.p')
        except:
            print 'Symbol not found'
    def removeFromExclude(self, symbol):
        try:
            index = self.indexes[symbol]
            while self.excludeSymbolList.count(index)>0:
                self.excludeSymbolList.remove(index)
            dumpData(self.excludeSymbolList, 'data/excludeSymbols.p')
        except:
            print 'Symbol not found'

    def clearNotes(self, index):
        DIR = 'data/financials/'+str(index)+'/'
        f = open(DIR+'notes.txt','w')
        f.close()
        print 'Notes cleared'

    def clearNotesForSymbol(self, symbol):
        try:
            self.clearNotes(self.indexes[symbol])
        except:
            print 'Symbol not found'

    def readNotes(self, index):
        try:
            DIR = 'data/financials/'+str(index)+'/'
            f = open(DIR+'notes.txt','r')
            print f.read()
            f.close()
        except:
            print 'No notes found'

    def readNotesForSymbol(self, symbol):
        try:
            self.readNotes(self.indexes[symbol])
        except:
            print 'Symbol not found'
    def applyFilter(self,f):
        self.filteredFinancialData =  dict((k,(v,l+(1 if f(v) is True else 0))) for (k,(v,l)) in self.filteredFinancialData.iteritems() if v is not None)

    def applyFilterInt(self,i):
        self.applyFilter(self.filters[i])

    def FLOAT(self,x):
        if x != '--':
            return float(x)

    def printFilteredData(self):
        for (i,(v,l)) in self.filteredFinancialData.iteritems():
            #try:
                if v is not None and v[0] is not None and v[1] is not None and l !=0:
                    print format("Name",25),format(self.stockSymbols[i][0],10)
                    print format("Symbol",25),format(self.stockSymbols[i][1]+'/'+self.stockSymbols[i][2],10)
                    print format("EPS quarterly",25),format(map(self.FLOAT,v[1]['EPS Before Extra Ordinary']['Basic EPS']),60)
                    print format("EPS quarterly growth",25),format(self.calculateEpsLastYearChange(v[1]['EPS Before Extra Ordinary']['Basic EPS'],v[1]['month']),30)
                    print format("Sales quarterly",25),format(map(self.FLOAT,v[1]['Net Sales/Income from operations']),30)
                    print format("Sales Growth Quarterly",25),format(self.salesGrowth(v[1]['Net Sales/Income from operations'],v[1]['month']),60)
                    print format("AfterTaxProfitMargin quarterly",30),format(self.afterTaxProfitMargin(v[1]['Net Profit/(Loss) For the Period'],v[1]['Net Sales/Income from operations']),30)
                    print format("AfterTaxProfit quarterly",20  ),format(map(self.FLOAT,v[1]['Net Profit/(Loss) For the Period']),30)
                    print format("EPS Annually",25),format(map(self.FLOAT,v[0]['EPS Before Extra Ordinary']['Basic EPS']),60)
                    print format("EPS Annual growth",25),format(self.calculateEpsAnnualChange(v[0]['EPS Before Extra Ordinary']['Basic EPS'],v[0]['month']),30)
                    print '---------------------------------------------------------------'
            #except:
             #  print 'error'
              # pass

    def clearFilters(self):
        self.filteredFinancialData = self.completeFinancialData

    def saveState(self):
        filteredSortedList = dict([(i,(v,l)) for (i,(v,l)) in self.filteredFinancialData.items() if v is not None and v[0] is not None and v[1] is not None and l >1])
        dumpData(filteredSortedList, 'storedState.p')

    def loadState(self):
        self.filteredFinancialData = load('storedState.p')

    def writeTocsv(self,filename):
        fieldnames = ['Name','filters passed','NSE','BSE','Sector','epsQ','epsQ%','salesQ','salesQ%', 'ATPMQ','ATPQ','epsA','epsA%']
        writer = csvWriter(filename, fieldnames)
        filteredSortedList = self.filteredFinancialData.items()
        filteredSortedList = sorted(filteredSortedList, cmp = comparator, reverse = True)
        for (i,(v,l)) in filteredSortedList:
            if v is None or v[0] is None or v[1] is None or l == 0 or l == 1:
                continue
            row = {}
            row[fieldnames[0]] = self.stockSymbols[i][0]
            row[fieldnames[1]] = l
            row[fieldnames[2]] = self.stockSymbols[i][1]
            row[fieldnames[3]] = self.stockSymbols[i][2]
            row[fieldnames[4]] = self.stockSymbols[i][3]
            row[fieldnames[5]] = v[1]['EPS Before Extra Ordinary']['Basic EPS']
            row[fieldnames[6]] = self.calculateEpsLastYearChange(v[1]['EPS Before Extra Ordinary']['Basic EPS'],v[1]['month'])
            row[fieldnames[7]] = v[1]['Net Sales/Income from operations']
            row[fieldnames[8]] = self.salesGrowth(v[1]['Net Sales/Income from operations'],v[1]['month'])
            row[fieldnames[9]] = self.afterTaxProfitMargin(v[1]['Net Profit/(Loss) For the Period'],v[1]['Net Sales/Income from operations'])
            row[fieldnames[10]] = v[1]['Net Profit/(Loss) For the Period']
            row[fieldnames[11]] = v[0]['EPS Before Extra Ordinary']['Basic EPS']
            row[fieldnames[12]] = self.calculateEpsAnnualChange(v[0]['EPS Before Extra Ordinary']['Basic EPS'],v[0]['month'])
            writer.writerow(row)



if __name__ == "__main__":
    obj = filtering()
    obj.removeFromExclude('ATVPROJ')
    #obj.getAllParsedFinancialData()

    #getAllParsedFinancialData()
    #obj.applyFilter(obj.ATPMfilter)
    #obj.applyFilter(obj.salesQuarterFilter)

    #obj.applyFilter(obj.epsQuarterFilter)
    #obj.applyFilter(obj.epsAnnualFilter)
    #obj.printFilteredData()
    #printFilteredData()
    #saveOnlyRelevantTableData(7000,7630)
    #updateDicts(0, 7630)
    pass
