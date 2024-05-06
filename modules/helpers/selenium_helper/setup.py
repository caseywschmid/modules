from setuptools import setup, find_packages

setup(
    name="CWS_Selenium_Helper",
    version="0.0.1",
    packages=find_packages(),
    author="Casey Schmid",
    author_email="caseywschmid@gmail.com",
    url="https://github.com/caseywschmid/modules.git#subdirectory=modules/helpers/selenium_helper",
    install_requires=[
        "selenium==4.20.0",
        "PyAutoGUI==0.9.54",
        "psutil==5.9.8",
        # add other dependencies as needed
    ],
    # Add other metadata as needed
)
