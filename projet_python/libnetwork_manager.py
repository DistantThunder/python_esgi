# Définition d'un client réseau gérant en parallèle l'émission
# et la réception des messages (utilisation de 2 THREADS).

import socket
import threading
import time


HOST = '127.0.0.1'
PORT = 40017

# -----------------------------------------------------------------------


class ThreadReception(threading.Thread):
    """objet thread gérant la réception des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn           # réf. du socket de connexion

    def run(self):
        while 1:
            message_recu = self.connexion.recv(128)
            print(message_recu.decode())
            if message_recu == b'' or message_recu.upper() == b"FIN":
                break
        # Le thread <réception> se termine ici.
        # On force la fermeture du thread <émission> :

        print ("Client arrêté en réception. Connexion interrompue!")

        self.connexion.close()

# ------------------------------------------------------------------------


class ThreadEmission(threading.Thread):
    """objet thread gérant l'émission des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn           # réf. du socket de connexion

    def run(self):
        while 1:
            time.sleep(0.5)
            message_emis = input("saisir un msg :")
            self.connexion.send(message_emis.encode())
            if message_emis.upper() == "FIN":
                break

        print("Client arrêté en émission. Connexion interrompue.")
        self.connexion.close()

# ------------------------------------------------------------------------


# v Renommé pour contraindre à la norme de nommage des classes "CamelCase"


class ThreadEmissionAdmin(threading.Thread):
    """objet thread gérant l'émission des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn           # réf. du socket de connexion

    def run(self):
        while 1:
            time.sleep(0.5)
            message_emis = input(menu())
            self.connexion.send(message_emis.encode())
            if message_emis.upper()=="7":
                break

        print("Client arrêté en émission. Connexion interrompue.")
        self.connexion.close()

# ------------------------------------------------------------------------
