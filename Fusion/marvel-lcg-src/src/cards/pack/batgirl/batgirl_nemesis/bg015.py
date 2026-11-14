from . import *

# * Black Mask — sbire, PV 4, ATQ 2, boost 1, Incite 1 (desc), nemesis de Batgirl. « [star] Black Mask's SCH is equal to the number of
# cards with a printed [mental] resource in the engaged player's hand. If his SCH is 0, the engaged player is dealt a facedown
# encounter card when Black Mask schemes. »
# Cartes de reference : `27154` (`ThisGainKeyword(.., change_on_event=OnEvent.HandCards("EngagedPlayer"))`), `rz020` (WhenUnitWouldScheme),
# `53009` Aerial Recon (`DealEncounterCard` face cachee).


def GetAbilities() -> Sequence['Ability']:

    def valeur(effect: 'Effect', ui: List['CardFace']) -> int:
        this = effect.this.CastTo(Minion)
        joueur = this.GetEngagedPlayer()
        if joueur is None:
            return 0
        cartes = CartesDeLaMain(joueur, "B")
        ui.extend(cartes)
        return len(cartes)

    def black_mask(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        this = effect.this.CastTo(Minion)
        joueur = this.GetEngagedPlayer()
        if joueur is None or len(CartesDeLaMain(joueur, "B")) > 0:
            return
        joueur.DealEncounterCards(1, effect)

    return [
        AbilityFactory.ThisGainKeyword(
            valeur,
            scheme=1,
            change_on_event=OnEvent.HandCards("EngagedPlayer"),
        ),
        AbilityFactory.WhenUnitWouldScheme(AbilityType.ForcedInterrupt, "This", black_mask),
    ]
