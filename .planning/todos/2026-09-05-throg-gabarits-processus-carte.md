# PROCESSUS-CARTE.md — les 17 gabarits du pack THROG (set 159, `tg`)

Gate de `PROCESSUS-HEROS.md` : un gabarit rempli par carte. Rédigés le
05/09/2026. Auteur du pack : **Rainy**, zip « Throg ».
Aspect **Agressivité**, arbitrage utilisateur (le zip n'a aucune decklist).

**Preuves communes**, citées une fois :

- **Étape 7, cas** : `test_capacites.py … /tmp/cap5.json tg0` → **37/37**.
- **Étape 7, substitution** : `substituer_pack.py` → **17/17 cartes** ont au
  moins un cas qui tombe au rouge sans leur module. Détail :

  | Carte | rouges | Carte | rouges | Carte | rouges |
  |---|---|---|---|---|---|
  | tg001a | 1/2 | tg007 | 1/1 | tg013 | 3/4 |
  | tg001b | 3/3 | tg008 | 1/2 | tg014 | 1/1 |
  | tg002 | 1/1 | tg009 | 2/3 | tg015 | 1/2 |
  | tg003 | 2/2 | tg010 | 4/4 | tg016 | **4/4** |
  | tg004 | 1/1 | tg011 | 2/2 | | |
  | tg005 | 1/1 | tg012 | 1/2 | | |
  | tg006 | 1/2 | | | | |

  Les cas qui restent verts sont tous des **contre-cas d'ABSENCE d'effet**, ou
  la ligne de base de `tg013` qui n'implique pas son module : ils sont listés
  carte par carte ci-dessous, jamais masqués.
  ⚠ `tg016` est à **4/4**, y compris le cas de la défense : c'est la preuve que
  le correctif moteur est réellement exercé par un cas, et pas seulement écrit.
- **Étape 1** : pack `throg` en queue de `cards.json`, set
  `159. Custom (Throg)`, préfixe `tg` déclaré, `verifier_prefixes` OK
  (aucun doublon, aucun préfixe non déclaré, aucun numéro emprunté).
- **Étape 4, image** : `assets/pics/tg0*.jpg` pour les 17, découpées du zip par
  `tools/importer_images_throg.py` (la recette est le seul artefact
  reproductible, `assets/pics/` étant gitignoré).
- `test_cards` : **5272 ok / 0 erreur** (5255 avant le pack, soit +17).
- `verifier_desc_mots_cles throg` : « les 17 cartes ont un desc conforme à
  leur texte ».
- `verifier_noms_modules` : « aucun nom inconnu dans throg ».
- `verifier_appels_modules` : « tous les appels de throg existent » —
  **et la gate a été CALIBRÉE** (§9 de PROCESSUS-CARTE) : on lui a injecté un
  `Faces.GiveStatusQuiNExistePas` dans `tg010`, elle a rendu
  « throg.throg/tg010.py:54 … n'existe pas / 1 appel(s) inexistant(s) », puis
  le fichier a été remis. Un « OK » non calibré ne prouve rien.
- **Étape 3** : `deck/starter/throg.json`, et le deck **monte une partie**
  (`verifier_tous_les_decks`, `DECK_NOM=throg` → « identite tg001a, main 6,
  deck 34 »). Main 6 et non 5 : la partie commence en forme civile, et
  Puddlegulp a une main de 6.
- **Étape 10** : contrôle des signatures étrangères sur les **122 decks de
  départ** → **0 écart**.
- **Étape 7 (héros)** : biographie `tg001a` dans `heros-info.js`
  (`node --check` OK).
- **Étape 8 (héros)** : les 17 textes français dans `textes-fr-fanmade.ts`
  (`tsc --noEmit` OK), **déployés** par `ui-app/deployer.sh` — sans quoi rien
  n'apparaît dans le jeu (§11 du GUIDE).
- **Étape 8, autoplay** : **16 parties**, deux vilains, avec `beta_ray_bill`
  comme témoin dans chaque fournée.

  | Fournée | Throg | Témoin `beta_ray_bill` |
  |---|---|---|
  | Rhino, 8 parties | 4.2 rounds, 0 % V, 0 bloquée | 4.1 rounds, 0 % V, 0 bloquée |
  | Klaw, 8 parties | 4.0 rounds, 0 % V, 0 bloquée | 4.5 rounds, 0 % V, 0 bloquée |

  **Grep exhaustif des 32 journaux : 0 traceback**
  (`NameError|AttributeError|TypeError|KeyError|AssertionError`). Le profil de
  Throg est celui du témoin, à quelques dixièmes de round près.
- `audit_cartes` : OK.
- `verifier_cartes_en_jeu throg` : OK.
- `verifier_api_cartes` : 3 fautes, **toutes ANTÉRIEURES et hors de ce pack** —
  `blink/bk007.py` (handler jamais passé à une fabrique, code mort),
  `spot/sp018.py` (`CardFinder(..., is_odd_cost=...)`, argument inconnu) et
  `web_of_deceit/underling/__init__.py` (garde sur une API inexistante,
  branche morte). Aucune dans `throg`. Signalées, pas corrigées : autre pack,
  autre chantier.

---

## LES DEUX GATES DE PORTÉE (fichiers moteur PARTAGÉS touchés)

`card_face.py` (énum `COUNTER`), `can_defense.py` et `sender_unit.py` ont été
modifiés : le §6bis du GUIDE impose alors la passe complète, pas seulement les
cas du pack.

- **`verifier_tous_les_decks`, les 122 decks** → **121/122**. Le seul échec est
  `sp_dr` (« setup : AssertionError: self=[(01,31002a) Peni Parker] »), déjà
  consigné comme **antérieur** par le portage `beta_ray_bill` du matin même.
- **Batterie complète `test_capacites`** → **1330/1334**. Les 4 rouges sont les
  4 rouges antérieurs de `squirrel_girl` (`sg006`, `sg007`, `sg009`, `sg013`),
  même pack et même compte que la batterie du matin (1293/1297). L'écart de
  total, **1297 → 1334, est exactement les 37 cas ajoutés ici**. Aucun des
  quatre ne touche à une défense de base : le correctif moteur n'a rien cassé.

---

## CE QUE CES BLOCS NE PEUVENT PAS VOIR

⚠ **Aucune partie n'a été jouée par un humain dans le navigateur.** C'est le
seul juge de « est-ce que la carte est agréable et fait ce qu'elle promet », et
le processus demande de l'écrire noir sur blanc quand ce n'est pas fait.

⚠ **L'autoplay n'exerce que 11 des 17 cartes**, même sur 16 parties et deux
vilains. Recensement cumulé (déclenchements) : `tg009` 28, `tg010` 15,
`tg007` 12, `tg008` 10, `tg002` 7, `tg001a` 6, `tg013` 4, `tg016` 4,
`tg011` 3, `tg003` 1 — plus `tg001b`, exercée à chaque mise en place.

**Jamais activées** : `tg004`, `tg005`, `tg006`, `tg012`, `tg014`, `tg015`.
Deux raisons, mesurées et non supposées :

- les trois Interruptions et l'Action à coût du pack (`tg004` Hammer Throw,
  `tg005` Lightning Leap, `tg006` Thunderous Charge) ne sont **jamais jouées** :
  le pilote se contente de les dépenser comme ressources (« Throg gains
  resource Y from Lightning Leap » revient dans presque toutes les parties) ;
