# Résolution du jeu du calisson

## Le jeu du calisson
Pour une présentation du jeu, voir le site du créateur Olivier Longuet, accessible ici :
[Le jeu du calisson](https://mathix.org/calisson/blog/)
## Présentation du projet
Le but est ici d'automatiser la résolution et la conception de grilles de jeu, à l'aide de quelques programmes Python.
Les bibliothèques utilisées sont classiques : numpy et pyplot.

Les fichiers, comportant de nombreux commentaires, sont pour l'instant destinés à être chargés dans un environnement de développement (Pyzo, Spyder, Visual Studio, ...) afin de pouvoir lancer les différentes fonctions (exemples d'utilisations fournis).

Les fonctions contenues dans ces fichiers ne permettent pas l'interactivité fournie par la page web de mathix, mais peuvent servir à :
- créer des empilements aléatoires de cubes
- représenter graphiquement ces empilements
- générer automatiquemment une énigme (une grille de jeu) à partir d'un empilement
- résoudre une énigme (générée automatiquement, faite 'à la main', récupérée sur le site mathix) et représenter graphiquement la solution
- lancer l'interface de résolution d'une énigme sur le site mathix 

## Les différents fichiers
Seuls les fichiers python (*.py) sont intéressants à télécharger, afin de pouvoir les exécuter dans son nvironnement de développement favori.
- calisson.py : contient les fonctions de représentation graphique ainsi que celles permettant la résolution d'une énigme
- gen_calisson.py : contient les fonctions permettant la génération automatique (et aléatoire) d'un empilement ainsi que d'une énigme
- html_calisson : contient les fonctions d'interfaçage avec mathix.org (récupération d'une énigme présente sur le site et résolution, lancement du site sur une énigme générée localement pour une résolution manuelle)
- tests_calisson.py : comme son nom l'indique, fichiers de test divers et variés de résolutions d'énigmes.

Le répertoire calisson_js ne contient qu'une copie de la page HTML de mathix permettant la résolution d'une énigme. Cela peut être utilisé depuis python pour tenter une résolution dans l'interface HTML sans avoir de connexion internet active. 





