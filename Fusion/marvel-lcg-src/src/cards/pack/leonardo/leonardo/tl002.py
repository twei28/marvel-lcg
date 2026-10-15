from . import *

# * Splinter — ALLIE signature, x1. NINJA. RAT. SENSEI.
# Cout 3, [wild]. ATQ 2*, CTR 2*, PV 3 (« * » = degats consecutifs 1).
# Response: After Splinter enters play, choose an identity-specific card in
#   your discard pile and put it on top of your deck.
#
# Cartes de reference :
#  - `01083` Mockingbird / `ho002` : `AfterCardEnterPlay(Response, "This", op)` ;
#  - `25009` Visit Valhalla / `51009` Aja-Adanna :
#    `.SetTarget(card_class="IdentitySpecific", from_where=["YourDiscardPile"])`
#    pour « an identity-specific card in your discard pile » ;
#  - `bt011` Hank's Kimono : `Faces.MoveAllToDeck([face], deck, "Top", effect)`
#    (la position est un argument POSITIONNEL).
#
# Mots-pieges :
#  - « ON TOP of your deck » : dessus, pas melange ;
#  - Response OBLIGATOIRE seulement s'il y a une cible : sans carte
#    specifique a l'identite en defausse, la capacite n'est pas proposee ;
#  - ATQ/CTR « 2* » : base automatique de `desc` (can_attack.py:47-52), aucun
#    script pour les degats consecutifs ;
#  - « Ally » classe `Hero` (carte signature).


def GetAbilities() -> Sequence['Ability']:

    def splinter(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        Faces.MoveAllToDeck(list(effect.targets), joueur.player_deck, "Top", effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            splinter,
        ).SetTarget(card_class="IdentitySpecific", from_where=["YourDiscardPile"]),
    ]
