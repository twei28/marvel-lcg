# PROCESSUS-CARTE.md : les 15 gabarits du pack ARES (set 164, `ar`)

> **Mise à jour du 07/10/2026 (audit du backlog)** : CLOS : 15 gabarits « OUI ». L'unique case vide est la partie jouée à la main, sortie du backlog le 15/09.

Gate de `PROCESSUS-HEROS.md` : un gabarit rempli par carte. Rédigés le
07/09/2026. Auteur du pack : **Rainy**, zip « Ares » (dossier `A créer`).

⚠ **Aucun aspect n'a été arbitré, et c'est voulu.** Consigne utilisateur du
06/09/2026 : on n'invente plus de deck d'aspect pour un héros homebrew. Le
`player_deck` est **vide**. Détail : `PROCESSUS-HEROS.md` étape 3.

**Trois arbitrages utilisateur, posés AVANT d'écrire (étape 3)** :

| Carte | Question | Réponse du 07/09/2026 |
|---|---|---|
| `ar007` God of War | « play it on that minion » : payer ou gratuit ? | **On paie le coût** (Feint, Reeling, Sundered coûtent 0 ; un TACTIC d'aspect coûte son prix, l'obligation s'applique) |
| `ar013` Aegis Breastplate | « deal that much damage to the attacker » hors attaque ? | **L'identité du joueur à l'origine** prend les dégâts renvoyés |
| `ar003` To Battle! | « Choose two of the following » : répétition ? | **Deux options différentes** |

**Preuves communes**, citées une fois :

- **Étape 1** : pack `ares` en queue de `cards.json` (15 cartes), set
  `164. Custom (Ares)` dans `sets_info.json`, préfixe `ar` déclaré,
  `verifier_prefixes` OK, checksums recalculés par `recalculer_checksums.py`.
- **Étape 3 (héros)** : `deck/starter/ares.json`, 15 exemplaires signature,
  obligation `ar010`, set némésis `ar011`-`ar014` (Lead the Charge x2),
  `metadata.deckbuilding.hors_aspect` = 5 améliorations TACTIC d'autres aspects
  (Lord of War), avec la clé **`types: ["Upgrade"]`, ajoutée au deck-builder
  ce jour** (`quotaHorsAspect`, `public/js/deckbuilder/app.js`) et documentée
  au §5.4 du GUIDE.
- **Étape 4, images** : `assets/pics/ar0*.jpg` pour les 15, copiées du zip
  par `tools/importer_images_ares.py` (⚠ `0.2 Ares.jpg` est le HÉROS,
  `0.1 Ares.jpg` l'ALTER-EGO : vérifié sur le libellé imprimé, pas sur le
  numéro).
- **Icônes de ressource** : vérifiées par découpe des coins contre trois
  cartes de Sunfire à `RES` déclaré (`sf002` Y, `sf006` B, `sf008` R), planche
  `scratchpad/ares/petites/coins.png`. Résultat : Spray and Pray **Y**, To
  Battle! **B**, Ares' Axe **R**, Battle Helm **B**, Feint **R**, God of War
  **G**, Reeling **R**, Sundered **R**.
- **Mot-clé maison `seek`** : fiche `docs/reference/mots-cles/seek.md` créée
  avant d'écrire une ligne (lecture de beta_ray_bill : chercher dans la zone
  nommée).
- `test_cards` : **5335 ok / 0 erreur** (5320 avant le pack, soit **+15**).
  Un seul échec en cours de route, `ar005`, sur le nom d'un paramètre
  (`took_excess_damage` n'existe pas sur `AfterUnitDefeatedUnit`, c'est
  `has_excess_damage`), attrapé par `test_cards`.
- `verifier_desc_mots_cles ares` / `verifier_noms_modules` /
  `verifier_appels_modules ares` / `verifier_cartes_en_jeu ares` : **OK**.
- **Étape 7, cas** : `test_capacites.py … ar0` → **36/36**, en passe parallèle
  (`PARALLELES=4`) **et** en passe séquentielle (table en fin de fichier).
- **Étape 7, substitution** : `substituer_pack.py … ar0` : table en fin de
  fichier.
- **Étape 7 (héros)** : biographie `ar001a` dans `heros-info.js` (`node
  --check` OK).
- **Étape 8 (héros)** : les 15 textes français dans `textes-fr-fanmade.ts`
  (`tsc` OK).
