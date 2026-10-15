from . import *

# Power Skrull Engineering 1B — complot principal, face B. Menace 5[per_hero],
# depart 1[per_hero], escalade +1[per_hero].
# When Revealed: Discard cards from the encounter deck until a POWER SKRULL card
#   is discarded. Reveal that card. Shuffle the encounter discard pile into the
#   encounter deck.
#
# Cartes de reference : **`01116b`** Underground Distribution
# (`Worlds.DiscardEncounterCardsUntil`) comme `sk102`/`sk083a` (meme coffret) ;
# **`32113a`** Master Mold (`Worlds.GetEncounterDeck(effect).ShuffleWithDiscardPile(False, effect)`).
#
# ⚠ Mots-pieges : « Shuffle the encounter DISCARD PILE into the encounter deck » =
# la defausse ENTIERE (y compris les cartes defaussees par cette recherche) ; l'ordre
# imprime est « discard until, reveal, PUIS shuffle » : l'attachement revele est deja sur
# Paibok, il ne retourne pas au deck. Valeurs de menace dans desc (relues sur le scan).


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        RevelerPouvoirDuDeck(effect, message.GetToPlayer())
        Worlds.GetEncounterDeck(effect).ShuffleWithDiscardPile(False, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
    ]
