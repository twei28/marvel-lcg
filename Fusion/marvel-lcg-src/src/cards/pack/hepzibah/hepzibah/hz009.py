from . import *
# Feline Grace (x2). Evenement DEFENSE SKILL, cout 0.
#
# Hero Interrupt (defense): When you would take any amount of damage from an attack, prevent 4 of that damage.
# Special: Ready Hepzibah. (Limit once per phase.)
#
# Cartes de reference : kb003 Evasive Shot (`WhenUnitWouldTakeDamage(HeroInterrupt, "You", .., is_from_attack=True)` + `PreventDamage(4)`),
# ze003 (Special nomme depuis la main).
# ⚠ « Limit once per phase » d'un Special resolu depuis la MAIN : un marqueur (round, phase) pose sur LA CARTE (la meme copie ne
# redresse pas deux fois dans la phase) ; `LimitOncePerPhase()` ne vaut pas pour une carte hors jeu.
def GetAbilities() -> Sequence['Ability']:
    def feline_grace(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        message.PreventDamage(4, effect)
    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Event)
        joueur = JoueurDuSpecial(effect, message)
        marque = (effect.world.round_id, effect.world.phase_id)
        if joueur is None or getattr(this, "hz_grace_phase", None) == marque:
            return
        this.hz_grace_phase = marque
        Faces.ReadyAll([joueur.GetIdentity()], effect)
    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            feline_grace,
            is_from_attack=True,
        ).SetPlay().SetLabel('defense'),
        AbilityFactory.WhenResolveSpecialAbility("This", special).NoOutOfPlayLimit(),
    ]
