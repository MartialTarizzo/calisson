# %% Jeu du calisson
"""" Pour la présentation et les règles du jeu, cf https://mathix.org/calisson/blog/

Contrairement à la présentation par 'calissons', on adopte ici la modélisation
3D de l'empilement des cubes dans une zone de rangement cubique, dont le côté
est de taille n.
"""

# Imports pour la suite
import random as rd
import matplotlib.pyplot as plt
import numpy as np

# Taille de la zone de rangement des cubes
n = 5

# %% Section 1 : génération d'un empilement
# --------------------------------------------
"""
représentation de l'empilement des petits cubes :
liste de n**2 élements, représentant le nombre de petits cubes empilés
au dessus du carré de coordonnées (i,j) dans le plan horizontal.
L'index du carré (i,j) dans la liste est i * n + j , i=0..n-1, j=0..n-1
le carré (0,0) est le plus éloigné de l'observateur, base i,j,k directe
"""

# le jeu, vide de tout cube
def kVide():
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

# %% génération d'une configuration contenant nbCubes
# La config est obtenue en ajoutant les cubes un à un à partir de la config vide,
# et en prenant une config au hasard à chaque étape.
def make_config(nbCubes):
    k = kVide()
    f = 1   # pour estimer le nombre de façons différentes d'empiler les nbCubes
    for i in range(nbCubes):
        lk = ajouteCube(k)
        m = len(lk)
        f *= m
        k = rd.choice(lk)
    return k, f


