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

    nEssai = 1
    while True:
        if trace : print(f"Essai n°{nEssai}")
        enigme = []
        for c in encJeu:
            if len(c[1])>1: # plusieurs arêtes possibles
                p = 0.5 - nEssai/(1+nEssai) # proba d'en prendre 2
                if rd.random() < p:
                    enigme.extend(rd.choices(c[1], k=2))
                else: # on n'en prend qu'une !
                    enigme.extend(rd.choices(c[1], k=1))
            else: # une seule arête à dessiner
                p = 0.6 + 0.4 * nEssai/(1+nEssai) - 1/n #  à ajuster par l'expérience ...
                if rd.random() < p:
                    enigme.extend(c[1])

        enigme = list(set(enigme))
        # lancement de la résolution
        lres = doSolve(enigme, n)
        # une seule solution complète ?
        if (len(lres) == 1) and not (-1 in lres[0]):
            break
        nEssai+=1
    return (enigme, konfig, encSol)




# %% test
""" 
#--------- génération auto version 1 ----------

import time

n = 6
start = time.monotonic()
enigme, konf, sol = randomEnigma(n, trace = True)
print(f"durée de la génération d'une énigme de taille {n} : {time.monotonic()-start} s")
# recherche de la solution de l'énigme
from calisson import test_solver
test_solver(enigme, n)

# -----------------------------
"""

# %% gen 2 : Tentative de nouvelle génération
"""
principe :
- modif des fonctions d'encodage (cf calisson.py) qui retourne maintenant la liste des arêtes en 2D et en 3D
- Pour générer une énigme :
  + tirage d'un empilement au hasard
  + encodage des arêtes
  + on tire au hasard une arête 3D pour chaque cube visible
  + dans  une matrice initialement remplie de -1, on tente de placer chacune des arêtes tirées en modifiant la matrice
    pour tenir compte des contraintes. L'arête est conservée dans l'énigme si elle modifie la matrice.
    (si elle ne modifie pas la matrice, c'est qu'elle est inutile pour la résolution :-)

Ça ne donne pas des résultats fondamentalement différents de la technique précédente ...

********************* ATTENTION *****************************
la fonction suivante (randomEnigma_bis) est incomplète : 
la résolution de l'énigme générée peut retourner retourner plusieurs résultats, dont certains
cubes peuvent être indéterminés.

En attente de suppresion ou d'amélioration ...

****** !!!!!!! NE PAS UTILISER EN L'ÉTAT !!!!!!! *******************

"""
from calisson import placeSommet
def randomEnigma_buggee(n, trace = False):
    konfig = make_random_config(n)
    # conversion en matrice 3D
    jeu = matrice_jeu(konfig)
    # encodage 2D des arêtes
    encJeu = encodage(jeu)
    # encodage de la solution sous la même forme que l'énigme
    encSol = encodeSolution(encJeu)

    M = -np.ones((n, n, n), dtype='int')

    ar3 = [rd.choices(list(zip(e[1], e[2])), k=1)[0] for e in encJeu]

    enig = []

    for ar in ar3:
        Mp = M.copy()
        args = list(ar[1])
        args.append(Mp)
        r, Mp = placeSommet(*args)
        if not(np.all(np.equal(Mp, M))):
            if trace : print(f'Changement pour {ar}')
            enig.append(ar[0])
        else:
            if trace : print(f'Pas de changement pour {ar}')
        M = Mp

    return enig

"""test 

n = 6
enigme = randomEnigma_bis(n)
test_solver(enigme, n)

"""

# %% Genération version 3 : en ne partant pas d'un empilement, mais créant une grille à partir de contraintes
import time

def randomEnigma_fromConstraints(n, trace = False):
    start = time.monotonic()

    # la liste qui sera retournée
    enig = []
    if trace : print(f"Génération d'une énigme de taille {n}")
    if trace : print("élimination des cubes indéterminés")    
    while True:
        rs = doSolve(enig, n) # la liste des Résultats de la réSolution

        rsf = list(filter(lambda m : -1 in m, rs)) # la liste des résultats contenant dess cubes indéterminés
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
    return enig

# %% Test
"""

n = 5
enigme = randomEnigma_fromConstraints(n, True)
rs = test_solver(enigme, n)

"""


# %%
