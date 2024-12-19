from typing import List
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from lib.helpers.generalhelpers import transformation_to_element_name


class BasePage(object):
    def __init__(self, context):
        self.web_driver = context.web_driver
        self.context = context
        self.base_url = self.get_url_per_environment(context)

    def delete_all_cookies(self):
        """
        delete all saved cookies in the driver
        """
        self.web_driver.delete_all_cookies()

    def reload_page(self):
        """
        reload the paged opened in the driver
        """
        self.web_driver.refresh()

    def visit_page(self, url):
        self.web_driver.get(url)

    def close(self):
        """
        close the current driver session
        """
        self.web_driver.close()

    def quit(self):
        """
        close the webdriver instance
        """
        self.web_driver.quit()

    def get_current_url(self):
        return self.web_driver.current_url
    
    def find_element(self, selector) -> WebElement:
        """
        find a page element in the DOM
        """
        try:
            return self.web_driver.find_element(selector[0], selector[1])
        except NoSuchElementException as e:
            raise e

    def find_elements(self, selector) -> List[WebElement]:
        """
        find int the page one list of elements rendered in the DOM
        """
        try:
            return self.web_driver.find_elements(selector[0], selector[1])
        except NoSuchElementException as e:
            raise e

    def switch_to(self, window_name):
        """
        Switch to tabs or iframes
        :return: new web context
        """
        return self.web_driver.switch_to.window(window_name)

    def current_window_handle(self):
        """
        Get current window handler
        :return: Current window handler
        """
        return self.web_driver.current_window_handle

    def visit(self, url):
        """
        navigate webdriver to different pages
        """
        if url == "":
            return self.web_driver.get(self.base_url)
        else:
            return self.web_driver.get(url)

    def get_window_handles_per_position(self, position):
        return self.web_driver.window_handles[position]

    @staticmethod
    def get_url_per_environment(context):
        country = context.config.userdata["country"]
        return '{}{}'.format("https://www.kayak.com.", country)

    def get_title_page(self) -> str:
        return self.web_driver.title

    def are_element_presents(self, list_element, context):
        validation_list = []
        elements = transformation_to_element_name(list_element)
        print("*" *10)
        print(list_element)
        print(elements)
        print("*" *10)
        for element in elements:
            selector = self.context.current_page.webElements.__dict__.get(element)
            if selector is None:
                raise TypeError(f' The {element} selector name is not created')
            web_element = context.browser.find_elements(selector)
            validation_list.append(len(web_element) > 0)
        return validation_list
