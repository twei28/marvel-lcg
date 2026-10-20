from . import *

# Outpost Collapse Protocol — MANIGANCE ANNEXE (Kree Sentry). Menace de depart 1, Hinder 2[per_hero]. 2 icones de boost.
# Forced Response: After resolving step one of the villain phase, the first player deals 1 damage to each character they
#   control.
#
# Cartes de reference :
#  - Hinder 2[per_hero] : BASE AUTOMATIQUE `desc.Hinder = "2*"` (fiche hinder.md, modele 16066).
#  - « After resolving step one of the villain phase » : `AfterResolveVillainPhaseStep(ForcedResponse, 1, op)`, modele
#    gs117b / 04096b.
#  - « the first player deals 1 damage to each character they control » : `DealDamage(joueur.GetControlCharacters(), 1)`
#    (modele 54035 pour `DealDamage`).
#
# ⚠ Mots-pieges : « the FIRST player » (pas chaque joueur) ; « EACH character THEY CONTROL » = son identite, ses allies
# ET Rick Jones, que le premier joueur controle ; pas les sbires ni le mechant ; « 1 damage » a chacun.


def GetAbilities() -> Sequence['Ability']:

    def effondrement(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        Unused(message)
        premier = Worlds.GetFirstPlayer(effect)
        personnages = [f for f in premier.GetControlCharacters() if f.IsInPlay()]
        if personnages:
            effect.this.DealDamage(personnages, 1, effect)

    return [
        AbilityFactory.AfterResolveVillainPhaseStep(AbilityType.ForcedResponse, 1, effondrement),
    ]
