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

Howto
-----

.. code:: bash

  $ python3 -m venv .venv
  $ source .venv/bin/activate
  $ pip install -r requirements.txt
  $ python src/docker-dc.py
  $ pytest
