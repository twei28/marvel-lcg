from . import *

# Carjacking
# When Revealed: Discard cards from the encounter deck until a VEHICLE
#   attachment is discarded and reveal it. If your identity does not have a
#   VEHICLE attachment, you may spend 3 resources of the same type to attach
#   the discarded attachment to your identity instead.
# Modeles : 60184 Wanted (DiscardEncounterCardsUntil), 60127 Tug of War (branche
# payante offerte seulement si payable, PeutCouvrirLeCout), 40122a
# (Cost("3", same_type=True)).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        face = Worlds.DiscardEncounterCardsUntil(effect, trait="VEHICLE", card_type=Attachment)
        if face is None:
            return
        identite = joueur.GetIdentity()
        if AUnVehicule(identite):
            face.Reveal(joueur, effect)
            return

        def payable(effet_choix: 'Effect', message_choix: 'Message.WhenPlayerChooseAbility') -> bool:
            return PeutCouvrirLeCout(joueur, effet_choix, Cost("3", same_type=True))

        def attacher(targets: Sequence['CardFace'], res: 'Resources') -> None:
            face.CastTo(Attachment).AttachTo2(identite, effect)

        def sinon(targets: Sequence['CardFace']) -> None:
            face.Reveal(joueur, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("3", same_type=True),
                "Spend 3 resources of the same type: attach the discarded attachment to your identity instead",
                attacher, conditions=[payable]),
            AbilityFactory.Otherwise(sinon),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
