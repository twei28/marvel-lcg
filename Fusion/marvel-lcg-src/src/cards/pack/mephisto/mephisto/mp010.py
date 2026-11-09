from . import *

# * Gluttonous Restoration — pacte BARGAIN. Peril (natif). Capacites communes : `AbilitesDuPacte`.
# « Alter-Ego Interrupt : When you make a basic recovery, restore your identity to its printed hit point value and you may discard any
# number of status cards from it. »
#
# Cartes de reference : mantis/mt001b (`WhenUnitUseBasicPower(.., powers=["REC"])` : « basic recovery » = le pouvoir de base REC, PAS le message
# `WhenUnitWouldRecovery` qui part aussi pour un soin d'evenement ; son `is_basic_recovery` est ignore par la fabrique), `HealHealth("Printed")`
# (can_health.py), dazzler/__init__ `RetirerUnStatut` (retrait d'un statut par `LoseState`).
# ⚠ Mots-pieges : « restore to its PRINTED hit point value » (pas « heal all damage » : la valeur imprimee) ; « ANY NUMBER of status cards »,
# facultatif : le joueur arrete quand il veut ; interruption AVANT le soin normal (qui ne trouve alors plus rien a soigner).


def GetAbilities() -> Sequence['Ability']:
    def restaure(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        identite = message.trigger
        identite.HealHealth("Printed", effect)
        joueur = identite.GetControlByPlayer()
        presents = [nom for nom in STATUTS_RETIRABLES if identite.HasStatus(nom)]
        if joueur is None or not presents:
            return
        joueur.ChooseAbilities(
            effect,
            *[AbilityFactory.ForChoiceAbility(
                "Discard a %s status card" % nom,
                lambda cibles, nom=nom: identite.CastTo(CanStatus).LoseState(nom, effect, 1))
              for nom in presents],
            forced=False,
            choose_x_different_options=len(presents),
        )

    return [
        *AbilitesDuPacte(),
        AbilityFactory.WhenUnitUseBasicPower(AbilityType.AlterEgoInterrupt, "You", restaure, powers=["REC"]),
    ]
