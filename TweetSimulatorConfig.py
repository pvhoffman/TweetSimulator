import ConfigParser

class TweetSimulatorConfig:
    def __init__(self):
        self._config_file_name = 'config.ini'

    def _config_value(self, value):
        config = ConfigParser.ConfigParser()
        config.read(self._config_file_name)
        return config.get('Main', value)

    def TwitterUser(self):
        return self._config_value('TwitterUser')

    def ConsumerKey(self):
        return self._config_value('ConsumerKey')

    def ConsumerSecret(self):
        return self._config_value('ConsumerSecret')

    def AccessKey(self):
        return self._config_value('AccessKey')

    def AccessSecret(self):
        return self._config_value('AccessSecret')

    def DatabasePath(self):
        return self._config_value('DatabasePath')

    def StatusUpdateInterval(self):
        return self._config_value('StatusUpdateInterval')

