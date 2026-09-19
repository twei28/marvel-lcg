# Portage FEAR NO EVIL (pack officiel `fne`, set 60) — vilains, manigances, sets modulaires, campagne

**Source** : scans Hall of Heroes (`hallofheroeslcg.com/fear-no-evil/`, 208 scans
`60001` → `60210a`, 710×1030), rulebook `mc60_rulebook-web.pdf` (28 p.) et
journal de campagne `mc60_campaign_log.pdf`, tous deux téléchargés le
18/09/2026. **Aucun texte de carte sur MarvelCDB ni marvelsdb-json-data pour
60065 → 60210** : chaque carte est lue sur son scan.
**Décisions utilisateur (18/09/2026)** : 5 tuiles de manigance + modale de
choix du vilain (comme les variantes de héros) ; tout livrer, un bloc à la
fois, chaque bloc vérifié en entier avant le suivant ; en cas de doute sur une
carte, montrer le scan et poser une question multichoix.
**Ordre des blocs** : 1) Hammerhead + Art Museum Heist + Cops + The Owl (premier
scénario jouable) ; 2) Bullseye, Electro, Purple Man, Typhoid Mary ; 3) The
Getaway, Protection Racket, The Raft Breakout, Stop the Presses + Disasters,
Drive, Tombstone, Tracksuit Mafia ; 4) Kingpin ; 5) mode campagne.

---

## Bloc 1 — Hammerhead, Art Museum Heist, Cops, The Owl (18/09/2026)

### 1. Inventaire → card_id (27 cartes, 4 sets)

| card_id | Carte | Type | Imprimé | Ex. |
|---|---|---|---|---|
| `60086` | * Hammerhead (I) | Villain | SCH 2 / ATK 1★ / 14[per_hero] PV, CRIMINAL MAGGIA UNDERLING | 1/14 |
| `60087` | * Hammerhead (II) | Villain | SCH 2 / ATK 2★ / 15[per_hero], Toughness, Retaliate 1 | 2/14 |
| `60088` | * Hammerhead (III) | Villain | SCH 3 / ATK 3★ / 16[per_hero], Toughness, Retaliate 2 | 3/14 |
| `60089` | Energy Gatling Gun | Attachment TECH | +1 ATK, boost 2 | 4/14 |
| `60090` | Hardheaded | Attachment CONDITION | +1 SCH, boost 1 + ★ | 5/14 |
| `60091` | * Chameleon | Minion | SCH 1★ / ATK 1 / 5 PV, boost 3 | 6/14 |
| `60092` | Maggia Enforcers | Minion | SCH ★ / ATK 2 / 3 PV, Guard, boost 0 | 7-8/14 |
| `60093` | Maggia Underboss | Minion | SCH 1★ / ATK 1★ / 4 PV, Villainous, boost 1 | 9-10/14 |
| `60094` | Consolidate Power | Side scheme | 6 menaces, boost 1 | 11/14 |
| `60095` | Power Struggle | Side scheme | 5 menaces, accélération, boost 1 | 12/14 |
| `60096` | "Head First!" | Treachery | boost 2 | 13-14/14 |
| `60121a/b` | Art Museum Heist | Main scheme | 1B : 1[per_hero] départ, 9[per_hero] cible, +X[per_hero]★ | 1/9 |
| `60122` | * Impossible Object | Attachment ART | +1 SCH/THW, Surge, boost 2, coût [mental] | 2/9 |
| `60123` | * Inspiring Pottery | Attachment ART | +1 SCH/THW, Surge, boost 2, coût [wild] | 3/9 |
| `60124` | * Replica Shield | Attachment ART | +1 SCH/THW, Surge, boost 2, coût [physical] | 4/9 |
| `60125` | * Stunning Landscape | Attachment ART | +1 SCH/THW, Surge, boost 2, coût [energy] | 5/9 |
| `60126` | Art Thief | Minion THIEF | SCH 2 / ATK 2 / 3 PV, boost ★ seule | 6-7/9 |
| `60127` | Tug of War | Treachery | boost 1 | 8-9/9 |
| `60182` | Cop | Minion POLICE | SCH ★ / ATK 2 / 3 PV, Quickstrike, Vulnerable, boost 0 | 1-2/5 |
| `60183` | Crooked Cop | Minion CRIMINAL POLICE | SCH 1 / ATK 2 / 4 PV, Quickstrike, Vulnerable, boost ★ | 3/5 |
| `60184` | Wanted | Obligation (sans Give to) | boost 2 | 4/5 |
| `60185` | Police Cordon | Side scheme | 3 menaces, ★ Hinder 1[per_hero], boost 3 | 5/5 |
| `60191` | Flight Serum | Attachment SUPERPOWER | +1 SCH / +1 ATK, boost 2 | 1-2/5 |
| `60192` | * Mister Fish | Minion CRIMINAL MAGGIA | SCH 1 / ATK 2★ / 4 PV, boost 2 | 3/5 |
| `60193` | * The Owl | Minion AERIAL CRIMINAL | SCH 3 / ATK 2★ / 5 PV, Quickstrike, boost ★ | 4/5 |
| `60194` | Swoop Down | Treachery | boost 3 | 5/5 |

Icônes vérifiées par comparaison (règle Lockjaw) contre des cartes du **même
pack** dont `desc.RES` est connu : `60007` Elektra = G (étoile), `60003` = Y
(éclair), `60004` = B (nœuds), `60002` = R (poing). Accélération de Power
Struggle comparée à `ag011` (pointe + barre) : accélération, pas aléa.

### 2. Fichiers écrits

- `data/cards.json` : 27 entrées dans `fne` (set_name `Hammerhead`, `Art Museum
  Heist`, `Cops`, `The Owl`) ; `data/sets_info.json` : `scenarios`,
  `encounters: [cops, the_owl]`, `max_id 60210` ; checksums recalculés.
- `data/encounter_sets/{hammerhead,art_museum_heist,cops,the_owl}.json`.
- `data/scenarios/art_museum_heist_hammerhead.json` (+ `_expert`) : les 4
  œuvres en `set_aside`, sets `hammerhead`, `art_museum_heist`, `standard`
  (+ `expert`), modulaires `cops`, `the_owl`.
- `src/cards/pack/fne/{hammerhead,art_museum_heist,cops,the_owl}/` : 27
  scripts + helpers (`ReponseForceeCoupDeBoule`, `CapacitesDUneOeuvre`,
  `DeplacerUneOeuvreVersLeVilain`, `PeutCouvrirLeCout` au niveau du pack).
- `assets/pics/600xx.jpg` : 27 scans.
- `public/js/prepare/mechants-info.js` : fiche Hammerhead (`60086`).
- `ui-app/src/board/fne-oeuvre-volee.test.ts` : 3 cas plateau (verts).
- `tools/test_capacites.py` : 57 cas `[fne]` + 5 vérificateurs
  (`fne_oeuvres`, `fne_escalade`, `fne_boost_du_vilain`,
  `fne_cartes_distribuees`, `fne_garde_patrouille`, `fne_engage_joueur`),
  générés par `scratchpad/gen_cas_fne_b1.py` (copie jointe en §6).

### 3. Fichiers PARTAGÉS touchés (→ passe complète des decks + batterie complète dues)

| Fichier | Quoi | Pourquoi |
|---|---|---|
| `src/game/card/face/card_face.py` | traits `MAGGIA`, `POLICE` ajoutés à `TRAITS` | absents de l'énum |
| `src/game/card/face/card_type/obligation.py` | `give_to` rend `None` sans assert ; `CheckPrintedValue` n'exige plus `GiveTo` | 60184 Wanted, obligation de set modulaire : la révélation plantait (`assert printed_give_to != None`) alors que la branche « au joueur qui révèle » existait |
| `tools/test_capacites.py` | clé `defausse_rencontre` lit aussi `Worlds.GetEncounterDiscardPileCards` | la pile du vilain était invisible (`defausse = []`) |

### 4. Ce que le harnais a trouvé (3 passes : 13/55 → 45/57 → 57/57)

- 24 échecs « AssertionError vide » : la partie commence en **alter-ego**,
  `Puzzle.Exhaust('01001a')` fabriquait une seconde identité. → `ChangeForm`.
- `Puzzle.Damage('60182', 3)` frappait la **copie du deck** (FindOrCreateFace
  fouille le deck avant le terrain). → `EmptyEncounterDeck` d'abord.
- L'œuvre posée au Setup (graine 42 : Pottery) donnait **stalwart + 1 SCH** au
  vilain : Impossible Object / Stunning Landscape « n'étourdissaient pas ».
- `OnEvent.Form(Identity|Ally)` : union refusée, exception avalée → Chameleon
  ne se recalculait pas. → `Friend`.
- **Tug of War** : la branche payante est offerte même impayable, `Otherwise`
  jamais. → condition `PeutCouvrirLeCout` ; et `message.GetToPlayer()`
  n'existe pas sur `WhenPlayerChooseAbility` (joueur passé par clôture).
- `main_exclusive: []` non appliqué : Great Responsibility jouée par le pilote
  encaissait la menace de Chameleon. → `["01088"]`.
- `Puzzle.Damage(40)` sur Hammerhead II absorbé par Toughness (stade III
  jamais atteint). → 1 puis 40.
- **Trouvé par l'AUTOPLAY, invisible aux 57 cas** : `PeutCouvrirLeCout`
  envoyait `Message.CheckPlayerCanPayCost` depuis la condition de choix de
  Tug of War ; chaque carte en main qui y répond plante dans
  `add_to_pay_list` (`KeyError: None`, resources.py:216), 5 à 7 tracebacks par
  partie, avalés par le moteur. Le harnais ne l'a jamais vu (mains contrôlées
  par `main_exclusive`). → le helper ne lit plus que les icônes imprimées.
- Détail complet des recettes : `RECETTES-MOTEUR.md` §3 (7 lignes) et §7ter.

### 5. Gabarits PROCESSUS-CARTE (un par carte)

Conventions : « cas » = nom dans `tools/test_capacites.py` (préfixe = card_id,
filtre `[fne]`) ; « subst » = verdict de `tools/substituer_pack.py` ; les
mots-pièges de l'étape 5 sont listés quand la carte en porte.

#### 60086 / 60087 / 60088 : * Hammerhead (I, II, III)
- [x] Étape 2 : `01118` Sonic Converter (AfterUnitAttackAndDamageUnit sur
      "Character", target_in_play) ; Toughness / Retaliate = bases desc.
- [x] Étape 5 : « attacks **and damages** » (≠ attacks) → fabrique AndDamage ;
      « **already** stunned » → statut lu AVANT de le poser (Steady : une
      carte ≠ stunned) ; « a character » → héros ou allié ("Character").
- [x] Étape 6 : PV 14/15/16[per_hero], ATK 1/2/3, SCH 2/2/3, Retaliate 1/2,
      dégâts 1/1/2 ↔ `ReponseForceeCoupDeBoule(1|1|2)` et `desc`.
- [x] Étape 7 : `60086 … l'identite est etourdie` (stun + 1 dégât),
      `60086 … deja etourdie : 1 degat de plus` (2), `60087 (expert) … 2 ATK +
      1` (3), `60088 (expert) … 3 ATK + 2` (5). Subst : `60086` rouges 2/2 ; `60087` rouges 1/1 ; `60088` rouges 1/1 ;
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué.
- [x] Étape 8 bis : statut posé → couvert par la jauge de statuts (générique) ; NON.
- Carte terminée : OUI

#### 60089 : Energy Gatling Gun
- [x] Étape 2 : `01099` Charge (attache à Rhino), `al014`/`42030`
      (`CostFunc.Discard("This")` pour « → »), `50096` Leaping Kick
      (`BasicAttack([allié])`), `Message.AfterUnitAttackEnd.attacked_targets`.
- [x] Étape 5 : « if … was **not defeated** » → condition `survivant` dans
      `conditions` ; « discard this card **→** » = COÛT, pas effet ; « **that**
      character » = l'unité attaquée (défenseur ou identité), pas le joueur ;
      « again » = seconde attaque, la carte défaussée ne peut pas relancer.
- [x] Étape 6 : +1 ATK (`ATK+`), boost 2.
- [x] Étape 7 : `60089 … le survivant est re-attaque` (4 dégâts, carte hors
      jeu) ; contre-cas `… le defenseur est vaincu, pas de seconde attaque`
      (Spider-Woman 2 PV meurt, carte en jeu). Subst : `60089` rouges 2/2 ;
- [x] Étape 7 bis : NON.
- [x] Étape 8 : 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué.
- [x] Étape 8 bis : attachement sur le vilain (générique, `fne-oeuvre-volee`
      dessine un attachement sur `area_villain`) ; OUI, couvert.
- Carte terminée : OUI

#### 60090 : Hardheaded
- [x] Étape 2 : `16064` Drang's Spear (stalwart attaché), `01118` (Cost YBR),
      `52037` Growing Strong (boost → tough à `activating_enemy`).
- [x] Étape 5 : « Hero Action » = sous-type dédié ; trois ressources de
      couleurs différentes → `Cost("YBR")` ; boost ★ = `WhenCardBecomeBoost`.
- [x] Étape 6 : +1 SCH (`SCH+`), boost 1, YBR.
- [x] Étape 7 : `… gagne stalwart et +1 SCH` (stun refusé, scheme +1),
      `… Hero Action [energy][mental][physical] : defaussee`, `… Boost :
      l'ennemi qui s'active devient robuste`. Subst : `60090` rouges 3/3 ;
- [x] Étape 7 bis : NON.  · Étape 8 : 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué.  · Étape 8 bis : attachement + statut, couvert.
- Carte terminée : OUI

#### 60091 : * Chameleon
- [x] Étape 2 : `27067` Sand Clone (ThisGainKeyword à fonction), `32117`
      (DoSchemes), rafraîchi par `OnEvent.Form(Friend)`.
