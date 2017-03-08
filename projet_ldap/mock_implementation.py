from random import choice
from hashlib import md5
import string

# Base de données utilisateurs stockée dans un dictionnaire.

userdb = {}

char_space=string.ascii_letters+string.digits
print("Caractères utilisés : ", char_space,"\n")


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
    username = input("Saisissez un nouvel utilisateur:\n>>> ")
    motpasse = genpasswd()
    userdb[username]=hashing(motpasse)
    print("Utilisateur => ' {:s} '\nMot de passe => {:s} \nHash => {:s}".format(username, motpasse, userdb[username]))
    return 0


## Fonction "check_user" prend un nom d'utilisateur en argument et cherche dans le dictionnaire.
## Sinon demande une saisie à l'utilisateur
def check_user(username=""):
    # Un string vide renverra 'False'
    if username:
        username = input("Which user are you looking for?\n>>> ")

    print("Checking user {:s}".format(username))
    return userdb.__contains__(username)


#def delete_user():


add_user()
print(check_user("yann"))
#delete_user()