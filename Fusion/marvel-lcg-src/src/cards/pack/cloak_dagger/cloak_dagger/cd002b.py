from . import *

# * Tandy Bowen — custom « DesignHacker »
# During deck building, see insert.
# [star] Harmony — Tandy Bowen and Tyrone Johnson get +2 REC while Tyrone
#   Johnson is in play.
#
# Face alter-ego de l'identité LIÉE. Comme Enlightening (cd001b), le bonus est
# porté par chaque face pour elle-même, sous la même condition.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.ThisGainKeyword(
            CompterFaceEnJeu(NOM_TYRONE, AlterEgo),
            recover=2,
            # `OnEvent.CardInPlay` ne voit PAS un changement de face : la carte
            # d'identite reste en jeu, seule sa face change, et le bonus ne se
            # recalculait donc jamais quand l'autre heros basculait en
            # alter-ego. `OnEvent.Form(Identity)` ecoute `AfterUnitChangeForm`
            # sur n'importe quelle identite de la table, ce qu'il faut ici
            # puisque la condition porte sur l'identite de l'AUTRE joueur.
            change_on_event=OnEvent.Form(Identity),
        ).SetName("Harmony"),
        # Moitie d'Enlightening (imprimee sur Tyrone) qui revient a Tandy :
        # conditionnee a « Tandy en jeu », donc toujours vraie ici.
        AbilityFactory.ThisGainKeyword(
            stalwart=1,
        ).SetName("Enlightening"),
    ]
