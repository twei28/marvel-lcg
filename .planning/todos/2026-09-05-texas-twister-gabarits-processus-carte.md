# PROCESSUS-CARTE.md — les 25 gabarits du pack TEXAS TWISTER (set 157, `tt`)

Gate de `PROCESSUS-HEROS.md` : un gabarit rempli par carte. Rédigés le
05/09/2026. Auteur du pack : **Kajislav**, zip « Texas Twister (Released) ».

**Preuves communes**, citées une fois :

- **Étape 7, cas** : `test_capacites.py … /tmp/rapport.json tt0` → **34/34**.
- **Étape 7, substitution** : `substituer_pack.py .game-src 53100 tt0` →
  **25/25 cartes** tombent au rouge sans leur module.
- **Étape 1** : pack `texas_twister` en queue de `cards.json`, set
  `157. Custom (Texas Twister)`, préfixe `tt` déclaré, `verifier_prefixes` OK.
- **Étape 4, image** : `assets/pics/tt0*` pour les 25, découpées du zip.
- `test_cards` : **5242 ok / 0 erreur**.
- `verifier_appels_modules` : « tous les appels de texas_twister existent »
  — avec l'outil **réparé** la veille (il ne lisait aucun sous-dossier de pack
  avant le 04/09/2026).
- `verifier_cartes_en_jeu` : « les 25 cartes portent ce que leur texte
  annonce ».
- **Étape 3** : `deck/starter/texas_twister.json`, conforme au scan
  « starter deck texas twister » carte pour carte (15 signature, 25 aspect
  Meneur, 5 némésis, 1 obligation), et `verifier_tous_les_decks` au vert.
- **Batterie complète** (les énums TRAITS *et* COUNTER sont touchées) :
  **1277/1281**, les 4 rouges étant les 4 rouges antérieurs de
  `squirrel_girl`, mot pour mot identiques avant et après.
- **Étape 8, autoplay** : 16 parties (Rhino, Klaw), **0 erreur** au grep
  exhaustif et **0 partie bloquée**. Témoin `blink` dans la même fournée :
  mêmes chiffres (0 % de victoire, 4.1 / 4.8 rounds contre 3.5 / 5.1) et **une**
  partie bloquée, donc Texas Twister est au moins aussi propre que le témoin.
  Lecture ligne à ligne : Vortex Control s'applique dans les 16 parties, et
  Keep Spinning redresse bien le héros après un pouvoir de base.
- **Étape 10** : contrôle sur les **120 decks de départ** → **0 écart** (aucune
  carte signature étrangère). `verifier_tous_les_decks` : **119/120**, le seul
  échec (`sp_dr`) étant antérieur.
- **Étape 7 (héros)** : biographie dans `heros-info.js`.
- **Étape 8 (héros)** : les 25 textes français dans `textes-fr-fanmade.ts`.

⚠ **LE PRÉFIXE `tt` ÉTAIT LIBRE**, malgré le dossier `src/cards/pack/tt/` : ce
dossier est le pack **officiel Thor**, dont les cartes portent des `card_id`
numériques. Le registre des préfixes ne connaît que les préfixes de `card_id`,
et il a validé `tt` sans réserve.

---

## LA MÉCANIQUE : UNE SEULE PHRASE, QUATRE CARTES

« After you use one of Texas Twister's basic powers *(THW, ATK, or DEF)* »
revient sur **quatre** cartes : l'identité héros (`tt001a`, +1 à **ce**
pouvoir jusqu'à la fin du round, **sans limite**), les **cinq** Keep Spinning
(`tt004`, le redresser), Cyclonic Suction (`tt007`, piocher) et Twist Again
(`tt019`, redresser le héros **et** Shooting Star). Chaque usage rend le
suivant meilleur.

Et le set némésis vise exactement ça : l'obligation `tt020` interdit de
redresser l'identité par un effet de carte joueur, et Master Pandemonium taxe
chaque activation.

Le moteur avait déjà la fabrique : `AbilityFactory.AfterUnitUseBasicPower`
(`friend.py:373`), avec `powers=["ATK", "THW", "DEF"]` et `message.power`.
Modèles : `14001a` Quicksilver, `04032` Captain Marvel, `28001a` Nova.

---

## CE QUE LES GATES ONT TROUVÉ

