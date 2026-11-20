from . import *
# Family Matters, obligation. 2 icones de boost.
#
# Give to the Izzy Kane player. (desc.GiveTo, aucun script)
# Your hand size is reduced by 3.
# Alter-Ego Action: Exhaust Izzy Kane or Cannonball → discard Family Matters.
#
# Cartes de reference : gs031 Forgotten Life (`GiveKeywordToInPlayWhenApplyThis(.., hand_size=-1)` : obligation qui RESTE en jeu) ;
# ar010 Ire of Athena (« Exhaust A or discard B → discard this card » = DEUX `PlayerActionToDiscardThis(AlterEgoAction)`, un cout chacune ;
# RECETTES §5 « Deux couts alternatifs »).
# ⚠ « DISCARD Family Matters » (et non « remove from the game ») : l'obligation retourne a la defausse rencontre.
def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            hand_size=-3,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.AlterEgoAction,
        ).SetName("Exhaust Izzy Kane")
        .SetCostFunc(CostFunc.Exhaust("YourIdentity")),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.AlterEgoAction,
        ).SetName("Exhaust Cannonball")
        .SetCostFunc(CostFunc.Exhaust(name="Cannonball", card_type=Ally, from_where=["YouControlCards"])),
    ]
