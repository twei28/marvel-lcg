from . import *

# * Tyrone Johnson — custom « DesignHacker »
# During deck building, see insert.
# Enlightening — Tandy Bowen and Tyrone Johnson gain stalwart while Tandy
#   Bowen is in play.
#
# Le setup ne sort plus que Forces Combined (70003) : Dagger n'est plus une
# carte à mettre en jeu, c'est l'identité du joueur lié, créée au chargement
# par `SceneLoader.ExpandLinkedIdentity`.
#
# « Tandy Bowen ET Tyrone Johnson » : chaque face porte le mot-clé pour
# elle-même, sous la même condition. Celle de Tandy vit sur 70002b.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.SetupPutIntoPlay(
            ["70003"],
        ),
        AbilityFactory.ThisGainKeyword(
            CompterFaceEnJeu(NOM_TANDY, AlterEgo),
            stalwart=1,
            # `OnEvent.CardInPlay` ne voit PAS un changement de face : la carte
            # d'identite reste en jeu, seule sa face change, et le bonus ne se
            # recalculait donc jamais quand l'autre heros basculait en
            # alter-ego. `OnEvent.Form(Identity)` ecoute `AfterUnitChangeForm`
            # sur n'importe quelle identite de la table, ce qu'il faut ici
            # puisque la condition porte sur l'identite de l'AUTRE joueur.
            change_on_event=OnEvent.Form(Identity),
        ).SetName("Enlightening"),
        # Moitie de Harmony (imprimee sur Tandy) qui revient a Tyrone : elle
        # est conditionnee a « Tyrone en jeu », donc toujours vraie ici.
        AbilityFactory.ThisGainKeyword(
            recover=2,
        ).SetName("Harmony"),
    ]
