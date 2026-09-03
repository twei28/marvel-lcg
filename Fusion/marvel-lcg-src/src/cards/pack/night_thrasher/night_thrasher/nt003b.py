from . import *

# * Battle Board — FACE [[WEAPON]] de l'amelioration PERMANENTE a deux faces.
# Permanent.
# Night Thrasher gets +1 ATK and +1 DEF.
# Hero Response: After you flip to this side, deal 1 damage to an enemy.
#
# Cartes de reference :
#  - **`34002b`** Phoenix Force et **`as002b`** Spider Armor : la seconde face
#    d'une amelioration permanente, et son bonus continu cite par NOM PROPRE.
#  - `45075b` / `as002a` pour `AfterFlipToThisFace`.
#  - `08013` / partout pour `this.DealDamage(cibles, 1, effect)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **NIGHT THRASHER** gets +1 ATK and +1 DEF » : NOM PROPRE, la seule face
#    HEROS. `CardFinder(name="Night Thrasher")`, jamais `"You"`.
#  - « **Hero** Response » ici, alors que la face VEHICLE imprime « Response »
#    nue : les deux faces ne s'ecrivent pas pareil, et c'est voulu — infliger
#    des degats depuis la forme civile n'aurait pas de sens.
#  - « deal 1 damage to **an enemy** » : un ennemi au choix, sans lien avec ce
#    qui vient de se passer.
#  - Cette face n'a PAS `desc.Setup` : c'est nt003a, la face VEHICLE, qui
#    arrive a la mise en place. La partie commence donc toujours planche cote
#    vehicule.
#  - « Permanent. » : base automatique lue dans `desc.Permanent`, aucun script
#    (fiche mots-cles/permanent.md).


def GetAbilities() -> Sequence['Ability']:

    def retour_sur_arme(effect: 'Effect', message: 'Message.AfterCardFlip') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        this.DealDamage(effect.targets, 1, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name="Night Thrasher"),
            control_by="You",
            attack=1,
            defense=1,
        ),
        AbilityFactory.AfterFlipToThisFace(
            AbilityType.HeroResponse,
            retour_sur_arme,
        ).SetTarget(Enemy),
    ]
