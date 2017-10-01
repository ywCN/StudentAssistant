import re

class Parse:
    def __init__(self):
        self.f = self.open_file()

    def open_file(self):
        return open(r'test.txt')

    def get_course_name(self, line):
        course_name_regex = ''
        m = re.search(course_name_regex, line)
        course_name = ''
        if m:
            course_name = m.group(1)
        return course_name
