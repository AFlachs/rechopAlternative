import pandas as pd

solutions = open('solution.csv', 'r')

trucks_df = pd.DataFrame(columns=["Semestre", "Type 1", "Type 2"])

cities_list = ["Anvers", "Charleroi", "Gand", "Bruxelles", "Hasselt", "Liege"]

p0_dfs = [pd.DataFrame([[cities_list[i], 0, 0, 0] for i in range(len(cities_list) - 1)],
                       columns=["Ville", "Type 1", "Type 2", "Type 2 (+ Anvers)"]) for s in range(11)]
p1_dfs = [pd.DataFrame([[cities_list[i], 0, 0, 0] for i in range(len(cities_list) - 1)],
                       columns=["Ville", "Type 1", "Type 2", "Type 2 (+ Anvers)"]) for s in range(11)]


def insert_truck(variable_indices, value):
    global trucks_df
    if variable_indices[0] == '1':
        trucks_df.at[variable_indices[1], :] = [variable_indices[1], value, 0]
    else:
        trucks_df.iat[int(variable_indices[1]), 2] = value


def insert_na(variable_indices, value):
    global p0_dfs, p1_dfs
    if variable_indices[0] == '0':
        p0_dfs[int(variable_indices[1])].at[0, "Type 2"] = value
    if variable_indices[0] == '1':
        p1_dfs[int(variable_indices[1])].at[0, "Type 2"] = value


def insert_n1(variable_indices, value):
    global p0_dfs, p1_dfs
    if variable_indices[0] == '0':
        p0_dfs[int(variable_indices[2])].at[int(variable_indices[1]), "Type 1"] = value
    if variable_indices[0] == '1':
        p1_dfs[int(variable_indices[2])].at[int(variable_indices[1]), "Type 1"] = value


def insert_n2(variable_indices, value):
    global p0_dfs, p1_dfs
    if variable_indices[0] == '0':
        if (variable_indices[3] == '0'):
            p0_dfs[int(variable_indices[2])].at[int(variable_indices[1]), "Type 2"] = value
        else:
            p0_dfs[int(variable_indices[2])].at[int(variable_indices[1]), "Type 2 (+ Anvers)"] = value
    if variable_indices[0] == '1':
        if (variable_indices[3] == '0'):
            p1_dfs[int(variable_indices[2])].at[int(variable_indices[1]), "Type 2"] = value
        else:
            p1_dfs[int(variable_indices[2])].at[int(variable_indices[1]), "Type 2 (+ Anvers)"] = value


def manage_var(var_type, variable_indices, value):
    if var_type == 'c':
        insert_truck(variable_indices, value)
    elif var_type == 'na':
        insert_na(variable_indices, value)
    elif var_type == 'n1':
        insert_n1(variable_indices, value)
    elif var_type == 'n2':
        insert_n2(variable_indices, value)


for line in solutions:
    line = line.rstrip("\n")
    var_name, value = line.split(';')
    var_type, indices = var_name.split('_')
    variable_indices = indices.split(',')

    manage_var(var_type, variable_indices, value)

print("Planning du semestre : ")
print(p0_dfs[9])
print(p1_dfs[9])

print("Organisation des camions sur les semestres")
print(trucks_df)
