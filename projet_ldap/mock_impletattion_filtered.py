from random import choice
from hashlib import md5
from sys import argv
import string
import sqlite3


userdb = {}
script, argv = argv
char_space=string.ascii_letters+string.digits

print("Caractères utilisés : ", char_space,"\n")

db_object = sqlite3.connect("myldap.sqlite3")
dbcon_object = db_object.cursor()


def db_initialize(tableName):

    dbcon_object.execute("SELECT 1 FROM sqlite_master WHERE type = ? AND name = ?", ["table", tableName])
    qResult = dbcon_object.fetchone()



    if qResult:
        print("Checking DATABASE...\nSQLite table ' {:s} ' exists! Proceeding...\n".format(tableName))
        return 0
    else:
        print("Table ' {:s} ' does not exist! Creating it before continuing...\n".format(tableName))

        dbcon_object.execute("DROP TABLE IF EXISTS %s" % tableName)
        dbcon_object.execute("""CREATE TABLE %s (
                                uid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                username text,
                                password CHAR(32)
                                ) """ % tableName)
        print("Done!\n\n")
        return 0

def genpasswd():
    password = ""
    for i in range(8):
        password += choice(char_space)
    return password


def hashing(input_password):
        md5hash = md5()
        md5hash.update(input_password.encode(encoding='ascii', errors='strict'))
        return md5hash.hexdigest()


# Fonction d'ajout d'utilisateur
def add_user():
# On saisit le nom d'utilisateur
    username = (input("Saisissez un nouvel utilisateur:\n>>> "))
# On utilise la fonction genpasswd() définie précédemment
    motpasse = genpasswd()
# On hashe le mot de passe généré en employant la fonction hashing définie précédemment
    pwHash = (hashing(motpasse))
# On récupère le nom d'utilisateur et le hash du mot de passe pour en faire une nouvelle entrée
    new_user = (username,pwHash)
# On affiche tout ce qu'on a fait précédemment (nom; mot de passe; hash)
    print("Utilisateur => ' {:s} '\nMot de passe => {:s} \nHash => {:s}".format(new_user[0], motpasse, new_user[1]))
    print("New user is : ", new_user)
# on l'ajoute dans la BDD
    dbcon_object.execute("INSERT INTO users VALUES(null,?,?)", new_user)
    return 0



def check_user(user=""):

    if user == "":
        user = input("Which user are you looking for?\n>>> ")

    print("Checking user ' {:s} ' ...".format(user))
    dbcon_object.execute("SELECT uid,username FROM users WHERE username = ?", [user])
    return dbcon_object.fetchall()


def delete_user():
        user = input("Which user are you deleting? \n>>> ")
        qResult = check_user(user)
        if len(qResult) == 1:
            print("Un utilisateur a été trouvé.")
            print("Voulez-vous effacer l'utilisateur {:s} ? o/N".format(qResult[0][1]))
            answer = input(">>>")
            if answer == ("O" or "o"):
                print("ATTENTION! Cette opération est irréversible!!\nEntrez 'OK' en toutes lettres pour confirmer:\n")
                confirm = input(">>>")
                if confirm == "OK":
                    print("Deleting {:s}...\n".format(qResult[0][1]))
                    dbcon_object.execute("DELETE FROM users WHERE uid = ? AND username = ?", [qResult[0][0], qResult[0][1]])
                    print("Done!")
                else:
                    print("Confirmation non reçue. Arrêt...\n")
                    exit(1)
            elif answer == ("N" or "n"):
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

        print("Done !\n")





admin = 1

db_initialize("users")

if admin == 1:
    delete_user()
else:
    print("Your are not admin!!\nExiting...")
    exit(1)

db_object.commit()

db_object.close()

del dbcon_object
del db_object
