from . import *

# Borrowed Gear

def GetAbilities() -> Sequence['Ability']:

    def nombre_d_ameliorations(effect: 'Effect', attach: 'CardFace', ui: List['CardFace']) -> int:
        return min(4, len(attach.GetAttachedUpgrades()))

    def borrowed_gear(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Upgrade)

        initiator = effect.GetInitiator()
        allies = initiator.discard_pile.FindCards(card_type=Ally)
        if not allies:
            return
        face = initiator.MayChooseOneText(allies)
        if face is None:
            return
        this.TuckCardUnderHere(face, effect)

        # « l'allie attache gagne les TRAITS de l'allie face cachee » : le
        # moteur donne un trait a la fois, d'ou la boucle.
        porteur = this.GetBindFace()
        if porteur is None:
            return
        for trait in face.traits:
            this.effect.Register(
                AbilityFactory.GiveKeywordToAttached(
                    Ally,
                    trait=trait,
                )
            )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Ally)
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Ally,
            health=nombre_d_ameliorations,
            ex_change_on_event=OnEvent.CardInPlay(Upgrade),
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            borrowed_gear
        ),
    ]
