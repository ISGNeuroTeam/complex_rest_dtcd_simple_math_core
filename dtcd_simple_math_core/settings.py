import configparser
import logging.config
import os

from pathlib import Path
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


def set_logger(loglevel, logfile, logger_name):
    levels = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG
    }

    log_dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': "%(asctime)s %(levelname)-s PID=%(process)d %(module)s:%(lineno)d "
                          "func=%(funcName)s - %(message)s"
            },
            'with_hid': {
                'format': "%(asctime)s %(levelname)-s PID=%(process)d HID=%(hid)s %(module)s:%(lineno)d "
                          "func=%(funcName)s - %(message)s"
            }
        },
        'handlers': {
            'file_handler_standard': {
                'filename': logfile,
                'level': levels[loglevel],
                'class': 'logging.FileHandler',
                'formatter': 'standard'
            },
            'file_handler_with_hid': {
                'filename': logfile,
                'level': levels[loglevel],
                'class': 'logging.FileHandler',
                'formatter': 'with_hid'
            },
            'stream_handler_standard': {
                'stream': 'ext://sys.stdout',
                'level': levels[loglevel],
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
            'stream_handler_with_hid': {
                'stream': 'ext://sys.stdout',
                'level': levels[loglevel],
                'class': 'logging.StreamHandler',
                'formatter': 'with_hid'
            },
        },
        'loggers': {
            'osr': {
                'handlers': ['file_handler_standard', 'stream_handler_standard'],
                'level': levels[loglevel],
                'propagate': False
            },
            'osr_hid': {
                'handlers': ['file_handler_with_hid', 'stream_handler_with_hid'],
                'level': levels[loglevel]
            },
        },
        'root': {
            'handlers': ['file_handler_standard', 'stream_handler_standard'],
            'level': levels[loglevel]
        }
    }

    logging.config.dictConfig(log_dict)
    result = logging.getLogger(logger_name)
    return result


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
plugin_name = 'dtcd_simple_math_core'
CONNECTOR_CONFIG = ini_config['ot_simple_connector']
EVAL_GLOBALS = ini_config['eval_globals']
GRAPH_GLOBALS = ini_config['graph_globals']

# set graph key names
GRAPH_KEY_NAMES = ini_config['graph_key_names']

# set otl create fresh swt table query
OTL_CREATE_FRESH_SWT = GRAPH_GLOBALS['otl_create_fresh_swt']

# set logger
base_logs_dir = ini_config['general'].get('logs_path', '.')
logger = set_logger(ini_config['logging'].get('level', 'INFO'),
                    os.path.join(base_logs_dir, 'dtcd_simple_math_core.log'), plugin_name)
logger.info('Version: %s' % __version__)
logger.info('OT simple connector config: %s' % CONNECTOR_CONFIG)
logger.info(f'OTL create fresh swt table command: {OTL_CREATE_FRESH_SWT}')
