# Portage du pack HARRY OSBORN (Green Goblin) — journal de validation

Set 131, préfixe `ho`, 18 `card_id` (ho001a/b + ho002-ho017). Auteur
**Dipsome** (« MC Custom Content By: Dipsome »). Zip source : `A créer/New
Ultimate Green Goblin-20260829T085545Z-1-001.zip` (23 scans, AUCUN livret,
AUCUNE decklist d'aspect).

Ce document tient le gabarit `PROCESSUS-CARTE.md` pour chaque carte du pack,
comme l'exige la « Gate finale » de `PROCESSUS-HEROS.md`. C'était l'item n°8
du plan `.planning/todos/2026-08-29-plan-heros-vilains-fanmade.md` (groupe A,
difficulté 2/5), pris après Angela (n°10) le même jour.

---

## 0. Ce que le pack apporte au projet, au-delà du héros

### Trois fiches mots-clés créées avant d'écrire une ligne de script

`temporary.md`, `piercing.md` et `overkill.md` manquaient à
`docs/reference/mots-cles/`. La fiche `temporary.md` documente un piège réel :
le mécanisme visible dans `has_temporary.py` (`ResolvedTemporaryDiscard`) est
COMMENTÉ, la vraie défausse de fin de round passe par `ProcessTemporary()`
dans `world_action.py`.

### Le trait EARTH-6160 ajouté à l'énum moteur

Tout le pack vit dans l'univers Ultimate 2023 (Terre-6160) : trait ajouté à
`TRAITS` (`src/game/card/face/card_face.py`), sur le modèle du correctif
`superior_iron_man`.

### Le `[filtre]` de test_capacites.py, documenté depuis toujours, enfin réel

L'usage annonçait un 4e argument `[filtre]` qui n'existait pas (aucun
`sys.argv[4]` dans le fichier) : la batterie complète (829 cas, ~2 h)
tournait pour valider 26 cas. Constaté en lançant `... rapport.json ho0`,
implémenté le jour même (sous-chaîne cherchée dans le nom des cas, index
absolus conservés). Une passe filtrée ne remplace PAS la batterie complète
quand un fichier moteur partagé a changé.

### Deux appels latents `CastTo(SideScheme)` repérés ailleurs

`SideScheme` n'existe pas dans l'espace `cards.pack` (la classe moteur est
`SchemeSide2`). Le portage l'a payé au premier test de ho014 (`NameError`) ;
`an011` (angela) et `50074` (aos/black_widow) portent le MÊME appel, jamais
exécuté par leurs cas. À corriger un jour.

### L'icône du side scheme, identifiée par comparaison (leçon Lockjaw)

| Carte | Icône imprimée | Conclusion |
|---|---|---|
| ho014 Ruler of Manhattan | « + » sur une carte inclinée | **hazard** (comme 01107 et vp012) |
| ho017 Refrain From Argument | « ! » en étoile | **crisis** (comme 01108) |

Première saisie inversée (Crisis/Hazard), corrigée AVANT tout script en
relisant le tableau de comparaison du journal venompool.

### Les homonymes, en pagaille

Consignés dans `metadata.collision_note` de `deck/starter/harry_osborn.json`
et en tête de `src/cards/pack/harry_osborn/__init__.py` : Green Goblin
(vilains officiels 02001b-02003b/02014-02016, sbire wd033), **Risky Business**
(l'obligation ho013 porte le nom du SET vilain officiel de Norman Osborn ET de
l'obligation du pack `gob` — coïncidence pure, déjà signalée dans le plan),
Repulsor Blast et Powered Gauntlets (signatures Iron Man aux textes
différents), Goblin Glider/Pumpkin Bombs (attachements du vilain officiel),
Kingpin (wd091-wd093, 60061), Bullseye (56088, 60033), Spider-Man (une dizaine
d'alliés officiels).

### Coquilles du matériel source, corrigées à la saisie

ho014 : « until a side scheme is discard », « eqial » ; ho016 :
« Villainious », « Bullseyes's ». Sens sans ambiguïté dans les quatre cas.

---

## 1. Étapes de `PROCESSUS-HEROS.md`

| Étape | État | Preuve |
|---|---|---|
| 1. Cartes dans `data/cards.json` | ✅ | pack `harry_osborn`, 18 card_id ; JSON hors nouveau pack **identique octet pour octet** (contrôle `avant==apres` après ré-échappement ascii) ; checksums recalculés |
| 2. Scripts | ✅ | 16 modules (ho001b n'a qu'une règle de deckbuilding, AUCUNE capacité runtime : pas de module, comme le vérifie `audit_cartes` texte_seul=0) ; `test_cards` **4750 ok / 0 err** ; `verifier_api_cartes` : rien sur ho0* ; `audit_cartes` : rien sur ho0* |
| 3. Deck de départ | ✅ | `deck/starter/harry_osborn.json`, aspect AGRESSIVITÉ choisi par l'utilisateur le 31/08/2026 (aucune decklist d'auteur) ; la règle de ho001b est UTILISÉE : Sonic Rifle x2 + Stun Gun x2 + Energy Barrier x2 (3 TECH hors aspect) ; montage en vraie partie OK (« identite ho001a, main 6, deck 34 ») |
| 4. `data/nemesis/harry_osborn_nemesis.json` | ✅ | 5 entrées (ho016 en double) |
| 5. `data/sets_info.json` | ✅ | « 131. Custom (Harry Osborn / Green Goblin) », max_id ho017, aligné sur le libellé de `tools/prefixes_fanmade.json` (cartes: 18) |
| 6. Images | ✅ | 18 jpg dans `assets/pics/` (1500x2150, side schemes en paysage), convertis des scans du zip |
| 7. Biographie | ✅ | entrée `ho001a` dans `heros-info.js` ; **vérifiée au survol dans le wizard** (31/08/2026, capture : filtre FAN-MADE → vignette GREEN GOBLIN → panneau `hh-bio` avec bio, identité civile, base, équipes, ennemis, première apparition) |
| 8. Texte français | ✅ | 18 entrées dans `ui-app/src/board/textes-fr-fanmade.ts`, vocabulaire aligné sur `mots-cles.ts` (Robuste/Solide/Perçant/Déferlement/Vilenie/Entrave) ; `ui-app/deployer.sh` passé (build + vérification de sortie OK, déployé dans l'installation) |
| 9. Validation carte par carte | ✅ | §2 ci-dessous : 26 cas, 26/26 verts, 17/17 substitutions rouges |
| 10. Signature d'un autre héros | ✅ | contrôle du guide passé sur les 107 decks : 0 anomalie |

## 2. Gabarits par carte (PROCESSUS-CARTE.md)

Convention de preuve : « cas N » renvoie au nom complet dans
`tools/test_capacites.py` (bloc « Pack harry_osborn ») ; « subst. rouge X/Y »
= le module remplacé par un stub vide fait tomber X de ses Y cas
(`substitutions.sh`, 31/08/2026). La passe verte de référence est
`BILAN : 26/26 cas passes` (rapport `/tmp/rapport-ho4.json`).

### ho001a : * Green Goblin (face héros)

- [x] Étape 2 : références : iw001a Boo! (« After you attack an enemy » →
      `AfterUnitAttackEnd(..., "You", against_who=Enemy)`), wd005 (retrait de
      statut en COÛT, choix du joueur si plusieurs), 08013 Stealth Strike
      (double cible via `ChooseAbilities`).
- [x] Étape 5 : mots-pièges : « from THAT enemy » (coût) vs « to AN enemy »
      (dégâts) — contraste imprimé respecté ; « remove 1 status card » sans
      restriction de type → Tough compte. Piège moteur trouvé : le champ est
      `attacked_targets`, PAS `attacked` (AttributeError au premier passage).
- [x] Étape 6 : nombres : 1 statut / 2 dégâts / 2 menaces — identiques
      texte, desc (aucun) et script.
- [x] Étape 7 : cas « ho001a Green Goblin — Response » (vert) ; subst.
      rouge 1/1. La chaîne est RE-prouvée par 5 autres cas (ho003, ho004,
      ho006, ho009-ressource, ho010-AERIAL) dont les attendus intègrent ses
      +2 dégâts et la consommation du statut.
- [x] Étape 8 : autoplay ciblé §3.

Carte terminée : OUI.

### ho001b : * Harry Osborn (face alter-ego)

- [x] Étape 2 : règle de DECKBUILDING pure (« You may include ... 3 TECH
      upgrades ... »), même famille que ma001b (« upgrade cards ... from any
      aspect ») : AUCUNE capacité runtime, donc aucun module — le moteur ne
      valide pas les decks, la règle s'applique à la construction
      (deck de départ : 3 TECH hors aspect, documentés dans l'aspect_note).
- [x] Étape 5 : « maximum number of copies » = jusqu'à 3 exemplaires par
      carte (règle générale), « 3 TECH upgrades » = 3 cartes DISTINCTES.
- [x] Étape 6 : REC 3 / PV 9 / HS 6 dans desc, conformes au scan.
- [x] Étape 7 : rien à déclencher (pas de capacité). Le cas « ho013 — à la
      remise » prouve au passage que l'identité alter-ego vit correctement.
- [x] Étape 8 : autoplay ciblé §3.

Carte terminée : OUI.

### ho002 : * Spider-Man (Peter Parker), allié

- [x] Étape 2 : 01083 Mockingbird (`AfterCardEnterPlay` + `GiveStatus`),
      14006 Speed Cyclone (`range=(1, 2)`).
- [x] Étape 5 : « a TOTAL of 2 ... on UP TO 2 enemies » : répartition libre
      (2 sur une cible unique, sinon 1+1).
- [x] Étape 6 : coût 4 / PV 3 / THW 2* / ATK 2* / 2 stun / 2 ennemis.
- [x] Étape 7 : cas « ho002 Spider-Man » (2 ennemis, 1 stun chacun) vert ;
      subst. rouge 1/1.
- [x] Étape 8 : autoplay ciblé §3.

Carte terminée : OUI.

### ho003 : Repulsor Blast (x2)

- [x] Étape 2 : 05015 Tackle (jumeau structurel : stun + dégâts à LA MÊME
      cible, `canbe_stunned=True`).
- [x] Étape 5 : « to THAT enemy » ; l'ordre imprimé (stun AVANT dégâts) est
      respecté dans l'opération.
- [x] Étape 6 : coût 2 / stun / 4 dégâts.
- [x] Étape 7 : cas « ho003 Repulsor Blast » vert (6 dégâts au total, chaîne
      ho001a comprise) ; subst. rouge 1/1.
- [x] Étape 8 : autoplay ciblé §3.

Carte terminée : OUI.

### ho004 : Pumpkin Bomb (x2)

- [x] Étape 2 : 04006 Explosive Arrow (sélecteur
      `"VillainAndEngagedSamePlayerMinion"`, le choix du joueur est porté par
      le sélecteur), 14006 (`effect.GetCostX()`), ag006/th009
      (`if_this_attack_defeats` par unité vaincue).
- [x] Étape 5 : « confuse AN enemy » (pas forcément un ennemi touché) ;
      « defeated this way » → uniquement les victimes de CES dégâts. Piège de
      harnais : forcer `cibles` excluait le sbire du sélecteur AoE.
- [x] Étape 6 : X partout, aucune constante cachée.
- [x] Étape 7 : cas « ho004 Pumpkin Bomb » vert (X=2, sbire mort, confusion
      posée puis consommée par la chaîne) ; subst. rouge 1/1.
- [x] Étape 8 : autoplay ciblé §3.

Carte terminée : OUI.

### ho005 : * Gwen Stacy Osborn

- [x] Étape 2 : an002 Sera (`GiveKeywordToInPlayWhenApplyThis(Identity,
      control_by="You", recover=1)`), 31009 (double coût d'inclinaison
      chaîné), 01083 (confusion).
- [x] Étape 5 : « Harry Osborn gets +1 REC » = l'identité (le REC n'existe
      qu'en alter-ego) ; l'action exige d'incliner LES DEUX cartes.
- [x] Étape 6 : coût 2 / +1 REC.
- [x] Étape 7 : cas « +1 REC en continu » et « Alter-Ego Action » verts ;
      subst. rouge 2/2.
- [x] Étape 8 : autoplay ciblé §3.

Carte terminée : OUI.

### ho006 : * Norman Osborn

- [x] Étape 2 : 32047 Aggressive Energy / 54002 Cybernetic Arm (MOT POUR MOT
      « that event deals 1 additional damage » : `RegisterTemp` +
      `DealAdditionalDamage(1)` jusqu'à résolution de l'événement payé) ;
      déclencheur `WhenPlayerPlayCard(HeroInterrupt, "You",
      CardFinder2("ATTACK", Event))` (37006, 05011).
- [x] Étape 5 : « When you play an [[ATTACK]] event » : le JEU de la carte,
      pas son paiement (contraste avec 32047/54002).
- [x] Étape 6 : coût 1 / +1 dégât.
- [x] Étape 7 : cas « ho006 Norman Osborn » vert (4+1+2=7 avec la chaîne) ;
      subst. rouge 1/1.
- [x] Étape 8 : autoplay ciblé §3.

Carte terminée : OUI.

### ho007 : * Otto Octavius

- [x] Étape 2 : 01034 Stark Tower (« choose a player », `ForEachTargets`),
      an001b (`Search.PlayerCard(include_player_deck=True, ...)` +
      `GainCard`).
- [x] Étape 5 : « THAT player searches THEIR deck » : le joueur choisi
      fouille et reçoit ; « (Shuffle.) » = comportement par défaut de la
      fouille. « add it » (sic, coquille d'auteur conservée dans le texte).
- [x] Étape 6 : coût 2.
- [x] Étape 7 : cas « ho007 Otto Octavius » vert (Energy Barrier remonte du
      deck en main) ; subst. rouge 1/1.
- [x] Étape 8 : autoplay ciblé §3.

Carte terminée : OUI.

### ho008 : * Goblin Armor

- [x] Étape 2 : an008 Siri's Dress (`health=3`), 01038 Powered Gauntlets
      officiel (variante conditionnée au trait, `hero.HasTrait("AERIAL")`),
      an004 (`RemoveThreatFromSchemes` + `SetTarget(Scheme2)`).
- [x] Étape 5 : « 2 threat INSTEAD » : branches exclusives, jamais 1+2.
- [x] Étape 6 : +3 PV / 1 menace / 2 menaces.
- [x] Étape 7 : cas « +3 points de vie », « 1 menace SANS AERIAL »,
      « 2 menaces AVEC AERIAL » verts ; subst. rouge 3/3.
- [x] Étape 8 : autoplay ciblé §3.

Carte terminée : OUI.

### ho009 : * Goblin Helmet

- [x] Étape 2 : 31009 SP//dr Command (redressement à trait), an007 Asgard's
      Assassin (`CanGenerateResources(resources_fn=...)` payé par
      `SetCostFunc`), 21006 Energy Duplication (couleur imprimée d'une AUTRE
      carte, `FacesCounter.GetPrintedResources`).
- [x] Étape 5 : « the printed resource ON THAT upgrade » : couleur lue sur la
      TECH épuisée. Découverte moteur : dans le couple Can+Do de 31001a,
      `res` est figé AVANT le `PayCost` (resources.py:398) — un `res_fn` sur
      `return_exhausted_cards` lisait l'état d'avant paiement (constaté :
      casque incliné, TECH non). Montage final : une seule
      `CanGenerateResources` + `CostFunc.Custom` qui épuise la première TECH
      prête. **ÉCART ASSUMÉ, documenté dans le module** : pas de choix du
      joueur quand plusieurs TECH prêtes de couleurs différentes (la couleur
      est figée à l'annonce). À vérifier en partie réelle si le cas se
      présente.
- [x] Étape 6 : coût 2 / 1 TECH épuisée / 1 ressource.
- [x] Étape 7 : cas « redresse une amélioration TECH » et « génère la
      ressource IMPRIMÉE » verts (casque ET Forcefield Generator inclinés,
      Repulsor Blast payé) ; subst. rouge 2/2. Piège de harnais documenté
      dans le cas : `Puzzle.Exhaust('05017')` attrapait la copie du DECK
      (le deck de départ contient 2x 05017), d'où le passage à 31019.
- [x] Étape 8 : autoplay ciblé §3.

Carte terminée : OUI.

### ho010 : Powered Gauntlets (x2)

- [x] Étape 2 : 01038 homonyme officiel (squelette exhaust→dégât + test de
      trait ; textes DIFFÉRENTS, aucun partage de code), 50134 Innocent
      Bystanders (`ForChoiceAbilityWithCost(Cost("1"))` + `Otherwise`).
- [x] Étape 5 : « you may spend » : strictement optionnel ; « confuse THAT
      enemy » : l'ennemi déjà blessé par les gants.
- [x] Étape 6 : coût 2 / 1 dégât / 1 ressource.
- [x] Étape 7 : cas « PAS de confusion sans AERIAL » et « AERIAL : une
      ressource dépensée » verts ; subst. rouge 2/2.
- [x] Étape 8 : autoplay ciblé §3.

Carte terminée : OUI.

### ho011 : * Goblin Glider

- [x] Étape 2 : an008/ra007 (`GiveKeywordToAttached("You", attack=1,
      trait="AERIAL")`), an001a (`Faces.ReadyAll` sur le héros).
- [x] Étape 5 : « Green Goblin gets » : l'identité (convention an008 pour un
      héros nommé) ; le trait part avec le planeur (continu par
      construction).
- [x] Étape 6 : coût 3 / +1 ATK.
- [x] Étape 7 : cas « +1 ATK et trait AERIAL » et « redresse Green Goblin »
      verts ; subst. rouge 2/2. Le trait est RE-prouvé par les branches
      AERIAL de ho008 et ho010.
- [x] Étape 8 : autoplay ciblé §3.

Carte terminée : OUI.

### ho012 : "That Had to Hurt" (x2)

- [x] Étape 2 : 50144 Solid Sound Constructs (quasi jumeau :
      `GiveKeywordToAttached(stalwart=-1)` + `AfterStatusCardPlaceOn`),
      33005 Exploit Weakness (`CanPlayThisUpgradeCard(Enemy)` + MaxPerUnit +
      Temporary), 01009 Webbed Up (`SetPlay(hero_form_only=True)`).
- [x] Étape 5 : « loses the stalwart OR steady keyword » : les deux retraits
      posés en continu, neutres sur un mot-clé absent ; « gets a status
      card » sans restriction → stun, confuse ET tough déclenchent ;
      « deal 1 damage to IT » : le personnage attaché. Temporary/MaxPerUnit :
      desc, bases automatiques (fiche temporary.md créée pour l'occasion).
- [x] Étape 6 : coût 1 / max 1 par ennemi / 1 dégât.
- [x] Étape 7 : cas « ho012 That Had to Hurt » vert — il prouve les DEUX
      moitiés d'un coup : Bullseye (ho016) est Stalwart, sans ho012 le stun
      serait refusé ; avec, le stun passe ET la Response inflige 1 dégât ;
      subst. rouge 1/1.
- [x] Étape 8 : autoplay ciblé §3.

Carte terminée : OUI.

### ho013 : Risky Business (obligation)

- [x] Étape 2 : an010 (`WhenThisObligationGiveToYou` + stun), wd005
      (`PlayerActionToDiscardThis`), 01034 Stark Tower (`FindTopmost` +
      `ReturnToHand`).
- [x] Étape 5 : « Return ... » = phrase séparée après « discard this card » :
      l'action se résout même sans TECH en défausse ; « the TOPMOST TECH
      upgrade » : la plus au-dessus, prouvée par une défausse à deux cartes.
- [x] Étape 6 : Boost 2 / 1 carte remontée.
- [x] Étape 7 : cas « à la remise : le joueur est étourdi » et « défausse et
      remonte la TECH du dessus » verts ; subst. rouge 2/2.
- [x] Étape 8 : autoplay ciblé §3.

Carte terminée : OUI.

### ho014 : Ruler of Manhattan (side scheme némésis)

- [x] Étape 2 : an011 (`WhenThisRevealed`), 15004 Hex Bolt
      (`Worlds.DiscardEncounterCards` + `FacesCounter.CountTotalBoostIcons`),
      an015 (révélation depuis la défausse, `face.Reveal(None, effect)`).
- [x] Étape 5 : « Remove threat from HERE » (d'elle-même) ; « on THAT card »
      (le complot déterré) ; coquilles imprimées corrigées ; garde-fou
      anti-boucle si aucun side scheme n'existe (leçon Underling). Piège payé :
      `SideScheme` n'existe pas dans `cards.pack`, la classe est
      `SchemeSide2` (NameError au premier passage).
- [x] Étape 6 : menace 5 / boost 3 / hazard 1 ; le retrait vaut le nombre
      d'icônes de la carte déterrée (2 pour 01107 → 5-2=3, vérifié).
- [x] Étape 7 : cas « ho014 Ruler of Manhattan » vert (01110 défaussé, 01107
      révélé, menace 3) ; subst. rouge 1/1.
- [x] Étape 8 : autoplay ciblé §3 (set némésis mélangé au deck rencontre).

Carte terminée : OUI.

### ho015 : * Kingpin (sbire némésis)

- [x] Étape 2 : 04125 Red Skull (MOT POUR MOT « +1 ATK for each side scheme
      in play », `ThisGainKeywordForEachFaceInPlay(CardFinder(
      card_type=SchemeSide2))`, étoile codée sans verrou Expert — convention
      moteur), 01059 Jessica Jones (le pendant SCH), an013
      (`WhenCardBecomeBoost`), 50134 (`PlaceThreatOnSchemes`, littéral
      "EachSideScheme").
- [x] Étape 6 : +1/+1 par complot annexe / 2 menaces par complot / PV 8 /
      boost 2.
- [x] Étape 7 : cas « +1 SCH et +1 ATK » et « Boost : 2 menaces » verts ;
      subst. rouge 2/2.
- [x] Étape 8 : autoplay ciblé §3.

Carte terminée : OUI.

### ho016 : * Bullseye (sbire némésis, x2)

- [x] Étape 2 : Stalwart/Villainous : desc, bases automatiques (11041
      Deathunt 9000, fiches stalwart.md / villainous.md — coquille
      « Villainious » corrigée) ; l'étoile : 27078 « Now We're Angry! »
      (`UnitAttackGainKeyword`, `attacker="This"` pour ne pas toucher les
      Bullseye homonymes 56088/60033), fiches piercing.md et overkill.md
      créées.
- [x] Étape 6 : PV 6 / SCH 1 / ATK 1*.
- [x] Étape 7 : cas « ho016 Bullseye » vert — défenseur = l'ALLIÉ ho002 avec
      robuste : elle saute ET l'ATK 1 blesse (seul le dégât discrimine, la
      robustesse part aussi quand elle absorbe ; première version sur
      l'identité DEF 2, rouge à tort) ; subst. rouge 1/1. **L'overkill du
      même handler est indéclenchable par le harnais** (ATK 1 ne déborde
      jamais d'un défenseur à 1 PV minimum) : couvert par la même ligne de
      code que le piercing prouvé, à observer en partie réelle si un effet
      booste l'ATK de Bullseye.
- [x] Étape 8 : autoplay ciblé §3.

Carte terminée : OUI.

### ho017 : Refrain From Argument (side scheme némésis)

- [x] Étape 2 : Hinder 1* et Crisis : desc, bases automatiques (fiches
      hinder.md — le `*` note « par joueur » — et crisis.md) ; le boost :
      16140 Sound the Alarms (`WhenCardBecomeBoost("This", RevealThisCard)`)
      avec la condition « no side scheme in play » via `conditions`.
- [x] Étape 6 : menace 2 / entrave 1 par joueur / boost 0 (étoile seule).
- [x] Étape 7 : cas « se révèle s'il n'y a AUCUN complot annexe » (vert,
      menace 3 = 2+1) et contre-cas « Boost muet » (vert) ; subst. rouge
      1/2 — le contre-cas vérifie une ABSENCE d'effet et reste vert par
      construction sous stub, même situation assumée que vp014/vp015.
- [x] Étape 8 : autoplay ciblé §3.

Carte terminée : OUI.

## 3. Autoplay ciblé (étape 8)

8 parties `harry_osborn` contre Rhino (normal, profil équilibré) + 8 parties
TÉMOIN `venompool`, mêmes graines, le 31/08/2026 :

| Deck | V | D | %V | rounds tenus | incidents (« ! ») |
|---|---|---|---|---|---|
| harry_osborn | 0 | 8 | 0 % | 4,4 | 0 |
| venompool (témoin) | 0 | 8 | 0 % | 5,4 | 0 |

- **Grep exhaustif des 16 journaux** (`NameError|AttributeError|TypeError|
  KeyError|AssertionError`) : **0 partout**.
- Le 0 % de victoire ne dit rien du deck (le témoin fait pareil, et le TODO
  des decks fan-made rappelle que Deadpool officiel fait 0 % aussi) ; les
  rounds tenus sont comparables (4,4 vs 5,4).
- **Lecture des journaux, cartes du pack** : les 16 cartes jouables
  apparaissent en partie (ho008 et ho013 dans les 8 journaux, le set némésis
  dans 1 partie — l'obligation doit sortir pour l'amener). Le casque ho009 a
  utilisé SES DEUX capacités en partie réelle : redressement des Powered
  Gauntlets (« activates, targets [ho010] ») et paiement en ressource
  (casque + gants inclinés ensemble au fil d'un paiement).

## 4. Batteries finales

- `test_capacites.py` filtré `ho0` : **26/26** (`/tmp/rapport-ho4.json`).
- Substitutions : **17/17 cartes** prouvées (`substitutions.sh`).
- `test_cards` : 4750 ok / 0 err. `verifier_api_cartes` / `audit_cartes` :
  rien sur ho0*.
- Passe des 107 decks : **107/107**. Le premier passage (91/107) tournait en
  même temps que les cas de comportement : chaque harnais RÉÉCRIT
  `.game-src/launch.json` avant chaque processus fils, deux passes simultanées
  se marchent dessus quelle que soit la plage de ports — cause réelle des
  « AssertionError: ip/port », annotée dans les docstrings des deux outils.
  Repasse propre : 102/107 + les 5 premiers decks (touchés par la batterie
  pas encore tuée) reverifiés un à un, tous OK.
- Batterie complète des 829 cas (non-régression, fichiers moteur partagés
  touchés : `card_face.py` enum TRAITS, harnais) : **801/829**, et les 28
  rouges sont tous EXPLIQUÉS, aucun n'est une régression du portage :
  - 23 cas du pack `jj` pointaient `"heros": "jessica_jones"`, orphelins
    depuis que ce nom désigne l'ancienne version set 61 (renommage
    `jessica_jones_custom` à l'époque d'iron_lad). **Corrigés le jour même**
    et re-vérifiés : 28/28 cas jj verts au `[filtre]` ;
  - 5 écarts de comportement préexistants (sg009/sg013/sg007/sg006, ss012),
    sans traceback, sans lien avec les fichiers touchés aujourd'hui :
    consignés dans `.planning/todos/2026-08-31-cas-rouges-sg-ss.md`.
- `tools/substituer_pack.py` (promu du script jetable du jour) : passe réelle
  sur ho016, « rouges 1/1 », arbre git propre après restauration.

## 5. Ce que ces contrôles ne peuvent pas voir — reste à faire

- **Une vraie partie jouée à la main dans le navigateur** (gate finale de
  PROCESSUS-HEROS.md) : non faite.
- **L'écart assumé de ho009** (pas de choix entre plusieurs TECH prêtes de
  couleurs différentes) et **l'overkill de ho016** (indéclenchable, ATK 1) :
  à observer en partie réelle.
