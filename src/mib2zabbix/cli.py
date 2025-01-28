'''mib2zabbix CLI module'''


# System imports
import logging

# Local imports
from . import utils

logger = logging.getLogger(__name__)

def main():
    """Main CLI function
    """
    print("Entered mib2zabbix:main")

    utils.parse_mib('/home/dmcken/code/mib2zabbix/test/')
