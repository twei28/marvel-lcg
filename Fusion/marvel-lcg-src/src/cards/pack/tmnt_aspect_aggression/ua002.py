from . import *

# Apex Predator — EVENEMENT 1* [energy], aspect Aggression (TMNT Aspects, Inkwire). ATTACK. FERAL.
# [star] Rampage 2. (As an additional cost for this card, take 2 damage and discard 2 cards from the top of
#   your deck.)
# Hero Action (attack): Choose: • Deal 4 damage to an enemy. • Stun an enemy.
#
# MOT-CLE (fiche lue AVANT le code) : Rampage X — docs/reference/mots-cles/rampage.md : `CostFunc.Rampage(2)`.
# CARTES DE REFERENCE
#  - `ua015` Demolish : meme mot-cle sur une Hero Action (attack), `.SetPlay().SetLabel('attack')`.
#  - `sk041` (Lyja) / `20008` Multi-Gun : « Choose: » = `ChooseAbilities` de `ForChoiceAbility` ciblees.
# TEXTE CONTRE CODE
#  ⚠ « Choose » : UNE des deux branches, au choix du joueur, a la resolution (apres le cout).
#  ⚠ « an enemy » : vilain ou sbire, dans les deux branches ; la branche « Stun » n'est offerte que s'il existe
#    un ennemi qui peut etre sonne (`canbe_stunned`).
#  Aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def apex(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        effect.GetInitiator().ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 4 damage to an enemy",
                lambda cibles: this.DealDamage(cibles, 4, effect),
            ).SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility(
                "Stun an enemy",
                lambda cibles: Faces.GiveStatus(cibles, "Stunned", effect),
            ).SetTarget(Enemy, canbe_stunned=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            apex,
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.Rampage(2)),
    ]
