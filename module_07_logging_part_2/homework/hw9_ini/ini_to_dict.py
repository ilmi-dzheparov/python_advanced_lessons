import configparser
from configparser import ExtendedInterpolation

config = configparser.ConfigParser(interpolation=ExtendedInterpolation())
config.read('logging_conf.ini')


config_dict = {}
for section in config.sections():
    if '_' not in section:
        config_dict[section] = {}
        if config.options(section)[0] == 'keys':
            for key in config.get(section=section, option='keys').split(','):
                config_dict[section][key] = {}
    if '_' in section:
        keys = section.split('_')
        key_1 = keys[0] + 's'
        key_2 = keys[1]
        for option in config.options(section):
            config_dict[key_1][key_2][option] = config.get(section=section, option=option)


print(config_dict)