- **Étape 10** : signatures étrangères : aucune carte d'aspect dans le deck,
  rien à contrôler.

---

## PAS DE GATE DE PORTÉE : AUCUN FICHIER MOTEUR PARTAGÉ TOUCHÉ

Rien hors de `src/cards/pack/ares/` n'a été modifié côté moteur. Aucun
mot-clé nouveau dans le moteur (`seek` est une lecture, pas une primitive),
aucun compteur nouveau, aucune fabrique nouvelle. Tous les traits imprimés
(OLYMPUS, SOLDIER, TACTIC, PREPARATION, TITLE, CONDITION, ARMOR, WEAPON,
ELITE, AVENGER) existent déjà dans l'énumération `TRAITS`.

Le seul fichier partagé touché est **hors moteur** : `public/js/deckbuilder/app.js`
(clé `types` du quota hors aspect, additive, aucun héros existant ne la
définit).

---

## LA MÉCANIQUE : LA BRIQUE 6, POUSSÉE LOIN

Trois améliorations JOUEUR se posent sur un ENNEMI (`ar006` Feint sur un
ennemi, `ar008` Reeling et `ar009` Sundered sur un sbire, « Max 1 per enemy »
= `desc.MaxPerUnit`), et le reste du kit les LIT :

| Carte | Ce qu'elle fait des améliorations sur l'ennemi |
|---|---|
| `ar004` Ares' Axe | +1 ATQ par amélioration attachée à la cible, percant |
| `ar007` God of War | en joue une depuis le deck quand un sbire entre en jeu |
| `ar008` Reeling | overkill + 2 aux dégâts excédentaires |
| `ar005` Battle Helm | convertit les dégâts excédentaires en menace retirée |
| `ar012` Athena | refuse toute amélioration TACTIC |

Modèles : `ss012` Mark of Kaine (pack scarlet_spider, **auteur Arnaud**) pour
overkill + exces, `gmw/16045` Follow Through, `bk009` Portal, `yd012` Yaka
Arrow, `sf009` Burning.

---

## CE QUE LES GATES ONT TROUVÉ

Sept cas rouges à la première passe, tous instructifs, **quatre défauts de
code corrigés**, le reste des cas mal montés :

### 1. `ForcedInterruptHero` n'est pas réservé à la forme héros par le moteur

`ability_type.py` : `HeroInterrupt`, `HeroResponse`, `HeroAction` portent
`is_hero_type = True` (vérifié par `effect.GetInitiator().IsHero()`,
`ability.py:112`). **`ForcedInterruptHero` ne le porte pas.** Feint partait
donc en forme civile. Le contre-cas l'a vu ; corrigé par une condition
explicite `en_forme_heros` dans `ar006`. À garder en tête pour toute
« Forced Hero Interrupt » future.

### 2. Le sélecteur de `CanPlayThisUpgradeCard` ne consulte pas `CheckIfFaceCanAttachTo`

Pour « play it ON THAT MINION », une première version verrouillait la cible
par une règle temporaire `CheckIfFaceCanAttachTo → SetCannotAttachTo`. Le
journal de partie montre Feint jouée **sur Rhino**. Remplacé par le chemin de
`yd012` : jouer normalement, puis `AttachTo2(sbire)` si la carte a atterri
ailleurs (« Rhino unequipped Feint ; Hydra Bomber equipped Feint (God of
War) » dans le journal). ⚠ Le message `CheckIfFaceCanAttachTo` reste
consulté par `AttachTo2` et par notre `PeutSAttacherA` : c'est là qu'Athena
refuse les TACTIC.

### 3. Le harnais défend

`Puzzle.Boost` et `Puzzle.Reveal` font activer l'ennemi par le vrai flux, et
le pilote **déclare Ares défenseur** (DEF 2) : trois cas mesuraient 2 de
moins que prévu. `Puzzle.Exhaust('ar001a')` avant l'activation règle le
point ; consigné aussi dans les `pourquoi` des cas.

### 4. Goblin (`39043`) retire lui-même 2 menaces en mourant

Le cas du casque lisait 4 menaces retirées pour 2 d'excès : le journal montre
« Breakin' & Takin' perd 2 pions (Goblin) » AVANT le casque. Cas remonté sur
Hydra Bomber (2 PV, When Revealed seulement). Leçon : lire le JOURNAL, pas
le seul chiffre (PROCESSUS-CARTE 7.7).

