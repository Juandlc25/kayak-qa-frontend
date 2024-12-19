import re
import logging

from lib.constants import Constants
from lib.integrations.slack import send_not_created_tc
from lib.integrations.testrail import APIClient, APIError

logger = logging.getLogger()


class TestrailHelper:
    def __init__(self, url_base, project_id=Constants.PROJECT_ID_NC_LC):
        self.url_base = url_base
        self.project_id = project_id

    @staticmethod
    def get_test_case_id(test_case_name):
        patron = 'C([0-9]+)'
        result = re.findall(patron, test_case_name)
        return result[0]

    def set_test_case_result(self, test_run_id, tc_id, test_case_status, duration, comment, app_version):
        comment = '{}{}{}'.format(comment, '\n', self.transform_time(duration))

        if duration <= 1:
            elapsed = '%s seconds' % int(1)
        else:
            elapsed = '%s seconds' % int(duration)

        body = {
            "status_id": test_case_status,
            "comment": comment,
            "elapsed": elapsed,
            "version": app_version,
        }
        url = '{}{}{}{}'.format("add_result_for_case/", test_run_id, "/", tc_id)
        test_rail_api = APIClient(self.url_base)
        try:
            return test_rail_api.send_post(url, body)
        except APIError as e:
            logger.error(e)
            if str(e).__contains__('No (active) test found for the run/case combination.'):
                return send_not_created_tc(tc_id)

    def add_attachment_to_result(self, result_response, screenshot_name):
        url = '{}{}'.format("add_attachment_to_result/", result_response['id'])
        test_rail_api = APIClient(self.url_base)
        return test_rail_api.send_post(url, screenshot_name)

    @staticmethod
    def get_tc_status_code(status_name):
        return Constants.TC_STATUS_CODE[status_name]

    def update_test_case(self, tc_id, steps):
        test_rail_api = APIClient(self.url_base)
        url = '{}{}'.format("update_case/", tc_id)
        body = {
            "custom_automation_steps": steps
        }
        return test_rail_api.send_post(url, body)

    @staticmethod
    def transform_time(duration):
        timings = (int(duration / 60.0), duration % 60)
        return 'Took %dm%02.3fs' % timings

    def get_test_run_id(self, test_run_type, all_data=False, acceptance_test=False, stability_test=False):
        test_rail_api = APIClient(self.url_base)
        url = '{}{}{}'.format("get_runs/", self.project_id, '&is_completed=0')
        test_runs = test_rail_api.send_get(url)
        return self.get_test_run_by_name(test_runs, test_run_type, all_data=all_data, acceptance_tests=acceptance_test, stability_test=stability_test)

    def calculate_percentage_of_test_run(self) -> object:
        test_run_data = self.get_test_run_id(test_run_type='FE', all_data=True)
        passed_count = test_run_data["passed_count"]
        blocked_count = test_run_data['blocked_count']
        untested_count = test_run_data['untested_count']
        retest_count = test_run_data['retest_count']
        failed_count = test_run_data['failed_count']
        total_test_cases = int(passed_count) + int(blocked_count) + int(untested_count) + int(retest_count) + int(
            failed_count)
        percentage_passed = int(passed_count) / total_test_cases * 100
        details = {
            'percentage': round(percentage_passed),
            'url': test_run_data['url']
        }
        return details

    @staticmethod
    def get_test_run_by_name(test_runs, test_run_type, all_data=False, acceptance_tests=False, stability_test=False):
        test_run_data = ""
        if acceptance_tests:
            test_run_title = '{}{}{}'.format(' ', test_run_type, ' Automated Acceptance Tests')
        elif stability_test:
            test_run_title = '{}{}{}'.format(' ', test_run_type, ' Automated Stability Tests')
        else:
            test_run_title = '{}{}{}'.format(' ', test_run_type, ' Automated Regression Tests')
        for test_run in test_runs['runs']:
            if test_run_title in test_run['name']:
                if all_data:
                    test_run_data = test_run
                else:
                    test_run_data = test_run['id']
        return test_run_data
