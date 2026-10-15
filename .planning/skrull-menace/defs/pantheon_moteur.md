# Skrull Pantheon / Dard'van Sect — modifications des fichiers PARTAGES (moteur, ui)

Regle du brief : additif et minimal, chaque modification consignee (fichier, quoi, pourquoi, cas qui la prouve).

| Fichier | Quoi | Pourquoi | Cas qui la prouve |
|---|---|---|---|
| `Fusion/marvel-lcg-src/src/game/card/face/card_face.py` (enum `COUNTER`) | 1 compteur : `'faith'` | jetons de FOI poses sur le mechant Kly'bn / Sl'gur't (insert p.14) ; sans eux `IsCounter` refuse le nom et la pose echoue | tous les cas `[pantheon]` (Setup : `foi: 1`) |
| `Fusion/marvel-lcg-src/src/game/card/face/card_face.py` (enum `TRAITS`) | 1 trait : `"GOD"` | trait imprime sur les six faces du mechant (purement declaratif : `TRAITS` n'est qu'un `Literal`) | cartes chargees (`[pantheon] sk170a Setup normal`) |
| `Fusion/marvel-lcg-src/tools/traits_fr_maison.json`, `public/js/prepare/traits-fr.js`, `public/js/traduction/traits-fr.js`, `ui-app/src/board/traits-fr.ts` | `"GOD": "DIEU"` | trait francais (affichage seulement) | — |
| `ui-app/src/board/compteurs-fr.ts` (+ `.test.ts`) | `faith: 'foi'` | nom francais du compteur sur le plateau (un nom absent reste en anglais) | `compteurs-fr.test.ts` |

Aucun autre fichier de `src/game/**` n'est touche ; `src/cards/pack/__init__.py` non plus. Le retournement du mechant, l'avance « du meme
cote » des stades et la carte d'environnement double face utilisent le moteur tel quel (`Card.Flip`, `Scenario.AdvanceVillainStage`).

Tout le reste vit dans `src/cards/pack/skrull_menace/skrull_pantheon/` et `.../dardvan_sect/` (scripts et helpers des deux sets).

## Recettes et pieges payes par ce bloc (a reporter dans `docs/reference/RECETTES-MOTEUR.md`, §7 et §1)

- **Mechant a DEUX FACES par stade** (`"villain": ["sk170a,sk170b", "sk171a,sk171b"]`, modele Typhoid Mary) : les degats, les jetons et les
  cartes d'etat/boost/attachements sont des composants de la CARTE, ils survivent donc a `card.Flip`. `Scenario.AdvanceVillainStage`
  choisit la face du stade suivant par le NOM du mechant vaincu : « Sl'gur't (I) vaincu » donne « Sl'gur't (II) » (le stade suivant arrive du
  meme cote) sans une ligne de code. Les jetons (compteur maison) restent d'un stade a l'autre ; le « When Revealed » du nouveau stade en ajoute un.
- **« Flip the villain »** : `mechant.card.Flip(effect)` (`call_reveal=True` resout le « When Revealed » de la face d'arrivee). Le moteur
  NE defausse PAS les attachements, cartes d'etat ni cartes de boost : le helper `RetournerLeMechant` les defausse avant (`GetAttachedAttachments`,
  `card.components.status.GetDeck()`, `card.components.boostable.GetDeck()`). Apres le retournement `Puzzle.*('sk170a')` ne retrouve plus la
  carte : viser la face VISIBLE.
- **« Advance to stage 2B »** (sauter la face A d'un complot) : retourner la carte du stade 2 dans `world.main_schemes_deck`
  (`card.Flip(effect, call_reveal=False)`) puis `scheme.Advance(carte.face, effect)` : `World.AdvanceMainScheme` accepte une FACE en `to_face`.
  `Advance("2A", effect)` est le chemin ordinaire (face A resolue puis face B).
- **Environnement double face mis de cote** : `"set_aside": ["sk175a,sk175b"]` ; `face.PutIntoPlay(joueur, effect)` le met en jeu face A, `card.Flip` pour la B.
- **« After resolving step one of the villain phase »** : `AbilityFactory.AfterResolveVillainPhaseStep(ForcedResponse, 1, op)` (modele hs226).
  Distribuer face cachee : `Worlds.DiscardEncounterCards(n, effect)` rend les cartes defaussees, `player.DealEncounterCard(face, effect)` les prend
  dans la defausse (revelees a l'etape 4).
- **Bonus qui suit un compteur d'une AUTRE carte** : `ThisGainKeyword(fn, attack=1, scheme=1, health=1, change_on_event=OnEvent.Counter(Villain, 'faith'))`
  (Nogor) et `GiveKeywordToAttached(Minion, scheme=1, get_new_value=fn, ex_change_on_event=OnEvent.Counter(Villain, 'faith'))` (Blessed by) :
  le bonus suit pose ET retrait de jetons. `OnEvent.Counter` ne filtre pas sur le nom du compteur (tout mouvement sur la carte rafraichit).
- **« would attack ... instead »** : `message.SetBeInstead(effect)` ; l'activation est annulee SANS carte de boost et SANS question de defense
  (preuve : `passer_sur_option="Defense"` n'est jamais pose, donc a ne PAS mettre dans le cas).
- **Harnais** : (1) un deck de test rempli de cartes UNIQUES (Sandman) boucle a l'infini des que deux exemplaires sont reveles (la regle d'unicite
  defausse + remelange + Renfort) : completer avec des cartes non uniques et inertes (`sk107` Skrull Scientist) ; (2) un deck qui s'epuise remelange sa
  defausse : prevoir des cartes de remplissage SOUS les cartes mesurees ; (3) en forme alter ego le mechant manigance et la menace atteint vite
  le seuil du complot 1B (9) : jouer en forme heros (`ChangeForm('01001b')`) + `passer_sur_option="Defense"` pour mesurer une phase du mechant ;
  (4) `carte_du_surge` exige UN SEUL exemplaire de la carte semee dans le deck ; (5) `Puzzle.PlaceThreat('<complot>', -n)` retire de la menace par le
  chemin des jetons (`AfterCardRemovedToken`) : c'est lui qui declenche « when the last threat is removed » ; (6) `Cost('2', same_type=True)` : l'Action est
  OFFERTE meme sans paire de meme type (le moteur ne teste la couleur qu'au paiement) ; le paiement mixte est refuse ; (7) un deux-joueurs
  se monte avec `heros2` ; une phase du mechant entiere : `Puzzle.RunVillainPhase()`.