### 1. Moxie faussait **toutes** les mesures d'attribut — deuxième fois

Le deck contient trois `12016` Moxie, que le pilote joue systématiquement en
Réponse au passage en forme héros : **+1 ATQ, +1 CTR et +1 DEF** pour tout le
round. Les cinq cas qui mesurent un attribut lisaient donc un point de trop
partout.

La leçon avait déjà été payée sur `doctor_druid` (04/09/2026), où elle avait
rendu **trois cas verts par accident**. Ici elle a été payée en rouge, ce qui
est déjà mieux — mais elle sera repayée tant que le remède n'est pas dans le
processus. **Le remède** : `main_exclusive` ne vide la main qu'**après**
`mise_en_place`, donc le changement de forme doit vivre dans `declencher`, pas
avant. Les cinq cas concernés le disent en tête.

### 2. `Puzzle.Thwart` ne fait **rien** sans menace sur le complot

Deux cas mesuraient « l'allié ne prend aucun dégât conséquent » et passaient
au vert… parce que le contre n'avait jamais eu lieu. Sans menace, il n'y a pas
de cible légale, `MakeBasicPowerLikeInTurn` ne fait rien, et zéro dégât veut
dire « rien ne s'est passé ».

**Le remède, désormais dans les quatre cas concernés** :
`Puzzle.SetThreat('01097b', 5)` en mise en place, et un **témoin de menace**
dans `attendu` (5 → 4 pour un CTR 1, 5 → 3 pour un CTR 2). Le modèle existait
déjà — `aa019` Wiccan le fait depuis le pack agatha_harkness.

### 3. `dans_deck_joueur` lit un deck **lié à sa défausse**

`player_deck.GetAll()` renvoie aussi les cartes de la défausse
(`BindDiscardPile`, `player.py:73`). Le cas de `tt001b` — « remélangez 2
cartes SUPERPOWER de votre défausse dans votre deck » — passait donc au vert
**sans le module**. Sorti par la substitution, et par elle seule. Remplacé par
une vérification outillée qui mesure le **départ** de la défausse.

### 4. Le pilote prend le **minimum** d'un « up to N »

`range=(0, 2)` : le pilote choisit **zéro** carte, la capacité « active » sans
rien faire, et le journal ne montre qu'un `Drew Daniels activates`
parfaitement muet. Il faut `cibles`, **et** `choisir_option` : le repli
générique n'honore `cibles` que pour **une** cible, seule la branche
`choisir_option` applique `forcees[:maxi]`.

### 5. Deux objets, un seul `card_id`

Première version du cas `tt001b` : deux `tt003`/`tt004` posés en défausse,
alors que le deck en contient déjà. Le pilote a remélangé l'exemplaire **de la
main de départ**, et le contrôle par `card_id` voyait toujours « tt004 en
défausse ». Le journal, lui, montrait bien deux cartes remélangées. Les cartes
du cas sont donc désormais **étrangères au deck** (`bk005`, `bk006`).

### 6. Une attaque fait **déclarer une défense**, qui incline l'identité

Le cas de `tt021` mesurait « l'identité est inclinée » après
`Puzzle.Attack('tt021')`. Elle l'était — par la **défense** déclarée par le
pilote, pas par la carte. Substitution : vert sans le module.
`Puzzle.Scheme` est l'activation propre, sans défense, et le cas
discriminant est désormais celui de la branche « dépenser une énergie », qui
vide la main **et** laisse l'identité prête.

### 7. Cinq API invalides, cinq symptômes différents

| Écrit | Réalité | Symptôme |
|---|---|---|
| `AbilityFactory.CanAttachToCard` | `AttachToFaceWhenPutIntoPlay` | `test_cards` rouge |
| `UnitCannotTakeDamage("Attached")` | un `CardFinder` nommé | `assert not isinstance(check_rule, Sequence)` à **chaque** dégât, avalé |
| `SetTarget(..., control_by=)` | `check_fn=` | `TypeError`, avalé |
| `CardFinder(name=[a, b])` | `names=[a, b]` | filtre qui ne matche jamais, **muet** |
| `ForChoiceAbility(...).SetCost(...)` | `ForChoiceAbilityWithCost(cost, nom)` | assert explicite du moteur |

