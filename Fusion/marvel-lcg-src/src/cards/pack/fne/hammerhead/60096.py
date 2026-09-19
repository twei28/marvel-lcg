from . import *

# "Head First!"
# When Revealed (Alter-Ego): This card gains surge.
# When Revealed (Hero): Hammerhead attacks you. If you are stunned, Hammerhead
#   gets +2 ATK for this attack and this attack gains overkill.
#
# Modele : 04086 Swinging Stone (AttackProperty(additional_value=...)), 01106
# Stampede (surge en alter-ego). L'overkill se declare dans la meme propriete.

def GetAbilities() -> Sequence['Ability']:

    def tete_la_premiere(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        hammerhead = TrouverHammerhead(effect)
        if hammerhead is None:
            return
        if joueur.GetIdentity().IsStunned():
            propriete = AttackProperty(additional_value=2, overkill=True)
        else:
            propriete = AttackProperty()
        hammerhead.DoAttackYou(joueur, effect, property=propriete)

    return [
        AbilityFactory.WhenThisRevealed(
            "Alter-Ego",
            ThisCardGainSurge,
        ),
        AbilityFactory.WhenThisRevealed(
            "Hero",
            tete_la_premiere,
        ),
    ]
