# Définition d'un client réseau gérant en parallèle l'émission
# et la réception des messages (utilisation de 2 THREADS).

# Variables définies dans le script
HOST = '127.0.0.1'
PORT = 40017
auteur="Jeremy Reisser & Florian Pompey"
date="16 mars 2017"

# Importation des modules utiles pour le script
import sys
import pickle
import socket
import os
import time
import getpass
import hashlib
import threading

#-----------------------------------------------------------------------
class ThreadReception(threading.Thread):
    """objet thread gérant la réception des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn           # réf. du socket de connexion
        
    def run(self):
        while 1:
            message_recu = self.connexion.recv(128)
            print(message_recu.decode())
            if message_recu ==b'' or message_recu.upper() == b"FIN":
                break
        # Le thread <réception> se termine ici.
        # On force la fermeture du thread <émission> :
        
        print ("Client arrêté en réception. Connexion interrompue!")
        
        self.connexion.close()
    
#------------------------------------------------------------------------
class ThreadEmission(threading.Thread):
    """objet thread gérant l'émission des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn           # réf. du socket de connexion
        
    def run(self):
        while 1:
            time.sleep(0.5)
            message_emis = input("saisir un msg :")
            self.connexion.send(message_emis.encode())
            if message_emis.upper()=="FIN":
                break
         
        print("Client arrêté en émission. Connexion interrompue.")
        self.connexion.close()
		
