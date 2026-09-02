from . import *

# Dark Apotheosis — ATTACHEMENT NECROVERSE (×2). +1 MNG / +1 ATQ, 2 icones de
# boost.
#
# Attach to the enemy with the most hit points remaining.
# Hero Action: Spend [physical][mental] resources and discard the top 3 cards
#   of your deck → discard this card.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Attach to the enemy with the most hit points remaining » : le helper
#   `FindMostHpUnit` du pack trors (cite dans zola/__init__.py) fait
#   exactement ce tri ; `AttachToFaceWhenPutIntoPlay` accepte un `CardFinder`
#   dynamique via `check_effect_fn`, mais le plus simple et le plus lisible
#   est de passer une fonction de selection.
# - Les bonus +1 MNG / +1 ATQ sont IMPRIMES (`desc["ATK+"]`, `desc["SCH+"]`) :
#   bases automatiques, aucun script.
# - Action a cout mixte : meme montage que nv002.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « the enemy with the MOST HIT POINTS REMAINING » -> les PV RESTANTS, pas les
#   PV imprimes : un vilain blesse peut ceder la place a un sbire frais.
# « an ENEMY » -> vilain OU sbire, ce set modulaire n'est lie a aucun vilain.
# « Spend [physical][mental] AND discard the top 3 » -> cout a deux parties.


def GetAbilities() -> Sequence['Ability']:

    def ennemi_le_plus_solide(effect: 'Effect') -> Sequence['CardFace']:
        ennemis = Worlds.FindCardsOnField(effect, CardFinder(card_type=Enemy))
        if not ennemis:
            return []
        meilleur = max(ennemis, key=lambda e: e.health)
        return [meilleur]

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            ennemi_le_plus_solide
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("RB"))
        .SetCostFunc(CostFunc.DiscardDeckTopCards("YourDeck", 3)),
    ]
