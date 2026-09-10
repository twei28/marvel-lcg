from . import *

# Seige — EVENEMENT, cout 4, RES [wild]. ATTACK.
# ⚠ « Seige » est la COQUILLE IMPRIMEE de l'auteur pour « Siege ». On porte ce
# qui est imprime : c'est le NOM de la carte.
# Hero Action (attack): Exhaust Iron Patriot and discard any number of
#   REGISTERED allies in play. Deal X damage to an enemy (to a maximum of 15),
#   where X is the combined ATK of those discarded characters. This attack
#   gains overkill.
#
# CARTE DE REFERENCE
#  - `29017` Go All Out : « Exhaust your hero » en COUT, par
#    `SetCostFunc(CostFunc.Exhaust("YourHero"))`.
#  - `01021` Gamma Slam : « Deal X damage ... (to a maximum of N) ».
#
# TEXTE CONTRE CODE
#  ⚠ Le sacrifice est le COUT et les degats l'EFFET, mais les deux sont lies :
#    on doit lire l'ATQ des allies AVANT de les defausser, sinon la somme vaut
#    zero. C'est le piege de la carte.
#  ⚠ « ANY NUMBER » : zero est permis. La carte devient alors une attaque a 0,
#    ce qui est mauvais mais legal — on ne l'interdit pas.
#  ⚠ « to a maximum of 15 » : plafond dur, pas une suggestion.
#  ⚠ « gains OVERKILL » : le surplus passe au complot principal.


# ⚠ « This attack gains OVERKILL » se passe par `property=AttackProperty(
# overkill=True)`, JAMAIS par un `overkill=True` a la racine de `DealDamage` —
# ce mot-cle n'existe pas dans sa signature (card_face.py:643) et la carte
# levait `TypeError` en pleine resolution, apres avoir DEJA defausse les
# allies. Mesure du 09/09/2026.


def GetAbilities() -> Sequence['Ability']:

    MAXIMUM = 15

    def siege(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        sacrifies = [c for c in (effect.targets2 or []) if c is not None]
        # ⚠ L'ATQ se lit AVANT la defausse.
        degats = min(MAXIMUM, sum(c.attack for c in sacrifies))
        Faces.DiscardAll(sacrifies, effect)
        if degats > 0:
            this.DealDamage(effect.targets, degats, effect,
                            property=AttackProperty(overkill=True))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            siege,
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("YourHero"))
        .SetTarget(Enemy)
        .SetTarget2(CardFinder(trait=TRAIT_REGISTERED, card_type=Ally),
                    is_optional=True),
    ]
