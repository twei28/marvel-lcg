# PROCESSUS-CARTE.md — les 16 gabarits du pack SPIDER-MAN NOIR (set 160, `sn`)

Gate de `PROCESSUS-HEROS.md` : un gabarit rempli par carte. Rédigés le
05/09/2026. Auteur du pack : **Rainy**, zip « Spider-Man Noir ».
Aspect **Justice**, arbitrage utilisateur (le zip n'a aucun dossier `Extras`,
donc aucune decklist).

**Preuves communes**, citées une fois :

- **Étape 7, cas** : `test_capacites.py … sn0` → **40/40**, en passe
  **parallèle** (`PARALLELES=4`) **et** en passe **séquentielle**, verdicts
  identiques un à un (l'exigence écrite en tête de `test_capacites.py`).
- **Étape 7, substitution** : `substituer_pack.py … sn0` → **16/16 cartes** ont
  au moins un cas qui tombe au rouge sans leur module.

  | Carte | rouges | Carte | rouges | Carte | rouges |
  |---|---|---|---|---|---|
  | sn001a | 3/3 | sn006 | 2/3 | sn011 | 2/2 |
  | sn001b | 3/3 | sn007 | 2/4 | sn012 | 1/2 |
  | sn002 | 2/3 | sn008 | 1/2 | sn013 | 2/2 |
  | sn003 | 1/1 | sn009 | 2/3 | sn014 | 2/4 |
  | sn004 | 1/1 | sn010 | 1/2 | sn015 | 2/3 |
  | sn005 | 1/2 | | | | |

  Les cas restés verts sont **tous** des contre-cas d'ABSENCE d'effet ou des
  lignes de base qui n'impliquent pas le module mesuré. Ils sont listés carte
  par carte plus bas, jamais masqués.
- **Étape 1** : pack `spider_man_noir` en queue de `cards.json`, set
  `160. Custom (Spider-Man Noir)`, préfixe `sn` déclaré, `verifier_prefixes` OK
  (aucun doublon, aucun préfixe non déclaré, aucun numéro emprunté).
- **Étape 4, image** : `assets/pics/sn0*.jpg` pour les 16, découpées du zip par
  `tools/importer_images_spider_man_noir.py` (la recette est le seul artefact
  reproductible, `assets/pics/` étant gitignoré).
- `test_cards` : **5288 ok / 0 erreur** (5272 avant le pack, soit **+16**).
- `verifier_desc_mots_cles spider_man_noir` : « les 16 cartes ont un desc
  conforme à leur texte ».
- `verifier_noms_modules` : « aucun nom inconnu dans spider_man_noir ».
- `verifier_cartes_en_jeu spider_man_noir` : « les 16 cartes portent ce que leur
  texte annonce ».
- `verifier_appels_modules` : « tous les appels de spider_man_noir existent » —
  **et la gate a été CALIBRÉE** (§9 de PROCESSUS-CARTE) : on lui a injecté un
  `Faces.GiveStatusQuiNExistePas` dans `sn010`, elle a rendu
  « spider_man_noir.spider_man_noir/sn010.py:42 … n'existe pas / 1 appel(s)
  inexistant(s) », puis le fichier a été remis et la gate repassée au vert. Un
  « OK » non calibré ne prouve rien.
- **Étape 3** : `deck/starter/spider_man_noir.json`, et le deck **monte une
  partie** (`verifier_tous_les_decks`, `DECK_NOM=spider_man_noir` →
  « identite sn001a, main 6, deck 34 »). Témoin `throg` dans la même fournée :
  « identite tg001a, main 6, deck 34 ».
- **Étape 10** : contrôle des signatures étrangères sur les **123 decks de
  départ** → **0 écart**.
- **Étape 7 (héros)** : biographie `sn001a` dans `heros-info.js`
  (`node --check` OK).
- **Étape 8 (héros)** : les 16 textes français dans `textes-fr-fanmade.ts`,
  **déployés** par `ui-app/deployer.sh` (« Sortie conforme », « Déployé dans 1
  installation ») — sans quoi rien n'apparaît dans le jeu (§11 du GUIDE).
- `audit_cartes` : 0 type d'argument, 0 texte-seul, 0 construction impossible,
  0 module en erreur ; **aucune des 101 suspicions « marqueur sans capacité »
  et aucun des 2 `exhaust_sans_cout` ne concerne ce pack**.
- `verifier_api_cartes` : **5920 fichiers, 3 en faute, toutes ANTÉRIEURES et
  hors de ce pack** — `blink/bk007.py` (handler jamais passé à une fabrique,
  code mort), `spot/sp018.py` (`CardFinder(..., is_odd_cost=...)`, argument
  inconnu), `web_of_deceit/underling/__init__.py` (garde sur une API
  inexistante, branche morte). Signalées, pas corrigées : autre pack, autre
  chantier.

---

## PAS DE GATE DE PORTÉE : AUCUN FICHIER MOTEUR PARTAGÉ TOUCHÉ

Contrairement au portage `throg` du même jour, **rien** hors de
`src/cards/pack/spider_man_noir/` n'a été modifié côté moteur. Le §6bis du
GUIDE (batterie complète + les 122 decks) ne s'applique donc pas ici. Les seuls
fichiers partagés touchés sont **le harnais et les données** :
`data/cards.json`, `data/sets_info.json`, `tools/prefixes_fanmade.json`,
`tools/test_capacites.py` (40 cas ajoutés), `deck/starter/`,
`data/nemesis/`, `heros-info.js`, `textes-fr-fanmade.ts`.

---

## LA MÉCANIQUE : UNE SEULE ZONE, ET LE HÉROS EST À 0 SANS ELLE

`sn001a` a **ATQ 0 et CTR 0 IMPRIMÉS** et gagne +X aux deux, X étant le nombre
de cartes glissées sous lui, plafonné à 3 à la POSE. Sans pile, ce héros ne
frappe ni ne contre : la pile n'est pas un bonus, c'est son moteur entier.
**Onze des seize cartes** la lisent ou l'alimentent.

| Carte | Ce qu'elle fait de la pile |
|---|---|
| `sn001a` Spider-Sense | la **compte** (+X ATQ/CTR) et la **remplit** (après une traîtrise) |
| `sn001b` Gumshoe | la remplit depuis le deck rencontre, **ou** échange contre du contre |
| `sn002` Guns Blazing | y **glisse le sbire** qu'elle vainc |
| `sn003` Webs Within Webs | y glisse la carte défaussée |
| `sn004` Web Shot | y **détourne une carte de boost** |
| `sn005` Web Swinging | en défausse une pour redresser, puis en **reglisse** une |
| `sn006`, `sn007`, `sn009`, `sn010` | en **défaussent** une comme coût |
| `sn011` In Walks Trouble | en **révèle une au hasard** |
| `sn013` Electro Noir | en **donne une au sbire** comme carte de boost |
| `sn014` Lightning Strikes Twice | **compte ses icônes** pour infliger des dégâts |

⚠ **LA ZONE EST PORTÉE PAR LA CARTE, PAS PAR LA FACE.**
`CardFace.GetPlacedCardArea()` rend `self.card.components.placed_card`
(`card_face.py:1017`) : les deux faces partagent la même pile. C'est ce que le
texte imprimé suppose sans le dire, en écrivant tantôt « under him » (sn001a),
« here » (sn001b), « under your hero » (sn003, sn007, sn009), « under your
identity » (sn006, sn011, sn013, sn014). **Quatre formulations, une seule
zone.** Vérifié dans le moteur, pas supposé — et c'est pour ça que les cas de
`sn001b` mesurent `pose_sous` sur `sn001b` tandis que ceux de `sn001a` le
mesurent sur `sn001a` : c'est bien la même pile.

`sn013` Electro Noir est la carte qui **retourne le pack contre lui-même** : il
prend au héros exactement ce qui fait sa force, et le laisse à 0/0 s'il vide la
pile.

---

## CE QUE LES GATES ONT TROUVÉ

### 1. `CountTotalBoostIcons` IGNORE l'étoile — `sn014` comptait faux

`sn014` dit « For each icon (**[star] and [boost]**) in the boost area of cards
tucked under your identity, take 1 damage ». Écrite d'abord avec
`FacesCounter.CountTotalBoostIcons`, elle ne comptait que la moitié :

- `CountTotalBoostIcons` (faces_counter.py:142) ne somme que
  `CountBoostIconsInternal`, c'est-à-dire les icônes **chiffrées** ;
- l'étoile vit dans une propriété séparée, `boost_star`
  (has_boost_icon.py:52), qui vaut 1 dès qu'une `AbilityType.Boost` existe ;
- **seule** `CountTotalBoostStarAndBoost` (faces_counter.py:160) additionne les
  deux.

Une pile de trois cartes à étoile seule aurait rendu **0 dégât au lieu de 3**,
et aucune gate statique ne l'aurait vu. Trouvé en lisant le moteur avant
d'écrire le cas, corrigé, et le cas mesure maintenant l'écart : `24050` Dark
Dealings porte **une icône chiffrée ET une étoile**, la carte inflige 2.

⚠ Le helper `IconesDeBoost` du set garde `CountTotalBoostIcons`, lui : `sn001b`
et `sn003` disent « the number of **boost** icons discarded », sans étoile.
**Deux comptes différents dans le même set, et c'est imprimé.**

### 2. Un coût `CostFunc.Custom` impayé n'annule RIEN : le joueur perdait sa carte

Contre-cas de `sn005`, pile vide. L'événement était **proposé, joué et
défaussé**, `CostFunc.Custom` rendait `False`, l'effet ne tombait pas — et la
carte était perdue pour rien.

La cause est dans `CostFunc.Base.HasTargets` (cost_func.py:47), qui décide si
la capacité est offerte : elle rend `True` dès que le sélecteur a une cible, or
`CostFunc.Custom(None, …)` se rabat sur `Select.From("This")`, c'est-à-dire la
carte elle-même, toujours présente. Le `False` du paiement arrive **trop tard**.

La règle imprimée, elle, interdit de payer un coût qu'on ne peut pas payer. On
conditionne donc l'OFFRE : helper `PileNonVide` posé sur les **cinq** capacités
du set dont le coût est « discard a card tucked » (`sn005`, `sn006`, `sn007`,
`sn009` Action, `sn010`). Modèle **`58008` Ionic Belt** du pack `wonder_man`,
seule autre carte du dépôt à payer sur une pile glissée, qui fait exactement
cela (`conditions=[check_mode]`, testant `len(GetTuckedCards(...)) > 0`).

**Quatre contre-cas écrits pour la famille**, un par carte à coût, plus celui
de `sn005` qui l'a trouvée.

### 3. `ResolveBoostCards` boucle à l'infini sur un « instead » qui ne déplace rien

`CanBoost.ResolveBoostCards` (can_boost.py:51-62) fait `continue` sur
`is_be_instead` **sans retirer la carte du paquet de boost** : poser
`SetBeInstead` sans faire QUITTER la carte fige la partie, et `test_capacites`
ne rendrait qu'un timeout.

Lu **avant** d'écrire `sn004` Web Shot, pas découvert après. Conséquence, et
c'est ce que dit le texte imprimé : la carte part **toujours** — « discard it
instead » est inconditionnel, « and tuck it » est ce qui lui arrive ensuite, et
seulement s'il reste de la place. Les deux branches du code sortent la carte du
paquet. Le cas prouve les deux moitiés à la fois : la partie ne se fige pas, et
la carte finit sous le héros.

### 4. Le héros défend tout seul et efface les chiffres

Cinq cas mesurent des dégâts subis par l'identité. Sans `Puzzle.Exhaust`
préalable, le pilote **déclare une défense de base** et la DEF 3 de Spider-Man
Noir annule des attaques à 1 ou 2 : les cas lisaient 0. Même leçon que `tg011`
la veille. Le héros est désormais incliné d'avance dans `sn008`, `sn013` (deux
cas) et `sn014` (deux cas).

