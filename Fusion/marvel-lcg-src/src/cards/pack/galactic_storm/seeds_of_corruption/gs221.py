from . import *

# Whisper in the Mind — TRAITRISE (Seeds of Corruption), x2. ★ + 1 icone de boost.
# When Revealed: Find a copy of your obligation and reveal it. If your obligation was not revealed this way,
#   this card gains surge.
# ★ Boost: If your obligation is in the victory display or if it was removed from the game, shuffle it into
#   the encounter deck.
#
# Cartes de reference :
#  - **`sm/down_to_earth/27135`** Loose Ends : `Search.SearchForCard(effect, joueur, include_encounter_deck=
#    True, include_encounter_discard_pile=True, include_set_aside=True, ..., card_type=Obligation,
#    obligation_give_to=joueur)` puis `face.Reveal(joueur, effect)`, sinon `ThisCardGainSurge(effect)`.
#  - « Find » (livret Galactic Storm p.4) : chercher dans chaque zone ou la carte peut se trouver (« play area,
#    set-aside area, player deck, discard pile, encounter deck, etc. »), SANS regarder les cartes rencontre
#    distribuees face cachee. Lecture retenue (question Q4 du lot GS-8) : deck rencontre, defausse rencontre,
#    zone mise de cote ; la pile de victoire et la zone retiree du jeu ne sont PAS fouillees (c'est le role du
#    ★ Boost de les rendre au deck).
#  - Boost : `WhenCardBecomeBoost("This", op)` (an013) ; `Worlds.VictoryDisplay(effect)` ; zone retiree du jeu :
#    `Search.SearchForCard(..., include_removed_area=True)` (27135) ; `Faces.ShuffleAllTo(..., "EncounterDeck")`.
#
# ⚠ Mots-pieges : « YOUR obligation » (celle de l'identite du joueur qui revele, `obligation_give_to`) ;
# « a COPY » (une seule) ; « If ... NOT revealed this way, this card gains SURGE » ; Boost : « you » = le joueur
# active ; « IN the victory display OR REMOVED from the game » (deux zones) ; « shuffle it INTO the encounter
# deck ».


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        face = Search.SearchForCard(
            effect,
            joueur,
            include_encounter_deck=True,
            include_encounter_discard_pile=True,
            include_set_aside=True,
            card_type=Obligation,
            obligation_give_to=joueur,
        )
        if face is not None:
            face.Reveal(joueur, effect)
        else:
            ThisCardGainSurge(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        sienne = CardFinder(card_type=Obligation, obligation_give_to=joueur)
        trouvees = list(Worlds.VictoryDisplay(effect).FindCards(sienne))
        if not trouvees:
            trouvees = list(effect.world.area_removed.FindCards(sienne))
        if trouvees:
            Faces.ShuffleAllTo(trouvees[:1], "EncounterDeck", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
