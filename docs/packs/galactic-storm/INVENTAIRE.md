# Galactic Storm : inventaire complet (lot GS-0, 20/10/2026)

Source : les quatre archives `MC custom content by Kajislav-20261014T200011Z-1-00{1..4}.zip` (racine du dépôt), partie
Galactic Storm extraite par `docs/packs/galactic-storm/sources/z1..z4` (dossier ignoré par git, règle ajoutée à `.gitignore`).
Les transcriptions (texte anglais imprimé, marqueur `[?]` pour toute lecture douteuse) sont dans `transcriptions/<bloc>.md`,
les règles dans `REGLES.md`, les questions pour l'utilisateur dans `.planning/todos/2026-10-20-gs0-questions.md`.

## 1. Ce que contient chaque archive (partie Galactic Storm)

| Archive | Fichiers extraits | Contenu |
|---|---|---|
| zip 1 (001) | 123 | boîte de sortie (2000x2000), 5 alliés d'identité, **livret 1.1**, Binary (16), Quasar (14), Accuser Corps (5), Imperial Guard (8 dont l'insert), Nega Bomb (2 dont l'insert), Seeds (1), Starforce (5), Earth Under Siege (20), Hala (11 dont insert), Kree Sentry (11 dont insert), Majestrix (13 dont insert), Supreme Intelligence (10) |
| zip 2 (002) | 110 | 2 alliés de campagne, 3 alliés d'identité, **livret 1.2 compressé**, page 24 du livret (journal), boîtes, Binary (15), Quasar (20), modulaires, Earth Under Siege (19, dont insert page 2), Hala, Kree Sentry, Majestrix, Supreme Intelligence (insert) |
| zip 3 (003) | 126 | allié Gladiator, 2 alliés d'identité, boîte, dos spoiler de Doctor Minerva, Binary (20), Quasar (14), modulaires, Earth Under Siege (26, dont insert page 1), Hala, Kree Sentry, Majestrix, Supreme Intelligence |
| zip 4 (004) | 10 | **livret 1.2 non compressé** (336 Mo, même mise en page), 5 cartes de mise en place de Majestrix (Deathbird II, III, Earn the People's Favor IB, Majestrix's Verdict IIB, Shi'ar Throne support), 4 de Hala (Tanalth II, III, Hidden on Hala IB, Reckoning Begins IIA) |

Total : 369 fichiers (dont 3 PDF). Les comptes par dossier correspondent au cadrage : Campagne 24, Binary 51, Quasar 48, Kree Sentry 27,
Majestrix 38, Hala 37, Earth Under Siege 65, Supreme Intelligence 27, Imperial Guard 24, Accuser Corps 7 cartes, Nega Bomb 5,
Seeds 7, Starforce 9 (les listes `unzip -l` comptaient en plus une ligne par dossier).

Fichiers non-cartes : 7 couvertures de coffret/pack (1876x3076), 8 dos de couverture (889x966 / 1111x966), 8 images de sortie
(2800x1800), 8 compteurs de PV (1024x512 : Binary, Quasar, Annihilus, Attuma, Destroyer, Doctor Minerva, Mole Man, Veranke),
5 boîtes (9292x9292, 5000x5000, 2000x2000), 5 inserts de scénario + 2 inserts de modulaire (4520x4520), la page 24 du livret,
3 PDF, 2 images de deck de départ (Binary, Quasar : livret de liste de cartes) et le dos spoiler de Doctor Minerva (1459x2085).

### Doublons et manques constatés

- **Aucun doublon d'octets** (somme de contrôle sur les 369 fichiers).
- Le livret 1.2 existe en deux versions (compressé 5,6 Mo dans le zip 2, non compressé 336 Mo dans le zip 4) : même mise en page,
  le texte lu est celui du compressé.
- Le livret est une suite d'images sans texte extractible : tout est lu à l'œil (REGLES.md).
- **Pas d'insert** pour Accuser Corps, Seeds of Corruption ni Starforce (leurs règles sont dans le livret p.8 et p.19 et l'insert
  de Supreme Intelligence pour Starforce).
- Pas de pile de victoire, ni de carte de journal de campagne en carte : seule la page 24 du livret.
- Plusieurs **noms de fichier diffèrent du nom imprimé** : « 21 War Academies of Hala » et « 20 War Academies of Hala » sont la carte
  **Mobilizing the Empire** (151) ; « 01 Kree Ruler I/II/III » sont les trois **Kree Leader** (138A, 139A, 140A) ; « Grip of
  Annihilation » = **Death Grip** (85) ; « lair collapse protocol » = **Outpost Collapse Protocol** (87) ; « caught in their sights » =
  **Caught in Its Sights** (89) ; « 22 detention facility of hala » = **Secrets of Detention Cells** (152).
- Plusieurs cartes de scénario sont **pivotées** de 90 degrés dans l'image (compagnons de manigance, Earthfall 1B, etc.).
- Les cartes **Veranke** d'Earth Under Siege existent aussi, déjà portées en partie, dans le coffret Skrull Menace (voir
  `.planning/skrull-menace/INVENTAIRE.md` : « cartes Veranke de Earth Under Siege, 4 cartes + cadran de PV » laissées hors périmètre).

## 2. Totaux par bloc contre les 305 cartes attendues

Le livret p.2 annonce **305 cartes** (109 joueur, 24 méchant, 172 rencontre). Le décompte réel des images de cartes est de
**319** (323 images au format carte 1500x2150, moins 2 listes de deck de départ et 2 inserts de modulaires rangés dans le même
format). Écart : **+14**. Ce que je peux établir :

- Les **24 cartes méchant** correspondent exactement (Kree Sentry 3, Deathbird 3, Kree Leader/Tanalth 3, six méchants d'Earth Under
  Siege 12, Supreme Intelligence 3).
- 319 moins les 13 cartes de campagne = 306, soit un de plus que 305 : le livret compte peut-être les cartes sans la campagne,
  ou compte deux fois ou une fois de moins une carte. **Non tranché** (question Q2).
- Les exemplaires multiples (deux Pursued by the Flame, quatre Kree Infantry, etc.) sont des fichiers distincts : une carte
  physique par fichier. Le nombre de cartes **distinctes** (numéro + nom + face) est donné dans la colonne de droite.

| Bloc | Images totales | Hors carte | Images de carte | Cartes distinctes |
|---|---|---|---|---|
| binary | 24 | 1 (liste du deck de départ) | 23 | 17 |
| binary-reskins | 23 | 0 | 23 | 23 |
| quasar | 25 | 1 (liste du deck de départ) | 24 | 18 |
| quasar-reskins | 19 | 0 | 19 | 19 |
| kree-sentry | 23 | 0 | 23 | 17 |
| majestrix-verdict | 34 | 0 | 34 | 27 |
| hala-ultimatum | 33 | 0 | 33 | 23 |
| earth-under-siege | 30 | 0 | 30 | 27 |
| earth-under-siege-ensembles | 24 | 0 | 24 | 17 |
| supreme-intelligence | 23 | 0 | 23 | 16 |
| imperial-guard | 24 | 1 (insert) | 23 | 23 |
| modular-sets | 28 | 1 (insert Nega Bomb) | 27 | 21 |
| campagne | 13 | 0 | 13 | 13 |
| **Total** | **323** | **4** | **319** | **259** |

