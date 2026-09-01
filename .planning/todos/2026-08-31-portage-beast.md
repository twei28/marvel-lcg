# Portage BEAST (Hank McCoy) — set 134, préfixe `bt`, pack `beast`

**Source** : `A créer/BEAST (X-MEN)-20260829T085944Z-1-001.zip` (29 images, aucun
rulebook, aucune decklist d'aspect).
**Plan** : item n° 11 de `.planning/todos/2026-08-29-plan-heros-vilains-fanmade.md`,
groupe A, difficulté 2/5.
**Aspect du deck de départ** : **Protection** (choix utilisateur du 31/08/2026 ;
motif : DEF 3 imprimé, Thick Skinned récompense l'encaissement à 0, Experimental
Warfare est un événement DEFENSE, Civilian Disguise pioche après chaque défense,
Hunter Gear donne +1 DEF).

---

## 1. Inventaire du zip → card_id

24 entrées distinctes. La numérotation imprimée « n/15 » et « n/5 » est reportée
en commentaire.

### Identité
| card_id | Carte | Imprimé |
|---|---|---|
| `bt001a` | * Beast (Hero) | THW 1 / ATK 2 / DEF 3 / HS 5 / PV 13 |
| `bt001b` | * Dr Hank McCoy (AlterEgo) | REC 4 / HS 6 / PV 13 |

### Signature (16 exemplaires, 13 card_id)
| card_id | Carte | Imprimé | Ex. |
|---|---|---|---|
| `bt002` | * Wonder Man | 1/15, allié 3, RES R | 1 |
| `bt003` | * Phoenix | 1B/15, allié 3, RES R | 1 |
| `bt004` | Experimental Warfare | 2/15, event 1, RES B | 1 |
| `bt005` | Fighting With Friends | 3/15 + 4/15, event 1, RES Y | 2 |
| `bt006` | In The Heat Of Battle | 5/15, event 2, RES B | 1 |
| `bt007a` | Multi-Tasking | 6/15, event 1, **RES B** | 1 |
| `bt007b` | Multi-Tasking | 7/15, event 1, **RES R** | 1 |
| `bt008` | Primal Rage | 8/15 + 9/15, event 0, RES R | 2 |
| `bt009` | Alien Materials | 10/15 + 11/15, ressource **double YB** | 2 |
| `bt010` | Beast's Lab | 12/15, support 4, RES B | 1 |
| `bt011` | Hank's Kimono | 13/15, support 1, RES Y | 1 |
| `bt012` | Civilian Disguise | 14/15, support 1, RES B | 1 |
| `bt013` | Hunter Gear | 15/15, upgrade 2, RES R | 1 |

### Discovery (5, hors-deck)
| card_id | Carte | Imprimé |
|---|---|---|
| `bt014` | * Peter Parker | 1/5, allié 2, RES G |
| `bt015` | Space Hand Grenade | 2/5, upgrade 1, RES Y |
| `bt016` | Ambush | 3/5, event 0, RES R |
| `bt017` | Automated Life-Support | 4/5, upgrade 2, RES B |
| `bt018` | Mecha-Beast | 5/5, upgrade 3, RES R |

### Obligation et némésis
| card_id | Carte | Imprimé | Ex. |
|---|---|---|---|
| `bt019` | Unfinished Projects | obligation, boost 2 | 1 |
| `bt020` | Lizard-Fied Mutants | 1/5 + 2/5, sbire 4 PV, boost 2 | 2 |
| `bt021` | Dark Transformation | 3/5, traîtrise, boost 1 | 1 |
| `bt022` | Dark Beast | 4/5, sbire 6 PV, boost 3 | 1 |
| `bt023` | Mutant Science Program | 5/5, complot annexe 5[per_hero], boost 2 | 1 |

## 2. Ce que la lecture des images a corrigé

- **Multi-Tasking 6/15 et 7/15 ne sont PAS deux copies** : même texte, mais
  l'icône de ressource diffère (mental / physique). Deux card_id, sur le
  précédent `01043a/b/c/d` (Wakanda Forever!, quatre ressources). Fighting With
  Friends, Primal Rage et Alien Materials sont, eux, de vraies copies.
- **Alien Materials est une ressource DOUBLE** (`RES: "YB"`, énergie + mental),
  comme `01088` Energy (`YY`) ou `01044` Vibranium (`GG`).
- Les icônes ont été lues coin par coin, jamais au nom du fichier (leçon
  Lockjaw) : c'est ce contrôle qui a séparé `bt007a` de `bt007b`.

## 3. Contenu manquant ou incohérent dans le zip (à trancher avec l'utilisateur)

1. **« Mutation Degeneration »** : l'obligation `bt019` dit « remove Mutation
   Degeneration from the game », mais aucune carte de ce nom n'est dans le zip
   et aucune carte du némésis ne la met en jeu.
2. **« Lizard-Fied Minion »** : `bt023` va chercher « the Lizard-Fied Minion »,
   alors que le sbire du pack s'appelle « Lizard-Fied Mutant**s** ».
3. **Wonder Man 1/15 et Phoenix 1B/15** : deux alliés au texte identique mais
   aux traits différents (AVENGER / PSIONIC.X-MEN) qui se partagent le
   numéro 1. Deck de 16 cartes signature, ou choix entre les deux ?
4. **`bt006` In The Heat Of Battle** : « **shuffle** 1 discovery card into your
   **hand** » — on ne mélange pas dans une main.
5. **`bt001b` Setup** : « All cards you mulligan from your hand during setup are
   shuffled back into your deck » — le moteur ne donne pas prise sur le
   mulligan de mise en place.

## 4. Fichiers moteur PARTAGÉS à modifier (règle de portée §6bis du GUIDE)

- `src/game/card/face/card_face.py`, énum `TRAITS` : ajouter **`LIZARD`**
  (`bt020`). Purement déclaratif (`Literal` de typage, aucun contrôle à
  l'exécution).
- `src/game/card/face/card_face.py`, énum `COUNTER` : ajouter **`disguise`**
  (`bt012`, « Enters play with 3 disguise counters »). `test` (`bt023`) y est
  **déjà**. Celui-ci est lu à l'exécution par `IsCounter`.

→ Une **batterie complète** est donc due APRÈS le portage. Les deux ajouts sont
additifs : aucune carte existante ne les emploie.

## 5. Incident du 31/08/2026 — deux harnais en parallèle

La batterie de la session précédente (PID 268915, `/tmp/rapport-batterie-aa.json`,
port 50000, démarrée à 21:12) **n'était pas morte** : le rapport était absent
parce qu'il n'est écrit qu'à la fin. En vérifiant les ports libres (`ss`) mais
pas les processus (`pgrep`), une seconde batterie a été lancée à 21:38 et les
deux ont tourné ensemble jusqu'à 21:46 — exactement ce que le harnais interdit
(chaque fils réécrit `.game-src/launch.json`).

- La seconde a été tuée à 21:46 ; la première a fini à 23:24.

**Résultat de la batterie (23:24, `/tmp/rapport-batterie-aa.json`) : 835/862**,
et le détail des 27 échecs valide le diagnostic mot pour mot :

| Nature | Nombre | Détail |
|---|---|---|
| Faux échecs `ip/port` | **22** | Une tranche contiguë (`mk006`, `lj005`…`lj027`, `20001a`, `mf006`, `mf007`, `th006`…`th015`, `iw013`…`iw016`, `gp002`, `gp010`, `ht007`, `58001a`) : exactement les cas joués pendant les 8 minutes de chevauchement. |
| Vrais rouges | **5** | `sg006`, `sg007`, `sg009`, `sg013`, `ss012` — les **cinq rouges PRÉEXISTANTS** de `.planning/todos/2026-08-31-cas-rouges-sg-ss.md`, ni un de plus. |

→ **Aucune régression d'Agatha Harkness.** Les 22 faux échecs sont imputables
à la double batterie, et la batterie finale du §4 les rejouera.
- **Leçon, à porter dans RECETTES-MOTEUR.md §7** : avant de lancer un harnais,
  `pgrep -af test_capacites` — un port libre ne prouve pas qu'aucune passe ne
  tourne, puisque chaque cas ouvre puis referme son port.

## 6. À DEMANDER À L'AUTEUR — les 13 points relevés sur le pack

Liste destinée à être envoyée telle quelle. Chaque point donne le texte
imprimé, le problème, et ce qui a été codé en attendant (décision utilisateur
du 31/08/2026). Rien n'est bloquant : le pack tourne avec ces lectures.

### A. Contenu manquant ou nom qui ne correspond à rien

1. **« Mutation Degeneration » n'existe pas** (obligation *Unfinished
   Projects*). Le texte dit « Discard 2 upgrade/support cards in play →
   remove Mutation Degeneration from the game », mais aucune carte de ce nom
   n'est dans le pack et rien ne la met en jeu.
   *Codé* : comme le nom de l'obligation elle-même (elle est retirée de la
   partie), sur le modèle de l'obligation officielle *Chaotic Forces*, qui a
   exactement cette structure. **Est-ce une carte oubliée dans le zip, ou un
   ancien nom de l'obligation ?**

