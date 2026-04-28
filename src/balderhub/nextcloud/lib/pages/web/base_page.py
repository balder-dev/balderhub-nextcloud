from typing import Union, List

import balder
from balderhub.html.lib.scenario_features.html_page import HtmlPage
from balderhub.html.lib.utils.selector import Selector
import balderhub.html.lib.utils.components as html
from balderhub.url.lib.utils import Url

from balderhub.nextcloud.lib.scenario_features import IsNextcloudServer
from balderhub.nextcloud.lib.utils.components.web import ModalVideo, ModalWelcome, SettingMenu


class BasePage(HtmlPage):
    """
    base class for all web pages of the nextcloud web app
    """

    class Server(balder.VDevice):
        """
        remote serve vdevice
        """
        nextcloud = IsNextcloudServer()

    @property
    def applicable_on_url_schema(self) -> Union[Url, List[Url]]:
        raise NotImplementedError

    @property
    def modal_video(self) -> ModalVideo:
        """
        :return: selector to get the video modal
        """
        return ModalVideo.by_selector(
            self.driver, Selector.by_xpath(".//div[contains(@class, 'modal-wrapper') and .//video")
        )

    @property
    def modal_welcome(self) -> ModalWelcome:
        """
        :return: selector to get the welcome model
        """
        return ModalWelcome.by_selector(
            self.driver,
            Selector.by_xpath(".//div[contains(@class, 'modal-wrapper') "
                              "and .//h2[contains(text(), 'A collaboration platform that puts you in control')]]")
        )

    @property
    def _btn_setting_menu(self):
        return html.HtmlButtonElement.by_selector(
            self.driver,
            Selector.by_xpath('.//button[@aria-label="Settings menu"]')
        )

    def open_setting_menu(self, timeout_sec: float = 1) -> SettingMenu:
        """
        Open the settings menu.

        This method attempts to locate and return the `SettingMenu` instance associated
        with the application's user interface. If the settings menu is already visible,
        it retrieves it directly. Otherwise, it interacts with the UI to display the
        settings menu and waits for it to become visible within a specific timeout period.

        :param timeout_sec: timeout in seconds
        :return: An instance of `SettingMenu` representing the settings menu.
        :raises TimeoutException: If the settings menu does not become visible within
            the specified timeout period.
        """
        setting_menu = SettingMenu.by_selector(
            self.driver,
            Selector.by_id('header-menu-user-menu')
        )
        if setting_menu.is_visible():
            return setting_menu
        self._btn_setting_menu.click()
        return setting_menu.wait_to_be_visible_for(timeout_sec)
