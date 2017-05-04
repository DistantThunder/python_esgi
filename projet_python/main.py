# -*- coding: utf-8 -*-

from ldap3 import Server, Connection, ALL

server = Server('192.168.122.82', use_ssl=False, get_info=ALL, connect_timeout=5)
conn = Connection(server)

try:
    with open('ldap.conf', 'r') as conf_file:
        conf_file.readline()

except OSError:
    print("Fichier non  trouvé.")

conn.bind()
print(conn)
print(server.info)

