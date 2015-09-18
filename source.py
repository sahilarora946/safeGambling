from symbols import updateSymbols
from analyzeData import filtering
fObj = None
clear = "\n" * 100
def analyzeData():
    #data = load('symbolsMCupdated.p')
    global fObj
    if fObj is None:
        fObj = filtering()
    FILTER = [ 0 for i in range(fObj.filterCount)]
    while True:
        print clear
        print 'Press 0 to load complete Data'
        print 'Press 1 to show the filteredlist'
        print 'Press 2 x to apply a filter'
        print 'x is (1:epsQuarterPercentFilter, 2:salesQuarterFilter, 3:AfterTaxProfitMarginFilter, 4:epsAnnualFilter'
        print 'Press 3 to remove a filter'
        print 'Press 4 to clear all filters'
        print 'Press 5 to save data in csv file'
        print 'Press 6 to email results'
        print 'Press 7 to show applied filters'
        print 'Press 8 to apply all the filters'
        print 'Press 9 to save state'
        print 'Press 10 to load previous saved state'
        print 'Press 11 x to enter notes for symbol x'
        print 'Press 12 x to read notes for symbol x'
        print 'Press 13 x to clear the notes for symbol x'
        print 'Press 14 x to add a symbol to be EXCLUDED'
        print 'Press 15 x to remove a symbol from Banned list'

        input = raw_input().strip('\n').split(' ')
        input[0] = int(input[0])
        if input[0] == 0:
            fObj.getAllParsedFinancialData()
        if input[0] == 1:
            fObj.printFilteredData()
        elif input[0] == 2:
            input[1] = int(input[1])-1
            fObj.applyFilterInt(input[1])
            FILTER[input[1]] = 1
        elif input[0] == 3:
            input[1] = int(input[1])-1
            FILTER[input[1]] = 0
            fObj.clearFilters()
            for i in range(len(Filter)):
                if Filter[i] == 1:
                    fObj.applyFilterInt(i)
        elif input[0] == 4:
            fObj.clearFilters()
            FILTER = [ 0 for i in range(fObj.filterCount)]
        elif input[0] == 5:
            fObj.writeTocsv(input[1])
        elif input[0] == 6:
            fObj.email(input[1])
        elif input[0] == 7:
            print FILTER
        elif input[0] == 8:
            for i in range(fObj.filterCount):
                fObj.applyFilterInt(i)
                FILTER[i] = 1
        elif input[0] == 9:
            fObj.saveState()
        elif input[0] == 10:
            fObj.loadState()
        elif input[0] == 11:
            fObj.writeNotesForSymbol(input[1])
        elif input[0] == 12:
            fObj.readNotesForSymbol(input[1])
        elif input[0] == 13:
            fObj.clearNotesForSymbol(input[1])
        elif input[0] == 14:
            fObj.excludeSymbol(input[1])
        elif input[0] == 15:
            fObj.removeFromExclude(input[1])

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
