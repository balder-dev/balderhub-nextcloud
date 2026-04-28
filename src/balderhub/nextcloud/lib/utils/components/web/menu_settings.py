from balderhub.html.lib.utils import components as html
from balderhub.html.lib.utils.selector import Selector


class SettingMenu(html.HtmlDivElement):
    """
    settings menu that will be opened after pressing on the ``Settings menu`` button (profile icon) in the header
    """

    @property
    def btn_view_profile(self):
        """
        :return: returns the button for ``View profile``
        """
        return html.HtmlAnchorElement.by_selector(self.driver, Selector.by_id('profile'), parent=self)

    @property
    def btn_appearance_and_accessibility(self):
        """
        :return: returns the button for ``Appearance and accessibility``
        """
        return html.HtmlAnchorElement.by_selector(self.driver, Selector.by_id('accessibility_settings'), parent=self)

    @property
    def btn_settings(self):
        """
        :return: returns the button for ``Settings``
        """
        return html.HtmlAnchorElement.by_selector(self.driver, Selector.by_id('settings'), parent=self)

    @property
    def btn_admin_settings(self):
        """
        :return: returns the button for ``Settings``
        """
        return html.HtmlAnchorElement.by_selector(self.driver, Selector.by_id('admin_settings'), parent=self)


    @property
    def btn_apps(self):
        """
        :return: returns the button for ``Apps``
        """
        return html.HtmlAnchorElement.by_selector(self.driver, Selector.by_id('core_apps'), parent=self)

    @property
    def btn_accounts(self):
        """
        :return: returns the button for ``Accounts``
        """
        return html.HtmlAnchorElement.by_selector(self.driver, Selector.by_id('core_users'), parent=self)


    @property
    def btn_about(self):
        """
        :return: returns the button for ``About``
        """
        return html.HtmlAnchorElement.by_selector(self.driver, Selector.by_id('firstrunwizard_about'), parent=self)


    @property
    def btn_help(self):
        """
        :return: returns the button for ``Help``
        """
        return html.HtmlAnchorElement.by_selector(self.driver, Selector.by_id('help'), parent=self)

    @property
    def btn_log_out(self):
        """
        :return: returns the button for ``Log out``
        """
        return html.HtmlAnchorElement.by_selector(self.driver, Selector.by_id('logout'), parent=self)
