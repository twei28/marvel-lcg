from . import *

# Puncture Wound
# Attach to an enemy that Wolverine or Honey Badger attacked this turn.
# Attached enemy gets -1 ATK.
# Forced Response: After the player phase begins, discard this card and deal
#   3 damage to attached enemy.
#
# Copie de Puncture Wound (43012). Le modele relisait l'historique des
# attaques du tour en comparant des NOMS ; on exige en plus que l'attaquant
# soit le tien, sinon une attaque du Wolverine officiel d'un autre joueur
# rendrait cette carte jouable.


def GetAbilities() -> Sequence['Ability']:

    def puncture_wound(effect: 'Effect', message: 'Message.AfterPhaseBegin') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        enemy = this.GetBindFace()

        Faces.DiscardAll([this], effect)
        this.DealDamage([enemy], 3, effect)

    def puncture_wound_check(effect: 'Effect', face: 'CardFace') -> bool:
        world = effect.world

        for unit, _, targets in world.stat.this_turn_made_attack:
            if not (unit.IsName(NOM_HEROS) or unit.IsName(NOM_SOEUR)):
                continue
            if unit.GetControlByPlayer() != effect.GetInitiator():
                continue
            if face in targets:
                return True
        return False

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(
                card_type=Enemy,
                check_effect_fn=puncture_wound_check
            )
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Enemy,
            attack=-1,
        ),
        AbilityFactory.AfterPhaseBegin(
            AbilityType.ForcedResponse,
            "Player",
            puncture_wound
        ),
    ]
