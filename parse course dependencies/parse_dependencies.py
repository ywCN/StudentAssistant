import re
import sqlite3
import os

'''
This program will parse as many as possible dependencies from the file.
If no pre-requisite and nor co-requisite is found, the course has no dependencies with others. 
However, the course my still need permissions from instructor.

The pdf file is firstly converted into a text file. Then this program will parse dependencies in it.
'''


class ParseDependency:

    def __init__(self):
        self.text = r'catalog.txt'
        self.file = self.open_file()
        self.db = r'course_dependencies.db'

        if os.path.isfile(self.db):
            print("Please delete or rename {} and run this program again.".format(self.db))
            exit()
        else:
            self.conn2 = sqlite3.connect(self.db)  # new db
            self.c2 = self.conn2.cursor()
            self.create_table()

    def open_file(self):
        try:
            return open(self.text, encoding='utf-8')
        except FileNotFoundError:
            print("Please put {} in the same path!".format(self.text))
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
        for line in self.file:
            if "Prerequisites: " in line and cache != '':
                loc = line.index("Prerequisites: ")
                parsed_line = line[loc:]
                self.save_info(parsed_line.strip(), dep, cache)
                cache = ''
            elif "Corequisites: " in line and cache != '':
                loc = line.index("Corequisites: ")
                parsed_line = line[loc:]
                self.save_info(parsed_line.strip(), dep, cache)
                cache = ''
            elif self.is_valid_line(line[:7]) and len(line) < 10 and 'or' not in line:
                cache = line.strip()
            else:
                pass  # skip invalid lines

        return dep

    def save_info(self, line, dep, course):
        """
        :param data:
        :return: None
        """
        dep[course] = {}
        reqs = self.parse_line(line.replace(u'\xa0', u' '))
        dep[course]['Prerequisites'] = reqs[0]
        dep[course]['Corequisites'] = reqs[1]

    def parse_line(self, line):
        """
        :param line: str
        :return: (str, str)
        """
        pre = ''
        co = ''

        if line == 'Prerequisites: Corequisites:':
            return pre, co
        elif 'Prerequisites: Corequisites:' in line:
            co = line.replace('Prerequisites: Corequisites: ', '')
        elif 'Prerequisites: ' in line and 'Corequisites: ' in line:
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

    def create_table(self):
        self.c2.execute("CREATE TABLE IF NOT EXISTS dependencies(CourseID TEXT, Prerequisites TEXT, Corequisites TEXT)")

    def insert_entry(self, data):
        self.c2.execute("INSERT INTO dependencies (CourseID, Prerequisites, Corequisites) VALUES (?, ?, ?)",
                        (data[0], data[1], data[2]))
        self.conn2.commit()

    def save_into_db(self):
        dep = self.parse_file()
        for key in dep:
            data = [key, dep[key]['Prerequisites'], dep[key]['Corequisites']]
            self.insert_entry(data)


def main():
    demo = ParseDependency()
    demo.save_into_db()


if __name__ == '__main__':
    main()