---

## MOTS-CLÉS RENCONTRÉS

| Mot-clé | Carte | État |
|---|---|---|
| `restricted` | sn007 | fiche existante, base automatique `desc.Restricted` |
| `ranged` | sn007 | fiche existante, `AttackProperty(ranged=True)` |
| `retaliate` | sn013 | fiche existante, base automatique `desc.Retaliate` |
| `amplify` | sn012 | fiche existante, base automatique `desc.Amplify`, AUCUN script |
| `surge` | sn011, sn015 | fiche existante — ici **accordé** par `sn015` aux cartes du set, pas imprimé sur elles |
| `boost` | sn014 | fiche existante — l'étoile n'existe que si `WhenCardBecomeBoost` est écrite |
| `special` | sn001a, sn013, sn014 | fiche existante, les `[star]` codés toujours actifs (aucune mention « in expert mode ») |

**Aucune fiche n'a eu à être créée** : les sept mots-clés du pack existaient
déjà dans `docs/reference/mots-cles/`.

⚠ L'icône **Amplify** de `sn012` a été identifiée **par comparaison d'image**
avec `16054` Vendetta, carte officielle dont le `desc` déclare
`"Amplify": "1"` — jamais nommée à vue. C'est un « + » fondu dans l'icône de
boost, à ne pas confondre avec le « + » sur carte inclinée (hazard) ni avec
celui sur maison soulignée (acceleration). Leçon Lockjaw.

