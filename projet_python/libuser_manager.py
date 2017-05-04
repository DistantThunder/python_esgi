from random import choice
from hashlib import md5, sha384
from sys import argv
from getpass import getpass
import string
import sqlite3


##### VARIABLES
# Arguments en ligne de commande
script = argv
# Définition de l'espace de caractères pour nos mots de passe
char_space = string.ascii_letters+string.digits

# Affichage dudit espace sur la sortie standard
# print("Caractères utilisés : ", char_space,"\n")

# Connection à la base de données SQLITE3
# Créée automatiquement si elle n'existe pas et initi
db_object = sqlite3.connect("myldap.sqlite3")
dbcon_cursor = db_object.cursor()


#############################################################################>>>>>>>>>>>>>>>>> FONCTIONS
# Initialise la base de données si besoin
def db_initialize(tableName):
    # REQUÊTES SQLITE EFFECTUÉES AVEC SUBSTITUTION '?' AFIN DE MINIMISER RISQUES INJECTION SQL
    dbcon_cursor.execute("SELECT 1 FROM sqlite_master WHERE type = ? AND name = ?", ["table", tableName])
    qResult = dbcon_cursor.fetchone()
    # L'EVALUATION RENVOIE 'False' SI qResult N'A AUCUN TYPE (==VIDE). DONC :
    # SI qResult *- A UN TYPE -* ET DONC *-N'EST PAS VIDE-*, LA REQUÊTE SQLite PRÉCÉDENTE
    # A RENVOYÉ UNE VALEUR -> LA TABLE A ÉTÉ TROUVÉE.
    if qResult:
        print("Checking DATABASE...\nSQLite table ' {:s} ' exists! Proceeding...\n".format(tableName))
        return 0
    else:
        print("Table ' {:s} ' does not exist! Creating it before continuing...\n".format(tableName))
        # NOTE : LES NOMS DE TABLES NE **PEUVENT PAS** ÊTRE PASSÉS EN SUBSTITUTION DE PARAMÈTRE '?'!!!!
        dbcon_cursor.execute("DROP TABLE IF EXISTS %s" % tableName)
        dbcon_cursor.execute("""CREATE TABLE %s (
                                uid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                username text,
                                password CHAR(32)
                                ) """ % tableName)
        print("Done!\n\n")
        return 0


# Fonction de génération de mot de passe aléatoire
def genpasswd():
    password = ""
# On va boucler sur le char_space pour obtenir un peu plus de randomness
# par multiple invocations de "choice".
    for i in range(8):
        password += choice(char_space)
    return password


# Fonction de hashage : prend en argument un mot de passe et génère une empreinte avec algo MD5
def hashing(input_password):
        md5hash = md5()
        md5hash.update(input_password.encode(encoding='ascii', errors='strict'))
        return md5hash.hexdigest()


def add_user():
    username = (input("Saisissez un nouvel utilisateur:\n>>> "))
    motpasse = genpasswd()
    pwHash = (hashing(motpasse))
    new_user = (username,pwHash)
    print("Utilisateur => ' {:s} '\nMot de passe => {:s} \nHash => {:s}".format(new_user[0], motpasse, new_user[1]))
    dbcon_cursor.execute("INSERT INTO users VALUES(null,?,?)", new_user)
    return 0


## Fonction "check_user" prend un nom d'utilisateur en argument et cherche dans la base de donnée utilisateurs.
## Si aucun paramètre fournit en entrée, demande input nom d'utilisateur
def check_user(user=""):
    # Un string vide renverra 'False', donc il vaut mieux inverser le test ici.
    if user == "":
        user = input("Which user are you looking for?\n>>> ")

    print("Checking user ' {:s} ' ...".format(user))
    dbcon_cursor.execute("SELECT uid,username FROM users WHERE username = ?", [user])
    return dbcon_cursor.fetchall()


