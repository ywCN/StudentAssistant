import sqlite3
import os


class DiceData:
    """
    This class is used for cleaning up data in the old database and create a new database.
    This class will split the data in the first version of database.
    Some data will be abandoned; some new data will be created.

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
    def __init__(self):
        self.old_db = r'courses.db'
        self.new_db = r'courses2.db'
        if os.path.isfile(self.old_db):  # make sure old database exists and new database not exist
            self.old_conn = sqlite3.connect(self.old_db)  # old db
            self.old_cursor = self.old_conn.cursor()
            if os.path.isfile(self.new_db):
                print("Please delete or rename {} and run this program again.".format(self.new_db))
                exit()
            else:
                self.new_conn = sqlite3.connect(self.new_db)  # new db
                self.new_cursor = self.new_conn.cursor()
                self.create_table()
        else:
            print("Please put {} in the same path of this .py file.".format(self.old_db))
            exit()
        self.call_numbers = self.get_all_call_numbers()  # for looping through the old database

    def get_all_call_numbers(self):
        query = 'select courses.CallNumber from courses'
        calls = self.query_info(query)
        call_numbers = []
        for call in calls:
            call_numbers.append(call[0])
        return call_numbers

    def query_info(self, query):  # in old database
        """
        :type query: str
        :rtype: List[List[str]]
        """
        self.old_cursor.execute("{}".format(query))
        return self.old_cursor.fetchall()

    def create_table(self):  # in new database
        self.new_cursor.execute("CREATE TABLE IF NOT EXISTS courses"
                                "(CourseID TEXT, CourseName TEXT, CourseSection TEXT, CallNumber TEXT, Status TEXT, "
                                "Seats TEXT, Day TEXT, Time TEXT, Campus TEXT, Location TEXT, Instructor TEXT, "
                                "StartDate TEXT, EndDate TEXT, MinCredit TEXT, MaxCredit TEXT)")

    def insert_entry(self, data):  # in new database
        self.new_cursor.execute("INSERT INTO courses "
                                "(CourseID, CourseName, CourseSection, CallNumber, Status, Seats, Day, Time, Campus, "
                                "Location, Instructor, StartDate, EndDate, MinCredit, MaxCredit) "
                                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                                    data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8],
                                    data[9], data[10], data[11], data[12], data[13], data[14]))
        self.new_conn.commit()

    def parse_line(self, info):
        CourseSection = Seats = Day = Time = Location = StartDate = EndDate = MinCredit = MaxCredit = 'NA'
        section_elements = info[0].split('-')  # BIO -381-A  Cell Biology -> BIO , 381, A  Cell Biology
        section_elements2 = section_elements[2].split('  ')  # A  Cell Biology -> A, Cell Biology
        # CourseID = section_elements[0] + section_elements[1]  # BIO 381

        CourseID = section_elements[0][:-1] + section_elements[1]  # BIO381
        CourseName = section_elements2[-1]

        if len(section_elements) == 3:
            CourseSection = section_elements2[0]
        elif len(section_elements) == 4:
            CourseSection = section_elements[-1] + section_elements2[0]

        CallNumber = info[1]

        status_seats_available_elements = info[2].split(' - ')  # Open - 33 of 96 -> Open, 33 of 96
        if status_seats_available_elements[0] == 'Open' and len(status_seats_available_elements) > 1:
            Status = 'Open'
            seats_elements = status_seats_available_elements[1].split(' of ')
            if len(seats_elements) == 2:
                Seats = seats_elements[0]
            else:
                Seats = 'unlimited'
        elif len(status_seats_available_elements) == 1 and 'Open' in status_seats_available_elements[0]:
            Status = 'Open'
        else:
            Status = 'Closed'

        if 'AM' in info[3] or 'PM' in info[3]:
            days_time_location = info[3].split()
            Day = days_time_location[0]
            Time = days_time_location[1]
            Campus = 'Main Campus'
            if 'Not Applicable' not in info[3]:
                Location = ' '.join(days_time_location[4:])
        elif 'TBA' in info[3]:
            Day = 'TBA'
            Time = 'TBA'
            Campus = 'TBA'
        elif 'WEB' in info[3]:
            Campus = 'Web Campus'
        elif 'N/A' in info[3]:
            Campus = 'Main Campus'
        elif 'Main Campus' in info[3]:
            Campus = 'Main Campus'
        elif 'Web Campus' in info[3]:
            Campus = 'Web Campus'
        else:
            Campus = 'Off Campus'

        Instructor = info[4]

        if ' to ' in info[5]:
            dates = info[5].split(' to ')
            if len(dates) == 2:
                StartDate = dates[0][-8:]
                EndDate = dates[1]

        if '- ' in info[6]:
            credit = info[6].split('- ')
            if len(credit) == 2:
                MinCredit = credit[0]
                MaxCredit = credit[1]
        else:
            MinCredit = info[6]

        data = [CourseID, CourseName, CourseSection, CallNumber, Status, Seats, Day, Time, Campus, Location, Instructor,
                StartDate, EndDate, MinCredit, MaxCredit]  # put them into a list container

        self.insert_entry(data)  # insert them into database

    def parse_old_db(self):  # driver program for this class
        for call in self.call_numbers:
            query = 'select * from courses where courses.CallNumber == {}'.format(call)
            info = self.query_info(query)[0]
            self.parse_line(info)
        self.finalize()

    def finalize(self):
        self.old_cursor.close()
        self.new_cursor.close()
        self.old_conn.close()
        self.new_conn.close()


def main():
    demo = DiceData()
    demo.parse_old_db()


if __name__ == '__main__':
    main()
