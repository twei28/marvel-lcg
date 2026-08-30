from . import *

# Spider-pathy (1/2) — SUPERPOWER
# Action: Search the encounter deck for the topmost minion and put it into
#   play engaged with you. Draw 1 card.
#
# "the topmost minion" : `Search.EncounterCard(include_discard_pile=False,
# card_type=Minion)` cherche le PREMIER sbire rencontre en descendant le
# deck de rencontre depuis le dessus (Search.SearchForCard, meme famille
# que core/legions_of_hydra/01180.py mais sans nom precis, filtre par
# card_type seul). "put it into play engaged with you" : `face.PutIntoPlay
# (player, effect)` engage AUTOMATIQUEMENT un Minion avec le joueur qui le
# met en jeu (commentaire "Will auto engage if this is a Minion",
# face_on_event.py:169).


def GetAbilities() -> Sequence['Ability']:

    def spider_pathy(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        face = Search.EncounterCard(
            effect,
            include_discard_pile=False,
            card_type=Minion,
        )
        if face:
            face.PutIntoPlay(initiator, effect)

        initiator.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            spider_pathy,
        ).SetPlay()
        .SetName("Spider-pathy"),
    ]
