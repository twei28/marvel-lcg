from . import *

# CORRECTIF (27/10/2026, passe de fusion hg028-hg076) : bug de donnees (cle `Quickstrike` absente du `desc`)
# CORRIGE A LA SOURCE -- `"Quickstrike": "1"` ajoute au `desc` de cette carte dans `data/cards_custom.json` (forme exacte des
# 98 cartes officielles de `data/cards.json`). Le contournement `AbilityFactory.ThisGainKeyword(quickstrike=1)`
# est donc RETIRE du script (il aurait double la source du mot-cle) : Quickstrike est desormais lu nativement
# par `HasQuickstrike`, comme `01167` * Vulture. Prouve par les cas `[hg] hg063 Quickstrike` (tools/cas/the_hunger_core.py).
#
# Zombie Nova Prime — METAZOMBIE (Fallen Heroes, modulaire). COSMIC. SCH 1. ATK 2. HP 6.
# Guard. Quickstrike. Villainous.
#
# Cartes de reference :
#  - « Guard » (mots-cles/guard.md) et « Villainous » (mots-cles/villainous.md) : cles natives
#    `desc.Guard`/`desc.Villainous` (confirmees presentes dans `data/cards_custom.json` : `"Guard": "1"`,
#    `"Villainous": "1"`), aucun script -- modele `11041` * Deathunt 9000 (Villainous + Toughness, sans
#    capacite [star] propre pour ces deux mots-cles -- `11041` porte une capacite ANNEXE que hg063 n'a pas).
#  - « Quickstrike » : cle native `desc.Quickstrike` (`"Quickstrike": "1"` dans `data/cards_custom.json`
#    depuis le correctif du 27/10/2026 en tete), AUCUN script, comme `hg062` Zombie Wasp.
#
# ⚠ Mots-pieges :
#  - « Villainous » n'a AUCUN rapport avec les regles d'engagement (mots-cles/villainous.md) : Zombie Nova
#    Prime recoit une carte de boost a CHAQUE activation (attaque OU manigance), exactement comme un
#    vilain -- rien a coder, lu nativement via `GetBoostCardNum()` surcharge par `HasVillainous`.
#  - Quickstrike reste independant de Villainous : l'attaque declenchee a
#    l'engagement (Quickstrike) tire AUSSI une carte boost (puisque Zombie Nova Prime est Villainous et que
#    `can_attack.py` consulte `GetBoostCardNum()` a CHAQUE activation, y compris celle-ci) -- comportement
#    attendu, aucune garde a ecrire pour l'empecher (le texte imprime ne restreint pas Villainous a
#    l'activation normale par opposition a Quickstrike).
#  - Quickstrike est resolu par le moteur natif (`Minion.OnEngagePlayer`), comme pour hg062.
#
# Bloc nombres texte <-> code : SCH 1 / ATK 2 / HP 6 / Guard 1 / Villainous 1 / Quickstrike 1 -> `desc`.


def GetAbilities() -> Sequence['Ability']:

    # Quickstrike : cle native `desc.Quickstrike` (voir CORRECTIF du 27/10/2026 en tete), aucun script.
    return []
