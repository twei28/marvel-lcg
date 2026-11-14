from . import *

# * Sersi — ALLIE de campagne (Identity-Specific / Campaign, n° 234). Cout 2. THW 1 / ATK 1, 3 PV.
# ETERNAL.
# Honorary.
# Action: Exhaust Sersi, deal 1 damage to her, and spend a [mental] resource -> choose a status card in
#   play. Replace that status card with a different status card.
#
# Cartes de reference :
#  - **`core/she_hulk/01027`** Focused Rage : `.SetCostFunc(CostFunc.Exhaust("This")).SetCostFunc(
#    CostFunc.TakeDamage(1, "..."))`, cout a plusieurs parties qui s'enchainent.
#  - **`card_finder/finder.py`** `has_status="Any"` : selectionne une carte qui porte DEJA un statut, pour
#    « choose a status card in play » (le choix porte sur le PERSONNAGE qui le porte, le statut lui-meme
#    n'a pas de case a cocher separee).
#  - **`card/face/component/status.py`** `DiscardStatusCard(name, effect, "All")` (retirer l'ancien) +
#    **`attribute/can_status.py`** `GainStatus(name, effect)` (poser le nouveau) : les deux API natives du
#    systeme de statuts (Tough/Stunned/Confused/Exposed/Cloaked/Dazed/Intensified).
#
# ⚠ Mots-pieges :
#  - « a DIFFERENT status card » : le nouveau statut propose au choix ne peut pas etre le meme que celui
#    retire (liste des 7 statuts moins celui qui vient d'etre retire) ;
#  - un personnage peut porter PLUSIEURS statuts a la fois (Tough + Stunned par exemple) : « a status
#    card » est singulier -> on cible UN statut precis parmi ceux portes, pas tous a la fois (choix du
#    joueur si plusieurs types coexistent) ;
#  - « spend a [mental] resource » : fait partie du cout (fleche), pas une condition d'effet.


STATUTS = ["Confused", "Stunned", "Tough", "Exposed", "Cloaked", "Dazed", "Intensified"]


def GetAbilities() -> Sequence['Ability']:

    def sersi(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        cible = effect.targets[0].CastTo(CanStatus)
        presents = [s for s in STATUTS if cible.HasStatus(s)]
        if not presents:
            return
        statut_actuel = presents[0]

        def retirer_et_poser(nouveau: str):
            def action(_cibles: Sequence['CardFace']):
                cible.components.status.DiscardStatusCard(statut_actuel, effect, "All")
                cible.GainStatus(nouveau, effect)
            return action

        joueur.ChooseAbilities(
            effect,
            *[
                AbilityFactory.ForChoiceAbility(nouveau, retirer_et_poser(nouveau))
                for nouveau in STATUTS if nouveau != statut_actuel
            ],
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            sersi,
        ).SetTarget(CardFinder(has_status="Any"))
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.TakeDamage(1, "This"))
        .SetCostFunc(CostFunc.Spend(Cost("B"))),
    ]
