#!/bin/bash
service samba-ad-dc start
sleep 5
DCPROMO=/etc/dcpromo/dcpromo
DNSDOMAINNAME=$(cat $DCPROMO | grep "\-\-realm" | cut -d"=" -f2 | cut -d" " -f1 | tr [A-Z] [a-z])
HOSTNAME=$(cat $DCPROMO | grep "\-\-host-name" | cut -d"=" -f2 | cut -d" " -f1 | tr [A-Z] [a-z])
ADMINPASS=$(cat $DCPROMO | grep "\-\-adminpass" | cut -d"=" -f2 | cut -d" " -f1 )
AD_IPADDR=$(samba-tool dns query 127.0.0.1 $DNSDOMAINNAME $HOSTNAME A | egrep -o --regexp='[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}.[0-9]{1,3}')
ETH0_IPADDR=$(ip addr show eth0 | egrep -o --regexp='[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}.[0-9]{1,3}')
if [ "$AD_IPADDR" != "$ETH0_IPADDR" ]; then
  samba-tool dns update 127.0.0.1 $DNSDOMAINNAME $HOSTNAME A $AD_IPADDR $ETH0_IPADDR --username=Administrator --password=$ADMINPASS
fi
service samba-ad-dc stop
sleep 5
/usr/sbin/samba --interactive
