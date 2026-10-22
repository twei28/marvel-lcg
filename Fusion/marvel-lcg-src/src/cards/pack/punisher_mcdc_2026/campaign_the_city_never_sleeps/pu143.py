from . import *

# Punisher's Ordnance Cache — AMELIORATION de campagne (recompense du combat 2, p266). Permanent.
# Setup : Place 1 counter here, plus 1 more for each player who did not play the last game together.
# Action : Remove 1 counter from here and place 3 threat on the main scheme -> search your deck, discard pile, and collection for an aspect or
#   basic WEAPON card and add it to your hand. Any player may trigger this ability.
#
# Cartes de reference : pu141 (le meme Setup et le meme « any player »), hood/24007 (deux couts chaines : `SetCostFunc(...).SetCostFunc(
# CostFunc.PlaceThreatOn(n, card_type=MainScheme))`), an001b (`Search.PlayerCard` deck + defausse), dz031 / bc004 (`Search.Collection` + main).
# ⚠ Mots-pieges :
#  - « Remove 1 counter AND place 3 threat -> » : DEUX couts, payes avant la recherche ; sans compteur (ou sans complot principal) l'Action n'est
#    pas offerte ; « on the main scheme » : 3 menaces fixes (pas par joueur).
#  - « aspect or basic WEAPON » : classe Aggression / Justice / Leadership / Protection / 'Pool / Determination (sixieme aspect officiel) / Basic, trait WEAPON ; JAMAIS une carte de
#    classe Hero (cartes de heros) ni Campaign.
#  - « search your deck, discard pile, AND collection » : une seule carte, prise dans l'une des trois zones. Le deck et la defausse sont proposes
#    d'abord (facultatif) ; si le joueur n'y prend rien, la collection (`Search.Collection`, carte fabriquee) ; la carte va en MAIN.
#  - `CardFinder(trait=...)` seul est refuse (il exige un `card_type`) : le trait WEAPON est teste dans `check_face_fn`.
#  - Pas de limite par round imprimee (contrairement a pu141) : seul le nombre de compteurs borne l'usage.

CLASSES_PERMISES = ('Aggression', 'Justice', 'Leadership', 'Protection', "'Pool", 'Determination', 'Basic')


def _arme_permise(classe: 'str|None') -> bool:
    return classe in CLASSES_PERMISES


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        Unused(message)
        Faces.PlaceCountersOn([effect.this], JetonsDeDepart(effect), 'counter', effect)

    def action(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        face = Search.PlayerCard(
            effect, joueur,
            include_player_deck=True,
            include_discard_pile=True,
            may=True,
            finder=CardFinder(check_face_fn=lambda f: f.HasTrait("WEAPON") and _arme_permise(f.paper.desc.get("Class"))),
        )
        if face is None:
            face = Search.Collection(
                effect, joueur,
                trait="WEAPON",
                check_fn=lambda paper: _arme_permise(paper.desc.get("Class")),
            )
        if face is not None:
            joueur.GainCard([face], effect)

    return [
        AbilityFactory.AfterGameSetup(mise_en_place),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, action)
        .SetCostFunc(CostFunc.Counter("This", 1, 'counter'))
        .SetCostFunc(CostFunc.PlaceThreatOn(3, card_type=MainScheme))
        .AnyPlayerCanDoThis(),
    ]