### 5. `Puzzle.CreateEncounterDeck` AJOUTE au deck, il ne le remplace pas

(`puzzle.py:83`). Un contre-cas « deck rencontre sans sbire » n'est donc pas
montable sur Rhino ; la condition `deck_rencontre_a_un_sbire` de `ar001a`
reste sans témoin outillé (voir « ce que ces blocs ne peuvent pas voir »).

### 6. ⚠ Une recherche sans correspondance donne quand même une carte (MOTEUR, non corrigé)

`SearchInternal.SearchForCardsInternal` (`search_internal.py:44-46`) : quand
aucune face ne passe le filtre, `select_face = all_faces` et le joueur choisit
parmi TOUTES les cartes ; le pilote en prend une. Constaté sur le contre-cas
de `ar001b` (deck sans TACTIC : la main gagnait une carte). Comportement
partagé par toutes les recherches du dépôt, **hors périmètre de ce pack** :
signalé dans SESSION.md pour un correctif moteur avec la batterie complète.

### 7. `Puzzle.SetThreat` sur la manigance PRINCIPALE plante

`AssertionError: prev_scheme.card=[01097a]` : les cas du casque emploient une
manigance annexe mise en jeu (`01107`, menace figée à 5).

### 8. La substitution a attrapé un attendu creux (`ar010`)

Le cas « chaque TACTIC coûte +1 : To Battle! devient injouable » lisait
« Feint reste dans le deck ». Sans le module, il restait **VERT** : To
Battle! se jouait et sortait bien une Feint, mais le deck naturel d'Ares en
contient trois. Attendu réécrit sur la MAIN (Genius jamais dépensé reste seul
en main, To Battle! en défausse). C'est exactement ce que la substitution
est censée trouver (PROCESSUS-CARTE 7.6) : un cas vert qui ne prouve rien.

### 9. ⚠ Le pilote d'autoplay bloquait sur toute suite de 3 attaques identiques (OUTIL, corrigé)

Premier autoplay : **7 parties bloquées sur 8**, toutes sur Spray and Pray,
question fautive « Deal 1 damage to an enemy (plage [1, 1]) ». L'empreinte
anti-répétition de `tools/autoplay.py` (`empreinte`) ne comptait ni les PV
du vilain ni ceux des sbires (`pv_ratio` est celui du HÉROS) : cinq tirs
sur Rhino avaient la même signature, et `MAX_REPETITIONS = 2` tombait au
troisième. Burst Fire et It's Clobberin' Time! ne passaient que parce que
leurs DEUX attaques tiennent dans le budget. Correctif additif dans le
pilote, même geste que le correctif lady_sif du 03/09 (aligner `empreinte`
sur `progres`) ; résultats après correctif dans le bloc final.

---

## ⚠ Ce que ces blocs ne peuvent pas voir

- `ar001a` : la condition « le deck rencontre contient un sbire » (voir 5).
- `ar007` : le **paiement** d'une amélioration TACTIC d'aspect jouée depuis le
  deck (aucune carte de ce genre dans un deck déterministe du harnais) ; le
  cas ne prouve que le chemin coût 0.
- `ar011` : « minions gain quickstrike » (le Tenace est prouvé, l'attaque
  éclair ne l'est pas : aucune clé d'état ne la mesure).