⚠ **`ELITE` n'est pas un mot-clé, c'est un TRAIT** (`sn013`) : il va dans
`traits`, jamais dans `desc`. De même **`AERIAL`** accordé par `sn010`.

---

## HOMONYMES ET NOMS

- ⚠ **« Spider-Man Noir » est DÉJÀ le nom de deux ALLIÉS du dépôt** : `31015`
  (pack `spdr`) et `wd118` (pack `web_of_deceit`). Un
  `CardFinder(name="Spider-Man Noir")` les attraperait. **Aucune carte du pack
  ne nomme le héros** : toutes passent par le TYPE ou par le littéral
  `"YourHero"`. Même discipline que `beta_ray_bill`, pour la raison inverse
  (là-bas les deux faces portaient le même nom).
  Et `31015` n'est pas qu'un homonyme : il porte **mot pour mot la même
  mécanique** que `sn001a` (`ThisGainKeyword` sur la taille de la pile,
  `AfterYouResolveTreachery` qui glisse la traîtrise, plafond 3 compris). La
  carte fan est une version HÉROS de cet allié, et c'est la carte de référence
  du module.
- ⚠ **« Peter Parker » est pris QUATRE fois** : `01001b` (Spider-Man officiel),
  `sr001b` (`spider_man_rainy`), `as001b` (`armored_spidey`) et `bt014`, un
  **allié** du pack `beast`. `sn011` écrit malgré tout
  `desc.GiveTo = "Peter Parker"`, comme le texte imprimé et comme les **trois**
  obligations déjà livrées qui font pareil (`01165`, `sr013`, `as014`).
  `Worlds.FindPlayerByName` rend le PREMIER joueur qui répond au nom : en solo
  c'est toujours le bon, à plusieurs avec deux Peter Parker à la table
  l'ambiguïté existe — elle est **antérieure et partagée** par les quatre
  cartes.
