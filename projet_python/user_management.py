import libuser_manager
from random import choice
from hashlib import md5
from sys import argv
from getpass import getpass
import string
import sqlite3


db_object = sqlite3.connect("myldap.sqlite3")
dbcon_cursor = db_object.cursor()
libuser_manager.db_initialize("users")

#Définition de la fonction
def interface():

#On explique ce qu'on attend de la personne qui lance le programme (les paramètres)
    print("Saisissez add pour ajouter un utilisateur.\nSaisissez delete pour effacer un utilisateur.\nSaisissez modify pour mettre à jour un utilisateur.\nSaisissez exit pour sortir du programme.\n")


#Déclaration de la variable boucle qui servira à imposer nos entrées
    boucle = True

#Début de la boucle
    while boucle==True:

#demande de saisie
        answer=input("Que voulez vous faire ?\n\n")

#Ajout de l'utilisateur
        if answer=="add":
            print("Ajout utilisateur\n")
            libuser_manager.add_user()
#Suppression de l'utilisateur
        elif answer=="delete":
            print("Suppression utilisateur\n")
            libuser_manager.delete_user()
#Modification de l'utilisateur
        elif answer=="modify":
            print("Modification de l'utilisateur\n")
            libuser_manager.maj_user()
        elif answer=="login":
            print("Test d'authentification")
            libuser_manager.user_login()
#Sortie du programme
        elif answer=="exit":
            boucle=False
            print("Sortie du programme\n")
#Redemande de saisir tant que ce n'est pas un de nos paramètres
        else:
            print("Saisie non reconnue\n")

interface()

