# Secret Invasion — modifications des fichiers PARTAGES (moteur, ui)

Regle du brief : additif et minimal, chaque modification consignee (fichier, quoi, pourquoi, cas qui la prouve). Une modification de moteur
exige de relancer toute la batterie : faite (voir SECRET-INVASION-GABARITS.md).

| Fichier | Quoi | Pourquoi | Cas qui la prouve |
|---|---|---|---|
| `Fusion/marvel-lcg-src/src/game/card/face/card_face.py` (enum `TRAITS`) | 3 traits : `"CAMOUFLAGED"`, `"REVEALED"`, `"IMPOSTOR"` | traits imprimes sur Veranke (les deux faces) et sur les 20 cartes double face du paquet Impostor ; purement declaratif (`TRAITS` n'est qu'un `Literal`), lus par `HasTrait` | tous les cas `[secret_invasion]` (ex. `sk189a valeurs imprimees`, `sk208a valeurs imprimees de l'allie`) |
| `Fusion/marvel-lcg-src/src/game/card/face/card_face.py` (enum `COUNTER`) | compteur `'suspicion'` | jetons de SOUPCON de l'environnement « Who Do You Trust? » (sk194) ; sans l'entree `IsCounter` refuse le nom | `sk194 Menace POSEE...`, `sk189a Reponse forcee...` |
| `Fusion/marvel-lcg-src/src/game/operate/worlds.py` (`Worlds.ASIDE_DECK_NAME`) | nom `"ImpostorDeck"` | le moteur cree un `SetAsideDeck` par nom liste dans ce Literal (`world.py:131`) : le paquet IMPOSTOR (20 cartes double face) et sa defausse | `sk189a Setup...` (sans la ligne : `KeyError`) |
| `Fusion/marvel-lcg-src/src/game/ability/factory/resources.py` | `PaiementEnGroupeInterdit(world)` (nouvelle fonction) ; `CheckAnyPlayerMayHelpPay(face, effet=None)` : une capacite marquee `cout_en_groupe` ouvre le paiement a tous les joueurs, sauf si une carte en jeu porte `interdit_paiement_en_groupe` ; les deux controles « Alliance » le respectent aussi | « The players can pay this ability's costs as a group » (Spider-Woman, sk189a/190a/191a) ; « Players cannot pay any card's or ability's costs as a group » (sk201 Mistrust and Paranoia). Le mot-cle Alliance du moteur est reserve aux evenements et sans exception possible | `sk189a « You are a Skrull! » : 2 joueurs... EN GROUPE` (vert), le cas jumeau avec Mistrust (rien), `sk201...` |
| `Fusion/marvel-lcg-src/src/game/event/manager.py` (`SimpleCheckEffects`) | une branche `Villain.IsType(this)` : le joueur COURANT est le joueur qui interroge, comme pour un environnement (`Fix 27077a`) | une Action de heros portee par un MECHANT n'etait jamais offerte : son « controleur » est le scenario, qu'aucun joueur n'egale. Aucun mechant imprime n'a d'action de heros (« You are a Skrull! » est la premiere) | `sk189a « You are a Skrull! » : incline un heros et depense 1 ressource` |
| `ui-app/src/board/compteurs-fr.ts` (+ `.test.ts`) | `suspicion: 'soupçon'` | nom francais du compteur sur le plateau | `compteurs-fr.test.ts` |

Aucun autre fichier de `src/game/**`, ni `src/cards/pack/__init__.py` ; `tools/test_capacites.py` n'est PAS touche (cas dans `tools/cas/secret_invasion.py`).
`data/cards.json`, `data/sets_info.json` : par `defs/inserer_secret_invasion.py` uniquement (idempotent, a rejouer apres fusion).

Tout le reste vit dans `src/cards/pack/skrull_menace/secret_invasion/` (64 modules + helpers `__init__.py`).

Ce qui N'A PAS demande de moteur (mesure) : le retournement d'un allie en sbire (`Card.Flip(call_reveal=False)` puis `Reveal` explicite, meme
famille que 60113a Establish Trust) ; l'interruption « quitter le jeu -> retourner a la place » (`WhenCardWouldLeavePlay` + `SetBeInstead`,
37034 Psionic Shield) ; la defausse IMPOSTOR (`Faces.BindDiscardPile`, comme les pouvoirs de Super-Skrull) ; le retournement du mechant
et le « meme cote » (`AdvanceVillainStage` choisit la face de meme NOM) ; le mechant double face (precedent 60110a Typhoid Mary / 39012 Spiral).
