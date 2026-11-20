from . import *

# Punisher's RPG — ATTACHEMENT. ARMAMENT. WEAPON. ATQ +2★, Boost 2, Uses (1+1 par joueur ammo).
# Attach to Punisher. Uses (1+1[per hero] ammo counters).
# When Revealed : Discard each other ARMAMENT card in play.
# ⚠ « indirect » : le degat indirect se repartit entre les personnages d'un JOUEUR ; contre un ENNEMI (Target Lock) l'attaque reste
# normale (sinon le moteur l'annule : ni degats ni « after attacks »). Condition posee sur les cibles de l'attaque.
# ★ Punisher's attacks deal indirect damage. Exhaust any character damaged by his attack.
# ★ Forced Response : After Punisher attacks, remove 1 ammo counter from here.
#
# Cartes de reference : punishers_armory/pu115 et pu117, sk166 (`UnitAttackGainKeyword(indirect_damage=True)`),
# `Faces.ExhaustAll(took_damage_targets)`.

from ..punishers_armory import DefausserLesAutresArmements

def GetAbilities() -> Sequence['Ability']:

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        blesses = list(message.took_damage_targets)
        if blesses:
            Faces.ExhaustAll(blesses, effect)
        Faces.RemoveCountersOn([effect.this], 1, 'ammo', effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Punisher", card_type=Villain)),
        AbilityFactory.WhenThisRevealed(None, DefausserLesAutresArmements),
        AbilityFactory.UnitAttackGainKeyword(
            "AttachedCharacter", indirect_damage=True,
            conditions=[lambda effect, message: all(not Enemy.IsType(c) for c in message.attacked)],
        ),
        AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, "AttachedCharacter", None, apres_attaque),
    ]
