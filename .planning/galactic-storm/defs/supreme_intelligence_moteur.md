# Lot GS-8 (Supreme Intelligence + Starforce, Seeds of Corruption, Nega-Bomb) : modifications du moteur et des fichiers partagés

Toutes ADDITIVES. Chaque ligne : fichier, quoi, pourquoi, cas qui la prouve.

| Fichier | Modification | Pourquoi | Preuve |
|---|---|---|---|
| `src/game/card/face/card_face.py` | `"STARFORCE"` ajouté à l'énum `TRAITS` | trait imprimé sur gs204, gs209-gs216 ; lu par gs198a/b, gs199a, gs208, gs217 | tous les cas `[gs8] gs198a`, `gs208`, `gs217` |
| `src/game/card/face/card_face.py` | `'integrity'` ajouté à l'énum `COUNTER` | `desc.Uses = "7*,integrity"` de gs200 Holding Tank (`has_uses.py` assert `IsCounter`) | `[gs8] gs198a Setup` (7 pions), `[gs8] gs200 ...` |
| `src/game/card/face/card_type/scheme_main.py` | `GainTargetThreatValue` ignore toute modification quand le texte du complot porte « target threat value of this scheme cannot be changed » | gs198b Protectors of the Kree Empire (1B) ; aucun mécanisme existant | `[gs8] gs198b ... ne peut pas etre modifie` : VU ROUGE ligne neutralisée (« objectif apres un gain de 3 = 9 »), vert rétablie ; témoin `[gs8] gs198b TEMOIN : sur 2B` (11 -> 14) |
| `ui-app/src/board/compteurs-fr.ts` | `integrity: 'intégrité'` | libellé français du pion de Holding Tank sur le plateau | `ui-app/src/board/supreme-intelligence-plateau.test.ts` (vu rouge avant l'ajout) |

Données partagées (rejouer `inserer_supreme_intelligence.py` après fusion) : `data/cards.json` clé `galactic_storm`
(créée), `data/sets_info.json` entrée `144. Custom (Galactic Storm)` (créée si absente : scénario
`gs_supreme_intelligence`, sets `gs_starforce`, `gs_seeds_of_corruption`, `gs_nega_bomb`), checksums recalculés.

Batterie complète de `test_capacites` : NON lancée (interdite pour ce lot). Les trois modifications moteur sont
additives (un trait, un nom de compteur, une condition gardée par une phrase qu'aucune autre carte n'imprime :
vérifié par grep de `data/cards.json`).
