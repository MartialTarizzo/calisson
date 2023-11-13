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

from calisson import projection, doSolve, encodage, encodeSolution

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




# %% test : décommenter cette section ##
"""
#--------- génération auto----------
n = 6
enigme, konf, sol = randomEnigma(n, trace = True)

# recherche de la solution de l'énigme
from calisson import test_solver
test_solver(enigme, n)
# -----------------------------
"""