# PROCESSUS-CARTE.md — les 13 gabarits du pack BLACK CAT (set 161, `bc`)

Gate de `PROCESSUS-HEROS.md` : un gabarit rempli par carte. Rédigés le
05/09/2026. Auteur du pack : **Rainy**, zip « Black Cat ».
Aspect **Protection**, arbitrage utilisateur (le zip n'a aucune decklist).

**Preuves communes**, citées une fois :

- **Étape 7, cas** : `test_capacites.py … bc0` → **29/29**, en passe
  **parallèle** (`PARALLELES=4`) **et** en passe **séquentielle**, verdicts
  identiques un à un.
  ⚠ Une passe parallèle a rendu **28/29** avec « processus mort » sur `bc003`,
  trace `AttributeError: type object 'Engine' has no attribute 'game'` à
  l'initialisation. Ce n'est **pas** une régression mais la collision de ports
  décrite en tête de `test_capacites.py` (un run précédent encore en
  TIME_WAIT). Le cas relancé seul sur une plage éloignée passe. Écrit ici
  plutôt que masqué.
- **Étape 7, substitution** : `substituer_pack.py … bc0` → **13/13 cartes** ont
  au moins un cas qui tombe au rouge sans leur module.

  | Carte | rouges | Carte | rouges | Carte | rouges |
  |---|---|---|---|---|---|
  | bc001a | 2/3 | bc005 | 1/1 | bc009 | 1/2 |
  | bc001b | 2/3 | bc006 | 1/1 | bc010 | 2/3 |
  | bc002 | 1/2 | bc007 | 1/2 | bc011 | 2/2 |
  | bc003 | 2/2 | bc008 | 2/2 | bc012 | 2/2 |
  | bc004 | 4/5 | | | | |

  Les cas restés verts sont **tous** des contre-cas d'ABSENCE d'effet ou des
  lignes de base. Ils sont listés carte par carte plus bas, jamais masqués.
  ⚠ Le filtre de `substituer_pack.py` est **`card_id` + une espace** : un cas
  nommé « bc001a/bc001b … » n'était compté que pour `bc001b`. Renommé
  « bc001a et bc001b … » pour que les deux le portent.
- **Étape 1** : pack `black_cat` en queue de `cards.json`, set
  `161. Custom (Black Cat)`, préfixe `bc` déclaré, `verifier_prefixes` OK.
  ⚠ La clé de pack de `cards.json`, le `name` de `sets_info.json`, le dossier
  de module et le nom du deck valent tous **`black_cat`** :
  `FileManager.CleanName("Black Cat")` rend `black_cat`, et les gates prennent
  ce nom en argument. Écrit d'abord `blackcat`, ce qui donnait des gates
  vertes sur **0 carte** — un « OK » qui ne mesurait rien.
- **Étape 4, image** : `assets/pics/bc0*.jpg` pour les 13, découpées du zip par
  `tools/importer_images_black_cat.py`.
- `test_cards` : **5301 ok / 0 erreur** (5288 avant le pack, soit **+13**).
- `verifier_desc_mots_cles black_cat` : « les 13 cartes ont un desc conforme à
  leur texte ».
- `verifier_noms_modules` / `verifier_cartes_en_jeu` : OK sur les 13.
- `verifier_appels_modules` : « tous les appels de black_cat existent » —
  **et la gate a été CALIBRÉE** (§9 de PROCESSUS-CARTE) : `Faces
  .GiveStatusQuiNExistePas` injecté dans `bc009`, elle a rendu
  « black_cat.black_cat/bc009.py:48 … n'existe pas / 1 appel(s) inexistant(s) »,
  puis le fichier a été remis et la gate repassée au vert.
- **Étape 3** : `deck/starter/black_cat.json`, et le deck **monte une partie**
  (`verifier_tous_les_decks`, `DECK_NOM=black_cat` → « identite bc001a, main 6,
  deck 35 »).
- **Étape 10** : contrôle des signatures étrangères sur les **124 decks de
  départ** → **0 écart**.
- **Étape 7 (héros)** : biographie `bc001a` dans `heros-info.js`
  (`node --check` OK).
- **Étape 8 (héros)** : les 13 textes français dans `textes-fr-fanmade.ts`,
  **déployés** par `ui-app/deployer.sh`.
- `audit_cartes` : 0 type d'argument, 0 texte-seul, 0 construction impossible,
  0 module en erreur. **Deux suspicions « marqueur sans capacité » nouvelles,
  toutes deux FAUSSES et expliquées** : `bc004` et `bc010` contiennent la
  chaîne « Hero Action » **entre guillemets, comme donnée** (« an attachment
  with the text "Hero Action" »), et l'audit y voit un marqueur d'aptitude
  manquant. Le texte est fidèle à la carte imprimée : on ne le change pas.
- `verifier_api_cartes` : **5935 fichiers, 3 en faute, toutes ANTÉRIEURES et
  hors de ce pack** (`blink/bk007.py`, `spot/sp018.py`,
  `web_of_deceit/underling/__init__.py`).

---

## PAS DE GATE DE PORTÉE : AUCUN FICHIER MOTEUR PARTAGÉ TOUCHÉ

Rien hors de `src/cards/pack/black_cat/` n'a été modifié côté moteur. Le §6bis
du GUIDE ne s'applique pas. En particulier **le compteur `web` existait déjà**
dans l'énum `COUNTER` (`card_face.py:156`) : aucun correctif, contrairement à
`foe` pour throg.

---

## CE QUE LE ZIP CONTIENT, ET CE QU'IL NE CONTIENT PAS

**13 fichiers, et c'est tout le pack.** Deux faces, neuf cartes signature
(dont Spider-Man en deux versions), une obligation.

⚠ **AUCUN SET NÉMÉSIS.** Pas une carte de rencontre. `nemesis_set` est donc
**vide** dans le deck de départ, cas unique sur les 124 decks. Vérifié et non
supposé : le deck monte une partie, et `01190` Shadow of the Past ne trouve
alors aucun sbire de némésis à mettre en jeu, donc **gagne simplement
Déferlement** — ce que son propre texte prévoit (« If your nemesis minion does
not enter the game this way, this card gains surge »). Rien à inventer, rien à
emprunter à un autre héros. Le plan de portage notait déjà le même manque pour
le pack `hulk` du même auteur.

⚠ **`bc002` et `bc003` sont DEUX CARTES**, pas deux illustrations. Toutes deux
« BLACK CAT (1/15) », toutes deux `* Spider-Man` :

| | `bc002` (noir) | `bc003` (rouge) |
|---|---|---|
| PV | 4 | 3 |
| Traits | SYMBIOTE. WEB-WARRIOR. | AVENGER. |
| Dégâts consécutifs | **aucun** | 1 sur ATQ et CTR |
| Capacité | ★ Forced Interrupt sur les pouvoirs de base | Interrupt qui **annule une activation** |
| `Multiverse` | non | **oui** |

Le `hero_deck` compte donc **16 entrées pour 15 cartes numérotées**, précédent
`thor_jane_foster` (16 entrées, pour la même raison).

---

## LA MÉCANIQUE : UNE PILE, ET DES ICÔNES DE BONUS COMME MONNAIE

Le pack tient sur deux choses à la fois :

1. **la PILE glissée sous l'identité**, plafonnée à 3 ;
2. **les ICÔNES DE BONUS des cartes de rencontre**, lues partout comme une
   monnaie : dégâts (`bc006`, `bc008`), menace retirée (`bc005`), prévention
   (`bc011`), malus à l'ennemi (`bc007`), et **substitution pure** (`bc001a`).

⚠ **LE PLAFOND DE 3 N'EST PAS UN PLAFOND DE POSE.** Les deux faces impriment
« If there are **more than** 3 tucked cards here, discard all but 3 of those
cards » : on **peut** dépasser 3, et une règle continue ramène la pile à 3
**après coup**, la joueuse choisissant lesquelles garder. C'est l'inverse du
pack `spider_man_noir` livré le matin même, dont chaque carte imprime
« (to a maximum of 3) » et **refuse** la pose. Recopier `GlisserSousIdentite`
de Noir aurait été faux, et la différence est **observable** : ici une carte
entre toujours, et c'est une **autre** qui peut partir.

⚠ **LA ZONE EST PORTÉE PAR LA CARTE, PAS PAR LA FACE**
(`card_face.py:1017`) : les deux faces partagent la pile. Le texte imprimé le
suppose sans le dire, en écrivant tantôt « here » (bc001a, bc001b), « under
Black Cat » (bc005, bc006, bc008, bc009), « under your hero » (bc007), « under
your identity » (bc010, bc012). **Quatre formulations, une seule zone.**

⚠ **DEUX COMPTES D'ICÔNES DIFFÉRENTS DANS LE MÊME SET, ET C'EST IMPRIMÉ.**
Cinq cartes écrivent « each icon (**[star] and [boost]**) » → `IconesEtEtoiles`
(`CountTotalBoostStarAndBoost`). **Deux** ne le précisent pas — `bc002` (« each
boost icon ([boost]) ») et `bc008` (« the number of icons ») → `IconesSeules`
(`CountTotalBoostIcons`, qui **ignore l'étoile**, faces_counter.py:142).
Harmoniser aurait été une erreur : sur `bc008` l'écart est même **le sel de la
carte**, puisqu'une carte à étoile seule y vaut 0 dégât et déclenche donc la
branche de consolation « If that number was 0, tuck it ».

---

## CE QUE LES GATES ONT TROUVÉ

### 1. Tychokinesis **vide la pile que les autres cartes essaient de remplir**

Découvert en écrivant le cas de la règle des 3 cartes. Première écriture :
glisser trois cartes avec `bc005` et `bc006`, puis une quatrième avec `bc007`.
Le cas lisait **1** au lieu de 3, et le journal l'explique ligne par ligne :
`bc006` Lucky Hit **compte** des icônes → le moteur envoie
`WhenBoostIconsWouldBeCount` → **Tychokinesis se déclenche** → elle consomme la
carte glissée et la défausse. La pile se vide au moment même où on la remplit.

Ce n'est pas un défaut, c'est le pack : `bc001a` est branchée sur *tout*
comptage d'icônes, y compris ceux de ses propres cartes. La seule carte du
pack qui glisse **sans jamais compter** est la Response de `bc010` — d'où les
quatre attachements volés coup sur coup dans le cas final. Écrit dans le
« pourquoi » du cas pour qu'un futur lecteur ne refasse pas le chemin.

### 2. `Puzzle.SetThreat` ne peut pas BAISSER la menace de `bc004`

Deux cas « When Defeated » lisaient une main inchangée. Le journal dit
« **Threat cannot be removed from Big Heist** » : `Puzzle.SetThreat` **retire**
de la menace, et le verrou imprimé sur la carte elle-même (« Only THIEF
characters can remove threat ») le refuse — le harnais n'est pas un personnage
VOLEUR. Le complot restait donc à 4 et n'était jamais vaincu. Corrigé en
contrant **deux fois**, l'héroïne redressée entre les deux.

### 3. L'allié se déclarait DÉFENSEUR et effaçait le chiffre mesuré

Contre-cas de `bc003` : l'identité lisait 0 dégât alors qu'elle aurait dû
encaisser. Le pilote déclarait **l'allié** défenseur (`bc003` a 3 PV, Rhino
frappe à 2). Un zéro qui ne prouvait rien. L'allié est désormais incliné
d'avance, comme l'héroïne. Même famille que la leçon `tg011` de la veille,
appliquée cette fois à un allié.

### 4. `bc002` n'a AUCUN dégât consécutif imprimé, et le montage évident ne
partait donc jamais

Le bloc de statistiques porte « 2★ » — l'étoile de la capacité Special — et
**pas** l'éclat des dégâts consécutifs, que `bc003` porte, lui. Vérifié par
**découpe d'image** des deux blocs côte à côte, jamais à vue (leçon Lockjaw).
Dans les données, l'éclat s'écrit avec un **astérisque dans la valeur**
(`can_attack.py:47-52`, `value.count('*')`) : d'où `"ATK": "2"` sur `bc002` et
`"ATK": "2*"` sur `bc003`.

Conséquence directe : `WhenAllyWouldTakeConsequentialDamage` n'est envoyé **que
si la valeur imprimée est déjà > 0** (`ally.py:41-46`). Le montage naturel —
un temp accroché à ce message qui appelle `IncreaseDamage` — ne serait **jamais
parti**, et le cas serait resté vert en ne mesurant rien. On augmente donc la
**valeur** elle-même, modèle `33016` Coordinated Attack (qui la baisse de 1 par
le même appel).

### 5. `bc010` était injouable en partie réelle, et seul l'autoplay l'a vu

`AfterCardDiscard(Response, None, …)` se déclenche sur **chaque défausse de la
partie**, et une Response est **optionnelle** : le moteur pose donc la question
à chaque fois, même quand l'opération va sortir aussitôt. Mesure de l'autoplay,
8 parties : **250 questions « Response », dont 243 pour cette seule carte.**
Les trois tests étaient écrits dans le corps de l'opération ; déplacés dans
`conditions`, ils ne changent **rien** au résultat et suppriment la question.
Après correction, même fournée : **10 questions**, mêmes 7,5 rounds, mêmes
causes de fin.

⚠ **Défaut d'ERGONOMIE, invisible pour toutes les gates statiques et pour les
cas de test.** Seule une partie réellement jouée le montre. À retenir pour
toute capacité branchée sur un message fréquent (`AfterCardDiscard`,
`AfterCardsMoved`, `WhenBoostIconsWouldBeCount`) : **le filtre va dans
`conditions`, jamais dans le corps.**

### 6. `Search.Collection` existe, et la « brique 4 » n'en était pas une

Le plan de portage donnait « recherche dans toute la COLLECTION » pour la
difficulté majeure du pack, et le journal de `wd029` Multiverse Recruit assume
un **écart** sur ce même texte. Or `Search.Collection` (`search.py:371`) fait
exactement cela : elle interroge `CardsDB.GetPapers`, **fabrique** la carte
choisie dans la défausse du joueur et la rend. Mécanique officielle, portée par
`44009`, `50171` et `dz031` Tribute. Le cas le prouve en partie : `01057`
Combat Training arrive en jeu **sans qu'un seul point de ressource soit
dépensé**.

⚠ **L'écart assumé par `wd029` est donc ÉVITABLE.** Consigné ici pour qu'on y
revienne — ce n'est pas le chantier de ce pack.

---

## MOTS-CLÉS RENCONTRÉS

| Mot-clé | Carte | État |
|---|---|---|
| `Multiverse` | bc003 | ❌ **absent des fiches → fiche `multiverse.md` CRÉÉE**. Employé par TROIS auteurs (`ra002` rainy, `bw003` brawn, `bc003`) et défini par AUCUN. Définition arbitrée : marqueur de deckbuilding, **zéro ligne de code**, l'unicité native fait tout le travail |
| `special` | bc001a, bc002 | fiche existante, les `[star]` codés toujours actifs |
| `boost` | tout le pack | fiche existante — et la distinction icône chiffrée / étoile est ici **imprimée deux fois différemment**, voir plus haut |

⚠ **`MULTIVERSE` est aussi un TRAIT** (`wd029`), et les deux notions n'ont rien
à voir : un trait va dans `traits`, ce mot-clé-ci ne va nulle part.
⚠ **`THIEF` est un TRAIT**, pas un mot-clé : il n'était porté que par **trois**
cartes du dépôt avant ce pack (`37001a`/`37001b` * Gambit et `48021` * Gambit
allié). En solo avec Black Cat, il n'y a donc **qu'elle** pour contrer
`bc004`.

---

## HOMONYMES ET NOMS

- ⚠ **« * Black Cat » est DÉJÀ le nom de TROIS cartes** : `01002` (alliée du
  set Spider-Man), `wd045` (**SBIRE** du set Electro) et `vp002` (alliée de
  Venompool). Aucune carte du pack ne cherche l'héroïne par son nom : toutes
  passent par le TYPE ou par `"YourHero"`.
- ⚠ **« * Spider-Man » existe QUINZE fois au dépôt** (`01001a` en tête). Les
  deux alliés du pack sont les seizième et dix-septième.
- ⚠ **« Grappling Hook » est déjà `08008`** (amélioration Black Widow) **et
  `50069`** (attachement Black Widow). `bc009` est la troisième. Le texte
  français s'écrit sur le `card_id`.
- ⚠ **« Cat Burglary » est un homonyme INTERNE au pack** : c'est à la fois le
  libellé de la capacité de `bc001b` et le nom de la carte `bc005`. Les deux
  coexistent sur la table.
- ✅ **« Felicia Hardy » n'a AUCUN homonyme** au dépôt : le `desc.GiveTo` de
  l'obligation est sans ambiguïté, contrairement à « Peter Parker », pris
  quatre fois et payé la veille sur `sn011`.
- ⚠ **Le zip numérote les deux faces à l'envers** : « 0.1 » est l'ALTER-EGO,
  « 0.2 » le HÉROS. Vérifié sur les libellés imprimés.
- ⚠ **`bc012` porte le bandeau BLACK CAT**, pas « … NEMESIS » : le module vit
  dans `black_cat/black_cat/`. Piège `bt019` payé une **10ᵉ** fois, et la
  **6ᵉ** fois où il est vu AVANT d'écrire.

---

## ÉCARTS ASSUMÉS

- **`bc007`, « -1 ATK AND -1 SCH »** : les deux sont écrits, mais une
  activation est **soit** une attaque **soit** une manigance — le moteur
  n'expose que l'une des deux à la fois (`would_message` est un
  `WhenUnitWouldAttack` **ou** un `WhenUnitWouldScheme`). On applique celui qui
  existe. Ce n'est pas un écart de fidélité : les deux moitiés de la phrase ne
  peuvent pas tomber ensemble.
- **`bc001a` compte AVANT de défausser, `bc001b`/`bc005`/`bc007` aussi.**
  `CountBoostIconsInternal` (`has_boost_icon.py:33`) court-circuite tout et rend
  `printed_boost` tant que la carte est dans une zone `is_place_card_area` ;
  une fois défaussée, elle repasse par le chemin normal, qui envoie un message
  et peut donner autre chose. `15001a` Scarlet Witch, la carte modèle,
  défausse d'abord — mais **sa** carte vient du deck, pas de la pile.
  Là où `DiscardEncounterTopCard` ne laisse pas le choix (`bc006`, `bc011`),
  on compte après, et cela ouvre la porte à Tychokinesis : combinaison voulue,
  écrite dans les modules pour qu'on ne « corrige » pas l'ordre.
- **`Rand.RandomChoice` est DÉTERMINISTE sous `disable_shuffle`** : il rend le
  PREMIER de la liste. Le cas de `bc012` en profite, mais il ne prouve donc pas
  le caractère aléatoire, seulement que la bonne zone est lue.
- **`bc010`, « ✱✱ resources instead for an attachment »** : on ne JOUE pas un
  attachement, c'est une carte de rencontre. « Payer pour un attachement »
  désigne le coût imprimé **sur lui** — 132 attachements du dépôt portent
  « Hero Action: Spend X resources → discard this card ». C'est la lecture
  retenue, et elle rend la carte cohérente avec sa propre Response. Aucune
  autre lecture ne donne un sens à la parenthèse.
- **`bc004` / `bc010`, la sélection par le TEXTE** : `face.paper.text` est lu
  et on y cherche la sous-chaîne « Hero Action » / « Hero Response ». Aucune
  primitive moteur. Conséquence : un attachement dont le texte serait traduit
  ou reformulé ne serait plus vu. Le champ `text` de `cards.json` est en
  anglais pour tout le dépôt, la lecture est donc stable — mais c'est une
  dépendance à une chaîne, et elle est écrite ici.

---

## CE QUE CES BLOCS NE PEUVENT PAS VOIR

⚠ **Aucune partie n'a été jouée par un humain dans le navigateur.**

**Autoplay : 8 parties contre Rhino, profil équilibré, avec `spider_man` comme
témoin dans la même fournée.**

| Deck | rounds | %V | bloquées |
|---|---|---|---|
| `black_cat` | 7.5 | 0 % | **0** |
| `spider_man` (témoin) | 5.6 | 0 % | 1 |

**Grep exhaustif des journaux : 0 traceback.** Black Cat tient 7,5 rounds
contre 5,6 au témoin officiel, et ne se coince jamais.

**Ce que l'autoplay a réellement exercé** (comptage des actes, pas une simple
apparition dans un journal) :

