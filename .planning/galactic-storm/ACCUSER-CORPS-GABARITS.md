# Gabarits PROCESSUS-CARTE.md — Modulaire Accuser Corps (gs156-gs160), lot GS-6

Preuves : `Fusion/marvel-lcg-src/tools/cas/accuser_corps.py` (filtre `[ac]`), rapport `/tmp/ac_final.json`,
bilan **5/9 cas verts**. `test_cards` / `verifier_appels_modules` : voir HALA-ULTIMATUM-GABARITS.md (même
pack `galactic_storm`, même run). Autoplay : Accuser Corps est le modulaire déclaré par défaut dans
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
- [ ] Étape 7 : `[ac] gs156 Forced Interrupt` (le +1 ATK) et son TEMOIN sont **ROUGES** (« degats sur
      l'identite = 0 » dans les deux cas, avec ET sans la carte) : l'attaque de test
      (`Puzzle.Attack('gs138b')`) n'inflige aucun dégât mesuré dans ce montage — cause non élucidée faute
      de temps (possible défense automatique du pilote de test, ou ciblage par défaut différent de
      l'identité). `[ac] gs156 Forced Response` (défausse après un ennemi ACCUSER CORPS vaincu) également
      **ROUGE** (« gs156 est encore en jeu »), alors que le TEMOIN symétrique (sans le trait, la carte
      reste) est VERT — suggère que le déclencheur `WhenUnitBeDefeated` avec un `CardFinder(trait=...)`
      part bien dans un sens (rien ne se passe à tort) mais pas dans l'autre (devrait partir, ne part
      pas) : piste à reprendre en priorité (peut-être le trait ACCUSER CORPS n'est pas lu correctement
      sur gs159 au moment de sa défaite, ou le timing `ForcedResponse` après la fin de combat).
- **Carte terminée : NON** — deux capacités sur trois non prouvées, à corriger/revérifier avant mise en
  partie réelle. Points à vérifier en priorité listés ci-dessus.

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
- [ ] Étape 7 : `[ac] gs160 ... un ennemi ACCUSER CORPS en jeu` **ROUGE** (« degats sur l'identite = 0 »),
      même famille de souci que gs156 (dégâts non mesurés après une activation forcée — à reprendre avec
      la même investigation). `[ac] gs160 ... AUCUN ennemi` (branche de repli, recherche + révélation)
      **VERT**.
- **Carte terminée : NON** — branche de repli prouvée, branche principale (activation contre vous) non
  prouvée pour la raison ci-dessus, à corriger avant mise en partie réelle.

---

## Pistes à reprendre en priorité (hors périmètre du temps disponible pour ce lot)

1. **gs156 et gs160 : « degats sur l'identite = 0 »** après une activation forcée par script
   (`DoActivate`) contre un joueur dont l'identité est en jeu (via `HEROS`). À vérifier : le pilote de
   test choisit-il automatiquement de DÉFENDRE (ramenant les dégâts à 0 par la défense de base du héros),
   ou l'activation ne cible-t-elle pas réellement l'identité ? Comparer avec `[hu] gs155` (qui mesure
   `cartes_distribuees` plutôt que `degats_identite` pour la MÊME primitive `DoActivate`, et PASSE) — la
   différence de méthode de mesure est peut-être la clé.
2. **gs156 Forced Response** (défausse après la défaite d'un ennemi ACCUSER CORPS) : le TEMOIN symétrique
   passe (rien ne se passe à tort) mais le cas principal ne part pas. Vérifier que `gs159.HasTrait("ACCUSER
   CORPS")` est bien lisible AU MOMENT PRÉCIS du message `WhenUnitBeDefeated` (le trait est déclaré dans
   `desc.traits` de `accuser_corps_cards.py`, confirmé présent dans `cards.json` après insertion).
