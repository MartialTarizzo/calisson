# %% Jeu du calisson
# testEvalLosanges.py : test de la fonctions d'évaluation de la difficulté d'une énigme 
# à partir de la représentation 2D
# voir evalLosanges.py pour la fontion ppale
#
# ============================================================================
# Auteur : Martial Tarizzo
#
# Licence : CC BY-NC-SA 4.0 DEED
# https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr
# ============================================================================

# %% évaluation des grilles générées sans évaluation

from evalLosanges import calcListLosAcuteFold

from html_calisson import make_enigma_from_url

# Lecture des fichiers de grilles
def getEnigmas(size, level):
    """retourne  la liste des énigmes pour une taille et un niveau donné
    Args:
        size (integer): la taille de la grille (3..6)
        level (integer): son niveau (1..3)
    Returns:
        list: liste des énigmes correspondante
    """
    dir = "./data/"
    lFiles = [
        "enigmes_3_1.js", "enigmes_3_2.js", "enigmes_3_3.js",
        "enigmes_4_1.js", "enigmes_4_2.js", "enigmes_4_3.js",
        "enigmes_5_1.js", "enigmes_5_2.js", "enigmes_5_3.js",
        "enigmes_6_1.js", "enigmes_6_2.js", "enigmes_6_3.js"
    ]
    lLevels = [
        (3, 1), (3, 2), (3, 3),
        (4, 1), (4, 2), (4, 3),
        (5, 1),(5, 2), (5, 3),
        (6, 1), (6, 2), (6, 3)
    ]
    with open(dir + 
              lFiles[
                  lLevels.index((size, level))], 'r') as f:
        lenigs = f.readlines()[1:-1]
        lenigs = [make_enigma_from_url(s[:-1])[0] for s in lenigs]
    return lenigs


#%% Fabrication des histogrammes pour le dos de stats
import time

import matplotlib.pyplot as plt

for size in range(3,7):
    fig = plt.figure(figsize=(9,4))
    axs = fig.subplots(1,3, sharey=True)

    start = time.monotonic()
    # size = 4

    for level in range(1,4):

        # level = 3

        lnlos = [len(calcListLosAcuteFold(e, size)) / (3 * size**2) * 100
                for e in getEnigmas(size, level)]
        print()
        print(time.monotonic() - start)

        # plt.plot(lnlos)
        axs[level-1].hist(lnlos, label = f"{size}.{level}",orientation="vertical")
        axs[level-1].hist(lnlos, 
                          label = f"cumul {size}.{level}",
                          histtype="step",
                          orientation="vertical",
                          cumulative=True,
                          linewidth = 2)
        
        axs[level-1].legend(loc='upper left')
        axs[level-1].grid()
    fig.suptitle("Règles de l'angle aigu et du pli")
    axs[1].set_xlabel("% de losanges placés")
    axs[0].set_ylabel("nombre de grilles")
    plt.show()

# %% Essai de génération de grille avec évaluation de la difficulté
from gen_calisson import randomEnigma2

size = 4
nTotLos = 3*size**2

# nombre minimal de losanges déductibles par angle aigu/pli
nMinLos = 0.1 * nTotLos 
# nombre maximal de losanges déductibles par angle aigu/pli
nMaxLos = 0.6 * nTotLos

# recherche d'une grille vérifiant les contraintes précédentes
while True:
    e = randomEnigma2(size, easy=0)
    nlos = len(calcListLosAcuteFold(e, size))
    if  nMinLos <= nlos <= nMaxLos:
        break

# test de la grille sélectionnée
from calisson import test_solver

test_solver(e, size)

from html_calisson import make_url

url = make_url(e, size)
url

