from . import *

# * Wiccan (face heros) — custom « CptScorp »
# Clairvoyance — During the player phase, play with the top card of the
#   encounter deck face up.
# Forced Interrupt: At the start of the villain phase, discard the top card
#   of the encounter deck.
#
# Clairvoyance -> modele EXACT : Falcon (`falcon/falcon/53001a.py`), qui
# imprime le meme « play with the top card of the encounter deck face up »
# et le rend par `*AbilityFactory.PlayWithTopCardOfDeckFaceup(lambda effect:
# Worlds.GetEncounterDecks(effect), only_during_player_phase=True)`. Le
# `only_during_player_phase=True` est ce qui rend « During the player phase »
# : la fabrique ajoute alors un `WhenPlayerPhaseBegin` et filtre ses autres
# declencheurs sur `effect.world.phase.IsPlayerPhase("AnyPlayer")`
# (game/ability/factory/deck.py:84-135). Magik (45030a) emploie la meme
# fabrique mais sur le deck JOUEUR, sans la restriction de phase : ce n'est
# donc pas elle le modele ici.
# `Worlds.GetEncounterDecks` (pluriel) et non `GetEncounterDeck` : certains
# scenarios en ont plusieurs, et Falcon les couvre tous.
#
# Forced Interrupt -> `AbilityFactory.WhenVillainPhaseBegin(AbilityType.
# ForcedInterrupt, ...)` (game/ability/factory/turn_phase.py:176), le
# declencheur « au debut de la phase du vilain » ; defausse du dessus par
# `Worlds.DiscardEncounterTopCard(effect)` (worlds.py:577), la meme brique
# qu'utilise Falcon dans sa Response « Eagle-Eyed ». C'est bien un
# INTERRUPT (avant le debut de la phase) et non un ForcedResponse : le texte
# imprime dit « Forced Interrupt ».
#
# Note de conception : la carte du dessus etant retournee face visible par
# Clairvoyance, la defausser en debut de phase du vilain est la contrepartie
# imprimee du kit (on ne conserve pas l'information d'un round sur l'autre).
# Rien a coder pour ca : la fabrique de Clairvoyance retourne la nouvelle
# carte du dessus au debut de la phase joueur suivante.

def GetAbilities() -> Sequence['Ability']:

    def defausser_le_dessus(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)

        Worlds.DiscardEncounterTopCard(effect)

    return [
        *AbilityFactory.PlayWithTopCardOfDeckFaceup(
            lambda effect:
                Worlds.GetEncounterDecks(effect),
            only_during_player_phase=True,
        ),
        AbilityFactory.WhenVillainPhaseBegin(
            AbilityType.ForcedInterrupt,
            defausser_le_dessus,
        ),
    ]
