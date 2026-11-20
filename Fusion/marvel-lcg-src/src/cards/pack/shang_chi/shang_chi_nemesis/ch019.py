from . import *

# * Zheng Zu (sbire NEMESIS de Shang-Chi) — PV 6, SCH 2, ATK 1★, boost 2. ELITE. MYSTIC.
# Forced Response: After Zheng Zu schemes, place 1 mystic counter here.
# [star] Zheng Zu gets +1 ATK for each mystic counter here.
#
# Cartes de reference :
#  - `nt013` (night_thrasher_nemesis) / `08012` : `AfterUnitSchemeEnd(ForcedResponse, "This", op)` (« after X schemes »).
#  - `64009` Embody the Dragon : valeur dynamique par compteur, `GiveKeywordToInPlayWhenApplyThis(finder, get_new_value=fn,
#    change_on_event=OnEvent.Counter("This", 'nom'))` ; `64001a` pour le compteur pose.
#  - `mystic` est deja un compteur connu du moteur (`CardFace.COUNTER`).
#
# ⚠ Mots-pieges :
#  - « After Zheng Zu SCHEMES » : sa propre activation de manigance (ATTAQUE exclue) ; le compteur se pose APRES (Forced Response).
#  - « +1 ATK FOR EACH mystic counter here » : ATK de base 1 + N compteurs ; la valeur imprimee « 1★ » vaut 1 de base.
#    Sans compteur : ATK 1.
#  - les compteurs restent sur LUI (« here »), pas sur la manigance annexe (ch020 compte les siens a part).
#  - « Shang-Chi's nemesis minion » : `desc.Nemesis`, rien a coder.


def GetAbilities() -> Sequence['Ability']:

    def mystiques(effect: 'Effect', face: 'CardFace') -> int:
        Unused(face)
        return effect.this.GetCounters('mystic')

    def apres_manigance(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        Faces.PlaceCountersOn([this], 1, 'mystic', effect)

    return [
        AbilityFactory.AfterUnitSchemeEnd(
            AbilityType.ForcedResponse,
            "This",
            apres_manigance,
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "This",
            attack=1,
            get_new_value=mystiques,
            change_on_event=OnEvent.Counter("This", 'mystic'),
        ),
    ]