| Carte | déclenchements |
|---|---|
| `bc001a` Tychokinesis | **32** |
| `bc001b` Cat Burglary | 28 |
| `bc008` * Black Cat's Claws | 22 activations |
| `bc003` / `bc002` * Spider-Man | 19 |
| `bc007` Misfortune | 9 |
| `bc010` Ill Gotten Gains | 10 Responses (250 **avant** le correctif du §5) |
| `bc006` Lucky Hit | 4, dont 4 « Tuck one of those cards » |
| `bc011` Nine Lives | 4 |
| `bc012` Luck's Ran Out | 4 révélations |
| `bc005` Cat Burglary | 3 |
| `bc009` Grappling Hook | 2 |
| `bc004` * Big Heist | **jouée 1 fois, jamais vaincue** |

**Aucune carte n'est restée totalement inerte** — c'est la première fois sur
les trois packs de la journée. En revanche `bc004` Big Heist n'a **jamais été
vaincue** en huit parties : ses 4 menaces, que seule l'héroïne peut retirer à
CTR 2, demandent deux tours entiers, et le pilote ne fait pas ce
raisonnement-là. Ses trois branches « When Defeated » restent donc prouvées par
leurs cas de test et par la substitution, **pas par une partie**.

---

## Gabarits, carte par carte

