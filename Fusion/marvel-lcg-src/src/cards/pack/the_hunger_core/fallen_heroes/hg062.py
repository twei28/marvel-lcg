from . import *

# CORRECTIF (27/10/2026, passe de fusion hg028-hg076) : le bug de donnees decrit ci-dessous est CORRIGE A LA
# SOURCE -- `"Quickstrike": "1"` ajoute au `desc` de cette carte dans `data/cards_custom.json` (forme exacte des
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
#  - « Quickstrike » (mots-cles/quickstrike.md) : normalement une cle native `desc.Quickstrike`
#    (`HasQuickstrike`, `can_quickstrike.py`), AUCUN script requis d'ordinaire (modele `01167` * Vulture).
#    ⚠⚠ BUG DE DONNEES CONSTATE LE 27/10/2026 (hors perimetre de cette tache -- `cards_custom.json` n'est
#    PAS un des 7 fichiers autorises) : l'entree `hg062` de `data/cards_custom.json` ne porte PAS de cle
#    `"Quickstrike"` dans son `desc` (seulement `SCH/ATK/HP/Guard/Retaliate`), alors que le `text` imprime
#    « Guard. Quickstrike. Retaliate 2. » l'annonce explicitement. Sans cette cle, `HasQuickstrike` restaure
#    `printed_quickstrike = 0` a chaque `OnResetKeywords` et la carte n'attaque JAMAIS a son engagement, en
#    silence (meme famille de piege que celui deja documente sur `hg007`, § « PIEGE DE REPERTOIRE » : un
#    defaut de donnees qui ne leve aucune erreur). CONTOURNEMENT applique ICI, dans ce script (puisque le
#    fichier JSON est hors perimetre de cette tache) : `AbilityFactory.ThisGainKeyword(quickstrike=1)` donne
#    dynamiquement le MEME attribut `quickstrike` que la cle `desc` aurait donne (meme plomberie
#    `face_gain.py`/`Gain()`, lue par le MEME `IsQuickstrike()`), de facon permanente et inconditionnelle
#    (`check_fn` par defaut = `lambda effect, ui: 1`, `change_on_event=OnEvent.NONE` car rien ne doit faire
#    varier cette valeur). A RETIRER le jour ou `"Quickstrike": "1"` est ajoute a `cards_custom.json`
#    (correctif propre, prefere) -- voir le rapport de fin de travail, marque « A CONFIRMER ».
#
# ⚠ Mots-pieges :
#  - Quickstrike N'A RIEN A VOIR avec un ordre de resolution face a Retaliate (les deux co-existent sans
#    interaction speciale, cf. mots-cles/retaliate.md) : Zombie Wasp qui s'engage avec un heros attaque
#    IMMEDIATEMENT (Quickstrike), et QUAND elle attaque -- la sienne ou celle d'un autre ennemi contre
#    elle -- Retaliate 2 s'applique normalement a chaque fois qu'elle EST attaquee.
#  - Le contournement ci-dessus NE DOIT PAS etre lu comme « coder l'attaque a la main » (ce que la fiche
#    Quickstrike interdit explicitement) : il donne seulement l'ATTRIBUT `quickstrike`, et c'est toujours
#    `Minion.OnEngagePlayer` / `CanQuickstrike.ResolveQuickstrike` (moteur natif) qui lit cet attribut et
#    declenche l'attaque -- aucune logique de combat n'est dupliquee ici.
#  - Retaliate 2 : trois cas natifs ou il ne part pas (attaque a distance, attaquant/defenseur deja vaincu,
#    attaque qui ignore Retaliate) -- rien a coder, deja dans `ResolveRetaliate` (cf. fiche).
#
# Bloc nombres texte <-> code : SCH 1 / ATK 1 / HP 4 / Guard 1 / Retaliate 2 -> `desc` ; Quickstrike SANS
# valeur numerique imprimee differente de 1 -> `quickstrike=1` dans le contournement, coherent avec le mot
# nu « Quickstrike. » (pas de « Quickstrike 2 » comme pourrait l'ecrire une autre carte).


def GetAbilities() -> Sequence['Ability']:

    # Quickstrike : cle native `desc.Quickstrike` (voir CORRECTIF du 27/10/2026 en tete), aucun script.
    return []
