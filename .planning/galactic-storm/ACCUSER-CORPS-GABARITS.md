# Gabarits PROCESSUS-CARTE.md — Modulaire Accuser Corps (gs156-gs160), lot GS-6

Preuves : `Fusion/marvel-lcg-src/tools/cas/accuser_corps.py` (filtre `[ac]`), bilan **9/9 cas verts**
(20/10/2026, après correctifs — voir HALA-ULTIMATUM-GABARITS.md pour le détail du correctif majeur de
cache `.game`, commun aux deux fichiers). `test_cards` : 6970/6970. `verifier_appels_modules
galactic_storm` : OK. Autoplay : Accuser Corps est le modulaire déclaré par défaut dans
`data/scenarios/gs_hala_ultimatum*.json` (« modular_sets »: ["gs_accuser_corps"]) : les 8 parties
d'autoplay du scénario 3 l'incluent déjà (voir HALA-ULTIMATUM-GABARITS.md). Un journal réel montre Kree
Accuser (gs159) attaquer et se faire attribuer Kree Resilience (gs146, Hala Ultimatum) comme carte de
boost — confirme que les deux ensembles se mélangent correctement dans la même partie.

## gs156 : The Accused

- [x] Étape 2 : `AttachToFaceWhenPutIntoPlay("YourIdentity")` (modèle tx018 Intruder Alert!) ;
      `WhenUnitWouldAttack` + `message.GainATKForThisAttack(1, effect)` (modèle OFFICIEL cw 56017 Savage
      Strike) restreint au joueur attaché via `message.against_player` ; `WhenUnitBeDefeated(ForcedResponse,
      CardFinder(trait="ACCUSER CORPS"), ...)` + `Faces.DiscardAll` ; Boost via `AttachTo2`.
- [x] Étape 5-6 : conforme au texte transcrit.
- [x] Étape 7 : les trois capacités sont VERTES (20/10/2026). Confirmé par sonde : la cause du « degats
      sur l'identite = 0 » était EXACTEMENT la piste anticipée en §1 ci-dessous — le pilote de test choisit
      TOUJOURS de défendre avec le DEF de base de l'identité (3), qui absorbe l'ATK de base de Tanalth
      stade I (2) et stade II (3), quel que soit l'effet testé. Stade III (ATK 4) est nécessaire pour un
      résidu mesurable mais n'existe PAS en mode normal (« Contents » de gs141a : réservé au mode expert) —
      `Puzzle.AdvanceVillain()` au-delà du stade II vide le deck des méchants et termine la partie.
      Solution retenue : `Puzzle.EnemyAttacks(..., additional_attack=2)` simule un ATK de base plus élevé
      sans toucher au stade ni aux cartes boost, pour une marge mesurable au-dessus de DEF 3
      (`[ac] gs156 Forced Interrupt` et son TEMOIN, tous deux VERTS). `[ac] gs156 Forced Response` : le
      déclencheur partait bien dans les DEUX sens (le trait ACCUSER CORPS est lu correctement) — la cause
      réelle était que le cas, SANS `DECK_NEUTRE`, laissait un second exemplaire de gs159 (2 copies dans le
      set modulaire) dans le deck de rencontre réel ; `Puzzle.Damage('gs159', 10)` (via `FindOrCreateFace`,
      qui fouille le deck AVANT les cartes en jeu) frappait CETTE copie non en jeu, sans effet visible ni
      trace au journal. `DECK_NEUTRE` ajouté + un second `Puzzle.Damage` (gs159 porte Toughness 1, qui
      absorbe le premier coup fatal) : VERT.
- **Carte terminée : OUI** — les trois capacités imprimées sont prouvées directement.

## gs157 : Universal Weapon

- [x] Étape 2 : `AttachToFaceWhenPutIntoPlay(Villain)` + `GiveKeywordToAttached("Character",
      trait="ACCUSER CORPS", steady=1)` (modèle baxter_stockman tx006 pour `trait=`) ; coût composite
      `CostFunc.TakeDamage(2, "YourIdentity")` + `CostFunc.DealPlayerEncounterCard(1, "Initiator")`
      (chaînage de deux `SetCostFunc`, confirmé additif par le moteur — `ability.py:1052`) ; effet
      `Faces.ShuffleAllTo` (pas `DiscardAll` : « shuffle into the encounter deck », pas une défausse).
- [x] Étape 5-6 : conforme.
- [x] Étape 7 : `[ac] gs157 Hero Action` **VERT** (2 dégâts sur l'identité, carte mélangée dans le deck
      rencontre, la carte quitte le jeu). Preuve directe du coût composite ET de l'effet, pas de
      substitution formelle faite (temps).
- [x] Étape 8 : autoplay conforme (scénario hôte).

**Carte terminée : OUI** pour le Hero Action (preuve verte directe) ; l'attache initiale au mechant et le
don de trait/steady n'ont pas de cas séparé (triviaux, modèle déjà prouvé ailleurs dans le pack).

## gs158 : Unwavering

