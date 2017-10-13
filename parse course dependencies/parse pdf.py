

# class ParsePDF:
f = open(r'catalog.txt', encoding='utf-8')

for line in f:
    if "Prerequisites: " in line or "Corequisites: " in line:
        print(line)

