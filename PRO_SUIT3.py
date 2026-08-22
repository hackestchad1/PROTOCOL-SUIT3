#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRO_SUIT3 - Suite Protocoles RPC, LDAP, Telnet
Développé par Hacker Tchadien - HiddenWorld
Usage éducatif et tests sur vos propres systèmes uniquement
"""

import os
import sys
import json
import time
import socket
import struct
import getpass
import argparse
import subprocess
from datetime import datetime

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    class FakeFore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = ""
    class FakeStyle:
        BRIGHT = DIM = RESET_ALL = ""
    Fore = FakeFore()
    Style = FakeStyle()

class Colors:
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    BOLD = Style.BRIGHT
    DIM = Style.DIM
    RESET = Style.RESET_ALL

def clear():
    os.system('clear' if os.name != 'nt' else 'cls')

def banner():
    print(f"""
{Colors.CYAN}{Colors.BOLD}
   ██████╗ ██████╗  ██████╗      ███████╗██╗   ██╗██╗████████╗██████╗ 
   ██╔══██╗██╔══██╗██╔═══██╗     ██╔════╝██║   ██║██║╚══██╔══╝╚════██╗
   ██████╔╝██████╔╝██║   ██║     ███████╗██║   ██║██║   ██║    ▄███╔╝
   ██╔═══╝ ██╔══██╗██║   ██║     ╚════██║██║   ██║██║   ██║    ▀▀══╝ 
   ██║     ██║  ██║╚██████╔╝     ███████║╚██████╔╝██║   ██║    ██╗   
   ╚═╝     ╚═╝  ╚═╝ ╚═════╝      ╚══════╝ ╚═════╝ ╚═╝   ╚═╝    ╚═╝   
{Colors.RESET}
{Colors.GREEN}{Colors.BOLD}        PRO_SUIT3 - RPC | LDAP | Telnet{Colors.RESET}
{Colors.YELLOW}        Développé par Hacker Tchadien - HiddenWorld{Colors.RESET}
    """)

def log(msg, level="INFO"):
    colors = {
        "INFO": Colors.CYAN,
        "OK": Colors.GREEN,
        "WARN": Colors.YELLOW,
        "ERROR": Colors.RED,
        "RPC": Colors.MAGENTA,
        "LDAP": Colors.BLUE,
        "TELNET": Colors.YELLOW
    }
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Colors.DIM}[{timestamp}]{Colors.RESET} {colors.get(level, Colors.WHITE)}[{level}]{Colors.RESET} {msg}")

class RPCProtocol:
    """Implémentation éducative du protocole RPC (Remote Procedure Call)"""
    
    PORT = 135
    KNOWN_UUIDS = {
        "e1af8308-5d1f-11c9-91a4-08002b14a0fa": "MS Exchange Directory",
        "12345678-1234-ABCD-EF00-0123456789AB": "LSA (Local Security Authority)",
        "00000000-0000-0000-0000-000000000000": "Test UUID"
    }
    
    def __init__(self, target, port=135):
        self.target = target
        self.port = port
        self.sock = None
    
    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5)
            self.sock.connect((self.target, self.port))
            log(f"Connecté à {self.target}:{self.port} (RPC Endpoint Mapper)", "RPC")
            return True
        except Exception as e:
            log(f"Erreur connexion RPC: {e}", "ERROR")
            return False
    
    def send_epm_request(self):
        """Envoie une requête RPC Endpoint Mapper basique"""
        try:
            # Requête RPC BIND minimale pour éducation
            bind_request = bytes([
                0x05, 0x00, 0x0b, 0x03, 0x10, 0x00, 0x00, 0x00,
                0x48, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00,
                0xb8, 0x10, 0xb8, 0x10, 0x00, 0x00, 0x00, 0x00,
                0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
            ])
            self.sock.send(bind_request)
            response = self.sock.recv(1024)
            log(f"Réponse reçue ({len(response)} octets)", "RPC")
            self.parse_rpc_response(response)
            return response
        except Exception as e:
            log(f"Erreur requête RPC: {e}", "ERROR")
            return None
    
    def parse_rpc_response(self, data):
        if len(data) < 16:
            log("Réponse trop courte", "WARN")
            return
        version_major = data[0]
        version_minor = data[1]
        packet_type = data[2]
        packet_flags = data[3]
        log(f"Version RPC: {version_major}.{version_minor}", "RPC")
        log(f"Type de paquet: {packet_type} | Flags: {packet_flags}", "RPC")
    
    def scan_ports(self):
        """Scanne les ports RPC courants"""
        rpc_ports = [135, 593, 445, 139, 1025, 1026, 1027]
        found = []
        for port in rpc_ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                result = s.connect_ex((self.target, port))
                if result == 0:
                    found.append(port)
                    log(f"Port {port} ouvert", "OK")
                s.close()
            except:
                pass
        return found
    
    def disconnect(self):
        if self.sock:
            self.sock.close()


class LDAPProtocol:
    """Implémentation éducative du protocole LDAP"""
    
    PORT = 389
    SSL_PORT = 636
    
    def __init__(self, server, port=389, use_ssl=False):
        self.server = server
        self.port = port
        self.use_ssl = use_ssl
        self.sock = None
    
    def build_bind_request(self, username, password):
        """Construit une requête LDAP BindRequest simple"""
        version = bytes([0x02, 0x01, 0x03])  # INTEGER 3
        dn = self.ldap_string(username)
        auth = bytes([0x80]) + self.ber_length(len(password.encode())) + password.encode()
        bind_request = bytes([0x60]) + self.ber_length(len(version) + len(dn) + len(auth)) + version + dn + auth
        message_id = bytes([0x02, 0x01, 0x01])  # INTEGER 1
        message = bytes([0x30]) + self.ber_length(len(message_id) + len(bind_request)) + message_id + bind_request
        return message
    
    def ldap_string(self, s):
        data = s.encode('utf-8')
        return bytes([0x04]) + self.ber_length(len(data)) + data
    
    def ber_length(self, length):
        if length < 128:
            return bytes([length])
        else:
            encoded = length.to_bytes((length.bit_length() + 7) // 8, 'big')
            return bytes([0x80 | len(encoded)]) + encoded
    
    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5)
            self.sock.connect((self.server, self.port))
            log(f"Connecté à {self.server}:{self.port} (LDAP)", "LDAP")
            return True
        except Exception as e:
            log(f"Erreur connexion LDAP: {e}", "ERROR")
            return False
    
    def bind(self, username, password):
        try:
            request = self.build_bind_request(username, password)
            self.sock.send(request)
            response = self.sock.recv(1024)
            log(f"Réponse bind reçue ({len(response)} octets)", "LDAP")
            self.parse_ldap_response(response)
            return response
        except Exception as e:
            log(f"Erreur bind LDAP: {e}", "ERROR")
            return None
    
    def parse_ldap_response(self, data):
        if len(data) < 5:
            return
        try:
            result_code = data[-7] if len(data) > 7 else data[-1]
            codes = {0: "success", 1: "operationsError", 2: "protocolError", 49: "invalidCredentials"}
            log(f"Code résultat LDAP: {result_code} ({codes.get(result_code, 'unknown')})", "LDAP")
        except Exception as e:
            log(f"Erreur parsing: {e}", "ERROR")
    
    def search(self, base_dn, filter_str="(objectClass=*)"):
        """Construit une SearchRequest LDAP basique"""
        log(f"Préparation de la recherche LDAP sur {base_dn}", "LDAP")
        log("Utilisez un vrai client LDAP comme ldapsearch pour des recherches complètes", "WARN")
    
    def disconnect(self):
        if self.sock:
            self.sock.close()


class TelnetProtocol:
    """Implémentation éducative du protocole Telnet"""
    
    PORT = 23
    
    def __init__(self, target, port=23):
        self.target = target
        self.port = port
        self.sock = None
    
    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5)
            self.sock.connect((self.target, self.port))
            log(f"Connecté à {self.target}:{self.port} (Telnet)", "TELNET")
            return True
        except Exception as e:
            log(f"Erreur connexion Telnet: {e}", "ERROR")
            return False
    
    def send_command(self, command, wait=1):
        try:
            self.sock.send((command + "\n").encode())
            time.sleep(wait)
            response = self.sock.recv(4096)
            log(f"Réponse ({len(response)} octets):", "TELNET")
            print(response.decode('utf-8', errors='ignore')[:1000])
            return response
        except Exception as e:
            log(f"Erreur envoi commande: {e}", "ERROR")
            return None
    
    def negotiate(self):
        """Affiche le banner Telnet initial"""
        try:
            time.sleep(1)
            data = self.sock.recv(4096)
            log("Banner Telnet reçu:", "TELNET")
            print(data.decode('utf-8', errors='ignore')[:1000])
        except:
            pass
    
    def interactive_shell(self):
        log("Mode interactif Telnet (taper 'exit' pour quitter)", "TELNET")
        try:
            while True:
                command = input(f"{Colors.YELLOW}telnet>{Colors.RESET} ").strip()
                if command.lower() in ['exit', 'quit']:
                    break
                if command:
                    self.send_command(command)
        except KeyboardInterrupt:
            log("Interrompu", "WARN")
    
    def disconnect(self):
        if self.sock:
            self.sock.close()


def show_rpc_lesson():
    print(f"\n{Colors.CYAN}{Colors.BOLD}═══ COURS RPC (Remote Procedure Call) ═══{Colors.RESET}")
    print("""
