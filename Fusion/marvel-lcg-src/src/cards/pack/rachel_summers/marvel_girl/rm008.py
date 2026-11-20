from . import *

# * Askani — AMELIORATION (titre), cout 3 (energie), unique. TITLE.
# Alter-Ego Action: Exhaust Askani -> shuffle the top three cards from your discard pile into your deck.
# Interrupt: When you would be defeated, set your hit point dial to 1 instead. Then, discard this card.
#
# CARTES DE REFERENCE : `14007` Serval Industries (`Faces.ShuffleAllTo(cartes, joueur.player_deck, effect)`), `35006` « I Got
# Better » et `03008` Captain America's Helmet (`WhenUnitWouldBeDefeated` + `SetBeInstead` + `SetHealth(1)` + defausse).
#
# MOTS-PIEGES : « the TOP three » = les trois DERNIERES cartes entrees dans la defausse (indice -3 et suivants) ; « When YOU
# would be defeated » = l'identite, par n'importe quelle cause ; « Then, discard this card ».
def GetAbilities() -> Sequence['Ability']:
    def melanger(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        initiator = effect.GetInitiator()
        dessus = list(initiator.discard_pile.Get())[-3:]
        if dessus:
            Faces.ShuffleAllTo(dessus, initiator.player_deck, effect)

    def askani(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        heros = effect.targets[0].CastTo(Unit2)
        message.SetBeInstead(effect)
        heros.SetHealth(1, effect)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            melanger,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.Interrupt,
            "You",
            askani,
        ).SetTarget("YourIdentity"),
    ]
