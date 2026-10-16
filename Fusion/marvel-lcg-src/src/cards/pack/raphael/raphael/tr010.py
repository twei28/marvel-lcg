from . import *

# Gekido — AMELIORATION, cout 2, [physical]. CONDITION.
# Hero Action: Exhaust Gekido -> choose:
#   - Place 1 rage counter on Raphael.
#   - Heal 1 damage from Raphael.
#
# Valide en jeu : cas `tools/cas/tmnt_raphael.py` (voir .planning/todos/2026-10-16-raphael-gabarits-processus-carte.md).
#
# CARTES DE REFERENCE
#  - `ho010` / `sf007` : AMELIORATION sans « Attach to » = `CanPlayThisUpgradeCard()`
#    (elle s'attache a l'identite) + `WhenInYourPlayTurn(HeroAction)` +
#    `CostFunc.Exhaust("This")`.
#  - `30024` / `ma015` : « choose: A / B » = `ChooseAbilities(effect,
#    ForChoiceAbility(...), ForChoiceAbility(...))`. Le pilote du harnais prend
#    la PREMIERE branche (rage) : le soin n'est atteignable qu'avec
#    `preferer_option` en phase C.
#  - `42018` : `this.HealthUnits(cibles, n, effect)` pour le soin.
#
# TEXTE CONTRE CODE
#  ⚠ « Exhaust Gekido -> choose » : le choix est APRES la fleche, l'inclinaison
#    est le seul cout. Un seul choix, pas les deux.
#  ⚠ « Place 1 rage counter on Raphael » : PAS de « (to a maximum of 3) »
#    imprime (decision du 15/10/2026) : `plafonne=False`.
#  ⚠ « RAPHAEL » = l'identite (decision du 15/10/2026) ; une Hero Action
#    impose de toute facon la forme heros.
#  Pas de limite imprimee : seule l'inclinaison borne l'usage (une fois par
#  redressement).


def GetAbilities() -> Sequence['Ability']:

    def gekido(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        heros = IdentiteDuJoueur(effect, joueur)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Gekido: place 1 rage counter on Raphael",
                lambda targets:
                    PlacerRage(effect, joueur, plafonne=False),
            ),
            AbilityFactory.ForChoiceAbility(
                "Gekido: heal 1 damage from Raphael",
                lambda targets:
                    this.HealthUnits([heros], 1, effect) if heros is not None else None,
            ),
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            gekido,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
