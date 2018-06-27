## Introduction

This script is an fork of the [original](https://share.zabbix.com/cat-app/cluster/monitoring-citrix-xenserver-host-and-vms-based-on-pyton-xenapi) written by Robert Gladewitz, that is designed to monitor pools of xenserver hosts through zabbix.

The changes makes are to optimize the access and security in environments with a large number of hosts / pools.

`Marllus Lustosa - marlluslustosa@gmail.com`<br>
`Fabrício Silva  - fabricio.silva@sti.ufc.br`<br>
`Change: 25. June 2018`<br>

## Description

This script is based on XenAPI, that is, all client (zabbix) calls to the server are performed via XenAPI, using the Python language.

In the original script the files were saved in the format "/tmp/xenapi.hostperformance.tmp". However, when you have an environment with many pools to manage, you woulding need to create another script to add to another pool.

In this modification, the script writes the file specifying which server was managed 'at that time', obeying the pattern "/tmp/xenapi.hostperformance.tmp.NAME-OF-HOSTSERVER".
With this you can capture all the information regarding the server without having to create other calls using duplicate script.

Another change was the way he handles passwords.
In the original script you would have to put the password in 'plain text' as a parameter in the script execution, this means that there in the zabbix php web form (template configuration) you would have to type the password in 'plain text', the which is a tremendous insecurity.

In this script we try to solve this problem by creating a function to read the credentials (scrambled with base64) of a file (credentials.txt) that will be in the same directory as the citrix.xenserver.py script. So you can leave the username and password parameter blank in zabbix web which will not influence script execution since these credentials will be read from this file in the directory inside the zabbix operating system.

## Args
#### -h               Command line help

`-H <hostname>    Hostname of xenserver (-t host) or vm (-t vm)`<br>
`-m <hostname>    Hostname of xenserver master (ca be the same)`<br>
`-u <username>    Username for connect xenserver (local or domain user).`<br>
`-p <password>    Password for connect xenserver`<br>
`-c <command>     Command can be list, value`<br>
`-f <filter>      filter for values or lists (for list you can use regular expression, for values only the key)`<br>
`-t <host|vm>     querytype`<br>
`[-a <maxage>]    time of seconds, the cachefile will be use`<br>

## Building (testing on locally GNU/Linux (Connectivity to hosts xenserver))

You'll have to follow the steps below:

1. Download this project (.zip) or 'git clone https://gitlab.com/mlustosa/xenserver-zabbix-monitoring.git' in shell
1. Download Pyton XENApi.py from https://github.com/xapi-project/xen-api/tree/master/scripts/examples/python. Please use the last version, becaus of ssl support changes in pyton
1. Copy file XENApi.py to directory /usr/local/lib/python
1. Copy citrix.xenserver.py to you external script path and set userrights (chmod 755) (Generally in /usr/lib/zabbix/externalscripts).
1. Execute `$ python acesso.py` (To generate credentials.txt (username and password))
1. Change line `arq_cred     = /location/ofthe/archive/credentials.txt` to real location in system.

## Examples
List all CPUs:<br>
`#python citrix.xenserver.py -m myxenserver1 -u TheUserDoesNotMatter -p "ThePassDoesNotMatter" -c list -f "cpu\d+" -t host -H myxenserver2`

List all network interfaces:<br>
`#python citrix.xenserver.py -m myxenserver1 -u TheUserDoesNotMatter -p "ThePassDoesNotMatter" -c listni -f ".*" -t host -H myxenserver2`

List all network interfaces:<br>
`#python citrix.xenserver.py -m myxenserver1 -u TheUserDoesNotMatter -p "ThePassDoesNotMatter" -c listsr -f ".*" -t host -H myxenserver2`

List all vbd in a vm:<br>
`#python citrix.xenserver.py -m myxenserver1 -u TheUserDoesNotMatter -p "ThePassDoesNotMatter" -c listvbd -f ".*" -t host -H myvmhost`

Get value of cpu2:<br>
`#python citrix.xenserver.py -m myxenserver1 -u TheUserDoesNotMatter -p "ThePassDoesNotMatter" -c value -f cpu2 -t host -H myxenserver2`

## Building (Zabbix Server production)

Follow all steps of the Building Testing and:

1. Import the templates: 
    - zbx_template_xenserver_host.xml -->Monitoring XEN Host
    - zbx_template_xenserver_vm.xml --> Monitoring XEN VMs
    - Please note, the the name in zabbix and the name in xen have to be the same!
1. Set macros (Global on on all host you use this templates)
    - {$XENMASTER} -->Masterserver of XENCLUSTER
    - {$XENUSERNAME} --> Username for connect to XENCLUSTER
    - {$XENPASSWORD} --> Password for connect to XENCLUSTER

## Some knowing error

**DNS:**<br>
The XENApi functions returns the short name of xencluster server. So, if you are not have dns domain in search list, the resultion 
do not work. If you do not have a DNS server configured on zabbix or the test server you can add the manual entries in the /etc/hosts file, like this:<br>
*XEN-HOST-IP myserver01*


**Execution and filesystem rights for cache file:**<br>
If you test this script as root it will be created an cachefile. So, if zabbix later start this script as user user zabbix or 
www-data, the old cache file (creates by user root) can not open for writing. This script will exit with error.

## Important
If you test this script by executing as root it will be created an cachefile as user root. So, if zabbix later start this script as user user zabbix or www-data, the old cache file (creates by user root) can not open for writing. This script will exit with error!!!!!!!!!
