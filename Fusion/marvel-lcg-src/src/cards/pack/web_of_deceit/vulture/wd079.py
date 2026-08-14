from . import *

# Sweeping Swoop

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Stun your hero. »
        #
        # ⚠ La carte officielle (01168) ne deferle QUE si Vulture est en jeu ;
        # celle-ci deferle TOUJOURS, et le mot-cle est dans la donnee. Le boost,
        # lui, est identique au mot pres — d'ou la meme fabrique.
        joueur = message.GetToPlayer()
        if joueur.IsHero():
            Faces.GiveStatus([joueur.GetHero()], "Stunned", effect)

    def boost(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        # « [star] Boost: If this activation deals damage to a friendly
        # character, stun that character. »
        Faces.GiveStatus([message.trigger], "Stunned", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
        AbilityFactory.BoostIfThisActivationDealsDamage(
            Friend,
            boost
        ),
    ]
