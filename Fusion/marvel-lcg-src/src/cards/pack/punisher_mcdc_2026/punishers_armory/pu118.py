from . import *

# Frag Grenade — TRAITRISE. WEAPON. Boost 1.
# When Revealed : Take 3 indirect damage. You may discard a card you control to prevent X of this damage, where X is
#   equal to that card's cost.
#
# Cartes de reference : fne/the_getaway/60133.py (`TakeIndirectDamage`), skrull_menace/lyja/sk063.py (`MayChooseFace`),
# `commun.CartesQueTuControles`.
# ⚠ « a card you control » : EN JEU (allies, ameliorations, soutiens), pas la main ; X = cout imprime (0 si pas de cout) ;
# « prevent X OF this damage » : les degats tombent a max(0, 3 - X) ; on defausse la carte meme si X = 0 (le joueur ne
# la choisira pas).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        degats = 3
        candidates = CartesQueTuControles(joueur)
        if candidates:
            choisie = joueur.MayChooseFace(candidates, effect, not_move=True)
            if choisie is not None:
                cout = getattr(getattr(choisie, 'printed_cost', None), 'val', 0)
                Faces.DiscardAll([choisie], effect)
                degats = max(0, degats - cout)
        if degats > 0:
            joueur.GetIdentity().TakeIndirectDamage(this, degats, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
