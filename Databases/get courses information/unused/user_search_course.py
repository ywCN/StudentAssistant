from prettytable import PrettyTable
import sqlite3
import os


class SearchCourse:
    def __init__(self):
        self.db_name = r'courses.db'
        if os.path.isfile(self.db_name):
            self.conn = sqlite3.connect(r'courses.db')
            self.c = self.conn.cursor()
        else:
            print("Please put %s in the same path of this .py file." % self.db_name)
            exit()
        self.majors = self.analyze_database_section_title()[0]
        self.courses = self.analyze_database_section_title()[1]

    def analyze_database_section_title(self):
        majors = set()
        courses = {}
        query = "SELECT SectionTitle from courses"
        titles = self.query_info(query)
        for title in titles:
            words = title[0].split()
            majors.add(words[0])
            if words[0] in courses:
                courses[words[0]].add(words[0] + " " + words[1][:4])
            else:
                courses[words[0]] = set()

        return majors, courses

    def query_info(self, query):
        """
        :type query: str
        :rtype: List[List[str]]
        """
        self.c.execute("%s" % query)
        return self.c.fetchall()

    def ask_major(self):
        print(self.majors)
        major = input("Enter major:")
        while major.upper() not in self.majors:
            print("Major not found. Please enter again.")
            major = input("Enter major:")
        return major.upper()

    def ask_course(self):
        major = self.ask_major()
        print(self.courses[major])
        course = input("Enter course:")
        while course not in self.courses[major] and major + " -" + course not in self.courses[major]:
            course = input("Enter course:")
        if len(course) == 3:
            course = major + " -" + course
        return course

    def create_query(self):
        """
        SELECT * FROM courses WHERE SectionTitle LIKE '%SSW -555%'
        :return: str
        """
        course = self.ask_course()
        item = ["SELECT * FROM courses WHERE SectionTitle LIKE '%", course, "%'"]
        return "".join(item)

    def disconnect(self):
        """
        :return: null
        """
        self.c.close()
        self.conn.close()

    def display(self):
        t = PrettyTable(['SectionTitle', 'CallNumber', 'StatusSeatsAvailable', 'DaysTimeLocation', 'Instructor', 'SessionAndDates', 'Credits'])
        query = self.create_query()
        entries = self.query_info(query)
        for entry in entries:
            t.add_row(entry)
        print(t)


def main():
    demo = SearchCourse()
    demo.display()
    demo.disconnect()


if __name__ == '__main__':
    main()
