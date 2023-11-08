import sys

print(sys.path)

from calisson import test_solver, listCoord3D
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

# %% Génération auto d'énigme
# Version bourrin :
# on génére des arêtes au hasard, et on espère qu'une solution va pouvoir s'en dégager.
# Dans la majorité des cas, ça ne marche pas ...
# Il faudrait plutôt s'inspirer des fonctions de la section 1 ********* A FAIRE ******

import random as rd

def randomEnigma(n, m):
    """
    retourne une éngme tirée au hasard dans un jeu de taille n, contenant m contraintes.
    """
    # validation de la contrainte
    def valid(x, y, d):
        # couple (x,y) valide ou pas ?
        if (x+y) % 2 != 0:
            return False

        # coordonnées et direction dans la zone de jeu ?
        if d=="x" and len(listCoord3D(x-1, y-1, n)) > 0:
            # contrainte sur un bord ?
            if (y==x+2*n) or (y==x-2*n):
                return False
            else:
                return True
        if d=="y" and len(listCoord3D(x+1, y-1, n)) > 0:
            if (y==-x+2*n) or (y==-x-2*n):
                return False
            else:
                return True
        if d=="z" and len(listCoord3D(x, y+2, n)) > 0:
            if x==-n or x==n:
                return False
            else:
                return True
        # contrainte incorrecte
        return False

    enig = []
    dirs = "xyz"
    while len(enig) < m:
        # coordonnées et direction au hasard
        x = rd.randint(-n, n)
        y = rd.randint(-2*n, 2*n)
        d = rd.randint(0,2)

        # coordonnées de l'origine de la contrainte valides ?
        l3D = listCoord3D(x,y,n)
        if len(l3D) > 0:
            li = (x, y, dirs[d])
            if valid(*li):
                enig.append(li)
    return enig

rdEnig = randomEnigma(4,10)

listSol = test_solver(rdEnig, 4)
print(rdEnig)

# %% Section 6 : énigmes aléatoires, puis solution unique 'à la main'

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

lsol = doSolve(enigme, 4)
draw_solutions(enigme, 4,lsol[0:], cellSize = 6)




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