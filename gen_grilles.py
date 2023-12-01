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

from gen_calisson import randomEnigma
from gen_calisson import randomEnigma_fromConstraints, randomEnigma_fromConstraints_incremental
from html_calisson import make_url

import time
def generate_grids(size, method, nenig):
    """
    Génération d'un série d'énigmes sous la forme d'un fichier texte javascript prêt pour l'importation 
    args :
        size     # taille des énigmes
        method   # méthode de génération
        nenig    # nombre d'énigmes générées
    Écrit le fichier data/enigmes_{size}_{method}.js contenant les chaînes codant les énigmes générées.
    """
    start = time.monotonic()
    filename = f"data/enigmes_{size}_{method}.js"
    with open(filename, "w") as f:
        f.write(f'let enigme_{size}_{method} = `\\')
        f.write("\n")
        for i in range(nenig):
            if method == 1:
                enigme = randomEnigma(size)
            elif method == 2:
                enigme = randomEnigma_fromConstraints(size)
            elif method == 3:
                enigme = randomEnigma_fromConstraints_incremental(size)
            
            link = make_url(enigme, size)
            e =link.split('=')[-1]
            f.write(e)
            f.write("\n")
            print(f'écriture de l\'énigme {i+1}')
        f.write('`')
    stop = time.monotonic()  
    print(f'génération terminée pour {nenig} grilles de taille {size} en {stop-start:.0f} s')

# %% Lancement de la génération
"""
# Exemple de génération
import time

start = time.monotonic()
generate_grids(7, 1, 10)
print(f'durée totale : {time.monotonic()-start}')


"""