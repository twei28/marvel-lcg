# Lady Deathstrike (Mysteltainn) : gabarits PROCESSUS-CARTE, 19 card_id

Scénario `lady_deathstrike` (standard : stades I+II ; expert : II+III), préfixe `ld`, set 213. Source : zip « LadyDeathstrike » déposé le 24/10/2026.
Cas : `Fusion/marvel-lcg-src/tools/cas/lady_deathstrike.py` et `lady_deathstrike_b.py` (filtre `[ld]`). Plateau : `ui-app/src/board/lady-deathstrike-plateau.test.ts`.
Scénarios : `data/scenarios/lady_deathstrike(.json|_expert.json)` (et non `scenarios_custom/`, qui est le dossier des scénarios faits au wizard),
ensembles `data/encounter_sets/lady_deathstrike.json` et `reaver_resources.json`.

## Points d'identification et arbitrages

1. **Extraction** : une première extraction du zip avait été tronquée (`| head`), 4 cartes Bleeding Out (5-8) manquaient ; refaite, tout relu.
2. **Doublons** : Bleeding Out 5-8, Nanoskeleton 9-10, Tracker 13-15, Bide Time 17-18, Lash Out 20-21, Mutant Hunter 22-23, Inhibitor Collar 3-4 sont
   IDENTIQUES au pixel près (hors numéro) : une carte, plusieurs exemplaires dans `encounters` / `set_aside`.
3. **Icônes** identifiées par les GLYPHES de `ChampionsIcons.ttf` (pas à vue) : Bide Time = Crisis, Stalking Prey = Hazard, Chop-Shop = Amplify.
4. **Chop-Shop Cybernetics** (arbitrage 25/10) : « the attached enemy » = l'ennemi sur lequel le TECH s'attache, s'il y en a un ; un TECH sur une identité
   ne donne Tough qu'au vilain.
5. **Adamantium Nanoskeleton** (arbitrage 25/10) : « a player attacks » = tout personnage que le joueur contrôle (héros, allié, événement).
6. Modulaire par défaut `military_grade` (officiel) ; `reaver_resources` (maison, 3 cartes identiques à Military Grade) proposé dans `sets_info.json`.
7. Homonymes : `* Lady Deathstrike` (minions 35034, 43029), Titanium Exoskeleton / Inhibitor Collar (40091/40092), Stalking Prey (hs123) : tout passe par card_id.
8. Constat moteur : les attachements d'un vilain SUIVENT le stade suivant (les Griffes restent attachées de II à III).

## Gates du scénario

