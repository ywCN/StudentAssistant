import bs4 as bs
import urllib.request

sauce = urllib.request.urlopen('https://pythonprogramming.net/parsememcparseface/').read()
soup = bs.BeautifulSoup(sauce, 'lxml')  # lxml is parser

# print(sauce)
# print(soup)
# print(soup.title)
# print(soup.title)  # <title>Python Programming Tutorials</title>
# print(soup.title.name)  # title
# print(soup.title.string)  # Python Programming Tutorials
# print(soup.find_all('p'))  # find all paragraph tags
# for paragraph in soup.find_all('p'):
#     # print(paragraph)  # contains tags
#     # print(paragraph.string)  # missing some strings
#     print(paragraph.text)  # use this in most cases

# print(soup.get_text())  # find all paragraphs

for url in soup.find_all('a'):
    # print(url)  # get entire tag
    # print(url.text)  # wrong!
    print(url.get('href'))  # right way to get urls
