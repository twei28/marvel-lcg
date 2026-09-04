# PROCESSUS-CARTE.md — les 19 gabarits du pack YONDU (set 154, `yd`)

Gate de `PROCESSUS-HEROS.md` : un gabarit rempli par carte. Rédigés les 03 et
04/09/2026. Auteurs du pack : **BLUEHG + DESIGNHACKER**, format « MC4 SEALED ».

⚠ **`yd007` Jackpot! n'est pas prouvée par un test** — mais le défaut est dans
l'**outillage**, pas dans la carte. Arbitrage de l'utilisateur du 04/09/2026 :
**gardée telle quelle**. Voir son gabarit. Le reste du pack est complet.

**Preuves communes**, citées une fois :

- **Étape 7, cas** : `test_capacites.py … /tmp/rapport.json yd0` → **34/34 cas
  verts**.
  ⚠ **Le filtre est `argv[4]`, pas `argv[3]`** (`argv[3]` est le chemin du
  rapport). Passer le préfixe en 3ᵉ position déroule **les 1203 cas** sans
  filtre : c'est ce qui a fait croire à une batterie qui « ne converge pas »,
  50 minutes durant, le 03/09.
- **Étape 7, substitution** : `substituer_pack.py .game-src 44000 yd0` →
  **18/19 cartes** tombent au rouge sans leur module. Quatre cas restent verts
  et c'est légitime — ce sont des **contre-témoins d'absence d'effet**
  (`yd008`, `yd010`, `yd012`, `yd016`), chacun jumelé à un cas nominal qui,
  lui, passe au rouge. La 19ᵉ, `yd007`, est un vrai trou : détaillé plus bas.
- **Étape 1** : pack `yondu` en queue de `cards.json`, set
  `154. Custom (Yondu)` dans `sets_info.json`, préfixe `yd` déclaré, checksums
  recalculés, `verifier_prefixes` OK.
- **Étape 4, image** : `assets/pics/yd0*` pour les 19, découpées du zip
  `YONDU (MC4 SEALED)-20260902T070718Z-1-001.zip` (24 scans distincts, les
  exemplaires multiples comparés au pixel sur leur zone de règles).
- `test_cards` : **5181 ok / 0 erreur**.
- `verifier_appels_modules` : « tous les appels de yondu existent ».
- `verifier_cartes_en_jeu` : « les 19 cartes de yondu portent ce que leur texte
  annonce ».
- `verifier_tous_les_decks` : **`yondu` monte une partie** (identité `yd001b`,
  main 6, deck 34).
- **Étape 10** : contrôle sur les **117 decks de départ** → **0 écart**.
- **Deck de départ** : le seul du dépôt à suivre **exactement la decklist de
  l'auteur** (18 Agressivité + 7 Basic).

**Un mot-clé maison**, `summon`, **employé six fois et jamais défini par
l'auteur**. Arbitrage de l'utilisateur (03/09/2026) : **deck ET défausse**,
sans quoi une Yaka Arrow défaussée serait perdue pour la partie et neuf cartes
du pack deviendraient mortes. Fiche : `docs/reference/mots-cles/summon.md`.

**Un compteur maison**, `wound`, ajouté à l'énum `COUNTER` du moteur.

---

## Les six vrais défauts trouvés, tous silencieux

Aucun n'a été signalé par un message d'erreur. Chacun a demandé de lire un
journal de partie.

### 1. `AfterCardDetachFrom` ne peut PAS servir depuis le héros

« attached to **or removed from** » demande deux fenêtres. L'arrivée tient dans
`AfterCardAttachTo`. Le départ, non : ce message a pour `trigger`
l'**amélioration** (`sender_card.py:204`), pas l'hôte, donc une capacité portée
par le héros ne l'entend jamais — et le moteur marque de toute façon la carte
comme retirée **avant** de l'émettre (`can_attach.py:99`). La moitié des dégâts
du héros manquait, en silence.

Parade reprise du pack `alligator_loki`, qui a buté sur le même manque : la
fenêtre est ouverte **à la main**, dans `QuitterLHote`, au seul point de
passage du pack.

### 2. `DealDamage` exige `self is by_effect.this`

`QuitterLHote` faisait frapper la flèche depuis l'effet d'une autre carte, d'où
`AssertionError: self=Yaka Arrow by_effect.this=Whistle While You Work` —
**avalée par le moteur**. La carte paraissait simplement inerte. La frappe part
désormais de `effect.this`.

### 3. Une obligation n'a pas de joueur au sens de `GetControlByOrOwner`

`yd013` Banished est une carte de **rencontre** donnée au joueur.
`JoueurDeCetteCarte`, qui part de `effect.this`, ne rend aucun joueur : la
Tahlei restait introuvable et la branche « défaussez la flèche **et inclinez la
Tahlei** » n'inclinait rien. `LaTahlei` accepte maintenant un joueur explicite,
celui que le message de l'obligation désigne.