- `ar014` : « Give each minion a facedown boost card » (aucune clé d'état ne
  compte les cartes de bonus d'un sbire).
- `ar006` : les libellés `(attack/defense)` ne sont pas posés
  (`check_sub_type` refuse tout libellé sur `ForcedInterruptHero`, RECETTES
  §4bis) ; écart cosmétique, sans effet de règle connu.
- Une vraie partie jouée par un humain dans le navigateur : **pas faite**.

---

## Les gabarits, carte par carte

### ar001a : * Ares (héros)

- [x] Étape 2 : carte(s) de référence : `56007` Hunted (`CostFunc.SearchForCard`
      en coût, `searched_faces`), `br005`/`br011` (`seek`, `EngagePlayer`),
      `15003`/`bc004` (`PlayCardsLikeInTurn(ignore_resources_cost=True)`),
      `08013` (deux branches).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « Action » (face
      héros, donc forme héros de fait), « → » (le sbire est le COÛT),
      « engaged with you », « or » (deux branches exclusives), « ignoring its
      RESOURCE cost », « Limit once per round ».
      Résultat : conforme ; `conditions=[deck_rencontre_a_un_sbire]` ajoutée
      (RECETTES §5, coût offert sans cible).
- [x] Étape 6 : nombres : 14 PV / 3 ATQ / 1 CTR / 2 DEF / main 4 ; « draw 2 » ;
      `desc` et code identiques.
- [x] Étape 7 : cas : « le sbire convoqué est le COÛT, puis piocher 2 »,
      « branche jouer un événement en ignorant son coût » (Spray and Pray joué
      sans ressource : 5 dégâts).
- [x] Étape 7 bis : limite OUI. Témoin : « la limite once per round mord au
      second appel » : deux `Puzzle.Action`, le second refusé
      (`declencher_tolerant`), un seul sbire convoqué, main +2 seulement.
- [x] Étape 8 : autoplay ciblé : voir bloc final.

Carte terminée : OUI (réserve : la condition « deck sans sbire » n'a pas de
témoin outillé, voir 5).

### ar001b : * Ares (alter-ego)

- [x] Étape 2 : `dd001b` Fatalis (règle de deckbuilding déclarée, §5.4),
      `form.py:136` `WhenUnitWouldChangeForm`, `an001b`/`ho007`
      (`Search.PlayerCard` + `GainCard`).
- [x] Étape 5 : « Lord of War » (AUCUN code, `metadata.deckbuilding`, clé
      `types` neuve), « Interrupt: When you change form » (face alter-ego, donc
      au passage civil → héros), « a TACTIC CARD » (pas « upgrade » : trait
      seul).
      Résultat : conforme.
- [x] Étape 6 : 14 PV / REC 4 / main 5 ; « up to 5 » dans `hors_aspect.max`.
- [x] Étape 7 : cas : « une carte TACTIC du deck arrive en main » (deck figé
      `ar006` + `01088`, Feint arrive).
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : bloc final.

Carte terminée : OUI (réserve : le contre-cas « sans TACTIC » n'est pas
montable, voir 6 : comportement moteur).

### ar002 : Spray and Pray

- [x] Étape 2 : `th010` It's Clobberin' Time! (suite d'attaques, sélecteur
      reposé à chaque fois), `01053` Relentless Assault
      (`hero.DealDamage(..., property=AttackProperty())`).
- [x] Étape 5 : « the following ATTACK 5 times » (cinq attaques du héros, pas
      une de 5), « against ANY targets you choose » (sélecteur reposé).
      Résultat : conforme.
- [x] Étape 6 : coût 3, 5 fois, 1 dégât.
- [x] Étape 7 : cas : « cinq tirs d'1 sur Rhino : 5 dégâts », « cinq attaques
      DISTINCTES : Hydra Bomber (2) puis Hydra Mercenary (3) tombent ».
- [x] Étape 7 bis : aucune limite.
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### ar003 : To Battle!

- [x] Étape 2 : `br005` Star Jump (« Choose X of the following »), `an001b`
      (`Search.PlayerCard(include_discard_pile=True, finder=...)`), `an001a`
      (`Faces.ReadyAll`).
- [x] Étape 5 : « Choose TWO » (arbitrage : deux options différentes, la branche
      prise est retirée), « TACTIC OR WEAPON upgrade » (`traits=[...]`, OU),
      « deck AND discard pile », « hero-specific upgrade YOU CONTROL »
      (`card_class="IdentitySpecific"`, `from_where=["YouControlCards"]`,
      `canbe_ready=True`), « Ready Ares » (identité par le type).
      Résultat : conforme.
- [x] Étape 6 : coût 2, « two », « a » (une carte cherchée).
- [x] Étape 7 : cas : « deux premières branches » (Feint sort du deck, la
      hache est redressée, Ares reste incliné), « Ready Ares puis la
      recherche : deux options DIFFÉRENTES » (`preferer_option` sur Ares seul ;
      si la répétition était permise, Feint resterait dans le deck).
- [x] Étape 7 bis : aucune limite.
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### ar004 : * Ares' Axe

- [x] Étape 2 : `sf001a` (`WhenUnitWouldAttack(..., is_basic_attack=True)`),
      `60008` Cross-Examination (`len(GetAttachedUpgrades())`), `19018` Subdue
      (`GainATKForThisAttack`), `ho016` (`GainPiercing`).
- [x] Étape 5 : « Restricted » (desc), « When ARES makes a BASIC attack »
      (`"You"` + `is_basic_attack`), « exhaust Ares' Axe → » (coût
      `Exhaust("This")`), « for each UPGRADE attached to THAT enemy » (type
      Upgrade seul, un Attachment de rencontre ne compte pas), « gains
      piercing » (inconditionnel).
      Résultat : conforme.
