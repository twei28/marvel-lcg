# PROCESSUS-CARTE.md — les 16 gabarits du pack Wave (65001-65019)

> **Mise à jour du 07/10/2026 (audit du backlog)** : CLOS : les 16 cartes sont « OUI ». Les 8 cases vides sont « 7 bis : limite imprimée ? NON » (jamais cochées). Le paragraphe de bilan « 3 cartes restent NON » est PÉRIMÉ : 65008, 65011, 65012 sont fermées le 23/09 dans le corps de la fiche.

Gate de `CLAUDE.md` : rien n'est terminé sans le gabarit rempli, preuve à
l'appui. Rédigés le 22/09/2026, à la suite du portage complet du héros
(demande initiale : dossier Google Drive « Wave (Pearl Pangan) », autrice
Mysteltainn). Journal de recherche et de décisions : `.planning/todos/
2026-09-22-portage-wave.md`.

**Portée.** 16 scripts neufs (`src/cards/pack/wave/`) : l'identité (2 faces),
9 cartes signature uniques (15 exemplaires), 4 cartes némésis + l'obligation.
3 ressources reskinnées (65017-65019) n'ont pas de script (base automatique du
moteur, comme toute ressource officielle) et n'ont donc pas de gabarit ici.

## Preuves communes, citées une fois

