# Cas test_capacites du CORRECTIF MOTEUR du 14/11/2026 (src/game/ability/factory/boost.py, `check_cette_carte_est_le_boost`),
# noms prefixes « [boost_en_jeu] ». Une capacite de type BOOST posee par `WhenBoostCardTurnedFaceUp` ne vaut que lorsque la
# carte EST la carte de boost retournee : un permanent EN JEU ne doit rien faire quand une AUTRE carte de boost est retournee.
# Cartes concernees : 62029 Cottonmouth, 62030 Venomous Whispers, 62032 Asp (set nemesis de Luke Cage), 60062 Master
# Manipulator (deja couvert en boost par son cas [fne4]), 63029 Aka (tools/cas/elektra_nemesis.py).
# Les cas « EN JEU » sont ROUGES sans le correctif ; les cas « en boost » prouvent que la capacite marche toujours.
HEROS = "Puzzle.ChangeToFace('62001b', '62001a')"
MISE = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105')",
        "Puzzle.RemoveNemesisAside()", HEROS]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[boost_en_jeu] " + nom, "pourquoi": pourquoi, "scenario": "rhino", "heros": "luke_cage",
           "mise_en_place": MISE + list(mise), "declencher": declencher,
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu, "passer_sur_option": "Defense"}
    cas.update(cle)
    return cas


CAS = [
    _c("62029 Cottonmouth EN JEU : Rhino s'active avec une autre carte de boost (01105) -> Cottonmouth reste en jeu",
       "avant le correctif il se distribuait lui-meme au joueur et quittait le jeu",
       ["Puzzle.PutIntoPlay('62029')"], ["Puzzle.Boost('01105')"], {"en_jeu": ["62029"]}),
    _c("62029 Cottonmouth en boost : il est distribue face cachee au joueur Luke Cage",
       "la capacite Boost marche toujours quand la carte EST la carte de boost",
       [], ["Puzzle.Boost('62029')"], {"distribuees": 1}, verifier="ares_cartes_rencontre_distribuees"),
    _c("62032 Asp EN JEU : Rhino s'active avec une autre carte de boost (01105) -> Luke Cage n'est pas sonne",
       "avant le correctif chaque carte de boost retournee sonnait le joueur",
       ["Puzzle.PutIntoPlay('62032')"], ["Puzzle.Boost('01105')"], {"en_jeu": ["62032"], "statuts_absents": [["62001a", "Stunned"]]}),
    _c("62032 Asp en boost : Luke Cage est sonne",
       "la capacite Boost marche toujours quand la carte EST la carte de boost",
       [], ["Puzzle.Boost('62032')"], {"statuts": [["62001a", "Stunned"]]}),
    _c("62030 Venomous Whispers EN JEU : Rhino s'active avec une autre carte de boost (01105) -> Luke Cage n'est pas desoriente",
       "avant le correctif chaque carte de boost retournee desorientait le joueur",
       ["Puzzle.PutIntoPlay('62030')"], ["Puzzle.Boost('01105')"], {"en_jeu": ["62030"], "statuts_absents": [["62001a", "Confused"]]}),
    _c("62030 Venomous Whispers en boost : Luke Cage est desoriente",
       "la capacite Boost marche toujours quand la carte EST la carte de boost",
       [], ["Puzzle.Boost('62030')"], {"statuts": [["62001a", "Confused"]]}),
]
