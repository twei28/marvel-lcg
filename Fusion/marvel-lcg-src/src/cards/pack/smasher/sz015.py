from . import *
# Power Couple, evenement BASIQUE (Team-Up Cannonball / Smasher). Cout 2, [energy]. AERIAL. Max 1 par deck.
#
# Team-Up (Cannonball and Smasher). Max 1 per deck.   (desc.TeamUp, base automatique)
# Hero Action: Ready Smasher and Cannonball. They cannot take damage until the end of the round.
#
# Cartes de reference : hc020 Green Hell (Team-Up : le chargeur EXIGE `.SetTarget("TeamUp")` ; les deux personnages nommes deviennent les
# cibles) ; 29025 « Go for Champions! » (`RegisterTemp(UnitCannotTakeDamageWhile(Temp0, ..), unregister_after_exec=False, until_round_end=True)`).
# ⚠ Le nom « Power Couple » existe deja (jj022, Jessica Jones) : les deux cartes sont distinguees par leur card_id, jamais par le nom.
# ⚠ « They cannot take damage » : seulement les DEUX cibles du Team-Up (`m.trigger in cibles`), pas tout personnage de meme nom.
def GetAbilities() -> Sequence['Ability']:
    def power_couple(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        cibles = list(effect.targets)
        Faces.ReadyAll(cibles, effect)
        this.effect.RegisterTemp(
            AbilityFactory.UnitCannotTakeDamageWhile(
                AbilityType.Temp0,
                Unit2,
                conditions=[lambda e, m: m.trigger in cibles],
            ),
            unregister_after_exec=False,
            until_round_end=True,
        )
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            power_couple,
        ).SetPlay().SetLabel()
        .SetTarget("TeamUp"),
    ]
