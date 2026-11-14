from . import *

# Scheming from Within — MANIGANCE ANNEXE. Menace de depart 2[per_hero]. Hazard. 1 icone de boost + ★.
# When Revealed: Place 1 additional threat here for each villain beneath The Vault.
# [star] Boost: If Inspection of the Vault is in play, this card gets +1 boost icon for each villain beneath The Vault.
#
# Cartes de reference :
#  - Hazard : natif (desc.Hazard, fiche mots-cles/hazard.md ; icone verifiee sur le glyphe H de ChampionsIcons.ttf).
#  - « place N additional threat here » : `this.PlaceThreatOnSchemes([this], n, effect)` ; n = `len(MechantsSousLeVault)`.
#  - « this card gets +1 boost icon » : `AbilityFactory.WhenBoostIconsWouldBeCount` + `message.UpdateBoostIcon(n, effect)` (modele
#    56150, `IncreaseBoostIconsOnEncounterCard`).
#
# ⚠ Mots-pieges : « for each villain beneath » ne compte QUE les vilains (pas les sbires) ; l'effet de boost ne vaut que tant
# que l'Inspection est en jeu et que la carte est la carte de boost qu'on compte (pas quand elle est une manigance en jeu).


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        this = effect.this.CastTo(EncounterSideScheme)
        n = len(MechantsSousLeVault(effect))
        if n > 0:
            this.PlaceThreatOnSchemes([this], n, effect)

    def icones(effect: 'Effect', message: 'Message.WhenBoostIconsWouldBeCount') -> None:
        n = len(MechantsSousLeVault(effect))
        if n > 0:
            message.UpdateBoostIcon(n, effect)

    def inspection_et_cette_carte(effect: 'Effect', message: 'Message.WhenBoostIconsWouldBeCount') -> bool:
        return message.trigger is effect.this and InspectionEnJeu(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenBoostIconsWouldBeCount(AbilityType.NonKeyword, icones, conditions=[inspection_et_cette_carte]),
    ]
