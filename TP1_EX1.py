list1=["vendredi",19,"avril"]       # création d'une liste de 3 objets différents
print(list1)                        # Affichage du contenu de la liste
print(list1[0])                     # Affichage du 1er objet de la liste
len(list1)                          # Affichage de la taille 3 de la liste
list1.append(2012)                  # Ajout de l'objet entier 2012 à la fin de la liste
print(list1)                        # Affichage de la liste "list1"
list1[3]+1                          # Addition entre l'objet entier 2012 et l'objet "1"
del list1[0]                        # Suppression de l'objet d'indice 0: vendredi
print(list1)                        # Affichage de la liste "list1"
list1.insert(20,"Samedi")           # Ajout de Samedi à la fin de la liste "list1"
print(list1)                        # Affichage de la liste "list1"
print("jeudi" in list1)             # Faux, "jeudi" n'est pas dans objet 'list' "list1"
print("Samedi" in list1)            # Vrai
list2=list1[1:3]                    # Création de la sous-liste "list2" à partir des éléments 1 et 2de la liste "list1"
print(list2)                        # Affichage de la liste "list2"
list3=list1[:2]                     # Création de la sous-liste "list3" avec les éléments 0 & 1 de L1 
list4=list1[1:]						# Création de la liste "list4" avec les éléments la liste "list1" du deuxième élément, jusqu'à la fin de cette dernière
print(list3)						# Affichage "list3"
print(list4)						# Affichage "list4"
list3=list3+[2015]					# Concaténation de "list3" avec une liste contenant "2015"
print(list3)						# Affichage "list3"
list5=5*list1						# Création de la liste "list5" contenant 5 fois la liste "list1"
print(list5)						# Affichage "list5"
list1.extend([3,4])					# Ajout de la sous liste "[3,4]" à la liste "list1"
print(list1)						# Affichage "list1"
list6=list1.pop(0)					# Création de la liste "list6" avec le contenu de la liste "list1" avec l'élement d'indice 0 en moins (soit "19")
print(list5)						# Affichage "list5"
