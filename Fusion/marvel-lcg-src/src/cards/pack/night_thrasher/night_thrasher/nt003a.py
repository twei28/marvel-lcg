from . import *

# * Battle Board — FACE [[VEHICLE]] de l'amelioration PERMANENTE a deux faces.
# Classe Hero, pas de cout : elle arrive par `desc.Setup`.
# Permanent. Setup.
# Night Thrasher gets +1 THW and gains agile 1 (reduce damage from attacks
#   with boost cards by 1).
# Response: After you flip to this side, remove 1 threat from a scheme.
#
# Cartes de reference :
#  - **`34002a`** Phoenix Force et **`as002a`** Spider Armor (pack
#    armored_spidey) : l'amelioration PERMANENTE recto-verso et son
#    `AfterFlipToThisFace`. `45075b` Pursued by the Past pour le declencheur
#    « After you flip to this side ».
#  - `ok014` / `im007` pour `GiveKeywordToInPlayWhenApplyThis(..., thwart=1)`.
#  - `an004` / `vp001a` pour `this.RemoveThreatFromSchemes(cibles, 1, effect)`.
#  - **`27082`** Biting Retort pour l'accroche sur les cartes de boost
#    (`WhenBoostCardTurnedFaceUp`), et `ReduceCharacterTakeDamageBy`
#    (damage.py:404) pour la reduction elle-meme.
#
# ⚠ MOT-CLE MAISON `agile 1`, fiche docs/reference/mots-cles/agile.md, lue
# avant d'ecrire une ligne. AUCUNE PRIMITIVE MOTEUR. Le moteur ne garde la
# liste des cartes de boost d'une attaque que dans les messages d'APRES-COUP
# (`AfterUnitAttackUnit.boost_faces`, sender_damage.py:510) : au moment ou les
# degats tomberaient — la seule fenetre ou l'on peut encore les reduire — les
# cartes de boost ont deja ete defaussees a l'etape (d) de `can_boost.py`.
# Le montage inverse donc la lecture : on s'accroche au moment ou une carte de
# boost est RETOURNEE FACE VISIBLE pendant une attaque, et on enregistre a cet
# instant une reduction TEMPORAIRE bornee a cette attaque.
# ⚠ LE GARDE-FOU EST INDISPENSABLE : le message est envoye pour CHAQUE carte
# de boost retournee. Sans lui, une activation a trois cartes de boost
# reduirait de 3 et non de 1.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **NIGHT THRASHER** gets +1 THW » : un NOM PROPRE, celui de la seule
#    face HEROS. L'alter-ego s'appelle Dwayne Taylor et n'a pas de CTR.
#    `CardFinder(name="Night Thrasher")` et surtout PAS `"You"`, qui donnerait
#    le bonus aux deux faces (piege an002, trouve en partie reelle le
#    1/9/2026).
#  - « remove 1 threat from **a scheme** » : un complot au choix, principal ou
#    annexe. `Scheme2` couvre les deux ; aucune mention de Crise, donc pas
#    d'`ignore_crisis`.
#  - « After you flip **to this side** » : l'arrivee sur VEHICLE, pas le
#    depart. La face WEAPON porte son propre declencheur, symetrique.
#  - « **Response** » NUE cote VEHICLE, mais « **Hero** Response » cote WEAPON
#    (nt003b) : les deux faces ne s'ecrivent PAS pareil, et c'est imprime
#    ainsi. Retirer de la menace marche donc aussi en forme civile, infliger
#    des degats non.
#  - « Permanent. Setup. » : DEUX bases automatiques lues dans `desc`
#    (fiches mots-cles/permanent.md ; `desc.Setup` met la carte en jeu a la
#    mise en place). AUCUN script pour l'une ni pour l'autre.


def GetAbilities() -> Sequence['Ability']:

    def retour_sur_vehicule(effect: 'Effect', message: 'Message.AfterCardFlip') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        this.RemoveThreatFromSchemes(effect.targets, 1, effect)

    def agile(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> None:
        this = effect.this.CastTo(Upgrade)

        attaque = message.being_message.would_message

        # ⚠ GARDE-FOU : une seule reduction par ATTAQUE, quel que soit le
        # nombre de cartes de boost retournees.
        deja = getattr(this, "_agile_attaque", None)
        if deja is attaque:
            return
        this._agile_attaque = attaque

        this.effect.RegisterTemp(
            AbilityFactory.ReduceCharacterTakeDamageBy(
                CardFinder(name="Night Thrasher"),
                1,
            ),
            unregister_after_exec=True,
            until_event_end=attaque,
        )

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name="Night Thrasher"),
            control_by="You",
            thwart=1,
        ),
        AbilityFactory.WhenBoostCardTurnedFaceUp(
            AbilityType.NonKeyword,
            None,
            agile,
            while_attack=True,
        ),
        AbilityFactory.AfterFlipToThisFace(
            AbilityType.Response,
            retour_sur_vehicule,
        ).SetTarget(Scheme2),
    ]
