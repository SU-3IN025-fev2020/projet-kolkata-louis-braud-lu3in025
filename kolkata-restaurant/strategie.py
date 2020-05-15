import random
import math

def strategie_aleatoire(nb_restaurant):
    return random.randint(0, nb_restaurant - 1)

def strategie_tetu(indice, nb_restaurant):
    return indice % nb_restaurant

def strategie_restaurant_proche(position, restaurants):
    x1, y1 = position
    var = math.inf
    res = None
    for i in range (len(restaurants)):
        x2, y2 = restaurants[i]
        distance = abs(x1 - x2) + abs(y1 - y2)
        if distance < var:
            var = distance
            res = i
    return res



