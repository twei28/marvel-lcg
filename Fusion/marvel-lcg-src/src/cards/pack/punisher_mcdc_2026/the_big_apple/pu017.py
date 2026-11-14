from . import *

# Conflicting Evidence — TRAITRISE. Boost 2.
# When Revealed (Alter-Ego) : The villain attacks you. Do not give them a boost card for this attack.
# When Revealed (Hero) : The villain schemes. Do not give them a boost card for this scheme.
#
# Cartes de reference : punishers_hit_list/pu110.py (`DoAttackYou(..., AttackProperty(against_player=joueur, do_not_give_boost=True))`),
# gmw/16116.py (`DoSchemes(joueur, effect, property=SchemeProperty(...))`), sender `SchemeProperty.do_not_give_boost`.
# ⚠ « the villain » = le CAPO du territoire du joueur qui revele (`LeVilain`, R6) ; « attacks YOU » / « schemes » : contre ce joueur ;
# « them » (neutre) = le vilain ; la forme est celle du joueur qui revele.

def GetAbilities() -> Sequence['Ability']:

    def alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        vilain = LeVilain(effect, joueur)
        if vilain is not None:
            vilain.CastTo(Enemy).DoAttackYou(joueur, effect, property=AttackProperty(against_player=joueur, do_not_give_boost=True))

    def heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        vilain = LeVilain(effect, joueur)
        if vilain is not None:
            vilain.CastTo(Enemy).DoSchemes(joueur, effect, property=SchemeProperty(against_player=joueur, do_not_give_boost=True))

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", alter_ego),
        AbilityFactory.WhenThisRevealed("Hero", heros),
    ]
