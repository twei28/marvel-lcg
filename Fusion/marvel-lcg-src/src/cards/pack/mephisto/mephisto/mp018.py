from . import *

# Exposing Intentions — MANIGANCE ANNEXE. Boost 3, menace de depart 3[per_hero] (natifs, `desc`).
# Forced Interrupt : When a card is put into Damnation from a player's deck, put 1 additional card into Damnation from that player's deck.
# When Defeated : Each player looks at each card in Damnation, then shuffles 1[per_hero] card looked at this way back into their owner's deck.
# Shuffle the Damnation area.
#
# Cartes de reference : mp007a (`WhenCardWouldMoveToArea` sur le deplacement), `JoueurDontUneCarteVaEnDamnation` (les deux chemins),
# `RegarderEtRemelanger` (choix dans la Damnation), `MettreEnDamnation`.
# ⚠ Mots-pieges : « ONE additional card » : la carte en plus ne relance PAS l'interruption (sinon le deck se viderait : garde `en_cours`) ;
# « from THAT player's deck » : le deck du joueur dont la carte part, pas celui d'un autre ; « each card looked at ... 1[per_hero] » : par joueur,
# 1 x nombre de joueurs cartes ; « Shuffle the Damnation area » : chaque pile est melangee a la fin.


def GetAbilities() -> Sequence['Ability']:
    def une_en_plus(effect: 'Effect', message: 'Message.WhenCardWouldMoveToArea') -> None:
        this = effect.this
        if getattr(this, "_mp018_en_cours", False):
            return
        joueur = JoueurDontUneCarteVaEnDamnation(effect, message)
        if joueur is None:
            return
        suivantes = [c for c in joueur.player_deck.GetTops(2) if c is not message.trigger]
        if not suivantes:
            return
        this._mp018_en_cours = True
        try:
            Faces.MoveAllTo(suivantes[:1], joueur.damnation, effect)
            VerifierDamnation(effect)
        finally:
            this._mp018_en_cours = False

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        Unused(message)
        for joueur in JoueursDansLOrdre(effect):
            RegarderEtRemelanger(effect, joueur, NombreDeJoueurs(effect))
        for joueur in Worlds.GetPlayers(effect):
            joueur.damnation.Shuffle()

    return [
        AbilityFactory.WhenCardWouldMoveToArea(
            AbilityType.ForcedInterrupt, None, une_en_plus,
            conditions=[lambda effect, message: JoueurDontUneCarteVaEnDamnation(effect, message) is not None],
        ),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
