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

Python HOWTO
------------

.. code:: python3

  import ldap

  def test_active_directory(active_directory):
    con = ldap.initialize('http://127.0.0.1')
    assert con != None
