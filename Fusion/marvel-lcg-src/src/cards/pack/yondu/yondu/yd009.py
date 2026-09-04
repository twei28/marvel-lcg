from . import *

# Invest — amelioration signature, x1 (n/15 = 12). ITEM. TACTIC.
# Cout 2, ressource [physical].
# Hero Action: Exhaust Invest and spend 2 or more resources from your hand ->
#   if the number of resources spent this way was:
#   • 2 — Attach the Yaka Arrow upgrade to an enemy or to your identity.
#   • 3 — Ready Yondu and the Tahlei upgrade.
#   • 4 or more — Draw 5 cards.
#
# Cartes de reference :
#  - `32179` Ferocious Attack / `40122a` * Juggernaut's Helmet / `as002b` pour
#    `SetCost(Cost("2"))` sur une capacite deja en jeu.
#  - **`14006`** Speed Cyclone / `as017` / `yd006` pour `effect.GetCostX()`,
#    qui compte le SURPAIEMENT. ⚠ Dans les cas de test, `surpayer: True` est
#    OBLIGATOIRE, sinon X vaut 0 et seule la branche a 2 tombe.
#  - `AttacherLaFleche` (helper du set), `Faces.ReadyAll`, `DrawUp`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « spend **2 OR MORE** resources » : le minimum est 2, le reste est du
#    surpaiement. Le total depense vaut donc `2 + effect.GetCostX()`, et c'est
#    LUI qu'on compare aux trois seuils — jamais le seul X.
#  - Les trois branches sont EXCLUSIVES et fixees par le total : 2, 3, ou
#    4-et-plus. Ce n'est PAS un cumul, et ce n'est pas un choix : le joueur
#    decide en payant, pas apres.
#  - « **4 or more** » : la derniere branche est ouverte vers le haut, les
#    deux premieres sont exactes.
#  - « Exhaust Invest **and** spend » : le cout a DEUX parties, et oublier
#    l'une des deux est le piege `wd005`.
#  - « ready Yondu **and the Tahlei upgrade** » : les deux, et Tahlei peut ne
#    pas etre en jeu — `Faces.ReadyAll` fait le tri.
#  - Branche 2 : deux destinations seulement (un ennemi ou l'identite), la
#    main n'en est PAS une — comme `yd006`, contrairement a `yd011`/`yd012`.
#  - « **Hero** Action » : rien en forme civile.


def GetAbilities() -> Sequence['Ability']:

    def invest(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        # « 2 or more » : le cout imprime est 2, le reste est du surpaiement.
        total = 2 + max(0, effect.GetCostX())

        if total >= 4:
            joueur.DrawUp(5, effect)
            return

        if total == 3:
            heros = joueur.GetIdentity()
            a_redresser = [f for f in (heros, LaTahlei(effect)) if f is not None]
            Faces.ReadyAll(a_redresser, effect)
            return

        # total == 2
        if LaFleche(effect) is None:
            return
        identite = joueur.GetIdentity()
        ennemis = EnnemisEnJeu(effect)
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Attach Yaka Arrow to an enemy",
                lambda cibles: AttacherLaFleche(effect, cibles[0] if cibles else None),
                condition=bool(ennemis),
            ).SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility(
                "Attach Yaka Arrow to your identity",
                lambda cibles: AttacherLaFleche(effect, identite),
                condition=identite is not None,
            ),
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            invest,
        ).SetCost(Cost("2"))
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
