from . import *

# * Pete — SOUTIEN 1 [energy], aspect Aggression (TMNT Aspects, Inkwire). MUTANIMAL. PERSONA. PIGEON.
# Uses (3 pistol counters).
# Response: After you deal damage to an enemy, exhaust Pete and remove 1 pistol counter from him → deal 1 damage
#   to that enemy.
#
# MOT-CLE (fiche lue AVANT le code) : uses.md — `desc.Uses = "3,pistol"`, lu nativement (compteur 'pistol'
#   ajoute a `CardFace.COUNTER`, 16/10/2026).
# CARTES DE REFERENCE
#  - `16032` Schadenfreude (« each time YOU deal any amount of damage to an enemy ») = `AfterYouDealDamage(...)`
#    (damage.py : `AfterFaceDealDamage` dont la source est « YourIdentity »).
#  - `62018` / `61033b` : deux couts « exhaust X and remove 1 counter » = deux `SetCostFunc` enchaines.
# TEXTE CONTRE CODE
#  ⚠ « After YOU deal damage » : lecture du moteur pour 16032, MESUREE (cas `[ua] ua033`) : votre identite ET les
#    evenements que vous jouez declenchent Pete ; un allie, non. ⚠ Question Q-UA3 (aspects-aggression-questions.md) :
#    carte NON terminee tant que la reponse n'est pas rendue.
#  ⚠ « that enemy » = l'ennemi qui vient de prendre les degats (`message.who_took_damage`).
#  ⚠ « exhaust Pete AND remove 1 pistol counter » : deux couts, les deux payes ou aucun.


def GetAbilities() -> Sequence['Ability']:

    def pete(effect: 'Effect', message: 'Message.AfterFaceDealDamage') -> None:
        this = effect.this.CastTo(Support)
        # `who_took_damage` est une LISTE (sender_damage.py) : « that enemy » = l'ennemi blesse.
        cibles = [x for x in (message.who_took_damage or []) if Enemy.IsType(x) and x.IsInPlay()]
        if cibles:
            this.DealDamage(cibles[:1], 1, effect)

    return [
        AbilityFactory.AfterYouDealDamage(
            AbilityType.Response,
            Enemy,
            pete,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'pistol')),
    ]
