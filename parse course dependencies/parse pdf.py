import re

f = open(r'catalog.txt', encoding='utf-8')

re1 = '((?:[a-z][a-z]+))'  # Word 1
re2 = '( )'  # White Space 1
re3 = '(\\d+)'  # Integer Number 1

rg = re.compile(re1 + re2 + re3, re.IGNORECASE | re.DOTALL)
cache1 = ''
cache2 = ''
for line in f:
    flag = False
    m = rg.search(line[:6])
    if "Prerequisites: " in line:
        if line.startswith("Prerequisites: "):
            print
            print(line.strip())
        else:
            loc = line.index("Prerequisites: ")
            parsed_line = line[loc:]
            print(parsed_line.strip())
    elif "Corequisites: " in line:
        if line.startswith("Corequisites: "):
            print(line.strip())
        else:
            loc = line.index("Corequisites: ")
            parsed_line = line[loc:]
            print(parsed_line.strip())
    elif m and len(line) < 10 and 'or' not in line:
        print(line.strip())
