from . import *

# Protect Students (obligation, Boost 2). « Your hero gets -1 ATK, and -1 DEF. Alter-Ego Action : Exhaust your identity and reveal 1 card from the Hellfire deck
# -> heal 1 damage from each friendly character in play. Discard this card. »
# Cartes de reference : 04166 Anti-Hero Propaganda (`GiveKeywordToInPlayWhenApplyThis(Hero, attack=-1, defense=-1)` + `PlayerActionToDiscardThis`), 40160 Manufactured
# Drama (obligation sans `GiveTo`, `control_by="You"`), im009 (`CostFunc.Custom(None, fn)` : cout arbitraire, `False` bloque le paiement).
# ⚠ « Your hero » : le heros du joueur qui porte l'obligation (`control_by="You"`), pas tous les heros de la table. « friendly character » : identites ET allies
# de TOUS les joueurs (`Worlds.GetOnFieldFriendlyCharacters`). « reveal 1 card from the Hellfire deck » est une PARTIE DU COUT (avant la fleche) : le sbire est
# revele devant le joueur qui agit ; deck ET defausse Hellfire vides : le cout ne peut pas etre paye.


def GetAbilities() -> Sequence['Ability']:
    def soigner(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this
        Unused(message)
        this.HealthUnits(Worlds.GetOnFieldFriendlyCharacters(effect), 1, effect)
        Faces.DiscardAll([this], effect)

    def reveler(targets: 'Sequence[CardFace]', effect: 'Effect') -> bool:
        joueur = effect.GetInitiator()
        if joueur is None or DessusDuDeckHellfire(effect) is None:
            return False
        RevelerDuDeckHellfire(effect, joueur)
        return True

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(Hero, control_by="You", attack=-1, defense=-1),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, soigner)
        .SetCostFunc(CostFunc.Exhaust("YourIdentity"))
        .SetCostFunc(CostFunc.Custom(None, reveler)),
    ]
