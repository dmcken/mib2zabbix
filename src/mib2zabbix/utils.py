'''Utility functions'''


# System imports
import os

# External imports
import pysmi
import pysmi.compiler
import pysmi.debug
import pysmi.parser
import pysmi.reader

#
from pysmi.reader import FileReader, HttpReader
from pysmi.searcher import StubSearcher
from pysmi.writer import CallbackWriter
from pysmi.parser import SmiStarParser
from pysmi.codegen import JsonCodeGen
from pysmi.compiler import MibCompiler

# Globals
PERL_HELP_TEXT = '''
mib2zabbix.pl -o <OID> [OPTIONS]...

Export loaded SNMP MIB OIDs to Zabbix Template XML

    -f, --filename=PATH         output filename (default: stdout)

    -N, --name=STRING           template name (default: OID label)
    -G, --group=STRING          template group (default: 'Templates')
    -e, --enable-items          enable all template items (default: disabled)

    -o, --oid=STRING            OID tree root to export

    -v, --snmpver=1|2|3         SNMP version (default: 2)
    -p, --port=PORT             SNMP UDP port number (default: 161)

SNMP Version 1 or 2c specific

    -c, --community=STRING      SNMP community string (default: 'public')

SNMP Version 3 specific

    -L, --level=LEVEL           security level (noAuthNoPriv|authNoPriv|authPriv)
    -n, --context=CONTEXT       context name
    -u, --username=USERNAME     security name
    -a, --auth=PROTOCOL         authentication protocol (MD5|SHA)
    -A, --authpass=PASSPHRASE   authentication protocol passphrase
    -x, --privacy=PROTOCOL      privacy protocol (DES|AES)
    -X, --privpass=PASSPHRASE   privacy passphrase

Zabbix item configuration

    --check-delay=SECONDS       check interval in seconds (default: 60)
    --disc-delay=SECONDS        discovery interval in seconds (default: 3600)
    --history=DAYS              history retention in days (default: 7)
    --trends=DAYS               trends retention in days (default: 365)

    -h, --help                  print this message
'''
ZBX_ITEM_STATE = { 'ENABLED': 0, 'DISABLED': 1 }
ZBX_ITEM_VAL_TYPE = {
    'FLOAT': 0,
    'CHAR':  1,
    'LOG':   2,
    'UINT':  3,
    'TEXT':  4,
    'SNMPTRAP': 17,
}
ZBX_TYPE_MAP = {
    'BITS'          : ZBX_ITEM_VAL_TYPE['TEXT'],
    'COUNTER'       : ZBX_ITEM_VAL_TYPE['UINT'],
    'COUNTER32'     : ZBX_ITEM_VAL_TYPE['UINT'],
    'COUNTER64'     : ZBX_ITEM_VAL_TYPE['UINT'],
    'GAUGE'         : ZBX_ITEM_VAL_TYPE['UINT'],
    'GAUGE32'       : ZBX_ITEM_VAL_TYPE['UINT'],
    'INTEGER'       : ZBX_ITEM_VAL_TYPE['FLOAT'],
    'INTEGER32'     : ZBX_ITEM_VAL_TYPE['FLOAT'],
    'IPADDR'        : ZBX_ITEM_VAL_TYPE['TEXT'],
    'NETADDDR'      : ZBX_ITEM_VAL_TYPE['TEXT'],
    'NOTIF'         : ZBX_ITEM_VAL_TYPE['SNMPTRAP'],
    'TRAP'          : ZBX_ITEM_VAL_TYPE['SNMPTRAP'],
    'OBJECTID'      : ZBX_ITEM_VAL_TYPE['TEXT'],
    'OCTETSTR'      : ZBX_ITEM_VAL_TYPE['TEXT'],
    'OPAQUE'        : ZBX_ITEM_VAL_TYPE['TEXT'],
    'TICKS'         : ZBX_ITEM_VAL_TYPE['UINT'],
    'UNSIGNED32'    : ZBX_ITEM_VAL_TYPE['UINT'],
}
ZBX_STORAGE_MODE = {
    'ASIS':   0, # Store as-is
    'SPEED':  1, # Delta, speed per second
    'CHANGE': 2, # Delta, simple change
}


def parse_args():
    """_summary_

    Current perl help text is listed above.
    """
    # -f, --filename=PATH         output filename (default: stdout)

    # -N, --name=STRING           template name (default: OID label)
    # -G, --group=STRING          template group (default: 'Templates')
    # -e, --enable-items          enable all template items (default: disabled)
    # -o, --oid=STRING            OID tree root to export

    # --check-delay=SECONDS       check interval in seconds (default: 60)
    # --disc-delay=SECONDS        discovery interval in seconds (default: 3600)
    # --history=DAYS              history retention in days (default: 7)
    # --trends=DAYS               trends retention in days (default: 365)

    # -h, --help                  print this message

def parse_mib(mib_dir: str) -> dict:
    """Parse a mib file to a dictionary.

    Args:
        mib_dir (str): Location of MIB files.

    Returns:
        dict: Result dictionary (possibly multi-layer).
    """
    result_data = {}
    # Enable debugging to see detailed log messages
    # pysmi.debug.set_logger(pysmi.debug.Debug('all'))

    # Define MIB compiler
    mib_compiler = pysmi.compiler.MibCompiler(
        pysmi.parser.SmiV1Parser(),
        pysmi.reader.FileReader(mib_dir),
        None
    )

    # Load and compile MIB files
    mib_compiler.addSources(mib_dir)  # Add source directories
    mib_compiler.compile()

    # Iterate through the MIBs and extract relevant information
    for mib in mib_compiler.getMibModules():
        print(f"Module: {mib}")
        # Extracting object OIDs and description
        for obj in mib_compiler.getMibSymbols(mib):
            symbol = mib_compiler.getMibSymbol(mib, obj)
            print(f"Object: {obj} -> OID: {symbol.getOid()}")

    return result_data