- Trois homonymes sans conséquence : **Enhanced Spider-Sense** (`01004` est un
  ÉVÉNEMENT de Spider-Man, `sn008` une amélioration), **Organic Webbing**
  (`30011` spiderham, `52009` silk, `sn010` la troisième), **Thunderstorm**
  (`36004` est un SOUTIEN de Storm). Le texte français s'écrit sur le
  `card_id`, jamais sur le nom.
- ⚠ **`sn013` Electro Noir n'a rien de commun** avec l'Electro de
  `web_of_deceit` (`wd042`) : aucun code partagé.
- ⚠ **Le zip numérote les deux faces à l'envers**, comme tous les packs de
  Rainy : « 0.1 » est l'ALTER-EGO (Peter Parker), « 0.2 » le HÉROS. Vérifié sur
  les libellés imprimés ALTER-EGO / HERO, pas sur le nom de fichier.
- ⚠ **`sn011` porte le bandeau SPIDER-MAN NOIR**, pas « … NEMESIS » : son
  `set_name` est celui du set héros, le module vit donc dans
  `spider_man_noir/spider_man_noir/` et non dans `…_nemesis/`. Piège `bt019`
  payé une **9ᵉ** fois, et la **5ᵉ** où il est vu AVANT d'écrire.

---

## ÉCARTS ASSUMÉS

- **`sn008`, première moitié : INTESTABLE EN SOLO.** « When **another player**
  reveals a treachery, you reveal it instead » ne peut jamais partir à une
  table d'un joueur. Elle est écrite (`WhenCardWouldReveal` avec le littéral
  `"Other"` de `Condition.CheckWhichPlayer`), elle n'a **aucun cas sujet**, et
  c'est écrit ici plutôt que laissé croire à une couverture qu'il n'y a pas.
  La seconde moitié, elle, a son cas **et** son contre-cas.
