import re

class Parse:
    def __init__(self):
        self.f = self.open_file()

    def open_file(self):
        return open(r'test.txt')

    def get_course_name(self, line):
        re1 = '(")'  # Any Single Character 1
        re2 = '((?:[a-z][a-z]+))'  # Word 1
        re3 = '(\\s+)'  # White Space 1
        re4 = '(-)'  # Any Single Character 2
        re5 = '.*?'  # Non-greedy match on filler
        re6 = '(-)'  # Any Single Character 3
        re7 = '.*?'  # Non-greedy match on filler
        re8 = '(\\s+)'  # White Space 2
        re9 = '.*?'  # Non-greedy match on filler
        re10 = '(")'  # Any Single Character 4

        rg = re.compile(re1 + re2 + re3 + re4 + re5 + re6 + re7 + re8 + re9 + re10, re.IGNORECASE | re.DOTALL)
        m = rg.search(line)
        if m:
            c1 = m.group(1)
            word1 = m.group(2)
            ws1 = m.group(3)
            c2 = m.group(4)
            c3 = m.group(5)
            ws2 = m.group(6)
            c4 = m.group(7)
            print("({0})({1})({2})({3})({4})({5})({6})\n".format(c1, word1, ws1, c2, c3, ws2, c4))

        # course_name_regex = ''
        # m = re.search(course_name_regex, line)
        # course_name = ''
        # if m:
        #     course_name = m.group(1)
        # return course_name

    def print_course_name(self):
        for line in self.f:
            self.get_course_name(line)


def main():
    demo = Parse()
    demo.print_course_name()
    demo.f.close()


if __name__ == '__main__':
    main()
