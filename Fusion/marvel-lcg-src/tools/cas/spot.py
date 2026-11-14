# Cas test_capacites du pack THE SPOT (set fan-made, prefixe `sp`) : noms prefixes « [sp] » puis le card_id.
# Cree le 26/10/2026 pour sp018 Oddballs (`player.AskDiscardHandCards` n'existe nulle part dans le moteur : AttributeError des que la
# defausse de la main devait avoir lieu, releve par tools/verifier_api_cartes.py ; aucun cas ne couvrait ce pack).
#
# Rappels de montage :
#  - le vilain The Spot (stade I, sp002) porte Threat Level 1 (IMPAIR) : il compte toujours parmi les cartes « a Threat Level impair »
#    (sa menace n'est pas mesuree : elle vaut deja 2 jetons apres la mise en place) ;
#    Puma sp008 (TL 3) est impair, Rocket Racer sp007 (TL 2) pair, Chameleon sp010 (TL 5) impair ;
#  - 01083 Mockingbird (cout imprime 3, IMPAIR) et 01089 Genius (ressource, sans cout imprime : 0, PAIR) servent de main ;
#  - `main_exclusive` DEFAUSSE la main de depart apres la mise en place et la remplace par les cartes donnees.
SC = "the_spot"
HEROS = "spider_man"
VILAIN = "sp002"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    mise = SANS_BOOST + list(mise)
    cas = {"nom": "[sp] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", HEROS), "mise_en_place": mise, "declencher": declencher, "verifier": "etat_attendu", "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    _c("sp018 Oddballs : 2 cartes a Threat Level impair (le vilain TL1 et Puma TL3) -> 1 menace chacune, puis defausse de la carte a cout imprime impair",
       "« Place 1 threat on each Spot card with an odd Threat Level number. If 2 or fewer threat was placed this way, discard a card in your "
       "hand with an odd printed cost. » : 2 menaces posees (<= 2) donc Mockingbird (cout 3) est defausse, Genius (cout 0, pair) reste",
       ["Puzzle.PutIntoPlay('sp008')"], ["Puzzle.Reveal('sp018')"],
       {"jetons": [["sp008", "threat", 1]], "taille_main": 1, "en_main": ["01089"]},
       main_exclusive=["01083", "01089"], accepter_choix=True),
    _c("sp018 Oddballs : TEMOIN, 3 cartes a Threat Level impair (vilain TL1, Puma TL3, Chameleon TL5) -> 3 menaces, AUCUNE defausse",
       "« If 2 or fewer threat was placed this way » : 3 menaces posees, la defausse n'a pas lieu, la main reste a 2 cartes",
       ["Puzzle.PutIntoPlay('sp008')", "Puzzle.PutIntoPlay('sp010')"], ["Puzzle.Reveal('sp018')"],
       {"jetons": [["sp008", "threat", 1], ["sp010", "threat", 1]], "taille_main": 2},
       main_exclusive=["01083", "01089"], accepter_choix=True),
    _c("sp018 Oddballs : CONTRE-CAS, 2 menaces posees mais AUCUNE carte a cout imprime impair en main -> rien n'est defausse",
       "« discard a card in your hand with an odd printed cost » : sans carte a cout impair la defausse n'a pas lieu (Genius seule, cout 0)",
       ["Puzzle.PutIntoPlay('sp008')"], ["Puzzle.Reveal('sp018')"],
       {"jetons": [["sp008", "threat", 1]], "taille_main": 1, "en_main": ["01089"]},
       main_exclusive=["01089"], accepter_choix=True),
]