- **`sn001a`, aucun plafond sur le BONUS.** Le « (to a maximum of 3) » borne la
  POSE de cartes, pas le compte : le texte du `[star]` ne dit pas « to a maximum
  of +3 ». En pratique les deux coïncident, rien ne pouvant faire monter la pile
  au-delà de 3 — mais on code ce qui est écrit, et le plafond vit donc dans
  `GlisserSousIdentite`, pas dans le calcul du bonus.
- **`PileNonVide` est un AJOUT au texte imprimé.** Aucune des cinq cartes
  n'écrit « if there is a card tucked ». C'est la règle générale du jeu (on ne
  paie pas un coût qu'on ne peut pas payer) rendue explicite parce que le moteur
  ne l'applique pas seul (§2 ci-dessus). Choix technique au sens du §9 du GUIDE,
  consigné ici et dans le `__init__.py` du set.
- **`sn011`, « You may flip to alter-ego form ».** Le joueur qui refuse reste en
  héros et doit quand même choisir une branche — or la première exige
  d'incliner Peter Parker, qui n'est pas en jeu. En forme héros, **seule la
  seconde branche est offerte**, et c'est codé explicitement plutôt que laissé
  au hasard d'un `ForChoiceAbility` qui échouerait. C'est ce que dit la carte.
- **`Rand.RandomChoice` est DÉTERMINISTE sous `disable_shuffle`** : il rend le
  PREMIER de la liste. Les cas de `sn011` et `sn013` en profitent, mais ils ne
  prouvent donc pas le caractère aléatoire, seulement que la bonne zone est
  lue. Écrit noir sur blanc.
- **`sn013`, « a random ENCOUNTER CARD tucked »** : le filtre est
  `EncounterNonVillainCard`. La pile peut contenir un sbire vaincu (`sn002`),
  un complot annexe (`sn009`), une traîtrise (`sn001a`) : toutes sont des cartes
  de rencontre. Le filtre est donc large en pratique, mais il est écrit — une
  carte JOUEUR ne pourrait pas servir de carte de boost.

---

## CE QUE CES BLOCS NE PEUVENT PAS VOIR

⚠ **Aucune partie n'a été jouée par un humain dans le navigateur.** C'est le
seul juge de « est-ce que la carte est agréable et fait ce qu'elle promet », et
le processus demande de l'écrire noir sur blanc quand ce n'est pas fait.

**Autoplay : 8 parties contre Rhino, profil équilibré, avec `spider_man` comme
témoin dans la même fournée.**

| Deck | rounds | %V | bloquées |
|---|---|---|---|
| `spider_man_noir` | 6.1 | 0 % | **0** |
| `spider_man` (témoin) | 5.6 | 0 % | 1 |

**Grep exhaustif des journaux : 0 traceback** (`Traceback`). Le pack tient au
moins aussi bien que le témoin officiel, qui se coince une fois sur huit.
⚠ Un taux de victoire de 0 % ne dit rien du deck : le témoin officiel fait 0 %
lui aussi sur la même fournée, le pilote étant une heuristique.

**Ce que l'autoplay a réellement exercé** (comptage des actes sur les 8
parties, pas une simple apparition dans un journal) :

| Carte | déclenchements |
|---|---|
| `sn001a` Spider-Sense | 28 |
| `sn001b` Gumshoe | 22, dont 12 branches « tuck » |
| `sn006` The Black Cat Club | 13 Actions d'alter-ego, 13 branches « Draw 2 » |
| `sn002` Guns Blazing | 11 activations |
| `sn007` Dual Pistols | 9 activations, dont 3 redressées par `sn002` |
| `sn008` Enhanced Spider-Sense | 8 interruptions de héros |
| `sn009` Fancy Fedora | 6 « Remove 2 threat », 19 réponses |
| `sn010` Organic Webbing | 6 |
| `sn003` Webs Within Webs | 2 |
| `sn013` Electro Noir | 2 |
| `sn014` Lightning Strikes Twice | 2 |
| `sn011` In Walks Trouble | 1 (remise au joueur, résolue) |
| `sn012` Power Struggle | 1 (entré en jeu par `01190`) |

