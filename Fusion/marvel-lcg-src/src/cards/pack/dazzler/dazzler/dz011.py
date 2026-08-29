from . import *

# "The Serpent is Coming"
# SONG. ATTACK.
# Hero Action (attack): Deal 6 damage to an enemy. This attack gains ranged.
# Showtime!: Deal 2 damage to an enemy.
#
# Comme Shield Strike (rg007) pour le perforant : « ranged » n'est pas un
# keyword a accorder, c'est une propriete de l'attaque
# (`AttackProperty(ranged=True)`).
#
# Le « Showtime! » ne porte PAS le libelle attaque : il ne se resout pas comme
# une attaque du heros, il est declenche par une autre carte depuis la Setlist.


def GetAbilities() -> Sequence['Ability']:

    def le_serpent_arrive(effect: 'Effect',
                          message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        this.DealDamage(effect.targets, 6, effect,
                        property=AttackProperty(ranged=True))

    def showtime(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Event)
        # Le joueur CHOISIT la cible : `ResolveAbility` prendrait sinon la
        # premiere cible legale sans rien demander (cf. CiblesShowtime).
        this.DealDamage(CiblesShowtime(effect), 2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            le_serpent_arrive,
        ).SetPlay().SetLabel("attack")
        .SetTarget(Enemy),
        Showtime(showtime).SetTarget(Enemy, range=(0, 1)),
    ]