#------------------------------------------------------------------------
class ThreadEmission_admin(threading.Thread):
    """objet thread gérant l'émission des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn           # réf. du socket de connexion
        
    def run(self):
        while 1:
            time.sleep(0.5)
            message_emis = input(menu())
            self.connexion.send(message_emis.encode())
            if message_emis.upper()=="7":
                break
         
        print("Client arrêté en émission. Connexion interrompue.")
        self.connexion.close()
		
#------------------------------------------------------------------------


# Création d'une variable annuaire qui utilise le module pickle pour initialiser le dictionnaire
annuaire=pickle.load(open('dictionnaire.pkl','rb')) # Ouvre le fichier dictionnaire.pkl en lecture(mode binaire), il contient les entrées du dictionnaire


# Fonction pour la création d'utilisateurs
def addUser():
    print("\n***Ajout d'un contact***\n")
    loadAnnuaire()  # Appel de la fonction pour charger l'annuaire

# L'utilisateur doit saisir le nom d'un contact
    contact = input("Nom du contact\
(Attention : programme sensible à la casse): ")
# Condition si le résultat de la variable "contact" est présent dans l'annuaire
    if contact in annuaire:
# Afficher un message d'erreur puis sort de la condition
        print("\n***ERREUR. Ce contact existe déjà***\n")
# Sinon, on reste dans la condition
    else:
        p = getpass.getpass('Son mot de passe: ')   # getpass permet de ne pas afficher de caractère pendant la saisie du mot de passe (ne fonctionne pas depuis IDLE)
        p2 = getpass.getpass('Confirmer son mot de passe: ')    # confirmation de la saisie du mot de passe
        if p != p2: # Si les mots de passe ne correspondent pas
            print('\n***Erreur de confirmation***\n')   # Message d'erreur si les mots de passe ne sont pas identiques
            return # Retourne valeur vide et sort de la condition
        
        else:   # Si les mots de passe concordent  
            ph = hashlib.md5(p.encode()).hexdigest()  # On encode le mot de passe en md5 grâce au module hashlib, hexdigest permet de convertir en Hexadecimal  
            e = input("Son email : ")   # On demande à l'utilisateur de renseigner un email
            t = input("Son téléphone : ")   # On demande à l'utilisateur de renseigner un numéro de téléphone
            annuaire[contact]=ph,t,e    # On utilise les variables 'ph','e','t' comme valeurs pour la clé 'contact' dans le dictionnaire
            print("\n***","Le contact",contact, "a correctement été créé***\n")
            saveAnnuaire()  # Appel de la fonction pour sauvegarder l'annuaire
            
# Fontion pour la consultation des contacts dans l'annuaire
def consultADM():
    
        loadAnnuaire()  # Appel de la fonction pour charger l'annuaire    
        if len(annuaire) == 0:  # Condition pour vérifier si l'annuaire est vide
            print("\n***Il n'y a aucun contact dans l'annuaire***\n")   # Message si l'annuaire est vide
        else:
              print("\nListe des contacts dans l'annuaire:\n")  # Sinon on affiche les contacts présents dans l'annuaire
        for name, info in annuaire.items(): # Boucle qui permet d'identifier les clés et leurs valeurs associées dans le dictionnaire
            print("Login : ",name, "  ***  Mot de passe : ",\
                  info[0],"\nTéléphone : ", info[1],"  ***  Email : ", info[2],"\n__________\n") # Affiche le résultat avec un format personnalisé
        input("Appuyer sur ENTREE pour revenir au menu principal ")
        print("\n")
        print("\n")

# Fontion pour la consultation des contacts dans l'annuaire
def consultUSR():
        print("\nInformations de votre compte:\n")  # Affiche les informations du compte en cours
        loadAnnuaire()  # Appel de la fonction pour charger l'annuaire    
             
        for name, info in annuaire.items(): # Boucle qui de vérifier le nom de l'utilisateur en cours
            if user == name:
                print("Login : ",user, "  ***  Mot de passe : ",\
                  info[0],"\nTéléphone : ", info[1],"  ***  Email : ", info[2],"\n__________\n") # Affiche le résultat avec un format personnalisé
        input("Appuyer sur ENTREE pour revenir au menu principal ")
        print("\n")
        print("\n")
            
# Fonction pour la modification des utilisateurs
def modUserADM():
    print("\n***Modification d'un contact***\n")

    loadAnnuaire()  # Appel de la fonction pour charger l'annuaire
    
    print("***Quel contact souhaitez-vous modifier?***")    # Demande à l'utilisateur de renseigner le nom d'un contact
    modif = input("Entrez le nom du contact\
 (Attention à la casse): ")
    if modif not in annuaire:   # Condition si le contact renseigné n'est pas dans le dictionnaire
        print("\n***ERREUR. Ce contact n'existe pas***\n")  # Message d'erreur, sort de la condition
    else:
        for name, info in annuaire.items():
            if modif == name:
                confirm = input("\nEtes-vous sûr de vouloir modifier cet utilisateur(oui/non): ")
                if confirm != 'oui':
                    print("\n***MODIFICATION ANNULEE***\n\n")
                    return
                else:
                    newPwd = getpass.getpass("Entrez un nouveau Mot de passe: ")    # Sinon, demande à l'utilisateur de renseigner un nouveau mot de passe
                    newPwd_confirm = getpass.getpass("Confirmez le nouveau Mot de passe: ") # Demande à l'utilisateur de confirmer le mot de passe
                if newPwd != newPwd_confirm:    # Condition si les mots de passe renseignés ne correspondent pas
                    print("\n***Erreur de confirmation***\n")   # Message d'erreur et sort de la condition
                    return
                else:
                    ph = hashlib.md5(newPwd.encode()).hexdigest()   # Sinon, hash le mot de passe en md5
                    annuaire[modif] = ph, input("Entrez un nouveau Téléphone : "),\
                    input("Entrez un nouvel Email : ")    # Modifie les valeurs associées à la clé renseignée dans le dictionnaire
                    print("\n***MODIFICATION EFFECTUEE***\n\n")
                saveAnnuaire()  # Appel de la fonction pour sauvegarder l'annuaire


# Fonction pour la modification des utilisateurs
def modUserUSR():
    print("\n***Modification de votre compte***\n")
    loadAnnuaire()  # Appel de la fonction pour charger l'annuaire

    for name, info in annuaire.items():
            if user == name:
                confirm = input("\nEtes-vous sûr de vouloir modifier votre compte(oui/non): ")
                if confirm != 'oui':
                    print("\n***MODIFICATION ANNULEE***\n\n")
                    return
                else:
                    newPwd = getpass.getpass("Entrez un nouveau Mot de passe: ")    # Sinon, demande à l'utilisateur de renseigner un nouveau mot de passe
                    newPwd_confirm = getpass.getpass("Confirmez le nouveau Mot de passe: ") # Demande à l'utilisateur de confirmer le mot de passe
                    if newPwd != newPwd_confirm:    # Condition si les mots de passe renseignés ne correspondent pas
                        print("\n***Erreur de confirmation***\n")   # Message d'erreur et sort de la condition
                        return
                    else:
                        ph = hashlib.md5(newPwd.encode()).hexdigest()   # Sinon, hash le mot de passe en md5
                        annuaire[user] = ph, input("Entrez un nouveau Téléphone : "),\
                            input("Entrez un nouvel Email : ")    # Modifie les valeurs associées à la clé renseignée dans le dictionnaire
                    print("\n***MODIFICATION EFFECTUEE***\n\n")
                    saveAnnuaire()  # Appel de la fonction pour sauvegarder l'annuaire
        
# Fonction pour la suppression d'utilisateurs            
def delUser():
    print("\n***Suppression d'un contact***\n")
    
    loadAnnuaire()  # Appel de la fonction pour charger l'annuaire
    
    print("\n***Quel contact souhaitez-vous supprimer?***") # Demande à l'utilisateur de renseigner un contact
    suppr = input("Entrez le nom d'un contact\
 (Attention à la casse): ")

    if suppr == 'admin':
        print("\n***ERREUR. Impossible de supprimer cet utilisateur***\n")
    elif suppr not in annuaire:   # Condition si l'utilisateur renseigné n'existe pas dans l'annuaire
       print("\n***ERREUR. Ce contact n'existe pas***\n")   # Message d'erreur et sort de la condition
    else:
        confirm = input("\nEtes-vous sûr de vouloir supprimer ce contact(oui/non): ") # Sinon, demande de confirmation avant la suppression
        if confirm == 'oui':    # Si l'utilisateur répond 'oui, on supprime la clé du dictionnaire
            del annuaire[suppr]
            print("\n***",suppr,"a bien été supprimé de l'annuaire ***\n") # Message de confirmation que l'utilisateur renseigné a été supprimé
            saveAnnuaire()  # Appel de la fonction pour sauvegarder l'annuaire
        else:   # Si l'utilisateur ne renseigne pas 'oui', on sort de la condition
            return

# Fonction pour enregistrer les clés/valeurs du dictionnai re vers un fichier
def saveAnnuaire():
    f=open('dictionnaire.pkl','wb') # Variable qui permet de déclarer le fichier dictionnaire.pkl pour l'ouvrir en écriture (mode binaire) dans le script
    pickle.dump(annuaire,f,pickle.HIGHEST_PROTOCOL) # Utilisation du module pickle pour sauvegarder les données de l'annuaire dans le fichier dictionnaire.pkl
    f.close()   # Ferme le fichier

# Fonction pour charger les clés/valeurs du dictionnaire depuis un fichier        
def loadAnnuaire():
    f = open('dictionnaire.pkl','rb')   # Variable qui permet de déclarer le fichier dictionnaire.pkl pour l'ouvrir en lecture(mode binaire) dans le script
    annuaire = pickle.load(f)   # Ouverture du fichier dictionnaire.pkl pour les importer dans le dictionnaire initialisé dans le script
    

# Fonction d'initialisation de l'interface admin
running = True
def interfAdmin():

# Affichage de la page d'accueil
    print("***********************************************")
    print("*               ANNUAIRE PYTHON               *")
    print("***********************************************")
    print("*                                             *")
    print("*  Auteurs :",auteur," *")
    print("*  Date de création : ",date,"          *")
    print("*                                             *")
    print("***********************************************")
    print("*                                             *")
    print("*          Interface d'administration         *")
    print("*                                             *")


    while running:  # Boucle qui permet de revenir à cette partie du script pendant son exécution
        print("***********************************************")
        print("*               MENU PRINCIPAL                *")
        print("***********************************************")
        print("*                                             *")
        print("*  Que voulez-vous faire?                     *")
        print("*                                             *")
        print("*  1.  Ajouter un contact                     *") 
        print("*  2.  Modifier un contact                    *")      # Affichage du menu principal
        print("*  3.  Supprimer un contact                   *")     
        print("*  4.  Consulter l'annuaire                   *")
        print("*  5.  Quitter                                *")
        print("*                                             *")
        print("***********************************************")
        reponse = eval(input("Choix : ")) # Demande à l'utilisateur de renseigner un choix   

        try:
            if reponse == 1:    # Si l'utilisateur a renseigné '1', le script continue à la fonction addUser()
                addUser()

            elif reponse == 2:  # Si l'utilisateur a renseigné '2', le script continue à la fonction modUser()
                modUserADM()

            elif reponse == 3:  # Si l'utilisateur a renseigné '3', le script continue à la fonction delUser()
                delUser()

            elif reponse == 4:  # Si l'utilisateur a renseigné '4', le script continue à la fonction consult()
                consultADM()
        
            elif reponse == 5:  # Si l'utilisateur a renseigné '5', on quitte le script
                print("\nAu revoir !\n")
                time.sleep(1.5)
                sys.exit()
                
        
            else:
                print("\n***Veuillez entrer un choix valide***\n")    # Sinon, affiche un message si l'utilisateur n'a pas renseigné le choix attendu et boucle sur le menu principal

        except EOFError:
            print("\n\n***Appuyez sur '5' pour quitter le programme***\n")  # Exception en cas de message d'erreur
            continue
        

        except KeyboardInterrupt:
            print("\n\n***Appuyez sur '5' pour quitter le programme***\n")  # Exception en cas de message d'erreur
            continue


def interfUser():

# Affichage de la page d'accueil
    print("***********************************************")
    print("*               ANNUAIRE PYTHON               *")
    print("***********************************************")
    print("*                                             *")
    print("*  Auteurs :",auteur," *")
    print("*  Date de création : ",date,"          *")
    print("*                                             *")
    print("***********************************************")
    print("*                                             *")
    print("*            Interface utilisateur            *")
    print("*                                             *")


    while running:  # Boucle qui permet de revenir à cette partie du script pendant son exécution
        print("***********************************************")
        print("*               MENU PRINCIPAL                *")
        print("***********************************************")
        print("*                                             *")
        print("*  Que voulez-vous faire?                     *")
        print("*                                             *")
        print("*  1.  Consulter mon compte utilisateur       *")      # Affichage du menu principal
        print("*  2.  Modifier mes informations              *")     
        print("*  3.  Quitter                                *")
        print("*                                             *")
        print("***********************************************")
        reponse = eval(input("Choix : ")) # Demande à l'utilisateur de renseigner un choix   

        try:

            if reponse == 1:  # Si l'utilisateur a renseigné '1', le script continue à la fonction consultUSR()
                consultUSR()

            elif reponse == 2:  # Si l'utilisateur a renseigné '2', le script continue à la fonction modUserUSR()
                modUserUSR()
        
            elif reponse == 3:  # Si l'utilisateur a renseigné '3', on quitte le script
                print("\nAu revoir !\n")
                time.sleep(1.5)
                sys.exit()
                
        
            else:
                print("\n***Veuillez entrer un choix valide***\n")    # Sinon, affiche un message si l'utilisateur n'a pas renseigné le choix attendu et boucle sur le menu principal

        except EOFError:
            print("\n\n***Appuyez sur '5' pour quitter le programme***\n")  # Exception en cas de message d'erreur
            continue
        

        except KeyboardInterrupt:
            print("\n\n***Appuyez sur '5' pour quitter le programme***\n")  # Exception en cas de message d'erreur
            continue

while running:
        print("\nVeuillez vous identifier pour vous connecter à l'annuaire\n")
        user = input('Identifiant: ')
        passwrd = getpass.getpass('Mot de passe: ')
        passwrd = hashlib.md5(passwrd.encode()).hexdigest()

        for name, info in annuaire.items():
               
            if user == name:
                print()
                if passwrd == info[0]:
                    print()
                    if 'admin' in user:                        
                        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		
                        try:
                            print()
                            connexion.connect((HOST, PORT))
                        except socket.error:
                            print("La connexion a échoué...")
                            sys.exit()    
                        print("Connexion établie avec le serveur...\n")
                        time.sleep(1)
                        interfAdmin()

                        # Dialogue avec le serveur : on lance deux threads pour gérer
                        # indépendamment l'émission et la réception des messages :
                        
                        th_E1 = ThreadEmission_admin(connexion)
                        th_R1 = ThreadReception(connexion)
                        th_E1.start()
                        th_R1.start()
                        break

                    else:
                        print()
                        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		 
                        try:
                            connexion.connect((HOST, PORT))
                        except socket.error:
                            print("La connexion a échoué...")
                            sys.exit()    
                        print("Connexion établie avec le serveur...\n")
                        time.sleep(1)
                        interfUser()

                        # Dialogue avec le serveur : on lance deux threads pour gérer
                        # indépendamment l'émission et la réception des messages :

                        th_E2 = ThreadEmission(connexion)
                        th_R2 = ThreadReception(connexion)
                        th_E2.start()
                        th_R2.start()
                        break

                    
                else:
                    print ("\n***Login incorrect***\n")                    
                
          
