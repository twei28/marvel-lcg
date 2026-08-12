from . import *

# Get Under Control — custom « DesignHacker »
# Give to the Amadeus Cho player. Victory 1.
# You cannot put allies into play.
# Alter-Ego Action: Treat "The Trunk's" printed text box as if it were blank,
#   then remove "The Trunk" from the game → remove this obligation from the
#   game.


def GetAbilities() -> Sequence['Ability']:

    def get_under_control(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        initiator = effect.GetInitiator()

        trunk = FindTrunk(effect, initiator)
        if trunk:
            # « as if it were blank » : les capacités forcées de « The Trunk »
            # ne doivent pas se déclencher pendant son retrait.
            for face in trunk:
                face.TemporaryGain(effect, message, treat_as_blank=True)
            Faces.RemoveAllFromGame(trunk, effect)

        Faces.RemoveAllFromGame([this], effect)

    def trunk_en_jeu(effect: 'Effect') -> bool:
        return FindTrunk(effect, effect.this.CastTo(Obligation).GetGiveToPlayer()) != []

    return [
        AbilityFactory.PlayersCannotPlayCardWhile(
            "AttachedPlayer",
            Ally,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            get_under_control,
            conditions=[lambda effect, message: trunk_en_jeu(effect)],
        ),
    ]
