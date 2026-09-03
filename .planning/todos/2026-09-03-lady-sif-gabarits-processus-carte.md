# PROCESSUS-CARTE.md — les 18 gabarits du pack LADY SIF (set 150, `ls`)

Gate de `PROCESSUS-HEROS.md` : un gabarit rempli par carte. Rédigés le
03/09/2026. Auteur du pack : **Rainy**.

**Deux sets** : `Lady Sif` (ls001a-ls012) et `Lady Sif Nemesis` (ls013-ls017).
Seul pack de la vague 0 avec un set némésis complet.

**Preuves communes**, citées une fois :

- **Étape 7, substitution** : `substituer_pack.py .game-src 42100 ls0` →
  **18/18 cartes prouvées**. Sur les **31 cas, 30 tombent au rouge** quand le
  module de leur carte disparaît (passe du 03/09/2026, après l'ajout des 5 cas
  manquants). Le trente-et-unième est **assumé non sujet** et documenté :
  voir `ls002`.
- **Étape 8, autoplay** : **32 parties** (Rhino et Klaw, normal et expert,
  profil équilibré, 8 graines). **Grep exhaustif : 0 erreur sur les 32
  journaux**, et **0 partie bloquée** — après deux correctifs, voir §Bilan :
  5 blocages au premier jet, 3 après la simplification de `ls001a`, 0 après le
  correctif de l'empreinte du pilote. 3 victoires sur 32 : 38 % contre Rhino
  en expert, 0 % ailleurs. 5,5 rounds tenus en moyenne, 16 fins sur « The Main
  Scheme was Completed » contre 13 éliminations — Lady Sif meurt de la menace,
  pas des coups, ce qui est cohérent avec un CTR 1. Les 18 cartes apparaissent
  dans les journaux : `ls001a` **4706** occurrences (Valiant Warrior part à
  chaque pouvoir de base, c'est la mécanique vedette), `ls002` 933, `ls006` 328,
  `ls015` 314, et 9 au minimum pour la plus rare (`ls017`).
- **Témoin** : le même autoplay relancé sur `hulk_rainy` après le correctif du
  pilote rend **exactement** les chiffres de la veille (0/8, 0/8, 4/8, 1/8,
  0 incident) : le correctif est un non-événement là où rien ne bloquait.
- **Étape 4, image** : `assets/pics/ls0*.jpg` pour les 18, découpées du zip
  `Lady Sif-20260902T073844Z-1-001.zip`.
- **Étape 1** : pack `lady_sif` en queue de `cards.json`, set
  `150. Custom (Lady Sif)` dans `sets_info.json`, préfixe `ls` mis à jour dans
  `tools/prefixes_fanmade.json`, checksums recalculés.
- `test_capacites.py [ls0]` : **31/31 cas verts**.
- `test_cards` : **5101 ok / 0 erreur** (5083 avant le pack, +18).
- **Étape 10 de PROCESSUS-HEROS** : contrôle « jamais une signature d'un autre
  héros dans un deck » relancé sur les **113 decks de départ** → **0 écart**,
  alors que le héros porte le nom de l'allié signature `06002` de Thor.
- `verifier_cartes_en_jeu` : « les 18 cartes de lady_sif portent ce que leur
  texte annonce » ; `verifier_appels_modules` : « tous les appels de lady_sif
  existent ».
- **Les 18 scans ont été relus un par un le 03/09/2026**, avant la première
  ligne de code, et les icônes de ressource vérifiées les unes contre les
  autres à l'intérieur du pack (leçon Lockjaw) : le poing rouge de `ls003`
  contre l'éclair jaune de `ls005` contre la molécule bleue de `ls007` contre
  l'étoile verte de `ls002`. Le relevé du dossier de préparation était exact
  sur les 18 cartes.

**Deux arbitrages de l'utilisateur**, tranchés le 03/09/2026 :

1. **`ls007`** « Heal 1 damage from Thor or Odinson » vise **tout** personnage
   amical en jeu portant l'un de ces deux noms, **y compris chez un autre
   joueur** — la lecture la plus large des trois proposées, le texte ne disant
   pas « you control ».
2. **`ls014`** « If you cannot » se déclenche **dès que le moteur n'a posé
   aucun défenseur**, vérifié a posteriori sur `message.defender`, et pas
   seulement quand aucun héros n'est en jeu.

**Une question ne s'est pas posée** : le dossier de préparation annonçait
`ls014` comme « aucun modèle identifié ». Le grep du 03/09 en a rendu quatre
(`48006` Bamf!, `56047`, `45031` Colossus, `dd003` Doombot).

**Le pack en une phrase** : les pouvoirs de base paient deux fois. CTR 1 et
ATQ 2 ne paient pas gros, mais le pack multiplie les occasions de s'en servir,
et chaque usage retire 1 menace (`ls001a`) puis pioche (`ls009`).

---

### ls001a : * Lady Sif (Hero)

- [x] Étape 2 : `04032` * Captain Marvel pour `AfterUnitUseBasicPower(Response,
      "You", op)` — chez elle `"This"`, parce qu'elle est ALLIÉE ; `hk003` /
      `an004` pour la cible portée par **l'abilité elle-même**
      (`.SetTarget(Scheme2, has_threat=True)`).
- [x] Étape 5 : mots-pièges : **« a basic power »** = les TROIS pouvoirs, donc
      `powers=None` — un cas de test dédié le prouve sur une ATTAQUE de base,
      pas seulement sur une menée ; **AUCUNE limite imprimée**, contrairement à
      `ls009` qui plafonne à une fois par phase sur un déclencheur presque
      identique ; **« from A SCHEME »** au choix ; le libellé `(thwart)`
      alimente Désorienté. Résultat : conforme.
- [x] Étape 6 : CTR 1 / ATQ 2 / DEF 2, MNG 5, 13 PV ; 1 menace retirée.
      Résultat : conforme.
- [x] Étape 7 : 1 capacité, **2 cas**.
- [x] Étape 8 : voir preuve commune.

> ⚠ **Correctif payé en autoplay, et invisible aux 26 cas de test.** La
> première version portait la cible dans un `ChooseAbilities` +
> `ForChoiceAbility` (montage de `hk010`), donc **deux questions au joueur pour
> un seul effet**. Le garde-fou anti-répétition du pilote
> (`MAX_REPETITIONS = 2`, autoplay.py:47) construit sa clé sur l'« id » LOCAL
> de l'option, qui repart à 1 à chaque étape d'une capacité en plusieurs
> temps : les deux questions épuisaient le MÊME compteur. Sur une Response qui
> part à CHAQUE pouvoir de base — deux à trois fois par round — le budget
> tombait dès le 5ᵉ round. **Mesure : 5 parties bloquées sur 32.** C'est
> exactement le défaut que le commentaire d'`autoplay.py` décrit à propos de
> Super Spy (`ag001b`). La cible est passée sur l'abilité : une question, un
> compteur. Le joueur choisit toujours sa manigance ; ce qui disparaît, c'est
> la question « veux-tu déclencher », qui n'existait pas sur la carte imprimée.

**Carte terminée : OUI**

---

### ls001b : * Lady Sif (AlterEgo)

- [x] Étape 2 : `ho011` / `vv009` pour `Faces.ReadyAll` ; `aa003` * Ebony pour
      une Action portée par la face alter-ego ; `aa001a` pour
      `.LimitOncePerRound()`.
- [x] Étape 5 : mots-pièges : le type imprimé est **`Action` nu**, pas
      `Alter-Ego Action` — sans conséquence ici, la carte EST la face civile,
      mais on écrit ce qui est imprimé ; **« a FRIENDLY ASGARD character »** →
      `"YouControlUnit"`, qui exclut Enchantress et Skurge, **tous deux
      ASGARD** dans le set némésis du pack ; `canbe_ready=True`, sans quoi
      l'action se proposerait pour ne rien faire (leçon du blocage Underling) ;
      **« once per ROUND »**, pas par phase. Résultat : conforme.
- [x] Étape 6 : REC 4, MNG 6, 13 PV. Résultat : conforme.
- [x] Étape 7 : 1 capacité, **1 cas** — et il redresse l'alter-ego LUI-MÊME,
      qui porte le trait ASGARD. C'est la cible la plus sûre à monter : l'allié
      `ls002` existe aussi dans le DECK, où `Puzzle.Exhaust` irait le chercher
      (piège ho009).
- [x] Étape 8 : voir preuve commune.

**Carte terminée : OUI**

---

### ls002 : * Thor (Odinson) (Ally)

- [x] Étape 2 : `hk002` * Black Widow pour le squelette « allié signature à
      Response [star] » ; `AfterUnitAttackEnd(Response, "This", op)` ; `50013`
      * Slingshot pour le choix d'un JOUEUR (`SetTarget("Players")` +
      `Players.ForEachTargets`).
