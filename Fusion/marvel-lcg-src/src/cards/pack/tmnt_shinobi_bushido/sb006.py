from . import *

# Mercy — AMELIORATION OATH, classe Bushido (Inkwire, TMNT Shinobi). Cout 1, [energy].
# Max 1 per player.
# Hero Interrupt: When an enemy would be defeated by your hero, discard this card instead -> set that enemy's hit points to 1.
#   Then, draw 3 cards.
#
# Q-B1 RESOLUE le 17/10/2026 (`.planning/tmnt/shinobi-reponses.md`, option (a)) : lecture confirmee, carte terminee. Le texte imprime place
# « instead » apres « discard this card » et avant la fleche : deux lectures (le « instead » remplace la DEFAITE de l'ennemi, ou il
# qualifie la defausse), et « set that enemy's hit points to 1 » (PV restants a 1) n'est pas tranche non plus. LECTURE RETENUE :
#  - cout = defausser cette carte (devant la fleche) ;
#  - effet = la defaite n'a PAS lieu (« instead » : `message.SetBeInstead`), les PV RESTANTS de l'ennemi passent a 1
#    (`SetHealth(1)`), PUIS le joueur pioche 3 cartes.
#
# Mots-cles (fiches lues AVANT le code) : samurai counter / OATH (samurai-counter.md) ; « Max 1 per player » (base automatique,
# `desc.MaxPerUnit = "1"`).
#
# Cartes de reference :
#  - « When X would be defeated, instead set his hit point dial to N » : `drax/19011` Too Stubborn to Die
#    (`WhenUnitWouldBeDefeated` + `message.SetBeInstead` + `SetHealth`) ;
#  - cout « discard this card » : `nebu/22014` Justice Served ; pioche : `DrawUp` (`trors/spider_woman/04032`).
#
# TEXTE CONTRE CODE
#  ⚠ « When an ENEMY would be defeated BY YOUR HERO » : un ennemi (sbire ou vilain), vaincu par le HEROS du joueur (le tueur du
#    message est la face heros) ; la defaite par un ALLIE ou par des degats consecutifs ne declenche pas.
#  ⚠ « Hero Interrupt » : AVANT la defaite ; forme heros seule.
#  ⚠ « set that enemy's hit points to 1 » : les PV restants valent 1 (l'ennemi survit avec 1 PV), pas les PV maximum.
#  ⚠ « Then, draw 3 cards » : apres ; 3 cartes exactement.


def GetAbilities() -> Sequence['Ability']:

    def par_votre_heros(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> bool:
        tueur = message.killer
        joueur = effect.GetInitiator()
        if tueur is None or joueur is None or not Hero.IsType(tueur):
            return False
        return tueur.GetControlByPlayer() == joueur

    def mercy(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.SetBeInstead(effect)
        ennemi = message.trigger.CastTo(Unit2)
        ennemi.SetHealth(1, effect)
        joueur = effect.GetInitiator()
        if joueur is not None:
            joueur.DrawUp(3, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.HeroInterrupt,
            Enemy,
            mercy,
            conditions=[par_votre_heros],
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
