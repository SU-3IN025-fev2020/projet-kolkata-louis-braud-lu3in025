import queue

class Noeud():

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position  

def distManhattan(p1,p2):
    """ calcule la distance de Manhattan entre le tuple 
        p1 et le tuple p2
        """
    (x1,y1)=p1
    (x2,y2)=p2
    return abs(x1-x2)+abs(y1-y2) 

"""def aStar(debut, fin, obstacles):
    if debut == fin:
        return []
    liste_ouvert = queue.PriorityQueue()
    liste_ouvert.put((0, debut))
    liste_ferme = {}
    liste_ferme[debut] = None
    cout = {}
    cout[debut] = 0
    while not liste_ouvert.empty():
        (best, courant) = liste_ouvert.get()
        if courant == fin:
            break
        liste = []
        ligne, colonne = courant
        for positions in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_ligne = ligne + positions[0]
            new_colonne = colonne + positions[1]
            new_courant = (new_ligne, new_colonne)
            if ((new_courant not in obstacles) and new_ligne > 1 and new_colonne > 1 and new_ligne < 20 and new_colonne < 20):
                liste.append(new_courant)
        for i in liste:
            c = cout[courant] + 1
            if i not in cout or c < cout[i]:
                cout[i] = c
                best = c + distManhattan(fin, debut)
                liste_ouvert.put((best, i))
                liste_ferme[i] = courant
    courant = fin
    chemin = []
    while courant != debut:
        chemin.append(courant)
        courant = liste_ferme[courant]       
    chemin.reverse()
    return chemin"""

def aStar(debut, fin, obstacles):
    debut_noeud = Noeud(None, debut)
    debut_noeud.g = debut_noeud.h = debut_noeud.f = 0
    fin_noeud = Noeud(None, fin)
    fin_noeud.g = fin_noeud.h = fin_noeud.f = 0
    liste_ouvert = []
    liste_ferme = []
    liste_ouvert.append(debut_noeud)
    while len(liste_ouvert) > 0 :
        courant_noeud = liste_ouvert[0]
        courant_index = 0
        for index, noeud in enumerate(liste_ouvert):
            if noeud.f < courant_noeud.f:
                courant_noeud = noeud
                courant_index = index
        liste_ouvert.pop(courant_index)
        liste_ferme.append(courant_noeud)
        if courant_noeud == fin_noeud:
            chemin = []
            courant = courant_noeud
            while courant is not None:
                chemin.append(courant.position)
                courant = courant.parent
            return chemin[::-1]
        voisins = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            voisin = (courant_noeud.position[0] + new_position[0], courant_noeud.position[1] + new_position[1])
            #if voisin in obstacles:       
               # continue 
            if voisin[0] < 1 or voisin[0] > 19 or voisin[1] < 1 or voisin[1] > 19:
                continue
            nouveau_noeud = Noeud(courant_noeud, voisin)
            voisins.append(nouveau_noeud)
            
        for enfant in voisins:
            for i in liste_ferme:
                if enfant == i:
                    continue
            enfant.g = courant_noeud.g + 1
            enfant.h = ((enfant.position[0] - fin_noeud.position[0]) ** 2) + ((enfant.position[1] - fin_noeud.position[1]) ** 2)
            enfant.f = enfant.g + enfant.h
            for i in liste_ouvert:
                if enfant == i and enfant.g > i.g:
                    continue
            liste_ouvert.append(enfant)