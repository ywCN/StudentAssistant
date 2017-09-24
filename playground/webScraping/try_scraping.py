from selenium import webdriver
from selenium.webdriver.support.ui import Select
import getpass  # this does not work well for some reasons, should make this work later
import time
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd



def get_login_info():
    user = input("Enter the User Name:")
    password = input("Enter the Password:")
    # print("got password")
    return user, password


def do_things():
    driver = webdriver.PhantomJS("C:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
    driver.implicitly_wait(1)  # second
    driver.get("https://mystevens.stevens.edu/sso/web4student.php")
    # time.sleep(2)
    login(driver)
    # time.sleep(2)
    hover1_element = driver.find_element_by_id("menuHeading5")
    # print(hover1_element)
    hover2_element = driver.find_element_by_xpath("//div[a/@title='Course Sections']")
    # print(hover2_element)
    ActionChains(driver).move_to_element(hover1_element).move_to_element(hover2_element).click(hover2_element).perform()
    # # time.sleep(2)
    # ActionChains(driver).perform()
    # # time.sleep(2)
    # ActionChains(driver)..perform()
    time.sleep(2)
    # # majors = driver.find_elements_by_xpath("//select[option]")
    # majors = driver.find_elements_by_xpath("//select[option/@value]")
    # # print(type(classes))  # it is a list
    # # print(majors[0])
    # # print(majors[1])
    # majors[0].click() # test one object in the list
    # driver.find_element_by_name('submitbutton').submit()
    # time.sleep(2)
    # courses = driver.find_elements_by_xpath("//select[option]")
    # courses[0].click()
    # driver.find_element_by_name('submitbutton').submit()
    # time.sleep(2)
    # print("no problem!")
    get_raw_majors(driver.page_source)
    majors = parse_raw_major()
    # driver.find_element_by_xpath('//select[option/@value="%s"]' % majors[0]).click()

    # driver.find_element_by_xpath('//select[option/@value="BME"]').click()
    major_id = "CS"
    select = Select(driver.find_element_by_xpath('//select[option/@value="%s"]' % major_id))
    # select.select_by_visible_text("%s" % majors[major_id])  # works
    select.select_by_value(major_id)
    driver.find_element_by_name("submitbutton").submit()
    time.sleep(2)
    # page = driver.find_element_by_xpath("//tr[td/@class='dddefault']")  # dddefaultcenter should also be included
    # print(driver.page_source)
    get_raw_courses(driver.page_source, major_id)
    # majors = driver.find_elements_by_xpath()
    # print(majors)
    courses = parse_raw_courses(major_id)
    # print(courses)
    course_id = "CS  -570"
    select1 = Select(driver.find_element_by_xpath('//select[option/@value="%s"]' % course_id))
    # select1.select_by_visible_text("%s" % courses[course_id])  # does not work
    select1.select_by_value(course_id)
    # select1.select_by_visible_text('CS  -570 Intro Program/Data Struct/Algor')  # does not work
    driver.find_element_by_name("submitbutton").submit()
    time.sleep(2)
    # print(driver.page_source)
    parse_tables(driver.page_source)
    driver.quit()


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


def parse_raw_major():
    target = "<option value="
    file = open('majors_raw.txt')
    majors = {}
    for line in file:
        if target in line:
            words = line.strip().split("\"")
            majors[words[1]] = words[2][1:]
            # print(words[1], words[2][1:])
    return majors


def get_raw_courses(source, major):
    f = open('%s_raw.txt' % major, 'w+')
    f.write(source)
    f.close()


def parse_raw_courses(major):
    target = "<option value="
    file = open('%s_raw.txt' % major)
    courses = {}
    for line in file:
        if target in line:
            words = line.strip().split("\"")
            courses[words[1]] = words[2][1:]
    return courses


def parse_tables(source):

    dfs = pd.read_html(source)
    # print(type(dfs))  # <class 'list'>
    print(dfs[4])  # normally this is the table we need
    # for df in dfs:
    #     print(df)


do_things()