### bc001a : * Black Cat (face héros)
- [x] Étape 2 : `15001a` * Scarlet Witch, « Chaos Control » — MOT POUR MOT le
      même montage (`WhenBoostIconsWouldBeCount`, `SetBeInstead`,
      `SetBoostIcon`), seule la provenance de la carte change ; `48021`
      * Gambit pour la lecture des icônes d'une carte glissée.
- [x] Étape 5 : « count the icons **([star] and [boost])** » →
      `IconesEtEtoiles`. « on an **encounter card** » → une carte joueur
      distribuée en bonus ne déclenche pas. « count … **instead** » → le mot
      « instead » du moteur. « a card tucked here » → **la joueuse choisit**.
      ⚠ **Aucune limite imprimée** — ni « once per phase » comme `15001a`, ni
      « once per round » : on n'en ajoute pas.
- [x] Étape 6 : **PV 9, CTR 2, ATQ 1, DEF 2, main 5.** ATQ 1 est la plus faible
      du dépôt pour un héros : Black Cat ne frappe pas, elle transforme des
      icônes.
- [x] Étape 7 : 3 cas, **rouges 2/3** — le vert est la LIGNE DE BASE (pile
      vide, la carte de bonus compte pour elle-même), qui mesure une absence.
- [x] Étape 7 bis : limite imprimée **NON**. La règle des 3 cartes a son cas
      dédié, partagé avec `bc001b`.

