# %% Jeu du calisson
# calisson.py : fonctions de représentation graphique et de résolution
#
# ============================================================================
# Auteur : Martial Tarizzo
#
# Licence : CC BY-NC-SA 4.0 DEED
# https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr
# ============================================================================

"""" Pour la présentation et les règles du jeu, cf https://mathix.org/calisson/blog/

Contrairement à la présentation par 'calissons', on adopte ici la modélisation
3D de l'empilement des cubes dans une zone de rangement cubique, dont le côté
est de taille n.

Un empilement de cubes sera représenté par une matrice de dimension 3 : n x n x n
contenant des entiers dans {-1, 0, +1} représentant trois états possibles.
La signification de chaque élément de matrice est la suivante :
-1 -> cube indéterminé
0  -> absence de cube
+1 -> cube présent
"""

# Imports pour la suite
import random as rd
import matplotlib.pyplot as plt
import numpy as np



# %% Section 1 : Représentation graphique d'une configuration
# ------------------------------------------------------------
# sortie graphique sans interaction : on utilise pyplot pour faire simple

# Les couleurs pour les tracés
color_enigme = "black"
color_solution = "red"
color_indet = "gray"

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
        opt = {'color': color_solution, 'linewidth': 3}

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
        opt_indet = {'color': color_indet, 'linewidth': 4}
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
    opt = {'color': color_enigme, 'linestyle': 'dashed', 'linewidth': 1}
    for i in range(n+1):
        lineproj([0, 0, i], [n, 0, i], **opt)
        lineproj([0, 0, i], [0, n, i], **opt)
        lineproj([i, 0, 0], [i, n, 0], **opt)
        lineproj([0, i, 0], [n, i, 0], **opt)
        lineproj([i, 0, 0], [i, 0, n], **opt)
        lineproj([0, i, 0], [0, i, n], **opt)

    # le bord
    opt = {'color': color_enigme, 'linewidth': 3}

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
    opt = {'color': color_solution, 'linewidth': 3}  # options de tracé des cubes
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
    # du calcul des projections (cf fonction 'projection')
    plt.subplot(111,adjustable='box', aspect=1/np.sqrt(3))
    #plt.axis('equal')
    drawHex(n)
    drawAxes(jeu)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                projCube(jeu, i, j, k)
    plt.show()


# %% Section 2 : RECHERCHE DE LA SOLUTION D'UNE ENIGME
#  ---------------------------------------------------

# --------------------------
# 2.1 : Codage d'une énigme
# --------------------------
# Évidemment, ce codage doit être exprimé en 2D dans le plan de la projection
# orthographique.
# On prend comme repère (O,X,Y) centré sur l'hexagone englobant l'empilement.
# OX horizontal, vecteur unité pour passer d'un colonne de points à la suivante
# OY vertical vecteur unité pour passer d'un ligne de points horiz.
# à la suivante.
# En raison de la projection, la base est orthogonale, mais pas normée !
# Exemple : le suivi d'une arête de face supérieure d'un petit cube fait varier
# X et Y d'un unité, le suivi d'une arête verticale fait varier Y de 2 sans
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
# - chaîne de 1 caractère indiquant la présence d'une arête dans la direction
#   de la projection des axes 3D (x,y,z) à partir de (X,Y)
#   Ex : "x" -> arête dans la direction x
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
# 2.2 : encodage sous forme concrète
# --------------------------
"""
idée : reprendre le code de dessin, mais encoder concrètement les arêtes
sous la forme précédente plutôt que de les dessiner.
"""
# encodage d'un petit cube de coordonnées 3D [i,j,k]
# On tient compte de l'environnement du cube pour n'encoder que les arêtes
# nécessaires.
def encodeCube(jeu, i, j, k):
    """
    jeu : matrice 3D représentant l'empilage de cubes
    i,j,k : coordonnées 3D de l'origine du petit cube

    retourne une paire de deux listes contenant l'encodage en 2D et en 3D des arêtes visibles dans 
    la configuration du jeu :
    - la première liste avec la syntaxe pour chaque arête correspondant à celle de l'énigme :
      (X, Y, d) <-> coordonnées 2D et direction de l'arête
    - la deuxième liste avec les coordonnées 3D de l'origine de l'arête (x, y, z, d)
    """
    n = jeu.shape[0]
    def c(i, j, k):
        """ test de la présence d'un cube aux coordonnées [i,j,k]
        Avec prise en compte des bords pour contrôler le tracé des arêtes.
        """
        if i < 0 or j < 0 or k < 0:
            return True
        if i == n or j == n or k == n:
            return False
        
        # on n'est pas sur un bord
        if jeu[i,j,k] == -1: # cube indéterminé
            return False
        return jeu[i, j, k] == 1 # test de présence

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

    # élimination des arêtes tracées le long des bords du grand cube
    lar2 = []
    lar3 = []
    for (x,y,z,d) in lar:
        if not( # les arêtes suivantes sont le long du tracé de l'hexagone englobant->ne pas encoder
            (x==0 and ((z==n and d=='y') or (y==n and d=='z'))) or
            (y==0 and ((x==n and d=='z') or (z==n and d=='x'))) or
            (z==0 and ((y==n and d=='x') or (x==n and d=='y'))) ) :
            X,Y = projection([x,y,z])
            lar2.append((X,Y,d))
            lar3.append((x,y,z,d))

    return lar2, lar3

