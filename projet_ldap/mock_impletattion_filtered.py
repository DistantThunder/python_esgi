# On importe les librairies dont on va avoir besoin
# On créera aléatoirement un mot de passe donc besoin du random choice
from random import choice
# On va hasher le mot de passe en MD5 donc on importe md5 de hashlib
from hashlib import md5
# On va rentrer des arguments élaborés, donc on prend argv de la librairie sys
from sys import argv
# On utilisera des chaines de caractères, donc on prend string
import string
# On va créer une base de données contenant les users, et on la fera en sqlite3, il faut donc l'importer
import sqlite3


# Déclaration de la BDD
userdb = {}
# Déclaration de script
script = argv
# On créé la liste des caractères qu'on va employer pour générer les mots de passe, ici ça sera chiffres et lettres (majuscules comme minuscules)
char_space=string.ascii_letters+string.digits

# On affiche la liste des caractères qu'on utilisera, peu utile au programme final, ça sert de rappel et de débug
print("Caractères utilisés : ", char_space,"\n")

# Connexion à la BDD et déclaration du curseur dont on se servira
db_object = sqlite3.connect("myldap.sqlite3")
dbcon_object = db_object.cursor()


# On créé une table dans la BDD
def db_initialize(tableName):

# Execution d'une requète SQL demandant d'entrer le nom de la table voulue
    dbcon_object.execute("SELECT 1 FROM sqlite_master WHERE type = ? AND name = ?", ["table", tableName])
# On rentre le résultat dans une variable qu'on utilisera ensuite, mais juste la première valeur
    qResult = dbcon_object.fetchone()


# Affichage de la table demandée ou création de la table si elle n'existait pas, le tout en affichant ce que fait le programme.
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

# Création de la fonction de génération de mot de passe, qui choisit 8 caractères dans la liste définie au début et le stocke dans la variable password
def genpasswd():
    password = ""
    for i in range(8):
        password += choice(char_space)
    return password


# Création de la fonction de hashage en MD5 qui utilise le mot de passe généré précédement
def hashing(input_password):
        md5hash = md5()
        md5hash.update(input_password.encode(encoding='ascii', errors='strict'))
        return md5hash.hexdigest()


# Fonction d'ajout d'utilisateur
def add_user():
# On saisit le nom d'utilisateur qu'on stocke dans une chaine de caractères
    username = (input("Saisissez un nouvel utilisateur:\n>>> "))
# On utilise la fonction genpasswd() définie précédemment et on stocke
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


# Création de la fonction qui vérifiera l'existance d'un utilisateur dans la BDD
def check_user(user=""):

# On demande la saisie de l'utilisateur à rechercher et on met le résultat dans la variable user
    if user == "":
        user = input("Which user are you looking for?\n>>> ")

# Requète SQL qui va rechercher l'utilisateur dans la table users et affichera tous les résultats correspondants
    print("Checking user ' {:s} ' ...".format(user))
    dbcon_object.execute("SELECT uid,username FROM users WHERE username = ?", [user])
    return dbcon_object.fetchall()


# Création de la fonction de suppression d'utilisateur
def delete_user():
# On demande l'utilisateur à supprimer, et on enregistre cette variable dans user
        user = input("Which user are you deleting? \n>>> ")
# On regarde si l'utilisateur existance
        qResult = check_user(user)
        if len(qResult) == 1:
            print("Un utilisateur a été trouvé.")
# Demande de confirmation via saisie pour supprimer l'utilisateur
            print("Voulez-vous effacer l'utilisateur {:s} ? o/N".format(qResult[0][1]))
            answer = input(">>>")
            if answer == ("O" or "o"):
                print("ATTENTION! Cette opération est irréversible!!\nEntrez 'OK' en toutes lettres pour confirmer:\n")
                confirm = input(">>>")
                if confirm == "OK":
# Suppression de l'utilisateur de la BDD
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
# Gestion du cas ou il existe lusieurs utilisateurs du même non, et demande de la saisie de son UID qui est affiché
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
    #add_user()
else:
    print("Your are not admin!!\nExiting...")
    exit(1)

db_object.commit()

db_object.close()

del dbcon_object
del db_object
