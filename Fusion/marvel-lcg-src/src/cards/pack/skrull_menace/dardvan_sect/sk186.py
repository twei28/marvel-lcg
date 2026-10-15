from . import *

# Dard'van Sect (186) — COMPLOT ANNEXE. Menace 2[per_hero], 1 icone HAZARD, 3 icones Y.
# When Revealed: Give the villain 1 facedown boost card.
#
# Cartes de reference :
#  - « Give the villain 1 facedown boost card » : **`skrull_menace/new_revengers/sk167`** White Tiger (When Defeated :
#    meme phrase, `Faces.GiveFacedownBoostCards([mechant], 1, effect)`, modele **`30037`** Solus).
#  - Hazard : base AUTOMATIQUE (`desc.Hazard = "1"`, fiche mots-cles/hazard.md), aucun module.
#
# ⚠ Mots-pieges : « the VILLAIN » (le mechant, pas un sbire) ; « FACEDOWN boost card » (la carte vient du dessus
# du deck rencontre, face cachee, et se retournera a la PROCHAINE activation du mechant) ; l'icone noire
# « boite avec un plus » = HAZARD (carte penchee + croix, glyphe `H` de ChampionsIcons.ttf : voir
# defs/pantheon_questions.md).


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        mechant = Worlds.FindVillain(effect)
        if mechant is not None:
            Faces.GiveFacedownBoostCards([mechant], 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
    ]
