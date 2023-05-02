import logging
import re
import time
import unittest

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s "%(message)s"',
)

LOGGER = logging.getLogger(__name__)


class TestWuzzufLinksShowingUpandBiggerThanZero(unittest.TestCase):
    browser = None
    page_count = 5
    wuzzuf_link_pattern = (
        r'(https?:\/\/wuzzuf\.net\/[\w\-\._~:\/\?#\[\]@!\$&\'\(\)\*+,;\=]*)'
    )

    def setUp(self):
        LOGGER.info('Setting up selenium')
        options = uc.ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.browser = uc.Chrome(options=options)

    def tearDown(self):
        self.browser.quit()

    def test_wuzzuf_google_first_5_pages_links_have_results_greater_than_zero(
        self,
    ):
        wuzzuf_links = []
        self.browser.get('http://www.google.com')
        search = self.browser.find_element(By.NAME, 'q')
        search.send_keys('python jobs in egypt')
        search.send_keys(Keys.RETURN)
        time.sleep(5)

        for i in range(self.page_count):
            LOGGER.info(f'Scrapping page: {i}')
            links = self.browser.find_elements(By.CSS_SELECTOR, 'div.g a')
            wuzzuf_links.extend(
                [
                    link.get_attribute('href')
                    for link in links
                    if re.match(
                        self.wuzzuf_link_pattern, link.get_attribute('href')
                    )
                ]
            )
            next_button = self.browser.find_element(
                By.CSS_SELECTOR, '#pnnext > span:nth-child(2)'
            )
            next_button.click()
            if i != self.page_count:
                time.sleep(5)

        self.assertTrue(wuzzuf_links)
        LOGGER.info(f'Found {len(wuzzuf_links)} links: {wuzzuf_links}')

        for link in wuzzuf_links:
            LOGGER.info(f'Scrapping link: {link}')
            self.browser.get(link)
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.css-uzlk74')
                )
            )
            result = int(
                self.browser.find_element(
                    By.CSS_SELECTOR, '.css-uzlk74'
                ).text.split()[0]
            )
            self.assertGreater(result, 0)


if __name__ == '__main__':
    unittest.main()
