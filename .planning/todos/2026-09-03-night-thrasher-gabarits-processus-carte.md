# PROCESSUS-CARTE.md — les 18 gabarits du pack NIGHT THRASHER (set 153, `nt`)

Gate de `PROCESSUS-HEROS.md` : un gabarit rempli par carte. Rédigés le
03/09/2026. Auteur du pack : **DESIGNHACKER**, format « MC4 SEALED ».

**Preuves communes**, citées une fois :

- **Étape 7, substitution** : `substituer_pack.py .game-src 57000 nt0` →
  **18/18 cartes prouvées**. Deux cas restent verts sans module, et les deux
  sont légitimes : `nt003a` « la planche arrive AU SETUP » (l'arrivée est
  native, lue dans `desc.Setup` par `world.py:531`, aucun module en jeu) et
  `nt015` « sans la hache, aucun dégât » (**contre-cas d'ABSENCE d'effet**).
  Chacun a son jumeau nominal, lui au rouge.
- **Étape 7, cas** : `test_capacites.py [nt0]` → **29/29 cas verts**.
- **Étape 8, autoplay** : **32 parties** (Rhino et Klaw, normal et expert, profil équilibré). **Grep exhaustif : 0 traceback sur 32 journaux**, et **0 partie bloquée**. Les 18 cartes apparaissent dans les journaux et la Battle Board bascule **93 fois** : le pack tourne vraiment. ⚠ **0 victoire sur 32** — mais le témoin `armored_spidey`, relancé dans la MÊME fournée, rend **exactement le même profil** (0/32, 16 éliminations et 16 complots principaux, 0 blocage). Le zéro vient du pilote, pas du pack. ⚠ Une première fournée donnait **23 éliminations sur 32** et 2,2 rounds tenus contre Klaw expert : le deck ne comptait que DEUX alliés, or l'allié est la principale éponge à dégâts du jeu pour un héros à 9 PV et DEF 1. Deux améliorations « Max 1 par joueur » lentes ont été remplacées par `01058` * Daredevil et `08012` * Quake — éliminations **23 → 16**, rounds tenus en hausse partout.
- **Étape 4, image** : `assets/pics/nt0*.png` pour les 18, découpées du zip
  `NIGHT THRASHER (MC4 SEALED)-20260902T070659Z-1-001.zip` (26 fichiers hors
  `PRINTING FILES`, 18 cartes distinctes).
- **Étape 1** : pack `night_thrasher` en queue de `cards.json`, set
  `153. Custom (Night Thrasher)` dans `sets_info.json`, préfixe `nt` déclaré,
  checksums recalculés, `verifier_prefixes` OK.
- `test_cards` : **5162 ok / 0 erreur** (5144 avant le pack, +18).
- `verifier_appels_modules` : « tous les appels de night_thrasher existent ».
- `verifier_cartes_en_jeu` : « les 18 cartes de night_thrasher portent ce que
  leur texte annonce ».
- `verifier_tous_les_decks` : **`night_thrasher` au vert**, 115/116 (le seul
  échec restant, `sp_dr`, est antérieur au pack).
- **Étape 10 de PROCESSUS-HEROS** : contrôle sur les **116 decks de départ** →
  **0 écart**, alors que le héros porte le nom de l'allié officiel `dt125`.
- **Les 26 scans ont été lus un par un** avant la première ligne de code, et
  les exemplaires multiples **comparés au pixel** sur leur zone de règles :
  Disaster ×2, Drop In ×2, Kickflip ×4, Tailblock ×2 et Cosmic Connection ×2
  ne diffèrent que par leur numéro de collection.

**Un mot-clé maison**, `agile 1`, **défini par l'auteur** entre parenthèses sur
la carte — donc aucun arbitrage — mais **sans aucune primitive moteur**. Fiche
complète et montage retenu : `docs/reference/mots-cles/agile.md`.

**Deux décisions de l'utilisateur**, prises le 03/09/2026 avant la première
ligne de code :

1. **« Fired Up » écartée.** Le dossier `ENCOUNTER SET` du zip contient une
   carte étrangère : bandeau « MAGMA NEMESIS (2/5) », art et texte de Selene.
   Le set némésis de Night Thrasher est complet sans elle (Terrax 1/5,
   Cemented 2/5, Cosmic Connection 3/5 et 4/5, Cosmic Ax 5/5). À reprendre le
   jour où Magma sera portée.
