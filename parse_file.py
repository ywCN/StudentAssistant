import re


class Parse:
    def __init__(self):
        self.f = self.open_file()
        self.count_course = 0
        self.count_course_control_group = 0

    def open_file(self):
        return open(r'test.txt')

    def get_course_name(self, line):
        re1 = '(")'  # Any Single Character 1
        re2 = '((?:[a-z][a-z]+))'  # Word 1
        re3 = '(\\s+)'  # White Space 1
        re4 = '(-)'  # Any Single Character 2
        re5 = '(\\d+)'  # Integer Number 1
        re6 = '(-)'  # Any Single Character 3
        re7 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 1
        re8 = '(\\s+)'  # White Space 2
        re9 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 2
        re10 = '( )'  # Any Single Character 4
        re11 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 3
        re12 = '( )'  # Any Single Character 5
        re13 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 4
        re14 = '( )'  # Any Single Character 6
        re15 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 5
        re16 = '(")'  # Any Single Character 7

        rg = re.compile(
            re1 + re2 + re3 + re4 + re5 + re6 + re7 + re8 + re9 + re10 + re11 + re12 + re13 + re14 + re15 + re16,
            re.IGNORECASE | re.DOTALL)
        m = rg.search(line)
        if m:
            c1 = m.group(1)
            word1 = m.group(2)
            ws1 = m.group(3)
            c2 = m.group(4)
            int1 = m.group(5)
            c3 = m.group(6)
            var1 = m.group(7)
            ws2 = m.group(8)
            var2 = m.group(9)
            c4 = m.group(10)
            var3 = m.group(11)
            c5 = m.group(12)
            var4 = m.group(13)
            c6 = m.group(14)
            var5 = m.group(15)
            c7 = m.group(16)
            print("{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}{15}\n".format(c1, word1, ws1, c2, int1, c3, var1,
                                                                                    ws2, var2, c4, var3, c5, var4, c6,
                                                                                    var5, c7))
            self.count_course += 1

            # course_name_regex = ''
            # m = re.search(course_name_regex, line)
            # course_name = ''
            # if m:
            #     course_name = m.group(1)
            # return course_name

    def get_course_name1(self, line):
        re1 = '(")'  # Any Single Character 1
        re2 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 1
        re3 = '(\\s+)'  # White Space 1
        re4 = '(-)'  # Any Single Character 2
        re5 = '(\\d+)'  # Integer Number 1
        re6 = '(-)'  # Any Single Character 3
        re7 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 2
        re8 = '(\\s+)'  # White Space 2
        re9 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 3
        re10 = '( )'  # Any Single Character 4
        re11 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 4
        re12 = '( )'  # Any Single Character 5
        re13 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 5
        re14 = '(")'  # Any Single Character 6

        rg = re.compile(re1 + re2 + re3 + re4 + re5 + re6 + re7 + re8 + re9 + re10 + re11 + re12 + re13 + re14,
                        re.IGNORECASE | re.DOTALL)
        m = rg.search(line)
        if m:
            c1 = m.group(1)
            var1 = m.group(2)
            ws1 = m.group(3)
            c2 = m.group(4)
            int1 = m.group(5)
            c3 = m.group(6)
            var2 = m.group(7)
            ws2 = m.group(8)
            var3 = m.group(9)
            c4 = m.group(10)
            var4 = m.group(11)
            c5 = m.group(12)
            var5 = m.group(13)
            c6 = m.group(14)
            print(
                "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}\n".format(c1, var1, ws1, c2, int1, c3, var2, ws2, var3,
                                                                          c4, var4, c5, var5, c6))
            self.count_course += 1

    def print_course_name(self):
        for line in self.f:
            if "Open" in line:
                self.count_course_control_group += 1
            self.get_course_name(line)
            self.get_course_name1(line)

        print(self.count_course)
        print(self.count_course_control_group)


def main():
    demo = Parse()
    demo.print_course_name()
    demo.f.close()


if __name__ == '__main__':
    main()
