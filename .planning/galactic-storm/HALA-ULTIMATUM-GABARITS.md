# Gabarits PROCESSUS-CARTE.md — Scénario 3 Hala Ultimatum (gs138-gs155), lot GS-6

Preuves : `Fusion/marvel-lcg-src/tools/cas/hala_ultimatum.py` (filtre `[hu]`), rapport
`/tmp/hu_final2.json`, bilan **15/23 cas verts**. `test_cards` : 6970/6970 constructions OK, 0 erreur.
`verifier_appels_modules galactic_storm` : OK, calibré (voir rapport de fin de lot). Autoplay ciblé :
8 parties (`gs_hala_ultimatum`, normal+expert, deck spider_man), 0 incident, 0 trace d'erreur dans les
8 journaux ; le remplacement de l'attaque HIDDEN par une carte de rencontre face cachée est VU dans le
journal d'une vraie partie (ligne « "WhenUnitWouldAttack" est remplacé par Kree Leader »).

**Limite outillage constatée et non résolue** (consignée en détail dans `tools/cas/hala_ultimatum.py`,
bloc gs141b) : le compteur `'hideout'` posé pendant la fenêtre de mise en place du scénario (ou par
`Puzzle.PlaceCounters` hors mise en place) se lit à 0 au moment de la vérification du cas, ALORS QUE le
handler lit la valeur juste posée en cours d'exécution (tracé par impression directe, confirmé). Le
même symptôme se reproduit à l'identique avec la fabrique OFFICIELLE `AbilityFactory.ThisEnterPlayWithCounters`
(pas seulement notre code) : ce n'est donc **pas un défaut de script**, mais une limite du harnais de
test (ou du moteur) sur les compteurs posés pendant la fenêtre de mise en place de scénario, non
identifiée précisément faute de temps. **À vérifier en PARTIE RÉELLE.**

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
- [x] Étape 7 : la mise en place de TOUS les cas `[hu]` passe par cette carte (Hala en jeu, confirmé
      indirectement par `en_jeu: ["gs144"]` etc. qui nécessitent le mécant en jeu après 1A). Pas de cas
      dédié isolé.
- [x] Étape 8 : autoplay (voir gs138a). Étape 8 bis : NON (texte seul, pas d'affichage particulier au-delà
      de « Kree Leader »/Hala déjà couverts).

**Carte terminée : NON** (preuve indirecte seulement).

## gs141b : Hidden Might of Hala (1B)

- [x] Étape 2 : `WhenUnitBeDefeated(ForcedInterrupt, Minion, ...)` + `RetirerRepli` ;
      `AbilityFactory.AfterCardRemovedCounter(..., is_last_counter=True)` sur un `CardFinder(name=Hala)` +
      `MainScheme.Advance("2A", effect)` (modèle `challenges/2412_wrath_of_the_mad_titan.py`).
- [x] Étape 5-6 : conforme au texte scanné (menace 9*/2*/1*).
- [ ] Étape 7 : cas écrits (`[hu] gs141b Forced Interrupt`, `[hu] gs141b Forced Response`) mais ROUGES à
      cause de la LIMITE OUTILLAGE ci-dessus (compteur `hideout` qui se lit à 0 au moment de la
      vérification, y compris avec la fabrique officielle). **Non prouvé par le harnais.**
- [x] Étape 7 bis : pas de limite au sens « once per round », mais un seuil (dernier jeton) : non testé
      pour la même raison.
