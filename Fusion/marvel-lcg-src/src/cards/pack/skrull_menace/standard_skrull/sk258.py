from . import *

# Mobilization — TRAITRISE (Standard Skrull). 1 icone de boost.
# When Revealed (Alter-Ego): Engage each minion in play. The villain schemes.
# When Revealed (Hero): The villain and each minion engaged with you attacks you.
#
# Cartes de reference :
#  - Deux « When Revealed » selon la forme : **`01189`** Gang-Up / **`01187`** Assault (`WhenThisRevealed("Alter-Ego"
#    | "Hero", op)`).
#  - Heros : `Worlds.Enemies.VillainAndEngagedMinionsAttackYou(effect, joueur)` (modele 01189).
#  - « Engage each minion in play » : **`sk112`** Outnumbered (`Minion.EngagePlayer(joueur, effect)` pour chaque
#    sbire en jeu) ; « the villain schemes » : **`sk098`** (`DoSchemes`).
#
# ⚠ Mots-pieges : alter-ego : « EACH minion IN PLAY » (meme ceux engages avec un autre joueur : ils s'engagent
# avec celui qui revele) puis le mechant complote (meme sans sbire) ; heros : « the villain AND each minion engaged
# WITH YOU » (le mechant d'abord, puis les sbires engages avec ce joueur) ; le joueur est dans UNE seule forme :
# un seul des deux textes se joue.


def GetAbilities() -> Sequence['Ability']:

    def mobilisation_alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        for sbire in list(Worlds.GetOnFieldMinions(effect)):
            sbire.CastTo(Minion).EngagePlayer(joueur, effect)
        mechant = LeMechant(effect)
        if mechant is not None:
            mechant.DoSchemes(joueur, effect)

    def mobilisation_heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Worlds.Enemies.VillainAndEngagedMinionsAttackYou(effect, message.GetToPlayer())

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", mobilisation_alter_ego),
        AbilityFactory.WhenThisRevealed("Hero", mobilisation_heros),
    ]
