'''Basic SMI example'''

# System imports
import json
import pprint

# External imports
from pysmi.reader import FileReader, HttpReader
from pysmi.searcher import StubSearcher
from pysmi.writer import CallbackWriter
from pysmi.parser import SmiStarParser
from pysmi.codegen import JsonCodeGen
from pysmi.compiler import MibCompiler

#from pysmi import debug
#debug.set_logger(debug.Debug('reader', 'compiler'))

INPUT_MIB = 'CAMBIUM-ePMP-5.9.1-MIB'

inputMibs = [
    INPUT_MIB,
]
srcDirectories = [
    # Folder holding the file I want parsed
    '/home/dmcken/code/mib2zabbix/test',
    # System MIBs, want to get rid of this.
    "/usr/share/snmp/mibs",
]
HTTP_SOURCES = [
    ("mibs.pysnmp.com", 443, "/asn1/@mib@")
]

def save_to_dict(mib_name, json_doc, cb_ctx):
    '''Save the MIB output to the dictionary.
    '''
    cb_ctx[mib_name] = json.loads(json_doc)


# Initialize compiler infrastructure
json_output = {}
mibCompiler = MibCompiler(SmiStarParser(), JsonCodeGen(), CallbackWriter(save_to_dict, json_output))

# search for source MIBs here
mibCompiler.add_sources(*[FileReader(x) for x in srcDirectories])

# search for source MIBs at Web sites
mibCompiler.add_sources(*[HttpReader(x) for x in HTTP_SOURCES])

# never recompile MIBs with MACROs
mibCompiler.add_searchers(StubSearcher(*JsonCodeGen.baseMibs))

# run recursive MIB compilation
results = mibCompiler.compile(*inputMibs)

# print(f"{os.linesep}# Results: {'', ''.join(f'{x}:{results[x]}' for x in results)}")

pprint.pprint(
    json_output['CAMBIUM-PMP80211-MIB']['wirelessInterfaceScanFrequencyBandwidth'],
    width=120,
)
