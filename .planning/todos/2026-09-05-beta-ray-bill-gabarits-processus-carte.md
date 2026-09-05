# PROCESSUS-CARTE.md — les 13 gabarits du pack BETA RAY BILL (set 158, `br`)

Gate de `PROCESSUS-HEROS.md` : un gabarit rempli par carte. Rédigés le
05/09/2026. Auteur du pack : **Rainy**, zip « Beta Ray Bill ».

**Preuves communes**, citées une fois :

- **Étape 7, cas** : `test_capacites.py … /tmp/rapport.json br0` → **16/16**.
- **Étape 7, substitution** : `substituer_pack.py .game-src 61600 br0` →
  **13/13 cartes** tombent au rouge sans leur module.
- **Étape 1** : pack `beta_ray_bill` en queue de `cards.json`, set
  `158. Custom (Beta Ray Bill)`, préfixe `br` déclaré, `verifier_prefixes` OK.
- **Étape 4, image** : `assets/pics/br0*` pour les 13, découpées du zip.
- `test_cards` : **5255 ok / 0 erreur**.
- `verifier_appels_modules` : « tous les appels de beta_ray_bill existent ».
- `verifier_cartes_en_jeu` : « les 13 cartes portent ce que leur texte
  annonce ».
- **Étape 3** : `deck/starter/beta_ray_bill.json`, et le deck **monte une
  partie** (`identite br001a, main 5, deck 35`).
- **Batterie complète** (les énums TRAITS et COUNTER, la liste blanche de
  `factory.py` et le harnais lui-même sont touchés) : **1293/1297**, les 4
  rouges étant les 4 rouges antérieurs de `squirrel_girl`, mot pour mot
  identiques avant et après.
- **Étape 8, autoplay** : 16 parties (Rhino, Klaw), **0 erreur** au grep
  exhaustif et **0 partie bloquée**. Témoin `texas_twister` dans la même
  fournée : mêmes chiffres (0 % de victoire, 3.5 / 5.1 rounds contre
  4.5 / 4.1) et 0 partie bloquée elle aussi.
  Lecture ligne à ligne : Stormbreaker est cité 17 à 23 fois par partie, et
  la boucle rappel → mise en jeu → trait AERIAL se voit en clair.
- **Étape 10** : contrôle sur les **121 decks de départ** → **0 écart**.
  `verifier_tous_les_decks` : **120/121**, le seul échec (`sp_dr`) étant
  antérieur.
- **Étape 7 (héros)** : biographie dans `heros-info.js`.
- **Étape 8 (héros)** : les 13 textes français dans `textes-fr-fanmade.ts`.

---

## CE QUE LE PACK N'A PAS, ET CE QU'ON A MIS À LA PLACE

**Aucun set némésis.** Le zip s'arrête à l'obligation `br012` Unworthy.
C'est le **troisième pack de Rainy** dans ce cas, et le dépôt avait déjà
tranché deux fois :

- `hulk_rainy` : « AUCUN set nemesis dans le zip : le deck **emprunte celui du
  Hulk officiel** (10026-10028) » ;
- `viv_vision` : « AUCUNE carte nemesis dans le zip : `nemesis_set` prend le
  **modulaire officiel Zzzax**, que l'auteur recommande ».

Le deck emprunte donc celui de **Thor** (`06027`-`06030` : Family Feud, Loki,
deux Frost Giants, Trickster), calque exact de ce qui a été fait pour
hulk_rainy. C'est thématiquement juste — Bill est le frère d'armes de Thor, et
`br011` Hammer Time est littéralement une Team-Up avec lui — et ce n'est
jouable que depuis le correctif moteur du 02/09/2026, sans lequel `01190`
Shadow of the Past ne trouvait aucun sbire némésis.

**Aucune décklist.** Pas de dossier `Extras`. L'aspect retenu est
**Agressivité** : tout le kit cherche des sbires (`br005` en convoque un,
`br011` en pose un pour le frapper à 10, `br009` déclenche sur leur arrivée,
`br006` frappe ceux qui sont engagés).

---

## LA MÉCANIQUE : UNE SEULE AMÉLIORATION

`br010` **Stormbreaker** est unique, Restreinte, coûte 1, et **sept des treize
cartes la citent nommément** :

