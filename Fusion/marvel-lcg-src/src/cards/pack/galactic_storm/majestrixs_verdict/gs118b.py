from . import *

# Majestrix's Verdict (2B) — MANIGANCE PRINCIPALE, stade 2. Seuil 5[per_hero], escalade +2[per_hero][star], depart 0.
# When Revealed: Place 1[per_hero] threat on Imprisoned on Chandilar.
# Forced Interrupt: When this stage would be completed, flip this card and reveal it instead.
# [star] Forced Response: After resolving step one of the villain phase, place 2 threat on Imprisoned on
#   Chandilar for each player in alter-ego form.
#
# Cartes de reference :
#  - When Revealed / Forced Response : helpers communs avec gs117b (`MenaceSurLaPrisonParJoueur`,
#    `ApresEtapeUn`, modele 04096b).
#  - « When this stage would be completed, ... instead » : `WhenMainSchemeStageWouldBeCompleted` +
#    `message.SetBeInstead`, modele sk145b Mastering Superpowers (meme auteur).
#  - « flip this card and reveal it » : `card.Flip(effect)` ; une manigance en jeu qui se retourne est REVELEE
#    par le moteur (`OnAfterFlip`, `call_reveal`), donc 2A rejoue son « When Revealed » (execution d'un
#    STARJAMMER) puis avance seule vers 2B, qui repart a sa menace de depart (0).
#
# ⚠ Mots-pieges : « INSTEAD » : le stade n'est jamais accompli, la partie ne se perd pas par la manigance
# principale (seulement par la perte de Lilandra ou des heros) ; chaque passage execute un STARJAMMER.


def GetAbilities() -> Sequence['Ability']:

    def retourner(effect: 'Effect', message: 'Message.WhenMainSchemeStageWouldBeCompleted') -> None:
        this = effect.this.CastTo(MainScheme)
        message.SetBeInstead(effect)
        carte = this.card
        carte.Flip(effect)
        # 2A « Advance to stage 2B » : le stade qui commence repart de sa menace de depart (0). Le moteur garde
        # les pions d'une carte RETOURNEE (mesure du 20/10/2026 : 2B revenait avec ses 5 menaces, donc
        # « accomplie » a nouveau a la premiere menace) ; on les retire, Crise comprise (regle, pas un contre).
        retour = carte.face
        if MainScheme.IsType(retour) and retour.IsInPlay() and retour.threat > 0:
            retour.RemoveThreatFromSchemes([retour], "All", effect, ignore_crisis=True)

    return [
        MenaceSurLaPrisonParJoueur(),
        AbilityFactory.WhenMainSchemeStageWouldBeCompleted(AbilityType.ForcedInterrupt, "This", retourner),
        ApresEtapeUn(),
    ]
