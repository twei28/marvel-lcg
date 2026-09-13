from . import *

# Targeting Protocol — Amelioration 1 [mental], classe Hero. TECH.
# Hero Action: Exhaust this card → expose 2 enemies, or remove threat from a
#   scheme equal to the number of exposed status cards in play (to a maximum
#   of 3).
#
# Cartes de reference :
#  - `st002a` Head (Intact) pour l'exposition et sa fourchette `("Zero", 2)`.
#  - `dz037` / `aa005` pour le choix entre deux branches.
#  - `03011` Falcon pour un retrait de menace dont le montant se calcule au
#    moment de la selection.
#
# ⚠ SEULE CARTE DU DECK SANS COUT ADDITIONNEL, et seule amelioration TECH : la
# manigance annexe Rogue Asset (`st016`) lui donne le trait HACKED, ce qui la
# rend vulnerable a `st017` Disabled et `st018` Viral Assault.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « remove threat from **a** scheme » : UN complot, principal ou annexe.
#    Rien a repartir, contrairement a `st007` qui dit « from among schemes ».
#  - « equal to the number of exposed status cards **in play** (to a maximum of
#    3) » : tout le plateau, plafonne a 3. Le compte se lit a la resolution.
#  - Si aucun Exposed n'est en jeu, la seconde branche retire zero menace :
#    elle reste proposee, et c'est bien ce que dit la carte.
#  - Aucune mention de Crise : pas d'`ignore_crisis`.


def GetAbilities() -> Sequence['Ability']:

    def targeting_protocol(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        joueur = effect.GetInitiator()

        def exposer(cibles: Sequence['CardFace'], e: 'Effect') -> None:
            Exposer(cibles, e)

        def deminer(cibles: Sequence['CardFace'], e: 'Effect') -> None:
            this.RemoveThreatFromSchemes(cibles, min(3, ExposedEnJeu(e)), e)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility3("Expose 2 enemies", exposer)
            .SetTarget(Enemy, range=("Zero", 2)),
            AbilityFactory.ForChoiceAbility3(
                "Remove threat from a scheme", deminer)
            .SetTarget(Scheme2),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            targeting_protocol,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
