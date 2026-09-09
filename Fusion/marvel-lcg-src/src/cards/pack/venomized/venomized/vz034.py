from . import *

# Urban Camouflage — AMELIORATION, cout 3, RES [mental]. PREPARATION. SUPERPOWER.
# Max 1 per player.
# Hero Interrupt: When an enemy would attack you, take 1 damage and discard
#   this card -> give your hero a tough status card and confuse that enemy.
#
# CARTE DE REFERENCE
#  - `51019` Invisibility Gear : « Interrupt: When an enemy would attack you,
#    discard Invisibility Gear -> ... ». MEME fenetre
#    (`WhenUnitWouldAttack(..., Enemy, ..., against_player="You")`), meme cout
#    de defausse. Seuls s'ajoutent le degat et l'effet.
#  - `CostFunc.TakeDamage(1, "YourIdentity")` (`cost_func.py:408`), comme
#    `bl009` : le second cout.
#
# TEXTE CONTRE CODE
#  ⚠ DEUX couts avant la fleche : le degat ET la defausse. Deux `SetCostFunc`
#    chaines. Si l'un est impayable, la capacite ne part pas.
#  ⚠ « Hero Interrupt » : `AbilityType.HeroInterrupt`, pas `Interrupt` — c'est
#    l'ecart avec `51019`, qui vaut dans les deux formes.
#  ⚠ « give YOUR HERO a tough status card » mais « confuse THAT ENEMY » : deux
#    destinataires differents dans la meme phrase.
#  ⚠ « an ENEMY », pas « a minion » : le vilain declenche aussi.
def GetAbilities() -> Sequence['Ability']:

    def urban_camouflage(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        joueur = effect.GetInitiator()
        Faces.GiveStatus([joueur.GetHero()], "Tough", effect)
        Faces.GiveStatus([message.trigger], "Confused", effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            Enemy,
            urban_camouflage,
            against_player="You",
        ).SetCostFunc(CostFunc.TakeDamage(1, "YourIdentity"))
        .SetCostFunc(CostFunc.Discard("This")),
    ]
