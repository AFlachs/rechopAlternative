import numpy as np
import math


# cities_list = ["Anvers", "Charleroi", "Gand", "Bruxelles", "Hasselt", "Liege"]
def introduce_distances():
    distances = np.array(
        [   # Anvers    Charleroi   Gand    Bruxelles   Hasselt     Liege
            [0,        100,        40,     45,         50,         105],
            [0,        0,          100,    60,         80,         100],
            [0,        0,          0,      40,         60,         140],
            [0,        0,          0,      0,          50,         100],
            [0,        0,          0,      0,          0,          60 ],
            [0,        0,          0,      0,          0,          0  ],
        ]
    )
    distances += distances.transpose()
    return distances


def introduce_roads_distances():
    distances = introduce_distances()
    distances_1 = [2 * distances[i][5] for i in range(5)]  # Distance Liege - Ville - Liège
    distances_2 = [0] + [ distances[i][5] + distances[0][5] + distances[0][i] for i in range(1, 5)]
    # Distance Liège - Ville - Anvers - Liège, on considère pas anvers dedans
    return distances_1, distances_2


def introduce_roads_feasibility(v_moy, work_time):
    distances = introduce_distances()
    feasibility = np.zeros(5)  # Faisabilité des trajets passant par anvers et une ville
    for i in range(1, len(feasibility)):
        if ((distances[i][5] + distances[i][0] + distances[0][5]) / v_moy) + 2 < work_time:  # On ajoute 2 heures d'attente dans les villes
            feasibility[i] = 1
    return feasibility


def introduce_city_requests():
    # Tableau ayant une dimension "temps" (il en faut 10, 1 par semestre) et une dimension
    # villes, puis le remplir correctement
    city_requests = np.array(
        [   # Anvers    Charleroi   Gand    Bruxelles   Hasselt     Liege
            [0,         0,          0,      0,          0,          0],
            [0,         0,          0,      0,          0,          0],
            [9000,      12000,      2000,   6200,       350,        30000],
            [9000,      12000,      2000,   6200,       1650,       30000],
            [18000,     24000,      4000,   12400,      2000,       60000],
            [18000,     24000,      4000,   12400,      2000,       60000],
            [27000,     36000,      6000,   18600,      2350,       90000],
            [27000,     36000,      6000,   18600,      2350,       90000],
            [36000,     48000,      8000,   24800,      2700,       120000],
            [36000,     48000,      8000,   24800,      2700,       120000],
            [45000,     60000,      10000,  31000,      3050,       150000],
        ]
    )
    return city_requests


def introduce_selling_cost(d_r, b_p_1, b_p_2):
    selling_cost = np.array(
        [
            # camion de type 1
            [b_p_1*(1-math.pow(1/(1+d_r), i/2) for i in range(10)] + [ b_p_1*math.pow(1/(1+d_r), 5) ],
            # camion de type 2
            [math.pow(b_p_2/(1+d_r), i/2) for i in range(10)] + [ math.pow(b_p_2/(1+d_r), 5) ]
        ]
    )
    return selling_cost