Par ensemble de rencontre (images de carte) : Kree Sentry 23 ; Majestrix's Verdict 34 (dont 6 Starjammers) ; Hala Ultimatum 33 ;
Earth Under Siege 54 (28 d'ensembles des six méchants + 16 de mise en place + 10 reskins Standard/Expert) ; Supreme
Intelligence 23 ; Imperial Guard 23 ; Accuser Corps 7 ; Nega Bomb 4 ; Seeds of Corruption 7 ; Starforce 9 ; Binary 23 + 23
reskins ; Quasar 24 + 19 reskins ; campagne 13.

### Les 42 cartes officielles redessinées (reskins)

**Binary (23)** : Defense Specialist (37), Face the Past (21), Follow Through (18), Keep Them Busy (15), Soaring Acrobatics (30),
Spoiling for a Fight (14), Surveillance Specialist (39), Energy (25), Hall of Heroes (16), Deft Focus (29), Directed Force (20),
Marked (19), Aggressive Conditioning (17), Genius (26), Front Line Specialist (38), Into the Fray (12), Moment of Triumph (13),
Avengers Mansion (28), Combat Specialist (36), Hope Summers (22), Nick Fury (23), Specialized Training (24), Strength (27).
**Quasar (19)** : Defensive Conditioning (57), Martinex (63), Energy (65), Genius (66), Honorary Guardian (69), Knowhere (68), Change
of Fortune (56), Starhawk (53), Unflappable (59), Cosmo (60), Drax (61), Multitalented (64), Powerful Punch (55), S.H.I.E.L.D.
Deputy (70), Martyr (52), Desperate Defense (54), Electrostatic Armor (58), Gamora (62), Strength (67).
Total 23 + 19 = **42** (le cadrage disait 42 : exact). Les 10 reskins « Standard-Expert » d'Earth Under Siege (Advance, Assault,
Caught Off Guard, Masterplan, Gang-Up, Under Fire, Shadow of the Past, Exhaustion) sont, eux, des cartes de l'ensemble de rencontre
Standard/Expert redessinées, à rapprocher des cartes officielles `Standard` / `Expert` du moteur : à vérifier au lot GS-7
(elles portent l'indication « aucun » comme numéro imprimé).

## 3. Numérotation : une seule suite à établir, et pourquoi elle n'est pas établie

Le pied de carte porte « MC Custom Content By: Kajislav [planète] N », comme Skrull Menace. Pour Skrull Menace la suite était
unique (1 à 288) et le `card_id` était `sk` + numéro sur 3 chiffres. Ici, **la suite imprimée n'est pas unique** :

1. **Plage** : les numéros vont de 1 à 240, **jamais 305** ; le livret cite 224-236 pour la campagne (exact : 224 à 236 relevés).
2. **Trous** dans la suite : 31, 33, 34, 35, 40 à 48, 50, 51, 71 à 75, 238 (21 numéros absents). Ils correspondent vraisemblablement
   à des cartes non fournies ou à des numéros réservés (Quasar : 40-51 ; némésis : 31-35, 71-75).
3. **Collisions** entre cartes différentes : Binary « Pursued by the Flame » (4) et « Forgotten Life » (4) ; les 17 cartes de héros de
   Quasar portent toutes le numéro imprimé **4** (sauf Quantum Bubble, 49), alors que la suite de 1 à 16 est donnée par « QUASAR
   (n/16) » ; les némésis de Binary et de Quasar partagent 237, 239, 240 (Touched/Avatar of Oblivion ; Goin' Rogue/Entropy Ascendant ;
   Energy Transfer/Distant Manipulation) ; les cartes de Hala, d'Earth Under Siege, de Kree Sentry, de Majestrix, d'Imperial Guard
   et de Supreme Intelligence ont des numéros propres (76-223) sans collision entre blocs.
4. **Reskins Standard-Expert** (Earth Under Siege) : pas de numéro imprimé.
5. Les exemplaires multiples portent le **même** numéro (déjà le cas pour Skrull Menace : un `card_id` par numéro, une seule image).

Le numéro imprimé est donc utilisable pour 76 à 236 (hors collisions signalées) et pour 1 à 39 et 52 à 70 (héros), mais pas pour
les 17 cartes de Quasar (4) ni pour 237/239/240. **Proposition** (à valider, voir questions Q1) : `card_id` = `gs` + numéro imprimé
sur 3 chiffres (+ `a`/`b` pour les faces), avec suffixes `q` (Quasar) pour les trois némésis en collision, et pour les 17 cartes de
Quasar le numéro « n/16 » du pied de carte décalé de 300 (gs301 à gs316, gs349 inchangé pour Quantum Bubble), les reskins
Standard-Expert recevant la plage 241-250 qui est libre.

## 4. Vérification faite pendant le lot GS-0

- Transcription : 13 blocs, **319 cartes + 4 documents** transcrits, **895 marqueurs `[?]`** au total (icônes de ressource jamais
  nommées à vue, chiffres des pastilles, étoiles de renvoi).
- Numéros imprimés : relevés par une planche de découpes du pied de carte, vérifiés pour **tous** les blocs sauf Earth Under Siege,
  modulaires et campagne (relus à l'œil sur l'image pour les fiches échantillonnées).
- Relecture contre l'image (échantillon, lot GS-0) : Kree Sentry I, Sentry's Grasp, Rick Jones (scénario), Cosmic Influx, Energy
  Torrent, Rick Jones (campagne), Quantum Bands, Quantum Bubble, Araki, Supremor : **texte exact dans les 10 cas** ; erreurs
  récurrentes de lecture trouvées : les icônes rouges en forme de Y du bas de carte (icône de boost ordinaire, validée dans
  Skrull Menace), les étoiles noires `★` (renvoi au texte, convention de Skrull Menace) et les pastilles de PV (cercle orange avec
  chiffre) sont notées `[?]` sans être identifiées. L'échantillon couvre moins de 10 % de certains blocs : une relecture complète
  contre les images reste à faire au début de chaque lot GS-1, GS-2, GS-5, GS-8, comme les lots Skrull Menace l'ont fait carte par carte.
- Les erreurs de lecture signalées dans les fiches (« Forces Response » sur Doctor Minerva et Captain Atlas, « completes » sur 80B et
  The Endless Mind IIB, « highes » sur Ronan) sont **imprimées ainsi**.

## 5. Inventaire carte par carte

Colonnes : `#` = rang dans cet inventaire ; `N° imprimé` = numéro du pied de carte ; `Source` = zip puis chemin dans
`docs/packs/galactic-storm/sources/` (HP = Hero Packs, SP = Scenario Packs, MS = Modular Sets) ; `Dim.` = dimensions de l'image ;
`[?]` = nombre de marqueurs de doute dans la fiche de transcription.

### binary : héros Binary (Agressivité) : 2 faces d'identité, 15 cartes de héros, némésis Rogue, obligation

| # | N° imprimé | Nom | Face | Type | Aspect / set / bandeau | Source (zip/chemin) | Dim. | [?] | Remarque |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 4 | Forgotten Life | unique | Obligation | BINARY | z1/HP/Binary/Encounter Cards/41 forgotten life.png | 1500x2150 | 1 |  |
| 2 | aucun | Binary - starter deck | unique | livret de deck de depa | aucun | z1/HP/Binary/Extra/starter deck Binary.png | 1500x2150 | 0 | HORS CARTE (livret de deck ou insert) |
| 3 | 4 | Pursued by the Flame | unique | Event | BINARY | z1/HP/Binary/Hero Cards/05 Pursued by the Flame.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 4 | 4 | Pursued by the Flame | unique | Event | BINARY | z1/HP/Binary/Hero Cards/06 Pursued by the Flame.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 5 | 8 | White Hole | unique | Support | BINARY | z1/HP/Binary/Hero Cards/11 white hole.png | 1500x2150 | 2 |  |
| 6 | 11 | Light, Radiation, Heat | unique | Upgrade | BINARY | z1/HP/Binary/Hero Cards/15 light radiation heat.png | 1500x2150 | 2 |  |
| 7 | 239 | Goin' Rogue | unique | Side Scheme | BINARY NEMESIS | z2/HP/Binary/Encounter Cards/43 Going Rogue.png | 1500x2150 | 5 |  |
| 8 | 237 | Touched | unique | Attachment | BINARY NEMESIS | z2/HP/Binary/Encounter Cards/44 touched 2.png | 1500x2150 | 0 |  |
| 9 | 240 | Energy Transfer | unique | Treachery | BINARY NEMESIS | z2/HP/Binary/Encounter Cards/46 energy transfer.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 10 | 2 | Cosmic Influx | unique | Event | BINARY | z2/HP/Binary/Hero Cards/02 cosmic influx.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 11 | 3 | Fuel the Fire | unique | Event | BINARY | z2/HP/Binary/Hero Cards/04 fuel the fire.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 12 | 5 | Solar Flare | unique | Event | BINARY | z2/HP/Binary/Hero Cards/07 Solar Flare.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 13 | 6 | Energy Torrent | unique | Resource | BINARY | z2/HP/Binary/Hero Cards/09 energy torrent.png | 1500x2150 | 2 |  |
| 14 | 7 | Prophet-Singer | unique | Support | BINARY | z2/HP/Binary/Hero Cards/10 prophet singer.png | 1500x2150 | 1 |  |
| 15 | 1B | Carol Danvers | unique | Alter-Ego | HAND SIZE 5 / HIT POINTS 12 | z3/HP/Binary/0 carol danvers.png | 1500x2150 | 3 |  |
| 16 | 1A | Binary | unique | Hero | HAND SIZE 5 / HIT POINTS 12 | z3/HP/Binary/00 binary hero.png | 1500x2150 | 2 |  |
| 17 | 32 | Rogue | unique | Minion | BINARY NEMESIS | z3/HP/Binary/Encounter Cards/42 rogue nemesis 2.png | 1500x2150 | 3 |  |
| 18 | 240 | Energy Transfer | unique | Treachery | BINARY NEMESIS | z3/HP/Binary/Encounter Cards/45 energy transfer.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 19 | 2 | Cosmic Influx | unique | Event | BINARY | z3/HP/Binary/Hero Cards/01 cosmic influx.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 20 | 3 | Fuel the Fire | unique | Event | BINARY | z3/HP/Binary/Hero Cards/03 fuel the fire.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 21 | 5 | Solar Flare | unique | Event | BINARY | z3/HP/Binary/Hero Cards/08 Solar Flare.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 22 | 9 | Body in Flames | unique | Upgrade | BINARY | z3/HP/Binary/Hero Cards/12 body in flames.png | 1500x2150 | 2 |  |
| 23 | 10 | Energy Conversion | unique | Upgrade | BINARY | z3/HP/Binary/Hero Cards/13 Energy Conversion.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 24 | 10 | Energy Conversion | unique | Upgrade | BINARY | z3/HP/Binary/Hero Cards/14 Energy Conversion.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |

### binary-reskins : deck de départ de Binary : reskins de cartes officielles

| # | N° imprimé | Nom | Face | Type | Aspect / set / bandeau | Source (zip/chemin) | Dim. | [?] | Remarque |
|---|---|---|---|---|---|---|---|---|---|
| 25 | 37 | Defense Specialist | unique | Upgrade | BASIC | z1/HP/Binary/Starter deck_s reskins/Defense Specialist.png | 1500x2150 | 1 | officielle redessinée |
| 26 | 21 | Face the Past | unique | Event | BASIC | z1/HP/Binary/Starter deck_s reskins/Face the Past.png | 1500x2150 | 1 | officielle redessinée |
| 27 | 18 | Follow Through | unique | Upgrade | AGGRESSION | z1/HP/Binary/Starter deck_s reskins/Follow Through.png | 1500x2150 | 1 | officielle redessinée |
| 28 | 15 | Keep Them Busy | unique | Player Side Scheme | AGGRESSION | z1/HP/Binary/Starter deck_s reskins/Keep Them Busy.png | 1500x2150 | 5 | officielle redessinée |
| 29 | 30 | Soaring Acrobatics | unique | Upgrade | BASIC | z1/HP/Binary/Starter deck_s reskins/Soaring Acrobatics.png | 1500x2150 | 1 | officielle redessinée |
| 30 | 14 | Spoiling for a Fight | unique | Event | AGGRESSION | z1/HP/Binary/Starter deck_s reskins/Spoiling for a Fight.png | 1500x2150 | 1 | officielle redessinée |
| 31 | 39 | Surveillance Specialist | unique | Upgrade | BASIC | z1/HP/Binary/Starter deck_s reskins/Surveillance Specialist.png | 1500x2150 | 1 | officielle redessinée |
| 32 | 25 | Energy | unique | Resource | BASIC | z1/HP/Binary/Starter deck_s reskins/energy.png | 1500x2150 | 2 | officielle redessinée |
| 33 | 16 | Hall of Heroes | unique | Support | AGGRESSION | z1/HP/Binary/Starter deck_s reskins/hall of heroes.png | 1500x2150 | 1 | officielle redessinée |
| 34 | 29 | Deft Focus | unique | Upgrade | BASIC | z2/HP/Binary/Starter deck_s reskins/Deft Focus.png | 1500x2150 | 1 | officielle redessinée |
| 35 | 20 | Directed Force | unique | Event | BASIC | z2/HP/Binary/Starter deck_s reskins/Directed Force.png | 1500x2150 | 1 | officielle redessinée |
| 36 | 19 | Marked | unique | Upgrade | AGGRESSION | z2/HP/Binary/Starter deck_s reskins/Marked.png | 1500x2150 | 1 | officielle redessinée |
| 37 | 17 | Aggressive Conditioning | unique | Upgrade | AGGRESSION | z2/HP/Binary/Starter deck_s reskins/aggressive conditioning.png | 1500x2150 | 1 | officielle redessinée |
| 38 | 26 | Genius | unique | Resource | BASIC | z2/HP/Binary/Starter deck_s reskins/genius.png | 1500x2150 | 2 | officielle redessinée |
| 39 | 38 | Front Line Specialist | unique | Upgrade | BASIC | z3/HP/Binary/Starter deck_s reskins/Front Line Specialist.png | 1500x2150 | 1 | officielle redessinée |
| 40 | 12 | Into the Fray | unique | Event | AGGRESSION | z3/HP/Binary/Starter deck_s reskins/Into the Fray.png | 1500x2150 | 1 | officielle redessinée |
| 41 | 13 | Moment of Triumph | unique | Event | AGGRESSION | z3/HP/Binary/Starter deck_s reskins/Moment of Triumph.png | 1500x2150 | 1 | officielle redessinée |
| 42 | 28 | Avengers Mansion | unique | Support | BASIC | z3/HP/Binary/Starter deck_s reskins/avengers mansion.png | 1500x2150 | 1 | officielle redessinée |
| 43 | 36 | Combat Specialist | unique | Upgrade | BASIC | z3/HP/Binary/Starter deck_s reskins/combat specialist.png | 1500x2150 | 1 | officielle redessinée |
| 44 | 22 | Hope Summers | unique | Ally | BASIC | z3/HP/Binary/Starter deck_s reskins/hope summers.png | 1500x2150 | 3 | officielle redessinée |
| 45 | 23 | Nick Fury | unique | Ally | BASIC | z3/HP/Binary/Starter deck_s reskins/nick fury.png | 1500x2150 | 3 | officielle redessinée |
| 46 | 24 | Specialized Training | unique | Player Side Scheme | BASIC | z3/HP/Binary/Starter deck_s reskins/specialized training.png | 1500x2150 | 4 | officielle redessinée |
| 47 | 27 | Strength | unique | Resource | BASIC | z3/HP/Binary/Starter deck_s reskins/strength.png | 1500x2150 | 2 | officielle redessinée |

### quasar : héros Quasar (Protection) : identité, 15 cartes de héros, némésis, obligation

| # | N° imprimé | Nom | Face | Type | Aspect / set / bandeau | Source (zip/chemin) | Dim. | [?] | Remarque |
|---|---|---|---|---|---|---|---|---|---|
| 48 | 99 | Maelstrom | unique | Minion | QUASAR NEMESIS | z1/HP/Quasar/Encounter cards/44 Maelstrom nemesis.png | 1500x2150 | 2 |  |
| 49 | 239 | Entropy Ascendant | unique | Side Scheme | QUASAR NEMESIS | z1/HP/Quasar/Encounter cards/45 Entropy Ascendant.png | 1500x2150 | 6 |  |
| 50 | 240 | Distant Manipulation | unique | Treachery | QUASAR NEMESIS | z1/HP/Quasar/Encounter cards/47 distant manipulation.png | 1500x2150 | 0 | exemplaire multiple (x2, même n° et même nom) |
| 51 | 240 | Distant Manipulation | unique | Treachery | QUASAR NEMESIS | z1/HP/Quasar/Encounter cards/48 distant manipulation.png | 1500x2150 | 0 | exemplaire multiple (x2, même n° et même nom) |
| 52 | 4 | No Holding Back | unique | Event | QUASAR | z1/HP/Quasar/Hero cards/06 No Holding Back.png | 1500x2150 | 6 | exemplaire multiple (x2, même n° et même nom) |
| 53 | 4 | Quantum Absorption | unique | Upgrade | QUASAR | z1/HP/Quasar/Hero cards/13 Quantum Absorption.png | 1500x2150 | 3 |  |
| 54 | 4 | Quantum Jump | unique | Upgrade | QUASAR | z1/HP/Quasar/Hero cards/15 Quantum Jump.png | 1500x2150 | 5 |  |
| 55 | 4 | Quantum Bands | unique | Upgrade | QUASAR | z2/HP/Quasar/01 quantum Bands.png | 1500x2150 | 5 |  |
| 56 | 65 | Protector of the Universe | unique | Obligation | QUASAR | z2/HP/Quasar/Encounter cards/43 protector of the universe.png | 1500x2150 | 0 |  |
| 57 | aucun | Quasar | unique | Image non-carte | aucun | z2/HP/Quasar/Extra/starter deck Quasar.png | 1500x2150 | 0 | HORS CARTE (livret de deck ou insert) |
| 58 | 4 | Epoch | unique | Ally | QUASAR | z2/HP/Quasar/Hero cards/02 epoch.png | 1500x2150 | 10 |  |
| 59 | 4 | Flight of Light | unique | Event | QUASAR | z2/HP/Quasar/Hero cards/03 flight of light.png | 1500x2150 | 3 | exemplaire multiple (x2, même n° et même nom) |
| 60 | 4 | Flight of Light | unique | Event | QUASAR | z2/HP/Quasar/Hero cards/04 flight of light.png | 1500x2150 | 3 | exemplaire multiple (x2, même n° et même nom) |
| 61 | 4 | Righteous Fury | unique | Event | QUASAR | z2/HP/Quasar/Hero cards/08 Righteous Fury.png | 1500x2150 | 4 | exemplaire multiple (x2, même n° et même nom) |
| 62 | 4 | Unbreakable Guard | unique | Event | QUASAR | z2/HP/Quasar/Hero cards/10 Unbreakable Guard.png | 1500x2150 | 4 | exemplaire multiple (x2, même n° et même nom) |
| 63 | 4 | Quantum Energy | unique | Resource | QUASAR | z2/HP/Quasar/Hero cards/11 quantum enegry.png | 1500x2150 | 4 | exemplaire multiple (x2, même n° et même nom) |
| 64 | 4 | Wendell Vaughn | unique | Alter-Ego | HAND SIZE 6 / HIT POINTS 11 | z3/HP/Quasar/0 Wendell Vaughn.png | 1500x2150 | 2 |  |
| 65 | 4 | Quasar | unique | Hero | HAND SIZE 5 / HIT POINTS 11 | z3/HP/Quasar/00 quasar 2.png | 1500x2150 | 2 |  |
| 66 | 237 | Avatar of Oblivion | unique | Attachment | QUASAR NEMESIS | z3/HP/Quasar/Encounter cards/46 avatar of oblivion.png | 1500x2150 | 0 |  |
| 67 | 4 | No Holding Back | unique | Event | QUASAR | z3/HP/Quasar/Hero cards/05 No Holding Back.png | 1500x2150 | 6 | exemplaire multiple (x2, même n° et même nom) |
| 68 | 4 | Righteous Fury | unique | Event | QUASAR | z3/HP/Quasar/Hero cards/07 Righteous Fury.png | 1500x2150 | 4 | exemplaire multiple (x2, même n° et même nom) |
| 69 | 4 | Unbreakable Guard | unique | Event | QUASAR | z3/HP/Quasar/Hero cards/09 Unbreakable Guard.png | 1500x2150 | 4 | exemplaire multiple (x2, même n° et même nom) |
| 70 | 4 | Quantum Energy | unique | Resource | QUASAR | z3/HP/Quasar/Hero cards/12 quantum enegry.png | 1500x2150 | 3 | exemplaire multiple (x2, même n° et même nom) |
| 71 | 49 | Quantum Bubble | unique | Upgrade | QUASAR | z3/HP/Quasar/Hero cards/14 Quantum Bubble.png | 1500x2150 | 4 |  |
| 72 | 4 | Quantum Weapon | unique | Upgrade | QUASAR | z3/HP/Quasar/Hero cards/16 quantum Weapon.png | 1500x2150 | 4 |  |

### quasar-reskins : deck de départ de Quasar : reskins de cartes officielles

| # | N° imprimé | Nom | Face | Type | Aspect / set / bandeau | Source (zip/chemin) | Dim. | [?] | Remarque |
|---|---|---|---|---|---|---|---|---|---|
| 73 | 57 | Defensive Conditioning | unique | Upgrade | PROTECTION / BASIC | z1/HP/Quasar/Starter deck_s reskins/Defensive Conditioning.png | 1500x2150 | 1 | officielle redessinée |
| 74 | 63 | Martinex | unique | Ally | BASIC | z1/HP/Quasar/Starter deck_s reskins/Martinex.png | 1500x2150 | 3 | officielle redessinée |
| 75 | 65 | Energy | unique | Resource | BASIC | z1/HP/Quasar/Starter deck_s reskins/energy.png | 1500x2150 | 2 | officielle redessinée |
| 76 | 66 | Genius | unique | Resource | BASIC | z1/HP/Quasar/Starter deck_s reskins/genius.png | 1500x2150 | 2 | officielle redessinée |
| 77 | 69 | Honorary Guardian | unique | Upgrade | BASIC | z1/HP/Quasar/Starter deck_s reskins/honorary guardian.png | 1500x2150 | 1 | officielle redessinée |
| 78 | 68 | Knowhere | unique | Support | BASIC | z1/HP/Quasar/Starter deck_s reskins/knowhere.png | 1500x2150 | 1 | officielle redessinée |
| 79 | 56 | Change of Fortune | unique | Upgrade | PROTECTION | z2/HP/Quasar/Starter deck_s reskins/Change of Fortune.png | 1500x2150 | 1 | officielle redessinée |
| 80 | 53 | Starhawk | unique | Ally | PROTECTION | z2/HP/Quasar/Starter deck_s reskins/Starhawk.png | 1500x2150 | 1 | officielle redessinée |
| 81 | 59 | Unflappable | unique | Upgrade | PROTECTION | z2/HP/Quasar/Starter deck_s reskins/Unflappable.png | 1500x2150 | 1 | officielle redessinée |
| 82 | 60 | Cosmo | unique | Ally | BASIC | z2/HP/Quasar/Starter deck_s reskins/cosmo.png | 1500x2150 | 3 | officielle redessinée |
| 83 | 61 | Drax | unique | Ally | BASIC | z2/HP/Quasar/Starter deck_s reskins/drax.png | 1500x2150 | 1 | officielle redessinée |
| 84 | 64 | Multitalented | unique | Event | BASIC | z2/HP/Quasar/Starter deck_s reskins/multitalented.png | 1500x2150 | 4 | officielle redessinée |
| 85 | 55 | Powerful Punch | unique | Event | PROTECTION | z2/HP/Quasar/Starter deck_s reskins/powerful punch.png | 1500x2150 | 1 | officielle redessinée |
| 86 | 70 | S.H.I.E.L.D. Deputy | unique | Upgrade | BASIC | z2/HP/Quasar/Starter deck_s reskins/shield deputy.png | 1500x2150 | 1 | officielle redessinée |
| 87 | 52 | Martyr | unique | Ally | PROTECTION | z3/HP/Quasar/Starter deck_s reskins/Martyr.png | 1500x2150 | 1 | officielle redessinée |
| 88 | 54 | Desperate Defense | unique | Event | PROTECTION | z3/HP/Quasar/Starter deck_s reskins/desperate defense.png | 1500x2150 | 1 | officielle redessinée |
| 89 | 58 | Electrostatic Armor | unique | Upgrade | PROTECTION | z3/HP/Quasar/Starter deck_s reskins/electrostatic armor.png | 1500x2150 | 1 | officielle redessinée |
| 90 | 62 | Gamora | unique | Ally | BASIC | z3/HP/Quasar/Starter deck_s reskins/gamora.png | 1500x2150 | 1 | officielle redessinée |
| 91 | 67 | Strength | unique | Resource | BASIC | z3/HP/Quasar/Starter deck_s reskins/strength.png | 1500x2150 | 2 | officielle redessinée |

### kree-sentry : scénario 1, Kree Sentry

| # | N° imprimé | Nom | Face | Type | Aspect / set / bandeau | Source (zip/chemin) | Dim. | [?] | Remarque |
|---|---|---|---|---|---|---|---|---|---|
| 92 | 83 | Optic Blast Cannon | unique | Attachment | KREE SENTRY | z1/SP/Kree Sentry/Encounter cards/09 optic blast cannon.png | 1500x2150 | 4 |  |
| 93 | 84 | Repulsor Blast Unit | unique | Attachment | KREE SENTRY | z1/SP/Kree Sentry/Encounter cards/11 repulsor blast unit.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 94 | 85 | Death Grip | unique | Side Scheme | KREE SENTRY | z1/SP/Kree Sentry/Encounter cards/12 Grip of Annihilation.png | 1500x2150 | 4 |  |
| 95 | 86 | Locking on Target | unique | Side Scheme | KREE SENTRY | z1/SP/Kree Sentry/Encounter cards/13 Locking on Target.png | 1500x2150 | 6 | exemplaire multiple (x2, même n° et même nom) |
| 96 | 86 | Locking on Target | unique | Side Scheme | KREE SENTRY | z1/SP/Kree Sentry/Encounter cards/14 Locking on Target.png | 1500x2150 | 6 | exemplaire multiple (x2, même n° et même nom) |
| 97 | 87 | Outpost Collapse Protocol | unique | Side Scheme | KREE SENTRY | z1/SP/Kree Sentry/Encounter cards/15 lair collapse protocol.png | 1500x2150 | 4 |  |
| 98 | 90 | Intruder Elimination | unique | Treachery | KREE SENTRY | z1/SP/Kree Sentry/Encounter cards/20 intruder elimination.png | 1500x2150 | 1 | exemplaire multiple (x2, même n° et même nom) |
| 99 | 76 | Kree Sentry | I | Villain | KREE SENTRY | z1/SP/Kree Sentry/Setup cards/01 kree sentry I.png | 1500x2150 | 2 |  |
| 100 | 79B | Sentry Awakens | 1B | Main Scheme | KREE SENTRY | z1/SP/Kree Sentry/Setup cards/04 sentry awakens IB.png | 1500x2150 | 5 |  |
| 101 | 82 | Sentry's Grasp | unique | Attachment | KREE SENTRY | z1/SP/Kree Sentry/Setup cards/08 sentry_s grasp.png | 1500x2150 | 0 | exemplaire multiple (x2, même n° et même nom) |
| 102 | 84 | Repulsor Blast Unit | unique | Attachment | KREE SENTRY | z2/SP/Kree Sentry/Encounter cards/10 repulsor blast unit.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 103 | 88 | "Gotcha!" | unique | Treachery | KREE SENTRY | z2/SP/Kree Sentry/Encounter cards/17 Gotcha.png | 1500x2150 | 1 | exemplaire multiple (x2, même n° et même nom) |
| 104 | 89 | Caught in Its Sights | unique | Treachery | KREE SENTRY | z2/SP/Kree Sentry/Encounter cards/18 caught in their sights.png | 1500x2150 | 1 | exemplaire multiple (x2, même n° et même nom) |
| 105 | 77 | Kree Sentry | II | Villain | KREE SENTRY | z2/SP/Kree Sentry/Setup cards/02 kree sentry II.png | 1500x2150 | 2 |  |
| 106 | 79A | Sentry Awakens | 1A | Main Scheme | KREE SENTRY | z2/SP/Kree Sentry/Setup cards/04 sentry awakens IA.png | 1500x2150 | 1 |  |
| 107 | 80A | Self-Destruct Sequence | 2A | Main Scheme | KREE SENTRY | z2/SP/Kree Sentry/Setup cards/05 Self-Destruct Protocol IIA.png | 1500x2150 | 3 |  |
| 108 | 80B | Self-Destruct Sequence | 2B | Main Scheme | KREE SENTRY | z2/SP/Kree Sentry/Setup cards/05 Self-Destruct Protocol IIB.png | 1500x2150 | 6 |  |
| 109 | 81 | Rick Jones |  | Ally | KREE SENTRY | z2/SP/Kree Sentry/Setup cards/06 rick jones.png | 1500x2150 | 6 |  |
| 110 | 88 | "Gotcha!" | unique | Treachery | KREE SENTRY | z3/SP/Kree Sentry/Encounter cards/16 Gotcha.png | 1500x2150 | 1 | exemplaire multiple (x2, même n° et même nom) |
| 111 | 89 | Caught in Its Sights | unique | Treachery | KREE SENTRY | z3/SP/Kree Sentry/Encounter cards/19 caught in their sights.png | 1500x2150 | 1 | exemplaire multiple (x2, même n° et même nom) |
| 112 | 90 | Intruder Elimination | unique | Treachery | KREE SENTRY | z3/SP/Kree Sentry/Encounter cards/21 intruder elimination.png | 1500x2150 | 1 | exemplaire multiple (x2, même n° et même nom) |
| 113 | 78 | Kree Sentry | III | Villain | KREE SENTRY | z3/SP/Kree Sentry/Setup cards/03 kree sentry III.png | 1500x2150 | 2 |  |
| 114 | 82 | Sentry's Grasp | unique | Attachment | KREE SENTRY | z3/SP/Kree Sentry/Setup cards/07 sentry_s grasp.png | 1500x2150 | 0 | exemplaire multiple (x2, même n° et même nom) |

### majestrix-verdict : scénario 2, Majestrix's Verdict (+ Starjammers)

| # | N° imprimé | Nom | Face | Type | Aspect / set / bandeau | Source (zip/chemin) | Dim. | [?] | Remarque |
|---|---|---|---|---|---|---|---|---|---|
| 115 | 129 | Shi'ar Javelin | unique | attachment | MAJESTRIX'S VERDICT | z1/SP/Majestrix_s Verdict/Encounter cards/16 Shi_ar Javelin.png | 1500x2150 | 6 | exemplaire multiple (x2, même n° et même nom) |
| 116 | 129 | Shi'ar Javelin | unique | attachment | MAJESTRIX'S VERDICT | z1/SP/Majestrix_s Verdict/Encounter cards/17 Shi_ar Javelin.png | 1500x2150 | 6 | exemplaire multiple (x2, même n° et même nom) |
| 117 | 130 | Araki | unique | minion | MAJESTRIX'S VERDICT | z1/SP/Majestrix_s Verdict/Encounter cards/18 araki.png | 1500x2150 | 3 |  |
| 118 | 131 | Jailor of Chandilar | unique | minion | MAJESTRIX'S VERDICT | z1/SP/Majestrix_s Verdict/Encounter cards/20 Jailor of Chandilar.png | 1500x2150 | 4 | exemplaire multiple (x4, même n° et même nom) |
| 119 | 131 | Jailor of Chandilar | unique | minion | MAJESTRIX'S VERDICT | z1/SP/Majestrix_s Verdict/Encounter cards/22 Jailor of Chandilar.png | 1500x2150 | 4 | exemplaire multiple (x4, même n° et même nom) |
| 120 | 133 | Tapping the M'kraan Force | unique | side scheme | MAJESTRIX'S VERDICT | z1/SP/Majestrix_s Verdict/Encounter cards/24 Tapping the M_kraan Force.png | 1500x2150 | 7 |  |
| 121 | 134 | Tortured Prisoners | unique | side scheme | MAJESTRIX'S VERDICT | z1/SP/Majestrix_s Verdict/Encounter cards/25 Tortured Prisoners.png | 1500x2150 | 7 |  |
| 122 | 136 | Exemplar Punishment | unique | treachery | MAJESTRIX'S VERDICT | z1/SP/Majestrix_s Verdict/Encounter cards/28 Exemplar Punishment.png | 1500x2150 | 1 | exemplaire multiple (x2, même n° et même nom) |
| 123 | 137 | Sister's Deception | unique | treachery | MAJESTRIX'S VERDICT | z1/SP/Majestrix_s Verdict/Encounter cards/31 Sister_s Deception.png | 1500x2150 | 1 | exemplaire multiple (x2, même n° et même nom) |
| 124 | 122 | Ch'od | unique | ally | BASIC / MAJESTRIX'S VERDICT | z1/SP/Majestrix_s Verdict/Starjammers/09 Ch_od.png | 1500x2150 | 4 |  |
| 125 | 125 | Korvus | unique | ally | BASIC / MAJESTRIX'S VERDICT | z1/SP/Majestrix_s Verdict/Starjammers/12 korvus.png | 1500x2150 | 6 |  |
| 126 | 128 | Shi'ar Crest | unique | attachment | MAJESTRIX'S VERDICT | z2/SP/Majestrix_s Verdict/Encounter cards/15 Shi_ar crest.png | 1500x2150 | 5 |  |
| 127 | 132 | Private Audience | unique | side scheme | MAJESTRIX'S VERDICT | z2/SP/Majestrix_s Verdict/Encounter cards/23 Private Audience.png | 1500x2150 | 4 |  |
| 128 | 135 | Birthright to the Throne | unique | treachery | MAJESTRIX'S VERDICT | z2/SP/Majestrix_s Verdict/Encounter cards/26 Birthright to the Throne.png | 1500x2150 | 4 | exemplaire multiple (x2, même n° et même nom) |
| 129 | 136 | Exemplar Punishment | unique | treachery | MAJESTRIX'S VERDICT | z2/SP/Majestrix_s Verdict/Encounter cards/29 Exemplar Punishment.png | 1500x2150 | 1 | exemplaire multiple (x2, même n° et même nom) |
| 130 | 123 | Corsair | unique | ally | BASIC / MAJESTRIX'S VERDICT | z2/SP/Majestrix_s Verdict/Starjammers/10 corsair.png | 1500x2150 | 6 |  |
| 131 | 127 | Royal Cape of the Shi'ar | unique | attachment | MAJESTRIX'S VERDICT | z3/SP/Majestrix_s Verdict/Encounter cards/14 Royal Cape of the Shi_ar.png | 1500x2150 | 3 |  |
| 132 | 131 | Jailor of Chandilar | unique | minion | MAJESTRIX'S VERDICT | z3/SP/Majestrix_s Verdict/Encounter cards/19 Jailor of Chandilar.png | 1500x2150 | 4 | exemplaire multiple (x4, même n° et même nom) |
| 133 | 131 | Jailor of Chandilar | unique | minion | MAJESTRIX'S VERDICT | z3/SP/Majestrix_s Verdict/Encounter cards/21 Jailor of Chandilar.png | 1500x2150 | 4 | exemplaire multiple (x4, même n° et même nom) |
| 134 | 135 | Birthright to the Throne | unique | treachery | MAJESTRIX'S VERDICT | z3/SP/Majestrix_s Verdict/Encounter cards/27 Birthright to the Throne.png | 1500x2150 | 4 | exemplaire multiple (x2, même n° et même nom) |
| 135 | 137 | Sister's Deception | unique | treachery | MAJESTRIX'S VERDICT | z3/SP/Majestrix_s Verdict/Encounter cards/30 Sister_s Deception.png | 1500x2150 | 1 | exemplaire multiple (x2, même n° et même nom) |
| 136 | 114 | Deathbird | I | villain | MAJESTRIX'S VERDICT | z3/SP/Majestrix_s Verdict/Setup cards/01 Deathbird I.png | 1500x2150 | 4 |  |
| 137 | 117A | Earn the People’s Favor | 1A | main scheme | MAJESTRIX'S VERDICT | z3/SP/Majestrix_s Verdict/Setup cards/04 Earn the People’s Favor IA.png | 1500x2150 | 2 |  |
| 138 | 118A | Majestrix's Verdict | 2A | main scheme | MAJESTRIX'S VERDICT | z3/SP/Majestrix_s Verdict/Setup cards/05 Majestrix_s Verdict IIA.png | 1500x2150 | 0 |  |
| 139 | 119 | Imprisoned on Chandilar | unique | side scheme | MAJESTRIX'S VERDICT | z3/SP/Majestrix_s Verdict/Setup cards/06 Imprisoned on Chandilar.png | 1500x2150 | 0 |  |
| 140 | 120A | Shi'ar Throne | unique | side scheme | MAJESTRIX'S VERDICT | z3/SP/Majestrix_s Verdict/Setup cards/07 Shi_ar Throne side scheme.png | 1500x2150 | 4 |  |
| 141 | 121 | Lilandra | unique | ally | MAJESTRIX'S VERDICT | z3/SP/Majestrix_s Verdict/Starjammers/08 lilandra ally.png | 1500x2150 | 2 |  |
| 142 | 124 | Hepzibah | unique | ally | BASIC / MAJESTRIX'S VERDICT | z3/SP/Majestrix_s Verdict/Starjammers/11 hepzibah.png | 1500x2150 | 6 |  |
| 143 | 126 | Raza | unique | ally | BASIC / MAJESTRIX'S VERDICT | z3/SP/Majestrix_s Verdict/Starjammers/13 raza.png | 1500x2150 | 4 |  |
| 144 | 115 | Deathbird | II | villain | MAJESTRIX'S VERDICT | z4/SP/Majestrix_s Verdict/Setup cards/02 Deathbird II.png | 1500x2150 | 4 |  |
| 145 | 116 | Deathbird | III | villain | MAJESTRIX'S VERDICT | z4/SP/Majestrix_s Verdict/Setup cards/03 Deathbird III.png | 1500x2150 | 4 |  |
| 146 | 117B | Earn the People's Favor | 1B | main scheme | MAJESTRIX'S VERDICT | z4/SP/Majestrix_s Verdict/Setup cards/04 Earn the People’s Favor IB.png | 1500x2150 | 8 |  |
| 147 | 118B | Majestrix's Verdict | 2B | main scheme | MAJESTRIX'S VERDICT | z4/SP/Majestrix_s Verdict/Setup cards/05 Majestrix_s Verdict IIB.png | 1500x2150 | 8 |  |
| 148 | 120B | Shi'ar Throne | unique | support | MAJESTRIX'S VERDICT | z4/SP/Majestrix_s Verdict/Setup cards/07 Shi_ar Throne support.png | 1500x2150 | 2 |  |

### hala-ultimatum : scénario 3, Hala Ultimatum

| # | N° imprimé | Nom | Face | Type | Aspect / set / bandeau | Source (zip/chemin) | Dim. | [?] | Remarque |
|---|---|---|---|---|---|---|---|---|---|
| 149 | 144 | Grand-High Pursuer | unique | Attachment | HALA ULTIMATUM | z1/SP/Hala Ultimatum/Encounter cards/07 grand-high pursuer.png | 1500x2150 | 4 |  |
| 150 | 149 | Kree Soldier | unique | Minion | HALA ULTIMATUM | z1/SP/Hala Ultimatum/Encounter cards/15 kree soldier.png | 1500x2150 | 2 | exemplaire multiple (x4, même n° et même nom) |
| 151 | 149 | Kree Soldier | unique | Minion | HALA ULTIMATUM | z1/SP/Hala Ultimatum/Encounter cards/18 kree soldier.png | 1500x2150 | 2 | exemplaire multiple (x4, même n° et même nom) |
| 152 | 151 | Mobilizing the Empire | unique | Side Scheme | HALA ULTIMATUM | z1/SP/Hala Ultimatum/Encounter cards/21 War Academies of Hala.png | 1500x2150 | 4 | exemplaire multiple (x2, même n° et même nom); nom du fichier différent du nom imprimé |
| 153 | 153 | Advanced Arsenal | unique | Treachery | HALA ULTIMATUM | z1/SP/Hala Ultimatum/Encounter cards/23 advanced arsenal.png | 1500x2150 | 0 | exemplaire multiple (x2, même n° et même nom) |
| 154 | 153 | Advanced Arsenal | unique | Treachery | HALA ULTIMATUM | z1/SP/Hala Ultimatum/Encounter cards/24 advanced arsenal.png | 1500x2150 | 0 | exemplaire multiple (x2, même n° et même nom) |
| 155 | 154 | Battle Cry | unique | Treachery | HALA ULTIMATUM | z1/SP/Hala Ultimatum/Encounter cards/26 battle cry.png | 1500x2150 | 0 | exemplaire multiple (x2, même n° et même nom) |
| 156 | 155 | Bloodthirst of Hala | unique | Treachery | HALA ULTIMATUM | z1/SP/Hala Ultimatum/Encounter cards/28 bloodthirst of hala.png | 1500x2150 | 0 | exemplaire multiple (x2, même n° et même nom) |
| 157 | 145 | Kree Plasma Rifle | unique | Attachment | HALA ULTIMATUM | z2/SP/Hala Ultimatum/Encounter cards/08 kree plasma rifle.png | 1500x2150 | 4 |  |
| 158 | 147 | Kree Assassin | unique | Minion | HALA ULTIMATUM | z2/SP/Hala Ultimatum/Encounter cards/11 kree assassin.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 159 | 148 | Kree Pursuer | unique | Minion | HALA ULTIMATUM | z2/SP/Hala Ultimatum/Encounter cards/13 kree pursuer.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 160 | 148 | Kree Pursuer | unique | Minion | HALA ULTIMATUM | z2/SP/Hala Ultimatum/Encounter cards/14 kree pursuer.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 161 | 150 | House of Fiero | unique | Side Scheme | HALA ULTIMATUM | z2/SP/Hala Ultimatum/Encounter cards/19 House of Fiero.png | 1500x2150 | 4 |  |
| 162 | 151 | Mobilizing the Empire | unique | Side Scheme | HALA ULTIMATUM | z2/SP/Hala Ultimatum/Encounter cards/20 War Academies of Hala.png | 1500x2150 | 4 | exemplaire multiple (x2, même n° et même nom); nom du fichier différent du nom imprimé |
| 163 | 146 | Kree Resilience | unique | Attachment | HALA ULTIMATUM | z3/SP/Hala Ultimatum/Encounter cards/09 kree resilience.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 164 | 146 | Kree Resilience | unique | Attachment | HALA ULTIMATUM | z3/SP/Hala Ultimatum/Encounter cards/10 kree resilience.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 165 | 147 | Kree Assassin | unique | Minion | HALA ULTIMATUM | z3/SP/Hala Ultimatum/Encounter cards/12 kree assassin.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 166 | 149 | Kree Soldier | unique | Minion | HALA ULTIMATUM | z3/SP/Hala Ultimatum/Encounter cards/16 kree soldier.png | 1500x2150 | 2 | exemplaire multiple (x4, même n° et même nom) |
| 167 | 149 | Kree Soldier | unique | Minion | HALA ULTIMATUM | z3/SP/Hala Ultimatum/Encounter cards/17 kree soldier.png | 1500x2150 | 2 | exemplaire multiple (x4, même n° et même nom) |
| 168 | 152 | Secrets of Detention Core | unique | Side Scheme | HALA ULTIMATUM | z3/SP/Hala Ultimatum/Encounter cards/22 detention facility of hala.png | 1500x2150 | 4 |  |
| 169 | 154 | Battle Cry | unique | Treachery | HALA ULTIMATUM | z3/SP/Hala Ultimatum/Encounter cards/25 battle cry.png | 1500x2150 | 0 | exemplaire multiple (x2, même n° et même nom) |
| 170 | 155 | Bloodthirst of Hala | unique | Treachery | HALA ULTIMATUM | z3/SP/Hala Ultimatum/Encounter cards/27 bloodthirst of hala.png | 1500x2150 | 0 | exemplaire multiple (x2, même n° et même nom) |
| 171 | 138A | Kree Leader | I | Villain | HALA ULTIMATUM | z3/SP/Hala Ultimatum/Setup cards/01 Kree Ruler I.png | 1500x2150 | 2 |  |
| 172 | 138B | Tanalth | I | Villain | HALA ULTIMATUM | z3/SP/Hala Ultimatum/Setup cards/01 tanalth I.png | 1500x2150 | 2 |  |
| 173 | 139A | Kree Leader | II | Villain | HALA ULTIMATUM | z3/SP/Hala Ultimatum/Setup cards/02 Kree Ruler II.png | 1500x2150 | 2 |  |
| 174 | 140A | Kree Leader | III | Villain | HALA ULTIMATUM | z3/SP/Hala Ultimatum/Setup cards/03 Kree Ruler III.png | 1500x2150 | 2 |  |
| 175 | 141A | Hidden Might of Hala | 1A | Main Scheme | HALA ULTIMATUM | z3/SP/Hala Ultimatum/Setup cards/04 Hidden on hala IA.png | 1500x2150 | 2 |  |
| 176 | 142B | Reckoning Begins | 2B | Main Scheme | HALA ULTIMATUM | z3/SP/Hala Ultimatum/Setup cards/05 reckoning begins IIB.png | 1500x2150 | 2 |  |
| 177 | 143 | Hala | unique | Environment | HALA ULTIMATUM | z3/SP/Hala Ultimatum/Setup cards/06 Hala.png | 1500x2150 | 1 |  |
| 178 | 139B | Tanalth | II | Villain | HALA ULTIMATUM | z4/SP/Hala Ultimatum/Setup cards/02 tanalth II.png | 1500x2150 | 2 |  |
| 179 | 140B | Tanalth | III | Villain | HALA ULTIMATUM | z4/SP/Hala Ultimatum/Setup cards/03 tanalth III.png | 1500x2150 | 2 |  |
| 180 | 141B | Hidden Might of Hala | 1B | Main Scheme | HALA ULTIMATUM | z4/SP/Hala Ultimatum/Setup cards/04 Hidden on hala IB.png | 1500x2150 | 2 |  |
| 181 | 142A | Reckoning Begins | 2A | Main Scheme | HALA ULTIMATUM | z4/SP/Hala Ultimatum/Setup cards/05 reckoning begins IIA.png | 1500x2150 | 0 |  |

### earth-under-siege : scénario 4, Earth Under Siege (cartes générales, méchants, mise en place, reskins Standard/Expert)

| # | N° imprimé | Nom | Face | Type | Aspect / set / bandeau | Source (zip/chemin) | Dim. | [?] | Remarque |
|---|---|---|---|---|---|---|---|---|---|
| 182 | 190 | Veranke | unique | VILLAIN | VERANKE | z1/SP/Earth Under Siege/Setup Cards/01 veranke.png | 1500x2150 | 5 |  |
| 183 | 177 | Destroyer | unique | VILLAIN | DESTROYER | z1/SP/Earth Under Siege/Setup Cards/02 destroyer II.png | 1500x2150 | 5 |  |
| 184 | aucun | Assault | unique | TREACHERY | STANDARD | z1/SP/Earth Under Siege/Standard-Expert reskins/03 assault.png | 1500x2150 | 0 | exemplaire multiple (x2, même n° et même nom) |
| 185 | aucun | Assault | unique | TREACHERY | STANDARD | z1/SP/Earth Under Siege/Standard-Expert reskins/04 assault.png | 1500x2150 | 0 | exemplaire multiple (x2, même n° et même nom) |
| 186 | aucun | Shadow of the Past | unique | TREACHERY | STANDARD | z1/SP/Earth Under Siege/Standard-Expert reskins/07 shadows of the past.png | 1500x2150 | 3 |  |
| 187 | aucun | Exhaustion | unique | TREACHERY | EXPERT | z1/SP/Earth Under Siege/Standard-Expert reskins/08 exhaustion.png | 1500x2150 | 3 |  |
| 188 | 163 | Main Concern | unique | ATTACHMENT | EARTH UNDER SIEGE | z2/SP/Earth Under Siege/Encounter Cards/03 main concern.png | 1500x2150 | 4 |  |
| 189 | 164 | Observe the Perimeter | unique | OBLIGATION | EARTH UNDER SIEGE | z2/SP/Earth Under Siege/Encounter Cards/04 observe the perimeter.png | 1500x2150 | 6 |  |
| 190 | 166 | Annihilus | unique | VILLAIN | ANNIHILUS | z2/SP/Earth Under Siege/Setup Cards/01 annihilus.png | 1500x2150 | 5 |  |
| 191 | 181 | Doctor Minerva | unique | VILLAIN | DOCTOR MINERVA | z2/SP/Earth Under Siege/Setup Cards/01 doctor minerva.png | 1500x2150 | 5 |  |
| 192 | 167 | Annihilus | unique | VILLAIN | ANNIHILUS | z2/SP/Earth Under Siege/Setup Cards/02 annihilus II.png | 1500x2150 | 5 |  |
| 193 | 171 | Attuma | unique | VILLAIN | ATTUMA | z2/SP/Earth Under Siege/Setup Cards/02 attuma II.png | 1500x2150 | 5 |  |
| 194 | 182 | Doctor Minerva | unique | VILLAIN | DOCTOR MINERVA | z2/SP/Earth Under Siege/Setup Cards/02 doctor minerva II.png | 1500x2150 | 5 |  |
| 195 | 187 | Mole Man | unique | VILLAIN | MOLE MAN | z2/SP/Earth Under Siege/Setup Cards/02 mole man II.png | 1500x2150 | 5 |  |
| 196 | aucun | Advance | unique | TREACHERY | STANDARD | z2/SP/Earth Under Siege/Standard-Expert reskins/02 advance.png | 1500x2150 | 0 | exemplaire multiple (x2, même n° et même nom) |
| 197 | aucun | Caught Off Guard | unique | TREACHERY | STANDARD | z2/SP/Earth Under Siege/Standard-Expert reskins/05 Caught Off Guard.png | 1500x2150 | 2 |  |
| 198 | aucun | Masterplan | unique | TREACHERY | EXPERT | z2/SP/Earth Under Siege/Standard-Expert reskins/09 masterplan.png | 1500x2150 | 3 |  |
| 199 | 165 | Threat on the Horizon | unique | TREACHERY | EARTH UNDER SIEGE | z3/SP/Earth Under Siege/Encounter Cards/05 threat on the horizon.png | 1500x2150 | 0 | exemplaire multiple (x2, même n° et même nom) |
| 200 | 165 | Threat on the Horizon | unique | TREACHERY | EARTH UNDER SIEGE | z3/SP/Earth Under Siege/Encounter Cards/06 threat on the horizon.png | 1500x2150 | 0 | exemplaire multiple (x2, même n° et même nom) |
| 201 | 161A | Earthfall | A | MAIN SCHEME | EARTH UNDER SIEGE | z3/SP/Earth Under Siege/Setup Cards/00 Earthfall 1A.png | 1500x2150 | 0 |  |
| 202 | 161B | Earthfall | B | MAIN SCHEME | EARTH UNDER SIEGE | z3/SP/Earth Under Siege/Setup Cards/00 Earthfall 1B ALT.png | 1500x2150 | 5 |  |
| 203 | 162B | Enemies at Large | B | SIDE SCHEME | EARTH UNDER SIEGE | z3/SP/Earth Under Siege/Setup Cards/00 enemies at surge expert ALT.png | 1500x2150 | 5 |  |
| 204 | 162A | Enemies at Large | A | SIDE SCHEME | EARTH UNDER SIEGE | z3/SP/Earth Under Siege/Setup Cards/00 enemies at surge standard ALT.png | 1500x2150 | 5 |  |
| 205 | 170 | Attuma | unique | VILLAIN | ATTUMA | z3/SP/Earth Under Siege/Setup Cards/01 attuma.png | 1500x2150 | 5 |  |
| 206 | 176 | Destroyer | unique | VILLAIN | DESTROYER | z3/SP/Earth Under Siege/Setup Cards/01 destroyer.png | 1500x2150 | 5 |  |
| 207 | 186 | Mole Man | unique | VILLAIN | MOLE MAN | z3/SP/Earth Under Siege/Setup Cards/01 mole man.png | 1500x2150 | 5 |  |
| 208 | 191 | Veranke | unique | VILLAIN | VERANKE | z3/SP/Earth Under Siege/Setup Cards/02 veranke II.png | 1500x2150 | 5 |  |
| 209 | aucun | Advance | unique | TREACHERY | STANDARD | z3/SP/Earth Under Siege/Standard-Expert reskins/01 advance.png | 1500x2150 | 0 | exemplaire multiple (x2, même n° et même nom) |
| 210 | aucun | Gang-Up | unique | TREACHERY | STANDARD | z3/SP/Earth Under Siege/Standard-Expert reskins/06 Gang-up.png | 1500x2150 | 2 |  |
| 211 | aucun | Under Fire | unique | TREACHERY | EXPERT | z3/SP/Earth Under Siege/Standard-Expert reskins/10 under fire.png | 1500x2150 | 4 |  |

### earth-under-siege-ensembles : scénario 4, ensembles de rencontre des 6 méchants

| # | N° imprimé | Nom | Face | Type | Aspect / set / bandeau | Source (zip/chemin) | Dim. | [?] | Remarque |
|---|---|---|---|---|---|---|---|---|---|
| 212 | 168 | Portal to the Negative Zone | unique | side scheme | ANNIHILUS | z1/SP/Earth Under Siege/Annihilus encounter cards/03 portal to the negative zone.png | 1500x2150 | 4 |  |
| 213 | 169 | Annihilation Wave | unique | treachery | ANNIHILUS | z1/SP/Earth Under Siege/Annihilus encounter cards/06 annihilation wave.png | 1500x2150 | 1 | exemplaire multiple (x3, même n° et même nom) |
| 214 | 174 | Andromeda | unique | minion | (le symbole + precede le nom). ATTUMA | z1/SP/Earth Under Siege/Attuma encounter cards/05 andromeda.png | 1500x2150 | 5 |  |
| 215 | 179 | Programmed to Obliterate | unique | side scheme | DESTROYER | z1/SP/Earth Under Siege/Destroyer encounter cards/04 programmed to obliterate.png | 1500x2150 | 7 |  |
| 216 | 183 | Induced Mutation | unique | attachment | DOCTOR MINERVA | z1/SP/Earth Under Siege/Doctor Minerva encounter cards/03 induced mutation.png | 1500x2150 | 5 | exemplaire multiple (x2, même n° et même nom) |
| 217 | 183 | Induced Mutation | unique | attachment | DOCTOR MINERVA | z1/SP/Earth Under Siege/Doctor Minerva encounter cards/04 induced mutation.png | 1500x2150 | 6 | exemplaire multiple (x2, même n° et même nom) |
| 218 | 185 | Kree Secret Laboratory | unique | side scheme | DOCTOR MINERVA | z1/SP/Earth Under Siege/Doctor Minerva encounter cards/05 kree secret laboratory.png | 1500x2150 | 5 |  |
| 219 | 188 | Moloid | unique | minion | MOLE MAN | z1/SP/Earth Under Siege/Mole Man encounter cards/04 moloid.png | 1500x2150 | 3 | exemplaire multiple (x3, même n° et même nom) |
| 220 | 192 | Arch-Enemy's Face | unique | attachment | VERANKE | z1/SP/Earth Under Siege/Veranke encounter cards/03 arch enemy_s face.png | 1500x2150 | 2 |  |
| 221 | 169 | Annihilation Wave | unique | treachery | ANNIHILUS | z2/SP/Earth Under Siege/Annihilus encounter cards/04 annihilation wave.png | 1500x2150 | 1 | exemplaire multiple (x3, même n° et même nom) |
| 222 | 180 | Pure Destruction | unique | treachery | DESTROYER | z2/SP/Earth Under Siege/Destroyer encounter cards/05 pure destruction.png | 1500x2150 | 4 | exemplaire multiple (x2, même n° et même nom) |
| 223 | 188 | Moloid | unique | minion | MOLE MAN | z2/SP/Earth Under Siege/Mole Man encounter cards/03 moloid.png | 1500x2150 | 3 | exemplaire multiple (x3, même n° et même nom) |
| 224 | 188 | Moloid | unique | minion | MOLE MAN | z2/SP/Earth Under Siege/Mole Man encounter cards/05 moloid.png | 1500x2150 | 3 | exemplaire multiple (x3, même n° et même nom) |
| 225 | 193 | Replaced | unique | attachment | VERANKE | z2/SP/Earth Under Siege/Veranke encounter cards/04 replaced.png | 1500x2150 | 1 | exemplaire multiple (x2, même n° et même nom) |
| 226 | 193 | Replaced | unique | attachment | VERANKE | z2/SP/Earth Under Siege/Veranke encounter cards/05 replaced.png | 1500x2150 | 1 | exemplaire multiple (x2, même n° et même nom) |
| 227 | 169 | Annihilation Wave | unique | treachery | ANNIHILUS | z3/SP/Earth Under Siege/Annihilus encounter cards/05 annihilation wave.png | 1500x2150 | 1 | exemplaire multiple (x3, même n° et même nom) |
| 228 | 172 | Atlantean Amulet | unique | attachment | ATTUMA | z3/SP/Earth Under Siege/Attuma encounter cards/03 Atlantean Amulet.png | 1500x2150 | 5 |  |
| 229 | 173 | Atlantean Battle Gear | unique | attachment | ATTUMA | z3/SP/Earth Under Siege/Attuma encounter cards/04 Atlantean Battle Gear.png | 1500x2150 | 5 |  |
| 230 | 175 | Rising Sea Levels | unique | side scheme | ATTUMA | z3/SP/Earth Under Siege/Attuma encounter cards/06 rising sea levels.png | 1500x2150 | 5 |  |
| 231 | 178 | Uru Armor Plating | unique | attachment | DESTROYER | z3/SP/Earth Under Siege/Destroyer encounter cards/03 uru armor plating.png | 1500x2150 | 1 |  |
| 232 | 180 | Pure Destruction | unique | treachery | DESTROYER | z3/SP/Earth Under Siege/Destroyer encounter cards/06 pure destruction.png | 1500x2150 | 4 | exemplaire multiple (x2, même n° et même nom) |
| 233 | 184 | Captain Atlas | unique | minion | (le symbole + precede le nom). DOCTOR MI | z3/SP/Earth Under Siege/Doctor Minerva encounter cards/05 captain atlas.png | 1500x2150 | 7 |  |
| 234 | 189 | Underground Tremor | unique | treachery | MOLE MAN | z3/SP/Earth Under Siege/Mole Man encounter cards/06 underground tremor.png | 1500x2150 | 1 |  |
| 235 | 194 | Secret Invasion | unique | side scheme | VERANKE | z3/SP/Earth Under Siege/Veranke encounter cards/06 Secret Invasion.png | 1500x2150 | 3 |  |

### supreme-intelligence : scénario 5, Supreme Intelligence

| # | N° imprimé | Nom | Face | Type | Aspect / set / bandeau | Source (zip/chemin) | Dim. | [?] | Remarque |
|---|---|---|---|---|---|---|---|---|---|
| 236 | 201 | Genetic Augmentation | unique | Attachment | SUPREME INTELLIGENCE | z1/SP/Supreme Intelligence/Encounter cards/07 Genetic Augmentation.png | 1500x2150 | 1 | exemplaire multiple (x2, même n° et même nom) |
| 237 | 201 | Genetic Augmentation | unique | Attachment | SUPREME INTELLIGENCE | z1/SP/Supreme Intelligence/Encounter cards/08 Genetic Augmentation.png | 1500x2150 | 1 | exemplaire multiple (x2, même n° et même nom) |
| 238 | 203 | Ren-Varr | unique | Minion | SUPREME INTELLIGENCE | z1/SP/Supreme Intelligence/Encounter cards/13 ren varr.png | 1500x2150 | 6 |  |
| 239 | 204 | Supremor | unique | Minion | SUPREME INTELLIGENCE | z1/SP/Supreme Intelligence/Encounter cards/15 Supremor.png | 1500x2150 | 5 | exemplaire multiple (x2, même n° et même nom) |
| 240 | 207 | Supremor Seed | unique | Side scheme | SUPREME INTELLIGENCE | z1/SP/Supreme Intelligence/Encounter cards/18 Supremor Seed.png | 1500x2150 | 4 | exemplaire multiple (x2, même n° et même nom) |
| 241 | 195 | Supreme Intelligence | I | Villain | SUPREME INTELLIGENCE | z1/SP/Supreme Intelligence/Setup cards/01 supreme intelligence I.png | 1500x2150 | 2 |  |
| 242 | 196 | Supreme Intelligence | II | Villain | SUPREME INTELLIGENCE | z1/SP/Supreme Intelligence/Setup cards/02 supreme intelligence II.png | 1500x2150 | 2 |  |
| 243 | 198A | Protectors of the Kree Empire | 1/A | Main scheme | SUPREME INTELLIGENCE | z1/SP/Supreme Intelligence/Setup cards/04 protectors of the kree empire IA.png | 1500x2150 | 2 |  |
| 244 | 200 | Holding Tank | unique | Attachment | SUPREME INTELLIGENCE | z1/SP/Supreme Intelligence/Setup cards/06 holding tank.png | 1500x2150 | 3 |  |
| 245 | 202 | Kree Infantry | unique | Minion | SUPREME INTELLIGENCE | z2/SP/Supreme Intelligence/Encounter cards/10 kree infantry.png | 1500x2150 | 3 | exemplaire multiple (x4, même n° et même nom) |
| 246 | 204 | Supremor | unique | Minion | SUPREME INTELLIGENCE | z2/SP/Supreme Intelligence/Encounter cards/14 Supremor.png | 1500x2150 | 5 | exemplaire multiple (x2, même n° et même nom) |
| 247 | 206 | Selective Breeding | unique | Side scheme | SUPREME INTELLIGENCE | z2/SP/Supreme Intelligence/Encounter cards/17 selective breeding.png | 1500x2150 | 3 |  |
| 248 | 208 | Summon Reinforcements | unique | Treachery | SUPREME INTELLIGENCE | z2/SP/Supreme Intelligence/Encounter cards/21 summon reinforcements.png | 1500x2150 | 1 | exemplaire multiple (x2, même n° et même nom) |
| 249 | 202 | Kree Infantry | unique | Minion | SUPREME INTELLIGENCE | z3/SP/Supreme Intelligence/Encounter cards/09 kree infantry.png | 1500x2150 | 3 | exemplaire multiple (x4, même n° et même nom) |
| 250 | 202 | Kree Infantry | unique | Minion | SUPREME INTELLIGENCE | z3/SP/Supreme Intelligence/Encounter cards/11 kree infantry.png | 1500x2150 | 3 | exemplaire multiple (x4, même n° et même nom) |
| 251 | 202 | Kree Infantry | unique | Minion | SUPREME INTELLIGENCE | z3/SP/Supreme Intelligence/Encounter cards/12 kree infantry.png | 1500x2150 | 3 | exemplaire multiple (x4, même n° et même nom) |
| 252 | 205 | Loyalty to Supremor | unique | Side scheme | SUPREME INTELLIGENCE | z3/SP/Supreme Intelligence/Encounter cards/16 Loyalty to Supremor.png | 1500x2150 | 4 |  |
| 253 | 207 | Supremor Seed | unique | Side scheme | SUPREME INTELLIGENCE | z3/SP/Supreme Intelligence/Encounter cards/19 Supremor Seed.png | 1500x2150 | 4 | exemplaire multiple (x2, même n° et même nom) |
| 254 | 208 | Summon Reinforcements | unique | Treachery | SUPREME INTELLIGENCE | z3/SP/Supreme Intelligence/Encounter cards/20 summon reinforcements.png | 1500x2150 | 1 | exemplaire multiple (x2, même n° et même nom) |
| 255 | 197 | Supreme Intelligence | III | Villain | SUPREME INTELLIGENCE | z3/SP/Supreme Intelligence/Setup cards/03 supreme intelligence III.png | 1500x2150 | 2 |  |
| 256 | 198B | Protectors of the Kree Empire | 1/B | Main scheme | SUPREME INTELLIGENCE | z3/SP/Supreme Intelligence/Setup cards/04 protectors of the kree empire IB.png | 1500x2150 | 5 |  |
| 257 | 199A | The Endless Mind | 2A | Main scheme | SUPREME INTELLIGENCE | z3/SP/Supreme Intelligence/Setup cards/05 The Endless Mind IIA.png | 1500x2150 | 0 |  |
| 258 | 199B | The Endless Mind | 2B | Main scheme | SUPREME INTELLIGENCE | z3/SP/Supreme Intelligence/Setup cards/05 The Endless Mind IIB.png | 1500x2150 | 3 |  |

### imperial-guard : modulaire Imperial Guard

| # | N° imprimé | Nom | Face | Type | Aspect / set / bandeau | Source (zip/chemin) | Dim. | [?] | Remarque |
|---|---|---|---|---|---|---|---|---|---|
| 259 | 96 | Electron | unique | Minion | IMPERIAL GUARD | z1/MS/Imperial Guard/06 electron.png | 1500x2150 | 2 |  |
| 260 | 97 | Fang | unique | Minion | IMPERIAL GUARD | z1/MS/Imperial Guard/07 Fang.png | 1500x2150 | 2 |  |
| 261 | 103 | Mentor | unique | Minion | IMPERIAL GUARD | z1/MS/Imperial Guard/13 Mentor.png | 1500x2150 | 1 |  |
| 262 | 105 | Nightside | unique | Minion | IMPERIAL GUARD | z1/MS/Imperial Guard/15 Nightside.png | 1500x2150 | 2 |  |
| 263 | 109 | Starbolt | unique | Minion | IMPERIAL GUARD | z1/MS/Imperial Guard/19 starbolt.png | 1500x2150 | 1 |  |
| 264 | 111 | Warstar | unique | Minion | IMPERIAL GUARD | z1/MS/Imperial Guard/21 warstar.png | 1500x2150 | 1 |  |
| 265 | 112 | Guard Assembles | unique | Treachery | IMPERIAL GUARD | z1/MS/Imperial Guard/22 Guard Assembles.png | 1500x2150 | 1 |  |
| 266 | aucun (ce n'est pas une carte : page de regles du set modulaire) | Imperial Guard Modular Set | unique | page de regles | aucun | z1/MS/Imperial Guard/imperial guard insert.png | 1500x2150 | 0 | HORS CARTE (livret de deck ou insert) |
| 267 | 93 | Noble Bearing | unique | Environment | IMPERIAL GUARD | z2/MS/Imperial Guard/03 noble bearing.png | 1500x2150 | 0 |  |
| 268 | 94 | Astra | unique | Minion | IMPERIAL GUARD | z2/MS/Imperial Guard/04 Astra.png | 1500x2150 | 1 |  |
| 269 | 95 | Earthquake | unique | Minion | IMPERIAL GUARD | z2/MS/Imperial Guard/05 earthquake.png | 1500x2150 | 1 |  |
| 270 | 99 | Hobgoblin | unique | Minion | IMPERIAL GUARD | z2/MS/Imperial Guard/09 hobgoblin.png | 1500x2150 | 1 |  |
| 271 | 100 | Hussar | unique | Minion | IMPERIAL GUARD | z2/MS/Imperial Guard/10 Hussar.png | 1500x2150 | 1 |  |
| 272 | 102 | Manta | unique | Minion | IMPERIAL GUARD | z2/MS/Imperial Guard/12 manta.png | 1500x2150 | 1 |  |
| 273 | 106 | Oracle | unique | Minion | IMPERIAL GUARD | z2/MS/Imperial Guard/16 oracle.png | 1500x2150 | 1 |  |
| 274 | 107 | Pulsar | unique | Minion | IMPERIAL GUARD | z2/MS/Imperial Guard/17 pulsar.png | 1500x2150 | 2 |  |
| 275 | 91 | Disciplined Training | unique | Environment | IMPERIAL GUARD | z3/MS/Imperial Guard/01 disciplined training.png | 1500x2150 | 0 |  |
| 276 | 92 | Loyal Devotion | unique | Environment | IMPERIAL GUARD | z3/MS/Imperial Guard/02 Loyal Devotion.png | 1500x2150 | 0 |  |
| 277 | 98 | Gladiator | unique | Minion | IMPERIAL GUARD | z3/MS/Imperial Guard/08 gladiator.png | 1500x2150 | 1 |  |
| 278 | 101 | Magique | unique | Minion | IMPERIAL GUARD | z3/MS/Imperial Guard/11 magique.png | 1500x2150 | 1 |  |
| 279 | 104 | Neutron | unique | Minion | IMPERIAL GUARD | z3/MS/Imperial Guard/14 neutron.png | 1500x2150 | 1 |  |
| 280 | 108 | Smasher | unique | Minion | IMPERIAL GUARD | z3/MS/Imperial Guard/18 smasher.png | 1500x2150 | 1 |  |
| 281 | 110 | Titan | unique | Minion | IMPERIAL GUARD | z3/MS/Imperial Guard/20 titan.png | 1500x2150 | 1 |  |
| 282 | 113 | Imperial Formation | unique | Treachery | IMPERIAL GUARD | z3/MS/Imperial Guard/23 imperial formation.png | 1500x2150 | 0 |  |

### modular-sets : modulaires Accuser Corps, Nega Bomb, Seeds of Corruption, Starforce

| # | N° imprimé | Nom | Face | Type | Aspect / set / bandeau | Source (zip/chemin) | Dim. | [?] | Remarque |
|---|---|---|---|---|---|---|---|---|---|
| 283 | 157 | Universal Weapon | unique | Attachment | ACCUSER CORPS | z1/MS/Accuser Corps/02 universal weapon.png | 1500x2150 | 1 |  |
| 284 | 158 | Unwavering | unique | Attachment | ACCUSER CORPS | z1/MS/Accuser Corps/03 unwavering.png | 1500x2150 | 1 | exemplaire multiple (x2, même n° et même nom) |
| 285 | 158 | Unwavering | unique | Attachment | ACCUSER CORPS | z1/MS/Accuser Corps/04 unwavering.png | 1500x2150 | 1 | exemplaire multiple (x2, même n° et même nom) |
| 286 | 159 | Kree Accuser | unique | Minion | ACCUSER CORPS | z1/MS/Accuser Corps/05 kree accuser.png | 1500x2150 | 1 | exemplaire multiple (x2, même n° et même nom) |
| 287 | 159 | Kree Accuser | unique | Minion | ACCUSER CORPS | z1/MS/Accuser Corps/06 kree accuser.png | 1500x2150 | 1 | exemplaire multiple (x2, même n° et même nom) |
| 288 | 222B | Detonation | unique | Environment | NEGA-BOMB | z1/MS/Nega Bomb/01 Detonation.png | 1500x2150 | 0 |  |
| 289 | aucun | (pas de carte | unique | page de regles / livre | aucun | z1/MS/Nega Bomb/nega bomb insert.png | 1500x2150 | 0 | HORS CARTE (livret de deck ou insert) |
| 290 | 221 | Whisper in the Mind | unique | Treachery | SEEDS OF CORRUPTION | z1/MS/Seeds of Corruption/07 Whisper in the Mind.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 291 | 209 | Cadmi-M the Pursuer | : le nom est | Minion | STARFORCE | z1/MS/Starforce/01 Cadmi M.png | 1500x2150 | 1 |  |
| 292 | 210 | Doctor Minerva | : symbole en | Minion | STARFORCE | z1/MS/Starforce/02 Doctor Minerva.png | 1500x2150 | 1 |  |
| 293 | 213 | Protector | : symbole en | Minion | STARFORCE | z1/MS/Starforce/05 protector.png | 1500x2150 | 1 |  |
| 294 | 214 | Ronan the Accuser | : symbole en | Minion | STARFORCE | z1/MS/Starforce/06 ronan.png | 1500x2150 | 1 |  |
| 295 | 216 | Ultimus | : symbole en | Minion | STARFORCE | z1/MS/Starforce/08 ultimus.png | 1500x2150 | 1 |  |
| 296 | 222A | Nega-Bomb | unique. Cart | Side Scheme | NEGA-BOMB | z2/MS/Nega Bomb/01 nega bomb.png | 1500x2150 | 2 |  |
| 297 | 223 | Green Interference | unique | Treachery | NEGA-BOMB | z2/MS/Nega Bomb/03 Green Interference.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 298 | 218 | Manipulated Memories | unique | Attachment | SEEDS OF CORRUPTION | z2/MS/Seeds of Corruption/01 Manipulated Memories.png | 1500x2150 | 3 | exemplaire multiple (x2, même n° et même nom) |
| 299 | 218 | Manipulated Memories | unique | Attachment | SEEDS OF CORRUPTION | z2/MS/Seeds of Corruption/02 Manipulated Memories.png | 1500x2150 | 3 | exemplaire multiple (x2, même n° et même nom) |
| 300 | 219 | Psychic Shackles | unique. Cart | Side Scheme | SEEDS OF CORRUPTION | z2/MS/Seeds of Corruption/03 Psychic Shackles.png | 1500x2150 | 3 |  |
| 301 | 220 | Mental Torture | unique | Treachery | SEEDS OF CORRUPTION | z2/MS/Seeds of Corruption/04 Mental Torture.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 302 | 212 | Korath the Pursuer | : symbole en | Minion | STARFORCE | z2/MS/Starforce/04 Korath the Pursuer.png | 1500x2150 | 1 |  |
| 303 | 215 | Shatterax | : symbole en | Minion | STARFORCE | z2/MS/Starforce/07 shatterax.png | 1500x2150 | 1 |  |
| 304 | 217 | Starformation | unique | Treachery | STARFORCE | z2/MS/Starforce/09 starformation.png | 1500x2150 | 1 |  |
| 305 | 156 | The Accused | unique | Attachment | ACCUSER CORPS | z3/MS/Accuser Corps/01 the accused.png | 1500x2150 | 1 |  |
| 306 | 160 | Judgement Day | unique | Treachery | ACCUSER CORPS | z3/MS/Accuser Corps/07 judgement day.png | 1500x2150 | 1 |  |
| 307 | 223 | Green Interference | unique | Treachery | NEGA-BOMB | z3/MS/Nega Bomb/02 Green Interference.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 308 | 220 | Mental Torture | unique | Treachery | SEEDS OF CORRUPTION | z3/MS/Seeds of Corruption/05 Mental Torture.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 309 | 221 | Whisper in the Mind | unique | Treachery | SEEDS OF CORRUPTION | z3/MS/Seeds of Corruption/06 Whisper in the Mind.png | 1500x2150 | 2 | exemplaire multiple (x2, même n° et même nom) |
| 310 | 211 | Inndig-O the Accuser | : symbole en | Minion | STARFORCE | z3/MS/Starforce/03 Inndig-O the Accuser.png | 1500x2150 | 1 |  |

### campagne : cartes de campagne 224-236

| # | N° imprimé | Nom | Face | Type | Aspect / set / bandeau | Source (zip/chemin) | Dim. | [?] | Remarque |
|---|---|---|---|---|---|---|---|---|---|
| 311 | 230 | Doctor Pym | unique | Ally | IDENTITY-SPECIFIC / CAMPAIGN | z1/Campaigns/Galactic Storm/Identity-specific campaign allies/Doctor Pym ally.png | 1500x2150 | 5 |  |
| 312 | 236 | Thor | unique | Ally | IDENTITY-SPECIFIC / CAMPAIGN | z1/Campaigns/Galactic Storm/Identity-specific campaign allies/Thor ally.png | 1500x2150 | 8 |  |
| 313 | 227 | Binary | unique | Ally | IDENTITY-SPECIFIC / CAMPAIGN | z1/Campaigns/Galactic Storm/Identity-specific campaign allies/binary ally.png | 1500x2150 | 9 |  |
| 314 | 229 | Crystal | unique | Ally | IDENTITY-SPECIFIC / CAMPAIGN | z1/Campaigns/Galactic Storm/Identity-specific campaign allies/crystal ally.png | 1500x2150 | 11 |  |
| 315 | 232 | Her | unique | Ally | IDENTITY-SPECIFIC / CAMPAIGN | z1/Campaigns/Galactic Storm/Identity-specific campaign allies/her ally.png | 1500x2150 | 7 |  |
| 316 | 224 | Rick Jones | unique | Ally | BASIC / CAMPAIGN | z2/Campaigns/Galactic Storm/Campaign allies/01 Rick Jones ally.png | 1500x2150 | 6 |  |
| 317 | 228 | Captain Marvel | unique | Ally | IDENTITY-SPECIFIC / CAMPAIGN | z2/Campaigns/Galactic Storm/Identity-specific campaign allies/Captain Marvel ally.png | 1500x2150 | 10 |  |
| 318 | 233 | Living Lightning | unique | Ally | IDENTITY-SPECIFIC / CAMPAIGN | z2/Campaigns/Galactic Storm/Identity-specific campaign allies/Living Lightning ally.png | 1500x2150 | 9 |  |
| 319 | 234 | Sersi | unique | Ally | IDENTITY-SPECIFIC / CAMPAIGN | z2/Campaigns/Galactic Storm/Identity-specific campaign allies/sersi ally.png | 1500x2150 | 9 |  |
| 320 | 235 | Spider-Woman | unique | Ally | IDENTITY-SPECIFIC / CAMPAIGN | z2/Campaigns/Galactic Storm/Identity-specific campaign allies/spider-woman.png | 1500x2150 | 8 |  |
| 321 | 225 | Gladiator | unique | Ally | BASIC / CAMPAIGN | z3/Campaigns/Galactic Storm/Campaign allies/02 gladiator ally.png | 1500x2150 | 7 |  |
| 322 | 231 | Goliath | unique | Ally | IDENTITY-SPECIFIC / CAMPAIGN | z3/Campaigns/Galactic Storm/Identity-specific campaign allies/Goliath ally.png | 1500x2150 | 7 |  |
| 323 | 226 | Lauri-Ell | unique | Ally | BASIC / CAMPAIGN | z2/Campaigns/Galactic Storm/Campaign allies/03 Lauri Ell ally.png | 1500x2150 | 12 |  |