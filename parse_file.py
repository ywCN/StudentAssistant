import re


class Parse:
    def __init__(self):
        self.f = self.open_file()
        self.count_valid_lines = 0
        self.count_parsed_valid_lines = 0

    def open_file(self):
        return open(r'test.txt')  # row courses file

    def parse_line(self, line):
        """
        Wrapper of the other two parse methods.
        (SectionTitle, CallNumber, StatusSeatsAvailable, DaysTimeLocation, Instructor, SessionAndDates, Credits)
        :return: tuple
        """
        return self.parse_line1(line) + self.parse_line2(line)

    def parse_line1(self, line):
        """
        Parse first part of a line to get SectionTitle, CallNumber.
        :param line: self.preprocessed
        :return: tuple
        """
        words = line.split("\" \"")
        course_name = words[0][1:].split(" - ")[0]  # this is the course name. like this: TM -616-W0
        call_number = words[1][0:5]
        return course_name, call_number

    def parse_line2(self, line):
        """
        Parse second part of a line to get StatusSeatsAvailable, DaysTimeLocation, Instructor, SessionAndDates, Credits.
        :param line:
        :return: tuple
        """
        words = line.split('cart" ')
        partition = words[1]  # contains StatusSeatsAvailable, DaysTimeLocation, Instructor, SessionAndDates, Credits
        status_seats_available = days_time_location = instructor = session_and_dates = credit = "NA"
        if partition.startswith('"Open'):
            t = partition.split('"')
            length = len(t)  # only 3 cases: 7 9 11
            if length == 7:
                status_seats_available = t[1]
                days_time_location = t[3]
                instructor = t[4][1:]
                session_and_dates = t[5]
                credit = t[6].strip()
                # print(status_seats_available)
                # print(days_time_location)
                # print(instructor)
                # print(session_and_dates)
                # print(credit)
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
                # print(status_seats_available)
                # print(days_time_location)
                # print(instructor)
                # print(session_and_dates)
                # print(credit)
            elif length == 11:
                status_seats_available = t[1]
                days_time_location = t[3]
                instructor = t[5]
                session_and_dates = t[7]
                credit = t[9]
                # print(status_seats_available)
                # print(days_time_location)
                # print(instructor)
                # print(session_and_dates)
                # print(credit)
            else:
                print("AAAAAAAAAAAAAWWWWWWWWWWWWWWGGGGGGGGGGGGGGGGG")
                self.count_parsed_valid_lines -= 1
            self.count_parsed_valid_lines += 1
        elif partition.startswith('Cancelled'):
            t = partition.split('"')
            length = len(t)  # only 3 cases: 3 5 7
            if length == 3:
                status_seats_available = t[0]
                days_time_location = t[1][len('CANCELLED '):]
                credit = t[2][-5:].strip()
                # print(status_seats_available)
                # print(days_time_location)
                # print(credit)
                # # NO instructor
                # # NO session_and_dates
            elif length == 5:
                status_seats_available = t[0]
                days_time_location = t[1][len('CANCELLED '):]
                session_and_dates = t[3]
                credit = t[4][-5:].strip()
                # print(status_seats_available)
                # print(days_time_location)
                # print(session_and_dates)
                # print(credit)
                # # NO instructor
            elif length == 7:
                status_seats_available = t[0]
                days_time_location = t[1][len('CANCELLED '):]
                session_and_dates = t[3]
                credit = t[5].strip()
                # print(status_seats_available)
                # print(days_time_location)
                # print(session_and_dates)
                # print(credit)
                # # NO instructor
            else:
                print("AAAAAAAAAWWWWWWWWWWWWWWWWWGGGGGGGGGGGGGG")
                self.count_parsed_valid_lines -= 1
            self.count_parsed_valid_lines += 1
        elif partition.startswith('Closed'):
            t = partition.split('"')
            length = len(t)  # only 3 cases: 5 7 9
            if length == 5:
                status_seats_available = t[0]
                days_time_location = t[1]
                instructor = t[2][1:]
                session_and_dates = t[3]
                credit = t[4].strip()
                # print(status_seats_available)
                # print(days_time_location)
                # print(instructor)
                # print(session_and_dates)
                # print(credit)
            elif length == 7:
                status_seats_available = t[0]
                days_time_location = t[1]
                instructor = t[3]
                session_and_dates = t[5]
                credit = t[6].strip()
                # print(status_seats_available)
                # print(days_time_location)
                # print(instructor)
                # print(session_and_dates)
                # print(credit)
            elif length == 9:
                status_seats_available = t[0]
                days_time_location = t[1]
                instructor = t[3]
                session_and_dates = t[5]
                credit = t[7]
                # print(status_seats_available)
                # print(days_time_location)
                # print(instructor)
                # print(session_and_dates)
                # print(credit)
            else:
                print("AAAAAAAAAWWWWWWWWWWWWWWWWWGGGGGGGGGGGGGG")
                self.count_parsed_valid_lines -= 1
            self.count_parsed_valid_lines += 1
        elif partition.startswith('Open '):
            t = partition.split('"')
            length = len(t)  # only 3 cases: 5 7 9
            if length == 5:
                status_seats_available = t[0]
                days_time_location = t[1]
                instructor = t[2][1:-1]
                session_and_dates = t[3]
                credit = t[4].strip()
                # print(status_seats_available)
                # print(days_time_location)
                # print(instructor)
                # print(session_and_dates)
                # print(credit)
            elif length == 7:
                status_seats_available = t[0]
                days_time_location = t[1]
                instructor = t[3]
                session_and_dates = t[5]
                credit = t[6].strip()
                # print(status_seats_available)
                # print(days_time_location)
                # print(instructor)
                # print(session_and_dates)
                # print(credit)
            elif length == 9:
                status_seats_available = t[0]
                days_time_location = t[1]
                instructor = t[3]
                session_and_dates = t[5]
                credit = t[7]
                # print(status_seats_available)
                # print(days_time_location)
                # print(instructor)
                # print(session_and_dates)
                # print(credit)
            else:
                print("AAAAAAAAAWWWWWWWWWWWWWWWWWGGGGGGGGGGGGGG")
                self.count_parsed_valid_lines -= 1
            self.count_parsed_valid_lines += 1
        else:
            print("\n\n\nthis line is not matched", partition)
        return status_seats_available, days_time_location, instructor, session_and_dates, credit

    def get_days_time_location(self):
        pass

    def get_instructor(self):
        pass

    def get_session_and_dates(self):
        pass

    def get_credits(self):
        pass

    def populate_stage1(self, txt):
        """
        Get useful lines and save them into another file. This can be an optional process.
        Later this function can be changed to a function return boolean telling if this line is valid.
        :param txt:
        :return:
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

        rg = re.compile(re1 + re2 + re3 + re4 + re5 + re6 + re7 + re8 + re9 + re10, re.IGNORECASE | re.DOTALL)
        return rg.search(txt)

    def file_works(self):
        for line in self.f:
            if self.populate_stage1(line):
                self.count_valid_lines += 1
                for item in self.parse_line(line):
                    if len(self.parse_line(line)) != 7:
                        raise Exception("wrong length")
                    else:
                        print(item)
                print()

        if self.count_valid_lines != self.count_parsed_valid_lines:
            print("\nValid lines and parsed lines are different!")
            print("Valid lines:", self.count_valid_lines, "\nParsed lines:", self.count_parsed_valid_lines)
        else:
            print("nothing is wrong")

    def get_course_dependency(self):
        pass
        # TODO: parse dependencies from PDF file using regex, dependencies have 2 or more types, 1 pre-req, 2 co-req
        '''
        A prerequisite is a requirement that must be met before you take a course, 
        while a corequisite is a course that must be taken at the same time.
        '''


def main():
    demo = Parse()
    demo.file_works()
    demo.f.close()


if __name__ == '__main__':
    main()
