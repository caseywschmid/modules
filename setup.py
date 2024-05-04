from setuptools import setup, find_packages

setup(
    name="modules",
    version="0.1",
    packages=find_packages(),
    author="Your Name",
    url="https://github.com/caseywschmid/modules.git",
    install_requires=[
        "beautifulsoup4==4.12.3",
        "requests==2.31.0",
        # add other dependencies as needed
    ],
    # Add other metadata as needed
)