- [x] Étape 5 : mots-pièges : **« After Thor ATTACKS »** — l'attaque suffit,
      aucun dégât requis, et ce n'est ni « attacks and damages » ni « attacks
      or engages » ; **« choose A PLAYER »** : n'importe lequel, pas le
      contrôleur, donc jamais écrit en dur ; **« each minion engaged »** : tous,
      sans choix, y compris celui que Thor vient de frapper ; le `[star]` est
      une capacité permanente, pas un boost ; CTR 1* et ATQ 2* sont du dégât
      conséquent lu dans `desc`. Résultat : conforme.
- [x] Étape 6 : coût 3 / 3 PV / CTR 1* / ATQ 2*, ressource wild. Résultat :
      conforme.
- [x] Étape 7 : **1 capacité, 1 cas sujet**, plus 1 cas de non-régression.
      Le cas sujet est celui de la Response : ⚠ Sandman porte Toughness, c'est
      donc l'ABSENCE du statut Tenace qui prouve le dégât, pas un compteur de
      PV.
- [x] Étape 8 : voir preuve commune.

> ⚠ **Homonyme** : `25013` * Thor: Odinson porte le même nom ET le même
> sous-titre, mais une capacité totalement différente. Ne pas copier son
> module. Cinq autres « Thor » existent dans la base.

