import pickle
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TryScraping:
    def setup(self):
        browser = webdriver.Firefox()
        return browser

    def login(self, username, password, browser=None):
        browser.get("https://login.example.com/")

        pwd_btn = browser.find_element_by_name("password")
        act_btn = browser.find_element_by_name("loginId")
        submit_btn = browser.find_element_by_name("submit-btn")

        act_btn.send_keys(username)
        pwd_btn.send_keys(password)
        submit_btn.send_keys(Keys.ENTER)

        return browser

    def set_sessions(self, browser):
        request = requests.Session()
        headers = {
            "User-Agent":
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        }
        request.headers.update(headers)
        cookies = browser.get_cookies()
        for cookie in cookies:
            request.cookies.set(cookie['name'], cookie['value'])

        return request


if __name__ == "__main__":
    test = TryScraping()
    browser = test.login("textusername", "tespassword", test.setup())
    rq = test.set_sessions(browser)
    test.re.get("http://www.example.com")
