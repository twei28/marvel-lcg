from . import *

# Cosmic Power — Attachement de rencontre, Boost 1, ATK+ 0 [star]. 
# Attach to Galactus. If you cannot, attach to the villain.
# [star] Attached enemy's attacks gain overkill.
# Hero Action: Take 3 damage -> remove Cosmic Power from the game.
#
# Cartes de reference :
#  - `yd016` Sword-Gun-Arm (yondu_nemesis) : « Attach to X. If you cannot, ... » et
#    `UnitAttackGainKeyword("AttachedEnemy", overkill=True)`.
#  - `AbilityFactory.AttachToFaceWhenPutIntoPlay(finder, if_cannot_attach_to=Villain)` (attachment.py ; modeles 22030, 53039, ar013 : « EnemyLeader » vise le chef de l'EQUIPE ADVERSE du mode competitif, pas le vilain).
#  - `01027` Focused Rage : cout `CostFunc.TakeDamage(n, "YourIdentity")`.
#  - `4xxxx` Provoked/Hero Action sur attachement ennemi : `WhenInYourPlayTurn(HeroAction, op)`.
#
# ⚠ Mots-pieges :
#  - « If you cannot, attach to the VILLAIN » : Galactus absent (pas encore revele, ou deja retire) -> le mechant.
#  - « Attached enemy's attacks » : TOUTES les attaques du porteur (Galactus ou le mechant).
#  - « Take 3 damage -> » : COUT, subi par l'identite du joueur qui agit ; l'attachement est ensuite RETIRE DE
#    LA PARTIE (pas defausse).
#  - Le [star] devant « Attached enemy's attacks » est la convention d'impression de l'ATK+ `0*`.


def GetAbilities() -> Sequence['Ability']:

    def retirer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(message)

        Faces.RemoveAllFromGame([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name=NOM_GALACTUS, card_type=Minion),
            if_cannot_attach_to=Villain,
        ),
        AbilityFactory.UnitAttackGainKeyword(
            "AttachedEnemy",
            overkill=True,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            retirer,
        ).SetCostFunc(CostFunc.TakeDamage(3, "YourIdentity")),
    ]
