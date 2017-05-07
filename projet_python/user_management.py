import libuser_manager
from random import choice
from hashlib import md5
from sys import argv
from getpass import getpass
import string
from sys import exit
import sqlite3

# Initialisation de la connexion à la BDD SQLITE
dbcon_cursor = libuser_manager.dbcon_initialize("myldap.sqlite3")
# Initialisation de la table "users"
libuser_manager.db_initialize("users", dbcon_cursor)

# Définition de la fonction


def interface():
    print("\n" * 80)
    print("""
    ##########################################################################
    ##  _____ ____   ____ ___           ______   _______ _   _  ___  _   _  ##
    ## | ____/ ___| / ___|_ _|         |  _ \ \ / /_   _| | | |/ _ \| \ | | ##
    ## |  _| \___ \| |  _ | |   _____  | |_) \ V /  | | | |_| | | | |  \| | ##
    ## | |___ ___) | |_| || |  |_____| |  __/ | |   | | |  _  | |_| | |\  | ##
    ## |_____|____/ \____|___|         |_|    |_|   |_| |_| |_|\___/|_| \_| ##
    ##                                                                      ##
    ##########################################################################
    2016/2017 3A-SRC : OLANGUENA Yann & MALEZIEUX Éric
    \n""")

# Déclaration de la variable boucle qui servira à imposer nos entrées
    boucle = True

# Début de la boucle / "boucle == True" superflu.
    while boucle:
        # Demande de saisie, 'eval' évalue la valeur retournée par 'input' comme une expression python
        # de telle manière qu'un string peut prendre un type spécifique en fonction de sa valeur
        try:
            # On explique ce qu'on attend de la personne qui lance le programme (les paramètres)
            print("""
            1. Ajout d'un utilisateur.\n
            2. Retrait d'un utilisateur.\n
            3. Mise à jour des informations d'un utilisateur.\n
            4. Test d'authentification d'un utilisateur.\n
            5. Sortie du programme.\n
            """)

            answer = eval(input("Que voulez-vous faire ?\n\n>>> "))
            # Ajout de l'utilisateur
            if answer == 1:
                print("Ajout utilisateur\n")
                libuser_manager.add_user(dbcon_cursor)
                print("\nOpération terminée.\n")
    # Suppression de l'utilisateur
            elif answer == 2:
                print("Suppression utilisateur\n")
                libuser_manager.delete_user(dbcon_cursor)
    # Modification de l'utilisateur
            elif answer == 3:
                print("Modification de l'utilisateur\n")
                libuser_manager.maj_user(dbcon_cursor)
            elif answer == 4:
                print("Test d'authentification")
                libuser_manager.user_login(dbcon_cursor)
    # Sortie du programme
            elif answer == 5:
                boucle=False
                print("\n\nFin du programme...\n")
                return 0
    # Redemande de saisir tant que ce n'est pas un de nos paramètre
        except EOFError:
            print("Saisie non reconnue !\nEntrez '5' pour sortir du programme.\n")
    # Attrape le signal "KeyboardInterrupt" qui permet de mettre fin arbitrairement à un programme
    # et nous permet de terminer ce dernier "gracieusement".
        except KeyboardInterrupt:
            boucle=False
            print("\n\nFin du programme...\n")
            return 1

# Lancement de l'interface
interface()

# Quand on sort du menu, nettoyer les connecteurs de BDD
print("Cleaning up DB connector... \n")
try:
    del dbcon_cursor
    print("Done.")
    exit(0)
except NameError:
    print("Couldn't properly close DB connector!")
    exit(1)