from . import *

# Tapping the M'kraan Force — MANIGANCE ANNEXE (Majestrix's Verdict), menace de depart 2. Hinder 2[per_hero].
# Amplify. Hazard. 3 icones de boost.
# When Defeated: Heal 1 damage from each STARJAMMER ally in play.
#
# Cartes de reference :
#  - Hinder, Amplify, Hazard : BASES AUTOMATIQUES (`desc`, fiches hinder.md, amplify.md, hazard.md) ; icones
#    comparees par decoupe a sk252 (Amplify) et sk100 (Hazard).
#  - When Defeated d'une manigance : `WhenSchemeBeDefeated(WhenDefeated, "This")` (modele sk100) ;
#    « Heal 1 damage from each » : `HealthUnits(allies, 1)` (card_face.py).
#
# ⚠ Mots-pieges : « EACH STARJAMMER ally IN PLAY » (les glisses ne sont pas en jeu) ; soin bien au benefice des
# joueurs (manigance vaincue par eux).


def GetAbilities() -> Sequence['Ability']:

    def soigner(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        Unused(message)
        allies = StarjammersEnJeu(effect)
        if allies:
            effect.this.HealthUnits(allies, 1, effect)

    return [
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", soigner),
    ]
