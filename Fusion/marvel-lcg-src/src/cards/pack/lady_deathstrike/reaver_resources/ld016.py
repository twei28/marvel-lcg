from . import *

# Titanium Exoskeleton — ATTACHEMENT (module Reaver Resources). ARMOR. TECH. Boost 2.
# Attach to the enemy with the fewest remaining hit points.
# Attached enemy cannot take more than 2 damage from a single attack.
# Hero Action: Choose to either spend 3 resources of any type or remove a confused or stunned status card from attached enemy → discard this card.
#
# Cartes de reference :
#  - `40091` Titanium Exoskeleton (Military Grade, officiel) : TEXTE IDENTIQUE (FAQ de l'auteur : « 3 des memes cartes » que le modulaire
#    officiel) ; script recopie tel quel : `AttachToFaceWhenPutIntoPlay(Enemy, fewest_remaining_hp=True)`,
#    `UnitCannotTakeDamageWhile(NonKeyword, "AttachedEnemy", cannot_take_more_than_damage=2, is_from_attack=True)`,
#    `PlayerActionToDiscardThis(HeroAction).SetCostFunc(CostFunc.Custom(None, fn))` + `ForChoiceAbilityWithCost(Cost("3"))`.
#
# ⚠ Mots-pieges :
#  - « from a SINGLE attack » : le plafond de 2 vaut PAR attaque (les degats hors attaque ne sont pas plafonnes) ;
#  - « fewest REMAINING hit points » : PV restants, pas imprimes ; « Choose to either » : un seul des deux couts, au choix ;
#  - homonyme `40091` (Military Grade) : meme nom, set different, jamais cherche par nom.

def GetAbilities() -> Sequence['Ability']:

    def titanium_exoskeleton(targets: Sequence['CardFace'], effect: 'Effect'):
        this = effect.this.CastTo(Attachment)
        Unused(this)

        initiator = effect.GetInitiator()

        return initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("3")
            ),
            AbilityFactory.ForChoiceAbility(
                "Remove a confused or stunned status card from attached enemy",
                lambda targets:
                    Faces.DiscardAll(targets, effect),
            ).SetTarget(names=["Confused", "Stunned"],
                check_fn=lambda effect, face:
                    this.GetBindFace() == face.GetBindFace(),
                canbe_discard=True),
        ) != []


    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            Enemy,
            fewest_remaining_hp=True
        ),
        AbilityFactory.UnitCannotTakeDamageWhile(
            AbilityType.NonKeyword,
            "AttachedEnemy",
            cannot_take_more_than_damage=2,
            is_from_attack=True
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCostFunc(CostFunc.Custom(None, titanium_exoskeleton))
    ]

