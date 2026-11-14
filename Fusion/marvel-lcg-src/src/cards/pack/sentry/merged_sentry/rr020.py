from . import *

# * Merged Sentry : SBIRE (AERIAL. AVENGER. ELITE.), SCH 2☆ / ATQ 3, PV 4 par joueur, boost 3, Patrol, Guard, Toughness. Set « Merged Sentry » (modulaire).
# Merged Sentry gets +X ATK and cannot take less than X damage from each attack, where X is the number of overwhelm counters on him.
# ★ Forced Response: After Merged Sentry schemes or thwarts, place 1 overwhelm counter on him.
# When Defeated: The player who defeated Merged Sentry puts him into play under their control as an ally. Reset his hit points to 4, his THW is equal to his SCH, and he takes 1 consequential damage after he thwarts or attacks.
#
# CARTES DE REFERENCE
#  - « +X ATK » variable : `ThisGainKeyword(fn, attack=1, change_on_event=OnEvent.Counter("This", 'overwhelm'))` (rr016, `bw016`) ; plancher de degats : `WhenUnitWouldTakeDamage` + `IncreaseDamage` (rr016).
#  - « After X schemes » : `AbilityFactory.AfterUnitSchemeEnd(ForcedResponse, "This", op)` (do_scheme.py:70).
#  - « When Defeated : puts him under your control as an ally » : EXACTEMENT `warriors_three/wt020` (Skadihr) : `WhenUnitWouldBeDefeated(ForcedInterrupt, "This", op)` + `SetBeInstead` + `HealHealth(99)` + `Faces.TreatAsAlly(this, "tah_hellbender_ally", joueur, GameRule(this), process=..)`
#    puis `GainAttackConsequentialDamage(1)` / `GainThwartConsequentialDamage(1)`.
#
# TEXTE CONTRE CODE
#  « X = overwhelm counters ON HIM » (pas les balance counters de Sentry). « cannot take less than X damage from EACH ATTACK » : plancher par attaque (meme lecture que Void, decision utilisateur du 03/11). « schemes OR thwarts » : seule la manigance existe
#  tant qu'il est un sbire (apres sa defaite il est un allie : sa face est remplacee par le gabarit, ses capacites de sbire disparaissent). « Reset his hit points to 4 » : 4 PV (pas 4 par joueur). Chiffres : PV 4*, boost 3.


def GetAbilities() -> Sequence['Ability']:

    def x_courant(effect: 'Effect', faces: List['CardFace']) -> int:
        Unused(faces)
        return effect.this.GetCounters(NOM_SUBMERSION)

    def plancher(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        x = effect.this.GetCounters(NOM_SUBMERSION)
        subira = message.will_take_damage
        if x > 0 and 0 < subira < x:
            message.IncreaseDamage(x - subira, effect)

    def un_de_plus(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        Unused(message)
        Faces.PlaceCountersOn([effect.this], 1, NOM_SUBMERSION, effect)

    def devient_allie(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        joueur = None
        try:
            joueur = message.GetDefeatingPlayer()
        except Exception:
            joueur = None
        if joueur is None:
            joueur = effect.world.GetFirstPlayer()
        message.SetBeInstead(effect)
        this.HealHealth(99, effect)
        from game.effect.rule import GameRule

        def reprendre(allie: 'Any', ancien: 'Any') -> None:
            Unused(ancien)
            allie.printed_health = 4
            allie.printed_health_numeral = 4
            allie.starting_health = 4

        if Faces.TreatAsAlly(this, "tah_hellbender_ally", joueur, GameRule(this), process=reprendre):
            allie = this.card.face
            allie.GainAttackConsequentialDamage(1, effect)
            allie.GainThwartConsequentialDamage(1, effect)

    return [
        AbilityFactory.ThisGainKeyword(
            x_courant,
            attack=1,
            change_on_event=OnEvent.Counter("This", NOM_SUBMERSION),
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.NonKeyword, "This", plancher),
        AbilityFactory.AfterUnitSchemeEnd(AbilityType.NonKeywordStar, "This", un_de_plus),
        AbilityFactory.WhenUnitWouldBeDefeated(AbilityType.ForcedInterrupt, "This", devient_allie),
    ]
