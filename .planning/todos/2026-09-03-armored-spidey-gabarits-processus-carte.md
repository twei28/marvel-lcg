# PROCESSUS-CARTE.md — les 28 gabarits du pack ARMORED SPIDEY (set 152, `as`)

Gate de `PROCESSUS-HEROS.md` : un gabarit rempli par carte. Rédigés le
03/09/2026. Auteur du pack : **Kajislav**.

**Preuves communes**, citées une fois :

- **Étape 7, substitution** : `substituer_pack.py .game-src 56600 as0` →
  **28/28 cartes prouvées**, chacune avec au moins un cas qui tombe au rouge
  quand son module disparaît. Quatre cas restent verts sans module, et les
  quatre sont des **contre-cas d'ABSENCE d'effet**, assumés ici :
  `as012` (armure détruite, le bonus de CTR disparaît), `as013` (armure
  détruite, ni Riposte ni pion posé), `as022` (condition de mise en jeu — un
  soutien reste jouable même sans capacité `Play`) et `as024` (le pion article
  qui n'est PAS posé). Chacun a son cas jumeau nominal, lui au rouge.
- **Étape 7, cas** : `test_capacites.py [as0]` → **43/43 cas verts**. Sept
  d'entre eux ont dû être corrigés après lecture du journal, et aucune de ces
  sept corrections ne portait sur un module (voir §Ce que la batterie a appris).
- **Étape 8, autoplay** : voir §Bilan autoplay en fin de fichier.
- **Étape 4, image** : `assets/pics/as0*.png` pour les 28, découpées du zip
  `Armored Spidey (Released)-20260902T070129Z-1-001.zip` (38 fichiers, 27 cartes
  distinctes + les deux faces du feuillet de deck : Embrace It! ×2, Kick It! ×2,
  Sense It! ×2, Swing It! ×2, Underworld Impact ×2).
- **Étape 1** : pack `armored_spidey` en queue de `cards.json`, set
  `152. Custom (Armored Spidey)` dans `sets_info.json`, préfixe `as` déclaré,
  checksums recalculés, `verifier_prefixes` OK.
- `test_cards` : **5144 ok / 0 erreur** (5116 avant le pack, +28).
- `verifier_appels_modules` : « tous les appels de armored_spidey existent ».
- `verifier_cartes_en_jeu` : « les 28 cartes de armored_spidey portent ce que
  leur texte annonce ».
- **Étape 10 de PROCESSUS-HEROS** : contrôle relancé sur les **115 decks de
  départ** → **0 écart**.
- **Les 27 scans ont été relus un par un** avant la première ligne de code, et
  les icônes de ressource croisées à l'intérieur du pack (leçon Lockjaw).

**Trois compteurs et deux traits maison** ont dû être ajoutés aux énums du
moteur (`src/game/card/face/card_face.py`) : compteurs `metal`, `sense`,
`article` ; traits `OPERATIONAL` et `DESTROYED`. Sans eux, `IsCounter` et
`IsTrait` refusent le nom et **la carte tombe à la construction**, pas en jeu.

**Premier pack de la série à fournir sa decklist.** Kajislav donne le deck de
départ carte par carte (scans « 48/49 starter deck armored spidey »), aspect
**PROTECTION** : aucune question d'aspect n'a été posée, contrairement à
`hulk_rainy`, `lady_sif` et `iron_man_model_42`.

**Trois décisions de l'utilisateur**, prises le 03/09/2026 :

1. `as020` **Double Defense** : texte imprimé contradictoire (« Hero
   **Response** » mais « **When** … **would take** »). Décision : on suit le
   DÉCLENCHEUR, la carte est une **INTERRUPTION**. Une fois les dégâts subis
   il n'y a plus de « that amount » à réduire, et les trois cartes officielles
   au même texte (01098, im007) sont toutes des interruptions.
2. `as025` **Underworld Impact** : le « for each support you control » porte
   sur **LES DEUX** options du choix. La clause « If you do not control any
   supports, this card gains surge » le confirme.
3. **La carte « 28 Spider-Man »** de la decklist, non fournie par l'auteur :
   c'est un allié OFFICIEL (la numérotation des fichiers custom saute
   exactement les places des cartes officielles). Quatre candidats de classe
   Basic portent ce nom. **27049 est écarté** — son sous-titre est « Peter
   Parker », l'identité civile du héros, et on ne met pas deux fois la même
   personne à la table. Retenu : **13019 (Miles Morales)**.

