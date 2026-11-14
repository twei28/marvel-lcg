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
#  - « aspect or basic WEAPON » : les 5 aspects classiques Aggression / Justice / Leadership / Protection / 'Pool (SANS Determination : decision du 23/10/2026) / Basic, trait WEAPON ; JAMAIS une carte de
#    classe Hero (cartes de heros) ni Campaign.
#  - « search your deck, discard pile, AND collection » : UNE seule recherche sur les trois zones (decision du 23/10/2026) : une liste unique, les
#    armes du deck et de la defausse d'abord, puis la collection ; la carte va en MAIN.
#  - `CardFinder(trait=...)` seul est refuse (il exige un `card_type`) : le trait WEAPON est teste dans `check_face_fn`.
#  - Pas de limite par round imprimee (contrairement a pu141) : seul le nombre de compteurs borne l'usage.

CLASSES_PERMISES = ('Aggression', 'Justice', 'Leadership', 'Protection', "'Pool", 'Basic')


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
        # UNE seule recherche sur les trois zones (decision du 23/10/2026) : le joueur choisit UNE arme dans la liste « mon deck, ma defausse,
        # puis le reste de la collection » (les exemplaires physiques d'abord) ; si l'arme choisie est dans le deck ou la defausse c'est CETTE carte
        # qui rejoint la main (le deck est melange s'il a ete fouille), sinon un exemplaire est tire de la collection.
        from cards.database import CardsDB
        from game.card.factory import CardFactory
        physiques: List['CardFace'] = []
        for zone in (joueur.player_deck, joueur.discard_pile):
            physiques += [f for f in zone.Get() if f.HasTrait("WEAPON") and _arme_permise(f.paper.desc.get("Class"))]
        ids = Types.RemoveDuplicates([f.paper.card_id for f in physiques])
        ids += [x for x in CardsDB.GetPapers(trait="WEAPON", check_fn=lambda paper: _arme_permise(paper.desc.get("Class"))) if x not in ids]
        if not ids:
            return
        choisi = joueur.AskChoosePaper(ids)
        face = next((f for f in physiques if f.paper.card_id == choisi), None)
        if face is None:
            joueur.GainCard([CardFactory.GenerateCard(choisi, joueur.discard_pile, effect.world).face], effect)
            return
        du_deck = face in joueur.player_deck.Get()
        joueur.GainCard([face], effect)
        if du_deck:
            joueur.player_deck.Shuffle(effect)

    return [
        AbilityFactory.AfterGameSetup(mise_en_place),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, action)
        .SetCostFunc(CostFunc.Counter("This", 1, 'counter'))
        .SetCostFunc(CostFunc.PlaceThreatOn(3, card_type=MainScheme))
        .AnyPlayerCanDoThis(),
    ]