- `tg012`, `tg014` et `tg015` sont des complots némésis, qui n'arrivent que par
  `01190` Shadow of the Past — sorti une fois sur seize.

Ces six cartes restent prouvées par leur cas de test **et** par la preuve par
substitution, pas par une partie. C'est écrit ici pour ne pas être pris pour
une couverture qu'il n'y a pas.

Ce qui **se lit en clair** dans le journal, en revanche :

- la boucle du marteau, ligne par ligne (partie 1, lignes 185-206) : Throg
  déclare une défense de base → `Frogjolnir` s'incline et lui donne +1 DEF →
  Rhino ne place plus qu'1 dégât → Frogjolnir est **renvoyé en main** → *Throg
  activates, targets Throg* → **Throg readied**. C'est `tg001a` Froglike
  Stamina et `tg009` sur le même usage, bout à bout ;
- `tg016` Chomped : *« WhenUnitWouldAttack » est remplacé par [Chomped]*, puis
  la carte est défaussée et l'identité prend 1 dégât. Le mot « instead » de la
  carte imprimée, écrit par le moteur lui-même ;
- `tg011` : *activates → perd 1 compteur « foe » → [Shocker] va attaquer
  [Throg]*. Les trois moitiés de la carte, dans l'ordre.

---

## CE QUE LE PACK A, ET QUE LE PRÉCÉDENT N'AVAIT PAS