**Carte terminée : OUI**

### bc001b : * Felicia Hardy (face alter-ego)
- [x] Étape 2 : `48021` * Gambit (`LookAtDeck` + `AskChooseFace` +
      `TuckCardUnderHere`), à une carte près.
- [x] Étape 5 : ⚠ « **LOOK AT** the top 2 » et non « discard » : la carte non
      choisie **reste** sur le deck, ce que `LookAtDeck` fait déjà.
      « tuck 1 **of them** » → une des deux vues. ⚠ **Aucun plafond ici** : la
      carte entre toujours.
- [x] Étape 6 : PV 9, REC 3, main 6. Limite une fois par ROUND.
- [x] Étape 7 : 3 cas, **rouges 2/3** — le vert est le témoin d'épuisement, qui
      mesure une ABSENCE.
- [x] Étape 7 bis : limite imprimée **OUI**. Témoin : deux Actions dans le même
      round, la seconde par `declencher_tolerant`. Chiffre :
      `taille_pose_sous: 1`.

**Carte terminée : OUI**

### bc002 : * Spider-Man (version SYMBIOTE) — **OUI**
(2 cas, rouge 1/2 ; le vert est le contre-cas « sans icône, aucun bonus ».
⚠ Voir « ce que les gates ont trouvé » §4 : **aucun dégât consécutif imprimé**,
d'où `GainForThisActive` et non `IncreaseDamage`. ⚠ « each **boost icon**
([boost]) » sans l'étoile : `IconesSeules`. ⚠ « to **that** power » →
`message.GainValue`, qui aiguille seul vers le bon des quatre.)

