file_to_read = open('solution.csv', 'r')
total_trajets_type1 = [i for i in range(11)]
total_trajets_type2 = [j for j in range(11)]
bds = 128

for line in file_to_read.readlines():
    split_line = line.split(";")
    if split_line[0][0:2] == 'n1':
        total_trajets_type1[int(split_line[0][7])] += int(split_line[1])
    elif split_line[0][0:2] == 'n2':
        total_trajets_type2[int(split_line[0][7])] += int(split_line[1])
    elif split_line[0][0:2] == 'na':
        total_trajets_type2[int(split_line[0][5])] += int(split_line[1])
# Pour chaque semestre, il faut calculer le jour auquel on doit faire un changement
for s in range(len(total_trajets_type1)):
    print("Pour le type 1, changement le jour " + str(total_trajets_type1[s] % bds) + " au semestre " + str(s))

for s in range(len(total_trajets_type2)):
    print("Pour le type 2, changement le jour " + str(total_trajets_type2[s] % bds) + " au semestre " + str(s))
