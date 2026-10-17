from . import *

# Yomi — EVENEMENT DUAL Kuji-Kiri/Taijutsu, cout 1, [energy]. PSIONIC. SPELL. THWART.
# Classe : « Kuji-Kiri;Taijutsu ».
# Hero Action (thwart): Choose 1 card from the encounter discard pile and put it on top of the encounter deck -> remove 2
#   threat from a scheme.
#
# Mots-cles (fiches lues AVANT le code) : Shinobi (shinobi.md).
#
# Cartes de reference :
#  - effet « remove 2 threat from a scheme » (Hero Action thwart, `SetTarget(Scheme2)`) : `04049` Clear the Area ;
#  - cout qui CHOISIT une carte dans la defausse de rencontre : `CostFunc.Custom(Select.From(CardFinder(),
#    from_where=["EncounterDiscardPile"]), fn)` (`Select` de `valk/25001b`, `from_where=["EncounterDiscardPile"]`) ;
#  - deplacer au-dessus du deck de rencontre : `Faces.MoveAllToDeck(faces, deck, "Top", effect)` avec
#    `Worlds.GetEncounterDeck(effect)` (`harry_osborn/ho014`, `Faces.MoveAllToDeck` de `faces.py`).
#
# TEXTE CONTRE CODE
#  ⚠ « Choose 1 card from the encounter discard pile and put it on top of the encounter deck -> » : c'est un COUT (devant la
#    fleche), paye d'abord : si la defausse de rencontre est vide, la carte n'est pas jouable. La carte choisie est celle qui
#    se retrouve au DESSUS du deck de rencontre (la prochaine revelee).
#  ⚠ « remove 2 threat FROM A scheme » : UNE manigance au choix, principale ou annexe ; seules celles qu'un contre PEUT viser.
#  ⚠ « Hero Action (thwart) » : forme heros, libelle `thwart`.


def GetAbilities() -> Sequence['Ability']:

    def remettre_au_dessus(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        if not targets:
            return False
        return bool(Faces.MoveAllToDeck(list(targets), Worlds.GetEncounterDeck(effect), "Top", effect))

    def yomi(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.RemoveThreatFromSchemes(effect.targets, 2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            yomi,
        ).SetPlay().SetLabel('thwart')
        .SetCostFunc(CostFunc.Custom(
            Select.From(CardFinder(), from_where=["EncounterDiscardPile"]),
            remettre_au_dessus,
        ))
        .SetTarget(Scheme2),
    ]
