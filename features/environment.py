from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from lib.pages.basepage import BasePage
from lib.pages.homepage import HomePage


def before_all(context):
    driver = set_selenium_driver(context)
    driver.set_page_load_timeout(5)
    driver.maximize_window()

    context.web_driver = driver
    context.browser = BasePage(context)
    context.home = HomePage(context)

    contexts = {
        'home': context.home,
    }

    context.all_contexts = contexts


def after_scenario(context, scenario):
    sep = '\n'
    steps = []
    for step in scenario.steps:
        steps.append(str(step).replace('<', '').replace('>', '').capitalize())
    if test_rail_report(context) == 'True':
        validate_scenario(scenario, context, sep.join(steps))
    pass


def after_all(context):
    context.browser.quit()
    return print("===== That's all folks =====")


def after_step(context, step):
    if step.exception is not None:
        context.step_error = step.exception
        context.failed_step = step.name
    if step.status == 'failed':
        context.failed_step = step.name


def validate_scenario(scenario, context, steps):
    if scenario.status.name == 'failed':
        return print('Failed Step: ' + context.failed_step + '\n' + str(context.step_error))


def set_selenium_driver(context):
    env = context.config.userdata["driver"]
    if env == 'aws':
        driver = set_docker_driver()
    else:
        driver = set_local_driver()
    return driver


def set_local_driver() -> webdriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    return webdriver.Chrome(options=chrome_options)


def set_docker_driver() -> webdriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.set_capability('--lang', 'en-GB')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option('useAutomationExtension', False)

    return webdriver.Remote(
        command_executor='http://0.0.0.0:4444/wd/hub',
        desired_capabilities=chrome_options.to_capabilities()
    )

def test_rail_report(context):
    return context.config.userdata["testrail"]