- [x] Étapes 1 à 8 : cartes (`cards.json`), scripts, scénarios standard et expert, ensembles de rencontre, `sets_info.json` (set 213), images (`assets/pics/ld*.jpg`, non versionnées), textes FR (`textes-fr-fanmade.ts` + généré, compteur « saignement »).
- [x] `test_cards.py` 7347 OK / 0 erreur ; `verifier_prefixes.py` OK ; `verifier_traductions_fr.py` OK ; deck témoin spider_man monte une partie.
- [x] Cas : **72 cas `[ld]` verts** ; substitution : **19/19 cartes** avec au moins un cas rouge sans leur module (les cas restés verts sont des contre-cas d'absence ou de valeurs imprimées).
- [x] Plateau : `ui-app/src/board/lady-deathstrike-plateau.test.ts` 3/3 (calibré ROUGE), rendu générique suffisant.
- [x] Autoplay : 40 parties, 0 traceback.
- [ ] **Partie réelle jouée par un humain : NON FAITE** (tension du saignement, deck qui se vide, choix du modulaire Military Grade / Reaver Resources dans le wizard non vérifié dans le navigateur, enchaînement des stades).
- Cas « Permanent » calibré ROUGE le 25/10 : sans `Permanent` dans `desc` de ld005, le cas échoue (« ld005 n'est pas en jeu (accroche_a) »). Il ne repose donc pas que sur l'AssertionError du harnais : la vérification `accroche_a` après la tentative de défausse prouve que la carte reste attachée.



### ld001 : Lady Deathstrike (Villain)

```
* Lady Deathstrike (I) — VILAIN, stade 1. REAVER. PV 16 par joueur, ATK 2, SCH 1.
Forced Response: After Lady Deathstrike attacks and damages you, resolve the "Special" ability on the copy of Bleeding Out
  attached to your identity.

Cartes de reference :
 - `41013` Cypher : `AfterUnitAttackAndDamageUnit` (« attacks AND DAMAGES » : pas `AfterUnitAttackUnit`, qui part sans degat).
 - `45113` Barrage : `message.GetToPlayer()` = le joueur attaque ; `01100`/`40090` pour « the copy ... attached to your identity ».
 - helper du set `ResoudreSaignement` (ld005 Bleeding Out) : fiche mots-cles/special.md.

⚠ Mots-pieges :
 - « attacks and DAMAGES you » : aucune reponse si l'attaque est entierement absorbee (defense, Tenace) ;
 - « YOUR identity » : la copie de CE joueur (jeu a plusieurs), pas celle du premier joueur ;
 - Forced Response : obligatoire, APRES l'attaque ; HP « 16* » = 16 par joueur (`desc.HP = "16*"`) ;
 - nom `* Lady Deathstrike` partage avec deux SBIRES du depot : ne jamais chercher par nom (`IDS_VILAIN`).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - ld001 Lady Deathstrike (I) : attaque BIEN defendue (aucun degat) -> pas de Special
      - ld001 Lady Deathstrike (I) : attaque qui BLESSE -> Special sur la copie du joueur (3 -> 4, deck 6 -> 2)
      - ld001 Lady Deathstrike (I) : valeurs imprimees ATK 2, SCH 1, PV 16 (1 joueur), trait REAVER
      - ld001 Lady Deathstrike (I) : PV par joueur : 32 a deux joueurs
      Preuve par substitution : **rouges 1/4** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 40 parties (spider_man × lady_deathstrike standard, expert, rhino en témoin ; équilibré/agressif), grep tracebacks : 0 sur les 40 journaux. Journal lu : Bleeding Out saigne, le complot reçoit ses jetons. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ld002 : Lady Deathstrike (Villain)

```
* Lady Deathstrike (II) — VILAIN, stade 2. REAVER. PV 18 par joueur, ATK 3, SCH 1.
When Revealed: Find Reinforced Adamantium Claws and reveal it. If you cannot, resolve the "Special" ability on each copy of
  Bleeding Out in play.
Forced Response: After Lady Deathstrike attacks and damages you, resolve the "Special" ability on the copy of Bleeding Out
  attached to your identity.

Cartes de reference :
 - « Find X and reveal it » : `Find.FindAndReveal(effect, joueur, name=..., card_type=...)` (`59003` Embody Pathos, `60134a`),
   rend la carte revelee ou None (« If you cannot »).
 - Forced Response : `ld001` (meme texte, meme fabrique).

⚠ Mots-pieges :
 - « If you CANNOT » : Griffes introuvables (deja en jeu, ou ni dans le deck ni dans la defausse de rencontre) -> la
   branche Special sur CHAQUE copie en jeu (une par joueur) ; si on les trouve, AUCUN Special ;
 - les Griffes se REVELENT (elles s'attachent a Lady Deathstrike par leur propre capacite d'attache) : pas de mise en jeu directe.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - ld002 Lady Deathstrike (II) : mode EXPERT, le stade II est revele au Setup : il TROUVE les Griffes renforcees et les attache a lui
      - ld002 Lady Deathstrike (II) : Griffes INTROUVABLES (deck de rencontre vide) -> Special sur CHAQUE copie de Bleeding Out (3 -> 4, deck 6 -> 2)
      - ld002 Lady Deathstrike (II) : Griffes TROUVEES (standard, stade I vaincu) -> attachees a Lady Deathstrike, AUCUN Special (saignement 3, deck intact)
      - ld002 Lady Deathstrike (II) : apres une attaque qui blesse, Special sur la copie du joueur (3 -> 4) ; ATK 4 = 3 + 1 des Griffes
      Preuve par substitution : **rouges 4/4** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 40 parties (spider_man × lady_deathstrike standard, expert, rhino en témoin ; équilibré/agressif), grep tracebacks : 0 sur les 40 journaux. Journal lu : Bleeding Out saigne, le complot reçoit ses jetons. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ld003 : Lady Deathstrike (Villain)

```
* Lady Deathstrike (III) — VILAIN, stade 3. REAVER. PV 19 par joueur, ATK 3, SCH 1.
When Revealed: Resolve the "Special" ability on each copy of Bleeding Out in play. Find Reaver Commander and reveal it.
Forced Response: After a REAVER attacks and damages you, resolve the "Special" ability on the copy of Bleeding Out attached to
  your identity.

Cartes de reference :
 - `ld002` (Find.FindAndReveal, Special sur chaque copie) ; `41013` pour `AfterUnitAttackAndDamageUnit` avec un FILTRE d'attaquant
   (`CardFinder(trait=..., card_type=Enemy)`).

⚠ Mots-pieges :
 - « a REAVER attacks and damages you » : N'IMPORTE QUEL ennemi REAVER (Lady Deathstrike elle-meme, Reaver Tracker, les sbires du
   set Reavers), pas seulement elle ;
 - ORDRE : le Special sur chaque copie d'ABORD, puis le Commandant (la phrase le dit dans cet ordre) ; si le Commandant est
   introuvable on ne fait rien de plus (aucun « If you cannot » imprime ici).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - ld003 Lady Deathstrike (III) : valeurs imprimees PV 19 par joueur, ATK 3 + 1 des Griffes restees attachees d'un stade a l'autre = 4
      - ld003 Lady Deathstrike (III) : revele, Special sur chaque copie de Bleeding Out (3 -> 4) PUIS trouve et revele Reaver Commander (attache a elle)
      - ld003 Lady Deathstrike (III) : un AUTRE REAVER (Reaver Tracker) qui attaque et blesse declenche le Special
      - ld003 Lady Deathstrike (III) : un sbire NON REAVER (Hydra Mercenary) qui blesse ne declenche rien
      Preuve par substitution : **rouges 3/4** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 40 parties (spider_man × lady_deathstrike standard, expert, rhino en témoin ; équilibré/agressif), grep tracebacks : 0 sur les 40 journaux. Journal lu : Bleeding Out saigne, le complot reçoit ses jetons. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ld004a : Mutant Hunting Season (MainScheme)

```
Mutant Hunting Season (1A) — COMPLOT PRINCIPAL, stade 1A.
Contents: Lady Deathstrike (I) and (II) ((II) and (III) for expert mode). Lady Deathstrike, Reavers and Standard encounter
  sets. One modular set (Military Grade or Reaver Resources).
Setup: Attach a copy of Bleeding Out to each player, then set each remaining copy aside. Place 3 bleed counters on each copy
  of Bleeding Out.

Cartes de reference :
 - « Setup » d'une face 1A : `WhenCardSetup("This", op)` (`gs117a`, officiel `50087a` Batroc) ;
   cartes mises de cote : `Worlds.GetSetAsideAreaCards(effect, CardFinder(...))` ; mise en jeu `face.PutIntoPlay(joueur, effect)`.
 - « Contents » : composition du scenario, portee par `data/scenarios/lady_deathstrike*.json` (standard / expert), pas par le code.

⚠ Mots-pieges :
 - « a copy to EACH PLAYER » : un exemplaire par joueur (1 a 4), les autres RESTENT de cote (le scenario en liste 4) ;
 - « 3 bleed counters on EACH COPY » : chaque copie EN JEU recoit 3 compteurs ; les copies de cote n'existent pas encore.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ld004a Setup : chaque joueur a SA copie de Bleeding Out attachee a l'identite avec 3 compteurs bleed
      Preuve par substitution : **rouges 1/1** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 40 parties (spider_man × lady_deathstrike standard, expert, rhino en témoin ; équilibré/agressif), grep tracebacks : 0 sur les 40 journaux. Journal lu : Bleeding Out saigne, le complot reçoit ses jetons. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ld004b : Mutant Hunting Season (MainScheme)

```
Mutant Hunting Season (1B) — COMPLOT PRINCIPAL, stade 1B. Menace cible 9 par joueur, +1 par joueur par round, depart 1 par joueur.
Forced Response: After a player deck empties, place an acceleration token here.
If this scheme is completed, the players lose the game.

Cartes de reference :
 - valeurs « N par joueur » : `01097b` Rhino (`StartingThreat`, `TargetThreat`, `EscalationThreat` en `"N*"`).
 - « After a deck runs out » : `AfterDeckRunOut` (`sk288`, `ch002` Shang-Chi) ; ici N IMPORTE QUEL deck de joueur, donc `Ability(...)`
   construit a la main (la fabrique compare a UN deck) ; `scheme.PlaceAccelerationToken(n, effect)` (`56167`).

⚠ Mots-pieges :
 - « a PLAYER deck » : le deck de n'importe quel joueur, pas seulement le premier ; le deck de rencontre ne compte pas ;
 - le jeton d'acceleration se pose SUR CE complot et s'ajoute a l'escalade du round ;
 - « If completed, the players lose » : defaite native des complots principaux (rien a coder).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - ld004b Mutant Hunting Season : le deck du joueur se vide -> 1 jeton d'acceleration sur le complot
      - ld004b Mutant Hunting Season : un deck qui ne se vide pas ne donne aucun jeton
      - ld004b Mutant Hunting Season : menace de depart 1 par joueur (1 joueur : 1 ; 2 joueurs : 2)
      - ld004b Mutant Hunting Season : menace de depart 1 pour un joueur
      Preuve par substitution : **rouges 2/4** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 40 parties (spider_man × lady_deathstrike standard, expert, rhino en témoin ; équilibré/agressif), grep tracebacks : 0 sur les 40 journaux. Journal lu : Bleeding Out saigne, le complot reçoit ses jetons. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : jeton d'acceleration sur le complot principal. Cas plateau : ui-app/src/board/lady-deathstrike-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ld005 : Bleeding Out (Attachment)

```
Bleeding Out — ATTACHEMENT, CONDITION (4 exemplaires, un par joueur, mis de cote par ld004a).
Permanent. Attach to your identity.
Special: Place 1 bleed counter here. Discard cards from the top of your deck equal to the number of bleed counters here. If you
  discard an identity-specific card this way, take 1 damage.
Alter-Ego Action: Discard a card from your hand → remove 2 bleed counters from here.

Cartes de reference :
 - capacite nommee « Special » : `WhenResolveSpecialAbility("This", op)` (`ab007`, `baxter_stockman`), fiche mots-cles/special.md ;
   le corps vit dans le helper du set (`Saigner`) pour que Reaver Tracker lise « a-t-on defausse une carte d'identite ? ».
 - « Attach to your identity » : `AttachToFaceWhenPutIntoPlay("YourIdentity")` (`sk147`, `mf016`) ; `Permanent` : `desc.Permanent`
   natif (fiche permanent.md).
 - defausse du dessus du deck : `joueur.DiscardDeckTopCards(n, effect)` (`56167`) ; cout « discard a card from your hand » :
   `CostFunc.Discard("YourHandCards", range=(1, 1))` (`ar010`, `11018`).

⚠ Mots-pieges :
 - « Place 1 bleed counter THEN discard equal to the number of counters » : le compteur est pose AVANT le compte (3 -> 4 : 4 cartes) ;
 - « If you discard AN identity-specific card » : FAQ de l'auteur, 1 degat AU PLUS, que l'on defausse une ou plusieurs de ces cartes ;
 - « Alter-Ego ACTION » : seulement en forme alter-ego ; « remove 2 » : retire ce qu'il y a si moins de 2 compteurs ;
 - Permanent : ne peut pas etre defaussee (sauf par un effet du MEME set) ; copie par joueur : `LeSaignement(joueur)`.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (8 cas sujets) :
      - ld005 Bleeding Out : Special, +1 compteur bleed (3 -> 4) et defausse de 4 cartes du dessus du deck (6 -> 2), aucune carte d'identite : pas de degat de saignement
      - ld005 Bleeding Out : une carte d'IDENTITE parmi les 4 defaussees -> 1 degat de plus (2 de l'attaque + 1 = 3)
      - ld005 Bleeding Out : QUATRE cartes d'identite defaussees -> toujours 1 seul degat de saignement (FAQ de l'auteur)
      - ld005 Bleeding Out : Alter-Ego Action, defausse 1 carte de la main -> retire 2 compteurs bleed (3 -> 1)
      - ld005 Bleeding Out : avec 1 seul compteur, l'Alter-Ego Action retire ce qu'il y a (1 -> 0)
      - ld005 Bleeding Out : en forme HEROS l'Alter-Ego Action n'existe pas (aucun compteur retire)
      - ld005 Bleeding Out : sans carte en main, le cout n'est pas payable (aucun compteur retire)
      - ld005 Bleeding Out : Permanent, un effet d'un AUTRE set ne peut pas la defausser
      Preuve par substitution : **rouges 8/8** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 40 parties (spider_man × lady_deathstrike standard, expert, rhino en témoin ; équilibré/agressif), grep tracebacks : 0 sur les 40 journaux. Journal lu : Bleeding Out saigne, le complot reçoit ses jetons. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : attachement Permanent sur l'identite, compteurs bleed. Cas plateau : ui-app/src/board/lady-deathstrike-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ld006 : Adamantium Nanoskeleton (Attachment)

