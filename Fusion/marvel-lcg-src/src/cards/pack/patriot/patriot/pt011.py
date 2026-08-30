from . import *

# On Your Feet — AMELIORATION signature, custom « CptScorp »
# Cout 3, ressource [mental], aucun trait.
#
# Hero Action: Exhaust On Your Feet -> choose: ready an ally or heal 1 damage
#   from an ally.
#
# ---------------------------------------------------------------------------
# CARTE DE REFERENCE : `60044` Choreography pour le « choose: A or B » rendu
# par un `player.ChooseAbilities` a deux branches, chacune portant sa propre
# cible ; `iw003` Central City Estate pour le couple
# `WhenInYourPlayTurn(...).SetCostFunc(CostFunc.Exhaust("This"))` d'une carte
# posee en jeu.
#
# ---------------------------------------------------------------------------
# LA FLECHE EST UN COUT -> UN EFFET
#
# Cout = « Exhaust On Your Feet » -> `CostFunc.Exhaust("This")`. Une
# amelioration deja inclinee n'est pas proposee. Cout impayable = rien ne se
# passe.
#
# ---------------------------------------------------------------------------
# « AN ALLY », PAS « AN ALLY YOU CONTROL »
#
# Le texte n'imprime PAS « you control » (contrairement a pt003, pt005 et
# pt009) : la cible est donc `Ally`, c'est-a-dire TOUS les allies en jeu, y
# compris ceux d'un autre joueur (`Worlds.GetOnFieldAllies`). Mot-piege
# `you control` du PROCESSUS-CARTE §5, applique dans l'autre sens : on
# n'ajoute pas une restriction qui n'est pas ecrite. En solo la difference
# est nulle.
#
# Chaque branche filtre ses propres cibles legales, ce qui evite les choix
# vides :
#   - « ready an ally » -> `canbe_ready=True` (un allie deja pret n'est pas
#     proposable) ;
#   - « heal 1 damage from an ally » -> `canbe_heal=True` (un allie intact
#     n'est pas proposable).
# Si AUCUNE des deux branches n'a de cible, le `ChooseAbilities` ne propose
# rien : l'action aura incline la carte pour rien, ce qui est la lettre du
# texte (le cout n'est pas conditionne a l'existence d'une cible).
#
# Le soin part de l'amelioration (`this.HealthUnits`), qui route vers
# l'identite du controleur comme toute carte joueur.
#
# ⚠ PAS de `SetPlay()` (piege `66006`/`66007`).


def GetAbilities() -> Sequence['Ability']:

    def on_your_feet(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Ready an ally",
                lambda targets:
                    Faces.ReadyAll(list(targets), effect),
            ).SetTarget(Ally, range=(1, 1), canbe_ready=True),
            AbilityFactory.ForChoiceAbility(
                "Heal 1 damage from an ally",
                lambda targets:
                    this.HealthUnits(list(targets), 1, effect),
            ).SetTarget(Ally, range=(1, 1), canbe_heal=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            on_your_feet,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
