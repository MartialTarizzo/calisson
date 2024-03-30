# %% Jeu du calisson
# gen_grilles.py : fonctions de génération automatique 
# d'une série d'énigmes destinées au site testCalisson sur GitHub pages
#
# ============================================================================
# Auteur : Martial Tarizzo
#
# Licence : CC BY-NC-SA 4.0 DEED
# https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr
# ============================================================================
# %% pour la génération automatique d'une série d'énigmes
"""
L'appel à la fonction generate_grids de ce fichier permet la création d'une série d'énigmes 
sauvegardées dans le répertoire data avec une syntaxe 'javascript' permettant l'utilisation
comme script dans la page HTML index.html (voir dossier testCalisson)
"""

from gen_calisson import randomEnigma2
#from gen_calisson import randomEnigma_fromConstraints, randomEnigma_fromConstraints_incremental
from html_calisson import make_url
from calisson import doSolve

#  la fonction d'évaluation de la difficulté des grilles
from evalLosanges import calcListLosAcuteFold

import time

def generate_grids(size, method, nenig, withExport = False, metric = False):
    """
    Génération d'un série d'énigmes sous la forme d'un fichier texte javascript prêt pour l'importation 
    args :
        size     # taille des énigmes
        method   # niveau de facilité de l'énigme
        nenig    # nombre d'énigmes générées
    Écrit le fichier data/enigmes_{size}_{method}.js contenant les chaînes codant les énigmes générées.
    """

    def makeEnigma(size, level):
        # le dictionnaire des pourcentage de filtrage
        dictP = {
            (3, 1): (1, 1),
            (4, 1): (1, 1),
            (5, 1): (1, 1),
            (6, 1): (1, 1),
 
            (3, 2): (1/2, 1),
            (4, 2): (1/2, 1),
            (5, 2): (1/2, 1),
            (6, 2): (1/2, 1),
             
            (3, 3): (0.1, 0.9),
            (4, 3): (0.2, 0.8),
            (5, 3): (0.0, 0.8),
            (6, 3): (0.0, 0.6)
        }
        p1, p2 = dictP[(size, level)]
        
        while True:
            if level == 1:
                enigme = randomEnigma2(size, easy=10)
            elif level == 2:
                enigme = randomEnigma2(size, easy=5)
            elif level == 3:
                enigme = randomEnigma2(size, easy=0)
            
            p = len(calcListLosAcuteFold(enigme, size)) / (3 * size ** 2)
            if p1 <= p <= p2:
                return enigme

    # pour le suivi des métriques des grilles
    if metric:
        ldur = []
        lres = []
    fullstart = time.monotonic()
    filename = f"data/enigmes_{size}_{method}.js"
    with open(filename, "w") as f:
        if withExport:
            f.write(f'export let enigme_{size}_{method} = `\\')
        else:
            f.write(f'let enigme_{size}_{method} = `\\')
        f.write("\n")

        for i in range(nenig):
            if metric:
                start = time.monotonic()

            enigme = makeEnigma(size, method)
            
            if metric:
                stop = time.monotonic()
                ldur.append(stop-start)
                start = time.monotonic()
                doSolve(enigme, size)
                stop = time.monotonic()
                lres.append(stop-start)
            
            link = make_url(enigme, size)
            e =link.split('=')[-1]
            f.write(e)
            f.write("\n")
            print(f'écriture de l\'énigme {i+1}')
        f.write('`')
    fullstop = time.monotonic()  
    print(f'génération terminée pour {nenig} grilles de taille {size} en {fullstop-fullstart:.0f} s')

    if metric:
        return (fullstop-fullstart, ldur, lres)
    else:
        return (fullstop-fullstart)

# %%
# Génération de toutes les grilles "training"
start = time.time()

for s in [3,4,5,6]:
    for meth in [1,2,3]:
        generate_grids(s, meth, 100 , withExport = True)

print(f"Génération terminée en {time.time() - start}")
# %%
# Génération de toutes les grilles "speedy"
start = time.time()

for s in [3,4,5,6]:
    for meth in [1,2,3]:
        generate_grids(s, meth, 220 - (s-3) * 40 , withExport = True)

print(f"Génération terminée en {time.time() - start}")

# %% Lancement de la génération
"""
# Exemple de génération
generate_grids(6, 3, 10, True)


"""

import time, matplotlib.pyplot as plt
import math
lres = []
for s in range(2,6):
    for m in (1, 2, 3):
        lres.append((s, m, generate_grids(s, m, 8, True)))
lres

l1 = list(filter(lambda t: t[1]==1, lres))
l2 = list(filter(lambda t: t[1]==2, lres))
l3 = list(filter(lambda t: t[1]==3, lres))

lx = [e[0] for e in l1]
ly1 =  [(sum(e[2][1])/8) for e in l1]
ly2 =  [(sum(e[2][1])/8) for e in l2]
ly3 =  [(sum(e[2][1])/8) for e in l3]
plt.plot(lx,ly1, label = '1', color = 'red')
plt.plot(lx,ly2, label = '2', color = 'blue')
plt.plot(lx,ly3, label = '3', color = 'black')
plt.legend()
plt.grid()




# %%


def metrique_gen(size1, size2, method, nenig):
    lSizes = list(range(size1, size2+1))
    ltimes = []
    for s in lSizes:
        start = time.monotonic()
        generate_grids(s, method, nenig)
        duree = time.monotonic()-start
        ltimes.append(duree)
        print(f'durée totale : {duree}')
    plt.plot(lSizes, [math.log10(t) for t in ltimes])

metrique_gen(3,7,2,5)



# %%
