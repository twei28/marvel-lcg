from . import *

# Psychic Mirage. Attachement ILLUSION PSIONIC. « Attach to your identity. Uses (1 illusion counter). You cannot change form or ready your identity.
# When Revealed : ... Action : Discard an identity-specific card from your hand -> remove 1 illusion counter from here. »
# Cartes de reference : 02048 All Tied Up (`CardCannotReady("AttachedCharacter")` + `PlayersCannotChangeForms`), 36030 Claustrophobia (`PlayersCannotChangeForms(NonKeyword, "AttachedPlayer")`), 14024 (`CannotReady`),
# `CostFunc.Discard("YourHandCards", card_class="IdentitySpecific")`.


def GetAbilities() -> Sequence['Ability']:
    def action(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        RetirerUnCompteurIllusion(effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        PoserUnCompteurSiPsionique(),
        AbilityFactory.PlayersCannotChangeForms(AbilityType.NonKeyword, "AttachedPlayer"),
        *AbilityFactory.CardCannotReady("AttachedCharacter"),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, action).SetCostFunc(
            CostFunc.Discard("YourHandCards", card_class="IdentitySpecific", range=(1, 1))),
    ]
