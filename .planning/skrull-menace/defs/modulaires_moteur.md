# Sets modulaires restants (sk228-sk262) — modifications des fichiers PARTAGES (moteur, ui)

Regle du brief : additif et minimal, chaque modification consignee (fichier, quoi, pourquoi, cas qui la prouve).

**Moteur (`src/game/**`, `src/cards/pack/__init__.py`, enums de traits) : AUCUNE modification.** Tous les traits utilises
(`COSMIC ENTITY`, `ELITE`, `SKRULL`, `GENIUS`, `CONDITION`, `ITEM`, `WEAPON`, `ARTIFACT`, `SOLDIER`) et compteurs (`damage`) existaient deja.

Fichiers de donnees partages touches **uniquement par le script idempotent `defs/inserer_modulaires.py`** (a rejouer apres fusion) :

| Fichier | Quoi |
|---|---|
| `Fusion/marvel-lcg-src/data/cards.json` | 38 cartes sk228-sk262 (cle `skrull_menace`), dont 3 en `ability_link` (sk246 -> sk098, sk247 -> sk113, sk254 -> sk098) |
| `Fusion/marvel-lcg-src/data/sets_info.json` | 8 sets declares dans `encounters` de `143. Custom (Skrull Menace)` ; `max_id` >= `sk262` |
| `Fusion/marvel-lcg-src/data/encounter_sets/*.json` | `sk_shaper_of_worlds`, `sk_skrull_elite_{crusader,jazinda,skymax,war_skrull,xavin}`, `standard_skrull`, `expert_skrull` |
| `Fusion/marvel-lcg-src/data/scenarios/sk_essai_*.json` | 3 scenarios d'ESSAI (Rhino + les sets), non declares dans `sets_info.json` : invisibles de l'ecran de choix |

Ajouts hors fichiers partages : `src/cards/pack/skrull_menace/communs_modulaires.py` et huit dossiers de set
(`shaper_of_worlds/`, `skrull_elite_*/`, `standard_skrull/`, `expert_skrull/`), `tools/cas/modulaires.py`,
`ui-app/src/board/modulaires-skrull-plateau.test.ts`, `defs/{modulaires_cards,inserer_modulaires,copier_images_modulaires}.py`,
`defs/modulaires_fr.txt`.