- [x] Étape 6 : coût 1, +1 par amélioration.
- [x] Étape 7 : cas : « 3 + 2 (Feint, Sundered) + 1 = 6, Whirlwind tombe », «
      CONTRE-CAS sans la hache : 4, il survit », « piercing : le Tenace de Hydra
      Soldier ne bloque rien ».
- [x] Étape 7 bis : aucune limite (le coût d'inclinaison borne l'usage).
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### ar005 : * Ares' Battle Helm

- [x] Étape 2 : `an004` Murderous Glare (`AfterUnitDefeatedUnit(..., Enemy,
      is_from_attack=True).SetTarget(Scheme2, range=(1,1))`), `defeated.py`
      (`has_excess_damage`), `01063` Interrogation Room (même forme avec
      `Exhaust("This")`).
- [x] Étape 5 : « After ARES attacks AND defeats » (`"You"`,
      `is_from_attack=True`), « exhaust ... AND choose a scheme → » (deux
      coûts), « for each point of EXCESS damage » (`message.excess_damage`,
      `has_excess_damage=True`), « from THAT scheme ».
      Résultat : conforme.
- [x] Étape 6 : coût 2, 1 menace par point.
- [x] Étape 7 : cas : « 1 dégât excédentaire sur Hydra Bomber : 1 menace
      retirée, le casque s'incline », « CONTRE-CAS coup pile : aucun excès, la
      Réponse n'est pas offerte », « + Reeling : 3 menaces retirées et 3
      déversés sur Rhino ».
- [x] Étape 7 bis : aucune limite (inclinaison).
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### ar006 : Feint

- [x] Étape 2 : `bk009` Portal (`CanPlayThisUpgradeCard(CardFinder(card_type=
      Enemy))`), `02020` Hysteria (`WhenUnitWouldAttack(ForcedInterrupt,
      <ennemi>)`), `19018` (`GainATKForThisAttack(-2)`).
- [x] Étape 5 : « Max 1 per enemy » (`MaxPerUnit`), « FORCED HERO Interrupt »
      (`ForcedInterruptHero` + condition `en_forme_heros`, voir trouvaille 1),
      « (attack/defense) » (libellés non posés, RECETTES §4bis), « When
      ATTACHED enemy initiates an attack » (`conditions=[est_mon_hote]`),
      « discard Feint → -2 ATK ... Deal 2 damage » (malus et dégâts avant la
      défausse).
      Résultat : conforme, un défaut corrigé (forme civile).
- [x] Étape 6 : coût 0, -2, 2 dégâts, max 1.
- [x] Étape 7 : cas : « -2 ATQ (0 dégât à Ares), 2 dégâts au sbire, Feint
      défaussée », « CONTRE-CAS en forme civile : ne part pas ».
- [x] Étape 7 bis : « Max 1 per enemy » est une limite de POSE, lue par le
      moteur dans `desc` (`has_max_per.py`) ; pas de témoin dédié, `God of War
      + Athena` et `PeutSAttacherA` la relisent.
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### ar007 : God of War

- [x] Étape 2 : `br009` Oathbrother (`AfterCardEnterPlay(HeroResponse, Minion)`
      + `LimitOncePerPhase()`), `an001b` (`Search.PlayerCard(finder=
      CardFinder(check_face_fn=...))`), `bc004`/`dz031` (`AddToHand` +
      `PlayCardsLikeInTurn`), `yd012` (`AttachTo2` pour déplacer).
- [x] Étape 5 : « that CAN BE ATTACHED to that minion » (`PeutSAttacherA` :
      `CheckIfFaceCanAttachTo` + `MaxPerUnit`), « and PLAY it » (arbitrage :
      coût payé, `PlayCardsLikeInTurn` sans `ignore_resources_cost`), « ON THAT
      MINION » (`AttachTo2(sbire)` après le jeu, voir trouvaille 2), « After a
      minion ENTERS PLAY », « Limit once per PHASE ».
      Résultat : conforme, un défaut corrigé (cible du jeu).
