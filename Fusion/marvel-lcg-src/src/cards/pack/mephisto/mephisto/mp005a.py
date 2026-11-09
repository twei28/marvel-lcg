from . import *

# Complot principal Fiendish Investment (2A). When Revealed: Shuffle each BARGAIN attachment from the encounter discard pile into the encounter
# deck. In player order, each player must search the encounter deck for a BARGAIN attachment and reveal it. (Shuffle.)
#
# Cartes de reference : `Search.EncounterCard` + `Reveal` (fiche find.md, modele hp013/sk193a) ; remelange `Faces.ShuffleAllTo(.., "EncounterDeck")`.
# ⚠ Mots-pieges : la defausse est remelangee AVANT les recherches ; « IN PLAYER ORDER, EACH player MUST » (une recherche par joueur, obligatoire,
# a partir du premier joueur) ; « (Shuffle.) » : le deck de rencontre est melange apres les recherches.


def GetAbilities() -> Sequence['Ability']:
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        PactsDeLaDefausseDansLeDeck(effect)
        for joueur in JoueursDansLOrdre(effect):
            pacte = Search.EncounterCard(effect, joueur, include_discard_pile=False, trait="BARGAIN", card_type=Attachment)
            if pacte is not None:
                pacte.Reveal(joueur, effect)
        Worlds.GetEncounterDeck(effect).Shuffle()

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