**Un set némésis complet**, contrairement à `beta_ray_bill`, `hulk_rainy` et
`viv_vision` — les trois autres packs de Rainy, qui devaient tous emprunter le
set d'un héros officiel. Ici les cinq cartes sont fournies : Adorable
Distraction, Alligator Loki, Causing a Commotion, « Lost » Property, Chomped.

**Aucune decklist**, en revanche. Pas de dossier `Extras`. L'aspect
**Agressivité** a été arbitré par l'utilisateur le 05/09/2026.

---

## LA MÉCANIQUE : UNE SEULE AMÉLIORATION

`tg009` **Frogjolnir** est unique, Restreinte, coûte 1, et **cinq des onze
cartes du set héros la citent nommément** :

| Carte | Ce qu'elle fait du marteau |
|---|---|
| `tg001a` Froglike Stamina | le **renvoie en main** pour redresser Throg |
| `tg001b` Worthy | va le **chercher**, où qu'il soit |
| `tg002` Airborne Amphibian | le **redresse** avec le héros |
| `tg004` Hammer Throw | l'**incline et le rappelle** pour frapper à 6 |
| `tg009` lui-même | s'**incline** pour +1 à un pouvoir de base |
| `tg015` « Lost » Property | le **confisque** sous elle |

Même moteur économique que le Stormbreaker de `beta_ray_bill` : l'aller-retour
main ↔ jeu, en permanence.

---

## LE CONTRASTE QUI COMMANDE TOUT LE PACK

⚠ **Les deux faces ont des NOMS DIFFÉRENTS** : « Throg » en héros,
« Puddlegulp » en alter-ego. C'est l'inverse de `beta_ray_bill`, dont les deux
faces s'appellent pareil et où le filtre devait être le TYPE.

Conséquence, appliquée carte par carte : un **NOM PROPRE ne désigne qu'UNE
face**, « you » désigne l'identité, donc les deux. Le piège `an002` Sera /
`06007` Asgard (RECETTES-MOTEUR §3), trouvé **en partie réelle** le 1/9/2026 et
jamais par les tests. `tg010` Throg's Armor porte les deux écritures **sur la
même carte** :

> You get **+2 hit points**. — Hero Response: … give **Throg** a tough status
> card.

Deux contre-cas écrits pour ça, et une **clé de harnais créée** pour le
premier : `traits_absents` n'existait pas, on ne pouvait donc pas prouver
qu'un trait ne fuit pas sur l'autre face.

---

## LE CORRECTIF MOTEUR : LA DÉFENSE DE BASE DEVIENT REMPLAÇABLE

`Message.WhenUnitWouldDefend` portait le commentaire « No `CanBeInstead` » et
n'héritait pas de la classe. Ses trois sœurs — `WhenUnitWouldAttack`,
`WhenUnitWouldThwart`, `WhenUnitWouldRecovery` — l'ont toutes. **Aucune carte
du jeu ne pouvait remplacer une DÉFENSE de base.** `tg016` Chomped dit « When
you would use a basic power, … instead » : elle laissait donc passer un
pouvoir sur quatre, en silence.

Deux lignes, calquées sur `can_attack.py:151` :

