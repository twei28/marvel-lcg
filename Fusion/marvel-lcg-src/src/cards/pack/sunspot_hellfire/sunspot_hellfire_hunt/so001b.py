from . import *

# * Roberto Da Costa (face ALTER-EGO) — MUTANT. PV 10, REC 3, main 6.
# Setup: Place 5 solar counters here.
# Energy Absorption — Action: Discard up to 3 cards from your hand. For each resource icon discarded from these cards,
#   place 1 solar counter here.
#
# CARTES DE REFERENCE
#  - `sw001b` Julia Carpenter : le Setup d'une IDENTITE = `AbilityFactory.WhenCardSetup("This", op)` (tourne apres la
#    construction du deck) ; une Action nommee qui remplit le stock.
#  - `01023` Legal Practice : `CostFunc.Discard("YourHandCards", range=(1, N))` puis `effect.cost_func.Get(CostFunc.Discard)
#    .return_discarded_cards` pour savoir ce qui a ete defausse.
#  - `FacesCounter.GetPrintedResources(faces).val` : le nombre d'ICONES imprimees (YY = 2, wild = 1).
#
# TEXTE CONTRE CODE
#  ⚠ « UP TO 3 cards » : au moins une carte (defausser 0 carte ne fait rien : `range=(1, 3)`, comme 01023 « up to 5 »).
#  ⚠ « resource ICON discarded » : les icones IMPRIMEES des cartes defaussees, toutes couleurs, wild compris.
#  ⚠ « here » = l'identite (le stock survit au changement de forme, helpers du set).


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        PoserSolaires(effect.GetInitiator(), 5, effect)

    def energy_absorption(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        defaussees = effect.cost_func.Get(CostFunc.Discard).return_discarded_cards
        PoserSolaires(joueur, FacesCounter.GetPrintedResources(defaussees).val, effect)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            energy_absorption,
        ).SetName("Energy Absorption")
        .SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 3))),
    ]
