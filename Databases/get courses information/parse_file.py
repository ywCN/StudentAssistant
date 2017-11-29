import re
import os
import sqlite3
import unittest


class Parse:
    """
    This class will create a database used for further improvement.
    This database will be used by CleanUpDatabase class to create the final database.
    """
    def __init__(self):
        self.old_db = r'courses.db'
        if os.path.isfile(self.old_db):
            os.remove(self.old_db)
        self.conn = sqlite3.connect(self.old_db)
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
    def is_valid_line(txt):
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
            if self.is_valid_line(line):
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
                os.remove(self.new_db)
            self.new_conn = sqlite3.connect(self.new_db)  # new db
            self.new_cursor = self.new_conn.cursor()
            self.create_table()
        else:
            print("Please put {} in the same path of this .py file.".format(self.old_db))
            exit()
        self.call_numbers = self.get_all_call_numbers()  # for looping through the old database

    def get_all_call_numbers(self):
        query = 'select courses.CallNumber from courses'
        calls = self.query_info_from_old_db(query)
        call_numbers = []
        for call in calls:
            call_numbers.append(call[0])
        return call_numbers

    def query_info_from_old_db(self, query):  # in old database
        """
        :type query: str
        :rtype: List[List[str]]
        """
        self.old_cursor.execute("{}".format(query))
        return self.old_cursor.fetchall()

    def query_info_from_new_db(self, query):  # in old database
        """
        :type query: str
        :rtype: List[List[str]]
        """
        self.new_cursor.execute("{}".format(query))
        return self.new_cursor.fetchall()

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
        for call_number in self.call_numbers:
            query = 'select * from courses where courses.CallNumber == {}'.format(call_number)
            info = self.query_info_from_old_db(query)[0]
            self.parse_line(info)
        self.clean_up()
        self.finalize()

    def clean_up(self):
        self.new_cursor.execute("UPDATE courses SET Seats='0' WHERE Seats='NA'")
        self.new_cursor.execute("UPDATE courses SET Location='NA' WHERE Location=''")
        for call_number in self.call_numbers:
            query = 'select * from courses where courses.CallNumber == {}'.format(call_number)
            info = self.query_info_from_new_db(query)[0]
            if len(info[2]) > 4:
                self.new_cursor.execute("delete from courses where CallNumber == '{}'".format(call_number))
        self.new_conn.commit()

    def finalize(self):
        self.old_cursor.close()
        self.new_cursor.close()
        self.old_conn.close()
        self.new_conn.close()
        os.remove(self.old_db)


class TestParser(unittest.TestCase):
    def setUp(self):
        self.demo = Parse()

    def test_validation(self):
        """
        Test the validating function. See if it can handle bad inputs.
        :return:
        """

        str0 = ''
        self.assertFalse(self.demo.is_valid_line(str0))

        str1 = 'sasda/asdad/'
        self.assertFalse(self.demo.is_valid_line(str1))

        str2 = 'SectionTitle "Call Number" "StatusSeats Available" Activity "Days TimeLocation" Instructor "Session ' \
               'and Dates" Credits '
        self.assertFalse(self.demo.is_valid_line(str2))

        str3 = '"BIO -201-A  Intro to Bio for Non-Sci/Eng Maj" "12363 Add BIO -201-A to cart" "Open - 12 of 30" ' \
               'lecture "MW 09:00-09:30AM  Main Campus" "Agresti C" "Normal Academic Term01-17-18 to 05-16-18" 3.00 '
        self.assertTrue(self.demo.is_valid_line(str3))

        str4 = ' "Add to cart"  lecture "R 12:00-12:50PM  Main Campus"   '
        self.assertFalse(self.demo.is_valid_line(str4))

        str5 = '"Activity corequisite required RCT"       '
        self.assertFalse(self.demo.is_valid_line(str5))

    def test_parser(self):
        """
        Test the parse function. See if it can return expected result.
        Note the input must be valid because the original code will check line before parsing.
        :return:
        """

        str0 = '"BIO -201-A  Intro to Bio for Non-Sci/Eng Maj" "12363 Add BIO -201-A to cart" "Open - 12 of 30" ' \
               'lecture "MW 09:00-09:30AM  Main Campus" "Agresti C" "Normal Academic Term01-17-18 to 05-16-18" 3.00 '
        str0_parsed = ('BIO -201-A  Intro to Bio for Non-Sci/Eng Maj', '12363', 'Open - 12 of 30', 'MW 09:00-09:30AM  '
                       'Main Campus', 'Agresti C', 'Normal Academic Term01-17-18 to 05-16-18', '3.00')
        self.assertEqual(self.demo.parse_line(str0), str0_parsed)

        str1 = '"HAR -320-A  Video II" "12351 Add HAR -320-A to cart" "Open - 4 of 12" lecture "R 01:00-04:50PM  Main ' \
               'Campus Morton Complex 201" "Manzione C" "Normal Academic Term01-17-18 to 05-16-18" 3.00 '
        str1_parsed = ('HAR -320-A  Video II', '12351', 'Open - 4 of 12', 'R 01:00-04:50PM  Main Campus Morton '
                       'Complex 201', 'Manzione C', 'Normal Academic Term01-17-18 to 05-16-18', '3.00')
        self.assertEqual(self.demo.parse_line(str1), str1_parsed)

    def tearDown(self):
        self.demo.finalize()


def main():
    demo1 = Parse()
    demo1.parse_file()  # create a initial version of the database

    demo2 = CleanUpDatabase()
    demo2.parse_old_db()  # process the initial version of the database


if __name__ == '__main__':
    main()
    unittest.main()
