from . import *

# Mirror Image — amelioration signature. ILLUSION. SPELL. Cout 2. x1
# While in hero form, Agatha Harkness gets +1 THW.
# Interrupt: When you would take damage that would defeat you, discard this
#   card instead.
#
# Cartes de reference (RECETTES) :
#  - +1 THW : an008 (`GiveKeywordToAttached("You", thwart=1)`) — le THW
#    n'existe qu'en forme heros, la clause « While in hero form » est portee
#    par la stat elle-meme ;
#  - le bouclier : 56069 Mark V Armor (`WhenUnitWouldTakeDamage` +
#    `message.SetBeInstead(effect)`), condition « would defeat you » lue sur
#    `message.will_take_damage` contre les PV restants (56100 Cosmic Flight
#    pour le seuil).
#
# ⚠ « INSTEAD » : les degats ne tombent PAS (SetBeInstead), seule la carte
# part — piege « instead » de l'etape 5. On ne previent que si les degats
# TUERAIENT (>= PV restants) : un coup non letal passe au travers.

def GetAbilities() -> Sequence['Ability']:

    def bouclier(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)

        message.SetBeInstead(effect)
        Faces.DiscardAll([this], effect)

    def degats_letaux(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        identite = effect.this.GetControlByPlayer().GetIdentity()
        if identite is None:
            return False
        return message.will_take_damage >= identite.health

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            thwart=1,
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            "You",
            bouclier,
            conditions=[degats_letaux],
        ),
    ]
