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

def load(file):
    return pickle.load(open(file,'rb'))


if __name__ == "__main__":
    pass