```
Adamantium Nanoskeleton — ATTACHEMENT, ARMOR (x2). Boost 2.
Attach to Lady Deathstrike.
Forced Interrupt: When a player attacks Lady Deathstrike, prevent all damage that would be dealt to her and resolve the "Special"
  ability on the copy of Bleeding Out attached to that player's identity instead. Then, discard this card. (Max once per attack.)

Cartes de reference :
 - « Attach to <nom> » : `AttachToFaceWhenPutIntoPlay(CardFinder(...))` (`01100`, `04084`) ; ici par card_id (homonymes).
 - « prevent all damage that would be dealt » : `WhenUnitWouldTakeDamage(ForcedInterrupt, "AttachedEnemy", op, is_from_attack=True)`
   + `message.PreventDamage("All", effect)` (`26012` Mass Increase, `bk003`).

⚠ Mots-pieges :
 - DECISION UTILISATEUR (25/10/2026) : « a player attacks » = TOUT personnage que le joueur controle (heros, allie, evenement
   d'attaque) : l'armure ne se contourne pas avec un allie ; le Bleeding Out saigne est celui du joueur QUI CONTROLE l'attaquant ;
 - « (Max once per attack) » : avec DEUX exemplaires attaches, le premier empeche tous les degats (donc le second ne voit plus rien
   a empecher, `at_least_damage=1`) : une seule armure part par attaque ;
 - « prevent ALL damage ... INSTEAD » : le Special remplace les degats ; « Then, discard this card » dans tous les cas.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - ld006 Adamantium Nanoskeleton : le heros attaque Lady Deathstrike -> AUCUN degat, Special sur SA copie (3 -> 4), l'armure est defaussee
      - ld006 Adamantium Nanoskeleton : un ALLIE qui attaque Lady Deathstrike declenche aussi l'armure (decision utilisateur du 25/10/2026)
      - ld006 Adamantium Nanoskeleton : sans armure, la meme attaque blesse Lady Deathstrike (contre-cas, ATK 2)
      - ld006 Adamantium Nanoskeleton : DEUX armures, une seule part par attaque (Max once per attack) : l'autre reste attachee
      Preuve par substitution : **rouges 3/4** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 40 parties (spider_man × lady_deathstrike standard, expert, rhino en témoin ; équilibré/agressif), grep tracebacks : 0 sur les 40 journaux. Journal lu : Bleeding Out saigne, le complot reçoit ses jetons. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : attachement sur le vilain. Cas plateau : ui-app/src/board/lady-deathstrike-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ld007 : Reaver Commander (Attachment)

```
Reaver Commander — ATTACHEMENT, TITLE. Boost : etoile seule (« [star] Boost: Reveal this card »).
Attach to Lady Deathstrike. Lady Deathstrike gains steady.
Forced Response: After an ally is defeated by a REAVER, place 1 threat on the main scheme.
Hero Action: Spend [mental][mental] resources → discard this card.
[star] Boost: Reveal this card.

