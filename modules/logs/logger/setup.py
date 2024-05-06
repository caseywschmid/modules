from setuptools import setup, find_packages

setup(
    name="CWS_Logger",
    version="0.0.2",
    packages=find_packages(),
    author="Casey Schmid",
    author_email="caseywschmid@gmail.com",
    url="https://github.com/caseywschmid/modules.git#subdirectory=modules/logs/logger",
    install_requires=[
        "python-dotenv",
    ],
    # Add other metadata as needed
)
