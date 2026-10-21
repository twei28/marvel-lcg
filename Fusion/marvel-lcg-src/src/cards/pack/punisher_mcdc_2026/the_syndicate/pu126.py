from . import *

# * White Rabbit — SBIRE UNIQUE. CRIMINAL. SYNDICATE. SCH 2, ATQ 2★, 3 PV, Boost 2.
# ★ Forced Response : After White Rabbit attacks and damages you, discard a card you control from play.
# When Defeated : voir __init__.py.
#
# Cartes de reference : jigsaw/pu064.py et 27099 (`AfterUnitAttackAndDamageUnit(ForcedResponse, "This", "You")`),
# `commun.CartesQueTuControles`.
# ⚠ « a card YOU control FROM PLAY » : allies, ameliorations, soutiens du joueur attaque (pas la main, pas
# l'identite) ; le joueur choisit ; rien a defausser = rien. ATQ « ★ » : `desc.ATK = 0**`.

def GetAbilities() -> Sequence['Ability']:

    def apres_blessure(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        joueur = message.GetToPlayer()
        candidates = CartesQueTuControles(joueur)
        if not candidates:
            return
        choisie = candidates[0] if len(candidates) == 1 else joueur.AskChooseFace(candidates, effect)
        if choisie is not None:
            Faces.DiscardAll([choisie], effect)

    return [
        AbilityFactory.AfterUnitAttackAndDamageUnit(AbilityType.ForcedResponse, "This", "You", apres_blessure),
        DefaiteSyndicate(),
    ]
