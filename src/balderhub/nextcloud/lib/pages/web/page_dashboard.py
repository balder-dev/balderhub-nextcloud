from typing import Union, List

from balderhub.url.lib.utils import Url

from .base_page import BasePage


class PageDashboard(BasePage):
    """
    initial web app page that will be shown per default after login
    """

    @property
    def applicable_on_url_schema(self) -> Union[Url, List[Url]]:
        return Url(f'{self.Server.nextcloud.root_url.as_string()}/apps/dashboard')

    def open(self):
        """
        Navigates to the URL specified by the `applicable_on_url_schema` attribute.
        """
        self.driver.navigate_to(self.applicable_on_url_schema.as_string())