2. **« the Lizard-Fied Minion » n'existe pas** (*Mutant Science Program*). Le
   sbire du set némésis s'appelle « Lizard-Fied Mutant**s** ».
   *Codé* : c'est bien lui. **Confirmer.**

3. **Que devient *Mutant Science Program* à 0 compteur de test ?** Le texte
   n'en dit rien.
   *Codé* : elle reste en jeu, sa capacité cesse simplement de partir ; il
   faut la contrer normalement (5 menaces par héros).

### B. Textes qui se contredisent ou tournent en boucle

4. **« shuffle 1 discovery card into your **hand** »** (*In The Heat Of
   Battle*). On ne mélange pas dans une main. À noter que *Dr Hank McCoy* dit,
   lui, « shuffle 1 random discovery card into your **deck** ».
   *Codé* : mélangée dans le **deck**, le verbe l'emporte sur la zone.
   **Était-ce « add to your hand » ?**

5. **« repeat this hero action » = boucle infinie** (*Multi-Tasking*). La
   condition « If this was the first card you played this turn » reste vraie
   pendant la répétition : relue à chaque tour de boucle, l'effet ne s'arrête
   jamais.
   *Codé* : **une seule** répétition (l'effet se résout deux fois au total).

6. **« Hero **Response**: Ready your hero »** (*Fighting With Friends*) n'a
   aucun déclencheur (« After… »), donc aucune fenêtre où partir.
   *Codé* : comme une **Hero Action**. **Y avait-il un déclencheur prévu ?**

7. **« **Forced** Interrupt » sur un événement joué depuis la main**
   (*Ambush*). « Forced » veut dire que la carte part toute seule, sans que le
   joueur choisisse — inhabituel pour un événement (la carte officielle
   comparable, *Grasping Tendrils*, est une « Hero Interrupt »).
   *Codé* : **vraiment obligatoire**, conformément au mot imprimé.

8. **« **Action**: … → generate a resource »** (*Peter Parker*, *Hunter
   Gear*). Une capacité qui produit une ressource se libelle « **Resource**: »
   dans le jeu ; en « Action », la ressource arrive hors du paiement d'une
   carte et ne sert à rien. Le moteur n'accepte d'ailleurs que
   Resource / Hero Resource / Alter-Ego Resource.
   *Codé* : « **Resource** ». **Confirmer.**

9. ***Dr Hank McCoy*, « Setup »** : « All cards you mulligan from your hand
   during setup are shuffled back into your deck. » Aucun moteur ne donne
   prise sur le mulligan ; il a fallu ajouter le point d'accroche.
   *Codé* : fidèlement, hook moteur ajouté.

### C. Portées non qualifiées (le texte ne dit pas « you control »)

10. **« Exhaust **all upgrade cards in play** »** (*Experimental Warfare*).
    Toutes celles de la table, ou seulement les tiennes ?
    *Codé* : **les tiennes**. À la lettre, en multijoueur, Beast inclinerait
    l'équipement de tout le monde pour se protéger seul.

11. **« exhaust **an support card in play** »** (*Ambush*). Même question.
    *Codé* : **un des tiens**.

12. **« **All allies** are confused »** (*Dark Beast*). Ceux de tous les
    joueurs, ou seulement ceux du joueur qui a la némésis ?
    *Codé* : **tous les alliés en jeu**, à la lettre. Les sets némésis
    officiels ne visent d'habitude que leur propre joueur.

### D. Structure du pack

13. **Deux cartes n° 1 et une carte n° 1B.** *Wonder Man* (1/15) et *Phoenix*
    (1B/15) ont le même texte et les mêmes valeurs, mais des traits différents
    (AVENGER / PSIONIC. X-MEN) : le deck signature ferait 16 cartes au lieu
    des 15 annoncées. Par ailleurs *Multi-Tasking* **6/15 porte une ressource
    mentale et 7/15 une ressource physique** — ce ne sont donc pas deux copies
    de la même carte, contrairement à *Fighting With Friends*, *Primal Rage*
    et *Alien Materials* qui sont, eux, de vrais doublons.
    *Codé* : deux decks de départ proposés au choix dans l'assistant, l'un
    avec Wonder Man, l'autre avec Phoenix ; les deux Multi-Tasking sont
    conservées telles quelles. **La différence de ressource est-elle
    volontaire ?**

## 7. Fichiers moteur PARTAGÉS touchés — le relevé complet

Quatre, pas deux : le portage en a découvert deux de plus en cours de route.
Tous les quatre sont **additifs** (aucun comportement existant ne change), mais
tous les quatre déclenchent la règle de portée §6bis du GUIDE.

| Fichier | Ajout | Pourquoi | Découvert |
|---|---|---|---|
| `card_face.py` | trait `LIZARD` | `bt020`. `TRAITS` n'est qu'un `Literal` de typage, aucun contrôle ne le lit à l'exécution. | prévu |
| `card_face.py` | compteur `disguise` | `bt012` (`Uses: "3,disguise"`). Lu à l'exécution par `IsCounter` : sans lui, la carte tombe à la construction du deck. | prévu |
| `sender_player.py`, `player_phase.py`, `factory/setup.py` | message + envoi + fabrique `AfterPlayerResolveMulligans` | `bt001b` Setup. Le moteur n'avait AUCUN point d'accroche sur le mulligan : `WhenPlayerResolveMulligans` existait mais n'était jamais `.Send()`. | prévu (décision utilisateur) |
| `ability.py` | `ForcedInterrupt` dans `check_sub_type` | `bt016` Ambush. `ForcedInterrupt` manquait à la chaîne et tombait sur la branche qui n'autorise **aucun** libellé : le seul montage du deck levait `AssertionError: label='defense' … [bt016]`. **Exactement le même défaut que le correctif `AlterEgoResponse` du 4/8/2026.** | en montant le deck |

`tools/test_capacites.py` a également reçu trois clés de vérification neuves
(`dans_deck_joueur`, `mis_de_cote`, `taille_mis_de_cote`) : sans elles, aucune
capacité du pool Discovery n'était prouvable, une carte mélangée dans le deck
n'étant ni en jeu, ni en main, ni dans la défausse.

## 8. Journal des étapes

- **Étape 1, `data/cards.json`** : 25 entrées (`bt001a`…`bt023`), pack en queue
  de fichier, `custom: "Arnaud"`, checksums recalculés. ✅
- **Étape 2, scripts** : 18 modules dans `src/cards/pack/beast/{beast,
  beast_nemesis}/`. Pas de module pour `bt009` (ressource double sans texte) ni
  `bt020` (Guard/Patrol/Boost sont des bases automatiques). ✅
- **Étape 3, decks de départ** : `deck/starter/beast.json` (Wonder Man) et
  `deck/custom/beast_phoenix.json` (Phoenix), 15 cartes signature + 5 mises de
  côté + 25 cartes Protection chacun. Contrôle des signatures étrangères et des
  limites d'exemplaires : **0 anomalie**. ✅
- **Étape 4, `data/nemesis/beast_nemesis.json`** ✅
- **Étape 5, `data/sets_info.json`** : `134. Custom (Beast)` ✅ ;
  `tools/prefixes_fanmade.json` passé à 25 cartes ✅
- **Étape 6, images** : 25 fichiers dans `assets/pics/`. `bt023` a dû être
  **pivotée de 90°** : l'auteur livre le complot annexe en portrait, alors que
  la convention du moteur est le paysage droit (référence : `01107`). ✅
  ⚠ **Défaut préexistant relevé au passage** : `aa015` (complot annexe
  d'Agatha) est stocké pivoté, donc affiché de travers en jeu. Hors périmètre
  de ce portage, à corriger séparément.
- **Étape 7, biographie** : `bt001a` dans `heros-info.js` ✅ (survol dans le
  wizard **non vérifié**, voir §9)
- **Étape 8, textes FR** : 24 entrées dans `textes-fr-fanmade.ts` ✅
- **Montage du deck en partie réelle** : `identite bt001a, main 6, deck 34`,
  après correction de `ability.py`. ✅
- **Étape 9, `PROCESSUS-CARTE.md` par carte** : 24 cas écrits dans
  `test_capacites.py`, préfixe `bt0`. **24/24** à la troisième passe.

### Ce que les cas ont trouvé (et que rien d'autre n'aurait vu)

Trois passes ont été nécessaires : 15/24, puis 21/24, puis 24/24. Le tri entre
« mon cas est faux » et « mon module est faux » s'est fait **journal en main**,
jamais au jugé.

**Un seul VRAI défaut de module, mais il était fatal :**

- **`bt004` Experimental Warfare** — deux bugs successifs, tous deux invisibles
  à l'analyse statique :
  1. `AttributeError: 'Upgrade' object has no attribute 'CanBeExhaust'` en
     pleine défense. La méthode du moteur est `CanExhaust()`, sans argument ;
     de toute façon `Faces.ExhaustAll` fait déjà le tri, et c'est sa valeur de
     retour qu'il faut compter. **`verifier_api_cartes.py` n'a rien vu**
     (5575 fichiers analysés, 4 en faute, toutes préexistantes) : il ne
     contrôle pas les appels de méthode sur une face obtenue par filtrage.
  2. La seconde phrase (« si l'attaque a fait 0 dégât ») était montée sur
     `RegisterTemp` + `AbilityType.Temp0`, sur le modèle de ho006. **Elle ne
     s'est jamais déclenchée** — le journal montre la défense résolue à 0 puis
     « n'appliquent plus Experimental Warfare », sans que rien ne parte.
     Remontée sur `RunAt.AfterEnemyActivationEnd`, avec la condition « 0 dégât »
     lue directement sur les PV relevés avant l'attaque.

**Cinq cas faux, cinq leçons de harnais** (les modules, eux, marchaient) :

| Cas | Ce que le journal montrait | Correction |
|---|---|---|
| `bt001a` | La capacité partait, trouvait Counter-Punch… **et le pilote la jouait dans la foulée** : la carte n'était donc plus en main. | Poser une **ressource** (`01090`) sur le deck : le pilote ne peut pas la jouer. |
| `bt008` | « Rhino va attaquer Beast » — `Puzzle.Attack(card)` fait attaquer `card`, ce n'est pas la cible. | `Puzzle.Attack('bt001a', '01094')`. |
| `bt006` | `wd009` n'est pas une manigance annexe mais la **traîtrise Feedback**, qui étourdit tout le monde. | `01107` Breakin' & Takin', 2 menaces : les 4 de l'événement la vident, ce qui prouve **aussi** le bonus Discovery. |
| `bt014` | Peter Parker s'inclinait bien et payait… puis **`bt005` le redressait** (chaîne aval, RECETTES §7). | Payer `22034` Defensive Training, qui ne redresse rien. |
| `bt015` | Hydra Mercenary (3 PV) encaissait les 4 dégâts et **tombait** : `degats_min` ne trouvait plus la carte. | Prouver sa disparition (`hors_jeu`) plutôt que ses dégâts. |
| `bt010`, `bt011` | La clé `"action"` **n'existe pas** dans le harnais. | `declencher: ["Puzzle.Action('bt010')"]`. |
| `bt001b` | `Rand.RandomChoice` n'a pas rendu `bt014` : l'ordre du `set_aside` n'est pas garanti. | Compter le pool (`taille_mis_de_cote: 4`) au lieu de nommer la carte tirée. |

**Et un module qui n'était même pas chargé** — le plus grave, parce que
totalement silencieux :

- **`bt019` Unfinished Projects** : l'obligation entrait en jeu et ne faisait
  **rien**. Le moteur cherche le module dans le dossier du **`set_name`**
  (`cards.pack.<pack>.<CleanName(set_name)>.<card_id>`, database.py:195) ;
  `bt019` porte `set_name: "Beast"` mais son fichier était rangé dans
  `beast_nemesis/`. Le repli `_nemesis → nemesis-moins-le-suffixe` fonctionne
  dans un seul sens, jamais l'inverse. **Aucune erreur, aucun avertissement.**
  Seule l'absence de cas l'a fait remonter, via `substituer_pack.py`
  (« bt019 : AUCUN CAS »). Fichier déplacé dans `beast/`.

### Étape 8, autoplay ciblé — et le défaut que seul l'autoplay a vu

**Première fournée** : 8 parties Beast contre Rhino, 8 parties du témoin
Agatha Harkness. Grep exhaustif : **4 parties sur 8 en faute chez Beast, 0 chez
le témoin.** Toutes la même erreur :

- **`bt011` Hank's Kimono** : `TypeError: Search.PlayerCard() missing 1
  required keyword-only argument: 'include_player_deck'`. Le paramètre n'a
  **aucune valeur par défaut** (search.py:133) : il faut le passer même pour
  dire « non ». La carte plantait à **chaque** activation.
- **Le cas de test, lui, était au VERT.** Faux vert : le coût d'inclinaison est
  payé avant le plantage, et la ressource cherchée remontait dans le deck par
  le remélange de la défausse, satisfaisant `dans_deck_joueur`. Le cas a été
  durci avec `defausse_joueur: 0`, qui aurait attrapé le défaut.

**Seconde fournée, après correction** : 8 parties, **grep exhaustif = 0 partout**.

| | parties | victoires | rounds tenus | incidents |
|---|---|---|---|---|
| Beast | 8 | 0 | **6,1** | 0 |
| Agatha (témoin) | 8 | 0 | 5,0 | 0 |

0 % de victoire pour les deux : c'est le comportement connu de ce pilote contre
Rhino (Harry Osborn et Venompool font 0 % eux aussi, cf. journal Agatha). Beast
tient **plus longtemps** que le témoin, ce qu'on attend d'un personnage à DEF 3.

**Lecture des journaux** — les capacités partent vraiment :

- `"Thick_Skinned": 2` sur 11 rounds relevés, et `"Thick_Skinned": 4` sur 4
  autres : la capacité vedette se déclenche plusieurs fois par round.
- `"Discard_2_upgrade/support_cards_in_play_→_remove_this_obligation_from_the_game"`
  apparaît dans le journal : la branche issue de **l'arbitrage `bt019`** est
  jouée en partie réelle.
- 23 des 24 cartes du pack apparaissent en jeu. **Seule `bt018` Mecha-Beast
  n'est jamais vue** : carte Discovery à coût 3, elle doit d'abord rejoindre le
  deck par un passage en alter-ego, puis être piochée et payée — improbable en
  6 rounds. Sa preuve reste son cas de test.

### Batterie complète finale — 01/09/2026, `884 / 889`

Due parce que le portage a touché 4 fichiers moteur PARTAGÉS (§7). Lancée
seule, 2 h 15, `/tmp/rapport-batterie-finale.json`.

| Nature | Nombre | Détail |
|---|---|---|
| Verts | **884** | dont les **27/27** du pack `bt` |
| Rouges | **5** | `sg006`, `sg007`, `sg009`, `sg013`, `ss012` — les **cinq rouges PRÉEXISTANTS** de `.planning/todos/2026-08-31-cas-rouges-sg-ss.md`, ni un de plus |

→ **Aucune régression.** C'est le contrôle qui comptait vraiment : le hook de
mulligan s'exécute à la mise en place de **toutes** les parties, et
`check_sub_type` (ability.py) valide les capacités de **toutes** les cartes.
Les 884 verts couvrent une centaine de héros sans rapport avec Beast.

À comparer à la batterie de la veille (835/862, dont 22 faux échecs `ip/port`
dus à la double exécution) : cette passe-ci a tourné **seule**, et elle est
donc la seule qui fasse foi.

### Contrôles statiques

- `verifier_api_cartes.py` : 5575 fichiers, **4 en faute, toutes préexistantes**
  (spot, web_of_deceit), aucune dans `beast`. ⚠ Il n'a vu **ni** le
  `CanBeExhaust` de `bt004`, **ni** l'argument manquant de `bt011`.
- `verifier_coherence_cartes.py` : **0 image manquante, 0 obligation sans
  destinataire, 0 carte joueur sans classe d'aspect** pour `beast`.
- `substituer_pack.py` : **23/23 cartes**, tous les cas rouges sans leur module
  — aucun cas vert sous substitution (Agatha était à 20/22).
- `test_capacites.py [bt0]` : **27/27**.

## 8bis. SUITE PRÉVUE : une seconde version du pack Beast

L'utilisateur a signalé le 01/09/2026 une **autre version de Beast**, à porter
ensuite :

> https://drive.google.com/drive/folders/1f1jobxF_og5U2nMnhr1qUMQX8KkJm63T

**À faire AVANT de poster la liste de questions à l'auteur**
(`2026-09-01-beast-questions-auteur-EN.md`) : comparer les deux versions carte
par carte. Si c'est une révision, elle a peut-être déjà corrigé une partie des
13 points, et les poser ferait perdre du temps à tout le monde. Les candidats
les plus probables :

- « Mutation Degeneration » (carte fantôme de l'obligation) ;
- « shuffle 1 discovery card into your **hand** » ;
- « repeat this hero action » sans borne ;
- « Hero **Response** » sans déclencheur sur Fighting With Friends ;
- les deux cartes n° 1 (Wonder Man 1/15 et Phoenix 1B/15).

**Décision à prendre à ce moment-là** : la nouvelle version REMPLACE-t-elle le
set 134, ou coexiste-t-elle comme variante ? Précédent du projet : « Doctor
Doom Alt Arts » face à « Doctor Doom Hero Revised », que le plan fan-made
(§1) tranche en comparant les textes AVANT de décider — même art et même texte
donnent un simple jeu d'illustrations, pas un pack indépendant.

## 8ter. Gate `PROCESSUS-CARTE.md` — les 25 gabarits

Rédigés le 01/09/2026 dans
`.planning/todos/2026-09-01-beast-gabarits-processus-carte.md`, un par carte,
avec les preuves des étapes 2, 5, 6, 7 et 8.

**Résultat : 25 « OUI » sur 25.**

`bt001b` était d'abord à NON, faute de cas pour sa capacité `Setup` : le pilote
du harnais ne savait pas mulliganer. Le trou a été fermé le 01/09/2026 en
ajoutant au pilote la clé **`mulligan: "all" | [card_id, …]`** (l'option porte
le nom exact « Resolve Mulligans », trouvé par `TRACE_OPTIONS`). Clé additive :
sans elle, `option_mulligan()` rend `None` et la boucle historique reprend la
main, donc aucun cas existant ne change.

Le cas « bt001b Setup » vérifie `defausse_joueur: 0` **et** `taille_main: 6` :
le second prouve que la repioche a lieu AVANT le remélange. Substitution :
**rouge**, `defausse du joueur = 6 carte(s) (attendu 0)`.

`test_capacites.py [bt0]` : **28/28**.

→ **Il ne reste, pour la gate de `PROCESSUS-HEROS.md`, qu'une partie complète
jouée à la main.**

## 9. Ce que ces contrôles ne peuvent pas voir — reste à faire

- **Une vraie partie jouée à la main** (gate finale) : non faite.
- **Le survol de la biographie dans le wizard** : non vérifié (preuve exigée
  par l'étape 7 de `PROCESSUS-HEROS.md`).
- **Le déploiement `ui-app`** (textes FR côté client) : non refait.
- **`bt001b` Setup (mulligan)** : le harnais ne sait pas piloter un mulligan de
  mise en place — il n'y a aucune décision à intercepter dans un cas Puzzle. La
  capacité est donc **prouvée par le code et non par un cas**, ce qui est le
  seul trou de couverture du pack. À vérifier en partie réelle : écarter une
  carte au mulligan, puis constater qu'elle est dans le deck et non dans la
  défausse.
- **Le deck variante `beast_phoenix.json`** : `verifier_tous_les_decks.py` ne
  parcourt que `deck/starter/`, la variante n'est donc pas montée
  automatiquement. Elle ne diffère que par un card_id (`bt003` au lieu de
  `bt002`), tous deux couverts par un cas.
