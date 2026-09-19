from . import *

# Drained of Power (CONDITION) — Uses (3 drain counters) : base desc.
# When Revealed: Attach to your identity and exhaust each upgrade you control.
# Forced Interrupt: When an upgrade you control would ready, you may spend a
#   [energy] resource or 2 resources of any type. If you do, remove 1 drain
#   counter from here (and ready that upgrade). Otherwise, that upgrade does
#   not ready.
# Modeles : 50153 (AttachToFaceWhenPutIntoPlay("YourIdentity")), WhenCardWouldReady
# (control_by="You") + SetBeInstead pour « does not ready », Otherwise.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        ameliorations = [f for f in Worlds.FindCardsOnField(effect, card_type=Upgrade) if f.GetControlByPlayer() is joueur]
        if ameliorations:
            Faces.ExhaustAll(ameliorations, effect)

    def redressement(effect: 'Effect', message: 'Message.WhenCardWouldReady') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.trigger.GetControlByPlayer()
        if joueur is None:
            return

        def payer() -> None:
            Faces.RemoveCountersOn([this], 1, 'drain', effect)

        def sinon(targets: Sequence['CardFace']) -> None:
            message.SetBeInstead(effect)

        joueur.ChooseAbilities(
            effect,
            *ChoixPayerEnergieOuDeux(joueur, effect, "ready that upgrade", payer),
            AbilityFactory.Otherwise(sinon),
        )

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardWouldReady(
            AbilityType.ForcedInterrupt,
            CardFinder(card_type=Upgrade),
            redressement,
            control_by="You",
        ),
    ]
