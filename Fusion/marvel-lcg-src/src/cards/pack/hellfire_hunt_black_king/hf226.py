from . import *

# Mutant Experimentation (side scheme 3[per_hero], icone Hazard, boost 2). « When Defeated : Each player must choose and discard 1 card from their
# hand. » Cartes de reference : 04141 Prison Camps (`WhenSchemeBeDefeated`), `player.AskChooseFace` + `Faces.DiscardAll`.
# ⚠ « Each player » : tous les joueurs, pas seulement le vainqueur ; « must » : pas de refus ; main vide : rien.


def GetAbilities() -> Sequence['Ability']:
    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        for joueur in Worlds.GetPlayers(effect):
            main = list(joueur.hand_cards.Get())
            if not main:
                continue
            choisie = main[0] if len(main) == 1 else joueur.AskChooseFace(main, effect)
            if choisie is not None:
                Faces.DiscardAll([choisie], effect)

    return [AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue)]
