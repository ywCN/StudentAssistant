import sys  # PyQT needs this to take system arguments
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage
import bs4 as bs
import urllib.request


class Client(QWebEnginePage) :

    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.loadFinished.connect(self.on_page_load)

    def on_page_load(self):
        self.app.quit()


url = 'https://pythonprogramming.net/parsememcparseface/'
client_reponse = Client(url)
source = client_reponse.mainFrame().toHtml()  # get mainframe and convert to html

soup = bs.BeautifulSoup(source, 'lxml')
js_test = soup.find('p', class_='jstest')
print(js_test.text)

#  pretend we are a client or browser so we can run JS