---

## Ce que la batterie a appris (7 cas corrigés, 0 module en cause)

Aucune de ces sept corrections ne touchait un module : toutes portaient sur le
montage du cas. Elles sont consignées parce qu'elles se reproduiront.

1. **`as007`** — la main finissait à 3, pas 2 : `as001b` Egomaniac pioche
   AUSSI une carte quand un événement est joué. Les capacités du pack se
   cumulent.
2. **`as010`** — Gwen Stacy posée PRÊTE résout sa propre Réponse à vide sur sa
   propre arrivée et **brûle la limite du round** (journal : « Gwen Stacy
   activates, targets Gwen Stacy »). Le pilote ne sait pas DÉCLINER une
   Réponse facultative, là où un joueur humain la garderait. Le cas passe donc
   par `PutIntoPlay(..., exhaust=True)`, qui incline AVANT
   l'`AfterCardEnterPlay` (face_on_event.py:189).
3. **`as011`** — `main_exclusive` **défausse la main de départ** (6 cartes)
   avant de poser la sienne : la défausse du joueur finit à 8, pas à 2.
4. **`as015`** — l'allié posé PRÊT se déclare DÉFENSEUR et le héros ne subit
   plus rien. Même piège que `im007`, une marche plus loin : il faut incliner
   le héros ET l'allié.
5. **`as018`** — l'attaquant portait GARDE, ce qui rend le vilain **cible
   illégale** pour une riposte libellée `(attack)`. Attaquant remplacé par
   `01103` * Shocker.
6. **`as019`** — `Puzzle.Damage(sbire, 5)` tue bien le sbire, mais l'effet
   debug n'a **pas de joueur initiateur** et la Réponse n'est jamais proposée.
   Il faut une VRAIE attaque.
7. **`as023`** — la menace de départ du complot annexe (2) plus son Entrave 1
   le posent DÉJÀ à 3 : un seuil `menace_min` à 3 passait au vert **même sans
   le module**. Trouvé par la preuve par substitution, pas par la batterie.
   Et le remettre à ZÉRO le VAINC : il quitte le jeu avant la manigance.

**Un seul correctif de module est sorti de la batterie** : `as012`
`UnitIgnoreKeywordIcons` prenait `"You"`, que le moteur convertit en `"This"`
puis compare à `effect.this` — c'est-à-dire l'amélioration porteuse, jamais le
héros qui attaque. L'exemption ne s'appliquait donc **jamais**, et le héros
restait bloqué par Garde. Corrigé en `CardFinder(name="Armored Spidey")`.
⚠ Le montage `"You"` d'`im013` ne marche que parce qu'il enregistre l'abilité
EN TEMPORAIRE depuis l'interruption — **et son cas de test ne vérifie pas
l'exemption elle-même**.

**Un défaut ANTÉRIEUR trouvé au passage** : `verifier_tous_les_decks` a révélé
que le deck **`lady_sif` ne montait plus AUCUNE partie** depuis son portage de
la veille — `ls005` To Arms! porte deux capacités `Play` et manquait dans la
liste blanche de `factory.py`. `AssertionError` au setup, invisible pour
`test_cards`, `test_capacites` et `substituer_pack`. **Seul
`verifier_tous_les_decks` le voit, et il n'avait pas été relancé après ce
pack.** Corrigé.

---

## Gabarits, carte par carte

Les blocs « étape 2 » (carte de référence) et « étape 5 » (texte-contre-code)
sont écrits **en tête de chaque module**, avec le POURQUOI de chaque choix et
la liste des mots-pièges vérifiés. Ce fichier ne les recopie pas : il donne le
verdict et ce qui est propre à la carte.

### as001a : * Armored Spidey (face héros)

- [x] Étape 2 : `im007` Energy Shield (même phrase au compteur près), `01098`
      Armored Rhino Suit ; `CostFunc.Counter` pour le coût.
