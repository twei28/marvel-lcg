from . import *

# Weapon X Training

def GetAbilities() -> Sequence['Ability']:

    # « les allies que vous controlez A 1 PV RESTANT » : le bonus suit la sante,
    # il faut donc le recalculer a chaque changement de PV.
    def a_un_seul_pv(effect: 'Effect', face: 'CardFace') -> bool:
        this = effect.this.CastTo(Support)
        player = this.GetControlByPlayer()
        if player is None:
            return False
        return face.CastTo(Ally).GetControlByPlayer() == player \
            and face.CastTo(CanHealth).health == 1

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Ally, check_effect_fn=a_un_seul_pv),
            attack=2,
            attack_consequential_damage=2,
            change_on_event=OnEvent.Health(Ally),
        ),
    ]
