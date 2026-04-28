import time

import balder

import balderhub.selenium.lib.scenario_features
import balderhub.nextcloud.lib.pages.web
import balderhub.nextcloud.lib.scenario_features


class ScenarioUnitPageLogin(balder.Scenario):

    class NextcloudServer(balder.Device):
        _is_nextcloud = balderhub.nextcloud.lib.scenario_features.IsNextcloudServer()

    @balder.connect(NextcloudServer, balder.Connection)
    class WebClient(balder.Device):
        selenium = balderhub.selenium.lib.scenario_features.SeleniumFeature()
        page_login = balderhub.nextcloud.lib.pages.web.PageLogin(Server="NextcloudServer")
        page_dashboard = balderhub.nextcloud.lib.pages.web.PageDashboard(Server="NextcloudServer")

    @balder.fixture('variation')
    def make_sure_to_be_logged_out(self):
        # TODO improve
        self.WebClient.page_dashboard.open()
        if self.WebClient.page_dashboard.is_applicable() and not self.WebClient.page_login.is_applicable():
            # need to logout
            setting_menu = self.WebClient.page_dashboard.open_setting_menu()
            setting_menu.btn_log_out.click()
        #self.WebClient.page_login.wait_for_page() # todo get parameter should be ignored - needs to be configurable

    @balder.fixture('testcase')
    def open_login_page(self):
        self.WebClient.page_login.open()
        time.sleep(1)  # TODO wait_for_page

    def test_login_url_is_applied(self):
        """
        validates that opening the login page navigates the browser to the expected login URL
        """
        expected_url = self.WebClient.page_login.applicable_on_url_schema.as_string()
        current_url = self.WebClient.selenium.driver.current_url
        assert current_url.rstrip('/') == expected_url.rstrip('/'), \
            f'expected to be on `{expected_url}` but was on `{current_url}`'

    def test_username_input_exists(self):
        """
        validates that the username input field exists and is visible on the login page
        """
        assert self.WebClient.page_login.input_username.exists(), 'username input does not exist'
        assert self.WebClient.page_login.input_username.is_visible(), 'username input is not visible'

    def test_password_input_exists(self):
        """
        validates that the password input field exists and is visible on the login page
        """
        assert self.WebClient.page_login.input_password.exists(), 'password input does not exist'
        assert self.WebClient.page_login.input_password.is_visible(), 'password input is not visible'

    def test_login_button_exists(self):
        """
        validates that the login submit button exists and is visible on the login page
        """
        assert self.WebClient.page_login.btn_login.exists(), 'login button does not exist'
        assert self.WebClient.page_login.btn_login.is_visible(), 'login button is not visible'

    def test_type_username(self):
        """
        validates that text typed into the username input is reflected in the field's value
        """
        self.WebClient.page_login.input_username.type_text('some-user')
        assert self.WebClient.page_login.input_username.value == 'some-user', \
            f'unexpected value `{self.WebClient.page_login.input_username.value}` in username input'

    def test_type_password(self):
        """
        validates that text typed into the password input is reflected in the field's value
        """
        self.WebClient.page_login.input_password.type_text('some-password')
        assert self.WebClient.page_login.input_password.value == 'some-password', \
            f'unexpected value `{self.WebClient.page_login.input_password.value}` in password input'

    def test_login_with_empty_credentials_stays_on_login_page(self):
        """
        validates that submitting the login form without credentials does not leave the login page
        """
        self.WebClient.page_login.btn_login.click()
        time.sleep(1)
        expected_url = self.WebClient.page_login.applicable_on_url_schema.as_string()
        current_url = self.WebClient.selenium.driver.current_url
        assert current_url.rstrip('/') == expected_url.rstrip('/'), \
            f'expected to remain on login page `{expected_url}` but was on `{current_url}`'

    def test_open_navigates_to_login_url(self):
        """
        validates that calling ``open()`` actually navigates the browser to the login URL even
        when starting from a different (blank) location
        """
        self.WebClient.selenium.driver.navigate_to('about:blank')
        time.sleep(1)
        self.WebClient.page_login.open()
        time.sleep(1)
        expected_url = self.WebClient.page_login.applicable_on_url_schema.as_string()
        current_url = self.WebClient.selenium.driver.current_url
        assert current_url.rstrip('/') == expected_url.rstrip('/'), \
            f'expected to be on `{expected_url}` after open() but was on `{current_url}`'

    def test_username_input_is_initially_empty(self):
        """
        validates that the username input does not contain any pre-filled value when the login page is freshly opened
        """
        assert self.WebClient.page_login.input_username.value == '', \
            f'expected empty username input but got `{self.WebClient.page_login.input_username.value}`'

    def test_password_input_is_initially_empty(self):
        """
        validates that the password input does not contain any pre-filled value when the login page is freshly opened
        """
        assert self.WebClient.page_login.input_password.value == '', \
            f'expected empty password input but got `{self.WebClient.page_login.input_password.value}`'

    def test_login_button_is_clickable(self):
        """
        validates that the login submit button can be reached as a clickable element on the login page
        """
        self.WebClient.page_login.btn_login.wait_to_be_clickable_for(3)

    def test_login_with_invalid_credentials_stays_on_login_page(self):
        """
        validates that submitting the login form with invalid credentials does not leave the login page
        """
        self.WebClient.page_login.input_username.type_text('invalid-user')
        self.WebClient.page_login.input_password.type_text('invalid-password')
        self.WebClient.page_login.btn_login.click()
        time.sleep(2)
        expected_url = self.WebClient.page_login.applicable_on_url_schema.as_string()
        current_url = self.WebClient.selenium.driver.current_url
        assert current_url.rstrip('/').startswith(expected_url.rstrip('/')), \
            f'expected to remain on login page `{expected_url}` but was on `{current_url}`'
