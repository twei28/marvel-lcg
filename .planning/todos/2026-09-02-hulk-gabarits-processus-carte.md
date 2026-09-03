# PROCESSUS-CARTE.md — les 14 gabarits du pack HULK (set 148, `hk`)

Gate de `PROCESSUS-HEROS.md` : un gabarit rempli par carte. Rédigés le
02/09/2026. Auteur du pack : **Rainy**.

> ⚠ **Ce pack a été écrit deux fois.** Le 02/09/2026 vers 20 h 08, pendant la
> passe `substituer_pack.py`, la machine a planté : NTFS a rendu **six modules
> entièrement remplis d'octets nuls** (`hk005`, `hk006`, `hk009`, `hk011`,
> `hk012`, `hk013`, plus le `hk013.py.vrai` que l'outil de substitution venait
> de poser). Aucune sauvegarde n'a survécu — le `__pycache__` était nul lui
> aussi, et le pack n'était pas encore commité. Les six ont été **réécrits à
> partir de la batterie de tests**, qui, elle, était intacte : c'est elle qui a
> tenu lieu de spécification, avec le dossier de préparation
> `2026-09-02-prep-vague0-hulk.md` et les cartes de référence qu'il nomme.
> La leçon est écrite au §Bilan.

**Preuves communes**, citées une fois :

- **Étape 7, substitution** : `substituer_pack.py .game-src 31500 hk0` →
  **14/14 cartes prouvées**, et sur les **20 cas, 20 tombent au rouge** quand
  le module de leur carte disparaît (passe du 03/09/2026, après l'ajout des
  3 cas manquants). Aucun cas resté vert sans son module, aucune carte sans
  cas.
