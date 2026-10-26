from . import *

# Lawyers — ATTACHEMENT nemesis (x2 dans le set). PERSONA. SCH +1.
# Attach to Dario Agger. Otherwise, attach to the villain.
# Attached character gains villainous. If the attached character is the villain, it gets an additional boost card
#   when it schemes.
# Action: Spend 2 resources of any type → discard this card.
#
# CARTES DE REFERENCE (PROCESSUS-CARTE etape 2)
#  - « Attach to X, if able. If you cannot, attach to the villain » : `13029` Beetle Armor MK IV,
#    `22030` Lethal Weapon (`AttachToFaceWhenPutIntoPlay(CardFinder(name=...), ...)` + repli sur le vilain).
#  - villainous donne par un attachement : `hc010` Outer Demons (`GiveKeywordToAttached(villainous=1)`, asset.py:30).
#  - « additional boost card when it schemes » : `sk125` Rock Mimicry (`WhenUnitWouldAttack(ForcedInterrupt, ..., op)` +
#    `message.GiveAdditionalBoostCardForThisActivation(1, effect)`), ici `WhenUnitWouldScheme` sur « AttachedVillain »
#    (sender_enemy.py:244).
#  - Action « spend N resources → discard this » : `04166` Anti-Hero Propaganda (`SetCost(...)`, `PlayerActionToDiscardThis`) ; « 2 resources of any type » = `Cost("2")` (et non `Cost("GG")`, deux icones wild).
#
# MOTS-PIEGES
#  - « attached CHARACTER gains villainous » : Dario Agger OU le vilain ; un sbire villainous recoit une carte de
#    boost a chaque activation (fiche villainous.md), le vilain en a deja une.
#  - « If the attached character is THE VILLAIN, it gets AN ADDITIONAL boost card WHEN IT SCHEMES » : en PLUS de la
#    carte du vilain, et seulement quand il MANIGANCE (pas quand il attaque).
#  - « Spend 2 resources OF ANY TYPE » : deux ressources quelconques (Cost("2")), action de TOUT joueur.
#  - `SCH +1` imprime : bonus de l'attache.
def GetAbilities() -> Sequence['Ability']:

    def boost_en_plus(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        Unused(effect)
        message.GiveAdditionalBoostCardForThisActivation(1, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name=NOM_DARIO),
            if_cannot_attach_to=Villain,
        ),
        *AbilityFactory.GiveKeywordToAttached(
            "Character",
            villainous=1,
            scheme=1,
        ),
        AbilityFactory.WhenUnitWouldScheme(
            AbilityType.ForcedInterrupt,
            "AttachedVillain",
            boost_en_plus,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.Action,
        ).SetCost(Cost("2")),
    ]
