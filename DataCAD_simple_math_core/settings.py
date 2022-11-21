import configparser
import os

from pathlib import Path
from core.settings.ini_config import merge_ini_config_with_defaults, configparser_to_dict

default_ini_config = {
    'logging': {
        'level': 'INFO'
    },
    'db_conf': {
        'host': 'localhost',
        'port': '5432',
        'database':  'DataCAD_simple_math_core',
        'user': 'DataCAD_simple_math_core',
        'password': 'DataCAD_simple_math_core'
    }
}


# try to read path to config from environment
conf_path_env = os.environ.get('DataCAD_simple_math_core_conf', None)
base_dir = Path(__file__).resolve().parent
if conf_path_env is None:
    conf_path = base_dir / 'DataCAD_simple_math_core.conf'
else:
    conf_path = Path(conf_path_env).resolve()

config = configparser.ConfigParser()

config.read(conf_path)

config = configparser_to_dict(config)

ini_config = merge_ini_config_with_defaults(config, default_ini_config)


# configure your own database if you need
# DATABASE = {
#         "ENGINE": 'django.db.backends.postgresql',
#         "NAME": ini_config['db_conf']['database'],
#         "USER": ini_config['db_conf']['user'],
#         "PASSWORD": ini_config['db_conf']['password'],
#         "HOST": ini_config['db_conf']['host'],
#         "PORT": ini_config['db_conf']['port']
# }

