from . import *

# * Victorious — Zora Vukovic. Allie signature. HERALD. LATVERIA.
# Cout 3, 3 PV, CTR 1*, ATQ 3*. Toughness.
# Response: After Victorious enters play, search your deck and discard pile
#   for a SPELL event and add it to your hand.
#
# Cartes de reference :
#  - « After <allie> enters play » : 01083 Mockingbird / ho002,
#    `AfterCardEnterPlay(Response, "This", op)` (recette moteur §1) ;
#  - fouille deck + defausse puis mise en main : 04001b * Clint Barton,
#    `Search.PlayerCard(effect, player, include_player_deck=True,
#    include_discard_pile=True, ...)` puis `player.GainCard`.
#
# ⚠ `include_player_deck` est OBLIGATOIRE, sans valeur par defaut
# (search.py:133) : l'omettre leve un TypeError a chaque activation. Piege paye
# sur bt011 le 01/09/2026, trouve par l'autoplay et NON par le cas de test.
#
# ⚠ « Toughness » est une base automatique lue dans `desc` : aucun module.
#
# ⚠ Le filtre porte sur un EVENEMENT [[SPELL]], pas sur n'importe quelle carte
# SPELL : `CardFinder2("SPELL", Event)` — le pack contient aussi des
# ameliorations TECH, qu'il ne faut pas proposer ici.

def GetAbilities() -> Sequence['Ability']:

    def victorious(effect: 'Effect', message: 'Message.WhenCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            trait="SPELL",
            card_type=Event,
        )
        if face:
            initiator.GainCard(face, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            victorious,
        ),
    ]
