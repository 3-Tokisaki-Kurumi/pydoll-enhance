import platform
from typing import Optional, cast

from pydoll.browser.chromium.base import Browser
from pydoll.browser.managers import ChromiumOptionsManager
from pydoll.browser.options import ChromiumOptions
from pydoll.exceptions import UnsupportedOS
from pydoll.utils import validate_browser_paths


class Edge(Browser):
    """Edge browser implementation for CDP automation."""

    def __init__(
        self,
        options: Optional[ChromiumOptions] = None,
        connection_port: Optional[int] = None,
    ):
        """
        Initialize Edge browser instance.

        Args:
            options: Edge configuration options (default if None).
            connection_port: CDP WebSocket port (random if None).
        """
        options_manager = ChromiumOptionsManager(options)
        super().__init__(options_manager, connection_port)
        # Get fingerprint settings from already initialized options
        # Cast to ChromiumOptions to access fingerprint properties
        chromium_options = cast(ChromiumOptions, self.options)
        self.enable_fingerprint_spoofing = chromium_options.enable_fingerprint_spoofing
        self.fingerprint_manager = options_manager.get_fingerprint_manager()

    @staticmethod
    def _get_default_binary_location():
        """
        Get default Edge executable path based on OS.

        Returns:
            Path to Edge executable.

        Raises:
            UnsupportedOS: If OS is not supported.
            ValueError: If executable not found at default location.
        """
        os_name = platform.system()

        browser_paths = {
            'Windows': [
                (
                    r'C:\Program Files\Microsoft\Edge\Application'
                    r'\msedge.exe'
                ),
                (
                    r'C:\Program Files (x86)\Microsoft\Edge'
                    r'\Application\msedge.exe'
                ),
            ],
            'Linux': [
                '/usr/bin/microsoft-edge',
            ],
            'Darwin': [
                ('/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'),
            ],
        }

        browser_path = browser_paths.get(os_name)

        if not browser_path:
            raise UnsupportedOS()

        return validate_browser_paths(browser_path)
