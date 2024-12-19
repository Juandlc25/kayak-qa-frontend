import logging
from datetime import date

from lib.constants import Constants
from lib.helpers.testrail.testrailhelpers import TestrailHelper
from lib.integrations.testrail import APIClient

logger = logging.getLogger(__name__)


def get_fe_test_cases(project_id, acceptance_test, stability_test):
    logger.info("Getting automated test cases.")
    return get_all_test_cases('&filter=FE -', project_id, acceptance_test, stability_test)


def get_be_test_cases(project_id, acceptance_test, stability_test) -> object:
    logger.info("Getting automated test cases.")
    return get_all_test_cases('&filter=BE -', project_id, acceptance_test, stability_test)


def get_all_test_cases(url_filter, project_id, acceptance_test, stability_test) -> object:
    all_regression_tests = []
    all_acceptance_tests = []
    all_stability_tests = []
    test_rail_api = APIClient(Constants.TESTRAIL_URL_BASE)
    url = '{}{}{}'.format("get_cases/", project_id, url_filter)
    test_cases = test_rail_api.send_get(url)
    all_regression_tests.extend(get_automated_tc(test_cases['cases'], acceptance_test,
                                                 stability_test)['regression_tests'])
    if acceptance_test:
        all_acceptance_tests.extend(get_automated_tc(test_cases['cases'], acceptance_test,
                                                     stability_test)['acceptance_test'])
    if stability_test:
        all_stability_tests.extend(get_automated_tc(test_cases['cases'], acceptance_test,
                                                    stability_test)['stability_test'])
    while test_cases['_links'].__getitem__('next'):
        url = test_cases['_links'].__getitem__('next')[8:]
        test_cases = test_rail_api.send_get(url)
        all_regression_tests.extend(get_automated_tc(test_cases['cases'], acceptance_test,
                                                     stability_test)['regression_tests'])
        if acceptance_test:
            all_acceptance_tests.extend(get_automated_tc(test_cases['cases'], acceptance_test,
                                                         stability_test)['acceptance_test'])
        if stability_test:
            all_stability_tests.extend(get_automated_tc(test_cases['cases'], acceptance_test,
                                                        stability_test)['stability_test'])
    return {
        'regression_tests': all_regression_tests,
        'acceptance_test': all_acceptance_tests,
        'stability_test': all_stability_tests
    }


def get_automated_tc(tc_list, acceptance_test, stability_test) -> object:
    test_cases_automated = []
    acceptance_test_cases = []
    stability_test_cases = []
    for test_case in tc_list:
        if test_case.__getitem__('custom_automated') and test_case.__getitem__('type_id') == 9:
            test_cases_automated.append(test_case.__getitem__('id'))
        if acceptance_test:
            if test_case.__getitem__('custom_acceptance_test') and test_case.__getitem__('custom_automated') and \
                    test_case.__getitem__('type_id') == 9:
                acceptance_test_cases.append(test_case.__getitem__('id'))
        if stability_test:
            if test_case.__getitem__('custom_stability_test') and test_case.__getitem__('type_id') == 13:
                stability_test_cases.append(test_case.__getitem__('id'))
    return {
        'regression_tests': test_cases_automated,
        'acceptance_test': acceptance_test_cases,
        'stability_test': stability_test_cases
    }


def create_test_run(test_run_type, project_id, acceptance_test=False, stability_test=False):
    request_results = []
    regression_test_cases = None
    acceptance_test_cases = None
    stability_test_cases = None
    if test_run_type == 'FE':
        regression_test_cases = get_fe_test_cases(project_id, acceptance_test, stability_test)['regression_tests']
        acceptance_test_cases = get_fe_test_cases(project_id, acceptance_test, stability_test)['acceptance_test']
        stability_test_cases = get_fe_test_cases(project_id, acceptance_test, stability_test)['stability_test']
    if test_run_type == 'BE':
        regression_test_cases = get_be_test_cases(project_id, acceptance_test, stability_test)['regression_tests']
        acceptance_test_cases = get_be_test_cases(project_id, acceptance_test, stability_test)['acceptance_test']
        stability_test_cases = get_be_test_cases(project_id, acceptance_test, stability_test)['stability_test']
    request_results.append(create_test_run_request(regression_test_cases, test_run_type, project_id, acceptance_test=False, stability_test=False))
    if acceptance_test:
        request_results.append(
            create_test_run_request(acceptance_test_cases, test_run_type, project_id, acceptance_test=acceptance_test, stability_test=False))
    if stability_test:
        request_results.append(
            create_test_run_request(stability_test_cases, test_run_type, project_id, acceptance_test=False, stability_test=stability_test))
    return request_results


def create_test_run_request(automated_test_cases, test_run_type, project_id, acceptance_test, stability_test):
    test_rail_api = APIClient(Constants.TESTRAIL_URL_BASE)
    url = '{}{}'.format("add_run/", project_id)
    test_run_name = create_test_run_name(test_run_type, acceptance_test, stability_test)
    print(f'Creating the {test_run_name} test run')
    test_run_body = {
        "name": test_run_name,
        "description": 'Test Run created automatically',
        'assignedto_id': 7,
        "include_all": False,
        "case_ids": automated_test_cases
    }
    return test_rail_api.send_post(url, test_run_body)


def create_test_run_name(test_run_type, acceptance_test, stability_test):
    today = date.today()
    format_date = today.strftime("%m/%d/%Y")
    if acceptance_test:
        return '{}{}{}{}{}'.format('Test Run ', format_date, ' - ', test_run_type, ' Automated Acceptance Tests')
    elif stability_test:
        return '{}{}{}{}{}'.format('Test Run ', format_date, ' - ', test_run_type, ' Automated Stability Tests')
    else:
        return '{}{}{}{}{}'.format('Test Run ', format_date, ' - ', test_run_type, ' Automated Regression Tests')


def close_test_run(test_run_type, project_id, acceptance_tests=False, stability_test=False):
    test_runs = []
    test_rail_api = APIClient(Constants.TESTRAIL_URL_BASE)
    testrail_helper = TestrailHelper(Constants.TESTRAIL_URL_BASE, project_id=project_id)
    test_runs.append(testrail_helper.get_test_run_id(test_run_type, acceptance_test=False, stability_test=False))
    if acceptance_tests:
        test_runs.append(testrail_helper.get_test_run_id(test_run_type, acceptance_test=acceptance_tests,
                                                         stability_test=False))
    if stability_test:
        test_runs.append(testrail_helper.get_test_run_id(test_run_type, acceptance_test=False,
                                                         stability_test=stability_test))
    return close_test_run_request(test_rail_api, test_runs)


def close_test_run_request(test_rail_api, test_runs):
    request_results = []
    for test_run_id in test_runs:
        print(f'Closing the test run with the id: {test_run_id}')
        url = '{}{}'.format("close_run/", test_run_id)
        request_results.append(test_rail_api.send_post(url, ''))
    return request_results


def test_run_process(project_id) -> str:
    close_test_run('FE', project_id, acceptance_tests=False, stability_test=False)
    close_test_run('BE', project_id, acceptance_tests=False, stability_test=False)
    create_test_run('FE', project_id, acceptance_test=False, stability_test=False)
    create_test_run('BE', project_id, acceptance_test=False, stability_test=False)
    return 'Operation finalized'
