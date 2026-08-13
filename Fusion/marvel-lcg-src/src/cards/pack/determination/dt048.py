from . import *

# Pay The Piper

def GetAbilities() -> Sequence['Ability']:

    def pay_the_piper(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        villain = Worlds.FindVillain(effect)
        if villain is None:
            return

        # « les cartes de rencontre face cachee de VOTRE zone de joueur » : le
        # moteur les tient dans `dealt_encounter_cards` (50051, Intelligence).
        cachees = list(initiator.dealt_encounter_cards.Get())
        for face in cachees:
            villain.CastTo(CanBoost).GiveBoostCard(face, effect)

        villain.DoAttackYou(initiator, effect,
                            property=AttackProperty(overkill=True, piercing=True))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            pay_the_piper,
            # « one or more » : sans carte face cachee, la carte n'a rien a donner.
            conditions=[lambda effect, message:
                        len(effect.GetInitiator().dealt_encounter_cards.Get()) > 0],
        ).SetPlay(),
    ]
