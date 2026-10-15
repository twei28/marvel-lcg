from . import *

# * Stealing For Good — COMPLOT ANNEXE DE JOUEUR (Justice / Campaign, n° 276). Cout 0, menace de depart 2.
# Victory 0.
# When Defeated: The player who defeated this scheme may search their deck and discard pile for an upgrade
#   and add it to their hand. (Shuffle.) Then, they remove threat from a scheme equal to that upgrade's
#   printed cost.
#
# Cartes de reference :
#  - **`hd010`** Trapped : `Search.PlayerCard(include_player_deck=True, include_discard_pile=True, may=True,
#    card_type=...)` puis `player.GainCard(face, effect)` ; « the player who defeated » =
#    `message.GetDefeatingPlayer()`.
#  - **`jubilee/47021`** Multitalented : « remove threat from a scheme » = `this.RemoveThreatFromSchemes(cibles, n,
#    effect)` avec la cible choisie par `ChooseAbilities(... .SetTarget(Scheme2))`.
#
# ⚠ Mots-pieges :
#  - « THEN, they remove threat » : seulement si une amelioration a ete trouvee ET ajoutee a la main ; la
#    valeur est le cout IMPRIME de CETTE amelioration (`printed_cost.val`, pas le cout paye) ;
#  - « from A scheme » : UNE manigance au choix du vainqueur (le complot principal compris, sous reserve de
#    la Crise) ; cout imprime 0 : rien a retirer ;
#  - « may search » : facultatif ; « add it to their HAND » (pas en jeu).


def GetAbilities() -> Sequence['Ability']:

    def recompense(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        vainqueur = message.GetDefeatingPlayer()
        if vainqueur is None:
            return
        face = Search.PlayerCard(
            effect,
            vainqueur,
            include_player_deck=True,
            include_discard_pile=True,
            card_type=Upgrade,
            may=True,
        )
        if face is None:
            return
        vainqueur.GainCard(face, effect)
        n = face.printed_cost.val
        if n <= 0:
            return
        vainqueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove threat from a scheme equal to that upgrade's printed cost",
                lambda targets: this.RemoveThreatFromSchemes(targets, n, effect),
            ).SetTarget(Scheme2),
        )

    return [
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            recompense,
            has_defeating_player=True,
        ),
    ]
