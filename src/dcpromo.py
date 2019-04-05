#!/usr/bin/env python3
import os
import subprocess

SAMBA_DOMAIN = os.getenv('SAMBA_DOMAIN', 'acme')
SAMBA_HOST_NAME = os.getenv('SAMBA_HOST_NAME', 'dc')
SAMBA_ADMINPASS = os.getenv('SAMBA_ADMINPASS', 'Abc123')
SAMBA_KRBTGTPASS = os.getenv('SAMBA_KRBTGTPASS', SAMBA_ADMINPASS)
SAMBA_REALM = os.getenv('SAMBA_REALM', 'ACME.ORG')

def promote(samba_domain=None, samba_host_name=None, samba_adminpass=None, samba_krbtgtpass=None, samba_realm=None): 
    proc = subprocess.Popen([
        'samba-tool', 'domain', 'provision', 
        '--domain', samba_domain, 
        '--host-name', samba_host_name,
        '--adminpass', samba_adminpass,
        '--krbtgtpass', samba_krbtgtpass,
        '--realm', samba_realm])
    proc.wait()
    proc = subprocess.Popen(['cp', '/var/lib/samba/private/krb5.conf', '/etc/krb5.conf'])
    proc.wait()

def service_start(service):
    proc = subprocess.Popen(['service', service, 'start'])
    rc = proc.wait()
    return True if rc == 0 else False

def sshd():
    proc = subprocess.Popen(['/usr/sbin/sshd', '-D'])
    proc.wait()

if __name__ == '__main__':
    if not os.path.isfile('/etc/krb5.conf'):
        promote(samba_domain=SAMBA_DOMAIN, samba_host_name=SAMBA_HOST_NAME, samba_adminpass=SAMBA_ADMINPASS, samba_krbtgtpass=SAMBA_KRBTGTPASS, samba_realm=SAMBA_REALM)
    service_start('samba-ad-dc')
    sshd()