- `CanBeInstead` ajouté aux bases du message (`sender_unit.py`) ;
- `if would_defense_message.is_be_instead: return None` dans
  `CanDefense.DefenseInternal`, **avant** `SetDefender`.

Sans `SetDefender`, `being_atk_message.defense_messages` reste vide : la DEF
ne réduit rien (`can_attack.py:231`) et aucun `AfterUnitDefendEnd` ne part. Le
coût d'inclinaison, lui, reste payé — c'est le modèle **uniforme** du moteur
pour les quatre pouvoirs (`ThisCanAttack` friend.py:99 et `ThisCanDefense`
friend.py:236 posent tous deux `CostFunc.Exhaust("This")` avant la résolution).

⚠ `can_defense.py` et `sender_unit.py` sont des fichiers **partagés** : la
règle de portée du §6bis du GUIDE impose la batterie complète.

Décision utilisateur du 05/09/2026, à la question posée avant d'écrire la
carte : « il faut que ça match à 100 % ». Les trois options d'écart proposées
(interdire la défense, la laisser passer, la faire payer sans la remplacer)
ont donc été écartées au profit du correctif.

---

## CE QUE LES GATES ONT TROUVÉ

### 1. `Puzzle.Attack(hero, X)` fait DÉFENDRE X — la doc disait le contraire

`RECETTES-MOTEUR.md` §7 conseillait `Puzzle.Attack('<hero>', '<vilain>')` pour
faire frapper le héros. **Le second paramètre s'appelle `defender`**
(`puzzle.py:385`, docstring explicite) : il fait défendre cette carte, il ne
la désigne pas comme cible. Sur un vilain la différence ne se voit pas — il
est de toute façon la seule cible — mais sur un sbire l'attaque part ailleurs.

Deux cas lisaient 0 dégât sans rien comprendre (`tg005`, `tg012`). La cible se
force par **`cibles`**. Ligne corrigée dans RECETTES.

### 2. Le complot principal de Rhino se COMPLÈTE à 7

`01097b` porte `TargetThreat: 7*`. Trois cas posaient 10, 12 ou 20 menaces
pour avoir de la marge : le complot avançait, **et toutes les commandes
suivantes de la mise en place devenaient inertes** — sbires non posés, main non
vidée, carte non jouée. Aucun message. Les 61 cas existants du dépôt qui
touchent ce complot restent tous ≤ 6, ce qui explique que personne ne l'ait
rencontré. Les cas visent désormais un complot **annexe**, qui n'a pas de seuil.

### 3. `main_exclusive: []` ne vide PAS la main

Le harnais teste `if cas.get("main_exclusive")` : une liste vide est **fausse**,
le bloc est sauté, et la main de départ reste en place. Cinq cas mesuraient
donc une main de 7 cartes en en attendant 1. Il faut au moins une carte —
`["01090"]`, une ressource que le pilote ne peut pas jouer.

### 4. Un sélecteur ne voit pas le message d'un ÉVÉNEMENT joué en Interruption

`25013` * Thor calcule ses cibles dans un `SetTarget(fn, range="All")` qui lit
`effect.GetBindMessage(...)`. Ça marche pour une capacité d'**allié**, dont
l'effet est déjà lié au message quand le sélecteur tourne. Pour un
**événement** joué (`.SetPlay()`), le sélecteur est évalué **avant** la
liaison : il rend une liste vide, l'abilité n'a donc aucune cible légale et
n'est **jamais proposée**. La carte restait en main sans un mot.

`tg005` et `tg006` calculent leurs cibles **dans l'opération**. Il n'y a de
toute façon aucun choix à faire : le texte dit « each ».

### 5. Une capacité temporaire posée par un événement meurt avec lui