def delete_user():
        user = input("Which user are you deleting? \n>>> ")
        qResult = check_user(user)
        if len(qResult) == 1:
            print("Un utilisateur a été trouvé.")
            print("Voulez-vous effacer l'utilisateur {:s} ? o/N".format(qResult[0][1]))
            answer = input(">>>")
            if answer == "O" or "o":
                print("ATTENTION! Cette opération est irréversible!!\nEntrez 'OK' en toutes lettres pour confirmer:\n")
                confirm = input(">>>")
                if confirm == "OK":
                    print("Retrait de {:s}...\n".format(qResult[0][1]))
                    dbcon_cursor.execute("DELETE FROM users WHERE uid = ? AND username = ?", [qResult[0][0], qResult[0][1]])
                    print("Effectué.\n")
                else:
                    print("Confirmation non reçue. Arrêt...\n")
                    exit(1)
            elif answer == "N" or "n":
                print("Il s'agit du seul utilisateur trouvé. Arrêt...\n")
                exit(0)
            else:
                print("Nous n'avons pas compris votre réponse. Arrêt...\n")
                exit(1)
        elif len(qResult) == 0:
            print("Aucun utilisateur avec ce nom trouvé!!\n")
            exit(0)
        else:
            print("Attention, plusieurs utilisateurs trouvés avec ce nom!\n")
            print("+------------------------------------------------------+")
            print("|           UID           |      Nom d'utilisateur     |")
            print("+------------------------------------------------------+")
            for i in qResult:
                print("|{:d}                        |{:s}                        |".format(i[0], i[1]))
            print("+------------------------------------------------------+")

            del_id = input("Entrez l'UID de l'utilisateur à supprimer:\n>>> ")
            print("Voulez-vous effacer l'utilisateur {:s} identifié par UID {:d} ?".format(qResult[0][1], del_id))
            answer = input(">>>")
            if answer == "O" or "o":
                print("ATTENTION ! Cette opération est irréversible!!\nEntrez 'OK' en toutes lettres pour confirmer:\n")
                confirm = input(">>>")
                if confirm == "OK":
                    print("Deleting {:s}...\n".format(qResult[0][1]))
                    dbcon_cursor.execute("DELETE FROM users WHERE uid = ? AND username = ?", [qResult[0][0], qResult[0][1]])
                else:
                    print("Confirmation non reçue. Arrêt...\n")
                    exit(1)
            elif answer == "N" or "n":
                print("Il s'agit du seul utilisateur trouvé. Arrêt...\n")
                exit(0)
            else:
                print("Nous n'avons pas compris votre réponse. Arrêt...\n")
                exit(1)
        print("Done !\n")


def maj_user():
    print("Mise à jour du mot de passe.\n")
    userToUpd = input("Entrez le nom de l'utilisateur dont vous souhaitez modifier le mot de passe :\n>>>")
    qResult = check_user(userToUpd)
    if len(qResult) == 1:
            print("Un utilisateur a été trouvé.")
            print("Voulez-vous mettre à jour le mot de passe de {:s} ? o/N".format(qResult[0][1]))
            answer = input(">>>")
            if answer == "O" or "o":
                print("ATTENTION! Cette opération est irréversible!!\nEntrez 'OK' en toutes lettres pour confirmer:\n")
                confirm = input(">>>")
                if confirm == "OK":
                    newpassword = getpass("Entrez le nouveau mot de passe:\n>>>")
                    dbcon_cursor.execute("UPDATE users SET password = ? WHERE uid = ?", [hashing(newpassword), qResult[0][0]])
                    print("Mot de passe modifié pour {:s}".format(qResult[0][1]))
                else:
                    print("Confirmation non reçue. Arrêt...\n")
                    exit(1)
            elif answer == "N" or "n":
                print("Il s'agit du seul utilisateur trouvé. Abandon...\n")
                exit(0)
            else:
                print("Nous n'avons pas compris votre réponse. Abandon...\n")
                exit(1)
    elif len(qResult) == 0:
            print("Aucun utilisateur avec ce nom trouvé!!\n")
            exit(0)
    else:
            print("Attention, plusieurs utilisateurs trouvés avec ce nom!\n")
            print("+------------------------------------------------------+")
            print("|           UID           |      Nom d'utilisateur     |")
            print("+------------------------------------------------------+")
            for i in qResult:
                print("|{:d}                        |{:s}                         |".format(i[0], i[1]))
            print("+------------------------------------------------------+")

            maj_id = input("Entrez l'UID de l'utilisateur dont le mot de passe sera mis à jour:\n>>> ")
            print("Voulez-vous mettre à jour le mot de passe de ' {:s} ' identifié par ' UID {:d} ' ? o/N".format(qResult[0][1], int(maj_id)))
            answer = input(">>>")
            if answer == "O" or "o":
                print("ATTENTION ! Cette opération est irréversible!!\nEntrez 'OK' en toutes lettres pour confirmer:\n")
                confirm = input(">>>")
                if confirm == "OK":
                    newpassword = getpass("Entrez le nouveau mot de passe:\n>>>")
                    dbcon_cursor.execute("UPDATE users SET password = ? WHERE uid = ?", ([hashing(newpassword), int(maj_id)]))
                    print("Mot de passe modifié pour {:s}".format(qResult[0][1]))
                else:
                    print("Confirmation non reçue. Abandon...\n")
                    exit(1)
            elif answer == "N" or "n":
                print("No Arrêt...\n")
                exit(0)
            else:
                print("Nous n'avons pas compris votre réponse. Arrêt...\n")
                exit(1)


