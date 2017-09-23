from selenium import webdriver
from selenium.webdriver.support.ui import Select
import getpass  # this does not work well for some reasons
import time
from selenium.webdriver.common.action_chains import ActionChains
import bs4 as bs
import pandas as pd


def get_user_password():
    user = input("Enter the User Name:")
    password = input("Enter the Password:")
    # print("got password")
    return user, password


def do_things():
    info = get_user_password()
    driver = webdriver.PhantomJS("C:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
    driver.get("https://mystevens.stevens.edu/sso/web4student.php")
    time.sleep(2)
    driver.find_element_by_name("j_username").send_keys(info[0])
    driver.find_element_by_name("j_password").send_keys(info[1])
    driver.find_element_by_name('submit').submit()
    time.sleep(2)
    hover1_element = driver.find_element_by_id("menuHeading5")
    # print(hover1_element)
    hover2_element = driver.find_element_by_xpath("//div[a/@title='Course Sections']")
    # print(hover2_element)
    hover1 = ActionChains(driver).move_to_element(hover1_element)
    hover1.perform()
    time.sleep(2)
    hover2 = ActionChains(driver).move_to_element(hover2_element)
    hover2.perform()
    time.sleep(2)
    hover3 = ActionChains(driver).click(hover2_element)
    hover3.perform()
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
    select.select_by_visible_text("%s" % majors[major_id])
    driver.find_element_by_name("submitbutton").submit()
    time.sleep(2)
    # page = driver.find_element_by_xpath("//tr[td/@class='dddefault']")  # dddefaultcenter should also be included
    # print(driver.page_source)
    get_raw_courses(driver.page_source, major_id)
    # majors = driver.find_elements_by_xpath()
    # print(majors)
    courses = parse_raw_courses(major_id)
    # print(courses)
    # course_id = "CS -570"
    # select1 = Select(driver.find_element_by_xpath('//select[option/@value="%s"]' % course_id))
    # select1.select_by_visible_text("%s" % courses[course_id])
    # driver.find_element_by_name("submitbutton").submit()
    # time.sleep(2)
    print(driver.page_source)


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
            # print(words[1], words[2][1:])
    return courses

do_things()

# Service selection
# Here I had to select my school among others


# select = Select(driver.find_element_by_name('user_idp'))
# select.select_by_visible_text('ENSICAEN')
# driver.find_element_by_id('IdPList').submit()

# Login page (https://cas.ensicaen.fr/cas/login?service=https%3A%2F%2Fshibboleth.ensicaen.fr%2Fidp%2FAuthn%2FRemoteUser)
# Fill the login form and submit it

# Now connected to the home page
# Click on 3 links in order to reach the page I want to scrape

# driver.find_element_by_id('formMenu:linknotes1').click()
# driver.find_element_by_id('_id137Pluto_108_u1240l1n228_50520_:tabledip:0:_id158Pluto_108_u1240l1n228_50520_').click()

# Select and print an interesting element by its ID
