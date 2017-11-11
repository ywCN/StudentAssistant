from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

'''
Install PhantomJS before running this.
Run this ONLY in a terminal, NOT in IDE.
Currently this program only print scrapped info.
'''


class ScrapStevensCourses:

    def __init__(self):
        self.driver = webdriver.PhantomJS("C:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
        self.driver.implicitly_wait(10)  # wait up to 10 second for the targeting element
        self.driver.get("https://mystevens.stevens.edu/sso/web4student.php")
        self.raw_courses = open('all_courses_raw.txt', 'w+')  # output
        self.errors = open('errors.txt', 'w+')  # for unusual cases

    def login(self):
        self.driver.find_element_by_name("j_username").send_keys(input("Enter the User Name:"))
        self.driver.find_element_by_name("j_password").send_keys(input("Enter the Password:"))
        self.driver.find_element_by_name('submit').submit()

    def go_to_courses_description_page(self, course_id):
        select = Select(self.driver.find_element_by_xpath('//select[option/@value="%s"]' % course_id))
        select.select_by_value(course_id)
        self.driver.find_element_by_name("submitbutton").submit()

    def go_to_courses_page(self, major_id):
        select = Select(self.driver.find_element_by_xpath('//select[option/@value="%s"]' % major_id))
        select.select_by_value(major_id)
        self.driver.find_element_by_name("submitbutton").submit()

    def go_to_majors_page(self):
        hover1_element = self.driver.find_element_by_id("menuHeading5")
        hover2_element = self.driver.find_element_by_xpath("//div[a/@title='Course Sections']")
        ActionChains(self.driver)\
            .move_to_element(hover1_element)\
            .move_to_element(hover2_element)\
            .click(hover2_element).perform()
        time.sleep(2)

    def get_raw_majors(self):
        """
        write raw page source into a file.
        :return: none
        """
        f = open('majors_raw.txt', 'w+')
        f.write(self.driver.page_source)
        f.close()

    def parse_raw_majors(self):
        """
        Return a list of major names for future navigation.
        :param : str
        :return: List
        """
        self.get_raw_majors()  # need to close it before using the file again
        target = "<option value="
        file = open('majors_raw.txt')
        majors = []
        for line in file:
            if target in line:
                words = line.strip().split("\"")
                majors.append(words[1])
        return majors

    def get_raw_courses(self, major):
        """
        write raw page source into a file.
        :param major:
        :return: none
        """
        f = open('%s_raw.txt' % major, 'w+')
        f.write(self.driver.page_source)
        f.close()

    def parse_raw_courses(self, major):
        """
        Return a list of course names for future navigation.
        :param major: str
        :return: List
        """
        self.get_raw_courses(major)  # need to close it before using the file again
        target = "<option value="
        file = open('%s_raw.txt' % major)
        courses = []
        for line in file:
            if target in line:
                words = line.strip().split("\"")
                courses.append(words[1])
        file.close()
        return courses

    def save_tables(self):

        dfs = pd.read_html(self.driver.page_source)
        try:
            line = dfs[4].to_csv(sep=' ', index=False, header=False)  # this is the table we need
            line = line.replace(u'\xa0', u' ')  # remove invalid character
            self.raw_courses.write(line)
        except IndexError:  # just in case
            for line in dfs:
                line = line.replace(u'\xa0', u' ')
                self.errors.write(line.to_csv(sep=' ', index=False, header=False))

    def parse_tables(self):  # main driver for this program
        self.login()

        self.go_to_majors_page()
        majors = self.parse_raw_majors()  # major list

        for major in majors:
            self.go_to_courses_page(major)
            courses = self.parse_raw_courses(major)

            for course in courses:  # course list for each major
                self.go_to_courses_description_page(course)
                self.save_tables()
                self.driver.back()

            self.driver.back()

        self.driver.quit()
        self.raw_courses.close()
        self.errors.close()


def main():
    demo = ScrapStevensCourses()
    demo.parse_tables()


if __name__ == '__main__':
    main()
