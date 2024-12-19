from behave import then, use_step_matcher
from hamcrest import equal_to, assert_that, only_contains
import re

from lib.components.generalcomponents import GeneralComponents
from lib.helpers.generalhelpers import validate_text, transform_validation, transformation_helper, join_words, \
    split_and_replace_string, transformation_to_element_name

use_step_matcher("re")


@then(u'The page title should "(?P<assertion>contain|equal)" the "(?P<page_name>.*)" text')
def step_impl(context, assertion, page_name):
    validation_result = validate_text(assertion, page_name, context.current_page.get_title_page())
    return assert_that(validation_result, equal_to(True),
                       f'The expected title is "{page_name}", but was "{context.current_page.get_title_page()}"')


@then(u'I should be in the "(?P<page>.*)" page')
def step_impl(context, page):
    context.current_page = context.all_contexts[page]
    return assert_that(context.current_page.is_open(), only_contains(True),
                       'Some element is not present in the opened page')


@then(u'The page "(?P<expression>should|should not)" contain the next elements')
def step_impl(context, expression):
    list_validation = context.browser.are_element_presents(context.table, context)
    assertion = transform_validation(expression)
    return assert_that(list_validation, only_contains(assertion))


@then(u'The "(?P<element_name>.*)" "(?P<element_type>label|button|container)" should contain the "('
      u'?P<text_to_validate>.*)" text')
def step_impl(context, element_name, element_type, text_to_validate):
    element = transformation_helper(element_name, element_type)
    text_element = GeneralComponents.get_text_element(context, element).rstrip()
    new_text_to_validate = join_words(split_and_replace_string(text_to_validate))
    new_text_element = join_words(split_and_replace_string(text_element))
    return assert_that(new_text_to_validate, equal_to(new_text_element))


@then(u'The "(?P<element_name>.*)" "(?P<element_type>label|button|container)" "(?P<expression>should|should not)" be '
      u'present')
def step_impl(context, element_name, element_type, expression):
    element = transformation_helper(element_name, element_type)
    element_validation = GeneralComponents.check_exist_element(context, element)
    assertion = transform_validation(expression)
    return assert_that(element_validation, equal_to(assertion))


@then(u'The url page should be equal to the next "(?P<url>.*)" url')
def step_impl(context, url):
    country = context.config.userdata["country"]
    pattern = r"\.([a-z]{2,3})(?:/|$)"
    if re.search(pattern, url) and not url.endswith(".com"):
        country_url = url
    else:
        country_url = '{}.{}/'.format(url, country)
    GeneralComponents.wait_until_url_is(context.browser, country_url)

    return assert_that(context.web_driver.current_url, equal_to(country_url))


@then(u'The "(?P<element_name>.*)" "(?P<element_type>button)" "('u'?P<expression>should|should 'u'not)" be enabled')
def step_impl(context, element_name, element_type, expression):
    element_name = transformation_helper(element_name, element_type)
    assertion = transform_validation(expression)
    button_enabled = GeneralComponents.is_enabled_in_page(context, element_name)
    return assert_that(button_enabled, equal_to(assertion))
