import pytest
import ldap

def test_dc(active_directory):
    con = ldap.initialize('ldaps://127.0.0.1')
    con.set_option(ldap.OPT_X_SASL_NOCANON, 1)
    con.set_option(ldap.OPT_REFERRALS, 0)
    con.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
    con.protocol_version = ldap.VERSION3
    con.simple_bind_s('Administrator@OPENFORCE.ORG', 'Abc123!')
    dn = 'cn=Administrator,cn=Users,dc=openforce,dc=org'
    attr_name = 'cn'
    attr_val = 'Administrator'
    assert con.compare_s(dn, attr_name, attr_val) == True

def test_can_bind_as_administrator_at_realm(active_directory):
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

    assert entries.len == 15