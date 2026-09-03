from . import *

# Vibranium Enhancement — amelioration signature, x1. ARMOR. TECH. Cout 2,
# ressource [energy].
# While Spider Armor has the [[OPERATIONAL]] trait, Armored Spidey gains
#   retaliate 1 and steady.
# Response: After you play this card, if Spider Armor has the [[OPERATIONAL]]
#   trait, place 1 metal counter on it (to a maximum of 3).
#
# Cartes de reference :
#  - **`50093`** Embassy Guard (set Batroc) pour le « While <carte
#    recto-verso> has the <trait> » : `condition=` +
#    `change_on_event=OnEvent.Trait(CardFinder(name=...))`. Meme montage que
#    as012.
#  - **`bt012`** / `50144` pour `GiveKeywordToInPlayWhenApplyThis(...,
#    retaliate=1, steady=1)` : donner un mot-cle a un personnage.
#  - `AfterYouPlayThisFromHand(Response, op)` (play.py:350) pour « After you
#    play this card », qui est un `AfterPlayerPlayedCard("You", "This",
#    from_hand=True)` deja emballe.
#  - `34001b` * Jean Grey pour `Faces.PlaceCountersOn`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **Armored Spidey** gains » : un NOM PROPRE, la seule face HEROS.
#    Riposte et Stoique n'ont aucun sens sur la face civile. Contre-cas en
#    forme civile du (piege an002).
#  - « **if** Spider Armor has the [[OPERATIONAL]] trait » sur la Reponse :
#    condition lue AU MOMENT DE LA RESOLUTION, pas a l'annonce. Jouer la
#    carte armure detruite ne pose aucun compteur — et c'est logique, ce
#    serait la reparer gratuitement.
#  - « **to a maximum of 3** » : plafond explicite. Sans lui, deux copies
#    (ou un rejeu) monteraient l'armure au-dessus de son maximum imprime et
#    fausseraient as004 Burst It!. `MAX_METAL` est la constante du set.
#  - « place 1 metal counter **on it** » : sur l'AMELIORATION Spider Armor,
#    pas sur cette carte-ci ni sur l'identite.
#  - « retaliate 1 **and** steady » : les deux, et les deux sont des bases
#    automatiques du moteur (fiches mots-cles/retaliate.md et steady.md).
#    Rien a recoder : on se contente de les DONNER.
#  - ⚠ La carte porte le trait ARMOR, ce qui en fait la seconde cible legale
#    de `as018` Just a Ricochet (« Play only if you control an [[ARMOR]]
#    upgrade »), a cote de la Spider Armor elle-meme.


def GetAbilities() -> Sequence['Ability']:

    def vibranium_enhancement(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        armure = MonArmure(effect)
        if armure is None or not armure.HasTrait("OPERATIONAL"):
            return
        if armure.GetCounters('metal') >= MAX_METAL:
            return
        Faces.PlaceCountersOn([armure], 1, 'metal', effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name="Armored Spidey"),
            control_by="You",
            retaliate=1,
            steady=1,
            condition=ArmureOperationnelle,
            change_on_event=OnEvent.Trait(CardFinder(name=NOM_ARMURE)),
        ),
        AbilityFactory.AfterYouPlayThisFromHand(
            AbilityType.Response,
            vibranium_enhancement,
        ),
    ]