### bc003 : * Spider-Man (version AVENGER, Multiverse) — **OUI**
(2 cas, rouges 2/2 ; l'annulation est prouvée par TROIS chiffres à la fois —
0 dégât, 1 pion toile sur 2, pile retombée à 0 — donc les deux coûts sont bien
payés. ⚠ `CostFunc.Counter` sait se rendre indisponible seule
(`has_enough_counter`, cost_func.py:802) ; `CostFunc.Custom` **non**, d'où
`PileNonVide`. ⚠ « When **an enemy** activates » : pas de filtre ELITE,
contrairement à `av002` dont on copie le montage.)

### bc004 : * Big Heist — **OUI**
(5 cas, rouges 4/5 ; le vert est le contre-cas « un allié non-VOLEUR ne retire
rien », qui mesure une absence. ⚠ Voir §2 et §6 de « ce que les gates ont
trouvé ». ⚠ `by_character=CardFinder(non_trait="THIEF")` : le filtre est la
**négation**. ⚠ La carte trouvée en collection doit passer par la **MAIN**,
une carte en défausse n'étant pas jouable — piège payé par `dz031`.)

### bc005 : Cat Burglary — **OUI**
(1 cas, rouge 1/1 ; « 1 threat **plus** 1 additional » — 1 est un plancher.
⚠ **Pas de flèche** : rien n'est un coût, la carte reste jouable deck de
rencontre vide. ⚠ « discard 1 » puis « **tuck it** » désigne la MÊME carte,
mot-piège `wd022`.)

### bc006 : Lucky Hit — **OUI**
(1 cas, rouge 1/1 ; « for each icon **discarded this way** » — le total des
DEUX cartes. ⚠ « Tuck **one of** those cards » : une seule, et la pile vaut
donc 1.)

### bc007 : Misfortune — **OUI**
(2 cas, rouge 1/2 ; le vert est la LIGNE DE BASE — sans la carte, l'icône de
bonus **s'ajoute** à l'ATQ et l'identité prend 3 au lieu de 1. C'est l'écart
entre 3 et 1 qui mesure la carte. ⚠ **Carte à boucle infinie si on la code de
travers** : `ResolveBoostCards` fait `continue` sur `is_be_instead` sans
retirer la carte du paquet — piège identique à `sn004`, payé la veille.)

### bc008 : * Black Cat's Claws — **OUI**
(2 cas, rouges 2/2 ; le second est la branche « If that number was 0, tuck it »,
atteignable **uniquement** avec une carte sans icône chiffrée. ⚠ C'est ici que
l'écart de comptage avec le reste du set devient OBSERVABLE, voir plus haut.)

### bc009 : Grappling Hook — **OUI**
(2 cas, rouge 1/2 ; le vert est le contre-cas pile vide. ⚠ Le coût se paie sur
la MÊME pile que l'effet remplit : le cas prouve que la pile reste à 1 mais a
**changé de contenu**. Modèle `sn005` Web Swinging.)

### bc010 : Ill Gotten Gains — **OUI**
(3 cas, rouges 2/3 ; le vert est le contre-cas « un attachement SANS Hero
Action n'est pas ramassé », qui prouve le filtre par texte. ⚠ Voir §5 de
« ce que les gates ont trouvé » : la carte était **injouable** avant que
l'autoplay ne le montre. ⚠ **Aucun `for_card`** : le texte ne restreint pas ce
que la carte peut payer, il donne seulement DEUX ressources pour un
attachement — même arbitrage que `tg008`.)

### bc011 : Nine Lives — **OUI**
(2 cas, rouges 2/2 ; le second prouve que sans icône **rien n'est prévenu** et
que l'inclinaison est quand même perdue — c'est le pari imprimé.
⚠ L'attaquant des deux cas est un **SBIRE** : un sbire ne reçoit aucune carte
de bonus, le dessus du deck truqué reste donc celui que le coût défausse. Avec
le vilain, la carte aurait été consommée comme carte de bonus **avant**
d'arriver au coût — piège trouvé à l'écriture.)

### bc012 : Luck's Ran Out — **OUI**
(2 cas, rouges 2/2 ; ⚠ « **REVEAL** a random card » et non « discard » : la
carte est RÉSOLUE comme une carte de rencontre, ce que le cas mesure par la
menace posée par `01186` Advance. Le contre-cas prouve que la branche « if you
cannot → surge » est ATTEIGNABLE, mot-piège `wd028`.)

**13 cartes terminées sur 13.**
