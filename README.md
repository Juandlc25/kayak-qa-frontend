# Kayak qa frontend

This project was developed using the next technologies:

- Python 3.8
- Selenium
- Behave
- PyHamcrest
- Testrail Api

## Running the project:

To execute this project, you must first install the requirements file with the next command:

`python3 -m pip install requirements.txt`

Then of install all requirements you can execute the automated tests with the next command:

`behave --no-capture --format plain --tags={behave_tag} -Dcountry={coutry} -Dtestrail={testrail_report} -Ddriver={enviroment_to_run_tests}`
|

