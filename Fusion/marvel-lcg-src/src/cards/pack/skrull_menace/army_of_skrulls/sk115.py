from . import *

# Hijacked — COMPLOT ANNEXE x2 (Army of Skrulls). Menace 4, Hinder 1[per_hero],
# Crisis, ★.
# When Revealed: Search your deck, discard pile and hand for an ally and place
#   it beneath this scheme.
# When Defeated: Put the ally beneath this scheme into play under its owner's
#   control.
# ★ Boost: Reveal this card.
#
# Cartes de reference : **`04122`** Hydra Prison (meme recherche, `PlaceCardHere`,
# `GetPlacedCardArea`) ; **`16140`** (boost `RevealThisCard`).
# ⚠ « YOUR deck, discard pile and HAND » : le joueur qui revele ; « an ally »
# (au choix, n'importe lequel) ; « into PLAY under its OWNER's control » (pas
# en main comme Hydra Prison). Le deck du joueur est melange apres la
# recherche (natif SearchForCard). Hinder/Crisis : desc, natif.


def GetAbilities() -> Sequence['Ability']:

    def detourne(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        face = Search.SearchForCard(
            effect,
            message.GetToPlayer(),
            include_player_deck=True,
            include_player_discard_pile=True,
            include_player_hand_cards=True,
            card_type=Ally,
        )
        if face:
            this.PlaceCardHere(face, True, effect)

    def libere(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(message)
        allies = list(this.GetPlacedCardArea().Get())
        Faces.MoveAllToProcessingArea(allies, effect)
        for allie in allies:
            allie.PutIntoPlay(allie.GetOwnerPlayer(), effect)

    return [
        AbilityFactory.WhenThisRevealed(None, detourne),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", libere),
        AbilityFactory.WhenCardBecomeBoost("This", RevealThisCard),
    ]
