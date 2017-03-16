def interface()
ans=True
print("Saisissez main.py -h pour afficher l'aide d'utilisation du programme.\nSaisissez main.py -a pour ajouter un utilisateur.\nSaisissez main.py -d pour effacer un utilisateur.\nSaisissez main.py -m pour mettre à jour un utilisateur.\nSaisissez exit pour sortir du programme.\n"
ans=raw_input("Que voulez vous faire ?\n")
if ans=="main.py -h":
help()
print("Aide de main.py\n")
elif ans=="main.py -a":
add_user()
print("Ajout utilisateur\n")
elif ans=="main.py -d":
delete_user()
print("Suppression utilisateur\n")
elif ans=="main.py -m":
update_user()
print("Modification de l'utilisateur\n")
elif ans =="exit":
ans=False
print("Sortie du programme\n")
else:
print("Saisie non reconnue\n")
