# Portage du pack VENOMPOOL — journal de validation

Set 129, préfixe `vp`, 17 `card_id`. Auteur **CptScorp**, *Marvel Champions
Custom Project*, Cycle 2. Zip source : `A créer/Venompool (Council
Released)-20260813T091211Z-1-001.zip`.

Ce document tient le gabarit `PROCESSUS-CARTE.md` pour chaque carte du pack,
comme l'exige la « Gate finale » de `PROCESSUS-HEROS.md`.

---

## 0. Ce que le pack apporte au projet, au-delà du héros

### `drain X` a enfin une définition imprimée

L'insert du pack (« Venompool Insert.png ») définit le mot-clé maison resté
sans définition depuis `agent_anti_venom` :

> « When an ability instructs you to drain X from an enemy, deal X damage to
> that enemy, then heal X damage from your identity. »

C'est **mot pour mot** la lecture arbitrée à l'aveugle avec l'utilisateur le
4/8/2026. `docs/reference/mots-cles/drain-x.md` est mis à jour : la
convention n'est plus une supposition, et la question systématique qu'exigeait
la fiche avant tout nouvel appel à `Drain()` n'a plus lieu d'être.

### L'icône du side scheme, identifiée par comparaison d'image

`vp012` Shocking Entrance porte une icône « + sur une forme ». Plutôt que de
la nommer à vue (leçon Lockjaw, `PROCESSUS-CARTE.md` étape 3), elle a été
découpée du scan puis superposée aux icônes officielles :

| Carte | Icône | Forme |
|---|---|---|
| 01107 Breakin' & Takin' | **hazard** | « + » sur une **carte inclinée** |
| 01109 Bomb Scare | acceleration | « + » sur une **maison soulignée** |
| **vp012 Shocking Entrance** | **hazard** ✔ | « + » sur une carte inclinée |

`desc.Hazard = "1"`, pas `Acceleration`.

### Quatre homonymes préexistants

| Nom | Carte déjà présente | Conséquence |
|---|---|---|
| **Wade Wilson** | `44001b`, alter-ego officiel de Deadpool | `desc.GiveTo` de `vp011` se résout **par nom** (`Worlds.FindPlayerByName`). L'insert du pack interdit lui-même de jouer Deadpool et Venompool ensemble. |
| **Venompool** | `dt105`, allié de l'aspect fan-made Determination | Un allié à son propre nom est **exclu** du deck. Les modules ne résolvent jamais « Venompool » par son nom, toujours par le joueur (`GetVenompool`). |
| **Black Cat** | `01002` (allié signature de Spider-Man), `wd045` (sbire Electro) | Classe `Hero` : jamais mélangeable. |
| **Thwip!** / **Foresight** | `sr003` (Spider-Man Rainy), `mw009` (Madame Web) | Événements signature d'autres héros, classe `Hero`. |

Tout est consigné dans `metadata.collision_note` de `deck/starter/venompool.json`.

---

## 1. Étapes de `PROCESSUS-HEROS.md`

| Étape | État | Preuve |
|---|---|---|
| 1. Cartes dans `data/cards.json` | ✅ | 17 `card_id`, diff de **305 lignes ajoutées / 0 supprimée** |
| 2. Scripts | ✅ | 17 modules, `test_cards` 4895 → **4912 ok / 0 err** |
| 3. Deck de départ | ✅ | `deck/starter/venompool.json`, 15 signature + 25 aspect/basiques |
| 4. `data/nemesis/…` | ⬜ | facultatif (UI), non fourni |
| 5. `data/sets_info.json` | ✅ | set « 129. Custom (Venompool) » |
| 6. Images | ✅ | 17 `.jpg` en 975 px extraits des scans du zip |
| 7. Biographie | ✅ | `vp001a` dans `heros-info.js`, `node --check` propre |
| 8. Textes français | ✅ | 17 entrées, `tsc --noEmit` propre |
| 9. Validation carte par carte | 🟡 | 7 cas verts + 3 substitutions, §3 et §4 |
| 10. Points transverses | ✅ | 0 carte signature étrangère dans un `player_deck` |

**Aspect** : contrairement à `ms_america` et `patriot`, l'auteur fournit sa
decklist complète (planche « Venompool Starter Deck ») — aspect **Protection**,
aucun choix à faire.

---

