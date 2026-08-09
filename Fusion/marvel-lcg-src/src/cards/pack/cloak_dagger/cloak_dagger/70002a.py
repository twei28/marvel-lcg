from . import *

# * Dagger — custom « DesignHacker »
# [star] Destructive Duo — Dagger gets +2 ATK while Cloak is in play.
# [star] Bright Barrage — Damage Dagger deals using her basic attack power
#   (ATK) may be divided among enemies as you choose.
#
# Face héros de l'identité LIÉE (le second joueur créé au chargement).
#
# Bright Barrage modifie l'attaque de BASE : `ThisCanAttack(canbe_divided=True)`,
# exactement comme la forme géante de Wasp (13001c). L'ancienne adaptation en
# alliée devait passer par une action dédiée, faute d'attaque de base à
# modifier ; la face héros en a une, la capacité se rend donc telle quelle.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.ThisGainKeyword(
            CompterFaceEnJeu(NOM_CLOAK, Hero),
            attack=2,
            # `OnEvent.CardInPlay` ne voit PAS un changement de face : la carte
            # d'identite reste en jeu, seule sa face change, et le bonus ne se
            # recalculait donc jamais quand l'autre heros basculait en
            # alter-ego. `OnEvent.Form(Identity)` ecoute `AfterUnitChangeForm`
            # sur n'importe quelle identite de la table, ce qu'il faut ici
            # puisque la condition porte sur l'identite de l'AUTRE joueur.
            change_on_event=OnEvent.Form(Identity),
        ).SetName("Destructive Duo"),
        AbilityFactory.ThisCanAttack(
            canbe_divided=True,
        ).SetName("Bright Barrage"),
    ]
