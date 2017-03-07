# Déclaration d'une liste en "intention" (sans variables intermédiaires)

my_list = []
for i in "abc":
    for j in "de":
        my_list.append(i+j)
print(my_list)