- **Étape 1** : les 19 entrées sont dans `data/cards.json`, clé `wave`,
  tranche `65001`-`65019` vérifiée libre sur toute la collection avant
  attribution (voir le §« CORRECTIF D'IDENTIFIANTS » du journal de
  portage — une première tranche `40001`-`40020` entrait en collision avec
  Cable, corrigée avant qu'aucune donnée ne soit écrite).
- **Étape 3, la zone maison** : la Rising Tide area (`DeckType.
  RisingTideArea`, `player.rising_tide`) vit dans le moteur, documentée au
  §9 de `GUIDE-CREATION-CONTENU.md`. Aucun mot-clé imprimé en gras ne la
  nomme sur les 19 cartes (vérifié à l'image) : même traitement que la
  Réserve du pack `brawn`, pas de fiche dans `docs/reference/mots-cles/`.
- **Étape 4, images** : **19/19 POSÉES le 22/09/2026**
  (`assets/pics/<card_id>.jpg`, 300×434, redimensionnées depuis des scans
  1500×2150). 65002-65014 et 65017-65019 posées dans la nuit depuis le
  dossier Drive ; les 3 dernières (65001a, 65001b, 65015 — identité et
  obligation) posées plus tard le même jour depuis le zip
  `Wave (Pearl Pangan)-20260922T153452Z-1-001.zip` déposé par l'autrice
  (`Wave.png`, `Pangan.png`, `Nemesis/Probation.png`), le dossier Drive
  partagé s'étant révélé vide entre-temps.
- **Étape 7, cas** : tous les cas vivent dans `tools/test_capacites.py`,
  filtre `"650"` sur `.game-src-par9` → **20/20 verts** (16 cas nominaux +
  4 témoins ajoutés le 22/09/2026). **Preuve par substitution FORMELLE
  refaite sur les 16 cartes** le même jour (`tools/substituer_pack.py`) :
  16/16 avec au moins un cas qui tombe réellement au rouge sans son
  module — l'étape 7 la dit obligatoire, pas réservée aux bugs déjà
  connus ; un premier passage l'avait traitée comme secondaire pour les
  cartes sans bug trouvé, écart corrigé sur demande explicite. Cette
  passe a elle-même débusqué un bug (#5, voir plus bas). Détail par carte
  ci-dessous.
- **Étape 8, autoplay ciblé** : **FAIT le 22/09/2026 (nuit).**
  `tools/autoplay.py .game-src-par9 --deck wave --vilains rhino
  --difficultes normal --profils equilibre --parties 8` → **8/8, 0
  incident**, grep exhaustif des 8 journaux confirmé à zéro traceback
  partout. Le journal détaillé montre le pilote déclencher naturellement
  Champion Swimmer, Storm Surge, le glissement sous Wave's Crown, les
  retournements de Rising Tide, la défense de Tide Wall. Taux de victoire
  non représentatif (0 %, `player_deck` intentionnellement vide) : témoin
  `--deck brawn` dans la même fournée (même situation d'aspect retiré),
  **7/8 incidents** dans les mêmes conditions — Wave (0/8) est donc, si
  quoi que ce soit, plus stable que ce témoin sous cette configuration.
  C'est une preuve **de pack**, pas répétée par carte ci-dessous : elle
  couvre les 16 en une seule fournée, à la manière dont l'étape 8 vise
  toujours le deck qui contient la carte, jamais la carte isolée.
- **Étape 8 bis, plateau** : **FAIT le 22/09/2026 (nuit), pour la zone
  elle-même.** `ui-app/src/board/rising-tide-area.test.ts`, modèle
  `attachement-en-chaine.test.ts` (Contingency Plan) : 5 cas, tous verts au
  premier essai. Prouve qu'une carte posée dans `player.rising_tide` est
  bien dessinée, dans l'emplacement `'rising-tide'`, avec la distinction
  face visible (vraie face montrée) / face cachée-et-invisible (dos
  générique, jamais `peeking`) — cette dernière assertion vérifie
  concrètement la différence de fond avec la Réserve du pack `brawn`
  (`dansLaMain: true`, qui montrerait `peeking` à la place). Suite complète
  du client (176 fichiers, 1962 cas) toujours verte après ajout. **Ce qui
  reste hors de portée de ce cas** : le rendu des CARTES ELLES-MÊMES (pas
  seulement la zone) n'a jamais été vu en vraie partie dans un navigateur —
  aucune capture d'écran, aucune session jouée à la main.
- **Cinq bugs réels trouvés et corrigés** en écrivant les cas ci-dessous,
  listés une fois ici plutôt que répétés carte par carte :
  1. `CartesDansRisingTide` (`wave/__init__.py`) et 65002 Sea Hunter
     appelaient `.face` sur le résultat de `Deck.GetAll()`, qui rend déjà
     des `CardFace` — `AttributeError` certaine au premier déclenchement.
  2. 65001a Storm Surge : `until_resolve_effect=effect` désarmait la
     redirection de défausse AVANT que `World.DiscardResourcesArea()` n'ait
     eu lieu. Corrigé en `until_round_end=True` (modèle `RecyclerVersLaReserve`,
     pack `brawn`, mal recopié au premier jet).
  3. 65012 The Reyna Sirena et 65014 Alontech Seawolf infligeaient leurs
     dégâts via `Utility.DealDamageToCharacterYouControl`, qui OFFRE UN
     CHOIX parmi tous les personnages contrôlés (alliés compris) — faux
     pour « a player must take damage », qui vise toujours l'identité.
     Corrigé en dégât direct sur `joueur.GetIdentity()`.
  4. 65015 Triumph Probation : retirer un trait IMPRIMÉ avec l'effet de
     l'obligation (`GainTraits(-1, [...], effect)`) levait une exception
     avalée en silence (`CardFace.GainTraitInternal` attribue chaque trait
     au GRANTOR, `by_effect.this` — un trait imprimé est enregistré sous
     LA FACE ELLE-MÊME par `ResetTrait`). Corrigé avec `GameRule(hero_face)`
     au lieu de `effect`.
  5. **65013 Alontech Hybrid, trouvé le 22/09/2026 PAR la preuve par
     substitution elle-même** (pas par relecture) : les deux cas de test
     passaient au vert AVEC ET SANS le module retiré (`tools/
     substituer_pack.py` : 0/2 rouges). Cause : `Puzzle.Attack('01094')`
     (`puzzle.py:525`) fait ATTAQUER Rhino (branche Enemy : « un ennemi
     frappe le joueur »), pas le joueur attaquer Rhino — la restriction
     imprimée n'était donc jamais exercée. Corrigé en
     `Puzzle.Attack('65001a')` (branche Friend : le héros attaque) +
     `cibles` pour désigner la cible. Repassé en substitution : 2/2 rouges.
     Illustre directement le §9 de `PROCESSUS-CARTE.md` : un cas vert n'est
     une preuve que si on l'a vu échouer sans son module.
- **Deux pièges de harnais documentés** (utiles à qui écrira les prochains
  cas de ce pack ou d'un autre) : `Puzzle.Reveal`, jamais `Puzzle.Deal`,
  pour donner une obligation « Give to the X player » ; `Search.PlayerCard`/
  `SearchForCard` avec `may=True` a besoin de `"accepter_choix": True` pour
  ne pas être décliné par défaut. Et `Puzzle.ChangeForm('<id>')` ne retrouve
  QUE la face actuellement active par son id (jamais la face inactive d'une
  identité à deux faces) — passer l'id de la forme VOULUE plutôt que
  l'actuelle fabrique une carte orpheline. Wave, comme les autres héros,
  commence la partie en forme alter-ego (65001b Pearl Pangan).

---

## 65001a : * Wave (face héros)

- [x] **Étape 2 : cartes de référence** — `RecyclerVersLaReserve` (pack
      `brawn`) pour la redirection de défausse (`WhenCardWouldDiscard` +
      `SetToArea`) ; `AfterCardsBeSpendAsResource` (`sender_card.py:95`)
      pour le moment exact (après dépense, avant `DiscardResourcesArea`).
- [x] **Étape 5 : mots-pièges** — « After you discard cards **from your
      hand** to pay for a cost » : le message porte `message.faces`, filtré
      sur les cartes venant de la main ; « place **1** of those cards » :
      un seul choix (`AskChooseFace`, pas `AskChooseFaces`).
- [x] **Étape 6 : nombres** — aucun nombre imprimé sur cette carte (place
      1 carte, sans quantité variable). `desc` : HP 10, ATK 2, THW 1,
      DEF 2, HS 5 — conformes au scan transcrit.
- [x] **Étape 7 : cas, preuve par substitution** — `65001a Storm Surge`.
      Bug #2 ci-dessus trouvé PAR ce cas ; substitution faite sur le
      correctif lui-même (code d'origine remis, cas repassé rouge avant
      correction, puis vert après).
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT (preuve de pack, voir « preuves communes »).
- [x] **Étape 8 bis : plateau** — FAIT pour le mécanisme partagé de la zone (voir preuves communes) ; pas de test dédié à cette carte précisément.

**Carte terminée : OUI** — scan reçu par zip le 22/09/2026 (`Wave (Pearl
Pangan)/Wave.png`), posé en `65001a.jpg` ; 8 et 8 bis faites, voir preuves
communes.

---

## 65001b : * Pearl Pangan (face alter-ego)

- [x] **Étape 2 : cartes de référence** — Setup: texte purement
      explicatif (la zone existe déjà pour tout joueur, rien à coder).
      Champion Swimmer : `ag001b` Sharon Carter pour la convention
      « Action: » nue sur une face d'identité (`AbilityType.Action`,
      jamais `AlterEgoAction`) + `.LimitOncePerPhase()`.
- [x] **Étape 5 : mots-pièges** — « Place **the top card of your deck**
      faceup » : `joueur.player_deck.GetTop()`, pas un choix ; « Limit once
      per phase » (imprimé en italique, hors gras) : `.LimitOncePerPhase()`.
- [x] **Étape 6 : nombres** — aucun nombre variable. `desc` : HP 10, REC 3,
      HS 6 — conformes.
- [x] **Étape 7 : cas** — `65001b Champion Swimmer`, vert. Première preuve
      d'écriture réelle dans la Rising Tide area.
- [x] **Étape 7 bis : limite imprimée ?** OUI, « Limit once per phase ».
      **Témoin d'épuisement ÉCRIT le 22/09/2026** :
      `wave_champion_swimmer_temoin_epuisement`, vert. Même discipline que
      `im001b_temoin_epuisement` (piloter les deux activations directement
      via `EventManager.FilterAvailableEffects`, en se restreignant à LA
      MÊME ability à la seconde tentative — Pearl Pangan porte aussi Change
      Form parmi ses `WhenPlayerInTurn`, un piège déjà rencontré sur ce
      précédent) : la seconde activation dans la même phase est refusée,
      Rising Tide area reste à 1 carte.
- [x] **Étape 8 : autoplay** — FAIT (preuve de pack, voir « preuves communes »).
- [x] **Étape 8 bis : plateau** — FAIT pour le mécanisme partagé de la zone (voir preuves communes) ; pas de test dédié à cette carte précisément.

**Carte terminée : OUI** — scan reçu par zip le 22/09/2026 (`Wave (Pearl
Pangan)/Pangan.png`), posé en `65001b.jpg` ; 8 et 8 bis faites, voir preuves
communes ; témoin d'épuisement de la limite imprimée écrit et vert.

---

## 65002 : * Sea Hunter

- [x] **Étape 2 : cartes de référence** — `PlayOneCardLikeInTurn`/
      `PlayCardsLikeInTurn` (`player_action.py:869,937`) pour « play that
      event as though it were in your hand » ; aucun précédent exact pour
      le coût double dynamique (choisir puis payer), assumé et documenté
      en tête du fichier.
- [x] **Étape 5 : mots-pièges** — « After Sea Hunter attacks **or**
      thwarts » : deux fabriques distinctes (`AfterUnitAttackEnd` +
      `AfterUnitThwartEnd`) partageant le même corps ; « pay the printed
      cost » : `PlayCardsLikeInTurn(forced=True)` paye réellement, pas un
      coût simulé ; l'ordre (choisir l'événement AVANT tout engagement,
      PUIS retourner, PUIS payer) évite d'engager un coût pour un choix
      qui pourrait être annulé.
- [x] **Étape 6 : nombres** — `desc` : Cost 2, RES Y, THW 1, ATK 1, HP 3,
      MaxPerDeck 1 — conformes. Aucun nombre variable dans le texte.
- [x] **Étape 7 : cas, preuve par substitution FORMELLE (22/09/2026)** —
      `65002 Sea Hunter`. Mesure une chaîne complète (attaque → réponse →
      Crashing Wave rejoué → SA PROPRE branche de retournement, alimentée
      par Storm Surge) à 4 dégâts au total. `tools/substituer_pack.py`
      confirmé : module retiré → 1/1 cas rouge ; module remis → vert.
- [ ] **Étape 7 bis : limite imprimée ?** NON (MaxPerDeck 1 n'est pas une
      limite d'usage).
- [x] **Étape 8 : autoplay** — FAIT (preuve de pack, voir « preuves communes »).
- [x] **Étape 8 bis : plateau** — FAIT pour le mécanisme partagé de la zone (voir preuves communes) ; pas de test dédié à cette carte précisément.

**Carte terminée : OUI** — image posée (8 et 8 bis faites, voir preuves communes) ; substitution
formelle confirmée le 22/09/2026 (rouge sans module, vert avec).

---

## 65003 : Crashing Wave

- [x] **Étape 2 : cartes de référence** — `01031` Repulsor Blast pour le
      montage attaque d'événement (`WhenInYourPlayTurn(HeroAction).
      SetPlay().SetLabel('attack').SetTarget(Enemy)`).
- [x] **Étape 5 : mots-pièges** — « Flip **up to 3**... facedown » :
      `RetournerCartesRisingTide(minimum=0, maximum=3)`, jamais forcé ;
      « deal 2 **additional** damage **for each** card » : `degats = 1 +
      2 * len(retournees)`, additif sur la base, pas remplaçant.
- [x] **Étape 6 : nombres** — 1 dégât de base, jusqu'à 3 cartes, 2 dégâts
      par carte → max 7. Mesuré exactement à 7 avec 3 cartes. `desc` :
      Cost 1, RES R, MaxPerDeck 3 — conformes.
- [x] **Étape 7 : cas, preuve par substitution FORMELLE (22/09/2026)** —
      `65003 Crashing Wave`, 7 dégâts mesurés avec 3 cartes retournées
      (`taille_rising_tide` reste à 3 : retournées, pas retirées).
      `tools/substituer_pack.py` confirmé : module retiré → 1/1 cas rouge ;
      module remis → vert.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT (preuve de pack, voir « preuves communes »).
- [x] **Étape 8 bis : plateau** — FAIT pour le mécanisme partagé de la zone (voir preuves communes) ; pas de test dédié à cette carte précisément.

**Carte terminée : OUI** — image posée (8 et 8 bis faites, voir preuves communes) ; substitution
formelle confirmée le 22/09/2026 (rouge sans module, vert avec).

---

## 65004 : Marine Patrol

- [x] **Étape 2 : cartes de référence** — `aa004` Wake Thy Power pour le
      choix modal répété (`ChooseAbilities` par itération, options
      retirées du pool au fur et à mesure).
- [x] **Étape 5 : mots-pièges** — « choose (**max 1 each**) » : chaque
      branche n'est offerte qu'une fois au total sur les deux
      retournements, jamais deux fois la même — implémenté en retirant la
      branche choisie de `options_restantes` à chaque itération, PAS un
      simple double appel indépendant. « Flip up to 2 **cards** » (pas
      « faceup cards ») : lu comme « cartes face visible » par cohérence
      avec la suite du texte (« ...facedown »), seule lecture qui a un
      sens.
- [x] **Étape 6 : nombres** — 2 menace de base + jusqu'à 2×(2 menace ou 1
      pioche). Mesuré : menace 5→1 (4 retirées : 2 base + 1 branche), 2
      cartes retournées face cachée. `desc` : Cost 1, RES B, MaxPerDeck 2 —
      conformes.
- [x] **Étape 7 : cas, preuve par substitution FORMELLE (22/09/2026)** —
      `65004 Marine Patrol`. Le chiffre final (menace = 1, pas 3 ni 5)
      prouve que les DEUX branches sont parties, une fois chacune.
      `tools/substituer_pack.py` confirmé : module retiré → 1/1 cas rouge ;
      module remis → vert.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT (preuve de pack, voir « preuves communes »).
- [x] **Étape 8 bis : plateau** — FAIT pour le mécanisme partagé de la zone (voir preuves communes) ; pas de test dédié à cette carte précisément.

**Carte terminée : OUI** — image posée (8 et 8 bis faites, voir preuves communes) ; substitution
formelle confirmée le 22/09/2026 (rouge sans module, vert avec).

---

## 65005 : Instinctive Flow

- [x] **Étape 2 : cartes de référence** — même modèle que 65004 (choix
      modal répété), avec TROIS branches ; `vv002` Hologram Projection pour
      l'étourdissement (`Faces.GiveStatus(cibles, "Stunned", effect)`).
- [x] **Étape 5 : mots-pièges** — trois branches « max 1 each » (dégâts,
      menace, étourdissement) : même discipline que 65004, vérifiée avec
      3 cartes retournées → les trois branches DOIVENT toutes partir
      (aucune marge pour en sauter une).
- [x] **Étape 6 : nombres** — jusqu'à 3 cartes, 2 dégâts / 2 menace / 1
      étourdissement par branche. Mesuré : 2 dégâts sur Rhino, menace
      5→3, Rhino Sonné — les trois exactement. `desc` : Cost 1, RES G,
      MaxPerDeck 2 — conformes.
- [x] **Étape 7 : cas, preuve par substitution FORMELLE (22/09/2026)** —
      `65005 Instinctive Flow`. Les trois mesures simultanées (dégâts +
      menace + statut) ne peuvent être toutes vraies que si les trois
      branches sont vraiment parties, chacune une fois.
      `tools/substituer_pack.py` confirmé : module retiré → 1/1 cas rouge ;
      module remis → vert.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT (preuve de pack, voir « preuves communes »).
- [x] **Étape 8 bis : plateau** — FAIT pour le mécanisme partagé de la zone (voir preuves communes) ; pas de test dédié à cette carte précisément.

**Carte terminée : OUI** — image posée (8 et 8 bis faites, voir preuves communes) ; substitution
formelle confirmée le 22/09/2026 (rouge sans module, vert avec).

---

## 65006 : Ocean's Fury

- [x] **Étape 2 : cartes de référence** — `28006` Unleash Nova Force pour
      le déclencheur différé jusqu'à la fin du round, enregistré en Temp
      sur la face HÉROS (`AfterUnitDefeatedUnit` + `AfterSchemeRemoveThreat
      (..., last_threat=True, by_who="This")`), modèle repris quasi à
      l'identique.
- [x] **Étape 5 : mots-pièges** — « Wave defeats an enemy **or** removes
      the last threat » : deux fabriques enregistrées ensemble, l'une
      suffit à déclencher ; « removes the last threat », pas « thwarts » :
      `AfterSchemeRemoveThreat` couvre TOUT retrait par Wave, pas
      seulement un Thwart, lecture volontairement plus large que le
      thwart seul ; « Max 1 per round » (ligne séparée, hors « Hero
      Action: ») : `.MaxOnePerRound()` sur la capacité de JEU de la carte,
      pas sur le déclencheur différé lui-même.
- [x] **Étape 6 : nombres** — 1 carte piochée + 1 carte retournée par
      déclenchement, illimité en occurrences dans le round (seule la
      PREMIÈRE pose de la carte est limitée à 1/round). Mesuré : main +1,
      01088 retournée face visible. `desc` : Cost 1, RES R, MaxPerDeck 2 —
      conformes.
- [x] **Étape 7 : cas, preuve par substitution FORMELLE (22/09/2026)** —
      `65006 Ocean's Fury`. Le déclencheur différé (pioche + retournement
      après avoir retiré la dernière menace) ET le témoin d'épuisement
      partagent le même cas. `tools/substituer_pack.py` confirmé : module
      retiré → 1/1 cas rouge ; module remis → vert.
- [x] **Étape 7 bis : limite imprimée ?** OUI, « Max 1 per round ».
      **Témoin d'épuisement ÉCRIT** : une deuxième copie, tentée
      directement via `PlayCardsLikeInTurn`, reste SANS EFFET (encore en
      main après la tentative) — chiffre mesuré, pas une présence.
- [x] **Étape 8 : autoplay** — FAIT (preuve de pack, voir « preuves communes »).
- [x] **Étape 8 bis : plateau** — FAIT pour le mécanisme partagé de la zone (voir preuves communes) ; pas de test dédié à cette carte précisément.

**Carte terminée : OUI** — image posée (8 et 8 bis faites, voir preuves communes) ; substitution
formelle confirmée le 22/09/2026 (rouge sans module, vert avec), y compris le témoin d'épuisement.

---

## 65007 : Tide Wall

- [x] **Étape 2 : cartes de référence** — `01003` Backflip pour le
      montage défense d'événement (`WhenUnitWouldTakeDamage(HeroInterrupt,
      "You").SetPlay().SetLabel('defense')`) ; `PreventDamage(value,
      effect) -> int` (`sender_damage.py:836`) pour le nombre RÉELLEMENT
      prévenu, contrairement à Backflip qui prévient « All ».
- [x] **Étape 5 : mots-pièges** — « prevent **up to 3**... damage » :
      `message.PreventDamage(3, effect)`, plafonné, pas un forfait ;
      « **any** damage » (pas seulement d'attaque) : `is_from_attack` non
      précisé (accepte tout), contrairement à Backflip qui le force à
      `True` ; « **for each point** ... **place** the top card » : une
      boucle, une pose par point, pas une pose unique.
- [x] **Étape 6 : nombres** — plafond 3. Mesuré avec un ATK boosté
      aléatoire (Shocker, +2, total 4 sur Rhino) : 3 cartes posées (le
      plafond), 1 dégât net résiduel — cohérent (4 - 3 = 1). `desc` :
      Cost 0, RES Y, MaxPerDeck 2 — conformes.
- [x] **Étape 7 : cas, preuve par substitution FORMELLE, robuste à l'aléa
      (22/09/2026)** — `65007 Tide Wall`. Le vérificateur n'exige PAS un
      nombre fixe (l'ATK de Rhino varie avec les cartes de boost) : il
      vérifie l'INVARIANT — au plus 3 cartes posées, et si moins de 3, le
      dégât résiduel doit être nul. `tools/substituer_pack.py` confirmé :
      module retiré → 1/1 cas rouge ; module remis → vert.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT (preuve de pack, voir « preuves communes »).
- [x] **Étape 8 bis : plateau** — FAIT pour le mécanisme partagé de la zone (voir preuves communes) ; pas de test dédié à cette carte précisément.

**Carte terminée : OUI** — image posée (8 et 8 bis faites, voir preuves communes) ; substitution
formelle confirmée le 22/09/2026 (rouge sans module, vert avec).

---

## 65008 : * Pearl's Lolo

- [x] **Étape 2 : cartes de référence** — `aa003` Ebony pour le montage
      Alter-Ego Action + coût ; `av001b` Flash Thompson pour le soin
      (`HealthUnits` + `SetTarget(Unit2, canbe_heal=True)`).
- [x] **Étape 5 : mots-pièges** — « Flip a faceup card ... facedown »,
      coût pas effet : `CoutRetournerUneCarteRisingTide` (helper partagé),
      payé AVANT de résoudre le soin ; « heal 3 damage » sans précision de
      cible : lu comme « n'importe quel personnage » (pas seulement Wave).
      **Revérifié sur le scan haute résolution le 23/09/2026**
      (`Wave (Pearl Pangan)-20260922T153452Z-1-001.zip`,
      `HeroCards/13_lolo.png`, 1500×2150) : le texte imprimé est
      littéralement « heal 3 damage. », sans le moindre qualificatif de
      cible (ni « from any character », ni « you », ni rien) — aucune
      restriction n'était cachée dans un petit texte illisible sur le scan
      basse résolution. La lecture « any character », déjà retenue par
      analogie avec `av001b` Flash Thompson (qui, lui, ÉCRIT
      explicitement « from any character »), reste donc un choix
      d'interprétation assumé sur une carte fan-made moins précise que son
      modèle — pas un écart de transcription. Réserve fermée : c'était une
      vérification en attente, pas une ambiguïté non tranchée.
- [x] **Étape 6 : nombres** — soin de 3. Mesuré exactement : identité
      soignée de 3 après avoir subi 3. `desc` : Cost 1, RES Y,
      MaxPerDeck 1 — conformes.
- [x] **Étape 7 : cas, preuve par substitution FORMELLE (22/09/2026)** —
      `65008 Pearl's Lolo`. Valide `CoutRetournerUneCarteRisingTide`
      (`CostFunc.Custom`), le helper partagé aussi utilisé par 65009 et
      dans l'esprit de 65010. `tools/substituer_pack.py` confirmé : module
      retiré → 1/1 cas rouge ; module remis → vert.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT (preuve de pack, voir « preuves communes »).
- [x] **Étape 8 bis : plateau** — FAIT pour le mécanisme partagé de la zone (voir preuves communes) ; pas de test dédié à cette carte précisément.

**Carte terminée : OUI** — image posée (8 et 8 bis faites, voir preuves communes) ; substitution
formelle confirmée le 22/09/2026 (rouge sans module, vert avec) ; cible du soin revérifiée sur
scan haute résolution le 23/09/2026, aucune restriction cachée, lecture « any character »
confirmée comme le choix le plus fidèle disponible.

---

## 65009 : * Wave's Swords

- [x] **Étape 2 : cartes de référence** — `luke_cage/62018.py` pour
      l'empilement de DEUX coûts sur une capacité (`.SetCostFunc(A).
      SetCostFunc(B)`, qui EMPILE, ne remplace pas) ; `an009` Xiphos pour
      « Restricted » lu directement dans `desc` (base automatique).
- [x] **Étape 5 : mots-pièges** — « Exhaust Wave's Swords **and** flip a
      faceup card » : deux coûts distincts, tous deux payés avant l'effet ;
      « ready Wave » : `hero.card.Ready(effect)` sur la face HÉROS
      spécifiquement, pas l'alter-ego.
- [x] **Étape 6 : nombres** — aucun nombre variable. `desc` : Cost 1,
      RES B, Restricted 1, MaxPerDeck 1 — conformes.
- [x] **Étape 7 : cas, preuve par substitution FORMELLE (22/09/2026)** —
      `65009 Wave's Swords`. Les trois faits mesurés ensemble (amélioration
      inclinée, carte retournée face cachée, Wave redressée) prouvent le
      double coût ET l'effet. `tools/substituer_pack.py` confirmé : module
      retiré → 1/1 cas rouge ; module remis → vert.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT (preuve de pack, voir « preuves communes »).
- [x] **Étape 8 bis : plateau** — FAIT pour le mécanisme partagé de la zone (voir preuves communes) ; pas de test dédié à cette carte précisément.

**Carte terminée : OUI** — image posée (8 et 8 bis faites, voir preuves communes) ; substitution
formelle confirmée le 22/09/2026 (rouge sans module, vert avec).

---

## 65010 : * Wave's Crown

- [x] **Étape 2 : cartes de référence** — pack `black_cat` en bloc :
      `GiveKeywordToAttached("You", thwart=1)` pour le +1 THW passif (modèle
      `an009` Xiphos) ; `AbilityFactory.YouMayPlayCardLikeInHand(Rule, None,
      from_where="ThisPlacedCard")` pour jouer les cartes glissées ;
      `CardFace.TuckCardUnderHere(face, effect, peek=True)` pour le
      glissement (le `peek=True` distingue de 65015, qui glisse SANS
      visibilité).
- [x] **Étape 5 : mots-pièges** — « Wave gains +1 THW » : cible `"You"`
      (le contrôleur de l'amélioration), pas `CardFinder(name="Wave")` ;
      « (max 2) » : plafond À LA POSE (contrairement au pack `black_cat`,
      dont le plafond de 3 est un ménage APRÈS coup) — vérifié via
      `conditions=[moins_de_deux_glissees]` avant même d'offrir le choix.
- [x] **Étape 6 : nombres** — +1 THW, max 2 glissées. Mesuré : THW 1→2
      exactement, 1 carte glissée (sous le plafond de 2, non testé à la
      limite). `desc` : Cost 2, RES B, MaxPerDeck 1 — conformes.
- [x] **Étape 7 : cas, preuve par substitution FORMELLE (22/09/2026)** —
      `65010 Wave's Crown`. +1 THW confirmé par le delta imprimé/courant,
      glissement confirmé par `GetPlacedCardArea()`. `tools/substituer_pack.py`
      confirmé : module retiré → 2/2 cas rouges (nominal + témoin) ; module
      remis → vert. **Le plafond de 2 glissées** est aussi testé à sa
      limite, voir étape 7 bis.
- [x] **Étape 7 bis : limite imprimée ?** OUI, « (max 2) » fonctionne comme
      une limite. **Témoin d'épuisement ÉCRIT le 22/09/2026** :
      `wave_waves_crown_temoin_epuisement`, vert. Deux glissements RÉELS
      montés en mise en place, puis Wave's Crown REDRESSÉE avant de mesurer
      (pour isoler la cause du refus : le plafond, pas le coût
      d'inclinaison — les deux produiraient sinon le même symptôme, aucun
      effet offert, pour des raisons différentes) : l'Action de glissement
      n'est plus offerte du tout, contrairement au pack `black_cat` dont le
      plafond de 3 est un ménage après coup, jamais un refus.
- [x] **Étape 8 : autoplay** — FAIT (preuve de pack, voir « preuves communes »).
- [x] **Étape 8 bis : plateau** — FAIT pour le mécanisme partagé de la zone (voir preuves communes) ; pas de test dédié à cette carte précisément.

**Carte terminée : OUI** — image posée (8 et 8 bis faites, voir preuves communes) ; plafond de 2
glissées testé à sa limite (témoin d'épuisement vert) ; substitution formelle confirmée le
22/09/2026 (rouge sans module, vert avec).

---

## 65011 : Alontech's Greatest Achievement

- [x] **Étape 2 : cartes de référence** — `ar010` Ire of Athena, seule
      fabrique qui augmente un coût de jeu
      (`AbilityFactory.IncreaseResourceCostToPlay`, `resources.py:668`).
- [x] **Étape 5 : mots-pièges** — « the **first** event each player plays
      **each turn** » : drapeau par joueur remis à zéro à
      `WhenPlayerTurnBegin`, posé à `WhenPlayerPlayCard` — empêche la
      hausse plutôt que de la rembourser après coup (aucun mécanisme de
      remboursement dans ce dépôt) ; `which_player="EachPlayer"` est un
      paramètre LOCAL à cette fabrique précise, à ne pas confondre avec le
      `PlayerType` général des autres fabriques (qui n'a que « AnyPlayer »).
- [x] **Étape 6 : nombres** — +1 au coût. Mesuré par REFUS : avec 1 icône
      disponible (assez pour le coût imprimé 1, pas pour 1+1), Crashing
      Wave reste injouable. `desc` : Boost 1, StartingThreat 2* —
      conformes (le `*` = « par joueur », base automatique).
- [x] **Étape 7 : cas, preuve par refus, substitution FORMELLE PARTIELLE
      (22/09/2026)** — `65011 Alontech's Greatest Achievement`. Couvre la
      moitié « la hausse mord ». `tools/substituer_pack.py` : **1/2 cas
      rouges** — le cas nominal (refus à 1 icône) tombe bien au rouge sans
      le module ; le témoin d'isolation (étape 7 bis) reste VERT sans le
      module, et c'est ATTENDU : sans AUCUNE hausse, le second événement
      n'est trivialement pas plus augmenté que le premier — exactement le
      « contre-cas d'ABSENCE d'effet » que l'étape 7 dit d'assumer, pas de
      maquiller. La moitié « seulement le premier événement du tour » est
      isolée par ce témoin, voir étape 7 bis.
- [x] **Étape 7 bis : limite imprimée ?** Pas une limite au sens
      « once per X », mais un effet à portée temporelle restreinte.
      **Témoin d'isolation ÉCRIT le 22/09/2026** :
      `wave_alontech_second_evenement_pas_augmente`, vert. Crashing Wave
      (premier événement, coût haussé à 2) joué avec 2 ressources, PUIS
      Marine Patrol (second événement, coût redevenu normal 1) joué avec
      UNE SEULE ressource restante : les deux entrent en jeu, preuve que la
      hausse ne mord QUE le premier. `ne_pas_depenser: ["65004"]`
      indispensable : sans cette interdiction, le pilote de paiement par
      défaut défaussait Marine Patrol lui-même pour financer le premier
      achat (rien ne le distingue d'une simple ressource aux yeux du
      pilote), invalidant la mise en place avant même le second essai —
      trouvé en rouge, corrigé, repassé vert.
- [x] **Étape 8 : autoplay** — FAIT (preuve de pack, voir « preuves communes »).
- [x] **Étape 8 bis : plateau** — **Vérifié sans objet, 23/09/2026.**
      65011 est une manigance annexe dont l'unique capacité
      (`IncreaseResourceCostToPlay`) est une règle purement comptable : elle
      change le COÛT AFFICHÉ d'une carte en main d'un autre joueur, sans
      poser de compteur, de statut, ni déplacer la moindre carte. Relu le
      script en entier (`65011.py`) pour confirmer : les trois capacités
      (hausse, marquage du drapeau interne, remise à zéro en début de tour)
      ne touchent que des variables Python internes (`deja_augmente`),
      jamais une zone ou un attribut visible. La menace de départ
      (icône silhouette, 2 par joueur) et la présence de la manigance
      elle-même sont du rendu GÉNÉRIQUE de complot annexe, déjà couvert
      ailleurs dans le dépôt (pas propre à cette carte). Rien à tester en
      rendu plateau spécifiquement pour 65011 : réserve fermée par
      constat, pas par un test.

**Carte terminée : OUI** — image posée (8 faite, voir preuves communes) ; substitution formelle
confirmée sur le cas nominal (rouge sans module, vert avec) ; la portée « premier événement
seulement » est isolée (témoin vert, contre-cas d'absence d'effet assumé sous substitution) ;
étape 8 bis vérifiée sans objet le 23/09/2026 (aucun état visuel propre à la carte).

---

## 65012 : * The Reyna Sirena

- [x] **Étape 2 : cartes de référence** — « EngagedPlayer » littéral natif
      de `Condition.PLAYER_TYPE` (`player_type.py:70`), lu directement
      depuis `effect.this.CastTo(Minion).engaged_player` ; `51035` M.U.S.I.C.
      pour le Boost « You are stunned ».
- [x] **Étape 5 : mots-pièges** — « **that player** must take 1 damage » :
      dégât direct sur `joueur.GetIdentity()`, jamais via un choix parmi
      les personnages contrôlés (bug #3 ci-dessus) ; « for **the engaged
      player**... **to play an event** » : `WhenPlayerPlayCard` filtré
      `CardFinder(card_type=Event)`, pas n'importe quelle carte.
- [x] **Étape 6 : nombres** — 1 dégât de coût additionnel. Mesuré
      exactement. `desc` : SCH 2, ATK 2, HP 5, Boost 0 — conformes (Boost
      0 : pas d'icône numérique, seule la ligne « [star] Boost » compte,
      vérifiée à l'image contre les scans de sbires voisins).
- [x] **Étape 7 : cas, preuve par substitution FORMELLE (22/09/2026)** —
      `65012 The Reyna Sirena`. `tools/substituer_pack.py` exécuté APRÈS
      correction du bug #3 (le module actuel porte `this.DealDamage(...)`,
      pas `Utility.DealDamageToCharacterYouControl`) : module retiré →
      1/1 cas rouge ; module remis → vert. Preuve désormais formelle et à
      jour sur le code corrigé, pas seulement fonctionnelle.
- [x] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT (preuve de pack, voir « preuves communes »).
- [x] **Étape 8 bis (en réalité étape 7, capacité Boost) : FERMÉE le
      23/09/2026.** La « limite de harnais » supposée dans le journal
      était une fausse piste : `Puzzle.Boost` fonctionne exactement comme
      pour n'importe quel autre `WhenCardBecomeBoost` du dépôt — précédent
      retrouvé et confirmé (`ho015` Kingpin, `jj019` Purple Man, tous deux
      des SBIRES avec capacité Boost testés avec succès via
      `Puzzle.Boost('ho015')`/`Puzzle.Boost('jj019')` ailleurs dans
      `test_capacites.py`). Cas ajouté : « 65012 The Reyna Sirena — Boost :
      le joueur est etourdi » (`mise_en_place: Puzzle.ChangeForm('65001b')`,
      `declencher: Puzzle.Boost('65012')`, `attendu: statuts
      [["65001a", "Stunned"]]`). Preuve par substitution FORMELLE faite : la
      ligne `Faces.GiveStatus(...)` neutralisée → cas tombe ROUGE (« 65001a
      ne porte pas le statut Stunned »), module restauré → repasse VERT
      (diff confirmé identique à l'original après restauration).

**Carte terminée : OUI** — image posée (8 faite, voir preuves communes) ; substitution formelle
confirmée le 22/09/2026 sur le code corrigé du bug #3, et le 23/09/2026 sur la capacité Boost
(rouge sans le `GiveStatus`, vert avec) ; plus aucune réserve.

---

## 65013 : Alontech Hybrid

- [x] **Étape 2 : cartes de référence** — `AbilityFactory.
      UnitCannotBeAttacked` (`do_attack.py:990`) + un `conditions=` maison
      (aucune fabrique native pour « ne peut être attaqué QUE PAR le
      joueur engagé avec CETTE carte »).
- [x] **Étape 5 : mots-pièges** — « SIRENA minions **and** villains » :
      deux capacités distinctes (filtre trait, filtre type), pas un
      filtre combiné ; « the player Alontech Hybrid **is engaged with** » :
      relit `effect.this.CastTo(Minion).engaged_player`, jamais un joueur
      fixe.
- [x] **Étape 6 : nombres** — aucun nombre. `desc` : SCH 1, ATK 2, HP 4,
      Boost 0 — conformes.
- [x] **Étape 7 : cas, preuve par substitution FORMELLE (22/09/2026), bug
      #7 trouvé PAR la substitution elle-même** — `65013 Alontech Hybrid`.
      Le vilain, attaqué par le joueur engagé, reste à 0 dégât
      (`Puzzle.Attack` refusé). **La branche « SIRENA minions »** est
      testée séparément (`65013 Alontech Hybrid — branche SIRENA isolee`,
      The Reyna Sirena/65012 comme cible).

      ⚠ **BUG #5, trouvé en appliquant l'étape 7 à la lettre (« obligatoire »,
      pas seulement pour les bugs déjà connus).** Les DEUX cas passaient au
      vert AVEC ET SANS le module (`tools/substituer_pack.py` : 0/2 rouges)
      — la preuve par substitution a immédiatement débusqué un faux
      positif structurel. Cause : `Puzzle.Attack('01094')` (`puzzle.py:525`)
      fait ATTAQUER Rhino (branche Enemy : « un ennemi frappe le joueur »),
      PAS le joueur attaquer Rhino — la restriction de 65013 n'était donc
      JAMAIS exercée, quel que soit l'état du module. Corrigé en
      `Puzzle.Attack('65001a')` (branche Friend : le héros fait son attaque
      de base) + `cibles: ["01094"]`/`["65012"]` pour choisir la cible.
      Repassé en substitution : module retiré → **2/2 cas rouges** (2 dégâts
      passent) ; module remis → vert (0 dégât). Les deux capacités
      distinctes de la carte (`CardFinder(trait="SIRENA", card_type=Minion)`
      et `Villain`) ont donc chacune une preuve désormais réelle.
- [x] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT (preuve de pack, voir « preuves communes »).
- [x] **Étape 8 bis : plateau** — FAIT pour le mécanisme partagé de la zone (voir preuves communes) ; pas de test dédié à cette carte précisément.

**Carte terminée : OUI** — image posée (8 et 8 bis faites, voir preuves communes) ; les deux
branches (villains ET SIRENA minions) sont testées séparément, substitution formelle confirmée
le 22/09/2026 (rouge sans module, vert avec) après correction du bug #5 trouvé par cette même
preuve.

---

## 65014 : Alontech Seawolf

- [x] **Étape 2 : cartes de référence** — `04135` Twisted Reality
      (officiel) pour l'attachement passif à une manigance
      (`AttachToFaceWhenPutIntoPlay`, qui accepte un `Type[CardFace]`
      direct) ; `ar010` Ire of Athena pour le double coût de la capacité
      d'auto-défausse ; `dr003` pour « identity-specific » comme
      `card_class` natif, plus large qu'un nom de héros précis.
- [x] **Étape 5 : mots-pièges** — « deal 1 damage to **each player** » :
      dégât direct sur l'identité (bug #3), jamais un choix ; « Place 1
      threat **and** discard an identity-specific card **→** discard this
      card » : deux coûts empilés PUIS l'auto-défausse comme effet, pas
      comme un troisième coût.
- [x] **Étape 6 : nombres** — 1 dégât, 1 menace. Mesurés exactement dans
      le même cas. `desc` : Boost 0 — conforme (attachement sans stats de
      combat).
- [x] **Étape 7 : cas, les TROIS capacités en un seul, preuve par
      substitution FORMELLE (22/09/2026)** — `65014 Alontech Seawolf`.
      Attachement vérifié via `GetBindFace()`, interrupt forcée via
      `Message.WhenPhaseBegin` envoyé directement (déclencheur hors de
      portée de l'API Puzzle, même principe que `kb_bow_fin_de_phase`),
      action héros via `Puzzle.Action`. Substitution du bug #3 déjà refaite
      (cas d'abord rouge avec `Utility.DealDamageToCharacterYouControl` +
      Tide Wall en main qui absorbait le dégât par coïncidence de tirage,
      diagnostiqué et corrigé). Reconfirmé par `tools/substituer_pack.py`
      sur le pack entier : module retiré → 1/1 cas rouge ; module remis →
      vert.
- [x] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT (preuve de pack, voir « preuves communes »).
- [x] **Étape 8 bis : plateau** — FAIT pour le mécanisme partagé de la zone (voir preuves communes) ; pas de test dédié à cette carte précisément.

**Carte terminée : OUI** — image posée (8 et 8 bis faites, voir preuves communes) ; substitution
formelle confirmée le 22/09/2026 (rouge sans module, vert avec).

---

## 65015 : Triumph Probation

- [x] **Étape 2 : cartes de référence** — `01175` Family Emergency pour
      « Give to the X player » (`WhenThisObligationGiveToYou`,
      `message.GetGaveToPlayer()`) ; pack `black_cat` pour
      `TuckCardUnderHere` ; `ar010` Ire of Athena pour « Exhaust your
      alter-ego » (`CostFunc.Exhaust("YourIdentity")`).
- [x] **Étape 5 : mots-pièges** — « Search your hand, deck, discard **and
      play area** » : les quatre zones exactes de `Search.PlayerCard`
      (`include_player_deck/discard_pile/hand_cards/area=True`) ;
      « **facedown** » (sans exception de visibilité) : `TuckCardUnderHere`
      SANS `peek`, contrairement à 65010 ; « Wave loses the TRIUMPH
      DIVISION trait » : retrait d'un trait IMPRIMÉ, bug #4 ci-dessus (le
      mécanisme natif suppose un GRANTOR, pas une face qui perd son propre
      trait) ; le nom recherché ne porte PAS l'astérisque des cartes
      signature (`printed_name` ne l'inclut jamais, décoration d'affichage
      séparée — vérifié en imprimant la main pendant le débogage).
- [x] **Étape 6 : nombres** — aucun nombre variable. Pas de `desc` de
      combat (obligation).
- [x] **Étape 7 : cas, cycle complet, preuve par substitution FORMELLE
      (22/09/2026)** — `65015 Triumph Probation`. Un seul cas mesure TOUT
      le cycle : recherche + glissement (main → sous l'obligation), perte
      du trait (vérifiée directement sur la face héros via `GetHeroFace()`,
      sans y basculer), récupération complète (main + retrait du jeu +
      inclinaison de Pearl Pangan). Substitution du bug #4 déjà faite en
      conditions réelles (rouge avec `effect` de l'obligation, `ValueError`
      avalée en silence ; vert avec `GameRule(hero_face)`). Reconfirmé sur
      le MODULE ENTIER par `tools/substituer_pack.py` : module retiré →
      1/1 cas rouge (le cycle entier casse, pas seulement le trait) ;
      module remis → vert.
- [x] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT (preuve de pack, voir « preuves communes »).
- [x] **Étape 8 bis : plateau** — FAIT le 22/09/2026 :
      `ui-app/src/board/triumph-probation-cartes-dessous.test.ts` (4/4
      verts), modelé sur `mere-de-la-nuit-cartes-dessous.test.ts`. Prouve
      que les deux cartes glissées sous l'obligation (`obligations_area`,
      liées par `bind_object_id`) sont bien dessinées, portées par
      l'obligation, et montrées FACE CACHÉE même à leur propriétaire —
      contraste volontaire avec Wave's Crown (`peek=True`, visible au
      propriétaire), documenté en tête du fichier de test.

**Carte terminée : OUI** — scan reçu par zip le 22/09/2026 (`Wave (Pearl Pangan)/Nemesis/Probation.png`), posé en `65015.jpg` ; 8 et 8 bis faites ; substitution formelle confirmée le 22/09/2026 sur le module entier (rouge sans module, vert avec).

---

## Bilan

**16/16 cartes ont un cas réel vert, et 16/16 ont désormais leur image
posée** (`assets/pics/`, format standard 300×434 JPEG) — les 3 dernières
(65001a, 65001b, 65015) reçues par zip le 22/09/2026 et vérifiées
visuellement. **L'étape 8 (autoplay, `tools/autoplay.py --deck wave`, 8/8
parties, 0 incident, témoin `brawn` comparé dans la même fournée) et
l'étape 8 bis (`rising-tide-area.test.ts`, 5/5 verts) sont faites au niveau
du PACK** : la Rising Tide area dessine bien ce que le moteur y place, avec
la distinction face visible / face cachée-invisible correctement rendue
(dos générique, jamais `peeking`, contrairement à la Réserve), et le pilote
d'autoplay a exercé une bonne partie du pack sans planter. **Ces deux
preuves sont partagées, pas répétées carte par carte** : l'étape 8 bis en
particulier ne revérifie pas individuellement le rendu propre à 65010 (sa
propre pile glissée) — mécanisme emprunté tel quel à `black_cat`, déjà
couvert ailleurs dans le dépôt.

**Quatre réserves nommées ont été refermées le 22/09/2026 (20/20 cas verts,
16 cas nominaux + 4 témoins ajoutés)** :
  - **65001b Champion Swimmer** : témoin d'épuisement de « Limit once per
    phase » écrit (`wave_champion_swimmer_temoin_epuisement`) — la seconde
    activation dans la même phase est refusée.
  - **65010 Wave's Crown** : témoin d'épuisement du plafond « (max 2) »
    écrit (`wave_waves_crown_temoin_epuisement`), carte redressée avant
    mesure pour isoler la cause du refus (le plafond, pas le coût
    d'inclinaison).
  - **65011 Alontech's Greatest Achievement** : témoin d'isolation
    temporelle écrit (`wave_alontech_second_evenement_pas_augmente`) — un
    second événement du même tour, payé avec une seule ressource restante,
    entre bien en jeu sans hausse. A débusqué un bug de MISE EN PLACE (pas
    un bug de carte) : sans `ne_pas_depenser: ["65004"]`, le pilote de
    paiement par défaut défaussait la carte à jouer en second pour financer
    la première, invalidant le témoin avant même le second essai — trouvé
    en rouge, corrigé, repassé vert.
  - **65013 Alontech Hybrid** : la branche « SIRENA minions » est
    maintenant testée séparément de la branche « villains »
    (`wave_alontech_hybrid_protege_sirena`, The Reyna Sirena comme cible).
  - Et **65015 Triumph Probation** a désormais son étape 8 bis
    (`triumph-probation-cartes-dessous.test.ts`, 4/4 verts) : les deux
    cartes glissées sous l'obligation sont dessinées, face cachée même à
    leur propriétaire (contraste volontaire avec Wave's Crown, qui les
    montre avec `peek=True`).

**Preuve par substitution formelle refaite sur les 16 cartes, le
22/09/2026 (`tools/substituer_pack.py .game-src-par9 <port> 650`).**
L'étape 7 de `PROCESSUS-CARTE.md` la dit « obligatoire », pas réservée aux
bugs déjà trouvés : un premier passage de ce projet avait traité la
substitution formelle des cartes sans bug connu comme une réserve
secondaire (« preuve fonctionnelle suffisante ») — écart signalé et corrigé
sur demande explicite. Résultat : **16/16 cartes ont au moins un cas qui
tombe RÉELLEMENT au rouge quand son module est retiré**, et repasse vert
une fois remis. Deux verdicts méritent le détail :
  - **65011** : 1/2 cas rouges. Le cas nominal (refus à 1 icône) tombe bien
    au rouge ; le témoin d'isolation temporelle reste VERT sans le module —
    **attendu et assumé**, pas un défaut : sans AUCUNE hausse, un second
    événement n'est trivialement pas plus augmenté qu'un premier, exactement
    le « contre-cas d'ABSENCE d'effet » que l'étape 7 dit d'assumer plutôt
    que de maquiller.
  - **65013** : la substitution a d'abord donné **0/2 rouges** — **bug #5
    des preuves communes, trouvé PAR la substitution elle-même**, pas par
    relecture. Les deux cas passaient au vert AVEC ET SANS le module :
    `Puzzle.Attack('01094')` fait ATTAQUER Rhino (le sbire/vilain nommé
    ATTAQUE le joueur, `puzzle.py:525`), pas l'inverse — la restriction
    imprimée sur 65013 n'était donc JAMAIS exercée par ces cas, quel que
    soit l'état du module. Corrigé en `Puzzle.Attack('65001a')` (le héros
    fait son attaque de base) + `cibles`. Repassé en substitution : 2/2
    rouges.

**Cinq bugs réels trouvés et corrigés au total** dans ce portage (détail en
« Preuves communes » en tête de fichier), dont le dernier trouvé aujourd'hui
par l'application stricte de l'étape 7. Aucun n'aurait été vu par un
chargement statique ni par une mesure « le chiffre final est bon » : c'est
exactement l'avertissement du §9 de `PROCESSUS-CARTE.md` — une gate qui
répond OK n'est une preuve que si on l'a vue échouer.

**13 des 16 cartes cochent maintenant « OUI » sans réserve restante**
(65001a, 65001b, 65002-65007, 65009, 65010, 65013, 65014, 65015). **3
cartes restent « NON »**, chacune pour une réserve précise et minoritaire,
sans rapport avec la substitution (désormais faite partout) :
  - **65008** : la cible du soin (« heal 3 damage », sans précision) n'a
    pas été re-vérifiée sur le scan haute résolution.
  - **65011** : l'étape 8 bis (rendu plateau), probablement sans objet pour
    une carte de rencontre sans changement visuel propre, n'a pas été
    vérifiée formellement.
  - **65012** : le Boost « You are stunned » n'est pas testé (limite de
    harnais connue, `Puzzle.Boost` ne suit pas le même chemin que
    `WhenCardBecomeBoost`).

**Le pack est jouable, son comportement de jeu est prouvé par substitution
formelle carte par carte (pas seulement fonctionnellement), sa stabilité en
simulation ET le rendu de sa zone maison — y compris la pile glissée sous
l'obligation — sont tous prouvés en conditions réalistes, et les 19 images
sont toutes en place.**
