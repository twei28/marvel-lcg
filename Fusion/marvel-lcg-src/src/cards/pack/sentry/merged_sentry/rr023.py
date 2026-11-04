from . import *

# Scourge Blast : TRAHISON, boost 1 (x3). Set « Merged Sentry ».
# When Revealed: If Merged Sentry is in play, place 1 overwhelm counter on him. Take 1 indirect damage for each overwhelm counter on Merged Sentry. Otherwise, this card gains surge.
# ★ Boost: If this activation is an attack, this card gets +2 boost icons for this attack and this attack gains piercing.
#
# CARTES DE REFERENCE
#  - `ca018` (boost : `WhenCardBecomeBoost("This", op)` + `message.GainBoostIcon(n, effect)`) ; `ca014` (`this.DealIndirectDamage(identite, n, effect)`) ; surge `this.GainSurge(1, effect)`.
#
# TEXTE CONTRE CODE
#  « place 1 counter THEN take 1 indirect damage FOR EACH counter » : le compteur est pose AVANT le calcul. Sans Merged Sentry : surge seulement. Boost : seulement quand l'activation est une ATTAQUE (pas une manigance) ; +2 icones ET perforation.
#  ⚠ La perforation passe par `would_message.property.piercing` (champ de l'AttackProperty de l'activation) : lecture au mieux, mesuree par le cas.


def GetAbilities() -> Sequence['Ability']:

    def scourge_blast(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        merged = Worlds.FindCardOnField(effect, name=NOM_MERGED, card_type=Minion)
        if merged is None or joueur is None:
            this.GainSurge(1, effect)
            return
        Faces.PlaceCountersOn([merged], 1, NOM_SUBMERSION, effect)
        n = merged.GetCounters(NOM_SUBMERSION)
        if n > 0:
            this.DealIndirectDamage(joueur.GetIdentity(), n, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        propriete = message.would_message.property
        if isinstance(propriete, AttackProperty):
            message.GainBoostIcon(2, effect)
            propriete.piercing = True

    return [
        AbilityFactory.WhenThisRevealed(None, scourge_blast),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
