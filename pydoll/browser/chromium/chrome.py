import platform
from typing import Optional

from pydoll.browser.chromium.base import Browser
from pydoll.browser.managers import ChromiumOptionsManager
from pydoll.browser.options import ChromiumOptions
from pydoll.exceptions import UnsupportedOS
from pydoll.utils import validate_browser_paths


class Chrome(Browser):
    """Chrome browser implementation for CDP automation."""

    def __init__(
        self,
        options: Optional[ChromiumOptions] = None,
        connection_port: Optional[int] = None,
        enable_fingerprint_spoofing: bool = False,
        fingerprint_config=None,
    ):
        """
        Initialize Chrome browser instance.

        Args:
            options: Chrome configuration options (default if None).
            connection_port: CDP WebSocket port (random if None).
            enable_fingerprint_spoofing: Whether to enable fingerprint spoofing.
            fingerprint_config: Configuration for fingerprint generation.
        """
        options_manager = ChromiumOptionsManager(
            options,
            enable_fingerprint_spoofing,
            fingerprint_config
        )
        super().__init__(options_manager, connection_port)
        self.enable_fingerprint_spoofing = enable_fingerprint_spoofing
        self.fingerprint_manager = options_manager.get_fingerprint_manager()

    @staticmethod
    def _get_default_binary_location():
        """
        Get default Chrome executable path based on OS.

        Returns:
            Path to Chrome executable.

        Raises:
            UnsupportedOS: If OS is not supported.
            ValueError: If executable not found at default location.
        """
        os_name = platform.system()

        browser_paths = {
            'Windows': [
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            ],
            'Linux': [
                '/usr/bin/google-chrome',
            ],
            'Darwin': [
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            ],
        }

        browser_path = browser_paths.get(os_name)

        if not browser_path:
            raise UnsupportedOS(f'Unsupported OS: {os_name}')

        return validate_browser_paths(browser_path)
