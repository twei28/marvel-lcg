# Cas test_capacites de 17020 Cosmo (allié officiel, The Galaxy's Most Wanted), réécrit le 18/11/2026 après les rapports
# nicodede62 #148/#149 : le type de carte doit être NOMMÉ AVANT de choisir le paquet, et le paquet se choisit par son nom
# (l'ancien script le faisait choisir par une cible = la carte du dessus montrée face visible, puis nommait le type).
#
# Montage : deck `mantis` (Cosmo y figure), vilain Rhino 01094. Le deck rencontre est remplacé par des Assault 01187
# (TRAITRISE) : on sait donc ce qui sera défaussé du dessus. Le dessus du deck de Mantis n'est jamais une traîtrise.
# `preferer_option` : la première option dont le libellé contient un des fragments est prise, à CHAQUE question.
COSMO = "Puzzle.PutIntoPlay('17020', under_control=True)"
RENCONTRE_TRAITRISES = ["Puzzle.EmptyEncounterDeck()",
                        "Puzzle.CreateEncounterDeck('01187', '01187', '01187', '01187', '01187', '01187')"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {'nom': nom, 'pourquoi': pourquoi, 'scenario': cle.pop('scenario', 'rhino'), 'heros': cle.pop('heros', 'mantis'),
           'mise_en_place': list(mise), 'declencher': list(declencher), 'verifier': cle.pop('verifier', 'etat_attendu'),
           'attendu': attendu}
    cas.update(cle)
    return cas


CAS = [
    _c("17020 Cosmo — type nommé (Traîtrise) PUIS paquet choisi par son nom (deck rencontre) : la traîtrise défaussée "
       "correspond, Cosmo ne prend PAS de dégât consécutif",
       "rouge avec l'ancien script : la cible prise par défaut était le dessus du deck JOUEUR (pas une traîtrise)",
       [COSMO] + RENCONTRE_TRAITRISES, ["Puzzle.Attack('17020')"],
       {'degats': [['17020', 0], ['01094', 1]]},
       preferer_option=['Treachery', 'Encounter deck']),
    _c("17020 Cosmo — type nommé (Sbire) qui NE correspond PAS à la traîtrise défaussée : 1 dégât consécutif",
       "même position, mauvais type nommé : la conséquence s'applique",
       [COSMO] + RENCONTRE_TRAITRISES, ["Puzzle.Attack('17020')"],
       {'degats': [['17020', 1], ['01094', 1]]},
       preferer_option=['Minion', 'Encounter deck']),
    _c("17020 Cosmo — deck JOUEUR choisi : sa carte du dessus n'est pas une traîtrise, 1 dégât consécutif",
       "« a player deck » : le deck de Mantis est proposé par son nom (Player deck (Mantis))",
       [COSMO] + RENCONTRE_TRAITRISES, ["Puzzle.Attack('17020')"],
       {'degats': [['17020', 1], ['01094', 1]]},
       preferer_option=['Treachery', 'Player deck']),
]