- [x] Étape 6 : coût 2 ; « a » (une carte).
- [x] Étape 7 : cas : « Feint sort du deck et se joue SUR CE SBIRE » (Hydra
      Bomber déjà en jeu, Feint finit sur Hydra Soldier), « + Athena : rien à
      lui attacher, Feint reste dans le deck ».
- [x] Étape 7 bis : limite OUI. Témoin : « deux sbires dans la même phase, une
      seule amélioration jouée » (Sundered reste dans le deck).
- [x] Étape 8 : bloc final.

Carte terminée : OUI (réserve : paiement d'un TACTIC d'aspect non prouvé,
voir « ce que ces blocs ne peuvent pas voir »).

### ar008 : Reeling

- [x] Étape 2 : `ss012` Mark of Kaine (modèle EXACT : `WhenUnitWouldAttackUnit
      (None, "AttachedMinion") + GainOverKill`, `WhenUnitAttackDealExcessDamage
      + IncreaseDamage(2)`), `33032` Marked, `gmw/16045`.
- [x] Étape 5 : « Attach to a MINION », « Max 1 per enemy », « ATTACKS ...
      gain overkill » (toute attaque, `attacker=None`), « Increase the amount
      of EXCESS damage » (`WhenCalcDealExcessDamage`, envoyé seulement quand la
      santé passe sous zéro : à excès nul, rien, même lecture que Mark of
      Kaine), constantes → `NonKeyword`.
      Résultat : conforme.
- [x] Étape 6 : coût 0, +2, max 1.
- [x] Étape 7 : cas : « overkill, et l'excès gonflé de 2 se déverse sur Rhino »
      (Goblin 1 PV, attaque 3 : 4 sur Rhino), « CONTRE-CAS sans Reeling :
      Rhino ne prend rien », plus la synergie avec le casque.
- [x] Étape 7 bis : « Max 1 per enemy » : idem Feint.
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### ar009 : Sundered

- [x] Étape 2 : `sf006` Atomic Samurai / `dt094` (`WhenUnitWouldTakeDamage` +
      `IncreaseDamage`), `damage.py` (`is_from_attack=True`).
- [x] Étape 5 : « Attach to a MINION », « Max 1 per enemy », « from EACH
      ATTACK » (`is_from_attack=True`), « ATTACHED enemy takes »
      (`conditions=[est_mon_hote]`), constante → `ForcedInterrupt`.
      Résultat : conforme.
- [x] Étape 6 : coût 0, +1, max 1.
- [x] Étape 7 : cas : « 3 + 1 = 4 », « CONTRE-CAS : les 2 dégâts de Feint ne
      sont pas une attaque, ils restent 2 ».
- [x] Étape 7 bis : « Max 1 per enemy » : idem Feint.
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### ar010 : Ire of Athena

- [x] Étape 2 : `sf010` Shame / `04165` Martial Law (obligation qui reste en
      jeu), `resources.py:668` `IncreaseResourceCostToPlay`, RECETTES §5 (« A
      or B » = deux capacités, `an003`, `vv005`, `br004`).
- [x] Étape 5 : « each TACTIC YOU play » (`CardFinder(trait=TACTIC)`, `"You"`),
      « Exhaust your alter-ego OR discard a TACTIC card » (deux
      `PlayerActionToDiscardThis(AlterEgoAction)`), « DISCARD this card » (pas
      « remove », contrairement à Shame).
      Résultat : conforme.
- [x] Étape 6 : +1, 2 boost, « a » carte.
- [x] Étape 7 : cas : « To Battle! (2) devient injouable avec 2 icônes »
      (Genius reste seul en main, To Battle! en défausse ; attendu durci après
      la substitution, trouvaille 8), « CONTRE-CAS sans l'obligation : jouée,
      Feint en main », « premier coût : incliner l'alter-ego », « second coût :
      défausser une TACTIC, Ares reste prêt ».
- [x] Étape 7 bis : aucune limite.
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### ar011 : Athena's Guidance

- [x] Étape 2 : `40101` Mutant Slayers (`GiveKeywordToInPlayWhenApplyThis(...,
      quickstrike=1)`, `environment_helper.py:41` pour `toughness`), `01164`
      Titania's Fury (`WhenCardBecomeBoost` + `GiveBoostCardForThisActivation`).
