from . import *

# Perception Manipulation (x2 : hf342, hf343). Attachement ILLUSION PSIONIC, [star] Boost (0 icone). « Attach to your identity. Attached character cannot be readied.
# Alter-Ego Action : Spend [mental][mental] -> discard this card. [star] Boost : Change your form (flip your identity card). »
# Icone du cout « noeuds relies » = [mental] (`Cost("B")`, lue contre hf110 / rm004). Cartes de reference : hf305 Psychic Mirage (`AttachToFaceWhenPutIntoPlay("YourIdentity")` +
# `CardCannotReady("AttachedCharacter")`), 02020 / hf110 (`PlayerActionToDiscardThis(...).SetCost(Cost(...))`), `identite.ChangeToOtherIdentityForm(effect)` (identity.py).
# ⚠ « Spend [mental][mental] » : DEUX ressources mentales (`Cost("BB")`) ; l'action est celle de l'ALTER-EGO ; « cannot be readied » : l'identite ne se redresse plus
# (pendant la phase des joueurs ET a la fin du round).


def GetAbilities() -> Sequence['Ability']:
    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity() if joueur is not None else None
        if identite is not None:
            identite.ChangeToOtherIdentityForm(effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        *AbilityFactory.CardCannotReady("AttachedCharacter"),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.AlterEgoAction).SetCost(Cost("BB")),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
