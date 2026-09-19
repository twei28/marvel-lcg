from . import *

# Wanted (obligation du set modulaire Cops, sans « Give to »)
# Hero Action: Discard cards from the encounter deck until a POLICE minion is
#   discarded and put it into play engaged with you. Discard this card.
#
# Modeles : dz019 Performance Anxiety (obligation qui reste en jeu et se
# retire par une action), 11025 Rampage (DiscardEncounterCardsUntil +
# PutIntoPlay : un sbire pose par un joueur s'engage avec lui).

def GetAbilities() -> Sequence['Ability']:

    def recherche(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = effect.GetInitiator()
        face = Worlds.DiscardEncounterCardsUntil(effect, trait="POLICE", card_type=Minion)
        if face:
            face.PutIntoPlay(joueur, effect)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            recherche,
        ),
    ]
