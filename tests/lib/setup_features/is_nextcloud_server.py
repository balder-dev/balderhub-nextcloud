import balderhub.nextcloud.lib.scenario_features

class IsNextcloudServer(balderhub.nextcloud.lib.scenario_features.IsNextcloudServer):

    @property
    def hostname(self) -> str:
        return "nextcloud"
