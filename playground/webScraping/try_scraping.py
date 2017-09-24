from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import getpass  # this does not work well for some reasons, should make this work later
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

'''
This version is not stable. It may fail because of instability of connection.
Will be improved later.
'''


def get_login_info():
    user = input("Enter the User Name:")
    password = input("Enter the Password:")
    # print("got password")
    return user, password


def do_things():
    driver = webdriver.PhantomJS("C:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
    driver.implicitly_wait(1)  # second
    driver.get("https://mystevens.stevens.edu/sso/web4student.php")

    login(driver)

    go_to_majors_page(driver)
    get_raw_majors(driver.page_source)
    majors = parse_raw_majors()

    for major in majors:
        go_to_courses_page(driver, major)
        get_raw_courses(driver.page_source, major)
        courses = parse_raw_courses(major)

        for course in courses:
            go_to_courses_description_page(driver, course)
            parse_tables(driver.page_source)
            driver.back()

        driver.back()

    driver.quit()


def go_to_courses_description_page(driver, course_id):
    select1 = Select(driver.find_element_by_xpath('//select[option/@value="%s"]' % course_id))
    select1.select_by_value(course_id)

    driver.find_element_by_name("submitbutton").submit()


def go_to_courses_page(driver, major_id):
    select = Select(driver.find_element_by_xpath('//select[option/@value="%s"]' % major_id))
    select.select_by_value(major_id)
    driver.find_element_by_name("submitbutton").submit()
    time.sleep(2)


def go_to_majors_page(driver):
    hover1_element = driver.find_element_by_id("menuHeading5")
    hover2_element = driver.find_element_by_xpath("//div[a/@title='Course Sections']")
    ActionChains(driver).move_to_element(hover1_element).move_to_element(hover2_element).click(hover2_element).perform()
    time.sleep(2)


def login(driver):
    info = get_login_info()
    driver.find_element_by_name("j_username").send_keys(info[0])
    driver.find_element_by_name("j_password").send_keys(info[1])
    driver.find_element_by_name('submit').submit()


def get_raw_majors(source):
    # print(source)
    f = open('majors_raw.txt', 'w+')
    f.write(source)
    f.close()


def parse_raw_majors():
    target = "<option value="
    file = open('majors_raw.txt')
    # majors = {}
    majors = []
    for line in file:
        if target in line:
            words = line.strip().split("\"")
            majors.append(words[1])
            # majors[words[1]] = words[2][1:]
            # print(words[1], words[2][1:])
    return majors


def get_raw_courses(source, major):
    f = open('%s_raw.txt' % major, 'w+')
    f.write(source)
    f.close()


def parse_raw_courses(major):
    target = "<option value="
    file = open('%s_raw.txt' % major)
    # courses = {}
    courses = []
    for line in file:
        if target in line:
            words = line.strip().split("\"")
            courses.append(words[1])
            # courses[words[1]] = words[2][1:]
    return courses


def parse_tables(source):

    dfs = pd.read_html(source)
    # print(type(dfs))  # <class 'list'>
    print(dfs[4])  # normally this is the table we need
    # for df in dfs:
    #     print(df)

    # TODO: store and/or parse tables, save information in database


do_things()
