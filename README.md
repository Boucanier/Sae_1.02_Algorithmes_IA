# Création d'IA en python

SAÉ 1.02 : Comparaison d'approches algorithmiques

## Lancement du programme

Afin de simuler une partie, il faut renseigner les IA utilisées en modifiant la liste _joueurs_ dans le fichier [_main.py_](main.py). Il faut également indiquer le nombre de parties à simuler dans la variable _nb\_parties_. Enfin, pour lancer la simulation, il faut exécuter le fichier [_main.py_](main.py).

## Présentation du programme

Le but de ce projet est de réaliser une IA en python sur le jeu _Diamants_. L'objectif final est de se faire affronter plusieurs IA pour le comparer.
Le moteur de jeu fourni à l'avance se trouve dans le fichier [_moteur\_diamant.py_](moteur_diamant.py). Il permet de simuler une partie et ne pouvait être modifié pendant le projet.

Notre IA est l'[_IA\_SAE.py_](IA/IA_SAE.py). Elle est composée de plusieurs fonctions qui permettent de choisir une action à effectuer (rentrer (_R_) ou rester (_X_)).

Notre fichier [_main.py_](main.py) permet de simuler une partie entre plusieurs IA. Au bout d'un certain nombre de parties, il affiche le pourcentage de victoires de chaque IA ainsi que leur position moyenne. Ce fichier peut être modifié pour afficher plus d'informations.

---

Projet réalisé dans le cadre de la SAÉ 1.02 du premier semestre de BUT informatique à l'IUT de Vélizy

Janvier 2023
