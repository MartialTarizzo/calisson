# %% Jeu du calisson
# tests_calisson.py : test de la résolution automatique d'énigme
#
# ============================================================================
# Auteur : Martial Tarizzo
#
# Licence : CC BY-NC-SA 4.0 DEED
# https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr
# ============================================================================

# Évaluer la ligne suivante en premier
from calisson import test_solver

# puis évaluer les blocs de lignes (entre '# %%') pour résoudre chaque énigme

# %% taille 2 : en prendre une au choix ...

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

# %% taille 3.2

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


# %% taille 3.3

enigme=[(-2, 2, 'x'),
 (-1, 1, 'z'),
 (0, 4, 'y'),
 (-1, -1, 'y'),
 (1, -1, 'x'),
 (-2, -2, 'z'),
 (2, 2, 'x'),
 (2, -4, 'z')]
test_solver(enigme, 3)

# %% taille 3.4

enigme = [(1, 1, 'x'),(1, 1, 'y'), (-1, 3, 'z'),
# (1, -5, 'x'),
(0, -4, 'z'),(0, 4, 'y'), (0, -2, 'y'), (-2, 0, 'z')]

test_solver(enigme, 3)

# %% taille 3.5

enigme = [(1, 3, 'x'), (2, 2, 'z'), (-1, -3, 'z'),
(-2,0,"z"),
(0,-2,"y"),
(1,-1,"z"),
(0,0,"x")
]
test_solver(enigme, 3)


# %% taille 3.6

enigme = [(0, 2, 'x'), (-1, -1, 'x'), (-2, 2, 'x'),
#(-1, -1, 'z'),
 (2, 2, 'y'),
 (0, 2, 'y'),
(1,-3,"z"),
(-1,-3,"y") ]
test_solver(enigme, 3)

# %% taille 3.7

enigme = \
[(1,3,"x"),
(2,-2,"z"),
(2,2,"x"),
(0, -4, 'z'),
 (1, -1, 'x'), (-1, -1, 'x'), (2, -2, 'x'), (-2, -2, 'z'),
(-1,3,"x"),(-1,3,"y")]
test_solver(enigme, 3)

# %% taille 3.8

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

# %% taille 4.1
# construit à partir d'une énigme précédente (3.2), en ajoutant "à la main" des arêtes qui
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


# %% taille 4.2 difficile (pas de bord, pas d'esquisse de face)

enigme = [
 (2, -2, 'x'),
 (0, -4, 'y'),
 (-1,-3,"x"),
 (1,5,"y"),
 (-3,-1,"z"),
 (-2, 4, 'y'),
 (0, 4, 'y'),
 (-1, 5, 'y'),
 (2,0,"y"),
 (1,-1,"x"),
 (3, 1, 'z'),
 (-1, 1, 'y'),
 (-1, -1, 'x')
 ]

test_solver(enigme, 4)

# %% taille 4.3

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

## taille 4.4
enigme =[
(-1,3,"y"),
(-2,2,"x"),
(-2,0,"x"),
(0,4,"y"),
(-2,4,"x"),
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


## taille 4.5 : 3 solutions
enigme =[
(-1,3,"y"),
(-2,2,"x"),
(-2,0,"x"),
(1,3,"x"),

# decommenter pour fixer la solution
#(-1,-1,"z"),

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

## taille 5.1
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

# %% taille 5.2, difficile ...
enigme = [(-2, 0, 'x'), (2, -2, 'x'), (-2, -2, 'y'), (-1, 7, 'y'), (2, -4, 'y'),
(-3,3,'z'),
(-4,-4,'y'),
(-1,-1,'z'),
(0,-6,'x'),
(2,2,'y'),
(3,1,'y'),
(2,4,'z'),
(0,8,'y'),
(3,-1,'y'),
(1,-5,'x'),
(3, 3, 'z'), (-3, 1, 'x'), (0, -4, 'x'), (1, 1, 'x'), (-1, 3, 'z')
]
test_solver(enigme, 5)

# %% taille 5.3 plus facile
enigme = \
[(-1, -3, 'z'),
# (-4, -6, 'z'),
 (-4, -4, 'z'),
 (-4, -2, 'z'),
 (-3, -5, 'z'),
 (0, 2, 'z'),
 (0, 2, 'x'),
 (-1, 5, 'z'),
 (3, -3, 'z'),
 (2, 0, 'y'),
 #(2, 2, 'y'),
 (-2,2,"x"),
 (1, -5, 'z'),
 (-2, 0, 'x'),
 (3, 1, 'y'),
 (-1, 9, 'y'),
 (4, -6, 'z'),
 (2, 4, 'y'),
 (1,7, 'x'),
 (1, -3, 'z'),
 (-2, 4, 'x'),
 (-1, -5, 'z'),
 #(-3, -1, 'y'),
 (1, 3, 'z')]
test_solver(enigme, 5)

# %% taille 6.1 (grille mathix 447 corrigée)
# 447 incomplète ... 1 cube indéterminé

enigme = [(-4, 8, 'y'),
 (-1, 7, 'z'),
 (-2, 4, 'z'),
 (-4, 4, 'y'),
 (-3, 1, 'x'),
 (-5, -1, 'x'),
 (-1, 1, 'x'),
 (-1, -3, 'z'),
 (-3, -3, 'x'),
 (-4, -8, 'z'),
 (-1, -7, 'z'),
 (3, 7, 'z'),
 (4, 6, 'y'),
 (1, 7, 'x'),
 (5, 1, 'z'),
 (2, 4, 'x'),
 (3, 1, 'z'),
 (4, 0, 'z'),
 (2, 2, 'x'),
 (4, -2, 'y'),
 (1, -3, 'z'),
 (2, -2, 'y'),
 (3, -7, 'z'),
 (1, -5, 'x'),
 (1, -11, 'z')

# une des lignes ci-dessous lève l'indétermination
,(0,2,"z")
#,(0,4,"z")
#,(-1,3,"y")
#,(-1,3,"z")
]

test_solver(enigme, 6)

# %% taille 6.2 - générée automatiquement
# jolie d'origine, et rendue encore plus difficile en changeant 2 arêtes
enigme = [(-1, -3, 'x'),
 (-1, 1, 'x'),
 (0,-2,'z'),#(-1, -1, 'z'),
 (-1, 3, 'x'),
 (4, 2, 'x'),
 (1, -1, 'y'),
 (-5, 1, 'y'),
 (2, -4, 'x'),
 (-1, 7, 'x'),
 (4, -6, 'z'),
 (0, -6, 'z'),
 (2, 6, 'x'),
 (-3, 3, 'x'),
 (-3, 5, 'y'),
 (0, 10, 'y'),
 (2, 4, 'y'),
 (-2, 0, 'x'),
 (-5, -1, 'x'),
 (4,0,'y'), #(3, -1, 'z'),
 (2, 8, 'x'),
 (-1, -3, 'z'),
 (-4, -6, 'z'),
 #(2, -4, 'z'),
 (-1, -5, 'x'),
 (4, -2, 'y'),
 (-3, -5, 'z'),
 (1, 3, 'x'),
 (2, -6, 'y'),
 (3, -1, 'x')]

test_solver(enigme, 6)