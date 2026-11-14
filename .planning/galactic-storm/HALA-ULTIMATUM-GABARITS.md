# Gabarits PROCESSUS-CARTE.md — Scénario 3 Hala Ultimatum (gs138-gs155), lot GS-6

Preuves : `Fusion/marvel-lcg-src/tools/cas/hala_ultimatum.py` (filtre `[hu]`), bilan **23/23 cas verts**
(20/10/2026, après correctifs ci-dessous). `test_cards` : 6970/6970 constructions OK, 0 erreur.
`verifier_appels_modules galactic_storm` : OK. Autoplay ciblé : 8 parties (`gs_hala_ultimatum`,
normal+expert, deck spider_man), 0 incident, 0 trace d'erreur dans les 8 journaux ; le remplacement de
l'attaque HIDDEN par une carte de rencontre face cachée est VU dans le journal d'une vraie partie (ligne
« "WhenUnitWouldAttack" est remplacé par Kree Leader »).

**CORRECTIF MAJEUR (20/10/2026) : la « limite outillage » décrite ci-dessous dans les versions
précédentes de ce rapport était un faux diagnostic.** Cause réelle, trouvée par sonde directe
(`GetAbilities()` jamais appelée) : `.game/` (cache bytecode du moteur, `sys.path` prioritaire sur
`src/`) datait du 14/10/2026, AVANT la création de tout le contenu `galactic_storm/hala_ultimatum/` —
aucune des capacités du lot ne s'exécutait, silencieusement (`cards/database.py`, `except: pass` sur
l'import du module). Remède : `python launcher_fast.py --build-only --no-browser` après CHAQUE
modification de `src/`, pour recompiler le delta dans `.game/` (incrémental, < 1s une fois l'historique
construit). Sans ce rebuild, aucun test ne reflète le code réellement édité. L'ancien `.game` a été
déplacé en `.game.obsolete-2026-10-14/` (non supprimé, à la demande de l'utilisateur de ne jamais
détruire sans confirmation) ; `.game` a été reconstruit à neuf (8245 fichiers, 0 échec).

