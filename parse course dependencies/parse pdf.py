import re
f = open(r'catalog.txt', encoding='utf-8')

re1='((?:[a-z][a-z0-9_]*))'	# Variable Name 1
re2='(\\s+)'	# White Space 1
re3='(\\d+)'	# Integer Number 1
rg = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)
cache1 = ''
cache2 = ''
for line in f:
    flag = False
    m = rg.search(line[:6])
    if "Prerequisites: " in line:
        if line.startswith("Prerequisites: "):
            print(line)
        else:
            loc = line.index("Prerequisites: ")
            parsed_line = line[loc:]
            print(parsed_line)
    elif "Corequisites: " in line:
        if line.startswith("Corequisites: "):
            print(line)
        else:
            loc = line.index("Corequisites: ")
            parsed_line = line[loc:]
            print(parsed_line)
    elif m:
        print(line)
