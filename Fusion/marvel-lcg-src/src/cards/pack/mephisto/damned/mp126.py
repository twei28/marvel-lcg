from . import *

# Harmony Demon — SBIRE MYSTIC. PV 4, ATK 1, SCH 3, Boost 1, Incite 2, Teamwork (MYSTIC) (natifs).
# [star] Forced Response : After Harmony Demon activates, heal 1 damage from each other MYSTIC minion in play.
# [star] Boost : If this activation is a scheme, give the activating enemy a tough status card and this card gets +1 boost icon for this activation.
#
# Cartes de reference : activate.py `AfterEnemyActivatesAgainstYou`/`AfterEnemyActivationEnd`, `Faces.GiveStatus`, `GainBoostIcons`.
# ⚠ Mots-pieges : « EACH OTHER MYSTIC minion » : tous les autres, pas elle-meme ; Boost « IF this activation is a SCHEME » : rien pour une attaque ; le Tough va a l'ennemi QUI ACTIVE.


def GetAbilities() -> Sequence['Ability']:
    def soigne(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        for m in SbiresMystiquesEnJeu(effect, sauf=effect.this):
            m.CastTo(Minion).HealHealth(1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        if hasattr(message, "would_sch_message"):
            Faces.GiveStatus([message.activating_enemy], "Tough", effect)
            effect.this.CastTo(Minion).GainBoostIcons(1, effect)

    return [
        AbilityFactory.AfterEnemyActivationEnd(AbilityType.ForcedResponse, "This", soigne),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
