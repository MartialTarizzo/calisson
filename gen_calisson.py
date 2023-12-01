# %% Jeu du calisson
# gen_calisson.py : fonctions de génération automatique d'énigme
#
# ============================================================================
# Auteur : Martial Tarizzo
#
# Licence : CC BY-NC-SA 4.0 DEED
# https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr
# ============================================================================


import math
import random as rd
import numpy as np

from calisson import projection, doSolve, encodage, encodeSolution, test_solver

# %% Section 1 : génération d'un empilement
# --------------------------------------------
"""
représentation de l'empilement des petits cubes dans un grand cube de côté n :
liste de n**2 élements, représentant le nombre de petits cubes empilés
au dessus du carré de coordonnées (i,j) dans le plan horizontal.
L'index du carré (i,j) dans la liste est i * n + j , i=0..n-1, j=0..n-1
le carré (0,0) est le plus éloigné de l'observateur, base i,j,k directe
"""


# génération d'une configuration contenant nbCubes dans un grand cube de côté n
# La config est obtenue en ajoutant les cubes un à un à partir de la config vide,
# et en prenant une config au hasard à chaque étape.
def make_config(n, nbCubes):
    # le jeu, vide de tout cube
    def kVide(n):
        return [0]*n**2

    def ajouteCube(k):
        """retourne la liste de toutes les configurations de jeu possibles en
        ajoutant un cube à la configuration k fournie en argument."""
        l = []
        for i in range(n):
            for j in range(n):
                hok = k[i * n + j] < n
                iok = i > 0 and k[(i - 1) * n + j] > k[i * n + j]
                jok = j > 0 and k[i * n + j - 1] > k[i * n + j]
                # print(i,j,hok,iok,jok)
                if i == 0:
                    if j == 0:
                        ok = hok
                    else:
                        ok = hok and jok
                else:
                    if j == 0:
                        ok = hok and iok
                    else:
                        ok = hok and iok and jok
                if ok:
                    newk = k.copy()
                    newk[i * n + j] = newk[i * n + j] + 1
                    l.append(newk)
        return l

    k = kVide(n)
    f = 1   # pour estimer le nombre de façons différentes d'empiler les nbCubes
    for i in range(nbCubes):
        lk = ajouteCube(k)
        m = len(lk)
        f *= m
        k = rd.choice(lk)
    return k, f

# La représentation précédente (matrice n x n) de l'empilement est commode pour le générer,
#  mais n'est pas commode pour le tracé et la résolution.
# On va changer pour une matrice de dimension 3 : n x n x n
# Les arêtes des petits cubes sont donc de longueur 1.
# Chaque élément de la matrice est un entier dans {-1,0,+1} indiquant l'état
# d'un petit cube dont l'origine a pour coordonnées le point (i,j,k)
# état : -1 -> état inconnu, 0 -> cube absent, +1 -> cube présent

# Passage de la représentation compacte à la matrice de dimension 3
def matrice_jeu(konfig):
    # jeu est la matrice de taille n**3 obtenue à partir de la configuration k
    n = math.isqrt(len(konfig))
    jeu = np.zeros([n, n, n], dtype='int')
    for i in range(n):
        for j in range(n):
            for k in range(konfig[n*i+j]):
                jeu[i, j, k] = 1
    return jeu

