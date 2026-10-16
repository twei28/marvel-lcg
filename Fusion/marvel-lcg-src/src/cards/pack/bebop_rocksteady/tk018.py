from . import *

# Ole!  (Hinder 1[per_hero] est lu dans desc)

def GetAbilities() -> Sequence['Ability']:

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this
        vilains = VilainsEnJeu(effect)
        avant = {id(v): v.health for v in vilains}
        this.DealDamage(vilains, 2 * Worlds.GetPlayerNum(effect), effect)
        # « Stun each ENRAGED villain damaged this way » : lu APRES les degats (un
        # Special peut avoir retourne le Temper pendant la resolution).
        a_etourdir = [v for v in vilains if v.IsInPlay() and v.health < avant[id(v)] and v.HasTrait("ENRAGED")]
        if a_etourdir:
            Faces.GiveStatus(a_etourdir, "Stunned", effect)

    return [
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
        BoostReveleCetteCarte(),
    ]