> ⚠ **`CanPlayThisAllyCard()` a été RETIRÉ le 03/09/2026, et c'est la mesure
> qui l'a décidé.** Le squelette de `hk002` en portait un, recopié par
> habitude. Le cas écrit pour le prouver est resté **vert sans le module** :
> l'allié entre en jeu tout seul. Vérification dans la foulée sur tout le
> dépôt : **420 alliés sur 453 ne l'appellent pas**, dont `aa019` * Wiccan, la
> carte de référence de la Response ci-dessus. La fabrique ne sert qu'aux
> chemins où l'allié est joué HORS de son tour, depuis une fenêtre
> d'interruption (`dd003` Doombot, `45031` * Colossus) : c'est là que le
> commentaire du moteur « Without this, this ally cannot be play » s'applique.
> Une ligne morte de moins, un écart de moins, et le cas reste en place comme
> garde de non-régression.

**Carte terminée : OUI**

---

### ls003 : Impale (Event, ×2)

- [x] Étape 2 : `01053` Relentless Assault pour l'événement d'attaque portant
      un mot-clé par `AttackProperty` ; `hk003` / `08013` pour le choix à deux
      branches.
- [x] Étape 5 : mots-pièges : **« either ... or »** — les deux branches sont
      EXCLUSIVES, jamais un `AttackProperty(overkill=True, piercing=True)` ; le
      choix se fait AVANT de connaître le résultat ; les 6 dégâts sont UNE
      attaque, donc une seule Riposte ; aucun autre mot-clé imprimé ; libellé
      `(attack)`. Résultat : conforme.
- [x] Étape 6 : coût 3, ressource physique ; 6 dégâts. Résultat : conforme.
- [x] Étape 7 : 1 capacité, **1 cas**, avec `choisir_option` pour forcer la
      branche Déferlement — sans elle, le pilote prend toujours la première.
- [x] Étape 8 : voir preuve commune.

**Carte terminée : OUI**

---

### ls004 : Lead The Charge (Event, ×3)

- [x] Étape 2 : **`bw024` Strong as Silk** (même auteur), seule autre carte du
      dépôt à imprimer « makes a basic attack without exhausting », et dont le
      commentaire pose la règle : `BasicAttack` n'incline rien, c'est l'ACTION
      de base du joueur qui incline d'ordinaire. `GainUntilRoundEnd(attack=1)`
      de la même carte.
- [x] Étape 5 : mots-pièges : **« LADY SIF makes »**, la face héros nommément ;
      **« without exhausting »** → ne rien incliner, et le cas de test l'exige
      (`pret: ["ls001a"]`) ; **« ANOTHER friendly character »** → exclusion
      explicite du héros, sans quoi la carte se donnerait le bonus à elle-même ;
      **« until the end of the ROUND »** ; le +1 ATQ tombe APRÈS l'attaque, il
      ne la renforce pas. Résultat : conforme.
- [x] Étape 6 : coût 1, ressource physique ; +1 ATQ. Résultat : conforme.
- [x] Étape 7 : 1 capacité, **1 cas** qui vérifie les trois effets d'un coup :
      dégâts, héros resté prêt, +1 ATQ sur Thor.
- [x] Étape 8 : voir preuve commune.

**Carte terminée : OUI**

---

### ls005 : To Arms! (Event)

- [x] Étape 2 : `ag005` Parting Shots pour `ChangeToForm(Hero, effect)` ;
      `50134` / `ho010` pour « you may spend 1 resource »
      (`MayChooseOneAbility` + `ForChoiceAbilityWithCost`) ; **`an001b`
      * Aldrif Odinsdottir** et `ok001b` pour la fouille
      `include_player_deck=True, include_discard_pile=True`.
- [x] Étape 5 : mots-pièges : **« You MAY spend »** — facultatif, un
      `SetCostFunc` en ferait un coût obligatoire et rendrait la carte
      injouable sans ressource ; **« ready YOUR HERO »** relu APRÈS la bascule ;
      **« a WEAPON UPGRADE »** — le TYPE compte, `an001b` cherche une « WEAPON
      card » sans type ; **« deck AND discard pile »** — le modèle d'origine
      `01040b` T'Challa ne fouille QUE le deck, le copier aurait tu la moitié de
      la phrase ; « Shuffle your deck » est le comportement par défaut de
      `Search`. Résultat : conforme.
- [x] Étape 6 : coût 0, ressource énergie ; 1 ressource facultative.
      Résultat : conforme.
- [x] Étape 7 : 2 capacités, **2 cas** — et le second place l'arme dans la
      DÉFAUSSE, pas dans le deck : c'est lui qui prouve la moitié de phrase que
      le modèle d'origine n'a pas.
- [x] Étape 8 : voir preuve commune.

> ⚠ **Correctif préventif du 03/09/2026** : `Player.GetHero()` lève un
> `assert` hors forme de héros (`player_get.py:208`) et le moteur avale
> l'exception. L'appel a été gardé par `IsHero()`, sans quoi un effet adverse
> qui empêche le changement de forme (`vv011` Grounded, `02048` All Tied Up)
> ferait échouer la carte **en silence**. Le défaut a été payé pour de bon sur
> `ls014`, dans le même pack.

**Carte terminée : OUI**

---

### ls006 : Valiant Defense (Event, ×3)

- [x] Étape 2 : **`25011` Shieldmaiden** (pack valk), jumeau du montage :
      `WhenUnitBeingAttack(HeroInterrupt, ...)` + `GainForThisActive(...,
      message.would_atk_message, defense=N)` + `DeclareDefender` ; `01013`
      Photonic Blast pour « paid using a [energy] resource » ; `dd003` Doombot,
      dont le commentaire écrit noir sur blanc que **`DeclareDefender`
      n'incline pas**.
