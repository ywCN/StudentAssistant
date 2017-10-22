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
            self.c2 = self.conn2.cursor()
            self.create_table()
        else:
            print("Please put {} in the same path of this .py file.".format(self.db_name))
            exit()
        self.call_numbers = self.get_all_call_numbers()
        # print(self.call_numbers[1])

    def get_all_call_numbers(self):
        # query = 'select courses.SectionTitle from courses'
        # print(type(self.query_info(query)))  # list
        # print(len(self.query_info(query)))  # 2052
        query = 'select courses.CallNumber from courses'
        calls = self.query_info(query)
        call_numbers = []
        for call in calls:
            call_numbers.append(call[0])
        # print(len(call_numbers))  # 2052
        return call_numbers

    def query_info(self, query):  # in old database
        """
        :type query: str
        :rtype: List[List[str]]
        """
        self.c1.execute("{}".format(query))
        return self.c1.fetchall()

    def create_table(self):  # in new database
        self.c2.execute("CREATE TABLE IF NOT EXISTS courses(CourseID TEXT, CourseName TEXT, CourseSection TEXT, "
                        "CallNumber TEXT, Status TEXT, Seats TEXT, Day TEXT, Time TEXT, Campus TEXT, Location TEXT, "
                        "Instructor TEXT, StartDate TEXT, EndDate TEXT, MinCredit TEXT, MaxCredit TEXT)")

    def insert_entry(self, data):  # in new database
        self.c2.execute("INSERT INTO courses (CourseID, CourseName, CourseSection, CallNumber, Status, "
                        "Seats, Day, Time, Campus, Location, Instructor, StartDate, EndDate, MinCredit, MaxCredit "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
        self.conn2.commit()

    def print_old_db(self):
        # for call in self.call_numbers:
        #     query = 'select * from courses where courses.CallNumber == {}'.format(call)
        #     print(self.query_info(query))
        query = 'select * from courses where courses.CallNumber == 10032'
        info = self.query_info(query)[0]
        # print(type(info))  # tuple
        print(info)
        self.parse_line(info)

    def parse_line(self, info):
        CourseID = CourseName = CourseSection = CallNumber = Status = Seats = Day = Time \
            = Campus = Location = Instructor = StartDate = EndDate = MinCredit = MaxCredit = 'NA'
        section_elements = info[0].split('-')  # BIO -381-A  Cell Biology -> BIO , 381, A  Cell Biology
        section_elements2 = section_elements[2].split('  ')  # A  Cell Biology -> A, Cell Biology
        # CourseID = section_elements[0] + section_elements[1]  # BIO 381
        CourseID = section_elements[0][:-1] + section_elements[1]  # BIO381
        CourseName = section_elements2[1]
        CourseSection = section_elements2[0]

        print(CourseID, CourseName, CourseSection)


def main():
    demo = DiceData()
    demo.print_old_db()


if __name__ == '__main__':
    main()


