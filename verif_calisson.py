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

Le point d'entrée principal est la fonction checkGrid.

Deux utilisations possibles :

1) Conception d'une grille à partir de rien
    a) on lance d'abord checkGrid avec une url vide ( "" ) :
     C'est le fonctionnement classique pour le concepteur de grille.
     Une grille vide s'affiche dans le navigateur, et la conception
     s'effectue 'à la main' :
     - clic gauche sur une arête -> arête de l'énigme (en noir)
     - clic milieu sur une arête -> arête de la solution (en rouge)
     - clic droit -> dessin d'un losange
     rem : on peut se contenter des clic-gauche pour dessiner l'énigme
          et s'en remettre à Python pour la résoudre ... voir ci-dessous

     Le bouton de sauvegarde de l'url permet alors de récupérer l'url dans le PP

    b) on relance checkgrid en collant l'url depuis le PP.
     Le programme va alors tenter de résoudre l'énigme, afficher la fenêtre
     de résolution et lancer la page HTML.

     Si l'énigme a une seule solution, c'est parfait. on passe au point (c)
     Sinon, on retouche l'énigme dans la page HTML (on passe en mode
     "modification de grille" en faisant Alt-clic_gauche sur la grille).
     Quand les modifs sont faites, on génére l'url de la grille retouchée,
     on la copie dans le PP.
     Pour pouvoir relancer le code python, on ferme la fenêtre d'affichage
     des solutions, et on retourne en (b)
     (On peut fermer ou non la fenête du navigateur. Si on ne la ferme pas,
     le prochain affichage se fera dans un nouvel onglet. Cela permet au besoin
     de comparer avec une version précédente, voire de revenir en arrière en
     récupérant l'url dans l'onglet correspondant)

    c) Quand l'énigme a une seule solution, il suffit d'appeler la fonction
     make_url_sol avec la dernière url copiée dans le PP.
     Le navigateur s'ouvre sur la page HTML et la fenêtre de calcul de la
     solution est affichée. Le passage en mode retouche de la grille permet
     une ultime vérification avant de copier l'url définitive, dont on fait
     ce qu'on veut !

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

    Ceci permet de corriger à moindre frais une énigme défectueuse.

