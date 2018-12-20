import pytest
import ldap

def test_dc(active_directory):
    con = ldap.initialize('ldaps://127.0.0.1:389')
    con.simple_bind_s('Administrator@OPENFORCE.ORG', 'Abc123!!')
    assert con != None