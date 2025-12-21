# %% mkPdfGrids.py 
# Ce fichier est destiné à la production de grilles à imprimer pour le jeu du calisson

# La fonction utile est makePdfPages, située à la fin du fichier.

# Toutes les fonctions qui précèdent sont des adaptations de fonctions équivalentes (voire identiques)
# situées dans d'autres fichiers.
# Elles ont en général subi de légères modifications pour générer une sortie matplotlib dans un subplot 
# plutôt que le plot entier.


#%% Les importations système
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

#%% les importations de génération d'énigme et de résolution

from gen_calisson import randomEnigma2
from evalLosanges import calcListLosAcuteFold

from calisson import doSolve

#%% Reprise du code contenu dans calisson.py
# argument ax ajouté si nécessaire pour dessiner dans un subplot

# Les couleurs

# 1) pour les tracés de lignes
color_enigme = "black"
color_grid = "gray"
color_solution = "red"
color_indet = "gray"

# 2) pour le coloriage des losanges
color_poly_xy = "aqua"  # losange horizontal
color_poly_xz = "pink"  # losange incliné vers la droite
color_poly_yz = "khaki"  # losange incliné vers la gauche

color_poly_xy = "yellow"  # losange horizontal
color_poly_xz = "cyan"  # losange incliné vers la droite
color_poly_yz = "magenta"  # losange incliné vers la gauche



# Deux utilitaires
def line(ax, A, B, **kwargs):
    """trace une ligne dans le plan de figure entre les points A et B.
    Chaque point est représenté par un doublet [x, y]"""
    ax.plot([A[0], B[0]], [A[1], B[1]], **kwargs)


# Passage 3D -> 2D
def projection(A):
    """formules de la projection orthographique.
    A est un point de l'espace 3D, défini par ses coordonnées [x,y,z]
    Retourne  les coordonnées de la projection de A dans le plan de figure
    """
    x, y, z = A[0], A[1], A[2]
    # return [1/np.sqrt(2) * (y - x), 1/np.sqrt(6) * (2 * z - (x + y))]
    #
    # La formule 'officielle' ci-dessus effectue la projection dans une base du
    # plan de figure orthonormée.
    # En omettant les facteurs d'échelle, il faudra fixer le rapport d'affichage
    # dans les fonctions de tracé pour compenser.
    # L'avantage est que le pointeur de souris dans la fenêtre de tracé
    # indique correctement les coordonnées utilisées pour le codage des énigmes
    return [y - x, 2 * z - (x + y)]


def lineproj(ax, A, B, **kwargs):
    """dessine la ligne entre les points 3D A et B dans le plan de projection"""
    Ap = projection(A)
    Bp = projection(B)
    line(ax, Ap, Bp, **kwargs)


# dessin de l'aire de jeu
def drawHex(ax, n):
    """tracé de l'hexagone qui représente la projection du grand cube
    de rangement"""

    # les lignes intérieures
    opt = {"color": color_grid, "linestyle": "dashed", "linewidth": 1}
    for i in range(n + 1):
        lineproj(ax, [-n + i, 0, i], [n, 0, i], **opt)
        lineproj(ax, [0, -n + i, i], [0, n, i], **opt)
        lineproj(ax, [i, -n + i, 0], [i, n, 0], **opt)
        lineproj(ax, [-n + i, i, 0], [n, i, 0], **opt)
        lineproj(ax, [i, 0, -n + i], [i, 0, n], **opt)
        lineproj(ax, [0, i, -n + i], [0, i, n], **opt)
    # le bord
    opt = {"color": color_enigme, "linewidth": 2}

    lineproj(ax, [0, 0, n], [n, 0, n], **opt)
    lineproj(ax, [n, 0, n], [n, 0, 0], **opt)
    lineproj(ax, [n, 0, 0], [n, n, 0], **opt)
    lineproj(ax, [n, n, 0], [0, n, 0], **opt)
    lineproj(ax, [0, n, 0], [0, n, n], **opt)
    lineproj(ax, [0, n, n], [0, 0, n], **opt)


def draw_enigma(ax, e):
    opt_enig = {"color": color_enigme, "linewidth": 3}
    for p in e:
        x0, y0 = p[:2]
        d = p[2]
        if "x" == d:
            line(ax, [x0, y0], [x0 - 1, y0 - 1], **opt_enig)
        if "y" == d:
            line(ax, [x0, y0], [x0 + 1, y0 - 1], **opt_enig)
        if "z" == d:
            line(ax, [x0, y0], [x0, y0 + 2], **opt_enig)


