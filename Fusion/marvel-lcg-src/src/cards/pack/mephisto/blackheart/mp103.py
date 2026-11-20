from . import *

# * Black-Hearted — pacte BARGAIN (modulaire Blackheart). Boost 3, Peril (natifs, `desc`). When Revealed : meme texte que les sept pactes (`AbilitesDuPacte`).
# Interrupt : When the villain phase begins, if this is the only BARGAIN attachment you control, look at the top 3 cards of the encounter deck. Put them back in
# any order.
# Response : After your turn begins, discard this card -> find Blackheart and reveal him. (If he is already in play, he engages you.) Blackheart activates against you.
# ⚠ Sa Response n'est PAS celle des autres pactes (pas de Mephisto, pas d'icones de boost) : `reponse_propre`.
#
# Cartes de reference : tmnt_aspect_justice/uj016 (`LookAtDeck("EncounterDeck", 3)` + `PlaceOnTopInAnyOrder`), nt011 (`WhenVillainPhaseBegin`), `Search.EncounterCard`
# + `Reveal` (find), `Minion.EngagePlayer`, `Enemy.DoActivate`.
# ⚠ Mots-pieges : « the ONLY BARGAIN attachment YOU control » (un seul pacte, le sien) ; « find Blackheart » : deck, defausse (et zone mise de cote) ; « already in play,
# he engages YOU » ; « Blackheart activates against you » dans les deux cas (revele ou deja la).


def GetAbilities() -> Sequence['Ability']:
    def le_seul_pacte(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> bool:
        porteur = effect.this.CastTo(Attachment).GetBindFace()
        joueur = porteur.GetControlByPlayer() if porteur is not None else None
        return joueur is not None and len(PactsDuJoueur(joueur)) == 1

    def regarde_trois(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        Unused(message)
        joueur = effect.this.CastTo(Attachment).GetBindFace().GetControlByPlayer()
        faces = joueur.LookAtDeck("EncounterDeck", 3, effect)
        if len(faces) > 1:
            joueur.PlaceOnTopInAnyOrder(list(faces), effect)

    def reponse(effect: 'Effect', message: 'Message.AfterPlayerTurnBegin') -> None:
        joueur = message.to_player
        blackheart = Worlds.FindCardOnField(effect, name="Blackheart", card_type=Minion)
        if blackheart is None:
            trouve = Search.EncounterCard(effect, joueur, include_discard_pile=True, include_set_aside=True, name="Blackheart", card_type=Minion)
            if trouve is not None:
                trouve.Reveal(joueur, effect)
            blackheart = Worlds.FindCardOnField(effect, name="Blackheart", card_type=Minion)
        else:
            blackheart.CastTo(Minion).EngagePlayer(joueur, effect)
        if blackheart is not None:
            blackheart.CastTo(Minion).DoActivate(joueur, effect)

    return [
        *AbilitesDuPacte(reponse),
        AbilityFactory.WhenVillainPhaseBegin(AbilityType.Interrupt, regarde_trois, conditions=[le_seul_pacte]),
    ]
