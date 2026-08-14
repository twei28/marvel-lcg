from . import *

# * Kingpin's Cane

def GetAbilities() -> Sequence['Ability']:

    def a_lattaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        # « [star] Forced Interrupt: When Kingpin initiates an attack against
        # you, put the top card of your deck into play facedown as a CORRUPT
        # side scheme. »
        joueur = message.GetAgainstPlayer()
        if joueur:
            PoserUneManiganceCorrompue(joueur, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # « [star] Boost: After this activation, attach this card to Kingpin. »
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()

        def apres() -> None:
            villain = Worlds.FindVillain(effect)
            if villain:
                this.PutIntoPlay(joueur, effect)
                this.AttachTo2(villain, effect)

        message.AfterThisActivation(effect, apres)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            Villain
        ),
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.ForcedInterrupt,
            "AttachedVillain",
            a_lattaque
        ),
        # « Hero Action: Spend [physical][physical][physical] resources →
        # discard this card. »
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("RRR")),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost
        ),
    ]
