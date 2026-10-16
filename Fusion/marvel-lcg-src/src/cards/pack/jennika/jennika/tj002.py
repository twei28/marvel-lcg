from . import *

# Composure — evenement signature, x3. SKILL. Cout 1, [mental].
# Action: Choose a card in your discard pile -> add that card to your hand.
#
# Carte de reference : `mts/adam_warlock/21040` Quantum Magic — MEME texte mot
# pour mot : `Action` + `SetPlay()` + `SetTarget(from_where=["YourDiscardPile"])`,
# puis `GainCard` (la carte rejoint la main).
#
# ⚠ Mots-pieges :
#  - « Action » (sans « Hero ») : jouable en forme heros ET alter-ego ;
#  - « a card in YOUR discard pile » : la defausse du joueur, tout type de carte ;
#  - Composure se joue puis part en defausse APRES la resolution : elle ne peut
#    pas se choisir elle-meme ;
#  - aucun libelle (pas de « (attack/thwart) » imprime).


def GetAbilities() -> Sequence['Ability']:

    def composure(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        joueur.GainCard(effect.targets, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            composure,
        ).SetPlay().SetLabel()
        .SetTarget(from_where=["YourDiscardPile"]),
    ]
