from . import *

# Collective Prayers (187) — TRAITRISE. 1 icone Y.
# When Revealed: Discard the top card of the encounter deck for each character in play. Reveal each card
#   discarded this way that belongs to the Dard'van Sect encounter set.
#
# Cartes de reference :
#  - « each character in play » : **`texas_twister/tt015`** Living Lightning (`Worlds.FindCardsOnField(effect,
#    card_type=Unit2)` = identites, allies, sbires, mechant) ;
#  - defausse de plusieurs cartes : `Worlds.DiscardEncounterCards(n, effect)` rend les cartes (modele sk106 /
#    sk139) ; revelation : `face.Reveal(joueur, effect)` (modele sk145a).
#
# ⚠ Mots-pieges : « the top card ... FOR EACH character in play » (autant de cartes que de personnages EN JEU au
# moment de la revelation, vilain et sbires compris) ; « reveal EACH card discarded this way THAT BELONGS to the
# Dard'van Sect encounter set » (seulement celles du set : ce n'est pas une carte a deux jeux de cartes) ; les
# cartes revelees le sont dans l'ordre de la defausse ; si le deck s'epuise, le moteur s'arrete (pas de remelange).


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        nombre = len(list(Worlds.FindCardsOnField(effect, card_type=Unit2)))
        defaussees = Worlds.DiscardEncounterCards(nombre, effect)
        for face in defaussees:
            if effect.world.is_game_over:
                return
            if face.paper.set_name == ENSEMBLE:
                face.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
    ]