| Carte | Ce qu'elle fait du marteau |
|---|---|
| `br001a` Worthy | le **rappelle en main**, et frappe pour 3 s'il était en jeu |
| `br003` Hammer Throw | l'**incline**, frappe pour 6, puis le rappelle |
| `br004` Hammer Twirl | l'**incline** pour prévenir, et frappe s'il a **payé** |
| `br002` Eye of the Storm | ignore la crise s'il a **payé** |
| `br008` Calm Before the Storm | change de bonus selon qu'il est **en jeu** |
| `br010` lui-même | se **défausse** pour payer un événement |
| `br012` Unworthy | le **confisque** sous elle |

Le marteau fait l'aller-retour main ↔ jeu en permanence : c'est le moteur
économique du héros.

---

## CE QUE LES GATES ONT TROUVÉ

### 1. Un événement Team-Up qui fait tomber le SETUP du deck

`database.py:223` pose `assert selectors[0].target_text == "TeamUp"` dès qu'un
événement porte `TeamUp` dans son `desc`. Sans `.SetTarget("TeamUp")`,
`br011` Hammer Time faisait échouer **le setup du deck** —
`AssertionError: origin_card_id='br011'` — et ni `test_cards`, ni
`test_capacites`, ni `substituer_pack` ne le voient. C'est exactement la leçon
`ls005`, qui avait laissé le deck lady_sif injouable une journée entière ; ici
elle a coûté une minute, parce que `verifier_tous_les_decks` a été lancé
**juste après l'écriture du deck**.

### 2. Le harnais sous-payait tout coût mixte, d'une icône

`Requirement ([energy])` combiné à un coût chiffré se rend `"Y2"` côté moteur :
une énergie **plus** deux ressources, donc trois. Le harnais calculait
`len("Y2") = 2`. Le pilote s'arrêtait à deux icônes, le moteur refusait le
paiement, et la carte tombait « injouable » sans le moindre message :
`br006` Thunderstrike n'était pas testable. Corrigé dans `payer()` — on somme
les chiffres et on compte les lettres, `len()` restant juste pour les coûts
purement colorés (« RB », « YY »).

C'est une **correction du harnais**, pas du pack : elle vaut pour les cinq
cartes à `Requirement` déjà présentes dans le dépôt.

### 3. Quatre API inventées, dont une que `test_cards` ne voit pas

| Écrit | Réalité | Symptôme |
|---|---|---|
| `SetTarget("EachPlayerIdentity")` | `"VillainAndEngagedSamePlayerMinion"` | **rien** — `test_cards` construit la carte sans broncher, la chaîne n'étant validée qu'à la sélection |
| `CanGenerateResources(for_card_type=Event)` | `for_card=CardFinder(card_type=Event)` | `test_cards` rouge |
| `AbilityFactory.ThisNotReadyInReadyStep()` | `CardCannotReady` + condition sur la règle `EndPhase` | `test_cards` rouge |
| `OnEvent.Exhaust("This")` | n'existe pas — `condition=` seul, réévalué à chaque lecture | `test_cards` rouge |

Le premier est le plus instructif : `SetTarget` prend une chaîne libre, et
seul le fait d'être allé **compter les usages du littéral dans le dépôt** l'a
sorti. Il n'apparaissait qu'une fois — dans mon propre code.

### 4. « does not ready at the end of the player phase » n'a pas de modèle

Aucune carte du dépôt ne porte ce texte. Le moteur redresse tout par
`Faces.ReadyAll(faces, EndPhase(player))` (`player_phase.py:100`) : on bloque
donc le redressement **uniquement** quand l'effet qui redresse est cette
règle-là. Un `CardCannotReady` sans condition interdirait aussi `br005` Star
Jump, qui existe précisément pour redresser le vaisseau, et Skuttlebutt serait
mort au premier usage.

### 5. Trois pièges de cas déjà connus, repayés

- **`Puzzle.Damage` n'est pas « vous ».** `br012` dit « After **you** defeat an
  enemy » : une `DebugRule` n'est pas le joueur, la Réponse forcée ne partait
  pas. Et `Puzzle.Damage('01101', 2)` posée en mise en place ne touchait même
  pas le sbire en jeu — `FindOrCreateFace` avait créé un **second objet du même
  card_id**, exactement le piège du cas `tt001b` (pack texas_twister).
- **Le pilote paie le minimum d'un coût X**, c'est-à-dire **zéro** : le moteur
  annonce `cost: 0` pour un `desc.Cost` valant « X ». `br002` et `br005`
  « activaient » sans rien faire, journal muet. La clé `surpayer` est
  obligatoire sur toute carte à coût X.
