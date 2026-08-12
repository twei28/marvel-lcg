from . import *

# Bushman's Knife — custom « DesignHacker » (némésis de Moon Knight)
# Attach to Bushman, if able. If you cannot, attach to the minion with the
#   most remaining hit points.  (+2 ATK : clé desc « ATK+ », gérée nativement)
# [star] Attached character's attacks gain piercing.
# Hero Action: Spend a [physical] resource → discard this card.


def GetAbilities() -> Sequence['Ability']:

    # CORRECTIF 4/8/2026 : le piercing ne partait JAMAIS. La condition lisait le
    # porteur avec `this.GetAttachedUnit()`, methode qui n'existe pas, gardee par
    # un `hasattr` : elle renvoyait donc toujours None, sans lever d'erreur ni
    # laisser de trace. La cible `"AttachedMinion"` de `UnitAttackGainKeyword`
    # fait le travail nativement, comme Razor Claws 27059.

    def se_defausser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Attachment)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name="Bushman", card_type=Minion),
            if_cannot_attach_to=Minion,
            most_remaining_hp=True,
        ),
        AbilityFactory.UnitAttackGainKeyword(
            "AttachedMinion",
            piercing=True,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            se_defausser,
        ).SetName("Bushman's Knife")
        .SetCost(Cost("R")),
    ]
