import os
import time
import signal
import psutil
import pyautogui

from typing import NoReturn
from typing import Annotated

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from constants.settings import LOG_LEVEL

import logging
from ..logs import logger

logger.configure_logging(__name__, log_level=LOG_LEVEL)
log = logging.getLogger(__name__)


class SeleniumHelper:
    def __init__(self):
        self.driver = None
        self.wait = None
        # Global flag to control the logging loop
        self.is_logging_active = False

    def start_coordinate_logging(
        self, logging_interval: float = 0.5, duration: int = 30
    ):
        """
        Logs the current mouse coordinates at specified intervals for a given
        duration.

        Args:
            logging_interval (float, optional): The time interval (in seconds)
            between each log of the mouse coordinates. Defaults to 0.5 seconds.
            
            duration (int, optional): The total duration (in seconds) for which
            the mouse coordinates will be logged. Defaults to 30 seconds.
        """
        log.fine("start_coordinate_logging")
        self.is_logging_active = True
        end_time = time.time() + duration
        while time.time() < end_time:
            log.info(pyautogui.position())
            time.sleep(logging_interval)
        self.is_logging_active = False

    def open_chrome_in_debug(self):
        """
        This function opens a new Chrome window in incognito mode. It bypasses
        having to open the Terminal window.

        Note: In incognito mode, none of the authentication stuff works.
        """
        log.fine("open_chrome_in_debug")
        os.system(
            f"open -na 'Google Chrome' --args --incognito --fresh --remote-debugging-port=9222"
        )

    def open_chrome(self):
        """
        This function opens a new Chrome window in incognito mode.
        """
        log.fine("open_chrome")
        os.system(f"open -na 'Google Chrome' --args --incognito --fresh")

    def open_url_in_new_chrome_incognito_window(
        self,
        url: str,
        zoom: Annotated[int, "the zoom level you want to set"] = 100,
        debug: Annotated[bool, "whether to open the browser in debug mode"] = False,
        window_size: tuple[int, int] = (1300, 2100),
        window_position: tuple[int, int] = (100, 0)
    ):
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
        log.fine(f"open_url_in_new_chrome_incognito_window - DEBUG {debug}")
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

    def close_browser(self):
        log.fine("close_browser")
        if self.driver:
            self.driver.close()

    def close_chrome(self):
        """
        Closes the main Chrome process.

        This method iterates through all system processes to find the main
        Chrome process (not a child process like a tab or extension) and sends a
        termination signal to it.
        """
        log.fine("close_chrome")
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
        log.fine("take_screenshot")
        if self.driver is None:
            raise ValueError(
                "Driver not initialized. Please open a browser window first."
            )
        self.driver.save_screenshot(f"{file_path}")

    def capture_html(self, filename=None):
        log.fine("capture_html")
        if self.driver is None:
            raise ValueError(
                "Driver not initialized. Please open a browser window first."
            )
        html = self.driver.page_source
        if filename is not None:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)
        return html
