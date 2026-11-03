from . import *

# Really? (Vraiment ?) (x2) : EVENEMENT (DEFENSE. SHAPESHIFTER.), cout 1, [energy].
# Hero Interrupt (defense): When you would take any amount of damage, prevent 3 of that damage. If the Friend shapeshift form upgrade is faceup, ready Mystique.
# (FR 1.1.1 ; l'EN beta 4.2 disait « draw 1 card » : le FR, plus recent, prime)
#
# CARTES DE REFERENCE
#  - `05005` Wiggle Room / `14015` Side Step : `WhenUnitWouldTakeDamage(HeroInterrupt, "You", op).SetPlay().SetLabel('defense')` + `message.PreventDamage(3, effect)`.
#
# TEXTE CONTRE CODE
#  « prevent 3 of THAT damage » : 3 points de CE paquet de degats (moins s'il y en a moins). « If the FRIEND form is FACEUP » : my005 face `a`. « ready MYSTIQUE » : l'identite du joueur (le heros). Interruption de HEROS.
#  Chiffres : cout 1, prevenir 3.


def GetAbilities() -> Sequence['Ability']:

    def really(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        joueur = effect.GetInitiator()
        message.PreventDamage(3, effect)
        if FormeVisible(joueur, ID_FRIEND):
            Faces.ReadyAll([joueur.GetIdentity()], effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            really,
        ).SetPlay().SetLabel('defense'),
    ]
