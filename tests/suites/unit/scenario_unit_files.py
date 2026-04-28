import logging
import time

import balder

import balderhub.selenium.lib.scenario_features
import balderhub.nextcloud.lib.pages.web
import balderhub.nextcloud.lib.scenario_features

logger = logging.getLogger(__name__)


class ScenarioUnitPageFiles(balder.Scenario):

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
    def open_files_page(self, dismiss_welcome_modal):
        self.WebClient.page_files.open()
        self.WebClient.page_files.wait_for_page()

    def test_files_url_is_applied(self):
        """
        validates that opening the files page navigates the browser to the expected files URL
        """
        expected_url = self.WebClient.page_files.applicable_on_url_schema[0].as_string()
        current_url = self.WebClient.selenium.driver.current_url
        assert current_url.rstrip('/').startswith(expected_url.rstrip('/')), \
            f'expected to be on `{expected_url}` but was on `{current_url}`'

    def test_new_menu_button_exists(self):
        """
        validates that the ``New`` menu toggle button exists and is visible on the files page
        """
        assert self.WebClient.page_files.btn_menutoggle_new.exists_within(1), '`New` button does not exist'
        assert self.WebClient.page_files.btn_menutoggle_new.is_visible(), '`New` button is not visible'

    def test_files_list_or_empty_hint_is_visible(self):
        """
        validates that either the files list table or the ``No files in here`` hint is visible on the files page
        """
        self.WebClient.page_files.table_files.exists_within(1)
        assert (
            self.WebClient.page_files.table_files.is_visible()
            or self.WebClient.page_files.span_no_files.is_visible()
        ), 'neither the files list table nor the `No files in here` hint is visible'

    def test_open_plus_menu(self):
        """
        validates that clicking the ``New`` menu toggle opens the plus menu
        """
        menu = self.WebClient.page_files.open_plus_menu()
        assert menu.exists(), 'plus menu does not exist after click'
        assert menu.is_visible(), 'plus menu is not visible after click'

    def test_get_all_visible_list_elements_returns_list(self):
        """
        validates that retrieving all visible list elements returns a list (possibly empty)
        """
        elements = self.WebClient.page_files.get_all_visible_list_elements()
        assert isinstance(elements, list), \
            f'expected list of file row items, got `{type(elements).__name__}`'
