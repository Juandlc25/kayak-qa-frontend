import logging

from lib.components.generalcomponents import GeneralComponents
from lib.helpers.generalhelpers import validate_wait_results
from lib.pages.basepage import BasePage
from lib.pages.webelements.homewebelements import HomeWebElements

logger = logging.getLogger(__name__)


class HomePage(BasePage):

    def __init__(self, context):
        BasePage.__init__(self, context)
        self.context = context
        self.web_driver = context.browser
        self.webElements = HomeWebElements

    def get_title_page(self):
        return self.web_driver.get_title_page()

    def get_current_url(self):
        return self.web_driver.get_current_url()

    def is_open(self):
        return validate_wait_results(
            GeneralComponents.wait_until_element_is_present(self.context, HomeWebElements.where_label),
            GeneralComponents.wait_until_element_is_present(self.context, HomeWebElements.signin_button))

    def reload_page(self):
        return self.reload_page()
