# Aspect TMNT Basic (`ub`, pack `tmnt_aspect_basic`) : gabarits PROCESSUS-CARTE

16/10/2026, branche `aspects-ub`. 59 scans (`tools/tmnt_aspects_numerotation.tsv`), 58 cartes intégrées
(ub019 Honorable Blades non intégrée, Q-ub03). Questions : `.planning/tmnt/aspects-basic-questions.md`.
Cas : `Fusion/marvel-lcg-src/tools/cas/tmnt_aspect_basic.py` (filtre `[ub]`, 158 cas, 158 verts).
Entrées `cards.json` : générées par un script (scratchpad `ub/entrees.py`) recopié sur les scans.

## Communs à toutes les cartes du pack

- **Ressource** (icône en bas à gauche) vérifiée contre les ressources du MÊME pack : ub054 Strength (poing
  rouge, RR), ub016 Genius (nœuds bleus, BB), ub011 Energy (éclair jaune, YY), ub007 Digging Deep (étoile
  verte, G). Relevé carte par carte dans la colonne RES de `desc`.
- **Bandeau « ✦ <titre d'origine> »** (décision Q-R1, merge 02da1e10) : `unique_also` posé sur ub001 Nick
  Fury, ub003 Spider-Man, ub006 Ironheart, ub012 Weapon X, ub015 White Fox, ub018 Cerebro, ub028 Mockingbird,
  ub034 The Sorcerer Supreme, ub043 X-Mansion, ub048 Hulk, ub053 Stick, ub056 X-Bunker. Bandeaux SANS ✦
  (Game Time, Helicarrier, Avengers Mansion, Crew Quarters, X-Men Instruction, Bloodgem, X-Gene, Cell Phone) :
  cartes non uniques, pas d'`unique_also`.
- **Reskins (IDENTIQUE)** : `ability_link` vers l'officielle, aucun script. Modules d'origine relus : aucun
  nom ni card_id en dur ; `grep '"<id>"' src/game src/engine` : seulement des commentaires (01084, 12033,
  40057, 12024) et la liste des ressources de base dans `scene.py` (nom de rejeu). Ressources de base
  (01088/01089/01090) : PAS de module d'origine (pures données) → pas d'`ability_link` (le chargeur
  l'interdirait : `assert not load_from_ability_link`).
- **Preuve des reskins** : chaque cas existe sur le reskin ET en TÉMOIN sur l'officielle (même montage, même
  chiffre, `_paire`). Substitution : `SANS_LIEN=1` (retire tous les `ability_link`) → voir le bilan en bas.