- [x] Étape 5 : mots-pièges `from an attack` (≠ « any amount » d'im007), `you`,
      la flèche = COÛT, `up to 2`. Résultat : conforme.
- [x] Étape 6 : PV 10, ATQ 2, CTR 2, DEF 2, main 5, 1 pion metal, 2 dégâts
      prévenus — identiques dans `cards.json` et le script.
- [x] Étape 7 : cas « un pion metal prévient les 2 dégâts de Rhino »,
      rouge 1/1 sans module.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as001b : * Peter Parker (face alter-ego)

- [x] Étape 2 : `34001b` * Jean Grey (MÊME phrase de Setup), `31002a` pour
      `flip_to_trait`, `17022` pour la Réponse.
- [x] Étape 5 : `a player plays a card UNDER YOUR CONTROL` (deux joueurs dans
      la même phrase), `once per round PER PLAYER` (≠ as010). Résultat :
      conforme.
- [x] Étape 6 : PV 10, REC 3, main 6, 3 pions metal, pioche 1.
- [x] Étape 7 : 2 cas (Setup, Egomaniac), rouges 2/2.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as002a : Spider Armor (face [[OPERATIONAL]])

- [x] Étape 2 : `34002a` Phoenix Force (même phrase au compteur près),
      `45075b` pour `AfterFlipToThisFace`.
- [x] Étape 5 : `the LAST metal counter`, `flip TO THIS SIDE`, `here`,
      `Permanent` (base automatique, aucun script). Résultat : conforme.
- [x] Étape 6 : 3 pions metal.
- [x] Étape 7 : 2 cas (destruction, rechargement), rouges 2/2.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as002b : Spider Armor (face [[DESTROYED]])

- [x] Étape 2 : `34002b` Phoenix Force, `32179` / `40122a` pour
      `SetCost(Cost("3"))`.
- [x] Étape 5 : **ARMORED SPIDEY** = nom propre → `CardFinder(name=...)` et
      pas `"You"` (piège an002) ; `of ANY type` ≠ `same_type`. Résultat :
      conforme.
- [x] Étape 6 : -1 ATQ, -1 DEF, 3 ressources.
- [x] Étape 7 : 2 cas (malus, réparation), rouges 2/2.
      ⚠ Le contre-cas en forme CIVILE est structurellement impossible à
      observer : la face alter-ego n'a ni ATQ ni DEF, ce qui est précisément
      ce qui rend `CardFinder(name=...)` sûr.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as003 : * Spider-Bot

- [x] Étape 2 : `08018` Spycraft pour `CostFunc.Discard("This")`, `32030b`
      Kitty Pride pour le retournement.
- [x] Étape 5 : `to its OPERATIONAL side` (≠ « flip it ») → test de trait
      avant retournement ; `Toughness` base automatique ; « Action » NUE.
      Résultat : conforme.
- [x] Étape 6 : coût 4, PV 3, CTR 1*, ATQ 3**, Robustesse 1.
- [x] Étape 7 : cas « se défausser remet l'armure sur OPERATIONAL », rouge 1/1.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as004 : Burst It!

- [x] Étape 2 : `42018` * Angel's Aerie (`RemoveEachCounter` +
      `return_remove_counter`), `01053` pour les dégâts de zone.
- [x] Étape 5 : `Remove EACH` = COÛT ; `for each … THIS WAY` = ce que le coût
      a réellement enlevé ; `each enemy in play` sans restriction d'engagement ;
      Hero Action SANS libellé. Résultat : conforme.
- [x] Étape 6 : coût 0, 1 dégât par pion.
- [x] Étape 7 : cas « 3 pions = 3 dégâts à chaque ennemi », rouge 1/1.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as005 : Embrace It!

- [x] Étape 2 : `34002a` pour `AfterCardRemovedCounter`, `ls005` pour la garde
      `IsHero()`.
- [x] Étape 5 : `ready your IDENTITY` (≠ « your hero ») → `GetIdentity()`,
      jamais `GetHero()` qui lève un assert avalé par le moteur ; `After YOU
      remove` → filtre multijoueur. Résultat : conforme.
- [x] Étape 6 : coût 0.
- [x] Étape 7 : cas « retirer un pion redresse l'identité », rouge 1/1.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as006 : Kick It!

- [x] Étape 2 : `05015` Tackle, `im002` pour le « you may » payé en compteur.
- [x] Étape 5 : `stun THAT enemy` = MÊME cible (≠ as009) ; le retrait est dans
      le CORPS parce que l'effet principal tombe de toute façon ; `(attack)`.
      Résultat : conforme.
- [x] Étape 6 : coût 2, 4 dégâts, 1 pion.
- [x] Étape 7 : cas « 4 dégâts et le pion étourdit la MÊME cible », rouge 1/1.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as007 : Sell It!