- [x] Étape 2 : `AttachToFaceWhenPutIntoPlay(Enemy)` ; `AfterUnitAttackAndDamageUnit(ForcedResponse,
      "AttachedEnemy", "Character", ...)` (modèle gs076 Kree Sentry, adapté à « AttachedEnemy ») ;
      `Faces.DiscardAll` ; Boost via `AttachTo2`.
- [x] Étape 5-6 : conforme (le badge ATK +3[star] est natif, `desc.ATK+`).
- [x] Étape 7 : `[ac] gs158 Forced Response` **VERT** (l'ennemi porteur attaque et blesse un personnage ->
      la carte se défausse). Pas de TEMOIN ni substitution formelle (temps).
- [x] Étape 8 : autoplay conforme.

**Carte terminée : OUI** pour la Réponse forcée (preuve verte directe, un seul aller-retour non
substitué) ; le Boost n'a pas de cas dédié.

## gs159 : Kree Accuser

- [x] Toughness + Villainous natifs (desc), aucun module requis.
- [x] Étape 7 : `[ac] gs159 Kree Accuser` **VERT** (1 dégât absorbé par Toughness, 0 dégât final).
- [x] Étape 8 : autoplay — Kree Accuser VU attaquer dans un journal réel.

**Carte terminée : OUI.**

## gs160 : Judgement Day

- [x] Étape 2 : `face.DoActivate(joueur, effect)` par ennemi ACCUSER CORPS trouvé (modèle officiel 11051
      Ancient Grudge) ; branche de repli `Search.EncounterCard(..., trait="KREE", card_type=Minion)`
      (modèle gs141a, même pack).
- [x] Étape 5-6 : conforme.
- [x] Étape 7 : les deux branches sont VERTES (20/10/2026). Confirmé par sonde : le pilote de test
      choisit TOUJOURS de défendre avec le DEF de base (3), qui absorbe l'ATK natif de gs159 (2) — exactement
      la piste anticipée en §1 ci-dessous. Impossible d'utiliser `additional_attack` ici (l'activation part
      du SCRIPT de gs160 via `face.DoActivate`, pas d'un `Puzzle.EnemyAttacks` qu'on contrôle). Trouvaille
      en prime : `Enemy.DoActivate` bifurque ATTAQUE/MANIGANCE sur `against_player.IsAlterEgo()`
      (`enemy.py:327`) — sans `HEROS`, Peter Parker en alter-ego fait COMPLOTER gs159 au lieu de
      l'attaquer (confirmé au journal : menace posée sur la manigance principale, PAS la branche à
      prouver). Preuve retenue : AVEC `HEROS`, la menace de la manigance principale (gs141b) ne bouge PAS
      — preuve indirecte mais univoque que la branche ATTAQUE (et non MANIGANCE) a bien été prise.
      `[ac] gs160 ... AUCUN ennemi` (branche de repli, recherche + révélation) VERT, déjà correct.
- **Carte terminée : OUI** — les deux branches sont prouvées (preuve indirecte mais univoque pour la
  branche principale, les dégâts bruts restant hors de portée du harnais pour la même raison que gs156).

---

## Pistes résolues le 20/10/2026 (anciennement « à reprendre en priorité »)

1. **gs156 et gs160 : « degats sur l'identite = 0 »** après une activation forcée par script
   (`DoActivate`) contre un joueur dont l'identité est en jeu (via `HEROS`). RÉSOLU : le pilote de test
   choisit bien TOUJOURS de défendre avec le DEF de base (3), confirmé par sonde (`Puzzle.EnemyAttacks`
   avec `players_may_defend=False` ne change rien quand la cible est un personnage ami — ce kwarg n'agit
   QUE sur les attaques contre une cible ennemie, voir `enemy.py:242` « Cible ALLIEE : le contrôleur ...
   PEUT défendre »). Pour gs156, contournement par `additional_attack=2` (kwarg disponible via
   `Puzzle.EnemyAttacks`) ; pour gs160 (activation non pilotée par `Puzzle.EnemyAttacks`), preuve
   indirecte par la menace de la manigance principale (voir ci-dessus). `[hu] gs155` (qui PASSE en
   mesurant `cartes_distribuees`) s'en sort parce que son activation redirige vers une distribution de
   carte (mécanique HIDDEN), jamais vers un dégât brut comparable à du DEF — pas une différence de méthode
   de mesure, une différence d'EFFET réel.
2. **gs156 Forced Response** (défausse après la défaite d'un ennemi ACCUSER CORPS) : RÉSOLU. Le
   déclencheur partait bien dans les deux sens (le trait ACCUSER CORPS est lu correctement sur gs159 au
   moment de sa défaite). La cause réelle : `Puzzle.Damage('gs159', 10)` frappait un second exemplaire de
   gs159 resté dans le deck de rencontre réel (2 copies dans le set modulaire, `DECK_NEUTRE` absent du
   cas) — `FindOrCreateFace` fouille le deck de rencontre AVANT les cartes en jeu, sans effet visible ni
   trace au journal sur la copie réellement en jeu. `DECK_NEUTRE` ajouté au cas, plus un second
   `Puzzle.Damage` (gs159 porte Toughness 1, qui absorbe le premier coup fatal avant la vraie défaite).