RPC permet à un programme d'exécuter du code sur une machine distante.

Commandes clés:
- Port par défaut: 135 (Endpoint Mapper)
- Ports dynamiques: 1025-5000
- Outils réels: rpcclient, rpcdump, impacket-rpcdump

Exemples de commandes Linux:
  rpcclient -U "" <target>
  impacket-rpcdump <target>
  nmap -p 135,445 --script=msrpc-enum <target>

Dans ce script:
  PRO_SUIT3.py --target 192.168.1.1 --rpc
""")

def show_ldap_lesson():
    print(f"\n{Colors.BLUE}{Colors.BOLD}═══ COURS LDAP (Lightweight Directory Access Protocol) ═══{Colors.RESET}")
    print("""
LDAP sert à accéder et gérer les annuaires (Active Directory, OpenLDAP).

Commandes clés:
- Port par défaut: 389 (LDAP), 636 (LDAPS)
- Base DN: dc=example,dc=com
- Outils réels: ldapsearch, enum4linux, bloodhound-python

Exemples de commandes Linux:
  ldapsearch -x -H ldap://<server> -b "dc=example,dc=com"
  ldapsearch -x -D "cn=admin,dc=example,dc=com" -w password -b "dc=example,dc=com"

Dans ce script:
  PRO_SUIT3.py --target 192.168.1.1 --ldap --user admin --password pass
