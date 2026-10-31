from . import *

# Psychokinetic Blast — EVENEMENT, cout 3, [mental]. ATTACK. PSIONIC.
# Hero Action (attack): Deal 6 damage to an enemy. Confuse that enemy.
#
# CARTE DE REFERENCE : `30007` Swinging Web Pig, texte identique mot pour mot (6 degats + Confused).
#
# TEXTE CONTRE CODE
#  « Hero Action (attack) » -> `HeroAction` + `SetLabel('attack')`. « an enemy » -> `SetTarget(Enemy)`.
#  « that enemy » -> la MEME cible (`effect.targets`) pour les degats et pour le statut.
#  Chiffres : 6 degats (cout 3 dans `cards.json`).


def GetAbilities() -> Sequence['Ability']:

    def psychokinetic_blast(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        this.DealDamage(effect.targets, 6, effect)
        Faces.GiveStatus(effect.targets, "Confused", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            psychokinetic_blast,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
