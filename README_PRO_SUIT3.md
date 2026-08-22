# PRO_SUIT3 - Suite Protocoles RPC, LDAP, Telnet

**Développé par Hacker Tchadien - HiddenWorld**

PRO_SUIT3 est une suite éducative avancée pour comprendre et tester en pratique les protocoles RPC, LDAP et Telnet sur vos propres systèmes.

## ⚠️ Avertissement

Usage strictement légal et éducatif. Testez uniquement sur vos propres machines ou avec autorisation écrite.

## Fonctionnalités

- Cours interactifs RPC, LDAP, Telnet
- Tests de connexion réels en socket
- Scan des ports associés
- Client Telnet interactif
- Requête LDAP BindRequest
- Requête RPC Endpoint Mapper

## Installation

```bash
pip install -r requirements_PRO_SUIT3.txt
python3 PRO_SUIT3.py
```

## Commandes de lancement

### Mode menu interactif
```bash
python3 PRO_SUIT3.py
```

### Test RPC
```bash
python3 PRO_SUIT3.py -t 192.168.1.1 --rpc
```

### Test LDAP
```bash
python3 PRO_SUIT3.py -t 192.168.1.1 --ldap -u "cn=admin,dc=example,dc=com" -P password
```

### Test Telnet
```bash
python3 PRO_SUIT3.py -t 192.168.1.1 --telnet -p 23
```

### Test complet
```bash
python3 PRO_SUIT3.py -t 192.168.1.1 --rpc --ldap --telnet
```

## Licence

MIT - Usage éducatif uniquement