# Le dessin des calissons : losanges remplis selon les trois couleurs color_poly...
def drawPolygons(ax, jeu):
    """
    jeu est la matrice 3D représentant l'empilement des cubes
    dessine les losanges correspondants aux faces visibles des petits cubes, ainsi
    que les faces visibles du grand cube englobant.
    """

    # les trois fonctions qui suivent dessinent les différentes faces à partir
    # du point de coordonnées 3D (i,j,k)
    def losange_xy(i, j, k):
        A = projection([i, j, k])
        B = projection([i + 1, j, k])
        C = projection([i + 1, j + 1, k])
        D = projection([i, j + 1, k])
        lX = [p[0] for p in (A, B, C, D)]
        lY = [p[1] for p in (A, B, C, D)]
        ax.fill(lX, lY, facecolor=color_poly_xy)

    def losange_xz(i, j, k):
        A = projection([i, j, k])
        B = projection([i, j, k + 1])
        C = projection([i + 1, j, k + 1])
        D = projection([i + 1, j, k])
        lX = [p[0] for p in (A, B, C, D)]
        lY = [p[1] for p in (A, B, C, D)]
        ax.fill(lX, lY, facecolor=color_poly_xz)

    def losange_yz(i, j, k):
        A = projection([i, j, k])
        B = projection([i, j, k + 1])
        C = projection([i, j + 1, k + 1])
        D = projection([i, j + 1, k])
        lX = [p[0] for p in (A, B, C, D)]
        lY = [p[1] for p in (A, B, C, D)]
        ax.fill(lX, lY, facecolor=color_poly_yz)

    # Balayage de tous les cubes de l'empilement
    n = jeu.shape[0]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if jeu[i, j, k] == -1:  # cube indéterminé -> on ne fait rien
                    continue

                if jeu[i, j, k] == 1:
                    # cube rempli: on ne dessine que les faces au niveau du grand cube
                    if i == n - 1:
                        losange_yz(i + 1, j, k)
                    if j == n - 1:
                        losange_xz(i, j + 1, k)
                    if k == n - 1:
                        losange_xy(i, j, k + 1)
                    continue
                # cube vide : on ne dessine que si les cubes qui l'entourent sont remplis
                # ou si on se trouve sur les faces du grand cube passant par l'origine
                if i == 0 or jeu[i - 1, j, k] == 1:
                    losange_yz(i, j, k)
                if j == 0 or jeu[i, j - 1, k] == 1:
                    losange_xz(i, j, k)
                if k == 0 or jeu[i, j, k - 1] == 1:
                    losange_xy(i, j, k)


