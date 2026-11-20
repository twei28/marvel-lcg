from . import *

# * Lauri-Ell — ALLIE de campagne (Basic / Campaign, n° 226). Cout 3. THW 1* / ATK 2**, 5 PV. KREE.
# Honorary. Toughness.
# [star] Response: After Lauri-Ell attacks and damages an enemy, discard each boost card on that enemy.
#
# Cartes de reference :
#  - **`galactic_storm/earth_under_siege` `ExcesVersMenaceSurManigancePrincipale`** (gs176 Destroyer) :
#    `AbilityFactory.AfterUnitAttackUnit(ForcedResponse, "This", Unit2, ...)`, meme trigger « apres avoir
#    attaque et touche » (mesure `message.took_damage_targets`/`excess_damage`).
#  - **« boost card ON an enemy »** = le stock de cartes boost FACE CACHEE qu'un ennemi peut accumuler
#    HORS activation (`fne/kingpin/60165` James Wesley : « give him a facedown boost card... placee dans
#    sa pile de boost », `CanBoost.GiveFacedownBoostCardsInternal` -> `self.components.boostable`). Le
#    composant `Boostable` (`card/face/component/boostable.py`) stocke ce surplus dans
#    `components.boostable.GetDeck()` ; `Faces.DiscardAll` sur son contenu le vide.
#
# ⚠ Mots-pieges :
#  - « attacks AND DAMAGES an enemy » : l'ennemi doit avoir reellement pris des degats (`message.
#    took_damage_targets`), pas seulement avoir ete attaque (riposte, tenace qui absorbe tout, etc.) ;
#  - « that enemy » : uniquement celui qui a pris les degats, pas tous les ennemis engages ;
#  - « EACH boost card » : toutes celles de la pile, pas seulement celle de l'activation en cours (qui de
#    toute facon est deja videe avant la fin de l'attaque) — cette carte cible le SURPLUS persistant.
#  - « [star] » devant Response : footnote pure (convention GS-0 Q6 deja actee), aucun effet code.


def GetAbilities() -> Sequence['Ability']:

    def lauri_ell(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        for cible in message.took_damage_targets:
            pile = cible.components.boostable.GetDeck()
            cartes = pile.GetAll()
            if cartes:
                Faces.DiscardAll(cartes, effect)

    return [
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.ForcedResponse,
            "This",
            Enemy,
            lauri_ell,
        ),
    ]
