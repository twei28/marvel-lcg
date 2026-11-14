from . import *

# Underground Tremor — TRAITRISE (ensemble Mole Man).
# When Revealed: Deal 1 damage to each non-AERIAL character you control. If no damage was dealt this way,
#   this card gains surge. If no SUBTERRANEAN enemy is in play, shuffle this card into the encounter deck.
#
# Cartes de reference :
#  - « Deal 1 damage to each non-AERIAL character you control » : `effect.this.DealDamage(cibles, 1,
#    effect)` sur les personnages du joueur sans trait AERIAL (identite + allies).
#  - « If no damage was dealt this way, gains surge » : `ThisCardGainSurge` (modele gs240q).
#  - « If no SUBTERRANEAN enemy is in play, shuffle this card into the encounter deck » :
#    `Worlds.FindCardsOnField(effect, CardFinder(trait="SUBTERRANEAN", card_type=Enemy))` vide ->
#    `Faces.ShuffleAllTo([effect.this], "EncounterDeck", effect)`.
#
# ⚠ Mots-pieges : « EACH non-AERIAL character YOU control » = tous a la fois (pas un choix) ; les deux
# branches de fin (surge / remelange) sont INDEPENDANTES l'une de l'autre, pas un « else » (un tour sans
# degat ET sans sbire SUBTERRANEAN declenche les DEUX) ; le remelange se fait meme si la carte a deja
# gagne surge (elle repart quand meme dans le deck).


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        cibles = [f for f in ([joueur.GetIdentity()] + list(joueur.allies.Get())) if not f.HasTrait("AERIAL")]
        if cibles:
            effect.this.DealDamage(cibles, 1, effect)
        else:
            ThisCardGainSurge(effect)

        if not Worlds.FindCardsOnField(effect, CardFinder(trait="SUBTERRANEAN", card_type=Enemy)):
            Faces.ShuffleAllTo([effect.this], "EncounterDeck", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]