- [x] Étape 5 : « MINIONS gain quickstrike and toughness » (tous les sbires,
      pas le vilain ; Tenace à l'entrée en jeu, règle du mot-clé), « Give the
      ACTIVATING enemy an additional boost card » (`message.activating_enemy`).
      Résultat : conforme.
- [x] Étape 6 : menace 3 par joueur (`"3*"`), 2 boost, « an additional » = 1.
- [x] Étape 7 : cas : « Hydra Bomber entre en jeu avec sa carte Tenace », « [star]
      Boost : 2 + 2 + 2 = 6 dégâts » (carte supplémentaire = Breakin' & Takin',
      Ares incliné pour ne pas défendre).
- [x] Étape 7 bis : aucune limite.
- [x] Étape 8 : bloc final.

Carte terminée : OUI (réserve : « quickstrike » sans mesure outillée).

### ar012 : * Athena

- [x] Étape 2 : `ability_factory.py:178` `ThisCannotHaveCardsAttached`
      (`CheckIfFaceCanAttachTo` + `SetCannotAttachTo`, restreint ici aux
      TACTIC), `16118` Badoon Grunt (`DealEncounterCards`), `sender_card.py`
      `AfterThisActivation`.
- [x] Étape 5 : « Retaliate 1. Toughness. » (desc), « cannot have TACTIC
      UPGRADES attached » (type Upgrade + trait), « deal YOURSELF »
      (`GetAgainstPlayer`), « AFTER this activation » (`AfterThisActivation`).
      Résultat : conforme.
- [x] Étape 6 : 6 PV / SCH 3 / ATK 2, 1 boost, Riposte 1, 1 carte.
- [x] Étape 7 : cas : « God of War + Athena : rien à lui attacher », « [star]
      Boost : après l'activation, 1 carte rencontre face cachée » (vérificateur
      `ares_cartes_rencontre_distribuees`, 2 + 1 = 3 dégâts).
- [x] Étape 7 bis : aucune limite.
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### ar013 : * Aegis Breastplate

- [x] Étape 2 : `04065` * Crossbones' Armor (`SetBeInstead` +
      `PlaceCountersOn('damage')` + défausse à 5), `04029` * Crossfire's Rifle
      (`AttachToFaceWhenPutIntoPlay(..., if_cannot_attach_to=Villain)`).
