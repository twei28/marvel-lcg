from . import *

# * Buddy Training Program — COMPLOT ANNEXE DE JOUEUR (Protection / Campaign, n° 270). Menace de depart 2.
# Cout X (X = le stade du mechant : le coin haut droit imprime « X », decision utilisateur du 14/10/2026).
# Victory 0.
# X is equal to the villain's stage number.
# When Defeated: The player who defeated this scheme may give up to X friendly characters a tough status card.
#
# Cartes de reference :
#  - **`hd011`** In a World : complot annexe JOUEUR « Victory 0 » + « When Defeated » + « give each player a
#    tough status card » (`Faces.GiveStatus(..., "Tough", effect)`), et le joueur qui l'a vaincu =
#    `message.GetDefeatingPlayer()` (`has_defeating_player=True`).
#  - **`21013`** White Tiger : « X is equal to the villain's stage number » = `villain.printed_stage`.
#  - **`ar010`** (`IncreaseResourceCostToPlay(which_card, n, who)`) et `ReduceCostToPlayThis` (son miroir pour « This ») :
#    un cout dynamique propre a la carte = `IncreaseResourceCostToPlay("This", fn, "AnyPlayer")` ; `fn(effect)` est relu
#    a CHAQUE calcul de cout. Le desc porte Cost 0 ; la valeur imprimee « X » est ajoutee par le script (mesure :
#    `cc_cout`, cas `sk270 ... cout X = stade du mechant`).
#  - **`ss004`** Precise Force / RECETTES §6 : « up to N » = `range=(0, N)` ET UNIQUEMENT pour un « up to ».
#
# ⚠ Mots-pieges :
#  - « X » designe UN nombre unique : le stade du MECHANT (cout ET plafond de la recompense) ; relu a chaque
#    usage (le mechant peut avoir change de stade entre le jeu et la defaite) ;
#  - « The player who DEFEATED this scheme » (pas « each player ») ; « MAY » (la recompense est facultative) ;
#  - « up to X FRIENDLY characters » : heros et allies de TOUS les joueurs (classe Friend), 0 a X ;
#  - « a tough status card » : un personnage deja Tough n'en recoit pas de seconde (`canbe_tough`).


def StadeDuMechant(effect: 'Effect') -> int:
    mechant = Worlds.FindVillain(effect)
    return mechant.printed_stage if mechant is not None else 0


def GetAbilities() -> Sequence['Ability']:

    def recompense(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this)
        vainqueur = message.GetDefeatingPlayer()
        x = StadeDuMechant(effect)
        if vainqueur is None or x <= 0:
            return
        vainqueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Give up to X friendly characters a tough status card",
                lambda targets: Faces.GiveStatus(targets, "Tough", effect),
            ).SetTarget(Friend, range=(0, x), canbe_tough=True),
        )

    return [
        AbilityFactory.IncreaseResourceCostToPlay("This", StadeDuMechant, "AnyPlayer"),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            recompense,
            has_defeating_player=True,
        ),
    ]
