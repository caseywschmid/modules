from setuptools import setup, find_packages

setup(
    name="modules",
    version="0.1",
    packages=find_packages(),
    author="Casey Schmid",
    url="https://github.com/caseywschmid/modules.git",
    install_requires=[
        "beautifulsoup4==4.12.3",
        "requests==2.31.0",
        "selenium==4.20.0",
        "PyAutoGUI==0.9.54",
        "psutil==5.9.8",
        "openai==1.25.1",
        # add other dependencies as needed
    ],
    # Add other metadata as needed
)
