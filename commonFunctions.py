from commonSettings import *
def getParsedHTML(url):
    sock = urllib.urlopen(url)
    htmlSource = sock.read()
    sock.close()
    try:
        return BeautifulSoup(htmlSource, 'html.parser')
    except:
        BeautifulSoup(htmlSource, 'lxml')

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

def main():
    pass

if __name__ == "__main__":
    main()
