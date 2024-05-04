from setuptools import setup, find_packages

setup(
    name="modules",
    version="0.1",
    packages=["helpers"],
    author="Casey Schmid",
    url="https://github.com/caseywschmid/modules.git",
    install_requires=[
        "beautifulsoup4==4.12.3",
        "requests==2.31.0",
        # add other dependencies as needed
    ],
    # Add other metadata as needed
)