### 4. Le rappel en main est un départ comme un autre

`yd011` et `yd012` appelaient `Faces.ReturnToHand` en direct, sautant la
morsure du départ. La branche « en main » était donc gratuite à tort. Elles
passent par `RappelerLaFlecheEnMain`.

### 5. `yd007` Jackpot! ne peut pas débloquer un coût FIXE

Le moteur valide le coût **avant** d'autoriser la mise en jeu ; la carte double
**après** avoir été dépensée. ⚠ Une première rédaction en concluait « quasi
inerte » : **c'était trop fort**, faute d'avoir testé autre chose qu'un coût
fixe. Le doublement agit pendant le paiement, donc sur les coûts **variables**,
sur lesquels le kit de Yondu est bâti. Détail et arbitrage dans son gabarit.

### 6. `GetBindFace()` fait `assert face` — trouvé par l'AUTOPLAY, pas par les tests

Il lève une `AssertionError` dès que la carte n'est **pas** attachée, et la Yaka
Arrow passe son temps à l'être. **Neuf appels directs** dans le pack. Le moteur
avale l'exception : la capacité ne fait rien, en silence.

⚠ **Le tableau d'autoplay affichait `0 traceback` et `0 partie bloquée`.** Les
erreurs n'étaient que dans les **journaux de partie**, fichier par fichier —
2 fois sur 128 parties, depuis la condition de `yd015`. C'est exactement ce que
l'étape 8 impose (« grep exhaustif des journaux, pas seulement le bilan »).

Le pack lit désormais l'hôte d'une carte par un accesseur sûr, `Hote`, présent
dans les deux sets, avec l'avertissement écrit sur place.

---

## Ce que l'outillage ne couvre pas — dit, pas maquillé

- **Le surpaiement de `yd006`** (« repeat for each resource overpaid ») :
  `surpayer` vide la main dès le **premier** paiement, or il faut payer deux
  cartes dans le même cas. La répétition reste à vérifier en partie réelle.
- **Les paliers 3 et 4 de `yd009` Invest** : `surpayer` n'agit que sur les
  coûts de **mise en jeu**, pas sur ceux d'**activation** passés par
  `Puzzle.Action` (mesuré : main 1 au lieu de 5). Les deux cas correspondants
  ont été **retirés plutôt que laissés rouges**, et le palier réellement
  atteignable (X = 0) est testé.
- **Un déplacement d'ennemi à ennemi** : `cibles` apparie par `card_id` **sans
  consommer** les entrées, donc le choix retombe toujours sur l'hôte courant.
  Les cas visent la branche sans cible (« to your identity »).
- **Le doublement de `yd007`** : non observable, voir son gabarit.

### Deux pièges du harnais, désormais écrits dans `test_capacites.py`

- **Les espaces deviennent des underscores** dans le nom d'une option :
  `ForChoiceAbility("Add Yaka Arrow to your hand")` est publié
  `Add_Yaka_Arrow_to_your_hand`. Un `choisir_option` écrit avec des espaces ne
  s'apparie **jamais** et le harnais retombe silencieusement sur la première
  option. Constaté via `TRACE_OPTIONS=1`. **Deux cas de packs antérieurs**
  (Déferlement, Stun Thor) étaient dans ce cas et ont été corrigés.
- **`attributs_carte` attend un ÉCART**, pas une valeur absolue (le harnais
  compare `base + écart`).
- **Yondu a DEF 2, appliquée d'office** sans défenseur déclaré : un attaquant à
  ATQ 2 inflige 0. Trois cas ne pouvaient rien discriminer.

---

## Gabarits, carte par carte

Les blocs « étape 2 » et « étape 5 » sont écrits **en tête de chaque module**.
Ce fichier donne le verdict et ce qui est propre à la carte.

### yd001a : * Yondu (face héros)

- [x] Étape 2 : `alligator_loki/__init__.py` pour la fenêtre de départ ouverte
      à la main ; `AfterCardAttachTo` pour l'arrivée.
- [x] Étape 5 : mots-pièges « attached to **OR removed from** » = deux
      fenêtres ; l'arrivée sur l'identité **soigne**, sur un ennemi elle
      **blesse**. Résultat : conforme.
- [x] Étape 6 : PV 10, ATQ 2, CTR 2, DEF 2, main 5.
- [x] Étape 7 : 1 cas, rouge 1/1.

**Carte terminée : OUI**

### yd001b : * Yondu Udonta (face alter-ego)

- [x] Étape 2 : `ok001b` pour `Search.PlayerCard` + `GainCard`.
- [x] Étape 5 : deux actions distinctes, la seconde à coût `Exhaust`.
      `LimitOncePerRound` sur Crew Cut. Résultat : conforme.
