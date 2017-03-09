print("############## DÉNOMBREMENT DE MOTS DANS UNE CHAÎNE DE CARACTÈRES DONNÉES ##############\n\nVeuillez entrer une chaîne de caractères : \n")
string = input(">>")

def nbr_mots(sentence):
    dico={}
    for i in sentence.split():
        dico[i]=sentence.count(i)
    print(dico)

nbr_mots(string)      
    
