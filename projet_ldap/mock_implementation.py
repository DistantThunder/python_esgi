from random import choice
from hashlib import md5
import string


char_space=string.ascii_letters+string.digits
print("Caractères utilisés : ", char_space,"\n")


# Fonction de génération de mot de passe aléatoire
def genpasswd():
    password = ""
# On va boucler sur le char_space pour obtenir un peu plus de randomness
    for i in range(8):
        password += choice(char_space)
    return password


def hashing(input_password):
        md5hash = md5()
        md5hash.update(input_password.encode(encoding='ascii', errors='strict'))
        return md5hash.hexdigest()

motpasse = genpasswd()
print("Mot de passe généré: ' ", motpasse, " '\n")
print("Hash MD5 du mot de passe: ' ", hashing(motpasse), " '\n")