## 2. Arbitrages posés à l'utilisateur

| Carte | Question | Réponse (31/08/2026) |
|---|---|---|
| `vp016` Psyche Warp | « the ally with the highest printed ATK » : quels alliés ? | **Tes alliés seulement.** En multi, la carte ne peut pas défausser l'allié d'un coéquipier. |

Points **non** soumis à question, et pourquoi :

- **`vp007` « attacks » vs `vp010` « makes a basic attack »** : le contraste est
  imprimé dans le même pack, il est donc voulu. `is_basic_attack=None` sur
  l'un, `True` sur l'autre.
- **`vp001a` « Limit 1 [per_hero] per phase »** : sur une carte d'identité,
  l'icône joueur ne peut désigner que le porteur — personne d'autre ne
  déclenche la Response d'une identité qui n'est pas la sienne.
- **`vp006` « Each enemy may only be targeted once »** : rendu par l'absence de
  `repeat_rules`, là où `vp003` (« divided as you choose ») en a besoin. Choix
  technique, pas arbitrage de règles.
- **`vp011` « You MUST flip »** : `48026` et `16053`, les deux obligations
  modèles, disent « you MAY flip ». Le changement de forme est ici **forcé**,
  le helper `YouMayFlipToYourAlterEgoForm` n'est donc pas utilisé.

---

## 3. Les trois bugs trouvés par les cas de comportement

Aucun n'était visible pour `test_cards`, qui rendait **4912 ok / 0 err** avec
les trois en place. C'est exactement ce que `PROCESSUS-CARTE.md` annonce :
construire une capacité ne prouve pas qu'elle s'exécute.

### a. `vp003` — l'assertion qui empêchait la partie de monter

`AssertionError: face.paper.card_id='vp003'`, levée au **setup**. Le moteur
exige qu'un événement n'ait qu'**une** capacité `Play` ; celui-ci en a deux,
parce que sa portée change (« 4 damage divided among enemies, 6 instead if
True Form is in play ») et que `range` est figé à la construction.

Correctif : déclaration dans la liste blanche de `game/card/factory.py`, aux
côtés de `ht009`, `mk008`, `kb005` — et surtout de **`13006` Wasp Sting**,
déjà là pour exactement la même raison (formes GIANT / TINY).

### b. `KILLER_THRILL_NAME` — le piège du `*` d'unicité, tombé dedans après l'avoir lu

La constante cherchait `"* Killer Thrill"`. `cards/paper.py:46` retire le
préfixe (`lstrip("* ")`) : la recherche ne trouvait **rien, en silence**, et
ni Coldwar ni Guzz ne gagnaient jamais leur bonus. Piège déjà documenté sur
`pt012` « * Patriot's Shield ». Un commentaire d'avertissement est désormais
en tête de `venompool_nemesis/__init__.py`.

### c. `vp010` — `Upgrade` n'a pas de méthode `Discard()`

`this.Discard(effect)` levait un `AttributeError` **dans le handler**. Le
déclencheur `AfterCardLeavePlay`, lui, était correct — c'est la trace qui
l'a prouvé. Remplacé par `Faces.DiscardAll([this], effect)`.

---

## 4. Cas de comportement : 7/7, avec preuves par substitution

| Carte | Capacité couverte | Cas | Substitution |
|---|---|---|---|
| `vp002` | contre de base ignore crisis | ✅ | — |
| `vp009` | +3 points de vie | ✅ | — |
| `vp009` | `drain 1`, **les deux moitiés** | ✅ | ✅ sans le module : 0 dégât au lieu de 1 **et** identité à 4 au lieu de 3 |
| `vp010` | défausse quand Klyntar Suit part | ✅ | ✅ sans le module : la carte reste en jeu |
| `vp013` | +1 ATK par compteur d'adrénaline | ✅ | — |
| `vp014` | +1 ATK tant que Killer Thrill est là | ✅ | ✅ étoile réintroduite : le bonus disparaît |
| `vp015` | +1 SCH tant que Killer Thrill est là | ✅ | — |

### Trois pièges de mise en place, consignés dans le `pourquoi` du cas `drain`

