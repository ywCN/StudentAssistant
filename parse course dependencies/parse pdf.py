import re
import sqlite3
'''
This program will parse as many as possible dependencies from the file.
If no pre-requisite and nor co-requisite is found, the course has no dependencies with others. 
However, the course my still need permissions from instructor.

The pdf file is firstly converted into a text file. Then this program will parse dependencies in it.
'''


class ParsePDF:

    def __init__(self):
        self.file_name = r'catalog.txt'
        self.file = self.open_file()

    def open_file(self):
        try:
            return open(self.file_name, encoding='utf-8')
        except FileNotFoundError:
            print("Please put {} in the same path!".format(self.file_name))
            exit()

    def is_valid_line(self, text):
        re1 = '((?:[a-z][a-z]+))'  # Word 1
        re2 = '( )'  # White Space 1
        re3 = '(\\d+)'  # Integer Number 1

        rg = re.compile(re1 + re2 + re3, re.IGNORECASE | re.DOTALL)
        return rg.search(text)

    def parse_file(self):
        cache = ''
        dep = {}
        #TODO: return a dict {course: {pre:str, co:str}}
        for line in self.file:
            if "Prerequisites: " in line and cache != '':
                # print(cache)

                loc = line.index("Prerequisites: ")
                parsed_line = line[loc:]
                # print(parsed_line.strip())
                self.save_info(parsed_line.strip(), dep, cache)
                cache = ''
            elif "Corequisites: " in line and cache != '':
                # print(cache)

                loc = line.index("Corequisites: ")
                parsed_line = line[loc:]
                # print(parsed_line.strip())

                cache = ''
            elif self.is_valid_line(line[:7]) and len(line) < 10 and 'or' not in line:
                cache = line.strip()
            else:
                pass

        print(dep)

    def save_info(self, line, dep, course):
        """

        :param data:
        :return: None
        """
        # TODO: parse line and put data into dict
        dep[course] = {}
        reqs = self.parse_line(line)
        dep[course]['Prerequisites'] = reqs[0]
        dep[course]['Corequisites'] = reqs[1]

    def parse_line(self, line):
        pre = ''
        co = ''

        if 'Prerequisites: Corequisites:' in line:
            co = line.replace('Prerequisites: Corequisites: ', '')
        elif 'Prerequisites: ' in line and 'Corequisites: ' in line:
            print(line)
            data = line.split(' Corequisites: ')
            co = data[1]
            pre = data[0].replace('Prerequisites: ', '')
        elif 'Prerequisites' in line:
            pre = line.replace('Prerequisites: ', '')
        elif 'Corequisites' in line:
            co = line.replace('Corequisites: ', '')
        else:
            print('missing lines', line)
        return pre, co


def main():
    demo = ParsePDF()
    demo.parse_file()


if __name__ == '__main__':
    main()
