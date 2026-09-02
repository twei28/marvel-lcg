from . import *

# Blighted Chains — ATTACHEMENT NECROVERSE (×2 dans le set modulaire).
# 2 icones de boost.
#
# Attach to your identity.
# As an additional cost to use a hero's basic power, you must discard 1 random
#   card from your hand.
# Alter-Ego Action: Discard the top 2 cards of your deck → discard this card.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Attach to your identity » : `AttachToFaceWhenPutIntoPlay("YourIdentity")`
#   (attachment.py:47, qui accepte ce litteral tel quel).
# - « As an additional cost to use a hero's basic power » : trois fabriques
#   dediees, `AdditionalCostToAttack`, `AdditionalCostToThwart` et
#   `AdditionalCostToDefense` (ability/factory/additional_cost.py:51-80). Il
#   n'existe pas de cle unique « pouvoir de base » : le moteur les traite un
#   par un. `which_unit` = le HEROS attache, cible par "YourHero" : la carte
#   est posee sur l'identite, mais le cout ne frappe que ses pouvoirs de base
#   en forme heros.
# - Action qui se defausse elle-meme : 07020 (Ball and Chain),
#   `PlayerActionToDiscardThis(AbilityType.AlterEgoAction).SetCostFunc(...)`.
# - Cout « defausser le dessus du deck » : `CostFunc.DiscardDeckTopCards`
#   (cost_func.py:1079).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « to use A HERO'S BASIC POWER » -> les pouvoirs de base : ATQ, CTR et
#   parade. La RECUPERATION n'en est pas un ici (elle est propre a
#   l'alter-ego), et le moteur n'a pas de cout additionnel pour elle.
# « discard 1 RANDOM card » -> `CostFunc.Discard("RandomHandCard")`, le joueur
#   ne choisit pas.
# « ALTER-EGO Action » -> forme alter-ego seulement : la carte se retire donc
#   en changeant de forme, pas en heros.
# « Discard the top 2 cards of your deck → » -> c'est le COUT de l'action
#   (fleche), pas son effet. L'effet, c'est defausser cet attachement.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        AbilityFactory.AdditionalCostToAttack(
            CardFinder(card_type=Hero),
            CostFunc.Discard("RandomHandCard"),
        ),
        AbilityFactory.AdditionalCostToThwart(
            CardFinder(card_type=Hero),
            CostFunc.Discard("RandomHandCard"),
        ),
        AbilityFactory.AdditionalCostToDefense(
            CardFinder(card_type=Hero),
            CostFunc.Discard("RandomHandCard"),
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.AlterEgoAction,
        ).SetCostFunc(CostFunc.DiscardDeckTopCards("YourDeck", 2)),
    ]
