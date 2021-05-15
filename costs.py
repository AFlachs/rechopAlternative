from pulp import lpSum


def compute_qtt_liege(s, n1, n2, na):
    res = 16.5 * n1[1][0][s] \
          + 5.5 * lpSum(n2[0][v][s][1]
                        for v in range(1, 5)) \
          + 16.5 * lpSum(n2[1][v][s][1]
                         for v in range(1, 5)) \
          + 5.5 * na[0][s] \
          + 16.5 * na[1][s]
    return res


def compute_qtt_anvers(s, n1, na):
    res = 16.5 * n1[0][0][s] \
          + 16.5 * na[0][s] \
          + 5.5 * na[1][s]
    return res


def compute_quantity(ville, n1, n2, na, s):
    print("s=" + str(s))
    print("ville=" + str(ville))
    res = 0
    if ville == 0:
        res = compute_qtt_anvers(s, n1, na)
    elif ville == 5:
        res = compute_qtt_liege(s, n1, n2, na)
    else:
        res += 16.5 * n1[0][ville][s] \
               + 16.5 * lpSum(n2[0][ville][s][a]
                              for a in [0, 1]) \
               + 5.5 * lpSum(n2[1][ville][s][a]
                             for a in [0, 1])
    return res


def total_distance(v, s, d1, d2, n1, n2, na):
    """
    Distance totale pour une ville à un semestre
    :param v:
    :param s:
    :param d1: road_distances1
    :param d2: road_distances2
    :param n1:
    :param n2:
    :param na:
    :return:
    """
    if v == 0:
        return sum(na[p][s] * d1[0] for p in [0, 1])
    else:
        return sum(
            (n1[p][v][s] + n2[p][v][s][0]) * d1[v] + n2[p][v][s] * d2[v] for p in [0, 1]
        )


def fuel(fuel_price, conso, n1, n2, na, d1, d2, cities_number, semesters):
    return sum(fuel_price * conso * total_distance(v, s, d1, d2, n1, n2, na)
               for v in range(cities_number)
               for s in semesters)


def maintainance(n):
    return 1000 * n


def salary(V, na, n1, n2, semesters, cities_number, d1, d2):
    alpha = 13
    res = 0
    for s in semesters:
        for v in range(cities_number):
            res += total_distance(v, s, d1, d2, n1, n2, na) / V
        for p in [0, 1]:
            res += na[p][s]
            for v in range(1, cities_number):
                res += n1[p][v][s]
                for a in [0, 1]:
                    res += 2 * n2[p][v][s][a]
    return res * alpha


def buying_trucks(c):
    res = 0
    for i in [0, 1]:
        if i == 0:
            res += 40000 * c[i][10]
        else:
            res += 50000 * c[i][10]
    return res


def amortissement(V, semester_number):
    res = 0
    for s in range(1, semester_number):
        for a in range(1, s):
            for i in [0, 1]:
                res += V[s][a][i]
    return res
