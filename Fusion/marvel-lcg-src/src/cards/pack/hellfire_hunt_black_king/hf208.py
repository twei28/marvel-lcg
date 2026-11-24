from . import *

# Dust (Sooraya Qadir), allie CAPTIVE MUTANT. « [star] Interrupt : When Dust attacks, resolve this attack against the villain and each minion
# engaged with you. »
# Cartes de reference : 33012 Dust (officiel, meme nom, ATTAQUE tous les sbires : `WhenUnitWouldAttack(Interrupt, "This", op)` +
# `message.AlsoResolveThisAttackTo(units)`), 01130 Whirlwind (`AlsoResolveThisAttackTo`).
# ⚠ Mots-pieges : « the villain AND each minion engaged WITH YOU » : le vilain + les sbires engages avec le CONTROLEUR de Dust (pas tous les sbires) ;
# `AlsoResolveThisAttackTo` ignore la cible deja visee (jamais de doublon). Allie : consequences = icones imprimees (`desc.ATK "2**"`).


def GetAbilities() -> Sequence['Ability']:
    def dust(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Ally)
        controleur = this.GetControlBy()
        cibles = list(Worlds.GetVillains(effect))
        if Player.IsType(controleur):
            cibles += list(controleur.GetEngagedMinions())
        message.AlsoResolveThisAttackTo(cibles)

    return [AbilityFactory.WhenUnitWouldAttack(AbilityType.Interrupt, "This", dust), CaptifRecrute()]
