from symbols import updateSymbols, getMCSymbols
def main():

    while True:
        print 'Press 1 to update all the symbols'
        print 'Press 2 to get MoneyControl symbols'
        input = raw_input().strip('\n')
        if input == '1':
            updateSymbols()
        elif input == '2':
            getMCSymbols()
        else:
            break;




if __name__ == "__main__":
    main()
