from random import choice
from hashlib import md5
from sys import argv
import string
import sqlite3


##### VARIABLES
# Base de données utilisateurs stockée dans un dictionnaire.
userdb = {}
# Arguments en ligne de commande
script, argv = argv
# Définition de l'espace de caractères pour nos mots de passe
char_space=string.ascii_letters+string.digits

# Affichage dudit espace sur la sortie standard
print("Caractères utilisés : ", char_space,"\n")

# Connection à la base de données SQLITE3
db_object = sqlite3.connect("myldap.sqlite3")
dbcon_object = db_object.cursor()


###### FONCTIONS
# Initialise la base de données si besoin
def db_initialize(tableName):
    # REQUÊTES SQLITE EFFECTUÉES AVEC SUBSTITUTION '?' AFIN DE MINIMISER RISQUES INJECTION SQL
    dbcon_object.execute("SELECT 1 FROM sqlite_master WHERE type = ? AND name = ?", ["table", tableName])
    qResult = dbcon_object.fetchone()
    # L'EVALUATION RENVOIE 'False' SI qResult N'A AUCUN TYPE (==VIDE). DONC :
    # SI qResult *- A UN TYPE -* ET DONC *-N'EST PAS VIDE-*, LA REQUÊTE SQLite PRÉCÉDENTE
    # A RENVOYÉ UNE VALEUR -> LA TABLE A ÉTÉ TROUVÉE.
    if qResult:
        print("Checking DATABASE...\nSQLite table ' {:s} ' exists! Proceeding...\n".format(tableName))
        return 0
    else:
        print("Table ' {:s} ' does not exist! Creating it before continuing...\n".format(tableName))
        # NOTE : LES NOMS DE TABLES NE **PEUVENT PAS** ÊTRE PASSÉS EN SUBSTITUTION DE PARAMÈTRE '?'!!!!
        dbcon_object.execute("DROP TABLE IF EXISTS %s" % tableName)
        dbcon_object.execute("""CREATE TABLE %s (
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
    print("New user is : ", new_user)
    dbcon_object.execute("INSERT INTO users VALUES(null,?,?)", new_user)
    return 0


## Fonction "check_user" prend un nom d'utilisateur en argument et cherche dans le dictionnaire.
## Sinon demande une saisie à l'utilisateur
def check_user(user=""):
    # Un string vide renverra 'False', donc il vaut mieux inverser le test ici.
    print("At this point, username is:", user)
    if user == "":
        user = input("Which user are you looking for?\n>>> ")

    print("Checking user {:s}".format(user))
    dbcon_object.execute("SELECT uid,username FROM users WHERE username = ?", [user])
    return dbcon_object.fetchall()


def delete_user():
        user = input("Which user are you deleting? \n>>> ")
        qResult = check_user(user)
        if len(qResult) > 0:
            print("Des utilisateurs ont été trouvés.\n")
        elif len(qResult) = 1:
            break
        elif len(qResult) = 0:
            print("Aucun utilisateur avec ce nom trouvé!!\n")
            exit(0)
        else:
            for i in qResult:
                print("Utilisateur: {:s} avec UID {:d}".format(qResult[0],qResult[1]))

        print("Done !\n")




###### EXÉCUTION

admin = 1

### SEUL L'ADMIN PEUT SUPPRIMER DES UTILISATEURS ARBITRAIREMENT
if admin == 1:
    delete_user()
else
    print("Your are not admin!!\nExiting...")
    exit(1)

db_initialize("users")

# ENREGISTREMENT DES CHANGEMENTS SUR LA BDD "PHYSIQUE"
db_object.commit()

# Fermeture de la connexion à la BDD
db_object.close()

del dbcon_object
del db_object
