from . import *

# Darkhold Dwarf (module Darkhold). Sbire DEMON ELITE. « When Revealed : Tuck the topmost Spell of Darkhold encounter card from the encounter
# discard pile under here. When Defeated : Reveal the card tucked here. »
# Cartes de reference : mots-cles/tuck.md (`PlaceCardHere(faces, True, effect)` = tuck FACE VISIBLE, livret p.4 ; helper `Glisser` de gs119),
# 01034 (`FindTopmost` dans une defausse), 04112b (`WhenUnitBeDefeated` / « When Defeated »).
# ⚠ « topmost » : `Deck.FindTopmost` (premier element de `Get(True)`). Sans Spell of Darkhold dans la defausse, la carte ne fait rien.


def GetAbilities() -> Sequence['Ability']:
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        defausse = Worlds.GetEncounterDiscardPile(effect)
        sort = defausse.FindTopmost(CardFinder(trait=TRAIT_SORT))
        if sort is not None:
            this.PlaceCardHere([sort], True, effect)

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this
        glisses = list(this.GetPlacedCardArea().Get(True))
        if not glisses:
            return
        joueur = this.CastTo(Minion).GetEngagedPlayer()
        for face in glisses:
            face.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
