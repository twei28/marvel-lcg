from . import *
# Smoke Cloud — TRAITRISE DETERRENCE ([star] seul). When Revealed : confuse an enemy. This card gains surge. [star] Boost : give the enemy 1 additional
# boost card for this activation. If the enemy is attacking, reduce the damage dealt by this activation by 2. If the enemy is scheming, reduce the
# threat placed by this activation by 2.
# Reference : bm018 ; `Faces.GiveStatus(..., "Confused", effect)` (01028 : "Stunned").
def GetAbilities() -> Sequence['Ability']:
    def revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        MarquerResolue(this)
        joueur = JoueurRevelation(effect, message)
        ReactionDeSplitDecision(effect, joueur)
        cible = ChoisirUnEnnemi(joueur, effect) if joueur is not None else None
        if cible is not None:
            Faces.GiveStatus([cible], "Confused", effect)
        SurgeDeLaDissuasion(effect)
    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        MarquerResolue(this)
        if not BoostSupplementaireAnnule(this):
            message.GiveBoostCardForThisActivation(Villain, 1, effect)
        ReduireLActivation(message, 2)
    return [
        AbilityFactory.WhenThisRevealed(None, revealed),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
