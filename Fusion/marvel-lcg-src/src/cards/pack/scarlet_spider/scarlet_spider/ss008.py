from . import *

# Spider-pathy (2/2) — exemplaire physique 2 de 2, contenu identique a
# ss007 (voir ce fichier pour le detail du modele repris).


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
