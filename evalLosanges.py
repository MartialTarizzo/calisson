# %% Jeu du calisson
# evalLosanges.py : fonctions d'évaluation de la difficulté d'une énigme
# à partir de la représentation 2D
#
# Les fonctions de résolution à partir de la représentation 3D sont dans
# le fichier calisson.py
# Celles présentes dans ce fichier partent d'une tentative de résolution
# à partir des arêtes/losanges

# Dans l'état actuel, la résolution est loin d'être complète :
# les seules règles mises en oeuvre sont celles de l'angle aigu et du pli.

# Cela ne permet pas une résolution des grilles, mais se révèle efficace pour
# estimer la difficulté d'une grille, en permettant le calcul du nombre de
# losanges/arêtes déductible de l'application des deux règles précédentes.

# ============================================================================
# Auteur : Martial Tarizzo
#
# Licence : CC BY-NC-SA 4.0 DEED
# https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr
# ============================================================================


# %%

def listExternEdgesHex(n):
    """
    retourne la liste des arêtes délimitant l'hexagone de taille n
    Une arête est de la forme (x, y, dir)
    - x et y sont les coordonnées du sommet
    - dir est la direction de l'arête ("x" "y" ou "z")
    """
    r = []
    for x in range(n):
        r.append((x, 2 * n - x, "y"))
        r.append((-x, 2 * n - x, "x"))

        r.append((x - n, -x - n, "y"))
        r.append((-x + n, -x - n, "x"))

        r.append((n, -n + 2 * x, "z"))
        r.append((-n, -n + 2 * x, "z"))
    return r


def foldedLos(ar, los):
    """
    pour une arête donnée ar et un losange los contenant l'arête,
    cette fonction retourne le losange imposé par le pli matérialisé par 
    l'arête
    """

    # le dictionnaire suivant donne l'orientation du losange obtenu par pliage 
    # autour d'une arête d'un autre losange.
    # clé : (direction de l'arête, plan du losange origine)
    # valeur : plan du losange après le pli
    dictArLos = {
        ("z", "xz"): "yz",
        ("z", "yz"): "xz",
        ("x", "xz"): "xy",
        ("x", "xy"): "xz",
        ("y", "xy"): "yz",
        ("y", "yz"): "xy",
    }
    x, y, d = ar
    xl, yl, pl = los
    if d == "x":
        if y == yl:
            return (xl, yl, dictArLos[(d, pl)])
        elif pl == "xy":
            return (x, y - 2, dictArLos[(d, pl)])
        else:
            return (x - 1, y + 1, dictArLos[(d, pl)])
    if d == "y":
        if y == yl:
            return (xl, yl, dictArLos[(d, pl)])
        elif pl == "xy":
            return (x, y - 2, dictArLos[(d, pl)])
        else:
            return (x + 1, y + 1, dictArLos[(d, pl)])
    if d == "z":
        if x == xl:
            return (xl, yl, dictArLos[(d, pl)])
        else:
            return (x - (xl - x), yl, dictArLos[(d, pl)])


def sharpAngle(a1, a2):
    """détermine si les arêtes a1 et a2 forment un angle aigu
    Args: a1 et a2 sont deux arêtes, triplets de la forme (x, y, d)
    Returns: True/False
    """
    (x1, y1, d1) = a1
    (x2, y2, d2) = a2
    if d1 == "x":
        if x2 == x1 - 1 and y2 == y1 - 1 and d2 == "y":
            return True
        if x2 == x1 - 1 and y2 == y1 - 1 and d2 == "z":
            return True
        if x2 == x1 - 1 and y2 == y1 + 1 and d2 == "y":
            return True
        if x2 == x1 and y2 == y1 - 2 and d2 == "z":
            return True
    if d1 == "y":
        if x2 == x1 + 1 and y2 == y1 - 1 and d2 == "x":
            return True
        if x2 == x1 + 1 and y2 == y1 - 1 and d2 == "z":
            return True
        if x2 == x1 + 1 and y2 == y1 + 1 and d2 == "x":
            return True
        if x2 == x1 and y2 == y1 - 2 and d2 == "z":
            return True
    if d1 == "z":
        if x2 == x1 and y2 == y1 + 2 and d2 == "x":
            return True
        if x2 == x1 and y2 == y1 + 2 and d2 == "y":
            return True
        if x2 == x1 - 1 and y2 == y1 + 1 and d2 == "y":
            return True
        if x2 == x1 + 1 and y2 == y1 + 1 and d2 == "x":
            return True
    return False

def searchPairsSharpEdges(lar):
    """ recherche des couples d'arêtes formant un angle aigu
    Args:
        lar (list): list d'arêtes
    Returns:
        list: liste de listes de paire d'arêtes
    """
    lpair_sa = []
    for i in range(len(lar) - 1):
        a1 = lar[i]
        for j in range(i, len(lar)):
            a2 = lar[j]
            if sharpAngle(a1, a2):
                lpair_sa.append([a1, a2])
    return lpair_sa



