from . import *

# Zombie Rhino — METAZOMBIE (Fallen Heroes, modulaire du scenario The Hunger Core). CRIMINAL. SCH 0. ATK 3.
# PV 7. Guard. Boost 3.
# Guard.
# Charge. This minion's attacks have Piercing.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - [[guard]] (mots-cles/guard.md) : BASE NATIVE, `desc.Guard` = "1". Aucun script requis.
# - [[piercing]] (mots-cles/piercing.md) : mot-cle OFFICIEL, mais PAS un attribut natif lu depuis `desc`
#   (contrairement a Guard/Toughness/Villainous/Stalwart/Retaliate/Boost) : aucune cle `Piercing` dans
#   `data/cards_custom.json` pour hg068 (seules SCH/ATK/HP/Guard/Boost y figurent) -- la fiche precise que
#   Piercing se donne soit par un boost ponctuel (`message.GainPiercing`), soit en PERMANENCE via
#   `AbilityFactory.UnitAttackGainKeyword(attacker, piercing=True)`. « This minion's attacks have Piercing »,
#   SANS condition ni limite imprimee, releve de la seconde voie (permanente), exactement comme `04027`
#   Crossfire (« Crossfire's attacks gain piercing »).
# - « Charge » : ABSENT de `docs/reference/mots-cles/README.md` (grep exhaustif du dossier : aucune fiche
#   `charge.md`) et absent de tout mot-cle officiel imprime sur une carte MINION du depot (grep `data/
#   cards.json` sur le mot seul : uniquement des titres de cartes/capacites sans rapport -- « Charge » evenement
#   `08XXX`, la capacite nommee « Charge Up » du Badoon Ship, les compteurs "charge" de plusieurs upgrades --
#   AUCUN cas d'un Minion portant « Charge. » comme mot-cle nu suivi d'une regle generale). Recherche web
#   complementaire (27/10/2026) : le SEUL "Charge" officiel associe a Rhino est une carte TRAITRISE du Core Set
#   (« Charge », 01099, attachee au vilain Rhino : « Rhino's attacks gain piercing » + « the attack gains
#   overkill ») -- PAS un mot-cle de minion, et son effet (overkill) NE correspond PAS a la seule phrase imprimee
#   sur hg068 (qui ne donne que Piercing, jamais Overkill).
#
# A CONFIRMER : « Charge. » est traite ici comme un NOM D'AMBIANCE propre a cette carte (meme statut deja
# arbitre 6 fois dans ce pack pour « Shield »/« Storm »/« Web »/« Absorption »/« Ambush »/« Hex »/« Portal to
# Limbo », hg007-hg015) plutot que comme un mot-cle maison distinct a ficher : la phrase qui suit IMMEDIATEMENT
# (« This minion's attacks have Piercing. ») est auto-suffisante et epuise toute la regle visible sur le scan
# -- rien dans le texte imprime ne suggere un second effet cache sous le mot « Charge » lui-meme (a la
# difference de la carte officielle 01099, dont le nom N'EST PAS repris mot pour mot sur le scan TTS de
# hg068, seul le mot « Charge » l'est, sans les deux points ni la mise en page d'un mot-cle a part entiere).
# Si une relecture du scan original (TTS) devait reveler une regle supplementaire associee a ce mot, elle
# reste a ajouter -- aucune n'a ete trouvee dans le materiel fourni pour cette tache.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « This minion's attacks have Piercing » (permanent, sans restriction) : `AbilityFactory.
#   UnitAttackGainKeyword("This", piercing=True)`, modele EXACT `04027` Crossfire (« Crossfire's attacks gain
#   piercing » -> meme fabrique, meme forme a une seule ligne, sans le second volet boost de Crossfire qui,
#   lui, repond a un texte DIFFERENT -- « If this boost resolves during an attack » -- absent de hg068).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « Guard. » -> natif, rien a coder.
# « Charge. » -> ambiance, voir bloc A CONFIRMER ci-dessus, rien a coder.
# « This minion's attacks have Piercing » -> `UnitAttackGainKeyword("This", piercing=True)`, s'applique a
#   TOUTE attaque de Zombie Rhino (pas seulement sa premiere, ni conditionnee a quoi que ce soit).
#
# Bloc nombres texte <-> code : aucune valeur numerique imprimee en dehors de `desc` (SCH/ATK/HP/Guard/Boost,
# verifies contre `cards_custom.json`) -- aucune valeur numerique dans ce script.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
        ),
    ]
