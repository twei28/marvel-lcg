from . import *

# Mancatcher Net

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Choose and discard the lowest-cost support or upgrade
        # you control. Stun your identity. »
        joueur = message.GetToPlayer()
        cartes = [x for x in joueur.GetControlCards()
                  if Upgrade.IsType(x) or Support.IsType(x)]
        if cartes:
            plus_bas = min(x.printed_cost.val for x in cartes)
            cartes = [x for x in cartes if x.printed_cost.val == plus_bas]
            choisie = joueur.AskChooseFace(cartes, effect, prompt="Discard the lowest-cost card")
            Faces.DiscardAll([choisie or cartes[0]], effect)

        Faces.GiveStatus([joueur.GetIdentity()], "Stunned", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
