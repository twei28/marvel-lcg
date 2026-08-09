# Recovered automatically from Python 3.10 bytecode.
# Comments and original formatting were not present in the compiled file.

from . import *
from cards.pack.aoa.missions import MinionToMission, GetMissionScheme
def GetAbilities() -> Sequence['Ability']:
    def agent_of_apocalypse_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # CORRECTIF : l'original appelait Worlds.ScenarioArea('MissionArea'), un stub
        # `raise NotImplemented` du moteur — le choix « mission area » crashait.
        this = effect.this.CastTo(Minion)
        Unused(this)
        player = message.GetToPlayer()
        choices = [AbilityFactory.ForChoiceAbility('It activates against you', lambda targets: this.DoActivate(player, effect)).SetTarget([this])]
        if GetMissionScheme(effect):
            choices.insert(0, AbilityFactory.ForChoiceAbility('Add Agent of Apocalypse to the mission area', lambda targets: MinionToMission(effect, this)).SetTarget([this]))
        player.ChooseAbilities(effect, *choices)
    def agent_of_apocalypse_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        message.GiveActivatingEnemyAdditionalBoostCard(1, effect)
    return [AbilityFactory.WhenThisRevealed(None, agent_of_apocalypse_revealed), AbilityFactory.WhenCardBecomeBoost('This', agent_of_apocalypse_boost)]
