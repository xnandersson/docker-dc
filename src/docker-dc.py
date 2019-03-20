#!/usr/bin/env python
import docker
import os
import uuid

BUILD_DIR = '/tmp/{uuid}/'.format(uuid=uuid.uuid4().hex)

def mkdir_build_dir():
  try:
    os.mkdir(BUILD_DIR)
  except FileExistsError as e:
    pass

def create_dcpromo_debconf():
  with open(os.path.join(BUILD_DIR, 'dcpromo'), 'w') as f:
    f.write("""#!/bin/bash
if [ ! -f /etc/krb5.conf ]; then
samba-tool domain provision \
  --domain=${SAMBA_DOMAIN} \
  --host-name=${SAMBA_HOST_NAME} \
  --adminpass=${SAMBA_ADMINPASS} \
  --krbtgtpass=${SAMBA_KRBTGTPASS} \
  --realm=${SAMBA_REALM}
cp /var/lib/samba/private/krb5.conf /etc/krb5.conf
samba-tool user create nandersson Secret012
fi
service samba-ad-dc start
/usr/sbin/sshd -D\n""")

def create_dcpromo_template():
  with open(os.path.join(BUILD_DIR, 'dcpromo.template'), 'w') as f:
    f.write("""#!/bin/bash
samba-tool domain provision \
  --domain=openforce \
  --host-name=DC \
  --adminpass=Abc123!! \
  --krbtgtpass=Abc123!! \
  --machinepass=Abc123!! \
  --dnspass=Abc123!! \
  --root=root \
  --nobody=nobody \
  --users=staff \
  --server-role=dc \
  --use-rfc2307 \
  --realm=OPENFORCE.ORG \
  --dns-backend=SAMBA_INTERNAL\n""")

def create_dockerfile():
  with open(os.path.join(BUILD_DIR, 'Dockerfile'), 'w') as f:
    f.write("""FROM ubuntu:bionic
MAINTAINER Niklas Andersson <niklas.andersson@openforce.se>
ENV UPDATED_ON 2018-10-02
RUN apt-get update -y
RUN apt-get install samba -y
RUN apt-get install rsyslog nmap smbclient -y
RUN apt-get install ssh -y
RUN rm /etc/samba/smb.conf
RUN apt-get install vim -y
ADD dcpromo.template /usr/local/bin/
ADD dcpromo /usr/local/bin/dcpromo
RUN chmod +x /usr/local/bin/dcpromo
RUN mkdir /run/sshd
EXPOSE 22 53 88 135 139 389 445 464 636 1024 3268 3269
CMD /bin/bash\n""")

if __name__ == '__main__':
  mkdir_build_dir()
  create_dcpromo_debconf()
  create_dcpromo_template()
  create_dockerfile()
  client = docker.DockerClient(base_url='unix://var/run/docker.sock')
  client.images.build(path=BUILD_DIR, tag='xnandersson/samba-ad-dc', rm=True, pull=True)
