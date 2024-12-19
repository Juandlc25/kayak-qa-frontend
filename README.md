# Framework to Automate E2E Tests #
This project was developed using the next technologies:
* Python 3.8
* Selenium
* Behave
* PyHamcrest
* Testrail Api

## Installing `pip`:

* Download the script, from [get-pip](https://bootstrap.pypa.io/get-pip.py).
* Open a terminal/command prompt, cd to the folder containing the get-pip.py file and run:

| MacOS | Windows |
| ------ | ------ |
| `$ python get-pip.py` | `C:> py -m ensurepip --upgrade` |

>More details about this script can be found in [pypa/get-pip’s README](https://github.com/pypa/get-pip)

## Upgrading `pip`:

Upgrading your `pip` by running:

| MacOS | Windows |
| ------ | ------ |
| `$ python -m pip install --upgrade pip` | `C:> py -m pip install --upgrade pip` |

## Running the project:

To execute this project, you must first install the requirements file with the next command:

`python3 -m pip install requirements.txt`

Then of install all requirements you can execute the automated tests with the next command:

`behave --no-capture --format plain --tags={behave_tag} -Dcountry={coutry} -Dtestrail={testrail_report} -Ddriver={enviroment_to_run_tests}`
## Options

| Parameter               | Options                                                                                                            |
|-------------------------|--------------------------------------------------------------------------------------------------------------------|
| behave_tag              | here you can put the behave tag that you want run                                                                  |
| country                 | acronym of the country where you want the framework execution to be started, e.g co - br - pr                      |
| testrail_report         | true, false {if this parameter is true, will report the results in testrail}                                       |
| enviroment_to_run_tests | local, aws (use local if you want execute this project in your local machine)                                      |
