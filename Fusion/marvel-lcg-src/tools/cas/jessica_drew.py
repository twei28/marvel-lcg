# Cas test_capacites de 04031b Jessica Drew (alter ego de Spider-Woman), rapport #162 du 22/11/2026 : « Action : regardez la
# carte du dessus de N'IMPORTE QUEL deck » doit faire CHOISIR LE DECK PAR SON NOM, puis regarder seulement la carte de ce
# deck. L'ancien script posait une cible = la carte du dessus de chaque deck, montrées face visible AVANT le choix.
# Montage : deck `spider_woman`, vilain Rhino 01094 ; Jessica Drew démarre en alter ego (l'Action est jouable directement).
# `preferer_option` : première option dont le libellé contient un des fragments. Sans la correction, le choix est une CARTE
# (aucune option nommée « Encounter deck ») : `etat_attendu` échoue faute de pouvoir poser la réponse voulue.


def _c(nom, pourquoi, declencher, attendu, **cle):
    cas = {'nom': nom, 'pourquoi': pourquoi, 'scenario': 'rhino', 'heros': 'spider_woman',
           'mise_en_place': [], 'declencher': list(declencher), 'verifier': 'etat_attendu', 'attendu': attendu}
    cas.update(cle)
    return cas


CAS = [
    _c("04031b Jessica Drew — l'Action propose « Encounter deck » PAR SON NOM, sans aucune carte cible (rien de montré avant le choix)",
       "rouge avant le correctif : le choix était une carte face visible, aucune option « Encounter_deck » n'existait",
       ["Puzzle.Action('04031b', 'Action')"], {'option': 'Encounter deck', 'contient': [], 'exclut': []},
       verifier='cibles_legales_proposees', preferer_option=['Encounter deck']),
    _c("04031b Jessica Drew — « Player deck » est proposé lui aussi par son nom (Player_deck_(Jessica_Drew))",
       "même question : les deux decks, deux boutons nommés",
       ["Puzzle.Action('04031b', 'Action')"], {'option': 'Player deck', 'contient': [], 'exclut': []},
       verifier='cibles_legales_proposees', preferer_option=['Player deck']),
]
