# mib2zabbix
Python implemenation of [mib2zabbix](https://github.com/zabbix-tools/mib2zabbix) which was last updated in 2017 and is writen in perl. Within reason this will attempt to keep to the same interface as the original, given the major differences in zabbix since the original has since stopped development there are likely going to be differences that are unavoidable.


## Requirements
* Zabbix 7.0+
* Python 3.9+
  * Required packages
* Correctly configued MIB files

## Installation

### Install from GitHub

```bash
<pip command line>
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
