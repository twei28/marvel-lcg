from . import *

# Earthfall (1B) — MANIGANCE PRINCIPALE, stade 1. Seuil absent (pas d'avancee de stade, voir plus bas).
# Forced Response: After the villain phase ends, remove 1 safety counter from here. If there are less
#   safety counters here than the number of cards in the villain deck, reveal the top card of the villain
#   deck and shuffle the rest of its encounter set into the encounter deck.
# If this scheme is completed, the players lose the game.
#
# Cartes de reference :
#  - « After the villain phase ends » : `AbilityFactory.AfterPhaseEnd(ForcedResponse, "Villain", ...)`
#    (modele sk190b Queen Veranke).
#  - « remove 1 safety counter from here » : `Faces.RemoveCountersOn` (modele RetirerRepli, hala_ultimatum).
#  - « If there are less safety counters here than the number of cards in the villain deck, reveal... » :
#    comparaison directe `This.GetCounters('safety') < Villains.VillainDeckSize(effect)`, puis
#    `RevelerProchainMechantEtMelangerLeReste` (earth_under_siege/__init__.py).
#  - « If a villain is defeated, remove that villain from the game » (Galactic Storm p.16, regle generale,
#    pas imprimee sur une carte precise) : `AbilityFactory.AfterUnitBeDefeated(ForcedResponse, Villain,
#    ...)` + `Villains.Remove` (modele Sinister Six `WhenUnitBeDefeated` scenario, adapte en APRES pour
#    laisser le Forced Interrupt d'Enemies at Large (gs162a/b) mesurer « le DERNIER mechant » avant le
#    retrait).
#  - « If this scheme is completed, the players lose the game » : natif (desc, texte affiche), aucun
#    module (modele gs141b).
#
# ⚠ Mots-pieges : le retrait du mechant vaincu est une REPONSE (apres), pas une interruption : le Forced
# Interrupt d'Enemies at Large doit pouvoir constater qu'il ne restait qu'un seul mechant AVANT ce retrait ;
# « the villain deck » ici = `Villains.VillainDeckSize` (pile des mechants non encore reveles), PAS
# `Scenario.villain_deck` (jamais utilise sur ce scenario, voir gs161a).


def GetAbilities() -> Sequence['Ability']:

    def tic_de_securite(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        Unused(message)
        this = effect.this.CastTo(MainScheme)
        Faces.RemoveCountersOn([this], 1, 'safety', effect)
        if this.GetCounters('safety') < Villains.VillainDeckSize(effect):
            premier = Worlds.GetFirstPlayer(effect)
            RevelerProchainMechantEtMelangerLeReste(effect, premier)

    def mechant_retire(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        villain = message.trigger.CastTo(Villain)
        Villains.Remove(villain, effect)

    return [
        AbilityFactory.AfterPhaseEnd(AbilityType.ForcedResponse, "Villain", tic_de_securite),
        AbilityFactory.AfterUnitBeDefeated(AbilityType.ForcedResponse, Villain, mechant_retire),
    ]
