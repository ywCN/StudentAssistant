import re
import sqlite3
import os

'''
This program will parse as many as possible descriptions from the file.
If no pre-requisite and nor co-requisite is found, the course has no dependencies with others. 
However, the course my still need permissions from instructor.

The pdf file is firstly converted into a text file. Then this program will parse dependencies in it.
'''


class ParseDescription:

    def __init__(self):
        self.text = r'catalog.txt'
        self.file = self.open_file()
        self.db = r'course_descriptions.db'

        if os.path.isfile(self.db):
            print("Please delete or rename {} and run this program again.".format(self.db))
            exit()
        else:
            self.conn = sqlite3.connect(self.db)  # new db
            self.c = self.conn.cursor()
            self.create_table()

    def create_table(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS descriptions(CourseID TEXT, Description TEXT)")

    def insert_entry(self, data):
        self.c.execute("INSERT INTO descriptions (CourseID, Description) VALUES (?, ?)", (data[0], data[1]))
        self.conn.commit()

    def open_file(self):
        try:
            return open(self.text, encoding='utf-8')
        except FileNotFoundError:
            print("Please put {} in the same path!".format(self.text))
            exit()

    def print_info(self):  # line.replace(u'\xa0', u' ')

        re1 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 1
        re2 = '(\\s+)'  # White Space 1
        re3 = '(\\d+)'  # Integer Number 1

        rg = re.compile(re1 + re2 + re3, re.IGNORECASE | re.DOTALL)

        cache = []  # CourseID, , Course Name, ,(0-0-0), multiple lines, ,
        flag = False  # init
        # TODO: start caching line when encountering courseID, stop caching when encountering courseID
        for line in self.file:
            ln = line.strip().replace(u'\xa0', u' ')
            m = rg.search(ln)
            if m and not flag:
                # print(ln)  # got all ids
                cache.append(ln)
                flag = True
            elif m and flag:
                if len(cache) > 5 and len(cache[1]) == 0 and len(cache[3]) == 0 and '(' in cache[4]:
                    course_id = cache[0]
                    course_description = ' '.join(cache[6:])
                    if len(course_id) < 8:
                        self.insert_entry([course_id, course_description])
                cache.clear()
                cache.append(ln)
            else:
                cache.append(ln)


def main():
    demo = ParseDescription()
    demo.print_info()


if __name__ == '__main__':
    main()