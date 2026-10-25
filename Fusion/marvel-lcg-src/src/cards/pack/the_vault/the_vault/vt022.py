from . import *

# Corrupted Guardsman — SBIRE x4 (TRAITOR). ATK 3, SCH 1, PV 4, 1 icone de boost + ★. Incite 1.
# When Revealed: If Inspection of the Vault is in play, reveal 1 random minion beneath The Vault. If you cannot, this card
#   gains surge.
# [star] Boost: Shuffle 1 minion beneath The Vault into the encounter deck.
#
# Cartes de reference :
#  - Incite 1 : natif (desc.Incite, fiche mots-cles/incite.md), aucun module.
#  - « reveal 1 random minion beneath The Vault » : `RevelerAuHasardSousLeVault(effect, joueur, Minion)` (helper du set) ;
#    « If you cannot, gains surge » : `ThisCardGainSurge` (modele gs189).
#  - « [star] Boost: Shuffle 1 minion beneath ... into the encounter deck » : `WhenCardBecomeBoost("This", ...)` +
#    `Faces.ShuffleAllTo([sbire], "EncounterDeck", effect)` (modele gs163 pour la forme du Boost).
#
# ⚠ Mots-pieges : « If you cannot » couvre AUSSI l'absence d'Inspection en jeu (arbitrage de l'utilisateur, 25/10/2026 : sans
# Inspection, le Guardsman gagne Surge) ; « random » = tirage seme du moteur ; le sbire du Boost est tire AU HASARD aussi
# (arbitrage de l'utilisateur, 25/10/2026) ; rien dessous = le Boost ne fait rien.


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        revele = None
        if InspectionEnJeu(effect):
            revele = RevelerAuHasardSousLeVault(effect, message.GetToPlayer(), Minion)
        if revele is None:
            ThisCardGainSurge(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        dessous = SbiresSousLeVault(effect)
        if dessous:
            Faces.ShuffleAllTo([Rand.RandomChoice(dessous, effect)], "EncounterDeck", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
