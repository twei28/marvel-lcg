from . import *

# Hunted by the Past — ATTACHEMENT. SCH +1, ATQ +1 (desc), Boost 3.
# Attached minion gets +3 hit points.
# When Revealed : Find your nemesis minion, reveal it, and attach this card to it.
#
# Cartes de reference : punishers_hit_list/pu109.py (`Find.FindAndReveal` + `AttachTo2`), punishment/pu092.py (`GiveKeywordToAttached(..., health=...)`),
# `CardFinder(is_nemesis=joueur)` (game/card/card_finder).
# ⚠ « YOUR nemesis minion » : le sbire de l'ensemble nemesis du joueur qui revele (pas n'importe lequel) ; absent : rien (la carte reste sans porteur).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        nemesis = Find.FindAndReveal(effect, joueur, finder=CardFinder(card_type=Minion, is_nemesis=joueur))
        if nemesis is not None:
            this.AttachTo2(nemesis, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(Minion, health=3),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
