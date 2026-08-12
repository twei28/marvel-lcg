from . import *

# * Cloak — custom « DesignHacker »
# Retaliate 1.  (clé desc, gérée nativement)
# [star] Protective Pair — Cloak gets +2 DEF while Dagger is in play.
#
# Depuis la refonte du 5/8/2026, Dagger est une VRAIE identité (celle du joueur
# lié), plus une alliée : « while Dagger is in play » se lit donc au pied de la
# lettre, sur la face héros cd002a.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.ThisGainKeyword(
            CompterFaceEnJeu(NOM_DAGGER, Hero),
            defense=2,
            # `OnEvent.CardInPlay` ne voit PAS un changement de face : la carte
            # d'identite reste en jeu, seule sa face change, et le bonus ne se
            # recalculait donc jamais quand l'autre heros basculait en
            # alter-ego. `OnEvent.Form(Identity)` ecoute `AfterUnitChangeForm`
            # sur n'importe quelle identite de la table, ce qu'il faut ici
            # puisque la condition porte sur l'identite de l'AUTRE joueur.
            change_on_event=OnEvent.Form(Identity),
        ).SetName("Protective Pair"),
    ]
