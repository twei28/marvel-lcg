from . import *

# Flaming Sword — ATTACHEMENT. ARME. ATQ +1★, Boost 2. Attach to Hobgoblin.
# ★ Hobgoblin's attacks gain piercing.
# Hero Action : Exhaust your hero and resolve the "Pumpkin Bomb" ability twice → discard this card.
#
# Cartes de reference : jigsaw/pu058.py (attache + action de defausse a cout), galactic_storm/kree_sentry/gs083.py
# (`UnitAttackGainKeyword("AttachedCharacter", piercing=True)`), ares/ares/ar010.py (`CostFunc.Exhaust("YourIdentity")`).
#
# ⚠ « Exhaust YOUR HERO » : l'identite en forme HEROS (une Hero Action n'existe qu'en forme heros) ; « resolve ...
# twice » : deux Pumpkin Bomb d'affilee, avant la defausse.

def GetAbilities() -> Sequence['Ability']:

    def deux_bombes(effect: 'Effect', message: 'Message2') -> None:
        ResoudrePumpkinBomb(effect, effect.GetInitiator(), 2)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Hobgoblin", card_type=Villain)),
        AbilityFactory.UnitAttackGainKeyword("AttachedCharacter", piercing=True),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
            ex_operation=deux_bombes,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
