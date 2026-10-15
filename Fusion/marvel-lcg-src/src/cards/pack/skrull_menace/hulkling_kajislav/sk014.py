from . import *

# * Nega Rings — amelioration signature (16/16). ITEM. KREE. Cout 2 [energy].
# Hero Action: Exhaust Nega Rings and spend a [energy] resource → choose a card
#   in your hand and swap that card with a card of your choice in your discard
#   pile.
#
# Cartes de reference :
#  - **`40037b`** * Neena Thurman : « Choose a card in your hand. Swap that
#    card with the top card of your discard pile. » Meme echange, mais avec
#    une carte AU CHOIX de la defausse ici, pas celle du dessus : la carte
#    de main part sur la defausse (`MoveAllToDeck(..., discard_pile, "Top")`,
#    modele 16033 Salvage), la carte choisie revient en main (`GainCard`).
#  - `as002b` pour `SetCost(Cost("Y"))` sur une capacite deja en jeu (« spend a
#    [energy] resource »), et `Exhaust("This")`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **swap** » : ce n'est PAS une defausse (aucune Response « after you
#    discard » ne doit partir) : on DEPLACE la carte sur la defausse.
#  - « a card **of your choice** in your discard pile » : n'importe laquelle,
#    pas le dessus. Defausse vide : rien a echanger, l'action n'est pas
#    proposee (condition), sinon le cout serait paye pour rien.
#  - « spend a [energy] resource » : `Cost("Y")`, un joker convient.
#  - « **Hero** Action ».


def GetAbilities() -> Sequence['Ability']:

    def defausse_non_vide(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        joueur = effect.GetInitiator()
        return joueur is not None and len(list(joueur.discard_pile.Get())) > 0

    def anneaux(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        joueur = effect.GetInitiator()
        de_la_main = list(effect.targets)
        defausse = list(joueur.discard_pile.Get())
        if not de_la_main or not defausse:
            return
        recuperee = joueur.AskChooseFace(
            defausse, effect,
            prompt="Choose a card in your discard pile to swap with",
        )
        if not recuperee:
            return
        Faces.MoveAllToDeck(de_la_main, joueur.discard_pile, "Top", effect)
        joueur.GainCard(recuperee, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            anneaux,
            conditions=[defausse_non_vide],
        ).SetCost(Cost("Y"))
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(from_where=["YourHandCards"]),
    ]
