# Cas test_capacites des RELECTURES LIGNE A LIGNE du 26/10/2026 (balayage « search puis effet », docs/rapports/2026-10-26-balayage-search-then.md) :
# noms prefixes « [rs] » puis le card_id (substituer_pack.py / le filtre de test_capacites s'y reperent).
#
# Rappels de montage :
#  - `Puzzle.SendGameBeginSetup()` envoie `WhenGameBeginSetup` (capacites de type Setup / « When the game begins »), parti une seule fois AVANT le montage d'un cas ;
#  - `Search.Collection` fait choisir un TITRE au joueur (`AskChoosePaper`) ; le pilote du harnais prend toujours la PREMIERE option legale.
SC = "rhino"
HEROS = "spider_man"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    mise = SANS_BOOST + list(mise)
    cas = {"nom": "[rs] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", HEROS), "mise_en_place": mise, "declencher": declencher, "verifier": "etat_attendu", "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    _c("dt075 Multiverse Shenanigans : « choose any 3 DIFFERENT non-determination aspect cards » : trois cartes posees dessous, de trois titres DIFFERENTS",
       "« When the game begins, choose any 3 different non-determination aspect cards from your collection and set them aside. » Le pilote prend "
       "toujours la premiere option legale : si le script n'exclut pas les titres deja choisis, il pose trois fois la MEME carte",
       ["Puzzle.PutIntoPlay('dt075', under_control=True)"], ["Puzzle.SendGameBeginSetup()"],
       {"taille_pose_sous": [["dt075", 3]], "pose_sous_titres_distincts": [["dt075", 3]]}),
    _c("dt075 Multiverse Shenanigans : l'Action (epuiser + se distribuer une carte rencontre face cachee) cherche dans les cartes mises de cote et ajoute UNE a la main",
       "« Exhaust this card and deal yourself a facedown encounter card -> search the set-aside area for 1 of these chosen cards and add it to your hand. » "
       "Trois cartes de cote, une passe en main : il en reste DEUX dessous, la main gagne une carte, dt075 est epuisee",
       ["Puzzle.CreateEncounterDeck('01098', '01098', '01098')", "Puzzle.PutIntoPlay('dt075', under_control=True)"],
       ["Puzzle.SendGameBeginSetup()", "Puzzle.Action('dt075')"],
       {"taille_pose_sous": [["dt075", 2]], "pose_sous_titres_distincts": [["dt075", 2]], "exhausted": ["dt075"]}, accepter_choix=True),
    # --------------------------------------------------------------------------------------------- 56096b / 56072 : cartes Civil War (relues, jamais testees)
    # ⚠ Aucun cas du depot ne monte le mode COMPETITIF (deux equipes). Ces cas jouent la MEME carte en mode COOPERATIF : « the enemy team » y vaut le
    # premier joueur (worlds.py GetEnemyTeam) ; ils ne prouvent donc pas le partage entre deux tables.
    _c("56096b S.H.I.E.L.D. Recruits (When Revealed, coop, 1 joueur) : cherche 1 sbire dans le deck de rencontre et le DONNE au joueur face cachee ; revele, il entre en jeu",
       "« searches the encounter deck for 1[per_hero] minions and deals one to each player on your team as a facedown encounter card » : "
       "1 joueur -> 1 sbire (01101 Hydra Mercenary) quitte le deck, est donne face cachee, puis entre en jeu a la revelation des cartes donnees",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01098', '01101', '01098')"],
       ["Puzzle.Reveal('56096b')", "Puzzle.RevealDealtCards()"],
       {"en_jeu": ["01101"]}, accepter_choix=True),
    _c("56096b S.H.I.E.L.D. Recruits : CONTRE-CAS, aucun sbire dans le deck de rencontre -> rien n'est donne, rien ne plante",
       "la recherche ne trouve rien : le joueur ne recoit aucune carte (pas de « Then » imprime : la manigance se revele quand meme)",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01098', '01098')"],
       ["Puzzle.Reveal('56096b')", "Puzzle.RevealDealtCards()"],
       {"hors_jeu": ["01101"], "en_jeu": ["56096b"]}, accepter_choix=True),
    _c("56072 Stark Tower (When Defeated, coop) : cherche un attachement Iron Man dans le deck de rencontre ET la defausse et le REVELE (il s'attache a Iron Man)",
       "« The enemy team searches the encounter deck and discard pile for an Iron Man attachment and your team reveals it » : 56065 Powered Gauntlets "
       "est dans la DEFAUSSE de rencontre, pas dans le deck ; il doit finir attache au heros Iron Man",
       ["Puzzle.ChangeToFace('01029b', '01029a')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01098', '01098')",
        "Puzzle.CreateEncounterDiscardPile('56065')",
        "Puzzle.Reveal('56072')", "Puzzle.SetThreat('56072', 1)"],
       ["Puzzle.Thwart('01029a')"],
       {"attaches": [["01029a", "56065"]]}, heros="iron_man", cibles=["56072"], accepter_choix=True),
]
