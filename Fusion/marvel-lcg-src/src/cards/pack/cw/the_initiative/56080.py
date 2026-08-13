from . import *

# Drafted

def GetAbilities() -> Sequence['Ability']:

    def drafted(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(this)

        player = message.GetToPlayer()

        if Worlds.IsCompetitiveMode(effect):
            # « The enemy team attaches Drafted to a minion engaged with them
            # and that minion engages you. »
            team = Worlds.GetEnemyTeam(effect)
            minions = team.GetEngagedMinions()
            if minions:
                target = team.AskChooseFace(minions, effect)
                if target:
                    this.AttachTo2(target, effect)
                    target.CastTo(Minion).EngagePlayer(player, effect)
        else:
            minion = Worlds.DiscardEncounterCardsUntil(
                effect,
                card_type=Minion
            )
            if minion:
                minion.Reveal(player, effect)
                this.AttachTo2(minion, effect)


    return [
        AbilityFactory.WhenThisRevealed(
            None,
            drafted
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Minion,
            health=2,
            trait="AVENGER"
        ),
    ]

