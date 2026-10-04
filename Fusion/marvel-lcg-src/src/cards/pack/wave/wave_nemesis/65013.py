from . import *

# Alontech Hybrid — SBIRE, WAVE NEMESIS 3/5 et 4/5 (x2, meme card_id). SCH 1,
# ATK 2, HP 4. ALONTECH.
# SIRENA minions and villains cannot be attacked by the player Alontech
# Hybrid is engaged with.
#
# `AbilityFactory.UnitCannotBeAttacked(which_unit, conditions=[...])`
# (do_attack.py:990) restreint la CIBLE (`which_unit` compare a
# `message.being_attack`) ; il manque un moyen NATIF de filtrer l'ATTAQUANT
# sur « controle par le joueur engage AVEC CETTE carte », donc un
# `conditions=[...]` maison qui relit `effect.this.CastTo(Minion).
# engaged_player` (meme attribut que `ConditionPlayerType.CheckWhichPlayer`,
# "EngagedPlayer") et le compare au controleur de `message.attacker`
# (`CheckIfUnitCanBeAttackBy.attacker`, sender.py:104).
# DEUX capacites distinctes plutot qu'un filtre combine : « SIRENA minions »
# (trait) et « villains » (type, sans filtre de trait -- le vilain actif n'a
# pas necessairement le trait SIRENA) sont deux familles de cibles disjointes
# dans `CardFinder`.

def GetAbilities() -> Sequence['Ability']:

    def attaque_du_joueur_engage(effect: 'Effect', message: 'Message.CheckIfUnitCanBeAttackBy') -> bool:
        this = effect.this.CastTo(Minion)
        joueur_engage = this.engaged_player
        if joueur_engage is None:
            return False
        attaquant = message.attacker
        if attaquant is None:
            return False
        return attaquant.GetControlByPlayer() == joueur_engage

    return [
        AbilityFactory.UnitCannotBeAttacked(
            CardFinder(trait="SIRENA", card_type=Minion),
            conditions=[attaque_du_joueur_engage],
        ),
        AbilityFactory.UnitCannotBeAttacked(
            Villain,
            conditions=[attaque_du_joueur_engage],
        ),
    ]
