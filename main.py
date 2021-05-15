import json

import numpy as np
import pulp
from pulp import LpVariable, LpProblem, LpMinimize, lpSum, GLPK

import costs
import introduceProblem

# Paramètres ###########################

v_moy = 70  # km/h
work_time = 8  # heures
tau = 1  # heures
fuel_price = 1.5  # €/l
conso = 0.35  # l/km

max_capacity_1 = 16.5  # Tonnes
max_capacity_2 = 5.5  # Tonnes
depreciation_rate = 0.2  # pas d'unité
buying_price_1 = 40000  # euros
buying_price_2 = 50000  # euros
max_trucks_type1 = 6  # nombre max de camions de type 1
max_trucks_type2 = 5  # nombre max de camions de type 2
max_trucks = max_trucks_type2 + max_trucks_type1
# max_times_in_city = 1  # nombre de fois max qu'un camion peut passer dans une ville par jour
business_days_by_semester = 128
semesters = [i for i in range(10 + 1)]  # introduceProblem.introduce_semesters()
semester_number = len(semesters)

N = 10000000  # même principe que le big M
distances = introduceProblem.introduce_distances()
road_distances1, road_distances2 = introduceProblem.introduce_roads_distances()
t = introduceProblem.introduce_roads_feasibility(v_moy, work_time)  # Faisabilité des trajets passant par
# une ville et anvers

cities_number = 5
# transport_types = introduceProblem.introduce_truck_types()
selling_cost = introduceProblem.introduce_selling_cost(depreciation_rate, buying_price_1,
                                                       buying_price_2)  # cost[type][age]
requests = introduceProblem.introduce_city_requests()

# cities_list = ["Anvers", "Charleroi", "Gand", "Bruxelles", "Hasselt", "Liege"]
cities_number = 5  # On ne compte pas Liège

# Initialisation ###################

print("Initialisation")

problem = LpProblem(name="Projet", sense=LpMinimize)

n1 = [[[
    LpVariable('n1_{},{},{}'.format(p, v, s), cat='Integer', lowBound=0)
    for s in range(semester_number)]
    for v in range(cities_number)]
    for p in [0, 1]
]
# n1_pvs

n2 = [[0] + [[[
    LpVariable('n2_{},{},{},{}'.format(p, v, s, a), cat='Integer', lowBound=0)
    for a in [0, 1]]
    for s in range(semester_number)]
    for v in range(1, cities_number)]  # Ne peut pas être dans anvers
    for p in [0, 1]]
# n2_pvsa

na = [[
    LpVariable('na_{},{}'.format(p, s), cat='Integer', lowBound=0)
    for s in range(semester_number)]
    for p in [0, 1]]
# na_ps

c = [[
    LpVariable('c_{},{}'.format(i, s), cat='Integer', lowBound=0)
    for s in semesters]
    for i in [1, 2]]
# c_is

eta = [[[
    LpVariable('eta_{},{},{}'.format(s, a, i), cat='Integer', lowBound=0)
    for i in [0, 1] ]
    for a in range(1, s) ]
    for s in range(1, semester_number)]
# eta_s,a,i

V = [0] + [[[
    LpVariable('V_{},{},{}'.format(s, a, i), cat='Integer', lowBound=0)
    for i in [0, 1]]
    for a in range(1, s)]
    for s in range(1, semester_number)]
# V_s,a,i

delta = [[
    LpVariable('delt_{},{}'.format(s, i), cat='Binary', lowBound=0)
    for i in [0, 1] ]
    for s in range(1, semester_number+1)]
# delta_s,i

# Contraintes ################

# La quantité livrée doit être suffisante
for v in range(cities_number + 1):
    qtt = 0
    for s in semesters:
        qtt += costs.compute_quantity(v, n1, n2, na, s)
        problem += qtt >= requests[s][v]

# L'entreprise possède 10 camions au départ (contrainte d'initialisation)
problem += c[0][0] == 4
problem += c[1][0] == 6

for p in [0, 1]:
    for v in range(1, cities_number):
        for s in range(semester_number):
            problem += (t[v] - (1 / N) * n2[p][v][s][1] >= 0, 'trajet {}+a non faisable {},{}'.format(v, s, p))

for s in semesters:
    for i in [0, 1]:
        if i == 0:
            problem += ((lpSum(n1[p][v][s] for p in [0, 1]
                               for v in range(cities_number)) + 3) <= business_days_by_semester * c[i][s],
                        'net type 1, {}'.format(s))
        else:
            problem += ((lpSum(n2[p][v][s][a] for p in [0, 1]
                               for v in range(1, cities_number)
                               for a in [0, 1]) + lpSum(na[p][s] for p in [0, 1]) + 3) <= business_days_by_semester * \
                        c[i][s], 'net type 2, {}'.format(s))


for p in [0, 1]:
    for v in range(cities_number):
        problem += n1[p][v][0] == 0  # Le semestre 0 est celui avant le début des trajets, on ne comptabilise pas de course
        problem += na[p][0] == 0
    for a in [0, 1]:
        for v in range(1,cities_number):
            problem += lpSum(n2[p][v][0][a]) == 0


for s in range(1, semester_number-1):
    for i in [0, 1]:
        for a in range(1, s-1):
            problem += eta[s][a][i] == eta[s-1][a-1][i] - V[s][a][i]
        problem += lpSum(eta[s][a][i] for a in range(s)) == c[i][s]     # Force la somme des eta_s,a,i

for s in range(1, semester_number):
    for i in [0, 1]:
        problem += c[i][s] - c[i][s-1] >= delta[1][i]*N*-1
        problem += delta[2][i]*N*-1 <= c[i][s] - c[i][s-1] + lpSum(V[s][a][i] for a in range(0, s-1))
        problem += c[i][s-1] - c[i][s] - lpSum(V[s][a][i] for a in range(0, s-1)) >= delta[3][i]*-1*N
        problem += c[i][s-1] - c[i][s] >= delta[4][i]*-1*N
        problem += delta[5][i]*N <= lpSum(V[s][a][i] for a in range(0, s-1))
        problem += delta[1][i] + delta[2][i] <= 1
        problem += delta[1][i] + delta[3][i] <= 1
        problem += delta[4][i] + delta[5][i] <= 1


# Fonction objective ##############

problem += costs.maintainance(lpSum(c[i][s] for i in [0, 1]
                                    for s in semesters)) + \
           costs.salary(v_moy, na, n1, n2, semesters, cities_number, road_distances1, road_distances2) + \
           costs.fuel(fuel_price, conso, n1, n2, na, road_distances1, road_distances2, cities_number, semesters) + \
           costs.buying_trucks(c) + \
           costs.amortissement(V)


problem.solve(solver=GLPK(msg=True, keepFiles=True, timeLimit=30))

data = problem.toDict()


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


json_content = json.dumps(data, indent=4, cls=NpEncoder)

with open("jason_data.json", "w") as outfile:
    outfile.write(json_content)
