import logging
import time

import balder

import balderhub.selenium.lib.scenario_features
import balderhub.nextcloud.lib.pages.web
import balderhub.nextcloud.lib.scenario_features

logger = logging.getLogger(__name__)


class ScenarioUnitPageDashboard(balder.Scenario):

    class NextcloudServer(balder.Device):
        _is_nextcloud = balderhub.nextcloud.lib.scenario_features.IsNextcloudServer()

    @balder.connect(NextcloudServer, balder.Connection)
    class WebClient(balder.Device):
        selenium = balderhub.selenium.lib.scenario_features.SeleniumFeature()
        page_login = balderhub.nextcloud.lib.pages.web.PageLogin(Server="NextcloudServer")
        page_files = balderhub.nextcloud.lib.pages.web.PageFiles(Server="NextcloudServer")
        page_dashboard = balderhub.nextcloud.lib.pages.web.PageDashboard(Server="NextcloudServer")

    @balder.fixture('variation')
    def login_user(self):
        self.WebClient.page_login.open()
        time.sleep(1) # TODO
        if self.WebClient.page_login.is_applicable():
            logger.info('user does not seem to be logged in -> do login')
            self.WebClient.page_login.input_username.type_text('admin')
            self.WebClient.page_login.input_password.type_text('Admin12345')
            self.WebClient.page_login.btn_login.click()
            self.WebClient.page_dashboard.wait_for_page()
        else:
            logger.info('user seems to be logged in - do nothing')
        yield

    @balder.fixture('variation')
    def dismiss_welcome_modal(self, login_user):
        # wait for 5 seconds to make sure that modal sequence has started (if any)
        if not self.WebClient.page_files.modal_video.exists_within(5):
            logger.info('video modal is not shown within 5 seconds')
            return
        if self.WebClient.page_files.modal_video.was_hidden_within(10):
            logger.info('video modal disappeared automatically within 10 seconds')
        else:
            logger.error('video modal does not automatically disappeared within 10 seconds')
            return

        # wait till the video modal is visible and then close it
        start_time = time.perf_counter()
        while not (
                self.WebClient.page_files.modal_welcome.exists() and self.WebClient.page_files.modal_welcome.is_visible()):
            # TODO add timeout and make it possible to call this in easier call
            time.sleep(.5)
            if time.perf_counter() - start_time > 15:
                logger.info('no modal visible -> skip dismiss-welcome-modal')
                # no modal visible within the first 15 seconds -> break
                return
        logger.info('dismiss welcome modal')

        self.WebClient.page_files.modal_welcome.btn_close.click()
        self.WebClient.page_files.modal_welcome.wait_to_be_hidden_for(3)

    @balder.fixture('testcase')
    def open_dashboard_page(self, dismiss_welcome_modal):
        self.WebClient.page_dashboard.open()
        self.WebClient.page_dashboard.wait_for_page()

    def test_dashboard_url_is_applied(self):
        """
        validates that opening the dashboard page navigates the browser to the expected dashboard URL
        """
        expected_url = self.WebClient.page_dashboard.applicable_on_url_schema.as_string()
        current_url = self.WebClient.selenium.driver.current_url
        assert current_url.rstrip('/').startswith(expected_url.rstrip('/')), \
            f'expected to be on `{expected_url}` but was on `{current_url}`'

    def test_dashboard_page_is_applicable(self):
        """
        validates that the dashboard page reports itself as applicable when the browser is on the dashboard URL
        """
        assert self.WebClient.page_dashboard.is_applicable(), \
            'page_dashboard.is_applicable() returned False while being on the dashboard url'

    def test_open_navigates_to_dashboard_url(self):
        """
        validates that calling ``open()`` actually navigates the browser to the dashboard URL even
        when starting from a different (blank) location
        """
        self.WebClient.selenium.driver.navigate_to('about:blank')
        time.sleep(1)
        self.WebClient.page_dashboard.open()
        self.WebClient.page_dashboard.wait_for_page()
        expected_url = self.WebClient.page_dashboard.applicable_on_url_schema.as_string()
        current_url = self.WebClient.selenium.driver.current_url
        assert current_url.rstrip('/').startswith(expected_url.rstrip('/')), \
            f'expected to be on `{expected_url}` after open() but was on `{current_url}`'

    def test_setting_menu_button_exists(self):
        """
        validates that the ``Settings menu`` (profile icon) button exists and is visible on the dashboard page
        """
        # pylint: disable=protected-access
        btn = self.WebClient.page_dashboard._btn_setting_menu
        assert btn.exists(), '`Settings menu` button does not exist on the dashboard page'
        assert btn.is_visible(), '`Settings menu` button is not visible on the dashboard page'

    def test_open_setting_menu_returns_visible_menu(self):
        """
        validates that clicking the ``Settings menu`` button on the dashboard opens the settings menu
        """
        setting_menu = self.WebClient.page_dashboard.open_setting_menu()
        assert setting_menu.exists(), 'settings menu does not exist after opening it'
        assert setting_menu.is_visible(), 'settings menu is not visible after opening it'

    def test_open_setting_menu_is_idempotent(self):
        """
        validates that calling ``open_setting_menu`` while the menu is already open returns the already
        visible menu without raising
        """
        first = self.WebClient.page_dashboard.open_setting_menu()
        assert first.is_visible(), 'settings menu is not visible after the first open call'
        second = self.WebClient.page_dashboard.open_setting_menu()
        assert second.is_visible(), 'settings menu is not visible after the second open call'

    def test_setting_menu_contains_log_out_button(self):
        """
        validates that the settings menu opened from the dashboard contains the ``Log out`` button
        """
        setting_menu = self.WebClient.page_dashboard.open_setting_menu()
        assert setting_menu.btn_log_out.exists(), '`Log out` button does not exist in the settings menu'
        assert setting_menu.btn_log_out.is_visible(), '`Log out` button is not visible in the settings menu'

    def test_modal_welcome_is_dismissed(self):
        """
        validates that after the ``dismiss_welcome_modal`` fixture the welcome modal is no longer visible
        on the dashboard page
        """
        assert not (
            self.WebClient.page_dashboard.modal_welcome.exists()
            and self.WebClient.page_dashboard.modal_welcome.is_visible()
        ), 'welcome modal is still visible on the dashboard page after dismissal'