# Dessin des arêtes d'un petit cube de coordonnées 3D [i,j,k]
# On tient compte de l'environnement du cube pour le dessiner que les arêtes
# nécessaires.
# Le cube est dessiné en gris si inderterminé
def projCube(ax, jeu, i, j, k):
    n = jeu.shape[0]

    def c(i, j, k):
        """test de la présence d'un cube aux coordonnées [i,j,k]
        Avec prise en compte des bords pour contrôler le tracé des arêtes.
        """
        if i < 0 or j < 0:
            return True
        if k < 0:
            return True
        if k == n:
            return False
        if i == n or j == n:
            return False
        return jeu[i, j, k]  # on n'est pas sur un bord

    if jeu[i, j, k] == 1:  # cube certain
        # options de tracé des cubes certains
        opt = {"color": color_solution, "linewidth": 3}

        # SA est le sommet d'origine du cube, jamais visible.
        # S1 .. S7 désigne les 7 sommets potentiellement visibles
        # S1..S4 sont les 4 sommets de la face supérieure
        # S5..S7 sont les 3 sommets de la face inférieure
        SA = np.array([i, j, k])
        S1 = np.array([0, 0, 1]) + SA
        S2 = np.array([1, 0, 1]) + SA
        S3 = np.array([1, 1, 1]) + SA
        S4 = np.array([0, 1, 1]) + SA
        S5 = np.array([1, 0, 0]) + SA
        S6 = np.array([1, 1, 0]) + SA
        S7 = np.array([0, 1, 0]) + SA
        # on ne trace les lignes entre les différents sommets que si
        # la ligne est nécessaire, ce qui dépend de la présence des autres cubes
        # au voisinage du cube courant.
        # L1 : ligne entre S1 et S2
        if c(i, j - 1, k + 1) and not c(i, j, k + 1):
            lineproj(ax, S1, S2, **opt)
        # L2 : S2-S3
        if not c(i + 1, j, k) and not c(i, j, k + 1):
            lineproj(ax, S2, S3, **opt)
        # L3 : S3-S4
        if not c(i, j + 1, k) and not c(i, j, k + 1):
            lineproj(ax, S3, S4, **opt)
        # L4 : S4-S1
        if not c(i, j, k + 1) and c(i - 1, j, k + 1):
            lineproj(ax, S4, S1, **opt)
        # L5 : S2-S5
        if not c(i + 1, j, k) and c(i + 1, j - 1, k):
            lineproj(ax, S2, S5, **opt)
        # L6 : S3-S6
        if (not c(i + 1, j, k) and not c(i, j + 1, k)) or (
            c(i + 1, j, k) and c(i, j + 1, k) and not c(i + 1, j + 1, k)
        ):
            lineproj(ax, S3, S6, **opt)
        # L7 : S4-S7
        if not c(i, j + 1, k) and c(i - 1, j + 1, k):
            lineproj(ax, S4, S7, **opt)
        # L8 : S5-S6
        if not c(i + 1, j, k) and c(i + 1, j, k - 1):
            lineproj(ax, S5, S6, **opt)
        # L9 : S6-S7
        if not c(i, j + 1, k) and c(i, j + 1, k - 1):
            lineproj(ax, S6, S7, **opt)
        # pour voir le dessin pas à pas. commenter pour un dessin rapide !
        # plt.pause(0.005)
    elif jeu[i, j, k] == -1:
        # options de tracé des cubes indéterminés
        opt_indet = {"color": color_indet, "linewidth": 4}
        SA = np.array([i, j, k])
        S1 = np.array([0, 0, 1]) + SA
        S2 = np.array([1, 0, 1]) + SA
        S3 = np.array([1, 1, 1]) + SA
        S4 = np.array([0, 1, 1]) + SA
        S5 = np.array([1, 0, 0]) + SA
        S6 = np.array([1, 1, 0]) + SA
        S7 = np.array([0, 1, 0]) + SA
        lineproj(ax, S1, S2, **opt_indet)
        lineproj(ax, S2, S3, **opt_indet)
        lineproj(ax, S3, S4, **opt_indet)
        lineproj(ax, S4, S1, **opt_indet)
        lineproj(ax, S2, S5, **opt_indet)
        lineproj(ax, S3, S6, **opt_indet)
        lineproj(ax, S4, S7, **opt_indet)
        lineproj(ax, S5, S6, **opt_indet)
        lineproj(ax, S6, S7, **opt_indet)


# dessin des axes non masqués par des cubes
def drawAxes(ax, jeu):
    """
    Dessin des projections des axes 3D x, y ou z si pas de cube pour les cacher
    """
    n = jeu.shape[0]
    opt = {"color": color_solution, "linewidth": 3}  # options de tracé des cubes
    for i in range(n):
        if not jeu[0, 0, i]:
            lineproj(ax, [0, 0, i], [0, 0, i + 1], **opt)
        if not jeu[0, i, 0]:
            lineproj(ax, [0, i, 0], [0, i + 1, 0], **opt)
        if not jeu[i, 0, 0]:
            lineproj(ax, [i, 0, 0], [i + 1, 0, 0], **opt)


# tracé de la configuration
def draw_config(ax, jeu):
    """
    dessine à l'aide de pyplot l'empilement de cubes codé en 3D dans jeu.
    """
    n = jeu.shape[0]
    drawPolygons(ax, jeu)
    drawHex(ax, n)
    drawAxes(ax, jeu)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                projCube(ax, jeu, i, j, k)




#%% Reprise du code contenu dans gen_grilles.py

# la fonction suivante est initialement une fonction interne
# de la fonction generate_grids (dans gen_grilles.py)
# Présente ici comme fonction globale.

