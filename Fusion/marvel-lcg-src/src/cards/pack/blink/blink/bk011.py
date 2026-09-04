from . import *

# Little Surprise (x2) — EVENEMENT d'AGRESSIVITE, cout 1, [mental]. ATTACK.
# Hero Interrupt (attack): When an enemy schemes, deal 4 damage to that enemy.
#
# TEXTE CONTRE CODE
#  « When an enemy SCHEMES » -> `WhenUnitWouldScheme`, la fenetre AVANT que la
#    menace ne soit posee : les 4 degats peuvent donc tuer le sbire et annuler
#    sa manigance. C'est tout l'interet de la carte, et la raison pour laquelle
#    c'est une INTERRUPTION et non une Reponse.
#  « (attack) » -> libelle imprime, donc soumis a Patrouille.


def GetAbilities() -> Sequence['Ability']:

    def petite_surprise(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        this = effect.this.CastTo(Event)
        auteur = getattr(message, "trigger", None)
        if auteur is not None:
            this.DealDamage([auteur], 4, effect)

    return [
        AbilityFactory.WhenUnitWouldScheme(
            AbilityType.HeroInterrupt,
            Enemy,
            petite_surprise,
        ).SetPlay().SetLabel('attack'),
    ]
