from common.utils import load_json_file


class ConfigManager:
    def __init__(self, config_files=None):
        self.config = {}
        self.load_config_files(config_files if config_files else [])

    def load_config_files(self, config_files):
        for config_file in config_files:
            file_config = load_json_file(config_file)
            self.config.update(file_config)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def get_all(self) -> dict:
        return self.config