- [x] Étape 2 : `CostFunc.Counter` en forme TUPLE (`DeclareNumber`), `42018`
      pour le décompte.
- [x] Étape 5 : `draw 2 cards` PAR pion ; `Alter-Ego Action`. Résultat :
      conforme.
      ⚠ **Écart assumé** : « any number » inclut littéralement ZÉRO, mais le
      retrait est monté en COÛT avec un minimum de 1. Choix délibéré : la forme
      « jouable pour rien » est exactement le motif qui a bloqué une partie sur
      32 en autoplay au pack `iron_man_model_42`.
- [x] Étape 6 : coût 2, 2 cartes par pion, maximum 3 pions.
- [x] Étape 7 : cas « 1 pion retiré = 2 cartes piochées », rouge 1/1.
      ⚠ Le pilote répond TOUJOURS le minimum à `DeclareNumber`.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as008 : Sense It!

- [x] Étape 2 : `im011` Save The Day / `dz013` Velvet Sky pour l'annulation,
      `15004` pour le décompte d'icônes de boost.
- [x] Étape 5 : `cancel ALL` (≠ `WhenRevealed`, leçon dz013) ; `FROM THE
      ENCOUNTER DECK` (≠ im011) ; `for each boost icon DISCARDED THIS WAY` ;
      `or` = un choix entre deux effets nommés. Résultat : conforme.
- [x] Étape 6 : coût 1, 1 pion, 1 dégât ou 1 menace par icône.
- [x] Étape 7 : cas « la traîtrise est annulée et le pion frappe le vilain »,
      rouge 1/1.
      ⚠ Arbitrage technique : les deux options sont proposées dans UNE SEULE
      question. Deux questions enchaînées ont bloqué une partie d'autoplay au
      pack `lady_sif`.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as009 : Swing It!

- [x] Étape 2 : `08013` Stealth Strike pour le SECOND ciblage, `im002` pour le
      « you may ».
- [x] Étape 5 : `confuse AN enemy` = deuxième choix (≠ as006) ; `a scheme` =
      principal ou annexe ; `(thwart)`. Résultat : conforme.
- [x] Étape 6 : coût 2, 3 menaces, 1 pion.
- [x] Étape 7 : cas « 3 menaces retirées et un AUTRE ennemi désorienté »,
      rouge 1/1.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as010 : * Gwen Stacy

- [x] Étape 2 : `17022` * Knowhere, `ab007` * Donald Pierce (même auteur) pour
      la ressource.
- [x] Étape 5 : `ENTERS PLAY` (≠ « is played ») ; `PRINTED cost` ; `under YOUR
      control` ; `once per ROUND` GLOBALE (≠ as001b). Résultat : conforme.
- [x] Étape 6 : coût 3, seuil 2, ressource [wild].
- [x] Étape 7 : 2 cas (Réponse, Ressource), rouges 2/2.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as011 : * Parker Industries

- [x] Étape 2 : `lj005` * Kamala's Room (MÊME texte) et son correctif du
      9/8/2026 ; `01029b` pour le même texte sans inclinaison.
- [x] Étape 5 : `DISCARD the others` (≠ « bottom of your deck », 15007) ;
      relever le dessus AVANT la recherche ; `Alter-Ego Action`. Résultat :
      conforme.
- [x] Étape 6 : coût 1, 3 cartes regardées, 1 gardée.
- [x] Étape 7 : cas « 3 cartes regardées, 1 gardée, 2 défaussées », rouge 1/1.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as012 : Night Vision

- [x] Étape 2 : `50093` Embassy Guard / Alert Level (condition continue sur une
      carte recto-verso), `32002` * Shadowcat pour l'exemption.
- [x] Étape 5 : **ARMORED SPIDEY** = nom propre ; `WHILE` = condition continue,
      d'où `change_on_event` ; `guard AND patrol` et RIEN d'autre (pas de
      `crisis`, alors que le modèle Shadowcat coche les trois). Résultat :
      conforme **après correctif** (voir §Ce que la batterie a appris).
- [x] Étape 6 : coût 1, +1 CTR.
- [x] Étape 7 : 3 cas (bonus, contre-cas armure détruite, exemption de Garde),
      rouges 2/3 — le contre-cas d'absence reste vert, assumé.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as013 : Vibranium Enhancement

- [x] Étape 2 : `50093` pour la condition continue, `bt012` / `50144` pour les
      mots-clés donnés, `AfterYouPlayThisFromHand`.
