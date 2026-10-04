from . import *

# Savage She-Devil — evenement signature, x1 (10/15). ATTACK. THWART. Cout 4,
# ressource [Y].
# Hero Action (attack/thwart): Deal 5 damage to an enemy. Remove 5 threat
# from a scheme. If you used your "She-Devil" ability to reduce the cost of
# this card, this action ignores the guard and patrol keywords and any
# crisis icons in play.
#
# CARTES DE REFERENCE
#  - `18020` Hit and Run (officiel) : montage combo attaque+menee,
#    `.SetLabel('attack', 'thwart')` + `SetTarget`/`SetTarget2` distincts,
#    `effect.targets`/`effect.targets2`.
#  - `hc006` On the Prowl : `SetIgnoreKeyword(..., condition=...)` pour une
#    ignorance CONDITIONNELLE (ici pas `paid_with`, mais `AUtiliseSheDevil`).
#
# TEXTE CONTRE CODE
#  ⚠ « ignores the guard AND patrol keywords AND any crisis icons » : trois
#    mots-cles ignores ensemble, meme condition -> un seul
#    `.SetIgnoreKeyword('Guard', 'Patrol', 'Crisis', condition=...)`.
#  ⚠ La condition depend du MARQUEUR She-Devil, connu AVANT la resolution de
#    cette capacite (pose par `rs001a` avant `PlayCardsLikeInTurn`) : pas de
#    piege de timing comme `paid_with` (qui doit rester decidable APRES le
#    ciblage, ici la reponse est deja figee des le ciblage).

def GetAbilities() -> Sequence['Ability']:

    def she_devil_active(effect: 'Effect') -> bool:
        return AUtiliseSheDevil(effect.this)

    def savage_she_devil(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.DealDamage(effect.targets, 5, effect)
        this.RemoveThreatFromSchemes(effect.targets2, 5, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            savage_she_devil,
        ).SetPlay().SetLabel('attack', 'thwart')
        .SetTarget(Enemy)
        .SetTarget2(Scheme2)
        .SetIgnoreKeyword('Guard', 'Patrol', 'Crisis', condition=she_devil_active),
    ]
