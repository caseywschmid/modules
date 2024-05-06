from setuptools import setup, find_packages

setup(
    name="Beautiful Soup Helper",
    version="0.0.1",
    packages=find_packages(),
    author="Casey Schmid",
    url="https://github.com/caseywschmid/modules.git#subdirectory=modules/helpers/bs4_helper",
    install_requires=[
        "beautifulsoup4",
        "requests",
        # add other dependencies as needed
    ],
    # Add other metadata as needed
)