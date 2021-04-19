import configparser

"""A config parser that will read from config.ini."""

class ConfigParser():
    config_file_path = 'config/config.ini'
    config = configparser.ConfigParser()

    try:
        with open(config_file_path) as f:
            config.read(config_file_path)
    except (OSError, IOError) as e:
        raise Exception("Couldn't find path to config.ini.") from e
    
    @classmethod
    def get(cls, parent, child):
        return cls.config.get(parent, child)