`tg006` enregistrait son ignorance de la crise sur `this.effect` (l'événement).
L'événement quitte le jeu, et ses effets temporaires partent **avant** que le
contre ne retire la menace : la crise n'était jamais ignorée, et le complot
principal gardait ses menaces. La capacité est portée par le **héros**
(`contreur.effect`), leçon `ah007` déjà payée sur le pack
totally_awesome_hulk.

### 6. Substituer un module À LA MAIN donne un FAUX VERT

Remplacer un module par un `return []` avec un `printf >` laisse le
`__pycache__` du pack en place : le moteur recharge le `.pyc` de la vraie
carte et le cas **repasse au vert**. Trois substitutions manuelles ont ainsi
accusé à tort le cas Perforation de `tg013`. `substituer_pack.py` appelle
`purger_pycache()` avant et après chaque carte (lignes 79 et 93) : c'est la
seule différence, et elle change le verdict. Consigné dans RECETTES §7.

### 7. Un cas qui ne prouvait rien, attrapé par la substitution

Le cas Perforation de `tg013` mesurait `degats_identite_min: 3` sur un Throg
Tenace. Il restait vert sans le module. Une **ligne de base** a été ajoutée :
`01131` * Tiger Shark, ATK 3 identique et **aucune** Perforation, contre le
même Throg Tenace → **0 dégât**. C'est ce 0 qui donne son sens aux 3.
Mesure à la sonde : 3 dégâts avec le module, 0 sans.

### 8. Une clé d'assertion MORTE, et deux vrais défauts cachés dessous

`degats_identite_min` était écrite dans des cas depuis longtemps, mais
n'existait que dans `al_frogjolnir_sur_throg`, une vérification **propre au
pack alligator_loki**. Tout cas qui l'employait avec
`"verifier": "etat_attendu"` voyait son assertion **silencieusement ignorée**.

Cinq cas de ce pack passaient dessus. Deux cachaient un vrai défaut :

- **`tg011`** : « That enemy attacks you » lisait 0 dégât. Le sbire attaquait
  bien, mais Throg **déclarait une défense de base** et sa DEF 2 annulait
  l'ATQ 1 du sbire. L'identité est désormais inclinée d'avance.
- **`tg016`** : « When the round ends » ne partait **jamais**.
  `Puzzle.BeginVillainPhase()` OUVRE la phase du vilain, elle ne termine pas le
  round : le message `WhenRoundEnd` n'était jamais envoyé. Une vérification
  dédiée l'envoie à la main, sur le modèle `brawn_hulk_out_fin_de_round`.

Trouvé parce que le cas Perforation de `tg013` restait vert sous substitution
alors que la sonde mesurait **3 dégâts avec le module et 0 sans, trois fois de
suite**. La clé a été implantée dans `etat_attendu` puis **calibrée** : elle
fait maintenant tomber ce cas avec « degats sur l'identite = 0 (attendu au
moins 3) ».

⚠ Leçon générale, consignée dans RECETTES §7 : **avant d'écrire une clé de
`attendu`, vérifier qu'elle est lue par la fonction de vérification qu'on
déclare.** La liste en tête de `test_capacites.py` documente des clés que
toutes les vérifications n'implémentent pas.

### 9. Deux clés manquaient au harnais, et l'une bloquait une gate du processus

- **`traits_absents`** : le pendant négatif de `traits`. Sans elle, impossible
  de prouver qu'un trait accordé par une carte ne fuit pas sur l'autre face —
  alors que RECETTES §3 l'**exige** depuis le défaut `an002`, trouvé en partie
  réelle et jamais par les tests.
