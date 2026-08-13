from . import *

# Multiverse Shenanigans

def GetAbilities() -> Sequence['Ability']:

    # `Search.Collection` cherche dans TOUTE la base de cartes du jeu (44009,
    # Armed to the Teeth, en vit). Et `card_classes="Any"` vaut exactement
    # « n'importe quel aspect SAUF Determination » : la liste du moteur nomme
    # les cinq aspects officiels. C'est mot pour mot ce que demande la carte.
    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        this = effect.this.CastTo(Upgrade)

        player = this.GetControlByPlayer()
        if player is None:
            return
        for _ in range(3):
            face = Search.Collection(effect, player, card_classes="Any")
            if face is None:
                break
            this.TuckCardUnderHere(face, effect)

    def multiverse_shenanigans(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)

        player = this.GetControlByPlayer()
        mises_de_cote = list(this.GetPlacedCardArea().Get())
        if player is None or not mises_de_cote:
            return
        face = player.MayChooseOneText(mises_de_cote)
        if face:
            player.GainCard(face, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenGameBeginSetup(mise_en_place).NoOutOfPlayLimit(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            multiverse_shenanigans
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.DealPlayerEncounterCard(1, "Initiator")),
    ]
