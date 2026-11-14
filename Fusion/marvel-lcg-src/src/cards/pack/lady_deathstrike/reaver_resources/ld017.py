from . import *

# Inhibitor Collar — ATTACHEMENT (module Reaver Resources, x2). TECH. ATK -1. Boost 1.
# Attach to your identity.
# Treat your identity's printed text box as if it were blank (except for traits).
# Action: Choose to either exhaust a character you control or take 3 damage → discard this card. (Any player can do this.)
#
# Cartes de reference :
#  - `40092` Inhibitor Collar (Military Grade, officiel) : TEXTE IDENTIQUE ; script recopie tel quel : `AttachToFaceWhenPutIntoPlay("YourIdentity")`,
#    `GiveKeywordToAttached("Character", treat_as_blank=True)`, `PlayerActionToDiscardThis(Action).SetCostFunc(CostFunc.Custom(None, fn))
#    .AnyPlayerCanDoThis()` ; `ATK+ -1` natif de `desc`.
#
# ⚠ Mots-pieges :
#  - « (except for TRAITS) » : seuls les mots du cadre de texte sont ignores ; « Any player can do this » : le cout est paye par le joueur qui agit
#    (son personnage epuise, SES 3 degats), meme si le collier est sur l'identite d'un autre ;
#  - 2 exemplaires : peuvent etre attaches a la MEME identite (ATK -2) ;
#  - homonyme `40092` : jamais cherche par nom.

def GetAbilities() -> Sequence['Ability']:

    def inhibitor_collar(targets: Sequence['CardFace'], effect: 'Effect'):
        this = effect.this.CastTo(Attachment)
        Unused(this)

        initiator = effect.GetInitiator()

        return initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust a character you control",
                lambda targets:
                    Faces.ExhaustAll(targets, effect)
            ).SetTarget("YouControlUnit", canbe_exhaust=True),
            AbilityFactory.ForChoiceAbility(
                "Take 3 damage",
                lambda targets:
                    initiator.GetIdentity().TakeDamage(this, 3, effect),
            ).SetTarget("YourIdentity"),
        ) != []


    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            "YourIdentity",
        ),
        *AbilityFactory.GiveKeywordToAttached(
            "Character",
            treat_as_blank=True,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.Action,
        ).SetCostFunc(CostFunc.Custom(None, inhibitor_collar))
        .AnyPlayerCanDoThis(),
    ]