def makeEnigma(size, level):
    # le dictionnaire des pourcentage de filtrage 
    # pour l'évaluation de la difficulté des grilles en fonction
    # de la proportion "p" d'arêtes trouvables par angle aigu/pli

    # Pour une grille (taille, niveau), la grille sera retenue
    # si "p" est dans l'intervalle correspondant.
    # Par exemple, une grille de taille 4 et de niveau 3 sera retenue 
    # si 0.2 <= p <= 0.8
    # Les bornes du tableau qui suit sont issus d'une étude statistique
    # portant sur plusieurs dizaines de grilles de chaque type.
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

    # Les bornes de l'évaluation de la difficulté de la grille
    p1, p2 = dictP[(size, level)]
    
    while True:
        if level == 1:
            enigme = randomEnigma2(size, easy=10)
        elif level == 2:
            enigme = randomEnigma2(size, easy=5)
        elif level == 3:
            enigme = randomEnigma2(size, easy=0)
        
        # évaluation de la difficulté de la grille
        p = len(calcListLosAcuteFold(enigme, size)) / (3 * size ** 2)
        if p1 <= p <= p2:
            # énigme retenue !
            return enigme


# %% La fonction de fabrication des fichiers PDF
def makePdfPages(racineNomFichier, nPages=1, tailleGrille=4, niveau=1):
    """Fabrique dans le répertoire courant un fichier PDF contenant
    des énigmes et leurs solutions pour le jeu du calisson.
    Il y a 6 énigmes par page. Les pages des énigmes précèdent les pages des solutions.

    Args:
        racineNomFichier (string): début du nom de fichier généré
        nPages (int, optional): nombre de pages d'énigmes (6énigmes par page). 
        Defaults to 1.
        tailleGrille (int, optional): taille des grilles générées. Defaults to 4.
        niveau (int, optional): niveau des grilles. Defaults to 1.
    """
    # Le nombre de grilles par page
    nPageGrids = 6

    print(f'Génération des énigmes {tailleGrille}.{niveau}')
    # La liste des énigmes
    l_enigmes = [
        makeEnigma(tailleGrille, niveau)
        for _ in range(nPageGrids * nPages)
    ]
    # La liste des solutions associées
    l_solutions = [doSolve(enigme, tailleGrille, False)[0] for enigme in l_enigmes]

    print("Grilles et solutions calculées")

    # Instantiating PDF document
    pdf = PdfPages(f"{racineNomFichier}_{6 * nPages}_{tailleGrille}.{niveau}.pdf")

    print("Création des pages des énigmes")
    idxGrid = 0
    nc, nl = 2, 3
    plt.rcParams["figure.constrained_layout.use"] = True

    for idxPage in range(nPages):
        fig, axs = plt.subplots(ncols=nc, nrows=nl, figsize=(21 / 2.54, 29.7 / 2.54))

        for row in range(nl):
            for col in range(nc):
                drawHex(axs[row, col], tailleGrille)
                draw_enigma(axs[row, col], l_enigmes[idxGrid])
                axs[row, col].axis("off")
                axs[row, col].set_aspect(1 / np.sqrt(3))
                axs[row, col].set_title(f"grille {idxGrid+1}")

                idxGrid += 1
        fig.suptitle(f"Grilles de taille {tailleGrille}, niveau {niveau}")
        pdf.savefig(fig)
        plt.close()
        print(f'page {idxPage + 1}')

    print("Création des pages des solutions")

    idxGrid = 0

    # nc, nl = 2, 3
    # plt.rcParams["figure.constrained_layout.use"] = True
    for idxPage in range(nPages):
        fig, axs = plt.subplots(ncols=nc, nrows=nl, figsize=(21 / 2.54, 29.7 / 2.54))

        for row in range(nl):
            for col in range(nc):

                draw_config(axs[row, col], l_solutions[idxGrid])
                draw_enigma(axs[row, col], l_enigmes[idxGrid])
                axs[row, col].axis("off")
                axs[row, col].set_aspect(1 / np.sqrt(3))
                axs[row, col].set_title(f"grille {idxGrid+1}")

                idxGrid += 1
        fig.suptitle(f"Solutions des grilles de taille {tailleGrille}, niveau {niveau}")
        pdf.savefig(fig)
        plt.close()
        print(f'page {nPages + idxPage + 1}')

    pdf.close()
    print(f'Fin de création du fichier {racineNomFichier}_{6 * nPages}_{tailleGrille}.{niveau}.pdf')

# %% pour tester
makePdfPages("GrillesCalisson", nPages=4, tailleGrille=3, niveau=3)

# %% génération de 12 énigmes (2 pages d'énigmes) pour toutes les tailles/niveaux
for taille in [3,4, 5, 6]:
    for niveau in [1, 2, 3]:
        makePdfPages("GrillesCalisson", nPages=2, tailleGrille=taille, niveau=niveau)
