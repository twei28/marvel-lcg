from . import *

# * Venom

def GetAbilities() -> Sequence['Ability']:

    def venom_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        player = message.GetToPlayer()

        leader = Worlds.GetYourTeamLeader(effect)
        if leader:
            # « Venom attacks your leader. » Votre leader est sur la table
            # d'en face ; c'est une attaque ordinaire de sbire, pas la
            # procedure en quatre temps de la p.16, qui ne vaut que pour un
            # leader attaquant un leader.
            this.CastTo(Enemy).BasicAttack([leader], effect)
        else:
            this.DoActivate(player, effect)


    return [
        AbilityFactory.WhenThisRevealed(
            None,
            venom_revealed
        ),
    ]

