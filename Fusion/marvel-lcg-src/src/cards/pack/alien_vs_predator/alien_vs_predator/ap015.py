from . import *

# * Piercing Pharynx — ATTACHEMENT unique. CONDITION. XENOMORPH. ATK +1. Boost ★ (+1). (Fichier du zip : « Inner Teeth ».)
# Attach to Alien Queen and give her a tough status card. Otherwise, this card gains surge.
# Alien Queen gains retaliate 1.
# Hero Action: If Predator Warlord is in play, spend [energy][mental] resources → discard this card.
# [star] Boost: Reveal this card.
#
# Cartes de reference :
#  - « Attach to X and give her a tough status card » : `AttachToFaceWhenPutIntoPlay(.., when_attach_operation=)` + `GiveStatus("Tough")` ;
#  - « gains retaliate 1 » : `GiveKeywordToAttached(.., retaliate=1)` (01119 Klaw) ; ATK +1 : `desc.ATK+`, natif ;
#  - « Hero Action: If ..., spend → discard » : `PlayerActionToDiscardThis(HeroAction, conditions=[Warlord en jeu]).SetCost(Cost("YB"))` ;
#  - Boost : `RevealThisCard` (tk).
#
# ⚠ Mots-pieges :
#  - la carte Tenace n'est donnee QUE si la carte s'attache (sinon surge, rien d'autre) ;
#  - « IF Predator Warlord is in play » : apres sa defaite (stade 4), la carte ne peut plus etre defaussee ainsi ;
#  - [energy] = Y, [mental] = B.


def GetAbilities() -> Sequence['Ability']:

    def tenace(face: 'CardFace', effect: 'Effect') -> None:
        Faces.GiveStatus([face], "Tough", effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name=REINE, card_type=Villain), if_cannot_gain_surge=True,
                                                   when_attach_operation=tenace),
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name=REINE), retaliate=1),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
            conditions=[lambda effect, message: MechantNomme(effect, WARLORD) is not None],
        ).SetCost(Cost("YB")),
        BoostReveleCetteCarte(),
    ]
