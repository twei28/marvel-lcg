from . import *

# Elbow Strike — EVENEMENT 0 [physical], Taijutsu (TMNT Shinobi, Inkwire). SKILL.
# Hero Response: After your hero makes a basic attack and damages an enemy, daze that enemy.
#
# Mots-cles (fiches lues AVANT le code) : Dazed / « daze » (dazed.md) ; Shinobi (shinobi.md).
#
# Cartes de reference : `psylocke/41015` Upside the Head, MEME declencheur (« After your hero makes a basic attack and
#   damages an enemy » = `AfterUnitMakeBasicAttack(HeroResponse, "YourHero", op, damage_who=Enemy).SetPlay().SetLabel()
#   .SetTarget("DamageTarget")`) ; l'effet change : `ShinobiDaze` au lieu de confus / etourdi (`tx016` Wrapped Up).
#
# TEXTE CONTRE CODE
#  ⚠ « your HERO makes a BASIC attack » : l'attaque de base du heros (pas un evenement d'attaque, pas un allie) ;
#    « and DAMAGES an enemy » : seulement si l'ennemi a vraiment pris des degats (cible « DamageTarget »).
#  ⚠ « daze THAT enemy » : l'ennemi blesse, pas un autre ; un ennemi deja hebete n'en recoit pas une seconde.
#  ⚠ « Hero Response » : forme heros seulement ; aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def elbow_strike(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        ShinobiDaze(effect, [e for e in effect.targets if Unit2.IsType(e)])

    return [
        AbilityFactory.AfterUnitMakeBasicAttack(
            AbilityType.HeroResponse,
            "YourHero",
            elbow_strike,
            damage_who=Enemy,
        ).SetPlay().SetLabel()
        .SetTarget("DamageTarget"),
    ]