- **Étape 8 (autoplay)** : fournée commune en bas de fichier.
- **Étape 8 bis** : seules les cartes qui posent un statut/compteur/attachement sont concernées ; tous ces
  objets (Cloaked, Dazed, Tough, Stunned, pep, rage, charge, attachement d'amélioration à un allié) sont déjà
  dessinés par le plateau pour d'autres cartes (tl015/ta003/td005 Cloaked-Dazed, 01083 Stunned, 62020 rage,
  47019 charge, 01074 amélioration d'allié). Aucun nouvel objet visuel : pas de cas plateau ajouté.

## Extensions / correctifs moteur et cartes officielles (hors aspect, signalés)

- `src/game/card/face/card_face.py` : compteur `pep` ajouté à `CardFace.COUNTER` (ub037) ; `ui-app`
  `compteurs-fr.ts` : `pep`.
- `src/cards/pack/luke_cage/62020.py` (Hulk, officielle, reskinnée par ub048 Slash) : CORRECTIF, l'ATK par
  compteur rage n'était recalculée que quand un ALLIÉ entrait en jeu (`WhileValid(OnEvent.CardInPlay(Ally))`) :
  un compteur rage posé ne changeait rien. Cas `[ub] ub048 ...` rouge sur le TÉMOIN 62020 avant correctif.
  Modèle 27067 (`ThisGainKeyword(..., change_on_event=OnEvent.Counter("This", 'rage'))`).
- `src/cards/pack/fne/60029.py` (Stick, officielle, reskinnée par ub053 Splinter) : CORRECTIF, les deux options
  du « choose » étaient deux Interruptions distinctes, déclenchables TOUTES LES DEUX sur la même utilisation
  (+1 puis -1 et redressement). Une seule Interruption qui fait choisir (`ChooseAbilities`, modèle ht014).
  Cas : les deux options, chiffre mesuré (menace 5 → 3 ; 5 → 5 et carte redressée).

---

### ub001 : April O'Neil (reskin IDENTIQUE de 01084 Nick Fury)

- [x] Étape 2 : 01084 par `ability_link`.
- [x] Étape 5 : texte du scan = 01084 au nom près (« discard her »). Traits VIGILANTE (pas S.H.I.E.L.D/SPY).
      Forced Response (pas de choix de déclencher). Bandeau ✦ Nick Fury → `unique_also`.
- [x] Étape 6 : coût 4, THW 2* / ATK 2*, 3 PV, RES B (nœuds bleus). 2 menaces / 3 cartes / 4 dégâts : module.
- [x] Étape 7 : `ub001 ... option « 4 degats »` (Rhino 4) + témoin 01084 ; `... defausse a la fin du round`
      (vraie fin de round, `ub_apres_fin_de_round`) + témoin. Substitution : voir bilan.
- [x] Étape 7 bis : limite ? NON.
- [x] Étape 8 : fournée Leonardo-ub.
- [x] Étape 8 bis : NON (allié standard).

Carte terminée : OUI.

### ub002 : Assess the Situation (reskin IDENTIQUE de 12033)

- [x] Étape 2 : 12033 (`ability_link`). Hack du moteur `face_action.py` « 31002a, 12033 » : commentaire, vise
      31002 seulement.
- [x] Étape 5 : texte identique. ⚠ Trait TACTIC absent du scan → Q-ub01 (suivi du scan en attendant).
- [x] Étape 6 : coût 0, RES B, +1.
- [x] Étape 7 : `ub002 ... +1 taille de main` + témoin 12033.
- [x] 7 bis : NON. 8 : fournée Spider-Man-ub. 8 bis : NON.

**Mise à jour du 17/10/2026 (Réponse du 17/10/2026)** : le trait TACTIC absent du scan est un oubli de l'auteur ; **TACTIC remis**
(`traits` de l'entrée = `["TACTIC"]`, comme 12033). Cas de donnée `ub002 ... porte le trait TACTIC` (vérificateur
`tmnt_donnees_carte`) : ROUGE avec l'ancienne entrée (« trait TACTIC absent »), vert après.
Carte terminée : OUI (trait TACTIC remis).

### ub003 : Atilla (MODIFIÉE de 13019 Spider-Man Miles Morales)

- [x] Étape 2 : 13019 (même déclencheur `AfterPlayerPlayedCard("You","This")`, `AskChooseOneText`,
      `GainUntilPhaseEnd`). Script propre `ub003.py`.
- [x] Étape 5 : « Forced Response » (scan) au lieu de « Response » → `AbilityType.ForcedResponse` ; « from
      your hand » (mise en jeu par effet : rien) ; « until the end of the phase ». Traits FROG PUNK.
      Bandeau ✦ Spider-Man → `unique_also` (ne coexiste avec aucun Spider-Man).
- [x] Étape 6 : coût 3, THW 1* / ATK 2*, 3 PV, RES R ; +2.
- [x] Étape 7 : `ub003 ... THW choisi -> +2 CTR`, `... option ATK -> +2 ATQ` (rouges sans module) ;
      contre-cas `... mis en jeu SANS etre joue de la main` et `... bandeau Spider-Man` (verts sans module :
      absence d'effet / donnée). Substitution : 2/4 rouges, les 2 verts sont ces contre-cas.
- [x] 7 bis : NON. 8 : fournée Leonardo-ub. 8 bis : NON.

Carte terminée : OUI. (Remarque : la lecture « Forced » suit le scan ; si c'était une coquille pour
« Response », il suffit de changer le type.)

### ub004 : Basic Spell (reskin IDENTIQUE de 45051)

> **Converti en art alternatif de 45051 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ub004` n'existe plus dans `cards.json` (image `45051_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `45051` est conservé. Ce qui suit est l'historique.

- [x] 2 : 45051. 5 : texte identique (MYSTIC, trois options). 6 : coût 2, RES Y, 3/3/3.
- [x] 7 : `ub004 ... Doctor Strange ... 3 degats` + témoin ; contre-cas Spider-Man injouable + témoin.
- [x] 7 bis NON ; 8 : non jouée en autoplay (aucun héros MYSTIC dans la fournée) ; 8 bis NON.

Carte terminée : OUI (autoplay : la carte n'est pas dans les decks de la fournée, capacité prouvée par les
cas et par l'officielle).

### ub005 : Casey Jones (NOUVELLE)

- [x] Étape 2 : 23002 Iron Man allié (fouille deck + défausse d'un upgrade à trait).
- [x] Étape 5 : « deck AND discard pile », « WEAPON upgrade », Response facultative, (Shuffle).
- [x] Étape 6 : coût 3, THW 1* / ATK 2*, 2 PV, RES R.
- [x] Étape 7 : `ub005 ... deck`, `... DEFAUSSE` (rouges sans module) ; contre-cas `... NON WEAPON` (vert
      sans module, absence). Substitution 2/3.
- [x] 7 bis NON ; 8 : fournée Leonardo-ub ; 8 bis NON.

Carte terminée : NON — en attente de Q-ub09 (unicité avec tr002 et le héros Casey Jones).

### ub006 : Clyde (reskin IDENTIQUE de 13018 Ironheart)

- [x] 2 : 13018. 5 : texte identique ; traits FROG PUNK ; bandeau ✦ Ironheart. 6 : coût 2, 1*/1*, 2 PV, RES B.
- [x] 7 : `ub006 ... pioche 1 carte` + témoin. Cas ressource ub011/ub016/ub054 l'emploient aussi.
- [x] 7 bis NON ; 8 fournée Leonardo-ub ; 8 bis NON.

Carte terminée : OUI.

### ub007 : Digging Deep (reskin IDENTIQUE de 40060)

> **Converti en art alternatif de 40060 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ub007` n'existe plus dans `cards.json` (image `40060_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `40060` est conservé. Ce qui suit est l'historique.

- [x] 2 : 40060. 5 : texte identique. 6 : RES G (étoile verte).
- [x] 7 : défaussée du dessus du deck par le Rampage de ua015 Demolish → revient en main + témoin.
- [x] 7 bis NON ; 8 : dans les deux decks de la fournée ; 8 bis NON.

Carte terminée : OUI.

### ub008 : Donatello (NOUVELLE)

- [x] Étape 2 : 45048 Triage (déclencheur), 01084 (pioche).
- [x] Étape 5 : « enters play » (toute mise en jeu) ; « draw 2 ».
- [x] Étape 6 : coût 3, THW 2** / ATK 2** (deux icônes de dégât consécutif chacune), 2 PV, RES B.
- [x] Étape 7 : `ub008 ... pioche 2` ; substitution 1/1.
- [x] 7 bis NON ; 8 fournée Spider-Man-ub ; 8 bis NON.

Carte terminée : NON — en attente de Q-ub05 (unicité avec le héros Donatello).

### ub009 : Down Time (reskin IDENTIQUE de 05033)

> **Converti en art alternatif de 05033 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ub009` n'existe plus dans `cards.json` (image `05033_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `05033` est conservé. Ce qui suit est l'historique.

- [x] 2 : 05033. 5 : identique (Play under any player's control, Max 1 per player → `MaxPerUnit`). 6 : coût 1,
      RES R, +2 REC.
- [x] 7 : `ub009 ... +2 REC` + témoin. 7 bis NON. 8 : fournée Spider-Man-ub. 8 bis NON.

Carte terminée : OUI.

### ub010 : Endurance (reskin IDENTIQUE de 05023)

> **Converti en art alternatif de 05023 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ub010` n'existe plus dans `cards.json` (image `05023_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `05023` est conservé. Ce qui suit est l'historique.

- [x] 2 : 05023. 5 : identique. 6 : coût 1, RES Y, +3 PV.
- [x] 7 : `ub010 ... +3 points de vie` + témoin. 7 bis NON. 8 : non incluse dans la fournée. 8 bis NON.

Carte terminée : OUI.

### ub011 : Energy, ub016 : Genius, ub054 : Strength (ressources de base, IDENTIQUES de 01088/01089/01090)

- [x] 2 : 01088/01089/01090 n'ont AUCUN module (pures données) : pas d'`ability_link`.
- [x] 5 : « Max 1 per deck. » → `desc.MaxPerDeck`. 6 : RES YY / BB / RR.
- [x] 7 : `ubNNN ... ressource double ... paie SEULE Clyde (cout 2)` + témoin chacune. Pas de capacité :
      aucune substitution possible (assumé).
- [x] 7 bis NON ; 8 : dans les deux decks de la fournée ; 8 bis NON.

Cartes terminées : OUI.

### ub012 : E.P.F. R.N.D. (reskin IDENTIQUE de 35022 Weapon X)

- [x] 2 : 35022. 5 : identique (« Exhaust E.P.F. R.N.D. and take 1 damage »). Traits LOCATION NYC STREETS.
      Bandeau ✦ Weapon X.
- [x] 6 : coût 1, RES B, 1 dégât.
- [x] 7 : `ub012 ... defausse jusqu'a une carte d'identite` + témoin. 7 bis NON. 8 : hors fournée. 8 bis NON.

Carte terminée : OUI.

### ub013 : Face the Past (reskin IDENTIQUE de 49022)

> **Converti en art alternatif de 49022 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ub013` n'existe plus dans `cards.json` (image `49022_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `49022` est conservé. Ce qui suit est l'historique.

- [x] 2 : 49022. 5 : identique. 6 : coût 0, RES R, Max 1 per deck, 3 cartes.
- [x] 7 : montage du cas Hercules existant (Ares révélé, pas la Lernean Hydra) + témoin. 7 bis NON.
- [x] 8 : fournée Spider-Man-ub. 8 bis NON.

Carte terminée : OUI.

### ub014 : Fugitoid (NOUVELLE)

- [x] Étape 2 : 45020 Legion (même déclencheur, même lecture des icônes imprimées) ; 15019 (défausse choisie de
      la main).
- [x] Étape 5 : « discard 1 card from YOUR HAND » (choisie) ; « If that card's printed resource HAS » : une
      branche par icône présente ; « a FRIENDLY character » (`Friend`) ; « an enemy » ; [wild] → pioche 1 ;
      [star] = étoile de rappel (zéro code). Main vide : rien.
- [x] Étape 6 : coût 2, THW 1* / ATK 1*, 2 PV, RES Y ; 2 / 2 / 2 / 1.
- [x] Étape 7 : quatre cas, un par icône (Energy, Genius, Strength, Digging Deep), rouges sans module ;
      contre-cas main vide (vert sans module). Substitution 4/5.
- [x] 7 bis NON ; 8 fournée Leonardo-ub ; 8 bis NON.

Carte terminée : OUI.

### ub015 : Genghis (reskin IDENTIQUE de 40057 White Fox)

- [x] 2 : 40057 (correctif moteur « Fix 40057 » dans ability.py : générique, pas un card_id comparé).
- [x] 5 : identique (« put him into play »). FROG PUNK. Bandeau ✦ White Fox. 6 : coût 3, 1*/1*, 3 PV, RES Y.
- [x] 7 : défaussé par le Rampage de Demolish → mis en jeu + témoin. 7 bis NON. 8 : fournée Leonardo-ub. 8 bis NON.

Carte terminée : OUI.

### ub017 : Gofu Talisman (reskin IDENTIQUE de 45050 Bloodgem)

- [x] 2 : 45050. 5 : « Play only if you have the MYSTIC trait » au lieu de « your identity has » : même sens
      (« you » = votre identité) ; Max 1 per deck ; Ressource : s'incliner + 2 dégâts → [wild].
- [x] 6 : coût 0, RES G, 2 dégâts.
- [x] 7 : ressource (2 dégâts, inclinée) + témoin ; jouable Doctor Strange + témoin ; injouable Spider-Man +
      témoin. 7 bis NON. 8 : hors fournée. 8 bis NON.

Carte terminée : OUI.

### ub018 : Herold Lilja's Lab (MODIFIÉE de 34022 Cerebro)

- [x] 2 : 34022. Script propre (DIMENSION X / NINJA / MUTANIMAL en OU, TEMPORAL).
- [x] 5 : « top 5 », « whole deck instead if you control a TEMPORAL character », « ally », « Exhaust this card ».
      Bandeau ✦ Cerebro.
- [x] 6 : coût 1, RES B, 5 cartes.
- [x] 7 : top 5 → trouvé ; 7e sans TEMPORAL → introuvable ; 7e avec Malcolm 45002 → trouvé ; allié sans trait
      → pas pris ; injouable Spider-Man ; jouable Leo. Substitution 5/6.
- [x] 7 bis NON ; 8 fournée Leonardo-ub ; 8 bis NON.

Carte terminée : OUI.

### ub019 : Honorable Blades (NOUVELLE, Team-Up Leonardo + Usagi Yōjimbō)

**INTÉGRÉE le 17/10/2026.** Rectification : l'agent précédent croyait Usagi Yōjimbō absent de la base, c'est faux :
c'est l'allié `up041` (Protection, unique, RABBIT RONIN). Scan : « Team-Up (Leonardo and Usagi Yōjimbō). Max 1 per
deck. Hero Action: Ready Leonardo and Usagi Yōjimbō. Cloak Leonardo. Place a tough status card on Usagi Yōjimō. » : la
coquille « Yōjimō » (dernière ligne) est corrigée, le nom exact est celui de `up041` (texte affiché avec la bonne
orthographe). Coût 2, RES éclair = Y (énergie), aucun trait imprimé, Max 1 per deck.

- [x] Étape 2 : mot-clé **Team-Up** : fiche `mots-cles/teamup.md` lue (les ALLIÉS comptent, `.SetTarget("TeamUp")`
      obligatoire, `desc.TeamUp = "Leonardo;Usagi Yōjimbō"`) ; `34035` Soul Sisters (Phoenix) : « Ready A and B »
      (`Faces.ReadyAll(effect.targets)`), même déclencheur Hero Action + TeamUp ; `uj021` : « Cloak X » =
      `Faces.GiveStatus([x], "Cloaked")` ; `up016` : « place a tough status card » = `GiveStatus(..., "Tough")`.
- [x] Étape 5 : « Team-Up » (les DEUX en jeu, identité OU allié), « Ready Leonardo AND Usagi » (les deux), « Cloak
      LEONARDO » seulement, « tough on USAGI » seulement ; les personnages sont distingués par le nom
      (`effect.targets` n'est pas ordonné) ; « Max 1 per deck » (`MaxPerDeck`). Résultat : conforme.
- [x] Étape 6 : coût 2, RES Y, MaxPerDeck 1. Résultat : conforme.
- [x] Étape 7 : `[ub] ub019 ...` : Leonardo ET Usagi en jeu -> les deux redressés (inclinés au départ), Leonardo camouflé,
      Usagi Tenace (Tenace retiré avant) ; jouable avec les deux (contre-cas) ; PAS jouable avec Leonardo seul ; PAS
      jouable avec Usagi sans Leonardo (Spider-Man). 4/4 verts. **Substitution** : sans le script ni l'entrée, 4/4 ROUGES
      (`AssertionError: name_or_id='ub019'`) ; remis, 4/4 verts.
- [x] Étape 7 bis : limite imprimée « Max 1 per deck » : donnée de deck-building, pas une limite de jeu : NON.
- [x] Étape 8 : autoplay du 17/10 (section en fin de ce fichier).
- [x] Étape 8 bis : NON (statuts Cloaked / Tough déjà dessinés, cf. ud001 / ud006).

Carte terminée : OUI (image `ub019` déjà importée ; deck-builder / arts alternatifs hors périmètre).
Non prouvé : l'icône du coin (éclair) lue comme énergie à la vue, comparée à `ub011` dont la fiche porte `RES Y` ;
aucune partie jouée par un humain.

### ub020 : Improvised Club (NOUVELLE)

- [x] Étape 2 : 01074 Inspired (amélioration d'allié), 12017 Power Gloves (« attached ally »), 01118 Sonic
      Converter (« attacks and damages ..., stun that character »).
- [x] Étape 5 : « attached ally » ; « attacks AND damages » ; « a MINION » ; défausse = coût ; « stun THAT minion ».
- [x] Étape 6 : coût 1, RES Y, Max 1 per ally (`MaxPerUnit`).
- [x] Étape 7 : sbire attaqué et blessé → sonné, club défaussé (rouge sans module) ; contre-cas vilain (vert).
      Substitution 1/2.
- [x] 7 bis NON ; 8 fournée Leonardo-ub ; 8 bis : attachement à un allié et statut Stunned, déjà dessinés
      (01074, 01083) : NON.

Carte terminée : OUI.

### ub021 : Ingenuity (reskin IDENTIQUE de 29027)

- [x] 2 : 29027. 5/6 : identique, coût 2, RES B. 7 : ressource (paie Down Time) + jouable Peter Parker (GENIUS)
      + injouable Spider-Man héros, chacun + témoin. 7 bis NON. 8 fournée Spider-Man-ub. 8 bis NON.

Carte terminée : OUI.

### ub022 : Jennika (NOUVELLE)

- [x] Étape 2 : tv002 Bludgeon (défausse → dessus du deck) ; fiche shinobi.md (4 classes).
- [x] Étape 5 : « a Shinobi card » ; « YOUR discard pile » ; « on TOP » ; « (black) » sans code.
- [x] Étape 6 : coût 3, 2*/2*, 3 PV, RES Y.
- [x] Étape 7 : Decisive Strike (Taijutsu) remontée puis piochée (rouge sans module) ; Composure (non Shinobi)
      reste en défausse (vert, absence). Voir bilan.
- [x] 7 bis NON ; 8 fournée Spider-Man-ub ; 8 bis NON.

Carte terminée : NON — en attente de Q-ub08 (unicité avec l'héroïne Jennika).

### ub023 : Katsuichi (NOUVELLE)

- [x] Étape 2 : 01041 Shuri, 27048 (identity-specific).
- [x] Étape 5 : « your DECK » seulement ; « identity-specific CARD » (tout type).
- [x] Étape 6 : coût 3, THW 1* / ATK 2*, 3 PV, RES B.
- [x] Étape 7 : 01005 trouvée (rouge sans module) ; 01086 non prise (vert). 7 bis NON. 8 fournée Leonardo-ub.
      8 bis NON.

Carte terminée : OUI.

### ub024 : The Kennel Klub (MODIFIÉE de 33020 Utopia)

- [x] Étape 2 : 33020. `if_each_of_your_allies_has_trait` n'accepte qu'un trait → `condition=` + mêmes
      événements de recalcul que la fabrique.
- [x] Étape 5 : « EACH of your allies », « MUTANIMAL OR NINJA » (×3), « exhaust → ready a ... CHARACTER ».
      Ressource [mental] (l'officielle est [physical]).
- [x] Étape 6 : coût 2, RES B, +1.
- [x] Étape 7 : limite 4 avec 4 alliés NINJA/MUTANIMAL ; contre-cas Mockingbird (3 alliés) ; Réponse
      redresse Donatello ; contre-cas allié sans trait. Voir bilan.
- [x] 7 bis NON ; 8 fournée Leonardo-ub ; 8 bis NON.

Carte terminée : OUI.

### ub025 : Leonardo (NOUVELLE)

- [x] Étape 2 : 04032 Captain Marvel allié (« uses a basic power »), 33020 (redresser).
- [x] Étape 5 : « ANOTHER » (`another=True`), « NINJA ALLY », « YOU control ». [star] sans code.
- [x] Étape 6 : coût 3, THW 1* / ATK 2*, 3 PV, RES R.
- [x] Étape 7 : Donatello redressé (rouge sans module) ; Mockingbird reste incliné (vert). Voir bilan.
- [x] 7 bis NON ; 8 fournée Spider-Man-ub ; 8 bis NON.

Carte terminée : NON — en attente de Q-ub04 (unicité avec le héros Leonardo).

### ub026 : Limitless Stamina (reskin IDENTIQUE de 31023)

> **Converti en art alternatif de 31023 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ub026` n'existe plus dans `cards.json` (image `31023_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `31023` est conservé. Ce qui suit est l'historique.

- [x] 2 : 31023. 5/6 : identique, coût 1, RES R, 14 PV. 7 : Hulk redressé + témoin ; Spider-Man injouable +
      témoin. 7 bis NON. 8 : hors fournée. 8 bis NON.

Carte terminée : OUI.

### ub027 : Martial Arts Training (NOUVELLE)

- [x] Étape 2 : 60038 Innate Reflexes (Starting, « Your hero ... »), sm012 (gagner un trait). Fiche starting.md.
- [x] Étape 5 : « Your HERO » (forme héros seulement) ; « You MAY add » ; aucune icône de ressource (comme 60038).
- [x] Étape 6 : coût 1, pas de RES.
- [x] Étape 7 : trait gagné en héros ; absent en alter ego ; le trait fait partir Splinter (ub053) ; Starting
      accepté / refusé (deck de test `tools/cas/ub_deck_starting.json`). Voir bilan.
- [x] 7 bis NON ; 8 : dans les deux decks ; 8 bis NON.

Carte terminée : OUI.

### ub028 : Mary (reskin IDENTIQUE de 01083 Mockingbird)

- [x] 2 : 01083. 5/6 : identique, coût 3, 1*/1*, 3 PV, RES R ; FROG PUNK ; bandeau ✦ Mockingbird.
- [x] 7 : Rhino sonné + témoin. 7 bis NON. 8 fournée Spider-Man-ub. 8 bis NON.

Carte terminée : OUI.

### ub029 : Michelangelo (NOUVELLE)

- [x] Étape 2 : 45048 Triage. Étape 5 : « a FRIENDLY character » (`Friend`), 2.
- [x] Étape 6 : coût 3, 1*/1*, 3 PV, RES Y.
- [x] Étape 7 : soin de Spider-Man (3 → 1) ; soin d'un allié (2 → 0). Voir bilan.
- [x] 7 bis NON ; 8 fournée Spider-Man-ub ; 8 bis NON.

Carte terminée : NON — en attente de Q-ub06 (unicité avec le héros Michelangelo).

### ub030 : Multitalented (reskin IDENTIQUE de 47021)

- [x] 2 : 47021. 5/6 : identique, coût 3, RES R. 7 : payé en [physical] seul → 2 dégâts, menace intacte +
      témoin. 7 bis NON. 8 fournée Spider-Man-ub. 8 bis NON.

Carte terminée : OUI.

### ub031 : Mutagen (reskin IDENTIQUE de 38019 X-Gene)

- [x] 2 : 38019. 5 : identique ; sous-titre vertical « X-Gene » = bandeau sans ✦ (carte non unique).
- [x] 6 : coût 1, RES G. 7 : [wild] pour Swinging Web Kick + témoin ; ne paie pas Multitalented + témoin.
- [x] 7 bis NON ; 8 hors fournée ; 8 bis NON.

Carte terminée : OUI.

### ub032 : Mutanimal Van (MODIFIÉE de 41022 IPAC)

- [x] 2 : 41022 ; X-FORCE → MUTANIMAL. 5 : identique sinon. 6 : coût 1, RES B, 1 carte, 2 pioches.
- [x] 7 : Action → 2 pioches (rouge sans module) ; injouable sans MUTANIMAL. Voir bilan.
- [x] 7 bis NON ; 8 : hors fournée (aucun héros MUTANIMAL n'existe dans la base : la carte n'est jouable par
      AUCUNE identité actuelle — remarque, pas une question : le texte est clair) ; 8 bis NON.

Carte terminée : OUI.

### ub033 : Ninja He-Man (NOUVELLE)

- [x] Étape 2 : 27048 (« Play only if you control a <trait> card ») — `only_if_you_control_trait` n'accepte
      qu'un trait et `only_if_you_control_face` lit l'inventaire de l'identité : helper
      `JouableSiVousControlez` (`__init__.py` du pack, même test `IsControl(CardFinder2(trait))`, en OU).
      Toughness : `desc` ; Cloak : fiche cloak.md.
- [x] Étape 5 : « a NINJA or WARRIOR CARD » (toute carte) ; « cloak HIM ».
- [x] Étape 6 : coût 4, THW 2** / ATK 2*, 3 PV, RES R, Toughness 1.
- [x] Étape 7 : Leonardo le joue → Cloaked + Tough ; injouable Spider-Man ; jouable si Spider-Man contrôle
      Shuriken (NINJA). Voir bilan.
- [x] 7 bis NON ; 8 fournée Leonardo-ub ; 8 bis : statuts Cloaked/Tough déjà dessinés : NON.

Carte terminée : OUI.

### ub034 : Onmyōdō Saikō (reskin IDENTIQUE de 09026 The Sorcerer Supreme)

- [x] 2 : 09026. 5/6 : identique (« you have the MYSTIC trait »), coût 2, RES B ; bandeau ✦.
- [x] 7 : +1 taille de main en héros + témoin. 7 bis NON. 8 hors fournée. 8 bis NON.

Carte terminée : OUI.

### ub035 : Party Time (reskin IDENTIQUE de 33022 Game Time)

- [x] 2 : 33022. 5/6 : identique, coût 0, RES Y. 7 : allié avec TRAINING redressé et soigné + témoin.
- [x] 7 bis NON ; 8 fournée Spider-Man-ub ; 8 bis NON.

Carte terminée : OUI.

### ub036 : Party Wagon (MODIFIÉE de 32020 The X-Jet)

- [x] 2 : 32020 ; `for_player_whose_identity_has_trait` n'accepte qu'un trait : condition de paiement + 
      `any_player_can_trigger_this_when` posés à la main (NINJA ou TURTLE).
- [x] 5 : « for a player whose identity has the NINJA or TURTLE trait ». 6 : coût 3, RES Y.
- [x] 7 : paie le Katana de Leonardo (rouge sans module) ; Spider-Man ne peut pas s'en servir (vert). Voir bilan.
- [x] 7 bis NON ; 8 fournée Leonardo-ub ; 8 bis NON.

Carte terminée : OUI.

### ub037 : Pepperoni (NOUVELLE)

- [x] Étape 2 : 47019 (coût s'incliner + retirer un compteur), hd014 (« remove the last threat »),
      `AfterUnitDefeatedUnit("You", Enemy)`, 12033 (+1 taille de main). Uses : fiche uses.md, compteur `pep`
      ajouté au moteur.
- [x] Étape 5 : « YOU defeat AN ENEMY » / « remove the LAST threat from A scheme » ; coût double ; « until the
      end of the phase ».
- [x] Étape 6 : coût 2, RES R, Uses 3, 1 pep, +1.
- [x] Étape 7 : sbire vaincu → +1, 2 pep, inclinée ; dernière menace d'une annexe → +1 ; dernier pep → défaussée ;
      contre-cas sbire blessé non vaincu. Voir bilan.
- [x] 7 bis : limite imprimée ? NON (l'inclinaison borne, mesurée par `exhausted`).
- [x] 8 fournée Leonardo-ub ; 8 bis : compteur pep, objet « compteur » déjà dessiné (libellé FR ajouté) : NON.

Carte terminée : OUI.

### ub038 : Pizza Time (MODIFIÉE de 37021 Mutant Education)

- [x] 2 : 37021 ; « X-Mansion » → « Rupert's Pizzeria ». 5 : « up to 2 identity-specific », borne basse 1 sans
      Pizzeria (comme l'officielle). 6 : coût 0, RES Y.
- [x] 7 : 2 cartes remélangées sans pioche ; avec Rupert's → pioche 1 ; X-Mansion n'est pas Rupert's. Voir bilan.
- [x] 7 bis NON ; 8 fournée Leonardo-ub ; 8 bis NON.

Carte terminée : OUI.

### ub039 : Practiced Plan (reskin IDENTIQUE de 50058)

> **Converti en art alternatif de 50058 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ub039` n'existe plus dans `cards.json` (image `50058_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `50058` est conservé. Ce qui suit est l'historique.

- [x] 2 : 50058. 5/6 : identique, coût 0, RES Y. 7 : Widow's Bite défaussée revient en main + témoin.
- [x] 7 bis NON ; 8 fournée Spider-Man-ub ; 8 bis NON.

Carte terminée : OUI.

### ub040 : Press and Protect (NOUVELLE)

- [x] Étape 2 : 62023 (Team-Up + `SetTarget2/3`), 60055 (retirer 3 menaces). Fiche teamup.md : les alliés
      comptent (April = ub001 seulement ; Casey = ub005, tr002 ou le héros tc001).
- [x] Étape 5 : « Action » (pas de héros) ; « a scheme » ; « a FRIENDLY character » ; Max 1 per deck.
- [x] Étape 6 : coût 1, RES G, 3 menaces.
- [x] Étape 7 : April + Casey → 3 menaces, Tough ; sans Casey → injouable. Voir bilan.
- [x] 7 bis NON ; 8 fournée Leonardo-ub ; 8 bis NON (statut Tough déjà dessiné).

Carte terminée : OUI.

### ub041 : Raphael (NOUVELLE)

- [x] Étape 2 : 10013 She-Hulk allié. Étape 5 : « here », plafond +2.
- [x] Étape 6 : coût 3, THW 1* / ATK 2*, 3 PV, RES R ; +1 par jeton, max +2.
- [x] Étape 7 : 1 dégât +1 ; 2 dégâts +2 ; 4 dégâts (Reinforced Suit) +2 ; intact +0. Voir bilan.
- [x] 7 bis NON ; 8 fournée Spider-Man-ub ; 8 bis NON.

Carte terminée : NON — en attente de Q-ub07 (unicité avec le héros Raphael).

### ub042 : Ready to Rumble (reskin IDENTIQUE de 21022)

- [x] 2 : 21022. 5/6 : identique, coût 1, RES Y. 7 : changement de forme → héros redressé + témoin.
- [x] 7 bis NON ; 8 fournée Spider-Man-ub ; 8 bis NON.

Carte terminée : OUI.

### ub043 : Rupert's Pizzeria (MODIFIÉE de 32049 X-Mansion)

- [x] 2 : 32049 ; MUTANT/X-MEN → MUTANT/MUTANIMAL/NINJA. Bandeau ✦ X-Mansion.
- [x] 5/6 : coût 2, RES B, 1 dégât, déclenchable par tout joueur dont l'alter ego a MUTANT.
- [x] 7 : soigne Leo (MUTANT) ; soigne Slash ub048 (MUTANIMAL). Voir bilan.
- [x] 7 bis NON ; 8 fournée Leonardo-ub ; 8 bis NON.

Carte terminée : OUI.

### ub044 : Shell Phone (reskin IDENTIQUE de 47019 Cell Phone)

- [x] 2 : 47019 ; `desc.Uses = "3,charge"` recopié (ne vient pas par le lien). 5/6 : identique, coût 2, RES Y.
- [x] 7 : attaque à +1 (3 dégâts), 2 charges + témoin. 7 bis NON. 8 fournée Spider-Man-ub. 8 bis NON.

Carte terminée : OUI.

### ub045 : Shinobi Batman (NOUVELLE)

- [x] Étape 2 : 27048 Ghost-Spider (condition de jeu ; mais Interruption « When » là où le scan dit Response
      « After » → `AfterCardLeavePlay`) ; 18002 Nebula (traits en OU). Helper `JouableSiVousControlez`.
- [x] Étape 5 : « AFTER leaves play » ; « your DECK » ; « NINJA or VIGILANTE CARD ».
- [x] Étape 6 : coût 3, THW 2** / ATK 2*, 3 PV, RES B.
- [x] Étape 7 : vaincu → Katana en main ; injouable Spider-Man. Voir bilan.
- [x] 7 bis NON ; 8 fournée Leonardo-ub ; 8 bis NON.

Carte terminée : OUI.

### ub046 : Shuriken (NOUVELLE)

- [x] Étape 2 : 31029 (attacher à un personnage ami), ar010 (défausser une carte en coût), 10005 (« up to 3 »).
- [x] Étape 5 : Hero Action ; coût double ; « up to 3 » ; 1 dégât chacun.
- [x] Étape 6 : coût 2, RES Y, Max 1 per character (`MaxPerUnit`).
- [x] Étape 7 : 1 dégât à Rhino et au sbire, main vidée ; main vide → coût impayable. Voir bilan.
- [x] 7 bis NON ; 8 fournée Leonardo-ub ; 8 bis : amélioration attachée à un personnage ami, déjà dessinée : NON.

Carte terminée : OUI.

### ub047 : Sky Wagon (reskin IDENTIQUE de 01092 Helicarrier)

- [x] 2 : 01092. 5/6 : identique, coût 3, RES R, Max 1 per player. Traits NYC VEHICLE → Q-ub02.
- [x] 7 : Clyde payé avec une seule ressource + témoin. 7 bis NON. 8 fournée Spider-Man-ub. 8 bis NON.

**Mise à jour du 17/10/2026 (Réponse du 17/10/2026)** : l'utilisateur confirme les traits du scan (NYC, VEHICLE), **PAS LOCATION**.
Rien à changer (Helicarrier 01092 reste LOCATION / S.H.I.E.L.D, Sky Wagon non). Cas de donnée ajouté `ub047 Sky Wagon :
traits NYC et VEHICLE, PAS LOCATION` (vert ; donnée, ne rougit pas sous substitution du lien).
Carte terminée : OUI (traits du scan confirmés).

### ub048 : Slash (reskin IDENTIQUE de 62020 Hulk)

- [x] 2 : 62020 (CORRIGÉE, voir en tête). 5/6 : identique, coût 4, ATK 2**, pas de THW, 5 PV, RES R.
      NINJA TURTLE MUTANIMAL. Bandeau ✦ Hulk.
- [x] 7 : attaque du vilain → 1 rage, ATK +1 + témoin (rouge sur le témoin AVANT le correctif de 62020).
- [x] 7 bis NON ; 8 fournée Spider-Man-ub ; 8 bis NON (compteur rage déjà dessiné).

Carte terminée : NON — en attente de Q-ub10 (unicité avec Slash tm002).

### ub049 : Snow and Shadow (NOUVELLE)

- [x] Étape 2 : 62023 (Team-Up + cibles supplémentaires) ; fiches cloak.md, daze.md, teamup.md.
- [x] Étape 5 : « Ready Alopex AND Nobody » ; « Cloak A friendly character » ; « Daze AN enemy » ; Hero Action.
- [x] Étape 6 : coût 2, RES B, Max 1 per deck.
- [x] Étape 7 : Alopex et Nobody redressés, Nobody camouflé, Rhino hébété ; sans Nobody injouable. Voir bilan.
- [x] 7 bis NON ; 8 : hors fournée (exige le deck Alopex) ; 8 bis NON (Cloaked/Dazed déjà dessinés).

Carte terminée : OUI (autoplay non fait pour elle : il faudrait une fournée Alopex).

### ub050 : "Special Delivery!" (MODIFIÉE de 37031 X-Men Instruction)

- [x] 2 : 37031 ; X-MEN → DIMENSION X / MUTANIMAL / NINJA ; X-Mansion → Rupert's Pizzeria.
- [x] 5/6 : coût 0, RES Y. 7 : allié NINJA remélangé, Mockingbird non ; Rupert's → pioche. Voir bilan.
- [x] 7 bis NON ; 8 fournée Leonardo-ub ; 8 bis NON.

Carte terminée : OUI.

### ub051 : Spiritual Meditation (reskin IDENTIQUE de 15019)

> **Converti en art alternatif de 15019 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ub051` n'existe plus dans `cards.json` (image `15019_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `15019` est conservé. Ce qui suit est l'historique.

- [x] 2 : 15019. 5/6 : identique, coût 0, RES B. 7 : pioche 2 défausse 1 + témoin. 7 bis NON. 8 hors fournée.
      8 bis NON.

Carte terminée : OUI.

### ub052 : Splinter Dojo (MODIFIÉE de 33021 Danger Room)

- [x] 2 : 33021 ; X-MEN → MUTANIMAL/NINJA ; ET `AnyPlayerCanDoThis(player_alter_ego_has_trait="MUTANT")` (33021
      l'appelle sans condition : écart de l'officielle, non corrigé chez elle, signalé).
- [x] 5/6 : coût 2, RES Y. 7 : TRAINING du deck attachée ; de la défausse ; allié sans trait → rien ; en forme
      héros → rien. Voir bilan.
- [x] 7 bis NON ; 8 fournée Leonardo-ub ; 8 bis NON (attachement à un allié déjà dessiné).

Carte terminée : OUI.

### ub053 : Splinter (reskin IDENTIQUE de 60029 Stick)

- [x] 2 : 60029 (CORRIGÉE, voir en tête). 5/6 : identique, coût 2, RES R. Bandeau ✦ Stick.
- [x] 7 : option +1 (menace 5 → 3, inclinée) + témoin ; option -1 (5 → 5, redressée) + témoin ; et via ub027.
- [x] 7 bis NON ; 8 fournée Spider-Man-ub ; 8 bis NON.

Carte terminée : NON — en attente de Q-ub11 (unicité avec l'allié Splinter tl002).

### ub055 : Team-Building Exercise (reskin IDENTIQUE de 12024)

- [x] 2 : 12024 (« It's because of 12024 » dans resources.py : commentaire). 5/6 : identique (coquille « it's »
      du scan conservée dans le texte), coût 2, RES R.
- [x] 7 : Katana (NINJA) joué pour 0 par Leonardo + témoin. 7 bis NON. 8 fournée Spider-Man-ub. 8 bis NON.

Carte terminée : OUI.

### ub056 : The Market (reskin IDENTIQUE de 41023 X-Bunker)

- [x] 2 : 41023. 5/6 : identique (MUTANT inchangé), coût 2, RES Y ; LOCATION NYC SEWERS ; bandeau ✦ X-Bunker.
- [x] 7 : 1 annexe en victoire → 1 carte + témoin. 7 bis NON. 8 hors fournée. 8 bis NON.

Carte terminée : OUI.

### ub057 : Turtle Lair (reskin IDENTIQUE de 01091 Avengers Mansion)

- [x] 2 : 01091. 5/6 : identique, coût 4, RES B, Max 1 per player. 7 : pioche 1 + témoin. 7 bis NON.
- [x] 8 fournée Spider-Man-ub ; 8 bis NON.

Carte terminée : OUI.

### ub058 : Upstate Farmhouse (reskin IDENTIQUE de 20029 Crew Quarters)

- [x] 2 : 20029. 5/6 : identique, coût 1, RES B. 7 : soin 1 d'un alter ego + témoin. 7 bis NON.
- [x] 8 fournée Spider-Man-ub ; 8 bis NON.

Carte terminée : OUI.

### ub059 : Weapon Harness (MODIFIÉE de 20021 Side Holster)

- [x] 2 : 20021 ; « Play under any player's control » supprimé, NINJA exigé, 2 armes au lieu de 1 (deux
      `GiveKeywordToAttached(control_additional_restricted=...)`, chacune +1 à la limite).
- [x] 5/6 : coût 0, RES R, Max 1 per player.
- [x] 7 : 4 armes Restricted gardées ; témoin sans harnais 2 ; 5e arme → 4 au plus ; injouable Spider-Man.
      Voir bilan.
- [x] 7 bis : la limite mord (cas « 5e arme ») ; 8 fournée Leonardo-ub ; 8 bis NON.

Carte terminée : OUI.

---

## Bilan des preuves (16/10/2026)

- `[ub]` : **158/158 verts** (PARALLELES=6, ports 31000+).
- **Substitution des scripts** (`tools/substituer_pack.py .game-src 31300 ub`, 26 modules) : chaque module a au
  moins un cas qui rougit ; les cas restés verts sont TOUS des contre-cas d'absence d'effet ou de donnée
  (non jouable sans trait, allié sans trait, main vide, vilain au lieu d'un sbire...). Détail :
  ub003 2/4, ub005 2/3, ub008 1/1, ub014 4/5, ub018 5/6, ub020 1/2, ub022 1/2, ub023 1/2, ub024 2/4, ub025 1/2,
  ub027 4/5, ub029 2/2, ub032 2/2, ub033 2/3, ub036 1/2, ub037 3/4, ub038 2/3, ub040 1/2, ub041 3/4, ub043 2/2,
  ub045 2/2, ub046 1/2, ub049 1/2, ub050 2/2, ub052 2/4, ub059 3/4.
- **Substitution des reskins** (`SANS_LIEN=1` : tous les `ability_link` retirés) : 124/158 ; les 34 rouges
  sont exactement les cas de capacité des reskins (TÉMOINS officiels tous verts). Restés verts : les cas de
  données (non jouable sans trait : ub004/ub017/ub021/ub026/ub031 contre-cas ; ressources ub011/ub016/ub054,
  sans module par nature ; « jouable par » ub017/ub021).
- Non-régression : `[r` (rampage, reskin, raphael... 120/120), `62020` 2/2, `Luke Cage` 8/8 ;
  `verifier_appels_modules.py` (tmnt_aspect_basic, fne, luke_cage) OK ; `test_cards.py` 6607 ok, 0 erreur ;
  vitest `textes-fr-fanmade.test.ts` + `compteurs-fr.test.ts` 28/28.

## Étape 8 : fournée d'autoplay (commune)

8 parties par deck contre Rhino, normal, profil équilibré, ports 31500+ :
- deck Leonardo + aspect ub (`scratchpad/ub/deck-leo-ub.json` : 29 cartes ub) : 0 V / 8 D, 6,4 rounds, 0 blocage ;
  témoin Leonardo de départ : 0 blocage, mêmes causes de fin (4 éliminés / 4 manigance) ;
- deck Spider-Man + aspect ub (`deck-sm-ub.json` : 27 cartes ub) : 0 blocage ; témoin Spider-Man : 0 blocage.
- Grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 32 journaux : **0**.
- Lecture : 47 cartes ub différentes mises en jeu ou activées (Martial Arts Training 16 entrées en jeu,
  Fugitoid 12 + 10 activations, Atilla 12 + 6, Shuriken 4 activations, Shinobi Batman 3 Réponses après sortie,
  Ninja He-Man 2 camouflages, Pizza Time, Rupert's Pizzeria...). Fugitoid : la Réponse défausse bien une
  carte de la main (Vigilant tl004, [physical]) ; sans personnage blessé le soin n'a pas de cible.
- Non jouées en autoplay (hors des deux decks ou condition jamais remplie) : ub004, ub010, ub012, ub017, ub026,
  ub031, ub032 (aucune identité MUTANIMAL n'existe), ub034, ub049 (deck Alopex requis), ub051, ub056. Leur
  capacité est prouvée par les cas (et, pour les reskins, par l'officielle).

## Ce qui n'est pas prouvé

- Aucune partie humaine dans le navigateur.
- Le deck-builder masque les reskins homonymes d'une officielle (Q-R2, déjà ouverte) : Assess the Situation,
  Basic Spell, Digging Deep, Down Time, Endurance, Energy, Genius, Strength, Face the Past, Ingenuity, Limitless
  Stamina, Multitalented, Practiced Plan, Ready to Rumble, Spiritual Meditation, Team-Building Exercise,
  Martial Arts Training (homonyme de 41009 Psylocke) n'y ont probablement pas de tuile.
- Traits sans traduction FR dans `traits-fr.ts` : PUNK, LION, RONIN, DIMENSION X, NYC, MUTANIMAL (fichier hors
  bloc d'aspect, non modifié).

## Autoplay des retouches du 17/10/2026 (ub019, up030, ul031, ud005, uj002, ul019, ul033, ub002, ul038, ub047, up018)

`tools/autoplay.py`, Rhino normal, profil équilibré, 8 parties, port 30010, deck `deck-ret-A` (héros Leonardo ; cartes
retouchées : ub019 ×2, up041 ×2, up030 ×2, ul031, ud005, ul019, ul033, ub002, ul038, ul028, uj002, ub047, up018, + ub025 et
cartes Protection) : 4 schéma complété, 4 joueur éliminé, 0/8 bloquée ; **0 NameError / AttributeError / TypeError /
KeyError / AssertionError / Traceback sur 8 journaux**. Lecture : ub019 jouée (Usagi et Leonardo redressés, Tenace d'Usagi
retiré avant son jeu), up030 portée par Leonardo, ul031 / uj002 / ul038 / ul019 vus en partie. Pas de héros témoin (le deck de
départ Leonardo a un `player_deck` vide) : le taux de défaite n'est pas comparé. Rien de ce relevé ne remplace une partie
jouée par un humain (non faite).
