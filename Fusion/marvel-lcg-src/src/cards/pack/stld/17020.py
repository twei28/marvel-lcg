from . import *

# * Cosmo — ALLIE (The Galaxy's Most Wanted). THW 1 / ATQ 1, conséquences 1, PV 2.
# Interrupt: When Cosmo attacks or thwarts, name a card type, then discard the top card of a player deck or the encounter
# deck. If that card is of the named type, Cosmo does not take consequential damage for this use.
#
# CARTES DE REFERENCE
#  - `30020` Scarlet Spider (Kaine) : `initiator.DeclareCardType()` puis `card_type.IsType(face)` pour « name a card type ...
#    if it is of the named type ».
#  - `27043` Global Logistics : « a player deck or the encounter deck » = les decks des joueurs (`Worlds.GetPlayers`,
#    `player.player_deck`) et le(s) deck(s) rencontre (`Worlds.GetEncounterDecks`).
#
# TEXTE CONTRE CODE
#  ⚠ « name a card type, THEN discard the top card » : l'ORDRE compte. Le type est nommé AVANT de connaître la carte.
#    Correctif du 18/11/2026 (rapports nicodede62 #148/#149) : l'ancien script choisissait le paquet par une CIBLE
#    `PlayersDeckTop`/`EncounterDeckTop`, c'est-à-dire en montrant les cartes du dessus face visible, et ne demandait le type
#    qu'ensuite. Désormais : 1) on nomme le type, 2) on choisit le paquet par son NOM (aucune carte montrée), 3) on défausse.
#  « a player deck or the encounter deck » : n'importe quel deck de joueur (le sien ou celui d'un autre) ou le deck rencontre ;
#    un paquet vide n'est pas proposé (il n'a pas de carte du dessus à défausser).
#  « If THAT card is of the named type » : la carte réellement défaussée.
#  « for this use » : seulement les dégâts consécutifs de CETTE attaque / CE contrecarrage (`message.DoesNotTakeConsequentialDamage`).
#  Interrupt (pas Forced) : le joueur peut refuser.


def GetAbilities() -> Sequence['Ability']:

    def cosmo(effect: 'Effect', message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldThwart') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        initiator = effect.GetInitiator()

        # 1) Nommer le type, AVANT de rien voir.
        card_type = initiator.DeclareCardType(titre="Cosmo: name a card type")

        # 2) Choisir le paquet par son nom (aucune carte montree).
        decks: List['Deck'] = []
        libelles: List[str] = []
        for player in Worlds.GetPlayers(effect):
            if player.player_deck.GetSize() > 0:
                decks.append(player.player_deck)
                libelles.append("Player deck (%s)" % player.GetIdentity().name.lstrip("* ").strip())
        for deck in Worlds.GetEncounterDecks(effect):
            if deck.GetSize() > 0:
                decks.append(deck)
                libelles.append("Encounter deck")
        if not decks:
            return
        deck = decks[0] if len(decks) == 1 else initiator.AskChooseOneText(decks, libelles, titre="Cosmo: discard the top card of which deck?")

        # 3) Defausser la carte du dessus, puis comparer au type nomme.
        face = deck.GetTop()
        if face is None:
            return
        Faces.DiscardAll([face], effect)
        if card_type.IsType(face):
            message.DoesNotTakeConsequentialDamage(effect)

    return [
        AbilityFactory.WhenUnitWouldAttackOrThwart(
            AbilityType.Interrupt,
            "This",
            cosmo
        ),
    ]
