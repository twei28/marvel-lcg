from . import *

# CORRECTIF (27/10/2026, passe de fusion hg028-hg076) : bug de donnees (cle `Quickstrike` absente du `desc`)
# CORRIGE A LA SOURCE -- `"Quickstrike": "1"` ajoute au `desc` de cette carte dans `data/cards_custom.json` (forme exacte des
# 98 cartes officielles de `data/cards.json`). Le contournement `AbilityFactory.ThisGainKeyword(quickstrike=1)`
# est donc RETIRE du script (il aurait double la source du mot-cle) : Quickstrike est desormais lu nativement
# par `HasQuickstrike`, comme `01167` * Vulture. Prouve par les cas `[hg] hg062 Quickstrike` (tools/cas/the_hunger_core.py).
#
# Zombie Wasp — METAZOMBIE (Fallen Heroes, modulaire). AVENGER. SCH 1. ATK 1. HP 4.
# Guard. Quickstrike. Retaliate 2.
#
# Cartes de reference :
#  - « Guard » (mots-cles/guard.md) et « Retaliate 2 » (mots-cles/retaliate.md) : cles natives
#    `desc.Guard`/`desc.Retaliate` (confirmees presentes dans `data/cards_custom.json` : `"Guard": "1"`,
#    `"Retaliate": "2"`), aucun script -- memes mecanismes que `01101` Hydra Mercenary / `01040a`
#    * Black Panther.
#  - « Quickstrike » (mots-cles/quickstrike.md) : cle native `desc.Quickstrike` (`"Quickstrike": "1"` dans
#    `data/cards_custom.json` depuis le correctif du 27/10/2026 en tete), lue par `HasQuickstrike` /
#    `can_quickstrike.py`, AUCUN script (modele `01167` * Vulture).
#
# ⚠ Mots-pieges :
#  - Quickstrike N'A RIEN A VOIR avec un ordre de resolution face a Retaliate (les deux co-existent sans
#    interaction speciale, cf. mots-cles/retaliate.md) : Zombie Wasp qui s'engage avec un heros attaque
#    IMMEDIATEMENT (Quickstrike), et QUAND elle attaque -- la sienne ou celle d'un autre ennemi contre
#    elle -- Retaliate 2 s'applique normalement a chaque fois qu'elle EST attaquee.
#  - Quickstrike est resolu par le moteur natif (`Minion.OnEngagePlayer` / `CanQuickstrike.ResolveQuickstrike`) :
#    aucune logique de combat n'est dupliquee ici (la fiche Quickstrike interdit de coder l'attaque a la main).
#  - Retaliate 2 : trois cas natifs ou il ne part pas (attaque a distance, attaquant/defenseur deja vaincu,
#    attaque qui ignore Retaliate) -- rien a coder, deja dans `ResolveRetaliate` (cf. fiche).
#
# Bloc nombres texte <-> code : SCH 1 / ATK 1 / HP 4 / Guard 1 / Retaliate 2 / Quickstrike 1 -> `desc` (mot nu
# « Quickstrike. » = valeur 1).


def GetAbilities() -> Sequence['Ability']:

    # Quickstrike : cle native `desc.Quickstrike` (voir CORRECTIF du 27/10/2026 en tete), aucun script.
    return []