- [x] Étape 6 : PV 10, REC 3, main 6.
- [x] Étape 7 : 3 cas (deck, **défausse**, Whistlin'), rouges 3/3. Le cas
      « depuis la défausse » est celui qui justifie l'arbitrage `summon`.

**Carte terminée : OUI**

### yd002 : Cheap Shot — **OUI** (2 cas, rouges 2/2 ; nominal + contre-témoin sans flèche)
### yd003 : Fight Dirty — **OUI** (1 cas, rouge 1/1 ; jumelle de yd002 côté manigance)
### yd004 : Whistle While You Work — **OUI** (2 cas, rouges 2/2 ; branche nominale + repli « summon »)
### yd005 : Tough Motherlover — **OUI** (2 cas, rouges 2/2 ; condition lue dans la MAIN)
### yd006 : Twirlin' and Whirlin' — **OUI** (1 cas, rouge 1/1 ; surpaiement non couvert, voir plus haut)

### yd007 : Jackpot!

- [x] Étape 2 : `AfterYouSpendThisCard` + `WhenCountingResourcesOnCards`.
- [x] Étape 5 : « la PROCHAINE carte dépensée », donc un enregistrement
      temporaire. Résultat : conforme au texte.
- [x] Étape 6 : ressource [wild], aucun coût, 1 exemplaire au deck.
- [ ] **Étape 7 : 1 cas, rouge 0/1 — le doublement n'est PAS prouvé.**

**Carte terminée : NON au sens strict du processus** (aucun cas ne tombe au
rouge sans son module). **Mais la carte est correcte** : ce qui manque est un
montage de test, pas un correctif.

⚠ **CORRECTION D'UNE PREMIÈRE ANALYSE.** Ce fichier concluait « carte quasi
inerte ». **C'était trop fort**, faute d'avoir testé autre chose qu'un coût
fixe. Ce que le moteur impose : il valide le coût **avant** d'autoriser la mise
en jeu, avec les valeurs nominales (journal : `Helicarrier (Turn Option,Play)
[01092] WhenPlayerInTurn failed`). Jackpot, qui double **après** avoir été
dépensée, ne peut donc pas débloquer un coût **fixe** inatteignable.

Mais le doublement agit bien **pendant le paiement**, donc sur les coûts
**variables** — et le kit de Yondu est bâti dessus : `yd006` « repeat for each
resource overpaid » coûte 0 (jamais bloquée) et `yd009` lit des paliers. La
carte sert à ce pour quoi l'auteur l'a mise là.

**Pourquoi le doublement reste non testé** : il faudrait surpayer une carte
APRÈS en avoir payé une autre dans le même cas, or `surpayer` vide la main dès
le premier paiement. Même limite que `yd006` et `yd009`.

**Arbitrage de l'utilisateur, 04/09/2026 : gardée telle quelle**, fidèle au
texte de l'auteur.


### yd008 : Ravager Redshirts — **OUI** (2 cas, rouges 1/2 ; le vert est le contre-témoin)
### yd009 : Invest — **OUI** (1 cas, rouge 1/1 ; paliers 3 et 4 non couverts, voir plus haut)
### yd010 : Ravage — **OUI** (3 cas, rouges 2/3 ; le vert est le contre-témoin. Mot-clé maison `fragile` + compteur `wound`)
### yd011 : Tahlei — **OUI** (2 cas, rouges 2/2 ; branche « en main » incluse)
### yd012 : Yaka Arrow — **OUI** (3 cas, rouges 2/3 ; +1 ATQ/+1 CTR et interruption forcée à la mort de l'hôte)
### yd013 : Banished — **OUI** (2 cas, rouges 2/2 ; les DEUX branches, « remove from game » ≠ « discard »)
### yd014 : Price on Your Head — **OUI** (2 cas, rouges 2/2 ; branche Sav'rkk + repli sur le méchant)
### yd015 : * Sav'rkk — **OUI** (1 cas, rouge 1/1 ; volet RENCONTRE de `summon`)
### yd016 : Sword-Gun-Arm — **OUI** (2 cas, rouges 1/2 ; le vert est le contre-témoin. PV **restants**, pas imprimés)
### yd017 : Hard to Kill — **OUI** (2 cas, rouges 2/2 ; convocation + révélation, et la branche « déjà en jeu »)
### yd018 : Savage Destruction — **OUI** (1 cas, rouge 1/1 ; en forme civile, qui n'a aucune DEF)

---

## Correctif MOTEUR livré dans le même travail

Sans rapport avec Yondu, trouvé en cours de route sur signalement utilisateur
(« Angela peut faire ses trucs plusieurs fois par round ») :
`src/game/ability/condition/once_per.py`, `GetForDelayAbility`.
`LimitOncePerRound` était **silencieusement inerte** sur toute la famille
`AfterUnitDefeatedUnit`. Trois cartes touchées : `an001a`, `an009`, `vp001a`.
Détail complet dans `docs/reference/RECETTES-MOTEUR.md` et nouvelle **étape
7 bis** de `PROCESSUS-CARTE.md`.