def encodage(jeu):
    """
    arg : jeu est la matrice 3D décrivant l'empilement
    la fonction retourne une liste de triplets (coord,liste_arêtes_2D, liste_arêtes_3D) 
    pour tous les cubes dont certaines arêtes sont visibles.
    - coord est un triplet (i,j,k) donnant l'origine du cube
    - liste_arêtes_2D est une liste contenant les arêtes correspondantes, sous la forme
      d'un triplet utiisée dans l'énigme (X, Y, d) <-> coordonnées 2D et direction de l'arête
    - liste_arêtes_3D est une liste contenant les arêtes correspondantes, sous la forme
      d'un quadruplet (x, y, z, d) -> coordonnées 3D de l'origine de l'arête
      et direction de l'arête
    """
    lc = []
    n = jeu.shape[0]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                ec2, ec3 = encodeCube(jeu, i, j, k)
                if len(ec2) != 0: # cube visible
                    # print(f'cube {i,j,k} visible : {ec}')
                    lc.append(((i,j,k),ec2, ec3))
    return lc

# encodage des axes non masqués par des cubes
def encodeAxes(jeu):
    """
    encodage 2D des arêtes des axes 3D x, y ou z si pas de cube pour les cacher
    """
    la = []
    n = jeu.shape[0]
    for i in range(n):
        if not jeu[i, 0, 0]:
            X,Y = projection([i, 0, 0])
            la.append( (X, Y, "x") )
        if not jeu[0, i, 0]:
            X,Y = projection([0, i, 0])
            la.append( (X, Y, "y") )
        if not jeu[0, 0, i]:
            X,Y = projection([0, 0, i])
            la.append( (X, Y, "z") )
    return la

def encodeSolution(encJeu):
    # calcule l'encodage de la solution à partir de l'encodage du jeu
    # On récupère l'ensemble des arêtes encodées en 2D pour tous les cubes de
    # l'empilement puis on les regroupe dans un ensemble pour éviter les
    # doublons.
    # On retourne la liste correspondante
    s = set()
    for p in encJeu:
        for c in p[1]:
            s.add(c)
    return list(s)

def encodeSolution3D(encJeu):
    # calcule l'encodage de la solution à partir de l'encodage du jeu
    # On récupère l'ensemble des arêtes encodées en 3D pour tous les cubes de
    # l'empilement puis on les regroupe dans un ensemble pour éviter les
    # doublons.
    # On retourne la liste correspondante
    s = set()
    for p in encJeu:
        for c in p[2]:
            s.add(c)
    return s



# --------------------------
# 2.3 : Résolution d'un énigme
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
# - si on peut ajouter le sommet, modification de la matrice en prenant en compte les contraintes
#  afin de fixer la valeur des cubes dépendant des arêtes centrées sur le sommet
def placeSommet(xs, ys, zs, d, M):
    """
    Arguments :
    xs, ys, zs -> coordonnées 3D d'un sommet s de l'énigme
    d -> la chaîne indiquant la direction de l'arête à partir de s ("x" ou "y" ou "z")
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
    if d == "z":
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
    if d == "x":    # on permute le code de "z", dans le sens direct (x->y->z->x)
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
    if d == "y":    # on permute le code de "z", dans le sens indirect (x<-y<-z<-x)
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
            Mp[:xs, :ys+1, 0] = 1
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

    # fin de la fonction : le sommet s a été placé avec succès, modifs enregistrées dans Mp
    return (True, Mp)

# %% Section 3 : Résolution

""" # 3.1 : pour jouer à la main, étape par étape
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