- [x] Étape 5 : mots-pièges : **« using A [energy] »** → `HasColor`, jamais
      `OnlyHasColor` ; **« +2 DEF INSTEAD »** — 2 ou 1, jamais 3 ; **« for THIS
      ATTACK »** → `GainForThisActive` borné au message d'attaque, surtout pas
      `GainUntilRoundEnd` ; **« When an ENEMY attacks »** : vilain et sbires.
      Résultat : conforme.
- [x] Étape 6 : coût 1, ressource énergie ; +1 DEF, +2 si payée en énergie.
      Résultat : conforme.
- [x] Étape 7 : 1 capacité, **1 cas**. ⚠ **Le héros est incliné à la mise en
      place**, et c'est ce qui rend le cas SUJET : au premier passage le pilote
      défendait normalement, la carte n'était jamais jouée, et le cas passait
      au vert pour la mauvaise raison. ⚠ **Limite assumée** : la branche +2 DEF
      n'est PAS séparable contre Rhino étape 1 (ATQ 2) — les deux valeurs
      ramènent à 0 dégât. Il faudrait un ennemi à ATQ 4.
- [x] Étape 8 : voir preuve commune.

**Carte terminée : OUI**

---

### ls007 : * Sif's Chambers (Support)

- [x] Étape 2 : `aa003` * Ebony pour le squelette « soutien + Alter-Ego Action
      payée par `CostFunc.Exhaust("This")` » ; `38007` Energy Transfer pour
      `HealthUnits` ; `aa009` * The Witches' Road pour `AskChooseFaces` sur la
      défausse + `Faces.ShuffleAllTo`.
- [x] Étape 5 : mots-pièges : le `->` **ne couvre que le premier soin** — les
      deux phrases suivantes ne sont ni des coûts ni des conditions ; **« heal
      1 damage from LADY SIF »** : l'IDENTITÉ, via `GetIdentity()` et non un
      `CardFinder(name=...)`, l'allié officiel `06002` portant le même nom ;
      **« a LADY SIF card »** = une carte du **SET**, pas une carte de ce NOM,
      d'où `CardFinder(set_name="Lady Sif")` ; **« in YOUR discard pile »**, pas
      la défausse rencontre. Résultat : conforme.
- [x] Étape 6 : coût 1, ressource mentale ; 1 + 1 soin, 1 carte remélangée.
      Résultat : conforme.
- [x] Étape 7 : 1 capacité, **1 cas** qui vérifie les trois effets d'un coup.
- [x] Étape 8 : voir preuve commune.

> ⚠ **Arbitrage n° 1 de l'utilisateur** (voir en tête). « Thor or Odinson »
> vise tout personnage amical en jeu portant l'un des deux noms, même chez un
> autre joueur : les Thor officiels (`13011`, `25013`, `59020`, la face héros
> `06001a`) et `ra002` * Odinson sont donc des cibles légales. En solo avec le
> deck livré, la seule cible possible reste `ls002`.

**Carte terminée : OUI**

---

### ls008 : * Sif's Steed (Support)

- [x] Étape 2 : **`vv009` Insubstantial Flight** (même auteur, veille du
      portage) : **aucune fabrique n'enveloppe `Message.AfterCardExhausted`**,
      on construit l'`Ability` à la main, montage établi du dépôt (cd008,
      aa001b, dt009, gb001), avec le filtre
      `Condition.CheckWhichCard("YourHero", message.trigger, effect)` ; `ho011`
      * Goblin Glider pour la seconde capacité.
- [x] Étape 5 : mots-pièges : **« After Lady Sif EXHAUSTS »** sans complément —
      n'importe quel épuisement, y compris un coût payé par une autre carte, on
      ne filtre donc pas sur le pouvoir ; **« LADY SIF »** est porté par les
      deux faces, mais les deux capacités sont `Hero...`, d'où le filtre
      `"YourHero"` ; **aucune boucle possible** — redresser n'émet pas
      `AfterCardExhausted`, et le coût porte sur le SOUTIEN, écarté par le
      filtre. Résultat : conforme.
- [x] Étape 6 : coût 3, ressource énergie. Résultat : conforme.
- [x] Étape 7 : 2 capacités, **2 cas**. ⚠ Dans le second, **le héros est
      incliné AVANT que le soutien n'entre en jeu** : sinon c'est la Response
      qui tire et le cas ne prouve plus rien sur l'Action.
- [x] Étape 8 : voir preuve commune.

**Carte terminée : OUI**

---

### ls009 : * Sif's Crest (Upgrade)

- [x] Étape 2 : `05023` Endurance / `hk011` pour `GiveKeywordToAttached("You",
      health=2)` ; `04032` pour la famille « pouvoir de base », ici en version
      INTERRUPTION (`WhenUnitUseBasicPower`, friend.py:339) et non RESPONSE
      (`AfterUnitUseBasicPower`, friend.py:373) ; `aa001a` pour
      `.LimitOncePerPhase()`.