### 8. Deux montages que seul le journal explique

- **`tt013` Fifty-One** : « After Fifty-One is defeated… » imprimé **sur**
  Fifty-One. Au moment où la Réponse résout, il est dans la défausse, et le
  contrôle de zone générique la refuse. Il faut `NoOutOfPlayLimit()`
  (idiome `aa002`, `dz014`, `09032`). Le journal montrait `was defeated` puis
  plus rien.
- **`tt024` Soul Fragmentation** : `CostFunc.DiscardDeckTopCards` en **coût**
  d'un `WhenThisRevealed`. Une carte de rencontre n'a pas de joueur qui paie :
  le coût n'est jamais réglé, l'opération n'est jamais appelée, et le journal
  ne montre qu'un banal « was revealed / were discarded ». Défausse à la main,
  dans l'opération.

---

## ÉCARTS ASSUMÉS

- **`tt011` Whirling Debris** : « Hero Interrupt: When you make a basic
  attack, … damage from this attack may be divided among enemies ». Impossible
  en l'état : quand l'interruption part, la cible unique de l'attaque est
  choisie depuis longtemps. Le moteur ne sait répartir que si les cibles
  multiples sont choisies **à la sélection**, ce que fait
  `ThisCanAttack(canbe_divided=True)` (`cd002a` Dagger, `13001c` Wasp) — qui
  **remplace** la définition du pouvoir ATQ et ne peut donc pas s'allumer en
  cours de route. Rendue en **Hero Action** qui incline Whirling Debris **et**
  l'identité : c'est exactement ce que coûte une attaque de base plus la
  carte. Valeur de jeu identique, forme différente.
- **`tt016` Lone Star Rangers** et **`tt019` Twist Again** : imprimées
  « Hero **Action** » suivi d'un déclencheur « After … ». Les deux sont
  incompatibles — une Action se joue quand on veut, une capacité « After » est
  une **Réponse**. Le sous-type retenu est `HeroResponse` ; écrire `HeroAction`
  rendrait la carte jouable à n'importe quel moment sans vérifier le
  déclencheur.
- **`tt017` Phantom Rider** : texte imprimé fautif (« ingores »), et deux
  effets collés sans conjonction. Lecture retenue : il ignore
  Garde/Patrouille/Crise **et** subit 1 dégât conséquent de moins. L'autre
  lecture (la réduction ne vaut que lors des usages où il ignore quelque
  chose) est inapplicable — le moteur ne signale pas « une exemption a servi ».
- **`tt014` Firebird** : « discard the top card » n'est pas un coût sur la
  carte, mais le moteur n'a qu'un montage pour « défausser puis compter ce qui
  est sorti », et c'est le coût. Conséquence : l'interruption ne part pas si
  deck **et** défausse sont vides, là où le texte la ferait partir sans effet.

**Deux cas restent volontairement verts en substitution** : ce sont des
**contre-témoins** (`tt008` « un contre de base ne la défausse PAS »,
`tt014` « sans énergie, elle prend son dégât »). Un contre-témoin mesure une
**absence** : il ne peut pas tomber quand le module disparaît. Chacune des deux
cartes a par ailleurs un cas qui rougit.

---

## QUESTIONS OUVERTES CHEZ L'AUTEUR

1. **Phantom Rider** : le texte est fautif et ambigu (voir ci-dessus).
2. **Lone Star Rangers / Twist Again** : « Hero Action » ou « Hero Response » ?
3. **Décklist** : deux noms n'existent pas — « Civil Duty » est **Civic Duty**
   (`14023`), « The Power of All of Us » est **The Power in All of Us**
   (`13024`). Tranchés sur les cartes officielles.
4. Les **8 cartes d'aspect** du zip ne figurent pas dans la décklist du
   starter : volontaire ?

---

## Gabarits, carte par carte

Les blocs « étape 2 » et « étape 5 » sont en tête de chaque module.

### tt001a : * Texas Twister (face héros)
- [x] Étape 2 : `14001a` Quicksilver, `28001a` Nova, `12016` Moxie.
- [x] Étape 5 : « +1 to **that** power » — lu sur `message.power`, jamais
      deviné. **Aucune limite imprimée**, contrairement à Quicksilver : les
      bonus empilent, et c'est le moteur du pack.
