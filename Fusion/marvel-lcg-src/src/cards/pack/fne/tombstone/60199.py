from . import *

# Hit List (side scheme, 3[per_hero])
# Forced Response: After the villain phase begins, deal 3 indirect damage to
#   the first player. For each ally defeated this way, remove 1[per_hero]
#   threat from Hit List.
# AfterPhaseBegin("Villain") ; TakeIndirectDamage.
# ⚠ `operation=` de TakeIndirectDamage ne voit PAS les unites vaincues :
# can_health.py:288 n'envoie AfterUnitTookDamage (et n'appelle l'operation)
# que `if unit.IsInPlay()`, or l'allie vaincu est deja defausse. Mesure au
# harnais du 18/09/2026 (Spider-Woman vaincue, menace inchangee). On compare
# donc les allies en jeu avant et apres les degats.

def GetAbilities() -> Sequence['Ability']:

    def liste(effect: 'Effect', message: 'Message.AfterPhaseBegin') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        premier = Worlds.GetFirstPlayer(effect)
        identite = premier.GetIdentity()
        allies_avant = [a for a in premier.GetControlAllies() if a.IsInPlay()]
        identite.TakeIndirectDamage(this, 3, effect)
        vaincus = [a for a in allies_avant if not a.IsInPlay() or a.IsDefeated()]
        if vaincus:
            this.RemoveThreatFromSchemes([this], Worlds.GetPlayerNumIcon(effect) * len(vaincus), effect)

    return [
        AbilityFactory.AfterPhaseBegin(AbilityType.ForcedResponse, "Villain", liste),
    ]
