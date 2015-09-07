from symbols import updateSymbols
from analyzeData import filtering
fObj = None
clear = "\n" * 100
def analyzeData():
    #data = load('symbolsMCupdated.p')
    global fObj
    if fObj is None:
        fObj = filtering()
    fObj.getAllParsedFinancialData()
    FILTER = [ 0 for i in range(fObj.filterCount)]
    while True:
        print clear
        print 'Press 1 to show the filteredlist'
        print 'Press 2 x to apply a filter'
        print 'x is (1:epsQuarterPercentFilter, 2:salesQuarterFilter, 3:AfterTaxProfitMarginFilter, 4:epsAnnualFilter'
        print 'Press 3 to remove a filter'
        print 'Press 4 to clear all filters'
        print 'Press 5 to save data in csv file'
        print 'Press 6 to email results'
        print 'Press 7 to show applied filters'
        print 'Press 8 to apply all the filters'

        input = raw_input().strip('\n').split(' ')
        input[0] = int(input[0])
        if input[0] == 1:
            fObj.printFilteredData()
        elif input[0] == 2:
            input[1] = int(input[1])-1
            fObj.applyFilterInt(input[1])
            FILTER[input[1]] = 1
        elif input[0] == 3:
            input[1] = int(input[1])-1
            FILTER[input[1]] = 0
            for i in range(len(Filter)):
                if Filter[i] == 1:
                    fObj.applyFilterInt(i)
        elif input[0] == 4:
            fObj.clearFilters()
            FILTER = [ 0 for i in range(fObj.filterCount)]
        elif input[0] == 5:
            fObj.writeTocsv(input[1])
        elif input[0] == 7:
            print FILTER
        elif input[0] == 8:
            for i in range(fObj.filterCount):
                fObj.applyFilterInt(i)
                FILTER[i] = 1

        raw_input('Press enter to continue')



def main():
    while True:
        print 'Press 1 to update all the symbols'
        print 'Press 2 to get MoneyControl symbols'
        print 'Press 3 to analyze the data'
        input = raw_input().strip('\n')
        if input == '1':
            updateSymbols()
        elif input == '2':
            pass
            #getMCSymbols()
        elif input == '3':
            analyzeData()
        else:
            break;




if __name__ == "__main__":
    main()