2. **Aspect JUSTICE.** Aucune decklist fournie. Le kit récompense le trait
   `SKILL` (quatre cartes du pack en vivent) et Justice en a le plus gros
   vivier du jeu : 12. Il compense aussi la vraie faiblesse du héros, une CTR
   imprimée de 1.

---

## Ce que la batterie a appris — CINQ vrais défauts, pas des erreurs de test

Sur les vingt cas à corriger, **cinq portaient sur le contenu lui-même**. Les
autres étaient des montages de cas. Tous sont consignés parce qu'ils se
reproduiront.

### 1. `desc.Setup` n'existe QUE pour les cartes du deck du joueur

`world.py:531` balaie `player_deck`, `set_aside_nemesis_sets`, les decks de
rencontre et les decks additionnels — **jamais `set_aside`**, qui n'est lu que
par les clients (catalogue, lanceur), comme `PROCESSUS-HEROS.md` le dit déjà.
La Battle Board, placée en `set_aside` par mimétisme avec les autres
améliorations recto-verso du dépôt, **n'entrait jamais en jeu** : **vingt cas
sur vingt-neuf tombaient d'un coup**.

⚠ Ce n'est PAS la même situation que Phoenix Force, Spider Armor ou le SP//dr
Suit : celles-là sont posées par un `SetupPutIntoPlay` sur l'ALTER-EGO, et
`set_aside` n'y sert qu'à l'affichage. La Battle Board, elle, porte
`desc.Setup` sur la carte elle-même — c'est le motif `04159a`, et il exige
d'être **dans le deck**. Le deck compte donc 16 entrées signature, dont une
quitte le deck dès la mise en place : 15 restent, comme la numérotation
imprimée de l'auteur.

⚠ **Deux cartes du dépôt ont le même défaut latent** : `sr012` Impact Webbing
(pack `spider_man_rainy`) et `hd017` Nexus of all Realities (pack
`howard_the_duck`) portent `desc.Setup` et sont en `set_aside`. Non corrigées
ici — hors périmètre de ce portage — mais signalées.

### 2. Le module d'une obligation vit dans le dossier de SON set_name

`nt012` Practice a `set_name = "Night Thrasher"` (l'obligation appartient au
set du héros, comme `im014` et `as014`), mais son module avait été rangé dans
`night_thrasher_nemesis/`. `database.py:197` cherche le module dans le dossier
qui porte le nom du SET : **le fichier n'était jamais chargé**, l'obligation
entrait en jeu et ne faisait rien, en silence. Le journal le dit en deux
lignes — « Practice entered play », puis plus rien.

C'est **exactement le piège `bt019`**, écrit noir sur blanc en tête de ce pack,
et payé quand même.

### 3. Une carte est DÉJÀ dans `this_round_played_cards` quand son coût se calcule

`nt005` Kickflip lit « the last card you played this round ». Le moteur
enregistre la carte jouée **avant** `WhenCalculateEffectCost` : Kickflip se
voyait donc **elle-même** comme la dernière carte jouée, la condition était
toujours vraie, et la réduction **permanente**. Journal : « would play Kickflip
with () » sur la PREMIÈRE copie. Le module exclut désormais `effect.this`.

### 4. `AttackProperty` n'a pas de `indirect_damage`

`nt015` Cosmic Connection le passait : `TypeError` levé, **visible au journal**
mais la carte ne faisait plus rien. La bonne API est `DealIndirectDamage`
(`card_face.py:583`), qui redirige vers `unit.TakeIndirectDamage`.

### 5. Quatre cartes MORTES dans le premier jet du deck

`08018` Spycraft (« only if you control a **Spy** character »), `19031`
« Think Fast! » et `20028` Shake it Off (**guardian**), `52034` Quick Quip
(**Web-Warrior**). Night Thrasher est AVENGER et NEW WARRIOR, rien d'autre.
Une carte injouable ne casse aucun outil — le moteur ne valide pas les decks —
mais elle occupe une place pour rien. C'est un cas de test qui l'a dit, en
constatant que `08018` n'entrait pas en jeu.

### Et un ajout au harnais

