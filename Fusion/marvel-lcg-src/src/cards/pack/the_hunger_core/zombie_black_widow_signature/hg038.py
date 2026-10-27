from . import *

# Infiltrator — SIDE SCHEME (deck signature de Zombie Black Widow, carte 2/3, hg037-039). Menace de depart
#   2[per_hero] (`desc.StartingThreat = "2*"`). Hazard 1 (`desc.Hazard = "1"`). Aucun trait imprime.
# While this scheme is in play, Zombie Black Widow gets +1 SCH.
#
# ---------------------------------------------------------------------------
# ETAPE 1 : cards_custom.json
#
# `card_id hg038, type SideScheme, name "Infiltrator", desc.StartingThreat "2*", desc.Hazard "1", traits [],
# set_name "Zombie Black Widow (Signature)"` -- entree deja presente (portee depuis TTS le 27/10/2026), rien
# a y modifier pour cette tache.
#
# ---------------------------------------------------------------------------
# ETAPE 2 : CARTES DE REFERENCE
#
# - Carte-modele PRESQUE au mot pres, MEME SCENARIO : `hg029` Rooftop to Rooftop (set signature de Zombie
#   Spider-Man) : « While this scheme is in play, Zombie Spider-Man gets +1 SCH and cannot be attacked by
#   allies. » hg038 n'imprime QUE la premiere clause (« gets +1 SCH »), sans la clause « cannot be attacked
#   by allies » : repris ici tel quel, en retirant simplement la seconde capacite de hg029.
# - Fabrique d'origine (deja remontee par hg029) : `wd049` Dark Matter Conversion (pack web_of_deceit/electro,
#   « The villain gets +2 ATK and gains retaliate 1 ») : `*AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
#   CardFinder(card_type=Villain), attack=2, retaliate=1)`. Egalement confirmee par la carte officielle
#   `22029` Self-Preservation (pack Nebula Nemesis, SideScheme officielle : « Nebula gets -1 THW, -1 ATK, and
#   -1 DEF. Gamora gets +1 ATK and her attacks gain piercing. ») -> `*AbilityFactory.
#   GiveKeywordToInPlayWhenApplyThis(CardFinder(name="Nebula"), thwart=-1, attack=-1, defense=-1)` : une
#   SideScheme OFFICIELLE qui buffe/debuffe en continu une carte NOMMEE pendant qu'elle est en jeu, exactement
#   la charpente retenue ici.
# - « WHILE THIS SCHEME IS IN PLAY » : ne se code PAS comme une condition supplementaire, meme raisonnement
#   que `hg029`/`tg012` Adorable Distraction (pack throg_nemesis) : une capacite enregistree sur une carte en
#   jeu n'existe QUE tant que cette carte est en jeu (comportement natif du moteur). Rien a brancher sur un
#   signal « cette manigance a-t-elle ete defaussee ».
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - « +1 SCH » : pas un terme EN GRAS imprime sur cette carte (prose simple), aucun mot-cle officiel ou maison
#   a catalogue -- absent de `docs/reference/mots-cles/README.md`, meme constat deja fait sur `hg029`/`hg021`/
#   `hg026` (bonus de stats en prose, jamais declencheurs de fiche). Rien a ouvrir, rien a creer.
# - Hazard (`desc.Hazard = "1"`) : fiche `mots-cles/hazard.md` lue avant d'ecrire -- mot-cle NATIF, lu
#   directement depuis `desc` par `HasHazard` (`src/game/card/face/attribute/has_hazard.py`), aucun script
#   requis (« base automatique », meme traitement que Toughness/Restricted). L'icone Hazard n'est d'ailleurs
#   meme pas mentionnee dans le `text` imprime de `hg038` (seule trace : `desc.Hazard`), exactement le cas
#   decrit par la fiche (« le texte de ces cartes ne dit pas "Hazard", seule l'icone le dit »).
# - Pas de mot-cle imprime en gras du tout sur `hg038` : la carte ne contient qu'une seule phrase descriptive.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE (etape 5, mots-pieges)
#
# - « Zombie Black Widow » (nommement, pas « each Metazombie » ni « the villain ») -> `CardFinder(
#   name="Zombie Black Widow", card_type=Villain)` : nom UNIQUE au depot (`grep '"name": "Zombie Black
#   Widow"' data/cards.json data/cards_custom.json` : une seule occurrence, dans `cards_custom.json`, meme
#   verification que celle documentee par `hg026`/`hg029` pour « Zombie Hulk »/« Zombie Spider-Man »).
# - « gets +1 SCH » : exactement UN bonus de manigance, aucun bonus d'attaque ni de defense -- ne pas copier
#   le `attack=2, retaliate=1` de `wd049` ni le `thwart=-1, attack=-1, defense=-1` de `22029` : seul
#   `scheme=1` est imprime ici.
# - Pas de « cannot be attacked » ni d'autre clause sur cette carte (a la difference de sa carte-soeur
#   `hg029`/`hg021`) : une seule capacite a coder, ne rien ajouter qui ne soit pas imprime.
# - « While this scheme is in play » : aucune clause separee a coder (voir Etape 2 ci-dessus) -- NE PAS
#   ajouter de condition `effect.this.IsInPlay()` : elle serait toujours vraie quand l'ability s'evalue (une
#   ability d'une carte hors jeu ne s'evalue pas), donc redondante, et risquerait de masquer un vrai defaut
#   si jamais elle etait fausse par erreur ailleurs.
# - Pas de « unless »/« otherwise »/« instead »/« if you cannot »/surge dans le texte imprime : rien d'autre
#   a coder.
# - Carte DEFENSIVE pour Zombie Black Widow (buff pur), elle n'attaque ni ne maniganche jamais elle-meme : pas
#   de `WhenThisRevealed`, pas de `WhenRevealed` -- aucune clause de revelation imprimee sur cette carte
#   (contrastant avec `hg037`/`hg039`, les deux autres cartes du meme deck signature, qui en portent une).
#
# ---------------------------------------------------------------------------
# ETAPE 6 : NOMBRES, TEXTE <-> CODE
#
# - « +1 SCH » -> `scheme=1` (`cards_custom.json` ne porte aucun badge chiffre dans `desc` pour cette valeur,
#   elle n'existe qu'en prose dans `text` -- comme `hg021`/`hg026`/`hg029`).
# - « StartingThreat: "2*" » (menace de depart « 2 par heros ») : lu NATIVEMENT par le moteur depuis `desc`
#   (`game/card/face/base/scheme.py:18`, `RegisterAttribute("StartingThreat", "start_threat")`), comme
#   `01108`/`01150`/`hg029` (autres manigances annexes « 2* ») -- AUCUN script necessaire, base automatique
#   au meme titre que Toughness/Restricted (PROCESSUS-CARTE.md etape 6).
# - « Hazard: "1" » (une icone Hazard) : lue NATIVEMENT par le moteur depuis `desc` (`HasHazard`), comme
#   `01107`/`27191`/`vz031` -- AUCUN script necessaire (voir bloc mots-cles ci-dessus).
#
# A CONFIRMER EN JEU REEL : comme pour `hg037`/`hg039` (meme deck signature) et `hg029` (deck signature
# voisin), aucun outil de ce lot ne verifie l'ENTREE EN JEU de cette manigance depuis le deck signature de
# Zombie Black Widow (le mecanisme qui revele le dessus de ce deck n'est pas encore ecrit -- note deja posee
# par `hg026`/`hg029`). La capacite codee ci-dessous ne peut donc etre prouvee qu'une fois la carte placee en
# jeu par l'API Puzzle directement (`Puzzle.PutIntoPlay`/equivalent), pas par un scenario complet.


def GetAbilities() -> Sequence['Ability']:

    cible = CardFinder(name="Zombie Black Widow", card_type=Villain)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            cible,
            scheme=1,
        ),
    ]
