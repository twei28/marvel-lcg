from . import *
# Shadow of the Bat — TRAITRISE DETERRENCE ([star] seul). When Revealed : if Batman is in play, choose one : draw a card or ready a card. This card gains
# surge. [star] Boost : if Batman is in play, prevent all threat and damage from this activation.
# Reference : bg007 (`ChooseAbilities` a deux options), 01035 (`SetTarget(..., canbe_ready=True)`), bm019 (ReduireLActivation).
def GetAbilities() -> Sequence['Ability']:
    def revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        MarquerResolue(this)
        joueur = JoueurRevelation(effect, message)
        ReactionDeSplitDecision(effect, joueur)
        if BatmanEnJeu(effect) is not None and joueur is not None:
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility("Draw a card", lambda t: joueur.DrawUp(1, effect)).SetHasNoTargetEffect(),
                AbilityFactory.ForChoiceAbility("Ready a card", lambda t: Faces.ReadyAll(t, effect)).SetTarget(canbe_ready=True),
            )
        SurgeDeLaDissuasion(effect)
    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        MarquerResolue(this)
        if BatmanEnJeu(effect) is not None:
            ReduireLActivation(message, 99)
    return [
        AbilityFactory.WhenThisRevealed(None, revealed),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
