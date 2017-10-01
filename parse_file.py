import re


class Parse:
    def __init__(self):
        self.f = self.open_file()
        self.count_title = 0
        self.count_call_number = 0

    def open_file(self):
        return open(r'test.txt')

    def get_section_title(self, txt):
        re1 = '(")'  # Any Single Character 1
        re2 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 1
        re3 = '(\\s+)'  # White Space 1
        re4 = '(-)'  # Any Single Character 2
        re5 = '(\\d+)'  # Integer Number 1
        re6 = '(-)'  # Any Single Character 3

        rg = re.compile(re1 + re2 + re3 + re4 + re5 + re6, re.IGNORECASE | re.DOTALL)
        m = rg.search(txt)
        if m:
            words = txt.split("\" \"")
            course_name = words[0][1:].split(" - ")[0]  # this is the course name. like this: TM -612-WS  Regul/Plcy Telecomm Ind.
            print(course_name)
            print(words[1][0:5])
            self.count_title += 1

        # TODO: if m, return result. return "NA" at the end.
        # TODO: create other similar functions by using regex for CallNumber, StatusSeatsAvailable, DaysTimeLocation, Instructor, SessionAndDates, Credits
        # TODO: in order to populate the list

    def get_call_number(self, txt):
        pass
        # TODO: pre populate a list with "NA"
        # TODO: [SectionTitle, CallNumber, StatusSeatsAvailable, DaysTimeLocation, Instructor, SessionAndDates, Credits]
        # TODO:

    def get_status_seats_available(self):
        pass

    def get_days_time_location(self):
        pass

    def get_instructor(self):
        pass

    def get_session_and_dates(self):
        pass

    def get_credits(self):
        pass



    def print_function(self):
        for line in self.f:
            self.get_section_title(line)
        print(self.count_title)

    def get_course_dependency(self):
        pass
        # TODO: parse dependencies from PDF file using regex, dependencies have 2 or more types, 1 pre, 2 coreq
        '''
        A prerequisite is a requirement that must be met before you take a course, 
        while a corequisite is a course that must be taken at the same time.
        '''


def main():
    demo = Parse()
    demo.print_function()
    demo.f.close()


if __name__ == '__main__':
    main()
