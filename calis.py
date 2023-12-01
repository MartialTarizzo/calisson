#!/usr/local/bin/python3

# %% Jeu du calisson
# calis.py : fichier destiné à étre utilisé sur la ligne de commande dans un terminal
#
# ============================================================================
# Auteur : Martial Tarizzo
#
# Licence : CC BY-NC-SA 4.0 DEED
# https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr
# ============================================================================

import argparse


import os
from gen_calisson import randomEnigma, randomEnigma_fromConstraints
import verif_calisson
from verif_calisson import checkGrid, make_url_sol, openLocalBrowser, prefBrowser
from html_calisson import make_enigma_from_url, make_url

verif_calisson.prefBrowser = 'Safari'

def generate_enigma(dim, method):
    if method == 1:
        enigme = randomEnigma(dim, trace = True)
    elif method == 2:
        enigme = randomEnigma_fromConstraints(dim, trace = True)

    url = make_url(enigme, dim)
    return url

# -----------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("--size", help="generated grid size",
                    type=int)

parser.add_argument("--method", help="generation method to use (1 = fast, 2 = slow)",
                    type=int)

args = parser.parse_args()

dim = args.size
method = args.method

verif_calisson.localDir = os.getcwd() + "/calisson_js/"
verif_calisson.prefBrowser = "Safari"

print(f"génération d'une éngime de taille {dim} (méthode {method})")

url = generate_enigma(dim, method)

print("génération terminée. url :")
print(url)
openLocalBrowser(url)

