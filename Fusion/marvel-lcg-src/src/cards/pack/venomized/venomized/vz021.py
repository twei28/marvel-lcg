from . import *

# Symbiotic One By One — EVENEMENT, cout 1, RES [energy]. ATTACK. SYMBIOTE.
# Hero Action (attack): Deal 2 damage to an enemy. If this attack defeats that
#   enemy, deal 2 damage to an enemy.
#
# CARTE DE REFERENCE
#  - `28014` One by One (Agression, pack nova) : meme cout, meme ressource,
#    meme texte. Corps repris tel quel.
#
# TEXTE CONTRE CODE
#  ⚠ « If this attack DEFEATS that enemy » -> `if_this_attack_defeats`, un
#    parametre de `DealDamage` : la seconde attaque ne part que si la premiere
#    a mis K.O., ce qu'un test pose apres coup ne saurait pas dire.
#  ⚠ La seconde cible est LIBRE (« an enemy », pas « another ») : aucun
#    `exclude`, contrairement a vz019.
def GetAbilities() -> Sequence['Ability']:

    def symbiotic_one_by_one(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        def si_mis_ko(unit: 'Unit2'):
            Unused(unit)
            initiator = effect.GetInitiator()
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "",
                    lambda targets:
                        this.DealDamage(targets, 2, effect)
                ).SetLabel('attack').SetTarget(Enemy)
            )

        this.DealDamage(effect.targets, 2, effect, if_this_attack_defeats=si_mis_ko)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            symbiotic_one_by_one
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
