"""
Le code d'origine du fichier javascript traçant les différents segments de la figure

but : transformer ce code en python

v1x = -Math.sqrt(3) * longueur / 2
v1y = longueur / 2;
v2x = 0;
v2y = longueur;
v3x = Math.sqrt(3) * longueur / 2
v3y = longueur / 2;
centrex = Math.sqrt(3) / 2 * longueur * taille + marge
centrey = marge;
 for (j = 0; j < 2 * taille; j++) {
            for (i = 0; i < Math.min(taille + 1, 2 * taille - j); i++) {
                k = 0;
                if ((j > 0) && (i < taille)) {
                    tabsegment.push([
                        [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                        [centrex + (i + 1) * v1x + j * v2x + k * v3x, centrey + (i + 1) * v1y + j * v2y + k * v3y]
                    ])
                }
                if (i < taille) {
                    tabsegment.push([
                        [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                        [centrex + i * v1x + (j + 1) * v2x + k * v3x, centrey + i * v1y + (j + 1) * v2y + k * v3y]
                    ])
                }
                if (i > 0) {
                    tabsegment.push([
                        [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                        [centrex + i * v1x + j * v2x + (k + 1) * v3x, centrey + i * v1y + j * v2y + (k + 1) * v3y]
                    ])
                }
            }
        }

partie droite
for (j = 0; j < 2 * taille; j++) {
        for (k = 0; k < Math.min(taille + 1, 2 * taille - j); k++) {

            i = 0;

            if ((j > 0) && (k < taille)) {
                tabsegment[cpt] = [
                    [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                    [centrex + i * v1x + j * v2x + (k + 1) * v3x, centrey + i * v1y + j * v2y + (k + 1) * v3y]
                ];
            }
            if ((k < taille) && (k > 0)) {

                tabsegment[cpt] = [
                    [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                    [centrex + i * v1x + (j + 1) * v2x + k * v3x, centrey + i * v1y + (j + 1) * v2y + k * v3y]
                ];
            }
            if (k > 0) {

                tabsegment[cpt] = [
                    [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                    [centrex + (i + 1) * v1x + j * v2x + k * v3x, centrey + (i + 1) * v1y + j * v2y + k * v3y]
                ];
}
v1x = -longueur
v1y = longueur;
v2x = 0;
v2y = 2*longueur;
v3x = longueur
v3y = longueur;
"""

import numpy as np

def make_tab_segments(taille=3):
    # Les coordonnées javascript sont avec origine en haut et axe y vers le bas.
    # le codage des coordonnées pour mes fonctions est avec origine au centre et axe y vers le haut
    # cette fonction effectue la transformation js -> python
    def transf_coord(tab):
        for p in tab:
            p[0][1] = 2*taille - p[0][1]
            p[1][1] = 2*taille - p[1][1]

    tabsegment = []

    # tout ce qui suit n'est qu'une reprise du code JS, avec simplifications
    # car des variables sont inutiles (constamment nulles ...), et mes coordonnées
    # sont entières

    # partie gauche
    for j in range(2*taille):
        for i in range(min(taille+1, 2*taille-j)):
            if j>0 and i<taille:
                tabsegment.append([[-i, i + 2*j],
                            [-(i + 1), (i + 1) + 2*j]])
            if i<taille:
                tabsegment.append([[-i,  i  + 2*j],
                            [ -i, i + 2*(j+1)]])
            if i>0:
                tabsegment.append([[-i, i  + 2*j],
                            [-i + 1, i + 2*j + 1]])
    # partie droite sans la ligne verticale x==0
    for j in range(2 * taille):
            for k in range(min(taille + 1, 2 * taille - j)):
                if ((j > 0) and (k < taille)):
                    tabsegment.append([[ -i + k,2*j + k],
                        [(k + 1),  2*j + (k + 1)]])
                if ((k < taille) and (k > 0)):
                    tabsegment.append([[k,  2*j + k],
                        [ k,  2*(j + 1) + k]])
                if (k > 0):
                    tabsegment.append([[ k, 2*j + k],
                        [-1 + k, 1 + 2*j + k]])

    transf_coord(tabsegment)
    return tabsegment

import matplotlib.pyplot as plt

def line(A, B, **kwargs):
    """ trace une ligne dans le plan de figure entre les points A et B.
    Chaque point est représenté par un doublet [x, y] """
    plt.plot([A[0], B[0]], [A[1], B[1]], **kwargs)

def draw_config(tab):
    """
    dessine à l'aide de pyplot l'empilement de cubes codé en 3D dans jeu.
    """
    plt.figure(figsize=(6, 6))
    # l'aspect sqrt(2/6) est nécessaire en raison de la simplification
    # du calcul des projections (cf fonction 'projection)
    plt.subplot(111,adjustable='box', aspect=1/np.sqrt(3))
    #plt.axis('equal')
    for li in tab:
        line(*li)
        plt.pause(0.5)
    plt.show()

ts = make_tab_segments(2)
draw_config(ts)

"""
ts vaut
[[[0, 4], [0, 2]],
 [[-1, 3], [-1, 1]],
 [[-1, 3], [0, 2]],
 [[-2, 2], [-1, 1]],
 [[0, 2], [-1, 1]],
 [[0, 2], [0, 0]],
 [[-1, 1], [-2, 0]],
 [[-1, 1], [-1, -1]],
 [[-1, 1], [0, 0]],
 [[-2, 0], [-1, -1]],
 [[0, 0], [-1, -1]],
 [[0, 0], [0, -2]],
 [[-1, -1], [-2, -2]],
 [[-1, -1], [-1, -3]],
 [[-1, -1], [0, -2]],
 [[0, -2], [-1, -3]],
 [[0, -2], [0, -4]],
 [[1, 3], [1, 1]],
 [[1, 3], [0, 2]],
 [[2, 2], [1, 1]],
 [[0, 2], [1, 1]],
 [[1, 1], [2, 0]],
 [[1, 1], [1, -1]],
 [[1, 1], [0, 0]],
 [[2, 0], [1, -1]],
 [[0, 0], [1, -1]],
 [[1, -1], [2, -2]],
 [[1, -1], [1, -3]],
 [[1, -1], [0, -2]],
 [[0, -2], [1, -3]]]

 """