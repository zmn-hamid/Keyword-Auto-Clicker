import time
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import DOMAINS_PATH, KEYWORDS_PATH, REMOVE_SEARCHES


class AutoClicker:
    def __init__(self) -> None:
        self.keywords = []
        self.domains = []

    def fetch_keywords(self, keywords_path: str):
        self.keywords = list(
            map(lambda item: item.strip(), open(keywords_path).readlines())
        )

    def fetch_websites(self, domains_path: str):
        self.domains = list(
            map(lambda item: item.strip(), open(domains_path).readlines())
        )

    def init_driver(self):
        self.driver = webdriver.Chrome(
            service=Service(), options=webdriver.ChromeOptions()
        )

    def close_driver(self):
        self.driver.close()

    @staticmethod
    def find_first_url_in_text(text: str):
        for item in text.split():
            if item.startswith("https://"):
                return item

    @staticmethod
    def get_domain_from_url(url: str):
        return ".".join(urlparse(url).netloc.split(".")[-2:])

    @staticmethod
    def omit_search(search_text: str):
        """tells whether should omit this search or not"""
        for item in REMOVE_SEARCHES:
            if item in search_text:
                return True
        return False

    def main(self):
        for keyword in self.keywords:

            # get google.com
            self.driver.get("https://www.google.com/")

            # search the keyword
            search_bar = self.driver.find_element(By.NAME, "q")
            search_bar.send_keys(keyword)
            search_bar.send_keys(Keys.RETURN)

            # fetch the websites
            search_results = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_all_elements_located(
                    (By.XPATH, '//*[@id="search"]/div/div/div')
                )
            )

            # one by one:
            for search_result in search_results:
                # get text from element
                text = search_result.text

                # omit the search if it's not relevant
                # by default, the google suggestions are added
                if AutoClicker.omit_search(text):
                    continue

                # if is in the websites list
                url = AutoClicker.find_first_url_in_text(text)
                if (
                    url
                    and (domain := AutoClicker.get_domain_from_url(url)) in self.domains
                ):
                    # click on it
                    self.driver.find_element(By.PARTIAL_LINK_TEXT, domain).click()
                    time.sleep(1)

                    # go back
                    self.driver.back()


if __name__ == "__main__":
    clicker = AutoClicker()
    clicker.fetch_keywords(KEYWORDS_PATH)
    clicker.fetch_websites(DOMAINS_PATH)
    clicker.init_driver()
    clicker.main()
    if input("close [y/n]: ").lower() == "y":
        clicker.close_driver()
