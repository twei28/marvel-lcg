from . import *

# Harvest — COMPLOT ANNEXE (HELLMOUTH). Menace 3, Hinder 1[per_hero], Victory 0.
# When Defeated: Find Becoming and reveal it. Put the set-aside Prophecy Girl upgrade into play.
#
# CARTES DE REFERENCE
#  - `43021` Specialized Training : `WhenSchemeBeDefeated(WhenDefeated, "This", op)` + `Search.SearchForCard(include_set_aside=True, ..)` +
#    `face.PutIntoPlay(joueur, effect, under_control=True)` pour « put the set-aside X into play ».
#  - `mv013` : `face.Reveal(joueur, effect)` pour « find ... and reveal it ».
#
# TEXTE CONTRE CODE
#  « Find Becoming and reveal it » -> `Trouver` (deck, defausse, mise de cote), puis `Reveal`. « the set-aside Prophecy Girl » -> UNIQUEMENT la zone
#    de mise de cote (carte liee a Harvest par `desc.Linked`), mise en jeu sous le controle du joueur qui a vaincu. Victory 0 : `desc`.
#  ⚠ « Harvest » est aussi le nom d'une traitrise OFFICIELLE (05029) : toutes les recherches filtrent sur le type.


def GetAbilities() -> Sequence['Ability']:

    def harvest(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        joueur = JoueurDeLaDefaite(effect, message)
        becoming = Trouver(effect, joueur, NOM_BECOMING, EncounterSideScheme)
        if becoming:
            becoming.Reveal(joueur, effect)
        prophecy = Search.SearchForCard(effect, joueur, include_set_aside=True, name=NOM_PROPHECY_GIRL, card_type=Upgrade)
        if prophecy:
            prophecy.PutIntoPlay(joueur, effect, under_control=True)

    return [
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            harvest,
        ),
    ]
