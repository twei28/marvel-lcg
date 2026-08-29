from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this)
        # « Each player MAY change to alter-ego form. Heal damage from each
        # alter-ego equal to its REC. »
        # Le changement de forme est optionnel, le soin ne l'est PAS : il
        # s'applique a chaque alter-ego en jeu, y compris celui d'un joueur qui
        # a refuse de changer (ou qui etait deja en alter-ego). Les deux etaient
        # fusionnes dans le meme choix, ce qui privait ce joueur de son soin.
        joueurs = Worlds.GetPlayers(effect)
        for player in joueurs:
            if not player.IsAlterEgo():
                def change_form(_targets: Sequence['CardFace'], player: 'Player'=player):
                    player.GetIdentity().ChangeToForm(AlterEgo, effect)
                def decline(_targets: Sequence['CardFace']):
                    pass
                player.ChooseAbilities(
                    effect,
                    AbilityFactory.ForChoiceAbility('Change to alter-ego form', change_form),
                    AbilityFactory.ForChoiceAbility('Decline', decline),
                )
        for player in joueurs:
            alter_ego = player.GetAlterEgo()
            if alter_ego and alter_ego.IsInPlay():
                alter_ego.HealHealth(alter_ego.recover, effect)
    return [AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated)]
