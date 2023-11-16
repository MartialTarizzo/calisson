# verif_calisson.py : fonctions de vérification d'une grille
#
# ============================================================================
# Auteur : Martial Tarizzo
#
# Licence : CC BY-NC-SA 4.0 DEED
# https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr
# ============================================================================

from calisson import test_solver
from html_calisson import make_enigma_from_url, make_url
import webbrowser

# à définir en fonction de l'environnement de travail
# navigateur  utiliser
prefBrowser = 'Safari' # ou 'Chrome', 'Firefox'

# répertoire de travail
localDir = '/Users/martial/Desktop/calisson 2/calisson_js/'

# pour travailler localement, sans accès internet
def openLocalBrowser(orgurl):
    """
    orgurl est l'url d'une grille sur le site mathix
    On ouvre la grille fournie en argument dans l'explorateur local, avec
    le script javascript modifié permettant l'édition de la grille
    """

    localurl = localDir + 'calisson.html?tab=' + orgurl.split('=')[-1]
    webbrowser.get('Safari').open('file://' + localurl)


def checkGrid(orgurl):
    """
    Pour la vérification d'une grille :
    - ouvre le navigateur local avec le script local
    - affiche la résolution de l'énigme
    """
    openLocalBrowser(orgurl)

    dim, enigme = make_enigma_from_url(orgurl)
    test_solver(enigme, dim)

##

orgurl = """https://mathix.org/calisson/index.html?tab=ffffffffffttftftffftffffftffffffffftffffffffffffffffftftftfffffffffftftfftfffffffffffftffffffftftfffffftfffffffffffffffftfffffftffffffftfffffffffffftfffffffffttffffffffftffffffffffffffffffffftfttffffftffftfffff"""

checkGrid(orgurl)

##
orgurl = "https://mathix.org/calisson/index.html?tab=fffffffssfffsssffsffftfftfffffsffstffffsfsfsfssffssfstffsssfsffsfftfsfffsftfsffssftstfsffstsfsfssfftfftffsfsfsfftsfsffssfsstfsffftffsfssfsfffffsffsssftfftsfsffffssfffffffsfsffsffffffffffftffssftsffsfffstffssfsffsfffsfsfssftfsfssffftfffsfffffstfssfffssfsfffffstssfsftfsffsfffstfsfffffsfffsstsfsffffssfsfffsf463"

checkGrid(orgurl)
##

orgurl = "file:///Users/martial/Desktop/calisson 2/calisson_js/calisson.html?tab=fffffffstfffsstffsfffsfsfsfssfsfsffsffsssfsffsffsftfffsftfsffsfsfftfsffsssfsfffftfsssffsftfsffsfftffsftfsssftfffsfftffffssftsssfsffffssftffsfftfsfffssfsftffsfffffffftsfffssffsfffsffsfffffsfstffffsffsffffffsfttffffstfsfssfftssfsfffsffssftsfsfstssfsfffsfftffffssftfffffsffffffsstsftffffsfsfsfsfftssssfsffsfsf448"

checkGrid(orgurl)
##
orgurl = """
https://mathix.org/calisson/index.html?tab=fssffffssftfssfffffssftsftffsfftssfsfsfssfffftfsfstffffssftsfffsfftsfsft
"""


checkGrid(orgurl)

##
orgurl= """
https://mathix.org/calisson/index.html?tab=fssfffffffftfsfffffffffffffsfttffsfffssfffsstsfffsfsftsffsfttffsssftffsssfffsfsfsffstfsffstsfsfsffsfsfstffffffssfffffffftfsfssfffffffsftftfssfffstfsfffsstfsfftffsfsfsftfftsfssfsfffsfffsffssfsttfffsfftfssfffffff
"""
checkGrid(orgurl)