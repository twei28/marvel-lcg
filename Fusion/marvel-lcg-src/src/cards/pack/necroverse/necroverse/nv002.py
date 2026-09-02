from . import *

# * Annihilablade — ATTACHEMENT NECROVERSE. WEAPON. +1 ATQ (etoile), 4 icones
# de boost.
#
# Attach to the villain.
# [star] Forced Interrupt: When the villain's attack would defeat an ally,
#   remove that ally from the game instead of discarding it.
# Hero Action: Spend [physical][mental][energy] resources and discard the top 5
#   cards of your deck → discard this card.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Attach to the villain » : 01098 (Armored Rhino Suit) et 45107, mais avec
#   `CardFinder(card_type=Villain)` : ce set modulaire se pose sur N'IMPORTE
#   QUEL vilain, il n'est pas lie a Gorr.
# - « would defeat ... remove from the game instead » : an014 pour le couple
#   `WhenUnitWouldBeDefeated` + `SetBeInstead`, et `Faces.RemoveAllFromGame`
#   (modele aa014) pour le retrait.
# - Action a cout en ressources : `SetCost(Cost("RBY"))`, et
#   `CostFunc.DiscardDeckTopCards` pour la seconde moitie.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « the VILLAIN's attack » -> l'attaque du vilain, pas celle d'un sbire.
# « would defeat AN ALLY » -> seulement un allie : un heros vaincu suit son
#   cours normal.
# « REMOVE FROM THE GAME instead of discarding » -> l'allie ne va pas a la
#   defausse, il quitte la partie : aucune carte ne pourra le rappeler.
# « Spend [physical][mental][energy] AND discard the top 5 » -> un cout a DEUX
#   parties, toutes deux obligatoires.


def GetAbilities() -> Sequence['Ability']:

    def la_lame_efface(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(this)

        allie = message.trigger
        if allie is None:
            return
        message.SetBeInstead(effect)
        Faces.RemoveAllFromGame([allie], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(card_type=Villain)
        ),
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.ForcedInterrupt,
            Ally,
            la_lame_efface,
            conditions=[
                # « the VILLAIN's attack » : la defaite doit venir d'une
                # attaque du porteur de cet attachement.
                lambda effect, message: Villain.IsType(
                    getattr(message, "killer", None) or effect.this.bind_face),
            ],
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("RBY"))
        .SetCostFunc(CostFunc.DiscardDeckTopCards("YourDeck", 5)),
    ]