def user_login():
    loguser = input("Nom d'utilisateur : \n>>>")
    logpass = getpass("Mot de passe: \n>>>")
    qResult = check_user(loguser)
    if len(qResult) >= 1:
        dbcon_cursor.execute("SELECT * from users WHERE username = ? AND password = ?", [loguser, hashing(logpass)])
        auth_response = dbcon_cursor.fetchall()
        if len(auth_response) >= 1:
            print("Bravo, vous êtes authentifié!")
            exit(0)
        else:
            print("Mot de passe erroné pour cet utilisateur.\n")
            exit(1)
    else:
        print("Utilisateur non-existant.\n")
        exit(1)




#####################################################>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> EXÉCUTION

####### ACCESS CONTROL #######
# adminPw = "b604f00b579a3011b3778c07747664f1334dcad66daa4b8c6cd07021cbda2ad10a81047a387d4a79999c10f188a5e103"
# inputPw = getpass("Entrez le mot de passe administrateur:\n>>>")
# admin = 0
#
#
# if sha384(inputPw.encode()).hexdigest() == adminPw:
#     admin = 1
#     print("Vous êtes authentifié!\n")
# else:
#     admin = 0
#     print("Échec authentification")
#     exit(1)
#
db_initialize("users")
#
# ### SEUL L'ADMIN PEUT SUPPRIMER DES UTILISATEURS ARBITRAIREMENT
# if admin == 1:
#     add_user()
#     delete_user()
# else:
#     print("Your are not admin!!\nExiting...")
#     exit(1)


#Définition de la fonction d'interface principale
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

#On explique ce qu'on attend de la personne qui lance le programme (les paramètres)
    print("Saisissez 'add' pour ajouter un utilisateur.\nSaisissez 'delete' pour effacer un utilisateur.\nSaisissez 'modify' pour mettre à jour un utilisateur.\nSaisissez 'login' pour vous connecter.\nSaisissez 'exit' pour sortir du programme.\n")

#Déclaration de la variable boucle qui servira à imposer nos entrées
    boucle = True

#Début de la boucle
    while boucle==True:
#demande de saisie
        answer=input("Que voulez vous faire ?\n\n")

#Ajout de l'utilisateur
        if answer=="add":
            print("Ajout utilisateur\n")
            add_user()
# ENREGISTREMENT DES CHANGEMENTS SUR LA BDD "PHYSIQUE"
            db_object.commit()
#Suppression de l'utilisateur
        elif answer=="delete":
            print("Suppression utilisateur\n")
            delete_user()
# ENREGISTREMENT DES CHANGEMENTS SUR LA BDD "PHYSIQUE"
            db_object.commit()
#Modification de l'utilisateur
        elif answer=="modify":
            print("Modification de l'utilisateur\n")
            maj_user()
# ENREGISTREMENT DES CHANGEMENTS SUR LA BDD "PHYSIQUE"
            db_object.commit()
        elif answer=="login":
            print("Test d'authentification")
            user_login()
#Sortie du programme
        elif answer=="exit":
            boucle=False
            print("Sortie du programme\n")
#Redemande de saisir tant que ce n'est pas un de nos paramètres
        else:
            print("Saisie non reconnue\n")

interface()



# Fermeture de la connexion à la BDD
db_object.close()

del dbcon_cursor
del db_object
