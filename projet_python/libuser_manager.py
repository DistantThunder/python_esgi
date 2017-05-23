from random import choice
from hashlib import md5, sha384
from sys import argv
from getpass import getpass
import string
import sqlite3


# #### VARIABLES
# Arguments en ligne de commande
script = argv
# Définition de l'espace de caractères pour nos mots de passe
char_space = string.ascii_letters+string.digits

# Affichage dudit espace sur la sortie standard
# print("Caractères utilisés : ", char_space,"\n")


# ############################################################################>>>>>>>>>>>>>>>>> FONCTIONS

# Initialise la CONNEXION à la base de données
def dbcon_initialize(dbfile):
    # Connection à la base de données SQLITE3
    # Créée automatiquement si elle n'existe pas et initialisée
    db_object = sqlite3.connect(dbfile)
    return db_object.cursor()


# Initialise la base de données si besoin
def db_initialize(table_name, dbcon_cursor):
    # REQUÊTES SQLITE EFFECTUÉES AVEC SUBSTITUTION '?' AFIN DE MINIMISER RISQUES INJECTION SQL
    dbcon_cursor.execute("SELECT 1 FROM sqlite_master WHERE type = ? AND name = ?", ["table", table_name])
    q_result = dbcon_cursor.fetchone()
    # L'EVALUATION RENVOIE 'False' SI q_result N'A AUCUN TYPE (==VIDE). DONC :
    # SI q_result *- A UN TYPE -* ET DONC *-N'EST PAS VIDE-*, LA REQUÊTE SQLite PRÉCÉDENTE
    # A RENVOYÉ UNE VALEUR -> LA TABLE A ÉTÉ TROUVÉE.
    if q_result:
        print("Checking DATABASE...\nSQLite table ' {:s} ' exists! Proceeding...\n".format(table_name))
        return 0
    else:
        print("Table ' {:s} ' does not exist! Creating it before continuing...\n".format(table_name))
        # NOTE : LES NOMS DE TABLES NE **PEUVENT PAS** ÊTRE PASSÉS EN SUBSTITUTION DE PARAMÈTRE '?'!!!!
        dbcon_cursor.execute("DROP TABLE IF EXISTS %s" % table_name)
        dbcon_cursor.execute("""CREATE TABLE %s (
                                uid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                username text,
                                password CHAR(32)
                                ) """ % table_name)
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


def add_user(dbcon_cursor):
    username = (input("Saisissez un nouvel utilisateur:\n>>> "))
    motpasse = genpasswd()
    pw_hash = (hashing(motpasse))
    new_user = (username, pw_hash)
    print("Utilisateur => ' {:s} '\nMot de passe => {:s} \nHash => {:s}".format(new_user[0], motpasse, new_user[1]))
    dbcon_cursor.execute("INSERT INTO users VALUES(null,?,?)", new_user)
    return 0


# Fonction "check_user" prend un nom d'utilisateur en argument et cherche dans la base de donnée utilisateurs.
# Si aucun paramètre fournit en entrée, demande input nom d'utilisateur
def check_user(dbcon_cursor, user=""):
    # Un string vide renverra 'False', donc il vaut mieux inverser le test ici.
    if user == "":
        user = input("Which user are you looking for?\n>>> ")

    print("Checking user ' {:s} ' ...".format(user))
    dbcon_cursor.execute("SELECT uid,username FROM users WHERE username = ?", [user])
    return dbcon_cursor.fetchall()


def delete_user(dbcon_cursor):
        user = input("Which user are you deleting? \n>>> ")
        q_result = check_user(dbcon_cursor, user)
        if len(q_result) == 1:
            print("Un utilisateur a été trouvé.")
            print("Voulez-vous effacer l'utilisateur {:s} ? o/N".format(q_result[0][1]))
            answer = input(">>> ")
            if answer in {'O', 'o'}:
                print("ATTENTION! Cette opération est irréversible!!\nEntrez 'OK' en toutes lettres pour confirmer:\n")
                confirm = input(">>> ")
                if confirm == "OK":
                    print("Retrait de {:s}...\n".format(q_result[0][1]))
                    dbcon_cursor.execute("DELETE FROM users WHERE uid = ? AND username = ?",
                                         [q_result[0][0], q_result[0][1]])
                    print("Effectué.\n")
                else:
                    print("Confirmation non reçue. Arrêt...\n")
                    return 1
            elif answer in {'N', 'n'}:
                print("Il s'agit du seul utilisateur trouvé. Arrêt...\n")
                return 0
            else:
                print("Nous n'avons pas compris votre réponse. Arrêt...\n")
                return 1
        elif len(q_result) == 0:
            print("Aucun utilisateur avec ce nom trouvé!!\n")
            return 0
        else:
            print("Attention, plusieurs utilisateurs trouvés avec ce nom!\n")
            print("+------------------------------------------------------+")
            print("|           UID           |      Nom d'utilisateur     |")
            print("+------------------------------------------------------+")
            for i in q_result:
                print("|{:d}                        |{:s}                        |".format(i[0], i[1]))
            print("+------------------------------------------------------+")

            del_id = input("Entrez l'UID de l'utilisateur à supprimer:\n>>> ")
            print("Voulez-vous effacer l'utilisateur {:s} identifié par UID {:d} ?".format(q_result[0][1], del_id))
            answer = input(">>> ")
            if answer in {'O', 'o'}:
                print("ATTENTION ! Cette opération est irréversible!!\nEntrez 'OK' en toutes lettres pour confirmer:\n")
                confirm = input(">>> ")
                if confirm == "OK":
                    print("Deleting {:s}...\n".format(q_result[0][1]))
                    dbcon_cursor.execute("DELETE FROM users WHERE uid = ? AND username = ?",
                                         [q_result[0][0], q_result[0][1]])
                else:
                    print("Confirmation non reçue. Arrêt...\n")
                    return 1
            elif answer in {'N', 'n'}:
                print("Il s'agit du seul utilisateur trouvé. Arrêt...\n")
                return 0
            else:
                print("Nous n'avons pas compris votre réponse. Arrêt...\n")
                return 1
        print("Done !\n")