- [x] Étape 5 : mots-pièges : **l'écart avec `ls001a` est imprimé** — « When »
      contre « After », et une limite par phase contre aucune limite ;
      l'Interruption résout AVANT le pouvoir, donc la carte piochée peut payer
      l'attaque qui suit ; **« YOU get +2 hit points »** = l'identité, donc les
      DEUX faces (piège an002) ; **« Hero Interrupt »** : rien en forme civile,
      alors même que les +2 PV valent dans les deux. Résultat : conforme.
- [x] Étape 6 : coût 3, ressource mentale ; +2 PV (13 → 15), 1 carte.
      Résultat : conforme.
- [x] Étape 7 : 2 capacités, **2 cas** — et celui des PV est monté en forme
      CIVILE, la seule où une écriture `Hero` ne donnerait rien.
- [x] Étape 8 : voir preuve commune.

**Carte terminée : OUI**

---

### ls010 : * Sif's Spear (Upgrade)

- [x] Étape 2 : **`03009` * Captain America's Shield**, jumeau exact au nom
      près : `GiveKeywordToAttached(<cible>, defense=1, retaliate=1)`, et rien
      d'autre.
- [x] Étape 5 : mots-pièges : **`Restricted` est une base automatique**
      (`desc.Restricted`), aucun module — la recoder ferait compter la carte
      deux fois dans la limite ; **`retaliate 1`** se donne par le paramètre de
      la fabrique, pas par un module ; **« WHILE IN HERO FORM »** rendu par le
      TYPE de face (`Hero`) et non par le nom, les deux faces s'appelant
      « Lady Sif » et l'allié officiel `06002` aussi ; `"You"` donnerait le
      bonus à l'alter-ego, qui n'a pas de DEF (piège an002). Résultat :
      conforme.
- [x] Étape 6 : coût 1, ressource physique ; +1 DEF (2 → 3), riposte 1.
      Résultat : conforme.
- [x] Étape 7 : 1 capacité continue, **1 cas**.
- [x] Étape 8 : voir preuve commune.

**Carte terminée : OUI**

---

### ls011 : * Sif's Sword (Upgrade)

- [x] Étape 2 : `03009` / `ls010` pour `GiveKeywordToAttached(Hero, attack=1)` ;
      **`27078` "Now We're Angry!"** pour `UnitAttackGainKeyword(..., piercing=
      True)`.
- [x] Étape 5 : mots-pièges : **« BASIC attacks »** seulement —
      `is_basic_attack=True` est indispensable, sans lui Impale et Lead The
      Charge perforeraient aussi ; ⚠ mais Lead The Charge fait faire une
      attaque de BASE, et celle-là gagne bien le piercing ; **« WHILE IN HERO
      FORM » est répété DEUX fois** sur la carte, il porte sur les deux
      moitiés ; l'attaquant est borné par `"You"`, qui vise NOTRE identité.
      Résultat : conforme.
- [x] Étape 6 : coût 2, ressource physique ; +1 ATQ (2 → 3). Résultat :
      conforme.
- [x] Étape 7 : 2 capacités, **1 cas** qui les prouve toutes deux : Sandman
      porte Toughness, donc sans Perforation son statut Tenace absorberait tout
      et il prendrait 0. Il encaisse 3.
- [x] Étape 8 : voir preuve commune.

**Carte terminée : OUI**

---

### ls012 : Unrequited Love (Obligation)

- [x] Étape 2 : **`an010` Banished from Asgard**, squelette exact :
      `WhenThisObligationGiveToYou` + `YouMayFlipToYourAlterEgoForm` +
      `ChooseAbilities` + `Faces.DiscardAll` ; `05015` / `01083` pour
      `Faces.GiveStatus`.
- [x] Étape 5 : mots-pièges : **« You MAY flip »** et non « must » — le mot
      compte, `vp011` One Too Many Voices dit « must » et force la bascule par
      un autre chemin ; **« Stun LADY SIF »** : l'identité, quelle que soit la
      forme ; **« Stun OR confuse Thor »** : un choix, pas les deux ; **« If
      you cannot »** est réellement atteignable (Thor n'est pas en jeu la
      plupart du temps) et se lit sur le **RETOUR** de `GiveStatus`, ce qui
      couvre aussi le cas d'un Thor qui ne peut recevoir ni l'un ni l'autre ;
      « Discard this obligation » est INCONDITIONNEL. Résultat : conforme.
- [x] Étape 6 : 2 icônes de boost, `GiveTo` = « Lady Sif ». Résultat :
      conforme.
- [x] Étape 7 : 1 capacité, **2 cas** — le nominal sans Thor, et le
      **contre-cas** avec Thor en jeu, qui prouve que la branche de repli teste
      bien le retour de `GiveStatus` et pas la seule présence de l'allié.
- [x] Étape 8 : voir preuve commune.

**Carte terminée : OUI**

---

### ls013 : Captivating Wiles (SideScheme, némésis 1/5)

- [x] Étape 2 : `WhenPlayerPhaseBegin(ForcedInterrupt, op)` (turn_phase.py:163) ;
      `Worlds.GetFirstPlayer(effect)` (worlds.py:599) ; `50134` / `ho015` pour
      `PlaceThreatOnSchemes("MainScheme", 2, effect)` ; `an013` / `ho017` pour
      `WhenCardBecomeBoost`.
