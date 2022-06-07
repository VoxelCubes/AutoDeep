import random
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys



class SeleniumDefault:
    """
    Skeleton for apps using Selenium. Frequently needed shortcuts are available in here.
    """


    def __init__(self, driver_path='chromedriver'):
        """
        Instantiate the class needs to feed a selenium driver.
        @param driver_path : str - path to the selenium driver (mandatory)
        """

        self.url = None
        self.original_window = None
        self.driver = None

        self.driver_path = driver_path
        self.driver = webdriver.Chrome(self.driver_path)


    def connect_to_url(self, url):
        """
        Redirect the webpage to a new url.
        @param url : str - webpage to visit with webdriver.
        """
        self.url = url
        self.load_url()


    def load_url(self):
        """
        Instantiate a new driver instance.
        """
        self.driver.get(self.url)
        self.original_window = self.driver.window_handles[0]
        self.sleep(3)


    @staticmethod
    def paste_clipboard(element):
        """
        Copy clipboard content into the selected element
        @param element : selenium element
        """
        element.send_keys(Keys.SHIFT, Keys.INSERT)


    def scroll_to_element(self, element, sleep=1):
        """
        Scroll to any defined element on the webpage (essentially to make it clickable).
        @param element: selenium element - element to scroll to
        @param sleep: int - number of waiting seconds after scrolling. Default is 1.
        """
        y = element.location['y']
        y = y - 600
        self.driver.execute_script(f"window.scrollTo(0, {y})")
        self.sleep(sleep)


    @staticmethod
    def sleep(sleep=1):
        """
        Sleeping function : as web pages might take time to react, it is interesting to wait for their responses.
        To introduce noise the time value is slightly modified around the desired value.
        @param sleep: seconds to wait. Default is 1.
        """
        noise = random.random() - 0.5
        sleep = max(sleep + noise, 1)
        time.sleep(sleep)


    def close_driver(self):
        """
        Close the driver instance and the window associated.
        """
        self.driver.quit()
