##############################################################################
# votre IA : à vous de coder
# Rappel : ne pas changer les paramètres des méthodes
# vous pouvez ajouter librement méthodes, fonctions, champs, ...
##############################################################################

import random

class IA_Diamant:
    def __init__(self, match : str):
        """
            Génère l'objet de la classe IA_Diamant

            Args:
                match (str): decriptif de la partie
        """

        self.match = match

        # Ces listes retiennent les cartes qui son tirées à chaque tour
        # Elles sont réinitialisées à chaque manche
        self.histo_rubis = []
        self.histo_relique = []
        self.histo_pieges = []

        # Ici, on stock les pièges qui ont été retirés de la partie
        self.pieges_retires = []

        # Détecte toutes les informations sur la partie à partir de match
        self.nb_manches, self.nb_joueurs, nom_joueurs, self.numero_joueur = self.match.split('|')
        self.nom_joueur = nom_joueurs.split(',')[int(self.numero_joueur)]
        self.numero_joueur = int(self.numero_joueur)
        self.reste_rubis = 0
        self.manche_actu = 1
        self.nb_joueurs = int(self.nb_joueurs)
        self.nom_joueurs = nom_joueurs.split(',')

        # État des joueurs durant une manche (True : le joueur joue encore, False : il est sorti)
        self.en_jeu = [True] * self.nb_joueurs
        
        # Différentes valeurs que peuvent prendre les reliques
        self.valeurs_reliques = [5, 5, 5, 10, 10]

        self.temp_scores = [0] * self.nb_joueurs
        self.scores = [0] * self.nb_joueurs
        self.reliques_gagnees = 0
        self.nb_reliques_en_jeu = 0

        self.rentre = False
        
        # print("IA_GODINEAU_CHIRON reçoit match = '" + match + "'")

    def tri_carte(self, tour):
        '''
            Détecte la dernière carte tirée et l'enregistre dans le tableau adéquat

            Args:
                tour (str) : descriptif du dernier tour de jeu
        '''

        # La carte est le dernier élément de tour
        carte = tour.split('|')[-1]

        # Répartie les cartes aux bons endroits
        if carte == 'R' :
            self.histo_relique.append(carte)
            self.nb_reliques_en_jeu += 1
        elif carte[0] == 'P' :
            self.histo_pieges.append(carte)
        else :
            self.histo_rubis.append(int(carte))


    def action(self, tour : str) -> str:
        """Appelé à chaque décision du joueur IA

        Args:
            tour (str): descriptif du dernier tour de jeu

        Returns:
            str: 'X' ou 'R'
        """

        # print("    IA_GODINEAU_CHIRON reçoit tour = '" + tour + "'")
        
        # Si toutes les ia sont rentrées au tour d'AVANT, on rentre
        if self.en_jeu.count(True) == 1:
            self.rentre = True

        if tour == '' :
            return 'X'

        # Enregistre les informations sur la partie
        self.calcul_rubis(tour)
        
        # Enregistre les cartes au fur et à mesure de la partie
        self.tri_carte(tour)

        # Crée une liste de choix à chaque tour qui sera ensuite modifiée
        choice_list = ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'R', 'R', 'R'] # 3 chances sur 14 de sortir si aucune danger n'est découvert

        # Quand un piège est détecté, les chances de rentrer grandissent : On passe de 3 chances sur 14 à 7 chances sur 18 puis 11 sur 22 et ainsi de suite
        for i in range(len(self.histo_pieges)):
            choice_list.append('R')
            choice_list.append('R')
            choice_list.append('R')
            choice_list.append('R')

        # Si aucun piege, aucun rubis ou aucune relique n'est tiré, l'ia reste dans le jeu
        if (len(self.histo_pieges) == 0) or (len(self.histo_rubis) == 0) or (len(self.histo_relique) == 0):
            choice_list = ['X']

        # L'ia rentre si : il n'y a plus que l'ia ou l'ia et un autre joueur et qu'une relique valant 10 rubis est découverte ou si au moins 2 reliques sont découvertes
        if (((len(self.histo_relique) != 0) and (self.valeurs_reliques[self.reliques_gagnees] > 5)) or (len(self.histo_relique)>1)) and self.en_jeu.count(True) < 3:
            choice_list = ['R']

        # L'ia rentre si elle a au moins 10 rubis
        if (self.temp_scores[self.numero_joueur] > 9):
            choice_list = ['R']

        # Si l'ia a un écart conséquent, elle ne prend pas de risques
        if self.gagne():
            choice_list = ['R']

        # Si toutes les ia sont rentrées au tour d'avant et qu'elle n'a pas un grand écart, elle ne prend pas de risques
        if self.rentre and not self.gagne() :
            choice_list = ['R']

        # Le hasard décide de la décision de l'ia
        choice = random.choice(choice_list)

        return choice


    def gagne(self):
        '''
            Vérifie si l'ia est première et si elle est seule en jeu ou si son écart est important

            Args:
                self
            
            Returns:
                Boolean
        '''

        # Vérifie si l'ia est première et seule dans le jeu dans la dernière manche de la partie => elle rentre le cas échéant
        if self.manche_actu == int(self.nb_manches):
            if ((self.temp_scores[self.numero_joueur] + self.scores[self.numero_joueur]) == (max(self.scores) + self.temp_scores[self.scores.index(max(self.scores))])) and (self.en_jeu.count(True) == 1) :
                return True

        # Calcule les sommes des rubis de tous les joueurs (coffres + manche actuelle)
        temp_class = []
        for e in self.scores :
            temp_class.append(e)
        for i in range(len(self.scores)):
            if self.en_jeu[i]:
                temp_class[i] += self.temp_scores[i]

        # Si l'ia est première : vérifie qu'elle possède un certain écart avec le deuxième
        if (self.temp_scores[self.numero_joueur] + self.scores[self.numero_joueur]) == max(temp_class):
            temp_best = max(temp_class)
            temp_class.remove(temp_best)
            # Afin d'avoir plus de sécurité, l'écart est variable
            # L'écart grandit au fur et à mesure des manches
            if (temp_best - max(temp_class)) > (5*self.manche_actu+5) :
                return True
        return False


    def calcul_rubis(self, tour):
        '''
            Enregistre toutes les informations liées à la manche

            Args:
                tour (str) : descriptif du dernier tour de jeu
        '''

        # Dictionnaire comprenant les décisions des joueurs (vide pout l'instant)
        decisions = {'X':[], 'R':[], 'N':[]}
        choix = [None]*self.nb_joueurs

        # Détecte dans tour les décisions de chaque joueur et les met dans le dictionnaire
        for i in range(self.nb_joueurs):
            choix[i] = ((tour.split('|')[0]).split(','))[i]
            if not self.en_jeu[i]:
                choix[i] = 'N'
            decisions[choix[i]].append(i)

        # Calcul des rubis pour les joueurs qui sortent
        if decisions['R']:
            # Calcul du nombre de rubis gagné pour les joueurs quittant la grotte et recalcule le nombre de rubis restant sur le plateau
            gain = self.reste_rubis // len(decisions['R'])
            self.reste_rubis = self.reste_rubis % len(decisions['R']) 
            # Ajoute les rubis gagnés dans la manche dans les coffres des joueurs qui partent
            for i in decisions['R']:
                self.en_jeu[i] = False
                self.temp_scores[i] += gain
                self.scores[i] += self.temp_scores[i]

            # Calcul du nombre de rubis pour les reliques
            if len(decisions['R'])==1 and ('R' in self.histo_relique) :
                # Calcule les valeurs pour chaque relique sur le plateau et les attribue au joueur partant s'il est seul
                for i in range(len(self.histo_relique)):
                    self.scores[decisions['R'][0]] += self.valeurs_reliques[self.reliques_gagnees]
                    self.reliques_gagnees += 1
                # Supprime les reliques retirées du plateau
                self.histo_relique = []
                self.nb_reliques_en_jeu = 0
        
        # On ne prend plus en compte les joueurs qui sont sortis de la grotte

        # Calcul du nombre de rubis attribué à chaque joueur qui reste dans la grotte
        if (tour.split('|')[-1] != 'R') and (tour.split('|')[-1][0] != 'P') and (len(decisions['X'])!=0) :
            # Recalcule le nombre de gemmes restants dans la grotte
            self.reste_rubis += int(tour.split('|')[-1]) % len(decisions['X'])
            for i in decisions['X']:
                if self.en_jeu[i]:
                    self.temp_scores[i] += int(tour.split('|')[-1]) // len(decisions['X'])


    def fin_de_manche(self, raison : str, dernier_tour : str) -> None:
        """Appelé à chaque fin de manche

        Args:
            raison (str): 'R' si tout le monde est un piège ou "P1","P2",... si un piège a été déclenché
            dernier_tour (str): descriptif du dernier tour de la manche
        """
        # Enregistre les informations de la manche dans le dernier tour
        self.calcul_rubis(dernier_tour)
        if dernier_tour.split('|')[-1][0] == 'P':
            self.pieges_retires.append(dernier_tour.split('|')[-1])

        # Remet toutes les informations à 0 avant de lancer une nouvelle manche
        self.temp_scores = [0] * self.nb_joueurs
        self.en_jeu = [True] * self.nb_joueurs
        self.histo_relique = []
        self.histo_pieges = []
        self.histo_rubis = []
        self.reste_rubis = 0
        self.rentre = False
        self.manche_actu += 1

        # print("  IA_GODINEAU_CHIRON reçoit en fin de manche raison = '" + raison + "' et dernier_tour = '" + dernier_tour + "'" )


    def game_over(self, scores : str) -> None:
        """Appelé à la fin du jeu ; sert à ce que vous voulez

        Args:
            scores (str): descriptif des scores de fin de jeu
        """
        # print("IA_GODINEAU_CHIRON reçoit en fin de jeu scores = '" + scores +"'")
