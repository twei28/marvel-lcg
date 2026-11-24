from . import *
# Sudden Strike — TRAITRISE DETERRENCE (Boost 1 + [star]). When Revealed : if Batman is in play, Batman deals 3 damage to an enemy of your choice. This card
# gains surge. [star] Boost : give the enemy 1 additional boost card for this activation. If Batman is in play, Batman deals the activating enemy 2 damage.
# Reference : 01164 Titania's Fury (WhenThisRevealed + WhenCardBecomeBoost, `GiveBoostCardForThisActivation`).
def GetAbilities() -> Sequence['Ability']:
    def revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        MarquerResolue(this)
        joueur = JoueurRevelation(effect, message)
        ReactionDeSplitDecision(effect, joueur)
        batman = BatmanEnJeu(effect)
        if batman is not None and joueur is not None:
            cible = ChoisirUnEnnemi(joueur, effect)
            if cible is not None:
                batman.DealDamage([cible], 3, effect)
        SurgeDeLaDissuasion(effect)
    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        MarquerResolue(this)
        if not BoostSupplementaireAnnule(this):
            message.GiveBoostCardForThisActivation(Villain, 1, effect)
        batman = BatmanEnJeu(effect)
        if batman is not None and message.activating_enemy is not None:
            batman.DealDamage([message.activating_enemy], 2, effect)
    return [
        AbilityFactory.WhenThisRevealed(None, revealed),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
