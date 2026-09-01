from . import *

# Incomparable Ego — obligation. Boost 1. Acceleration 1. Hazard 1.
# GiveTo: Victor von Doom.
# Give to the Victor von Doom player.
# Exhaust each ally you control. Allies you control cannot ready.
# Alter-ego action: Exhaust your identity and discard a [mental] from your
#   hand -> discard this card.
# [star] Boost: Reveal this card.
#
# Cartes de reference :
#  - squelette d'obligation : aa014 / bt019 / dd012 ;
#  - « exhaust each ally + cannot ready » : 44032 « The Merc with the Mouth »
#    (pack deadpool), meme couple exact — `Faces.ExhaustAll` sur les allies
#    puis un blocage continu du redressement ;
#  - `[star] Boost` : an013 / ho015, `WhenCardBecomeBoost("This", op)`
#    (recette moteur §1).
#
# ⚠ Acceleration et Hazard sont des BASES AUTOMATIQUES lues dans `desc`
# (fiches acceleration.md et hazard.md) : aucun module. Les deux icones ont ete
# identifiees par COMPARAISON D'IMAGE, jamais a vue (lecon Lockjaw) : le « + »
# sur maison soulignee est l'acceleration, le « + » sur carte inclinee le
# hazard.
#
# ⚠ Cette obligation mord tres fort sur ce heros PRECIS : son alter-ego
# interdit d'ajouter des allies au deck, donc les seuls allies possibles sont
# les signatures dd002 et dd003. L'effet est faible en pratique — c'est
# volontaire, l'auteur compense par les deux icones.
#
# ⚠ « discard a [mental] from your hand » : n'importe quelle carte PORTANT une
# icone mentale imprimee, pas une carte de type Resource. D'ou
# `has_printed_res="B"` et non `card_type=Resource`.

def GetAbilities() -> Sequence['Ability']:

    def incomparable_ego(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this)

        player = message.GetGaveToPlayer()
        if player is None:
            return
        allies = player.allies.FindCards(card_type=Ally)
        if allies:
            Faces.ExhaustAll(allies, effect)

    def defausser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(message)
        Faces.DiscardAll([this], effect)

    def revelation_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Obligation)
        this.Reveal(None, effect)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            incomparable_ego,
        ),
        # ⚠ `CardCannotReady` rend une LISTE d'abilities, d'ou le `*`.
        # Modele 44032 « The Merc with the Mouth », meme couple exact
        # « exhaust each ally » + « allies cannot ready ».
        *AbilityFactory.CardCannotReady(
            Ally,
            control_by="You",
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            defausser,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))
        .SetCostFunc(CostFunc.Discard("YourHandCards", has_printed_res="B")),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            revelation_boost,
        ),
    ]
