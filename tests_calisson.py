import random as rd
from calisson import test_solver, listCoord3D, draw_config

#enigme = ((-1, 1, "y"), (0, 0, "y"), (0, 2, "z"))
# %% taille 2
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


# %% taille 3

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

# %% taille 4
# construit à partir du précédent (taille 3), en ajoutant "à la main" des arêtes qui
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


## 4 difficile (pas de bord, pas d'esquisse de face)
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


# %% Section 6 : énigmes aléatoires, puis retouchées 'à la main'

enigme=[(-2, 2, 'x'),
 (-1, 1, 'z'),
 (0, 4, 'y'),
 (-1, -1, 'y'),
 (1, -1, 'x'),
 (-2, -2, 'z'),
 (2, 2, 'x'),
 (2, -4, 'z')]
listSol = test_solver(enigme, 3)

# %%
# Exemples de résultats obtenus (n=3, m=6)

enigme = [(1, 1, 'xy'), (-1, 3, 'z'),
#(1, -5, 'x'),
(0, -4, 'z'),(0, 4, 'y'), (0, -2, 'y'), (-2, 0, 'z')]

test_solver(enigme, 3)

## taille 3
enigme = [(1, 3, 'x'), (2, 2, 'z'), (-1, -3, 'z'),
(-2,0,"z"),
(0,-2,"y"),
(1,-1,"z"),
(0,0,"x")
]
test_solver(enigme, 3)


## taille 3
enigme = [(0, 2, 'x'), (-1, -1, 'x'), (-2, 2, 'x'),
#(-1, -1, 'z'),
 (2, 2, 'y'),
 (0, 2, 'y'),
(1,-3,"z"),
(-1,-3,"y") ]
test_solver(enigme, 3)

## taille 4
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

## taille 4
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


## 3 solutions
enigme =[
(-1,3,"y"),
(-2,2,"x"),
(-2,0,"x"),
(1,3,"x"),

# fixe la solution
(-1,-1,"z"),

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

## taille 5
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

###### BUG ?
enigme =[
(-1,3,"y"),
(-2,2,"x"),
(-2,0,"x"),
(1,3,"x"),

# tracé incorrect si la ligne suivante est active
#(-1,3,"x"),

 (1, -5, 'z'),
 (-3, 3, 'z'),
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

##
enigme = \
[(1,3,"x"),
(2,-2,"z"),
(2,2,"x"),
(0, -4, 'z'),
 (1, -1, 'x'), (-1, -1, 'x'), (2, -2, 'x'), (-2, -2, 'z'),
(-1,3,"xy")]
test_solver(enigme, 3)
##
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

## 5 difficile ...
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

## 5 plus facile
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