- **`declencher_tolerant`** : `Puzzle.Action` lève un `AssertionError`
  (« n'offre aucune action disponible ») quand le moteur refuse le second
  déclenchement, c'est-à-dire **exactement quand la limite mord**. Le témoin
  d'épuisement exigé par l'étape 7 bis ne pouvait donc pas être vert pour
  **aucune** limite « once per round » portée par une Action. La preuve reste
  un chiffre dans `attendu` ; la clé ne fait qu'autoriser la tentative.

---

## MOTS-CLÉS RENCONTRÉS

| Mot-clé | Carte | État |
|---|---|---|
| `Uses` | tg011 | ❌ **absent des fiches → fiche `uses.md` CRÉÉE**. 9 cartes livrées l'employaient déjà sans fiche |
| `Restricted` | tg009 | fiche existante, base automatique `desc.Restricted` |
| `overkill` | tg004 | fiche existante |
| `guard` | tg005 | fiche existante (clause « ignoring », voir tg005) |
| `crisis` | tg006, tg012 | fiche existante |
| `hazard` | tg014 | fiche existante, icône identifiée **par comparaison d'image** |
| `hinder` | tg012 | fiche existante, base automatique `desc.Hinder = "1*"` |
| `toughness` | tg010 | fiche existante |
| `piercing` | tg013 | fiche existante |
| `boost` | tg016 | fiche existante — l'étoile n'existe que si `WhenCardBecomeBoost` est écrite |
| `special` | tg013, tg016 | fiche existante, les `[star]` codés toujours actifs |

Le compteur `foe` a été ajouté à l'énum `COUNTER` de `card_face.py` : sans lui,
`IsCounter('foe')` refuse le nom et l'obligation tombe dès la construction du
deck (même panne que `style` pour kate_bishop et `disguise` pour beast).

---

## ÉCARTS ASSUMÉS

- **`tg005` Lightning Leap, « ignoring the guard keyword »** : aucun code n'est
  nécessaire, le garde n'étant lu que par `Villain.CanBeAttackBy`
  (villain.py:72), c'est-à-dire à la SÉLECTION des cibles. Une cible ajoutée
  par `AddTarget` ne repasse pas par ce filtre. Conséquence : le message
  `AfterIgnoreKeywordOnCard("Guard")` n'est pas émis, faute d'avoir eu à
  ignorer quoi que ce soit. Une carte qui réagit à « after you ignore the guard
  keyword » (`32034` Acute Control, Justice) ne se déclencherait pas.
- **`tg006` Thunderous Charge, « in the order of your choice »** : le moteur
  résout les manigances dans l'ordre de la liste (can_thwart.py:139), le joueur
  ne choisit pas. Sans conséquence tant qu'aucune manigance ne déclenche un
  effet en étant vaincue.
- **`tg011`, « Victory 0 »** : `has_uses.py:54` teste `if self.victory:`, et `0`
  est faux — la carte est **défaussée** au lieu d'aller dans la pile de
  victoire. Écart moteur préexistant, partagé par `51031`, `53029`, `59004` et
  `br012`. Décrit dans `mots-cles/uses.md`. Sans conséquence tant qu'aucune
  carte ne compte la pile de victoire.
- **`tg013`, type de la première étoile** : le texte imprimé dit « Forced
  **Interrupt**: When Alligator Loki schemes **and places threat** ». On ne peut
  pas connaître « that much » avant que la menace soit posée. Le moteur n'a
  qu'une prise, `AfterEnemySchemeAndPlaceThreat`, qui est un « après ». La
  contradiction est dans le texte imprimé (même famille que « Forced Interrupt:
  After Maniac schemes », The Made Men) et n'a aucune conséquence observable :
  rien ne peut s'intercaler entre les deux moments.
- **`tg004` Hammer Throw, le retour en main devant la flèche** : c'est une
  seconde moitié de COÛT, pas un effet. Conséquence en jeu : aucune. Incliner
  exige déjà que le marteau soit en jeu et prêt, et un marteau en jeu revient
  toujours en main — le coût ne peut pas échouer à mi-chemin. Le retour est
  donc écrit dans le corps, avant les dégâts, ce qui rend l'ordre imprimé à
  l'identique sans ouvrir au joueur une seconde sélection de la même carte
  unique. Choix purement technique (GUIDE §9).

---

## HOMONYMES ET NOMS

- ⚠ **`tg004` Hammer Throw est le TROISIÈME du dépôt** : `06005` (Thor,
  officiel, incline Mjolnir → 8 dégâts puis le rend), `br003` (Beta Ray Bill,
  incline Stormbreaker → 6 dégâts puis le **cherche**), `tg004` (incline
  Frogjolnir **et le rend** → 6 dégâts). Un `Search(name="Hammer Throw")` voit
  les trois : le texte français est écrit sur le `card_id`, jamais sur le nom.
- ⚠ **`tg013` « * Alligator Loki » est un SBIRE**, sans aucun rapport avec
  `al001a`, le **héros** du pack `alligator_loki` (set 140) : 5 PV contre 9,
  aucun code commun. Le plan de portage s'était déjà trompé une fois en croyant
  l'inverse (§6 du todo du 29/08/2026).
- ⚠ **Le zip numérote les deux faces à l'envers** : « 0.1 » est l'ALTER-EGO
  (Puddlegulp), « 0.2 » le HÉROS (Throg). Vérifié sur les libellés imprimés
  ALTER-EGO / HERO et sur les statistiques, pas sur le nom de fichier. Même
  piège que `br001a/b`.
- ⚠ **Cinq cartes sont livrées en plusieurs exemplaires** et n'ont donc qu'un
  card_id. Les scans ont été comparés **au pixel** (coût, icône de ressource,
  bloc de texte) : écart maximal **0** partout. Ce n'est pas le cas de figure
  `bt007a/b` Multi-Tasking, où deux scans de même nom différaient par l'icône.

---

## Gabarits, carte par carte

### tg001a : * Throg (face héros)
- [x] Étape 2 : `14001a` * Quicksilver (« Super Speed — Response: After you use
      one of Quicksilver's basic powers, ready him. (Limit once per phase.) »),
      mot pour mot le même déclencheur, le même effet et la même limite ;
      `tt001a` pour la convention du `[star]` sur une face héros ;
      `53002`/`04004` pour `CostFunc.ReturnToHand`.
- [x] Étape 5 : « uses a BASIC POWER » = les trois du héros, pas la
      récupération (elle appartient à Puddlegulp, autre face). « return
      Frogjolnir to your hand » est **devant la flèche** : un coût, qui borne la
      carte. « to YOUR hand » → `to_who="Owner"`. « ready THROG » = la face
      héros, le nom ne désigne qu'elle.
- [x] Étape 6 : PV 12, CTR 1, ATQ 2, DEF 2, main 5. Limite une fois par PHASE.
- [x] Étape 7 : 2 cas, **rouge 1/2** — le second est le témoin d'épuisement,
      qui mesure une ABSENCE (Throg reste incliné) et reste donc vert sans
      module. Assumé, convention `vp014`/`ho017`.
- [x] Étape 7 bis : limite imprimée **OUI**. Témoin : deux pouvoirs de base
      dans la même phase, le marteau remis en jeu entre les deux pour que le
      coût du second soit **payable** — sans ça le cas prouverait l'absence de
      marteau, pas la limite. Chiffre mesuré au second : `exhausted: [tg001a]`.

**Carte terminée : OUI**

### tg001b : * Puddlegulp (face alter-ego)
- [x] Étape 2 : `br001b` Starfarer (même auteur, même structure) ; `04001b`
      Clint Barton ; `bk008` (⚠ `Search.PlayerCard` rend **une face ou None**).
- [x] Étape 5 : « FIND » couvre le deck, la défausse **et le terrain** — les
      deux chemins ont leur cas. ⚠ **Aucun effet secondaire**, contrairement au
      `Worthy` de `br001a` qui frappe pour 3 : ne pas recopier la carte de
      référence sans la relire.
- [x] Étape 6 : PV 12, REC 4, main 6. Limite une fois par ROUND.
- [x] Étape 7 : 3 cas, **rouges 3/3**.
- [x] Étape 7 bis : limite imprimée **OUI**. Témoin : deux Actions dans le même
      round, deux Frogjolnir dans le deck pour que la seconde soit payable.
      Chiffre : `taille_main: 2` (la ligne de base plus **un seul** marteau).
      ⚠ La seconde Action est refusée par le moteur : elle passe par
      `declencher_tolerant`, clé **créée pour ce témoin**.

**Carte terminée : OUI**

### tg002 : Airborne Amphibian — **OUI** (1 cas, rouge 1/1 ; ⚠ la seconde phrase ne fait JAMAIS rien en solo, il n'y a pas d'autre joueur — écrit dans le module plutôt que laissé croire à une panne)
### tg003 : Great Courage — **OUI** (2 cas, rouges 2/2 ; le second est le témoin du plafond « to a maximum of 3 » : 4 sbires engagés retirent 8 menaces, pas 10)
### tg004 : Hammer Throw — **OUI** (1 cas, rouge 1/1 ; troisième homonyme du dépôt, voir plus haut)
### tg005 : Lightning Leap — **OUI** (1 cas, rouge 1/1 ; cibles calculées dans l'opération, pas dans un `SetTarget` — voir « ce que les gates ont trouvé » §4)
### tg006 : Thunderous Charge — **OUI** (2 cas, rouge 1/2 ; le second est la ligne de base « sans elle, la crise bloque le complot principal », contre-cas d'absence, vert sous substitution et assumé)
### tg007 : * Foreverglade — **OUI** (1 cas, rouge 1/1 ; ⚠ `AlterEgoResponse` et non `Response`, sans quoi la récupération d'un allié en forme héros déclencherait aussi)
### tg008 : Frog of Thunder — **OUI** (2 cas, rouge 1/2 ; le second paie une carte NON Throg et attend 0 dégât — contre-cas d'absence, assumé. ⚠ AUCUN `for_card` : la ressource paie n'importe quoi, seul le BONUS est conditionné)
### tg009 : * Frogjolnir — **OUI** (3 cas, rouges 2/3 ; le vert est le contre-cas `traits_absents` en forme alter-ego, exigé par RECETTES §3 et rendu possible par la clé créée pour l'occasion)
### tg010 : * Throg's Armor — **OUI** (4 cas, rouges 4/4 ; les deux portées « You » / « Throg » sur la même carte, plus le témoin d'épuisement « once per phase » : deux sbires engagés, **une seule** carte piochée)
### tg011 : Trouble in Central Park — **OUI** (2 cas, rouges 2/2 ; ⚠ bandeau THROG donc module dans `throg/throg/`, piège `bt019` payé une **8ᵉ** fois. La flèche est APRÈS « put it into play » : convoquer est le COÛT. Témoin d'épuisement par `declencher_tolerant`)
### tg012 : Adorable Distraction — **OUI** (2 cas, rouge 1/2 ; le second est la ligne de base sans le complot, contre-cas d'absence assumé. ⚠ La carte protège une AUTRE carte : le littéral `"This"` de `th012` aurait été faux)
### tg013 : * Alligator Loki — **OUI** (4 cas, rouges 2/4 ; les deux verts sont le cas Perforation et sa ligne de base, voir « ce que les gates ont trouvé » §7 — la mesure à la sonde donne 3 dégâts avec le module et 0 sans)
### tg014 : Causing a Commotion — **OUI** (1 cas, rouge 1/1 ; ⚠ `Puzzle.CreatePlayerDeck` AJOUTE au deck, il ne le remplace pas : les trois cartes ont dû être remontées par `Puzzle.PutIntoDeck`, et choisies ÉTRANGÈRES au deck de Throg pour que `FindCommandCards` ne prenne pas un autre exemplaire)
### tg015 : « Lost » Property — **OUI** (2 cas, rouge 1/2 ; « It cannot be found while under here » ne demande AUCUN code, et c'est le cas qui le prouve : `Worthy` fouille le terrain, le deck et la défausse et ne rapporte rien)
### tg016 : Chomped — **OUI** (4 cas ; ⚠ la carte qui a exigé le correctif moteur. Le déclencheur est branché sur les messages `WhenUnitWould...` et PAS sur `WhenUnitUseBasicPower`, envoyé APRÈS le test de remplacement : un `SetBeInstead` posé depuis lui arriverait toujours trop tard)

**17 cartes terminées sur 17.**
