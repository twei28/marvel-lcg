from . import *

# * Bullseye

def GetAbilities() -> Sequence['Ability']:

    def bullseye_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        player = message.GetToPlayer()

        leader = Worlds.GetYourTeamLeader(effect)
        if leader:
            # « The enemy team discards an attachment from your leader. » Le
            # choix appartient a l'equipe adverse, la carte defaussee est sur
            # VOTRE leader, en face. S'il n'a aucun attachement, il n'y a rien
            # a defausser et la carte ne fait rien de plus.
            team = Worlds.GetEnemyTeam(effect)
            attachments = leader.GetAttachedAttachments()
            if attachments:
                team.AskDiscardFaces(attachments, (1, 1), effect)
        else:
            player.DiscardControlCards(effect, upgrade=True)


    return [
        AbilityFactory.WhenThisRevealed(
            None,
            bullseye_revealed
        ),
    ]

