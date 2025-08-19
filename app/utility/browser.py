import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


class SelectorMixin:

    def get_id(self, id):
        return Element(self._find_element(By.ID, id))

    def get_ids(self, id):
        return [Element(element) for element in self._find_elements(By.ID, id)]

    def get_class(self, class_name):
        return Element(self._find_element(By.CLASS_NAME, class_name))

    def get_classes(self, class_name):
        return [Element(element) for element in self._find_elements(By.CLASS_NAME, class_name)]

    def get_name(self, name):
        return Element(self._find_element(By.NAME, name))

    def get_names(self, name):
        return [Element(element) for element in self._find_elements(By.NAME, name)]

    def get_tag(self, tag_name):
        return Element(self._find_element(By.TAG_NAME, tag_name))

    def get_tags(self, tag_name):
        return [Element(element) for element in self._find_elements(By.TAG_NAME, tag_name)]

    def get_link_text(self, link_text):
        return Element(self._find_element(By.LINK_TEXT, link_text))

    def get_link_texts(self, link_text):
        return [Element(element) for element in self._find_elements(By.LINK_TEXT, link_text)]

    def get_partial_link_text(self, partial_link_text):
        return Element(self._find_element(By.PARTIAL_LINK_TEXT, partial_link_text))

    def get_partial_link_texts(self, partial_link_text):
        return [Element(element) for element in self._find_elements(By.PARTIAL_LINK_TEXT, partial_link_text)]

    def get_xpath(self, xpath):
        return Element(self._find_element(By.XPATH, xpath))

    def get_xpath_list(self, xpath):
        return [Element(element) for element in self._find_elements(By.XPATH, xpath)]

    def get_css(self, css):
        return Element(self._find_element(By.CSS_SELECTOR, css))

    def get_css_list(self, css):
        return [Element(element) for element in self._find_elements(By.CSS_SELECTOR, css)]

    def _find_element(self, selector, match):
        try:
            return self.driver.find_element(selector, match)
        except NoSuchElementException:
            return None

    def _find_elements(self, selector, match):
        try:
            return self.driver.find_elements(selector, match)
        except NoSuchElementException:
            return None


class Element(SelectorMixin):

    def __init__(self, element):
        self.driver = element

    @property
    def text(self):
        if not self.driver:
            return ""
        return self.driver.text

    def attr(self, name):
        if not self.driver:
            return ""
        return self.driver.get_attribute(name)


class Browser(SelectorMixin):

    def __init__(self, url=None):
        options = Options()

        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--window-size=1920,1200")
        options.add_argument(
            "--user-agent='Mozilla/5.0 (X11; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0'"  # noqa: E501
        )

        self.driver = Firefox(options=options)
        if url:
            self.request(url)

    def __del__(self):
        self.close()

    @property
    def title(self):
        return self.driver.title if self.driver else ""

    @property
    def source(self):
        return self.driver.page_source if self.driver else ""

    @property
    def final_url(self):
        return self.driver.current_url if self.driver else None

    def request(self, url):
        if self.driver:
            try:
                self.driver.get(url)
                time.sleep(2)
            except Exception:
                pass

    def close(self):
        if self.driver:
            self.driver.close()
