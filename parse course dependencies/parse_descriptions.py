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
            self.conn2 = sqlite3.connect(self.db)  # new db
            self.c2 = self.conn2.cursor()
            self.create_table()

    def open_file(self):
        try:
            return open(self.text, encoding='utf-8')
        except FileNotFoundError:
            print("Please put {} in the same path!".format(self.text))
            exit()

    def create_table(self):
        self.c2.execute("CREATE TABLE IF NOT EXISTS descriptions(CourseID TEXT, Description TEXT)")

    def insert_entry(self, data):
        self.c2.execute("INSERT INTO descriptions (CourseID, Description) VALUES (?, ?)", (data[0], data[1]))
        self.conn2.commit()