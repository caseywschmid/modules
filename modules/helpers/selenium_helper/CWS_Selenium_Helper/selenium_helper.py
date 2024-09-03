import os
import signal
import time
from importlib.metadata import version
from typing import Annotated, NoReturn

import psutil
import pyautogui
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


# ------ CONFIGURE LOGGING ------
import logging

try:
    # if running the code from the package itself
    if os.getenv("SELENIUM_HELPER_PACKAGE_TEST", "False").lower() in ("true", "1", "t"):
        from modules.logs.logger.CWS_Logger import logger
    else:
        # if running the code as an imported package in another project
        from CWS_Logger import logger  # type: ignore
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "The necessary 'Logger' module is not installed. Please install it by running \n'pip install git+https://github.com/caseywschmid/modules.git#subdirectory=modules/logs/logger'"
    )

logger.configure_logging(__name__)
log = logging.getLogger(__name__)


SELENIUM_VERSION = "4.20.0"
PYAUTOGUI_VERSION = "0.9.54"
PSUTIL_VERSION = "5.9.8"


class SeleniumHelper:
    def __init__(self, use_remote=False):
        self.driver = None
        self.wait = None
        # Global flag to control the logging loop
        self.is_logging_active = False
        self.use_remote = use_remote

        if self.use_remote:
            self.setup_remote_selenium()
        else:
            self.setup_local_selenium()

    def check_dependency_versions(self) -> NoReturn:
        current_selenium_version = version("selenium")
        current_pyautogui_version = version("PyAutoGUI")
        if not current_pyautogui_version:
            log.warning(
                "PyAutoGUI is not installed. SeleniumHelper.start_coordinate_logging() will not work."
            )
        current_psutil_version = version("psutil")
        if not current_psutil_version:
            log.warning(
                "psutil is not installed. SeleniumHelper.close_chrome() will not work."
            )
        # Check if the warning should be muted
        mute_warning = os.getenv("MUTE_SELENIUM_HELPER_WARNING", "False").lower() in (
            "true",
            "1",
            "t",
        )

        if not mute_warning:
            if current_selenium_version != SELENIUM_VERSION:
                log.warning(
                    f"The 'SeleniumHelper' tool was created using selenium version {SELENIUM_VERSION}. The version you have installed in this project ({current_selenium_version}) may not be compatible with this tool. If you encounter any issues, either downgrade your selenium version to {SELENIUM_VERSION} or email the creator at caseywschmid@gmail.com to have the package updated."
                )
            if current_pyautogui_version != PYAUTOGUI_VERSION:
                log.warning(
                    f"The 'SeleniumHelper' tool was created using PyAutoGUI version {PYAUTOGUI_VERSION}. The version you have installed in this project ({current_pyautogui_version}) may not be compatible with this tool. If you encounter any issues, either downgrade your PyAutoGUI version to {PYAUTOGUI_VERSION} or email the creator at caseywschmid@gmail.com to have the package updated."
                )
            if current_psutil_version != PSUTIL_VERSION:
                log.warning(
                    f"The 'SeleniumHelper' tool was created using psutil version {PSUTIL_VERSION}. The version you have installed in this project ({current_psutil_version}) may not be compatible with this tool. If you encounter any issues, either downgrade your psutil version to {PSUTIL_VERSION} or email the creator at caseywschmid@gmail.com to have the package updated."
                )
            log.info(
                "These warnings can be muted by setting the MUTE_SELENIUM_HELPER_WARNING environment variable to 'True'."
            )

    def setup_remote_selenium(self) -> NoReturn:
        log.fine("SeleniumHelper.setup_remote_selenium")
        # This url is for the Selenium Grid running on AWS Kubernetes
        # See HostedSelenium project for more details
        selenium_url = os.getenv("HOSTED_SELENIUM_URL", "HOSTED_SELENIUM_URL_NOT_SET")
        if selenium_url == "HOSTED_SELENIUM_URL_NOT_SET":
            log.error("You must set the HOSTED_SELENIUM_URL environment variable.")
            raise ValueError("HOSTED_SELENIUM_URL environment variable not set.")

        log.debug(f"Attempting to connect to Selenium Grid at {selenium_url}")

        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        options.set_capability("browserName", "chrome")
        options.set_capability("browserVersion", "124.0")
        options.set_capability("platformName", "linux")

        log.fine(f"Chrome options and capabilities set: {options.to_capabilities()}")

        try:
            self.driver = webdriver.Remote(
                command_executor=selenium_url,
                options=options,
            )
            self.wait = WebDriverWait(self.driver, 30)
            log.debug("Remote WebDriver created successfully")
        except Exception as e:
            log.error(f"Failed to create remote WebDriver: {str(e)}")
            raise

    def start_coordinate_logging(
        self, logging_interval: float = 0.5, duration: int = 30
    ) -> NoReturn:
        """
        Logs the current mouse coordinates at specified intervals for a given
        duration.

        Args:
            logging_interval (float, optional): The time interval (in seconds)
            between each log of the mouse coordinates. Defaults to 0.5 seconds.

            duration (int, optional): The total duration (in seconds) for which
            the mouse coordinates will be logged. Defaults to 30 seconds.
        """
        log.fine("Selenium_Helper.start_coordinate_logging")
        self.is_logging_active = True
        end_time = time.time() + duration
        while time.time() < end_time:
            log.info(pyautogui.position())
            time.sleep(logging_interval)
        self.is_logging_active = False

    def open_chrome_in_debug(self) -> NoReturn:
        """
        This function opens a new Chrome window in incognito mode. It bypasses
        having to open the Terminal window.

        Note: In incognito mode, none of the authentication stuff works.
        """
        log.fine("Selenium_Helper.open_chrome_in_debug")
        os.system(
            f"open -na 'Google Chrome' --args --incognito --fresh --remote-debugging-port=9222"
        )

    def open_chrome(self) -> NoReturn:
        """
        This function opens a new Chrome window in incognito mode.
        """
        log.fine("Selenium_Helper.open_chrome")
        os.system(f"open -na 'Google Chrome' --args --incognito --fresh")

    def open_url_in_new_chrome_incognito_window(
        self,
        url: str,
        zoom: Annotated[int, "the zoom level you want to set"] = 100,
        debug: Annotated[bool, "whether to open the browser in debug mode"] = False,
        window_size: tuple[int, int] = (1300, 2100),
        window_position: tuple[int, int] = (100, 0),
    ) -> tuple[webdriver.Chrome, WebDriverWait]:
        """
        Opens the specified URL in a new Chrome incognito window with optional
        debug mode, zoom level, window size, and window position.

        Args:
            url (str): The URL to be opened.

            zoom (int, optional): The zoom level for the browser window,
            expressed as a percentage. Defaults to 100.

            debug (bool, optional): If True, opens the browser in debug mode.
            Defaults to False.

            window_size (tuple[int, int], optional): The size of the browser window
            as a tuple (width, height). Defaults to (1300, 2100).

            window_position (tuple[int, int], optional): The position of the browser
            window as a tuple (x, y). Defaults to (100, 0).

        Returns:
            tuple: A tuple containing the WebDriver instance and the
            WebDriverWait instance for the opened browser window.
        """
        log.fine(
            f"Selenium_Helper.open_url_in_new_chrome_incognito_window - DEBUG {debug}"
        )
        if debug:
            self.open_chrome_in_debug()
            options = webdriver.ChromeOptions()
            options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            self.driver = webdriver.Chrome(options=options)
        else:
            self.driver = webdriver.Chrome()
        self.driver.set_window_size(*window_size)
        self.driver.set_window_position(*window_position)
        self.driver.get(url)
        log.info(f"Zoom level: {zoom}%")
        self.driver.execute_script(f"document.body.style.zoom='{zoom}%'")
        self.wait = WebDriverWait(self.driver, 5)
        return self.driver, self.wait

    def close_browser(self) -> NoReturn:
        log.fine("Selenium_Helper.close_browser")
        if self.driver:
            self.driver.close()

    def close_chrome(self) -> NoReturn:
        """
        Closes the main Chrome process.

        This method iterates through all system processes to find the main
        Chrome process (not a child process like a tab or extension) and sends a
        termination signal to it.
        """
        log.fine("Selenium_Helper.close_chrome")
        for process in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
            try:
                if "chrome" in process.info["name"].lower():
                    # Check if it's the main Chrome process by the absence of '--type='
                    if not any(
                        arg.startswith("--type=") for arg in process.info["cmdline"]
                    ):
                        psutil.Process(process.info["pid"]).send_signal(signal.SIGTERM)
                        break  # Exit after signaling the main process
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def take_screenshot(
        self,
        file_path: Annotated[
            str, "Needs to have the '.png' added at the source. It is not added here."
        ],
    ) -> NoReturn:
        """
        Takes a screenshot of the current state of the browser and saves it to
        the specified file path.

        Args:
            file_path (Annotated[str, "The file path where the screenshot will
            be saved. The '.png' extension should be added at the source as it
            is not added in this method."]): The path to save the screenshot
            file.

        Raises:
            ValueError: If the browser driver has not been initialized.

        Returns:
            NoReturn: This method does not return anything and only performs the
            action of saving a screenshot.
        """
        log.fine("Selenium_Helper.take_screenshot")
        if self.driver is None:
            raise ValueError(
                "Driver not initialized. Please open a browser window first."
            )
        self.driver.save_screenshot(f"{file_path}")

    def capture_html(self, filename=None) -> str:
        log.fine("Selenium_Helper.capture_html")
        if self.driver is None:
            raise ValueError(
                "Driver not initialized. Please open a browser window first."
            )
        html = self.driver.page_source
        if filename is not None:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)
        return html

    def open_local_html_file(self, file_path: str) -> NoReturn:
        log.fine("Selenium_Helper.open_local_html_file")
        if self.driver is None:
            raise ValueError(
                "Driver not initialized. Please open a browser window first."
            )
        try:
            self.driver.get(f"file://{file_path}")
        except FileNotFoundError:
            log.error(f"File not found: {file_path}")
            raise
        except WebDriverException as e:
            log.error(f"WebDriverException occurred: {e}")
            raise
