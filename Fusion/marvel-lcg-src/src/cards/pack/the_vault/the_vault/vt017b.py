from . import *

# The Vault Breakout (1B) — MANIGANCE PRINCIPALE, stade 1. Menace de depart 1[per_hero], seuil 6[per_hero][star], escalade
#   +1[per_hero].
# When Revealed: Reveal the top card of the villain deck.
# [star] Forced Interrupt: When this scheme would be completed, instead do each of the following:
#   1. Remove all but 1[per_hero] threat from here.
#   2. Reveal 1 random villain beneath The Vault.
#   3. Reveal Inspection of the Vault.
# (+ regle du livret p.1, non imprimee sur la carte : un vilain vaincu est retire de la partie, ses jetons, cartes d'etat et
#   attachements sont defausses ; apres le depart du dernier vilain, on revele le dessus du deck de vilains.)
#
# Cartes de reference :
#  - « When this stage would be completed, ... instead » : `WhenMainSchemeStageWouldBeCompleted` + `message.SetBeInstead`
#    (modele gs118b Majestrix's Verdict, sk145b) ; « remove all but N threat » : `RemoveThreatFromSchemes([this], n, effect,
#    ignore_crisis=True)` (modele gs118b).
#  - « Reveal 1 random villain beneath The Vault » : `RevelerAuHasardSousLeVault` (helper du set, `Card.Reveal`) ; « Reveal
#    Inspection » : `SetupCards.Reveal(..., only_set_aside=True)` (Obligation donnee au premier joueur : `GiveTo` de vt019).
#  - Retrait du vilain vaincu : `AfterUnitBeDefeated(ForcedResponse, Villain, ...)` + `Villains.Remove` (modele gs161b), puis
#    `ApresDepartDUnMechant` (reveler le suivant, ou la victoire).
#
# ⚠ Mots-pieges : « all BUT 1 per hero » : on ne retire que l'exces, jamais sous 1[per_hero] ; le retrait du vilain vaincu est une
# REPONSE, l'ordre des ecritures du livret p.1 ne change rien au resultat ; « if you cannot » absent : un tirage impossible (aucun
# vilain sous le Vault) ne fait rien, et le Vault declare alors la DEFAITE (aucun vilain dessous).


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)
        RevelerProchainMechant(effect, message.GetToPlayer())

    def completer_a_la_place(effect: 'Effect', message: 'Message.WhenMainSchemeStageWouldBeCompleted') -> None:
        this = effect.this.CastTo(MainScheme)
        message.SetBeInstead(effect)
        reste = this.threat - NombreDeJoueurs(effect)
        if reste > 0:
            this.RemoveThreatFromSchemes([this], reste, effect, ignore_crisis=True)
        joueur = Worlds.GetFirstPlayer(effect)
        RevelerAuHasardSousLeVault(effect, joueur, Villain)
        if not effect.world.is_game_over:
            SetupCards.Reveal(effect, joueur, name=NOM_INSPECTION, card_type=Obligation, only_set_aside=True)

    def mechant_retire(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        villain = message.trigger.CastTo(Villain)
        Villains.Remove(villain, effect)
        ApresDepartDUnMechant(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenMainSchemeStageWouldBeCompleted(AbilityType.ForcedInterrupt, "This", completer_a_la_place),
        AbilityFactory.AfterUnitBeDefeated(AbilityType.ForcedResponse, Villain, mechant_retire),
    ]
