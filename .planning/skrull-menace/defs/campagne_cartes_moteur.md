# Cartes de campagne (sk263-sk289b) — modifications des fichiers PARTAGES (moteur, docs)

Regle du brief : additif et minimal, chaque modification consignee (fichier, quoi, pourquoi, cas qui la prouve). Une modification
de moteur exige de relancer toute la batterie du bloc : faite (voir `CAMPAGNE-CARTES-GABARITS.md`).

| Fichier | Quoi | Pourquoi | Cas qui la prouve |
|---|---|---|---|
| `Fusion/marvel-lcg-src/src/game/world/world.py` | attribut `World.skip_villain_phases` (0 par defaut) + 4 lignes dans la boucle de round (`OnGameLoop`) : si > 0, on le decremente et on saute la phase du mechant ENTIERE (ni debut/fin de phase, ni etapes 1 a 4) | `sk280` Princess Anelle : « remove from the game -> skip the villain phase ». Aucun precedent propre (`jj/61020` neutralise les etapes une a une et laisse partir les Reponses forcees « apres l'etape 2 » des scenarios Super-Skrull/Paibok) | `sk280 ... la phase du mechant est sautee` (le drapeau passe a 1 apres `Puzzle.EndPlayerPhase`) ; la BOUCLE elle-meme est prouvee par l'autoplay : le journal porte « --- Phase : Villain (skipped) --- » dans 6 parties du deck `campagne` (voir gabarit sk280) |
| `Fusion/marvel-lcg-src/src/game/ability/factory/treat.py` (`TreatAsMinion`) | le bloc « Hack for 50171 » passe APRES `SwapCardFace` et n'ajoute plus une seconde fois les capacites du module (`CardFactory.CreateFace` les a deja ajoutees) | un gabarit sbire qui porte une capacite (`skrull_war_minion`, Reponse de sk268) faisait planter `FaceRegisterEffects` (« 'Minion' object has no attribute 'card' ») ; apres l'echange, chaque capacite etait enregistree DEUX fois (pioche en double) | `sk268 ... apres avoir attaque, 1 carte piochee` et `... si le joueur ne subit AUCUN degat, 2 cartes piochees` ; `sk243` (Skymax Elite, gabarit sans capacite) reste vert |
| `Fusion/marvel-lcg-src/src/game/operate/faces.py` (`Faces.TreatAsAlly`) | parametre facultatif `process(allie, sbire)` appele AVANT l'echange de face | `sk272` Fickle Alliance : un sbire cherche dans le deck rencontre n'a jamais eu de PV courants ; l'allie issu du gabarit (PV 0) etait vaincu en entrant en jeu. `process` lui donne les PV imprimes du sbire | `sk272 ... devient un allie (MNG imprime -> CTR, traits gardes)` ; `fne` (Kingpin, `ConvertirBlackCatEnAlliee`) n'utilise pas `process` : inchange |
| `Fusion/marvel-lcg-src/src/game/player/action/player_action.py` (`DrawUp`) | garde `and not player.is_eliminated` devant `player.Eliminate(by_effect)` apres `PopPlayerDeckCards` | l'AUTOPLAY a trouve un plantage de partie (`AssertionError`, `Player.Eliminate` : `assert self.is_eliminated == False`) : la Forced Interrupt de sk288 Sy-Torak Gem (« when your deck empties ... discard Sy-Torak Gem ») defausse la gemme PENDANT la pioche, le joueur perd ses +3 PV et tombe ; la boucle s'arrete (`len(faces) < size`) et le moteur tentait d'eliminer un joueur deja elimine. Aucun changement pour une pioche normale | `sk288 ... la gemme defaussee en pleine pioche fait perdre ses +3 PV` (ROUGE sans la garde : `AssertionError`, mesure par mutation ; VERT avec) |
| `Fusion/marvel-lcg-src/src/game/card/face/card_face.py` (enum `TRAITS`) | 5 traits : `"INITIATIVE"`, `"S.W.O.R.D."`, `"SQUADRON SUPREME"`, `"RUNAWAYS"`, `"CREW"` | traits imprimes sur les allies et soutiens de campagne ; purement declaratif (`TRAITS` n'est qu'un `Literal`) | tous les cas `[campagne_cartes]` (les cartes se construisent) |
| `docs/reference/mots-cles/` | `initiative.md` (nouveau, ajoute au README) ; `alliance.md` : paragraphe « Variante sk280 » | regle du projet : une fiche par mot-cle rencontre ; Alliance sur un soutien n'est pas le mecanisme natif | — |

Aucun autre fichier de `src/game/**`, ni `src/cards/pack/__init__.py` ; `tools/test_capacites.py` n'est PAS touche (cas dans
`tools/cas/campagne_cartes.py`). `data/cards.json`, `data/sets_info.json` : par `defs/inserer_campagne_cartes.py` uniquement
(idempotent, a rejouer apres fusion). `ui-app/src/board/textes-fr-fanmade.ts` et `data/translate_fr.json` : NON touches (textes
dans `defs/campagne_cartes_fr.txt`).

Tout le reste vit dans `src/cards/pack/skrull_menace/skrull_menace_campaign/` (27 modules + helpers `__init__.py`).

Ce qui N'A PAS demande de moteur (mesure) : le melange/attache face cachee (`PlaceCardHere`), les Reponses sur defausse
(`AfterCardDiscard`), le cout de ressource dynamique (`IncreaseResourceCostToPlay`), le bonus depuis la pile de victoire
(`GiveKeywordToInPlayWhenApplyThis(works_in_the_victory_display=True)`), Alliance sur un soutien (marque `cout_en_groupe`
posee par le bloc Secret Invasion), la resolution d'une Action de heros depuis la defausse (`Faces.ResolveAbility`).