Attention : la fenêtre graphique d'affichage de la grille résolue est souvent
bloquante pour le programme python (ça dépend du backend de python, donc de
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
localDir = '/Users/martial/Desktop/calisson/calisson_js/'
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

    webbrowser.get(prefBrowser).open('file://' + localurl)


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
        enigme, dim = make_enigma_from_url(orgurl)
        test_solver(enigme, dim)

def make_url_sol(url):
    """
    Arg : une url pour une grille ayant une solution unique et correcte, mais
          ne contenant pas nécessairement les arêtes correctes de la solution)

    Retourne l'url complète (avec la solution correcte) pour utilisation
    définitive
    """
    return make_url(*make_enigma_from_url(url))


# %% #######################################
""" 
Tests : quelques résultats obtenus avec le mode d'emploi décrit ci-dessus

- évaluer ce fichier ou incorporer la ligne suivante dans un fichier vide :

from verif_calisson import checkGrid, make_url_sol

- puis évaluer (ou coller dans le fichier vide) un à un les blocs de codes entre '----------------'
"""
# -----------------------------------
# %% conception à partir de rien ...
"""
url = ""

checkGrid(url)

"""
# %% Joyeux Noël !

url = "https://mathix.org/calisson/index.html?tab=ffffffffffffffffftfffftfffffffffffffffffffffffffffffttftfffffffffffffftfftfffttfffffffffffftffftfffffffffffftfffffftffffffffffffffffffffffffffffffffffffffttfffftfffffffffffffftfftfffffffffffffffffffftffffffffffftttfftffffffffffffffftffffffffffffffffffffffffffffffftffffffffffffftffffffffffffffffffffffffftfffffffffffffffffffffffffffftfftfffffffffffffttffftfffffffffftffftffftfffffftfftftffffftffffffffffffffffffffffffftfffffffffffffffffftfffftfftffffftfffffffffffffffffffffftffftffffffftftfftffffffffffttfffffffffffffftfffffffffffffffftffffffffffffffff"

checkGrid(url)

"""
l'évaluation de 

solurl = make_url_sol(url)

donne :
'https://mathix.org/calisson/index.html?tab=fffffssfffffffffstsffftfsfssffsfffssffffsfsffffffffsttftfsfsfssffffffstsftfsfttssfsffsffssftfsftsssfsffsffsftfsssfstsfsffsffsffsfsfffsfffssfsffsfsffsfsfsfttfsfftsfsfffffsfsffftfftffsfffsfsffffsfsfssftfsfsffssffftttfftfsfsfffffsfsffftfsffffffffsfsffsffffffffsfffffstsfsfffffssfsftffsffffffssfffffffffssffftfsfssffsfffssffffssffffffffstsftfsfsfssfffffsttfsftfssssfsfsftssftfsftsssfsftfststfsffstssfsfsfssssfsffsffsfffsfstssfsffsffsffsffsfftfsfftfftffsfftffsffsffffsffsffsffsfftfsftffssffstftfftsfsfffffsfttffsfffsfffffsftfsffffffffsffffstsfsffffssfsfffsf'

"""


# %% Essais de conception à la main sur plusieurs prénoms
## Edith

url = "https://mathix.org/calisson/index.html?tab=ffffffffffffffffffttfftfffffffffftfffftfftfffffffffffffttftffffffffffftffffffffftfffftfffffffffftffffffffftffffffffffffffffffftffffffffffftffffffffffffttfffffffffftftfffffffffffffffffffffffffffffffftftfffffffff"
checkGrid(make_url_sol(url))


# %%  Arnaud

url = "https://mathix.org/calisson/index.html?tab=fffffffttffffffsssftfsftstsftfsfssstfsfffssfffsffsffsfffsffffsftfsffsffsfffsfffsffffsfsfffttfsfsfftfsfttffffffffffffssfffffttsftffsffsfsffsffsffsffffsffsffsffsffffsfftfftfsfssfftfsftsttfsfssssftfsftfsfsffffffff"
checkGrid((url))

# %%#

# Violaine_1
url = "https://mathix.org/calisson/index.html?tab=fffffssfffffsssftfsftfssfftfsfsfffsfftfffffsfffffsfsftsffsfsfttsfffsffssftfsftfssfsfsfsstfsfsftfssfsffffffffffffffssffffttsftffsfffffftfsffssfsfttfsfsfssfftfsftsffsffsftfffsffffsfsfsfttfsfsstsftfsfsfsfsffffffff"

checkGrid((url))

# %%
# Violaine_2
url = "https://mathix.org/calisson/index.html?tab=fffffssfffffsssftfsftfssfftfsfsfffsfftfffffsfffffsfsftsffsfsfttsfffsffssftfsftfstfsfsfsstfsfsfsfssfsffffffffffffffssffffttsftffsfffffftfsffssfsfttfsfsfssfftfsftsffsffsftfffsffffsfsfsfttfsfsstsftfsfsfsfsffffffff"

checkGrid((url))

# -----------------------------------


# %% segments placés à la main, un peu partout au pif

url = "https://mathix.org/calisson/index.html?tab=fffffffttfffffffffftftfffffffffftfffffffffffftfffffffffffftffffffffffftf"

checkGrid(url)

checkGrid(make_url_sol(url))

# -----------------------------------
# %% grille Bonjour

checkGrid(make_url_sol("https://mathix.org/calisson/index.html?tab=fffffffffffffffttfftfffffffffftftfftfffffttffffftffffffffffffffftffffffffffffftfffffttftffffffftffffffftffffffffffffffffffffffttfftffffttffffffffffffftfffffffffffffffffffffftfffffftfftfffffftffftfffffffffftffff"))

# -----------------------------------

# %%grille calisson 1

checkGrid(make_url_sol("https://mathix.org/calisson/index.html?tab=fffffffffffffftffffffffffffffftfffftffffttffffffffftfffffffffffffffffftfftftffftfffffftffffftffftffffffffffffffffffffffftffffffffffffffffftffffftfffffftfffffffffftffffffffffftffffffffttfffffttftffffffftffffffff"))

# -----------------------------------

# %% calisson 2
checkGrid("https://mathix.org/calisson/index.html?tab=fffssffffftsfsfsfstffftsfsftstsfffsfsftsfssfsfsssfffsfftffsffsfffffsfffffsftfsftsfsfftsfffsftfstfsffffffffffffffssfffffsftfsfsfssffffstssfsfftfffffffsffsffsfffffffsffsfsfsfttffsftsttftfsfssftfsftfffsfffffffffff")


# -----------------------------------

# %% calisson 3

checkGrid(make_url_sol("httpf://mathix.org/califfon/index.html?tab=ffffffffffttftfffftffftfftfffffffffffftfffffffffffffffftffffffffffffffffffftffftffffftfffffftfftffffffffffffffffffffffffftfffffffffffftfffffftffffffffffffffffffffffffffffffttfffftfttftfffffftffftfffffffffffffff"))

# -----------------------------------
# %% la grille exemple donnée dans le commentaire du code (deux solutions)

orgurl="https://mathix.org/calisson/index.html?tab=fffstffsfftfffsfsssffsftsffftf"

checkGrid(orgurl)

# -----------------------------------
# %% Cette même grille après correction

orgurl="https://mathix.org/calisson/index.html?tab=fssffssftstffsfsfstfffsfffsftf"

checkGrid(orgurl)

# -----------------------------------
# %% énigme 216 (cubes indéterminés)

orgurl="mathix.org/calisson/index.html?tab=fffffstfffffffsssfsfsfssfffstfftsfssstsfffsftfssssfsffsffffsfffsffsfffttfsfssfffftfffsstffsfsfssffffsfffsfsssstfffsffffffffstfssffffsfsffssssfsfffffstfsftffsffffffffssffffssssfffsfsfsfstffsfstfffffffsfsffssffsffftfffftfsssfssffffsffftffsffsftftssffftfffffsfsfsfsftffsffffssstftffsffsffsfsffstfsfffsfftfffsf216"

checkGrid(orgurl)

# -----------------------------------
# %% énigme 216 corrigée (3 arêtes ajoutées)

orgurl = "https://mathix.org/calisson/index.html?tab=fffffstfffffffsssfsfsfssfffstfftsfssstsfffsftfssssfsffsffffsfffsffsfffttfsfssfffftfffsstfftfsfssffffsfffsfsssstfffsffffffffstfssffffsfsffssssfsfffffstfsftffsffffffffssfffftsssfffsfsfsfstffsfstfffffffsfsffssffsffftfffftfsstfssffffsffftffsffsftftssffftfffffsfsfsfsftffsffffssstftffsffsffsfsffstfsfffsfftfffsf216"

checkGrid(orgurl)

"""
# ----------------------
# %% pour tester des énigmes générées automatiquement

# ------------------ première méthode ------------
# rapide, mais donne des grilles grossières

from gen_calisson import randomEnigma

dim = 2
enigme = randomEnigma(dim, trace = True)

checkGrid(make_url(enigme, dim))


# ------------------ deuxième méthode ------------
# lente, mais grille qui ressemblent à celles faites à la main

from gen_calisson import randomEnigma_fromConstraints

dim = 2
enigme = randomEnigma_fromConstraints(dim, trace = True)

checkGrid(make_url(enigme, dim))

# -----------------------------------

"""