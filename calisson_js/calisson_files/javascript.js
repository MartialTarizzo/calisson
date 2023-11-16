/* 
javascript.js pour la page HTML de Calisson
*/

////////////////////////////////////////////////////
// Réglage de l'interface et initialisations diverses
////////////////////////////////////////////////////

taille = Number(document.getElementById("taille").value);
longueur = Number(document.getElementById("longueur").value);
marge = 5;
mode = "arete";

// valeurs utilisées pour le calcul des coordonnées des points/segments
v1x = -Math.sqrt(3) * longueur / 2
v1y = longueur / 2;
v2x = 0;
v2y = longueur;
v3x = Math.sqrt(3) * longueur / 2
v3y = longueur / 2;
centrex = Math.sqrt(3) / 2 * longueur * taille + marge
centrey = marge;

// définit le 'style' (???) d'interaction avec le jeu
// true -> on peut modifier la grille
// false -> grille non modifiable, on peut téléverser la solution trouvée, etc.
style = true;

// on cache le bouton de téléchargement de la solution
document.getElementById('terminedl').style.display = "none";

// Les 3 tableaux de travail, unidimentionnels
// pour les arêtes, contient des [[xa,ya],[xb,yb]], coord des extrémités des segments
tabsegment = [] 

/****************************************************
 tabmilieu est Le tableau fondamental, contenant la plus grande partie des infos sur la grille
 ce tableau contient des tableuax de la forme [x, y, traceSegment, typeLosange, affichelosange]

- x, y : coordonnées du milieu de l'arête
- traceSegment : valeur parmi (true, false, 'bloquee', 'solution')
    true -> segment présent tracé en noir avec point médian pour modification
    false -> segment absent tracé en pointillés avec point médian pour modification
    bloquee -> segment de l'énigme, tracé en noir et non modifiable
    solution -> tracé en rouge, permet de définir la solution de l'énigme lors de la conception de la grille
  En mode jeu, seules les trois première valeurs sont utilisées.
- typeLosange : valeur parmi ('gauche', 'hori', 'droite') en fonction de l'orientation du losange
- afficheLosange : booléen définissant l'affichage ou non du losange
*****************************************************/
tabmilieu = []  

// solution contient true, false ou "bloquee"
// "bloquee" -> arête fixée non modifiable. Fait partie de la solution 
//      <=> arête de l'énigme toujours affichée dans la page web
//  true -> arête de la solution, non affichée pendant le jeu (ça serait trop facile !)
// false -> arête ne faisant pas partie de la solution
solution = []; 

// modejeu est un drapeau permettant de savoir si on est mode jeu ou design
modejeu = false;
// la chaine contenue dans l'url contient-elle la solution ?
solutionpresente = false;

// différents compteurs
nblosangeutilise = 0;
chrono = 0;
chronofin = 0;

// le numéro de la grille si présent à la fin de l'url
numerogrille = '';

// réglage de l'interface sur un écran tactile 
var is_touch_device = function() {
    try {
        document.createEvent("TouchEvent");
        return true;
    } catch (e) {
        return false;
    }
}

if (!(is_touch_device())) {
    document.getElementById('btmode').style.display = 'none';
    document.getElementById('explicationcontrole').style.display = '';
    document.getElementById('explicationcontroleportable').style.display = 'none';
} else {
    document.getElementById('explicationcontrole').style.display = 'none';
    document.getElementById('explicationcontroleportable').style.display = '';
}

// variables permettant les dessins dans la page du navigateur
// canvas principal 
canvas = document.getElementById('canvas');
if (!canvas) {
    alert("Impossible de récupérer le canvas");
}
// et son contexte
context = canvas.getContext('2d');
if (!context) {
    alert("Impossible de récupérer le context du canvas");

}

// copie du canvas pour la miniature affichée à la fin du jeu au dessus du message de succès
canvasbis = document.getElementById('canvasbis');
if (!canvasbis) {
    alert("Impossible de récupérer le canvasbis");
}

contextbis = canvasbis.getContext('2d');
if (!contextbis) {
    alert("Impossible de récupérer le context du canvas");

}
// effacement de la zone de jeu
function clearCanvas() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    var w = canvas.width;
    canvas.width = 1;
    canvas.width = w;
    context.beginPath();
    context.fillStyle = "white";
    context.fillRect(0, 0, canvas.width, canvas.height);
    context.closePath();
}

