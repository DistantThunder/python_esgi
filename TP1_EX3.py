# Déclaration d'une liste en "extension" 

my_list = []
for i in "abc":
    for j in "de":
        my_list.append(i+j)
print(my_list)

# Version en "intention" de la même liste
ma_liste=[i+j for i in "abc" for j in "de"]
print(ma_liste)
