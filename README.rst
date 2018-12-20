================
Active Directory
================

Docker-dc is an implementation of Samba4 Active Domain Controller in Docker.

Prerequisites
-------------

.. code:: bash

  $ sudo apt-get install docker
  $ sudo usermod -a -G docker nandersson
  $ docker pull ubuntu:latest

Install
-------

.. code:: bash

  $ python3 -m venv .venv
  $ source .venv/bin/activate
  $ pip install -r requirements.txt
  $ python src/docker-dc.py
  $ pytest

Start Container
---------------

Start container and expose all ports locally

.. code:: bash

  $ docker run --privileged --name dc --rm -ti -e SAMBA_DOMAIN=openforce -e SAMBA_HOST_NAME=dc -e SAMBA_ADMINPASS=Abc123! -e SAMBA_KRBTGTPASS=Abc123! -e SAMBA_REALM=OPENFORCE.ORG -p 22:2222 -p 5353:53 -p 88:88 -p 135:135 -p 139:139 -p 389:389 -p 445:445 -p 464:464 -p 636:636 -p 1024:1024 -p 3268:3268 -p 3269:3269 xnandersson/samba-ad-dc dcpromo

Testing
-------

.. code:: bash

  $ echo TLS_REQCERT ALLOW >> ~/.ldaprc 
  $ ldapsearch  -H ldap://localhost:3268 -b 'cn=users,dc=openforce,dc=org' -x -D "Administrator@OPENFORCE.ORG"  -s sub -Z "(cn=*)" cn mail sn -w 'Abc123!'
  $ ldapsearch  -H ldap://localhost      -b 'cn=users,dc=openforce,dc=org' -x -D "Administrator@OPENFORCE.ORG"  -s sub -Z "(cn=*)" cn mail sn -w 'Abc123!'
  $ ldapsearch  -H ldap://localhost:3268 -b 'cn=users,dc=openforce,dc=org' -x -D "Administrator@OPENFORCE.ORG" -s sub -Z "(cn=*)" cn mail sn -w 'Abc123!'
  $ ldapsearch  -H ldaps://localhost:3269 -b 'dc=openforce,dc=org' -x -w 'Abc123!'  -D "OPENFORCE\Administrator" -s sub  '(sAMAccountName=nandersson)'
  $ ldapsearch  -H ldap://localhost:389 -b 'cn=users,dc=openforce,dc=org' -x -D "Administrator@OPENFORCE.ORG" -s sub -Z "(cn=*)" cn mail sn -w 'Abc123!'

Python HOWTO
------------

.. code:: python3

  import ldap

  con = ldap.initialize('ldaps://127.0.0.1')
  con.set_option(ldap.OPT_X_SASL_NOCANON, 1)
  con.set_option(ldap.OPT_REFERRALS, 0)
  con.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
  con.protocol_version = ldap.VERSION3
  con.simple_bind_s('Administrator@OPENFORCE.ORG', 'Abc123!')

  entries = con.search_s(
      base="dc=openforce,dc=org", 
      scope=ldap.SCOPE_SUBTREE, 
      filterstr='(objectClass=User)', 
      attrlist=('cn','displayName'))

  for entry in entries:
      print(entry)


Samba-tool
----------

.. code:: bash

  sudo samba-tool user list
  sudo samba-tool user setpassword Administrator
  samba-tool user setpassword nandersson
  sudo samba-tool dns query 192.168.1.10 1.168.192.in-addr.arpa 1.168.192.in-addr.arpa ALL -U Administrator --password='Abc123!'

DNS  
---

.. code:: bash

  samba-tool dns zonelist 192.168.1.10
  samba-tool dns zonelist 192.168.1.10  -U Administrator --password='Yb92!!Ha99'
  samba-tool dns zonecreate 192.168.1.10 1.168.192.in-addr.arpa
  samba-tool dns zonecreate 192.168.1.10 1.168.192.in-addr.arpa -U Administrator --password='Yb92!!Ha99'
  samba-tool dns add 192.168.1.10 1.168.192.in-addr.arpa 10 PTR dc.openforce.org -U Administrator --password='Yb92!!Ha99'
  samba-tool dns add 192.168.1.10 openforce.org kubernetes A 192.168.1.12 -U Administrator --password='Yb92!!Ha99'
  samba-tool dns add 192.168.1.10 1.168.192.in-addr.arpa 12 PTR kubernetes.openforce.org -U Administrator --password='Yb92!!Ha99'
  samba-tool dns add 192.168.1.10 openforce.org freeswitch A 192.168.1.14 -U Administrator --password='Yb92!!Ha99'
  samba-tool dns add 192.168.1.10 1.168.192.in-addr.arpa 14 PTR freeswitch.openforce.org -U Administrator --password='Yb92!!Ha99'
  samba-tool dns add 192.168.1.10 1.168.192.in-addr.arpa 15 PTR docker.openforce.org -U Administrator --password='Yb92!!Ha99'
  samba-tool dns add 192.168.1.10 openforce.org docker A 192.168.1.15 -U Administrator --password='Yb92!!Ha99'
  samba-tool dns add 192.168.1.10 openforce.org k8s CNAME kubernetes.openforce.org -U Administrator --password='Yb92!!Ha99'