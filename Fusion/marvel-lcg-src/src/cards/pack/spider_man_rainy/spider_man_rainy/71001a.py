from . import *

# * Spider-Man (Peter Parker) — custom « Rainy »
# Just Like Flies — Interrupt: When a minion engages you, web them.
#   (Limit twice per round.)
# Response: After a webbed enemy is defeated, remove 1 threat from a scheme.

def GetAbilities() -> Sequence['Ability']:

    def just_like_flies(effect: 'Effect', message: 'Message.WhenMinionEngagePlayer') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)
        Weber([message.trigger], 1, effect)

    def coup_au_filet(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Hero)
        this.RemoveThreatFromSchemes(effect.targets, 1, effect)

    def ennemi_toile(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> bool:
        return message.trigger.GetCounters('web') > 0

    return [
        AbilityFactory.WhenMinionEngagePlayer(
            AbilityType.Interrupt,
            Minion,
            "You",
            just_like_flies,
            conditions=[LimiteDeuxParRound],
        ).SetName("Just Like Flies"),

        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.Response,
            Enemy,
            coup_au_filet,
            conditions=[ennemi_toile],
        ).SetTarget(Scheme2),
    ]
