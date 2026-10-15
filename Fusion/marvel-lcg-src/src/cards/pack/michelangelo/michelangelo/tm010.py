from . import *

# * Mikey's Skateboard — amelioration signature, x1 (13/15). NYC. VEHICLE.
# Cout 2, ressource [physical].
# Response: After you change form, exhaust Mikey's Skateboard -> ready your
#   identity.
#
# Cartes de reference :
#  - declencheur : RECETTES-MOTEUR §1, `AfterUnitChangeForm(type, "You", op)`
#    (modeles 01019a, 12001a, bt001b) ;
#  - cout d'epuisement de la carte : `CostFunc.Exhaust("This")` (ls007) ;
#  - pose de l'amelioration : `lady_sif/ls009` — `CanPlayThisUpgradeCard()`
#    sans cible imposee (le texte imprime n'en impose aucune) ;
#  - redresser l'identite : `Faces.ReadyAll([identite], effect)` (ls005).
#
# ⚠ Mots-pieges :
#  - « After you change form » : DANS LES DEUX SENS (alter-ego -> heros et
#    heros -> alter-ego). `to_this_form` / `to_form` ne sont donc PAS passes.
#  - « ready YOUR IDENTITY » : l'identite dans sa forme APRES le
#    changement (relue via `GetIdentity()` au moment de l'effet).
#  - « Response », pas Hero/AlterEgo Response : disponible dans les deux
#    formes.
#  - Pas de limite imprimee : une fois par changement de forme (le cout
#    d'epuisement borne naturellement).

def GetAbilities() -> Sequence['Ability']:

    def skateboard(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            Faces.ReadyAll([identite], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            skateboard,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
