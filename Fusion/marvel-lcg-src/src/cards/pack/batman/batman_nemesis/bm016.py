from . import *
# Heads I Win — TRAITRISE (Boost 2). When Revealed : discard the top 2 cards of the encounter deck. The player with the most remaining hit points takes
# indirect damage equal to the number of boost icons discarded this way. If a deterrence card was discarded this way, this card gains surge.
# Reference : nt015 / rescue_rainy 90128 (`DealIndirectDamage(identite, n, effect)`), `FacesCounter.CountTotalBoostIcons`.
# ⚠ Les cartes de dissuasion ainsi defaussees ne sont pas resolues : RangerSiNonResolue les remelange a la fin de CET effet. Leurs icones ne comptent
# pas : `IconesDesCartesDefaussees` lit a leur place le dessus de la defausse rencontre (livret de l'auteur, verdict du 26/10/2026).
def GetAbilities() -> Sequence['Ability']:
    def heads(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        deck = Worlds.GetEncounterDeck(effect)
        defaussees = list(deck.GetTops(2))
        if defaussees:
            Faces.DiscardAll(defaussees, effect)
        icones = IconesDesCartesDefaussees(effect, defaussees) if defaussees else 0
        joueurs = Worlds.GetPlayers(effect)
        if icones > 0 and joueurs:
            meilleur = max(j.GetIdentity().health for j in joueurs)
            ex_aequo = [j.GetIdentity() for j in joueurs if j.GetIdentity().health == meilleur]
            # Egalite : RR FIRST PLAYER, le premier joueur choisit parmi les cibles admissibles (verdict du 26/10/2026).
            cible = ex_aequo[0] if len(ex_aequo) == 1 else effect.world.GetFirstPlayer().AskChooseFace(ex_aequo, effect)
            if cible is not None:
                this.DealIndirectDamage(cible, icones, effect)
        if any(EstDissuasion(f) for f in defaussees):
            ThisCardGainSurge(effect)
    return [AbilityFactory.WhenThisRevealed(None, heads)]