- [x] Étape 5 : nom propre ; `IF … OPERATIONAL` lu À LA RÉSOLUTION ; `to a
      MAXIMUM of 3` ; `on IT` = l'amélioration ; Riposte et Stoïque sont des
      bases automatiques qu'on DONNE, jamais qu'on recode. Résultat : conforme.
- [x] Étape 6 : coût 2, Riposte 1, 1 pion, plafond 3.
- [x] Étape 7 : 3 cas (Riposte, pose de pion, contre-cas armure détruite),
      rouges 2/3 — le contre-cas d'absence reste vert, assumé.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as014 : Corporate Expansion (obligation)

- [x] Étape 2 : `11020` Depowered (MÊME structure : interdiction permanente +
      sortie qui défausse), `as010` pour le déclencheur jumeau.
- [x] Étape 5 : `EVENT cards` seulement ; `while in HERO form` ; `ALTER-EGO
      Response` ; `PRINTED cost` ; `enters play` (≠ « you play »). Résultat :
      conforme.
- [x] Étape 6 : Boost 2, seuil 2.
- [x] Étape 7 : cas « une carte à 2+ en forme civile la défausse », rouge 1/1.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as015 : * Scarlet Spider

- [x] Étape 2 : `ThisEnterPlayWithCounters`, `27082` Biting Retort (la SEULE
      carte du dépôt qui modifie les icônes de boost), `an006` Angelic Ribbons.
- [x] Étape 5 : `THE VILLAIN` (≠ « an enemy ») ; `against you` ; la flèche =
      COÛT, et sur `"This"`, pas sur l'armure ; `EACH boost card` ; `for THAT
      activation` → `until_event_end`. Résultat : conforme.
- [x] Étape 6 : coût 3, PV 3, 3 pions sens, -1 icône.
- [x] Étape 7 : 2 cas (entrée avec 3 pions, réduction d'icône), rouges 2/2.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as016 : * Six-Armed Spider-Man

- [x] Étape 2 : `06030` Trickster (MÊME phrase), `bt012` pour le déclencheur
      de défense.
- [x] Étape 5 : `Six-Armed Spider-Man defends` = CET allié ; `the ATTACKING
      enemy` (pas un choix) ; `for each DIFFERENT card type` ≠ `len(faces)` ;
      aucune condition de dégâts subis (≠ as018). Résultat : conforme.
- [x] Étape 6 : coût 3, PV 4, 6 cartes défaussées.
- [x] Étape 7 : cas « sa défense punit l'attaquant par type défaussé »,
      rouge 1/1.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as017 : Defensive Briefing

- [x] Étape 2 : `14006` Speed Cyclone (X borne le NOMBRE de cibles),
      `12016` / `ab003` pour `GainUntilRoundEnd`.
- [x] Étape 5 : `up to X HEROES` (pas les identités ni les alliés) ; `EACH
      CHOSEN hero`, y compris ceux des autres joueurs ; `until the end of the
      ROUND` ; Hero Action sans libellé. Résultat : conforme.
- [x] Étape 6 : coût X, +3 DEF.
- [x] Étape 7 : cas « X ressources = +3 DEF », rouge 1/1.
      ⚠ `surpayer: True` obligatoire, sinon X vaut 0.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as018 : Just a Ricochet

- [x] Étape 2 : `bt001a` * Beast (`take_no_damage=True`, drapeau qu'aucune
      carte officielle n'employait avant le 1/9/2026), `SetPlay(
      only_if_you_control_face=...)`.
- [x] Étape 5 : `takes NO damage` = 0 dégât SUBI ; `YOUR HERO` ; `equal to your
      hero's DEF` = DEF COURANTE ; `AN enemy` (≠ as016) ; `an ARMOR upgrade`.
      Résultat : conforme.
      ⚠ **Écart assumé** : « makes a **basic** defense » ne se distingue pas
      d'une défense déclarée par une autre carte — `Message.AfterUnitDefendEnd`
      n'expose aucun drapeau pour ça.
- [x] Étape 6 : coût 1.
- [x] Étape 7 : cas « une défense à 0 dégât rend la DEF en dégâts »,
      rouge 1/1.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as019 : * The Daily Bugle

- [x] Étape 2 : `42018` * Angel's Aerie (MOT POUR MOT pour la seconde
      capacité), `ok014` / `bt004` pour les deux déclencheurs.
