import re


class Parse:
    def __init__(self):
        self.f = self.open_file()
        self.count_course = 0
        self.count_course_control_group = 0

    def open_file(self):
        return open(r'test.txt')

    def get_course_name(self, txt):
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
            self.count_course += 1

        # TODO : parse dependencies from PDF file



    def print_course_name(self):
        for line in self.f:
            self.get_course_name(line)
        print(self.count_course)


def main():
    demo = Parse()
    demo.print_course_name()
    demo.f.close()


if __name__ == '__main__':
    main()
