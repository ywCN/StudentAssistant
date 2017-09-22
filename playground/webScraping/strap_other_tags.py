import bs4 as bs
import urllib.request

sauce = urllib.request.urlopen('https://pythonprogramming.net/parsememcparseface/').read()
soup = bs.BeautifulSoup(sauce, 'lxml')

nav = soup.nav

# print(nav)

# for url in nav.find_all('a'):
#     print(url.get('href'))  # all the links in nav bar

body = soup.body
for paragraph in body.find_all('p'):
    print(paragraph.text)  # only get the text data in body part; enough for most strapping cases