- [x] Étape 5 : `a character OR a side scheme` = DEUX capacités ; `a
      CHARACTER` sans restriction de camp ; `SIDE scheme` = `SchemeSide2`
      (⚠ `SideScheme` n'existe pas dans `cards.pack`) ; `you control` sur le
      SOIN seulement ; `for EACH … THIS WAY` ; `A character` au singulier.
      Résultat : conforme.
- [x] Étape 6 : coût 2, 1 pion, 1 PV par pion.
- [x] Étape 7 : 3 cas (personnage vaincu, manigance annexe vaincue, soin),
      rouges 3/3.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as020 : Double Defense

- [x] Étape 2 : `im007` Energy Shield / `01098` Armored Rhino Suit, `08018`
      pour `CostFunc.Discard("This")`.
- [x] Étape 5 : **texte contradictoire arbitré par l'utilisateur** (Réponse
      annoncée, déclencheur d'Interruption → INTERRUPTION) ; `OTHER THAN your
      identity` — as001a couvre déjà l'identité, les deux cartes se complètent
      sans se recouvrir ; `from an attack` ; `your hero's DEF` COURANTE ;
      `Max 1 per player` base automatique. Résultat : conforme.
- [x] Étape 6 : coût 1, max 1 par joueur.
- [x] Étape 7 : cas « elle absorbe les dégâts d'un ALLIÉ qui défend »,
      rouge 1/1.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as021 : * Octo Spidey

- [x] Étape 2 : `32177` Swagger / `im013` (`GainValue` redirige vers le bon
      pouvoir), `16152` Contingency Plan (même phrase, même nombre de cartes).
- [x] Étape 5 : `a basic power` sans préciser lequel → aucun filtre `powers=`
      (≠ im013) ; `for THIS use` ; `for each DIFFERENT resource type` ;
      `[star]` sans « In expert mode » = toujours actif. Résultat : conforme.
- [x] Étape 6 : coût 4, PV 3, CTR 0*, ATQ 1*, 4 cartes défaussées.
- [x] Étape 7 : cas « son attaque de base gagne +1 par type de ressource »,
      rouge 1/1.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as022 : * Spider-Verse

- [x] Étape 2 : `17022` / `01073` pour `ally_limit`, `14017` Nerves of Steel
      pour `for_card`, `16142` * Milano pour `.AnyPlayerCanDoThis()`.
- [x] Étape 5 : `trait OR "Spider" in its title` = ALTERNATIVE, que `SetPlay`
      ne sait pas rendre → condition écrite à la main ;
      `face.TitleContain(...)` couvre les noms d'emprunt ; `for ANY player` ;
      `a [energy] resource` ≠ le [wild] du coût imprimé. Résultat : conforme.
      ⚠ **Écart assumé, arbitrage technique** : la carte imprime « **Action** :
      Exhaust … → generate … ». Le moteur ne sait produire une ressource que
      pendant un paiement, par `CanGenerateResources`, dont le type doit valoir
      `Resource` / `HeroResource` / `AlterEgoResource` (assert de
      resources.py:277). C'est donc `AbilityType.Resource` qui est écrit, comme
      sur les 15 cartes officielles au même texte. Aucune conséquence de jeu.
- [x] Étape 6 : coût 2, +1 allié.
- [x] Étape 7 : 3 cas (condition de mise en jeu, ressource, limite d'alliés),
      rouges 2/3 — la condition de mise en jeu reste verte sans module,
      **et c'est structurel** : un soutien reste jouable même sans capacité
      `Play`. Assumé.
      ⚠ La limite d'alliés se lit par une vérification outillée
      (`as022_limite_allies`) : le détour par « poser trois alliés puis en
      jouer un quatrième » ne prouve rien, `Puzzle.PutIntoPlay`
      court-circuitant le contrôle de limite.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as023 : * Kingpin (némésis)

- [x] Étape 2 : `AfterUnitSchemeEnd`, `15004` / `ho014` pour le décompte
      d'icônes, `50134` pour la pose de menace.
- [x] Étape 5 : ⚠ PAS `AfterEnemySchemeAndPlaceThreat`, qui ajoute la
      condition `placed_threat > 0` que le texte n'impose pas ; complot NOMMÉ
      (absent = rien, la menace ne se reporte PAS sur la principale) ; `for
      EACH boost icon` de la carte défaussée ; `SCHEMES` (≠ attaque). Résultat :
      conforme.
- [x] Étape 6 : PV 6, MAN 1*, ATQ 2, Boost 2.
- [x] Étape 7 : cas « sa manigance charge SON complot annexe », rouge 1/1
      **après correction du seuil** (voir §Ce que la batterie a appris).
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as024 : « The Kingpin of Crime » (némésis)

- [x] Étape 2 : `27127` Panic in the Streets (MÊME forme : un complot annexe
      qui neutralise une famille de soutiens), `12026` Tech Theft.
- [x] Étape 5 : `Hinder 1` base automatique ; `EACH non-permanent support`,
      tous joueurs confondus ; **non-permanent** est le mot qui fait la carte ;
      `PRINTED text box` = `treat_as_blank` ; rien ne vise les AMÉLIORATIONS.
      Résultat : conforme.
- [x] Étape 6 : menace de départ 2, Entrave 1, Boost 2.
- [x] Étape 7 : 2 cas (Gwen Stacy ne se redresse plus ; le pion article n'est
      pas posé), rouges 1/2 — le second est un contre-cas d'absence, assumé.
      ⚠ **Écart moteur constaté** : le `treat_as_blank` neutralise bien les
      Réponses, **pas le chemin de paiement** — une première version du cas
      visait la capacité `Resource` de Gwen Stacy, et elle payait quand même.
      Ce n'est pas un défaut de la carte.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as025 : Underworld Impact (némésis)

- [x] Étape 2 : `50134` pour la menace, `08013` pour le choix, `ag013` pour
      `ThisCardGainSurge`, **`27082` Biting Retort** pour les icônes de boost.
- [x] Étape 5 : portée du « for each » **arbitrée par l'utilisateur** (les
      DEUX options) ; `CHOOSE` = un vrai choix offert au joueur visé ; `YOU
      control` ; `take 1 damage` va à l'IDENTITÉ ; `[star] Boost` toujours
      actif. Résultat : conforme.
      ⚠ Aucune carte officielle ne fait « +1 boost icon FOR EACH x » :
      `WhenCardBecomeBoost` est le SEUL message de la chaîne qui porte le
      joueur visé (`against_player`) ET il est envoyé à l'étape (b) de
      `can_boost.py:79`, donc AVANT le `CountBoostIconsInternal()` de l'étape
      (c). L'ordre est vérifié dans le moteur, pas supposé.
- [x] Étape 6 : Boost 1, +1 icône par soutien.
- [x] Étape 7 : 2 cas (When Revealed, Boost), rouges 2/2.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

### as026 : Behind the Scenes (némésis)

- [x] Étape 2 : `06030` / `16152` pour `DiscardDeckTopCards`, `ag013` pour
      `ThisCardGainSurge`.
- [x] Étape 5 : `THAT discarded card` ; `EACH card from your hand` ; `YOUR`
      deck et main ; la condition de Surge porte sur la MAIN, pas sur le deck —
      un deck vide donne aussi Surge, les deux chemins sont couverts.
      Résultat : conforme.
- [x] Étape 6 : Boost 1.
- [x] Étape 7 : cas « la main perd TOUS les événements », rouge 1/1.
- [x] Étape 8 : voir §Bilan autoplay.

**Carte terminée : OUI**

---

## Ce que ces blocs ne peuvent pas voir

**Aucune partie n'a été jouée par un humain dans le navigateur.** Les 43 cas et
l'autoplay disent que les capacités s'exécutent et que la partie ne bloque pas ;
ils ne disent pas si le pack est agréable, ni si le rythme armure pleine /
armure détruite tient sur une vraie partie. Le point reste ouvert, et il est
écrit ici noir sur blanc.

**Multijoueur non testé.** Cinq cartes du pack ont une portée multijoueur
explicite (`as001b` « per player », `as004` « each enemy in play », `as017`
« each chosen hero », `as020` « a character other than your identity »,
`as022` « for any player`). Les helpers `ArmureDuJoueur` et `EstMonArmure` sont
écrits pour ne jamais toucher l'armure d'un autre Armored Spidey, mais rien ne
l'a vérifié en table à deux.

**L'écart `as022` sur « Action »** et l'écart `as018` sur « basic defense » sont
consignés dans les modules et ci-dessus : ce sont des limites du moteur, pas des
approximations d'écriture.
