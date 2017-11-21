import os

LDAP_BIND_DN = os.getenv("LDAP_BIND_DN", default="cn=whoistheprimaryowen,ou=Apps,dc=csh,dc=rit,dc=edu")
LDAP_BIND_PW = os.getenv("LDAP_BIND_PW", default=None)

PLUG_SUPPORT = os.environ.get('PLUG_ENABLED', 'False')
