from . import *

# The Getaway (FAILED)
# In expert mode, attachments cannot be discarded from play during the first round.
# Setup: Each player searches the encounter deck for an attachment and reveals
#   it. Deal a facedown encounter card to each player who could not.
# ⚠ « cannot be discarded » : WhenCardLeavePlay(Attachment) + SetBeInstead au
# round 1 en expert ; si le message ne se laisse pas remplacer, l'ecart est
# signale au journal (ecart assume, a mesurer).

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        def chacun(player: 'Player') -> None:
            face = Search.SearchForCard(effect, player, include_encounter_deck=True, card_type=Attachment)
            if face is not None:
                face.Reveal(player, effect)
            else:
                player.DealEncounterCards(1, effect)
        Players.ForEachPlayer(effect, chacun)

    def garde(effect: 'Effect', message: 'Message.WhenCardLeavePlay') -> None:
        if hasattr(message, "SetBeInstead"):
            message.SetBeInstead(effect)

    def premier_round_expert(effect: 'Effect', message: 'Message.WhenCardLeavePlay') -> bool:
        return Worlds.IsExpert(effect) and effect.world.round_id <= 1 and getattr(message.into_area.flags, "is_discard_pile", False)

    return [
        AbilityFactory.AfterGameSetup(mise_en_place),
        AbilityFactory.WhenCardLeavePlay(AbilityType.ForcedInterrupt, Attachment, garde, conditions=[premier_round_expert]),
    ]