def maj_user(dbcon_cursor):
    print("Mise à jour du mot de passe.\n")
    user_to_upd = input("Entrez le nom de l'utilisateur dont vous souhaitez modifier le mot de passe :\n>>> ")
    q_result = check_user(dbcon_cursor, user_to_upd)
    if len(q_result) == 1:
            print("Un utilisateur a été trouvé.")
            print("Voulez-vous mettre à jour le mot de passe de {:s} ? o/N".format(q_result[0][1]))
            answer = input(">>> ")
            print(answer)
            if answer in {'O', 'o'}:
                print("ATTENTION! Cette opération est irréversible!!\nEntrez 'OK' en toutes lettres pour confirmer:\n")
                confirm = input(">>> ")
                if confirm == "OK":
                    new_password = getpass("Entrez le nouveau mot de passe:\n>>> ")
                    dbcon_cursor.execute("UPDATE users SET password = ? WHERE uid = ?",
                                         [hashing(new_password), q_result[0][0]])
                    print("Mot de passe modifié pour {:s}".format(q_result[0][1]))
                else:
                    print("Confirmation non reçue. Arrêt...\n")
                    return 1
            elif answer in {'N', 'n'}:
                print("Il s'agit du seul utilisateur trouvé. Abandon...\n")
                return 1
            else:
                print("Nous n'avons pas compris votre réponse. Abandon...\n")
                return 1
    elif len(q_result) == 0:
            print("Aucun utilisateur avec ce nom trouvé!!\n")
            return 0
    else:
            print("Attention, plusieurs utilisateurs trouvés avec ce nom!\n")
            print("+------------------------------------------------------+")
            print("|           UID           |      Nom d'utilisateur     |")
            print("+------------------------------------------------------+")
            for i in q_result:
                print("|{:d}                        |{:s}                         |".format(i[0], i[1]))
            print("+------------------------------------------------------+")

            maj_id = input("Entrez l'UID de l'utilisateur dont le mot de passe sera mis à jour:\n>>> ")
            print("Voulez-vous mettre à jour le mot de passe de ' {:s} ' identifié par ' UID {:d} ' ? o/N".format(
                q_result[0][1], int(maj_id)))
            answer = input(">>> ")
            if answer in {'O', 'o'}:
                print("ATTENTION ! Cette opération est irréversible!!\nEntrez 'OK' en toutes lettres pour confirmer:\n")
                confirm = input(">>> ")
                if confirm == "OK":
                    new_password = getpass("Entrez le nouveau mot de passe:\n>>> ")
                    dbcon_cursor.execute("UPDATE users SET password = ? WHERE uid = ?",
                                         ([hashing(new_password), int(maj_id)]))
                    print("Mot de passe modifié pour {:s}".format(q_result[0][1]))
                else:
                    print("Confirmation non reçue. Abandon...\n")
            elif answer in {'N', 'n'}:
                print("Retour au menu principal.\n")
                return 1
            else:
                print("Nous n'avons pas compris votre réponse. Arrêt...\n")
                return 1


def user_login(dbcon_cursor):
    log_user = input("Nom d'utilisateur : \n>>> ")
    log_pass = getpass("Mot de passe: \n>>> ")
    q_result = check_user(dbcon_cursor, log_user)
    if len(q_result) >= 1:
        dbcon_cursor.execute("SELECT * from users WHERE username = ? AND password = ?", [log_user, hashing(log_pass)])
        auth_response = dbcon_cursor.fetchall()
        if len(auth_response) >= 1:
            print("Bravo, vous êtes authentifié!")
            return 0
        else:
            print("Mot de passe erroné pour cet utilisateur.\n")
            return 1
    else:
        print("Utilisateur non-existant.\n")
        return 1


# ####################################################>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> EXÉCUTION

# dbcon_cursor = None

# ###### ACCESS CONTROL #######
# adminPw = "b604f00b579a3011b3778c07747664f1334dcad66daa4b8c6cd07021cbda2ad10a81047a387d4a79999c10f188a5e103"
# inputPw = getpass("Entrez le mot de passe administrateur:\n>>> ")
# admin = 0
#
#
# if sha384(inputPw.encode()).hexdigest() == adminPw:
#     admin = 1
#     print("Vous êtes authentifié!\n")
# else:
#     admin = 0
#     print("Échec authentification")
#     return 1
#
# db_initialize("users")
#
# ### SEUL L'ADMIN PEUT SUPPRIMER DES UTILISATEURS ARBITRAIREMENT
# if admin == 1:
#     add_user()
#     delete_user()
# else:
#     print("Your are not admin!!\nExiting...")
#     return 1



