# -*- coding: utf-8 -*-

# Nicolas, 2020-03-20

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo

import random 
import numpy as np
import sys

import aStar
from aStar import Noeud
import strategie
import queue

    
# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'kolkata_6_10'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 10  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 2 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()

    #-------------------------------
    # Initialisation
    #-------------------------------
    nbLignes = game.spriteBuilder.rowsize
    nbColonnes = game.spriteBuilder.colsize
    print("lignes", nbLignes)
    print("colonnes", nbColonnes)
    
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    
    # on localise tous les objets  ramassables (les restaurants)
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
    nbRestaus = len(goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    print ("Wall states:", wallStates)
    
    # on liste toutes les positions permises
    allowedStates = [(x,y) for x in range(nbLignes) for y in range(nbColonnes)\
                     if (x,y) not in (wallStates + goalStates)]

    dansRestaus = {r:[] for r in range(nbRestaus)}

    taux = [0 for i in range(nbRestaus)]

    gain = [0 for i in range(nbPlayers)]

    restau = [0] * nbPlayers

    posPlayers = initStates
    
    #-------------------------------
    # Placement aleatoire des joueurs, en évitant les obstacles
    #-------------------------------

    for i in range(iterations):
        for j in range(nbPlayers):
            x,y = random.choice(allowedStates)
            players[j].set_rowcol(x,y)
            game.mainiteration()
            posPlayers[j]=(x,y)
    
    #-------------------------------
    # chaque joueur choisit un restaurant
    #-------------------------------

        for j in range(nbPlayers):
            if j % 2 == 0:
                c = strategie.strategie_aleatoire(nbRestaus)
            elif j == 1 or j == 3 or j == 5:
                c = strategie.strategie_tetu(j, nbRestaus)
            else:
                c = strategie.strategie_restaurant_proche(posPlayers[j], goalStates)
            restau[j]=c
            dansRestaus[c].append(j)

    #-------------------------------
    # Boucle principale de déplacements 
    #-------------------------------

        for j in range(nbPlayers):
            pos_restau = goalStates[restau[j]]
            chemin = aStar.aStar(posPlayers[j], pos_restau, wallStates)
            print(chemin)
            while posPlayers[j] != pos_restau:
                row, col = queue.heappop(chemin)
                players[j].set_rowcol(row, col)
                print ("Position du joueur : ", j, row, col)
                game.mainiteration()
                posPlayers[j]= (row,col)
                if (row,col) == pos_restau:
                    game.mainiteration()
                    print ("Le joueur ", j, " est arrivé")           
                    break

        for i in range(nbRestaus):
            if len(dansRestaus[i]) == 1 :
                j = dansRestaus[i][0]
                gain[j] += 1
            elif len(dansRestaus[i]) > 1 :
                j = random.choice(dansRestaus[i])
                gain[j] += 1
            taux[i] = len(dansRestaus[i])/nbPlayers
            print("Taux du restaurant ",i," : ", taux[i])
        dansRestaus = {r:[] for r in range(nbRestaus)}

    for i in range(len(gain)):
        print("Le gain du joueur ",i," est : ", gain[i]/iterations)
        
    pygame.quit()


if __name__ == '__main__':
    main()
    


