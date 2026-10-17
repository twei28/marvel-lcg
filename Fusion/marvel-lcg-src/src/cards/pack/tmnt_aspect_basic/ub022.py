from . import *

# * Jennika « Jenny » — ALLIE 3 [energy], 2*/2*, 3 PV, aspect Basic (TMNT Starter). NINJA. TURTLE.
# Response: After Jennika enters play, put a Shinobi (black) card from your discard pile on top of your deck.
#
# NOUVELLE. Cartes de reference : tv002 Bludgeon (« After Bludgeon enters play, put 1 card from your discard
# pile on top of your deck » : `AfterCardEnterPlay(Response, "This")` + `SetTarget(from_where=
# ["YourDiscardPile"])` + `Faces.MoveAllToDeck(..., "Top")`). Mot-cle « Shinobi » : fiche
# mots-cles/shinobi.md — une carte Shinobi porte l'une des quatre classes Bushido, Ninjutsu, Kuji-Kiri,
# Taijutsu (`CardFinder(card_classes=CLASSES_SHINOBI)`, liste reprise de cards/pack/jennika/jennika).
# « (black) » : rappel de la couleur des cartes Shinobi, zero code.
# TEXTE CONTRE CODE : « a Shinobi card » = UNE ; « YOUR discard pile » ; « on TOP of your deck ».

CLASSES_SHINOBI = ["Bushido", "Ninjutsu", "Kuji-Kiri", "Taijutsu"]


def GetAbilities() -> Sequence['Ability']:

    def jennika(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        cibles = [t for t in effect.targets if t is not None]
        if not cibles:
            return
        Faces.MoveAllToDeck(cibles, effect.GetInitiator().player_deck, "Top", effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            jennika,
        ).SetTarget(finder=CardFinder(card_classes=CLASSES_SHINOBI), from_where=["YourDiscardPile"]),
    ]