**Jamais activées** : `sn004` Web Shot, `sn005` Web Swinging et `sn015`
Thunderstorm. Raisons mesurées, non supposées :

- `sn004` et `sn005` sont des événements à fenêtre (Interruption, Réponse) : le
  pilote se contente de les **dépenser comme ressources**. Le journal le dit
  mot pour mot (« Web Swinging, total Y », 16 fois). Même comportement que les
  trois interruptions de `throg` la veille ;
- `sn015` est le cinquième membre du set némésis, qui n'arrive que par `01190`
  Shadow of the Past — sorti une fois sur huit, et il n'a alors amené que
  `sn012` et `sn013`.

Ces trois cartes restent prouvées par leurs cas de test **et** par la preuve par
substitution, pas par une partie. C'est écrit ici pour ne pas être pris pour une
couverture qu'il n'y a pas.

Ce qui **se lit en clair** dans les journaux, en revanche : la boucle complète
du pack, tour après tour — `Gumshoe` → `Tuck_that_card_under_your_identity` →
`Alter-Ego_Action` → `Discard_a_card_tucked_under_your_identity` →
`Draw_2_cards`, puis `Change_Form` et les Actions de héros payées sur la même
pile. C'est exactement l'économie que le pack annonce.

---

## Gabarits, carte par carte

### sn001a : * Spider-Man Noir (face héros)
- [x] Étape 2 : ⚠ `31015` * Spider-Man Noir (pack `spdr`), **l'allié officiel
      du même nom**, qui porte mot pour mot la même mécanique — c'est LA carte
      de référence, et aussi l'homonyme qui interdit tout `CardFinder(name=…)`
      dans le pack ; `52001a` * Silk pour la traîtrise résolue glissée et le
      `.SetTarget("Trigger")` ; `58001a` * Wonder Man pour le **correctif** :
      `get_new_value` passe par `asset_helper.check_fn`, qui fait
      `CastTo(CanAttach)` — posé sur une identité, cela lève
      « AssertionError: face_type=CanAttach » et rend la création de partie
      IMPOSSIBLE. `ThisGainKeyword` est la fabrique prévue pour un bonus
      dynamique porté par la carte elle-même.
- [x] Étape 5 : « +X ATK **and** THW » → LES DEUX sur le même
      `ThisGainKeyword` (`attack=1, thwart=1`), pas deux capacités.
      « the number of cards tucked under him » → `GetPlacedCardArea().GetSize()`,
      recalculé par `OnEvent.PlacedCard("Here")`. ⚠ **« Here » et non
      « Identity »** : le littéral « Identity » est un `# Hack` du moteur
      (on_event.py:419) qui rend True pour N'IMPORTE QUEL tuck, où qu'il soit ;
      Wonder Man devait s'en servir parce que sa pile est sur un SOUTIEN, ici
      elle est sur la carte qui porte la capacité. « tuck that card **here** » →
      CETTE carte, mot-piège « that » (`wd022`).
- [x] Étape 6 : **PV 10, CTR 0, ATQ 0, DEF 3, main 5.** ⚠ ATQ 0 et CTR 0 sont
      IMPRIMÉS ; DEF 3 est fixe, les étoiles ne sont sur CTR et ATQ que.
      Aucune limite imprimée.
- [x] Étape 7 : 3 cas, **rouges 3/3** — la Réponse, le bonus +2/+2 sur deux
      cartes glissées, et le plafond à 3.
- [x] Étape 7 bis : limite imprimée **NON**. Le plafond « (to a maximum of 3) »
      a néanmoins son contre-cas : quatre traîtrises révélées, la pile reste à
      3 et le bonus à +3.

**Carte terminée : OUI**

### sn001b : * Peter Parker (face alter-ego)
- [x] Étape 2 : `15004` / `ho014` pour `Worlds.DiscardEncounterTopCard` (qui
      rend la carte défaussée) et `FacesCounter.CountTotalBoostIcons` ;
      `ho009` pour `CostFunc.Custom(None, fn)` ; `01151` Under Attack /
      `br007` pour un `ChooseAbilities` à deux branches.
