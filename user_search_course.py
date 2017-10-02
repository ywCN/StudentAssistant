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
        # self.course_list = self.create_course_list()
        # self.major_list = self.create_major_list()

    def create_course_list(self):
        pass
        # TODO: query database course titles

    def create_major_list(self):
        pass

    def analyze_database_section_title(self):
        query = "SELECT SectionTitle from courses"
        titles = self.query_info(query)
        for title in titles:
            print(title)
        # return course_list, major_list

    def query_info(self, query):
        """
        :type query: str
        :rtype: List[List[str]]
        """
        self.c.execute("%s" % query)
        return self.c.fetchall()

    def ask_major(self):
        pass

        # TODO: getting input from user

    def ask_course(self):
        pass

        # TODO: getting input from user

    def create_query(self):
        """
        SELECT * FROM course WHERE ______
        :return: str
        """
        major = self.ask_major()
        course = self.ask_course()

    def disconnect(self):
        """
        :return: null
        """
        self.c.close()
        self.conn.close()


def main():
    demo = SearchCourse()
    demo.analyze_database_section_title()
    demo.disconnect()


if __name__ == '__main__':
    main()

