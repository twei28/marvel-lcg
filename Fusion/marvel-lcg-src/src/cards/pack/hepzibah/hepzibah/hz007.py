from . import *
# Feral Rage (x3). Evenement ATTACK SKILL, cout 1.
#
# Hero Action (attack): Deal damage to an enemy equal to your ATK.
# Special: Hepzibah gets +1 ATK until the end of the player phase.
#
# Cartes de reference : 10002 Crushing Blow / 25018 (`DealDamage(.., hero.attack, ..)`), 14022 (`GainUntilPhaseEnd(effect, attack=1)`),
# ze003 (Special nomme, `.NoOutOfPlayLimit()` : il se resout depuis la MAIN).
def GetAbilities() -> Sequence['Ability']:
    def feral_rage(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        hero = effect.GetInitiator().GetHero()
        this.DealDamage(effect.targets, hero.attack, effect)
    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = JoueurDuSpecial(effect, message)
        hero = joueur.GetHero() if joueur is not None else None
        if hero is not None:
            # « until the end of the PLAYER phase » : resolu en phase du mechant (Special via Feline Grace en defense), le bonus tient jusqu'a la
            # fin de la phase des joueurs SUIVANTE (RR « Lasting Effects ») ; sans `end_phase`, il tombait a la fin de la phase du mechant
            # (corrige le 26/10/2026 ; meme parametre que 62015 Take a Stand).
            hero.GainUntilPhaseEnd(effect, attack=1, end_phase="Player")
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            feral_rage,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
        AbilityFactory.WhenResolveSpecialAbility("This", special).NoOutOfPlayLimit(),
    ]
