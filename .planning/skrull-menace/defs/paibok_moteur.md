# Paibok / New Revengers — modifications des fichiers PARTAGES (moteur, ui)

Regle du brief : additif et minimal, chaque modification consignee (fichier, quoi, pourquoi, cas qui la prouve).

| Fichier | Quoi | Pourquoi | Cas qui la prouve |
|---|---|---|---|
| `Fusion/marvel-lcg-src/src/game/card/face/card_face.py` (enum `TRAITS`) | 3 traits : `"POWER SKRULL"`, `"REVENGER"`, `"COMPUTER"` | traits imprimes sur les 4 attachements de pouvoir de Paibok, sur 7 cartes de New Revengers et sur O.M.N.I.T.R.O.N.I.C.U.S. (purement declaratif : `TRAITS` n'est qu'un `Literal`) | tous les cas `[paibok]` (cartes chargees, `HasTrait` lu par les capacites) |
| `Fusion/marvel-lcg-src/src/game/card/face/card_face.py` (enum `COUNTER`) | 2 compteurs : `'mastery'`, `'absorption'` | jetons de MAITRISE poses sur Paibok (insert p.12) et d'ABSORPTION d'Asti the All-Seeing ; sans eux `IsCounter` refuse le nom et la pose echoue | `[paibok] sk144a/sk144b Setup`, `[paibok] sk163 Asti ... jetons` |
| `Fusion/marvel-lcg-src/tools/traits_fr_maison.json`, `public/js/prepare/traits-fr.js`, `public/js/traduction/traits-fr.js`, `ui-app/src/board/traits-fr.ts` | `"COMPUTER": "ORDINATEUR"` | trait francais ; `POWER SKRULL` et `REVENGER` sont des noms propres du coffret, laisses en anglais comme `SKRULL` et `AVENGER` | (affichage seulement) |
| `ui-app/src/board/compteurs-fr.ts` (+ `.test.ts`) | `mastery: 'maîtrise'`, `absorption: 'absorption'` | nom francais des compteurs sur le plateau (un nom absent reste en anglais) | `compteurs-fr.test.ts` |

Aucun fichier de `src/game/**` autre que l'enum ci-dessus n'est touche ; `src/cards/pack/__init__.py` non plus.

Tout le reste vit dans `src/cards/pack/skrull_menace/paibok/` et `.../new_revengers/` (scripts et helpers du set).