- [x] Étape 5 : « Attach to a MINION. Otherwise, the villain », « ANY amount of
      damage » (toute source), « place it HERE instead », « to the ATTACKER »
      (arbitrage : personnage source, sinon identité du joueur à l'origine),
      « 5 OR MORE » (`>=`), renvoi avant défausse.
      Résultat : conforme.
- [x] Étape 6 : 2 boost, seuil 5.
- [x] Étape 7 : cas : « absorbée (3 compteurs) et renvoyée (3 à Ares) », « 5 ou
      plus : défaussée (3 + 3) », « dégâts HORS attaque (Feint) : absorbés et
      renvoyés à l'identité », « Otherwise : sans sbire, sur Rhino »
      (vérificateur `ares_hotes`).
- [x] Étape 7 bis : aucune limite.
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### ar014 : Lead the Charge

- [x] Étape 2 : `04070`/`11051` (`DoActivate(player, effect)`), `04111` Zola
      (`Search.EncounterCard(include_discard_pile=True, card_type=Minion)` +
      `Players.ForEachPlayer`), `br011` (`PutIntoPlay` + `EngagePlayer`),
      `sf011` (`GiveFacedownBoostCards`).
- [x] Étape 5 : « EACH minion engaged with A PLAYER activates AGAINST THEM »,
      « who was NOT activated against this way », « deck AND discard pile »,
      « ENGAGED WITH THEM », « EACH minion a facedown boost card ».
      Résultat : conforme.
- [x] Étape 6 : 2 boost, 1 carte de bonus par sbire, « a minion » = 1.
- [x] Étape 7 : cas : « Hydra Soldier frappe Ares (2) », « joueur sans sbire :
      un sbire du deck rencontre est mis en jeu engagé ».
- [x] Étape 7 bis : aucune limite.
- [x] Étape 8 : bloc final.

Carte terminée : OUI (réserve : la carte de bonus donnée n'est pas mesurée).

---

## Étape 8 : autoplay ciblé et passes de contrôle

### Cas, passe parallèle puis séquentielle (07/09/2026, 21:17)

`test_capacites.py … 42000 … ar0` : **36/36** en séquentiel, **36/36** en
parallèle (`PARALLELES=4`), verdicts identiques cas par cas (comparaison des
deux JSON). Après la réécriture de l'attendu `ar010` (trouvaille 8) : les 4
cas `ar010` rejoués, **4/4**.

### Substitution (`substituer_pack.py … 31000 ar0`, sources rétablies, md5 identique à la sauvegarde)

| Carte | Rouges sans module | Vert restant (attendu : contre-cas ou cas partagé) |
|---|---|---|
| ar001a | 3/3 | |
| ar001b | 1/1 | |
| ar002 | 2/2 | |
| ar003 | 2/2 | |
| ar004 | 2/3 | contre-cas « sans la hache » |
| ar005 | 2/3 | contre-cas « coup pile, aucun excès » |
| ar006 | 1/2 | contre-cas « forme civile » |
| ar007 | 2/3 | cas partagé « Athena refuse les TACTIC » (rien à attacher, avec ou sans module) |
| ar008 | 2/3 | contre-cas « sans Reeling » |
| ar009 | 1/2 | contre-cas « les 2 dégâts de Feint ne sont pas une attaque » |
| ar010 | **3/4** (2/4 avant trouvaille 8) | contre-cas « sans l'obligation » |
| ar011 | 2/2 | |
| ar012 | 1/2 | cas partagé « Athena refuse les TACTIC » |
| ar013 | 4/4 | |
| ar014 | 2/2 | |

**15/15** cartes avec au moins un cas au rouge sans leur module.

### Decks

`DECK_NOM=ares verifier_tous_les_decks` : `{"ok": true, "message":
"identite ar001a, main 5, deck 10"}` (15 cartes, main de 5). Témoin
`sunfire` : `identite sf001a, main 6, deck 9`. Signatures étrangères
(Étape 10 de PROCESSUS-HEROS) : **0 sur 126 decks**.

### Autoplay (`autoplay.py --deck ares --vilains rhino --profils equilibre --parties 8`)

| Passe | Parties | Bloquées | Tracebacks | V / D | Rounds moy. |
|---|---|---|---|---|---|
| Avant correctif du pilote | 8 | **7** (toutes sur Spray and Pray, 3e tir) | 0 | 0 / 1 | 2,8 |
| Après correctif (trouvaille 9) | 8 | **0** | 0 | 0 / 8 (6 éliminés, 2 manigances) | 3,5 |
| Témoin `spider_man`, même réglage | 8 | 1 (Hero Action, hors Ares) | 0 | 0 / 7 | |

Cartes d'Ares jouées par le pilote sur les 8 parties : Feint 30, Spray and
Pray 16, Sundered 11, Battle Helm 6, Axe 6, Reeling 3, God of War 2. Quatre
« `WhenPlayerInTurn failed` » sur le casque : le pilote tente de le jouer
sans rien pour payer (même famille que Tenacity dans les commentaires du
pilote), pas un défaut de carte. Le 0 % de victoire est celui du profil
`equilibre` sur Rhino (le témoin officiel fait 0 % aussi) ; Ares meurt plus
vite parce que son deck de 15 cartes sans aspect se vide tous les trois
rounds.

### Bio (Étape 7 de PROCESSUS-HEROS)

Assistant local (`localhost:2345/prepare.html`, Solo, onglet FAN-MADE) : la
tuile `data-hero="ares"` existe, le survol ouvre la fiche « ARES, PV 14,
FAN-MADE » et le volet Biographie affiche le texte de `heros-info.js`
(civil, base, équipes, ennemis, Thor #129 (1966)). Capture vue le 07/09 à
21:28.

### Gate finale de PROCESSUS-HEROS

- [x] Étapes 1 à 8 complètes
- [x] 15 gabarits « Carte terminée : OUI » : ar001a, ar001b, ar002, ar003,
      ar004, ar005, ar006, ar007, ar008, ar009, ar010, ar011, ar012, ar013,
      ar014
- [x] `verifier_tous_les_decks` relancé, deck `ares` au vert
- [ ] Une partie complète jouée avec le héros : **pas faite** (à jouer par
      l'utilisateur)