def losFromListSharpEdges(lPairsSA):
    """ calcul des losanges correspondants aux couples d'arêtes 
        formant un angle aigu
    Args:
        lPairsSA (liste): liste de listes de paire d'arêtes
    Returns: 
        list: liste de losanges
    """

    def losFromSharpEdges(a1, a2):
        """ calcul du losange délimité par les arêtes a1 et a2
        Args:
            a1 (tuple): arête 1
            a2 (tuple): arête 2
        Returns:
            tuple: le losange concerné
        """
        # déstructuration des arêtes
        ((x1, y1, d1), (x2, y2, d2)) = a1, a2
        if d1 == "x":
            if d2 == "y":
                if y2 < y1:
                    return (x1, y1, "xy")
                return (x2, y2, "xy")
            else:  # d2 == "z"
                if x2 == x1:
                    return (x2, y2, "xz")
                return (x1, y1, "xz")
        elif d1 == "y":
            if d2 == "x":
                if y2 < y1:
                    return (x1, y1, "xy")
                return (x2, y2, "xy")
            else:  # d2 == "z"
                if x2 == x1:
                    return (x2, y2, "yz")
                return (x1, y1, "yz")
        else:  # d1 = "z"
            if d2 == "x":
                if x1 == x2:
                    return (x1, y1, "xz")
                return (x2, y2, "xz")
            else:  # d2 == "y"
                if x2 == x1:
                    return (x1, y1, "yz")
                return (x2, y2, "yz")

    return [losFromSharpEdges(p[0], p[1]) for p in lPairsSA]


# 
def listEdgesOfLos(los):
    """calcul de la liste des arêtes d'un losange
    Args:
        los (tuple): un losange
    Returns:
        list: la liste des arêtes
    """
    x0 = los[0]
    y0 = los[1]
    axes = los[2]
    if axes == "xy":
        return [
            (x0, y0, "x"),
            (x0, y0, "y"),
            (x0 + 1, y0 - 1, "x"),
            (x0 - 1, y0 - 1, "y"),
        ]
    elif axes == "xz":
        return [(x0, y0, "x"), (x0, y0, "z"), (x0, y0 + 2, "x"), (x0 - 1, y0 - 1, "z")]
    else:
        return [(x0, y0, "y"), (x0, y0, "z"), (x0, y0 + 2, "y"), (x0 + 1, y0 - 1, "z")]


def calcListLosAcuteFold(enigme, size):
    """ fonction principale de ce fichier
    Args:
        enigme (list): liste des arêtes de l'énigme
        size (integer): taille de la grille
    Returns:
        list: liste des losanges déduits des règles angle aigu / pli
    """

    # calcul de l'ensemble des arêtes, en ajoutant les bords de l'hexagone
    setExternEdges = set(listExternEdgesHex(size))
    setAr = set(enigme) | setExternEdges

    # L'ensemble des arêtes virtuelles : 
    # bords des losanges connus qui ne sont pas dans setAr
    # initialement vide. Sera rempli au fur et à mesure
    setArv = set()

    # La liste des losanges connus
    # initialement vide. Sera rempli au fur et à mesure
    llos = []

    # idée :
    # (1) on ajoute à llos tous les losanges déduits de la règle de l'angle aigu
    #     en propageant de proche en proche toujours selon la même règle,
    #     en mettant à jour la liste des arêtes virtuelles.
    #     À la fin de cette phase, plus d'angle aigu disponible.
    #     Si pas de nouveau losange, c'est fini pour cette phase
    # (2) on ajoute tous les nouveaux losanges déductibles de la règle du pli
    #     Si pas de nouveau losange, c'est fini.
    #     Sinon, on ajoute aux arêtes virtuelles les bords de ces nouveaux losanges
    #     et on retourne en (1)

    while True:     # boucle externe (1)
        while True: # boucle de propagation de l'angle aigu
            # longueur de la liste des losanges connus
            initL = len(llos)
            # calcul des paires d'arêtes formant un angle aigu
            lPairsSA = searchPairsSharpEdges(list(setAr | setArv))

            # Calcul des losanges formés par ces paires d'arêtes
            llosSA = losFromListSharpEdges(lPairsSA)
            # MAJ de llos
            llos.extend(llosSA)
            # élimination des doublons éventuels
            llos = list(set(llos))

            if len(llos) == initL: 
                # pas de nouveau losange
                break   # sortie de la boucle de l'angle aigu

            # MAJ de l'ensemble des arêtes virtuelles définies
            # par ces nouveaux losanges
            setArNewLos = set()
            for los in llosSA:
                setArNewLos = setArNewLos.union(listEdgesOfLos(los))
            setArv = setArv | (setArNewLos - setAr)

        # Recherche des nouveaux losanges selon la règle du pli
        lFoldedLos = [] # liste des losanges obtenus par pliage
        newArV = set()  # et les arêtes virtuelles correspondantes

        # La règle du pli n'est valable que pour les arêtes connues
        # avec certitude, donc pas pour les arêtes virtuelles
        for a in enigme:    # arêtes de l'éenigme uniquement !
            for los in llos:    # pour tous les losanges connus
                if a in listEdgesOfLos(los):
                    # l'arête fait partie du bord du losange
                    # on calcule le losange résultant de la règle du pli
                    flos = foldedLos(a, los)
                    if flos not in llos:
                        #  on a un nouveau losange : on l'ajoute
                        lFoldedLos.append(flos)
                        # et on ajoute ses arêtes aux arêtes virtuelles
                        for ap in listEdgesOfLos(flos):
                            newArV.add(ap)

        if len(lFoldedLos) == 0:
            # Si pas de nouveau losange, c'est fini 
            # => sortie de boucle principale
            break
        # on ajoute les nouveaux losanges
        llos.extend(list(set(lFoldedLos)))
        # et on met à jour l'ensemble des arêtes virtuelles
        setArv = setArv | (newArV - set(enigme) - setExternEdges)

    # on retourne la liste finale des losanges déterminés par les deux règles
    return llos
