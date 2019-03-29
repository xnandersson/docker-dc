import ldap

con = ldap.initialize('ldaps://127.0.0.1')
con.set_option(ldap.OPT_X_SASL_NOCANON, 1)
con.set_option(ldap.OPT_REFERRALS, 0)
con.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
con.protocol_version = ldap.VERSION3
#con.simple_bind_s('nandersson', 'Secret012')
#con.simple_bind_s('vandersson@OPENFORCE.ORG', 'Secret013')
con.simple_bind_s('cn=vandersson,cn=Users,dc=openforce,dc=org', 'Secret013')

entries = con.search_s(
  base="dc=openforce,dc=org",
  scope=ldap.SCOPE_SUBTREE,
  filterstr='(objectClass=User)',
  attrlist=('cn','displayName'))

for entry in entries:
  print(entry)
