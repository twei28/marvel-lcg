from . import *

# Universal Weapon — ATTACHEMENT (Accuser Corps). WEAPON. SCH+1, ATK+1. 1 etoile.
# Attach to the villain.
# Attached character gains steady and the ACCUSER CORPS trait.
# Hero Action: Take 2 damage and deal yourself 1 facedown encounter card → shuffle this card into the
#   encounter deck.
# [star] Boost: Attach to an enemy.
#
# Cartes de reference :
#  - « Attach to the villain » : `AttachToFaceWhenPutIntoPlay(Villain)`, modele 01153 Concussion Blasters.
#  - « Attached character gains steady and the ACCUSER CORPS trait » :
#    `AbilityFactory.GiveKeywordToAttached(Character, trait="ACCUSER CORPS", steady=1)`, modele
#    baxter_stockman tx006 (`trait=`, `guard=`), gs127 (meme pack, `retaliate=`).
#  - « Take 2 damage and deal yourself 1 facedown encounter card -> shuffle this card into the encounter
#    deck » : deux couts composes, `CostFunc.TakeDamage(2, "YourIdentity")` (modele tx018) +
#    `CostFunc.DealPlayerEncounterCard(1, "Initiator")` (`game/ability/cost_func.py`), effet
#    `Faces.ShuffleAllTo([effect.this], Worlds.GetEncounterDeck(effect), effect)`.
#
# ⚠ Mots-pieges : « SHUFFLE this card into the encounter deck », pas « discard » (la carte revient dans le
# paquet, pas la defausse) ; « Attached CHARACTER » (une fois boostee sur un ennemi, le mot-cle suit) ;
# « deal YOURSELF » = le joueur qui paie le cout, pas un autre.


def GetAbilities() -> Sequence['Ability']:

    def melanger(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        Faces.ShuffleAllTo([effect.this], Worlds.GetEncounterDeck(effect), effect)

    def booster(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        ennemi = message.activating_enemy
        if ennemi is not None:
            effect.this.CastTo(Attachment).AttachTo2(ennemi, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        *AbilityFactory.GiveKeywordToAttached("Character", trait="ACCUSER CORPS", steady=1),
        (AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, melanger)
            .SetCostFunc(CostFunc.TakeDamage(2, "YourIdentity"))
            .SetCostFunc(CostFunc.DealPlayerEncounterCard(1, "Initiator"))),
        AbilityFactory.WhenCardBecomeBoost("This", booster),
    ]
