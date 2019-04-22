=========================================
Samba4 Active Directory Domain Controller
=========================================

Abstract
--------

Docker Image, preloaded with Samba4 and a dcpromo-script
that promotes the container on startup using the supplied variables.


Build
-----

.. code:: bash
  
  $ sudo docker build -t xnandersson/dc .


Run
---

.. code:: bash

  $ sudo docker run \
      --privileged \
      --name dc \
      --rm \
      -d \
      -e SAMBA_DOMAIN=openforce \
      -e SAMBA_HOST_NAME=dc \
      -e SAMBA_ADMINPASS=Abc123! \
      -e SAMBA_KRBTGTPASS=Abc123! \
      -e SAMBA_REALM=OPENFORCE.ORG \
      -p 2222:22 -p 5353:53 -p 88:88 \
      -p 135:135 -p 139:139 -p 389:389 \
      -p 445:445 -p 464:464 -p 636:636 \
      -p 1024:1024 -p 3268:3268 -p 3269:3269 \
      xnandersson/dc /usr/local/bin/dcpromo.py


Administer
----------

.. code:: bash

  $ sudo docker exec -ti dc /bin/bash
  # samba-tool user create nandersson Secret012
  # samba-tool user setpassword Administrator
  # samba-tool user setpassword nandersson
  # samba-tool user list
  # samba-tool group add Staff
  # samba-tool group add Superusers
  # samba-tool group addmembers Staff nandersson
  # samba-tool group addmembers Superusers nandersson


Package Dependencies
--------------------

.. code:: bash

  $ sudo apt-get install docker.io devscripts python3-dev libldap2-dev libsasl2-dev python3-venv ldap-utils -y
  $ sudo docker pull ubuntu:latest
  $ sudo usermod -a -G docker ${USER} 
  $ su - ${USER}
  

Pytest
------

.. code:: bash

  $ python3 -m venv ~/venv3/docker-dc
  $ source ~/venv3/docker-dc/bin/activate
  $ pip install -U pip
  $ pip install -r requirements.txt
  $ echo TLS_REQCERT ALLOW >> ~/.ldaprc
  $ pytest
  

Python Example 
--------------

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
    

LDAP Search Example
-------------------

.. code:: bash
 
  $ ldapsearch  -H ldap://localhost:3268 -b 'cn=users,dc=openforce,dc=org' -x -D "Administrator@OPENFORCE.ORG"  -s sub -Z "(cn=*)" cn mail sn -w 'Abc123!'
  $ ldapsearch  -H ldap://localhost      -b 'cn=users,dc=openforce,dc=org' -x -D "Administrator@OPENFORCE.ORG"  -s sub -Z "(cn=*)" cn mail sn -w 'Abc123!'
  $ ldapsearch  -H ldap://localhost:3268 -b 'cn=users,dc=openforce,dc=org' -x -D "Administrator@OPENFORCE.ORG" -s sub -Z "(cn=*)" cn mail sn -w 'Abc123!'
  $ ldapsearch  -H ldaps://localhost:3269 -b 'dc=openforce,dc=org' -x -w 'Abc123!'  -D "OPENFORCE\Administrator" -s sub  '(sAMAccountName=nandersson)'
  $ ldapsearch  -H ldap://localhost:389 -b 'cn=users,dc=openforce,dc=org' -x -D "Administrator@OPENFORCE.ORG" -s sub -Z "(cn=*)" cn mail sn -w 'Abc123!'

DNS Example  
-----------

.. code:: bash

  $ samba-tool dns zonelist 192.168.1.10
  $ samba-tool dns zonelist 192.168.1.10  -U Administrator --password='Yb92!!Ha99'
  $ samba-tool dns zonecreate 192.168.1.10 1.168.192.in-addr.arpa
  $ samba-tool dns zonecreate 192.168.1.10 1.168.192.in-addr.arpa -U Administrator --password='Yb92!!Ha99'
  $ samba-tool dns add 192.168.1.10 1.168.192.in-addr.arpa 10 PTR dc.openforce.org -U Administrator --password='Yb92!!Ha99'
  $ samba-tool dns add 192.168.1.10 openforce.org kubernetes A 192.168.1.12 -U Administrator --password='Yb92!!Ha99'
  $ samba-tool dns add 192.168.1.10 1.168.192.in-addr.arpa 12 PTR kubernetes.openforce.org -U Administrator --password='Yb92!!Ha99'
  $ samba-tool dns add 192.168.1.10 openforce.org freeswitch A 192.168.1.14 -U Administrator --password='Yb92!!Ha99'
  $ samba-tool dns add 192.168.1.10 1.168.192.in-addr.arpa 14 PTR freeswitch.openforce.org -U Administrator --password='Yb92!!Ha99'
  $ samba-tool dns add 192.168.1.10 1.168.192.in-addr.arpa 15 PTR docker.openforce.org -U Administrator --password='Yb92!!Ha99'
  $ samba-tool dns add 192.168.1.10 openforce.org docker A 192.168.1.15 -U Administrator --password='Yb92!!Ha99'
  $ samba-tool dns add 192.168.1.10 openforce.org k8s CNAME kubernetes.openforce.org -U Administrator --password='Yb92!!Ha99'
  $ samba-tool dns query 192.168.1.10 1.168.192.in-addr.arpa 1.168.192.in-addr.arpa ALL -U Administrator --password='Abc123!'
