from . import *

# Faulty Creation — OBLIGATION (set « Venus »). Boost 2, icone Hazard imprimee.
# Give to the Bonnie player.
# You may flip to alter-ego form.
# Alter-Ego Action: Exhaust Bonnie -> remove Faulty Creation from the game.
#
# CARTES DE REFERENCE
#  - `01165` Eviction Notice : `WhenThisObligationGiveToYou(op)` +
#    `YouMayFlipToYourAlterEgoForm(player, effect)`.
#  - `tm013` All Alone (pack michelangelo) : `PlayerActionToRemoveThisFromGame(AlterEgoAction)
#    .SetCostFunc(CostFunc.Exhaust("YourIdentity"))`.
#
# TEXTE CONTRE CODE
#  ⚠ « You MAY flip » : facultatif (le texte ne dit pas « flip » tout court, contrairement a
#    `tm013`/`tr013`), donc `YouMayFlipToYourAlterEgoForm`, un choix avec bouton Passer ; rien
#    si le joueur est deja en alter-ego.
#  ⚠ « Exhaust BONNIE -> » : l'identite en forme alter-ego (Alter-Ego Action), seul cout.
#  ⚠ « remove FROM THE GAME » (pas defausse) : `PlayerActionToRemoveThisFromGame`.
#  ⚠ Icone Hazard (carte inclinee + croix) : `desc.Hazard = "1"`, lue nativement
#    (`mots-cles/hazard.md`), verifiee par decoupe contre `01107` Breakin' & Takin'.
#  Aucune limite imprimee ; l'obligation reste en jeu tant qu'on ne l'a pas retiree.


def GetAbilities() -> Sequence['Ability']:

    def faulty_creation(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this)
        joueur = message.GetGaveToPlayer()
        if joueur is not None:
            YouMayFlipToYourAlterEgoForm(joueur, effect)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            faulty_creation,
        ),
        AbilityFactory.PlayerActionToRemoveThisFromGame(
            AbilityType.AlterEgoAction,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
