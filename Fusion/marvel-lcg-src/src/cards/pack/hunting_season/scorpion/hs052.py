from . import *

# hs052 Restraining Pincers

def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity()

        def etourdir(cibles) -> None:
            Faces.GiveStatus([identite], "Stunned", effect)

        options = [AbilityFactory.ForChoiceAbilityWithCost(Cost("RR"))]
        if not identite.IsStunned():
            options.append(AbilityFactory.ForChoiceAbility("Stun your identity", etourdir))
        if not joueur.ChooseAbilities(effect, *options):
            ThisCardGainSurge(effect)

    def epuiser(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        joueur = message.trigger.GetControlBy()
        Faces.ExhaustAll([joueur.GetIdentity()], effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.BoostIfThisActivationDealsDamage("You", epuiser),
    ]
