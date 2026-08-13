from . import *

# * Colleen Wing

def GetAbilities() -> Sequence['Ability']:

    def misty_en_jeu(effect: 'Effect', ui: List['CardFace']) -> int:
        misty = Worlds.FindCardOnField(effect, finder=CardFinder(name="* Misty Knight"))
        if misty:
            ui.append(misty)
            return 1
        return 0

    def attaque_une_cible_avec_bounty(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        this = effect.this.CastTo(Ally)

        cible = message.target
        if cible.GetInventoryDeck().FindCard(name="Bounty"):
            this.GainForThisActive(effect, message, attack=1)

    return [
        Fragile(),
        AbilityFactory.ThisGainKeyword(
            misty_en_jeu,
            thwart=1,
            change_on_event=OnEvent.CardInPlay(Ally)
        ),
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.NonKeyword,
            "This",
            None,
            attaque_une_cible_avec_bounty,
        ),
    ]
