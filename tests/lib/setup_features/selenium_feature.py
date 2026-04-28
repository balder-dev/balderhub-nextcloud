from balderhub.selenium.lib.setup_features import SeleniumRemoteWebdriverFeature
from selenium.webdriver.common.options import BaseOptions
from selenium.webdriver.firefox.options import Options


class SeleniumFeature(SeleniumRemoteWebdriverFeature):

    @property
    def command_executor(self) -> str:
        return "http://seleniumfirefox:4444"

    @property
    def selenium_options(self) -> BaseOptions:
        return Options()
