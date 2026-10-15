from cards.pack.skrull_menace.communs_modulaires import *

# ===========================================================================
# Ensemble d'ELITE « SKRULL ELITE - XAVIN » (Skrull Menace, Kajislav) — sk250-sk253.
# Six cartes : le sbire * Xavin, deux Invisible Forcefield, le complot annexe Super-Skrull Training
# Program et deux Going Nova. Dossier du set : `FileManager.CleanName("Skrull Elite - Xavin")` =
# `skrull_elite_xavin`.
# ===========================================================================

NOM_CHAMP = "Invisible Forcefield"


def EstTraitrise(face: 'CardFace') -> bool:
    """« a treachery » : carte de TYPE Treachery OU portant le trait TREACHERY (les evenements de Lyja se
    melangent au deck rencontre et s'y comportent en traitrises : decision utilisateur du 15/10/2026
    pour sk066, appliquee ici de meme ; voir defs/modulaires_questions.md)."""
    return Treachery.IsType(face) or face.HasTrait("TREACHERY")
