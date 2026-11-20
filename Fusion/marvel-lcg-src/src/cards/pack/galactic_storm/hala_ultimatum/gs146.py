from . import *

# Kree Resilience — ATTACHEMENT (Hala Ultimatum). CONDITION. 1 etoile + 2 icones de boost. 2 exemplaires.
# Attach to the villain.
# Attached villain can have 1 additional tough status card.
# Hero Action: Spend [physical][physical] resources → discard this card.
# [star] Boost: Give the activating enemy a tough status card.
#
# Cartes de reference :
#  - « Attach to the villain » : `AttachToFaceWhenPutIntoPlay(Villain)`, modele 01153 Concussion Blasters.
#  - « Attached villain can have 1 additional tough status card » : `RetenirTenaceSupplementaire(1)`
#    (hala_ultimatum/__init__.py), construite sur le meme message que
#    `AbilityFactory.ThisCanHaveAdditionalTough` (modele tmnt_aspect_protection/up016.py), mais pour un
#    HOTE attache plutot que « This ».
#  - « Hero Action: Spend [physical][physical] resources -> discard this card » :
#    `PlayerActionToDiscardThis(HeroAction)` + `SetCost(Cost("RR"))`, modele gs083 Optic Blast Cannon
#    (memes deux icones de poing, meme pack).
#  - « Boost: Give the activating enemy a tough status card » : `message.activating_enemy` +
#    `Faces.GiveStatus`, modele gs138b/gs139b/gs140b (Tanalth) pour la pose de Tenace.
#
# ⚠ Mots-pieges : « 1 ADDITIONAL » (en plus du plafond de base, pas un plafond absolu de 1) ; deux
# exemplaires attaches ensemble au mechant empilent chacun leur +1 (lecture retenue, non teste en jeu a
# plusieurs copies simultanees — voir questions du lot) ; le Boost donne un tenace a L'ENNEMI QUI S'ACTIVE,
# pas forcement au porteur de la carte.


def GetAbilities() -> Sequence['Ability']:

    def booster(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Faces.GiveStatus([message.activating_enemy], "Tough", effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        RetenirTenaceSupplementaire(1),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("RR")),
        AbilityFactory.WhenCardBecomeBoost("This", booster),
    ]
