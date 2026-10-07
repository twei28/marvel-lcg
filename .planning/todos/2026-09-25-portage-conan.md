# Portage de Conan

> **Mise à jour du 07/10/2026 (audit du backlog)** : Portage fait. RESTE, vérifié dans `data/cards.json` au 07/10 : rs014 (desc réduit à GiveTo, sans Boost), rs015 (Boost « 0 », sans Amplify) et rs019 (Boost « 0 ») du pack Red Sonja, listés dans « Défauts trouvés au passage » et jamais corrigés. À corriger après relecture des scans.

Demande de l'utilisateur, 25/09/2026 : « je viens d'ajouter un zip avec le
héros Conan dans le dossier, tu peux le créer ». Zip à la racine du dépôt :
`Conan (09-26)-20260925T173138Z-1-001.zip` (auteur : RyCoRan, même auteur et
même gabarit que Red Sonja, 32 images 1500×2150).

## Tranche d'identifiants retenue

`cn001`-`cn017`, vérifiée libre sur toute la collection (aucun `card_id`
commençant par `cn` avant ce portage). Pack `conan`, `set_name` « Conan » et
« Conan Nemesis ».

## Ce qui a été lu (texte exact des scans, transcrit image par image)

**Insert** (`Conan Insert (1).png`) : trois formes héros (Thief, Barbarian,
King). King est mise de côté au départ et entre en jeu à 8 compteurs Crom sur
The Cimmerian. Thief et Barbarian partagent le même alter-ego. Toutes les
formes partagent le cadran de PV, les statuts, les cartes de rencontre.
Conan peut passer de l'alter-ego à l'une ou l'autre forme héros, d'une forme
héros à l'alter-ego, ou d'une forme héros à l'autre. Les capacités de carte ne
comptent pas dans le changement volontaire du tour. « 10 dégâts ou plus à un
ennemi, ou 8 menaces ou plus : 2 compteurs ? Non, 1 ennemi ou 1 manigance. Au
delà de 5, il faut d'autres ennemis ou manigances. » Les compteurs restent sur
The Cimmerian quand elle passe côté KING. Deux sbires némésis, tous deux
révélés par Shadow of the Past.

**Identité** (une carte à cinq faces, comme Moon Knight `mk001a-e`)
- `cn001a` * Conan the Thief (Hero) : THW 2, ATK 1, DEF 2, HP 11, HS 5.
  ADVENTURER. THIEF. « Rogue's Intuition — Response: After you remove 4 or
  more threat from a scheme in a phase, place 1 Crom counter on The
  Cimmerian. »
- `cn001b` * Conan (AlterEgo) : REC 3, HP 11, HS 6. CIMMERIA. THIEF.
  « Savage Vitality — Setup: Set King Conan aside. Put The Cimmerian upgrade
  into play, TITLE side faceup. Action: Spend 1 resource of any type → place
  1 Crom counter on The Cimmerian. (Limit once per round.) »
- `cn001c` * Conan the Barbarian (Hero) : THW 1, ATK 2, DEF 2, HP 11, HS 5.
  ADVENTURER. BARBARIAN. « Born of Battle — Response: After you deal 5 or more
  damage to an enemy in a phase, place 1 Crom counter on The Cimmerian. »
- `cn001d` * King Conan (Hero) : THW 2, ATK 2, DEF 3, HP 11, HS 5.
  ADVENTURER. KING. « Crown of Aquilonia — Response: After you use a basic
  power, place 2 Crom counters on The Cimmerian. »
- `cn001e` * Conan (AlterEgo, côté roi) : REC 3, HP 11, HS 6. KING.
  « Battle-Forged — Response: After you change to this form, choose: • Give
  King Conan a tough status card. • Remove all crom counters from The
  Cimmerian → heal 1 damage from King Conan for each crom counter removed
  this way. »
- Arts alternatifs : `Conan Retro alt Hero.png` (Barbarian, imprime HP 10 au
  lieu de 11 : coquille de l'art, les stats de référence restent celles de
  `00B`) et `King Conan alt hero.png`. Purement cosmétiques, non posés.