- [x] Étape 5 : mots-pièges : **« the FIRST player's identity »** — jamais
      `effect.GetInitiator()` ; **« When the player phase begins »** est une
      INTERRUPTION, donc l'identité est inclinée avant que le joueur ne joue,
      et il perd son action de base ; `Forced`, donc la capacité se répète à
      CHAQUE round ; la menace de départ `3 [per_hero]` est une base automatique
      (`desc.StartingThreat = "3*"`) ; le `[star] Boost` est un effet de boost,
      pas une capacité permanente. Résultat : conforme.
- [x] Étape 6 : menace de départ 3 par joueur, 1 icône de boost, 2 + 2 menaces.
      Résultat : conforme.
- [x] Étape 7 : 2 capacités, **2 cas**. Le déclencheur de phase est hors de
      portée de l'API Puzzle : un vérificateur maison renvoie dans le monde le
      message exact émis par `world.py:792`, même sonde que `vv010`. ⚠ Le cas
      du Boost lit **4** menaces et non 2, et c'est correct : `Puzzle.Boost`
      fait ACTIVER le vilain (puzzle.py:337), donc 1 (MNG de Rhino) + 1 (icône
      de boost) + 2 (effet `[star] Boost`).
- [x] Étape 8 : voir preuve commune.

**Carte terminée : OUI**

---

### ls014 : * Enchantress (Minion, némésis 2/5)

- [x] Étape 2 : le dossier de préparation annonçait « aucun modèle identifié » ;
      le grep du 03/09 en a rendu quatre. **`48006` Bamf!** — dont le
      commentaire donne la définition officielle : « declaring X the defender
      without exhausting encompasses the character making a basic defense and
      using their DEF to reduce damage dealt » ; `56047` "I Can Do This All
      Day" ; `45031` * Colossus ; **`dd003` Doombot**, qui pose la règle
      **`DeclareDefender` n'incline pas de lui-même**.
- [x] Étape 5 : mots-pièges : **« the ENGAGED hero »** et non l'attaquant — à
      deux joueurs, un allié d'un autre joueur peut la frapper et c'est quand
      même SON joueur engagé qui défend ; **« cancel that attack ...
      instead »** : les deux branches sont exclusives ; **« (Limit once per
      phase.) »** ; `ELITE` est un TRAIT, pas un mot-clé. Résultat : conforme.
- [x] Étape 6 : MNG 3 / ATQ 2 / 5 PV, 3 icônes de boost, 2 menaces en repli.
      Résultat : conforme.
- [x] Étape 7 : 1 capacité, **2 cas** — le nominal et la branche de repli.
      Le témoin du cas nominal est indirect mais net : **une défense de base
      EST un pouvoir de base**, donc Valiant Warrior tire une SECONDE fois et
      la principale tombe de 5 à 3 au lieu de 4.
- [x] Étape 8 : voir preuve commune.

> ⚠ **Arbitrage n° 2 de l'utilisateur** (voir en tête), et **la carte la plus
> chère du pack en temps de mise au point : trois passes de la batterie.**
> 1. `Player.GetHero()` lève un `assert` hors forme de héros et le moteur
>    **avale l'exception** : la capacité tirait bien, son corps mourait à la
>    deuxième ligne, et rien ne l'écrivait nulle part. Trouvé en traçant le
>    déclenchement à la main.
> 2. `CancelThisAttack` n'est définie que sur `WhenUnitWouldAttack`
>    (`sender_damage.py:181`), **pas** sur `WhenUnitBeingAttack` :
>    `AttributeError`, avalée elle aussi.
> 3. Même reprise sur `message.would_atk_message`, l'annulation arrive **trop
>    tard** depuis `WhenUnitBeingAttack` : les menaces tombaient, mais
>    Enchantress encaissait quand même.
> La fenêtre correcte est `WhenUnitWouldAttack` avec `attack_targets="This"`,
> celle qu'emploient `48006` et `56047`. **Aucun des trois défauts n'aurait été
> visible en lecture** : seuls les deux cas de test les ont sortis.

**Carte terminée : OUI**

---

### ls015 : * Skurge (Minion, némésis 3/5)

- [x] Étape 2 : **`24026` * Crossfire**, jumeau du montage —
      `WhenUnitWouldAttack(ForcedInterrupt, "This", op)` + `Filter.One(...,
      fewest_remaining_hp=True)` + `message.ReplaceTarget`. Seuls les mots-clés
      gagnés diffèrent : overkill + ranged là-bas, overkill + **piercing** ici.
- [x] Étape 5 : mots-pièges : **écart imprimé avec Crossfire** — « the
      character **YOU** control » borne au joueur engagé, alors que le module de
      Crossfire balaie toute la table (`GetOnFieldFriendlyCharacters`) ; en solo
      les deux écritures donnent le même résultat, à deux joueurs non ;
      **« fewest REMAINING hit points »** : les PV restants ; **« overkill AND
      piercing »** : les deux, contrairement au « either ... or » de `ls003` ;
      l'étoile de l'ATQ renvoie à la capacité `[star]`, ce n'est pas du dégât
      conséquent ; sans allié, le Boost ne fait rien et le texte ne prévoit
      aucun repli. Résultat : conforme.
- [x] Étape 6 : MNG 1 / ATQ 3* / 5 PV, 1 icône de boost. Résultat : conforme.
- [x] Étape 7 : 2 capacités, **2 cas**. ⚠ Le héros est incliné à la mise en
      place du premier : sans cela il se déclarait DÉFENSEUR à la place de
      Thor, encaissait 1 dégât, et la redirection n'était pas prouvée.
