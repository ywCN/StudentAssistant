import re


class Parse:
    def __init__(self):
        self.f = self.open_file()
        self.count_title_call_number = 0
        self.count_title_call_number_control = 0
        self.count_status = 0
        self.stage1 = self.open_stage1()

    def open_file(self):
        return open(r'test.txt')  # row courses file

    def open_stage1(self):
        return open(r'stage1.txt', 'w+')

    def get_section_title_and_call_number(self, txt):

        re1 = '(")'  # Any Single Character 1
        re2 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 1
        re3 = '(\\s+)'  # White Space 1
        re4 = '(-)'  # Any Single Character 2
        re5 = '(\\d+)'  # Integer Number 1
        re6 = '(-)'  # Any Single Character 3
        re7 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 2
        re8 = '.*?'  # Non-greedy match on filler
        re9 = '((?:[a-z][a-z0-9_]*))'
        re10 = '(")'  # Any Single Character 4

        rg = re.compile(re1 + re2 + re3 + re4 + re5 + re6 + re7 + re8 + re9 + re10, re.IGNORECASE | re.DOTALL)
        m = rg.search(txt)
        if m:
            words = txt.split("\" \"")
            course_name = words[0][1:].split(" - ")[0]  # this is the course name. like this: TM -616-W0
            print(course_name)
            call_number = words[1][0:5]
            print(call_number)  # this is the call number, like this: 10086
            self.count_title_call_number += 1
            # return course_name, call_number
        else:
            print("no match found")

        # TODO: if m, return result. return "NA" at the end.
        # TODO: create other similar functions by using regex for CallNumber, StatusSeatsAvailable, DaysTimeLocation, Instructor, SessionAndDates, Credits
        # TODO: in order to populate the list

    def get_status_seats_available(self, txt):
        # TODO: fill available variables; unavailable one are left with default "NA"
        words = txt.split('cart" ')
        # print(words[1])  # this part contains StatusSeatsAvailable, DaysTimeLocation, Instructor, SessionAndDates, Credits
        test = words[1]
        StatusSeatsAvailable = DaysTimeLocation = Instructor = SessionAndDates = Credits = "NA"
        if test.startswith('"Open'):
            # t = test.split('"')
            # length = len(t)  # only 3 cases: 7 9 11
            # if length == 7: #TODO: uncomment this
            #     # print(t)
            #     print(t[1])  # StatusSeatsAvailable
            #     print(t[3])  # DaysTimeLocation
            #     print(t[4][1:])  # Instructor
            #     print(t[5])  # SessionAndDates
            #     print(t[6].strip())  # credit
            # elif length == 9:
            #     print(t)
            #     print(t[1])  # StatusSeatsAvailable
            #     print(t[3])  # DaysTimeLocation
            #     print(t[5])  # Instructor
            #     if " STAFF " in t:
            #         print(t[4][1:-1])  # Instructor
            #     print(t[7])  # SessionAndDates
            #     print(t[8].strip())  # credit
            # elif length == 11:
            #     print(t)
            #     print(t[1])  # StatusSeatsAvailable
            #     print(t[3])  # DaysTimeLocation
            #     print(t[5])  # Instructor
            #     print(t[7])  # SessionAndDates
            #     print(t[9])  # credit
            # else: #TODO: uncomment this
            #     print("AAAAAAAAAAAAAWWWWWWWWWWWWWWGGGGGGGGGGGGGGGGG")
            # print(t[1])  # StatusSeatsAvailable
            # print(t[3])  # DaysTimeLocation
            #
            # if test.endswith('"'):
            #     credit = t[-2]
            # else:
            #     credit = t[-1].strip()
            #
            # print(credit)
            # print(t[4:])
            self.count_status += 1
            # TODO: fill available variables
        # elif test.startswith('Cancelled'):  #TODO: uncomment this
        #     t = test.split('"')
        #     length = len(t)  # only 3 cases: 3 5 7
        #     if length == 3:
        #         print(t[0])  # StatusSeatsAvailable
        #         print(t[1][len('CANCELLED '):])  # DaysTimeLocation
        #         print(t[2][-5:].strip())  # credit
        #         # NO Instructor
        #         # NO SessionAndDates
        #     elif length == 5:
        #         print(t)
        #         print(t[0])  # StatusSeatsAvailable
        #         print(t[1][len('CANCELLED '):])  # DaysTimeLocation
        #         print(t[3])  # SessionAndDates
        #         print(t[4][-5:].strip())  # credit
        #         # NO Instructor
        #     elif length == 7:
        #         # print(t)
        #         print(t[0])  # StatusSeatsAvailable
        #         print(t[1][len('CANCELLED '):])  # DaysTimeLocation
        #         print(t[3])  # SessionAndDates
        #         print(t[5].strip())  # credit
        #         # NO Instructor
        #     else:
        #         print("AAAAAAAAAWWWWWWWWWWWWWWWWWGGGGGGGGGGGGGG")
        #     self.count_status += 1
        # TODO: fill available variables
        # elif test.startswith('Closed'):
        #     t = test.split('"')
        #     length = len(t)  # only 3 cases: 5 7 9
        #     if length == 5:
        #         print(t)
        #         print(t[0])  # StatusSeatsAvailable
        #         print(t[1])  # DaysTimeLocation
        #         print(t[2][1:])  # Instructor
        #         print(t[3])  # SessionAndDates
        #         print(t[4].strip())  # credit
        #     elif length == 7:
        #         print(t)
        #         print(t[0])  # StatusSeatsAvailable
        #         print(t[1])  # DaysTimeLocation
        #         print(t[3])  # Instructor
        #         print(t[5])  # SessionAndDates
        #         print(t[6])  # credit
        #     elif length == 9:
        #         print(t)
        #         print(t[0])  # StatusSeatsAvailable
        #         print(t[1])  # DaysTimeLocation
        #         print(t[3])  # Instructor
        #         print(t[5])  # SessionAndDates
        #         print(t[7])  # credit
        #     else:
        #         print("AAAAAAAAAWWWWWWWWWWWWWWWWWGGGGGGGGGGGGGG")
        #     self.count_status += 1
        # TODO: fill available variables

        elif test.startswith('Open '):
            t = test.split('"')
            length = len(t)  # only 3 cases: 5 7 9
            if length == 5:
                pass
            elif length == 7:
                pass
            elif length == 9:
                pass
            # else:
            #     print("AAAAAAAAAWWWWWWWWWWWWWWWWWGGGGGGGGGGGGGG")

            self.count_status += 1
        # else:
        #     print("this line is not matched", test)

    def get_days_time_location(self):
        pass

    def get_instructor(self):
        pass

    def get_session_and_dates(self):
        pass

    def get_credits(self):
        pass

    def populate_stage1(self, txt):
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
        m = rg.search(txt)
        if m:
            self.stage1.write(txt)
            self.count_title_call_number_control += 1

    def file_works(self):
        for line in self.f:
            self.populate_stage1(line)

        self.stage1.close()
        self.stage1 = open(r'stage1.txt')

        for line in self.stage1:
            # self.get_section_title_and_call_number(line)
            self.get_status_seats_available(line)

        # print(self.count_title_call_number)
        print(self.count_title_call_number_control)
        print(self.count_status)

    def get_course_dependency(self):
        pass
        # TODO: parse dependencies from PDF file using regex, dependencies have 2 or more types, 1 pre, 2 coreq
        '''
        A prerequisite is a requirement that must be met before you take a course, 
        while a corequisite is a course that must be taken at the same time.
        '''


def main():
    demo = Parse()
    demo.file_works()
    demo.f.close()
    demo.stage1.close()


if __name__ == '__main__':
    main()
