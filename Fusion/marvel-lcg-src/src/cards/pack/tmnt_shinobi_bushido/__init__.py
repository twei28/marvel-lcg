from cards.pack import *

# Helpers PARTAGES des 20 cartes Bushido (Inkwire, TMNT Shinobi, prefixe `sb`). Un helper vit dans le `__init__.py` du dossier
# qui porte les scripts (lecon hk005 : un helper defini ailleurs leve un NameError avale par le moteur).
#
# Mots-cles (fiches lues AVANT le code) : samurai counter / OATH (mots-cles/samurai-counter.md) ; Uses (mots-cles/uses.md).


def OathsSousControle(joueur: 'Player|None', *, avec_compteurs: bool = False) -> 'List[CardFace]':
    """« les ameliorations [[OATH]] que vous controlez » (identite et allies compris), filtrees ou non sur
    « porte au moins un compteur samurai »."""
    if joueur is None:
        return []
    faces = list(joueur.GetControlUpgrade(CardFinder(trait="OATH")))  # type: ignore
    if avec_compteurs:
        faces = [f for f in faces if f.GetCounters('samurai') > 0]
    return faces


def PlacerUnCompteurSamurai(effect: 'Effect', joueur: 'Player|None', *, optionnel: bool = False) -> bool:
    """« place 1 samurai counter on an OATH upgrade you control » : le joueur CHOISIT l'amelioration ; sans amelioration OATH
    sous son controle l'effet ne fait rien. `optionnel` : « you may place » (le joueur peut refuser)."""
    candidats = OathsSousControle(joueur)
    if joueur is None or not candidats:
        return False
    place = [False]

    def action(cibles: 'Sequence[CardFace]') -> None:
        if cibles and Faces.PlaceCountersOn(list(cibles)[:1], 1, 'samurai', effect) is not None:
            place[0] = True

    choix = AbilityFactory.ForChoiceAbility("Place 1 samurai counter on an OATH upgrade you control", action).SetTarget(candidats)
    if optionnel:
        joueur.MayChooseOneAbility(effect, choix)
    else:
        joueur.ChooseAbilities(effect, choix)
    return place[0]