Une fois le cache reconstruit, 6 vrais bugs de script sont apparus (masqués jusqu'ici) et ont été
corrigés :
- `gs150.py`/`gs152.py` : `Ability.SetTarget(..., check_face_fn=...)` — paramètre inexistant sur
  `SetTarget` (il vit sur `CardFinder`). Corrigé en `finder=CardFinder(check_face_fn=...)` (gs150,
  motif `bind_to=CardFinder(card_type=Enemy)` encore plus direct) / `finder=CardFinder(...)` (gs152).
  Plantage réel à l'exécution (`TypeError`), pas une question de preuve.
- `gs153.py` : `Worlds.DiscardEncounterCardsUntil(..., finder=CardFinder(...))` — pas de paramètre
  `finder` sur cette fonction (seulement `**kwargs` relayés direct au `CardFinder` final). Corrigé en
  `check_face_fn=...` en kwarg direct. Plantage réel (`TypeError`), idem.
- Les cas de test eux-mêmes contenaient plusieurs erreurs d'hypothèse (`Puzzle.PlaceCounters` AJOUTE des
  compteurs, il ne les POSE jamais à une valeur absolue ; `Puzzle.CreateEncounterDeck` empile la DERNIÈRE
  carte citée AU-DESSUS ; un `Puzzle.Thwart`/`Puzzle.Attack` sans cible explicite peut tomber sur la
  manigance principale plutôt que la manigance visée ; la mise en place réelle engage déjà un sbire Kree
  avant que `DECK_NEUTRE` ne s'applique) : corrigées une à une, détail dans les sections par carte.

---

## gs138a / gs139a / gs140a : Kree Leader (I/II/III), face HIDDEN

- [x] Étape 2 : cartes de référence : immunité = brique commune `AbilityFactory.CannotBeAffectedByPlayerCards`
      (déjà codée, `mots-cles/immunite-cartes-joueur.md`) ; attachements indiscutables = modèle
      `skrull_menace/paibok/__init__.py` (`RegleDesPouvoirs`) ; moitié attaque = mécanique NEUVE, fiche
      `mots-cles/hidden.md`, composée de `Message.WhenUnitWouldAttack` + `SetBeInstead` (modèle
      `AbilityFactoryEnemy.EnemyCannotActivate`) + `Player.DealEncounterCards` (modèle ar012 Ares).
- [x] Étape 5 : texte-contre-code : « cannot be affected by player cards » / « Attachments ... cannot be
      discarded » / « the villain would attack you ... facedown encounter card instead » vérifiés mot à
      mot contre `docs/packs/galactic-storm/transcriptions/hala-ultimatum.md` et le scan `gs138a.png`
      (relu à l'image, confirmé : traits HIDDEN. KREE., ATK en étoile non chiffrée).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : PV 15*/18*/21* (per_hero), SCH 2 (les trois stades), ATK 0 (jamais
      utilisée, étoile sur le scan). Identiques.
      Résultat : conforme.
- [x] Étape 7 : cas sujets, preuve par substitution partielle :
      - **moitié attaque** : `[hu] gs138a HIDDEN, moitie attaque` (VERT) + TEMOIN ; substitution faite à
        la main (commenté `VillainNAttaquePasTantQuilEstCache()` dans `CapacitesKreeLeader()`) : ROUGE
        (le joueur subit l'attaque normale, 0 carte distribuée) ; module remis, VERT.
      - **attachements indiscutables** : `[hu] gs138a HIDDEN, attachements indiscutables` (VERT) + TEMOIN
        (après flip, la même carte se défausse) (VERT).
      - **immunité générique (CannotBeAffectedByPlayerCards)** : PAS de cas dédié ici — la brique est déjà
        testée par `briques_communes.py` (14 cas) ; le câblage précis (`while_fn=HasTrait('HIDDEN')`) n'a
        pas de preuve automatisée propre à cette carte (`Puzzle.Stun`/`Puzzle.Tough` contournent la
        protection via `DebugRule`, impropres à la preuve). À vérifier en partie réelle.
      Résultat : 2 capacités sur 3 prouvées par substitution ; la troisième (immunité) s'appuie sur la
      brique commune déjà prouvée ailleurs, sans preuve dédiée sur CETTE carte.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé 20/10/2026 : 8 parties (`gs_hala_ultimatum`, normal+expert, 4 graines
      chacun, profil équilibré, deck spider_man). 0 incident, 0 trace d'erreur dans les 8 journaux. Le
      remplacement de l'attaque est VU dans un journal réel (voir en-tête).
      Résultat : conforme.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (face HIDDEN à l'écran, attachements
      visibles). Pas de cas plateau dédié (hors périmètre du temps disponible) : à vérifier en partie
      réelle (affichage de la face HIDDEN, du trait, de l'icône ATK en étoile).

**Carte terminée : NON** — moitié attaque et attachements indiscutables prouvés par substitution ;
immunité générique câblée mais non prouvée dédiée ; plateau non vérifié. Fonctionnellement correcte
(construction + autoplay propres), mais le gabarit n'est pas complet au sens strict de PROCESSUS-CARTE.md.

## gs138b / gs139b / gs140b : Tanalth (I/II/III), face DISCOVERED

- [x] Étape 2 : `AfterUnitAttackAndDefeatUnit` (modèle 01051 Tigra / 01118 Sonic Converter pour le type
      « Character ») + `Faces.GiveStatus`/`Faces.GiveFacedownBoostCards` (modèle
      `skrull_menace/communs_modulaires.py`) + `Faces.HasStatus`.
- [x] Étape 5 : « attacks AND DEFEATS » / « a character » / « ALREADY has » vérifiés contre le texte des
      trois stades (identique I/II, différent III : Steady + recherche + Réponse combinée).
      Résultat : conforme.
- [x] Étape 6 : PV 15*/18*/21*, ATK 2/3/4, Steady (stade III seulement). Identiques au scan.
      Résultat : conforme.
- [x] Étape 7 : `[hu] gs138b Forced Response` (tenace donné) VERT ; `[hu] gs138b ... déjà un tenace` (boost
      donné, pas de second tenace) VERT (vérifié via `hu_boost_du_vilain` : pile de boost non vide) ;
      `[hu] gs140b When Revealed` (recherche + attache Grand-High Pursuer) VERT. Pas de preuve par
      substitution formelle (retrait du module) faute de temps — à faire en suivi.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : voir gs138a (même scénario d'autoplay).
- [x] Étape 8 bis : OUI (tenace, boost, Grand-High Pursuer attaché visibles). Non vérifié au plateau.

**Carte terminée : NON** — capacités prouvées vertes, substitution non faite, plateau non vérifié.

## gs141a : Hidden Might of Hala (1A)

- [x] Étape 2 : `WhenCardSetup` (modèle gs079a/gs117a), `SetupCards.PutIntoPlay`, `ChercherEtReveleMinionKree`.
- [x] Étape 5-6 : conforme au scan (« Contents »/« Setup » cités mot à mot).
- [x] Étape 7 : `[hu] gs143 entrée en jeu` et `[hu] gs143 Scour the Planet` (stade suivant) exigent Hala
      EN JEU après la mise en place : preuve indirecte mais désormais VERTE sur les deux (20/10/2026, après
      reconstruction du cache `.game` — cette capacité ne s'exécutait PAS du tout auparavant, voir en-tête).
- [x] Étape 8 : autoplay (voir gs138a). Étape 8 bis : NON (texte seul, pas d'affichage particulier au-delà
      de « Kree Leader »/Hala déjà couverts).

**Carte terminée : OUI** pour la mise en place (Hala + recherche KREE, preuve indirecte mais verte sur deux
cas distincts) ; pas de cas isolé dédié à la seule recherche « each player searches ».

## gs141b : Hidden Might of Hala (1B)

- [x] Étape 2 : `WhenUnitBeDefeated(ForcedInterrupt, Minion, ...)` + `RetirerRepli` ;
      `AbilityFactory.AfterCardRemovedCounter(..., is_last_counter=True)` sur un `CardFinder(name=Hala)` +
      `MainScheme.Advance("2A", effect)` (modèle `challenges/2412_wrath_of_the_mad_titan.py`).
- [x] Étape 5-6 : conforme au texte scanné (menace 9*/2*/1*).
- [x] Étape 7 : `[hu] gs141b Forced Interrupt` VERT (sbire vaincu → 1 jeton retiré) et `[hu] gs141b Forced
      Response` VERT (dernier jeton retiré → avance). Les deux étaient rouges par une cause réelle, pas une
      limite outillage (voir en-tête) : `Puzzle.PlaceCounters` AJOUTE des compteurs (jamais une pose à une
      valeur absolue) — `Puzzle.Counter(..., -3)` les RETIRE, modèle `Faces.RemoveCountersOn`. L'attendu du
      second cas visait aussi `gs142a` alors que la face « 2A » n'a pas de seuil de menace imprimé et
      s'auto-avance IMMÉDIATEMENT vers `gs142b` (même mécanique que 1A → 1B) : corrigé vers `gs142b`,
      confirmé par le journal (le flip du méchant et la mise de côté de Hala, propres à l'ability de
      gs142a, sont bien résolus avant l'auto-avance).
- [x] Étape 7 bis : « dernier jeton » prouvé directement par le second cas ci-dessus (pas de cas pour le
      seuil « once per round », non applicable ici — c'est gs143 qui porte cette limite).
- [x] Étape 8 : autoplay propre (0 incident) ; le mécanisme de repli est maintenant prouvé par le harnais
      lui-même (pas seulement par absence d'erreur en autoplay).

**Carte terminée : OUI** pour les deux capacités imprimées (retrait de jeton + avancée au dernier jeton),
preuve directe par substitution de valeur (3 vs 4 jetons avant le coup final).

## gs142a : Reckoning Begins (2A)

- [x] Étape 2 : `WhenThisRevealed` + `villain.card.Flip(effect)` (modèle `gob/risky_business/02006a.py`,
      `sk189a` Veranke) + `Faces.SetAside` + `Players.ForEachPlayer`/`DrawUp`.
- [x] Étape 5-6 : conforme au texte scanné.
- [x] Étape 7 : `[hu] gs142a When Revealed` VERT (villain flip, Hala mis de côté, attachement ET dégâts du
      stade HIDDEN conservés sur la même carte — preuve directe de la règle « all attachments, status
      cards, boost cards, damage and other elements remain »). Substitution faite à la main (retrait de
      l'appel `card.Flip`) : ROUGE (gs138a reste en jeu, gs138b absent) ; remis : VERT.
- [x] Étape 7 bis : NON applicable.
- [x] Étape 8 : conforme (autoplay).
- [x] Étape 8 bis : OUI — changement de face visible, attachement visible après flip. Pas de cas plateau
      dédié (`ui-app`) : à vérifier en partie réelle, mais le mécanisme moteur est prouvé par `test_capacites`.

**Carte terminée : OUI** pour la capacité imprimée (flip + préservation d'état + pioche), sous réserve du
plateau (affichage) non vérifié à l'écran.

## gs142b : Reckoning Begins (2B)

- [x] Aucune capacité active (texte de perte de partie natif, desc). `GetAbilities()` vide, construction
      vérifiée (`test_cards`). **Carte terminée : OUI.**

## gs143 : Hala

- [x] Étape 2 : calcul direct `2 + 2*Worlds.GetPlayerNumIcon` + `Faces.PlaceCountersOn` (pas de fabrique
      prête pour « N + M[per_hero] ») ; Action utilisable par tout joueur = modèle
      `next_evol/next_evolution_campaign/40190b.py`.
- [x] Étape 5-6 : conforme au scan.
- [x] Étape 7 : `[hu] gs143 entrée en jeu` VERT (2 + 2[per_hero] = 4 jetons pour 1 joueur, vérifié
      directement). `[hu] gs143 Scour the Planet` VERT (recherche + révélation d'un sbire KREE, puis
      pioche) — l'« assertion secondaire de taille de main » était une hypothèse de départ erronée
      (6 cartes piochées à la vraie mise en place de ce scénario, pas 5 : la main attendue après l'Action
      est 7, pas 6), corrigée.
- [x] Étape 7 bis : « Limit once per round per player » : `LimitOncePerRoundPerPlayer()`, pas de témoin
      d'épuisement testé (hors périmètre du temps disponible, pas bloqué techniquement).
- [x] Étape 8 : autoplay propre (Hala apparaît en jeu dans les journaux, aucun incident).

**Carte terminée : OUI** pour les deux capacités imprimées (entrée en jeu avec jetons + Action Scour the
Planet), preuve directe sur les deux. Seul le témoin d'épuisement de la limite « once per round » n'a pas
de cas dédié (non bloquant, juste hors périmètre).

## gs144 : Grand-High Pursuer

- [x] Étape 2 : `AttachToFaceWhenPutIntoPlay(Villain)` + `GiveKeywordToAttached(Villain, retaliate=1)`
      (modèle 01153/gs127) ; `PlayerActionToDiscardThis(HeroAction)` + `Cost("YBR")` (modèle 01118, icônes
      vérifiées par découpe contre gs002/gs003/gs004 — voir rapport) ; Boost via `message.activating_enemy`
      + `Faces.HasStatus`/`GiveFacedownBoostCards` (modèle gs083 pour le déclencheur).
- [x] Étape 5-6 : conforme (icônes de ressource RE-VÉRIFIÉES par découpe contre gs002/gs003/gs004, voir
      rapport final — lecture initiale confirmée).
- [x] Étape 7 : `[hu] gs138a HIDDEN, attachements indiscutables` prouve l'attache + le blocage de
      défausse (VERT). `[hu] gs144 Hero Action` (défausse par Hero Action) VERT (20/10/2026) : la cause
      réelle n'était PAS le paiement du coût composite, mais la protection HIDDEN elle-même — « Attachments
      attached to the villain cannot be discarded » bloque AUSSI la défausse volontaire par Hero Action
      tant que le méchant est HIDDEN (confirmé par le journal : « WhenCardWouldDiscard est remplacé par
      Kree Leader »). Le cas flip désormais le méchant vers DISCOVERED avant de tester le Hero Action ;
      `Cost("YBR")` se paie normalement une fois la protection levée.
- [x] Étape 8 : autoplay propre.

**Carte terminée : OUI** — attache/retaliate/protection HIDDEN ET Hero Action de défausse tous prouvés
directement.

## gs145 : Kree Plasma Rifle

- [x] Étape 2 : mêmes briques que gs144 (attache + `UnitAttackGainKeyword` piercing/ranged, modèle
      officiel 27147 Arm Cannon / gs083).
- [x] Étape 5-6 : conforme.
- [ ] Étape 7 : pas de cas dédié (temps insuffisant) ; construction vérifiée (`test_cards`), autoplay propre.
- **Carte terminée : NON** (construction + autoplay seulement).

## gs146 : Kree Resilience

- [x] Étape 2 : `RetenirTenaceSupplementaire(1)` (helper neuf, `hala_ultimatum/__init__.py`, même message
      que `AbilityFactory.ThisCanHaveAdditionalTough`, modèle `tmnt_aspect_protection/up016.py`, mais
      reciblé sur l'HÔTE attaché) ; `PlayerActionToDiscardThis` + `Cost("RR")` ; Boost via
      `Faces.GiveStatus`.
- [x] Étape 5-6 : conforme.
- [x] Étape 7 : `[hu] gs146 Kree Resilience` VERT (2 tenaces tiennent avec la carte) + TEMOIN VERT (sans
      la carte, le second tenace excédentaire est automatiquement défaussé par le plafond de base).
      Preuve par substitution directe (présence/absence de la carte), 4 sondes manuelles confirment le
      mécanisme pas-à-pas (journal de la session).
- [x] Étape 7 bis : NON applicable (pas de « limit »).
- [x] Étape 8 : autoplay propre ; Kree Resilience VUE utilisée comme carte de boost dans un journal réel.

**Carte terminée : OUI** pour le plafond de tenace supplémentaire (preuve solide). La Hero Action de
défausse n'a pas de cas dédié (même limite potentielle que gs144, non reproduite faute de temps).

## gs147 : Kree Assassin

- [x] Étape 2 : Retaliate natif.
- [x] Étape 7 : `[hu] gs147 Kree Assassin` VERT (20/10/2026) — la cause réelle n'était PAS le ciblage :
      la recherche de mise en place de gs141a (« each player searches the encounter deck for a KREE
      minion ») engage DÉJÀ un Kree Soldier (gs149) avec le héros avant que ce cas ne s'exécute (cette
      ability ne s'exécutait pas du tout avant le correctif du cache, voir en-tête — d'où l'absence de ce
      symptôme dans les rapports précédents). `Puzzle.Remove('gs149')` ajouté avant l'attaque : Retaliate
      prouvé directement.
- **Carte terminée : OUI** pour Retaliate (preuve directe) ; le Boost n'a pas de cas dédié (hors périmètre).

## gs148 : Kree Pursuer

- [x] Étape 2 : `WhenUnitBeDefeated(WhenDefeated, "This", ...)` + `LeVilain`/`Faces.HasStatus` +
      `Faces.ShuffleAllTo`.
- [x] Étape 7 : `[hu] gs148 Kree Pursuer When Defeated` VERT (mechant avec tenace -> remélangé dans le
      deck rencontre). Pas de substitution formelle faite.
- **Carte terminée : NON** (une capacité verte, substitution non faite).

## gs149 : Kree Soldier

- [x] Guard natif. Pas de cas dédié pour le Boost (« put into play engaged with you »). Construction +
      autoplay propres.
- **Carte terminée : NON**.

## gs150 : House of Fiyero *(nom corrigé — voir questions du lot : le scan porte « HOUSE OF FIYERO », la
   transcription GS-0 et l'INVENTAIRE.md avaient lu « Fiero »)*

- [x] Étape 2 : `WhenSchemeBeDefeated(WhenDefeated, "This", ..., has_defeating_player=True)` +
      `RetirerRepli` + `player.MayChooseOneAbility` + `ForChoiceAbility(...).SetTarget(Attachment,
      with_texts=["Hero Action"], bind_to=CardFinder(card_type=Enemy))`.
- [x] Étape 7 : `[hu] gs150 When Defeated` VERT (20/10/2026). DEUX bugs réels corrigés, aucun lié à une
      limite outillage : (1) `Ability.SetTarget(..., check_face_fn=...)` — paramètre inexistant sur
      `SetTarget` (il vit sur `CardFinder`), plantage réel (`TypeError`) ; corrigé en
      `bind_to=CardFinder(card_type=Enemy)`, modèle `invisible_woman/iw010.py`. (2) Le cas de test forçait
      `hideout=0` via `Puzzle.PlaceCounters(..., 0)`, qui AJOUTE des compteurs (jamais une pose absolue) —
      sans effet sur les 4 jetons déjà posés par la mise en place réelle ; et `Puzzle.SetThreat('gs150',
      0)` vainquait la manigance DIRECTEMENT en mise en place, sans joueur vainqueur
      (`has_defeating_player=True` ne voyait personne). Corrigé : `Puzzle.Counter(..., -99)` retire
      vraiment les jetons, et la menace est mise à 1 (le THW de base du héros) pour que ce soit le
      `Puzzle.Thwart` du déclencheur qui achève la manigance, avec un vainqueur réel.
- **Carte terminée : OUI** — preuve directe complète.

## gs151 : Mobilizing the Empire

- [x] Même structure que gs150, branche alternative plus simple (« draw 1 card »), SANS `.SetTarget`
      (donc pas touchée par le bug `check_face_fn` de gs150/gs152). Pas de cas dédié, construction +
      autoplay propres.
- **Carte terminée : NON** (construction + autoplay seulement ; pas de bug connu, juste pas de preuve
  dédiée).

## gs152 : Secrets of Detention Core *(nom de transcription retenu, lu directement sur le scan — voir
   questions du lot pour la variante « Cells » lue dans une fiche antérieure)*

- [x] Même structure, branche « ready a character they control » (`"YouControlUnit"`-style via
      `finder=CardFinder(check_face_fn=...)`).
- [x] Étape 7 : pas de cas dédié, mais le MÊME bug que gs150 était présent ici (`Ability.SetTarget(...,
      check_face_fn=...)`, plantage réel à l'exécution — jamais détecté car jamais exercé par un cas,
      seulement par `test_cards`/`verifier_appels_modules`, qui ne vont pas jusqu'à l'exécution de
      l'ability). Corrigé en `finder=CardFinder(check_face_fn=...)`, confirmé par `test_cards` (6970/6970)
      et `verifier_appels_modules` après correctif — mais SANS cas dédié qui l'EXÉCUTE, ce bug serait
      resté invisible une seconde fois. À surveiller : ajouter un cas dédié reste recommandé.
- **Carte terminée : NON** — bug de script réel corrigé, mais toujours sans preuve d'exécution dédiée.

## gs153 : Advanced Arsenal

- [x] Étape 2 : `DonnerTenaceAuVillainOuSinon` (helper partagé gs153/gs154/gs155) + branche « discard
      cards from the encounter deck until... » via `Worlds.DiscardEncounterCardsUntil` +
      `CardFinder(check_face_fn=...)` pour le « OR » (attachement OU sbire, aucun `card_type` simple ne
      couvre deux types).
- [x] Étape 7 : `[hu] gs153 When Revealed` (pas de tenace -> en reçoit un) VERT. `[hu] gs153 ... DEJA un
      tenace` VERT (20/10/2026). DEUX bugs réels corrigés : (1) `Worlds.DiscardEncounterCardsUntil(...,
      finder=CardFinder(...))` — cette fonction n'a PAS de paramètre `finder` (seulement `**kwargs`
      relayés directement au `CardFinder` final) ; plantage réel (`TypeError`), corrigé en
      `check_face_fn=...` en kwarg direct. (2) Le cas de test supposait la carte neutre (01186) au-dessus
      du sbire (gs149) dans le deck créé, alors que `Puzzle.CreateEncounterDeck` empile la DERNIÈRE carte
      citée AU-DESSUS (confirmé au journal : avec `('01186', 'gs149')`, c'est gs149 qui était défaussé en
      PREMIER) ; ordre inversé + deux cartes de bourrage sous les deux (le deck s'épuisait et se
      remélangeait avec la défausse EN COURS de résolution, effaçant 01186 de la défausse avant la
      vérification).
- **Carte terminée : OUI** — preuve directe sur les deux branches.

## gs154 : Battle Cry

- [x] Étape 2 : même helper + `Faces.GiveFacedownBoostCards` + Boost via `HasBoostIcon.GainBoostIcons(2,
      effect)` (`game/card/face/attribute/has_boost_icon.py`, API publique, AUCUN exemple existant dans le
      dépôt — première utilisation).
- [ ] Étape 7 : pas de cas fiable écrit (le cas initial utilisait une sonde de mise au point, retiré de la
      batterie finale). Construction + autoplay propres, mais le Boost « +2 icônes » n'est PAS prouvé.
- **Carte terminée : NON** — à vérifier en priorité en partie réelle (compter les icônes de boost
  effectivement ajoutées).

## gs155 : Bloodthirst of Hala

- [x] Étape 2 : même helper + `face.DoActivate(joueur, effect)` (modèle officiel 11051 Ancient Grudge).
- [x] Étape 7 : `[hu] gs155 When Revealed` VERT (le mechant a déjà un tenace -> s'active contre le joueur,
      vérifié via `cartes_distribuees` puisque le mechant est HIDDEN : l'activation se transforme bien en
      distribution de carte face cachée — preuve croisée avec la moitié attaque de HIDDEN).
- **Carte terminée : OUI** pour la branche « déjà un tenace » (preuve directe et croisée avec HIDDEN) ;
  la branche « pas encore de tenace » n'a pas de cas séparé (triviale, même helper que gs153 déjà verte).
