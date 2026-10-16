from . import *

# Shredder's Wrath (2B) — COMPLOT PRINCIPAL, face B. Menace de depart 2[per_hero],
# cible 10[per_hero], escalade +1[per_hero].
# When Revealed: Give each enemy a tough status card.
# Forced Response: After Shredder schemes, give Shredder a cloaked status card.
# If this scheme is completed, the players lose the game.
#
# Cartes de reference : `Faces.GiveStatus(Worlds.GetOnFieldEnemies(effect), ...)`
# (aoa 45092 pour GiveStatus Tough) ; `AfterUnitSchemeEnd` (bkw 08012) pour
# « after X schemes ». « If this scheme is completed, the players lose » : lu
# par le moteur sur le complot principal (aucun script, comme 01097b).
#
# Mots-pieges : « EACH enemy » = vilain ET sbires (Worlds.GetOnFieldEnemies) ;
# « after SHREDDER schemes » : seulement quand Shredder manigance, pas un sbire.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Faces.GiveStatus(Worlds.GetOnFieldEnemies(effect), "Tough", effect)

    def shredder_manigance(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        Cloak(effect, TrouverShredder(effect))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.AfterUnitSchemeEnd(
            AbilityType.ForcedResponse,
            CardFinder(card_ids=IDS_SHREDDER),
            shredder_manigance,
        ),
    ]
