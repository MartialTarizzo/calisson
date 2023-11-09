import math
import random as rd
import numpy as np

from calisson import projection

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

# Changement de modélisation de la configuration pour faciliter le tracé
# La section 1 représente le jeu par une matrice n x n.
# Cette représentation compacte n'est pas commode pour le tracé.
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

def make_random_config(n):
    """
    retourne une configuration aléatoire pour un jeu
    de dimension n
    """
    # nombre de cubes dans la configuration
    nbCubes = rd.randint(n**3//3, 2*n**3//3)
    print(f"on a {nbCubes} cubes dans la configuration")

    k, f = make_config(n, nbCubes)
    print(k, f)
    return k

# %% Génération d'un énigme
"""
idée : reprendre le code de dessin, mais encoder les arêtes plutôt que de les dessiner
"""
# encodage d'un petit cube de coordonnées 3D [i,j,k]
# On tient compte de l'environnement du cube pour n'encoder que les arêtes
# nécessaires.
def encodeCube(jeu, i, j, k):
    """
    jeu : matrice 3D représentant l'empilage de cubes
    i,j,k : coordonnées 3D de l'origine du petit cube

    retourne la liste des arêtes visibles dans la configuration du jeu, avec la
    syntaxe pour chaque arête correspondant à celle de l'énigme :
    (X, Y, d) <-> coordonnées 2D et direction de l'arête
    """
    n = jeu.shape[0]
    def c(i, j, k):
        """ test de la présence d'un cube aux coordonnées [i,j,k]
        Avec prise en compte des bords pour contrôler le tracé des arêtes.
        """
        if i < 0 or j < 0:
            return True
        if k < 0:
            return True
        if k == n:
            return False
        if i == n or j == n:
            return False
        return jeu[i, j, k]  # on n'est pas sur un bord

    # la liste des arêtes 3D retournées pour le cube courant
    lar = []

    if jeu[i, j, k] == 1: # cube certain

        # SA est le sommet d'origine du cube, jamais visible.
        # S1 .. S7 désigne les 7 sommets potentiellement visibles
        # S1..S4 sont les 4 sommets de la face supérieure
        # S5..S7 sont les 3 sommets de la face inférieure
        # on n'encode les lignes entre les différents sommets que si
        # elles sont nécessaires, ce qui dépend de la présence des autres cubes
        # au voisinage du cube courant.
        # L1 : ligne entre S1 et S2
        if c(i, j-1, k+1) and not c(i, j, k+1):
            lar.append((i,j,k+1,"x"))
        # L2 : S2-S3
        if not c(i+1, j, k) and not c(i, j, k+1):
            lar.append((i+1,j,k+1,"y"))
        # L3 : S3-S4
        if not c(i, j+1, k) and not c(i, j, k+1):
            lar.append((i,j+1,k+1,"x"))
        # L4 : S4-S1
        if not c(i, j, k+1) and c(i-1, j, k+1):
            lar.append((i,j,k+1,"y"))
        # L5 : S2-S5
        if not c(i+1, j, k) and c(i+1, j-1, k):
            lar.append((i+1,j,k,"z"))
        # L6 : S3-S6
        if (not c(i+1, j, k) and not c(i, j+1, k)) or \
                (c(i+1, j, k) and c(i, j+1, k) and not c(i+1, j+1, k)):
            lar.append((i+1,j+1,k,"z"))
        # L7 : S4-S7
        if not c(i, j+1, k) and c(i-1, j+1, k):
            lar.append((i,j+1,k,"z"))
        # L8 : S5-S6
        if not c(i+1, j, k) and c(i+1, j, k-1):
            lar.append((i+1,j,k,"y"))
        # L9 : S6-S7
        if not c(i, j+1, k) and c(i, j+1, k-1):
            lar.append((i,j+1,k,"x"))

    # conversion en 2D, en éliminant les arêtes tracées le long des bords du grand cube
    lar2 = []
    for (x,y,z,d) in lar:
        if not( # les arêtes suivantes sont le long du tracé de l'hexagone englobant->ne pas encoder
            (x==0 and ((z==n and d=='y') or (y==n and d=='z'))) or
            (y==0 and ((x==n and d=='z') or (z==n and d=='x'))) or
            (z==0 and ((y==n and d=='x') or (x==n and d=='y'))) ) :
            X,Y = projection([x,y,z])
            lar2.append((X,Y,d))

    return lar2

def encodage(jeu):
    """
    arg : jeu est la matrice 3D décrivant l'empilement
    la fonction retourne une liste de doublets (coord,liste_arêtes) pour tous les cubes
    dont certaines arêtes sont visibles.
    - coord est un triplet (i,j,k) donnant l'origine du cube
    - liste_arêtes est une liste contenant les arêtes correspondantes, sous la forme
      dans l'énigme (X, Y, d) <-> coordonnées 2D et direction de l'arête
    """
    lc = []
    n = jeu.shape[0]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                ec = encodeCube(jeu, i, j, k)
                if len(ec) != 0: # cube visible
                    # print(f'cube {i,j,k} visible : {ec}')
                    lc.append(((i,j,k),ec))
    return lc


def randomEnigma(n, konfig = []):
    # création d'un empilement aléatoire
    if konfig == []:
        konfig = make_random_config(n)
    # conversion en matrice 3D
    jeu = matrice_jeu(konfig)
    # encodage 2D des arêtes
    encJeu = encodage(jeu)

    # tirage de l'énigme
    # idée :
    # - pour chaque cube visible ayant plusieurs arêtes, en prendre une au hasard
    # - si le cube n'a qu'une arête visible, proba p d'être sélectionnée
    enigme = []
    p = 0.5
    for c in encJeu:
        if len(c[1])>1: # plusieurs arêtes
            enigme.extend(rd.choices(c[1], k=1))
        elif rd.random() > p:
            enigme.extend(c[1])

    enigme = list(set(enigme))
    return (enigme, konfig)


# %% tests
n=5
enigme, konf = randomEnigma(n)
print(enigme)

# représentation du jeu en cours
from calisson import draw_config
draw_config(matrice_jeu(konf))

from calisson import test_solver, listCoord3D, draw_config

test_solver(enigme, n)