// remet tout dans l'état de départ et dessine la figure
function rafraichit() {
    clearCanvas();

    taille = Number(document.getElementById("taille").value);
    longueur = Number(document.getElementById("longueur").value);
    canvas.width = Math.sqrt(3) * taille * longueur + 2 * marge;
    canvas.height = taille * longueur * 2 + 2 * marge;

    v1x = -Math.sqrt(3) * longueur / 2
    v1y = longueur / 2;
    v2x = 0;
    v2y = longueur;
    v3x = Math.sqrt(3) * longueur / 2
    v3y = longueur / 2;
    centrex = Math.sqrt(3) / 2 * longueur * taille + marge
    centrey = marge;

    miseajourpoint();   // remplit les tableaux de travail
    dessinerlafigure()  // puis affichage
}

// recalcule toutes les grandeurs géométriques dans tabsegment et tabmilieu
function miseajourpointencours() {
    cpt = 0;
    console.log(taille)
    //côté gauche avec diagonale verticale
    for (j = 0; j < 2 * taille; j++) {

        for (i = 0; i < Math.min(taille + 1, 2 * taille - j); i++) {
            k = 0;
            if ((j > 0) && (i < taille)) {
                tabsegment[cpt] = [
                    [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                    [centrex + (i + 1) * v1x + j * v2x + k * v3x, centrey + (i + 1) * v1y + j * v2y + k * v3y]
                ];
                tabmilieu[cpt][0] = centrex + (i + 0.5) * v1x + j * v2x + k * v3x;
                tabmilieu[cpt][1] = centrey + (i + 0.5) * v1y + j * v2y + k * v3y;
                cpt++
            }
            if (i < taille) {
                tabsegment[cpt] = [
                    [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                    [centrex + i * v1x + (j + 1) * v2x + k * v3x, centrey + i * v1y + (j + 1) * v2y + k * v3y]
                ];
                tabmilieu[cpt][0] = centrex + i * v1x + (j + 0.5) * v2x + k * v3x;
                tabmilieu[cpt][1] = centrey + i * v1y + (j + 0.5) * v2y + k * v3y;
                cpt++
            }
            if (i > 0) {
                tabsegment[cpt] = [
                    [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                    [centrex + i * v1x + j * v2x + (k + 1) * v3x, centrey + i * v1y + j * v2y + (k + 1) * v3y]
                ];
                tabmilieu[cpt][0] = centrex + i * v1x + j * v2x + (k + 0.5) * v3x;
                tabmilieu[cpt][1] = centrey + i * v1y + j * v2y + (k + 0.5) * v3y;
                cpt++
            }
        }
    }
    //côté droite sans diagonale verticale
    for (j = 0; j < 2 * taille; j++) {
        for (k = 0; k < Math.min(taille + 1, 2 * taille - j); k++) {

            i = 0;

            if ((j > 0) && (k < taille)) {
                tabsegment[cpt] = [
                    [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                    [centrex + i * v1x + j * v2x + (k + 1) * v3x, centrey + i * v1y + j * v2y + (k + 1) * v3y]
                ];
                tabmilieu[cpt][0] = centrex + i * v1x + j * v2x + (k + 0.5) * v3x;
                tabmilieu[cpt][1] = centrey + i * v1y + j * v2y + (k + 0.5) * v3y;
                cpt++
            }
            if ((k < taille) && (k > 0)) {

                tabsegment[cpt] = [
                    [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                    [centrex + i * v1x + (j + 1) * v2x + k * v3x, centrey + i * v1y + (j + 1) * v2y + k * v3y]
                ];
                tabmilieu[cpt][0] = centrex + i * v1x + (j + 0.5) * v2x + k * v3x;
                tabmilieu[cpt][1] = centrey + i * v1y + (j + 0.5) * v2y + k * v3y;
                cpt++
            }

            if (k > 0) {

                tabsegment[cpt] = [
                    [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                    [centrex + (i + 1) * v1x + j * v2x + k * v3x, centrey + (i + 1) * v1y + j * v2y + k * v3y]
                ];
                tabmilieu[cpt][0] = centrex + (i + 0.5) * v1x + j * v2x + k * v3x;
                tabmilieu[cpt][1] = centrey + (i + 0.5) * v1y + j * v2y + k * v3y;
                cpt++
            }
        }
    }
}

// Remet les trois tableaux de travail dans l'état de départ
function miseajourpoint(chaine) {
    if (chaine == undefined) {
        tabsegment = [];
        tabmilieu = [];
        //côté gauche avec diagonale verticale
        for (j = 0; j < 2 * taille; j++) {
            for (i = 0; i < Math.min(taille + 1, 2 * taille - j); i++) {
                k = 0;
                if ((j > 0) && (i < taille)) {
                    tabsegment.push([
                        [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                        [centrex + (i + 1) * v1x + j * v2x + k * v3x, centrey + (i + 1) * v1y + j * v2y + k * v3y]
                    ])
                    tabmilieu.push([centrex + (i + 0.5) * v1x + j * v2x + k * v3x, centrey + (i + 0.5) * v1y + j * v2y + k * v3y, false, "gauche", false])

                }
                if (i < taille) {
                    tabsegment.push([
                        [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                        [centrex + i * v1x + (j + 1) * v2x + k * v3x, centrey + i * v1y + (j + 1) * v2y + k * v3y]
                    ])
                    tabmilieu.push([centrex + i * v1x + (j + 0.5) * v2x + k * v3x, centrey + i * v1y + (j + 0.5) * v2y + k * v3y, false, "hori", false])
                }
                if (i > 0) {
                    tabsegment.push([
                        [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                        [centrex + i * v1x + j * v2x + (k + 1) * v3x, centrey + i * v1y + j * v2y + (k + 1) * v3y]
                    ])
                    tabmilieu.push([centrex + i * v1x + j * v2x + (k + 0.5) * v3x, centrey + i * v1y + j * v2y + (k + 0.5) * v3y, false, "droite", false])
                }
            }
        }
        //côté droit sans diagonale verticale
        for (j = 0; j < 2 * taille; j++) {
            for (k = 0; k < Math.min(taille + 1, 2 * taille - j); k++) {
                i = 0;
                if ((j > 0) && (k < taille)) {
                    tabsegment.push([
                        [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                        [centrex + i * v1x + j * v2x + (k + 1) * v3x, centrey + i * v1y + j * v2y + (k + 1) * v3y]
                    ])
                    tabmilieu.push([centrex + i * v1x + j * v2x + (k + 0.5) * v3x, centrey + i * v1y + j * v2y + (k + 0.5) * v3y, false, "droite", false])
                }
                if ((k < taille) && (k > 0)) {
                    tabsegment.push([
                        [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                        [centrex + i * v1x + (j + 1) * v2x + k * v3x, centrey + i * v1y + (j + 1) * v2y + k * v3y]
                    ])
                    tabmilieu.push([centrex + i * v1x + (j + 0.5) * v2x + k * v3x, centrey + i * v1y + (j + 0.5) * v2y + k * v3y, false, "hori", false])
                }
                if (k > 0) {
                    tabsegment.push([
                        [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                        [centrex + (i + 1) * v1x + j * v2x + k * v3x, centrey + (i + 1) * v1y + j * v2y + k * v3y]
                    ])
                    tabmilieu.push([centrex + (i + 0.5) * v1x + j * v2x + k * v3x, centrey + (i + 0.5) * v1y + j * v2y + k * v3y, false, "gauche", false])
                }
            }
        }
    } else {
        var p = 0;
        tabsegment = [];
        tabmilieu = [];
        solution = []
        //côté gauche avec diagonale verticale
        for (j = 0; j < 2 * taille; j++) {
            for (i = 0; i < Math.min(taille + 1, 2 * taille - j); i++) {
                k = 0;
                if ((j > 0) && (i < taille)) {
                    tabsegment.push([
                        [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                        [centrex + (i + 1) * v1x + j * v2x + k * v3x, centrey + (i + 1) * v1y + j * v2y + k * v3y]
                    ])
                    if (chaine[p] == 't') {
                        tabmilieu.push([centrex + (i + 0.5) * v1x + j * v2x + k * v3x, centrey + (i + 0.5) * v1y + j * v2y + k * v3y, "bloquee", "gauche", false])
                        solution.push('bloquee')
                    } else {

                        tabmilieu.push([centrex + (i + 0.5) * v1x + j * v2x + k * v3x, centrey + (i + 0.5) * v1y + j * v2y + k * v3y, false, "gauche", false])
                        if (chaine[p] == 's') {
                            solution.push(true)
                        } else {
                            solution.push(false)
                        }
                    }
                    p++;
                }
                if (i < taille) {
                    tabsegment.push([
                        [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                        [centrex + i * v1x + (j + 1) * v2x + k * v3x, centrey + i * v1y + (j + 1) * v2y + k * v3y]
                    ])
                    if (chaine[p] == 't') {
                        tabmilieu.push([centrex + i * v1x + (j + 0.5) * v2x + k * v3x, centrey + i * v1y + (j + 0.5) * v2y + k * v3y, 'bloquee', "hori", false])
                        solution.push('bloquee')
                    } else {
                        tabmilieu.push([centrex + i * v1x + (j + 0.5) * v2x + k * v3x, centrey + i * v1y + (j + 0.5) * v2y + k * v3y, false, "hori", false])
                        if (chaine[p] == 's') {
                            solution.push(true)
                        } else {
                            solution.push(false)
                        }
                    }
                    p++;
                }
                if (i > 0) {
                    tabsegment.push([
                        [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                        [centrex + i * v1x + j * v2x + (k + 1) * v3x, centrey + i * v1y + j * v2y + (k + 1) * v3y]
                    ])
                    if (chaine[p] == 't') {
                        tabmilieu.push([centrex + i * v1x + j * v2x + (k + 0.5) * v3x, centrey + i * v1y + j * v2y + (k + 0.5) * v3y, 'bloquee', "droite", false])
                        solution.push('bloquee')
                    } else {
                        tabmilieu.push([centrex + i * v1x + j * v2x + (k + 0.5) * v3x, centrey + i * v1y + j * v2y + (k + 0.5) * v3y, false, "droite", false])
                        if (chaine[p] == 's') {
                            solution.push(true)
                        } else {
                            solution.push(false)
                        }
                    }
                    p++;
                }
            }
        }
        //côté droite sans diagonale verticale
        for (j = 0; j < 2 * taille; j++) {
            for (k = 0; k < Math.min(taille + 1, 2 * taille - j); k++) {
                i = 0;
                if ((j > 0) && (k < taille)) {
                    tabsegment.push([
                        [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                        [centrex + i * v1x + j * v2x + (k + 1) * v3x, centrey + i * v1y + j * v2y + (k + 1) * v3y]
                    ])
                    if (chaine[p] == 't') {
                        tabmilieu.push([centrex + i * v1x + j * v2x + (k + 0.5) * v3x, centrey + i * v1y + j * v2y + (k + 0.5) * v3y, 'bloquee', "droite", false])
                        solution.push('bloquee')
                    } else {
                        tabmilieu.push([centrex + i * v1x + j * v2x + (k + 0.5) * v3x, centrey + i * v1y + j * v2y + (k + 0.5) * v3y, false, "droite", false])
                        if (chaine[p] == 's') {
                            solution.push(true)
                        } else {
                            solution.push(false)
                        }
                    }
                    p++;
                }
                if ((k < taille) && (k > 0)) {
                    tabsegment.push([
                        [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                        [centrex + i * v1x + (j + 1) * v2x + k * v3x, centrey + i * v1y + (j + 1) * v2y + k * v3y]
                    ])
                    if (chaine[p] == 't') {
                        tabmilieu.push([centrex + i * v1x + (j + 0.5) * v2x + k * v3x, centrey + i * v1y + (j + 0.5) * v2y + k * v3y, 'bloquee', "hori", false])
                        solution.push('bloquee')
                    } else {
                        tabmilieu.push([centrex + i * v1x + (j + 0.5) * v2x + k * v3x, centrey + i * v1y + (j + 0.5) * v2y + k * v3y, false, "hori", false])
                        if (chaine[p] == 's') {
                            solution.push(true)
                        } else {
                            solution.push(false)
                        }
                    }
                    p++;
                }
                if (k > 0) {
                    tabsegment.push([
                        [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                        [centrex + (i + 1) * v1x + j * v2x + k * v3x, centrey + (i + 1) * v1y + j * v2y + k * v3y]
                    ])
                    if (chaine[p] == 't') {
                        tabmilieu.push([centrex + (i + 0.5) * v1x + j * v2x + k * v3x, centrey + (i + 0.5) * v1y + j * v2y + k * v3y, 'bloquee', "gauche", false])
                        solution.push('bloquee')
                    } else {
                        tabmilieu.push([centrex + (i + 0.5) * v1x + j * v2x + k * v3x, centrey + (i + 0.5) * v1y + j * v2y + k * v3y, false, "gauche", false])
                        if (chaine[p] == 's') {
                            solution.push(true)
                        } else {
                            solution.push(false)
                        }
                    }
                    p++;
                }
            }
        }
    }
    console.log(tabmilieu)
}

function commencergrille() {

    document.getElementById('messagediv').style.display = "none";
    modejeu = true;
    chrono = 0;
    nblosangeutilise = 0;
    chronomarche();
    var tab = GET('tab');

    var yaunnombre = tab.match(/(\d+)/);

    if (yaunnombre) {
        numerogrille = yaunnombre[0];
        tab = tab.replace(numerogrille, '')
    } else {
        numerogrille = '';
    }

    if (GET('t') == undefined) {
        i = 0
        pastrouve = true
        while ((pastrouve) && (i < 30)) {
            i++;
            taillei = 3 * (3 * i * i - i);
            pastrouve = (taillei != tab.length)
        }
        taille = i;
    } else {
        taille = Number(GET('t'));
    }

    document.getElementById("taille").value = taille;
    rafraichit()
    document.getElementById('sptaille').style.display = "none";
    document.getElementById('genurl').style.display = "none";

    if (tab.indexOf('s') > -1) {
        solutionpresente = true;
        document.getElementById("chronospan").style.display = '';
        document.getElementById("chrono").innerHTML = chrono + ' s'
        document.getElementById("losange").style.display = '';
        document.getElementById("nblosange").innerHTML = '0';
    } else {
        solutionpresente = false;
        document.getElementById("chronospan").style.display = 'none';
        document.getElementById("losange").style.display = 'none';
    }

    v1x = -Math.sqrt(3) * longueur / 2
    v1y = longueur / 2;
    v2x = 0;
    v2y = longueur;
    v3x = Math.sqrt(3) * longueur / 2
    v3y = longueur / 2;
    centrex = Math.sqrt(3) / 2 * longueur * taille + marge
    centrey = marge;

    miseajourpoint(tab)
    dessinerlafigure()
}

// Associée au bouton 'Reset' : annule les actions de l'utilisateur
function reset() {
    //chronoarret();
    chronofin = 0;
    for (i = 0; i < tabmilieu.length; i++) {
        {
            if (tabmilieu[i][2] == true) {
                tabmilieu[i][2] = false;
            }
            if (tabmilieu[i][4] == true) {
                tabmilieu[i][4] = false;
            }
        }
    }
    dessinerlafigure()

    if (GET('tab') == undefined) {
        rafraichit()
        modejeu = false;
        solutionpresente = false;
        document.getElementById("chronospan").style.display = 'none';
        document.getElementById("losange").style.display = 'none';
        document.getElementById('messagediv').style.display = "none";
    } else {
        dessinerlafigure()
    }
}

function partage() {
    url = "https://mathix.org/calisson/index.html?tab=" + GET('tab');
    if (numerogrille != '') {
        window.open("https://twitter.com/intent/tweet?url=" + encodeURI(url) + "&text=J'ai réussi la grille n°" + numerogrille + " du @Jeuducalisson1 en " + chronofin + "s et en utilisant " + nblosangeutilise + " losange(s) !Vous saurez faire mieux ? ", "_blank ");
    } else {
        window.open("https://twitter.com/intent/tweet?url=" + encodeURI(url) + "&text=J'ai réussi une grille du @Jeuducalisson1 en " + chronofin + " s et en utilisant " + nblosangeutilise + " losange(s)! Vous saurez faire mieux ?", "_blank")
    }
}

// associée au bouton 'Ma grille est terminée'
function termine() {

    style = !style;

    dessinerlafigure();
    if (!style) {
        document.getElementById('terminedl').style.display = "";
        document.getElementById('termine').innerHTML = "Reprendre ma grille";
        document.getElementById('btreset').style.display = "none";
    } else {
        document.getElementById('terminedl').style.display = "none";
        document.getElementById('btreset').style.display = "";
        document.getElementById('termine').innerHTML = "Ma grille est terminée";
    }
    contextbis.drawImage(canvas, 0, 0, canvas.width, canvas.height, 0, 0, canvasbis.width, canvasbis.height);
}

function dessinerlafigure() {

    clearCanvas();
    for (i = 0; i < tabsegment.length; i++) {
        context.beginPath();
        context.lineWidth = 1;
        context.setLineDash([5, 10]);
        context.moveTo(tabsegment[i][0][0], tabsegment[i][0][1]);
        context.lineTo(tabsegment[i][1][0], tabsegment[i][1][1]);
        context.stroke();
        context.closePath();
    }

    //affichage des milieu et dessin du segments si doit être tracé.
    for (i = 0; i < tabmilieu.length; i++) {
        {
            if ((tabmilieu[i][2] == true) || (tabmilieu[i][2] == 'bloquee') || (tabmilieu[i][2] == 'solution')) { //on trace le segment si vrai
                context.beginPath();
                context.lineWidth = 5;
                context.setLineDash([]);
                context.moveTo(tabsegment[i][0][0], tabsegment[i][0][1])
                context.lineTo(tabsegment[i][1][0], tabsegment[i][1][1])
                if ((tabmilieu[i][2] == 'solution')) {
                    context.strokeStyle = "red";
                } else {
                    context.strokeStyle = "black";
                }
                context.stroke();
                context.closePath();
            }
            if ((tabmilieu[i][2] != 'bloquee') && (style)) {
                context.beginPath();
                context.lineWidth = 1;
                context.setLineDash([]);
                context.arc(tabmilieu[i][0], tabmilieu[i][1], 5, 0, 2 * Math.PI);
                context.fillStyle = "white";
                context.strokeStyle = "black";
                context.fill();
                context.stroke();
                context.closePath();
            }
            if ((tabmilieu[i][4]) && (style)) {
                var x = tabmilieu[i][0];
                var y = tabmilieu[i][1];
                switch (tabmilieu[i][3]) {
                    case "gauche":
                        x1 = x - 0.5 * v3x - 0.5 * v2x;
                        y1 = y - 0.5 * v3y - 0.5 * v2y;

                        x2 = x + 0.5 * v3x - 0.5 * v2x;
                        y2 = y + 0.5 * v3y - 0.5 * v2y;

                        x4 = x - 0.5 * v3x + 0.5 * v2x;
                        y4 = y - 0.5 * v3y + 0.5 * v2y;
                        x3 = x + 0.5 * v3x + 0.5 * v2x;
                        y3 = y + 0.5 * v3y + 0.5 * v2y;
                        couleur = "#ffe32e40";
                        break;
                    case "droite":
                        x1 = x + 0.5 * v2x - 0.5 * v1x;
                        y1 = y + 0.5 * v2y - 0.5 * v1y;

                        x3 = x - 0.5 * v2x + 0.5 * v1x;
                        y3 = y - 0.5 * v2y + 0.5 * v1y;

                        x2 = x - 0.5 * v2x - 0.5 * v1x;
                        y2 = y - 0.5 * v2y - 0.5 * v1y;

                        x4 = x + 0.5 * v2x + 0.5 * v1x;
                        y4 = y + 0.5 * v2y + 0.5 * v1y;
                        couleur = "#ff2e2e40";
                        break;
                    case "hori":
                        x2 = x - 0.5 * v1x - 0.5 * v3x
                        y2 = y - 0.5 * v1y - 0.5 * v3y

                        x1 = x + 0.5 * v1x - 0.5 * v3x
                        y1 = y + 0.5 * v1y - 0.5 * v3y
                        x3 = x - 0.5 * v1x + 0.5 * v3x
                        y3 = y - 0.5 * v1y + 0.5 * v3y

                        x4 = x + 0.5 * v1x + 0.5 * v3x
                        y4 = y + 0.5 * v1y + 0.5 * v3y
                        couleur = "#2eb3ff40";
                        break;

                }
                context.beginPath();
                context.fillStyle = couleur;
                context.lineWidth = 1;
                context.moveTo(x1, y1)
                context.lineTo(x2, y2)
                context.lineTo(x3, y3)
                context.lineTo(x4, y4)
                context.lineTo(x1, y1)
                context.fill();
                context.closePath();
            }
        }
    }
    //bordure
    for (i = 0; i < taille; i++) {
        context.beginPath();
        context.lineWidth = 5;
        context.strokeStyle = "black";
        context.setLineDash([]);
        context.moveTo(centrex + i * v1x, centrey + i * v1y)
        context.lineTo(centrex + (i + 1) * v1x, centrey + (i + 1) * v1y)
        context.moveTo(centrex + i * v1x + taille * v2x + taille * v3x, centrey + i * v1y + taille * v2y + taille * v3y)
        context.lineTo(centrex + (i + 1) * v1x + taille * v2x + taille * v3x, centrey + (i + 1) * v1y + taille * v2y + taille * v3y)

        context.moveTo(centrex + i * v2x + taille * v1x, centrey + i * v2y + taille * v1y)
        context.lineTo(centrex + (i + 1) * v2x + taille * v1x, centrey + (i + 1) * v2y + taille * v1y)
        context.moveTo(centrex + i * v2x + taille * v3x, centrey + i * v2y + taille * v3y)
        context.lineTo(centrex + (i + 1) * v2x + taille * v3x, centrey + (i + 1) * v2y + taille * v3y)

        context.moveTo(centrex + i * v3x, centrey + i * v3y)
        context.lineTo(centrex + (i + 1) * v3x, centrey + (i + 1) * v3y)
        context.moveTo(centrex + i * v3x + taille * v2x + taille * v1x, centrey + i * v3y + taille * v2y + taille * v1y)
        context.lineTo(centrex + (i + 1) * v3x + taille * v2x + taille * v1x, centrey + (i + 1) * v3y + taille * v2y + taille * v1y)

        context.stroke();
        context.closePath();
    }
}

function getMousePos(canvas, evt) {
    var rect = canvas.getBoundingClientRect();
    return {
        x: evt.clientX - rect.left,
        y: evt.clientY - rect.top
    };
}

canvas.addEventListener('pointerdown', function(evt) {
    ajouterenleversegment(evt)
}, false);

canvas.addEventListener('pointermove', function(evt) {
    curseur(evt)
}, false);
canvas.addEventListener('pointerout', function(evt) {
    dessinerlafigure()
}, false);

function ajouteunlosange(x, y) {
    var orientation;
    var booldejadessine;
    var s1, s2, s3, s4;
    booldejadessine = true;
    for (var i = 0; i < tabmilieu.length; i++) {
        if (Math.abs(x - tabmilieu[i][0]) < longueur / 5) {
            if (Math.abs(y - tabmilieu[i][1]) < longueur / 5) {
                if (tabmilieu[i][2] != 'bloquee') {
                    if ((!tabmilieu[i][4]) && (solutionpresente)) {
                        nblosangeutilise++;
                        document.getElementById('nblosange').innerHTML = nblosangeutilise;
                    }
                    tabmilieu[i][4] = !tabmilieu[i][4]
                    orientation = tabmilieu[i][3]
                }

            }
        }
    }
    //calculs des milieux des segments périphériques
    dessinerlafigure();

}

// MT+ pour passer du mode jeu au mode retouche de grille
function gotoDesign() {
    // MAJ de tabmilieu en fonction de solution
    for(var i = 0; i < solution.length; i++) {
        switch (solution[i]) {
            case true : tabmilieu[i][2]='solution'; break;
            case false : tabmilieu[i][2] = false; break;
            case 'bloquee' : tabmilieu[i][2] = true;
        } 
    }
    // réglage de l'interface : seul le bouton de génération du lien est actif
    document.getElementById('btreset').style.display = "none";
    document.getElementById('genurl').style.display = "";
    document.getElementById('terminedl').style.display = "none";
    document.getElementById('sptaille').style.display = "none";
    document.getElementById("chronospan").style.display = 'none';
    document.getElementById("losange").style.display = 'none';
    document.getElementById('termine').style.display = 'none';

    dessinerlafigure();
}
// MT-

// La fonction appelée à chaque clic de souris sur le point mileu d'un segment
function ajouterenleversegment(evt) {
    // console.log(evt.button);
    // +MT : si on appuie sur Alt (option sur mac) => passage en mode retouche de la grille
    if (evt.getModifierState('Alt')) {
        gotoDesign();
        return
    }
    //-MT

    if (style) {
        var pos = getMousePos(canvas, evt)
        var x = pos.x
        var y = pos.y
        if (evt.button == 1) {

            for (var i = 0; i < tabmilieu.length; i++) {
                if (Math.abs(x - tabmilieu[i][0]) < longueur / 5) {
                    if (Math.abs(y - tabmilieu[i][1]) < longueur / 5) {

                        if (tabmilieu[i][2] != 'bloquee') {
                            if (tabmilieu[i][2] != 'solution') {
                                tabmilieu[i][2] = "solution"
                            } else {
                                tabmilieu[i][2] = false;
                            }
                            console.log(tabmilieu[i][2]);
                        }
                        dessinerlafigure()
                        context.beginPath();
                        context.lineWidth = 1;
                        context.arc(tabmilieu[i][0], tabmilieu[i][1], 5, 0, 2 * Math.PI);
                        context.fillStyle = "black";
                        context.fill();
                        context.closePath();
                    }
                }
            }
        } else {
            if ((evt.button == 0) && (mode == "arete")) { //si pas clic droit

                for (var i = 0; i < tabmilieu.length; i++) {
                    if (Math.abs(x - tabmilieu[i][0]) < longueur / 5) {
                        if (Math.abs(y - tabmilieu[i][1]) < longueur / 5) {

                            if (tabmilieu[i][2] != 'bloquee') {
                                tabmilieu[i][2] = !tabmilieu[i][2];
                            }
                            dessinerlafigure()
                            context.beginPath();
                            context.lineWidth = 1;
                            context.arc(tabmilieu[i][0], tabmilieu[i][1], 5, 0, 2 * Math.PI);
                            context.fillStyle = "black";
                            context.fill();
                            context.closePath();
                        }
                    }
                }
            } else {
                ajouteunlosange(x, y)
                dessinerlafigure()
            }
        }
    }
    if (modejeu && solutionpresente) {
        if (testesolution()) {
            chronoarret()
            termine();
            dataURL = canvasbis.toDataURL();
            var chaine = "<img src='" + dataURL + "'/>"
            chaine = chaine + '<br/>Bravo! Vous avez fait un temps de ' + chronofin + ' s et utilisé ' + nblosangeutilise + ' losange(s).';
            document.getElementById('message').innerHTML = chaine;
            document.getElementById('messagediv').style.display = "";
        }
    }
}

function messageok() {
    document.getElementById('messagediv').style.display = "none";
}

function curseur(evt) {
    if (style) {
        var pos = getMousePos(canvas, evt)
        var x = pos.x
        var y = pos.y

        document.getElementById('canvas').style.cursor = 'auto';

        for (var i = 0; i < tabmilieu.length; i++) {
            if (Math.abs(x - tabmilieu[i][0]) < longueur / 5) {
                if (Math.abs(y - tabmilieu[i][1]) < longueur / 5) {
                    document.getElementById('canvas').style.cursor = 'pointer';
                    dessinerlafigure();
                    if (tabmilieu[i][2] != 'bloquee') {
                        context.beginPath();
                        context.lineWidth = 1;
                        context.arc(tabmilieu[i][0], tabmilieu[i][1], 5, 0, 2 * Math.PI);
                        context.fillStyle = "black";
                        context.fill();
                        context.closePath();
                    }
                }
            }
        }
    }
}
// associée au bouton de génération de l'url de la grille (mode design)
function genereurl() {
    chaine = "?tab=";

    for (i = 0; i < tabmilieu.length; i++) {
        if (tabmilieu[i][2] == true) {
            chaine = chaine + "t";
        } else {
            if (tabmilieu[i][2] == 'solution') {
                chaine = chaine + "s";
            } else {
                chaine = chaine + "f";
            }
        }
    }
    numerogrille = prompt('Indiquer le numéro de la grille (laisser vide si non défini');
    while (((isNaN(numerogrille))) && (numerogrille != '')) {
        numerogrille = prompt('Indiquer le numéro de la grille (laisser vide si non défini');
    }
     chaine = chaine + numerogrille
    copierdanspressepapier("https://mathix.org/calisson/index.html" + chaine)
    //	alert("Voici la chaîne à copier : https://mathix.org/calisson/index.html" + chaine)
}

function GET(param) {
    var vars = {};
    window.location.href.replace(location.hash, '').replace(
        /[?&]+([^=&]+)=?([^&]*)?/gi, // regexp
        function(m, key, value) { // callback
            vars[key] = value !== undefined ? value : '';
        }
    );

    if (param) {
        return vars[param] ? vars[param] : null;
    }
    return vars;
}

function chronomarche() {

    chronointerval = setInterval(function() {
        chrono++;
        document.getElementById("chrono").innerHTML = chrono + ' s'
    }, 1000);
}

function chronoarret() {
    chronofin = chrono;
    clearInterval(chronointerval);
}

function testesolution() {
    var bool = true;
    var i = 0;
    console.log(solution);
    console.log(solution[i] + "==" + tabmilieu[i][2])
    while ((i < tabmilieu.length) && (bool)) {
        bool = (solution[i] == tabmilieu[i][2])
        i++;
    }
    return ((i == solution.length) && (bool))
}

/////////////////////////////////////////////
// point d'entrée effectif
/////////////////////////////////////////////
function start() {
    if (GET('tab') == undefined) {
        rafraichit()
        modejeu = false;
        solutionpresente = false;
        document.getElementById("chronospan").style.display = 'none';
        document.getElementById("losange").style.display = 'none';
        document.getElementById('messagediv').style.display = "none";
    } else {
        commencergrille()
    }    
}

// On démarre !
start();

// on change la taille écran du graphique
function rafraichitlongueur() {
    longueur = Number(document.getElementById("longueur").value);
    if (GET('t') != undefined) {
        taille = Number(GET('t'));
        document.getElementById("taille").value = taille;
    }

    var tab = GET('tab');

    v1x = -Math.sqrt(3) * longueur / 2
    v1y = longueur / 2;
    v2x = 0;
    v2y = longueur;
    v3x = Math.sqrt(3) * longueur / 2
    v3y = longueur / 2;
    centrex = Math.sqrt(3) / 2 * longueur * taille + marge
    centrey = marge;
    canvas.width = Math.sqrt(3) * taille * longueur + 2 * marge;
    canvas.height = taille * longueur * 2 + 2 * marge;

    miseajourpointencours()
    dessinerlafigure()
}

// Associée au bouton de changement de mode pour interface tactile (arête/losange)
function changemode() {
    console.log(mode)
    if (mode == "arete") {
        mode = "losange";
        document.getElementById("btmode").innerHTML = "Mode losange";
    } else {
        mode = "arete";
        document.getElementById("btmode").innerHTML = "Mode arête";
    }
}

// empêche l'affichage du menu contextuel en cas de clic-droit sur la figure
canvas.oncontextmenu = function(event) {
    event.preventDefault();
}

// associée au bouton de téléchargement de l'image de la grille
function dl() {
    var canvas = document.getElementById("canvas");
    canvas.toBlob(function(blob) {
        saveAs(blob, "solution.png");
    });
}

function copierdanspressepapier(url) {
    // On tente d'écrire l'url directement dans le PP. Si le navigateur n'y arrive pas, on présente une fenêtre d'information
    // permettant de copier l'url "à la main"
    navigator.clipboard.writeText(url).then(function() {
        alert("Url dans le presse-papier!\n (controle-V pour coller l'url à l'endroit voulu) ");
    }, function() {
        prompt('Voici l\'url : ', url);
    });
}

// Fonction non utilisée. Certainement un vestige d'une tentative d'utilisation du PP
// mise en commentaires
/*
function copierdanspressepapier_back(url) {

    var content = document.getElementById('copiepressepapier');
    content.value = url;
    console.log(content)
    content.select();
    document.execCommand('copy');
    alert("Url dans le presse-papier!\n (controle-V pour coller l'url à l'endroit voulu) ");
}
*/