from . import *
# Masterstroke (Justice, evenement 3 [mental]). THWART. Requirement ([energy][mental][physical]).
# Hero Action (thwart): Discard the top 4 cards of the encounter deck, then for each card discarded this way choose one:
# • Remove threat from a scheme equal to the number of boost icons ([boost]) on that card.
# • Place that card on top of the encounter deck and draw 1 card.
#
# Cartes de reference : 15004 / ho014 (`Worlds.DiscardEncounterCards(n, effect)` + `FacesCounter.CountTotalBoostIcons`) ; 08013 / 16155
# (`ChooseAbilities(ForChoiceAbility(..))` + `.SetTarget(Scheme2)`) ; ag001b / bt011 (`Faces.MoveAllToDeck([face], deck, "Top", effect)`,
# position en argument POSITIONNEL) ; fiche requirement.md.
# ⚠ « boost icons ([boost]) » : les icones chiffrees SEULES (`CountTotalBoostIcons`, l'etoile n'est pas une icone de boost ici) ;
# « for EACH card discarded » : un choix par carte, dans l'ordre defausse ; « on TOP of the encounter deck » : chaque carte replacee passe
# au-dessus des precedentes.
def GetAbilities() -> Sequence['Ability']:
    def masterstroke(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()
        for face in Worlds.DiscardEncounterCards(4, effect):
            icones = FacesCounter.CountTotalBoostIcons([face])
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    f"Remove {icones} threat from a scheme",
                    lambda targets, n=icones: this.RemoveThreatFromSchemes(targets, n, effect)
                ).SetLabel('thwart').SetTarget(Scheme2),
                AbilityFactory.ForChoiceAbility(
                    "Place that card on top of the encounter deck and draw 1 card",
                    lambda targets, f=face: (
                        Faces.MoveAllToDeck([f], Worlds.GetEncounterDeck(effect), "Top", effect),
                        joueur.DrawUp(1, effect))
                ).SetHasNoTargetEffect(),
            )
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            masterstroke,
        ).SetPlay().SetLabel('thwart'),
    ]
