from . import *
def GetAbilities() -> Sequence['Ability']:
    def breakthrough(effect: 'Effect', message: 'Message.AfterCardPlacedCounter') -> None:
        this = effect.this.CastTo(Event)
        player = effect.GetInitiator()
        identity = player.GetIdentity()
        if identity:
            Faces.ReadyAll([identity], effect)
        # « Shuffle this card into your deck » : la carte quitte la zone ou elle
        # se trouve pour le deck du joueur, qui est melange dans la foulee.
        Faces.ShuffleAllTo([this], player.player_deck, effect)
    def check_alias_evidence(effect: 'Effect', message: 'Message.AfterCardPlacedCounter') -> bool:
        return message.counter_name == 'evidence' and message.trigger.name == 'Alias Investigations'
    return [
        # CORRECTIF (29/08/2026) : `.SetPlay()` manquait.
        # Breakthrough est un EVENEMENT : on le joue depuis sa main en reaction.
        # Sans capacite de jeu, deux consequences, l'une bruyante et l'autre
        # sourde. Bruyante : `CardFactory.CreateFace` (game/card/factory.py:120)
        # exige exactement UNE capacite `Play` sur un evenement et levait
        # `AssertionError: face.paper.card_id='61005'` — les trois decks
        # jessica_jones, jj_couverture et luke_cage ne montaient pas.
        # Sourde : meme sans l'assertion, la carte n'aurait jamais ete jouable.
        Ability(
            AbilityType.Response,
            Message.AfterCardPlacedCounter,
            [check_alias_evidence],
            breakthrough,
        ).SetPlay(),
    ]
