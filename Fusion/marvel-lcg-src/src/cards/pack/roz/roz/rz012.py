from . import *

# Hand-to-Hand — EVENEMENT, cout 0, [physical] (x2 dans le deck). SKILL.
# Response: After a minion or side scheme enters play, resolve the "Special" ability on 1 [[WAKANDA]] card
#   you control.
#
# CARTES DE REFERENCE (PROCESSUS-CARTE etape 2)
#  - Response d'evenement : `01024` One-Two Punch (`AfterUnitMakeBasicAttack(Response, ...).SetPlay().SetLabel()`).
#  - « After a minion or side scheme enters play » : `27189a` Wrist Navigators
#    (`AfterCardEnterPlay(..., CardFinder(card_type=Minion|SchemeSide2), op)`).
#  - Special : `51025` / `51001a` (`joueur.ResolveSpecialAbility(effect.targets, effect)`).
#
# MOTS-PIEGES
#  - « Response » SANS « Hero » : jouable par n'importe quel joueur, hors tour comme en tour.
#  - « a minion OR SIDE scheme » : un sbire ou une manigance ANNEXE (jamais le complot principal).
#  - « 1 WAKANDA card you control » : n'importe quel type de carte a Special (heros, amelioration, soutien, allie).
def GetAbilities() -> Sequence['Ability']:

    def corps_a_corps(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None:
            joueur.ResolveSpecialAbility(effect.targets, effect)

    return [
        CarteWakandaSousControle(
            AbilityFactory.AfterCardEnterPlay(
                AbilityType.Response,
                CardFinder(card_type=Minion|SchemeSide2),
                corps_a_corps,
            ).SetPlay().SetLabel(),
        ),
    ]