def make_random_config(n, nbCubes = 0, trace = False):
    """
    retourne une configuration aléatoire pour un jeu
    de dimension n contenant m cubes
    """
    # nombre de cubes dans la configuration, tiré au hasard entre n^3/3 et n^3/2 si non fourni
    if nbCubes == 0:
        nbCubes = rd.randint(n**3//3, 2*n**3//3)
        if trace: print(f"on a {nbCubes} cubes dans la configuration")

    k, f = make_config(n, nbCubes)
    if trace : print(k, f)
    return k

# %% section 2 : Génération d'un énigme

def randomEnigma(n, konfig = [], trace = False):
    """
    Pour une dimension de jeu valant n, génération d'un empilement, d'une énigme et de la solution.
    konfig est une matrice de dimension 2 (n x n) représentant un empilement (cf section 1)

    Retourne l'énigme, la configuration de l'empilement et la solution
    L'énigme et la solution sont sous la forme d'une liste de triplets (X,Y,direction) précisant
    les arêtes à dessiner dans la zone de jeu.

    La durée d'exécution de la fonction peut être assez longue si n est grand car l'énigme retournée
    est nécessairement correcte : solution unique sans indétermination.
    Ceci est assuré à l'aide d'une méthode basique essai/erreur :
    - génération aléatoire de l'énigme
    - tentative de résolution

    L'énigme n'est pas nécessairement 'subtile', aucun indice de difficulté n'est actuellement
    implémenté...
    Ça donne parfois (souvent) des énigmes assez faciles, ayant trop de segments,qu'on peut alors
    retoucher :
    - imprimer l'énigme
    - modifier/supprimer des segments
    - résoudre l'énigme retouchée pour voir si ça marche
    - recommencer jusqu'à satisfaction !
    """
    # création d'un empilement aléatoire
    if konfig == []:
        konfig = make_random_config(n)
    # conversion en matrice 3D
    jeu = matrice_jeu(konfig)
    # encodage 2D des arêtes
    encJeu = encodage(jeu)
    # encodage de la solution sous la même forme que l'énigme
    encSol = encodeSolution(encJeu)

    # tirage de l'énigme
    # idée :
    # - pour chaque cube visible ayant plusieurs arêtes, en prendre une ou deux au hasard
    #   selon la proba p
    # - si le cube n'a qu'une arête visible, proba p d'être sélectionnée pour éviter
    #   d'avoir de longues lignes en cas d'empilement de cubes pour lesquels une seule
    #   arête est visibles (cubes alignés verticalement en colonne par ex.)
    #
    # les probas p calculées dépendent de la taille du jeu et du nombre d'essais de
    # résolution. Plus la résolution est difficile (n grand, nombre d'essais grand)
    # plus la proba d'ajouter des arêtes dans l'énigme augmente.
    #
    # On vérifie que l'énigme ne possède qu'une seule solution sans indétermination.

    enigme = []
    for c in encJeu:
        if len(c[1])>1: # plusieurs arêtes possibles
            p = 0.25 # proba d'en prendre 2
            if rd.random() < p:
                enigme.extend(rd.choices(c[1], k=2))
            else: # on n'en prend qu'une !
                enigme.extend(rd.choices(c[1], k=1))
        else: # une seule arête à dessiner
            p = 0.8 - 1/n #  à ajuster par l'expérience ...
            if rd.random() < p:
                enigme.extend(c[1])

    enigme = list(set(enigme))

    # comme il est peu probable que l'énigme soit correcte, on fait une génération 
    # par contrainte pour compléter la grille
    enigme = randomEnigma_fromConstraints(n, trace, enigme)
    
    return enigme




# %% test
""" 
#--------- génération auto version 1 ----------

import time

n = 8
start = time.monotonic()
enigme = randomEnigma(n, trace = True)
print(enigme)
print(f"durée de la génération d'une énigme de taille {n} : {time.monotonic()-start} s")
# recherche de la solution de l'énigme
from calisson import test_solver
test_solver(enigme, n)
test_solver(enigme, n+1)
enigme = randomEnigma_fromConstraints(n+1, True, enigme)
test_solver(enigme, n+1)



# -----------------------------
"""


# %% Genération version 3 : en ne partant pas d'un empilement, mais créant une grille à partir de contraintes

import time

# L'idée ici est de partir des contraintes (-> les segments de l'énigme) pour générer la grille.
# En partant d'une énigme vide, on effectue une boucle calculant les petits cubes indéterminés (au départ, ils le sont tous !)
# puis en ajoutant une arête au hasard pour lever les indéterminations.
# Une fois tous les cubes déterminés, il se peut qu'il existe plusieurs solutions. On ajoute alors des arêtes
# permettant de sélectionner une seule solution.

# rem : ajout de l'argument par défaut enig pour permettre l'utilisation de cette fonction 
# par la fonction qui suit (randomEnigma_fromConstraints_incremental)
def randomEnigma_fromConstraints(n, trace = False, enig = []):
    start = time.monotonic()

    # la liste qui sera retournée
#    enig = []
    if trace : print(f"Génération d'une énigme de taille {n}")
    if trace : print("élimination des cubes indéterminés")    
    while True:
        rs = doSolve(enig, n) # la liste des Résultats de la réSolution

        rsf = list(filter(lambda m : -1 in m, rs)) # la liste des résultats contenant des cubes indéterminés
        if len(rsf) == 0:
            break       # fin de la première phase
        
        # On prend une config au hasard, avec indétermination
        M = rd.choice(rsf)

        # on calcule l'origine (en projection 2D) de tous les cubes indéterminés
        lci = []
        for x in range(n):
            for y in range(n):
                for z in range(n):
                    if M[x, y, z] == -1:
                        lci.append(tuple(projection((x,y,z))))
        # élimination des doublons
        lci = list(set(lci)) 

        # choix au hasard de l'origine d'un cube indéterminé et de la direction de l'arête
        ci = list(rd.choice(lci))
        cid = rd.choice(["x","y","z"])
        
        # ajout de l'arête à l'énigme
        ci.append(cid)
        enig.append(tuple(ci))
        if trace : print(f"nombre d'arêtes dans l'enigme : {len(enig)}")

    if trace : print(f'durée phase 1 : {time.monotonic()-start} s ({len(rs)} solution(s))')

    # le résultat de la résolution ne contient plus d'indétermination, mais il peut y avoir plusieurs solutions.
    # Idée : si on a plusieurs solutions, on calcule la différence entre les ensembles des arêtes de la deuxième 
    # et de la première solution (arêtes dans la deuxième mais pas dans la première).
    # On en choisit alors une au hasard qu'on ajoute à l'énigme  afin de lever l'ambiguïté.
    # On relance la résolution sur la nouvelle énigme et on recommence tant qu'il existe plusieurs solutions.
    if trace : print("élimination des solutions multiples")    
    while len(rs)>1:
        # calcul de la différence ensembliste des arêtes
        ars = set(encodeSolution(encodage(rs[1]))) - set(encodeSolution(encodage(rs[0])))
        # choix d'une arête au hasard
        ar = rd.choice(list(ars))
        # ajout à l'énigme
        enig.append(ar)
        if trace : print(f"nombre d'arêtes dans l'enigme : {len(enig)}")
        # on relance la résolution
        rs = doSolve(enig, n)

    # fini : on a une solution unique !
    if trace : print(f'durée totale : {time.monotonic()-start} s')

    # pour la justification des lignes suivantes : 
    # un argument nommé ayant une valeur par défaut mutable 
    # retient cette valeur entre les appels de la fonction ...
    # (voir https://stackoverflow.com/questions/16549768/lifetime-of-default-function-arguments-in-python par ex.)
    r = enig.copy()
    # on remet les args par défaut à leurs valeurs correctes
    randomEnigma_fromConstraints.__defaults__ = (False, [])
    return r

# Expérimentalement, pour les grilles de grande dimension (>4), la durée d'exécution de la fonction peut
# devenir assez importante. Dans la fonction précédente, la première phase d'élimination des cubes indéterminés
# est celle qui prend le plus de temps.
# D'où l'idée de réduire les calculs lors de cette phase en limitant le nombre de cubes indéterminés 
# de la façon suivante :
# pour calculer une grille de taille n, on place au centre une grille de taille (n-1) d'énigme (et donc de solution)
# connue. Les seuls cubes indéterminés se retrouveront donc sur la frontière de la grille à calculer.
# En pratique, cela se révèle nettement plus rapide, et fournit des grilles difficiles et denses !
def randomEnigma_fromConstraints_incremental(n, trace = False):
    if n < 5:
        return randomEnigma_fromConstraints(n, trace)
    enigme = randomEnigma_fromConstraints(4, trace)
    for nn in range(n - 4):
        enigme = randomEnigma_fromConstraints(5 + nn, trace, enigme)
    return enigme


# %% Test
"""

deb = time.monotonic()
# n = 4
# enigme = randomEnigma_fromConstraints_incremental(n, True)

# n = 5
# enigme = randomEnigma_fromConstraints_incremental(n, True)

n = 7
enigme = randomEnigma_fromConstraints_incremental(n, True)

# n = 8
# enigme = randomEnigma_fromConstraints_incremental(n, True)

print('======>' , time.monotonic() - deb)

rs = test_solver(enigme, n)

"""

# %% une taille 5 super jolie
"""
enigme = [(0, -2, 'x'),
 (2, -4, 'y'),
 (-1, 1, 'x'),
 (1, 1, 'y'),
 (-3, -1, 'y'),
 (1, -3, 'x'),
 (0, 4, 'x'),
 (-2, -4, 'x'),
 (0, 6, 'z'),
 (0, 0, 'y'),
 (3, 1, 'x'),
 (1, 3, 'z'),
 (-1, 5, 'y'),
 (-3, 1, 'x'),
 (-4, -2, 'z'),
 (4, -2, 'z'),
 (-1, -5, 'z'),
 (2, -2, 'y'),
 (-3, 3, 'x')]
test_solver(enigme, 5)
"""