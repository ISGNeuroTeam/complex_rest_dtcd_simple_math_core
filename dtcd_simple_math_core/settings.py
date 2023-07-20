"""Plugin's settings module"""
import configparser
import logging.config
import os

from pathlib import Path
# pylint: disable=import-error
from core.settings.ini_config import merge_ini_config_with_defaults, configparser_to_dict

__author__ = "Andrey Starchenkov"
__copyright__ = "Copyright 2023, ISG Neuro"
__credits__ = ["Nikita Serditov"]
__license__ = "OT.PLATFORM. License agreement."
__version__ = "0.1.0"
__maintainer__ = "Andrey Starchenkov"
__email__ = "astarchnenkov@isgneuro.com"
__status__ = "Pre-release"

default_ini_config = {
    'logging': {
        'level': 'DEBUG'
    },
    'db_conf': {
        'host': 'localhost',
        'port': '5432',
        'database': 'dtcd_simple_math_core',
        'user': 'dtcd_simple_math_core',
        'password': 'dtcd_simple_math_core'
    }
}

# try to read path to config from environment
conf_path_env = os.environ.get('dtcd_simple_math_core_conf', None)
base_dir = Path(__file__).resolve().parent
if conf_path_env is None:
    conf_path = base_dir / 'dtcd_simple_math_core.conf'
else:
    conf_path = Path(conf_path_env).resolve()

config = configparser.ConfigParser()
config.read(conf_path)
config = configparser_to_dict(config)
ini_config = merge_ini_config_with_defaults(config, default_ini_config)
plugin_name = 'dtcd_simple_math_core'  # pylint: disable=invalid-name
CONNECTOR_CONFIG = ini_config['ot_simple_connector']
EVAL_GLOBALS = ini_config['eval_globals']
GRAPH_GLOBALS = ini_config['graph_globals']
SETTINGS_FILE_PATH = Path().resolve()

# set graph key names
GRAPH_KEY_NAMES = ini_config['graph_key_names']

# set otl create fresh swt table query
OTL_CREATE_FRESH_SWT = GRAPH_GLOBALS['otl_create_fresh_swt']
RE_DATALAKENODE = GRAPH_GLOBALS['re_datalakenode']
FILTER_DATALAKENODE_COLUMNS = bool(GRAPH_GLOBALS['use_re_datalakenode'])

# set logger
base_logs_dir = ini_config['general'].get('logs_path', '.')
logger = logging.getLogger('dtcd_simple_math_core')
logger.info('Version: %s', __version__)
logger.info('OT simple connector config: %s', CONNECTOR_CONFIG)
logger.info('OTL create fresh swt table command: %s', OTL_CREATE_FRESH_SWT)
