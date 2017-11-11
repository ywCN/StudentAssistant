import re
import os
import sqlite3


class Parse:
    def __init__(self):
        self.db_name = r'courses.db'
        if os.path.isfile(self.db_name):
            print("Please delete or rename %s and run this program again." % self.db_name)
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

    def parse_file_into_database(self):
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
    demo = Parse()
    demo.parse_file_into_database()


if __name__ == '__main__':
    main()
