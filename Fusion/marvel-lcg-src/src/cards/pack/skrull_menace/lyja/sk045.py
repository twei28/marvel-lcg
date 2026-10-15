from . import *

# Ministerial Tiara — AMELIORATION, cout 2 [wild]. ITEM.
# Interrupt: When a boost card is turned faceup, if that card has a star icon (★) in
#   the boost area, exhaust this card → draw 1 card.
#
# Cartes de reference :
#  - **`22012`** Wraith / **`16158`** : `WhenBoostCardTurnedFaceUp(Interrupt, ...)`, la
#    fenetre « boost card turned faceup » (boost.py).
#  - **`has_boost_icon.py:50`** `boost_star` : l'etoile de boost = une capacite
#    `AbilityType.Boost` sur la carte (le moteur l'exprime ainsi pour toute carte).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « has a STAR icon in the boost area » : l'etoile ★ du champ de boost = la carte a
#    un « ★ Boost: » ; une icone de boost ordinaire (Y) ne compte pas. Les evenements
#    de Lyja portent l'etoile (decision du 15/10/2026).
#  - « Interrupt » : avant que l'effet de boost se resolve (la fenetre `TurnedFaceUp`
#    precede `WhenCardBecomeBoost`).
#  - « exhaust this card » : COUT (devant la fleche), une fois par redressement.
#  - « draw 1 card » : le joueur qui detient la Tiare (l'initiateur).


def GetAbilities() -> Sequence['Ability']:

    def a_une_etoile(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> bool:
        return bool(message.trigger.effect.Find(type=AbilityType.Boost))

    def piocher(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        effect.GetInitiator().DrawUp(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenBoostCardTurnedFaceUp(
            AbilityType.Interrupt,
            None,
            piocher,
            conditions=[a_une_etoile],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