- **Étape 8, autoplay** : **32 parties** (Rhino et Klaw, normal et expert,
  profil équilibré, 8 graines). **Grep exhaustif : 0 erreur sur les 32
  journaux**, et **0 incident** compté par l'outil lui-même. 5 victoires sur
  32 : 50 % contre Rhino en expert, 12 % contre Rhino en normal, **0 % contre
  Klaw** dans les deux difficultés. 4,1 rounds tenus en moyenne, 26 fins sur
  « All players were eliminated ». Les 14 cartes apparaissent dans les
  journaux : `hk001a` **4787** occurrences (Anger part à chaque dégât subi,
  c'est la mécanique vedette du pack), `hk010` 301, `hk013` 195, `hk006` 198,
  `hk005` 167, et 23 au minimum pour la plus rare (`hk007`).
- **Étape 4, image** : `assets/pics/hk0*.jpg` pour les 14.
- **Étape 1** : pack `hulk_rainy` en queue de `cards.json`, set
  `148. Custom (Hulk)` dans `sets_info.json`, préfixe `hk` déclaré dans
  `tools/prefixes_fanmade.json`, checksums refaits (`recalculer_checksums.py`
  → « inchangé » à la relecture du 02/09 au soir).
- `test_capacites.py [hk0]` : **20/20 cas verts**, dont les 8 cas des six
  modules réécrits et les 3 cas ajoutés le 03/09/2026.
- **Étape 10 de PROCESSUS-HEROS** : contrôle « jamais une signature d'un autre
  héros dans un deck » relancé sur `deck/starter/hulk_rainy.json` →
  **aucun écart**, alors que le pack porte deux homonymes de cartes du Hulk
  OFFICIEL (voir hk004 et hk012).

**Le pack en une phrase** : encaisser paie, et la couleur du paiement compte.
CTR 0 en forme héros, donc toute la menée passe par Bruce Banner et par
hk009 The Other Guy.

---

### hk001a : * Hulk (Hero)

- [x] Étape 2 : `aa001a` * Agatha Harkness (« Power Absorption ») pour
      `AfterUnitTookDamage(Response, "You", op)` sur une face héros ;
      `08013` Stealth Strike pour `ChooseAbilities` + `ForChoiceAbility`.
- [x] Étape 5 : mots-pièges : **aucun filtre `is_from_attack`** — le texte dit
      « takes damage », pas « from an attack », donc une traîtrise, un dégât
      indirect et le dégât que Hulk s'inflige lui-même déclenchent Anger ;
      c'est l'écart imprimé avec hk010, qui, lui, filtre. **« to AN enemy »** :
      n'importe lequel, pas « that enemy ». Le dégât rendu n'est **pas une
      attaque** (ni overkill, ni riposte adverse). Résultat : conforme.
- [x] Étape 6 : CTR 0 / ATQ 2 / DEF 3, MNG 4, 15 PV ; 1 dégât rendu.
      Résultat : conforme.
- [x] Étape 7 : 1 capacité, **1 cas**.
- [x] Étape 8 : voir preuve commune.

**Carte terminée : OUI**

---

### hk001b : * Bruce Banner (AlterEgo)

- [x] Étape 2 : **`52019` Ready for a Fight** (pack `silk`), jumeau MOT POUR
      MOT : « Interrupt: When an enemy would scheme, ... → change to hero form.
      That enemy attacks you instead. » Seul le coût diffère.
- [x] Étape 5 : mots-pièges : **l'ORDRE** — on change de forme AVANT que
      l'attaque ne parte, sinon Bruce Banner encaisse en forme civile, et c'est
      tout l'intérêt de la carte ; **« spend a [physical] resource »** est un
      COÛT (`SetCost(Cost("R"))`), à ne pas confondre avec le « if you paid
      using a [physical] » de hk006, qui est une condition d'EFFET ;
      **« an ENEMY »** : vilain et sbires. Résultat : conforme.
- [x] Étape 6 : REC 4, MNG 6, 15 PV ; coût 1 ressource physique.
      Résultat : conforme.
- [x] Étape 7 : 1 capacité, **1 cas**.
- [x] Étape 8 : voir preuve commune.

> ⚠ **Correction de la préparation** : le dossier de pré-portage annonçait
> « aucun modèle identifié, seul vrai point d'attention du pack ». C'était
> faux : le grep du 02/09 a rendu `52019` immédiatement. La fiche de prépa a
> été corrigée sur place (Q4 déclarée sans objet).

---

### hk002 : * Black Widow (Ally)

- [x] Étape 2 : `aa019` * Wiccan pour « After <allié> thwarts »
      (`AfterUnitAttackOrThwart` filtré sur le type du message) ; `ag005`
      Parting Shots pour `ChangeToForm(AlterEgo, effect)`.
- [x] Étape 5 : mots-pièges : **« from ANOTHER scheme »** → `exclude=` sur les
      manigances effectivement menées, sans quoi la carte se retirerait deux
      fois de la même ; le **`[star]`** de la Response est une capacité
      permanente, PAS une capacité de boost ; **« flip to YOUR alter-ego
      form »** : l'identité du joueur, pas l'alliée ; ATQ 1* et CTR 2* sont
      du dégât conséquent, lu nativement dans `desc`. Résultat : conforme.
- [x] Étape 6 : coût 3 / 3 PV / CTR 2* / ATQ 1*, ressource wild.
      Résultat : conforme.
- [x] Étape 7 : 2 capacités, **2 cas** (ajout du 03/09/2026) : la bascule de
      forme, et la Response de contre. Ce second cas est celui qui prouve le
      mot **« from ANOTHER scheme »** : Black Widow contre la principale de son
      CTR 2, et la Response doit se reporter sur l'annexe. Sans l'exclusion,
      elle retirerait deux fois de la même.
- [x] Étape 8 : voir preuve commune.

> ⚠ **Homonyme** : six « Black Widow » dans la base, dont l'alliée officielle
> `01075`, aux **stats différentes**. Deux cartes distinctes de même nom.

---

### hk003 : Brilliant Mind (Event, ×2)

- [x] Étape 2 : **`10004` Sub-Orbital Leap** (Hulk officiel) pour « using
      ONLY » → `OnlyHasColor` ; `08013` / `ho001a` pour le choix à deux
      branches.
- [x] Étape 5 : mots-pièges : **« using ONLY [mental] »** → `OnlyHasColor`, et
      surtout pas `HasColor` (hk006) ni le surpaiement (hk005) — trois
      tournures du même pack, trois lectures ; **un WILD compte comme mental**
      (`OnlyHasColor` convertit le vert, ce qui est la règle) ; **« from THAT
      scheme »** : la même manigance, on réutilise `effect.targets` sans
      reposer de sélecteur ; **« EITHER ... OR »** : un choix, pas les deux.
      Résultat : conforme.
- [x] Étape 6 : coût 2, ressource mentale ; 3 menaces, +2 si « only ».
      Résultat : conforme.
- [x] Étape 7 : 1 capacité, **2 cas** — le nominal ET le **contre-cas** payé
      en physique, qui prouve que le bonus ne part pas.
- [x] Étape 8 : voir preuve commune.

---

### hk004 : Hulk Smash (Event, ×2)

- [x] Étape 2 : `th010` It's Clobberin' Time! pour la suite d'attaques d'un
      même événement ; `08013` pour `SetLabel('attack').SetTarget(Enemy)`.
- [x] Étape 5 : mots-pièges : **« against the SAME target »** — la cible se
      choisit UNE FOIS, d'où l'écart volontaire avec th010, qui repose un
      sélecteur à chaque attaque ; **TROIS attaques distinctes**, pas une de 9
      (une Riposte se déclenche trois fois, un Tenace n'absorbe que la
      première) ; aucun mot-clé imprimé ; la cible peut mourir en route, les
      attaques restantes tombent dans le vide, ce qui est correct.
      Résultat : conforme.
- [x] Étape 6 : coût 3, ressource physique ; 3 × 3 dégâts. Résultat : conforme.
- [x] Étape 7 : 1 capacité, **1 cas** (9 dégâts minimum sur une cible unique).
- [x] Étape 8 : voir preuve commune.

> ⚠ **Homonyme de classe Hero** : `10003` Hulk Smash est une carte signature
> du HULK OFFICIEL. Documenté dans le `collision_note` du deck ; contrôle
> étape 10 relancé et vert.

---

### hk005 : Interception (Event, ×2) — **module réécrit après le plantage**

- [x] Étape 2 : `dz013` Velvet Sky / `09007` Protective Ward pour
      `CancelAllEffectsAndDiscardIt` ; `dt015` Preparation #2 pour
      `CostFunc.DealDamage(2, "YourHero")` ; `58005` Starstruck pour le
      surpaiement, transposé en `SurpaiementEnergieOuPhysique` (helper du set).
- [x] Étape 5 : mots-pièges : **« cancel ALL of its effects »** → niveau
      « All », et non le `CancelWhenRevealedEffect` d'an005, qui laisse passer
      les mots-clés (Surge compris) — leçon dz013, payée en partie réelle ;
      **pas de « you »** dans « when a treachery is revealed » → `"AnyPlayer"` ;
      **pas de « from the encounter deck »** → pas de `from_encounter` ;
      **« take 2 damage → »** est un coût, payé AVANT, et ces 2 dégâts
      déclenchent Anger ; **« If you OVERPAID »** : la carte coûte 0, donc tout
      paiement dépasse le coût, mais il doit contenir de l'énergie ou du
      physique — un mental seul ne retire aucune menace. Résultat : conforme.
- [x] Étape 6 : coût 0, ressource physique ; 2 dégâts subis, 2 menaces
      retirées. Résultat : conforme.
- [x] Étape 7 : 1 capacité, **1 cas** — et c'est le seul du pack qui exige
      `surpayer: True` dans le harnais, la carte coûtant 0.
- [x] Étape 8 : voir preuve commune.

> ⚠ **Piège du pack, payé le 02/09** : `SurpaiementEnergieOuPhysique` avait
> d'abord été défini dans le `__init__.py` du **pack**, pas du **set**. Les
> modules font `from . import *`, qui importe le `__init__` du SET : le
> `NameError` était avalé par le moteur, et la carte annulait bien la traîtrise
> mais ne retirait **jamais** ses 2 menaces. **Seul son cas de test l'a vu.**

---

### hk006 : Reckless Charge (Event, ×2) — **module réécrit après le plantage**

- [x] Étape 2 : **`01053` Relentless Assault**, même phrase imprimée pour la
      provenance du paiement → `HasColor("R")` → overkill porté par
      `AttackProperty` ; `dt015` pour `CostFunc.DealDamage(1, "YourHero")`.
- [x] Étape 5 : mots-pièges : **« Deal 1 damage to Hulk → »** est un COÛT, payé
      avant ; ce dégât **déclenche Anger**, donc la cible prend au moins 4 et
      non 3 — c'est voulu par le pack ; **« using A [physical] »** → `HasColor`
      et jamais `OnlyHasColor` ; **« this ATTACK gains overkill »** : overkill
      seulement, ni piercing ni ranged. Résultat : conforme.
- [x] Étape 6 : coût 1, ressource physique ; 1 dégât subi, 3 infligés.
      Résultat : conforme.
- [x] Étape 7 : 1 capacité, **1 cas** nominal (subst. 1/1). Le cas de hk007
      s'en sert en plus comme révélateur, mais il est compté chez hk007.
- [x] Étape 8 : voir preuve commune.

---

### hk007 : Natural Genius (Resource)

- [x] Étape 2 : **`10007` Limitless Strength**, la ressource du Hulk officiel,
      qui imprime la phrase MIROIR et se rend par `CheckThisCanDropPay(...,
      spend_this_only_in_hero_form=True)`. Le drapeau alter-ego existe dans la
      même signature (`resources.py:67`).
- [x] Étape 5 : mots-pièges : **« SPEND this card only in... »** restreint la
      DÉPENSE, pas la possession — la carte se pioche et se garde dans les deux
      formes ; **deux icônes imprimées** → `Resources("BB")`, la carte paie
      deux mentales, pas une. Résultat : conforme.
- [x] Étape 6 : aucune valeur de coût, RES `BB`. Résultat : conforme.
- [x] Étape 7 : 1 capacité, **1 cas**. ⚠ Le cas vérifie la **RESTRICTION**, pas
      la dépense : en forme héros, hk007 ne peut pas être dépensée, hk006 n'a
      alors aucune autre source de paiement, **Rhino ne prend rien** et hk007
      reste en main. Vérifier « hk006 est jouée » aurait été un faux vert.
- [x] Étape 8 : voir preuve commune.

---

### hk008 : Unnatural Strength (Resource)

- [x] Étape 2 : `10007` Limitless Strength, MÊME phrase au mot près. Seul le
      nombre d'icônes diffère : trois là-bas, **deux** ici (relevé sur le scan).
- [x] Étape 5 : mots-pièges : restriction de DÉPENSE, pas de pioche ; jumelle
      de hk007 — ensemble, les deux forcent le changement de forme pour
      dépenser sa main, ce qui alimente hk009. Résultat : conforme.
- [x] Étape 6 : aucune valeur de coût, RES `RR`. Résultat : conforme.
- [x] Étape 7 : 1 capacité, **1 cas**, miroir de celui de hk007 : en forme
      civile, hk008 n'est pas dépensable, hk003 ne part pas, **la menace ne
      bouge pas** et hk008 reste en main.
- [x] Étape 8 : voir preuve commune.

---

### hk009 : The Other Guy (Support) — **module réécrit après le plantage**

- [x] Étape 2 : `aa009` * The Witches' Road pour `AfterUnitChangeForm` ;
      `aa001a` pour `.LimitOncePerPhase()` ; hk001a / hk010 du même pack pour
      le choix de cible.
- [x] Étape 5 : mots-pièges : **la forme évaluée est celle d'APRÈS la
      bascule** — en passant de l'alter-ego au héros, c'est la branche HERO qui
      tire ; `to_form` est écrit en clair à côté du type d'abilité pour que les
      deux disent la même chose ; **« After YOU change form »** → `"You"`, pas
      un coéquipier ; **deux limites SÉPARÉES**, « once per phase » ne se
      partage pas ; les libellés `(thwart)` et `(attack)` alimentent Désorienté
      et Sonné ; **aucun coût**, le soutien ne s'incline pas.
      Résultat : conforme.
- [x] Étape 6 : coût 2, ressource mentale ; 1 menace ou 1 dégât, une fois par
      phase et par branche. Résultat : conforme.
- [x] Étape 7 : 2 capacités, **2 cas** — un par branche, et c'est la paire qui
      prouve que la forme est bien relue APRÈS la bascule.
- [x] Étape 8 : voir preuve commune.

---

### hk010 : Intimidating Roar (Upgrade)

- [x] Étape 2 : `aa001a` pour `AfterUnitTookDamage(..., is_from_attack=True)`,
      qui documente aussi la lecture du montant sur le message ; `ho009` /
      `sd015` pour `CanPlayThisUpgradeCard` + `CostFunc.Exhaust("This")`.
- [x] Étape 5 : mots-pièges : **« FROM AN ATTACK »**, d'où `is_from_attack=True`
      — c'est l'écart imprimé avec Anger (hk001a), les deux cartes du même pack
      ne se déclenchent pas aux mêmes moments ; **« 2 threat INSTEAD »** : 2 ou
      1, jamais 3 ; le montant se lit sur **`message.took_damage`** et non sur
      les PV perdus — une prévention partielle change le nombre réellement
      subi, et `getattr(message, "damage", 0)` aurait rendu 0 **en silence** ;
      **« exhaust → »** est un coût. Résultat : conforme.
- [x] Étape 6 : coût 1, ressource mentale ; 1 menace, 2 si ≥ 3 dégâts subis.
      Résultat : conforme.
- [x] Étape 7 : 1 capacité, **1 cas** (le seuil des 3 dégâts, donc la branche
      « 2 menaces »).
- [x] Étape 8 : voir preuve commune.

---

### hk011 : Limitless Endurance (Upgrade) — **module réécrit après le plantage**

- [x] Étape 2 : **`05023` Endurance**, même phrase imprimée pour les PV
      (`GiveKeywordToAttached("You", health=3)`) ; `aa003` * Ebony et `al011`
      pour le +1 REC nommé ; `38007` Energy Transfer pour `HealthUnits`.
- [x] Étape 5 : mots-pièges : **les deux bonus n'ont pas la même portée, et
      c'est imprimé** — « YOU get +3 hit points » vise l'identité, donc les
      DEUX faces (15 → 18) ; « BRUCE BANNER gets +1 REC » cite un nom PROPRE,
      celui de la seule face civile, donc REC 4 → 5 et seulement là. Écrire le
      second comme le premier donnerait un REC à la face héros, qui n'en a pas,
      **silencieusement** (piège §3 de RECETTES-MOTEUR, trouvé en partie réelle
      sur an002). **« heal 1 damage from HULK »** : la face héros, pas un allié
      du même nom. `card_type=AlterEgo` + `control_by="You"` parce que « Bruce
      Banner » est aussi le nom de l'alter-ego officiel `10001b`.
      Résultat : conforme.
- [x] Étape 6 : coût 3, ressource énergie ; +3 PV, +1 REC, 1 soin par round.
      Résultat : conforme.
- [x] Étape 7 : 3 capacités, **2 cas**. Le premier couvre les deux bonus
      permanents d'un coup (`attributs: {health: 3, recover: 1}`), qui sont la
      partie piégeuse ; le second (ajout du 03/09/2026) prouve l'action de
      soin : 3 dégâts posés, 1 soigné, il en reste 2.
- [x] Étape 8 : voir preuve commune.

---

### hk012 : Limitless Strength (Upgrade) — **module réécrit après le plantage**

- [x] Étape 2 : `an002` * Sera pour le bonus nommé ; `an007` Asgard's Assassin
      pour `CanGenerateResources(HeroResource, ...)` + `CostFunc.Exhaust`.
- [x] Étape 5 : mots-pièges : **« HULK gets +1 ATK »** cite un nom PROPRE, celui
      de la seule face HÉROS → `GiveKeywordToInPlayWhenApplyThis(Hero,
      control_by="You")` et pas `GiveKeywordToAttached("You")`, qui servirait
      les deux faces ; `control_by="You"` n'est pas décoratif — « Hulk » est le
      nom d'un allié officiel, d'un sbire et d'un héros officiel, un
      `CardFinder(name="Hulk")` nu servirait l'allié d'un autre joueur ;
      **« Hero Resource »** : rien en forme civile ; **« Exhaust → »** est un
      coût. Résultat : conforme.
- [x] Étape 6 : coût 3, ressource physique ; +1 ATQ, 1 ressource physique
      générée par round. Résultat : conforme.
- [x] Étape 7 : 2 capacités, **2 cas**. Le premier prouve le +1 ATQ ; le second
      (ajout du 03/09/2026) prouve la génération de ressource, sur le montage
      de `vv010` : la main est réduite à la seule carte à payer, donc
      l'amélioration est l'UNIQUE source de paiement possible.
- [x] Étape 8 : voir preuve commune.

> ⚠ **Homonyme de classe Hero** : `10007` Limitless Strength est une carte
> signature du HULK OFFICIEL — et c'est une **ressource** là-bas, une
> **amélioration** ici. Documenté dans le `collision_note` du deck ; contrôle
> étape 10 relancé et vert.

---

### hk013 : Inner Conflict (Obligation) — **module réécrit après le plantage**

- [x] Étape 2 : **`10025` Inner Demons**, l'obligation du HULK OFFICIEL, au mot
      près à un détail : elle défausse 2 cartes CHOISIES là-bas, **1 carte au
      HASARD** ici (`DiscardRandomHandCards`).
- [x] Étape 5 : mots-pièges : **relire la face APRÈS
      `ChangeToOtherIdentityForm`** — `identity.card.face` lu avant la bascule
      rend la face de DÉPART, et les deux branches testeraient alors le nom
      d'AVANT, c'est-à-dire l'inverse exact de ce que la carte demande ;
      **« Change form » est inconditionnel et vient en premier**, c'est lui qui
      décide de la branche ; cette bascule **déclenche hk009** ; **« 1 RANDOM
      card »** → `DiscardRandomHandCards`, pas `DiscardHandCards`, qui
      laisserait choisir ; **« exhaust your HERO »** : la face héros seule.
      Résultat : conforme.
- [x] Étape 6 : 1 bascule, 1 carte défaussée au hasard OU 1 héros incliné.
      Résultat : conforme.
- [x] Étape 7 : 1 capacité, **2 cas** — les deux branches, et c'est la paire
      qui prouve la relecture de la face après bascule.
- [x] Étape 8 : voir preuve commune.

---

## Bilan

**14 cartes, 14 « Carte terminée : OUI ».**

### La leçon du 02/09/2026 : un pack non commité n'existe pas

Le plantage a détruit six modules **et** leur bytecode, en une seconde, à la
fin d'une session de trois heures. Ce qui a sauvé le pack, ce n'est pas une
sauvegarde : c'est que **la batterie de tests, écrite en même temps que les
modules, était assez précise pour servir de spécification**. Chaque cas dit la
carte de référence, le piège, et l'état attendu ; les six modules ont été
réécrits dessus et sont repassés au vert du premier coup.

Deux conséquences pratiques :

1. **Commiter le pack dès que `test_capacites` est vert**, sans attendre la
   substitution ni l'autoplay. Le coût d'un commit intermédiaire est nul, celui
   d'un plantage est une session.
2. **Le champ `pourquoi` des cas de test n'est pas de la décoration.** C'est
   lui, et lui seul, qui a permis de retrouver `to_form`, `LimitOncePerPhase`,
   la portée du +1 REC et la relecture de face de hk013. Continuer à l'écrire
   comme on l'écrit : la carte de référence, le piège, le nombre attendu.

⚠ `substituer_pack.py` pose un stub sur le **fichier source** et sauvegarde
l'original en `<module>.py.vrai`. Un plantage pendant la passe laisse donc le
pack **à moitié substitué**. Après toute interruption, vérifier qu'il ne reste
aucun `*.vrai` et qu'aucun module ne fait 74 octets.

### Reste à faire (écarts assumés, aucun bloquant)

- ~~Trois capacités sans cas de test dédié~~ : **comblé le 03/09/2026** à la
  demande de l'utilisateur. La Response de contre de `hk002`, l'action de soin
  de `hk011` et la génération de ressource de `hk012` ont chacune leur cas
  sujet, vert du premier coup. La batterie passe de 17 à **20 cas**.
- **Aucun set némésis propre** : le zip n'en fournit pas. Le deck emprunte
  celui du Hulk officiel sur décision de l'utilisateur du 02/09, ce qui n'était
  jouable qu'après le correctif moteur du même jour (commit `89b9a45`).
- **Pas de `data/nemesis/hulk_rainy_nemesis.json`** : facultatif (étape 4), et
  sans objet puisque le set est emprunté.
- **0 % de victoire contre Klaw**, dans les deux difficultés, alors que Rhino
  en expert passe à 50 %. Ce n'est pas un défaut de script — 0 erreur sur les
  32 journaux — mais le CTR 0 de la face héros : contre une manigance qui monte
  vite, la menée ne passe que par Bruce Banner, donc par une bascule de forme
  que Klaw punit. À revoir côté **deck d'aspect** (plus de contre), pas côté
  modules.
