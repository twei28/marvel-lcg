from . import *

# * Eddie Brock (face ALTER-EGO) : CIVILIAN. REC 4, main 6, PV 12.
# You may include up to 5 ATTACK events in your deck from aspects other than your chosen aspect. (regle de construction de deck : texte seul, le moteur ne valide pas les decks)
# Dark Urges — Action: Discard cards from the encounter deck until you discard a minion. Put that minion into play engaged with you. (Limit once per round.)
#
# CARTES DE REFERENCE
#  - `01116b` Underground Distribution : `Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)` + `face.PutIntoPlay(joueur, effect)` (mise en jeu, SANS When Revealed).
#  - `mystique/my001b` : `WhenInYourPlayTurn(AbilityType.Action, op).SetName(..).LimitOncePerRound()` pour une « Action » imprimee sur l'identite.
#
# TEXTE CONTRE CODE
#  « Action » : jouable uniquement en forme alter-ego (face visible). « discard ... UNTIL you discard a minion » : `DiscardEncounterCardsUntil` (remelange la defausse si le deck s'epuise, regle native).
#  « engaged WITH YOU » : mis en jeu pour CE joueur. « Limit once per round » : `LimitOncePerRound`. Chiffres : PV 12, main 6, REC 4.


def GetAbilities() -> Sequence['Ability']:

    def pulsions_sombres(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        face = Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)
        if face is not None and joueur is not None:
            face.PutIntoPlay(joueur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            pulsions_sombres,
        ).SetName("Dark Urges").LimitOncePerRound(),
        NoterVictoire(),
    ]
