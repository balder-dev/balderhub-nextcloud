import logging
import time

import balder

import balderhub.nextcloud.lib.pages.web
from lib.setup_features.is_nextcloud_server import IsNextcloudServer

from lib.setup_features.selenium_feature import SeleniumFeature

logger = logging.getLogger(__file__)


class SetupWeb(balder.Setup):

    class NextcloudServer(balder.Device):
        is_nextcloud = IsNextcloudServer()

    @balder.connect(NextcloudServer, balder.Connection)
    class WebClient(balder.Device):
        page_login = balderhub.nextcloud.lib.pages.web.PageLogin()
        page_dashbpard = balderhub.nextcloud.lib.pages.web.PageDashboard()
        page_files = balderhub.nextcloud.lib.pages.web.PageFiles()
        page_markdown_editor = balderhub.nextcloud.lib.pages.web.PageMarkdownEditor()
        selenium = SeleniumFeature()

    @balder.fixture('setup')
    def setup_selenium(self):
        self.WebClient.selenium.create()
        yield
        self.WebClient.selenium.quit()

    #@balder.fixture('testcase')
    #def delete_all_files(self):
    #    yield
    #    self.WebClient.page_files.open()
    #    self.WebClient.page_files.wait_for_page()
    #    time.sleep(1)
    #    self.WebClient.page_files.table_files.checkbox_selectall.click()
    #    self.WebClient.page_files.table_files.actions_batch.btn_menutoggle.click()
    #    self.WebClient.page_files.table_files.actions_batch.context_menu.get_button_by_text('Delete').click()
    #    time.sleep(1)
    #    if self.WebClient.page_files.modal_confirm_deletion.exists():
    #        self.WebClient.page_files.modal_confirm_deletion.btn_delete.click()
    #    time.sleep(2)
    #    # todo assert not self.WebClient.page_files.table_files.exists()
