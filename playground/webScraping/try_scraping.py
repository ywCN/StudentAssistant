import requests
import sys
# https://mystevens.stevens.edu/sso/webselfservices.php
# https://mystevens.stevens.edu/sso/web4student.php

from selenium import webdriver
from selenium.webdriver.support.ui import Select # for <SELECT> HTML form
import time
driver = webdriver.PhantomJS("C:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")

# Service selection
# Here I had to select my school among others
driver.get("https://mystevens.stevens.edu/sso/web4student.php")
time.sleep(5)
# select = Select(driver.find_element_by_name('user_idp'))
# select.select_by_visible_text('ENSICAEN')
# driver.find_element_by_id('IdPList').submit()

# Login page (https://cas.ensicaen.fr/cas/login?service=https%3A%2F%2Fshibboleth.ensicaen.fr%2Fidp%2FAuthn%2FRemoteUser)
# Fill the login form and submit it
driver.find_element_by_id("user").send_keys("")
driver.find_element_by_id("password").send_keys("")
driver.find_element_by_id('submit').submit()
time.sleep(5)
# Now connected to the home page
# Click on 3 links in order to reach the page I want to scrape
driver.find_element_by_id('Course Sections').click()
# driver.find_element_by_id('formMenu:linknotes1').click()
# driver.find_element_by_id('_id137Pluto_108_u1240l1n228_50520_:tabledip:0:_id158Pluto_108_u1240l1n228_50520_').click()
select = Select(driver.find_element_by_name('Subject'))
select.select_by_visible_text('Biomedical Engineering')
driver.find_element_by_id('submitbutton').submit()
# Select and print an interesting element by its ID
page = driver.find_element_by_id('option value')
print(page.text)