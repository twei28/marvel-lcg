from . import *
# * Skillful Execution (Basic, manigance annexe de JOUEUR, cout 0 [energy], menace 2 par joueur). Victory 0.
# When Defeated: Each player may search their deck and discard pile for a SKILL card and add it to their hand. Reduce the cost of each
# SKILL played this phase by 1.
#
# Cartes de reference : 59028 Evaluate Threat / ul040 Weasel In (`CanPlayThisSchemeCard().SetPlay()` + `WhenSchemeBeDefeated(WhenDefeated,
# "This", op)` + `Players.ForEachPlayer`) ; 36018 (`ReduceCostToPlayFaceWhen(CardFinder(...), N, "You")`) ; `RegisterTemp(..,
# unregister_after_exec=False, until_phase_end=True)` pour la duree.
# ⚠ « each player MAY search » (facultatif) ; « the cost of EACH SKILL played this phase » : TOUTES les cartes SKILL jouees pendant la phase,
# de TOUS les joueurs (pas seulement celle qu'on vient de chercher). La reduction est posee sur l'identite de chaque joueur (la manigance
# vaincue part en vitrine, hors jeu).
def GetAbilities() -> Sequence['Ability']:
    def execution(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        def action(joueur: 'Player') -> None:
            face = Search.PlayerCard(effect, joueur, include_player_deck=True, include_discard_pile=True, may=True, trait="SKILL")
            if face:
                Faces.AddToHand([face], joueur, effect)
            joueur.GetIdentity().effect.RegisterTemp(
                AbilityFactory.ReduceCostToPlayFaceWhen(CardFinder(trait="SKILL"), 1, "You"),
                unregister_after_exec=False,
                until_phase_end=True,
            )
        Players.ForEachPlayer(effect, action)
    return [
        AbilityFactory.CanPlayThisSchemeCard().SetPlay(),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            execution,
        ),
    ]
