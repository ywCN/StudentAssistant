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

    def get_status_seats_available(self, txt):  # all if statements have covered all cases for status
        words = txt.split('cart" ')
        res = ''
        # print(words[1])  # this part contains StatusSeatsAvailable, DaysTimeLocation, Instructor, SessionAndDates, Credits
        test = words[1]
        credit = "AAAAAAAAAWWWWWWGGGGGGGGGGGGGGGGGGGGG"
        if test.startswith('"Open'):
            t = test.split('"')
            # print(t[1])  # StatusSeatsAvailable
            # print(t[3])  # DaysTimeLocation

            # if test.endswith('"'):
            #     credit = t[-2].strip()
            # else:
            #     credit = t[-1].strip()
            #
            # print(credit)
            # print(t[4:])
            self.count_status += 1
        elif test.startswith('Cancelled'):
            t = test.split('"')
            # print(t[1])  # StatusSeatsAvailable
            length = len(t)
            if length == 3:
                print(t)
            # elif length == 5:
            #     print(t)
            # elif length == 7:
            #     print(t)
            # else:
            #     print("AAAAAAAAAWWWWWWWWWWWWWWWWWGGGGGGGGGGGGGG")
            # print(t[3])  # DaysTimeLocation
            self.count_status += 1
        elif test.startswith('Closed'):
            self.count_status += 1
        elif test.startswith('Open '):
            self.count_status += 1
        else:
            print("this line is not matched", test)

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
