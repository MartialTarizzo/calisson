# %% Jeu du calisson
# verif_calisson.py : création/vérification d'une grille
#
# ============================================================================
# Auteur : Martial Tarizzo
#
# Licence : CC BY-NC-SA 4.0 DEED
# https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr
# ============================================================================
"""
Ce fichier est destiné à permettre :
- la création d'une grille ex nihilo
- la modification/vérification d'une grille d'url connu

Il s'appuie sur le lancement d'une page HTML locale dans un navigateur,
cette page exécutant du code javascript local permettant la modif de la grille
si besoin.

Le point d'entrée primcipale est la fonction checkGrid.

Deux utilisations possibles :

1) lancement de checkGrid avec une url vide ( "" )
    C'est le fonctionnement classique pour le concepteur de grille.
    Une grille vide s'affiche dans le navigateur, et la conception
    s'effectue 'à la main' :
    - clic gauche sur une arête -> arête de l'énigme (en noir)
    - clic milieu sur une arête -> arête de la solution (en rouge)
    - clic droit -> dessin d'un losange

    Le bouton de sauvegarde de l'url permet de récupérer l'url dans le PP

2) lancement de checkGrid avec une url non vide
    (Exemple d'url :
    "https://mathix.org/calisson/index.html?tab=fffstffsfftfffsfsssffsftsffftf")

    - la grille s'ouvre dans le navigateur
    - une fenêtre graphique de résolution de la grille est affichée

    Si la grille n'a qu'une seule solution, tout va bien :-)

    Sinon, il faut corriger la grille (c'est le cas de l'url donnée en exemple).
    L'utilisateur peut alors passer en mode "modification de grille" en faisant
    'Alt-Clic_gauche) dans la grille.
    La page HTML passe alors en mode "conception de grille", permettant
    les mêmes opérations que dans le mode d'utilisation (1)

    La copie de l'url de la grille modifiée permet alors  de recommencer
    la vérification en relançant checkGrid avec cette nouvelle url.

    Attention : la fenêtre graphique d'affichage de la grille est souvent bloquante
    pour le programme python (ça dépend du backend de python, donc de
    l'environnement de développement utilisé).
    Il faut donc la fermer avant de relancer la vérification.


"""

from calisson import test_solver
from html_calisson import make_enigma_from_url, make_url
import webbrowser

# -------- A AJUSTER -----------
# les deux variables qui suivent sont à définir en fonction de
# l'environnement de travail

# navigateur  préféré
prefBrowser = 'Safari' # ou 'Chrome', 'Firefox'

# répertoire de travail
localDir = '/Users/martial/Desktop/calisson 2/calisson_js/'
# -----------------------------

# pour travailler localement, sans accès internet
def openLocalBrowser(orgurl = ""):
    """
    orgurl est l'url d'une grille sur le site mathix
    On ouvre la grille fournie en argument dans le navigateur préféré en
    transformant l'url d'origine en une url locale.
    C'est alors le script javascript modifié qui s'exécute,
    permettant ainsi l'édition de la grille.
    """

    if orgurl == "":
        localurl = localDir + 'calisson.html'
    else:
        localurl = localDir + 'calisson.html?tab=' + orgurl.split('=')[-1]

    webbrowser.get('Safari').open('file://' + localurl)


def checkGrid(orgurl):
    """
    Arg : l'url d'une grille

    Pour la vérification d'une grille :
    - ouvre le navigateur local avec le script local
    - affiche la résolution de l'énigme
    """
    if orgurl == "":
        openLocalBrowser(orgurl)
    else:
        openLocalBrowser(orgurl)
        dim, enigme = make_enigma_from_url(orgurl)
        test_solver(enigme, dim)


""" Tests
- évaluer d'abord la ligne suivante :

from verif_calisson import checkGrid

- puis évaluer un à un les blocs de codes entre '----------------'

# -----------------------------------
# %% conception à partir de rien ...

checkGrid("")

# -----------------------------------
# la grille exemple donnée dans le commentaire du code (deux solutions)

orgurl="https://mathix.org/calisson/index.html?tab=fffstffsfftfffsfsssffsftsffftf"

checkGrid(orgurl)

# -----------------------------------
# Cette même grille après correction

orgurl="https://mathix.org/calisson/index.html?tab=fssffssftstffsfsfstfffsfffsftf"

checkGrid(orgurl)

# -----------------------------------
# énigme 216 (cubes indéterminés)

orgurl="mathix.org/calisson/index.html?tab=fffffstfffffffsssfsfsfssfffstfftsfssstsfffsftfssssfsffsffffsfffsffsfffttfsfssfffftfffsstffsfsfssffffsfffsfsssstfffsffffffffstfssffffsfsffssssfsfffffstfsftffsffffffffssffffssssfffsfsfsfstffsfstfffffffsfsffssffsffftfffftfsssfssffffsffftffsffsftftssffftfffffsfsfsfsftffsffffssstftffsffsffsfsffstfsfffsfftfffsf216"

checkGrid(orgurl)

# -----------------------------------
# énigme 216 corrigée (3 arêtes ajoutées)

orgurl = "https://mathix.org/calisson/index.html?tab=fffffstfffffffsssfsfsfssfffstfftsfssstsfffsftfssssfsffsffffsfffsffsfffttfsfssfffftfffsstfftfsfssffffsfffsfsssstfffsffffffffstfssffffsfsffssssfsfffffstfsftffsffffffffssfffftsssfffsfsfsfstffsfstfffffffsfsffssffsffftfffftfsstfssffffsffftffsffsftftssffftfffffsfsfsfsftffsffffssstftffsffsffsfsffstfsfffsfftfffsf216"

checkGrid(orgurl)
# -----------------------------------

"""
