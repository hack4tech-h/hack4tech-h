import importlib
from config import default


class Settings(object):
    def __init__(self):
        # Get configuration information in global variables
        for attr in dir(default):
            setattr(self, attr, getattr(default, attr))
        setting_modules = ['config.setting', 'config.api']
        for setting_module in setting_modules:
            setting = importlib.import_module(setting_module)
            for attr in dir(setting):
                setattr(self, attr, getattr(setting, attr))


settings = Settings()
