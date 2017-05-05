import libuser_manager
from random import choice
from hashlib import md5
from sys import argv
from getpass import getpass
import string
from sys import exit
import sqlite3

# Initialisation de la connexion à la BDD SQLITE

db_object = sqlite3.connect("myldap.sqlite3")
dbcon_cursor = db_object.cursor()
libuser_manager.db_initialize("users")

# Définition de la fonction


def interface():

    # On explique ce qu'on attend de la personne qui lance le programme (les paramètres)
    print("""
    1. Ajout d'un utilisateur.\n
    2. Retrait d'un utilisateur.\n
    3. Mise à jour des informations d'un utilisateur.\n
    4. Test d'authentification d'un utilisateur.\n
    5. Sortie du programme.\n
    """)

# Déclaration de la variable boucle qui servira à imposer nos entrées
    boucle = True

# Début de la boucle / "boucle == True" superflu.
    while boucle:
        # Demande de saisie
        answer = eval(input("Que voulez-vous faire ?\n\n"))
        try:
            # Ajout de l'utilisateur
            if answer == 1:
                print("Ajout utilisateur\n")
                libuser_manager.add_user()
    # Suppression de l'utilisateur
            elif answer == 2:
                print("Suppression utilisateur\n")
                libuser_manager.delete_user()
    # Modification de l'utilisateur
            elif answer == 3:
                print("Modification de l'utilisateur\n")
                libuser_manager.maj_user()
            elif answer == 4:
                print("Test d'authentification")
                libuser_manager.user_login()
    # Sortie du programme
            elif answer == 5:
                boucle=False
                print("Sortie du programme\n")
                exit(0)
    # Redemande de saisir tant que ce n'est pas un de nos paramètre
        except EOFError:
            print("Saisie non reconnue !\n Entrez '5' pour sortir du programme.\n")

# Lancement de l'interface
interface()

