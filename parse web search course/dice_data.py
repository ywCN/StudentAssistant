import sqlite3
import os

"""
This class will split the data in the first version of database.
Some data will be abandoned; some data will be created.

Before:
`SectionTitle`   TEXT,
`CallNumber`   TEXT,
`StatusSeatsAvailable`   TEXT,
`DaysTimeLocation`   TEXT,
`Instructor`   TEXT,
`SessionAndDates`   TEXT,
`Credits`   TEXT

After:
`CourseID`    TEXT,
`CourseName`    TEXT,
`CourseSection`    TEXT,
`CallNumber`    TEXT,
`Status`    TEXT,
`Seats`    TEXT,
`Day`    TEXT,
`Time`    TEXT,
`Campus`    TEXT,
`Location`    TEXT,
`Instructor`    TEXT,
`StartDate`    TEXT,
`EndDate`    TEXT,
`MinCredit`    TEXT,
`MaxCredit`    TEXT
"""


class DiceData:
    def __init__(self):
        self.db_name = r'courses.db'
        if os.path.isfile(self.db_name):
            self.conn1 = sqlite3.connect(self.db_name)  # old db
            self.c1 = self.conn1.cursor()
            self.conn2 = sqlite3.connect(r'courses2.db')  # new db
            self.c2 = self.conn1.cursor()
        else:
            print("Please put %s in the same path of this .py file." % self.db_name)
            exit()
        self.courses = self.get_all_courses()

    def get_all_courses(self):
        query = 'select courses.SectionTitle from courses'
        print(type(self.query_info(query)))

    def query_info(self, query):  # in old database
        """
        :type query: str
        :rtype: List[List[str]]
        """
        self.c1.execute("{}".format(query))
        return self.c1.fetchall()

    def create_table(self):  # in new database
        self.c2.execute("CREATE TABLE IF NOT EXISTS courses(CourseID TEXT, CourseName TEXT, CourseSection TEXT, CallNumber TEXT, Status TEXT, Seats TEXT, Day TEXT, Time TEXT, Campus TEXT, Location TEXT, Instructor TEXT, StartDate TEXT, EndDate TEXT, MinCredit TEXT, MaxCredit TEXT)")

    def insert_entry(self, data):  # in new database
        self.c2.execute("INSERT INTO courses (CourseID, CourseName, CourseSection, CallNumber, Status, Seats, Day, Time, Campus, Location, Instructor, StartDate, EndDate, MinCredit, MaxCredit VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
        self.conn2.commit()


def main():
    demo = DiceData()
    demo.get_all_courses()


if __name__ == '__main__':
    main()


