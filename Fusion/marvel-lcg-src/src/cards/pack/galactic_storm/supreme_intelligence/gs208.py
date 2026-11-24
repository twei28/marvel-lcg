from . import *

# Summon Reinforcements — TRAITRISE (Supreme Intelligence), x2. 2 icones de boost.
# When Revealed: If there is at least 1 STARFORCE minion set aside, the villain schemes. Otherwise, discard
#   cards from the top of the encounter deck until a minion is discarded and reveal it.
#
# Cartes de reference :
#  - « the villain schemes » : **`skrull_menace/standard_skrull/sk257`** (`mechant.DoSchemes(joueur, effect)`).
#  - « discard ... until a minion is discarded and reveal it » : **`baxter_stockman/tx009`** /
#    **`skrull_elite_crusader/sk233`** (`Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)` puis
#    `face.Reveal(joueur, effect)`).
#  - « set aside STARFORCE minion » : helper `SbiresStarforceMisDeCote` (gs198b).
#
# ⚠ Mots-pieges : « AT LEAST 1 STARFORCE minion SET ASIDE » (zone mise de cote, pas en jeu ; Supremor compte
# dans la lecture Q1) ; « the VILLAIN schemes » (contre le joueur qui revele) ; « Otherwise » ; « REVEAL it »
# (ses « When Revealed » partent, il s'engage avec le joueur) ; deck et defausse sans sbire : rien.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if SbiresStarforceMisDeCote(effect):
            mechant = LeMechant(effect)
            if mechant is not None:
                mechant.DoSchemes(joueur, effect)
            return
        sbire = Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)
        if sbire is not None:
            sbire.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
