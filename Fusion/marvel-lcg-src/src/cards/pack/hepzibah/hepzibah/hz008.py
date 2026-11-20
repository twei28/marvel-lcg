from . import *
# Keen Senses (x3). Evenement SKILL THWART, cout 1.
#
# Hero Action (thwart): Remove 2 threat from a scheme. If this removes the last threat on that scheme, ready Hepzibah.
# Special: Remove 1 threat from a scheme.
#
# Cartes de reference : 01023 Legal Practice (`RemoveThreatFromSchemes`, `SetTarget(Scheme2)`), 01024 One-Two Punch (`Faces.ReadyAll`),
# ze003 (Special nomme depuis la main). « the LAST threat » : menace avant > 0 et menace apres == 0.
def GetAbilities() -> Sequence['Ability']:
    def keen_senses(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        cible = effect.targets[0] if effect.targets else None
        avant = cible.threat if cible is not None else 0
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)
        if cible is not None and avant > 0 and cible.threat <= 0:
            Faces.ReadyAll([joueur.GetIdentity()], effect)
    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Event)
        joueur = JoueurDuSpecial(effect, message)
        intrigues = Intrigues(effect)
        if joueur is None or not intrigues:
            return
        cible = joueur.AskChooseFace(intrigues, effect, prompt="Remove 1 threat from a scheme")
        if cible:
            this.RemoveThreatFromSchemes([cible], 1, effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            keen_senses,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
        AbilityFactory.WhenResolveSpecialAbility("This", special).NoOutOfPlayLimit(),
    ]