- [x] Étape 5 : ⚠ **la flèche est APRÈS « Discard the top card »** : défausser
      est le COÛT, le choix est l'effet. La différence se voit quand le deck de
      rencontre est vide — l'Action n'est alors pas proposée du tout.
      « choose to **either** … **or** … » → branches exclusives ; le pilote
      prend la première par défaut (RECETTES §2), les deux cas forcent celle
      qu'ils mesurent par `preferer_option`. « tuck **that** card » →
      mot-piège `wd022`. « equal to the number of boost icons **discarded** » →
      les icônes de LA carte défaussée, sans étoile (c'est `sn014` qui compte
      l'étoile).
- [x] Étape 6 : PV 10, REC 4, main 6. Limite une fois par ROUND.
- [x] Étape 7 : 3 cas, **rouges 3/3**.
- [x] Étape 7 bis : limite imprimée **OUI**. Témoin : deux Actions dans le même
      round, la seconde par `declencher_tolerant`. Chiffre mesuré :
      `taille_pose_sous: 1` — une seule carte glissée, pas deux.

**Carte terminée : OUI**

### sn002 : Guns Blazing — **OUI**
(3 cas, rouges 2/3 ; le vert est le contre-cas « pile pleine », qui mesure une
ABSENCE. ⚠ « if this attack defeats **a minion** » et non « un ennemi » :
modèle `th009`/`ag006`, `if_this_attack_defeats` appelé PAR UNITÉ VAINCUE.
« tuck it **from the encounter discard pile** » : le sbire y est déjà arrivé
quand la fonction est appelée, on ne le repêche pas, on le déplace — montage
`52001a`. « and ready Dual Pistols » est INCONDITIONNEL, hors de la branche, et
le cas nominal le prouve sur une attaque qui ne vainc personne.)

### sn003 : Webs Within Webs — **OUI**
(1 cas, rouge 1/1 ; « equal to **3 plus** » — 3 est un plancher, `24050` porte
une icône donc 4 menaces retirées. La seconde phrase « Tuck the discarded
card » n'est PAS une branche : elle tombe toujours, et le même cas la mesure.)

### sn004 : Web Shot — **OUI**
(1 cas, rouge 1/1 ; ⚠ **carte à boucle infinie si on la code de travers**, voir
« ce que les gates ont trouvé » §3. « during an **enemy** activation » → vilain
OU sbire, donc PAS de `boost_for_card=Villain` contrairement à `sd020`.)

### sn005 : Web Swinging — **OUI**
(2 cas, rouge 1/2 ; le vert est le contre-cas pile vide, qui mesure une ABSENCE
— **et c'est lui qui a trouvé le défaut du §2**. ⚠ Le coût se paie sur la MÊME
pile que l'effet remplit : on défausse d'abord, on reglisse ensuite, et le cas
nominal le prouve en changeant le CONTENU de la pile à taille constante.)

### sn006 : * The Black Cat Club — **OUI**
(3 cas, rouges 2/3 ; le vert est le contre-cas pile vide. ⚠ DEUX coûts devant
la flèche, incliner ET défausser une carte glissée : piège `wd005`, où une
moitié de coût avait été perdue. « **Alter-Ego** Action » : indisponible en
forme héros, ce qui fait de ce club le seul endroit où la pile se convertit en
cartes ou en soins.)

### sn007 : Dual Pistols — **OUI**
(4 cas, rouges 2/4 ; les deux verts sont la **ligne de base** — l'attaque de
base, qui n'implique pas le module et se prend la Riposte — et le contre-cas
pile vide. C'est cette ligne de base à **1 dégât de Riposte** qui donne son sens
au **0** du cas `ranged` : sans elle, un zéro pourrait venir d'une Riposte
jamais appliquée, §7bis de RECETTES-MOTEUR. ⚠ PAS unique : le nom n'est pas
précédé de l'étoile sur le scan.)

### sn008 : Enhanced Spider-Sense — **OUI**
(2 cas, rouge 1/2 ; le vert est le contre-cas « un SBIRE attaque, on ne pioche
pas ». ⚠ « When **the villain** initiates an attack » et non « an enemy » :
mot-piège relevé à la relecture, et c'est exactement ce que le contre-cas
mesure. ⚠ La première moitié de la carte est **intestable en solo**, voir
« écarts assumés ». « draw 1 card » dans une INTERRUPTION : la carte piochée
arrive avant la résolution, elle peut encore être jouée en défense.)

### sn009 : Fancy Fedora — **OUI**
(3 cas, rouges 2/3 ; le vert est le contre-cas pile vide de l'Action. ⚠ « After
you **thwart and defeat** a side scheme » → `is_from_thwart=True`, la différence
avec `52001a` qui dit seulement « defeat » est imprimée. ⚠ « **Response** » et
non « Hero Response » : elle vaut aussi en forme civile, contre-intuitif sur une
carte de héros mais jouable — un allié peut contrer pendant qu'on est en civil.
⚠ RECETTES §3 : la classe des complots annexes est `SchemeSide2`, `SideScheme`
N'EXISTE PAS dans `cards.pack`.)

### sn010 : Organic Webbing — **OUI**
(2 cas, rouge 1/2 ; le vert est le contre-cas pile vide, qui mesure **deux**
absences — le héros reste incliné ET `traits_absents: [AERIAL]`. ⚠ « until the
end of the round » → `GainUntilRoundEnd`, pas un bonus permanent et pas « for
this use » : piège `tt001a`, où la différence était imprimée.)

### sn011 : In Walks Trouble — **OUI**
(2 cas, rouges 2/2 ; ⚠ bandeau SPIDER-MAN NOIR donc module dans
`spider_man_noir/spider_man_noir/`, piège `bt019` payé une **9ᵉ** fois.
⚠ « If you cannot, this card gains surge » : « you cannot » = pile VIDE,
mot-piège `wd028`, et le cas prouve que la branche est ATTEIGNABLE en mesurant
la menace posée par la carte supplémentaire révélée. Deux sorties différentes :
la première branche RETIRE DU JEU, la seconde DÉFAUSSE.)

### sn012 : Power Struggle — **OUI**
(2 cas, rouge 1/2 ; le vert est le contre-cas « contrer un AUTRE complot ne
fait rien subir », qui mesure une ABSENCE et prouve le littéral `"This"`.
⚠ « When **a character** thwarts this scheme » : n'importe quel personnage, un
allié encaisse aussi. ⚠ **FORCED INTERRUPT** : le dégât tombe AVANT que la
menace ne parte, un allié à 1 PV meurt donc sans avoir contré. Icône Amplify
identifiée par comparaison d'image, base automatique, aucun script.)

### sn013 : * Electro Noir — **OUI**
(2 cas, rouges 2/2 ; la branche nominale prouvée par la pile qui passe de 1 à
**0**, le repli « Otherwise » par l'écart de dégâts **1 → 3** — un sbire ne
reçoit aucune carte de boost de lui-même, les 2 icônes de `01103` Shocker
viennent donc bien du repli. ⚠ « **Otherwise** » n'est pas un choix : mot-piège
relevé à l'étape 5.)

### sn014 : Lightning Strikes Twice — **OUI**
(4 cas, rouges 2/4 ; les deux verts sont le contre-cas « aucune icône, aucun
dégât » et la **ligne de base** du ★ Boost — `01186` Advance sans étoile, une
seule activation à 2 dégâts, contre au moins 4 avec la carte. ⚠ Voir « ce que
les gates ont trouvé » §1 pour le comptage des icônes. ⚠ « **After** this
activation » et non « maintenant » : `RunAt.AfterEnemyActivationEnd`
(run_at.py:175) puis `DoActivate`, modèle `15027`. ⚠ **Il n'existe aucun helper
`ThisEnemyActivatesAgain`** : API inventée, écartée au grep avant d'être
écrite. Le message de boost porte l'activation sur `message.would_atk_message`,
à lire avec `getattr(..., None)` : elle n'existe pas quand le boost sert une
MANIGANCE.)

### sn015 : Thunderstorm — **OUI**
(3 cas, rouges 2/3 ; le vert est le contre-cas « en forme civile, aucun
dégât », qui mesure une ABSENCE et prouve le mot-piège « **if** they are in
hero form ». ⚠ « Cards from **this set** gain surge » → filtre sur le
`set_name` du set némésis, et il inclut cette carte-ci, d'où le « (including
this one) » de la phrase suivante. « **1 indirect** damage » →
`TakeIndirectDamage`, que le joueur peut répartir sur ses alliés. Coût
`Cost("YY")` relevé sur le scan, payé dans le cas par deux cartes à icône
[energy].)

**16 cartes terminées sur 16.**