""")

def show_telnet_lesson():
    print(f"\n{Colors.YELLOW}{Colors.BOLD}═══ COURS Telnet ═══{Colors.RESET}")
    print("""
Telnet est un protocole de terminal distant en clair (non sécurisé).

Commandes clés:
- Port par défaut: 23
- Remplacé par SSH pour la sécurité
- Tout transmis en clair (capturable avec Wireshark)

Exemples de commandes Linux:
  telnet <target> 23
  nc <target> 23

Dans ce script:
  PRO_SUIT3.py --target 192.168.1.1 --telnet
""")


def interactive_menu():
    clear()
    banner()
    while True:
        print(f"\n{Colors.CYAN}{Colors.BOLD}╔═══════════════════ MENU PRO_SUIT3 ═══════════════════╗{Colors.RESET}")
        print(f"{Colors.CYAN}║{Colors.RESET}  [1] Cours RPC                                        {Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.CYAN}║{Colors.RESET}  [2] Cours LDAP                                       {Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.CYAN}║{Colors.RESET}  [3] Cours Telnet                                     {Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.CYAN}║{Colors.RESET}  [4] Tester RPC sur une cible                         {Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.CYAN}║{Colors.RESET}  [5] Tester LDAP sur une cible                        {Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.CYAN}║{Colors.RESET}  [6] Tester Telnet sur une cible                      {Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.CYAN}║{Colors.RESET}  [7] Tous les protocoles sur une cible                {Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.CYAN}║{Colors.RESET}  [8] Quitter                                          {Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}╚═══════════════════════════════════════════════════════╝{Colors.RESET}")

        choice = input(f"\n{Colors.YELLOW}[?] Choix: {Colors.RESET}").strip()

        if choice in ['1', '2', '3']:
            target = input("Adresse cible [localhost]: ").strip() or "127.0.0.1"
            if choice == '1':
                show_rpc_lesson()
                rpc = RPCProtocol(target)
                rpc.scan_ports()
                if rpc.connect():
                    rpc.send_epm_request()
                    rpc.disconnect()
            elif choice == '2':
                show_ldap_lesson()
                ldap = LDAPProtocol(target)
                if ldap.connect():
                    user = input("Utilisateur LDAP (DN complet ou simple): ").strip()
                    pwd = getpass.getpass("Mot de passe: ").strip()
                    if user and pwd:
                        ldap.bind(user, pwd)
                    ldap.disconnect()
            elif choice == '3':
                show_telnet_lesson()
                telnet = TelnetProtocol(target)
                if telnet.connect():
                    telnet.negotiate()
                    telnet.interactive_shell()
                    telnet.disconnect()

        elif choice == '4':
            target = input("Adresse cible RPC: ").strip()
            rpc = RPCProtocol(target)
            rpc.scan_ports()
            if rpc.connect():
                rpc.send_epm_request()
                rpc.disconnect()

        elif choice == '5':
            target = input("Adresse cible LDAP: ").strip()
            port = int(input("Port [389]: ").strip() or "389")
            use_ssl = input("Utiliser SSL? [o/N]: ").strip().lower() == 'o'
            ldap = LDAPProtocol(target, port=port, use_ssl=use_ssl)
            if ldap.connect():
                user = input("Utilisateur: ").strip()
                pwd = getpass.getpass("Mot de passe: ").strip()
                if user and pwd:
                    ldap.bind(user, pwd)
                ldap.disconnect()

        elif choice == '6':
            target = input("Adresse cible Telnet: ").strip()
            port = int(input("Port [23]: ").strip() or "23")
            telnet = TelnetProtocol(target, port=port)
            if telnet.connect():
                telnet.negotiate()
                telnet.interactive_shell()
                telnet.disconnect()

        elif choice == '7':
            target = input("Adresse cible: ").strip()
            log(f"Test complet sur {target}", "INFO")
            rpc = RPCProtocol(target)
            rpc.scan_ports()
            if rpc.connect():
                rpc.send_epm_request()
                rpc.disconnect()
            ldap = LDAPProtocol(target)
            if ldap.connect():
                log("Port LDAP 389 ouvert", "OK")
                ldap.disconnect()
            telnet = TelnetProtocol(target)
            if telnet.connect():
                telnet.negotiate()
                telnet.disconnect()

        elif choice == '8':
            log("Au revoir.", "INFO")
            break
        else:
            log("Choix invalide", "WARN")

        input(f"\n{Colors.DIM}[Appuyez sur Entrée]{Colors.RESET}")
        clear()
        banner()


def main():
    parser = argparse.ArgumentParser(description="PRO_SUIT3 - Suite RPC LDAP Telnet")
    parser.add_argument("--target", "-t", help="Adresse cible")
    parser.add_argument("--rpc", action="store_true", help="Tester RPC")
    parser.add_argument("--ldap", action="store_true", help="Tester LDAP")
    parser.add_argument("--telnet", action="store_true", help="Tester Telnet")
    parser.add_argument("--port", "-p", type=int, help="Port personnalisé")
    parser.add_argument("--user", "-u", help="Utilisateur LDAP")
    parser.add_argument("--password", "-P", help="Mot de passe LDAP")
    args = parser.parse_args()

    if not args.target:
        interactive_menu()
        return

    if args.rpc:
        rpc = RPCProtocol(args.target, args.port or 135)
        rpc.scan_ports()
        if rpc.connect():
            rpc.send_epm_request()
            rpc.disconnect()

    if args.ldap:
        ldap = LDAPProtocol(args.target, args.port or 389)
        if ldap.connect():
            if args.user and args.password:
                ldap.bind(args.user, args.password)
            ldap.disconnect()

    if args.telnet:
        telnet = TelnetProtocol(args.target, args.port or 23)
        if telnet.connect():
            telnet.negotiate()
            if not args.rpc and not args.ldap:
                telnet.interactive_shell()
            telnet.disconnect()

    if not any([args.rpc, args.ldap, args.telnet]):
        interactive_menu()


if __name__ == "__main__":
    main()
