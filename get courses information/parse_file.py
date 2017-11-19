import re
import os
import sqlite3


class CleanUpDatabase:
    """
    This class is used for cleaning up data in the old database create by Parse class and create a new database.
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
        # CourseID = section_elements[0][:-1] + ' ' + section_elements[1]  # if need space, uncomment this line
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
        self.clean_up()
        self.finalize()

    def clean_up(self):
        self.new_cursor.execute("UPDATE courses SET Seats='0' WHERE Seats='NA'")
        self.new_conn.commit()
        for call in self.call_numbers:
            query = 'select * from courses where courses.CallNumber == {}'.format(call)
            info = self.query_info(query)[0]
            if len(info[2]) > 4:
                print(info[2])
                #  delete from courses where CallNumber == '10328'

    def finalize(self):
        self.old_cursor.close()
        self.new_cursor.close()
        self.old_conn.close()
        self.new_conn.close()
        # os.remove(self.old_db)  # TODO: uncomment this


class Parse:
    """
    This class will create a database used for further improvement.
    This database will be used by CleanUpDatabase class to create the final database.
    """
    def __init__(self):
        self.old_db = r'courses.db'
        if os.path.isfile(self.old_db):
            print("Please delete or rename %s and run this program again." % self.old_db)
            exit()
        else:
            self.conn = sqlite3.connect(r'courses.db')
            self.c = self.conn.cursor()
            self.create_table()
        self.raw_file = r'all_courses_raw.txt'
        try:
            self.f = open(self.raw_file)  # raw courses file
        except FileNotFoundError:
            print('Please put the {} file in the path.'.format(self.raw_file))
            exit()
        self.count_valid_lines = 0  # for validate output
        self.count_parsed_valid_lines = 0  # for validate output

    def parse_line(self, line):
        """
        Wrapper of the other two parse methods.
        (SectionTitle, CallNumber, StatusSeatsAvailable, DaysTimeLocation, Instructor, SessionAndDates, Credits)
        :return: tuple
        """
        return self.parse_line1(line) + self.parse_line2(line)  # combine two parts

    @staticmethod
    def parse_line1(line):
        """
        Parse first part of a line to get SectionTitle, CallNumber.
        :param line: self.preprocessed
        :return: tuple
        """
        words = line.split("\" \"")
        section_title = words[0][1:].split(" - ")[0]  # for example: TM -616-W0
        call_number = words[1][0:5]  # for example: 10086
        return section_title, call_number

    def parse_line2(self, line):
        """
        Parse second part of a line to get StatusSeatsAvailable, DaysTimeLocation, Instructor, SessionAndDates, Credits.
        A lot of cases.
        :param line:
        :return: tuple
        """
        words = line.split('cart" ')
        partition = words[1]  # contains StatusSeatsAvailable, DaysTimeLocation, Instructor, SessionAndDates, Credits
        status_seats_available = days_time_location = instructor = session_and_dates = credit = "NA"
        if partition.startswith('"Open'):
            t = partition.split('"')
            length = len(t)  # only 3 cases: 7 9 11
            self.count_parsed_valid_lines += 1
            if length == 7:
                status_seats_available = t[1]
                days_time_location = t[3]
                instructor = t[4][1:]
                session_and_dates = t[5]
                credit = t[6].strip()
            elif length == 9:
                status_seats_available = t[1]
                days_time_location = t[3]
                if " STAFF " in t:
                    instructor = t[4][1:-1]
                    session_and_dates = t[5]
                    credit = t[7]
                else:
                    instructor = t[5]
                    session_and_dates = t[7]
                    credit = t[8].strip()
            elif length == 11:
                status_seats_available = t[1]
                days_time_location = t[3]
                instructor = t[5]
                session_and_dates = t[7]
                credit = t[9]
            else:
                self.count_parsed_valid_lines -= 1
        elif partition.startswith('Cancelled'):
            t = partition.split('"')
            length = len(t)  # only 3 cases: 3 5 7
            self.count_parsed_valid_lines += 1
            if length == 3:
                status_seats_available = t[0]
                days_time_location = t[1][len('CANCELLED '):]
                credit = t[2][-5:].strip()
                # NO instructor. NO session_and_dates.
            elif length == 5:
                status_seats_available = t[0]
                days_time_location = t[1][len('CANCELLED '):]
                session_and_dates = t[3]
                credit = t[4][-5:].strip()
                # NO instructor.
            elif length == 7:
                status_seats_available = t[0]
                days_time_location = t[1][len('CANCELLED '):]
                session_and_dates = t[3]
                credit = t[5].strip()
                # NO instructor.
            else:
                self.count_parsed_valid_lines -= 1
        elif partition.startswith('Closed'):
            t = partition.split('"')
            length = len(t)  # only 3 cases: 5 7 9
            self.count_parsed_valid_lines += 1
            if length == 5:
                status_seats_available = t[0]
                days_time_location = t[1]
                instructor = t[2][1:]
                session_and_dates = t[3]
                credit = t[4].strip()
            elif length == 7:
                status_seats_available = t[0]
                days_time_location = t[1]
                instructor = t[3]
                session_and_dates = t[5]
                credit = t[6].strip()
            elif length == 9:
                status_seats_available = t[0]
                days_time_location = t[1]
                instructor = t[3]
                session_and_dates = t[5]
                credit = t[7]
            else:
                self.count_parsed_valid_lines -= 1
        elif partition.startswith('Open '):
            t = partition.split('"')
            length = len(t)  # only 3 cases: 5 7 9
            self.count_parsed_valid_lines += 1
            if length == 5:
                status_seats_available = t[0]
                days_time_location = t[1]
                instructor = t[2][1:-1]
                session_and_dates = t[3]
                credit = t[4].strip()
            elif length == 7:
                status_seats_available = t[0]
                days_time_location = t[1]
                instructor = t[3]
                session_and_dates = t[5]
                credit = t[6].strip()
            elif length == 9:
                status_seats_available = t[0]
                days_time_location = t[1]
                instructor = t[3]
                session_and_dates = t[5]
                credit = t[7]
            else:
                self.count_parsed_valid_lines -= 1
        else:
            print("\n\n\nthis line is not matched", partition)  # just in case
        return status_seats_available, days_time_location, instructor, session_and_dates, credit

    @staticmethod
    def pre_process_data(txt):
        """
        Get useful lines and save them into another file. This can be an optional process.
        Later this function can be changed to a function return boolean telling if this line is valid.
        regex generated by https://txt2re.com/
        :param txt:
        :return: bool
        """
        re1 = '(")'  # Any Single Character 1
        re2 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 1
        re3 = '(\\s+)'  # White Space 1
        re4 = '(-)'  # Any Single Character 2
        re5 = '(\\d+)'  # Integer Number 1
        re6 = '(-)'  # Any Single Character 3
        re7 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 2
        re8 = '.*?'  # Non-greedy match on filler
        re9 = '(\\s+)'  # White Space 2
        re10 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 3

        rg = re.compile('{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}'.format(re1, re2, re3, re4, re5, re6, re7, re8, re9, re10), re
                        .IGNORECASE | re.DOTALL)
        return rg.search(txt)

    def parse_file(self):
        for line in self.f:
            if self.pre_process_data(line):
                self.count_valid_lines += 1
                items = self.parse_line(line)
                if len(items) != 7:
                    raise Exception("wrong length")
                else:
                    self.insert_entry(items)

        if self.count_valid_lines != self.count_parsed_valid_lines:
            print("\nValid lines and parsed lines are different!")
            print("Valid lines:", self.count_valid_lines, "\nParsed lines:", self.count_parsed_valid_lines)
        else:
            print("--------------------------------------"
                  "\n| Nothing seems wrong. Take a break. |"
                  "\n--------------------------------------")
        self.finalize()

    def create_table(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS courses(SectionTitle TEXT, CallNumber TEXT, StatusSeatsAvailable "
                       "TEXT, DaysTimeLocation TEXT, Instructor TEXT, SessionAndDates TEXT, Credits TEXT)")

    def insert_entry(self, data):
        self.c.execute("INSERT INTO courses (SectionTitle, CallNumber, StatusSeatsAvailable, DaysTimeLocation, "
                       "Instructor, SessionAndDates, Credits) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
        self.conn.commit()  # required, or nothing happens

    def finalize(self):
        self.f.close()
        self.c.close()
        self.conn.close()


def main():
    # demo1 = Parse()  # TODO: uncomment this
    # demo1.parse_file()  # create a initial version of the database # TODO: uncomment this

    demo2 = CleanUpDatabase()
    demo2.parse_old_db()  # process the initial version of the database


if __name__ == '__main__':
    main()
