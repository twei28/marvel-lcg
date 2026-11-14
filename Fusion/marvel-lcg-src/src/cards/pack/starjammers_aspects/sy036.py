from . import *
# Decisive Action (Leadership, evenement 3 [energy]). ATTACK. THWART. Requirement ([energy][mental][physical]).
# Hero Action: Your hero gets +1 ATK and +1 THW until the end of the phase. Make a basic attack without exhausting. Make a basic thwart
# without exhausting.
#
# Cartes de reference : 61023 Grapnel Launcher (`hero.BasicThwart(cibles, effect)` n'epuise pas ; « without exhausting (even if you are
# exhausted) » acquis) ; wt006 (`GainUntilPhaseEnd(effect, attack=1, thwart=1)`) ; us004 (cibles d'une carte a deux effets : `SetTarget(Enemy)`
# + `SetTarget2(Scheme2)`).
# ⚠ « Your HERO » : la face heros (Hero Action) ; les +1 sont accordes AVANT l'attaque et le contre (« gets +1 ATK and +1 THW until the end
# of the phase » : ils comptent pour les deux pouvoirs de base de CETTE carte). Pas de libelle imprime : « Hero Action » nu.
def GetAbilities() -> Sequence['Ability']:
    def decisive_action(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        heros = effect.GetInitiator().GetHero()
        if heros is None:
            return
        heros.GainUntilPhaseEnd(effect, attack=1, thwart=1)
        heros.BasicAttack(effect.targets, effect)
        heros.BasicThwart(effect.targets2, effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            decisive_action,
        ).SetPlay()
        .SetTarget(Enemy)
        .SetTarget2(Scheme2),
    ]
