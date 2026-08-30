from . import *

# Duck Hunt — trahison nemesis, Boost 2
# When Revealed (Alter-Ego): The villain schemes. If there are side schemes in
#   play, divide and place threat from this activation among them instead.
# When Revealed (Hero): Give the villain a tough status card. If you cannot,
#   heal 3 damage from it instead.
#
# Structure des deux branches : modele exact core/rhino/01106.py (Stampede) et
# ok023 (War Drumming), `AbilityFactory.WhenThisRevealed("Alter-Ego"|"Hero",
# ...)` — DEUX abilities distinctes, pas un `if` sur la forme.
#
# ---- Branche ALTER-EGO -----------------------------------------------------
# « The villain schemes » : `villain.CastTo(Enemy).BasicSchemes(effect)`
# (can_scheme.py:166), modele ok021 (Malice, « Malice schemes ») — la seule
# facon de declencher une manigance de base HORS activation normale, avec
# ses cartes boost.
# « divide and place threat from this activation among them INSTEAD » : le
# pipeline `SchemesInternal` n'accepte QU'UNE cible de manigance
# (`Message.GettingEnemySchemeTarget`, can_scheme.py:68-72) — impossible d'y
# repartir la menace. On intercepte donc le placement lui-meme, modele exact
# aos/nick_fury/50035b.py (Stealth) : une interruption TEMPORAIRE
# `WhenSchemeWouldPlaceThreat` enregistree juste avant l'activation
# (`this.effect.RegisterTemp(..., unregister_after_exec=True)`), qui annule le
# placement sur le complot principal (`message.PreventThreat("All", effect)`,
# piege `instead` : la menace PART d'un endroit et ARRIVE ailleurs, elle n'est
# pas dupliquee) puis la repartit une par une entre les manigances annexes.
# La repartition point par point via un `ChooseAbilities` repete est le
# rendu du depot pour « divided as you choose » (modele ok008 Spear Thrust,
# qui repete exactement ce motif pour ses degats divises).
# Un drapeau `deja_redirige` empeche la re-entrance : les menaces que nous
# posons ensuite sur les manigances annexes ne doivent pas re-declencher
# l'interruption.
# `which_scheme=MainScheme` : seul le placement sur le complot PRINCIPAL est
# detourne (c'est la cible par defaut d'une manigance de vilain).
#
# ---- Branche HEROS ---------------------------------------------------------
# « Give the villain a tough status card » : `Faces.GiveStatus([villain],
# "Tough", effect)` (modele ok006/trors 04017). « If you CANNOT » = le vilain
# porte deja Tenace : verifie par `CanStatus.HasStatus("Tough")` AVANT, pas
# apres un echec silencieux. « heal 3 damage from IT » : le vilain lui-meme
# (piege `that <nom>`), `this.HealthUnits([villain], 3, effect)` (modele
# il002/albert ab012).


def GetAbilities() -> Sequence['Ability']:

    def duck_hunt_alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        villain = Worlds.FindVillain(effect)
        if villain is None:
            return

        joueur = message.GetToPlayer()
        manigances = list(Worlds.GetSideSchemes(effect))

        if not manigances or joueur is None:
            villain.CastTo(Enemy).BasicSchemes(effect)
            return

        deja_redirige = [False]

        def rediriger(eff: 'Effect', msg: 'Message.WhenSchemeWouldPlaceThreat') -> None:
            if deja_redirige[0]:
                return
            deja_redirige[0] = True

            valeur = msg.value
            msg.PreventThreat("All", eff)
            if valeur <= 0:
                return

            def poser(targets: Sequence['CardFace']) -> None:
                if targets:
                    this.PlaceThreatOnSchemes(targets, 1, eff)

            for _ in range(valeur):
                joueur.ChooseAbilities(
                    eff,
                    AbilityFactory.ForChoiceAbility(
                        "Place 1 threat on a side scheme",
                        poser,
                    ).SetTarget(SchemeSide2),
                )

        this.effect.RegisterTemp(
            AbilityFactory.WhenSchemeWouldPlaceThreat(
                AbilityType.Temp0,
                MainScheme,
                rediriger,
            ),
            unregister_after_exec=True,
        )

        villain.CastTo(Enemy).BasicSchemes(effect)

    def duck_hunt_hero(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(message)

        villain = Worlds.FindVillain(effect)
        if villain is None:
            return

        if villain.CastTo(CanStatus).HasStatus("Tough"):
            this.HealthUnits([villain], 3, effect)
        else:
            Faces.GiveStatus([villain], "Tough", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            "Alter-Ego",
            duck_hunt_alter_ego,
        ),
        AbilityFactory.WhenThisRevealed(
            "Hero",
            duck_hunt_hero,
        ),
    ]