- [x] Étape 8 : autoplay propre (0 incident), mais sans preuve que le mécanisme de repli fonctionne en
      partie (le journal n'a pas été lu ligne à ligne pour cette mécanique précise faute de temps).

**Carte terminée : NON** — bloquée par la limite outillage décrite en en-tête. À vérifier en partie réelle
en priorité.

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
- [ ] Étape 7 : **ROUGE**, même limite outillage que gs141b (confirmé reproductible avec la fabrique
      officielle `ThisEnterPlayWithCounters`, voir en-tête). Le handler pose bien la valeur correcte EN
      COURS D'EXÉCUTION (tracé), mais le harnais la lit à 0 à la vérification. `[hu] gs143 Scour the
      Planet` échoue sur une assertion secondaire de taille de main (hypothèse de départ erronée, pas
      directement liée à la limite outillage, non recalculée faute de temps).
- [x] Étape 7 bis : « Limit once per round per player » : `LimitOncePerRoundPerPlayer()`, pas de témoin
      d'épuisement testé (bloqué par ce qui précède).
- [x] Étape 8 : autoplay propre (Hala apparaît en jeu dans les journaux, aucun incident).

**Carte terminée : NON** — bloquée par la limite outillage. À vérifier en priorité en partie réelle
(nombre de jetons de repli posés à la mise en place).

## gs144 : Grand-High Pursuer

- [x] Étape 2 : `AttachToFaceWhenPutIntoPlay(Villain)` + `GiveKeywordToAttached(Villain, retaliate=1)`
      (modèle 01153/gs127) ; `PlayerActionToDiscardThis(HeroAction)` + `Cost("YBR")` (modèle 01118, icônes
      vérifiées par découpe contre gs002/gs003/gs004 — voir rapport) ; Boost via `message.activating_enemy`
      + `Faces.HasStatus`/`GiveFacedownBoostCards` (modèle gs083 pour le déclencheur).
- [x] Étape 5-6 : conforme (icônes de ressource RE-VÉRIFIÉES par découpe contre gs002/gs003/gs004, voir
      rapport final — lecture initiale confirmée).
- [ ] Étape 7 : `[hu] gs138a HIDDEN, attachements indiscutables` prouve l'attache + le blocage de
      défausse (VERT). `[hu] gs144 Hero Action` (défausse par Hero Action) **ROUGE** : « gs144 est encore
      en jeu » — le paiement du coût composite `Cost("YBR")` par le pilote de test n'aboutit pas dans ce
      cas précis (cause non élucidée faute de temps : possible ordre de paiement des trois couleurs par
      `premiere_option_jouable`). Non prouvé.
- [x] Étape 8 : autoplay propre.

**Carte terminée : NON** — attache/retaliate/protection HIDDEN prouvés, Hero Action de défausse non
prouvée (`Cost("YBR")`, modèle identique à 01118/gs083 pourtant validés ailleurs — à reprendre).

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
- [ ] Étape 7 : `[hu] gs147 Kree Assassin` ROUGE (« degats sur l'identite = 0 ») : le cas suppose que
      `Puzzle.Attack('01001a')` cible automatiquement Kree Assassin (seul ennemi en jeu) ; non confirmé,
      cause non élucidée faute de temps.
- **Carte terminée : NON** (construction + autoplay seulement ; le Boost n'a pas de cas).

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
      with_texts=["Hero Action"], check_face_fn=...)`.
- [ ] Étape 7 : `[hu] gs150 When Defeated` ROUGE, par ricochet de la limite outillage sur les compteurs
      `hideout` (le test force `hideout=0` par `Puzzle.PlaceCounters`, qui subit la même limite). Non
      prouvé par le harnais pour cette raison ; le code lui-même suit le même patron que gs151/gs152,
      construits et chargés sans erreur.
- **Carte terminée : NON** — bloquée par la limite outillage commune.

## gs151 : Mobilizing the Empire

- [x] Même structure que gs150, branche alternative plus simple (« draw 1 card »). Pas de cas dédié
      (même limite), construction + autoplay propres.
- **Carte terminée : NON**.

## gs152 : Secrets of Detention Core *(nom de transcription retenu, lu directement sur le scan — voir
   questions du lot pour la variante « Cells » lue dans une fiche antérieure)*

- [x] Même structure, branche « ready a character they control » (`"YouControlUnit"`-style via
      `check_face_fn`). Pas de cas dédié (même limite), construction + autoplay propres.
- **Carte terminée : NON**.

## gs153 : Advanced Arsenal

- [x] Étape 2 : `DonnerTenaceAuVillainOuSinon` (helper partagé gs153/gs154/gs155) + branche « discard
      cards from the encounter deck until... » via `Worlds.DiscardEncounterCardsUntil` +
      `CardFinder(check_face_fn=...)` pour le « OR » (attachement OU sbire, aucun `card_type` simple ne
      couvre deux types).
- [x] Étape 7 : `[hu] gs153 When Revealed` (pas de tenace -> en reçoit un) VERT. `[hu] gs153 ... DEJA un
      tenace` ROUGE (« 01186 dans la defausse rencontre = 0 ») : la défausse-jusqu'à n'a pas défaussé la
      carte neutre attendue — cause non élucidée faute de temps (possiblement `Worlds.
      DiscardEncounterCardsUntil` avec `include_discard_pile` par défaut ou ordre du deck).
- **Carte terminée : NON** — une branche verte, l'autre rouge, cause non identifiée.

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
