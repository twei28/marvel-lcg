from . import *

# Gluttony — RESSOURCE [physical]. Max 1 per deck.
# Response: After you spend this card, ready your hero.
#
# CARTE DE REFERENCE
#  - `21046` Audacity (pack mts) : « Max 1 per deck. Hero Response: After you
#    spend this card, deal 1 damage to the villain. » Meme montage,
#    `AfterYouSpendThisCard` ; seul l'effet change.
#
# TEXTE CONTRE CODE
#  ⚠ « Response » et non « Hero Response » : la ressource se depense dans LES
#    DEUX formes. Mais « ready your HERO » ne veut rien dire en alter-ego —
#    `SetTarget("YourHero")` ne rend alors aucune cible et la capacite ne part
#    pas, ce qui est le comportement voulu.
#  ⚠ « Max 1 per deck » est dans `cards.json` (`MaxPerDeck`), regle de
#    CONSTRUCTION de deck : rien a coder.
def GetAbilities() -> Sequence['Ability']:

    def gluttony(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(this, message)

        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.Response,
            gluttony
        ).SetTarget("YourHero"),
    ]