**`Puzzle.BeginVillainPhase()`** a été ajouté à `src/game/puzzle/puzzle.py`.
Le harnais savait faire attaquer, contrer, manigancer et défendre, mais pas
**franchir une frontière de phase** : aucun des 1136 cas de la batterie ne
joignait « quand la phase du méchant commence ». `nt011` Prewind Stance en
vit. La commande reproduit exactement l'ouverture de phase du moteur
(`world.py:789`) sans jouer la suite de la phase.

---

## Gabarits, carte par carte

Les blocs « étape 2 » (carte de référence) et « étape 5 » (texte-contre-code)
sont écrits **en tête de chaque module**, avec le POURQUOI de chaque choix et
la liste des mots-pièges vérifiés. Ce fichier donne le verdict et ce qui est
propre à la carte.

### nt001a : * Night Thrasher (face héros)

- [x] Étape 2 : `as001b` (même déclencheur `AfterPlayerPlayedCard(… "You" …)`),
      `15001a` pour `LimitOncePerPhase`.
- [x] Étape 5 : mots-pièges `[[SKILL]]` = trait et non type ; `once per PHASE`
      (≠ per round, l'inverse de la face civile). Résultat : conforme.
- [x] Étape 6 : PV 9, ATQ 1, CTR 1, DEF 1, main 5.
- [x] Étape 7 : cas « jouer une carte SKILL retourne la planche », rouge 1/1.
- [x] Étape 8 : couverte par la fournée commune (voir les preuves communes).

**Carte terminée : OUI**

### nt001b : * Dwayne Taylor (face alter-ego)

- [x] Étape 2 : `mw001b` (règle de construction de deck, rien à scripter),
      `Faces.ShuffleAllTo`, `32030b` pour `LimitOncePerRound`.
- [x] Étape 5 : `X` = nombre de cartes choisies et non un coût ; `into your
      DECK` ≠ défausse ; `once per ROUND`. Résultat : conforme.
- [x] Étape 6 : PV 9, REC 3, main 6, plafond de 4 cartes SKILL hors aspect.
- [x] Étape 7 : cas « 2 cartes SKILL remélangées, 2 piochées », rouge 1/1.
- [x] Étape 8 : couverte par la fournée commune (voir les preuves communes).

**Carte terminée : OUI**

### nt002 : Disaster

- [x] Étape 2 : `08013` Stealth Strike (ciblage DANS l'opération, imposé ici
      car la nature de la cible n'est connue qu'APRÈS le retournement).
- [x] Étape 5 : `Then` = la face se lit APRÈS la bascule ; deux libellés en un
      seul `SetLabel`. Résultat : conforme.
- [x] Étape 6 : coût 2, 3 menaces, 4 dégâts.
- [x] Étape 7 : 2 cas (branche VEHICLE, branche WEAPON), rouges 2/2.
      ⚠ Disaster porte SKILL : Varial Heelflip rebascule derrière elle, et le
      compte n'est pas 5-3=2 mais 5-1-3=1. Trois capacités du pack
      s'enchaînent sur une seule carte jouée.
- [x] Étape 8 : couverte par la fournée commune (voir les preuves communes).

**Carte terminée : OUI**

### nt003a : * Battle Board (face [[VEHICLE]])

- [x] Étape 2 : `34002a` / `as002a` (permanente recto-verso), `45075b`
      (`AfterFlipToThisFace`), **`27082`** Biting Retort pour l'accroche sur
      les cartes de boost.
- [x] Étape 5 : **NIGHT THRASHER** = nom propre ; `a scheme` = principal ou
      annexe ; `Response` nue ici contre `Hero Response` sur l'autre face ;
      `Permanent. Setup.` = deux bases automatiques. Résultat : conforme.
- [x] Étape 6 : +1 CTR, agile 1, 1 menace, 3 pions… (aucun compteur ici).
- [x] Étape 7 : 4 cas (arrivée au Setup, +1 CTR, retour sur VEHICLE, agile 1),
      rouges 3/4 — l'arrivée au Setup est native, aucun module en jeu.
- [x] Étape 8 : couverte par la fournée commune (voir les preuves communes).

**Carte terminée : OUI**

### nt003b : * Battle Board (face [[WEAPON]])

- [x] Étape 2 : `34002b` / `as002b`, `45075b`.
- [x] Étape 5 : nom propre ; `Hero Response` (≠ la face VEHICLE) ; `an enemy`
      sans lien avec ce qui précède ; pas de `desc.Setup` sur cette face.
      Résultat : conforme.
- [x] Étape 6 : +1 ATQ, +1 DEF, 1 dégât.
- [x] Étape 7 : 2 cas (bonus continus, dégât au retournement), rouges 2/2.
- [x] Étape 8 : couverte par la fournée commune (voir les preuves communes).

**Carte terminée : OUI**

### nt004 : Drop In

- [x] Étape 2 : `01019a` / `bt001b` (`to_form=Hero`), `08013` (ciblage dans
      l'opération, filtres différents par branche).
- [x] Étape 5 : `change TO HERO form` (≠ nt008) ; confuse/stun à ne pas
      intervertir ; `canbe_confused` / `canbe_stunned`. Résultat : conforme.
- [x] Étape 6 : coût 1.
- [x] Étape 7 : 2 cas (branche VEHICLE, branche WEAPON), rouges 2/2.
- [x] Étape 8 : couverte par la fournée commune (voir les preuves communes).

**Carte terminée : OUI**

### nt005 : Kickflip

- [x] Étape 2 : `ReduceCostToPlayThis` + `player.stat.this_round_played_cards`.
- [x] Étape 5 : `the LAST card` (`[-1]`, jamais `any(...)`) ; `a Night Thrasher
      event` = ce `set_name` ; `this round` ≠ this turn. Résultat : conforme
      **après correctif** (défaut n°3 ci-dessus).
- [x] Étape 6 : coût 1, réduction 1, 1 dégât, 1 carte.
- [x] Étape 7 : 2 cas (effets de base, réduction de coût), rouges 2/2.
- [x] Étape 8 : couverte par la fournée commune (voir les preuves communes).

**Carte terminée : OUI**

### nt006 : Melon Grab

- [x] Étape 2 : `im002` (répartition libre par `AssignDamage`), `27078` pour
      percant/déferlement.
- [x] Étape 5 : 8 dégâts pour 3 — c'est imprimé ; `can be divided` =
      facultatif ; branches exclusives. Résultat : conforme.
      ⚠ Écart assumé identique à im002 : `AssignDamage` n'accepte pas de
      `property` — **sans conséquence ici**, la branche VEHICLE n'a aucun
      mot-clé à porter.
- [x] Étape 6 : coût 3, 8 dégâts.
- [x] Étape 7 : cas « planche WEAPON : 8 dégâts perçants », rouge 1/1.
- [x] Étape 8 : couverte par la fournée commune (voir les preuves communes).

**Carte terminée : OUI**

### nt007 : Tailblock

- [x] Étape 2 : `im007` / `as001a` (`PreventDamage`), `09015` pour le libellé
      `(defense)`.
- [x] Étape 5 : `any amount` **SANS** `from an attack` — différence exacte avec
      `as001a` ; 1+pioche contre 3 sec, à ne pas intervertir. Résultat :
      conforme.
- [x] Étape 6 : coût 1, prévention 1 ou 3, pioche 2.
- [x] Étape 7 : cas « planche VEHICLE : 1 prévenu et 2 piochées », rouge 1/1.
- [x] Étape 8 : couverte par la fournée commune (voir les preuves communes).

**Carte terminée : OUI**

### nt008 : * The Mancave

- [x] Étape 2 : `01019a` (changement de forme), `42018` pour le soin,
      `im001b` / `16024` pour `UpdateNextCardPlayCost`.
- [x] Étape 5 : `change form` tout court (≠ nt004) ; `your identity` ;
      `the NEXT SKILL card … THIS TURN` (`in_this='Turn'`) ; **aucun coût
      d'inclinaison imprimé**, à ne pas ajouter. Résultat : conforme.
      ⚠ Le nom est « The **Mancave** », en un mot, alors que le fichier du zip
      dit « The Man Cave ».
- [x] Étape 6 : coût 2, soin 1, réduction 1.
- [x] Étape 7 : 2 cas (soin en civil, réduction en héros), rouges 2/2.
- [x] Étape 8 : couverte par la fournée commune (voir les preuves communes).

**Carte terminée : OUI**

### nt009 : * Escrima Sticks

- [x] Étape 2 : `27078` (`UnitAttackGainKeyword` + `conditions`), `50093` pour
      la condition continue sur une carte recto-verso, `bt006` pour le
      remélange.
- [x] Étape 5 : `your attacks` = celles du héros ; bonus côté **VEHICLE**
      (contre-intuitif mais imprimé) ; `Shuffle into your DECK` ≠ défausse.
      Résultat : conforme.
- [x] Étape 6 : coût 3, 6 dégâts.
- [x] Étape 7 : 2 cas (l'Action et le remélange, le percant qui traverse
      Robuste), rouges 2/2.
- [x] Étape 8 : couverte par la fournée commune (voir les preuves communes).

**Carte terminée : OUI**

### nt010 : Multi-Skilled

- [x] Étape 2 : `14017` Nerves of Steel (`for_card`), `ab007` pour le coût
      d'inclinaison.
- [x] Étape 5 : le [wild] généré n'est PAS le [mental] du coût imprimé —
      icône croisée avec `nt004` et `nt007` du même pack (leçon Lockjaw) ;
      `for a SKILL card` = trait ; une seule `CanGenerateResources` par carte.
      Résultat : conforme.
- [x] Étape 6 : coût 1.
- [x] Étape 7 : cas « sa ressource paie seule une carte SKILL à 1 »,
      rouge 1/1.
- [x] Étape 8 : couverte par la fournée commune (voir les preuves communes).

**Carte terminée : OUI**

### nt011 : Prewind Stance

- [x] Étape 2 : `ok014` (bonus continus), `WhenPlayerTurnBegin` et
      `WhenVillainPhaseBegin` (deux messages, donc deux capacités).
- [x] Étape 5 : nom propre ; `turn OR villain phase` = deux déclencheurs ;
      `exhaust →` = coût ; `Hero Interrupt`. Résultat : conforme.
      ⚠ Le nom est « Prewind Stance », alors que le fichier du zip dit
      « Night Thrasher's Suit ».
- [x] Étape 6 : coût 3, +1 DEF, riposte 1.
- [x] Étape 7 : 2 cas (bonus continus, phase du méchant), rouges 2/2.
      ⚠ Le second n'a été possible qu'après l'ajout de
      `Puzzle.BeginVillainPhase()` au harnais.
- [x] Étape 8 : couverte par la fournée commune (voir les preuves communes).

**Carte terminée : OUI**

### nt012 : Practice (obligation)

- [x] Étape 2 : `im014` / `an010` (obligation à choix), `11020` pour
      l'interdiction, `YouCannotFlipCards` + `RegisterTemp`.
- [x] Étape 5 : `exhaust OR discard` = un OU dans le coût, rendu par deux
      options ; `remove from the GAME` ≠ `Discard` ; interdiction
      **temporaire**. Résultat : conforme **après correctif** (défaut n°2).
      ⚠ `desc.GiveTo` vaut « Dwayne Taylor », l'alter-ego, alors que la carte
      imprime « the Night Thrasher player » : convention du moteur, les deux
      désignent le même joueur, et « Night Thrasher » ne résolvait aucun
      joueur.
- [x] Étape 6 : Boost 1.
- [x] Étape 7 : cas « incliner l'identité retire l'obligation de la PARTIE »,
      rouge 1/1.
- [x] Étape 8 : couverte par la fournée commune (voir les preuves communes).

**Carte terminée : OUI**

### nt013 : * Terrax the Tamer (némésis)

- [x] Étape 2 : `AfterEnemyActivatesAgainstYou`, `15004` pour la défausse du
      deck de rencontre, `an015` pour la révélation.
- [x] Étape 5 : `activates` = attaque OU manigance (≠ `as023`, qui imprime
      `schemes`) ; `discarded THIS WAY` ; symétrie avec `nt016`. Résultat :
      conforme.
- [x] Étape 6 : PV 7, MAN 1, ATQ 2, Boost 2, 8 cartes.
- [x] Étape 7 : cas « son activation défausse 8 cartes et révèle la hache »,
      rouge 1/1.
- [x] Étape 8 : couverte par la fournée commune (voir les preuves communes).

**Carte terminée : OUI**

### nt014 : Cemented (némésis)

- [x] Étape 2 : `PlayersCannotMakeBasicAttack`, `YouCannotFlipCards`,
      `iw015` pour le texte vierge contre défausse.
- [x] Étape 5 : `Hinder 1[per_hero]` = base automatique ; `heroes or allies` ;
      `upgrades or identities` = deux familles ; `each player MAY` ;
      `until the end of the PHASE`. Résultat : conforme.
      ⚠ **Deux écarts assumés**, tous deux en faveur du joueur :
      `YouCannotFlipCards` ne porte que sur les cartes du joueur courant
      (identique en solo), et le texte vierge est posé globalement, le moteur
      ne connaissant pas de texte vierge par joueur.
- [x] Étape 6 : menace 2, Entrave 1*, Boost 2.
- [x] Étape 7 : cas « le héros ne peut plus attaquer en pouvoir de base »,
      rouge 1/1.
- [x] Étape 8 : couverte par la fournée commune (voir les preuves communes).

**Carte terminée : OUI**

### nt015 : Cosmic Connection (némésis)

- [x] Étape 2 : `06030` / `as025` (`WhenThisRevealed`), `ag013` pour le Surge,
      `DealIndirectDamage`.
- [x] Étape 5 : deux conditions **cumulatives** ; `your hero has a WEAPON card`
      — la hache elle-même est attachée à Terrax et ne compte pas ; `3
      INDIRECT damage` ; `If NO damage` = zéro. Résultat : conforme **après
      correctif** (défaut n°4).
- [x] Étape 6 : Boost 1, 3 dégâts.
- [x] Étape 7 : 2 cas (nominal, contre-cas sans la hache), rouges 1/2 — le
      contre-cas d'absence reste vert, assumé.
- [x] Étape 8 : couverte par la fournée commune (voir les preuves communes).

**Carte terminée : OUI**

### nt016 : * Cosmic Ax (némésis)

- [x] Étape 2 : `ag013` Hallucination (attachement qui cherche son porteur),
      `40122a` pour `ATK+`, `an013` pour le Boost.
- [x] Étape 5 : `If you cannot` vérifié AVANT de fouiller (piège `wd028`) ;
      `discarded THIS WAY` ; symétrie avec `nt013` ; `+2 ATK` lu dans `desc`.
      Résultat : conforme.
- [x] Étape 6 : Boost 2, +2 ATQ, 8 cartes.
- [x] Étape 7 : cas « Terrax en jeu : la hache s'attache et lui donne +2 ATQ »,
      rouge 1/1.
      ⚠ La hache se **révèle**, elle ne se **pose** pas : un attachement sans
      porteur n'entre nulle part, et `Puzzle.PutIntoPlay` s'arrêtait à
      « created ».
- [x] Étape 8 : couverte par la fournée commune (voir les preuves communes).

**Carte terminée : OUI**

---

## Ce que ces blocs ne peuvent pas voir

**Aucune partie n'a été jouée par un humain dans le navigateur.** Les 29 cas et
l'autoplay disent que les capacités s'exécutent et que la partie ne bloque
pas ; ils ne disent pas si le rythme véhicule/arme est agréable à jouer.

**Multijoueur non testé.** Deux écarts de `nt014` Cemented ne se voient qu'à
plusieurs, et les helpers `PlancheDuJoueur` / `JoueurDeCetteCarte` sont écrits
pour ne jamais toucher la planche d'un autre Night Thrasher, mais rien ne l'a
vérifié en table à deux.

**Le contre-cas du mot-clé `agile` est partiel.** Le contre-cas réellement
discriminant serait une attaque **sans** carte de boost, et le harnais ne sait
pas en produire : une activation d'ennemi en reçoit toujours. Le contre-cas
monté (`nt003a`, « agile ne touche PAS aux dégâts hors attaque ») prouve que la
réduction n'est **pas permanente** — le piège que la fiche du mot-clé signale —
mais il reste vert sous substitution, faute de pouvoir opposer les deux
montages. C'est écrit dans `docs/reference/mots-cles/agile.md`, et c'est la
seule gate du pack restée entrouverte.

**Le garde-fou d'`agile` n'est pas exercé en solo.** Il empêche la réduction de
se cumuler quand une activation retourne plusieurs cartes de boost ; à un
joueur, Rhino n'en distribue qu'une. Le code est là et commenté, mais seule une
partie à plusieurs le mettra à l'épreuve.