- ⚠ **`GetCostX` compte les CARTES dépensées, pas les icônes** : une seule
  carte-ressource donne X = 1, même quand elle porte deux icônes (`01090`
  Strength, « RR »). Mesuré, pas supposé.

---

## ÉCARTS ASSUMÉS

- **`br002` Eye of the Storm** : « Spend X **[energy]** resources ».
  `desc.Cost` ne connaît que `"X"` (16 cartes du dépôt) et `"R"` (une seule,
  `10002` Crushing Blow), mais **pas de X typé** : aucune carte du jeu ne
  combine les deux. Le joueur paie donc X ressources de n'importe quel type.
  L'écart est en sa faveur.
- **`br007` Skuttlebutt** : « While Skuttlebutt is ready, you get +1 hand
  size » repose sur `condition=` seul, aucun `OnEvent` ne couvrant l'état
  prêt/incliné. La valeur est réévaluée à chaque lecture, ce que le cas
  vérifie ; seul l'affichage pourrait retarder.

---

## HOMONYMES ET NOMS

- ⚠ **Les deux faces portent le même nom**, « * Beta Ray Bill » : il n'a pas
  d'identité civile. Partout où la forme compte, le filtre est le **type**
  (`Hero` / `AlterEgo`), jamais le nom. Et le zip numérote **`0.1` l'alter-ego
  et `0.2` le héros**, dans cet ordre inverse — vérifié sur les libellés
  imprimés, pas sur les noms de fichiers.
- ⚠ **`br003` Hammer Throw est l'homonyme exact de `06005`**, la Hammer Throw
  officielle de Thor (8 dégâts là-bas, 6 ici). Troisième homonymie du dépôt
  après « Hulk Smash » et « Limitless Strength » (pack hulk_rainy).

---

## Gabarits, carte par carte

### br001a : * Beta Ray Bill (face héros)
- [x] Étape 2 : `04001b` Clint Barton, `bk008` (`Search.PlayerCard` rend **une
      face ou None**).
- [x] Étape 5 : « **find** » couvre deck, défausse **et terrain** ; « if it
      **leaves play** this way » restreint les 3 dégâts au rappel depuis le jeu.
- [x] Étape 6 : PV 14, CTR 1, ATQ 2, DEF 2, main 4. Limite une fois par round.
- [x] Étape 7 : 2 cas, rouges 2/2 (dont le contre-témoin « depuis le deck »).

**Carte terminée : OUI**

### br001b : * Beta Ray Bill (face alter-ego)
- [x] Étape 5 : « a **copy of** Star Jump » — n'importe lequel des deux.
- [x] Étape 6 : PV 14, REC 3, main 5.
- [x] Étape 7 : 1 cas, rouge 1/1.

**Carte terminée : OUI**

### br002 : Eye of the Storm — **OUI** (1 cas, rouge 1/1 ; coût X + `surpayer`, écart sur le type de ressource)
### br003 : Hammer Throw — **OUI** (1 cas, rouge 1/1 ; copie de `06005`, son homonyme officiel)
### br004 : Hammer Twirl — **OUI** (1 cas, rouge 1/1 ; ⚠ **deux capacités `Play`**, déclarée dans la liste blanche de `factory.py` AVANT d'écrire le module)
### br005 : Star Jump — **OUI** (1 cas, rouge 1/1 ; « choose X of the following », et la seule carte qui redresse Skuttlebutt)
### br006 : Thunderstrike — **OUI** (1 cas, rouge 1/1 ; le littéral `VillainAndEngagedSamePlayerMinion`, et le correctif de paiement du harnais)
### br007 : * Skuttlebutt — **OUI** (2 cas, rouges 2/2 ; « does not ready », sans modèle dans le dépôt)
### br008 : Calm Before the Storm — **OUI** (2 cas, rouges 2/2 ; deux bonus exclusifs, chacun contre-témoin de l'autre)
### br009 : Oathbrother — **OUI** (1 cas, rouge 1/1 ; « seek an event **from your deck** », le deck seul)
### br010 : * Stormbreaker — **OUI** (1 cas, rouge 1/1 ; la carte autour de laquelle tout le pack tourne)
### br011 : Hammer Time — **OUI** (1 cas, rouge 1/1 ; `.SetTarget("TeamUp")` obligatoire, sans quoi le deck ne monte pas)
### br012 : Unworthy — **OUI** (1 cas, rouge 1/1. ⚠ bandeau BETA RAY BILL : module dans `beta_ray_bill/`, piège `bt019` payé une **7ᵉ** fois)

**13 cartes terminées sur 13.**
