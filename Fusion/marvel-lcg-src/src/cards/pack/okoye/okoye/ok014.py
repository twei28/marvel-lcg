from . import *

# * Royal Protector — TITLE
# Increase your ally limit by 1. Okoye gets +1 THW while in hero form.
# Hero Response: After a WAKANDA ally is defeated, exhaust Royal Protector ->
#   ready Okoye.
#
# TITLE, non-attachable (aucune ligne "Attach to..." imprimee) : porte
# directement par le joueur, modele Alexei Shostakov's own upgrades ou plus
# simplement kb011/kb012 (Upgrade sans attache, `SetCostFunc` seul). "Increase
# your ally limit by 1" : `ally_limit` param deja expose par
# `AbilityFactory.GiveKeywordToInPlayWhenApplyThis` (environment.py:78),
# module sur le porteur lui-meme (`"You"`). "Okoye gets +1 THW while in hero
# form" : `AbilityFactory.GiveKeywordToInPlayWhenApplyThis(Hero, control_by=
# "You", thwart=1)` cible la face Heros precisement (elle n'existe QUE quand
# active), pas de condition de forme supplementaire necessaire.
#
# "Hero Response: After a WAKANDA ally is defeated, exhaust -> ready Okoye" :
# modele bkw/08031.py (AfterUnitBeDefeated) + `Faces.ReadyAll`.


def GetAbilities() -> Sequence['Ability']:

    def royal_protector(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        Faces.ReadyAll([initiator.GetHero()], effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            ally_limit=1,
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Hero,
            control_by="You",
            thwart=1,
        ),
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.HeroResponse,
            ("YouControl", CardFinder(card_type=Ally, trait="WAKANDA")),
            royal_protector,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