# nombre de cubes dans la configuration
nbCubes = rd.randint(n**3//3, 2*n**3//3)
print(f"on a {nbCubes} cubes dans la configuration")

k, f = make_config(nbCubes)
print(k, f)
# %% Section 2 : Représentation graphique d'une configuration
# ------------------------------------------------------------

# sortie graphique sans interaction : on utilise pyplot pour faire simple

# Deux utilitaires


def line(A, B, **kwargs):
    """ trace une ligne dans le plan de figure entre les points A et B.
    Chaque point est représenté par un doublet [x, y] """
    plt.plot([A[0], B[0]], [A[1], B[1]], **kwargs)


def dot(A, size, **kwargs):
    """ dessine un point au point A """
    plt.scatter(*A, (size,), marker='o', **kwargs)

# Passage 3D -> 2D
def projection(A):
    """ formules de la projection orthographique.
    A est un point de l'espace 3D, défini par ses coordonnées [x,y,z]
    Retourne  les coordonnées de la projection de A dans le plan de figure
    """
    x, y, z = A[0], A[1], A[2]
    # return [1/np.sqrt(2) * (y - x), 1/np.sqrt(6) * (2 * z - (x + y))]
    #
    # La formule 'officielle' ci-dessus effectue la projection dans une base du
    # plan de figure orthonormée.
    # En omettant les facteurs d'échelle, il faudra fixer le rapport d'affichage
    # dans les fonctions de tracé pour compenser.
    # L'avantage est que le pointeur de souris dans la fenêtre de tracé
    # indique correctement les coordonnées utilisées pour le codage des énigmes
    return [y - x, 2 * z - (x + y)]


def lineproj(A, B, **kwargs):
    """ dessine la ligne entre les points 3D A et B dans le plan de projection
    """
    Ap = projection(A)
    Bp = projection(B)
    line(Ap, Bp, **kwargs)


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
    jeu = np.zeros([n, n, n], dtype='bool')
    for i in range(n):
        for j in range(n):
            for k in range(konfig[n*i+j]):
                jeu[i, j, k] = True
    return jeu


jeu = matrice_jeu(k)
# print(jeu)

# Dessin d'un petit cube de coordonnées 3D [i,j,k]
# On tient compte de l'environnement du cube pour le dessiner que les arêtes
# nécessaires.
# Le cube est dessiné en bleu s'il est correct, en gris si inderterminé
def projCube(jeu, i, j, k):
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

    if jeu[i, j, k] == 1: # cube certain
        # options de tracé des cubes certains
        opt = {'color': 'blue', 'linewidth': 3}

        # SA est le sommet d'origine du cube, jamais visible.
        # S1 .. S7 désigne les 7 sommets potentiellement visibles
        # S1..S4 sont les 4 sommets de la face supérieure
        # S5..S7 sont les 3 sommets de la face inférieure
        SA = np.array([i, j, k])
        S1 = np.array([0, 0, 1])+SA
        S2 = np.array([1, 0, 1])+SA
        S3 = np.array([1, 1, 1])+SA
        S4 = np.array([0, 1, 1])+SA
        S5 = np.array([1, 0, 0])+SA
        S6 = np.array([1, 1, 0])+SA
        S7 = np.array([0, 1, 0])+SA
        # on ne trace les lignes entre les différents sommets que si
        # la ligne est nécessaire, ce qui dépend de la présence des autres cubes
        # au voisinage du cube courant.
        # L1 : ligne entre S1 et S2
        if c(i, j-1, k+1) and not c(i, j, k+1):
            lineproj(S1, S2, **opt)
        # L2 : S2-S3
        if not c(i+1, j, k) and not c(i, j, k+1):
            lineproj(S2, S3, **opt)
        # L3 : S3-S4
        if not c(i, j+1, k) and not c(i, j, k+1):
            lineproj(S3, S4, **opt)
        # L4 : S4-S1
        if not c(i, j, k+1) and c(i-1, j, k+1):
            lineproj(S4, S1, **opt)
        # L5 : S2-S5
        if not c(i+1, j, k) and c(i+1, j-1, k):
            lineproj(S2, S5, **opt)
        # L6 : S3-S6
        if (not c(i+1, j, k) and not c(i, j+1, k)) or \
                (c(i+1, j, k) and c(i, j+1, k) and not c(i+1, j+1, k)):
            lineproj(S3, S6, **opt)
        # L7 : S4-S7
        if not c(i, j+1, k) and c(i-1, j+1, k):
            lineproj(S4, S7, **opt)
        # L8 : S5-S6
        if not c(i+1, j, k) and c(i+1, j, k-1):
            lineproj(S5, S6, **opt)
        # L9 : S6-S7
        if not c(i, j+1, k) and c(i, j+1, k-1):
            lineproj(S6, S7, **opt)
        # pour voir le dessin pas à pas. commenter pour un dessin rapide !
        # plt.pause(0.005)
    elif jeu[i, j, k] == -1:
        # options de tracé des cubes indéterminés
        opt_indet = {'color': 'gray', 'linewidth': 4}
        SA = np.array([i, j, k])
        S1 = np.array([0, 0, 1])+SA
        S2 = np.array([1, 0, 1])+SA
        S3 = np.array([1, 1, 1])+SA
        S4 = np.array([0, 1, 1])+SA
        S5 = np.array([1, 0, 0])+SA
        S6 = np.array([1, 1, 0])+SA
        S7 = np.array([0, 1, 0])+SA
        lineproj(S1, S2, **opt_indet)
        lineproj(S2, S3, **opt_indet)
        lineproj(S3, S4, **opt_indet)
        lineproj(S4, S1, **opt_indet)
        lineproj(S2, S5, **opt_indet)
        lineproj(S3, S6, **opt_indet)
        lineproj(S4, S7, **opt_indet)
        lineproj(S5, S6, **opt_indet)
        lineproj(S6, S7, **opt_indet)



# dessin de l'aire de jeu
def drawHex(n):
    """ tracé de l'hexagone qui représente la projection du grand cube
    de rangement """

    # les lignes intérieures
    opt = {'color': 'black', 'linestyle': 'dashed', 'linewidth': 1}
    for i in range(n+1):
        lineproj([0, 0, i], [n, 0, i], **opt)
        lineproj([0, 0, i], [0, n, i], **opt)
        lineproj([i, 0, 0], [i, n, 0], **opt)
        lineproj([0, i, 0], [n, i, 0], **opt)
        lineproj([i, 0, 0], [i, 0, n], **opt)
        lineproj([0, i, 0], [0, i, n], **opt)

    # le bord
    opt = {'color': 'red', 'linewidth': 4}

    lineproj([0, 0, n], [n, 0, n], **opt)
    lineproj([n, 0, n], [n, 0, 0], **opt)
    lineproj([n, 0, 0], [n, n, 0], **opt)
    lineproj([n, n, 0], [0, n, 0], **opt)
    lineproj([0, n, 0], [0, n, n], **opt)
    lineproj([0, n, n], [0, 0, n], **opt)

# dessin des axes non masqués par des cubes
def drawAxes(jeu):
    """
    Dessin des projections des axes 3D x, y ou z si pas de cube pour les cacher
    """
    n = jeu.shape[0]
    opt = {'color': 'blue', 'linewidth': 3}  # options de tracé des cubes
    for i in range(n):
        if not jeu[0, 0, i]:
            lineproj([0, 0, i], [0, 0, i+1], **opt)
        if not jeu[0, i, 0]:
            lineproj([0, i, 0], [0, i+1, 0], **opt)
        if not jeu[i, 0, 0]:
            lineproj([i, 0, 0], [i+1, 0, 0], **opt)

# tracé de la configuration
def draw_config(jeu):
    """
    dessine à l'aide de pyplot l'empilement de cubes codé en 3D dans jeu.
    """
    n = jeu.shape[0]
    plt.figure(figsize=(6, 6))
    # l'aspect sqrt(2/6) est nécessaire en raison de la simplification
    # du calcul des projections (cf fonction 'projection)
    plt.subplot(111,adjustable='box', aspect=1/np.sqrt(3))
    #plt.axis('equal')
    drawHex(n)
    drawAxes(jeu)
    for i in range(n):
        for j in range(n):
            for kk in range(n):
                projCube(jeu, i, j, kk)
    plt.show()

# représentation du jeu en cours
draw_config(jeu)

# %% Section 3 : RECHERCHE DE LA SOLUTION D'UNE ENIGME
#  ##########################

# --------------------------
# 3.1 : Codage d'une énigme
# --------------------------
# Évidemment, ce codage doit être exprimé en 2D dans le plan de la projection
# orthographique.
# On prend comme repère (O,X,Y) centré sur l'hexagone englobant l'empilement.
# OX horizontal, vecteur unité pour passer d'un colonne de points à la suivante
# OY vertical vecteur unité pour passer d'un ligne de points horiz.
# à la suivante.
# En raison de la projection, la base est orthogonale, mais pas normée !
# Exemple : le suivi d'une arête de face supérieure d'un petit cube fait varier
# X et Y d'un unité, le suivi d'une arête verticale fait varier et Y de 2 sans
# changer X.

# passage de (X,Y)->[((x,y,z), ...]
def listCoord3D(X, Y, n):
    """
    retourne la liste des coordonnées 3D (x,y,z) des points possibles pour un
    point (X,Y) dans le plan de projection.
    """
    r = []
    for x in range(n+1):
        z = (X+Y) // 2 + x
        y = X + x
        if (0 <= z <= n) and (0 <= y <= n):
            r.append([x, y, z])
    return r

#  Codage des arêtes
# L'ensemble des arêtes de l'énigme est codé ainsi :
# - coordonnées du point X,Y dans le plan de projection
# - chaîne de 1 à 3 caractères indiquant la présence d'une arête dans la direction
#   de la projection des axes 3D (x,y,z) à partir de (X,Y)
#   Ex : "x" -> arête dans la direction x
#        "zy" -> arêtes dans les directions y et z
#        "xyz" -> arêtes dans les 3 directions !
#
#   En projection, ça ressemble donc à une étoile Mercedes
#     |
#   (X,Y)
#   /   \
# L'énigme de la fin de la page
# https://mathix.org/calisson/blog/index.php?static2/regle
# est donc codée ainsi :
# ((0,2,"z"), (0,0,"x"), (1,1,"x"))

# --------------------------
# 3.2 : Résolution d'un énigme
# --------------------------
# codage du jeu :
# matrice M [i,j,k] représentant canoniquement la présence d'un petit cube
# dont l'origine est en (i,j,k)
# Trois valeurs possibles :
#     -1 -> on ne sait pas
#     0  -> absence obligatoire
#     1  -> présence obligatoire
# L'état initial de M est d'être remplie de -1
# La prise en compte d'un arête fournie par l'énigme va forcer certaines valeurs
# en raison des contraintes liées à la règle du jeu

# placement d'un sommet
# C'est la fonction fondamentale de prise en compte des contraintes
# Elle opére en deux étapes :
# - vérification de la cohérence du sommet en cours de placement avec ce qui existe déjà
# - si on peut ajouter le sommet, prise en compte des contraintes afin de fixer la valeur
#   des cubes dépendant des arêtes centrées sur le sommet
def placeSommet(xs, ys, zs, d, M):
    """Arguments :
    xs, ys, zs -> coordonnées 3D d'un sommet de l'énigme
    d -> la chaîne indiquant la présence ou non d'un arête
    M -> matrice représentant l'état courant du jeu
    Valeur de retour :
    couple (r , M')
    r -> booléen indiquant si l'ajout du sommet est possible
    M' -> copie de la matrice du jeu modifiée avec les contraintes résultant de
    l'ajout de s
    """
    n = M.shape[0]
    Mp = M.copy()  # copie de M

    # trait vertical (selon z)
    if "z" in d:
        if zs == n:  # arête en dehors de la zone de jeu
            return (False, M)
        # aucun cube (x,y,z) avec x<xs & y<ys & z<=zs ne doit être vide
        # aucun cube (x,y,z) avec x>=xs & y>=ys & z>=zs ne doit être rempli
        if (0 in M[:xs, :ys, :zs+1]) or (1 in M[xs:, ys:, zs:]):
            return (False, M)  # échec
        # pour une arête interne, les cubes symétriques / à l'arête et au plan
        # orthogonal au vecteur (1,1,0) doivent être de même nature si déjà
        # de valeur connue
        if 0 < xs < n and 0 < ys < n and zs < n and \
                ((M[xs-1, ys, zs], M[xs, ys-1, zs]) in ((0, 1), (1, 0))):
            return (False, M)  # échec
        # gestion des bords x==0 et y==0
        if xs == 0 and ys > 0 and M[xs, ys-1, zs] == 0:
            return (False, M)  # échec
        if ys == 0 and xs > 0 and M[xs-1, ys, zs] == 0:
            return (False, M)  # échec
        # gestion des bords x==0 et y==0
        if xs == n and 1 in M[xs-1, ys:, zs:]:
            return (False, M)  # échec
        if ys == n and 1 in M[xs:, ys-1, zs:]:
            return (False, M)  # échec

        # pas d'incompatibilités avec les contraintes existantes :
        # on modifie la matrice en ajoutant les contraintes liées à l'arête
        Mp[:xs, :ys, :zs+1] = 1 # cubes nécessairement présents
        Mp[xs:, ys:, zs:] = 0 # cubes nécessairement vides

        # gestion des bords
        if xs == 0:
            Mp[0, :ys, :zs+1] = 1
        if ys == 0:
            Mp[:xs, 0, :zs+1] = 1
        if xs == n:
            Mp[xs-1, ys:, zs:] = 0
        if ys == n:
            Mp[xs:, ys-1, zs:] = 0

        # pour une arête interne, les cubes symétriques / à l'arête et au plan
        # orthogonal au vecteur (1,1,0) doivent être de même nature
        if 0 < xs < n and 0 < ys < n and zs < n:
            Mp[xs-1, ys, zs] = Mp[xs, ys-1,
                                    zs] = max(Mp[xs-1, ys, zs], Mp[xs, ys-1, zs])
            # si les cubes sont vides, les suivants selon x et y le sont aussi
            if Mp[xs-1, ys, zs] == 0:
                Mp[xs-1:, ys:, zs:] = 0
                Mp[xs:, ys-1:, zs:] = 0
            elif Mp[xs-1, ys, zs] == 1: # cubes plein -> cubes précédents à remplir
                Mp[:xs+1, :ys, :zs+1] = 1
                Mp[:xs, :ys+1, :zs+1] = 1

    # trait bas-gauche (selon x) ou trait droit (selon y)
    # situation analogue à la précédente :
    # une rotation de +/- 2 Pi/3 autour de l'axe (1,1,1) d'un empilement
    # valide est aussi valide
    # on a donc deux fois le code ci-dessus, aux permutations de x, y, z près
    # C'est un peu long et il faut faire attention, mais rien de nouveau
    if "x" in d:    # on permute le code de "z", dans le sens direct (x->y->z->x)
        if xs == n:
            return (False, M)  # pas possible
        if (0 in M[:xs+1, :ys, :zs]) or (1 in M[xs:, ys:, zs:]):
            return (False, M)  # échec
        if xs < n and 0 < ys < n and 0 < zs < n and \
                ((M[xs, ys-1, zs], M[xs, ys, zs-1]) in ((0, 1), (1, 0))):
            return (False, M)  # échec
        if ys == 0 and zs > 0 and M[xs, ys, zs-1] == 0:
            return (False, M)  # échec
        if zs == 0 and ys > 0 and M[xs, ys-1, zs] == 0:
            return (False, M)  # échec
        if ys == n and 1 in M[xs:, ys-1, zs:]:
            return (False, M)  # échec
        if zs == n and 1 in M[xs:, ys:, zs-1]:
            return (False, M)  # échec

        Mp[:xs+1, :ys, :zs] = 1
        Mp[xs:, ys:, zs:] = 0
        if ys == 0:
            Mp[:xs+1, 0, :zs] = 1
        if zs == 0:
            Mp[:xs+1, :ys, 0] = 1
        if ys == n:
            Mp[xs:, ys-1, zs:] = 0
        if zs == n:
            Mp[xs:, ys:, zs-1] = 0
        if xs < n and 0 < ys < n and 0 < zs < n:
            Mp[xs, ys-1, zs] = Mp[xs, ys, zs -
                                    1] = max(Mp[xs, ys-1, zs], Mp[xs, ys, zs-1])
            if Mp[xs, ys-1, zs] == 0:
                Mp[xs:, ys-1:, zs:] = 0
                Mp[xs:, ys:, zs-1:] = 0
            elif Mp[xs, ys-1, zs] == 1:
                Mp[:xs+1, :ys+1, :zs] = 1
                Mp[:xs+1, :ys, :zs+1] = 1
    if "y" in d:    # on permute le code de "z", dans le sens indirect (x<-y<-z<-x)
        if ys == n:
            return (False, M)  # pas possible
        if (0 in M[:xs, :ys+1, :zs]) or (1 in M[xs:, ys:, zs:]):
            return (False, M)  # échec
        if 0 < xs < n and ys < n and 0 < zs < n and \
                ((M[xs, ys, zs-1], M[xs-1, ys, zs]) in ((0, 1), (1, 0))):
            return (False, M)  # échec
        if zs == 0 and xs > 0 and M[xs-1, ys, zs] == 0:
            return (False, M)  # échec
        if xs == 0 and zs > 0 and M[xs, ys, zs-1] == 0:
            return (False, M)  # échec
        if zs == n and 1 in M[xs:, ys:, zs-1]:
            return (False, M)  # échec
        if xs == n and 1 in M[xs-1, ys:, zs:]:
            return (False, M)  # échec

        Mp[:xs, :ys+1, :zs] = 1
        Mp[xs:, ys:, zs:] = 0
        if zs == 0:
            Mp[0, :ys+1, :zs] = 1
        if xs == 0:
            Mp[0, :ys+1, :zs] = 1
        if zs == n:
            Mp[xs:, ys:, zs-1] = 0
        if xs == n:
            Mp[xs-1, ys:, zs:] = 0
        if 0 < xs < n and ys < n and 0 < zs < n:
            Mp[xs, ys, zs-1] = Mp[xs-1, ys,
                                    zs] = max(Mp[xs, ys, zs-1], Mp[xs-1, ys, zs])
            if Mp[xs, ys, zs-1] == 0:
                Mp[xs:, ys:, zs-1:] = 0
                Mp[xs-1:, ys:, zs:] = 0
            elif Mp[xs, ys, zs-1] == 1:
                Mp[:xs, :ys+1, :zs+1] = 1
                Mp[:xs+1, :ys+1, :zs] = 1

    # fin de la fonction
    return (True, Mp)

# %% Section 4 : Résolution

# 4.1 : pour jouer à la main, étape par étape
n = 2
#enigme = ((0, 2, "z"), (0, 0, "x"), (1, 1, "x"))
enigme = ((0, 0, "x"), (1, 1, "x"), (0, 2, "z"))

for i in range(len(enigme)):
    print(f"{enigme[i][:2]} -> {listCoord3D(enigme[i][0], enigme[i][1], n)}")

# Test de placeSommet sur l'énigme précédente
# la matrice initiale
M0 = -np.ones((n, n, n), dtype='int')
print(M0)
r, M1 = placeSommet(0, 1, 1, "x", M0)
print(r, M1)
r, M1 = placeSommet(1, 1, 1, "x", M1)
print(r, M1)
r, M1 = placeSommet(0, 0, 1, "z", M1)
print(r, M1)

# deuxième passe nécessaire car il subsiste des emplacements non fixés (= -1)
r, M1 = placeSommet(0, 1, 1, "x", M1)
print(r, M1)
r, M1 = placeSommet(1, 1, 1, "x", M1)
print(r, M1)
r, M1 = placeSommet(0, 0, 1, "z", M1)
print(r, M1)

draw_config(M1)

# Existe-t-il des énigmes pour lesquelles plus de 2 passes soient nécessaires ???
# Ça paraît probable, si la taille du jeu est plus grande.

# L'idée sera donc de rechercher un point fixe en répétant les placement de sommets
# jusqu'à ce que la configuration n'évolue plus, ce qui est fait dans la section suivante.

# 4.2 : Résolution de l'enigme

# fonction utilitaire, pour simplifier la saisie des énigmes
def trans2D_3D(enigme, n):
    """
    retourne à partir d'une énigme 2D son codage avec les coordonnées 3D des points.
    Comme un point 2D peut correspondre à plusieurs points en 3D, on associe à chaque point 2D
    une liste de points en 3D.
    Cette fonction retourne donc une liste de listes, chacune étant associée à un sommet 2D.
    Chaque élément est un n-uplet de la forme (x, y, z, "xyz")
    """
    # transformation de l'énigme 2D en énigme 3D
    enig3 = []
    for c in enigme:
        lc3D = listCoord3D(c[0], c[1], n)
        enig3.append([(c3[0], c3[1], c3[2], c[2]) for c3 in lc3D])

    # on retourne la liste de toutes les combinaisons
    return (enig3)


(trans2D_3D(enigme, n))

# Le solveur : automatisation de la recherche d'un point fixe représentant la solution
def solve(lc3D, M, lr, p=0):
    """
    Args :
    - lc3d est une liste de contraintes 3D représentant l'énigme
    - M est la matrice de représentation du jeu
    - lr est la liste modifiée par effet de bord, contenant les matrices solutions
    - p est le niveau de récursion, utilisé pour les impressions de débogage.
      !!!! à supprimer plus tard !!!!

    """
    if lc3D == []:
        print('<-', M)
        lr.append(M)
        return
    for c in lc3D[0]:
        r, Mp = placeSommet(*c, M)
        if r:
            print("  "*(p+1), c)
            solve(lc3D[1:], Mp, lr, p+1)
        else:
            print("--"*(p+1), c)


def doSolve(enigme, n):
    """
    Gestion du solveur : la fonction solve retourne une liste de résultats possibles.
    Chacun de ces résultats peut être incomplet (des cubes sont encore indéterminés)
    car des contraintes peuvent ne pas être exploitées totalement,
    les déductions dépendant de décisions obtenues en plaçant des arêtes plus tard
    au cours du calcul.
    Pour chaque résultat contenant des cubes non déterminés, on recherche un point
    fixe : résultat n'évoluant plus lors de la résolution.
    """

    # la fonction de recherche du point fixe. Un résultat en argument.
    # retourne le point fixe de ce résultat
    def pf(r):
        if -1 not in r: # pas d'indétermination
            return r
        # il y a des cubes non déterminés. On refait un tour ...
        print('Recherche de point fixe ...')
        lrc = []
        solve(lc3D, r, lrc)
        if len(lrc) > 0:
            if np.array_equal(lrc[0], r): # pas d'évolution -> point fixe atteint
                return r
            return pf(lrc[0])  # on recommence !
        else:
            return []

    M = -np.ones((n, n, n), dtype='int')
    lc3D = trans2D_3D(enigme, n)
    lr = []
    solve(lc3D, M, lr)  # première passe
    lrf = []
    for r in lr:
        rr = pf(r)
        if len(rr) > 0:
            lrf.append(pf(r))
    return lrf


# %% Section 5 : tests de résolution

# fonctions pour faciliter les tests

def test_solver(enig, dim):
    """
    - Résoud une énigme et retourne la liste des solutions
    - Imprime le nombre de configurations possibles épuisant toutes les
      contraintes de l'énigme, en informant si la solution est incomplète
    - ouvre une fenêtre graphique représentant l'énigme et la/les solutions/s
      (5 solutions affichées au max)
      Si les contraintes sont insuffisantes, il est possible que certains
      cubes soient indéterminés (affichés en gris).

    Args : l'énigme 2D et la dimension du cube.
    """
    lsol = doSolve(enig, dim)

    print(f"Nombre de solutions : {len(lsol)}")
    ns = 0
    for s in lsol:
        ns += 1
        if -1 in s:
            nmu = len(np.where(s==-1)[0])
            print(f'solution {ns} incomplète : il reste {nmu} cube(s) non déterminé(s) !')

    # calcul de l'affichage
    draw_solutions(enig, dim, lsol)

    return lsol


# tracé des solutions
def draw_solutions(enigma, n, lSols, cellSize = 4):
    """
    dessine à l'aide de pyplot l'enigme ainsi que les solutions trouvées.
    - enigma représente l'énigme (ie. les segments connus avant résolution)
    - lSols est une liste des solutions trouvées

    Le dessin se fait dans une grille de 2 x 3 cellules (subplots) au maximum,
    ce qui impose qu'on ne trace que l'énigme et 5 solutions au max.
    Si lSols est vide, on ne dessine que l'énigme.

    args :
    - enigma : énigme à résoudre
    - n : dimension de l'espace de jeu (côté du grand cube)
    - lSols : liste des solutions trouvées
    - cellSize : taille d'une cellule (<-> 1 subplot) affichant l'énigme
      ou une solution
    """
    # Remarque : dans les fonctions de tracé, l'aspect sqrt(2/6) est nécessaire
    # en raison de la simplification du calcul des projections
    # (cf fonction 'projection)

    # la fonction de tracé de l'énigme dans le subplot courant
    def draw_enigma(e):
        opt_enig = {'color': 'red', 'linewidth': 4}
        for p in e:
            x0, y0 = p[:2]
            d = p[2]
            if 'x' in d:
                line([x0, y0], [x0 - 1, y0-1],**opt_enig)
            if 'y' in d:
                line([x0, y0], [x0 + 1, y0-1],**opt_enig)
            if 'z' in d:
                line([x0, y0], [x0, y0+2],**opt_enig)

    # Le tracé d'une solution dans le subplot courant
    def draw_solution(s):
        drawHex(n)
        drawAxes(jeu)
        for i in range(n):
            for j in range(n):
                for kk in range(n):
                    projCube(s, i, j, kk)


    if len(lSols) == 0:
        print('Pas de solutions !')
        plt.figure(figsize=(cellSize, cellSize), tight_layout = True)
        plt.subplot(111, adjustable='box', aspect=1/np.sqrt(3))
        drawHex(n)
        draw_enigma(enigma)
    else:
        nls = len(lSols)
        # trop de solutions ?
        if nls > 5 :
            print(f'Trop de solutions ({nls})')
            print('Seules les 5 premières seront dessinées !')

        # définition de l'arrangement des subplots
        if nls < 3: # subplots sur une seule ligne
            formatSubPlots = 111 + 10 * nls
            plt.figure(figsize=(cellSize * (1 + nls), cellSize),
                        tight_layout = True)
        else: # subplots sur 2 lignes et 3 colonnes
            formatSubPlots = 231
            plt.figure(figsize = (3*cellSize, 2*cellSize), tight_layout = True)

        # tracé de l'enigme dans le premier subplot
        plt.subplot(formatSubPlots, adjustable='box', aspect=1/np.sqrt(3))
        drawHex(n)
        draw_enigma(enigma)

        # tracé des solutions dans les subplots restants
        for ns in range(min(nls, 5)):
            plt.subplot(formatSubPlots + ns + 1,
                        adjustable='box', aspect=1/np.sqrt(3))
            # tracé de la solution
            draw_solution(lSols[ns])
            # on superpose l'énigme pour voir l'énigme en même temps !
            draw_enigma(enigma)
    plt.show()



# %% taille 2
#enigme = ((-1, 1, "y"), (0, 0, "y"), (0, 2, "z"))
#enigme = [(0,2,"x"),(1,1,"z"), (-1,-3,"z"),(1,-3,"z")]
enigme = [(0,2,"z"),(-1,1,"y"), (1,-1,"z")]

#enigme = ((0, 2, "z"), (0, 0, "x"), (1, 1, "x"))
#enigme = ((0, 0, "x"), (1, 1, "x"), (0, 2, "z"))

test_solver(enigme, 2)

# %% taille 3.1
enigme = [
(0,2,"z"),
(-1,1,"y"),
(1,-1,"z"),
(0,-2,"x"),
(-1,1,"x"),
(2,0,"y"),
(-2,-2,"y"),
(1,3,"y"),
(0,-4,"z")
]


test_solver(enigme, 3)


# %% taille 3

enigme = (
    (1,1,'x'),
    (-1,1, "z"),
    (2,0, "z"),
    (-1,-1,"x"),
    (1,-1,"y"),
    (0,-2,"y"),
    (-1,-3,"y")
)

test_solver(enigme, 3)

# %% taille 4
# construit à partir du précédent (taille 3), en ajoutant "à la main" des arêtes qui
# me semblent pertinentes.

# Certaines sont peut-être inutiles, je n'ai pas épuisé tous les cas ;-)

# je le pense difficile à faire à la main, mais peut-être pas ...

enigme = (
  (1,1,'x'), # (0,0,"z"), # soit l'un, soit l'autre => même solution
   # (-1,1, "z"), # pas nécessaire
  #  (2,0, "z"),    # idem
    (-2,0,"z"),
  #  (-3,1,"z"),
    (-1,-1,"x"),
    (1,-1,"y"),
    (0,-2,"y"),
    (0,-4,"y"),
    (-1,-3,"y"),
    (3,3,"x"),
    (2,4,"x"),
    (1,5,"x"),
    (-1,5,"x"),
    (-3,1,"y"),
    (-1,-3,"x")
)

test_solver(enigme, 4)

# %% Génération auto d'énigme
# Version bourrin :
# on génére des arêtes au hasard, et on espère qu'une solution va pouvoir s'en dégager.
# Dans la majorité des cas, ça ne marche pas ...
# Il faudrait plutôt s'inspirer des fonctions de la section 1 ********* A FAIRE ******

def randomEnigma(n, m):
    """
    retourne une éngme tirée au hasard dans un jeu de taille n, contenant m contraintes.
    """
    # validation de la contrainte
    def valid(x, y, d):
        # couple (x,y) valide ou pas ?
        if (x+y) % 2 != 0:
            return False

        # coordonnées et direction dans la zone de jeu ?
        if d=="x" and len(listCoord3D(x-1, y-1, n)) > 0:
            # contrainte sur un bord ?
            if (y==x+2*n) or (y==x-2*n):
                return False
            else:
                return True
        if d=="y" and len(listCoord3D(x+1, y-1, n)) > 0:
            if (y==-x+2*n) or (y==-x-2*n):
                return False
            else:
                return True
        if d=="z" and len(listCoord3D(x, y+2, n)) > 0:
            if x==-n or x==n:
                return False
            else:
                return True
        # contrainte incorrecte
        return False

    enig = []
    dirs = "xyz"
    while len(enig) < m:
        # coordonnées et direction au hasard
        x = rd.randint(-n, n)
        y = rd.randint(-2*n, 2*n)
        d = rd.randint(0,2)

        # coordonnées de l'origine de la contrainte valides ?
        l3D = listCoord3D(x,y,n)
        if len(l3D) > 0:
            li = (x, y, dirs[d])
            if valid(*li):
                enig.append(li)
    return enig

rdEnig = randomEnigma(4,10)

listSol = test_solver(rdEnig, 4)
print(rdEnig)

# %% Section 6 : énigmes aléatoires, puis solution unique 'à la main'

enigme=[(-2, 2, 'x'),
 (-1, 1, 'z'),
 (0, 4, 'y'),
 (-1, -1, 'y'),
 (1, -1, 'x'),
 (-2, -2, 'z'),
 (2, 2, 'x'),
 (2, -4, 'z')]
listSol = test_solver(enigme, 3)

# %%
# Exemples de résultats obtenus (n=3, m=6)

enigme = [(1, 1, 'xy'), (-1, 3, 'z'),
#(1, -5, 'x'),
(0, -4, 'z'),(0, 4, 'y'), (0, -2, 'y'), (-2, 0, 'z')]

test_solver(enigme, 3)

## taille 3
enigme = [(1, 3, 'x'), (2, 2, 'z'), (-1, -3, 'z'),
(-2,0,"z"),
(0,-2,"y"),
(1,-1,"z"),
(0,0,"x")
]
test_solver(enigme, 3)


## taille 3
enigme = [(0, 2, 'x'), (-1, -1, 'x'), (-2, 2, 'x'),
#(-1, -1, 'z'),
 (2, 2, 'y'),
 (0, 2, 'y'),
(1,-3,"z"),
(-1,-3,"y") ]
test_solver(enigme, 3)

## taille 4
enigme = [
    (-1, -3, 'z'),
    (1, 3, 'y'),
    (0,0,"z"),# (1, 3, 'x'),
    (0, 4, 'z'),
    (0,0,"y"),
    (2,-2,"x"),
    (-1,1,"x"),
    (2,-2,"y"),
    (3,1,"x"),
    (-2,-2,"x"),
    (-2,4,"y"),
    (2,-4,"x"),
    (-1,-3,"x"),
    (-3,-1,"z"),
    (-1,3,"x")
]
test_solver(enigme, 4)

## 3 solutions
enigme =[#(3, -1, 'z'),
(-1,3,"y"),
(-2,2,"x"),
(-2,0,"x"),
(1,3,"x"),
 (1, -5, 'z'),
 (3, 3, 'z'),
 (1, 1, 'x'),
 (-1, 5, 'x'),
 (-2, -4, 'z'),
  (3, -1, 'y'),
  (2, 2, 'z'),
  (-1, -3, 'y'),
   (-1, -1, 'y')
   ]
test_solver(enigme, 4)

## taille 5
enigme = [
    (-1, -3, 'z'),
    (1, 3, 'y'),
    (0,0,"z"),
    (0, 4, 'z'),
    (2,-2,"x"),
    (-1,1,"x"),
    (2,-2,"y"),
    (3,1,"x"),
    (-2,-2,"x"),
    (-2,4,"y"),
    (2,-4,"x"),
    (-1,-3,"x"),
    (-3,-1,"z"),
    (-2,2,"x"),
    (0,-6,"x"),
    (3,3,"z"),
    (4,2,"z"),
    (-4,4,"y"),
    (2,6,"x")
]
test_solver(enigme, 5)

###### BUG ?
enigme =[
(-1,3,"y"),
(-2,2,"x"),
(-2,0,"x"),
(1,3,"x"),

# tracé incorrect si la ligne suivante est active
(-1,3,"x"),

 (1, -5, 'z'),
 (-3, 3, 'z'),
 (3, 3, 'z'),
 (1, 1, 'x'),
 (-1, 5, 'x'),
 (-2, -4, 'z'),
  (3, -1, 'y'),
  (2, 2, 'z'),
  (-1, -3, 'y'),
   (-1, -1, 'y')
   ]

lsol = doSolve(enigme, 4)
draw_solutions(enigme, 4,lsol[0:], cellSize = 4)
print(listCoord3D(-1,3,4))