Cartes de reference :
 - « Boost: Reveal this card » : `WhenCardBecomeBoost("This", RevealThisCard)` (`04084` Ball and Chain) ;
 - `steady` : `*GiveKeywordToAttached(Enemy, steady=1)` (fiche mots-cles/steady.md) ;
 - « Spend ... → discard this card » : `PlayerActionToDiscardThis(HeroAction).SetCost(Cost("BB"))` (`40090`, `02019`) ;
 - « after an ally is defeated by X » : `AfterUnitDefeatedUnit(type, <tueur>, Ally, op)` (`defeated.py`).

⚠ Mots-pieges :
 - « defeated BY a REAVER » : le tueur est un ennemi REAVER (pas n'importe quelle cause de defaite) ;
 - « place 1 threat on THE MAIN scheme » : le complot principal (`ld004b`), pas une manigance annexe ;
 - [mental][mental] = DEUX icones noeuds bleus (verifie contre les icones mentales du pack Shang-Chi) : `Cost("BB")` ;
 - le Boost est une ETOILE seule : aucune icone numerique (`desc.Boost` absent).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (6 cas sujets) :
      - ld007 Reaver Commander : attache a Lady Deathstrike, qui gagne STEADY (peut porter 2 etourdissements : un 1er Stun ne l'etourdit qu'a moitie)
      - ld007 Reaver Commander : un allie vaincu PAR un REAVER (Reaver Tracker) -> 1 menace sur le complot principal (1 -> 2)
      - ld007 Reaver Commander : un allie vaincu par un NON-REAVER (Hydra Mercenary) -> aucune menace en plus
      - ld007 Reaver Commander : Hero Action, depenser [mental][mental] (Genius BB) defausse la carte
      - ld007 Reaver Commander : [mental][mental] exige : avec de l'energie seulement (Energy YY) la carte reste attachee
      - ld007 Reaver Commander : [star] Boost : revelee comme carte boost, elle s'ATTACHE a Lady Deathstrike
      Preuve par substitution : **rouges 5/6** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 40 parties (spider_man × lady_deathstrike standard, expert, rhino en témoin ; équilibré/agressif), grep tracebacks : 0 sur les 40 journaux. Journal lu : Bleeding Out saigne, le complot reçoit ses jetons. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : attachement sur le vilain. Cas plateau : ui-app/src/board/lady-deathstrike-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ld008 : Reinforced Adamantium Claws (Attachment)

```
Reinforced Adamantium Claws — ATTACHEMENT, WEAPON. ATK +1[star]. Boost : etoile seule.
Attach to Lady Deathstrike.
[star] Lady Deathstrike's attacks gain piercing.
Hero Response: After you attack Lady Deathstrike, resolve the "Special" ability on the copy of Bleeding Out attached to your identity
  → discard this card.
[star] Boost: Reveal this card.

Cartes de reference :
 - `40090` Heavy Armament : `AfterUnitAttackUnit(HeroResponse, "You", "AttachedEnemy", DiscardThisCard)` + cout ; `ATK+` natif de `desc`.
 - « gain piercing » : `UnitAttackGainKeyword("AttachedEnemy", piercing=True)` (fiche mots-cles/piercing.md) ;
 - cout = resoudre le Special : `CostFunc.Custom(None, fn)` (`40092` Inhibitor Collar) ; `ld007` pour le Boost « Reveal ».

⚠ Mots-pieges :
 - « → » : ce qui precede est le COUT : le joueur DOIT pouvoir resoudre son Special (toujours possible), puis la carte est defaussee ;
 - « After YOU attack » : le heros du joueur (Hero Response), pas un allie ;
 - `ATK+` « 1* » : +1 ATK a l'ennemi porteur (lu dans desc), l'etoile renvoie au piercing du texte ;
 - si ld002 ne trouve pas les Griffes (deja en jeu), elles ne sont pas re-revelees.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (6 cas sujets) :
      - ld008 Reinforced Adamantium Claws : attachees a Lady Deathstrike, ATK +1 (2 -> 3)
      - ld008 Reinforced Adamantium Claws : [star] les attaques de Lady Deathstrike gagnent PIERCING : une carte Tough du heros est defaussee ET les degats passent (3)
      - ld008 Reinforced Adamantium Claws : SANS les Griffes, la meme attaque est absorbee par Tough (contre-cas)
      - ld008 Reinforced Adamantium Claws : Hero Response, apres que le heros attaque Lady Deathstrike -> Special sur SA copie (3 -> 4) et les Griffes sont defaussees
      - ld008 Reinforced Adamantium Claws : Hero Response absente en alter-ego (le heros n'attaque pas)
      - ld008 Reinforced Adamantium Claws : [star] Boost : revelees comme carte boost, elles s'ATTACHENT a Lady Deathstrike
      Preuve par substitution : **rouges 5/6** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 40 parties (spider_man × lady_deathstrike standard, expert, rhino en témoin ; équilibré/agressif), grep tracebacks : 0 sur les 40 journaux. Journal lu : Bleeding Out saigne, le complot reçoit ses jetons. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : attachement sur le vilain. Cas plateau : ui-app/src/board/lady-deathstrike-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ld009 : Reaver Tracker (Minion)

```
Reaver Tracker — SBIRE (x3). REAVER. PV 3, ATK 2, SCH 1, Boost 1.
When Revealed: Resolve the "Special" ability on the copy of Bleeding Out attached to your identity. If you did not discard an
  identity-specific card this way, place 1 threat on the main scheme.

Cartes de reference :
 - `WhenThisRevealed(None, op)` + `message.GetToPlayer()` (`nt015`, `56167`) ; helper `ResoudreSaignement` (ld005) qui RENDS
   « a-t-on defausse une carte d'identite ? » ;
 - `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (`01107`).

⚠ Mots-pieges :
 - « If you DID NOT discard an identity-specific card » : la menace se pose quand AUCUNE carte d'identite n'a ete defaussee
   (deck vide ou cartes d'aspect seules) ; si une est defaussee, le joueur a pris son degat et PAS de menace ;
 - « YOUR identity » : le joueur a qui le sbire est revele.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - ld009 Reaver Tracker : revele, Special sur la copie du joueur (3 -> 4, deck 6 -> 2) ; aucune carte d'identite defaussee -> 1 menace sur le complot (1 -> 2)
      - ld009 Reaver Tracker : une carte d'IDENTITE defaussee -> 1 degat et PAS de menace en plus (reste 1)
      - ld009 Reaver Tracker : valeurs imprimees PV 3, ATK 2, SCH 1, REAVER
      Preuve par substitution : **rouges 2/3** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 40 parties (spider_man × lady_deathstrike standard, expert, rhino en témoin ; équilibré/agressif), grep tracebacks : 0 sur les 40 journaux. Journal lu : Bleeding Out saigne, le complot reçoit ses jetons. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ld010 : Deep Wound (Obligation)

```
Deep Wound — OBLIGATION de rencontre (sans « Give to » : va au joueur qui la revele). Boost 2.
Your hero gets -1 ATK, -1 THW and -1 DEF.
Response: After you resolve the "Alter-Ego Action" on the copy of Bleeding Out attached to your identity, discard a card from your
  hand → discard this card.

Cartes de reference :
 - obligation de set sans « Give to » : `11018` Weakened (Kang), `60184` Wanted (`desc.GiveTo = ""`) ;
 - malus de heros : `GiveKeywordToInPlayWhenApplyThis(Hero, control_by="You", attack=-1, thwart=-1, defense=-1)` (`64009` pour le
   `control_by="You"`) ;
 - « After you resolve the Alter-Ego Action » : `AfterPlayerResolveAbility(..., which_abilities="AlterEgoAction", control_by_you=True)`
   (`27009`) ; cout `CostFunc.Discard("YourHandCards", range=(1, 1))`.

⚠ Mots-pieges :
 - « YOUR hero » : le heros du porteur de l'obligation, forme heros seulement (en alter-ego aucune stat ne bouge) ;
 - la Response porte sur l'Alter-Ego Action de VOTRE Bleeding Out (ld005), pas sur n'importe quelle action ;
 - « discard a card → discard this card » : le cout est la defausse d'une carte de la main, l'effet defausse l'obligation.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - ld010 Deep Wound : revelee, elle va au joueur et son HEROS a -1 ATK, -1 THW, -1 DEF (2/1/3 -> 1/0/2)
      - ld010 Deep Wound : SANS elle, le heros garde ATK 2, THW 1, DEF 3 (contre-cas des valeurs de base)
      - ld010 Deep Wound : en ALTER-EGO aucune stat de heros ne bouge (le malus vise le heros)
      - ld010 Deep Wound : Response, apres l'Alter-Ego Action de Bleeding Out, defausser une carte de la main defausse l'obligation
      Preuve par substitution : **rouges 2/4** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 40 parties (spider_man × lady_deathstrike standard, expert, rhino en témoin ; équilibré/agressif), grep tracebacks : 0 sur les 40 journaux. Journal lu : Bleeding Out saigne, le complot reçoit ses jetons. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ld011 : Bide Time (SideScheme)

```
Bide Time — MANIGANCE ANNEXE (x2). Menace de depart 2, Crisis 1, Boost 3.
When Defeated: The player who defeated this scheme resolves the "Special" ability on the copy of Bleeding Out attached to their identity.

Cartes de reference :
 - « When Defeated » d'une manigance annexe : `WhenSchemeBeDefeated(WhenDefeated, "This", op)` + `message.defeating_player`
   (`br012`, `gs120a`) ; `Crisis` : `desc.Crisis` natif (fiche mots-cles/crisis.md).

⚠ Mots-pieges :
 - icone du coin = CRISIS (glyphe `C` de ChampionsIcons.ttf, comparee a Crowd Control 01108) : tant qu'elle est en jeu, on ne peut pas
   retirer de menace du complot principal ;
 - « the player who DEFEATED » : celui qui a retire la derniere menace, PAS le joueur a qui elle a ete revelee ;
 - menace de depart fixe (2, aucune icone par joueur) ; trois icones Boost.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ld011 Bide Time : vaincue par le joueur (2 menaces, THW 2) -> Special sur SA copie (3 -> 4, deck 6 -> 2)
      - ld011 Bide Time : revelee, elle porte l'icone CRISIS (1) et 2 menaces
      Preuve par substitution : **rouges 1/2** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 40 parties (spider_man × lady_deathstrike standard, expert, rhino en témoin ; équilibré/agressif), grep tracebacks : 0 sur les 40 journaux. Journal lu : Bleeding Out saigne, le complot reçoit ses jetons. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : manigance annexe. Cas plateau : ui-app/src/board/lady-deathstrike-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ld012 : Stalking Prey (SideScheme)

```
Stalking Prey — MANIGANCE ANNEXE. Menace de depart 3, Hazard 1, Boost 2.
When Revealed: Place additional threat here equal to the number of bleed counters on the copy of Bleeding Out attached to your
  identity.

Cartes de reference :
 - menace posee a la revelation : `this.PlaceThreatOnSchemes([this], n, effect)` (`01107`) ; compteurs : `face.GetCounters('bleed')`.

⚠ Mots-pieges :
 - icone du coin = HAZARD (glyphe `H`, comparee a Breakin' & Takin' 01107) : une carte de rencontre de plus ;
 - « ADDITIONAL » : s'ajoute aux 3 menaces de depart ; « YOUR identity » : le joueur a qui la carte est revelee ;
 - sans copie de Bleeding Out (cas theorique) : +0 ;
 - homonyme `hs123`/`hs124` (Kraven) : ne jamais chercher par nom.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ld012 Stalking Prey : revelee, 3 menaces de depart + 3 (compteurs bleed de la copie du joueur) = 6
      - ld012 Stalking Prey : avec 5 compteurs bleed, 3 + 5 = 8 menaces
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 40 parties (spider_man × lady_deathstrike standard, expert, rhino en témoin ; équilibré/agressif), grep tracebacks : 0 sur les 40 journaux. Journal lu : Bleeding Out saigne, le complot reçoit ses jetons. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : manigance annexe a menace. Cas plateau : ui-app/src/board/lady-deathstrike-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ld013 : Lash Out (Treachery)

```
Lash Out — TRAITRISE (x2). SKILL. Boost 1 + etoile.
When Revealed: Lady Deathstrike attacks you (even if you are in alter-ego). Do not give her a boost card for this attack. If this
  attack deals any amount of damage, give Lady Deathstrike a tough status card.
[star] Boost: Give Lady Deathstrike a tough status card.

Cartes de reference :
 - `02030` I See You : `villain.DoAttackYou(joueur, effect, property=AttackProperty(do_not_give_boost=True))` ;
   `DoAttackYou(..., if_this_attack_deals_damage=fn)` (enemy.py) pour « if this attack deals damage » ;
 - `Faces.GiveStatus([vilain], "Tough", effect)` (`22006`) ; Boost etoile : `WhenCardBecomeBoost("This", op)` (`01154`).

⚠ Mots-pieges :
 - « even if you are in alter-ego » : l'attaque a lieu dans les deux formes (l'alter-ego encaisse) ;
 - « Do NOT give her a boost card » : `do_not_give_boost=True` ; « ANY amount of damage » : au moins 1 degat reel (une attaque
   entierement parree ne donne rien) ;
 - le Boost est un EFFET d'etoile : il donne Tough meme sans attaque revelee pour cette carte ;
 - « Lady Deathstrike » : le vilain (card_id), pas un sbire homonyme.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - ld013 Lash Out : revelee, Lady Deathstrike attaque (meme en alter-ego) : le joueur est blesse (2) -> Lady Deathstrike recoit un statut Tough
      - ld013 Lash Out : l'attaque est entierement PARÉE (allie) -> aucun degat, PAS de Tough
      - ld013 Lash Out : [star] Boost : revelee comme carte boost, Lady Deathstrike recoit un statut Tough
      Preuve par substitution : **rouges 2/3** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 40 parties (spider_man × lady_deathstrike standard, expert, rhino en témoin ; équilibré/agressif), grep tracebacks : 0 sur les 40 journaux. Journal lu : Bleeding Out saigne, le complot reçoit ses jetons. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ld014 : Mutant Hunter (Treachery)

```
Mutant Hunter — TRAITRISE (x2). SKILL. Boost 1.
When Revealed (Alter-Ego): Resolve the "Special" ability on the copy of Bleeding Out attached to your identity. This card gains surge.
When Revealed (Hero): Place 1 bleed counter on the copy of Bleeding Out attached to your identity. Lady Deathstrike attacks you.

Cartes de reference :
 - deux « When Revealed » selon la forme : `WhenThisRevealed("AlterEgo"?)` — modele `02030` I See You (`player.IsAlterEgo()`), `01124`
   Klaw (« When Revealed (Alter-Ego) ») ; `ThisCardGainSurge(effect)` (`nt015`, `ag013`) ;
 - attaque : `villain.DoAttackYou(joueur, effect)` (`ld013`) ; compteur : `Faces.PlaceCountersOn([saignement], 1, 'bleed', effect)`.

⚠ Mots-pieges :
 - UNE SEULE des deux branches selon la forme DU JOUEUR QUI REVELE (alter-ego : Special + surge ; heros : compteur + attaque) ;
 - forme HEROS : seulement +1 compteur bleed (PAS un Special : aucune defausse de deck) puis l'attaque normale (avec boost) ;
 - « This card gains surge » en alter-ego seulement.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ld014 Mutant Hunter : revelee en ALTER-EGO -> Special (3 -> 4, deck 6 -> 2) et SURGE (la carte suivante est aussi revelee)
      - ld014 Mutant Hunter : revelee en forme HEROS -> +1 compteur bleed (3 -> 4) SANS Special (deck intact) puis Lady Deathstrike attaque (2 degats)
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 40 parties (spider_man × lady_deathstrike standard, expert, rhino en témoin ; équilibré/agressif), grep tracebacks : 0 sur les 40 journaux. Journal lu : Bleeding Out saigne, le complot reçoit ses jetons. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ld015 : Integrated Augmentations (Attachment)

```
Integrated Augmentations — ATTACHEMENT (module Reaver Resources). TECH. WEAPON. ATK +1[star]. Boost 2.
Attach to the enemy with the highest printed ATK.
Attached enemy gains retaliate 1.
[star] Attached enemy's attacks gain ranged.
Hero Response: After you attack the attached enemy, spend [energy][mental] resources → discard this card.

Cartes de reference :
 - `40090` Heavy Armament (Military Grade) : MEME squelette (`AttachToFaceWhenPutIntoPlay(Enemy, highest_atk=True)`,
   `GiveKeywordToAttached(Enemy, retaliate=..)`, `AfterUnitAttackUnit(HeroResponse, "You", "AttachedEnemy", DiscardThisCard).SetCost(..)`) ;
   `32028` Unstoppable pour `highest_printed_atk=True` ; `50107b` M.O.D.O.K. pour `UnitAttackGainKeyword(..., ranged=True)`.

⚠ Mots-pieges :
 - « highest PRINTED ATK » : l'ATK IMPRIMEE (`highest_printed_atk`), pas l'ATK courante ; egalite : le moteur depart des cas ex aequo ;
 - `[energy][mental]` : DEUX types differents, `Cost("YB")` ; « After YOU attack the attached enemy » : le heros ;
 - ATK+ « 1* » (desc) : +1 ATK a l'ennemi porteur ; l'etoile = les attaques a distance.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (5 cas sujets) :
      - ld015 Integrated Augmentations : s'attache a l'ennemi de plus haute ATK IMPRIMEE (Lady Deathstrike II ATK 3 > Reaver Tracker ATK 2), qui gagne retaliate 1 et ATK +1
      - ld015 Integrated Augmentations : Hero Response, apres l'attaque du heros sur l'ennemi porteur, depenser [energy][mental] (Energy + Genius) defausse la carte
      - ld015 Integrated Augmentations : l'ennemi porteur riposte (retaliate 1) : le heros qui l'attaque prend 1 degat
      - ld015 Integrated Augmentations : [star] les attaques de Lady Deathstrike gagnent RANGED : un heros a Riposte (Black Panther) ne la blesse PAS
      - ld015 Integrated Augmentations : SANS l'augmentation, la meme attaque contre Black Panther (riposte 1) blesse Lady Deathstrike (contre-cas)
      Preuve par substitution : **rouges 4/5** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 40 parties (spider_man × lady_deathstrike standard, expert, rhino en témoin ; équilibré/agressif), grep tracebacks : 0 sur les 40 journaux. Journal lu : Bleeding Out saigne, le complot reçoit ses jetons. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : attachement sur un ennemi. Cas plateau : ui-app/src/board/lady-deathstrike-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ld016 : Titanium Exoskeleton (Attachment)

```
Titanium Exoskeleton — ATTACHEMENT (module Reaver Resources). ARMOR. TECH. Boost 2.
Attach to the enemy with the fewest remaining hit points.
Attached enemy cannot take more than 2 damage from a single attack.
Hero Action: Choose to either spend 3 resources of any type or remove a confused or stunned status card from attached enemy → discard this card.

Cartes de reference :
 - `40091` Titanium Exoskeleton (Military Grade, officiel) : TEXTE IDENTIQUE (FAQ de l'auteur : « 3 des memes cartes » que le modulaire
   officiel) ; script recopie tel quel : `AttachToFaceWhenPutIntoPlay(Enemy, fewest_remaining_hp=True)`,
   `UnitCannotTakeDamageWhile(NonKeyword, "AttachedEnemy", cannot_take_more_than_damage=2, is_from_attack=True)`,
   `PlayerActionToDiscardThis(HeroAction).SetCostFunc(CostFunc.Custom(None, fn))` + `ForChoiceAbilityWithCost(Cost("3"))`.

⚠ Mots-pieges :
 - « from a SINGLE attack » : le plafond de 2 vaut PAR attaque (les degats hors attaque ne sont pas plafonnes) ;
 - « fewest REMAINING hit points » : PV restants, pas imprimes ; « Choose to either » : un seul des deux couts, au choix ;
 - homonyme `40091` (Military Grade) : meme nom, set different, jamais cherche par nom.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - ld016 Titanium Exoskeleton : s'attache a l'ennemi qui a le MOINS de PV restants (Reaver Tracker 3 PV < Lady Deathstrike 16)
      - ld016 Titanium Exoskeleton : l'ennemi porteur ne prend pas plus de 2 degats d'une meme attaque (Haymaker 3 -> 2)
      - ld016 Titanium Exoskeleton : SANS l'exosquelette, Haymaker (3) acheve le Reaver Tracker (3 PV) : contre-cas
      Preuve par substitution : **rouges 2/3** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 40 parties (spider_man × lady_deathstrike standard, expert, rhino en témoin ; équilibré/agressif), grep tracebacks : 0 sur les 40 journaux. Journal lu : Bleeding Out saigne, le complot reçoit ses jetons. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : attachement sur un ennemi. Cas plateau : ui-app/src/board/lady-deathstrike-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ld017 : Inhibitor Collar (Attachment)

```
Inhibitor Collar — ATTACHEMENT (module Reaver Resources, x2). TECH. ATK -1. Boost 1.
Attach to your identity.
Treat your identity's printed text box as if it were blank (except for traits).
Action: Choose to either exhaust a character you control or take 3 damage → discard this card. (Any player can do this.)

Cartes de reference :
 - `40092` Inhibitor Collar (Military Grade, officiel) : TEXTE IDENTIQUE ; script recopie tel quel : `AttachToFaceWhenPutIntoPlay("YourIdentity")`,
   `GiveKeywordToAttached("Character", treat_as_blank=True)`, `PlayerActionToDiscardThis(Action).SetCostFunc(CostFunc.Custom(None, fn))
   .AnyPlayerCanDoThis()` ; `ATK+ -1` natif de `desc`.

⚠ Mots-pieges :
 - « (except for TRAITS) » : seuls les mots du cadre de texte sont ignores ; « Any player can do this » : le cout est paye par le joueur qui agit
   (son personnage epuise, SES 3 degats), meme si le collier est sur l'identite d'un autre ;
 - 2 exemplaires : peuvent etre attaches a la MEME identite (ATK -2) ;
 - homonyme `40092` : jamais cherche par nom.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - ld017 Inhibitor Collar : s'attache a l'IDENTITE du joueur, ATK -1 (alter-ego : le collier est attache, aucun effet de stat)
      - ld017 Inhibitor Collar : Action, epuiser un personnage (le heros) defausse le collier
      - ld017 Inhibitor Collar : Action, l'autre branche : 3 degats a l'identite defaussent aussi le collier
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 40 parties (spider_man × lady_deathstrike standard, expert, rhino en témoin ; équilibré/agressif), grep tracebacks : 0 sur les 40 journaux. Journal lu : Bleeding Out saigne, le complot reçoit ses jetons. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : attachement sur l'identite. Cas plateau : ui-app/src/board/lady-deathstrike-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ld018 : Chop-Shop Cybernetics (SideScheme)

```
Chop-Shop Cybernetics — MANIGANCE ANNEXE (module Reaver Resources). Menace de depart 3, Amplify 1, Hinder 1 par joueur, Boost 3.
Hinder 1[per_hero].
Forced Response: After a TECH attachment enters play, give the villain and the attached enemy a tough status card.

Cartes de reference :
 - `Hinder`, `Amplify` : natifs de `desc` (fiches mots-cles/hinder.md, amplify.md ; `16066` Blockade, `16054` Vendetta) ;
 - « After an attachment attaches » : `AfterCardAttachTo(ForcedResponse, CardFinder(card_type=Attachment, trait="TECH"), ..., op)`
   (`message.upgrade` = l'attachement, `message.to_face` = le porteur) ; `Faces.GiveStatus(cibles, "Tough", effect)`.

⚠ Mots-pieges :
 - icone du coin = AMPLIFY (glyphe `F`, comparee a Vendetta 16054) : chaque icone Boost d'une carte boost recoit +1 par manigance Amplify ;
 - DECISION UTILISATEUR (25/10/2026) : « the attached enemy » = l'ENNEMI sur lequel le TECH vient de s'attacher, s'il y en a un ; un TECH
   pose sur une IDENTITE (Inhibitor Collar) ne donne Tough qu'au VILAIN ; si le porteur EST le vilain, il n'a qu'UN statut ;
 - « the VILLAIN » : le vilain en jeu (Lady Deathstrike), pas un sbire.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - ld018 Chop-Shop Cybernetics : revelee, 3 menaces de depart + Hinder 1 par joueur = 4, icone AMPLIFY 1
      - ld018 Chop-Shop Cybernetics : un attachement TECH s'attache a un SBIRE (Integrated Augmentations sur Reaver Tracker) -> le vilain ET le sbire recoivent Tough
      - ld018 Chop-Shop Cybernetics : un TECH pose sur l'IDENTITE du joueur (Inhibitor Collar) -> le vilain seul recoit Tough (decision du 25/10/2026)
      - ld018 Chop-Shop Cybernetics : un attachement qui n'est PAS TECH (Reinforced Claws) ne donne aucun Tough
      Preuve par substitution : **rouges 2/4** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 40 parties (spider_man × lady_deathstrike standard, expert, rhino en témoin ; équilibré/agressif), grep tracebacks : 0 sur les 40 journaux. Journal lu : Bleeding Out saigne, le complot reçoit ses jetons. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : manigance annexe a menace. Cas plateau : ui-app/src/board/lady-deathstrike-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).
