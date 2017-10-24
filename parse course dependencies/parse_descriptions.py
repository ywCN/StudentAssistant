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
        self.course_db = r'courses2.db'  # get ids from this db
        self.conn2 = sqlite3.connect(self.course_db)  # new db
        self.c2 = self.conn2.cursor()

    #     if os.path.isfile(self.db):
    #         print("Please delete or rename {} and run this program again.".format(self.db))
    #         exit()
    #     else:
    #         self.conn = sqlite3.connect(self.db)  # new db
    #         self.c = self.conn.cursor()
    #         self.create_table()
    #
    # def create_table(self):
    #     self.c.execute("CREATE TABLE IF NOT EXISTS descriptions(CourseID TEXT, Description TEXT)")
    #
    # def insert_entry(self, data):
    #     self.c.execute("INSERT INTO descriptions (CourseID, Description) VALUES (?, ?)", (data[0], data[1]))
    #     self.conn.commit()

    def open_file(self):
        try:
            return open(self.text, encoding='utf-8')
        except FileNotFoundError:
            print("Please put {} in the same path!".format(self.text))
            exit()

    def get_all_ids(self):
        query = 'select courses.CallNumber from courses'
        calls = self.query_info(query)
        ids = set()
        for call in calls:
            ids.add(call[0])
        return ids

    def query_info(self, query):  # in old database
        """
        :type query: str
        :rtype: List[List[str]]
        """
        self.c2.execute("{}".format(query))
        return self.c2.fetchall()

    def print_info(self):  # line.replace(u'\xa0', u' ')
        cache = []  # CourseID, , Course Name, ,(0-0-0), mutiple lines, ,
        # TODO: start caching line when encountering courseID, stop caching when encounting courseID
        # In the cache:
        # if [0]
        # if line length > 1, abandon cache
        # if line length > 70, abandon cache
        # if line length > 1, abandon cache
        # while line length < 70, cache line






def main():
    demo = ParseDescription()
    demo.print_info()


if __name__ == '__main__':
    main()