- [x] Étape 6 : PV 10, ATQ 1, CTR 1, DEF 1, main 5. Traits AERIAL, RANGER.
- [x] Étape 7 : 2 cas, rouges 2/2 (dont un témoin d'empilement).

**Carte terminée : OUI**

### tt001b : * Drew Daniels (face alter-ego)
- [x] Étape 5 : « up to 2 » = `range=(0, 2)` ; filtre par **trait**
      SUPERPOWER ; destination **deck**, contraste imprimé avec tt005.
- [x] Étape 6 : PV 10, REC 3, main 6.
- [x] Étape 7 : 1 cas, rouge 1/1, par vérification outillée.

**Carte terminée : OUI**

### tt002 : * Shooting Star — **OUI** (1 cas, rouge 1/1 ; redresse l'IDENTITÉ, pas elle-même)
### tt003 : Accelerated Rotation — **OUI** (1 cas, rouge 1/1 ; les trois pouvoirs, contraste avec tt001a)
### tt004 : Keep Spinning — **OUI** (1 cas, rouge 1/1 ; ×5 dans le deck, la carte la plus jouée)
### tt005 : * Pine Ridge Reservation — **OUI** (1 cas, rouge 1/1 ; les deux moitiés, modèle `aa003`)
### tt006 : * Agent T — **OUI** (1 cas, rouge 1/1 ; ⚠ le trait s'écrit `S.H.I.E.L.D` **sans point final** côté moteur)
### tt007 : Cyclonic Suction — **OUI** (1 cas, rouge 1/1 ; non unique, deux exemplaires piochent deux fois)
### tt008 : Spin It to the Left! — **OUI** (3 cas, rouges 2/3 ; le vert est un contre-témoin)
### tt009 : Spin It to the Right! — **OUI** (2 cas, rouges 2/2 ; miroir exact, et l'exclusion mutuelle ROTATION)
### tt010 : * Texas Twister's Hat — **OUI** (2 cas, rouges 2/2 ; Solide mesuré par vérification outillée, `attendu.statuts` ne discrimine pas)
### tt011 : Whirling Debris — **OUI** (1 cas, rouge 1/1 ; écart assumé sur la répartition)
### tt012 : * Armadillo — **OUI** (1 cas, rouge 1/1 ; compteur maison `shell`, retrait en **coût**)
### tt013 : * Fifty-One — **OUI** (1 cas, rouge 1/1 ; `by_consequential=True` + `NoOutOfPlayLimit()`)
### tt014 : * Firebird — **OUI** (2 cas, rouges 1/2 ; le vert est le contre-témoin « sans énergie »)
### tt015 : * Living Lightning — **OUI** (1 cas, rouge 1/1 ; frappe **tout le monde**, allié voisin compris)
### tt016 : Lone Star Rangers — **OUI** (1 cas, rouge 1/1 ; « **character** », donc le héros aussi)
### tt017 : * Phantom Rider — **OUI** (1 cas, rouge 1/1 ; `UnitIgnoreKeywordIcons` avec le `which_unit` nommé, leçon `as012`)
### tt018 : * Red Wolf — **OUI** (1 cas, rouge 1/1 ; ⚠ `under_your_control=True`, et il déclenche sur sa propre entrée)
### tt019 : Twist Again — **OUI** (1 cas, rouge 1/1 ; `names=` et non `name=`)
### tt020 : Rodeo Extravaganza — **OUI** (2 cas, rouges 2/2. ⚠ bandeau TEXAS TWISTER : module dans `texas_twister/`, piège `bt019` payé une **6ᵉ** fois, vu avant d'écrire)
### tt021 : * Master Pandemonium — **OUI** (2 cas, rouges 2/2 ; `ForChoiceAbilityWithCost`)
### tt022 : Portal to Hell — **OUI** (1 cas, rouge 1/1 ; Hinder et Crisis sont des bases automatiques, rien à coder)
### tt023 : Demonic Limbs — **OUI** (2 cas, rouges 2/2 ; la clause de repli passe par `if_cannot_operation`)
### tt024 : Soul Fragmentation — **OUI** (1 cas, rouge 1/1 ; trois `if` indépendants, l'énergie n'est **pas** citée)

**25 cartes terminées sur 25.**
