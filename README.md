# mib2zabbix
Python implemenation of [mib2zabbix](https://github.com/zabbix-tools/mib2zabbix) which was last updated in 2017 and is writen in perl. Within reason this will attempt to keep to the same interface as the original, given the major differences in zabbix since the original has since stopped development there are going to be differences that are unavoidable (simple examples being snmp version and community string being unneccesary as they are no longer defined in the template but at the host level).

## Goals

* Read a mib file or group of files and produce a zabbix importable JSON, XML or YAML file.

## Requirements
* Zabbix 7.0+
* Python 3.9+
  * Required packages
* Correctly configued MIB files

## Installation

### Install from GitHub

Via pip or pipx

```bash
pip install -U git+https://github.com/dmcken/mib2zabbix.git
```

### Mappings

This table describes how MIB elements are translated into Zabbix template elements:

| MIB Type | Zabbix object |
| -------- | ------------- |
| Scalar OID | Zabbix SNMP Item |
| Table OID | Zabbix SNMP Discovery Rule |
| Table Column OID | Zabbix Discovery Prototype |
| Trap/Notification OID | Zabbix SNMP Trap Item |
| OID Enums | Zabbix Value Maps |
