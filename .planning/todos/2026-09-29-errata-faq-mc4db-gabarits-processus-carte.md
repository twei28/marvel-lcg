# Errata et rulings FAQ de MC4DB : 11 cartes officielles corrigées (29/09/2026)

Source : `https://mc4db.merlindumesnil.net/api/public/errata?locale=en` (81
errata, RRG jusqu'à 1.8) et `.../api/public/faq?locale=en` (88 rulings), relevés
par les audits du matin. Cartes retenues : 6 errata (57065, 04136, 08009,
25007, 49028, 58002) et 5 rulings (51038, 04028, 05030, 16034, 53002).

Harnais : `.game-src-e` (copie de `.game-src`, un autre agent tenant
`.game-src`), port 43000, `PARALLELES=4`, filtre `[mc4db]` (14 cas, tous
nommés par leur `card_id`). Preuve par substitution :
`tools/substituer_pack.py .game-src-e 43100 <card_id>`, un module à la fois,
empreinte des 11 modules identique avant/après (`cmp`).

Chronologie des passes (rapports dans le scratchpad de la session) :
`rap_rouge` et `rap_rouge2` (scripts d'AVANT : 2/14 puis 3/14), `rap_4`
(après les 5 premiers correctifs : 12/14, Melee et Redwing encore rouges),
`rap_5` (13/14), `rap_vert` (**14/14**).

Deux cartes se sont révélées DÉJÀ CONFORMES une fois le cas écrit ; leur
script n'a pas été touché, seul `cards.json` porte le texte de l'erratum :

- **49028 Exodus** : « for that attack » : `this.attack` lu à
  `AfterUnitAttackEnd` inclut ENCORE les boosts (`GainForThisActive` court
  jusqu'à la fin de l'activation). Mesuré : ATK 2 + Explosion (boost 2) =
  4 cartes défaussées. L'audit se trompait.
- **04136 Bitter Rival** : `range=("Zero", n)` ne veut pas dire « zéro
  permis » : `SelectorRange.GetTargetMin` rend `len(targets)` pour `"Zero"`,
  donc autant de personnages que possible, plafonné à `n`. Mesuré : deux
  manigances annexes, deux personnages, les deux inclinés. L'audit se
  trompait aussi.

Deux changements MOTEUR, tous deux additifs :

- `src/game/message/sender/sender_enemy.py` : `WhenMinionWouldEngagePlayer`
  gagne `CanBeInstead`.
- `src/game/card/face/card_type/minion.py` : `OnEngagePlayer` s'arrête après
  le message « would » si `is_be_instead` (l'engagement remplacé ne résout ni
  « engages », ni Quickstrike, ni « after engages », ni guard/patrol pour ce
  joueur).

Trois commandes Puzzle ajoutées pour les cas (`src/game/puzzle/puzzle.py`) :
`PutIntoPlay(..., player=)`, `PlaceUnder(card, host)`,
`TurnEncounterTopFaceUp()`.

`data/cards.json` : textes de 57065, 04136, 08009, 25007, 49028, 58002 mis
au texte post-errata ; checksums recalculés (`8c5917… -> 52473b…`). ⚠ Le
fichier a d'abord été réécrit avec le mauvais indent (diff de 99 000 lignes)
puis remis à `indent=1` : diff final 1324/11, dont le WIP antérieur.

---

### 57065 : * Moon Knight (errata RRG 1.8, « Limit once per phase »)

- [x] Étape 2 : carte de référence : `aa001a` (Agatha, `.LimitOncePerPhase()`
      sur une aptitude), même mécanisme `ConditionOncePer.LimitOncePerPhase`
      (`once_per.py:69`), clé = l'objet aptitude de CETTE carte.
- [x] Étape 5 : texte-contre-code : « Resolve the When Revealed of the topmost
      treachery » inchangé ; « (Limit once per phase.) » = `.LimitOncePerPhase()`
      sur `WhenThisRevealed`. Résultat : conforme.
- [x] Étape 6 : Retaliate 2, Toughness, HP 5 / ATK 2 / SCH 2 / Boost 2 :
      `desc` inchangé, aucun nombre dans le script.
- [x] Étape 7 : cas « resout la traitrise du dessus de la defausse »
      (Concussive Blast : 1 dégât à l'identité) vert ; substitution
      **rouges 2/2**.
- [x] Étape 7 bis : limite imprimée OUI. Témoin d'épuisement : cas « temoin
      d'epuisement : Limit once per phase », DEUX `Puzzle.Reveal('57065')`
      dans la même phase, dégâts mesurés au second : **2 avant** (rap_rouge),
      **1 après** (rap_vert).
- [x] Étape 8 : voir le bloc autoplay en fin de fiche (Moon Knight est une
      carte de rencontre du set `synthezoid` : aucun des 8 decks joués ne la
      rencontre contre Rhino, l'autoplay ne l'exerce donc pas).
- [x] Étape 8 bis : ne change rien à ce qu'on voit. NON.

Carte terminée : OUI.

### 04136 : Bitter Rival (errata RRG 1.5, « for each side scheme, choose and exhaust »)

- [x] Étape 2 : référence : le script lui-même (`ForChoiceAbility` +
      `SetTarget(range=("Zero", n))`), lu contre `selector_range.py:28-80`.
- [x] Étape 5 : « For each side scheme in play, choose and exhaust a character
      you control » : `GetTargetMin` rend `len(targets)` pour `"Zero"`,
      plafonné par `max = n` manigances : un personnage par manigance,
      obligatoire tant qu'il en reste. Résultat : conforme, script inchangé,
      texte de `cards.json` mis à l'erratum.
- [x] Étape 6 : aucun nombre imprimé hors le compte des manigances (mesuré).
- [x] Étape 7 : cas « UN personnage epuise PAR manigance annexe » (2 annexes,
      Spider-Man + Mockingbird 01083 sous contrôle : les deux inclinés) vert ;
      substitution **rouges 1/1**. ⚠ Ce cas est passé au VERT dès que le
      montage a été juste (la forme héros doit être prise d'abord) : c'est
      un cas de non-régression, pas un rouge→vert.
- [x] Étape 7 bis : pas de limite. NON.
- [x] Étape 8 : carte du set `red_skull`, non rencontrée contre Rhino.
- [x] Étape 8 bis : NON (inclinaison déjà dessinée).

Carte terminée : OUI (aucun correctif nécessaire).

### 08009 : * Synth-Suit (errata RRG 1.8, « trigger » → « resolve »)

- [x] Étape 2 : référence `08001a` Widowmaker, même carte-mère, déjà passé à
      `AfterPlayerResolveAbility(..., control_by_you=True)`.
- [x] Étape 5 : « After you resolve the ability of a Preparation card you
      control, exhaust Synth-Suit → ready Black Widow » :
      `AfterPlayerResolveAbility(HeroResponse, "You", CardFinder2("PREPARATION"),
      control_by_you=True)`, coût `Exhaust("This")`, cible « Black Widow »
      `canbe_ready`. Résultat : conforme.
- [x] Étape 6 : +1 DEF inchangé.
- [x] Étape 7 : cas « apres qu'une carte Preparation a RESOLU sa capacite,
      Black Widow se redresse » (Widow's Bite 08010 part sur l'entrée d'Hydra
      Mercenary ; Black Widow inclinée d'avance, redressée après ; Synth-Suit
      inclinée) vert ; substitution **rouges 1/1**.
      ⚠ Le passage « trigger → resolve » n'est PAS discriminé par ce cas :
      il l'était vert AVANT le correctif aussi. La différence ne se voit que
      si une capacité déclenchée ne se résout pas (annulée), ce que le
      harnais ne sait pas provoquer sur une carte Preparation. Assumé.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : deck `black_widow`, voir bloc autoplay.
- [x] Étape 8 bis : NON.

Carte terminée : OUI, avec la réserve ci-dessus sur la preuve de « resolve ».

### 25007 : * Aragorn (errata RRG 1.5, « Valkyrie » → « You »)

- [x] Étape 2 : référence : la première moitié du même script
      (`GiveKeywordToAttached("You", health=4)`), déjà sur « You ».
- [x] Étape 5 : « You get +4 hit points and gain the aerial trait » : les deux
      `GiveKeywordToAttached` visent `"You"`. Résultat : conforme.
- [x] Étape 6 : +4 PV : `health=4`, inchangé.
- [x] Étape 7 : cas « You gagne AERIAL, aussi en alter-ego » (Aragorn attaché
      à Brunnhilde, forme alter-ego) : **rouge avant** (« trait AERIAL absent
      de l'identite », rap_rouge2), vert après ; substitution **rouges 1/1**.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : deck `valkyrie`, voir bloc autoplay.
- [x] Étape 8 bis : NON (trait, pas de dessin).

Carte terminée : OUI.

### 49028 : * Exodus (errata, « for that attack »)

- [x] Étape 2 : référence : `can_attack.py:327-339` (`GainForThisActive`
      des boosts) et `AfterUnitAttackEnd`.
- [x] Étape 5 : « equal to his total ATK for that attack » : `this.attack`
      à `AfterUnitAttackEnd` = ATK de base + boosts de cette attaque
      (mesuré). Résultat : conforme, script inchangé.
- [x] Étape 6 : HP 6 / ATK 2 / SCH 2 / Boost 3, Steady, Toughness, Villainous
      (`desc`, mots-clés lus nativement).
- [x] Étape 7 : cas « defausse egale a son ATK TOTALE, boost compris »
      (deck rencontre monté avec Explosion, boost 2, sur le dessus : 4 cartes
      défaussées) vert dès le premier passage ; substitution **rouges 1/1**.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : sbire némésis de Magneto, non rencontré contre Rhino sans
      Magneto.
- [x] Étape 8 bis : NON.

Carte terminée : OUI (aucun correctif nécessaire).

### 58002 : Ionic Physiology (errata RRG 1.8, « → » devient « Then, »)

- [x] Étape 2 : référence : le script lui-même ; « Max 3 cards tucked here »
      = plafond lu par `len(this.GetPlacedCardArea().Get()) < 3`.
- [x] Étape 5 : « tuck that event from your discard pile under this card.
      Then, heal 1 damage from your identity » : la Response part dès qu'un
      événement à énergie imprimée est joué par le contrôleur ; le tuck se
      fait SI le plafond le permet et si l'événement est encore en défausse /
      en résolution ; le soin part dans tous les cas. Résultat : conforme.
      Mots-pièges : `Then` (plus un coût), `Max 3` (plafond, pas condition).
- [x] Étape 6 : 3 cartes, 1 soin : inchangés.
- [x] Étape 7 : cas « 3 cartes deja glissees, l'evenement energie soigne
      QUAND MEME 1 » (`Puzzle.PlaceUnder` ×3, identité blessée de 3, Active
      Altruism joué) : **rouge avant** (dégâts 3, rap_rouge), vert après
      (dégâts 2, 3 cartes toujours posées) ; substitution **rouges 1/1**.
- [x] Étape 7 bis : « Max 3 » n'est pas une limite d'usage mais un plafond
      de cartes : c'est le cas ci-dessus qui le tient (taille 3 après coup).
- [x] Étape 8 : deck `wonder_man`, voir bloc autoplay.
- [x] Étape 8 bis : les cartes glissées se dessinaient déjà (mécanisme
      `PlaceCardHere` inchangé). NON.

Carte terminée : OUI.

### 51038 : Target Spotter (FAQ : le sbire n'engage jamais l'autre joueur)

- [x] Étape 2 : référence : RECETTES « instead » = `message.SetBeInstead(effect)`
      sur un message `Would...` (aa010, ag012, av002) ; `Minion.OnEngagePlayer`
      pour l'ordre would → engages → Quickstrike → after.
- [x] Étape 5 : « Interrupt: When a minion would engage a player, remove 1
      target counter → that minion cannot activate until the end of the
      phase. Engage that minion. » : `EnemyCannotActivate` jusqu'à la fin de
      phase inchangé ; si le joueur visé n'est pas l'initiateur,
      `SetBeInstead` puis `EngagePlayer(initiator)` immédiat. Si c'est le
      même joueur, rien à remplacer (pas de `SetBeInstead`, sans quoi son
      propre engagement ne se résoudrait plus). Résultat : conforme.
- [x] Étape 6 : Uses (2 target), 1 compteur par usage : inchangés.
- [x] Étape 7 : cas « le sbire n'engage JAMAIS l'autre joueur » (partie à
      DEUX, Badoon Grunt 16118 engagé par `Puzzle.Engage(player=1)`, « after
      this engages you » distribue une carte rencontre) : **rouge avant**
      (« le joueur 1 a recu 1 carte rencontre », rap_rouge2), vert après
      (joueur 0 : 1 carte, joueur 1 : 0, sbire engagé avec le joueur 0) ;
      substitution **rouges 1/1**.
- [x] Étape 7 bis : Uses = règle du mot-clé, pas une limite d'aptitude. NON.
- [x] Étape 8 : carte Aggression ; aucun des decks de départ joués ne
      l'emporte. Non exercée par l'autoplay.
- [x] Étape 8 bis : le sbire change de zone d'engagement, dessin existant.
      NON.

Carte terminée : OUI.

### 04028 : Marked for Death (FAQ : la Mockingbird du joueur Clint)

- [x] Étape 2 : référence : le script lui-même ; filtre par
      `GetControlByPlayer()` comme `check_energy_event` de 58002.
- [x] Étape 5 : « The Clint Barton player searches their hand, deck, discard
      pile, and play area for Mockingbird » : la recherche en jeu ne garde
      que les alliées CONTRÔLÉES par ce joueur. Résultat : conforme.
- [x] Étape 6 : aucun nombre.
- [x] Étape 7 : cas « la Mockingbird du joueur Clint, pas celle d'un autre
      joueur » (partie à DEUX : 04004 en main de Clint, 01083 basique en jeu
      chez Spider-Man via `PutIntoPlay(player=1)`) : **rouge avant** (01083
      glissée, rap_rouge), vert après (04004 glissée, 01083 en jeu) ;
      substitution **rouges 1/1**.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : manigance némésis de Hawkeye ; deck `hawkeye` joué, voir bloc
      autoplay (rencontre non garantie).
- [x] Étape 8 bis : mécanisme `PlaceCardHere` inchangé. NON.

Carte terminée : OUI.

### 05030 : Melee (FAQ : 2e cible et guard)

- [x] Étape 2 : référence : `Villain.CanBeAttackBy` (`villain.py:71`), la
      règle Guard telle que le moteur l'applique à la 1re cible.
- [x] Étape 5 : « Deal 3 damage to an enemy. Deal 3 damage to another
      enemy. » : la 2e cible est choisie parmi les ennemis encore en jeu,
      autres que la 1re, et attaquables (`CanBeAttackBy`) : le vilain n'y
      figure que si aucun sbire guard engagé ne subsiste. Résultat :
      conforme. Mot-piège `another` : déjà tenu.
- [x] Étape 6 : 3 et 3 : inchangés.
- [x] Étape 7 : cas « le vilain reste protege si le sbire guard SURVIT »
      (Hydra Soldier 4 PV) : **rouge avant** (Rhino 3 dégâts, rap_4), vert
      après (Rhino 0, sbire 3) ; cas « le vilain devient ciblable si la 1re
      VAINC le sbire guard » (Hydra Mercenary 3 PV) vert ; substitution
      **rouges 2/2**.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : carte Aggression ; deck `ms_marvel` joué, voir bloc autoplay
      (Melee n'y est pas garantie).
- [x] Étape 8 bis : NON.

Carte terminée : OUI.

### 16034 : Battery Pack (FAQ : le compteur prend le type de la carte d'arrivée)

- [x] Étape 2 : référence : `CanPlaceCounter.ConvertAllPurpose`
      (`can_place_counter.py`) : `'all-purpose'` prend le premier nom de
      compteur présent sur la carte, sinon `'counter'`.
- [x] Étape 5 : « move a charge counter from this card to another tech
      upgrade you control » : coût `Counter("This", 1, "charge")`, pose
      `PlaceCountersOn([cible], 1, 'all-purpose')`. Résultat : conforme.
- [x] Étape 6 : 2 charge à l'entrée, 1 déplacé : inchangés.
- [x] Étape 7 : cas « le compteur deplace prend le TYPE de la carte
      d'arrivee » (Bambino 54018, Uses 3 ammo) : **rouge avant**
      (« 54018.ammo=3, charge=1 », rap_4), vert après (ammo 4, charge 0,
      Battery Pack 1) ; substitution **rouges 1/1**.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : deck `rocket_raccoon`, voir bloc autoplay.
- [x] Étape 8 bis : le plateau dessine les compteurs par leur nom
      (`compteurs-fr.ts`, `card-model.ts:483`), aucun nom en dur : un ammo
      de plus se dessine comme les autres. NON.

Carte terminée : OUI.

### 53002 : * Redwing (FAQ : injouable si le dessus visible n'a pas d'icône)

- [x] Étape 2 : référence : `conditions=[...]` de `WhenInYourPlayTurn`
      (`turn_phase.py:6`), comme les conditions de forme du dépôt.
- [x] Étape 5 : « choose to either deal X damage to an enemy or remove X
      threat from a scheme. X is the number of icons in the discarded card's
      boost area » inchangé ; ruling : si `encounter_deck.GetTop()` est face
      visible (`card.state.is_face_up`) et compte 0 icône
      (`CountTotalBoostStarAndBoost`), la Hero Action n'est pas offerte.
      Résultat : conforme.
- [x] Étape 6 : X mesuré (Explosion → 2).
- [x] Étape 7 : cas nominal « X = icones de la carte defaussee » vert ; cas
      « INJOUABLE si le dessus du deck rencontre est VISIBLE sans icone »
      (Hard to Keep Down 01104, `TurnEncounterTopFaceUp`,
      `Puzzle.Action('53002', 'HeroAction')` tolérant) : **rouge avant**
      (action partie, Redwing inclinée, rap_5), vert après ; substitution
      **rouges 1/2** : le cas « injouable » reste vert sans module (contre-cas
      d'absence d'effet : sans aptitude, rien ne part non plus). Assumé.
      ⚠ Piège vu : sans le type `'HeroAction'`, `Puzzle.Action` retombe sur
      l'attaque de base de l'allié quand la Hero Action est refusée.
      ⚠ Réserve : « dessus visible » est rendu par `card.state.is_face_up`
      sur la carte du dessus ; aucune carte du dépôt ne pose ce drapeau
      aujourd'hui (seule la commande Puzzle ajoutée le fait). La condition
      est donc juste mais inerte tant qu'aucun effet ne rend le dessus
      visible.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : deck `falcon`, voir bloc autoplay.
- [x] Étape 8 bis : NON.

Carte terminée : OUI, avec la réserve sur « dessus visible ».

---

## Étape 8, bloc autoplay commun

`tools/autoplay.py .game-src-e --deck <d> --vilains rhino --parties 3
--paralleles 3 --port 43300`, 8 decks (`wonder_man`, `valkyrie`, `falcon`,
`rocket_raccoon`, `black_widow`, `hawkeye`, `ms_marvel`,
`black_panther_shuri`), **24 parties, toutes « terminee », 0 traceback au
grep exhaustif** des 24 journaux `/tmp/autoplay_<deck>_rhino_normal_equilibre_<n>.log`
(NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout).
Pas de témoin séparé : les 8 decks se servent mutuellement de témoins
(rounds 3 à 8, aucun blocage). Lecture des journaux : Battery Pack activé 8
fois (compteur « counter » sur Cybernetic Skeleton / Booster Boots, « charge »
sur Rocket's Pistol : le type suit bien la carte d'arrivée) ; Mockingbird
jouée et redressée normalement chez Hawkeye ; Ionic Physiology en jeu dès la
mise en place. Melee, Target Spotter, Marked for Death, Exodus, Moon Knight et
Bitter Rival **ne sont pas sortis** en 24 parties contre Rhino : pour eux, la
seule preuve est le harnais.

⚠ HORS PÉRIMÈTRE, VU DANS LES JOURNAUX : Battery Pack s'est ciblé LUI-MÊME
deux fois (« s'active, cible [[Battery Pack]] ») alors que le texte dit
« another tech upgrade » et que le sélecteur porte `another=True`. Le
sélecteur, pas le correctif du jour ; à ouvrir en fiche.

Cache d'essai `.game-src-e` (et `-par0..3`) supprimé en fin de passe.
