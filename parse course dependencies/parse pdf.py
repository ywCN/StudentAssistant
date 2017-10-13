

# class ParsePDF:
f = open(r'catalog.txt')
for line in f:
    if "Prerequisites: " in line or "Corequisites: " in line:
        print(line)
        