import bs4 as bs
import urllib.request
import pandas as pd

# sauce = urllib.request.urlopen('https://pythonprogramming.net/parsememcparseface/').read()
# soup = bs.BeautifulSoup(sauce, 'lxml')  # lxml is parser
sauce = urllib.request.urlopen('https://pythonprogramming.net/sitemap.xml').read()
soup = bs.BeautifulSoup(sauce, 'xml')
for url in soup.find_all('loc'):
    print(url.text)
#
# # <tr> table rows
# # <th> table header
# # <td> table data
#
# # table = soup.table
# table = soup.find('table')  # same as above
# # print(table)  # contains tags
# table_rows = table.find_all('tr')
#
# for tr in table_rows:
#     td = tr.find_all('td')
#     row = [i.text for i in td]
#     print(row)

# # dfs = pd.read_html('https://pythonprogramming.net/parsememcparseface/')  # parse all tables it can find
# dfs = pd.read_html('https://pythonprogramming.net/parsememcparseface/', header=0)  # make first row the header
# for df in dfs:
#     print(df)

