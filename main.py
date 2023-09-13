##############################################################################
# main                                                                       #
##############################################################################

# Dans ce fichier que vous pouvez compléter vous lancez vos expérimentations

from moteur_diamant import partie_diamant

if __name__ == '__main__':
    nb_parties = 10000
    joueurs = ['IA80', 'IA85', 'IA90', 'IA_sae']
    nb_win = {joueur : 0 for joueur in joueurs}
    pos = {joueur : 0 for joueur in joueurs}
    for i in range(nb_parties):
        scores = partie_diamant(5, joueurs)
        gagnant = scores.index(max(scores))
        nb_win[joueurs[gagnant]] += 1
        id = list(range(1,len(joueurs)+1))
        scores = [x for _,x in sorted(zip(scores, joueurs))]
        scores.reverse()
        for i in range(len(scores)-1):
            if scores[i+1] == scores[i]:
                id[i] += 1
        for i in range(len(joueurs)):
            pos[scores[i]] += id[i]

    for i in range(len(joueurs)):
        dis_score = str(round(((nb_win[joueurs[i]]/(nb_parties))*100),2)) + '%, position moyenne : ' + str(round((pos[joueurs[i]]/nb_parties),2))
        print(joueurs[i], ':',dis_score)
    print(nb_parties, 'parties')
    print(nb_win)