- [x] Étape 8 : voir preuve commune.

> ⚠ **Deux bases automatiques, aucun script** : `Teamwork (ASGARD)` →
> `desc.Teamwork`, et `Toughness` → `desc.Toughness`. Les recoder ferait
> **doubler** leur effet — pour Teamwork, le sbire s'activerait deux fois.
> La fiche `docs/reference/mots-cles/teamwork.md` a été **écrite pour ce
> pack** : le mot-clé est porté par 31 cartes officielles et le moteur le
> connaît depuis toujours, mais aucune fiche n'existait.

**Carte terminée : OUI**

---

### ls016 : Hypnotic Suggestion (Attachment, némésis 4/5)

- [x] Étape 2 : **`55008b` Trance of Greed** (pack enchantress), jumeau au
      repli près : même `WhenInYourPlayTurn(ForcedAction)` +
      `CostFunc.Exhaust("This")`, et même couple `player.DrawUp(1, effect)` /
      `player.PlayCardsLikeInTurn(faces, effect)`, dont le RETOUR dit si la
      carte a pu être jouée ; `02048` All Tied Up pour
      `AttachToFaceWhenPutIntoPlay("YourIdentity")` et
      `PlayerActionToDiscardThis`.
- [x] Étape 5 : mots-pièges : `Forced Action` — la phase du joueur ne peut pas
      se terminer tant qu'elle est possible, le joueur ne peut donc pas
      l'ignorer ; **« then play that card (paying its costs) »** — le joueur
      PAIE, donc pas d'`ignore_resources_cost`, l'inverse exact de `dd003`
      Doombot qui, lui, avait déjà payé ; **« If you cannot »** lu sur le
      RETOUR, cas très atteignable ; l'Action d'alter ego a **deux parties de
      coût** — incliner la carte ET dépenser un mental (piège `wd005`).
      Résultat : conforme.
- [x] Étape 6 : 1 icône de boost, 2 menaces en repli, coût [mental].
      Résultat : conforme.
- [x] Étape 7 : 3 capacités, **3 cas**. L'Action forcée, montée pour que « If
      you cannot » tire (deck réduit à `ls003` coût 3, main à 2 mentales).
      L'attachement (ajout du 03/09/2026), prouvé par un **vérificateur maison**
      qui lit `GetBindFace()` : « en jeu » ne dit rien de l'hôte, une carte
      accrochée au vilain serait « en jeu » elle aussi. L'Action d'alter ego
      enfin, dont le coût a DEUX parties (incliner ET dépenser un mental) et
      qui exige un `Puzzle.Ready` préalable, l'Action forcée de la même carte
      l'inclinant dès son entrée en jeu.
- [x] Étape 8 : voir preuve commune.

> ⚠ **Homonyme** : `ag014` Hypnotic Suggestion est une TRAITRISE du pack maison
> agent_13. Deux cartes distinctes de même nom, dans deux packs maison.

**Carte terminée : OUI**

---

### ls017 : Love Concoction (Attachment, némésis 5/5)

- [x] Étape 2 : `02048` All Tied Up pour l'attachement et
      `PlayerActionToDiscardThis` ; **`02035` Intimidation** pour
      `Faces.GiveFacedownBoostCards` ; `27078` / `ho017` pour
      `WhenCardBecomeBoost("This", RevealThisCard)`, le helper existant déjà
      dans `cards/pack/__init__.py`.
- [x] Étape 5 : mots-pièges : le coût est **double des deux côtés** — incliner
      ET donner une carte de boost au vilain ; **« ready your identity » n'est
      PAS « discard this card »** : la première capacité laisse l'attachement en
      place, tour après tour, et c'est tout le sens du trait TEMPTATION ; comme
      la capacité forcée incline la carte, l'Action d'alter ego qui l'incline
      aussi n'est plus payable ce round-là — pour s'en débarrasser il faut la
      prendre EN PREMIER ; `desc.Boost = "0"`, la carte n'ajoute rien à
      l'activation. Résultat : conforme.
- [x] Étape 6 : aucune icône chiffrée, une icône `[star]`. Résultat : conforme.
- [x] Étape 7 : 4 capacités, **3 cas**. Le `[star] Boost`, qui est le seul
      chemin d'entrée en jeu de la carte. L'Action forcée (ajout du
      03/09/2026) : l'identité inclinée à la mise en place se redresse, et la
      carte RESTE en jeu. L'Action d'alter ego : même coût double, mais la
      carte PART. Les deux ensemble rendent le dilemme imprimé, puisqu'en
      partie réelle la seconde n'est prenable qu'AVANT la première.
- [x] Étape 8 : voir preuve commune.

**Carte terminée : OUI**

---

## Bilan

**18 cartes, 18 « Carte terminée : OUI ».**

### Ce que ce portage a appris, et que la lecture seule ne donnait pas

**Le moteur avale les exceptions des modules de cartes.** Trois défauts de
`ls014` — un `assert` de `GetHero()`, un `AttributeError` sur
`CancelThisAttack`, puis une fenêtre trop tardive — se sont tous présentés de
la même façon : **la carte ne fait rien, et rien ne l'écrit nulle part**. Ni
`test_cards`, ni `verifier_appels_modules`, ni `verifier_cartes_en_jeu` ne les
voient : la carte se construit, ses appels existent, et elle porte bien ce que
son texte annonce. **Seul un cas de test qui compte un nombre les sort.**