- [x] Étape 5 : « highest THW among **characters** » → amis seulement (les
      ennemis n'ont pas de THW) ; alter-ego = 0 ; « Chameleon schemes » =
      manigance de base (SCH + X), pas une menace fixe.
- [x] Étape 6 : SCH 1, ATK 1, PV 5, boost 3.
- [x] Étape 7 : `… +X SCH, X = THW le plus haut (heros THW 1)` (+1), `… suit
      l'allie au THW 2` (+2), contre-cas `… alter-ego : X = 0`, `… When
      Revealed : il manigance (1 + 1)` (menace 2). Subst : `60091` rouges 3/4 (contre-cas d'absence d'effet, vert par construction) ;
- [x] Étape 7 bis : NON.  · Étape 8 : 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué.  · Étape 8 bis : NON (chiffres).
- Carte terminée : OUI

#### 60092 : Maggia Enforcers
- [x] Étape 2 : `24016` Mandrill (`ThisGainKeywordForEachFaceInPlay`), Guard = base.
- [x] Étape 5 : « SCH **is equal to** » → SCH imprimé 0 + 1 par MAGGIA ;
      « (including this one) » → le filtre l'inclut (mesuré : 2 avec le vilain).
- [x] Étape 6 : PV 3, ATK 2, boost 0, SCH ★.
- [x] Étape 7 : `… SCH = ennemis MAGGIA (Hammerhead + lui)` (2), `… un
      troisieme MAGGIA entre : SCH 3`. Subst : `60092` rouges 2/2 ;
- [x] 7 bis NON · 8 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué. · 8 bis NON.
- Carte terminée : OUI

#### 60093 : Maggia Underboss
- [x] Étape 2 : `02020` Hysteria (WhenUnitWouldAttack + WhenUnitWouldScheme,
      `GiveAdditionalBoostCardForThisActivation`), Villainous = base.
- [x] Étape 5 : « activates against **you** » → `GetAgainstPlayer()` ; « if you
      are stunned » = identité étourdie, dans `conditions` ; « for this
      activation » = 1 carte de plus, pas un bonus permanent.
- [x] Étape 6 : PV 4, ATK 1, SCH 1, boost 1, +1 carte.
- [x] Étape 7 : `… joueur etourdi : une carte boost de plus (1+3+3 = 7)`,
      contre-cas `… non etourdi … (1+3 = 4)`. Subst : `60093` rouges 1/2 (contre-cas d'absence d'effet, vert par construction) ;
- [x] 7 bis NON · 8 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué. · 8 bis NON.
- Carte terminée : OUI

#### 60094 : Consolidate Power
- [x] Étape 2 : `56091` Dangerous Recruits (`GiveBoostCard`), en Forced
      RESPONSE (`AfterUnitBeDefeated`) et non Interrupt comme le modèle.
- [x] Étape 5 : « After a minion is defeated » (défaite, pas dégâts) ; « to
      the villain » → `Worlds.FindVillain`.
- [x] Étape 6 : 6 menaces (fixe, pas d'icône joueur), boost 1.
- [x] Étape 7 : `… sbire vaincu : il devient boost face cachee du vilain`
      (vérificateur `fne_boost_du_vilain`). Subst : `60094` rouges 1/1 ;
- [x] 7 bis NON · 8 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué. · 8 bis : la pile de boost est dessinée (générique) ; couvert.
- Carte terminée : OUI

#### 60095 : Power Struggle
- [x] Étape 2 : `24023` Out for Blood (`fewest_remaining_hp`), `01116b`
      (`DiscardEncounterCardsUntil`), `01095` (`Reveal`) ; Accélération = base.
- [x] Étape 5 : « **Defeat** » (pas dégâts) → `Faces.DefeatUnits` ; « until
      you discard a minion. **Reveal that minion** » → le même objet.
- [x] Étape 6 : 5 menaces, boost 1, 1 icône accélération.
- [x] Étape 7 : `… vainc le sbire le plus faible, defausse jusqu'a un sbire et
      le revele` (60092 hors jeu, 01101 en jeu, 01186 en défausse). Subst : `60095` rouges 1/1 ;
- [x] 7 bis NON · 8 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué. · 8 bis NON.
- Carte terminée : OUI

#### 60096 : "Head First!"
- [x] Étape 2 : `04086` Swinging Stone (`AttackProperty(additional_value)`),
      `01106` Stampede (surge en alter-ego).
- [x] Étape 5 : (Alter-Ego)/(Hero) = deux `WhenThisRevealed` ; « If you are
      stunned » lu à la révélation ; « +2 ATK for **this** attack » et
      « gains overkill » portés par la propriété de l'attaque, pas permanents.
- [x] Étape 6 : +2, boost 2.
- [x] Étape 7 : `(Hero) — etourdi : +2 ATK … = 4`, contre-cas `non etourdi :
      ATK 1, puis etourdi`, `(Alter-Ego) — surge`. Subst : `60096` rouges 3/3 ;
      ⚠ L'overkill n'est pas mesuré à part : il ne se voit qu'avec un
      défenseur allié abattu, et une attaque déclenchée par une révélation ne
      passe pas par `Puzzle.Attack(..., defender)`. La propriété est la même
      que celle prouvée sur 50096 Leaping Kick.
- [x] 7 bis NON · 8 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué. · 8 bis NON.
- Carte terminée : OUI

#### 60121a / 60121b : Art Museum Heist
- [x] Étape 2 : `55004a` Prime Real Estate (Setup + `SetupCards.AttachTo`
      Random), `16091b` (escalade dynamique), `04080` Dense Forest
      (`is_undefended_attack=True`), `IfThisSchemeStageIsCompletedPlayersLoseTheGame`.
- [x] Étape 5 : « attach 1 **at random** » → `choose="Random"` ; « Shuffle the
      other 3 » → `ShuffleAllTo("EncounterDeck")` ; « X is **1 more than** » →
      `(1 + n) × joueurs` ; « **undefended** attack against an **identity** » →
      `Enemy` → `Identity`, `is_undefended_attack` ; « attach 1 ART on **that**
      identity » → le joueur attaqué choisit parmi SES œuvres.
- [x] Étape 6 : 1[per_hero] départ, 9[per_hero] cible, escalade 0 + X.
- [x] Étape 7 : `60121a … mise en place : 1 oeuvre au hasard sur le vilain, 3
      dans le deck`, `60121b … escalade … 4 oeuvres -> 5`, contre-cas `aucune
      oeuvre -> 1`, `… attaque non defendue … son oeuvre passe au vilain`,
      contre-cas `… defendue par un allie, l'oeuvre reste`. Subst : `60121a` rouges 1/1 ; `60121b` rouges 3/4 (contre-cas d'absence d'effet, vert par construction) ;
- [x] 7 bis NON · 8 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué. · 8 bis : le complot et l'escalade sont
      dessinés par la jauge générique ; les œuvres qui bougent : `fne-oeuvre-volee.test.ts` (3/3).
- Carte terminée : OUI

#### 60122 / 60123 / 60124 / 60125 : les quatre œuvres (ART)
- [x] Étape 2 : tronc `CapacitesDUneOeuvre` : `AttachToFaceWhenPutIntoPlay(Villain)`,
      `AfterCardAttachTo(ForcedResponse, "This", Unit2)`, deux `HeroAction`
      (`Cost(x)` / `CostFunc.Exhaust("YourIdentity")`, RECETTES §5 « or » =
      deux capacités) ; stalwart de Pottery : `GiveKeywordToAttached("Character",
      stalwart=1)` (`16064`) ; Surge et `SCH+`/`THW+` = bases desc.
- [x] Étape 5 : « After this card attaches to a **character** » → Unit2, part
      à l'attache initiale ET aux déplacements ; « attach this card to **your
      hero** » → condition « pas déjà sur mon héros » ; « Spend a [x] resource
      **or** exhaust your hero » → deux capacités.
- [x] Étape 6 : coûts B / G / R / Y ↔ icônes vérifiées §1 ; +1 SCH/THW ; boost 2.
- [x] Étape 7 : `60122 … revelee : s'attache au vilain, le desoriente, surge`,
      `60122 … Hero Action [mental] : passe sur le heros, qui est desoriente`,
      `60122 … Hero Action incliner …` ; `60123 … revelee : le vilain gagne
      stalwart`, `60123 … sur le heros : stalwart …, +1 THW` ; `60124 …
      robuste` ; `60125 … etourdi`. Subst : `60122` rouges 3/3 ; `60123` rouges 2/2 ; `60124` rouges 1/1 ; `60125` rouges 1/1 ;
- [x] 7 bis NON · 8 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué. · 8 bis OUI : `fne-oeuvre-volee.test.ts`
      (dessinée sur le héros, sur le vilain, avec le sérum à côté ; 3/3).
- Carte terminée : OUI

#### 60126 : Art Thief
- [x] Étape 2 : `01095` Rhino (`Search.EncounterCard(include_discard_pile)`),
      l'œuvre trouvée entre par `PutIntoPlay` (elle s'accroche seule, sans
      surge) ; « If you cannot » → `DeplacerUneOeuvreVersLeVilain`.
- [x] Étape 5 : « If you **cannot** » → branche atteignable (deck + défausse
      sans œuvre) ; « from **an** identity » → choix parmi toutes.
- [x] Étape 6 : PV 3, ATK 2, SCH 2, boost ★ seule (0 icône).
- [x] Étape 7 : `… trouve une oeuvre dans le deck (2 au total)`, `… sans
      oeuvre trouvable : en prend une a l'identite`, `… Boost : … (2 avec celle
      que vole l'attaque non defendue)`. Subst : `60126` rouges 3/3 ;
- [x] 7 bis NON · 8 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué. · 8 bis : couvert par `fne-oeuvre-volee`.
- Carte terminée : OUI

#### 60127 : Tug of War
- [x] Étape 2 : `50134` Innocent Bystanders (`ForChoiceAbilityWithCost`) +
      `Otherwise`, condition `PeutCouvrirLeCout`.
- [x] Étape 5 : « You **may** spend … **Otherwise** » → branche payante
      offerte seulement si payable, sinon Otherwise ; « from **the villain** to
      **your** identity » / « from **an** identity to the villain » ; « this
      card gains surge » dans la branche Otherwise seulement.
      ⚠ Écart assumé : `PeutCouvrirLeCout` compte les icônes IMPRIMÉES de la
      main et de la réserve ; un générateur en jeu (support à ressource) n'est
      pas compté : la branche payante peut être cachée alors qu'elle serait
      payable par ce seul moyen.
- [x] Étape 6 : RRR, boost 1.
- [x] Étape 7 : `… [physical] x3 payes : une oeuvre revient du vilain a
      l'identite`, `… sinon : … va au vilain et surge`. Subst : `60127` rouges 2/2 ;
- [x] 7 bis NON · 8 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué. · 8 bis : couvert par `fne-oeuvre-volee`.
- Carte terminée : OUI

#### 60182 : Cop
- [x] Étape 2 : `WhenUnitWouldScheme` + `SetBeInstead` (RECETTES §2
      « instead »), `BasicAttack([vilain])` ; When Defeated →
      `PlaceThreatOnSchemes("MainScheme", 2)` ; Quickstrike / Vulnerable = bases.
- [x] Étape 5 : « would scheme … **instead** » → l'activation est remplacée
      (menace 0 mesurée, 2 dégâts sur le vilain) ; « Place 2 threat on the
      main scheme ».
- [x] Étape 6 : PV 3, ATK 2, SCH ★ (0), 2 menaces, boost 0.
- [x] Étape 7 : `… manigance remplacee par une attaque contre le vilain`,
      `… When Defeated : 2 menaces`. Subst : `60182` rouges 2/2 ;
- [x] 7 bis NON · 8 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué. · 8 bis NON.
- Carte terminée : OUI

#### 60183 : Crooked Cop
- [x] Étape 2 : `WhenUnitBeDefeated.GetDefeatingPlayer()` +
      `DealEncounterCards(1)` ; `27080` (`TakeIndirectDamage` en boost).
- [x] Étape 5 : « The **defeating** player » (pas le joueur engagé) ; « deals
      **themself** » ; « **indirect** damage ».
- [x] Étape 6 : PV 4, ATK 2, SCH 1, 1 carte, 2 dégâts, boost ★ seule.
- [x] Étape 7 : `… vaincu par le heros : ce joueur recoit 1 carte rencontre
      face cachee`, `… Boost : 2 degats indirects (1 ATK + 2)`. Subst : `60183` rouges 2/2 ;
- [x] 7 bis NON · 8 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué. · 8 bis NON.
- Carte terminée : OUI

#### 60184 : Wanted
- [x] Étape 2 : `dz019` (obligation qui reste en jeu, action à coût),
      `11025` Rampage (`DiscardEncounterCardsUntil` + `PutIntoPlay`) ;
      **correctif moteur** `obligation.py` (obligation sans « Give to »).
- [x] Étape 5 : « until a POLICE minion is discarded » → `trait="POLICE"` ;
      « put it into play **engaged with you** » (PutIntoPlay par le joueur
      engage) ; « Discard this card » → `DiscardAll([this])` explicite.
- [x] Étape 6 : boost 2.
- [x] Étape 7 : `… Hero Action : un sbire POLICE sort du deck engage avec moi,
      l'obligation part`. Subst : `60184` rouges 1/1 ;
- [x] 7 bis NON · 8 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué. · 8 bis : obligation en `obligations_area` (générique) ; couvert.
- Carte terminée : OUI

#### 60185 : Police Cordon
- [x] Étape 2 : `GiveKeywordToInPlayWhenApplyThis(CardFinder(trait=POLICE,
      Minion), guard=1, patrol=1)` (liste, déballage `*`), `01095` pour la
      recherche + `Reveal` ; Hinder = base desc (`1*`).
- [x] Étape 5 : « **Each** POLICE minion » → filtre continu ; « gains guard and
      patrol » → deux mots-clés ; « Search … and **reveal** it ».
- [x] Étape 6 : 3 menaces + Hinder 1[per_hero] = 4 mesurées ; boost 3.
- [x] Étape 7 : `… les sbires POLICE gagnent garde et patrouille ; Hinder 1 :
      4 menaces` (`fne_garde_patrouille`), `… When Revealed : revele un sbire
      POLICE du deck`. Subst : `60185` rouges 2/2 ;
- [x] 7 bis NON · 8 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué. · 8 bis NON.
- Carte terminée : OUI

#### 60191 : Flight Serum
- [x] Étape 2 : `AttachToFaceWhenPutIntoPlay(CardFinder(non_trait=AERIAL,
      Enemy), if_cannot_gain_surge=True)`, `GiveKeywordToAttached("Character",
      trait="AERIAL")`, `18027` In A Bind (`CostFunc.Discard("YourHandCards",
      trait="ATTACK", card_type=Event)`) ; `SCH+`/`ATK+` = bases.
- [x] Étape 5 : « Attach to a **non**-AERIAL enemy. **Otherwise**, surge » →
      `if_cannot_gain_surge` ; « Attached enemy gains AERIAL » ; « Discard an
      ATTACK event from your hand **→** » = coût.
- [x] Étape 6 : +1 SCH, +1 ATK, boost 2.
- [x] Étape 7 : `… s'attache a un ennemi non-AERIAL, qui gagne AERIAL, +1 ATK
      et +1 SCH`, `… aucun ennemi non-AERIAL : surge`, `… Hero Action :
      defausser un evenement ATTACK`. Subst : `60191` rouges 3/3 ;
- [x] 7 bis NON · 8 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué. · 8 bis : couvert par `fne-oeuvre-volee` (sérum dessiné sur le vilain).
- Carte terminée : OUI

#### 60192 : * Mister Fish
- [x] Étape 2 : `04027` Crossfire (`UnitAttackGainKeyword`), `45135`
      (`EngagePlayer`) ; `PlayerFinder` ne trie pas par PV : `min(health)`.
- [x] Étape 5 : « attacks gain piercing **and** ranged » → les deux ; « engages
      the player whose identity has the **fewest** remaining hit points » →
      partie à DEUX pour l'exercer.
- [x] Étape 6 : PV 4, ATK 2, SCH 1, boost 2.
- [x] Étape 7 : `… engage le joueur dont l'identite a le moins de PV (partie a
      deux)`, `… piercing : la robustesse saute et 2 degats passent`, `…
      ranged : la riposte de Black Panther ne le touche pas`. Subst : `60192` rouges 3/3 ;
- [x] 7 bis NON · 8 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué. · 8 bis NON.
- Carte terminée : OUI

#### 60193 : * The Owl
- [x] Étape 2 : `04027` Crossfire (exact : permanent + boost `during_attack`).
- [x] Étape 5 : « If this activation is an attack » → `during_attack=True` ;
      ★ permanent ≠ ★ Boost (fiches `special`, `boost`).
- [x] Étape 6 : PV 5, ATK 2, SCH 3, boost ★ seule.
- [x] Étape 7 : `… piercing : la robustesse saute`, `… Boost pendant une
      attaque : l'attaque de Hammerhead devient perforante`, contre-cas
      `… la riposte de Black Panther touche The Owl` (pas ranged). Subst : `60193` rouges 2/3 (contre-cas d'absence d'effet, vert par construction) ;
- [x] 7 bis NON · 8 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué. · 8 bis NON.
- Carte terminée : OUI

#### 60194 : Swoop Down
- [x] Étape 2 : `32117` Master Mold's Children (vilain puis sbires engagés),
      `04086` (`additional_value`) ; déroulé à la main pour porter le +2 par
      ennemi AERIAL.
- [x] Étape 5 : « The villain **and** each minion engaged with you » → vilain
      d'abord, puis chaque sbire engagé encore en jeu ; « **Each** AERIAL enemy
      gets +2 … for **its** activation » → propriété par ennemi.
- [x] Étape 6 : +2 SCH / +2 ATK, boost 3.
- [x] Étape 7 : `(Hero) … 1 + 4 = 5`, `(Alter-Ego) … 2 + 5 = 7`. Subst : `60194` rouges 2/2 ;
- [x] 7 bis NON · 8 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué. · 8 bis NON.
- Carte terminée : OUI

### 6. Gates statiques du bloc (18/09/2026)

- `test_cards` : 5598 ok / 0 err ; `verifier_api_cartes` : 0 fichier fne en faute ;
  `audit_cartes` : aucune suspicion sur les 27 cartes ; `verifier_coherence_cartes`
  : rien sur le bloc ; `verifier_appels_modules fne` : OK ; `verifier_noms_modules fne` : OK.
- Harnais : **57/57 cas `[fne]`** (PARALLELES=4, port 40000).
- Substitution : 27/27 modules prouvés (5 passes `substituer_pack.py`, préfixes 6008/6009/6012/6018/6019, ports 31000-35800) ; empreinte md5 du pack identique avant/après (`6dd56080…`). Deux cas restent verts sans module, tous deux des contre-cas d'ABSENCE d'effet : `60093` « non étourdi, seul le boost Villainous » et `60193` « la riposte de Black Panther touche The Owl » (pas ranged).
- Autoplay : 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué.
- Passe complète des decks (fichiers partagés touchés) : 135/136 (14:37 → 15:01). L'échec, `superior_iron_man`, est étranger au pack : `si012.py` Spectacular Save appelait `GetControlByPlayer()` sur l'ennemi qui subit les dégâts (assert `isinstance(owner, Player)`) dès que la carte était en main lors d'une attaque du héros. Corrigé à la source (`GetControlByOrOwner` + `Player.IsType`), deck remonté sur `.game-src-b2` : OK (identité si001a, main 6, deck 9). → 136/136.
- Batterie complète `test_capacites` : **1987/1991** (15:01 → 16:18, PARALLELES=4, port 40000). Les 4 rouges sont les rouges PRÉEXISTANTS de `.planning/todos/2026-08-31-cas-rouges-sg-ss.md` (`sg006`, `sg007`, `sg009`, `sg013`) ; rejoués un par un : toujours rouges ; `sg009` rejoué avec `obligation.py` et `card_face.py` remis à l'état git (stash) : toujours rouge → aucune régression du bloc 1. `launch.json` principal vérifié : `127.0.0.1:2345`.
- Plateau : `ui-app/src/board/fne-oeuvre-volee.test.ts` 3/3.

### 7. Ce que ces gates ne voient pas (à dire en fin de bloc)

- Aucune partie humaine jouée dans le navigateur sur ce scénario.
- L'overkill de Head First! (voir gabarit 60096).
- `PeutCouvrirLeCout` ignore les générateurs de ressources EN JEU (gabarit 60127).
- La modale de choix du vilain n'existe pas encore : avec un seul underling
  porté, la tuile « Art Museum Heist (Hammerhead) » suffit ; la modale arrive
  avec Bullseye (bloc 2).

## Bloc 2 — Bullseye, Electro, Purple Man, Typhoid Mary (18/09/2026)

### 1. Inventaire → card_id (50 cartes, 4 sets)

- **Bullseye** (`bullseye.json`, `art_museum_heist_bullseye[_expert].json`) :
  60065/60066/60067 * Bullseye I-II-III ; 60068a,60068b * Adamantium-Laced
  Spine / * Damaged Spine (une carte, deux faces) ; 60069 Raise the Stakes ;
  60070 Deadly Sai ; 60071 ×3 Incessant Pursuit ; 60072 * Lady Bullseye ;
  60073 Deranged Bloodlust ; 60074 Everything is a Weapon ; 60075 ×2 Unerring
  Desire.
- **Electro** (`electro_fne.json`, nom « Electro » ; `electro.json` est déjà
  pris par Web of Deceit) : 60076/60077/60078 * Electro I-II-III ; 60079
  * Electric Charge ; 60080 Drained of Power ; 60081 * Whiplash ; 60082 ×2
  Charging Up ; 60083 ×2 Chain Lightning ; 60084 ×2 Energy Overload ; 60085 ×2
  Shocking Revelation.
- **Purple Man** (`purple_man.json`) : 60097/60098/60099 * Purple Man I-II-III ;
  60100 Converted ; 60101 ×2 Firefighter ; 60102 Judge ; 60103 Security
  Guard ; 60104 Skater Punk ; 60105 « Fight. » ; 60106 « Protect. » ; 60107
  « Serve. » (obligations à Uses 3 command) ; 60108 Power of Suggestion ;
  60109 ×2 Sway the Masses ; gabarit `influenced_minion` (pack `""`) pour
  Converted.
- **Typhoid Mary** (`typhoid_mary.json`) : 60110a,60110b * Typhoid Mary /
  * Bloody Mary (A, normal) ; 60111a,60111b (B, expert) ; 60112 Disturbed
  Psyche (Setup) ; 60113a,60113b Establish Trust / * Mary Walker (complot
  Permanent Setup ↔ attachement) ; 60114 Telekinesis ; 60115 ×2 Psionic
  Slash ; 60116 Psi Nova ; 60117 Assembled Armor ; 60118 ×2 Hail of Blades ;
  60119 Scavenged Bulwark ; 60120 ×3 Hand Lookout.
- Scénarios : `art_museum_heist_<vilain>.json` (+ `_expert`), stades
  `[I, II]` / `[II, III]`, Typhoid Mary à stade unique déclaré
  `"60110a,60110b"` / `"60111a,60111b"` (les deux faces d'une même carte).
- `sets_info.json` « 60. Fear No Evil » : scenarios + underlings complétés
  (bullseye, electro, purple_man, typhoid_mary).

### 2. Fichiers écrits

- `src/cards/pack/fne/bullseye/` (`__init__.py` : `TrouverBullseye`,
  `DeadlySaiAttache`, `CapacitesDeBullseye`, `RetournerLaColonne` ; 11 scripts),
  `electro/` (`TrouverElectro`, `Charges`/`PoserCharges`/`RetirerCharges`,
  `CapacitesDElectro`, `ChoixPayerEnergieOuDeux` ; 10 scripts),
  `purple_man/` (`CapacitesDePurpleMan`, `ObligationCommandee` ; 13 scripts),
  `typhoid_mary/` (`TrouverMary`, `MaryActive`, `JetonsPsyche`,
  `VerifierVictoire`, `FlipMaryWalkerVersEstablishTrust`, `CapacitesDeMary` ;
  16 scripts).
- `data/cards.json` (+ checksums), 4 sets, 8 scénarios, `sets_info.json`.
- Harnais : 91 cas `[fne2]` (générateur `scratchpad/b2/gen_cas_fne_b2.py`,
  session 258dc511) + vérificateurs `fne_mots_cles`, `fne_converti`,
  `fne_carte_distribuee`, `fne_mis_de_cote_scenario`, `fne_setup_psyche`,
  `fne_fin_phase_vilain`, `fne_fin_de_round`, `fne_partie_gagnee`.
- Docs : `RECETTES-MOTEUR.md` §7quater (9 pièges), fiches
  `mots-cles/setup.md` et `mots-cles/forced-action.md`.

### 3. Fichiers PARTAGÉS touchés (→ passe complète des decks + batterie complète dues)

- `src/game/ability/factory/treat.py` (CORRECTIF, deux sites) :
  `TreatAttachedCardAsMinion`/`TreatAsMinion` effaçaient par `ResetKeywords`
  les mots-clés donnés au sbire à son entrée en jeu par `SwapCardFace`
  (Guard de Purple Man sur Converted). Les gains venus d'autres faces sont
  sauvés et remis après le reset.
- `src/game/card/face/card_type/scheme_side.py` (CORRECTIF) : un complot
  annexe Permanent n'envoyait jamais `WhenSchemeBeDefeated` (`pass`) ; les
  messages partent, la défausse reste sautée (60113a Establish Trust).
- `src/cards/pack/fne/__init__.py` : `PeutCouvrirLeCout` exige aussi la
  quantité (`Resources.CanPayThisCost` ne teste que la couleur).
- Déjà au bloc 1 : `card_face.py` (traits MAGGIA/POLICE/INFLUENCED/HAND/NINJA,
  compteur `drain`, jeton `damage`), `obligation.py`, `si012.py`.

### 4. Ce que le harnais a trouvé (5 passes : 47/85 → 56/87 → 76/87 → 83/87 → 87/87)

- **Vilain recto-verso déclaré sur une face** (`"villain": ["60110a"]`) :
  `card.Flip` retournait Typhoid Mary FACE CACHÉE (21 rouges). → les deux
  faces dans le scénario. MaGog n'était pas un modèle : il ne se retourne pas.
- **Le Setup de Disturbed Psyche ne partait pas** (`WhenCardSetup` jamais
  envoyé à une carte posée par le mot-clé). → `AfterGameSetup`. Sous graine
  42 la partie commence sur Bloody Mary : cas recalés, `TYPHOID` =
  `Puzzle.Flip('60110b')`.
- **`card.Flip` d'un attachement le détache** et la face B restait dans les
  limbes (« Bullseye perd l'amélioration », puis rien) ; et le harnais, ne
  trouvant pas la copie mise de côté, CRÉAIT la colonne sur un seul id (sans
  face arrière). → `RetournerLaColonne` (démarquer + raccrocher) et
  `PutIntoPlay('60068a,60068b')`.
- **Lady Bullseye** : `GiveAdditionalBoostCardForThisActivation` sur le
  message d'attaque vise la PROCHAINE activation. → carte posée face cachée
  par `GiveFacedownBoostCardsInternal` (4 → 7 dégâts).
- **Converted sans guard** : trace `DEBUG` dans treat.py, `Guard: {Purple
  Man: 1}` avant `ResetKeywords`, plus rien après. → correctif moteur (§3) ;
  la première tentative (reset AVANT l'échange) plantait : `ResetKeyword(self)`
  exige une face déjà portée par une carte.
- **Establish Trust jamais vaincue** : `EncounterSideScheme.OnBeDefeated`
  fait `pass` pour Permanent. → correctif moteur (§3) ; 5 cas Mary Walker
  suivaient.
- **Drained of Power** : `Puzzle.Ready('01008')` redressait la copie de
  Web-Shooter restée dans le deck (→ `EmptyPlayerDeck`) ; et la branche
  « 2 ressources » était offerte avec une seule carte (`CanPayThisCost` ne
  teste que la couleur) → quantité exigée dans `PeutCouvrirLeCout`.
- **Electro III / Psionic Slash** : le Confused d'Impossible Object survit à
  `ARTS_OFF` et remplace la manigance. → `Puzzle.Confuse` (bascule).
- **Expert** : le Setup retourne aussi la vilaine expert (60111b), et sa
  Toughness absorbe le premier `Puzzle.Damage` (Assembled Armor). → 1 puis 5
  puis 3.
- **Psionic Slash** : Great Responsibility jouée par le pilote encaissait la
  menace. → `main_exclusive: ["01088"]` ; Bloody Mary SCH 1 → 1 menace, pas 2.
- Détail complet : `RECETTES-MOTEUR.md` §7quater.

### 5. Gabarits PROCESSUS-CARTE (un par carte)

Conventions : « cas » = nom dans `tools/test_capacites.py` (préfixe = card_id,
filtre `[fne2]`) ; « subst » = verdict de `tools/substituer_pack.py` ; les
mots-pièges de l'étape 5 sont listés quand la carte en porte.

#### 60065 / 60066 / 60067 : * Bullseye (I, II, III)
- [x] Étape 2 : `SetupCards.SetAsideCards` (mise de côté nommée), `Find.FindAndAttachTo` / `Find.FindAndReveal` (find.py:74, fouille mise de côté + deck + défausse), `IncreaseBoostIconsOnEncounterCard` (bc/sd020 pour le contexte de boost), `WhenUnitWouldAttack` + `GainRanged` (Deadly Sai lu par `DeadlySaiAttache`).
- [x] Étape 5 : « Find » ≠ « Search » (aucune fouille de deck offerte au joueur, la carte est PRISE où qu'elle soit) ; « each boost card **dealt to him** » → seulement SES boosts, pendant SON activation (drapeau d'activation, sinon l'icône comptait aussi les cartes en zone de boost d'un sbire) ; « his attacks gain ranged unless Deadly Sai » → lu à chaque attaque, pas figé.
- [x] Étape 6 : PV 14/16/18[per_hero], ATK 1/2/3, SCH 0/1/1 ↔ `desc` ; `Stage` A/B/C ; When Revealed I = mise de côté, II = attache, III = révèle Deranged Bloodlust.
- [x] Étape 7 : `60065 … When Revealed : la colonne d'adamantium est mise de cote a la mise en place`, `60065 … chaque carte boost gagne une icone : 1 ATK + (0+1) = 2`, `60065 … son attaque gagne ranged : la riposte de Black Panther ne le touche pas`, `60066 … 60066 Bullseye II [fne2] (expert) — When Revealed : la colonne est trouvee et attachee a la mise en place`, `60067 … 60067 Bullseye III [fne2] (expert) — When Revealed : Deranged Bloodlust est trouvee et revelee`. Subst : `60065` rouges 3/3 ; `60066` rouges 1/1 ; `60067` rouges 1/1.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON (vilain standard, jauges génériques).
- Carte terminée : OUI

#### 60068a,60068b : * Adamantium-Laced Spine / * Damaged Spine
- [x] Étape 2 : `WhenUnitWouldTakeDamage` + `PreventDamage` (60117 même patron), compteur `damage` sur l'attachement (`PlaceCountersOn`/`RemoveCountersOn`), `AfterUnitSchemeEnd(Bullseye)`, retournement par `RetournerLaColonne` (card.Flip + démarquage + `OnAttachTo`, voir RECETTES §7quater).
- [x] Étape 5 : « prevent all but 3 » → évité = total − 3 (jamais négatif) ; « place the prevented damage **here** » → compteurs sur l'attachement, PAS des dégâts ; « if there is **6 or more** » → ≥ 6 après la pose ; « if there is **no** damage » → ≤ 0 après le retrait de 3 ; Permanent = base, la carte ne quitte jamais le jeu, elle se retourne.
- [x] Étape 6 : une carte à deux faces (`"60068a,60068b"` dans le set), Permanent, TECH ; seuils 6 et 0.
- [x] Étape 7 : `60068a … 5 degats : 3 passent, 2 sont poses sur la colonne`, `60068a … a 6 degats poses, la carte se retourne (Damaged Spine) et reste attachee`, `60068b … apres une manigance de Bullseye, 3 degats sont retires (6 -> 3)`, `60068b … plus aucun degat : la carte se retourne (Adamantium-Laced Spine)`. Subst : `60068a` rouges 2/2 ; `60068b` rouges 2/2.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON (compteurs génériques sur attachement).
- Carte terminée : OUI

#### 60069 : Raise the Stakes
- [x] Étape 2 : `02020` Hysteria (boost supplémentaire dans `WhenUnitWouldAttack`), `01099` Charge (`RunAt.AfterEnemyActivationEnd`), `24023` Out for Blood (capacité Temp `WhenUnitBeDefeated(Friend)` bornée à l'attaque en cours), `RemoveAllFromGame` / `ShuffleAllTo("EncounterDeck")`.
- [x] Étape 5 : « **If this attack defeats** a friendly character » → il faut SAVOIR qui a été vaincu PENDANT cette attaque (capacité temporaire, retirée à la fin) ; « remove **them and this card** » → l'allié ET Raise the Stakes ; « Otherwise, shuffle » → dans le deck rencontre, pas la défausse.
- [x] Étape 6 : attaché à Bullseye, +1 boost par attaque ; deux issues exclusives.
- [x] Étape 7 : `60069 … 1 carte boost de plus ; personne n'est vaincu : la carte retourne dans le deck`, `60069 … l'attaque vainc un allie defenseur : l'allie ET la carte sont retires du jeu`. Subst : `60069` rouges 2/2.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60070 : Deadly Sai
- [x] Étape 2 : `desc.ATK+` = +2 ATK natif ; `UnitAttackGainKeyword(piercing)` ; « lose ranged » lu par `DeadlySaiAttache` dans la capacité étoilée de Bullseye ; `AfterUnitDefendAgainstAttack("You", attacker=Bullseye)` + `Cost("2", different_type=True)` (`05002` Red Dagger).
- [x] Étape 5 : « lose ranged **and** gain piercing » → les deux ; « **your hero** defends » → défense par le héros (pas un allié) contre Bullseye précisément ; « 2 **different** resources » → `different_type=True`, deux icônes distinctes.
- [x] Étape 6 : +2 ATK, WEAPON, attaché à Bullseye.
- [x] Étape 7 : `60070 … Bullseye perd ranged (la riposte le touche) et gagne piercing (+2 ATK)`, `60070 … Hero Response apres une defense du heros : 2 ressources differentes -> defaussee`. Subst : `60070` rouges 2/2.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60071 : Incessant Pursuit
- [x] Étape 2 : `21178` Beguiled (finder `not_with_attach`), `50096` Leaping Kick (`BasicAttack([allié], overkill)`), RECETTES §2 « instead » (`SetBeInstead`), garde de récursion (l'attaque redirigée ne doit pas redéclencher l'interruption).
- [x] Étape 5 : « Attach to an ally **without** Incessant Pursuit attached. Otherwise, surge » → trois exemplaires, le finder exclut les alliés déjà poursuivis ; « the villain would attack **you** » → le contrôleur de l'allié attaché ; « it attacks attached ally **instead** » → remplacement, l'attaque de base contre le joueur n'a pas lieu ; « If this attack defeats attached ally, remove them from the game ».
- [x] Étape 6 : 3 exemplaires, CONDITION.
- [x] Étape 7 : `60071 … s'attache a un allie ; le vilain attaque cet allie a la place du joueur`, `60071 … l'allie attache est vaincu : il est retire du jeu`. Subst : `60071` rouges 2/2.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60072 : * Lady Bullseye
- [x] Étape 2 : `WhenBoostCardWouldTurnedFaceUp(while_attack=True, boost_for_card="This")` (`bc007`/`sd020`), `CanBoost.GiveFacedownBoostCardsInternal` (sender_card.py:751), Villainous = base desc.
- [x] Étape 5 : « When **resolving** boost cards » → la fenêtre est la résolution (défenseur connu), pas la déclaration ; « if that attack is **undefended** » → `being_message.defender is None` ; « 1 additional boost card » → UNE fois par attaque (drapeau sur le message), même si plusieurs boosts se retournent.
- [x] Étape 6 : ASSASSIN, HAND, Villainous ; ATK 1 → 1 + 3 + 3 = 7 sans défense, 1 + 3 − 3 = 1 défendue.
- [x] Étape 7 : `60072 … attaque non defendue : Villainous + 1 carte de plus (1 + 3 + 3 = 7)`, `60072 … contre-cas defendue par le heros : une seule carte boost (1 + 3 - DEF 3 = 1)`. Subst : `60072` rouges 1/2.
- [x] Étape 7 bis : une fois par attaque : contre-cas « défendue par le héros » = une seule carte.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60073 : Deranged Bloodlust
- [x] Étape 2 : `01109` Bomb Scare (menace additionnelle à la révélation), `07009` Escaped Convict (`message.AfterThisActivation`), `Worlds.FindVillain().printed_stage`.
- [x] Étape 5 : « equal to Bullseye's **stage number** » → 1/2/3 lu sur la face active ; « Boost: **After this activation**, reveal this card » → pas pendant, après (RunAt).
- [x] Étape 6 : complot annexe 4 + stade, aléa = base.
- [x] Étape 7 : `60073 … When Revealed : 4 + stade de Bullseye (1) = 5 menaces`, `60073 … Boost : apres l'activation, la carte est revelee`. Subst : `60073` rouges 2/2.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60074 : Everything is a Weapon
- [x] Étape 2 : `27080` (indirect), `08013` (`ChooseAbilities` à deux branches), `11041` Deathunt (`GiveBoostCardForThisActivation` en contexte de boost) + `GainPiercing`.
- [x] Étape 5 : « When Revealed (Alter-Ego) / (Hero) » → deux textes selon la forme ; « Bullseye **activates** against you » → `DoActivate` (attaque OU manigance selon la forme) ; « Boost: **If Bullseye is attacking** » → seulement si l'ennemi actif est Bullseye ET que c'est une attaque.
- [x] Étape 6 : 2 indirects (AE) ; 1 + 1 = 2 (branche activation) ; 1 + 2 + 1 = 4 avec piercing (robustesse sautée).
- [x] Étape 7 : `60074 … 60074 Everything is a Weapon [fne2] (Alter-Ego) — 2 degats indirects`, `60074 … 60074 Everything is a Weapon [fne2] (Hero) — premiere branche : Bullseye s'active contre toi (1 + 1 = 2)`, `60074 … 60074 Everything is a Weapon [fne2] (Hero) — seconde branche : un allie que tu controles est retire du jeu`, `60074 … Boost pendant l'attaque de Bullseye : 1 carte de plus et piercing (1 + 2 + 1 = 4, robustesse sautee)`. Subst : `60074` rouges 4/4.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60075 : Unerring Desire
- [x] Étape 2 : `56091` (`villain.GiveBoostCard`), `an013` Hel-Wolf (`GainOverKill` en boost), `ChooseAbilities`.
- [x] Étape 5 : « give **this card** to the villain as a facedown boost card » → la carte elle-même quitte la zone de révélation ; « a PERSONA support **you control** » → trait PERSONA, soutien, contrôlé ; « Boost: If this activation is an attack » → overkill seulement en attaque.
- [x] Étape 6 : 2 exemplaires.
- [x] Étape 7 : `60075 … premiere branche : donnee au vilain comme carte boost face cachee`, `60075 … seconde branche : un soutien PERSONA que tu controles est retire du jeu`. Subst : `60075` rouges 2/2.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60076 / 60077 / 60078 : * Electro (I, II, III)
- [x] Étape 2 : `CapacitesDElectro(charges_par_manigance, charges_au_reveil)` : `AfterUnitSchemeEnd` ForcedResponse + `PoserCharges` ; I = When Revealed attache Electric Charge avec 2[per_hero] charges (`Find.FindAndAttachTo`), III = +3[per_hero] à la révélation.
- [x] Étape 5 : « After Electro schemes » → après la manigance (Response), pas pendant ; « [per_hero] » → `GetPlayerNumIcon` ; charges = compteurs `charge` sur Electric Charge, pas sur Electro.
- [x] Étape 6 : PV/ATK/SCH ↔ desc ; +1/+1/+2 charge par manigance.
- [x] Étape 7 : `60076 … When Revealed : Electric Charge attachee avec 2[per_hero] charges a la mise en place`, `60076 … apres une manigance : +1 charge (2 -> 3)`, `60077 … stade II revele : +2[per_hero] charges (Find deja attachee), puis +1 par manigance (2 + 2 + 1 = 5)`, `60078 … 60078 Electro III [fne2] (expert) — a la revelation +3[per_hero] charges, puis +2 par manigance (2 + 3 + 2 = 7)`. Subst : `60076` rouges 2/2 ; `60077` rouges 1/1 ; `60078` rouges 1/1.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60079 : * Electric Charge
- [x] Étape 2 : `CostFunc.Counter("This", 1, 'charge')` (le retrait est le COÛT, la flèche) + `GiveAdditionalBoostCardForThisActivation` + `GainOverKill` dans `WhenUnitWouldAttack` ; deux Hero Actions `Cost("Y")` / `Cost("2")` (RECETTES §5 « or »).
- [x] Étape 5 : « remove 1 charge counter **→** » → coût : sans charge, rien ne se déclenche (contre-cas) ; « Spend a [energy] resource **or** 2 resources of any type » → deux capacités, chacune payable séparément ; Permanent = base.
- [x] Étape 6 : attachée à Electro ; 1 + 3 + 3 = 7 avec charge, 1 + 3 = 4 sans.
- [x] Étape 7 : `60079 … quand Electro attaque : 1 charge depensee, 1 carte boost de plus et overkill (1 + 3 + 3 = 7)`, `60079 … contre-cas sans charge : une seule carte boost (1 + 3 = 4)`, `60079 … Hero Action [energy] : retire 1 charge`, `60079 … Hero Action 2 ressources quelconques : retire 1 charge`. Subst : `60079` rouges 3/4.
- [x] Étape 7 bis : coût épuisable : contre-cas « sans charge » = une seule carte boost.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60080 : Drained of Power
- [x] Étape 2 : `50153` (`AttachToFaceWhenPutIntoPlay("YourIdentity")`), `Faces.ExhaustAll`, `WhenCardWouldReady(control_by="You")` + `SetBeInstead`, `ChoixPayerEnergieOuDeux` + `Otherwise` ; Uses (3 drain) = base desc.
- [x] Étape 5 : « exhaust **each upgrade** you control » → tous, pas un ; « When an upgrade you control **would ready** » → interruption sur le redressement ; « **you may** spend » → choix, `Otherwise` = ne se redresse pas ; « If you do, remove 1 drain counter » → et le redressement a lieu ; Uses : la carte sort au dernier pion (natif, non recodé).
- [x] Étape 6 : 3 drain ; [energy] ou 2 quelconques.
- [x] Étape 7 : `60080 … When Revealed : attachee a l'identite, les ameliorations sont inclinees`, `60080 … une amelioration se redresse en payant [energy] : 1 drain de moins`, `60080 … sans ressource : l'amelioration ne se redresse pas`. Subst : `60080` rouges 3/3.
- [x] Étape 7 bis : 3 usages (Uses) : natif.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60081 : * Whiplash
- [x] Étape 2 : `WhenUnitWouldBeAttacked` + `CostFunc.Counter(CardFinder(name="Electric Charge"), 1, 'charge')`, `Worlds.DiscardEncounterTopCard`, `FacesCounter.CountTotalBoostIcons`, `TakeDamage` sur `message.trigger` (l'attaquant).
- [x] Étape 5 : « remove 1 charge counter from Electric Charge **→** » → coût pris sur UNE AUTRE carte ; « for **each boost icon** on the discarded card » → icônes chiffrées, pas les étoiles.
- [x] Étape 6 : CRIMINAL ; 3 dégâts pour Under Fire (3 icônes).
- [x] Étape 7 : `60081 … attaque : 1 charge depensee, la carte du dessus est defaussee, 1 degat par icone (3)`. Subst : `60081` rouges 1/1.
- [x] Étape 7 bis : coût épuisable (charges).
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60082 : Charging Up
- [x] Étape 2 : `WhenSchemeBeDefeated(WhenDefeated, "This")` + `PoserCharges(3)`.
- [x] Étape 5 : « When Defeated » → à la défaite du complot, pas à sa révélation.
- [x] Étape 6 : complot 6, aléa = base, 2 exemplaires.
- [x] Étape 7 : `60082 … vaincue : +3 charges (2 -> 5)`. Subst : `60082` rouges 1/1.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60083 : Chain Lightning
- [x] Étape 2 : `ForChoiceAbility` par personnage contrôlé (`GetOnFieldFriendlyCharacters`), `Charges` > 0 → 3 dégâts au lieu de 1, `RetirerCharges(1)`.
- [x] Étape 5 : « **For each** character you control, choose » → un choix PAR personnage ; « 3 damage instead if there are **any** charge counters » → lu au moment du choix ; « Remove 1 charge counter » → sur la seconde branche seulement.
- [x] Étape 6 : 2 exemplaires.
- [x] Étape 7 : `60083 … premiere branche : le personnage est incline`, `60083 … seconde branche : 3 degats (charges presentes) et 1 charge de moins`. Subst : `60083` rouges 2/2.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60084 : Energy Overload
- [x] Étape 2 : `FacesCounter` sur la main (`has_printed_res="Y"`), `ThisCardGainSurge`, `ForChoiceAbility` par carte : défausser / étourdir un personnage.
- [x] Étape 5 : « no cards with a **printed** [energy] resource in your hand » → icône imprimée, pas les générateurs ; « Otherwise, **for each** card » → un choix par carte [energy].
- [x] Étape 6 : 2 exemplaires.
- [x] Étape 7 : `60084 … une carte [energy] en main : defaussee (premiere branche)`, `60084 … aucune carte [energy] en main : surge`. Subst : `60084` rouges 2/2.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60085 : Shocking Revelation
- [x] Étape 2 : `player.DiscardDeckTopCards(n)`, n = cartes contrôlées (`GetControlByOrOwner() is joueur` + `Player.IsType`, identité comprise), `ForChoiceAbility` par carte [energy] défaussée : 1 indirect / +1 charge.
- [x] Étape 5 : « for **each card you control** » → tout ce qui est en jeu sous ton contrôle, identité comprise (assert `GetControlByPlayer` sur une carte non-joueur : `GetControlByOrOwner`) ; « **printed** [energy] » → icône imprimée.
- [x] Étape 6 : 2 exemplaires.
- [x] Étape 7 : `60085 … 1 carte du deck par carte controlee ; Energy defaussee -> 1 degat indirect`, `60085 … seconde branche : +1 charge (2 -> 3)`. Subst : `60085` rouges 2/2.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60097 / 60098 / 60099 : * Purple Man (I, II, III)
- [x] Étape 2 : `CapacitesDePurpleMan(guard, villainous, patrol)` = `*GiveKeywordToInPlayWhenApplyThis(CardFinder(trait="INFLUENCED", card_type=Minion), ...)` + `WhenCardBecomeBoost(conditions=[du_set])` → `message.AfterThisActivation` + `DealEncounterCard` (`27093` Fearmonger).
- [x] Étape 5 : « Each INFLUENCED minion gains **guard** » (I), « guard **and villainous** » (II), « guard, villainous, **and patrol** » (III) → cumul par stade ; « After a boost card **from this set** is resolved » → set Purple Man seulement (contre-cas d'un autre set) ; « deal that player 1 facedown encounter card » → après l'activation.
- [x] Étape 6 : PV/ATK/SCH ↔ desc.
- [x] Étape 7 : `60097 … chaque sbire INFLUENCED gagne guard (pas patrol ni villainous)`, `60097 … une carte boost du set Purple Man est distribuee au joueur apres l'activation`, `60097 … contre-cas : une carte boost d'un autre set n'est pas distribuee`, `60098 … 60098 Purple Man II [fne2] (expert) — guard ET villainous, pas patrol`, `60099 … 60099 Purple Man III [fne2] (expert) — guard, villainous ET patrol`. Subst : `60097` rouges 2/3 ; `60098` rouges 1/1 ; `60099` rouges 1/1.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60100 : Converted
- [x] Étape 2 : `21178` Beguiled : `TreatAttachedCardAsMinion(Ally, "Influenced Minion", engager)` sur le gabarit `influenced_minion` (trait INFLUENCED, texte vide, SCH = THW imprimé, sans dégâts consécutifs) ; `Filter.One(highest_cost=True)` ; `ThisCardGainSurge`.
- [x] Étape 5 : « Treat attached ally as an INFLUENCED minion with a **blank text box** » → gabarit vide ; « SCH is equal to its **base** THW » → THW imprimé ; « does not take consequential damage » → natif au gabarit ; « attach to the **highest-cost** ally you control **and engage it** » → `EngagePlayer` dans le `process` ; « Otherwise, surge ».
- [x] Étape 6 : guard vient de Purple Man (§3 : correctif treat.py), pas de Converted.
- [x] Étape 7 : `60100 … s'attache a l'allie le plus cher, qui devient un sbire INFLUENCED engage, SCH = son THW, guard`, `60100 … aucun allie : surge`. Subst : `60100` rouges 2/2.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON (sbire rendu par l'image de l'allié, `pic_id`).
- Carte terminée : OUI

#### 60101 : Firefighter
- [x] Étape 2 : `UnitAttackGainKeyword(piercing)`, `WhenUnitBeDefeated` + `Filter.One(highest_cost=True)` sur soutiens + améliorations ; Vulnerable = base.
- [x] Étape 5 : « the highest-cost support **or** upgrade **from play** » → les deux types confondus, un seul défaussé.
- [x] Étape 6 : CIVILIAN, INFLUENCED, 2 exemplaires.
- [x] Étape 7 : `60101 … vaincu : le soutien ou l'amelioration le plus cher est defausse`, `60101 … ses attaques sont perforantes`. Subst : `60101` rouges 2/2.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60102 : Judge
- [x] Étape 2 : `WhenUnitBeDefeated` + `PlaceThreatOnSchemes("MainScheme", 3)`.
- [x] Étape 5 : « Place 3 threat on the **main** scheme ».
- [x] Étape 6 : CIVILIAN, INFLUENCED.
- [x] Étape 7 : `60102 … vaincu : 3 menaces sur le complot principal`. Subst : `60102` rouges 1/1.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60103 : Security Guard
- [x] Étape 2 : `WhenUnitBeDefeated` + `Filter.One(highest_atk=True)` sur `GetOnFieldAllies` ; Patrol, Vulnerable = bases.
- [x] Étape 5 : « the ally with the highest ATK **in play** » → tous joueurs confondus.
- [x] Étape 6 : CIVILIAN, INFLUENCED, Patrol.
- [x] Étape 7 : `60103 … vaincu : l'allie a l'ATK le plus haut est defausse`. Subst : `60103` rouges 1/1.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60104 : Skater Punk
- [x] Étape 2 : `WhenUnitBeDefeated` + `message.killer` → joueur → identité `TakeDamage(3)`.
- [x] Étape 5 : « the **defeating player's** identity » → celui qui l'a vaincu (`killer`), pas le joueur engagé.
- [x] Étape 6 : CIVILIAN, INFLUENCED.
- [x] Étape 7 : `60104 … vaincu par le heros : 3 degats a son identite`. Subst : `60104` rouges 1/1.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60105 / 60106 / 60107 : « Fight. » / « Protect. » / « Serve. »
- [x] Étape 2 : `ObligationCommandee(nom, action)` = `WhenInYourPlayTurn(ForcedAction)` + `CostFunc.Exhaust("This")` + `CostFunc.Counter("This", 1, 'command')` (`ls016`) ; Uses (3 command) = base ; `obligation.py` : `give_to` peut être `None` (obligation de vilain, sans porteur).
- [x] Étape 5 : « Forced Action » → le joueur ne peut pas finir sa phase tant que c'est payable (fiche `forced-action.md`) ; « Exhaust this card **and** remove 1 command counter → » → deux coûts ; « deal 2 damage to a hero **or** ally » / « give the villain a tough status card » / « place 2 threat on the main scheme ».
- [x] Étape 6 : 3 pions : trois usages, puis la carte sort (Uses natif).
- [x] Étape 7 : `60105 … obligation revelee avec 3 pions ; Forced Action : incliner + 1 pion -> 2 degats a un heros ou allie`, `60106 … Forced Action : le vilain devient robuste`, `60107 … Forced Action : 2 menaces sur le complot principal`. Subst : `60105` rouges 1/1 ; `60106` rouges 1/1 ; `60107` rouges 1/1.
- [x] Étape 7 bis : 3 usages (Uses) : natif, non recodé.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60108 : Power of Suggestion
- [x] Étape 2 : `*GiveKeywordToInPlayWhenApplyThis(Minion, trait="INFLUENCED")` ; Hinder 3[per_hero] = base (`[star]`).
- [x] Étape 5 : « **Each** minion gains the INFLUENCED trait » → et donc guard/villainous/patrol de Purple Man par ricochet (mesuré).
- [x] Étape 6 : complot 2, hinder 3 → 5 menaces.
- [x] Étape 7 : `60108 … chaque sbire gagne INFLUENCED (donc guard) ; Hinder 3 : 5 menaces`. Subst : `60108` rouges 1/1.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60109 : Sway the Masses
- [x] Étape 2 : `Search.SearchForCard` limitée à la DÉFAUSSE rencontre (`01095` fouille deck + défausse ; ici défausse seule) + `Reveal`, sinon `ThisCardGainSurge`.
- [x] Étape 5 : « from the encounter **discard pile** » → jamais le deck ; « Otherwise, surge » → défausse sans INFLUENCED.
- [x] Étape 6 : 2 exemplaires.
- [x] Étape 7 : `60109 … un sbire INFLUENCED de la defausse est revele`, `60109 … defausse vide : surge`. Subst : `60109` rouges 2/2.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60110a,60110b / 60111a,60111b : * Typhoid Mary / * Bloody Mary (A et B)
- [x] Étape 2 : `CapacitesDeMary(pv)` : `WhenUnitWouldBeDefeated` + `SetBeInstead` + `ResetHealth("10*"|"13*")` + `PlaceTokensOn(Disturbed Psyche, 'damage')` (`39001a` MaGog) + `VerifierVictoire` ; 60111b : `WhenThisRevealed` → 1 dégât à chaque identité ; Toughness (60111a) = base.
- [x] Étape 5 : « would be defeated » → interruption, la vilaine ne quitte JAMAIS le jeu ; « place 1 damage **token** on Disturbed Psyche » → jeton, pas compteur ; « reset her hit points » → PV pleins ; la face qui apparaît au retournement résout son When Revealed (FAQ du livret).
- [x] Étape 6 : SCH 2/1, ATK 1/2 (A) ; SCH 3/1, ATK 1/3 (B) ; PV 10/13[per_hero] ; une carte à deux faces déclarée `"60110a,60110b"`.
- [x] Étape 7 : `60110a … « vaincue » : 1 jeton damage sur Disturbed Psyche et PV remis a 10`, `60110b … meme reponse sur la face B`, `60111a … 60111a Typhoid Mary (B) [fne2] (expert) — robuste : le premier degat est absorbe`, `60111b … 60111b Bloody Mary (B) [fne2] (expert) — When Revealed au retournement : 1 degat a chaque identite`. Subst : `60110a` rouges 1/1 ; `60110b` rouges 1/1 ; `60111a` rouges 0/1 ; `60111b` rouges 1/1.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON (le plateau affiche la face active ; le dos = l'autre face, `back_faces`).
- Carte terminée : OUI

#### 60112 : Disturbed Psyche
- [x] Étape 2 : Setup = base (fiche `setup.md`) ; `AfterGameSetup` + `Rand.RandomChoice` + `card.Flip` ; `WhenPhaseEnd(ForcedInterrupt, "Villain")` → `Flip` ; `AfterCardPlacedToken` → `VerifierVictoire` (`32130`, `Worlds.SetGameOver(True)`).
- [x] Étape 5 : « Setup: Put the villain into play **on a random side** » → le scénario l'a déjà mise en jeu : on la retourne une fois sur deux ; « When the villain phase **ends** » → `WhenPhaseEnd`, pas le début ; « 3 or more **tokens** here » → damage + threat confondus ; « the players **win** ».
- [x] Étape 6 : environnement, Setup.
- [x] Étape 7 : `60112 … mise en place : la vilaine, l'environnement (Setup) et Establish Trust (Setup) sont en jeu`, `60112 … Setup : la vilaine est mise sur une face au hasard (ici : retournee)`, `60112 … a la fin de la phase du mechant, la vilaine se retourne (Bloody -> Typhoid)`, `60112 … 3 jetons : les joueurs gagnent`. Subst : `60112` rouges 4/4.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON (jetons génériques).
- Carte terminée : OUI

#### 60113a,60113b : Establish Trust / * Mary Walker
- [x] Étape 2 : 60113a : `IfExpertModeThisGainKeyword(hinder="3*")`, `WhenSchemeBeDefeated` + `PlaceTokensOn('threat')` + `Flip` + `AttachTo2(vilaine)` (§3 : correctif scheme_side.py) ; 60113b : `AttachToFaceWhenPutIntoPlay(Villain)`, `EnemyCannotActivate(NonKeywordStar, "AttachedEnemy")`, `AfterUnitTookDamage(AttachedEnemy)` + `WhenRoundEnd` → `DealEncounterCard` à chaque joueur + `FlipMaryWalkerVersEstablishTrust` (retour révélé).
- [x] Étape 5 : « Permanent » + « Flip this card » → le complot ne se défausse pas, il se retourne (le moteur sautait la défaite : correctif) ; « Attached villain **cannot activate** » ; « After the villain takes damage **or** the round ends » → deux déclencheurs, même réponse ; « flip it and **reveal** Establish Trust » → la menace de départ 8[per_hero] est reposée par `Reveal`.
- [x] Étape 6 : complot 8[per_hero], hinder 3[per_hero] en expert.
- [x] Étape 7 : `60113a … vaincue : 1 jeton threat, la carte se retourne en Mary Walker attachee a la vilaine`, `60113b … la vilaine attachee ne peut pas s'activer`, `60113b … la vilaine subit des degats : chaque joueur recoit 1 carte rencontre et Establish Trust revient`, `60113b … fin de round : meme rechute`. Subst : `60113a` rouges 1/1 ; `60113b` rouges 3/3.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60114 : Telekinesis
- [x] Étape 2 : `AttachToFaceWhenPutIntoPlay(Villain)`, `desc.SCH+` (+2), `PlayerActionToDiscardThis(HeroAction).SetCost(Cost("BB"))`, boost : `MaryActive('Typhoid Mary')` + `TakeIndirectDamage(3)` + `ExhaustAll` des personnages blessés.
- [x] Étape 5 : « **If Typhoid Mary** is activating » → la face A nommée, pas Bloody (contre-cas) ; « Exhaust each character **damaged this way** » → seulement ceux touchés par l'indirect.
- [x] Étape 6 : +2 SCH ; 1 + 1 + 3 = 5.
- [x] Étape 7 : `60114 … attachee a la vilaine : +2 SCH ; Hero Action [mental][mental] : defaussee`, `60114 … revelee : +2 SCH sur la vilaine`, `60114 … Boost, Typhoid Mary active : 3 degats indirects en plus (1 + 1 + 3 = 5)`, `60114 … contre-cas Bloody Mary active : pas de degats indirects (2 + 1 = 3)`. Subst : `60114` rouges 3/4.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60115 : Psionic Slash
- [x] Étape 2 : `FlipMaryWalkerVersEstablishTrust` puis `DoSchemes` ; boost : `MaryActive('Typhoid Mary')` + 3 dégâts à un allié contrôlé (`Filter.One`).
- [x] Étape 5 : « If the Mary Walker attachment is in play, flip it and reveal Establish Trust. The villain schemes » → dans cet ordre ; « **If Typhoid Mary** is activating ».
- [x] Étape 6 : 2 exemplaires.
- [x] Étape 7 : `60115 … Mary Walker en jeu : elle se retourne en Establish Trust revelee, puis la vilaine manigance`, `60115 … Boost, Typhoid Mary active : 3 degats a un allie que tu controles (Hellcat vaincue)`. Subst : `60115` rouges 2/2.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60116 : Psi Nova
- [x] Étape 2 : `Faces.DealDamage(1)` à chaque personnage contrôlé + `GiveStatus(identité, Stunned)` ; boost : `MaryActive('Typhoid Mary')` → Stunned.
- [x] Étape 5 : « each character **you control** » ; « **You** are stunned » → l'identité.
- [x] Étape 6 : —
- [x] Étape 7 : `60116 … revelee : 1 degat a chaque personnage, identite etourdie`, `60116 … Boost, Typhoid Mary active : identite etourdie`. Subst : `60116` rouges 2/2.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60117 : Assembled Armor
- [x] Étape 2 : `60068a` (`WhenUnitWouldTakeDamage` + `PreventDamage(total)` + compteurs `damage`), seuil 5 / 8 (`Worlds.IsExpert`), `DiscardAll([this])` ; `desc.ATK+` (+2) ; boost : `MaryActive('Bloody Mary')` → Confused.
- [x] Étape 5 : « **any amount** of damage » → tout est placé ici, rien ne passe ; « **5 or more** (8 or more in expert mode) » ; « **If Bloody Mary** is activating ».
- [x] Étape 6 : +2 ATK, ARMOR.
- [x] Étape 7 : `60117 … 3 degats a la vilaine : places sur l'armure a la place`, `60117 … 5 degats accumules : l'armure est defaussee`, `60117 … 60117 Assembled Armor [fne2] (expert) — 5 degats ne suffisent pas, 8 oui`, `60117 … Boost, Bloody Mary active : identite desorientee`. Subst : `60117` rouges 4/4.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60118 : Hail of Blades
- [x] Étape 2 : `FlipMaryWalkerVersEstablishTrust` puis `DoAttackYou` (attaque même en alter-ego) ; boost : `MaryActive('Bloody Mary')` → 2 dégâts.
- [x] Étape 5 : « The villain attacks you (**even if you are in alter-ego form**) » → attaque forcée hors forme héros ; « **If Bloody Mary** is activating ».
- [x] Étape 6 : 2 exemplaires.
- [x] Étape 7 : `60118 … revelee en alter-ego : la vilaine attaque quand meme (Bloody Mary ATK 2)`, `60118 … Boost, Bloody Mary active : 2 degats en plus (2 + 0 + 2 = 4)`. Subst : `60118` rouges 2/2.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60119 : Scavenged Bulwark
- [x] Étape 2 : `Faces.GiveStatus([vilaine], "Tough")` ; Surge = base ; boost : `MaryActive('Bloody Mary')` → Tough.
- [x] Étape 5 : « Give the villain a tough status card » (quelle que soit la face) ; « **If Bloody Mary** is activating, give **her** ».
- [x] Étape 6 : Surge.
- [x] Étape 7 : `60119 … revelee : la vilaine devient robuste, et surge`, `60119 … Boost, Bloody Mary active : elle devient robuste`. Subst : `60119` rouges 2/2.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60120 : Hand Lookout
- [x] Étape 2 : `11041` Deathunt : `message.GiveBoostCardForThisActivation(Enemy, 1, effect)` ; Guard, Toughness = bases.
- [x] Étape 5 : « Give the **activating enemy** an additional boost card » → l'ennemi actif, vilain ou sbire.
- [x] Étape 6 : HAND, NINJA, Guard, Toughness, 3 exemplaires.
- [x] Étape 7 : `60120 … Boost : une carte boost de plus pour l'ennemi actif (2 + 1 + 3 = 6)`. Subst : `60120` rouges 1/1.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 8 parties Spider-Man vs les 4 scénarios (profil équilibré, graines 1-2, 107 s) : 0 V / 7 D, 1 bloquée (Electro graine 2 : boucle du pilote sur Tenacity 01093, voir §7), 0 traceback (grep des 8 journaux).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

## Bloc 3A — The Getaway, The Raft Breakout, Stop the Presses! (18/09/2026, agent A)

Écrit par un agent parallèle ; son rapport (bilan, gabarits, pièges,
questions) est RECOPIÉ ici, le brouillon de session ayant disparu avec le
répertoire temporaire. Pièges : RECETTES-MOTEUR §7quinquies à §7septies.
Substitution : passe finale du coordinateur, voir « Fusion et gates de fin ».

### 1. Bilan harnais

**BILAN : 72/72 cas passes** (`[fne3a]`, PARALLELES=4, port 41000, passe finale du 18/09/2026 après tous les correctifs ; cas d'index 1934 à 2005).

Historique des passes : 15/23 (The Getaway seul) → 16/23 (7 morts : édition concurrente de `environment.py`) → 8/23 (`puzzle.py` en cours d'édition) → 23/23 → 53/70 → 67/70 → 70/70 → 71/72 → **72/72**.

Cas par carte (nom complet dans `tools/test_capacites.py`, préfixe = card_id) :

- **60128a** (2) :
  - OK `60128a The Getaway 1A [fne3a] — Setup : 1 compteur speed sur le complot, Out Front attachee au vilain`
  - OK `60128a The Getaway 1A [fne3a] (expert) — Setup : 2 compteurs speed`
- **60128b** (3) :
  - OK `60128b The Getaway 1B [fne3a] — fin de round avec de la menace, Out Front en jeu : +1 speed puis +1 de plus (1 -> 3)`
  - OK `60128b The Getaway 1B [fne3a] — fin de round, Alongside en jeu : +1 speed et Alongside se retourne en Out Front (1 -> 2)`
  - OK `60128b The Getaway 1B [fne3a] — contre-cas : sans menace sur le complot, rien ne se passe (speed reste 1)`
- **60129a** (5) :
  - OK `60129a Out Front [fne3a] — attachee au vilain : ses attaques gagnent ranged, la riposte de Black Panther ne le touche pas`
  - OK `60129a Out Front [fne3a] — Forced Interrupt : 3 degats au vilain deviennent 3 menaces retirees du complot (5 -> 2), le vilain n'a rien`
  - OK `60129a Out Front [fne3a] — le retrait ignore la crise (Crowd Control 01108 en jeu) : 5 -> 2`
  - OK `60129a Out Front [fne3a] — plus de menace sur le complot : la carte se retourne (Alongside) et reste attachee au vilain`
  - OK `60129a Out Front [fne3a] — un contre du heros ramene la menace a 0 : la carte se retourne aussi`
- **60129b** (1) :
  - OK `60129b Alongside [fne3a] — When Revealed au retournement : chaque joueur prend 1 degat indirect, le vilain 2[per_hero] degats`
- **60130** (5) :
  - OK `60130 Escort Vehicle [fne3a] — guard, patrol (bases) ; 1 compteur speed : ni toughness, ni quickstrike, ni surge`
  - OK `60130 Escort Vehicle [fne3a] — 3 compteurs speed : gagne toughness et entre en jeu robuste`
  - OK `60130 Escort Vehicle [fne3a] — 6 compteurs speed : aussi quickstrike, il attaque en entrant (2 degats)`
  - OK `60130 Escort Vehicle [fne3a] — 9 compteurs speed : aussi surge, le temoin du dessus du deck est revele`
  - OK `60130 Escort Vehicle [fne3a] — contre-cas : deja en jeu quand le 3e compteur arrive, il gagne toughness SANS carte de statut (regle : a l'entree en jeu seulement)`
- **60131** (2) :
  - OK `60131 Jackknifed Tanker Truck [fne3a] — Hinder 1[per_hero] : 3 menaces, crise ; le vilain ne peut pas subir de degats (Out Front retiree)`
  - OK `60131 Jackknifed Tanker Truck [fne3a] — avec Out Front en jeu : aucun degat ET aucune menace retiree (« cannot » prime sur « would »)`
- **60132** (3) :
  - OK `60132 Burning Rubber [fne3a] — 1 compteur : premiere branche, 1 ressource depensee (Energy), pas de menace`
  - OK `60132 Burning Rubber [fne3a] — 3 compteurs, une seule carte en main : 1 paiement, puis la branche payante n'est plus offerte : 2 menaces (2 -> 4)`
  - OK `60132 Burning Rubber [fne3a] — 2 compteurs, seconde branche choisie : 2 menaces (2 -> 4), la main est intacte`
- **60133** (3) :
  - OK `60133 Pedestrians [fne3a] — 1 compteur : premiere branche, le heros est incline, 0 degat`
  - OK `60133 Pedestrians [fne3a] — 2 compteurs, un seul personnage : incline au premier, plus rien de pret au second -> 1 degat indirect`
  - OK `60133 Pedestrians [fne3a] — 2 compteurs, seconde branche choisie : 2 degats indirects, le heros reste pret`
- **60142a** (1) :
  - OK `60142a The Raft Breakout 1A [fne3a] — Setup : Master Key attachee au vilain, un sbire PRISONER defausse depuis le deck et revele`
- **60142b** (2) :
  - OK `60142b The Raft Breakout 1B [fne3a] — un sbire non-ELITE vaincu retire 1 menace du complot (5 -> 4)`
  - OK `60142b The Raft Breakout 1B [fne3a] — un sbire ELITE vaincu retire 2 menaces (5 -> 3)`
- **60143** (3) :
  - OK `60143 Master Key [fne3a] — le vilain manigance avec un sbire en boost : ce sbire est distribue au joueur face cachee apres l'activation`
  - OK `60143 Master Key [fne3a] — contre-cas : le vilain ATTAQUE avec un sbire en boost, rien n'est distribue`
  - OK `60143 Master Key [fne3a] — contre-cas : manigance avec une traitrise en boost, rien n'est distribue`
- **60144** (3) :
  - OK `60144 Absorbing Man [fne3a] — attaque : la carte du dessus de mon deck (Energy) est glissee sous lui, +1 ATK (1 + 1 = 2)`
  - OK `60144 Absorbing Man [fne3a] — deux attaques, Energy puis Genius : 2 types differents, +1 puis +2 (2 + 3 = 5)`
  - OK `60144 Absorbing Man [fne3a] — contre-cas : deux Energy glissees = un seul type, +1 puis +1 (2 + 2 = 4)`
- **60145** (5) :
  - OK `60145 Baron Zemo [fne3a] — When Revealed : 1 menace sur Hellcat, qui devient un sbire DECEIVED engage, SCH = son THW (2), texte vide`
  - OK `60145 Baron Zemo [fne3a] — Zemo quitte le jeu : Hellcat redevient un allie sous mon controle, la menace reste sur elle (FAQ)`
  - OK `60145 Baron Zemo [fne3a] — la menace retiree de l'allie converti : il redevient un allie (Zemo toujours en jeu)`
  - OK `60145 Baron Zemo [fne3a] — le sbire DECEIVED est vaincu : la carte redevient Hellcat et va dans MA defausse, plus aucun sbire converti`
  - OK `60145 Baron Zemo [fne3a] — contre-cas : aucun allie en jeu, la revelation ne fait rien et ne plante pas`
- **60146** (2) :
  - OK `60146 Drang [fne3a] — apres son attaque : 1 compteur barrage, puis 1 degat indirect par compteur (1 + 0 + 1 = 2)`
  - OK `60146 Drang [fne3a] — deuxieme attaque : 2 compteurs, 2 indirects ((1 + 1) + (1 + 2) = 5)`
- **60147** (3) :
  - OK `60147 Mysterio [fne3a] — apres son attaque, la traitrise en boost est distribuee au joueur face cachee`
  - OK `60147 Mysterio [fne3a] — contre-cas : un sbire en boost n'est pas distribue`
  - OK `60147 Mysterio [fne3a] — contre-cas : il MANIGANCE avec une traitrise en boost, rien n'est distribue`
- **60148** (2) :
  - OK `60148 Proxima Midnight [fne3a] — attaque, premiere branche : 1 menace sur le complot principal (2 -> 3), ATK 2`
  - OK `60148 Proxima Midnight [fne3a] — seconde branche : +2 ATK pour cette attaque (2 + 2 = 4), pas de menace`
- **60149** (2) :
  - OK `60149 Rhino [fne3a] — robuste a l'entree (Toughness) ; ses attaques gagnent overkill : Spider-Woman (2 PV) defend, 1 degat passe`
  - OK `60149 Rhino [fne3a] — Boost : l'ennemi qui s'active (Hammerhead) devient robuste`
- **60150** (7) :
  - OK `60150 Imprisoned [fne3a] — obligation revelee : je ne peux pas attaquer (0 degat au vilain)`
  - OK `60150 Imprisoned [fne3a] — je ne peux pas contrer (la menace reste a 5)`
  - OK `60150 Imprisoned [fne3a] — je ne peux pas passer en alter-ego`
  - OK `60150 Imprisoned [fne3a] — Hero Action : 3 ressources quelconques (Energy YY + Genius BB) -> defaussee`
  - OK `60150 Imprisoned [fne3a] — Hero Action : incliner le heros (THW 1) et Hellcat (THW 2) = 3 -> defaussee`
  - OK `60150 Imprisoned [fne3a] — contre-cas : THW total 1 (heros seul), la seconde capacite ne part pas, l'obligation reste`
  - OK `60150 Imprisoned [fne3a] — Boost : la carte est revelee (elle entre en jeu chez le joueur)`
- **60151a** (1) :
  - OK `60151a Stop the Presses! 1A [fne3a] — Setup : Daily Bugle en jeu, UN soutien DAILY BUGLE au hasard sous mon controle (3 stamina), les 3 autres retires du jeu`
- **60151b** (5) :
  - OK `60151b Stop the Presses! 1B [fne3a] — attaque non defendue du vilain, premiere branche : 2 menaces ici (1 -> 3)`
  - OK `60151b Stop the Presses! 1B [fne3a] (expert) — 3 menaces au lieu de 2 (1 -> 4)`
  - OK `60151b Stop the Presses! 1B [fne3a] — seconde branche : 1 stamina retiree du soutien DAILY BUGLE que je controle (3 -> 2), pas de menace`
  - OK `60151b Stop the Presses! 1B [fne3a] — contre-cas : attaque DEFENDUE par le heros, rien (menace 1)`
  - OK `60151b Stop the Presses! 1B [fne3a] — un soutien DAILY BUGLE quitte le jeu (dernier stamina retire) : les joueurs perdent`
- **60152** (1) :
  - OK `60152 Daily Bugle [fne3a] — Alter-Ego Action : incliner mon soutien DAILY BUGLE -> +1 stamina dessus (3 -> 4)`
- **60153** (1) :
  - OK `60153 Ben Urich [fne3a] — Action : incliner + 1 stamina -> regarde les 2 cartes du dessus du deck rencontre, en defausse 1`
- **60154** (2) :
  - OK `60154 Betty Brant [fne3a] — Interrupt : la carte boost retournee (Under Fire, 3 icones) est annulee, une autre (Advance, 0) la remplace : 1 + 0 = 1`
  - OK `60154 Betty Brant [fne3a] — contre-cas : Betty deja inclinee, l'interruption n'est pas offerte (1 + 3 = 4)`
- **60155** (1) :
  - OK `60155 J. Jonah Jameson [fne3a] — Action : incliner + 1 stamina + 1 carte rencontre face cachee -> pioche 2 (main 1 -> 3)`
- **60156** (1) :
  - OK `60156 Robbie Robertson [fne3a] — Response : la carte distribuee (Hydra Mercenary) est regardee, defaussee, et une autre (Advance) est distribuee a la place`
- **60157** (3) :
  - OK `60157 Exclusive Interview [fne3a] — When Revealed : chaque soutien DAILY BUGLE est incline ; 6 menaces`
  - OK `60157 Exclusive Interview [fne3a] — les soutiens DAILY BUGLE ne peuvent pas se redresser`
  - OK `60157 Exclusive Interview [fne3a] — contre-cas : sans elle, Ben Urich se redresse`
- **60158** (3) :
  - OK `60158 Breaking News [fne3a] — When Revealed, premiere branche : mon soutien DAILY BUGLE est incline et perd 1 stamina (3 -> 2)`
  - OK `60158 Breaking News [fne3a] — seconde branche : 2 menaces sur le complot principal (1 -> 3), le soutien intact`
  - OK `60158 Breaking News [fne3a] — Boost : mon soutien DAILY BUGLE est incline (stamina intacte)`

Grep exhaustif des journaux des cas verts (`Traceback|NameError|AttributeError|TypeError|KeyError|AssertionError`) : **0** sur les 72.

Autoplay (§5 du brief) : `/tmp/autoplay-a.json`, 6 parties (3 scénarios × graines 11-12, 150 s) : 0 V / 6 D, 0 bloquée, **0 traceback** sur les 6 journaux `/tmp/autoplay_spider_man_<scenario>_normal_equilibre_{11,12}.log` ; plus `/tmp/autoplay-a-getaway56.json` (The Getaway, graines 5-6, après le correctif 60130) : 0 traceback.

### 5. Gabarits PROCESSUS-CARTE (un par carte)

Conventions : « cas » = nom dans `tools/test_capacites.py` ; subst : passe
finale du coordinateur ; Hammerhead (60086 → 60087) vilain de référence ;
graine 42 : le Setup de The Raft Breakout défausse 6 cartes et révèle **Drang**
(60146) ; celui de Stop the Presses! donne **Ben Urich** (60153) au joueur 1 et
retire Betty Brant, J. Jonah Jameson, Robbie Robertson du jeu.

#### The Getaway

##### 60128a : The Getaway 1A
- [x] Étape 2 : `60121a` Art Museum Heist 1A (`WhenCardSetup("This", op)` du complot 1A) ; `60066` Bullseye II (`Find.FindAndAttachTo`, qui fouille la mise de côté du scénario, où `set_aside: ["60129a,60129b"]` range Out Front avec ses deux faces) ; `Worlds.IsExpert` (`60117`) pour « 2 counters instead in expert mode ».
- [x] Étape 5 : « Place 1 speed counter **here** » → sur le complot (les compteurs vivent sur la carte : lus sur la face 1B après la progression) ; « **2 counters instead** in expert mode » → `IsExpert` ; « Attach the Out Front attachment (129A) to the villain » → face A attachée, face B au dos. ⚠ Le script livré appelait `WhenCardSetup(op)` à un argument : corrigé en `WhenCardSetup("This", op)` (précision du coordinateur).
- [x] Étape 6 : 1 / 2 (expert) compteurs ↔ script ; scénario : Out Front `set_aside` ↔ `60129a,60129b`.
- [x] Étape 7 : `60128a … Setup : 1 compteur speed sur le complot, Out Front attachee au vilain` (compteur 1, `hotes` 60129a→60086, menace de départ 2) ; `60128a … (expert) — Setup : 2 compteurs speed` (compteur 2, hôte 60087). Subst : passe finale du coordinateur.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `the_getaway_hammerhead` (profil équilibré, graines 11-12, journaux distincts de l'agent B) : 0 V / 2 D, 0 bloquée, 4,0 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; puis parties 5 et 6 rejouées après le correctif `OnEvent.Counter` de 60130 (celles où l'agent B avait vu 15 tracebacks par journal) : 0 V / 2 D, 5,5 rounds, Escort Vehicle en jeu (33 et 24 lignes), **0 traceback / 0 erreur**. Témoin même fournée : the_raft_breakout et stop_the_presses ci-dessous. Lecture du journal : Out Front convertit les dégâts en menace, Alongside apparaît à 0 menace et revient en Out Front en fin de round ; les parties se perdent par complot complété (le pilote ne sait pas jouer autour de la menace).
- [x] Étape 8 bis : compteur sur le complot + attachement sur le vilain : jauges génériques (compteurs de carte, attachement sur `area_villain` déjà couvert par `fne-oeuvre-volee.test.ts`) ; OUI, couvert.
- Carte terminée : OUI

##### 60128b : The Getaway 1B
- [x] Étape 2 : `bw015` Hulk Out / `tg016` Chomped (`WhenRoundEnd` + vérificateur qui envoie `Message.WhenRoundEnd`) ; `RetournerLAttachement` (pack fne, retournement d'un attachement recto-verso sans le perdre, RECETTES §7quater) ; `IfThisSchemeStageIsCompletedPlayersLoseTheGame` (60121b).
- [x] Étape 5 : « **if there is threat here** » → lu AVANT toute action (contre-cas à 0 menace : rien) ; « **do each of the following** » → 1 puis 2, toujours ; « If Alongside is in play, flip it to Out Front. **Otherwise**, place 1 additional » → deux branches exclusives (3 cas) ; « When the round ends » = `WhenRoundEnd`, pas `BeginVillainPhase` (RECETTES §7).
- [x] Étape 6 : départ 2★ / cible 9★ / escalade +2★ ↔ scan 60128b ↔ `desc` ; +1 et +1 compteur.
- [x] Étape 7 : `60128b … fin de round avec de la menace, Out Front en jeu : +1 speed puis +1 de plus (1 -> 3)` ; `60128b … fin de round, Alongside en jeu : +1 speed et Alongside se retourne en Out Front (1 -> 2)` (Alongside hors jeu, Out Front accrochée à 60086) ; contre-cas `60128b … sans menace sur le complot, rien ne se passe (speed reste 1)` (vert par construction sous substitution). Subst : passe finale du coordinateur.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `the_getaway_hammerhead` (profil équilibré, graines 11-12, journaux distincts de l'agent B) : 0 V / 2 D, 0 bloquée, 4,0 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; puis parties 5 et 6 rejouées après le correctif `OnEvent.Counter` de 60130 (celles où l'agent B avait vu 15 tracebacks par journal) : 0 V / 2 D, 5,5 rounds, Escort Vehicle en jeu (33 et 24 lignes), **0 traceback / 0 erreur**. Témoin même fournée : the_raft_breakout et stop_the_presses ci-dessous. Lecture du journal : Out Front convertit les dégâts en menace, Alongside apparaît à 0 menace et revient en Out Front en fin de round ; les parties se perdent par complot complété (le pilote ne sait pas jouer autour de la menace).
- [x] Étape 8 bis : compteurs + retournement d'attachement : `back_faces` et compteurs génériques ; OUI, couvert (même rendu que 60068a/b prouvé au bloc 2).
- Carte terminée : OUI

##### 60129a / 60129b : Out Front / Alongside (une carte, deux faces)
- [x] Étape 2 : `AttachToFaceWhenPutIntoPlay(Villain)` (60114) ; `UnitAttackGainKeyword("AttachedEnemy", ranged=True)` (50107b, fiche `ranged.md`) ; `WhenUnitWouldTakeDamage(Villain)` + `PreventDamage("All")` (60117 Assembled Armor) + `RemoveThreatFromSchemes("MainScheme", n, ignore_crisis=True)` (si007) ; `AfterSchemeRemoveThreat(MainScheme, last_threat=True)` (39016 Spiral) + `RetournerLAttachement(call_reveal=True)` ; Alongside : `WhenThisRevealed` + `TakeIndirectDamage` (27080) + `DealDamage` ; Permanent = base desc.
- [x] Étape 5 : « If there is **no threat** on the main scheme, flip this card » → après chaque retrait (dégâts convertis ET contre, 2 cas) ; « Attached villain's attacks gain ranged » → `[star]` permanent, pas une Réponse ; « would be dealt **any amount** of damage … **instead** » → tout est évité, la menace retirée vaut le total ; « (ignoring crisis icons) » → `ignore_crisis=True` (cas avec Crowd Control) ; Alongside « **Each player** takes 1 indirect damage. The villain takes 2[per_hero] » → `ForEachPlayer` + `GetPlayerNumIcon` ; la face qui apparaît au retournement résout son When Revealed (`call_reveal=True`, FAQ Bloody Mary B).
  ⚠ Piège payé : `AfterSchemeRemoveThreat` prend un TYPE (`MainScheme`), la chaîne `"MainScheme"` lève un `AssertionError` AVALÉ dans `CheckWhichCard` (carte inerte, journal muet hors trace `<F>`).
- [x] Étape 6 : 2[per_hero] dégâts, 1 indirect, Permanent ↔ `desc` ; une carte à deux faces `"60129a,60129b"`.
- [x] Étape 7 : `60129a … ses attaques gagnent ranged, la riposte de Black Panther ne le touche pas` (dégâts 0, menace intacte) ; `60129a … 3 degats au vilain deviennent 3 menaces retirees (5 -> 2)` ; `60129a … ignore la crise (Crowd Control 01108) : 5 -> 2` ; `60129a … plus de menace : la carte se retourne (Alongside) et reste attachee` ; `60129a … un contre du heros ramene la menace a 0 : la carte se retourne aussi` ; `60129b … When Revealed au retournement : 1 indirect par joueur, 2[per_hero] au vilain`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `the_getaway_hammerhead` (profil équilibré, graines 11-12, journaux distincts de l'agent B) : 0 V / 2 D, 0 bloquée, 4,0 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; puis parties 5 et 6 rejouées après le correctif `OnEvent.Counter` de 60130 (celles où l'agent B avait vu 15 tracebacks par journal) : 0 V / 2 D, 5,5 rounds, Escort Vehicle en jeu (33 et 24 lignes), **0 traceback / 0 erreur**. Témoin même fournée : the_raft_breakout et stop_the_presses ci-dessous. Lecture du journal : Out Front convertit les dégâts en menace, Alongside apparaît à 0 menace et revient en Out Front en fin de round ; les parties se perdent par complot complété (le pilote ne sait pas jouer autour de la menace).
- [x] Étape 8 bis : attachement recto-verso sur le vilain : OUI, même mécanisme que 60068a/b (bloc 2, `back_faces`), couvert.
- Carte terminée : OUI

##### 60130 : Escort Vehicle
- [x] Étape 2 : `60091` Chameleon / `27067` (`ThisGainKeyword(check_fn, change_on_event=…)`), `OnEvent.Counter("MainScheme", 'speed')` ; Guard, Patrol = bases desc.
- [x] Étape 5 : « **at least** » → `>=` ; « 6 – This minion **also** gains quickstrike » → cumulatif (3 seuils, 3 fabriques) ; « gains toughness » en cours de partie → le compteur de mot-clé seulement, PAS de carte de statut (`GainToughness` ne touche que `GetKeyword`, le statut n'est posé que par `OnWhenCardEnterPlay`) : contre-cas dédié.
  ⚠ Piège payé (signalé par l'agent B en autoplay, 15 tracebacks par journal) : `OnEvent.Counter("MainScheme", 'speed')` avec une CHAÎNE lève `assert not isinstance(check_rule, Sequence)` (card_type.py:247) à chaque compteur posé pendant que le sbire est en jeu ; mes quatre premiers cas posaient les compteurs AVANT l'entrée en jeu et ne le voyaient pas. Corrigé en `OnEvent.Counter(MainScheme, 'speed')` ; prouvé par le contre-cas « déjà en jeu quand le 3e compteur arrive » (0 erreur au journal) et par les parties 5 et 6 rejouées (0 traceback, Escort Vehicle en jeu).
- [x] Étape 6 : PV 5, ATK 2, SCH 2, boost 3, seuils 3 / 6 / 9.
- [x] Étape 7 : `60130 … guard, patrol ; 1 compteur : ni toughness, ni quickstrike, ni surge` ; `60130 … 3 compteurs : gagne toughness et entre en jeu robuste` ; `60130 … 6 compteurs : aussi quickstrike, il attaque en entrant (2 degats)` ; `60130 … 9 compteurs : aussi surge, le temoin du dessus du deck est revele` ; contre-cas `60130 … deja en jeu quand le 3e compteur arrive, il gagne toughness SANS carte de statut`. Vérificateur `fne3a_mots_cles` (IsGuard/IsPatrol/IsToughness/IsQuickstrike/`surge`). Subst : passe finale du coordinateur.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `the_getaway_hammerhead` (profil équilibré, graines 11-12, journaux distincts de l'agent B) : 0 V / 2 D, 0 bloquée, 4,0 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; puis parties 5 et 6 rejouées après le correctif `OnEvent.Counter` de 60130 (celles où l'agent B avait vu 15 tracebacks par journal) : 0 V / 2 D, 5,5 rounds, Escort Vehicle en jeu (33 et 24 lignes), **0 traceback / 0 erreur**. Témoin même fournée : the_raft_breakout et stop_the_presses ci-dessous. Lecture du journal : Out Front convertit les dégâts en menace, Alongside apparaît à 0 menace et revient en Out Front en fin de round ; les parties se perdent par complot complété (le pilote ne sait pas jouer autour de la menace).
- [x] Étape 8 bis : NON (mots-clés et statut : jauges génériques).
- Carte terminée : OUI

##### 60131 : Jackknifed Tanker Truck
- [x] Étape 2 : `UnitCannotTakeDamage(Villain)` (fabrique corrigée le 30/08/2026, rend une liste : déballage `*`) ; Hinder `1*`, Crisis = bases desc.
- [x] Étape 5 : « The villain **cannot** be dealt damage » → « cannot » prime sur le « would » d'Out Front : ni dégât ni menace retirée (cas dédié, mesuré) ; « [star] Hinder 1[per_hero] » = base.
- [x] Étape 6 : 2 menaces + Hinder 1★ = 3 mesurées ; boost 2 ; 1 icône crise.
- [x] Étape 7 : `60131 … Hinder 1[per_hero] : 3 menaces, crise ; le vilain ne peut pas subir de degats (Out Front retiree)` ; `60131 … avec Out Front en jeu : aucun degat ET aucune menace retiree`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `the_getaway_hammerhead` (profil équilibré, graines 11-12, journaux distincts de l'agent B) : 0 V / 2 D, 0 bloquée, 4,0 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; puis parties 5 et 6 rejouées après le correctif `OnEvent.Counter` de 60130 (celles où l'agent B avait vu 15 tracebacks par journal) : 0 V / 2 D, 5,5 rounds, Escort Vehicle en jeu (33 et 24 lignes), **0 traceback / 0 erreur**. Témoin même fournée : the_raft_breakout et stop_the_presses ci-dessous. Lecture du journal : Out Front convertit les dégâts en menace, Alongside apparaît à 0 menace et revient en Out Front en fin de round ; les parties se perdent par complot complété (le pilote ne sait pas jouer autour de la menace).
- [x] Étape 8 bis : NON (complot annexe standard, pastille Crise générique).
- Carte terminée : OUI

##### 60132 : Burning Rubber
- [x] Étape 2 : `60127` Tug of War (`ForChoiceAbilityWithCost(Cost("1"), …, conditions=[PeutCouvrirLeCout])`) ; `60083` Chain Lightning (un `ChooseAbilities` par élément : `PourChaqueCompteurDeVitesse`).
- [x] Étape 5 : « **For each** speed counter » → un choix PAR compteur (cas à 3 compteurs) ; « Spend 1 resource **of any type** » → `Cost("1")` ; branche payante offerte seulement si payable (sinon le moteur l'offre seule et le paiement échoue, leçon Tug of War) : cas « une seule carte en main, 3 compteurs » = 1 paiement puis 2 menaces. ⚠ Écart hérité de `PeutCouvrirLeCout` : les générateurs de ressources EN JEU ne sont pas comptés (gabarit 60127).
- [x] Étape 6 : 1 ressource / 1 menace par compteur ; boost 1.
- [x] Étape 7 : `60132 … 1 compteur : premiere branche, 1 ressource depensee (Energy), pas de menace` ; `60132 … 3 compteurs, une seule carte en main : 1 paiement, puis la branche payante n'est plus offerte : 2 menaces (2 -> 4)` ; `60132 … 2 compteurs, seconde branche choisie : 2 menaces (2 -> 4), la main est intacte`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `the_getaway_hammerhead` (profil équilibré, graines 11-12, journaux distincts de l'agent B) : 0 V / 2 D, 0 bloquée, 4,0 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; puis parties 5 et 6 rejouées après le correctif `OnEvent.Counter` de 60130 (celles où l'agent B avait vu 15 tracebacks par journal) : 0 V / 2 D, 5,5 rounds, Escort Vehicle en jeu (33 et 24 lignes), **0 traceback / 0 erreur**. Témoin même fournée : the_raft_breakout et stop_the_presses ci-dessous. Lecture du journal : Out Front convertit les dégâts en menace, Alongside apparaît à 0 menace et revient en Out Front en fin de round ; les parties se perdent par complot complété (le pilote ne sait pas jouer autour de la menace).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

##### 60133 : Pedestrians
- [x] Étape 2 : `60083` Chain Lightning (choix par élément, branche « incliner un personnage ») ; `Faces.ExhaustAll` (bt004) ; `TakeIndirectDamage` (27080).
- [x] Étape 5 : « **For each** speed counter » → un choix par compteur ; « Exhaust a character **you control** » → `GetControlCharacters`, un personnage PRÊT ; branche cachée quand plus rien n'est prêt (cas « 2 compteurs, un seul personnage » : incliné puis 1 indirect). ⚠ Piège payé : `ForChoiceAbility` n'a PAS de `conditions=` (seule la variante `WithCost` en a) ; `condition=` est un booléen évalué à la construction, et `branches()` est rappelée à chaque compteur, donc réévaluée (`TypeError` avalé sinon, carte inerte).
- [x] Étape 6 : 1 personnage / 1 indirect par compteur ; boost 1.
- [x] Étape 7 : `60133 … 1 compteur : premiere branche, le heros est incline, 0 degat` ; `60133 … 2 compteurs, un seul personnage : incline au premier, plus rien de pret au second -> 1 degat indirect` ; `60133 … 2 compteurs, seconde branche choisie : 2 degats indirects, le heros reste pret`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `the_getaway_hammerhead` (profil équilibré, graines 11-12, journaux distincts de l'agent B) : 0 V / 2 D, 0 bloquée, 4,0 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; puis parties 5 et 6 rejouées après le correctif `OnEvent.Counter` de 60130 (celles où l'agent B avait vu 15 tracebacks par journal) : 0 V / 2 D, 5,5 rounds, Escort Vehicle en jeu (33 et 24 lignes), **0 traceback / 0 erreur**. Témoin même fournée : the_raft_breakout et stop_the_presses ci-dessous. Lecture du journal : Out Front convertit les dégâts en menace, Alongside apparaît à 0 menace et revient en Out Front en fin de round ; les parties se perdent par complot complété (le pilote ne sait pas jouer autour de la menace).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### The Raft Breakout

##### 60142a : The Raft Breakout 1A
- [x] Étape 2 : `60121a` (`WhenCardSetup("This", op)`) ; `Find.FindAndAttachTo` (60066, fouille la mise de côté `set_aside: ["60143"]`) ; `Worlds.DiscardEncounterCardsUntil(trait="PRISONER", card_type=Minion)` + `Reveal` (60095 Power Struggle, 11025 Rampage) ; `Players.ForEachPlayer`.
- [x] Étape 5 : « **Each player** discards cards … until **they** discard a PRISONER minion and reveal **that** minion » → une boucle par joueur, le même objet révélé (graine 42 : 6 cartes défaussées, Drang révélé engagé) ; « Attach Master Key to the villain ». Script livré corrigé (`WhenCardSetup` à deux arguments).
- [x] Étape 6 : scénario : Master Key en `set_aside` ↔ 60143.
- [x] Étape 7 : `60142a … Setup : Master Key attachee au vilain, un sbire PRISONER defausse depuis le deck et revele` (`hotes` 60143→60086, `en_jeu_trait` PRISONER ≥ 1). Subst : passe finale du coordinateur.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `the_raft_breakout_hammerhead` (profil équilibré, graines 11-12) : 0 V / 2 D, 0 bloquée, 4,5 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; témoin même fournée `the_getaway_hammerhead` 4,0 rounds, 0 traceback. Journal : Master Key attachée, un PRISONER révélé au Setup, cartes distribuées après manigance ; 1 partie perdue par élimination, 1 par complot.
- [x] Étape 8 bis : attachement sur le vilain (générique) ; OUI, couvert.
- Carte terminée : OUI

##### 60142b : The Raft Breakout 1B
- [x] Étape 2 : `WhenUnitBeDefeated(ForcedResponse, Minion, op)` écouté PAR LE COMPLOT (le sbire vaincu = `message.trigger`), + `RemoveThreatFromSchemes([this], n)` ; `IfThisSchemeStageIsCompletedPlayersLoseTheGame`. ⚠ Le script livré passait par `GiveAbilityToInPlayWhenApplyThis(Minion, abilities=[…])` (modèle 50070) : cette fabrique ne donne la capacité que sur un événement **Faceup** (`environment_helper2.py:213`, « Fix for 50070 »), jamais à l'entrée en jeu ; un sbire mis en jeu sans retournement (PutIntoPlay, allié converti par Zemo) ne la recevait pas. L'écoute au niveau du complot donne le même résultat, et un sbire au texte vide (DECEIVED) garde la capacité, ce que veulent les règles (un texte vide n'efface que le texte imprimé).
- [x] Étape 5 : « **Each minion** gains » → tout sbire vaincu, quel que soit son set ; « **2 threat instead** if this minion has the ELITE trait » → `HasTrait("ELITE")` (Drang) ; « Remove … from the **main** scheme ».
- [x] Étape 6 : départ 2★ / cible 11★ / +1★ ↔ `desc` ; 1 / 2 menaces.
- [x] Étape 7 : `60142b … un sbire non-ELITE vaincu retire 1 menace du complot (5 -> 4)` ; `60142b … un sbire ELITE vaincu retire 2 menaces (5 -> 3)`. Vu aussi en chemin réel : Zemo (ELITE) vaincu dans le cas `60145 … Zemo quitte le jeu` retire 2 menaces (journal xa1967). Subst : passe finale du coordinateur.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `the_raft_breakout_hammerhead` (profil équilibré, graines 11-12) : 0 V / 2 D, 0 bloquée, 4,5 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; témoin même fournée `the_getaway_hammerhead` 4,0 rounds, 0 traceback. Journal : Master Key attachée, un PRISONER révélé au Setup, cartes distribuées après manigance ; 1 partie perdue par élimination, 1 par complot.
- [x] Étape 8 bis : NON (menace, jauge générique).
- Carte terminée : OUI

##### 60143 : * Master Key
- [x] Étape 2 : `60097` Purple Man (`WhenCardBecomeBoost(None, op)` + `message.AfterThisActivation` + `DealEncounterCard`, 27093 Fearmonger), helper `DistribuerLesBoostsDeCeType(type_carte=Minion, attaque=False, vilain_seulement=True)` ; `AttachToFaceWhenPutIntoPlay(Villain)` ; Permanent = base.
- [x] Étape 5 : « After the villain **schemes** against you » → seule la manigance (contre-cas attaque) ; « each of that activation's boost cards **that is a minion** » → filtre `Minion` (contre-cas traîtrise) ; « deal … **to yourself** as a facedown encounter card » → `message.GetToPlayer()` (le joueur contre qui l'ennemi s'active), après l'activation.
- [x] Étape 6 : ITEM, Permanent ; boost `[star]` seul (la face n'a pas d'icône chiffrée).
- [x] Étape 7 : `60143 … le vilain manigance avec un sbire en boost : ce sbire est distribue au joueur face cachee apres l'activation` ; contre-cas `60143 … le vilain ATTAQUE avec un sbire en boost, rien n'est distribue` ; contre-cas `60143 … manigance avec une traitrise en boost, rien n'est distribue` (les deux contre-cas restent verts sous substitution, par construction). Subst : passe finale du coordinateur.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `the_raft_breakout_hammerhead` (profil équilibré, graines 11-12) : 0 V / 2 D, 0 bloquée, 4,5 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; témoin même fournée `the_getaway_hammerhead` 4,0 rounds, 0 traceback. Journal : Master Key attachée, un PRISONER révélé au Setup, cartes distribuées après manigance ; 1 partie perdue par élimination, 1 par complot.
- [x] Étape 8 bis : attachement sur le vilain, cartes distribuées face cachée (génériques) ; OUI, couvert.
- Carte terminée : OUI

##### 60144 : * Absorbing Man
- [x] Étape 2 : `01132` Melter (`WhenUnitAttackYou(ForcedInterrupt, "This", op)`) ; `TuckCardUnderHere` (sn005, Spider-Man Noir, pile glissée) ; `FacesCounter.GetPrintedResourcesTypes` (« each different resource icon », faces_counter.py:54) ; `message.GainATKForThisAttack` (60148, 04086) ; Villainous = base.
- [x] Étape 5 : « tuck the top card of **your** deck under him » → `GetAgainstPlayer().player_deck.GetTop()` ; « +1 ATK **for this attack** » → `GainATKForThisAttack`, pas permanent ; « for **each different** resource type » → types distincts (contre-cas deux Energy = +1) ; le joker compte pour un type (`GetResourceIconTypes`).
- [x] Étape 6 : PV 6, ATK 1, SCH 1, boost 3 ; +1 par type.
- [x] Étape 7 : `60144 … la carte du dessus de mon deck (Energy) est glissee sous lui, +1 ATK (1 + 1 = 2)` (`pose_sous`, `taille_pose_sous` 1) ; `60144 … deux attaques, Energy puis Genius : 2 types differents, +1 puis +2 (2 + 3 = 5)` ; contre-cas `60144 … deux Energy glissees = un seul type, +1 puis +1 (2 + 2 = 4)`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `the_raft_breakout_hammerhead` (profil équilibré, graines 11-12) : 0 V / 2 D, 0 bloquée, 4,5 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; témoin même fournée `the_getaway_hammerhead` 4,0 rounds, 0 traceback. Journal : Master Key attachée, un PRISONER révélé au Setup, cartes distribuées après manigance ; 1 partie perdue par élimination, 1 par complot.
- [x] Étape 8 bis : cartes glissées sous un sbire : OUI, même zone `placed_card` que Spider-Man Noir (couverte au plateau par `su012`/Contingency Plan du 09/09/2026, `enUnites` lit la pile glissée) ; couvert.
- Carte terminée : OUI

##### 60145 : * Baron Zemo
- [x] Étape 2 : `60100` Converted / `21178` Beguiled (gabarit `deceived_minion`, pack "", trait DECEIVED, texte vide, `HP 0` : PV, dégâts et jetons vivent sur la CARTE et suivent la face) ; branche `diff == 1` de `TreatAttachedCardAsMinion` (treat.py) recopiée dans `ConvertirEnDeceived` (SwapCardFace `no_detach=True`, `printed_scheme = printed_thwart`, sauvegarde des mots-clés étrangers du correctif du 18/09) ; `RendreLAllie` = `SwapBackToPrintedCard` + `PutIntoPlay(under_control=True)` ; écouteurs bruts `Ability(NonKeyword, Message.AfterCardPlacedToken|AfterCardRemovedToken, …)` (la fabrique `AfterCardPlacedToken` porte `Condition2.ThisIsTrigger` et ne sert qu'à « This ») ; `AfterCardEnterPlay("This")`, `WhenCardLeavePlay("This")` (21139a).
  ⚠ Le script livré (cadre `GiveKeywordToInPlayWhenApplyThis(apply=…, change_on_event=OnEvent.Token(Ally))` + `TreatAsMinion`) convertissait mais NE DÉFAISAIT PAS sur retrait du jeton : la face alliée échangée est ignorée par `is_setting_as`, et `OnEvent.Token(Ally)` ne voit plus qu'un sbire ; `TreatAsMinion` pose en outre sur Zemo des temporaires qu'on ne peut pas retirer.
- [x] Étape 5 : « Treat **each** ally with threat on it » → tout allié, de tout joueur, dès qu'il porte un jeton (posé par Zemo ou par un autre effet) et aussi ceux qui en portent quand Zemo entre en jeu ; « **blank text box** » → gabarit sans texte ; « Its SCH is equal to its **base** THW » → THW imprimé ; « does not take consequential damage » → natif au gabarit ; When Revealed « an ally **without** threat on it » → filtre ; « It engages its controller » → `EngagePlayer(controleur)`. FAQ (livret) : Zemo quitte le jeu → l'allié revient, la menace reste.
- [x] Étape 6 : PV 6, ATK 1, SCH 2, boost 3 ; 1 jeton.
- [x] Étape 7 : `60145 … When Revealed : 1 menace sur Hellcat, qui devient un sbire DECEIVED engage, SCH = son THW (2), texte vide` (+ PV max 3 conservés) ; `60145 … Zemo quitte le jeu : Hellcat redevient un allie sous mon controle, la menace reste sur elle (FAQ)` ; `60145 … la menace retiree de l'allie converti : il redevient un allie (Zemo toujours en jeu)` ; `60145 … le sbire DECEIVED est vaincu : la carte redevient Hellcat et va dans MA defausse` ; contre-cas `60145 … aucun allie en jeu, la revelation ne fait rien et ne plante pas`. Vérificateurs `fne3a_converti`, `fne3a_zemo_retrait`, `fne3a_zemo_vaincu`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `the_raft_breakout_hammerhead` (profil équilibré, graines 11-12) : 0 V / 2 D, 0 bloquée, 4,5 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; témoin même fournée `the_getaway_hammerhead` 4,0 rounds, 0 traceback. Journal : Master Key attachée, un PRISONER révélé au Setup, cartes distribuées après manigance ; 1 partie perdue par élimination, 1 par complot.
- [x] Étape 8 bis : sbire rendu par l'image de l'allié (`pic_id`), même chemin que Converted (bloc 2) ; NON.
- Carte terminée : OUI

##### 60146 : * Drang
- [x] Étape 2 : `AfterUnitAttackEnd(ForcedResponse, "This", op)` (iw001a, RECETTES §1) ; `PlaceCountersOn(barrage)` ; `TakeIndirectDamage` (27080) ; compteur `barrage` déjà dans l'énum `COUNTER`.
- [x] Étape 5 : « **After** Drang attacks you » → Réponse, après l'attaque ; « place 1 barrage counter … **Then**, take 1 indirect damage **for each** barrage counter » → pose d'abord, compte ensuite (1 puis 2). ⚠ Piège payé : `AfterUnitAttackEnd` n'a pas d'attribut `attacked_you` ; le joueur est `message.GetAgainstPlayer()` (`AttributeError` avalé, carte inerte).
- [x] Étape 6 : PV 6, ATK 1, SCH 1, boost 3.
- [x] Étape 7 : `60146 … apres son attaque : 1 compteur barrage, puis 1 degat indirect par compteur (1 + 0 + 1 = 2)` ; `60146 … deuxieme attaque : 2 compteurs, 2 indirects ((1 + 1) + (1 + 2) = 5)`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `the_raft_breakout_hammerhead` (profil équilibré, graines 11-12) : 0 V / 2 D, 0 bloquée, 4,5 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; témoin même fournée `the_getaway_hammerhead` 4,0 rounds, 0 traceback. Journal : Master Key attachée, un PRISONER révélé au Setup, cartes distribuées après manigance ; 1 partie perdue par élimination, 1 par complot.
- [x] Étape 8 bis : NON (compteur générique).
- Carte terminée : OUI

##### 60147 : * Mysterio
- [x] Étape 2 : même helper que Master Key, `DistribuerLesBoostsDeCeType(Treachery, attaque=True, vilain_seulement=False)` (60097 / 27093).
- [x] Étape 5 : « After Mysterio **attacks** you » → seule l'attaque (contre-cas manigance) ; « that is a **treachery** » → filtre `Treachery` (contre-cas sbire) ; « to yourself » → le joueur attaqué.
- [x] Étape 6 : PV 6, ATK 1, SCH 2, boost 3.
- [x] Étape 7 : `60147 … apres son attaque, la traitrise en boost est distribuee au joueur face cachee` ; contre-cas `60147 … un sbire en boost n'est pas distribue` ; contre-cas `60147 … il MANIGANCE avec une traitrise en boost, rien n'est distribue`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `the_raft_breakout_hammerhead` (profil équilibré, graines 11-12) : 0 V / 2 D, 0 bloquée, 4,5 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; témoin même fournée `the_getaway_hammerhead` 4,0 rounds, 0 traceback. Journal : Master Key attachée, un PRISONER révélé au Setup, cartes distribuées après manigance ; 1 partie perdue par élimination, 1 par complot.
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

##### 60148 : * Proxima Midnight
- [x] Étape 2 : `WhenUnitAttackYou(ForcedInterrupt, "This", op)` (01132) + `ChooseAbilities(ForChoiceAbility, ForChoiceAbility)` (08013, 16155) ; `PlaceThreatOnSchemes("MainScheme", 1)` ; `GainATKForThisAttack(2)` (04086).
- [x] Étape 5 : « choose to **either** … **or** » → deux branches, le joueur attaqué choisit ; « +2 ATK **for this attack** » → propriété de l'attaque.
- [x] Étape 6 : PV 7, ATK 2, SCH 1, boost 3 ; 1 menace / +2.
- [x] Étape 7 : `60148 … premiere branche : 1 menace sur le complot principal (2 -> 3), ATK 2` ; `60148 … seconde branche : +2 ATK pour cette attaque (2 + 2 = 4), pas de menace`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `the_raft_breakout_hammerhead` (profil équilibré, graines 11-12) : 0 V / 2 D, 0 bloquée, 4,5 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; témoin même fournée `the_getaway_hammerhead` 4,0 rounds, 0 traceback. Journal : Master Key attachée, un PRISONER révélé au Setup, cartes distribuées après manigance ; 1 partie perdue par élimination, 1 par complot.
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

##### 60149 : * Rhino
- [x] Étape 2 : `UnitAttackGainKeyword("This", overkill=True)` (27078, ho016) ; `WhenCardBecomeBoost("This", op)` + `GiveStatus([activating_enemy], "Tough")` (52037 Growing Strong, 60090) ; Toughness, Villainous = bases desc.
- [x] Étape 5 : « Rhino's attacks gain overkill » → `[star]` permanent, propriété d'attaque ; « Boost: Give the **activating enemy** a tough status card » → `message.activating_enemy`.
- [x] Étape 6 : PV 7, ATK 3, SCH 1, boost 3.
- [x] Étape 7 : `60149 … robuste a l'entree (Toughness) ; ses attaques gagnent overkill : Spider-Woman (2 PV) defend, 1 degat passe` ; `60149 … Boost : l'ennemi qui s'active (Hammerhead) devient robuste`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `the_raft_breakout_hammerhead` (profil équilibré, graines 11-12) : 0 V / 2 D, 0 bloquée, 4,5 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; témoin même fournée `the_getaway_hammerhead` 4,0 rounds, 0 traceback. Journal : Master Key attachée, un PRISONER révélé au Setup, cartes distribuées après manigance ; 1 partie perdue par élimination, 1 par complot.
- [x] Étape 8 bis : NON (statut générique).
- Carte terminée : OUI

##### 60150 : Imprisoned
- [x] Étape 2 : `27133` (`PlayersCannotThwartWhile("You", None)`), `11049` (`PlayersCannotAttackWhile`), `PlayersCannotChangeForms(NonKeyword, "You", to_form=AlterEgo)` ; deux `WhenInYourPlayTurn(HeroAction)` (RECETTES §5 « or » = deux capacités), `.SetCost(Cost("3"))` / `CostFunc.Custom(None, fn)` (ho009) ; `Faces.DiscardAll([this])` explicite (hc013 : une obligation révélée reste en jeu) ; `WhenCardBecomeBoost("This")` + `Reveal(GetToPlayer())` (60073) ; obligation de set sans « Give to » (60184, correctif obligation.py du bloc 1).
- [x] Étape 5 : « You cannot thwart, attack, **or** change to alter-ego form » → trois interdits, trois cas ; « Spend 3 resources of any type **or** exhaust characters you control with a **total** THW of 3 or more → discard » → deux capacités, la seconde fait choisir des personnages prêts jusqu'à 3 THW (contre-cas THW total 1 : rien ne se passe, l'obligation reste, le héros reste prêt : le coût Custom rend False et la fabrique n'offre l'action que si des cibles existent) ; « Boost: Reveal this card » → la carte entre en jeu chez le joueur attaqué.
- [x] Étape 6 : 3 ressources / THW 3 ; boost 0 icône.
- [x] Étape 7 : `60150 … je ne peux pas attaquer (0 degat au vilain)` ; `60150 … je ne peux pas contrer (la menace reste a 5)` ; `60150 … je ne peux pas passer en alter-ego` ; `60150 … Hero Action : 3 ressources quelconques (Energy YY + Genius BB) -> defaussee` ; `60150 … Hero Action : incliner le heros (THW 1) et Hellcat (THW 2) = 3 -> defaussee` ; contre-cas `60150 … THW total 1 (heros seul), la seconde capacite ne part pas, l'obligation reste` ; `60150 … Boost : la carte est revelee`. Subst : passe finale du coordinateur (les trois interdits sont des contre-cas d'ABSENCE d'action : rouges attendus sous substitution puisque l'action redevient possible).
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `the_raft_breakout_hammerhead` (profil équilibré, graines 11-12) : 0 V / 2 D, 0 bloquée, 4,5 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; témoin même fournée `the_getaway_hammerhead` 4,0 rounds, 0 traceback. Journal : Master Key attachée, un PRISONER révélé au Setup, cartes distribuées après manigance ; 1 partie perdue par élimination, 1 par complot.
- [x] Étape 8 bis : obligation en `obligations_area` (générique, 60184) ; couvert.
- Carte terminée : OUI

#### Stop the Presses!

##### 60151a : Stop the Presses! 1A
- [x] Étape 2 : `60121a` (`WhenCardSetup("This", op)`) ; `Worlds.GetSetAsideAreaCards` (le scénario met Daily Bugle et les 4 soutiens en `set_aside`) ; `Rand.RandomChoice` (bt001b, déterministe sous graine 42 : Ben Urich) ; `PutIntoPlay(player, under_control=True)` (60139 pour un soutien de rencontre sous contrôle) ; `Faces.RemoveAllFromGame` (60069). Uses (3 stamina) = base desc (fiche `uses.md` : pions posés à l'entrée, sortie au dernier pion, non recodée).
- [x] Étape 5 : « Put the Daily Bugle environment into play » → premier joueur ; « **Each player** puts a **random** DAILY BUGLE support … **under their control** » → une boucle par joueur, tirage sans remise ; « **Remove each remaining** … from the game » → `area_removed` (3 mesurés). Script livré corrigé (`WhenCardSetup` à deux arguments).
- [x] Étape 6 : 1 soutien par joueur, 3 stamina ; scénario `set_aside: [60152, 60153, 60154, 60155, 60156]`.
- [x] Étape 7 : `60151a … Setup : Daily Bugle en jeu, UN soutien DAILY BUGLE au hasard sous mon controle (3 stamina), les 3 autres retires du jeu` (vérificateur `fne3a_bugle`, indépendant de la graine). Subst : passe finale du coordinateur.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `stop_the_presses_hammerhead` (profil équilibré, graines 11-12) : 0 V / 2 D, 0 bloquée, 2,5 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; témoin même fournée `the_raft_breakout_hammerhead` 4,5 rounds, 0 traceback. Journal : Daily Bugle + un soutien sous contrôle au Setup ; les parties se perdent vite (Forced Response du 1B à chaque attaque non défendue : le pilote ne défend pas, 2 menaces par round en plus de l'accélération).
- [x] Étape 8 bis : soutien de RENCONTRE sous le contrôle d'un joueur avec compteurs : même rendu que les œuvres/soutiens d'aspect (zone `area_hero` du joueur) ; environnement en zone vilain ; couvert par les jauges génériques. ⚠ Non vérifié au plateau par un cas dédié (pas de changement de zone atypique : `PutIntoPlay(under_control)` est le chemin de 60139/Converted).
- Carte terminée : OUI

##### 60151b : Stop the Presses! 1B
- [x] Étape 2 : `60121b` Art Museum Heist 1B (`AfterUnitAttackUnit(ForcedResponse, Enemy, Identity, is_undefended_attack=True)`) ; `ChooseAbilities` (08013) ; `RetirerUneEndurance` = `RemoveCountersOn(stamina)` (53029) ; `WhenCardLeavePlay(ForcedInterrupt, CardFinder(DAILY BUGLE, Support))` + `Worlds.SetGameOver(False)` (21139a Odin) ; `IfThisSchemeStageIsCompletedPlayersLoseTheGame` ; `Worlds.IsExpert` (60117).
- [x] Étape 5 : « After an enemy makes an **undefended** attack against **you** » → identité attaquée sans défenseur (contre-cas défendue) ; « **3 threat instead** in expert mode » → cas expert ; « Remove 1 stamina counter from a DAILY BUGLE support **you control** » → branche offerte seulement si le joueur en contrôle un (`condition=` booléen) ; « If a DAILY BUGLE support **leaves play** … the players lose the game » → `WhenCardLeavePlay`, quel que soit le contrôleur (Uses fait sortir la carte au 3e pion retiré : cas dédié). ⚠ Piège payé : `ForChoiceAbility` n'a pas de `conditions=` (voir 60133).
- [x] Étape 6 : départ 1★ / cible 9★ / +1★ ↔ `desc` ; 2 (3 expert) menaces ; 1 stamina.
- [x] Étape 7 : `60151b … attaque non defendue du vilain, premiere branche : 2 menaces ici (1 -> 3)` ; `60151b … (expert) — 3 menaces au lieu de 2 (1 -> 4)` ; `60151b … seconde branche : 1 stamina retiree du soutien DAILY BUGLE que je controle (3 -> 2), pas de menace` ; contre-cas `60151b … attaque DEFENDUE par le heros, rien (menace 1)` ; `60151b … un soutien DAILY BUGLE quitte le jeu (dernier stamina retire) : les joueurs perdent` (`fne3a_bugle_perte`). Subst : passe finale du coordinateur.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `stop_the_presses_hammerhead` (profil équilibré, graines 11-12) : 0 V / 2 D, 0 bloquée, 2,5 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; témoin même fournée `the_raft_breakout_hammerhead` 4,5 rounds, 0 traceback. Journal : Daily Bugle + un soutien sous contrôle au Setup ; les parties se perdent vite (Forced Response du 1B à chaque attaque non défendue : le pilote ne défend pas, 2 menaces par round en plus de l'accélération).
- [x] Étape 8 bis : NON (menace, compteurs, fin de partie : génériques).
- Carte terminée : OUI

##### 60152 : Daily Bugle
- [x] Étape 2 : `WhenInYourPlayTurn(AlterEgoAction, op).SetCostFunc(CostFunc.Exhaust(CardFinder(trait, Support)))` + `return_exhausted_cards` pour viser CE soutien (31009, ho005) ; `PlaceCountersOn(stamina)`.
- [x] Étape 5 : « **Alter-Ego** Action » → sous-type dédié (la partie de test commence en alter-ego) ; « Exhaust a DAILY BUGLE support **you control** → place 1 stamina counter **on that support** » → le coût désigne la cible ; « (Any player can do this.) » → environnement en zone commune, action offerte à chaque joueur en alter-ego (une partie à deux joueurs n'a pas été montée : écart de preuve, pas de code).
- [x] Étape 6 : +1 stamina (3 → 4, au-delà de la valeur Uses initiale : autorisé, rien ne borne).
- [x] Étape 7 : `60152 … Alter-Ego Action : incliner mon soutien DAILY BUGLE -> +1 stamina dessus (3 -> 4)` (soutien incliné, stamina 4). Subst : passe finale du coordinateur.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `stop_the_presses_hammerhead` (profil équilibré, graines 11-12) : 0 V / 2 D, 0 bloquée, 2,5 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; témoin même fournée `the_raft_breakout_hammerhead` 4,5 rounds, 0 traceback. Journal : Daily Bugle + un soutien sous contrôle au Setup ; les parties se perdent vite (Forced Response du 1B à chaque attaque non défendue : le pilote ne défend pas, 2 menaces par round en plus de l'accélération).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

##### 60153 : * Ben Urich
- [x] Étape 2 : `CoutDeReporter()` = `CostFunc.Exhaust("This")` + `CostFunc.Counter("This", 1, 'stamina')` (60105 « Fight. », 61033a) ; `player.LookAtDeck("EncounterDeck", 2)` (bc006 Cat Burglary) ; `AskChooseFace(forced=False)` (= « you may ») ; `Faces.DiscardAll`. Uses = base.
- [x] Étape 5 : « Exhaust Ben Urich **and** remove 1 stamina counter → » → deux coûts ; « look at the top 2 » → `LookAtDeck` ; « You **may** discard 1 » → `forced=False` (⚠ `AskChooseFace` n'a pas de paramètre `may` : `TypeError` avalé) ; « (Put the rest back in the same order.) » → `LookAtDeck` ne déplace pas les cartes (`not_move`).
- [x] Étape 6 : 2 cartes, 1 défaussée, 3 stamina (Uses).
- [x] Étape 7 : `60153 … Action : incliner + 1 stamina -> regarde les 2 cartes du dessus du deck rencontre, en defausse 1` (Hydra Mercenary défaussé, Advance reste, stamina 2, incliné). Subst : passe finale du coordinateur.
- [x] Étape 7 bis : Uses (3) : natif, non recodé (sortie prouvée sur 60151b « quitte le jeu »).
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `stop_the_presses_hammerhead` (profil équilibré, graines 11-12) : 0 V / 2 D, 0 bloquée, 2,5 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; témoin même fournée `the_raft_breakout_hammerhead` 4,5 rounds, 0 traceback. Journal : Daily Bugle + un soutien sous contrôle au Setup ; les parties se perdent vite (Forced Response du 1B à chaque attaque non défendue : le pilote ne défend pas, 2 menaces par round en plus de l'accélération).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

##### 60154 : * Betty Brant
- [x] Étape 2 : `bc007` Misfortune (`WhenBoostCardWouldTurnedFaceUp` + `SetBeInstead`, la carte DOIT quitter le paquet de boost sinon boucle) ; `60072` Lady Bullseye (`GiveFacedownBoostCardsInternal(1, effect, would_message)` : la carte de remplacement est posée face cachée et retournée par la boucle de `ResolveBoostCards`) ; `CoutDeReporter()`.
- [x] Étape 5 : « **Interrupt**: When a boost card is turned faceup » → optionnelle (le pilote l'accepte), fenêtre AVANT le retournement ; « cancel that card's boost icons **and** "Boost" ability » → la carte n'est jamais retournée ni comptée (défaussée) ; « Give the activating enemy **another** boost card **for this activation** » → face cachée immédiatement (RECETTES §7quater : `GiveAdditionalBoostCardForThisActivation` viserait l'activation suivante) ; contre-cas Betty inclinée : le coût n'est pas payable, l'interruption n'est pas offerte.
- [x] Étape 6 : 1 + 0 = 1 (Under Fire 3 icônes annulée, Advance 0 en remplacement) vs 1 + 3 = 4 sans elle.
- [x] Étape 7 : `60154 … la carte boost retournee (Under Fire, 3 icones) est annulee, une autre (Advance, 0) la remplace : 1 + 0 = 1` (Under Fire en défausse, stamina 2, inclinée) ; contre-cas `60154 … Betty deja inclinee, l'interruption n'est pas offerte (1 + 3 = 4)`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : Uses (3) : natif.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `stop_the_presses_hammerhead` (profil équilibré, graines 11-12) : 0 V / 2 D, 0 bloquée, 2,5 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; témoin même fournée `the_raft_breakout_hammerhead` 4,5 rounds, 0 traceback. Journal : Daily Bugle + un soutien sous contrôle au Setup ; les parties se perdent vite (Forced Response du 1B à chaque attaque non défendue : le pilote ne défend pas, 2 menaces par round en plus de l'accélération).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

##### 60155 : * J. Jonah Jameson
- [x] Étape 2 : `CoutDeReporter()` + `CostFunc.DealPlayerEncounterCard(1, "Initiator")` (trois coûts chaînés, RECETTES §5) ; `DrawUp(2)`.
- [x] Étape 5 : « Exhaust …, remove 1 stamina counter, **and** deal yourself 1 facedown encounter card → draw 2 cards » → trois coûts, tous payés avant la pioche (mesurés : incliné, stamina 2, 1 carte distribuée, main 1 → 3).
- [x] Étape 6 : 1 carte distribuée, 2 piochées.
- [x] Étape 7 : `60155 … Action : incliner + 1 stamina + 1 carte rencontre face cachee -> pioche 2 (main 1 -> 3)`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : Uses (3) : natif.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `stop_the_presses_hammerhead` (profil équilibré, graines 11-12) : 0 V / 2 D, 0 bloquée, 2,5 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; témoin même fournée `the_raft_breakout_hammerhead` 4,5 rounds, 0 traceback. Journal : Daily Bugle + un soutien sous contrôle au Setup ; les parties se perdent vite (Forced Response du 1B à chaque attaque non défendue : le pilote ne défend pas, 2 menaces par round en plus de l'accélération).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

##### 60156 : * Robbie Robertson
- [x] Étape 2 : `AfterPlayerDealEncounterCard(Response, op)` (player.py:414) ; la carte = `message.would_message.face`, le joueur = `message.GetToPlayer()` (⚠ pas de `trigger` sur un `TriggerPlayerMessage` : `AttributeError` avalé) ; `AskChooseFace(forced=False)` ; `DealEncounterCards(1)` ; `CoutDeReporter()`.
- [x] Étape 5 : « After **a player** is dealt a facedown encounter card » → tout joueur, la Réponse est au contrôleur de Robbie (une partie à deux n'a pas été montée) ; « look at **that** encounter card » → la carte distribuée ; « You **may** discard it **and** deal **that player** another » → `forced=False`, puis `joueur_vise.DealEncounterCards(1)`.
- [x] Étape 6 : 1 défaussée, 1 redistribuée, stamina 2.
- [x] Étape 7 : `60156 … Response : la carte distribuee (Hydra Mercenary) est regardee, defaussee, et une autre (Advance) est distribuee a la place` (`distribuees` = [01186], Hydra Mercenary en défausse, stamina 2, incliné). ⚠ Montage : une carte au fond du deck (`01193`), sinon le deck vidé remélange sa défausse et la carte défaussée « disparaît » (RECETTES §7ter). Subst : passe finale du coordinateur.
- [x] Étape 7 bis : Uses (3) : natif.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `stop_the_presses_hammerhead` (profil équilibré, graines 11-12) : 0 V / 2 D, 0 bloquée, 2,5 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; témoin même fournée `the_raft_breakout_hammerhead` 4,5 rounds, 0 traceback. Journal : Daily Bugle + un soutien sous contrôle au Setup ; les parties se perdent vite (Forced Response du 1B à chaque attaque non défendue : le pilote ne défend pas, 2 menaces par round en plus de l'accélération).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

##### 60157 : Exclusive Interview
- [x] Étape 2 : `*CardCannotReady(CardFinder(trait, Support))` (state.py:224, rend une liste) ; `WhenThisRevealed` + `Faces.ExhaustAll(SoutiensDailyBugle)` (bt004).
- [x] Étape 5 : « DAILY BUGLE supports **cannot ready** » → continu, tous joueurs ; « When Revealed: Exhaust **each** DAILY BUGLE support » → tous (deux soutiens en jeu dans le cas). Témoin du harnais : sans la carte, `Puzzle.Ready` redresse bien un soutien.
- [x] Étape 6 : 6 menaces, boost 1.
- [x] Étape 7 : `60157 … When Revealed : chaque soutien DAILY BUGLE est incline ; 6 menaces` ; `60157 … les soutiens DAILY BUGLE ne peuvent pas se redresser` ; témoin `60157 … contre-cas : sans elle, Ben Urich se redresse` (vert par construction sous substitution). Subst : passe finale du coordinateur.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `stop_the_presses_hammerhead` (profil équilibré, graines 11-12) : 0 V / 2 D, 0 bloquée, 2,5 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; témoin même fournée `the_raft_breakout_hammerhead` 4,5 rounds, 0 traceback. Journal : Daily Bugle + un soutien sous contrôle au Setup ; les parties se perdent vite (Forced Response du 1B à chaque attaque non défendue : le pilote ne défend pas, 2 menaces par round en plus de l'accélération).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

##### 60158 : Breaking News
- [x] Étape 2 : `ChooseAbilities(ForChoiceAbility(condition=bool), ForChoiceAbility)` (08013) ; `ExhaustAll` + `RetirerUneEndurance` ; `PlaceThreatOnSchemes("MainScheme", 2)` ; `WhenCardBecomeBoost("This")` (an013).
- [x] Étape 5 : « (under **any** player's control) » → `SoutiensDailyBugle(effect)` sans filtre de joueur, le joueur qui révèle choisit s'il y en a plusieurs ; branche cachée s'il n'y a aucun soutien ; « Boost: Exhaust a DAILY BUGLE support » → sans retrait de stamina (mesuré : stamina 3).
- [x] Étape 6 : 1 stamina / 2 menaces ; boost 0 icône.
- [x] Étape 7 : `60158 … premiere branche : mon soutien DAILY BUGLE est incline et perd 1 stamina (3 -> 2)` ; `60158 … seconde branche : 2 menaces sur le complot principal (1 -> 3), le soutien intact` ; `60158 … Boost : mon soutien DAILY BUGLE est incline (stamina intacte)`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 2 parties Spider-Man vs `stop_the_presses_hammerhead` (profil équilibré, graines 11-12) : 0 V / 2 D, 0 bloquée, 2,5 rounds, **0 traceback / 0 erreur** (grep exhaustif) ; témoin même fournée `the_raft_breakout_hammerhead` 4,5 rounds, 0 traceback. Journal : Daily Bugle + un soutien sous contrôle au Setup ; les parties se perdent vite (Forced Response du 1B à chaque attaque non défendue : le pilote ne défend pas, 2 menaces par round en plus de l'accélération).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

### 6. Questions pour l'utilisateur (hypothèse littérale implémentée)

Aucune ambiguïté bloquante. Deux hypothèses littérales implémentées, à confirmer si l'on veut :

1. **60131 Jackknifed Tanker Truck + Out Front** (scan `scratchpad/scans/60131.jpg`, `60129a.jpg`) : quand le vilain « cannot be dealt damage » et qu'Out Front dit « when the villain **would** be dealt damage, remove that amount of threat instead », j'ai retenu que « cannot » prime : aucun dégât ET aucune menace retirée (c'est ce que fait le moteur). Options : A) garder (recommandé, c'est la règle « cannot » du RRG) ; B) la menace est quand même retirée ; C) Autre (précise).
2. **60152 Daily Bugle « (Any player can do this.) »** et **60156 Robbie « After a player is dealt … »** : implémentés pour tout joueur, mais seule une partie à UN joueur a été montée au harnais. Options : A) suffisant pour l'instant (recommandé) ; B) monter un cas à deux joueurs (`heros2`) avant livraison ; C) Autre (précise).

### 7. Ce que ces gates ne voient pas

- Aucune partie humaine dans le navigateur sur ces trois scénarios.
- Preuve par substitution : passe finale du coordinateur (`substituer_pack.py`), non lancée ici (interdit du brief §3.4). Contre-cas d'ABSENCE d'effet attendus verts sous substitution : 60128b « sans menace », 60143 × 2, 60147 × 2, 60145 « aucun allié », 60151b « défendue », 60154 « Betty inclinée », 60157 « témoin Ready », 60130 « 1 compteur ».
- Parties à deux joueurs (Daily Bugle « any player », Robbie « a player », Raft 1A « each player », Alongside « each player ») : non montées.
- `PeutCouvrirLeCout` (Burning Rubber) ignore les générateurs de ressources en jeu (écart hérité du bloc 1).

## Bloc 3B — Drive, Disasters, Tombstone, Tracksuit Mafia (18/09/2026, agent B)

Écrit par un agent parallèle ; son rapport (bilan, gabarits, pièges,
questions) est RECOPIÉ ici, le brouillon de session ayant disparu avec le
répertoire temporaire. Pièges : RECETTES-MOTEUR §7quinquies à §7septies.
Substitution : passe finale du coordinateur, voir « Fusion et gates de fin ».

### 1. Bilan harnais

```
FILTRE « [fne3b] » : 66/2182 cas retenus
BILAN : 66/66 cas passes
```
(PARALLELES=4, port 42200, `/tmp/rapport-b.json`, passe finale après trois corrections de script et deux corrections de montage ; passes précédentes 34/66 puis 63/66.)

Cas par carte (préfixe = card_id, tous `[fne3b]`) :

| Carte | Cas |
|---|---|
| 60186 Sports Car | s'attache a l'ennemi a l'ATK le plus haut (Enforcers 2 > Hammerhead 1) : +1 ATK · l'ennemi a l'ATK le plus haut porte deja un VEHICLE (Utility Van) : la voiture passe a Hammerhead · aucun ennemi sans VEHICLE : surge · 3 degats a Hammerhead : places sur la voiture a la place · 3 + 1 = 4 degats accumules : la voiture est defaussee, Hammerhead intact · 6 degats d'un coup : tout est place ici, rien ne deborde sur Hammerhead, la voiture part |
| 60187 Motorcycle | s'attache a l'ennemi au SCH le plus haut (Hammerhead 2 > Underboss 1) : +1 SCH · l'attaque de base du heros (2) est placee sur la moto, Hammerhead intact · 2 + 1 = 3 degats accumules : la moto est defaussee |
| 60188 Utility Van | s'attache a l'ennemi avec le moins de PV restants (Mercenary 3 < Hammerhead 14) · PV RESTANTS, pas imprimes : Hammerhead blesse a 2 PV passe devant le Mercenary (3) · 5 degats sur le sbire porteur (3 PV) : poses sur le van, le sbire est intact · 5 + 1 = 6 degats accumules : le van est defausse, le sbire toujours intact |
| 60189 Traffic Jam | revele : 2 + Hinder 2[per_hero] = 4 menaces, icone crise · Hammerhead a moto manigance (2 + 1) : la menace va sur Traffic Jam, pas sur le complot principal · contre-cas : Hammerhead sans vehicule manigance, la menace va sur le complot principal · le heros a bord d'un vehicule contre Consolidate Power : la menace est retiree de Traffic Jam a la place · contre-cas : le heros sans vehicule contre Consolidate Power normalement |
| 60190 Carjacking | sans 3 ressources identiques : la Sports Car defaussee du deck est revelee et s'attache a Hammerhead · 3 [physical] payes : la Sports Car s'attache a l'identite a la place · contre-cas : l'identite porte deja un VEHICLE, pas de choix, la moto trouvee va a Hammerhead · aucun VEHICLE dans le deck : tout est defausse (le deck vide se remelange), rien ne s'attache |
| 60177 Mystic Incursion | revelee : Uses (2 civils), icone crise ; Hero Action [mental][mental] : 1 civil retire · Hero Action incliner le heros (non MYSTIC) : 1 civil retire · incliner Wong (MYSTIC) : 2 civils retires, la carte quitte le jeu (Uses) |
| 60178 Sinking Ferry | Hero Action [energy][energy] : 1 civil retire · incliner Wasp (AERIAL) : 2 civils retires, la carte quitte le jeu · contre-cas : incliner Wong (MYSTIC, pas AERIAL) : 1 seul civil |
| 60179 Towering Inferno | Hero Action [physical][physical] : 1 civil retire · incliner le heros robuste : 2 civils retires, la carte quitte le jeu, la robustesse reste · contre-cas : incliner Wong (MYSTIC, pas robuste) : 1 seul civil |
| 60180 Collapsing Bridge | revele : 1 + Hinder 2[per_hero] = 3 menaces, icone alea · Hellcat contre 2 : 5 - 2 + 1 = 4 menaces · contre-cas : la menace retiree du complot principal ne fait pas rechuter le pont · Hellcat contre 2 (3 -> 1 -> 2), puis Spider-Woman contre 2 (2 -> 0) : le pont est vaincu, rien ne revient |
| 60181 Bystanders in Peril | une catastrophe en jeu : +1 civil (2 -> 3) · aucune catastrophe en jeu : Sinking Ferry est cherchee dans le deck et revelee (2 civils) · la catastrophe est dans la defausse : trouvee aussi · Boost : +1 civil sur la catastrophe en jeu (attaque 1 + 1 icone = 2) |
| 60195 Cold as Ice | s'attache au sbire aux PV imprimes les plus hauts (Underboss 4 > Enforcers 3), qui devient robuste : +2 SCH · aucun sbire : surge · le sbire attache manigance (0 + 2) : l'identite du premier joueur est desorientee, la carte est defaussee |
| 60196 Hard as Marble | s'attache au sbire aux PV imprimes les plus hauts, qui devient robuste : +2 ATK · le sbire attache attaque le heros (1 + 2 = 3) : le heros est etourdi, la carte defaussee · l'attaque est defendue par Brawn (5 PV) : c'est Brawn qui est etourdi (3 degats) · le defenseur (Spider-Woman 2 PV) est vaincu : personne a etourdir, la carte est quand meme defaussee |
| 60197 Beetle | When Revealed : Hard as Marble (deck) est attachee a Beetle ; Gatling Gun (deck) et Hardheaded (defausse), reservees au vilain, restent · contre-cas : seul un attachement reserve au vilain est disponible : rien n'est attache |
| 60198 Tombstone | Boost : Hammerhead devient robuste (attaque 1 + 0 icone) · Quickstrike (base desc) : entre en jeu engage en forme heros et attaque (2) |
| 60199 Hit List | revele (3 menaces) ; la phase du mechant commence : 3 degats indirects au premier joueur, aucun allie vaincu : la menace reste · Spider-Woman (2 PV) prend 2 et meurt, l'identite 1 : 1[per_hero] menace retiree (3 -> 2) |
| 60200 Ivan Banionis | When Revealed : 1 jeton acceleration sur lui · apres sa manigance (SCH 0) : un second jeton acceleration · Teamwork (TRACKSUIT), base desc : entre en jeu avec Tracksuit Bro deja la : les deux s'activent (2 + 2) |
| 60201 The Clown | apres sa manigance (Villainous : Advance, 0 icone) : une carte boost face cachee lui reste (Under Fire) · puis il attaque : la carte gardee s'ajoute a celle de Villainous (1 + 3 + 3 = 7) |
| 60202 Tracksuit Mafioso | vaincu avec Tracksuit Mafia en jeu : glisse sous le complot · sans le complot : le heros qui l'acheve (5 + 2) est etourdi ET desoriente · limite : vaincu sans personnage (Puzzle.Damage) et sans complot : rien a etourdir, pas d'erreur |
| 60203 Tracksuit Bro | vaincu avec Tracksuit Mafia en jeu : glisse sous le complot · sans le complot : melange dans le deck rencontre |
| 60204 Tracksuit Mafia | When Revealed (3[per_hero]) : defausse jusqu'a un sbire TRACKSUIT (Advance defaussee) et le glisse dessous · un TRACKSUIT (Mafioso) revele depuis le deck : le joueur revele le Bro glisse dessous · contre-cas : aucun TRACKSUIT dans le deck a la revelation : tout est defausse, rien dessous · contre-cas : un sbire non-TRACKSUIT revele : rien ne sort de dessous |

Ce que le harnais a trouvé (3 passes : 34/66 → 63/66 → 66/66) :
- Les 27 premiers rouges de la passe 1 : `AttributeError: 'World' object has no attribute 'world'` dans `Puzzle.FindOrCreateFace` (`puzzle.py:50`, `Worlds.GetSetAsideAreaCards(self.world)`) : état TRANSITOIRE du correctif Protection Racket du coordinateur, réglé à 19:10 (le fichier itère désormais `self.world.aside_deck`). Rien à faire côté B.
- **60199 Hit List** : `operation=` de `TakeIndirectDamage` n'est jamais rappelée pour une unité VAINCUE (`can_health.py:288`, `if unit.IsInPlay()`), la menace ne bougeait pas. → comparaison des alliés en jeu avant / après.
- **60180 Collapsing Bridge** : `AfterSchemeRemoveThreat` part AVANT le contrôle de défaite (`scheme.py:145-150`) : un pont ramené à 0 recevait 1 menace et n'était JAMAIS vaincu. → condition `encore_de_la_menace` (`threat > 0`). Et le montage `Puzzle.SetThreat('60180', 2)` depuis 3 était un RETRAIT qui déclenchait la réponse (3 → 2 → 3) : descente par deux contres.
- **60197 Beetle** : `Asset2.CanAttachTo` (asset.py:69) ne teste que MaxPerUnit : Energy Gatling Gun (« Attach to the villain ») s'accrochait à Beetle. → helper `PeutSAccrocherAUnSbire` (relecture de la phrase imprimée « Attach to … », voir §3 et §4).
- **60190 Carjacking** sans véhicule : le deck épuisé se remélange avec la défausse (`deck.py:483`) ; l'attendu lit `dans_deck_rencontre`.
- **60196** : Groot (16047) se soigne de 2 après sa défense ; remplacé par Brawn (10011).
- Port 42050 occupé par un autre processus à deux passes (« aucun resultat (processus mort) », `AssertionError: ip/port` dans le journal) : rejoué sur 42100 puis 42200.

### 5. Gabarits PROCESSUS-CARTE (un par carte)

Conventions : « cas » = nom dans `tools/test_capacites.py` (préfixe = card_id, filtre `[fne3b]`) ; « subst : passe finale du coordinateur » ; étape 8 commune (voir bas de section) ; les bases `desc` (Uses, Crisis, Hazard, Hinder, Peril, Teamwork, Villainous, Retaliate, Vulnerable, Quickstrike, Surge, `ATK+`/`SCH+`/`THW+`) ont toutes leur fiche dans `mots-cles/`, aucune fiche à créer.

Étape 8 commune (autoplay, profil équilibré, Spider-Man, graines 1-8) :
- 8 parties vs `the_getaway_hammerhead` (charge **Drive**) : 0 V / 8 D, 0 bloquée, 4,1 rounds ; tracebacks : **0 dans 6 journaux, 15 dans chacun des journaux 5 et 6, tous identiques et étrangers à Drive** (`AssertionError card_type.py:247`, `OnEvent.Counter("MainScheme", 'speed')` de **60130 Escort Vehicle**, set The Getaway, agent A : une chaîne est une `Sequence`, voir §4). Drive vu en partie : Utility Van révélé 2× (sur Maggia Enforcers, puis sur Hammerhead), Motorcycle révélée 1× (sur Hammerhead), Sports Car / Motorcycle / Van servis comme boost, Sports Car et Van défaussés par Power Struggle ; Traffic Jam et Carjacking jamais révélés (parties courtes).
- 8 parties vs `art_museum_heist_hammerhead --modulaires disasters,tombstone,tracksuit_mafia` : 0 V / 7 D, **1 bloquée** (graine 7 : boucle du pilote sur Tenacity 01093, défaut CONNU du bloc 2, après un échange normal avec Tracksuit Mafioso, Retaliate 2 bien appliqué), 5,5 rounds, **0 traceback, 0 erreur** (grep `NameError|AttributeError|TypeError|KeyError|AssertionError` sur les 8 journaux). Vu en partie : Mystic Incursion et Sinking Ferry perdent des civils par les Hero Actions du pilote ; Hard as Marble révélée 3× (Chameleon s'équipe et devient robuste) ; Beetle attaque 3× avec ses boosts Villainous ; Ivan révélé 2× avec son jeton d'accélération, glissé sous Tracksuit Mafia à sa révélation, puis défaussé quand le complot quitte le jeu ; Mafioso révélé 3×, Bro 2× ; Cold as Ice, Hit List, Collapsing Bridge, Bystanders in Peril, Towering Inferno seulement comme boost. Témoin : la même fournée bloc 1 (`rhino`, 0 traceback) reste la référence, non rejouée ici.

##### 60186 : Sports Car
- [x] Étape 2 : `AttachToFaceWhenPutIntoPlay(CardFinder(Enemy, not_with_attach=CardFinder(trait=VEHICLE)), highest_atk=True, if_cannot_gain_surge=True)` (60191 Flight Serum pour le finder + surge) ; `WhenUnitWouldTakeDamage(Enemy, conditions=[le_porteur])` + `PreventDamage("All")` + compteurs `damage` (60117 Assembled Armor, même patron) ; `desc.ATK+` = +1 natif. Tronc commun `CapacitesDUnVehicule(seuil, **critere)` (drive/__init__.py).
- [x] Étape 5 : « the enemy with the **highest ATK** » → `highest_atk` (Enforcers 2 > Hammerhead 1) ; « **without** a VEHICLE attachment » → `not_with_attach` (cas Van-sur-Enforcers) ; « **Otherwise**, surge » → `if_cannot_gain_surge` ; « **any amount** of damage … place it here **instead** » → tout est prévenu et posé, rien ne déborde (cas 6 dégâts) ; « If there is **4 or more** » → seuil lu après la pose.
- [x] Étape 6 : +1 ATK (`ATK+`), boost 2, seuil 4 ↔ `CapacitesDUnVehicule(4, highest_atk=True)`.
- [x] Étape 7 : 6 cas (voir tableau §1) ; contre-cas d'absence : « aucun ennemi sans VEHICLE : surge ». Subst : passe finale du coordinateur.
- [x] Étape 7 bis : NON (seuil, pas limite).
- [x] Étape 8 : commune (Sports Car seulement comme boost et défaussée par Power Struggle en partie ; le montage réel est prouvé par le cas « attaque de base du héros » de 60187, même tronc).
- [x] Étape 8 bis : OUI (attachement sur un ennemi, compteurs `damage` dessus) : couvert par `fne-oeuvre-volee.test.ts` (attachement dessiné sur `area_villain`) et par `enUnites` (sous-arbre par `bind_object_id`, aussi pour un sbire) ; les compteurs sont la jauge générique.
- Carte terminée : OUI

##### 60187 : Motorcycle
- [x] Étape 2 : même tronc, `highest_sch=True`, `desc.SCH+`/`THW+`.
- [x] Étape 5 : « highest **SCH** » → `highest_sch` ; ⚠ mesure faite avec `ARTS_OFF` (Pottery donne +1 SCH à Hammerhead et fausserait `attributs_carte`) ; « 3 or more ».
- [x] Étape 6 : +1 SCH/THW, boost 1, seuil 3.
- [x] Étape 7 : 3 cas, dont « l'attaque de base du heros (2) est placee sur la moto » qui prouve le chemin réel (`Puzzle.Attack('01001a')` + `cibles`). Subst : passe finale du coordinateur.
- [x] 7 bis NON · 8 commune (révélée 1× sur Hammerhead) · 8 bis OUI, couvert (idem 60186).
- Carte terminée : OUI

##### 60188 : Utility Van
- [x] Étape 2 : même tronc, `fewest_remaining_hp=True` (24023 Out for Blood).
- [x] Étape 5 : « fewest **remaining** hit points » → santé courante, prouvé par le cas Hammerhead blessé à 2 PV ; « 6 or more ».
- [x] Étape 6 : aucun bonus, boost 1, seuil 6.
- [x] Étape 7 : 4 cas (un sbire à 3 PV survit à 5 dégâts). Subst : passe finale du coordinateur.
- [x] 7 bis NON · 8 commune (révélé 2×) · 8 bis OUI, couvert.
- Carte terminée : OUI

##### 60189 : Traffic Jam
- [x] Étape 2 : `WhenSchemeWouldPlaceThreat(ForcedInterrupt, None, op, conditions=[…])` + `message.PreventThreat("All")` + `PlaceThreatOnSchemes([this])` ; `WhenSchemeWouldRemoveThreat(ForcedInterrupt, None, op, conditions=[…])` + `message.SetCannotBeRemoved(effect)` + `RemoveThreatFromSchemes([this])` (fabriques scheme.py:22/83, modèle 50043 Eyepatch Camera pour le « instead » de menace). Hinder 2*, Crisis = bases.
- [x] Étape 5 : « a **character** with a VEHICLE attachment » → `AUnVehicule` sur `sch_message.trigger` (manigance) ou `by_effect.this` (effet), et sur `by_face` (contre) ; « that threat is added **here instead** » → prévention totale + pose ici ; « removed from **here** instead » → verrou + retrait ici ; `message.trigger is this` exclu (pas de récursion). ⚠ Avec la Crise en jeu, le complot principal n'est plus contrable : le cas « retrait » vise Consolidate Power (60094).
- [x] Étape 6 : 2 + Hinder 2[per_hero] = 4 mesurés, boost 3, icône crise (`icones`).
- [x] Étape 7 : 5 cas (2 nominaux + 2 contre-cas + révélation). Journal : « La menace ne peut pas être retirée de Consolidate Power » puis « Traffic Jam perd 1 ». Subst : passe finale du coordinateur.
- [x] 7 bis NON · 8 commune (jamais révélé en 8 parties, parties courtes) · 8 bis : chiffres et icône crise (pastille générique) ; NON.
- Carte terminée : OUI

##### 60190 : Carjacking
- [x] Étape 2 : `Worlds.DiscardEncounterCardsUntil(trait="VEHICLE", card_type=Attachment)` (60184 Wanted) ; `ChooseAbilities(ForChoiceAbilityWithCost(Cost("3", same_type=True), …, conditions=[payable]), Otherwise(...))` avec `PeutCouvrirLeCout` (60127 Tug of War, RECETTES §3) ; `face.Reveal(joueur, effect)` depuis la défausse (60109) ; `AttachTo2(identite)`.
- [x] Étape 5 : « until a VEHICLE attachment is discarded **and reveal it** » → la carte trouvée est révélée (elle s'accroche seule, surge si impossible) ; « **If your identity does not have** a VEHICLE » → contre-cas sans choix ; « **you may** spend 3 resources **of the same type** » → branche offerte seulement si payable (Energy YY refusée, RRR acceptée) ; « attach … to your identity **instead** » → la révélation n'a pas lieu (cas RRR : `hotes [[60186, 01001a]]`).
- [x] Étape 6 : 3 ressources, même type, boost 2.
- [x] Étape 7 : 4 cas. Subst : passe finale du coordinateur.
- [x] 7 bis NON · 8 commune (jamais révélée) · 8 bis OUI (attachement de rencontre sur l'IDENTITÉ) : couvert par `fne-oeuvre-volee.test.ts` (œuvre dessinée sur le héros, même zone d'améliorations).
- Carte terminée : OUI

##### 60177 / 60178 / 60179 : Mystic Incursion / Sinking Ferry / Towering Inferno
- [x] Étape 2 : tronc `CapacitesDeCatastrophe(cout, libelle, double)` : deux `WhenInYourPlayTurn(HeroAction)` (RECETTES §5 « or » = deux capacités, modèle 60122-60125 œuvres), l'une `.SetCost(Cost("BB"|"YY"|"RR"))`, l'autre `.SetCostFunc(CostFunc.Exhaust("Hero|Ally"))` dont `return_exhausted_cards` dit QUI a été incliné ; `Faces.RemoveCountersOn([this], n, 'civilian')` ; Uses (2 civilian) et Crisis = bases (fiche `uses.md` : la sortie au dernier pion est native, NON recodée ; compteur `civilian` ajouté à l'énum par le coordinateur).
- [x] Étape 5 : « Spend [x][x] **or** exhaust a hero or ally **you control** » → deux capacités ; « **2 counters instead** if you exhausted a MYSTIC / AERIAL character / a character **that has a tough status card** » → `double(f)` sur la carte inclinée, lu après l'inclinaison (incliner ne consomme pas la robustesse : `statuts [[01001a, Tough]]` après) ; contre-cas croisés (Wong sur Ferry et Inferno : 1 seul).
- [x] Étape 6 : 2 civils, BB / YY / RR, 1 ou 2 retirés, boost 2, crise.
- [x] Étape 7 : 60177 : 3 cas ; 60178 : 3 cas ; 60179 : 3 cas (voir tableau). Subst : passe finale du coordinateur.
- [x] 7 bis : Uses 2 = épuisement natif, prouvé par `hors_jeu` après 2 retirés.
- [x] Étape 8 : commune (Mystic Incursion et Sinking Ferry perdent des civils en partie par les Hero Actions du pilote, aucune erreur).
- [x] Étape 8 bis : compteurs sur un environnement (jauge générique) ; NON.
- Carte terminée : OUI (les trois)

##### 60180 : Collapsing Bridge
- [x] Étape 2 : `AfterSchemeRemoveThreat(ForcedResponse, "This", op, conditions=[au_moins_une, encore_de_la_menace])` (fabrique scheme.py:156) + `PlaceThreatOnSchemes([this], 1)` ; Hinder 2*, Hazard = bases.
- [x] Étape 5 : « After **any amount** of threat is removed » → `value > 0` ; « from **Collapsing Bridge** » → `"This"` (contre-cas : le complot principal contré ne fait rien) ; ⚠ hypothèse : le pont ramené à 0 est **vaincu**, la réponse ne résout pas (`threat > 0`), sinon il est invincible (question §5).
- [x] Étape 6 : 1 + Hinder 2[per_hero] = 3 mesurés, +1 par retrait, boost 2.
- [x] Étape 7 : 4 cas (révélation, rechute 5 → 4, contre-cas, défaite par deux contres). Subst : passe finale du coordinateur.
- [x] 7 bis NON · 8 commune (vu comme boost seulement) · 8 bis NON (chiffres).
- Carte terminée : OUI (sous réserve de la question §5.1)

##### 60181 : Bystanders in Peril
- [x] Étape 2 : `Worlds.FindCardsOnField(trait="DISASTER", card_type=Environment)` + `AskChooseFace` si plusieurs + `PlaceCountersOn(civilian)` ; `Search.SearchForCard(include_encounter_deck, include_encounter_discard_pile)` + `Reveal` (60109, 60185) ; `WhenCardBecomeBoost("This")` ; Peril = base.
- [x] Étape 5 : « Place 1 civilian counter on **a** DISASTER environment » → choix si plusieurs ; « **If no counter was placed** this way » → retour booléen de `PoserUnCivil` ; « search the encounter deck **and** discard pile … and **reveal** it » → les deux zones (deux cas) ; « [star] Boost » = `WhenCardBecomeBoost`.
- [x] Étape 6 : 1 civil, boost 1.
- [x] Étape 7 : 4 cas. Subst : passe finale du coordinateur.
- [x] 7 bis NON · 8 commune · 8 bis NON.
- Carte terminée : OUI

##### 60195 : Cold as Ice
- [x] Étape 2 : `AttacheAuSbireLePlusSolide()` = `AttachToFaceWhenPutIntoPlay(Minion, highest_printed_hp=True, if_cannot_gain_surge=True, when_attach_operation=GiveStatus Tough)` ; `AfterUnitSchemeEnd(ForcedResponse, "AttachedEnemy")` (60068b) + `GiveStatus([Worlds.GetFirstPlayer().GetIdentity()], "Confused")` + `DiscardAll([this])` ; `desc.SCH+` = +2.
- [x] Étape 5 : « the minion with the highest **base** hit points » → `highest_printed_hp` (Underboss 4 > Enforcers 3) ; « **and give that minion** a tough status card » → au moment de l'accrochage ; « Otherwise, surge » ; « After attached minion **schemes** » → `AfterUnitSchemeEnd` ; « the **first player's** identity » → `GetFirstPlayer` ; « and discard Cold as Ice » → défausse après.
- [x] Étape 6 : +2 SCH (menace 1 + 0 + 2 = 3 mesurée), boost 2.
- [x] Étape 7 : 3 cas. Subst : passe finale du coordinateur.
- [x] 7 bis NON · 8 commune (vu comme boost) · 8 bis OUI (attachement sur un sbire + statut) : couvert (`enUnites`, statuts génériques).
- Carte terminée : OUI

##### 60196 : Hard as Marble
- [x] Étape 2 : même accrochage ; `AfterUnitAttackEnd(ForcedResponse, "AttachedEnemy")` avec `message.attacked_targets` (60089 Gatling Gun) + `GiveStatus Stunned` + `DiscardAll`.
- [x] Étape 5 : « stun **the attacked character** » → le défenseur (Brawn) ou l'identité, jamais « le joueur » ; cibles filtrées `IsInPlay and not IsDefeated` (Spider-Woman vaincue : rien à étourdir, carte quand même défaussée).
- [x] Étape 6 : +2 ATK (1 + 2 = 3 mesurés), boost 2.
- [x] Étape 7 : 4 cas. Subst : passe finale du coordinateur.
- [x] 7 bis NON · 8 commune (révélée 3× : Chameleon s'équipe et devient robuste) · 8 bis OUI, couvert.
- Carte terminée : OUI

##### 60197 : * Beetle
- [x] Étape 2 : `Search.SearchForCard(faces=candidats, card_type=Attachment)` (60109) + `AttachTo2(this)` ; candidats = deck + défausse filtrés par `PeutSAccrocherAUnSbire` (tombstone/__init__.py) ; Villainous = base.
- [x] Étape 5 : « an attachment **that can attach to a minion** » → ⚠ la règle moteur `Asset2.CanAttachTo` ne connaît que MaxPerUnit (Gatling Gun s'accrochait) ; la cible imprimée ne vit que dans le sélecteur fermé de `AttachToFaceWhenPutIntoPlayInternal` (asset.py:153) : le helper relit la phrase « Attach to … » du `paper.text` (villain / hero / identity / ally → non ; minion / enemy / character → oui, traits `[[X]]` exigés, `non-[[X]]` refusés). Limites assumées : « without a VEHICLE attachment » n'est pas relu ; une carte sans phrase « Attach to » est acceptée. « attach it to Beetle » → accrochage direct, SANS le « give that minion a tough status card » de Hard as Marble (instruction propre à SON entrée en jeu, non résolue ici).
- [x] Étape 6 : PV 5, ATK 1, SCH 1, boost 2.
- [x] Étape 7 : 2 cas (nominal : Hard as Marble prise, Gatling Gun et Hardheaded laissées ; contre-cas : rien). Le contre-cas était ROUGE avec le script d'origine (Gatling Gun attaché). Subst : passe finale du coordinateur.
- [x] 7 bis NON · 8 commune (attaque 3× avec ses boosts) · 8 bis OUI (attachement sur un sbire), couvert.
- Carte terminée : OUI (passe 1, relecture du texte)

**Passe 2 (18/09/2026, après le correctif du coordinateur `ability.attach_selector`)** :
- [x] Étape 2 : `PeutSAccrocherAUnSbire` interroge désormais la VRAIE règle : l'ability `func_name="AttachToWhenEnterPlay"` de l'attachement (`face.ability.Find(func_name=...)`), puis `attach_selector.selector_filter.CheckFinder(sbire, GameRule(face))` = le finder (Villain / Minion / Enemy, `non_trait`, `not_with_attach`) et ses conditions (`CanAttachTo`, donc aussi `CheckIfFaceCanAttachTo` et MaxPerUnit). ⚠ Pas `GetAllLegalTargets` : il applique `selector_rule.Process` (tri `highest_printed_hp` / `highest_atk`), et « peut s'accrocher à un sbire » dépendrait alors des AUTRES sbires en jeu. La relecture du texte « Attach to … » ne subsiste qu'en repli, si aucune ability n'expose de sélecteur (dit en commentaire).
- [x] Étape 5 : les deux limites assumées de la passe 1 tombent : « without a VEHICLE attachment » et `non-[[Aerial]]` sont désormais lus par le finder lui-même.
- [x] Étape 7 : `[fne3b]` rejoué : 66/66 ; nominal (Hard as Marble prise, Gatling Gun et Hardheaded laissées) et contre-cas (« seul un attachement reserve au vilain » : rien) tous deux verts. ⚠ Première relance ROUGE sur le nominal : `NameError: name 'GameRule' is not defined` (`cards.pack` ne le ré-exporte pas ; import local `from game.effect.rule import GameRule`), exception avalée par le `any(...)` donc « aucun candidat » ; vu au journal `/tmp/capacites_xb2062.log`, pas au verdict.
- [x] Étape 8 : 2 parties Spider-Man vs `art_museum_heist_hammerhead --modulaires tombstone` (graines 1-2) : 0 V / 2 D, 0 bloquée, 4,5 rounds, 0 traceback, 0 erreur (grep des 2 journaux) ; Cold as Ice révélée, Beetle non tiré.
- Carte terminée : OUI

##### 60198 : * Tombstone
- [x] Étape 2 : `WhenCardBecomeBoost("This")` + `GiveStatus([Worlds.FindVillain()], "Tough")` (60106) ; Quickstrike = base.
- [x] Étape 5 : « Give **the villain** a tough status card » (pas l'ennemi actif) ; ★ Boost seul, boost 0 icône.
- [x] Étape 6 : PV 8, ATK 2, SCH 2, boost 0 (1 + 0 = 1 dégât mesuré).
- [x] Étape 7 : 2 cas (Boost ; Quickstrike natif : 2 dégâts à l'entrée en forme héros). Subst : passe finale du coordinateur.
- [x] 7 bis NON · 8 commune · 8 bis NON (statut générique).
- Carte terminée : OUI

##### 60199 : Hit List
- [x] Étape 2 : `AfterPhaseBegin(ForcedResponse, "Villain")` (turn_phase.py:189, `Puzzle.BeginVillainPhase()` pour le harnais) + `identite.TakeIndirectDamage(this, 3)` + `RemoveThreatFromSchemes([this], GetPlayerNumIcon × n)`.
- [x] Étape 5 : « After the villain phase **begins** » ; « 3 **indirect** damage to the **first player** » → `GetFirstPlayer`, le joueur répartit ; « For **each ally defeated this way** » → ⚠ `operation=` n'est pas rappelée pour une unité vaincue (`can_health.py:288`) : comparaison des alliés en jeu avant / après ; « 1[per_hero] threat ».
- [x] Étape 6 : 3[per_hero] (3 mesurés), 3 dégâts, 1[per_hero] par allié.
- [x] Étape 7 : 2 cas (sans allié : menace 3, identité 3 ; Spider-Woman vaincue : menace 2, identité 1). Subst : passe finale du coordinateur.
- [x] 7 bis NON · 8 commune (vu comme boost) · 8 bis NON.
- Carte terminée : OUI

##### 60200 : * Ivan Banionis
- [x] Étape 2 : `this.PlaceAccelerationToken(1)` (50081) dans `WhenThisRevealed` et `AfterUnitSchemeEnd(ForcedResponse, "This")` ; Teamwork = base (`desc.Teamwork: TRACKSUIT`).
- [x] Étape 5 : « Place 1 acceleration **token** here » → jeton `acceleration_token` sur le sbire (lu par `scheme_main.py:116`) ; « After Ivan Banionis schemes » → part même à SCH 0 (mesuré : 2e jeton).
- [x] Étape 6 : SCH 0, ATK 2, PV 5, boost 2, 1 jeton par événement.
- [x] Étape 7 : 3 cas, dont le témoin Teamwork : Bro puis Ivan attaquent (2 + 2 = 4, journal lu) : le moteur applique par défaut la règle pré-1.6 (`v16_teamwork = False`, fiche `teamwork.md`), question §5.3. Subst : passe finale du coordinateur.
- [x] 7 bis NON · 8 commune (révélé 2×, jeton posé, glissé sous Tracksuit Mafia) · 8 bis OUI (jeton sur un sbire) : jauge de jetons générique ; NON prouvé à part.
- Carte terminée : OUI

##### 60201 : * The Clown
- [x] Étape 2 : `AfterUnitSchemeEnd(ForcedResponse, "This")` + `Faces.GiveFacedownBoostCards([this], 1)` (55007b) ; Teamwork, Villainous = bases.
- [x] Étape 5 : « give **him** 1 facedown boost card » → la carte reste dans SA pile jusqu'à sa prochaine activation (vérificateur `fne_boost_du_vilain`, `vilain: 60201`) et s'ajoute à celle de Villainous (1 + 3 + 3 = 7 mesurés).
- [x] Étape 6 : SCH 0, ATK 1, PV 6, boost 2.
- [x] Étape 7 : 2 cas. Subst : passe finale du coordinateur.
- [x] 7 bis NON · 8 commune · 8 bis OUI (pile de boost d'un sbire) : dessinée par la pile générique (60094 bloc 1) ; couvert.
- Carte terminée : OUI

##### 60202 : * Tracksuit Mafioso
- [x] Étape 2 : `WhenUnitBeDefeated(WhenDefeated, "This")` + `TrouverTracksuitMafia` (FindCardOnField name) + `TuckCardUnderHere` (50081) ; sinon `message.killer` + `GiveStatus` Stunned et Confused ; Retaliate 2, Teamwork, Vulnerable = bases.
- [x] Étape 5 : « **Tuck** this card under the Tracksuit Mafia side scheme » → face cachée dessous (`pose_sous`) ; « **Otherwise** » → seulement sans le complot ; « the **character** that defeated » → `killer` (héros ou allié), rien si `Puzzle.Damage` (limite) ; ⚠ Retaliate ne mord pas quand le défenseur est vaincu par l'attaque (« ignore Retaliate » au journal) : 0 dégât au héros.
- [x] Étape 6 : PV 7, ATK 0, SCH 3, Retaliate 2, boost 3.
- [x] Étape 7 : 3 cas. Subst : passe finale du coordinateur.
- [x] 7 bis NON · 8 commune (révélé 3×, Retaliate 2 appliqué en partie) · 8 bis OUI (carte glissée sous un complot annexe) : couvert par `ui-app/src/board/mere-de-la-nuit-cartes-dessous.test.ts` (même mécanisme : `bind_object_id` du complot dans `area_schemes_side`, face cachée).
- Carte terminée : OUI

##### 60203 : Tracksuit Bro
- [x] Étape 2 : même tronc ; sinon `Faces.ShuffleAllTo([this], "EncounterDeck")` (60069).
- [x] Étape 5 : « Otherwise, **shuffle** this card into the encounter deck » → `dans_deck_rencontre`, plus en jeu.
- [x] Étape 6 : PV 3, ATK 2, SCH 1, boost 2.
- [x] Étape 7 : 2 cas. Subst : passe finale du coordinateur.
- [x] 7 bis NON · 8 commune (révélé 2×) · 8 bis OUI, couvert (idem 60202).
- Carte terminée : OUI

##### 60204 : Tracksuit Mafia
- [x] Étape 2 : `Worlds.DiscardEncounterCardsUntil(trait="TRACKSUIT", card_type=Minion)` + `TuckCardUnderHere` (60184, 50081) ; `WhenCardRevealed(ForcedResponse, CardFinder(trait="TRACKSUIT", card_type=Minion), op, conditions=[…])` (reveal.py:92) + `GetPlacedCardArea()` + `Reveal` du sbire posé ; drapeau `en_cours` contre la récursion (le sbire sorti de dessous est lui aussi « révélé »).
- [x] Étape 5 : « until a TRACKSUIT minion is discarded and **tuck that minion here** » → le même objet ; « After **a player** reveals a TRACKSUIT minion **from the encounter deck** » → `Puzzle.Reveal` passe par le deck (`IsFromEncounterDeck` vrai) ; ⚠ la condition ne lit pas `IsFromEncounterDeck()` : un TRACKSUIT révélé depuis la défausse (Sway the Masses n'existe pas dans ces sets) déclencherait aussi, écart théorique noté ; « that player reveals **1** minion tucked here » → choix si plusieurs ; contre-cas non-TRACKSUIT.
- [x] Étape 6 : 3[per_hero] (3 mesurés), boost 2.
- [x] Étape 7 : 4 cas. Subst : passe finale du coordinateur.
- [x] 7 bis NON · 8 commune (révélé 1× : Ivan glissé dessous ; défaussé quand le complot part) · 8 bis OUI : couvert par `mere-de-la-nuit-cartes-dessous.test.ts`.
- Carte terminée : OUI

### 6. Questions pour l'utilisateur (hypothèse littérale implémentée)

1. **60180 Collapsing Bridge** (scan `scratchpad/scans/60180.jpg`) : quand la DERNIÈRE menace est retirée du pont, que se passe-t-il ?
   A) Le pont est vaincu, la Réponse Forcée ne résout pas (implémenté : un complot annexe est vaincu dès que sa dernière menace part, RRG « Defeated » ; sinon il ne peut jamais être vaincu par un contre).
   B) Le pont reçoit 1 menace et reste en jeu (le moteur faisait cela avant ma garde : il fallait retirer TOUTE la menace puis… c'était impossible).
   C) Autre (précise).
2. **Teamwork (60200-60203)** : le moteur applique par défaut la règle pré-1.6 (`v16_teamwork = False`) : quand Ivan entre avec Bro déjà en jeu, LES DEUX s'activent (4 dégâts mesurés). La règle RRG 1.6 n'active que le nouveau venu. Quelle règle veux-tu pour tout le jeu ? (réglage moteur, hors de mon périmètre)
   A) Garder la règle par défaut du moteur (tous s'activent).
   B) Passer `v16_teamwork = True` (seul l'entrant s'active).
   C) Autre (précise).

### 7. Ce que ces gates ne voient pas

- `src/cards/pack/fne/tombstone/__init__.py` (helper `PeutSAccrocherAUnSbire`, passe 2 : `attach_selector` + import local de `GameRule`), `tombstone/60197.py`, `tombstone/60199.py`, `disasters/60180.py`.
- `tools/test_capacites.py` : bloc 3B (66 cas) et section `# ---- pack fne (bloc 3B)`, uniquement par le générateur sous `flock`.
- Générateur de cas : `gen_cas_fne_b.py` (copié dans `.planning/todos/generateurs-fne/`).
- Rien sous `src/game/`, ni `data/`, ni `fne/__init__.py`, ni git.

Ce que ces gates ne voient pas : aucune partie humaine dans le navigateur ; Traffic Jam et Carjacking jamais révélés en autoplay (8 parties courtes) ; le plateau n'a pas été relancé sur un état contenant un véhicule sur l'identité (couvert par analogie avec les œuvres d'Art Museum Heist, même zone).

## Bloc 3P — Protection Racket (18/09/2026, coordinateur)

### 1. Inventaire → card_id (13 cartes, 1 set)

- **Protection Racket** (`protection_racket.json`, `protection_racket_<vilain>[_expert].json`) :
  60134a-60138a Protection Racket 1A (cinq copies, face commune) ; 60134b Battle
  in the Bodega, 60135b Bull in a China Shop, 60136b Hung Out to Dry, 60137b Pawn
  Shop Showdown, 60138b A Slice of the Pizza Dough (1B, un commerce par joueur) ;
  60139 Shop Proprietor ; 60140 Man-Bull ; 60141 Change of Venue.
- Règle du livret (p. 13) et article FFG : UN complot principal PAR JOUEUR, choisi
  (au hasard en expert), les autres mis de côté ; le vilain ne pose sa menace que
  sur le complot du joueur qu'il vise ; un joueur dont le complot est complété est
  éliminé ; tous complétés → partie perdue.

### 2. Fichiers écrits

- `src/cards/pack/fne/protection_racket/__init__.py` : `CLE="proprietaire_racket"`,
  `Proprietaire`, `ComplotsRacket`, `ComplotDuJoueur`, `DansCetteAire`,
  `MettreEnJeuLeComplot`, `EchangerLeComplot`, `CapacitesCommunes1B`
  (`GetMainScheme` par joueur, élimination, jetons d'accélération, défaite
  commune), `CapacitesDe1A` (choix par joueur au Setup, propriétaire posé à la
  révélation) ; 13 scripts.
- Moteur : `src/game/puzzle/puzzle.py` (`FindOrCreateFace` fouille les cartes
  mises de côté) ; `src/game/card/face/card_type/scheme_side.py` (Permanent),
  `environment.py` (`CanCrisis`), `treat.py` (mots-clés sauvegardés), voir bloc 2 §3.
- Harnais : 11 cas `[fne3p]` (générateur `.planning/todos/generateurs-fne/gen_cas_fne_p.py`) +
  vérificateur `fne3p_racket` (nb de complots en jeu / de côté, propriétaire,
  menace du complot du joueur).

### 4. Ce que le harnais a trouvé

`Puzzle.Reveal('60136a')` tombait sur `assert prev_scheme.card.back_faces`
(doublon fabriqué : la mise de côté n'était pas fouillée, correctif harnais) ;
`Worlds.GetSetAsideAreaCards` exige un `Effect` (shim dans le vérificateur) ;
`Faces.HealAll` n'existe pas (`face.HealHealth(1, effect)`).
**BILAN : 13/13 cas passes** (`[fne3p]`, port 41000 ; 11/11 avant l'autoplay, puis
deux cas ajoutés pour les deux défauts que l'autoplay a trouvés).

### 5. Gabarits PROCESSUS-CARTE (un par carte)

#### 60134a-60138a : Protection Racket 1A (face commune)
- [x] Étape 2 : `WhenCardSetup("This", op)` (choix du complot par joueur, `AskChooseFace` ; au hasard en expert via `Worlds.IsExpert`), `WhenThisRevealed` (propriétaire posé sur la CARTE, `setattr(this.card, CLE, player_id)`), mise de côté des autres (`SetupCards`, `MettreEnJeuLeComplot` = `Reveal`), capacités communes 1B.
- [x] Étape 5 : « each player chooses **a different** main scheme » → un complot par joueur, jamais deux fois le même ; « **at random** in expert » → `Worlds.IsExpert` ; « set the rest aside » → mise de côté (fouillée par `Change of Venue`).
- [x] Étape 6 : 5 copies déclarées dans le set, `Stage 1A` sans menace.
- [x] Étape 7 : `60134a … mise en place : le joueur choisit son complot (premiere option : Battle in the Bodega), les quatre autres restent de cote`, `60134a … (expert) — mise en place au hasard : un seul complot en jeu, quatre de cote`. Subst : passe finale.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 4 parties Spider-Man vs `protection_racket_hammerhead` et `_bullseye` (profil équilibré) : première passe 3 tracebacks (Man-Bull boost, vilain vaincu) corrigés puis rejouée : 0 traceback (voir « Fusion et gates de fin ») ; parties à deux joueurs non montées (cf. §7).
- [x] Étape 8 bis : NON (complot principal standard ; plusieurs complots principaux = précédent Tower Defense déjà dessiné).
- Carte terminée : OUI

#### 60134b : Battle in the Bodega (1B)
- [x] Étape 2 : `CapacitesCommunes1B` (`GetMainScheme` rend ce complot seulement pour SON joueur, `AfterGameSetup` ranger, élimination → `SetGameOver(False)` si tous complétés, miroir des jetons d'accélération), `AfterUnitAttackUnit(Enemy, "YouControlCharacter")` + `LimitOncePerPhase` (non expert).
- [x] Étape 5 : « After an enemy attacks a character **in this play area** » → `DansCetteAire` (contrôlé par le propriétaire du complot) ; « deal 1 damage to that enemy and place 1 threat here » → sur CE complot ; « **Limit once per phase** » (standard seulement) → `LimitOncePerPhase`, témoin d'épuisement.
- [x] Étape 6 : 1B, menace de départ 0, cible 7[per_hero]… ↔ `desc` ; accélération 1[per_hero].
- [x] Étape 7 : `60134b … le vilain manigance contre le joueur : la menace tombe sur SON complot (0 + 2)`, `60134b Battle in the Bodega … le vilain attaque le heros : 1 degat au vilain et 1 menace ; limite une fois par phase (seconde attaque : rien de plus)`. Subst : passe finale.
- [x] Étape 7 bis : OUI, témoin : la seconde attaque de la même phase ne rajoute ni dégât ni menace (cas ci-dessus, mesuré 1 / 1).
- [x] Étape 8 : autoplay 4 parties Spider-Man vs `protection_racket_hammerhead` et `_bullseye` (profil équilibré) : première passe 3 tracebacks (Man-Bull boost, vilain vaincu) corrigés puis rejouée : 0 traceback (voir « Fusion et gates de fin ») ; parties à deux joueurs non montées (cf. §7).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60135b : Bull in a China Shop (1B)
- [x] Étape 2 : `WhenUnitBeDefeated(Unit2)` + `message.excess_damage` (les dégâts excédentaires n'existent qu'à la défaite, RECETTES §7quater), `PlaceThreatOnSchemes` sur ce complot.
- [x] Étape 5 : « **excess** damage dealt to an ally in this play area » → uniquement quand l'allié est VAINCU, montant = dégâts − PV restants ; « place that much threat here ».
- [x] Étape 6 : idem 60134b.
- [x] Étape 7 : `60135b … degats excedentaires sur un allie de cette aire : autant de menace (5 sur 3 PV = 2)`, `60135b Bull in a China Shop [fne3p] — contre-cas : le VILAIN vaincu (stade I) n'est dans l'aire de personne : pas de menace, pas de plantage, stade II en jeu` (ajouté après l'autoplay : `GetControlByPlayer` posait un assert sur le vilain vaincu, partie bloquée). Subst : passe finale.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 4 parties Spider-Man vs `protection_racket_hammerhead` et `_bullseye` (profil équilibré) : première passe 3 tracebacks (Man-Bull boost, vilain vaincu) corrigés puis rejouée : 0 traceback (voir « Fusion et gates de fin ») ; parties à deux joueurs non montées (cf. §7).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60136b : Hung Out to Dry (1B)
- [x] Étape 2 : `AfterCardEnterPlay` (personnage entrant dans cette aire), `DealDamage` 1 + 1 menace ici.
- [x] Étape 5 : « After a **character** enters play in this play area » → héros, allié (pas une amélioration) contrôlé par le propriétaire.
- [x] Étape 7 : `60136b … un personnage entre en jeu dans cette aire : 1 degat et 1 menace`. Subst : passe finale.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 4 parties Spider-Man vs `protection_racket_hammerhead` et `_bullseye` (profil équilibré) : première passe 3 tracebacks (Man-Bull boost, vilain vaincu) corrigés puis rejouée : 0 traceback (voir « Fusion et gates de fin ») ; parties à deux joueurs non montées (cf. §7).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60137b : Pawn Shop Showdown (1B)
- [x] Étape 2 : `ReduceCostToPlayFaceWhen(Upgrade, 1, "AnyPlayer", conditions)` (rabais pour les améliorations jouées dans cette aire), `AfterCardEnterPlay(Upgrade)` → 1 menace ici.
- [x] Étape 5 : « upgrades cost 1 less to play in this play area » → rabais limité aux joueurs propriétaires ; « after an upgrade enters play here → 1 threat ».
- [x] Étape 7 : `60137b … une amelioration entre en jeu dans cette aire : 1 menace`. Subst : passe finale.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 4 parties Spider-Man vs `protection_racket_hammerhead` et `_bullseye` (profil équilibré) : première passe 3 tracebacks (Man-Bull boost, vilain vaincu) corrigés puis rejouée : 0 traceback (voir « Fusion et gates de fin ») ; parties à deux joueurs non montées (cf. §7).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60138b : A Slice of the Pizza Dough (1B)
- [x] Étape 2 : `AfterUnitDefeatedUnit` / `AfterUnitDefeatedScheme` + `face.HealHealth(1, effect)` (pas `Faces.HealAll`, inexistant), 1 menace ici.
- [x] Étape 5 : « After a hero in this play area defeats a minion » → le héros propriétaire ; « heal 1 damage from that hero and place 1 threat here ».
- [x] Étape 7 : `60138b … le heros vainc un sbire : il soigne 1 degat et 1 menace ici`. Subst : passe finale.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 4 parties Spider-Man vs `protection_racket_hammerhead` et `_bullseye` (profil équilibré) : première passe 3 tracebacks (Man-Bull boost, vilain vaincu) corrigés puis rejouée : 0 traceback (voir « Fusion et gates de fin ») ; parties à deux joueurs non montées (cf. §7).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60139 : Shop Proprietor
- [x] Étape 2 : allié de rencontre révélé sous contrôle (`PutIntoPlay(under_control=True)`), Surge, `WhenCardLeavePlay("This")` → 4 menaces sur le complot du joueur.
- [x] Étape 5 : « put into play under **your** control » → le joueur qui révèle ; « surge » ; « when Shop Proprietor **leaves play** » → défaite, défausse, retrait : tout départ ; « place 4 threat on **your** main scheme » → `ComplotDuJoueur`.
- [x] Étape 7 : `60139 … revele : entre en jeu sous ton controle et surge ; quand il quitte le jeu : 4 menaces sur ton complot`. Subst : passe finale.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 4 parties Spider-Man vs `protection_racket_hammerhead` et `_bullseye` (profil équilibré) : première passe 3 tracebacks (Man-Bull boost, vilain vaincu) corrigés puis rejouée : 0 traceback (voir « Fusion et gates de fin ») ; parties à deux joueurs non montées (cf. §7).
- [x] Étape 8 bis : NON (allié standard).
- Carte terminée : OUI

#### 60140 : Man-Bull
- [x] Étape 2 : boost via `ennemi.effect.RegisterTemp(AfterUnitAttackEnd(Temp0, …))` (dégâts non subis → menace), sbire standard sinon.
- [x] Étape 5 : « for each point of damage from this attack **not dealt** to the hero » → dégâts absorbés par un défenseur (allié, PV) comptés en menace sur le complot du joueur attaqué.
- [x] Étape 7 : `60140 … attaque defendue par Hellcat (3 PV) : 4 - 3 = 1 menace sur le complot`, `60140 Man-Bull [fne3p] (expert) — carte BOOST de l'attaque de Hammerhead II (ATK 2) sur Hellcat a 1 PV : 1 degat en exces = 1 menace sur le complot du joueur` (ajouté après l'autoplay du 18/09/2026 : `RegisterTemp` sans `unregister_after_exec` levait un TypeError avalé à chaque boost). Subst : passe finale.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 4 parties Spider-Man vs `protection_racket_hammerhead` et `_bullseye` (profil équilibré) : première passe 3 tracebacks (Man-Bull boost, vilain vaincu) corrigés puis rejouée : 0 traceback (voir « Fusion et gates de fin ») ; parties à deux joueurs non montées (cf. §7).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

#### 60141 : Change of Venue
- [x] Étape 2 : `EchangerLeComplot` (le complot du joueur repart de côté, un complot mis de côté au hasard entre en jeu avec la même menace, même propriétaire), Surge.
- [x] Étape 5 : « swap your main scheme with a **random** set-aside main scheme » → hasard ; « move all threat » → la menace suit ; « surge ».
- [x] Étape 7 : `60141 … le complot du joueur (4 menaces) est echange contre un complot mis de cote au hasard, qui recoit les 4 menaces ; surge`. Subst : passe finale.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : autoplay 4 parties Spider-Man vs `protection_racket_hammerhead` et `_bullseye` (profil équilibré) : première passe 3 tracebacks (Man-Bull boost, vilain vaincu) corrigés puis rejouée : 0 traceback (voir « Fusion et gates de fin ») ; parties à deux joueurs non montées (cf. §7).
- [x] Étape 8 bis : NON.
- Carte terminée : OUI

### 6. Questions pour l'utilisateur
Aucune : les règles du livret p. 13 et l'article FFG sur les complots par joueur ont été relus (voir la discussion du 18/09/2026).

### 7. Ce que ces gates ne voient pas
Aucune partie à DEUX joueurs sur Protection Racket hors les cas de campagne (`heros2`) ; aucune partie humaine.

## Bloc 4 — Kingpin (18/09/2026, agent C)

Écrit par un agent parallèle ; son rapport (bilan, gabarits, pièges,
questions) est RECOPIÉ ici, le brouillon de session ayant disparu avec le
répertoire temporaire. Pièges : RECETTES-MOTEUR §7quinquies à §7septies.
Substitution : passe finale du coordinateur, voir « Fusion et gates de fin ».

### 1. Bilan harnais

`BILAN : 70/70 cas passes` (filtre `[fne4]`, PARALLELES=4, port 43000, rapport
`/tmp/rapport-c.json`, journaux `/tmp/capacites_xc<index>.log`). Deux passes :
55/70 puis 70/70 (§3 pour ce que la première passe a trouvé). Gates statiques :
`verifier_appels_modules fne` : OK ; `verifier_noms_modules fne` : OK.
Autoplay : 4 parties Spider-Man (2 × `kingpin_fne`, 2 × `kingpin_fne_expert`,
profil équilibré, graines 1-2, 55 s) : 0 V / 4 D, 0 bloquée, 3,0 rounds, **0 Traceback,
0 NameError/AttributeError/TypeError/KeyError/AssertionError** (grep exhaustif des 4
journaux `/tmp/autoplay_spider_man_kingpin_fne*_normal_equilibre_*.log`). Lecture du
journal graine 1 : Vulture révélé au Setup, Public Support posé par 1B, Kingpin
« va attaquer » puis manigance, le pilote consomme le Hero Action du complot à chaque
round (révèle un sbire de plus) et meurt au round 3 sous Vulture + Tracksuit Bro +
Diamondback : pas un défaut, la partie est jouable.

Cas par carte (70) :
- 60159a (5) : mise en place ; pas de dégâts ; Webbed Up jouée puis défaussée ; manigance à la place de l'attaque ; (+ contre-cas Webbed Up sur la face 2).
- 60159b (5) : boost en plus à l'attaque ; contre-cas Vulture engagé ; boost en plus à la manigance ; Steady (base) ; contre-cas overkill standard.
- 60160a (1) expert : pas de dégâts + manigance (SCH 3). 60160b (1) expert : boost en plus + overkill (7 sur l'identité).
- 60161a (2) : Setup Spider-Man (Vulture révélé) ; Setup Echo (60061 Kingpin retiré, UNDERLING révélé).
- 60161b (3) : Hero Action (5 menaces, remélange, sbire révélé) ; contre-cas 4 menaces ; expert 4 menaces.
- 60163a (3) : +1 support à la défaite ; bascule à 4 compteurs (Kingpin A2, Endgame 2B, HIGH) ; contre-cas 3 compteurs.
- 60162a (4) : Vulture en jeu → UNDERLING ; Vulture en défausse → trouvé ; Vulture retiré → UNDERLING ; expert Organized Crime.
- 60162b (2) : Vulture gagne guard ; contre-cas au stade 1.
- 60163b (3) : Interrupt (carte boost remplacée, 2 dégâts) ; contre-cas sans compteur (5) ; Forced Response.
- 60164 (5) : A1 → surge ; A2 → attachée, attaque remplacée ; contre remplacé ; dernier grip → sortie ; alter-ego interdit.
- 60165 (4) : révélée (attache, +1 SCH, carte boost) ; Hero Action (Emergency) ; contre-cas sans THWART ; Boost.
- 60166 (5) : révélée (stun) ; attaque et blesse → stun + défausse ; contre-cas robuste ; Boost ; Boost déjà étourdi.
- 60167 (3) : A1 → surge ; A2 → attachée, dégâts posés, retaliate ; 8 dégâts → défaussée.
- 60168 (4) : révélée (confus) ; Hero Action (Swinging Web Kick) ; Boost ; Boost déjà confus.
- 60169 (2) : 4e menace → alliée ; contre-cas 3e menace.
- 60170 (2) : attaque (+1 dégât) ; Boost.
- 60171 (3) : renvoi des dégâts ; sans pion ; contre-cas hors attaque.
- 60172 (3) : +2/+2 ; dégât → pion ; sans pion.
- 60173 (3) : vaincue, nemesis hors jeu → révélée ; nemesis en jeu → +3 ; menace 2* + Hazard.
- 60174 (1) : +2 PV. 60175 (3) : révélée (4 → 3) ; réserve vide → surge ; Boost. 60176 (4) : Vulture s'active ; en défausse → trouvé ; retiré → UNDERLING ; Boost overkill.

### 5. Gabarits PROCESSUS-CARTE (un par carte)

Conventions : « cas » = nom dans `tools/test_capacites.py` (filtre `[fne4]`) ;
« subst : passe finale du coordinateur » (brief §3.4). Modèles de l'étape 2 lus
dans le dépôt avant d'écrire. Aucune carte du set ne porte de limite imprimée
(« Limit once per… ») : étape 7 bis = NON partout.

##### 60159a / 60160a : * Kingpin (A1 / B1)
- [x] Étape 2 : `sd022` (`*UnitCannotTakeDamage`, liste), `46003` Snow Clone (`*UnitCannotHaveUpgradeAttached`, liste), `51019` Invisibility Gear / `ag005` (`message.DoSchemeInstead` sur `WhenUnitWouldAttack`) ; Stalwart = base desc. Helper `CapacitesDeKingpin1`.
- [x] Étape 5 : « cannot be dealt damage » → prévention totale (10 dégâts → 0) ; « or have upgrades attached » → CardFinder(name=Kingpin, **Villain**) pour ne pas viser le SBIRE Kingpin d'Echo ; « When Kingpin would attack **you**, he schemes **instead** » → SetBeInstead + DoSchemes contre le même joueur (menace 2 = SCH 2 + 0 icône, 0 dégât). Mots-pièges : « instead » (remplacement, pas duplication) ; « you ».
- [x] Étape 6 : SCH 2/3, ATK 0 (★), PV 25/28[per_hero], Stalwart 1 ↔ desc ; aucun nombre dans le script.
- [x] Étape 7 : `60159a … ne peut pas subir de degats : 10 degats -> 0`, `60159a … Webbed Up ne peut pas s'attacher a lui : jouee, elle est defaussee sans s'attacher` (contre-cas `60159b … Webbed Up s'attache a la face 2`), `60159a … quand il attaquerait, il manigance a la place (0 degat, 2 menaces)`, `60160a … (expert) — pas de degats, et il manigance … (SCH 3)`. Subst : passe finale du coordinateur.
      ⚠ Écart moteur constaté (demande D1) : `UnitCannotHaveUpgradeAttached` laisse CHOISIR Kingpin comme cible, l'amélioration est payée puis défaussée à l'attache (journal 2084 : « Webbed Up placée sur la table » puis « défaussée ») ; le joueur perd la carte. La moitié « CheckIfFaceCanAttachTo » de la fabrique n'est jamais envoyée par le moteur.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : autoplay §1 (4 parties, 0 traceback) ; journal lu : « Kingpin va attaquer » → « WhenUnitWouldAttack est remplacé » → manigance, à chaque round.
- [x] Étape 8 bis : NON (vilain recto-verso : le retournement est dessiné par la jauge générique, comme Typhoid Mary).
- Carte terminée : OUI (avec l'écart D1 signalé).

##### 60159b / 60160b : * Kingpin (A2 / B2)
- [x] Étape 2 : `60093` Maggia Underboss (`WhenUnitWouldAttack` + `WhenUnitWouldScheme`, `GiveAdditionalBoostCardForThisActivation`, condition dans `conditions`), `an013` (`GainOverKill`) ; Steady = base desc. Helper `CapacitesDeKingpin2(overkill)`.
- [x] Étape 5 : « activates against **you** » → `GetAgainstPlayer()` ; « if you are **not engaged with a minion** » → `engaged_minions.GetSize() == 0` (contre-cas Vulture engagé : 5 au lieu de 8) ; « for this activation » (pas permanent) ; B2 « gains overkill **if it is an attack** » → seulement dans le handler d'attaque.
- [x] Étape 6 : SCH 2/3, ATK 2/3, PV 25/28[per_hero], Steady 1, +1 carte.
- [x] Étape 7 : `60159b … attaque sans sbire engage : 1 carte boost de plus (2 + 3 + 3 = 8)`, `… contre-cas : Vulture engage … (2 + 3 = 5)`, `… manigance sans sbire engage … (8 menaces)`, `… Steady (base desc) : une seule carte stun ne l'empeche pas d'attaquer`, `60160b … (expert) — … carte de plus ET overkill (… 7 passent)`, contre-cas `60159b … contre-cas overkill : en standard, l'exces … est perdu`. Subst : passe finale du coordinateur (les deux contre-cas d'absence resteront verts).
- [x] Étape 7 bis : NON. · Étape 8 : §1. · Étape 8 bis : NON.
- Carte terminée : OUI

##### 60161a / 60161b : The King's Gambit (1A / 1B)
- [x] Étape 2 : 1A `60121a` (`WhenCardSetup("This")`), `01190` (nemesis par joueur, `set_aside_nemesis_sets`, `IsNemesis`) ; 1B `56096b` (When Revealed d'une face 1B), `16073b` (Hero Action sur un complot principal + `IfThisSchemeStageIsCompletedPlayersLoseTheGame`), `60095` (`DiscardEncounterCardsUntil` + `Reveal`), `SetupCards.PutIntoPlay(name=…)` pour Public Support (mis de côté par le scénario).
- [x] Étape 5 : « **shares a title** with a character in play » → même `name` qu'une `Unit2` en jeu (Echo : le sbire Kingpin ↔ le vilain) ; « **instead** removes … then finds an UNDERLING … **not in play** » → `RemoveAllFromGame` puis `Find` filtré `not IsInPlay()` ; « LOW side faceup » → face 60163a, contrôle du joueur qui révèle ; « Remove 5 threat from here (**4 … in expert**) » → coût `CostFunc.Custom` + condition (valeur lue à l'exécution, `Worlds.IsExpert`) ; « Shuffle the discard pile into the deck, **then** discard … until a minion … reveal **that** minion » → même objet. Mots-pièges : « instead », « that minion », « unless/if » (expert).
- [x] Étape 6 : 3[per_hero] départ / 11[per_hero] cible / +1[per_hero] ↔ desc (scan 60161b relu) ; 5 / 4 ↔ `seuil()`.
- [x] Étape 7 : `60161a … Setup : le sbire nemesis (Vulture) est revele ; 1B et Public Support LOW sont en jeu`, `60161a … Setup avec Echo : … retire du jeu et un UNDERLING revele a la place` (heros=echo, `fne4_sbires_en_jeu` : retirees [60061]), `60161b … Hero Action : 5 menaces retirees, la defausse remelangee, un sbire defausse et revele`, `… contre-cas : 4 menaces seulement, l'action n'est pas offerte`, `… (expert) — 4 menaces suffisent (4 -> 0)`. Subst : passe finale du coordinateur. ⚠ Le Setup et le When Revealed de 1B jouent PENDANT la mise en place (avant le harnais) : ils sont prouvés par l'état de départ (cas 1), pas par un déclencheur.
- [x] Étape 7 bis : NON. · Étape 8 : §1 (le pilote utilise l'action chaque round : « Remove_threat_from_here… » dans le journal). · Étape 8 bis : NON (complot + environnement posé : jauges génériques ; Public Support est un environnement ordinaire, dessiné comme Disturbed Psyche).
- Carte terminée : OUI

##### 60162a / 60162b : Endgame (2A / 2B)
- [x] Étape 2 : `01190` (nemesis), `Find.FindAndReveal(if_no_entered_play)` (find.py:52), `60097` Purple Man (`GiveKeywordToInPlayWhenApplyThis(Minion, guard=1)`), `IfThisSchemeStageIsCompletedPlayersLoseTheGame`.
- [x] Étape 5 : « finds their nemesis minion and reveals it » → Find (deck, défausse, réserve nemesis ; JAMAIS la zone retirée) ; « whose nemesis minion **did not enter play this way** » → deux chemins : trouvé mais déjà en jeu (`if_no_entered_play`) OU introuvable (retiré du jeu) → UNDERLING ; « In expert mode, the **first player** finds and reveals Organized Crime » → `Worlds.GetFirstPlayer` ; « Each minion gains guard ».
- [x] Étape 6 : 0[per_hero] / 7[per_hero] / +1[per_hero] ↔ desc.
- [x] Étape 7 : `60162a … Vulture deja en jeu n'entre pas en jeu « this way », un UNDERLING est trouve et revele`, `… Vulture en defausse est trouve et revele (aucun UNDERLING)`, `… Vulture retire du jeu, un UNDERLING est revele a la place`, `… (expert) — le premier joueur trouve et revele Organized Crime`, `60162b … chaque sbire gagne guard (Vulture)`, contre-cas `… au stade 1, Vulture n'a pas guard`. Le stade 2 est atteint par le VRAI chemin (Public Support, 4 compteurs, `Puzzle.BeginVillainPhase`). Subst : passe finale du coordinateur.
- [x] Étape 7 bis : NON. · Étape 8 : §1 (aucune partie n'atteint le stade 2 en 3 rounds : le chemin est prouvé par les 6 cas ci-dessus). · Étape 8 bis : NON.
- Carte terminée : OUI

##### 60163a / 60163b : Public Support (LOW / HIGH)
- [x] Étape 2 : `60094` (`AfterUnitBeDefeated(ForcedResponse, Minion)`), `nt011` / `WhenVillainPhaseBegin` (le harnais a `Puzzle.BeginVillainPhase`), `60112` (`card.Flip` du vilain), `MainScheme.Advance("2A")` (scheme_main.py:175 → `world.AdvanceMainScheme`), `60068a/b` (retournement d'une carte non attachée : `card.Flip`, les compteurs restent). HIGH : `WhenEnemyActivateAgainstYou(Interrupt)` + `property.additional_boost_card` / `give_additional_boost` (can_attack.py:265, can_scheme.py:114).
- [x] Étape 5 : « at least 2[per_hero]+2 » → `2 × GetPlayerNumIcon + 2` (4 en solo ; contre-cas 3) ; « flip Kingpin **and** advance the main scheme to stage 2A. **Then**, flip this card » → ordre respecté (journal 2098 : Kingpin retourné → « The King's Gambit progresse » → Endgame révélé → Public Support retourné) ; HIGH « When an enemy would be given a facedown boost card, remove 1[per_hero] support counters … **instead** » → remplacement de la carte boost de l'activation (condition : au moins 1[per_hero] compteur ET une carte à donner). ⚠ Écart assumé (demande D2) : le moteur n'a aucun message « would be given a boost card » ; l'Interrupt n'intercepte que la carte de l'ACTIVATION, pas celles données hors activation (James Wesley, Bag of Tricks), ni une seconde carte de la même activation.
- [x] Étape 6 : 2[per_hero]+2 ; 1[per_hero] ; +1 compteur.
- [x] Étape 7 : LOW `60163a … apres la defaite d'un sbire : 1 compteur support`, `… 4 compteurs (2x1+2) au debut de la phase du mechant : Kingpin retourne (A2), complot au stade 2 (Endgame 2B), carte retournee (HIGH)`, `… contre-cas : 3 compteurs, rien ne bouge` ; HIGH `60163b … Interrupt : 1 compteur retire a la place de la carte boost de Kingpin (2 + 0 = 2)`, `… contre-cas sans compteur : la carte boost est donnee (2 + 3 = 5)`, `… Forced Response : sbire vaincu, +1 compteur`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : NON. · Étape 8 : §1 (« Public Support s'active » à chaque sbire vaincu dans les journaux). · Étape 8 bis : OUI (compteurs + carte recto-verso hors attache) ; couvert par les jauges génériques (compteurs sur environnement, comme Disturbed Psyche 60112 ; retournement comme 60110a/b) : aucun cas plateau ajouté, à confirmer par le coordinateur au moment du rendu.
- Carte terminée : OUI (écart D2 signalé)

##### 60164 : Bear Hug
- [x] Étape 2 : `60080` (attachement de rencontre sur l'identité), `AttachToFaceWhenPutIntoPlayInternal` (asset.py:153) avec `Select.From("YourHero")` filtré par `check_effect_fn` (la condition sur le SÉLECTEUR, pour que le « cannot » déclenche le surge via `if_cannot_operation`), `60150` Imprisoned (`PlayersCannotChangeForms(to_form=AlterEgo)`), `60182` Cop (`SetBeInstead`) transposé à `WhenUnitWouldAttack("You")` / `WhenUnitWouldThwart("You")` ; Uses (3 grip) = base desc (sortie native).
- [x] Étape 5 : « If Kingpin has the MARTIAL ARTIST trait, attach to **your** hero. **Otherwise**, surge » → deux branches mesurées ; « You cannot change to alter-ego form » ; « When **you** would thwart or attack, remove 1 grip counter … **instead** » → l'action est annulée (Vulture indemne, menace intacte), le coût d'inclinaison reste payé (modèle uniforme du moteur, RECETTES §6). « you » = l'identité : un allié attaque normalement ; un ÉVÉNEMENT d'attaque du héros est aussi remplacé (non mesuré : le harnais n'a exercé que les pouvoirs de base).
- [x] Étape 6 : 3 grip ↔ `Uses "3,grip"` ; 1 par remplacement ; boost 2.
- [x] Étape 7 : `60164 … Kingpin A1 (pas MARTIAL ARTIST) : surge, la carte ne s'attache pas`, `… Kingpin A2 : attachee au heros avec 3 grip ; une attaque du heros retire 1 grip a la place (Vulture indemne)`, `… un contre du heros retire 1 grip a la place (menace intacte)`, `… le dernier grip retire : la carte quitte le jeu (Uses)`, `… impossible de passer en alter-ego`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : NON. · Étape 8 : §1. · Étape 8 bis : OUI (attachement sur le héros + compteurs) ; couvert par `fne-oeuvre-volee.test.ts` (attachement de rencontre dessiné sur le héros) et la jauge de compteurs.
- Carte terminée : OUI

##### 60165 : * James Wesley
- [x] Étape 2 : `60117` (`AttachToFaceWhenPutIntoPlay(Villain)`), `56091`/`60094` (carte boost hors activation : `GiveFacedownBoostCardsInternal(1, effect, None)`), `45014` (`CostFunc.Discard("YourHandCards", trait, Event)`), `21170` Loki's Staff (`WhenThisBoostAttachTo`). Helper `CapacitesDUnePersona`.
- [x] Étape 5 : « Attach to Kingpin **and** give him a facedown boost card » → les deux à la révélation ; « Discard a THWART event from your hand **→** discard James Wesley. Kingpin schemes » → coût (défausse d'Emergency), puis défausse de Wesley AVANT la manigance (SCH 2, sans le +1) ; « [star] Boost: Attach this card to Kingpin » → la carte quitte la zone de boost, pas défaussée.
- [x] Étape 6 : +1 SCH ↔ `SCH+`, 1 carte boost, boost ★ seule (0).
- [x] Étape 7 : `60165 … revele : attache a Kingpin (+1 SCH) et une carte boost face cachee lui est donnee` (`fne4_wesley_revele` : pile de boost = [01186]), `… Hero Action : Emergency (THWART) defaussee -> Wesley defausse, Kingpin manigance (2 menaces)`, `… contre-cas : sans evenement THWART en main, l'action n'est pas offerte`, `… Boost : apres l'activation, attache a Kingpin`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : NON. · Étape 8 : §1. · Étape 8 bis : attachement sur le vilain, couvert (générique, `area_villain`).
- Carte terminée : OUI

##### 60166 : * Kingpin's Cane
- [x] Étape 2 : `ReponseForceeCoupDeBoule` (60086 : `AfterUnitAttackAndDamageUnit(…, target_in_play=True)`), retour de `Faces.GiveStatus` (19001a : compte les unités servies), `08029` (`identity.TakeDamage(this, 1, effect)`).
- [x] Étape 5 : « After Kingpin attacks **and damages** a hero » (≠ attacks : contre-cas Tough → rien) ; « stun that hero. **If a hero is stunned this way**, discard this card » → `GiveStatus > 0` (un héros Stalwart refuserait et la canne resterait) ; Boost « If you were **already** stunned, take 1 damage » → statut lu AVANT la pose.
- [x] Étape 6 : +1 ATK ↔ `ATK+`, 1 dégât, boost ★+1.
- [x] Étape 7 : `60166 … revele : attache a Kingpin (+1 ATK), tu es etourdi`, `… Kingpin A2 attaque et blesse le heros (2 + 1 = 3) : heros etourdi, canne defaussee`, `… contre-cas : heros robuste, 0 degat, pas d'etourdissement, la canne reste`, `… Boost : tu es etourdi (2 + 1 icone = 3 degats)`, `… Boost, deja etourdi : 1 degat de plus (3 + 1 = 4)`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : NON. · Étape 8 : §1. · Étape 8 bis : attachement + statut, couvert.
- Carte terminée : OUI

##### 60167 : Mountain of Muscle
- [x] Étape 2 : `CapacitesDUnVehicule` (drive : `AttachToFaceWhenPutIntoPlay(…, if_cannot_gain_surge=True)` + `WhenUnitWouldTakeDamage` `PreventDamage("All")` + compteurs `damage`), `03009` (`*GiveKeywordToAttached(…, retaliate=1)`, rend une LISTE).
- [x] Étape 5 : « If Kingpin has the MARTIAL ARTIST trait, attach to Kingpin. **Otherwise**, surge » → `CardFinder(name, Villain, trait)` ; « Kingpin gains retaliate 1 » (1 dégât au héros qui l'attaque) ; « When Kingpin would take **any amount** of damage, place it here **instead**. **Then**, if there is **8 or more** damage here, discard » → total posé, seuil testé après la pose.
- [x] Étape 6 : retaliate 1, seuil 8, boost 2.
- [x] Étape 7 : `60167 … Kingpin A1 : surge, pas d'attache`, `… Kingpin A2 : attachee, 3 degats poses dessus a la place, retaliate 1 sur l'attaque du heros` (compteurs 5, identité 1), `… 8 degats accumules : defaussee, Kingpin indemne`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : NON. · Étape 8 : §1. · Étape 8 bis : attachement + compteurs sur attachement (60068a même dessin), couvert.
- Carte terminée : OUI

##### 60168 : * Vanessa Fisk
- [x] Étape 2 : `CapacitesDUnePersona` (voir 60165), `60118` (`DoAttackYou`), `PlaceThreatOnSchemes("MainScheme", 1)`.
- [x] Étape 5 : « Attach to Kingpin. You are confused » ; « Discard an ATTACK event → discard Vanessa Fisk. Kingpin attacks **you** » (A2, héros incliné : 2 dégâts) ; Boost « If you were **already** confused, place 1 threat on the main scheme » → lu avant.
- [x] Étape 6 : +1 SCH, 1 menace, boost ★ seule.
- [x] Étape 7 : `60168 … revele : attache a Kingpin (+1 SCH), tu es desoriente`, `… Hero Action : Swinging Web Kick (ATTACK) defausse -> Vanessa defaussee, Kingpin A2 attaque (2 degats)`, `… Boost : tu es desoriente (pas de menace en plus)`, `… Boost, deja desoriente : 1 menace sur le complot principal`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : NON. · Étape 8 : §1. · Étape 8 bis : couvert (attachement, statut).
- Carte terminée : OUI

##### 60169 : * Black Cat
- [x] Étape 2 : `60145` Baron Zemo / harnais clé `jetons` (la menace sur un sbire est un JETON 'threat'), `Faces.TreatAsAlly` (faces.py:340, fiche `registered.md` : recopie nom, image, ATK, SCH→THW), gabarit `karma_controlled_ally` (ATK 0** / THW 0** = 2 dégâts consécutifs), `60079` (Hero Action à coût coloré sur une carte de rencontre).
- [x] Étape 5 : « Spend a [mental] resource → place 1 threat here. **If there is 4 threat here**, take control of Black Cat as an ally » → conversion dans l'action (seule source de menace « here ») ; « treat … as an ally that takes **2** consequential damage after she attacks **or** thwarts » → les deux étoiles du gabarit (mesuré 2/2). ⚠ Écarts assumés (demande D3 + question Q3) : le gabarit porte le trait CONTROLLED au lieu de THIEF UNDERLING ; Villainous n'existe pas pour un allié (FAQ du livret : elle le garde) ; « While there is 4 threat here » n'est pas relu en continu (rien ne retire cette menace).
- [x] Étape 6 : 4 menaces, 1 par action, 2 consécutifs, [mental].
- [x] Étape 7 : `60169 … Hero Action [mental] : 4e menace, elle passe sous ton controle comme alliee (1/1, 2 degats consecutifs)` (`fne4_black_cat_alliee`), `… contre-cas : 3e menace seulement, elle reste un sbire`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : NON. · Étape 8 : §1 (le pilote a joué l'action, journal graine 1 : « Spend_a_mental_resource… »). · Étape 8 bis : OUI (sbire → allié, changement de zone) ; même mécanisme dessiné que les alliés REGISTERED d'Iron Patriot (`pic_id` recopié) : pas de cas plateau ajouté, à confirmer par le coordinateur.
- Carte terminée : OUI (écarts D3/Q3 signalés)

##### 60170 : * Diamondback
- [x] Étape 2 : `60144` (« When X attacks you » = `WhenUnitWouldAttack("This")`), `08029` (`TakeDamage(this, 1)`), `27080` (dégât en boost, joueur = `GetToPlayer()`).
- [x] Étape 5 : « When Diamondback attacks **you**, take 1 damage » → `GetAgainstPlayer().GetIdentity()` ; Villainous = base (1 carte boost, Advance 0 icône) ; Boost « Take 1 damage ».
- [x] Étape 6 : 1 et 1 ; boost ★+2.
- [x] Étape 7 : `60170 … quand il t'attaque : 1 degat, puis l'attaque (1 + 1 + 0 = 2)`, `… Boost : 1 degat (2 + 2 icones + 1 = 5)`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : NON. · Étape 8 : §1 (journal graine 1 : « 1 dégât de Diamondback »). · Étape 8 bis : NON.
- Carte terminée : OUI

##### 60171 : * Spot
- [x] Étape 2 : `sr015` Mysterio (`ThisEnterPlayWithCounters`, `WhenUnitWouldTakeDamage("This")` + `PreventDamage("All")`), l'attaquant = `message.would_atk_message.attacker`, `is_from_attack=True`.
- [x] Étape 5 : « would be dealt damage **from an attack** » (contre-cas `Puzzle.Damage` : passe) ; « if there is at least 1 spot counter … remove 1 … and deal **that** damage to the attacker **instead** » → même montant (2), Spot indemne ; « **Otherwise**, place 1 spot counter here » (il prend les dégâts ET gagne un pion).
- [x] Étape 6 : 1 pion à l'entrée, 1 retiré / 1 posé.
- [x] Étape 7 : `60171 … entre avec 1 spot ; attaque du heros : le pion est retire et les 2 degats renvoyes a l'attaquant`, `… sans pion : il subit les 2 degats et gagne 1 spot`, `… contre-cas : des degats hors attaque ne sont pas renvoyes`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : NON. · Étape 8 : §1. · Étape 8 bis : compteurs sur sbire (générique), couvert.
- Carte terminée : OUI

##### 60172 : * Stilt-Man
- [x] Étape 2 : `sr015` (pions à l'entrée, dégâts remplacés tant qu'il reste un pion), `dt133` (`ThisGainKeyword` dynamique, rafraîchi par `OnEvent.Counter("This", 'stilt')`).
- [x] Étape 5 : « gets +1 SCH and +1 ATK **for each** stilt counter » → `check_fn = GetCounters('stilt')` (2 → +2/+2, 1 → +1/+1, 0 → +0) ; « When Stilt-Man would take **any amount** of damage, remove 1 stilt counter … **instead** » → prévention totale tant qu'il a un pion ; sans pion le remplacement est impossible et les dégâts passent (lecture littérale, même choix que Mysterio sr015).
- [x] Étape 6 : 2 pions, +1/+1 par pion.
- [x] Étape 7 : `60172 … entre avec 2 stilt : +2 SCH et +2 ATK`, `… 3 degats : 1 stilt retire a la place, +1/+1 seulement`, `… sans stilt : les 3 degats passent`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : NON. · Étape 8 : §1. · Étape 8 bis : compteurs, couvert.
- Carte terminée : OUI

##### 60173 : Kingpin's Influence
- [x] Étape 2 : `60113a` (`WhenSchemeBeDefeated(WhenDefeated, "This")`), `message.GetDefeatingPlayer()` (sender_scheme.py:210), `CardFinder(card_type=EncounterSideScheme, is_nemesis=joueur)` (checker.py:304, marqueur `nemesis_of_player`), `Find.FindAndReveal` (fouille la réserve nemesis) ; Hazard = base desc (scan relu : carte inclinée avec « + », RECETTES §8).
- [x] Étape 5 : « **The player who defeated** this scheme » → `GetDefeatingPlayer` ; « places 3 threat on **their** nemesis side scheme. **If it is not in play**, they find it and reveal it » → en jeu : +3 ; hors jeu : trouvée et révélée (menace de départ 3*), SANS les 3 (lecture littérale, question Q1).
- [x] Étape 6 : 3 menaces ; 2[per_hero] et Hazard 1 ↔ desc (mesurés).
- [x] Étape 7 : `60173 … vaincue : Highway Robbery (nemesis) hors jeu -> trouvee et revelee (3 menaces)`, `… vaincue, Highway Robbery deja en jeu : 3 menaces de plus (3 -> 6)`, `… en jeu : 2[per_hero] menaces et 1 icone Hazard`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : NON. · Étape 8 : §1. · Étape 8 bis : NON (menace, jauge générique).
- Carte terminée : OUI (question Q1 ouverte)

##### 60174 : Organized Crime
- [x] Étape 2 : `60097` (`*GiveKeywordToInPlayWhenApplyThis(CardFinder(Minion), health=2)`).
- [x] Étape 5 : « **Each** minion gets +2 hit points » → tous les sbires en jeu, y compris ceux qui entrent après (Diamondback posé après : 8 ; Vulture déjà là : 6).
- [x] Étape 6 : +2 ; 3[per_hero] ↔ desc (mesuré 3).
- [x] Étape 7 : `60174 … chaque sbire a +2 PV (Diamondback 8, Vulture 6)`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : NON. · Étape 8 : §1. · Étape 8 bis : NON.
- Carte terminée : OUI

##### 60175 : Bag of Tricks
- [x] Étape 2 : `01190` Shadow of the Past (`set_aside_nemesis_sets`), `Rand.RandomChoice` (60112), `CanBoost.GiveBoostCard` (60094 : la carte rejoint la pile de boost et la boucle de `ResolveBoostCards` la retourne dans la foulée, journal 2146 : Sweeping Swoop « s'active » comme boost).
- [x] Étape 5 : « Reveal a **random** card from your set-aside nemesis set » (4 → 3 après la mise en place, Vulture déjà révélé) ; « **If no card is revealed this way**, this card gains surge » (réserve vide → surge, témoin révélé) ; Boost « Give **this character** a random card … as an **additional** boost card » → `message.activating_enemy`, réserve 4 → 3, dégâts ≥ 2.
- [x] Étape 6 : 1 carte ; boost ★ seule.
- [x] Étape 7 : `60175 … revelee : une carte au hasard du set nemesis mis de cote est revelee (4 -> 3, Sweeping Swoop en defausse)`, `… set nemesis vide : surge` (`fne4_bag_sans_reserve` : le vérificateur vide la réserve puis révèle, voir §3), `… Boost : une carte du set nemesis donnee en boost supplementaire (4 -> 3, au moins 2 degats)`. Subst : passe finale du coordinateur. ⚠ Sous graine 42 la carte tirée est Sweeping Swoop (01168), qui porte Surge elle-même : aucun témoin « pas de surge » possible sur le cas nominal avec Spider-Man.
- [x] Étape 7 bis : NON. · Étape 8 : §1. · Étape 8 bis : NON.
- Carte terminée : OUI

##### 60176 : Unrelenting Hate
- [x] Étape 2 : `60074` (`DoActivate`), `Find.FindAndReveal` (deck, défausse, réserve ; jamais la zone retirée), `TrouverEtRevelerUnderling`, `an013` (`GainOverKill` en boost, `would_atk_message` lu avec `getattr`).
- [x] Étape 5 : « **Your** nemesis minion activates against you » (Vulture en jeu : 3 dégâts, héros incliné) ; « If … not in play, find it and reveal it » (défausse → trouvé, aucun UNDERLING) ; « **If you cannot find it**, find an UNDERLING minion **that is not in play** and reveal it » (retiré du jeu → UNDERLING) ; Boost « **If this activation is an attack**, it gains overkill » (manigance : rien).
- [x] Étape 6 : boost ★+1.
- [x] Étape 7 : `60176 … revelee : Vulture (en jeu) s'active contre toi (3 degats)`, `… Vulture en defausse : trouve et revele`, `… Vulture retire du jeu : un UNDERLING est trouve et revele`, `… Boost : l'attaque gagne overkill (2 + 1 = 3 sur Spider-Woman 2 PV : 1 passe)`. Subst : passe finale du coordinateur.
- [x] Étape 7 bis : NON. · Étape 8 : §1 (journal graine 1 : Unrelenting Hate → Vulture révélé → 3 dégâts). · Étape 8 bis : NON.
- Carte terminée : OUI

### 6. Questions pour l'utilisateur (hypothèse littérale implémentée)

**Q1, 60173 Kingpin's Influence** (scan `scratchpad/scans/60173.jpg`) : « places 3 threat on
their nemesis side scheme. If it is not in play, they find it and reveal it. » Quand le
complot nemesis n'est PAS en jeu :
- A) (implémenté, lecture littérale) on le trouve et on le révèle, avec sa menace de
  départ seulement (Highway Robbery : 3) ;
- B) on le révèle PUIS on y pose les 3 menaces (3 + 3 = 6) ;
- C) Autre (précise).

**Q2, 60163b Public Support HIGH** (scan `60163b.jpg`) : « When an enemy would be given a
facedown boost card, remove 1[per_hero] support counters from here instead. » Tant que le
moteur n'a pas la fenêtre D2, l'Interrupt ne remplace que la carte boost de l'ACTIVATION
(une par activation), pas celles données par James Wesley ou Bag of Tricks :
- A) acceptable en attendant D2 (recommandé) ;
- B) bloquer la carte jusqu'à D2 ;
- C) Autre (précise).

**Q3, 60169 Black Cat** (scan `60169.jpg`) : une fois alliée, la FAQ du livret dit qu'elle
GARDE Villainous (une carte boost à chaque attaque de base, comme un héros villainous).
Le moteur ne le sait pas pour un allié :
- A) écart accepté, elle attaque sans carte boost (implémenté) ;
- B) demander au coordinateur d'étendre `HasVillainous` aux alliés (moteur) ;
- C) Autre (précise).

### 7. Ce que ces gates ne voient pas

- Aucune partie humaine jouée dans le navigateur sur ce scénario ; le rendu du
  retournement de Public Support et de Black Cat convertie n'a pas de cas plateau propre.
- Bear Hug contre un ÉVÉNEMENT d'attaque/contre du héros (non exercé par le harnais).
- Les faces B en autoplay n'atteignent jamais le stade 2 (parties perdues au round 3).
- Preuve par substitution : passe finale du coordinateur (`substituer_pack.py` non lancé,
  brief §3.4). Empreinte md5 des 23 fichiers du set au moment du rapport :
  `md5sum src/cards/pack/fne/kingpin/*.py | md5sum` = `3cd6f556e7c3fe29e1572cc37acc5302`.

### 8. Passe 2 (après les correctifs moteur D1-D4) et D1 bis

#### Bilan

`BILAN : 71/72 cas passes` (filtre `[fne4]`, PARALLELES=4, port 43000, deux cas
ajoutés). Le seul rouge est VOLONTAIRE : `60159a Kingpin A1 [fne4] — Webbed Up ne peut
pas s'attacher a lui : aucune cible legale, la carte reste en main` (réécrit en
`en_main` comme demandé) reste rouge parce que le correctif D1 ne couvre pas le JEU
d'une amélioration (D1 bis ci-dessous) ; il mesure la vérité attendue, pas celle du
jour (règle « ne jamais retirer une assertion parce qu'elle échoue »).
Autoplay passe 2 : 2 parties Spider-Man vs `kingpin_fne` (graines 1-2) : 0 V / 2 D,
3,0 rounds, **0 Traceback, 0 erreur Python** ; journal graine 1 : la fenêtre de Public
Support HIGH joue (« Public Support s'active »). Gates statiques non rejouées (aucun
nouvel appel d'API hors la fabrique livrée par le coordinateur).

#### Ce qui a changé

- `60163b.py` réécrit sur `AbilityFactory.WhenEnemyWouldBeGivenBoostCards(Interrupt,
  Enemy, remplacer, conditions=[remplacable])` : `message.SetNum(message.num - 1)` +
  `RemoveCountersOn(1[per_hero] 'support')` ; condition `num > 0` et assez de compteurs.
  Vaut pour TOUTES les sources : nouveau cas `60163b … Interrupt sur la carte boost
  donnee par James Wesley (hors activation) : compteur retire, pile de boost vide`
  (`fne4_pile_boost_vide`, vert). Les deux cas d'activation (2 dégâts / 5) passent
  inchangés. Écart D2 LEVÉ, question Q2 retirée.
- `kingpin/__init__.py` : `GABARIT_ALLIE_BLACK_CAT = "fne_black_cat_ally"` ; `60169.py` :
  mention d'écart retirée. Nouveau cas `60169 … alliee, elle garde Villainous : son
  attaque recoit 1 carte boost (1 + 3 = 4 sur Diamondback)` (vert : `Puzzle.Attack('60169')`
  retrouve la face échangée par son ancien id, la carte boost Under Fire ajoute 3).
  Écart D3 LEVÉ, question Q3 retirée.
- Cas `60175 … set nemesis vide : surge` : repasse par quatre `Puzzle.Remove` (D4), le
  vérificateur `fne4_bag_sans_reserve` reste dans le harnais mais n'est plus appelé
  (à supprimer par le générateur si le coordinateur le souhaite).
- Cas `60159a … Webbed Up` : `en_main: ["01009"]`, rouge (voir D1 bis).

#### Gabarits mis à jour

- **60159a / 60160a** : étape 7, cas Webbed Up ROUGE : journal `/tmp/capacites_xc<index>.log`
  (passe 2) « Spider-Man s'apprête à jouer Webbed Up avec BBYY » → « WhenCardWouldAttachTo
  est remplacé par Kingpin » → « défaussée(s) » : Kingpin est encore OFFERT comme cible.
  Carte terminée : **NON**, bloquée sur D1 bis (le script est complet, c'est le moteur qui
  offre la cible) ; tout le reste de la face (dégâts, manigance à la place) est vert.
- **60163a / 60163b** : étape 2 : `WhenEnemyWouldBeGivenBoostCards` (activate.py, message
  sender_enemy.py:65, envoyé par can_boost.py avant `PopEncounterCards`) ; étape 5 : « When
  an enemy would be given a facedown boost card … instead » → UNE carte retirée du compte
  par fenêtre, pour toute source ; étape 7 : + le cas James Wesley. Écart levé. Carte
  terminée : OUI.
- **60169** : étape 2 : gabarit `fne_black_cat_ally` (pack "", Villainous 1, THIEF UNDERLING,
  0**/0**), `Ally` hérite de `HasVillainous` ; étape 5 : « treat Black Cat as an ally … »
  + FAQ (Villainous gardé) rendus ; étape 7 : + le cas d'attaque avec carte boost.
  Reste non relu en continu : « While there is 4 threat here » (aucune source ne retire
  cette menace). Carte terminée : OUI.
- **60175** : étape 7 : cas « réserve vide » par `Puzzle.Remove` (D4). Carte terminée : OUI.

#### D1 bis (moteur, `src/game/ability/factory/play.py:64`) : le jeu d'une amélioration ne consulte pas `CanAttachTo`

`grep -rn "\.CanAttachTo(" src/game` : trois appelants seulement, `attachment.py:88`
(`AttachToFaceWhenPutIntoPlay`, attachements RÉVÉLÉS) et `checker.py:282/286` (finders
`canbe_attach_by` / `canbe_attach_to`, posés uniquement par `SetTarget(...)` de cartes
précises). `CanPlayThisUpgradeCard(Enemy)` (play.py:80, Webbed Up 01009) construit
`Select.From(CardFinder(card_type=Enemy))` sans l'un ni l'autre : le message
`CheckIfFaceCanAttachTo` envoyé par `Asset2.CanAttachTo` n'est jamais atteint sur ce
chemin. Diff proposé, dans `CanPlayThisUpgradeCard` juste après la construction de
`selector` (les quatre branches) :
```python
        if selector is not None:
            from game.card.face.base import Asset2
            selector.selector_filter.AddParameter(
                check_effect_fn=lambda effect, face:
                    Asset2.IsType(effect.this) and effect.this.CastTo(Asset2).CanAttachTo(face))
```
(`AddParameter(check_effect_fn=…)` est exactement ce que fait `AttachToFaceWhenPutIntoPlay`,
attachment.py:141 ; `Upgrade.CanAttachTo` relit ensuite le sélecteur de la capacité Play,
upgrade.py:84, donc pas de récursion : il lit `selector_filter.CheckFinder(face, None)`
qui n'appelle pas `check_effect_fn`… à VÉRIFIER par le coordinateur avant de poser, une
boucle serait possible si `CheckFinder` évalue `check_effect_fn`). Une fois posé, le cas
`60159a … Webbed Up` doit passer au vert sans autre changement.

#### Questions pour l'utilisateur (état après passe 2)

Seule **Q1** (Kingpin's Influence, lecture littérale implémentée) reste ouverte. Q2 et Q3
sont tranchées côté moteur (D2, D3).

## Bloc 5 — Campagne (18/09/2026, coordinateur)

### 1. Inventaire → card_id (6 cartes, 12 faces)

60205a,60205b Art Museum Heist ; 60206a,60206b The Getaway ; 60207a,60207b
Protection Racket ; 60208a,60208b The Raft Breakout ; 60209a,60209b Stop the
Presses! (environnements Completed / Failed) ; 60210a,60210b * Typhoid Mary /
* Bloody Mary (alliée de campagne). Set « Fear No Evil Campaign ».

### 2. Fichiers écrits

- `src/cards/pack/fne/campaign.py` : clés du carnet (`Completed Scenarios`,
  `Failed Scenarios`, `Progress: <affaire>`, `Villain: <affaire>`, `Trust
  Established?`, `Mary Defeated?`, `Allies removed from the campaign`, PV
  restants par joueur = clé moteur) ; `MettreLesEnvironnements`,
  `RetirerLesCartesRetirees`, `MaryWalker`, `MarquesDeLAffaire(manigance)`,
  `MarquesKingpin`, `CollectFNE`, `CapacitesDeCampagne(manigance, garde=None)`,
  `CapacitesDeCampagneKingpin()` ; branchées sur 60121a, 60128a, 60134a (garde
  `_premier_complot`), 60142a, 60151a, 60161a.
- `src/cards/pack/fne/fear_no_evil_campaign/` (`ChercherEnMain`,
  `DefausserDeLaMain`, `RechuteVers` ; 12 scripts).
- `src/cards/pack/mts/campaign.py` : estampille nettoyée (`[^a-z0-9_]`), sans
  quoi « Stop the Presses! » ne correspondait à aucun scénario.
- `data/campagnes/fne.json` (`ordre_libre`, vilains, 5 affaires + Kingpin
  `catalogue: kingpin_fne`, victoire commune) ; `verifier_campagnes.py` OK.
- Lanceur : `public/js/campagne/ordre-libre.js` (module pur : tirage de
  progression, états, vilains, catalogue, défaite) + `tools/tests-lanceur/ordre-libre.test.mjs`
  (12/12) ; `public/js/campagne/app.js` (`vueCampagneLibre`, `lancerScenario`
  avec catalogue et vilain, `estTerminee`) ; CSS `campagne.css` (carnet) ;
  `dico-en.js` ; test d'écran `ui-check/tests/campagne-ordre-libre.spec.ts`
  (4/4 sur un moteur port 40000).
- Harnais : 27 cas `[fne5]` (`.planning/todos/generateurs-fne/gen_cas_fne_5.py`) + vérificateurs
  `fne5_trait`, `fne5_collect` ; clé de cas `carnet` (→ `campaign_log` + règle `mode_campaign`).

### 4. Ce que le harnais a trouvé
`KeyError: 'Class'` sur les environnements de campagne (desc sans `Class`) ;
`WhenCampaignSetup` part après le retournement des complots (garde par CARTE) ;
Hinder du camion ; statuts à lire sur l'alter-ego ; `CollectFNE` testait le
préfixe « * » du nom alors que `paper.py` le retire au chargement (`is_unique`) :
les alliés retirés n'étaient jamais relevés. **BILAN : 27/27 cas passes**
(`[fne5]`, ports 41000 puis 42200 pour les 4 derniers).

### 5. Gabarits PROCESSUS-CARTE (un par carte)

#### 60205a,60205b : Art Museum Heist (Completed / Failed)
- [x] Étape 2 : `MettreLesEnvironnements` (WhenCampaignSetup, face selon « Completed Scenarios » / « Failed Scenarios »), Setup de la face : chaque identité reçoit un statut robuste (`GiveStatus Tough`, `AfterGameSetup`) ; côté Failed : chaque joueur choisit étourdi ou désorienté (`ChooseAbilities`), les deux en expert (`Worlds.IsExpert`).
- [x] Étape 5 : « each identity » → le héros ET l'alter-ego portent le statut (mesuré sur 01001b, la partie commence en alter-ego) ; « choose : stunned or confused » → choix, « both in expert ».
- [x] Étape 6 : environnement à deux faces (`"60205a,60205b"`), traits COMPLETED / FAILED, set « Fear No Evil Campaign », sans `Class`.
- [x] Étape 7 : `60205a Art Museum Heist (Completed) [fne5] — carnet : affaire completee -> l'environnement entre en jeu, chaque identite est robuste`, `60205b Art Museum Heist (Failed) [fne5] — carnet : affaire echouee -> face Failed, le joueur choisit etourdi (premiere option)`, `60205b Art Museum Heist (Failed) [fne5] (expert) — etourdi ET desoriente`, `Marques de progression [fne5] — 2 marques sur Art Museum Heist : +2 menaces sur le complot a la mise en place (1 + 2)`, `Marques de progression [fne5] (expert) — 2 marques : +4 (1 + 4)`. Subst : passe finale.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : couvert par l'autoplay des blocs 2 à 4 (le mode campagne s'y ajoute sans changer le déroulé) et par les 4 tests d'écran `ui-check/tests/campagne-ordre-libre.spec.ts` (tirage, choix, défaite, Kingpin).
- [x] Étape 8 bis : NON (environnement standard, sans compteur).
- Carte terminée : OUI


#### 60206a,60206b : The Getaway (Completed / Failed)
- [x] Étape 2 : `MettreLesEnvironnements` (WhenCampaignSetup, face selon « Completed Scenarios » / « Failed Scenarios »), Setup de la face : après les mulligans, chaque joueur peut chercher une amélioration dans son deck (`WhenCampaignSetupAfterMulligans`, `ChercherEnMain`) ; côté Failed : chaque joueur révèle un attachement du deck rencontre (`Find.FindAndReveal(Attachment)`).
- [x] Étape 5 : « after mulligans » → message dédié `WhenCampaignSetupAfterMulligans` (pas au Setup) ; « **may** search » → `forced=False`.
- [x] Étape 6 : environnement à deux faces (`"60206a,60206b"`), traits COMPLETED / FAILED, set « Fear No Evil Campaign », sans `Class`.
- [x] Étape 7 : `60206a The Getaway (Completed) [fne5] — en jeu ; apres les mulligans, chercher une amelioration (may) : la main compte 7 cartes`, `60206b The Getaway (Failed) [fne5] — en jeu ; chaque joueur revele un attachement du deck rencontre a la mise en place (1 oeuvre au Setup + 1 revelee + 1 par l'Art Thief qu'elle appelle = 3 attachements)`. Subst : passe finale.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : couvert par l'autoplay des blocs 2 à 4 (le mode campagne s'y ajoute sans changer le déroulé) et par les 4 tests d'écran `ui-check/tests/campagne-ordre-libre.spec.ts` (tirage, choix, défaite, Kingpin).
- [x] Étape 8 bis : NON (environnement standard, sans compteur).
- Carte terminée : OUI


#### 60207a,60207b : Protection Racket (Completed / Failed)
- [x] Étape 2 : `MettreLesEnvironnements` (WhenCampaignSetup, face selon « Completed Scenarios » / « Failed Scenarios »), Setup de la face : après les mulligans, chaque joueur peut chercher un soutien ; côté Failed : chaque joueur défausse 1 carte de sa main (2 en expert, `DefausserDeLaMain`).
- [x] Étape 5 : « discard 1 card (2 in expert) » → après la pioche de départ, main 6 → 5 ; en expert 6 → 4.
- [x] Étape 6 : environnement à deux faces (`"60207a,60207b"`), traits COMPLETED / FAILED, set « Fear No Evil Campaign », sans `Class`.
- [x] Étape 7 : `60207a Protection Racket (Completed) [fne5] — en jeu ; apres les mulligans, chercher un soutien (may) : Aunt May arrive en main`, `60207b Protection Racket (Failed) [fne5] — en jeu ; chaque joueur defausse 1 carte de sa main (6 -> 5)`. Subst : passe finale.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : couvert par l'autoplay des blocs 2 à 4 (le mode campagne s'y ajoute sans changer le déroulé) et par les 4 tests d'écran `ui-check/tests/campagne-ordre-libre.spec.ts` (tirage, choix, défaite, Kingpin).
- [x] Étape 8 bis : NON (environnement standard, sans compteur).
- Carte terminée : OUI


#### 60208a,60208b : The Raft Breakout (Completed / Failed)
- [x] Étape 2 : `MettreLesEnvironnements` (WhenCampaignSetup, face selon « Completed Scenarios » / « Failed Scenarios »), Setup de la face : après les mulligans, chaque joueur peut chercher un allié ; côté Failed : les six prisonniers du Raft sont mêlés au deck rencontre (`GenerateCard` + `ShuffleAllTo('EncounterDeck')`).
- [x] Étape 5 : « shuffle the PRISONER minions into the encounter deck » → les six, même hors du set de rencontre du scénario (générés).
- [x] Étape 6 : environnement à deux faces (`"60208a,60208b"`), traits COMPLETED / FAILED, set « Fear No Evil Campaign », sans `Class`.
- [x] Étape 7 : `60208a The Raft Breakout (Completed) [fne5] — en jeu ; apres les mulligans, chercher un allie (may) : Black Cat arrive en main`, `60208b The Raft Breakout (Failed) [fne5] — en jeu ; les six prisonniers du Raft sont meles au deck rencontre`. Subst : passe finale.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : couvert par l'autoplay des blocs 2 à 4 (le mode campagne s'y ajoute sans changer le déroulé) et par les 4 tests d'écran `ui-check/tests/campagne-ordre-libre.spec.ts` (tirage, choix, défaite, Kingpin).
- [x] Étape 8 bis : NON (environnement standard, sans compteur).
- Carte terminée : OUI


#### 60209a,60209b : Stop the Presses! (Completed / Failed)
- [x] Étape 2 : `MettreLesEnvironnements` (WhenCampaignSetup, face selon « Completed Scenarios » / « Failed Scenarios »), Setup de la face : chaque joueur met un soutien DAILY BUGLE en jeu sous son contrôle (`PutIntoPlay(under_control)`, moins les retirés) ; côté Failed : chaque joueur reçoit 1 carte rencontre face cachée (2 en expert, `DealEncounterCards`).
- [x] Étape 5 : « a DAILY BUGLE support » → parmi les quatre du set, moins ceux retirés de la campagne ; « dealt 1 facedown encounter card (2 in expert) ».
- [x] Étape 6 : environnement à deux faces (`"60209a,60209b"`), traits COMPLETED / FAILED, set « Fear No Evil Campaign », sans `Class`.
- [x] Étape 7 : `60209a Stop the Presses! (Completed) [fne5] — en jeu ; chaque joueur met un soutien DAILY BUGLE en jeu sous son controle`, `60209b Stop the Presses! (Failed) [fne5] — en jeu ; 1 carte rencontre distribuee face cachee`. Subst : passe finale.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : couvert par l'autoplay des blocs 2 à 4 (le mode campagne s'y ajoute sans changer le déroulé) et par les 4 tests d'écran `ui-check/tests/campagne-ordre-libre.spec.ts` (tirage, choix, défaite, Kingpin).
- [x] Étape 8 bis : NON (environnement standard, sans compteur).
- Carte terminée : OUI


#### 60210a,60210b : * Typhoid Mary / * Bloody Mary (alliée de campagne)
- [x] Étape 2 : `MaryWalker` (WhenCampaignSetup : « Trust Established? » coché et « Mary Defeated? » non → `PutIntoPlay(under_control=True)`), alliée à deux faces (`RechuteVers(card_type)` : retour côté Bloody Mary / Typhoid Mary), `CollectFNE` coche « Mary Defeated? » quand elle est dans la pile de victoire.
- [x] Étape 5 : « if Trust Established is checked **and** Mary Defeated is not » → double condition ; « put into play under **any** player's control » → premier joueur ; « Mary Defeated? » → pile de victoire à la fin de la partie.
- [x] Étape 6 : alliée unique, deux faces `"60210a,60210b"`, set « Fear No Evil Campaign ».
- [x] Étape 7 : `60210a Typhoid Mary (alliee) [fne5] — carnet : Trust Established sans Mary Defeated -> l'alliee entre en jeu sous ton controle`, `60210a Typhoid Mary (alliee) [fne5] — contre-cas : Mary Defeated coche -> pas d'alliee`, `60210a Typhoid Mary (alliee) [fne5] — apres que tu reveles un sbire : soignee et retournee (Bloody Mary)`, `Carnet sortant [fne5] — victoire avec Disturbed Psyche a 2 jetons et Black Cat retiree du jeu : Completed + Trust Established? + Allies removed` (a trouve un vrai defaut : `paper.name` n'a plus l'etoile a l'execution, `is_unique` a la place ; sans ce cas aucun allie retire n'aurait jamais ete inscrit au carnet), `Cartes retirees de la campagne [fne5] — carnet : Black Cat retiree -> hors du deck de Spider-Man (retiree du jeu)`, `Environnements multiples [fne5] — deux affaires completees et une echouee : trois environnements en jeu sur la bonne face`. Subst : passe finale.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : couvert par l'autoplay des blocs 2 à 4 (le mode campagne s'y ajoute sans changer le déroulé) et par les 4 tests d'écran `ui-check/tests/campagne-ordre-libre.spec.ts` (tirage, choix, défaite, Kingpin).
- [x] Étape 8 bis : NON (alliée standard).
- Carte terminée : OUI

#### Capacités de campagne des manigances (60121a, 60128a, 60134a, 60142a, 60151a, 60161a)
- [x] Étape 7 : `The Getaway (campagne) [fne5] — carnet : Art Museum Heist completee -> 60205a entre en jeu sur The Getaway aussi`, `The Getaway (campagne) [fne5] — 2 marques : Jackknifed Tanker Truck est revele avec 1 menace de plus (2 + Hinder 1 + 1 marque = 4)`, `The Raft Breakout (campagne) [fne5] — 2 marques : chaque prisonnier revele au Setup est robuste et recoit 1 carte boost`, `Stop the Presses! (campagne) [fne5] — 1 marque : le soutien DAILY BUGLE du joueur perd 1 compteur stamina (3 -> 2)`, `Protection Racket (campagne, 2 joueurs) [fne5] — deux complots 1A, mais UN SEUL environnement 60205a entre en jeu`, `Protection Racket (campagne) [fne5] — 1 marque : 1 menace de plus sur le complot du joueur`, `Kingpin (campagne) [fne5] — 3 affaires completees : les trois environnements en jeu, chaque sbire en jeu robuste`, `Kingpin (campagne) [fne5] — 4 affaires completees : James Wesley est trouve et revele (attache a Kingpin)`, plus les cas Art Museum Heist (marques 1 menace / 2 en expert, cartes retirées, PV persistants).
- Carte terminée : OUI (capacités inertes hors campagne : `Worlds.IsCampaign`).

### 6. Décisions et questions
- Ordre libre : tirage fait par l'écran une fois par partie (`campagne.tirage`), défaite déclarée par le joueur (le plateau n'ouvre pas de panneau sur une défaite standard), en expert l'affaire progresse ; Kingpin en expert retourne un environnement Completed ou perd la campagne. Vilain : ordre recommandé du livret au premier parcours, imposé une fois inscrit.
- Aucune question ouverte.

### 7. Ce que ces gates ne voient pas
Aucune campagne jouée de bout en bout à la main ; le panneau de récompenses du plateau relit l'estampille (nettoyée) mais n'a pas été rejoué sur les six manigances.

## Fusion et gates de fin (18/09/2026, coordinateur)

### 1. Ce que la fusion a demande

- Correctifs moteur demandes par les agents et poses par le coordinateur :
  `Asset2.CanAttachTo` envoie `Message.CheckIfFaceCanAttachTo` (il n'etait
  envoye nulle part) ; `CanPlayThisUpgradeCard` filtre ses cibles par
  `CanAttachTo` (D1 bis, pose au bon endroit par l'agent C : le bloc etait
  d'abord tombe dans la fabrique des SOUTIENS) ; message et fabrique
  `WhenEnemyWouldBeGivenBoostCards` (Public Support HIGH, toutes sources) ;
  `Ally` herite de `HasVillainous` + gabarit `fne_black_cat_ally` (Black Cat
  ralliee) ; `ability.attach_selector` expose (Beetle) ; `Puzzle.FindOrCreateFace`
  fouille les cartes mises de cote ET la reserve nemesis.
- **Un defaut de carte trouve par la gate de substitution** : `60140` Man-Bull
  etait inerte (voir §3). Son script lisait un attribut inexistant ; les deux
  cas passaient grace a la menace d'une AUTRE carte. Reecrit et reprouve.
- Deux regressions de ces correctifs, trouvees et corrigees le soir meme :
  la recherche « mise de cote » passait AVANT la recherche « en jeu » (une
  carte en double, `60068a`, recevait ses compteurs sur la copie hors jeu) ;
  le filtre d'accrochage plantait sur les soutiens (`Helicarrier`), corrige
  par un test `Asset2.IsType` puis deplace dans la bonne fabrique.
- Les capacites de campagne ont ete branchees sur les SIX faces 1A
  (`60121a`, `60128a`, `60134a` avec garde, `60142a`, `60151a`, `60161a`).
- Generateurs de cas : chacun n'ecrivait pas ses verificateurs de la meme
  facon, et « du marqueur a `def etat_attendu` » effacait ceux des autres
  blocs (les 6 `fne4_` perdus deux fois). Les cinq generateurs bornent
  desormais leur section par un marqueur de fin.

### 2. Bilans des blocs, apres fusion

| Bloc | Filtre | Bilan |
|---|---|---|
| 1 | `[fne]` | 57/57 |
| 2 | `[fne2]` | 91/91 |
| 3A | `[fne3a]` | 73/73 (le 73e : Robbie a deux joueurs) |
| 3B | `[fne3b]` | 66/66 |
| 3P | `[fne3p]` | 13/13 (dont les deux cas `60140` réécrits) |
| 4 | `[fne4]` | 72/72 |
| 5 | `[fne5]` | 27/27 |

Passe finale, tous blocs ensemble (filtre `[fne`), apres le dernier correctif
de la nuit : **399/399**, et `test_cards` 5742 ok / 0 erreur.

Lanceur de campagne : `node --test tools/tests-lanceur/ordre-libre.test.mjs`
12/12 ; ecran `ui-check/tests/campagne-ordre-libre.spec.ts` 4/4 (moteur reel,
port 40000) ; suite du plateau `npx vitest run` 1676/1676.

### 3. Preuve par substitution des blocs 3 à 5

`scratchpad` de session `chaine_fin.sh` : `substituer_pack.py .game-src <port>
<préfixe>` pour les préfixes `6012` à `6021`, empreinte md5 du pack relevée
avant et après (le pack n'est pas commité : `git status` ne suffirait pas à
détecter un stub oublié, voir l'en-tête de l'outil).

⚠ **UN CAS VERT SANS SON MODULE N'EST PAS FORCÉMENT ACCEPTABLE.** Chacun des
30 modules concernés a été rejoué avec un stub, cas par cas
(`generateurs-fne/qui_reste_vert.py`), pour savoir LEQUEL restait vert. Quatre
familles, toutes légitimes sauf une :

1. **contre-cas d'absence d'effet** : ils mesurent que rien ne se passe, ils ne
   peuvent pas rougir (`60172` « sans stilt : les 3 dégâts passent », `60189`
   deux contre-cas, `60202`, `60180`, `60143`, `60147`, `60159b`...) ;
2. **valeurs natives de `desc`** : menace de départ, Hinder, icône, Steady...
   aucun module ne les code (`60173` « en jeu : 2[per_hero] menaces et 1 icône
   Hazard », `60180` « révélé : 3 menaces », `60189`, `60159b` Steady) ;
3. **cas dont le SUJET est un autre fichier** : la menace du vilain vient de
   `CapacitesCommunes1B` (`protection_racket/__init__.py`, que la substitution
   par `card_id` ne couvre pas) pour `60134b` ; l'entrée en jeu de l'alliée
   vient de `MaryWalker()` (`campaign.py`) pour `60210a` ; la garde « un seul
   environnement » vient de `60134a` pour `60205a` ;
4. **un vrai défaut, trouvé par cette gate** : `60140` Man-Bull était
   **inerte** (rouges **0/2**). Son script lisait `AfterUnitAttackEnd.excess_damage`,
   attribut qui n'existe pas : il ne posait jamais de menace, et ses deux cas
   passaient parce que Battle in the Bodega en posait une de son côté sur la
   même attaque. Réécrit sur `WhenUnitBeDefeated.excess_damage` (la seule
   fenêtre où l'excès existe), cas rejoués sur un scénario neutre (Art Museum
   Heist, complot remis à zéro) pour qu'aucune autre carte ne puisse fournir la
   menace mesurée : **rouges 2/2** après correction.

Les cinq modules « AUCUN CAS » sont des artefacts de nommage : les quatre
copies `60135a`-`60138a` partagent le script de `60134a` (un seul jeu de cas,
nommé `60134a`), et `60210b` est la face arrière de `60210a`.

**77 modules sur 107** tombent au rouge sur TOUS leurs cas quand
on les remplace par un stub vide. Empreinte md5 du pack avant/apres : **IDENTIQUE**.

Modules dont au moins un cas reste vert sans le module (voir les quatre
familles ci-dessus) : `60121b` (3/4), `60128b` (2/3), `60134b` (1/2), `60135b` (1/2), `60130` (4/5), `60140` (0/2, **corrigé depuis : 2/2**), `60143` (1/3), `60145` (4/5), `60147` (1/3), `60159b` (2/6), `60151b` (4/5), `60154` (1/2), `60157` (2/3), `60161b` (2/3), `60162b` (1/2), `60163a` (2/3), `60163b` (3/4), `60172` (2/3), `60173` (2/3), `60180` (1/4), `60189` (2/5), `60190` (3/4), `60193` (2/3), `60197` (1/2), `60198` (1/2), `60205a` (2/3), `60200` (2/3), `60202` (2/3), `60204` (3/4), `60210a` (1/3).

Sans aucun cas sujet : `60135a`, `60136a`, `60137a`, `60138a`, `60210b`.

| Module | Verdict |
|---|---|
| `60121a` | rouges 1/1 |
| `60121b` | rouges 3/4 |
| `60122` | rouges 3/3 |
| `60123` | rouges 2/2 |
| `60124` | rouges 1/1 |
| `60125` | rouges 1/1 |
| `60126` | rouges 3/3 |
| `60127` | rouges 2/2 |
| `60128a` | rouges 2/2 |
| `60128b` | rouges 2/3 |
| `60129a` | rouges 5/5 |
| `60129b` | rouges 1/1 |
| `60120` | rouges 1/1 |
| `60134a` | rouges 2/2 |
| `60134b` | rouges 1/2 |
| `60135a` | AUCUN CAS — gate non tenue |
| `60135b` | rouges 1/2 |
| `60136a` | AUCUN CAS — gate non tenue |
| `60136b` | rouges 1/1 |
| `60137a` | AUCUN CAS — gate non tenue |
| `60137b` | rouges 1/1 |
| `60138a` | AUCUN CAS — gate non tenue |
| `60138b` | rouges 1/1 |
| `60139` | rouges 1/1 |
| `60130` | rouges 4/5 |
| `60131` | rouges 2/2 |
| `60132` | rouges 3/3 |
| `60133` | rouges 3/3 |
| `60140` | rouges 0/2 |
| `60141` | rouges 1/1 |
| `60142a` | rouges 1/1 |
| `60142b` | rouges 2/2 |
| `60143` | rouges 1/3 |
| `60144` | rouges 3/3 |
| `60145` | rouges 4/5 |
| `60146` | rouges 2/2 |
| `60147` | rouges 1/3 |
| `60148` | rouges 2/2 |
| `60149` | rouges 2/2 |
| `60159a` | rouges 3/3 |
| `60159b` | rouges 2/6 |
| `60151a` | rouges 1/1 |
| `60151b` | rouges 4/5 |
| `60152` | rouges 1/1 |
| `60153` | rouges 1/1 |
| `60154` | rouges 1/2 |
| `60155` | rouges 1/1 |
| `60156` | rouges 1/1 |
| `60157` | rouges 2/3 |
| `60158` | rouges 3/3 |
| `60150` | rouges 7/7 |
| `60160a` | rouges 1/1 |
| `60160b` | rouges 1/1 |
| `60161a` | rouges 2/2 |
| `60161b` | rouges 2/3 |
| `60162a` | rouges 4/4 |
| `60162b` | rouges 1/2 |
| `60163a` | rouges 2/3 |
| `60163b` | rouges 3/4 |
| `60164` | rouges 5/5 |
| `60165` | rouges 4/4 |
| `60166` | rouges 5/5 |
| `60167` | rouges 3/3 |
| `60168` | rouges 4/4 |
| `60169` | rouges 3/3 |
| `60177` | rouges 3/3 |
| `60178` | rouges 3/3 |
| `60179` | rouges 3/3 |
| `60170` | rouges 2/2 |
| `60171` | rouges 3/3 |
| `60172` | rouges 2/3 |
| `60173` | rouges 2/3 |
| `60174` | rouges 1/1 |
| `60175` | rouges 3/3 |
| `60176` | rouges 4/4 |
| `60182` | rouges 2/2 |
| `60183` | rouges 2/2 |
| `60184` | rouges 1/1 |
| `60185` | rouges 2/2 |
| `60180` | rouges 1/4 |
| `60181` | rouges 4/4 |
| `60186` | rouges 6/6 |
| `60187` | rouges 3/3 |
| `60188` | rouges 4/4 |
| `60189` | rouges 2/5 |
| `60190` | rouges 3/4 |
| `60191` | rouges 3/3 |
| `60192` | rouges 3/3 |
| `60193` | rouges 2/3 |
| `60194` | rouges 2/2 |
| `60195` | rouges 3/3 |
| `60196` | rouges 4/4 |
| `60197` | rouges 1/2 |
| `60198` | rouges 1/2 |
| `60199` | rouges 2/2 |
| `60205a` | rouges 2/3 |
| `60205b` | rouges 2/2 |
| `60206a` | rouges 1/1 |
| `60206b` | rouges 1/1 |
| `60207a` | rouges 1/1 |
| `60207b` | rouges 1/1 |
| `60208a` | rouges 1/1 |
| `60208b` | rouges 1/1 |
| `60209a` | rouges 1/1 |
| `60209b` | rouges 1/1 |
| `60200` | rouges 2/3 |
| `60201` | rouges 2/2 |
| `60202` | rouges 2/3 |
| `60203` | rouges 2/2 |
| `60204` | rouges 3/4 |
| `60210a` | rouges 1/3 |
| `60210b` | AUCUN CAS — gate non tenue |

### 3 bis. Gates statiques et batterie finale

Passe du 18/09/2026 (avant la correction de Man-Bull) : `test_cards` 5742 ok /
0 erreur ; `verifier_api_cartes` 14 fichiers en faute, tous anterieurs au pack
`fne` sauf `fne/tombstone/__init__.py` (faux positif : `GameRule` y est
importe DANS la fonction) ; `verifier_coherence_cartes` 100 % ;
`verifier_noms_modules`, `verifier_appels_modules`, `verifier_campagnes` OK ;
checksums recalcules.

Chaine finale lancee le 18/09 a 23:54 (`/tmp/gates_finales.sh`, journal
`/tmp/gates_finales.log`), dans cet ordre et JAMAIS en parallele : batterie
complete (`.game-src-b2`), passe des decks (`.game-src-a`), gates statiques
(`.game-src-c`).

**Batterie complete** : **2331/2335** cas passes (2335 rendus, 4 rouges). Les
quatre rouges sont ceux, ANTERIEURS, d'un pack mis de cote, identiques a la
ligne de base d'avant le portage : aucune regression. Une premiere passe en
avait montre 57, tous artefactuels (voir RECETTES §7decies).

Rouges :

- `sg006 The Forager — le depenser fait fouiller le dessus du deck` : Strength, posee sur le dessus du deck, n'a pas ete defaussee : la branche optionnelle du Forager n'a pas ete prise
- `sg007 The Gatherer — le depenser soigne 1 degat a Squirrel Girl` : degats restants = 3 (3 infliges, 1 soin attendu, donc 2)
- `sg009 Squirrel Girl's Costume — un sbire vaincu appelle 1 ecureuil` : 0 carte(s) SQUIRREL en jeu (attendu au moins 1)
- `sg013 Call the Squirrels — 2 ecureuils entrent en jeu PRETS` : ecureuils inclines alors qu'ils devraient etre prets : ['sg002']

**Passe des decks** : **136/136** decks montent une partie (aucun traceback
dans les 136 journaux).

**Gates statiques** : `test_cards` **5742 ok / 0 erreur** ;
`verifier_api_cartes` 13 fichiers en faute, **aucun du pack `fne`** (le faux
positif sur `tombstone/__init__.py` a disparu, `GameRule` y etant importe dans
la fonction) ; `verifier_noms_modules`, `verifier_appels_modules` : aucun
manquement ; `verifier_campagnes` : toutes les cles declarees existent dans le
moteur.

### 3 ter. Questions de règles tranchées par le Rules Reference v1.8 (19/09/2026)

**60180 Collapsing Bridge, sa dernière menace retirée** : l'implémentation
(le pont est vaincu, la Réponse Forcée ne repose rien) est la lecture
**correcte**, et le guide de référence officiel le dit deux fois :

- entrée **DEFEAT** : « If a character has zero or fewer remaining hit points,
  **or if a side scheme has no threat on it, it is defeated.** If an ally,
  minion, or side scheme is defeated, it is discarded. » La défaite n'attend
  pas : elle découle de l'état.
- entrée **IN PLAY AND OUT OF PLAY** : « Card abilities on all card types,
  except event cards and treachery cards, **can only be initiated or affect
  the game while they are in play** unless they specifically refer to being
  used from an out-of-play area. » Le pont défaussé ne peut donc plus rien
  poser, et « here » ne désigne plus rien en jeu.

Le correctif moteur qui va avec (`scheme_side.py` : la Réponse Forcée ne
résout que s'il reste de la menace) est donc conforme, et sans lui le pont
était littéralement invincible.

### 3 quater. Les autres questions, tranchees elles aussi (19/09/2026)

**60131 Jackknifed Tanker Truck (« le vilain ne peut pas subir de degats ») +
60129a Out Front (« quand le vilain SUBIRAIT des degats, retirez autant de
menace a la place »)** : l'implementation (rien ne se passe : ni degat, ni
menace retiree) est la bonne. Le Rules Reference distingue les degats
**infliges** (« dealt ») des degats **subis** (« taken ») : l'entree PREVENT
le dit noir sur blanc, et la regle officielle publiee sur l'Armored Rhino Suit
montre le mecanisme : attaquer ouvre la fenetre « degats INFLIGES », c'est
elle qui declenche l'interruption « would be dealt », et la fenetre « degats
SUBIS » ne s'ouvre jamais ensuite. Le camion interdit precisement d'en
**infliger** : la fenetre qui porte le declencheur d'Out Front n'existe pas,
donc l'interruption ne part pas. L'entree « CANNOT » confirme
(« absolute and cannot be countermanded »). Un camion qui aurait dit
« ne peut pas SUBIR de degats » laisserait, lui, Out Front jouer.

**60173 Kingpin's Influence** (« place 3 threat on their nemesis side scheme.
If it is not in play, they find it and reveal it ») : lecture litterale, dans
l'ordre ecrit. Au moment de la premiere phrase le complot nemesis n'est pas en
jeu, or « card abilities only interact with, and can only target, cards that
are in play » (entree IN PLAY AND OUT OF PLAY) : la pose de menace ne trouve
pas de cible et ne fait rien. La seconde phrase le met en jeu, avec sa menace
imprimee. Aucun arbitrage officiel n'existe sur cette carte (sortie d'avril
2026) ; si FFG tranche l'inverse, une ligne suffira a le changer.

**60152 Daily Bugle « (Any player can do this.) » et 60156 Robbie Robertson
(« after A PLAYER is dealt a facedown encounter card »)** : le second est
desormais MESURE a deux joueurs. `Puzzle.Deal` a recu un parametre `joueur`
(19/09/2026) et le cas
`60156 Robbie Robertson [fne3a] (2 joueurs) — ...` sert la carte au joueur 2 :
Robbie, controle par le joueur 1, la regarde, la defausse et en fait
distribuer une autre AU JOUEUR 2 (cle `distribuees_de`). Bloc 3A : 73/73.
Le Daily Bugle reste couvert pour le seul joueur 1 : le harnais ne sait pas
faire AGIR le second joueur (`Puzzle.Action` passe par le joueur courant).

### 4. Ce que ces gates ne voient pas

Aucune partie humaine ; le pilote d'autoplay ne joue jamais une Alter-Ego
Action ; la campagne n'a pas ete jouee de bout en bout a la main ; a deux
joueurs, seul ce que le joueur 1 DECLENCHE est mesure (le harnais ne conduit
pas le second joueur), meme si les EFFETS sur le joueur 2 le sont desormais.

## Le livret et les images (19/09/2026)

Le portage etait joue et prouve, mais il lui manquait deux choses pour
ressembler aux autres boites.

### 1. Les planches du livret

`public/stories/fne/` etait VIDE et chaque scenario de `fne.json` avait une
liste de pages vide : l'ecran de campagne n'affichait que le texte. Le livret
officiel (`scratchpad/mc60_rulebook.pdf`, 28 pages carrees de 540 points) a ete
rasterise a 975x975, la taille des planches des autres boites, avec `pypdf`
et `PyMuPDF` (il n'y a pas de `pdftotext` ni de `pdftoppm` sur cette machine).

Le livret est fait de pages qui vont PAR PAIRES : la page paire porte la
planche de bande dessinee, la page impaire d'en face porte les regles du
scenario. D'ou la correspondance :

| Page | Fichier | Contenu |
|---|---|---|
| 5 | `00-campagne-regles-1.jpg` | Scenarios interchangeables, conseils par vilain |
| 6-7 | `00-vilains-1.jpg`, `-2.jpg` | Portraits des cinq sous-fifres |
| 8 | `00-campagne-regles-2.jpg` | Regles du mode campagne |
| 9 | `00-campagne-regles-3.jpg` | Les 14 etapes de la mise en place |
| 11 | `00-campagne-intro-1.jpg` | Planche d'ouverture (Daredevil entend les sirenes) |
| 12-13 | `03-protection_racket-intro/regles` | Le racket |
| 14-15 | `04-the_raft_breakout-...` | L'evasion du Raft |
| 16-17 | `01-art_museum_heist-...` | Le casse du musee |
| 18-19 | `02-the_getaway-...` | La fuite |
| 20-21 | `05-stop_the_presses-...` | Arretez les rotatives |
| 22-23 | `06-kingpin-...` | Le Caid |
| 24 | `06-kingpin-epilogue-1.jpg` | Epilogue : Fisk ligote, « See you in court » |

Deux cles sont PROPRES a l'ordre libre, parce que la vue lineaire n'a nulle
part ou les mettre : `pages_intro` (la planche d'ouverture, qui vaut pour la
campagne et pas pour une affaire) et `pages_vilains` (les portraits, replies
sous le choix du vilain). `vueCampagneLibre` les rend, en plus de la BD et de
la page de regles de l'affaire retenue et du bloc « Regles de la campagne ».

⚠ **Defaut vu a la capture, pas au test** : posee en tete de colonne, la
planche d'ouverture poussait le CARNET — la seule chose qu'on vient lire sur
cet ecran — sous la ligne de flottaison. Elle est passee sous le tableau des
affaires. Le test d'ecran, lui, etait vert dans les deux cas : il verifiait la
presence, pas la place.

Preuve : `ui-check/tests/campagne-ordre-libre.spec.ts` compte desormais 5 cas,
dont un qui exige que chaque planche soit non seulement dans le DOM mais
CHARGEE (`naturalWidth > 100`, car `pageLivret` retire en silence une image
introuvable).

### 2. Les images des cartes

95 cartes sur 171 (tout ce qui va de `60128` a `60210`) n'avaient aucune image
locale. Le serveur officiel les sert (verifie : HTTP 200 sur Cerebro pour
`60140`, la ou MarvelCDB rend 404), donc elles s'affichaient en ligne, mais pas
hors connexion et avec un aller-retour reseau par carte. Les 95 scans ont ete
installes dans `assets/pics/` (29 Mo). Il ne reste sans image que cinq entrees
`full_link` (`60051`, `60056`-`60059`), qui sont des REIMPRESSIONS et
empruntent l'image de leur carte source.

## Le chemin complet, de l'ecran de campagne au plateau (19/09/2026)

Question de l'utilisateur : « on peut faire la campagne ? ». Rien ne le
prouvait : tous les tests s'arretaient AVANT le bouton « Lancer le scenario »,
parce qu'un lancement cree une vraie partie sur le moteur vise.

Fait sur un moteur d'essai (port 40000) :
`ui-check/tests/campagne-ordre-libre-lancement.spec.ts`
(`npm run campagne-lancement`, script separe et en-tete d'avertissement, comme
`glisser-plateau.spec.ts`). Il cree une campagne, tire la progression, choisit
Le casse du musee ET Bullseye (pas le vilain recommande, pour verifier que le
CHOIX arrive), lance, et mesure :

- le plateau s'ouvre sur la bonne partie (Bullseye et la manigance en jeu) ;
- `partieEnCours.scenario` vaut `art_museum_heist` ;
- `Villain: art_museum_heist` vaut `bullseye` au carnet ;
- le tirage a ete consomme ;
- `localStorage['mc-campagne-partie']` porte la campagne et le scenario, sans
  quoi le panneau de recompenses ne s'ouvrirait jamais a la fin.

⚠ Le premier passage a echoue en **HTTP 500** : l'equipe d'une campagne porte
le DECK ENTIER (l'ecran de preparation l'y met), pas son nom. C'etait un
defaut du TEST, mais c'est exactement la panne qu'un joueur verrait
(« Failed to create the game »), et rien d'autre ne l'aurait attrapee.

Deux autres constats de cette passe :

- la vignette de la boite manquait (`assets/textures/sets/60. Fear No Evil.webp`
  n'existait pas, la tuile restait noire a la creation). Fabriquee depuis la
  couverture du livret, au format des autres (300x300 webp, bandeau
  « Rulebook » rogne) ;
- le plateau demande a MarvelCDB le texte francais de chaque carte : pour ce
  pack il rend 404, et le panneau reste vide. C'est sans consequence (le
  moteur memorise l'absence et n'affiche rien), mais les cartes de Fear No Evil
  n'auront pas leur traduction tant que MarvelCDB ne les publiera pas.

**Ce qui reste non mesure** : la FIN d'un scenario. Le carnet sortant
(`CollectFNE`), la mise en place des environnements et les marques ont leurs
cas au harnais, le panneau de recompenses a ses propres tests, mais la boucle
complete « gagner une partie -> le carnet s'ecrit -> la partie suivante monte
avec l'environnement » n'a jamais ete jouee d'un trait.
