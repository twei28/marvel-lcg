from cards.pack import *

# ===========================================================================
# Pack AGATHA HARKNESS — contenu custom de « Ripper3 ». Set 132, prefixe `aa`.
#
# La sorciere de Salem, mentor de Wanda. Deux sets : `Agatha Harkness`
# (aa001a-aa014, dont les cartes d'aspect bonus aa019-aa021) et
# `Agatha Harkness Nemesis` (aa015-aa018, Death).
#
# ---------------------------------------------------------------------------
# LE PACK EN UNE PHRASE : LE DESSUS DU DECK EST UNE RESSOURCE
#
#   aa001a Power Absorption -> encaisser une attaque defausse le deck et
#                              repeche un SPELL
#   aa003 Ebony             -> regarde le dessus, en garde une
#   aa004 Wake Thy Power    -> defausse 2 et convertit les icones
#   aa006 Soul Harvest      -> defausse 1 et statue selon la couleur
#   aa007 Occult Knowledge  -> revient en main quand elle tombe du deck
#   aa012 Regained Youth    -> soigne quand le deck se vide
#   aa013 Ghost Agatha      -> filtre le dessus, et survit a l'elimination
#
# Et « Agatha All Along » (aa008, manigance-joueur a 13 menaces) recompense
# les degats SUBIS : la sorciere veut se faire frapper.
#
# ⚠ HOMONYMES PREEXISTANTS, tous dans d'autres sets (aucune collision d'id) :
#  - « Agatha Harkness » : 15007 est un SOUTIEN SIGNATURE du pack officiel
#    Scarlet Witch — jouer Agatha AVEC Wanda officielle met deux cartes du
#    meme nom en jeu (regle d'unicite : nos aa001a/b sont des identites, pas
#    des soutiens, les deux coexistent legalement mais le clin d'oeil est la) ;
#  - « Scarlet Witch » (aa002) : hero officiel 15001a, allie signature 14002
#    (Quicksilver), allie Justice 58014 ;
#  - « Wiccan » (aa019) : HERO fan-made wc001a (pack wiccan), allie Justice
#    officiel 15011, allie signature 56030 (Hulkling), sbire 57061 ;
#  - « Pixie » (aa020) : allie Leadership officiel 36017 — MEME classe, seule
#    la regle d'unicite les depart en jeu ;
#  - « Death » (aa016) : vilain officiel 45084a/b (Four Horsemen, AoA).
# Tout est consigne dans le collision_note du deck de depart.
# ===========================================================================


def RunicMagicianEnJeu(effect: 'Effect') -> bool:
    """aa011 en jeu chez le joueur : Power Absorption peut ignorer SPELL."""
    initiator = effect.GetInitiator()
    if initiator is None:
        return False
    return any(getattr(f.paper, "card_id", None) == "aa011"
               for f in initiator.GetControlCards())