Deux conséquences pratiques :

1. **`Player.GetHero()` ne s'appelle jamais nu.** Il lève un `assert` hors
   forme de héros (`player_get.py:208`). Le garder par `IsHero()` est gratuit ;
   ne pas le garder coûte une carte morte en silence. Vérifié sur tout le pack
   au passage : `ls004` et `ls008` sont des `HeroAction`, donc sûrs par
   construction ; `ls005` a été gardé par précaution.
2. **Avant d'écrire une méthode sur un message, vérifier dans quelle CLASSE de
   message elle est définie.** `CancelThisAttack` vit sur
   `WhenUnitWouldAttack`, pas sur `WhenUnitBeingAttack`, et les deux fenêtres
   se ressemblent assez pour qu'on les confonde. `verifier_appels_modules` ne
   peut pas l'attraper : il vérifie que le NOM existe quelque part, pas sur
   quel type.

**Le harnais aussi ment quand on lit son verdict trop vite.** Deux cas
passaient au vert ou à l'orange pour la mauvaise raison : `ls006`, parce que le
pilote défendait normalement au lieu de jouer la carte, et `ls015`, parce que
le héros se déclarait défenseur à la place de Thor. Dans les deux, **incliner
le héros à la mise en place** est ce qui a rendu le cas sujet. Et
`Puzzle.Attack(x, y)` fait **défendre** `y` : passer une cible en second
argument ajoutait une défense de base fantôme, donc un déclenchement de plus
de Valiant Warrior.

### Le troisième défaut : celui que seul l'autoplay pouvait voir

Les 26 cas de test étaient verts, la substitution 26/26, `test_cards` sans
erreur — et le pack bloquait **5 parties sur 32**. La question fautive était
toujours la même : `Valiant_Warrior(id=3, plage=[1, 1])`, une question
**forcée** à laquelle le pilote ne pouvait plus répondre.

Deux causes, découvertes l'une après l'autre :

1. **`ls001a` posait DEUX questions pour un seul effet** (`ChooseAbilities` +
   `ForChoiceAbility`, le montage de `hk010`). Le compteur anti-répétition du
   pilote se construit sur l'« id » LOCAL de l'option, qui repart à 1 à chaque
   étape : les deux questions épuisaient le même budget. Ramenée à une seule
   question, la carte est passée de 5 blocages à 3.
2. **L'empreinte de situation du pilote ignorait les manigances ANNEXES.**
   `menace_ratio` ne lit que la principale ; une capacité qui retire de la
   menace d'une annexe ne bougeait donc aucun des cinq termes de la clé, et
   deux déclenchements successifs partageaient la même situation alors que la
   partie avait bel et bien avancé. **Le même fichier avait déjà la bonne
   réponse** : l'empreinte de PROGRÈS du désistement, trente lignes plus bas,
   comptait les annexes depuis toujours. Les deux signatures ne regardaient
   pas le même monde. Alignées, on passe à **0 blocage**.

Le correctif de `tools/autoplay.py` est **strictement additif** — un terme de
plus ne peut que séparer des situations jusque-là confondues, jamais en
confondre de nouvelles — et le témoin `hulk_rainy` le confirme chiffre pour
chiffre.

**La leçon de méthode** : une capacité sans limite qui part plusieurs fois par
round est un cas de charge que les tests unitaires ne reproduisent pas. Un
`ChooseAbilities` imbriqué est gratuit sur une carte rare et coûteux sur une
carte fréquente : quand l'effet n'offre AUCUN choix de branche, la cible va sur
l'abilité.

### Reste à faire (écarts assumés, aucun bloquant)

- ~~Cinq capacités sans cas de test dédié~~ : **comblé le 03/09/2026** à la
  demande de l'utilisateur. Quatre ont leur cas sujet, vert du premier coup ;
  la cinquième, le `CanPlayThisAllyCard` de `ls002`, s'est révélée être une
  ligne morte et a été retirée,
  et la batterie passe de 26 à **31 cas**. Le relevé des journaux d'autoplay
  qui a motivé l'ajout mérite d'être gardé : `ls002` avait été jouée **67 fois**
  en 32 parties, mais **`ls016` et `ls017` ne sont JAMAIS entrées en jeu** —
  elles ne sortaient que comme cartes de boost. Ces deux-là n'étaient donc ni
  prouvées ni infirmées par quoi que ce soit avant ces cas.
- **La branche +2 DEF de `ls006`** n'est pas séparable de la branche +1 dans le
  scénario Rhino : il faudrait un ennemi à ATQ 4.
- **`desc.Nemesis`** a été posé sur `ls014` et `ls015`, ce que **40 sbires
  némésis OFFICIELS n'ont pas** (relevé le 03/09/2026 : `06029` Frost Giant,
  `45056` * S'ym, `49030` * Fabian Cortez…). Sans ce champ, `IsNemesis` rend
  False pour un sbire (`card_encounter.py:35`) et `01190` Shadow of the Past ne
  le met jamais en jeu. C'est un écart de DONNÉES officielles, pas du pack :
  signalé ici, non corrigé.
