import bs4 as bs
import urllib.request

sauce = urllib.request.urlopen('https://pythonprogramming.net/parsememcparseface/').read()
soup = bs.BeautifulSoup(sauce, 'lxml')  # lxml is parser

# <tr> table rows
# <th> table header
# <td> table data

# table = soup.table
table = soup.find('table')  # same as above
# print(table)  # contains tags
table_rows = table.find_all('tr')

for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text for i in td]
    print(row)