1. Sans `ChangeToFace` préalable, `Puzzle.Damage('vp001a')` **instancie une
   seconde identité** dans l'aside deck, et le rendu lève `AssertionError`
   (modèles `ma005`, `hd001a`, qui font tous le `ChangeToFace` d'abord).
2. La face se désigne par **`card_id`** (`vp001b`), jamais par « Wade
   Wilson » : c'est l'homonyme de `44001b`, l'alter-ego de Deadpool.
3. L'attaquant doit être un **sbire** (ATK fixe, pas de carte de boost) et le
   héros **épuisé**. Avec Rhino, le pilote défendait, les dégâts tombaient à
   0 et la Response ne partait pas : **le module avait raison, c'était le cas
   qui était faux.**

---

## 5. Étape 8 : autoplay ciblé — fait

8 parties `venompool` contre 8 parties `deadpool` en **témoin** (le témoin
naturel : l'insert du pack dit que c'est le même personnage), même vilain
(Rhino), même difficulté, même profil, mêmes graines.

| deck | parties | V | D | rounds | incidents |
|---|---|---|---|---|---|
| **venompool** | 8 | 0 | 8 | **5,4** | **0** |
| deadpool (témoin) | 8 | 0 | 8 | 4,5 | **0** |

Causes de fin **identiques** des deux côtés : 7 « Main Scheme Completed »,
1 « All players eliminated ». Le 0 % de victoire est une propriété du
pilote heuristique, pas du pack — le guide prévient qu'un taux absolu ne
veut rien dire. Venompool tient même une manche de plus que son témoin.

**Grep exhaustif** des 8 journaux (`NameError|AttributeError|TypeError|
KeyError|AssertionError`) : **0 partout**.

**Lecture des journaux** : les **17 `card_id` du pack** apparaissent en
partie réelle, identité et set némésis compris. Aucune carte n'est restée
lettre morte.

---

## 6. Batterie finale (31/08/2026)

| Preuve | Référence | Après portage |
|---|---|---|
| `test_cards` | 4895 ok / 0 err | **4912 ok / 0 err** (+17) |
| `verifier_tous_les_decks` | 104/104 | **105/105** |
| `verifier_prefixes` | propre | propre |
| `verifier_coherence_cartes` | 0 obligation orpheline, 0 image manquante | identique |
| `launch.json` du jeu | `127.0.0.1:2345` | `127.0.0.1:2345` |
| `git diff --stat` | propre | propre |

---

## 7. Cas de comportement : 25/25, avec 15 preuves par substitution

| Carte | Capacité | Cas | Substitution : sans le module |
|---|---|---|---|
| `vp001a` | Fear Factor | ✅ | menace 8 au lieu de 7 |
| `vp001b` | REC **bloquée** > 3 PV | ✅ | « autorisée à 7 PV » |
| `vp001b` | REC **autorisée** ≤ 3 PV | ✅ | — (l'autre moitié de la même condition) |
| `vp001b` | Unexpected Bond | ✅ | — |
| `vp002` | ignore les icônes de crise | ✅ | — |
| `vp003` | 4 dégâts **sans** True Form | ✅ | 6 dégâts (branche élargie) |
| `vp003` | 6 dégâts **avec** True Form | ✅ | 4 dégâts (branche rétrécie) |
| `vp005` | étourdit le vilain | ✅ | — |
| `vp005` | « instead » : 3 menaces | ✅ | menace 9 au lieu de 6 |
| `vp008` | Foresight (3 effets) | ✅ | — |
| `vp009` | +3 points de vie | ✅ | — |
| `vp009` | `drain 1`, les deux moitiés | ✅ | 0 dégât **et** identité à 4 |
| `vp010` | défausse en cascade | ✅ | reste en jeu |
| `vp012` | 3 dégâts indirects (révélation) | ✅ | — |
| `vp012` | 1 dégât indirect (Boost) | ✅ | 2 au lieu de 3 |
| `vp013` | +1 ATK par compteur | ✅ | — |
| `vp014` | +1 ATK si Killer Thrill | ✅ | étoile réintroduite : bonus perdu |
| `vp015` | +1 SCH si Killer Thrill | ✅ | — |
| `vp016` | meilleur allié par ATQ imprimée | ✅ | 0 dégât |
| `vp016` | aucun allié → surge | ✅ | — |
| `vp004` | Tasty Meal, les **4** effets | ✅ | les trois bonus de stats disparaissent |
| `vp006` | Whack-a-Rabbit, borne calculée | ✅ | un seul déclenchement au lieu de deux |
| `vp007` | soin après attaque | ✅ | identité à 3 dégâts au lieu de 2 |
| `vp011` | flip **forcé** en alter-ego | ✅ | face active reste `vp001a` |
| `vp015` | Plotting | ✅ | la menace du complot ne monte pas |

La paire `vp003` est la plus probante : **chaque cas passe au rouge quand on
lui donne la portée de l'autre branche**, ce qui prouve non seulement que
chaque branche fait son travail, mais que la condition True Form choisit
bien la bonne des deux.

### `vp013` Forced Interrupt : hors de portée du harnais, prouvé autrement

Aucune commande `Puzzle` ne termine une phase (`End()` ne fait que relâcher
le mode « skip »), et `kb012 Kate's Bow`, qui porte le **même** déclencheur
`WhenPlayerPhaseEnd`, contourne de la même façon. La preuve vient donc des
journaux d'autoplay, qui jouent de vraies phases :

```
323: Killer Thrill activates
324: would place 1 'adrenaline' counter
325: reçoit 1 compteur(s) « adrenaline »
447: reçoit 1 compteur(s) « adrenaline »
449: perd 2 compteur(s) « adrenaline »
```

Toute la chaîne y est : pose automatique, franchissement du seuil de 2,
retrait de **tous** les compteurs, activation.

---

## 8. Trois cas qui ne prouvaient RIEN — et comment on l'a su

C'est la preuve par substitution qui les a démasqués, pas la lecture.

**a. La menace qui coïncidait.** Fear Factor et Thwip! posaient le complot
`01109` puis attendaient une menace de **2** après retrait. Or 2 est
exactement la `StartingThreat` de cette carte : les deux cas passaient
module débranché. Valeurs portées à 8 → 7 et 9 → 6.

**b. Le cas qui plafonnait à la place du module.** Les deux cas de `vp003`
fournissaient respectivement 4 et 6 cibles. La différence venait donc du
**cas**, pas de la carte. Les deux en fournissent 6 désormais, et c'est à la
carte de plafonner à 4 sans True Form.

**c'. La face de mise en place.** Le complot principal en jeu est `01097b`,
pas `01097a` : cette dernière n'est que la face de setup et `par_id` ne la
trouve pas. 73 cas du fichier utilisaient déjà `01097b`.

**c. Le décalage d'indices.** `test_capacites` ne se pilote que par
`CAS_INDEX`, un **rang**. Retirer le cas `vp013` a décalé tous les suivants :
deux substitutions ont visé la mauvaise carte et sont revenues vertes à
tort. Le journal de partie l'a montré — je croyais lancer « vilain déjà
étourdi », le moteur exécutait « étourdit le vilain ».

**Règle qui en découle** : relever la table des indices avant toute
substitution, et faire afficher au script la neutralisation effective dans
le fichier avant de lancer.

---

## 9. Ce qui reste — la gate n'est pas franchie

`PROCESSUS-HEROS.md` est catégorique : **« Pas de héros à moitié validé »**.

- **La partie réelle au navigateur n'a pas été faite.** Le processus la
  désigne comme le seul juge de « est-ce que la carte est **agréable** et
  fait ce qu'elle promet ». L'autoplay prouve qu'aucune carte ne plante, pas
  qu'elles sont plaisantes à jouer, ni que l'équilibrage tient.
- **Une seule capacité reste sans cas sujet** : le `[star]` Boost de
  `vp014`/`vp015` (« deal this card to yourself as a facedown encounter
  card »). Son mécanisme est repris **mot pour mot** de `bw021 Imperius
  Rex!`, avec le piège de redirection que cette carte documente elle-même
  (le moteur range une carte de boost APRÈS la résolution de son effet, il
  faut détourner le rangement à venir). `bw021` n'a pas non plus de cas pour
  cette moitié-là.
- Le piercing conditionnel de `vp004` (« if True Form is in play, this
  attack gains piercing ») n'est pas isolé par un cas : les quatre autres
  effets de la carte le sont.

### Point matériel

`assets/pics/` est hors git : les 17 images ne vivent que dans le dossier du
jeu, et sont **postérieures** à la sauvegarde
`~/marvel-backups/pics-2026-08-31.tar`. Elles restent régénérables depuis le
zip de `A créer/`.