**16 signatures, 11 cartes uniques** (CONAN 1/16 à 16/16 ; les paires
02-03, 04-05, 06-07, 08-09, 10-11 ne diffèrent que par le numéro, vérifié par
différence d'image : seule la zone du numéro change)
1. `cn002` * Bêlit (Ally) — Cost 3, THW 1★, ATK 1★, HP 3. ADVENTURER.
   PIRATE. « While you have the THIEF or KING trait, Bêlit gets +1 THW. While
   you have the BARBARIAN or KING trait, Bêlit gets +1 ATK. Response: After
   Bêlit enters play, if you have the KING trait, ready your identity. »
2-3. `cn003` Crush Your Enemies (Event) ×2 — Cost 1★. ATTACK. « ★ Discount 1
   (KING). Hero Action (attack): Deal 3 damage to an enemy (4 damage instead
   if you are King Conan). »
4-5. `cn004` Reaper's Cleave (Event) ×2 — Cost 1★. THWART. « ★ Discount 1
   (KING). Hero Action (thwart): Remove 2 threat from a scheme (3 threat
   instead if you are King Conan). »
6-7. `cn005` Destroyer's Defiance (Event) ×2 — Cost 1★. DEFENSE. « ★ Discount
   1 (KING). Hero Interrupt (defense): When you would take any amount of
   damage, prevent all of that damage. Place 1 Crom counter on The Cimmerian
   (2 counters instead if you are King Conan). »
8-9. `cn006` Hyborian Havoc (Event) ×2 — Cost 3. ATTACK. THWART. « Hero Action
   (attack/thwart): Deal 5 damage to an enemy or remove 4 threat from a
   scheme. If you are: • Conan the Thief, confuse an enemy. • Conan the
   Barbarian, stun an enemy. • King Conan, all of the above. »
10-11. `cn007` Cimmerian Counter (Event) ×2 — Cost 1★. ATTACK. THWART.
   « ★ Discount 1 (KING). Hero Action (attack/thwart): After you defend
   against an enemy attack, deal damage to an enemy equal to your ATK or
   remove threat from a scheme equal to your THW. »
12. `cn008` Savage Sword (Event) — Cost 4★. ATTACK. THWART. « ★ Discount 1
   (KING). Hero Action (attack/thwart): Exhaust your hero → deal damage to an
   enemy or remove threat from a scheme equal to the total of your hero's
   THW, ATK and DEF values. »
13. `cn009` * The Scarlet Citadel (Player Side Scheme) — coût 0 (badge en
   haut à droite), menace de départ 5 (en bas à gauche). « Victory 0. While
   The Scarlet Citadel is in the victory display, if you have the: • THIEF
   trait, you get +1 THW and ignore the patrol keyword. • BARBARIAN trait you
   get +1 ATK and ignore the guard keyword. • KING trait, all of the above. »
14. `cn010` Savage Tales (Resource). « Hero Response: After you spend this
   card, place 1 Crom counter on The Cimmerian (2 instead if you are King
   Conan). »
15. `cn011` * Atlantean Sword (Upgrade) — Cost 2. WEAPON. « Restricted. Hero
   Response (attack/thwart): After you play an event, exhaust Atlantean Sword
   → deal damage to an enemy or remove threat from a scheme equal to that
   event's printed cost. »
16. `cn012a` * The Cimmerian (Upgrade, sans coût) — TITLE. « Permanent.
   Response: After there are at least 8 Crom counters here, ready your
   identity and swap him with King Conan. Remove your other identities from
   the game. Flip this card. »
   `cn012b` * The Cimmerian (verso) — KING. « Permanent. Hero Interrupt: When
   you use one of King Conan's basic powers, remove X Crom counters from here
   and exhaust The Cimmerian → King Conan gets +X to that power for this
   use. »

**Obligation**
`cn013` The Coils of Doom — « Give to the Conan player. Uses (3 serpent
counters). Victory 0. Hero Action: Spend 1 resource of any type or remove 1
Crom counter from The Cimmerian → remove 1 serpent counter from here. »
Icône Hazard ×1, Boost ×2.

**Némésis (5 cartes, CONAN NEMESIS 1/5 à 5/5)**
- `cn014` (1/5) Frozen Ambush (Side Scheme) — menace de départ 4. « Forced
  Response: After an identity changes form place 2 threat here. » Icône
  Amplify ×1, Boost ×3.
- `cn015` (2/5) * Hrothgar (Minion) — SCH 1, ATK 3, HP 5. GIANT. Toughness.
  « Response: After you make a basic attack against Hrothgar, deal 1 damage
  to Hymdul. (Conan's nemesis minion.) ★ Boost: You are stunned. »
- `cn016` (3/5) * Hymdul (Minion) — SCH 1, ATK 3, HP 5. GIANT. Toughness.
  « Response: After you make a basic attack against Hymdul, deal 1 damage to
  Hrothgar. (Conan's nemesis minion.) ★ Boost: You are confused. »
- `cn017` (4/5, 5/5) Grapple on the Glacier (Treachery) ×2 — « When
  Revealed: Search the encounter deck and discard pile for a GIANT minion and
  put it into play engaged with you. Otherwise, take 4 damage. » Boost ×2.

## Icônes (vérifiées)

Icônes de rencontre tranchées contre les glyphes de la police officielle
`public/fonts/ChampionsIcons.ttf` (méthode de `mots-cles/hazard.md`) :
Frozen Ambush porte le glyphe `F` (Amplify, et non Acceleration), The Coils
of Doom le glyphe `H` (Hazard), les « Y » rouges sont le glyphe `B` (Boost).

Icônes de ressource, lues contre les glyphes `P` (physique, rouge, `R`),
`M` (mentale, bleue, `B`), `E` (énergie, jaune, `Y`), `W` (joker, vert, `G`) :
cn002 G, cn003 R, cn004 B, cn005 Y, cn006 R, cn007 Y, cn008 G, cn009 R,
cn010 RY (deux icônes empilées, convention `rs010`), cn011 Y. cn012 : aucune.

## Arbitrages demandés à l'utilisateur (25/09/2026, un par carte)

1. `cn001a`/`cn001c` : le seuil se CUMULE par cible sur la phase (3 + 3 sur le
   même sbire = 6 ≥ 5 → 1 compteur), un compteur par ennemi (ou manigance)
   et par phase. Comptent : Conan, ses événements, ses améliorations et
   ressources. Bêlit (alliée) ne compte pas.
2. `cn007` Cimmerian Counter : jouée en **Hero Response** juste après avoir
   défendu contre une attaque ennemie. Précision de l'utilisateur : « utiliser
   une carte défense, c'est défense aussi », confirmée par le Rules Reference
   v1.8 (entrée Defend, Defense) : une capacité marquée « (defense) »
   déclenchée PENDANT une attaque ennemie fait de l'identité le défenseur,
   considéré comme ayant défendu. Hors attaque (dégâts de traîtrise), ce n'est
   pas une défense. Ce n'est pas non plus une défense de base (la DEF ne
   réduit rien).
3. `cn012a` The Cimmerian : l'échange garde le CÔTÉ (héros → King Conan
   héros, alter-ego → Conan roi alter-ego). Ce n'est pas un changement de
   forme : Battle-Forged ne se déclenche pas, Frozen Ambush ne prend pas de
   menace.

## Défauts trouvés au passage dans le pack Red Sonja (même gabarit)

Relevés en comparant les icônes, à corriger après Conan :
- `rs015` Queen of the Frozen Wastes : le scan porte Amplify ×1 et Boost ×3,
  `desc` n'a que `Boost: "0"`.
- `rs014` A Warrior's Burden et `rs019` Frozen Fury : Boost ×2 imprimé,
  `Boost` absent ou `"0"` dans `desc`.
- `rs002` Conan (allié) : THW 1★ / ATK 1★ imprimés (dégâts conséquents),
  encodés `"1"` sans étoile.

## Plan d'exécution

- [x] Lecture des 32 scans, transcription ci-dessus.
- [x] Arbitrages (3 questions).
- [x] A. `data/cards.json` : clé `conan`, 22 entrées (The Cimmerian compte
      deux faces), empreintes recalculées.
- [x] B. Scripts `src/cards/pack/conan/{conan,conan_nemesis}/*.py`, plus le
      crochet moteur `hors_pile_identite` (King mise de côté).
- [x] C. `deck/starter/conan.json` (The Cimmerian créée au Setup,
      `player_deck` VIDE).
- [x] D. `data/sets_info.json` (« 177. Custom (Conan) ») et préfixe `cn`.
- [x] F. Images `assets/pics/cn0XX.jpg` (22, 615 px).
- [x] G. Biographie `heros-info.js` (`cn001a`).
- [x] H. Textes FR + compteurs `crom` et `serpent` (test 6/6).
- [x] I. Cas `test_capacites.py` : 49/49 ; substitution 21/22, cn009
      prouvée à la main (3/4).
- [x] J. `verifier_tous_les_decks.py` : le deck monte.
- [x] K. Autoplay ciblé + grep : 8 parties, 0 bloquée, 0 traceback (après
      correction du pilote, voir plus bas).
- [x] L. Plateau : portée limitée aux noms FR des compteurs (voir gabarits).
- [x] M. Gabarits PROCESSUS-CARTE :
      `.planning/todos/2026-09-25-conan-gabarits-processus-carte.md`.
- [ ] N. Partie humaine : hors backlog depuis le 15/09/2026.

## Statut au 25/09/2026 (soir)

**Portage terminé**, non déployé et non commité (attente du « déploie »).

- **Blocage autoplay graine 2, cause trouvée** : le moteur propose une carte
  impayable (comme pour toute carte, officielle ou non) avec
  `target_payment.payment` vide. Le pilote le voyait, mais gardait l'option
  parce qu'elle exige une cible (plage [1, 1]). Correctif dans
  `tools/autoplay.py` : un « Play » impayable est décliné, jouer une carte
  n'étant jamais imposé. Rejeu graine 2 : partie menée à son terme.
- **Incident de session** : un appel bidon injecté dans cn010.py pour
  calibrer `verifier_appels_modules` pendant qu'un autoplay tournait a
  produit 6 tracebacks dans la partie 6. Fichier restauré (md5). Règle :
  aucune modification de `src/` pendant un harnais ou un autoplay.
- **Reste** : défauts Red Sonja listés plus haut, à corriger ensuite.
