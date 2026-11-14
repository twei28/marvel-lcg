from . import *
# Vigilantism — TRAITRISE DETERRENCE (Boost 1 + [star]). When Revealed : if Batman is in play, Batman removes 2 threat among schemes, divided as you choose.
# This card gains surge. [star] Boost : give the enemy 1 additional boost card for this activation. If Batman is in play, Batman removes up to 2 threat
# from the main scheme.
# Reference : bm004 (une cible CHOISIE par point de menace).
def GetAbilities() -> Sequence['Ability']:
    def revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        MarquerResolue(this)
        joueur = JoueurRevelation(effect, message)
        ReactionDeSplitDecision(effect, joueur)
        batman = BatmanEnJeu(effect)
        if batman is not None and joueur is not None:
            for _ in range(2):
                complots = [f for f in Worlds.GetOnFieldCards(effect) if Scheme2.IsType(f) and f.threat > 0]
                if not complots:
                    break
                cible = joueur.AskChooseFace(complots, effect)
                batman.RemoveThreatFromSchemes([cible], 1, effect)
        SurgeDeLaDissuasion(effect)
    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        MarquerResolue(this)
        if not BoostSupplementaireAnnule(this):
            message.GiveBoostCardForThisActivation(Villain, 1, effect)
        batman = BatmanEnJeu(effect)
        principal = Worlds.FindMainScheme(effect)
        if batman is not None and principal is not None:
            batman.RemoveThreatFromSchemes([principal], 2, effect)
    return [
        AbilityFactory.WhenThisRevealed(None, revealed),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
