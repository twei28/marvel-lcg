from . import *

# Mental Torture — TRAITRISE (Seeds of Corruption), x2. 1 icone de boost.
# When Revealed: Discard 1 random card from your hand. If a [mental] resource was discarded this way, stun
#   your identity.
#
# Cartes de reference :
#  - **`wolv/deathstrike/35037`** Hack 'n' Slash : `player.DiscardRandomHandCards(1, effect)` puis lecture
#    des ressources imprimees de la carte defaussee.
#  - **`ip035`** / `AUneRessourceMentaleImprimee` du set : icone [mental] imprimee.
#  - « stun your identity » : `Faces.GiveStatus([identite], "Stunned", effect)` (05015).
#
# ⚠ Mots-pieges : « 1 RANDOM card from YOUR hand » (le joueur qui revele) ; « IF a [mental] resource was
# discarded THIS WAY » (la carte defaussee porte une icone mentale imprimee) ; main vide : rien ; « stun
# YOUR IDENTITY » (heros ou alter ego : l'etat s'applique a l'identite quelle que soit la forme).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        defaussees = joueur.DiscardRandomHandCards(1, effect)
        if any(AUneRessourceMentaleImprimee(f) for f in defaussees or []):
            Faces.GiveStatus([joueur.GetIdentity()], "Stunned", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
