from . import *

# Angelic Ribbons — amelioration. WEAPON. Cout 1.
# Angela gains steady.
# Hero Interrupt: When an enemy activates, discard this card -> that enemy gets
#   -X ATK and -X SCH for that activation, where X is Angela's ATK.
#
# Cartes de reference : 05023 Endurance / ra007 Mjolnir pour l'octroi de
# `steady` a l'identite portee (fiche mots-cles/steady.md), et vp010 True Form
# (pack venompool) pour le montage « Interrupt paye par la carte elle-meme ».
#
# ⚠ « discard this card » est le COUT, pas l'effet : `CostFunc.Discard("This")`.
# ⚠ « for THAT activation » : le moteur a une brique DEDIEE pour ca,
# `GainForThisActive(effect, message.would_message, ...)` — modele 40185
# * Dragoness (pack aoa), qui porte le meme libelle « +X ATK and +X SCH for
# that activation ». Un `Gain()` ordinaire serait PERMANENT : l'ennemi
# garderait le malus toute la partie.
# ⚠ X est l'ATQ d'ANGELA au moment ou l'on paie — Xiphos (+1 ATK) la fait
# monter, donc on lit la valeur COURANTE de l'identite, jamais l'imprimee.

def GetAbilities() -> Sequence['Ability']:

    def angelic_ribbons(effect: 'Effect', message: 'Message.WhenEnemyActivateAgainstYou') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        identite = None
        initiator = effect.GetInitiator()
        if isinstance(initiator, Player):
            identite = initiator.GetIdentity()
        if identite is None:
            return
        malus = identite.attack
        if malus <= 0:
            return

        ennemi = effect.this.CastTo(Upgrade)
        Unused(ennemi)
        cible = message.trigger
        if cible is None:
            return
        cible.GainForThisActive(
            effect,
            message.would_message,
            attack=-malus,
            scheme=-malus,
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            steady=1,
        ),
        AbilityFactory.WhenEnemyActivateAgainstYou(
            AbilityType.HeroInterrupt,
            Enemy,
            angelic_ribbons,
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
