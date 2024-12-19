import datetime
import logging
import time
from datetime import datetime

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from lib.constants import Constants
from lib.helpers.generalhelpers import transformation_to_element_name

logger = logging.getLogger(__name__)


class GeneralComponents(object):
    def __init__(self, context):
        self.web_driver = context.web_driver

    def wait_until_element_is_present(self, web_element, timeout=Constants.MEDIUM_WAIT):
        error_message = f'The "{web_element}" element took more than {timeout} seconds longer than the configured time to be present in the DOM.'
        try:
            return WebDriverWait(self.web_driver, timeout).until(EC.presence_of_element_located(web_element),
                                                                 error_message)
        except TimeoutException as e:
            raise e

    def wait_until_element_is_clickable(self, web_element, timeout=Constants.MEDIUM_WAIT):
        error_message = f'The "{web_element}" element took more than {timeout} seconds longer than the configured time to be clickable in the DOM.'
        try:
            return WebDriverWait(self.web_driver, timeout).until(EC.element_to_be_clickable(web_element), error_message)
        except TimeoutException as e:
            raise e

    def wait_until_element_is_not_present(self, web_element, timeout=Constants.MEDIUM_WAIT):
        error_message = f'The "{web_element}" element took more than {timeout} seconds longer than the configured time not to be present in the DOM.'
        try:
            element_present = EC.invisibility_of_element(web_element)
            return WebDriverWait(self.web_driver, timeout).until(element_present, error_message)
        except TimeoutException as e:
            raise e

    def wait_until_title_is(self, title, timeout=Constants.MEDIUM_WAIT):
        error_message = f'The title page is not equal to the "{title}" Title after of {timeout} seconds'
        try:
            return WebDriverWait(self.web_driver, timeout).until(EC.title_is(title), error_message)
        except TimeoutException as e:
            raise e

    def wait_until_title_contain(self, title, timeout=Constants.MEDIUM_WAIT):
        error_message = f'The title page not contain the "{title}" title after of {timeout} seconds'
        try:
            return WebDriverWait(self.web_driver, timeout).until(EC.title_contains(title), error_message)
        except TimeoutException as e:
            raise e

    def wait_until_text_is_present_in_value(self, locator, text, timeout=Constants.MEDIUM_WAIT):
        error_message = f'Text in value is not present after of {timeout} seconds'
        try:
            return WebDriverWait(self.web_driver, timeout).until(EC.text_to_be_present_in_element_value(locator, text),
                                                                 error_message)
        except TimeoutException as e:
            raise e

    def wait_until_element_is_not_visible(self, web_element, timeout=Constants.MEDIUM_WAIT):
        error_message = f'The "{web_element}" element took more than {timeout} seconds longer than the configured time to not be visible in the DOM.'
        try:
            return WebDriverWait(self.web_driver, timeout, 1).until(EC.invisibility_of_element(web_element),
                                                                    error_message)
        except TimeoutException as e:
            raise e

    def wait_until_element_is_visible(self, web_element, timeout=Constants.MEDIUM_WAIT):
        error_message = f'The "{web_element}" element took more than {timeout} seconds longer than the configured time to not be visible in the DOM.'
        try:
            return WebDriverWait(self.web_driver, timeout, 1).until(EC.visibility_of(web_element), error_message)
        except TimeoutException as e:
            raise e

    def wait_until_two_elements_are_present(self, web_element_1, web_element_2, timeout=Constants.MEDIUM_WAIT):
        error_message = f'The elements took more than {timeout} seconds longer than the configured time to be present in the DOM.'
        try:
            return WebDriverWait(self.web_driver, timeout).until(
                EC.all_of(EC.presence_of_element_located(web_element_1),
                          EC.presence_of_element_located(web_element_2)),
                error_message)
        except TimeoutException as e:
            raise e

    def wait_until_two_elements_are_clickable(self, web_element_1, web_element_2, timeout=Constants.MEDIUM_WAIT):
        error_message = f'The elements took more than {timeout} seconds longer than the configured time to be clickable in the DOM.'
        try:
            return WebDriverWait(self.web_driver, timeout).until(
                EC.all_of(EC.element_to_be_clickable(web_element_1),
                          EC.visibility_of_element_located(web_element_2)), error_message)
        except TimeoutException as e:
            raise e

    def wait_until_url_is(self, url, timeout=Constants.MEDIUM_WAIT):
        error_message = f'The page not contain the {url} url after of {timeout} seconds'
        try:
            return WebDriverWait(self.web_driver, timeout).until(EC.url_to_be(url), error_message)
        except TimeoutException as e:
            raise e

    def wait_until_url_contains(self, contains, timeout=Constants.MEDIUM_WAIT):
        error_message = f'The url not contains {contains} after of {timeout} seconds'
        try:
            return WebDriverWait(self.web_driver, timeout).until(EC.url_contains(contains), error_message)
        except TimeoutException as e:
            raise e

    @staticmethod
    def find_into_element(web_element, selector) -> WebElement:
        try:
            return web_element.find_element(selector[0], selector[1])
        except NoSuchElementException as e:
            raise e

    @staticmethod
    def find_elements_into_element(web_element, selector):
        try:
            return web_element.find_elements(selector[0], selector[1])
        except NoSuchElementException as e:
            raise e

    @staticmethod
    def is_element_present_in_component(list_element, context, component_name):
        validation_list = []
        elements = transformation_to_element_name(list_element)
        for element in elements:
            component_elements = context.current_page.get_component_elements_per_name(component_name)
            web_element = context.browser.find_elements(component_elements.__dict__.get(element))
            validation_list.append(len(web_element) > 0)
        return validation_list

    @staticmethod
    def get_text_element_in_value_attribute(context, selector_name) -> str:
        element = context.current_page.webElements.__dict__.get(selector_name)
        return context.browser.find_element(element).get_attribute("value")

    @staticmethod
    def get_attribute_of_element(element, attribute):
        return element.get_attribute(attribute)

    @staticmethod
    def get_text_element(context, selector_name) -> str:
        element = context.current_page.webElements.__dict__.get(selector_name)
        return context.browser.find_element(element).text

    @staticmethod
    def get_text_web_element(web_element):
        return web_element.text

    @staticmethod
    def check_exist_element(context, selector_name):
        try:
            element = context.current_page.webElements.__dict__.get(selector_name)
            context.browser.find_element(element)
        except NoSuchElementException as e:
            logger.error(e)
            return False
        return True

    @staticmethod
    def check_unique_elements(element_list):
        return len(set(element_list)) == len(element_list)

    @staticmethod
    def check_search_elements(element_list, value):
        element_list = element_list[1:-1]
        return all(value in item for item in element_list)

    @staticmethod
    def click_multiple_items(element_list):
        clicked_items = []
        for elements in element_list:
            clicked_items.append(elements.click())
        return clicked_items

    @staticmethod
    def string_to_list(value, separator=str):
        return value.split(separator)

    @staticmethod
    def click_component_by_name(context, component_name, name_element):
        component_elements = context.current_page.get_component_elements_per_name(component_name)
        web_element = context.browser.find_element(component_elements.__dict__.get(name_element))
        return web_element.click()

    @staticmethod
    def list_to_string(value, separator=str):
        return separator.join(map(str, value))

    @staticmethod
    def current_date():
        today = datetime.today()
        return str(today).replace(":", "_").replace(".", "_").replace("-", "_")

    @staticmethod
    def is_enabled_in_component(context, component_name, element_name) -> bool:
        component_elements = context.current_page.get_component_elements_per_name(component_name)
        web_element = context.browser.find_element(component_elements.__dict__.get(element_name))
        return web_element.is_enabled()

    @staticmethod
    def clear_textbox(web_element):
        return web_element.clear()

    @staticmethod
    def type_in_textbox(txt, web_element):
        GeneralComponents.clear_textbox(web_element)
        return web_element.send_keys(txt)

    @staticmethod
    def get_text_element_from_component(context, component_name, element_name) -> str:
        component_elements = context.current_page.get_component_elements_per_name(component_name)
        web_element = context.browser.find_element(component_elements.__dict__.get(element_name))
        return web_element.text

    def wait_until_element_searched_is_present(self, web_element, expected_text, timeout=Constants.MEDIUM_WAIT):
        error_message = f'The element took more than {timeout} seconds longer than the configured time to be present in the DOM.'
        try:
            return WebDriverWait(self.web_driver, timeout).until(
                EC.text_to_be_present_in_element(web_element, expected_text), error_message)
        except TimeoutException as e:
            raise e

    @staticmethod
    def is_enabled_in_page(context, element_name) -> bool:
        web_element = context.current_page.webElements.__dict__.get(element_name)
        return context.browser.find_element(web_element).is_enabled()

    @staticmethod
    def get_element_list_from_component(context, component_name, element_name):
        enabled_elements = []
        component_elements = context.current_page.get_component_elements_per_name(component_name)
        element_list = context.browser.find_elements(component_elements.__dict__.get(element_name))
        for element in element_list:
            if GeneralComponents.is_enabled_in_component(context, component_name, element_name):
                enabled_elements.append(element)
        return enabled_elements

    @staticmethod
    def type_in_textarea(context, component_name, element_name, text):
        component_elements = context.current_page.get_component_elements_per_name(component_name)
        web_element = context.browser.find_element(component_elements.__dict__.get(element_name))
        web_element.clear()
        return web_element.send_keys(text)

    @staticmethod
    def check_format_matches(test_format, expected_format):
        try:
            test_format = datetime.strptime(test_format, expected_format)
            return bool(datetime.strftime(test_format, expected_format))
        except ValueError:
            return False

    @staticmethod
    def is_clickable(context, component_name, element_name) -> bool:
        component_elements = context.current_page.get_component_elements_per_name(component_name)
        web_element = context.browser.find_element(component_elements.__dict__.get(element_name))
        return web_element.isClickable()

    @staticmethod
    def is_displayed(context, component_name, element_name):
        component_elements = context.current_page.get_component_elements_per_name(component_name)
        web_element = context.browser.find_element(component_elements.__dict__.get(element_name))
        return web_element.is_displayed()
