"""Módulo de funções relacionadas ao LDAP"""

from flask import current_app
from ldap3 import Server, Connection, MOCK_SYNC, ALL

def checa_ldap(login, senha):
    url_ldap = current_app.config["LDAP_URL"]
    port_ldap = current_app.config["LDAP_PORT"]
    mascara_ldap = current_app.config["LDAP_QUERY"]
    mascara = mascara_ldap.format(login)


    if current_app.config['INIT_LDAP_TEST']:
            entries = []
            assert isinstance(current_app.config["LDAP_TEST_PASS"],str)
            for user in current_app.config['LDAP_TEST_USERS']:
                entries.append({
                    'dn': f'uid={user},ou=users,dc=ufabc,dc=edu,dc=br',
                    'objectclass': ['user'],
                    'attributes': {'userPassword': current_app.config["LDAP_TEST_PASS"]},
                    })

            server = Server('localhost', port=8389)
            connection = Connection(server, user=mascara, password=senha, client_strategy=MOCK_SYNC)

            for ent in entries:
                connection.strategy.add_entry(ent['dn'], attributes=ent['attributes'])
    else:
        server = Server(url_ldap, port=port_ldap, get_info=ALL)
        connection = Connection(server, user=mascara, password=senha)

    return connection.bind()