draw_config(M1) """

# Existe-t-il des énigmes pour lesquelles plus de 2 passes soient nécessaires ?
# Ça paraît probable, si la taille du jeu est plus grande.

# L'idée sera donc de rechercher un point fixe en répétant les placement de sommets
# jusqu'à ce que la configuration n'évolue plus, ce qui est fait dans la section suivante.

# 3.2 : Résolution de l'enigme

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


# Le solveur : force brute !
# fonction récursive qui essaie de placer toutes les arêtes désignés par l'énigme
# jusqu'à épuisement du stock.
def solve(lc3D, M, lr, p = 0, trace = False):
    """
    Args :
    - lc3d est une liste de contraintes 3D représentant l'énigme
    - M est la matrice de représentation du jeu
    - lr est la liste modifiée par effet de bord, contenant les matrices solutions
    - p est le niveau de récursion, utilisé pour les impressions de traçage.
    - trace = True provoque l'impression des infos de traçage. Ralentit fortement la résolution
      en raison des impressions dans la console (qui peuvent être très nombreuses !)

    """
    if lc3D == []:
        if trace : print('<-', M)
        lr.append(M)
        return
    for c in lc3D[0]:
        r, Mp = placeSommet(*c, M)
        if r:
            if trace : print("  "*(p+1), c)
            solve(lc3D[1:], Mp, lr, p+1, trace = trace)
        else:
            if trace : print("--"*(p+1), c)

# automatisation de la recherche des points fixes
def doSolve(enigme, n, trace = False):
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
    # retourne le point fixe de ce résultat ou [] si résultat impossible
    def pf(r):
        lrc = []
        solve(lc3D, r, lrc, trace = trace)
        if len(lrc) > 0:
            if np.array_equal(lrc[0], r): # pas d'évolution -> point fixe atteint
                return r
            if trace : print('Recherche de point fixe ...')
            return pf(lrc[0])  # on recommence !
        else:
            return []

    M = -np.ones((n, n, n), dtype='int')
    lc3D = trans2D_3D(enigme, n)
    lr = []
    solve(lc3D, M, lr, trace = trace)  # première passe

    # recherche du point fixe pour chaque solution trouvée, et fabrication
    # de la liste définitve des résultats.
    # chaque résultat peut être correct, ou incorrect pour de multiples raisons :
    # - cubes indéterminés
    # - arêtes de l'énigme ne faisant pas partie de la solution (car examinées
    #   trop tôt au cours de la résolution en étant compatibles avec la config,
    #   elles sont rendues incorrectes en tenant compte des arêtes suivantes
    # Il faut donc chercher le point fixe pour tous les résultats retournés
    # par le premier appel à solve
    lrf = []
    for r in lr:
        pfr = pf(r)
        if len(pfr) > 0:
            lrf.append(pfr)

    return lrf

# %% Section 5 : fonctions pour faciliter les tests

def test_solver(enig, dim, trace = False, file = None):
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
    lsol = doSolve(enig, dim, trace)

    print(f"Nombre de solutions : {len(lsol)}")
    ns = 0
    for s in lsol:
        ns += 1
        if -1 in s:
            nmu = len(np.where(s==-1)[0])
            print(f'solution {ns} incomplète : il reste {nmu} cube(s) non déterminé(s) !')

    # calcul de l'affichage
    cs = 5 if ns < 3 else 4
    draw_solutions(enig, dim, lsol, cs, file)

    return lsol

# tracé des solutions
def draw_solutions(enigma, n, lSols, cellSize = 4, file = None):
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
    - file : nom du fichier de sortie. Si = None, ouverture d'une fenêtre graphique
    """
    # Remarque : dans les fonctions de tracé, l'aspect sqrt(2/6) est nécessaire
    # en raison de la simplification du calcul des projections
    # (cf fonction 'projection)

    # la fonction de tracé de l'énigme dans le subplot courant
    def draw_enigma(e):
        opt_enig = {'color': color_enigme, 'linewidth': 4}
        for p in e:
            x0, y0 = p[:2]
            d = p[2]
            if 'x' == d:
                line([x0, y0], [x0 - 1, y0-1],**opt_enig)
            if 'y' == d:
                line([x0, y0], [x0 + 1, y0-1],**opt_enig)
            if 'z' == d:
                line([x0, y0], [x0, y0+2],**opt_enig)

    # Le tracé d'une solution dans le subplot courant
    def draw_solution(s):
        drawHex(n)
        drawAxes(s)
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
    if file == None:
        plt.show()
    else:
        plt.savefig(file)
        plt.close()
