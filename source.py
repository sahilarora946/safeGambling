from symbols import updateSymbols, getMCSymbols
def analyzeData():
    data = load('symbolsMCupdated.p')
    while True:
        print 'Press 1 to show the list'

def main():
    while True:
        print 'Press 1 to update all the symbols'
        print 'Press 2 to get MoneyControl symbols'
        print 'Press 3 to analyze the data'
        input = raw_input().strip('\n')
        if input == '1':
            updateSymbols()
        elif input == '2':
            getMCSymbols()
        elif input == '3':
            analyzeData()
        else:
            break;




if __name__ == "__main__":
    main()
