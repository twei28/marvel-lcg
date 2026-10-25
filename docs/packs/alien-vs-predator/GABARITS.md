# Alien vs. Predator (RyCoRan) : gabarits PROCESSUS-CARTE, 55 card_id

Scénario `alien_vs_predator` (standard : méchants A) et `alien_vs_predator_expert` (méchants B), préfixe `ap`, set 216. Source : zip « Alien vs Predator
(06-26) » (60 images : 8 faces de méchants, 8 faces de complots, 25 cartes de rencontre dont 3 doublons, 4 images × 4 Alien Scout, Apex Standard 7,
Clan Yautja 6, encart). Sets : `alien_vs_predator`, `xenomorph_deck`, `apex_standard` (remplace le Standard), `clan_yautja` (modulaire).
Cas : `Fusion/marvel-lcg-src/tools/cas/alien_vs_predator.py`, `_b`, `_c`, `_d` (filtre `[ap]`). Plateau : `ui-app/src/board/alien-vs-predator-plateau.test.ts`.
Transcriptions : `docs/packs/alien-vs-predator/TRANSCRIPTIONS.md`. Recettes : `docs/reference/RECETTES-MOTEUR.md` §25. Fiche : `mots-cles/mechants-multiples.md`.

## Arbitrages utilisateur du 25/10/2026 (questions posées carte montrée, scan à l'appui)

1. **The Ultimate Hunt 1B, compteur actif** : seul le méchant ACTIF s'active à chaque activation, puis le compteur passe à l'autre.
2. **Second méchant vaincu** (stade 3/4) : les joueurs GAGNENT ; sa face « Defeated » ne se joue pas.
3. **Cloaking Device** : « Hero Action: After a hero makes a basic attack... » = Réponse de héros, juste après l'attaque de base contre l'ennemi équipé.
4. **Alien Onslaught × Alien Scout** : un Scout atteint par la défausse compte pour un pion Accélération ET est distribué face cachée.
5. **1B, méchant sonné** (sa carte d'état remplace l'activation) : le compteur actif passe quand même.
6. **2B, méchant sonné au moment d'attaquer** : le compteur passe, PAS de carte boost.
7. **Expanding Hive × « When Defeated »** d'un sbire à 3 PV ou plus : la Hive le donne d'abord en boost ; son « When Defeated » se résout ensuite sans reprendre la carte.

## Décisions prises seules (texte sans ambiguïté, règle ou insert), à signaler

- **« The villain » des cartes joueur** : rien d'imprimé ; règle des scénarios à compteur (Sinister Six) : le méchant actif, pour toutes les cartes.
- **Deck Xenomorph « next to Alien Queen »** : les 16 Alien Scout sont glissés SOUS la Reine, face cachée (le plateau montre la pile) ; « a Xenomorph card » = une au hasard.
- **Les deux méchants vaincus ensemble** (2 dégâts de 1B sur deux méchants à 2 PV, manigances vides) : victoire (insert « Ultimate Hunt 1B »).
- **2B « Then, remove 2[per_hero] threat »** fait partie du « if » (sinon la menace ne monterait jamais au seuil, le stade n'ayant pas de seuil).
- **Warlord « When Predator Warlord attacks »** : toute attaque (alliés visés compris) ; le joueur attaqué choisit l'option.
- **Doublons du zip** (identiques au pixel près hors numéro) : Thermal Target 13-14, Facehugger 16-17, Xenomorph Drone 18-19.
- **Masterplan** et **Shadow of the Past** : textes identiques au core : `ability_link` 01192 / 01190.
- **Coquille du scan** : Thermal Target « discard thiis card » (sans flèche) : lu comme la flèche des autres cartes.

## Gates du scénario

- [x] Cartes (`cards.json`, 55 card_id, set 216), scripts (`src/cards/pack/alien_vs_predator/`, 53 modules, 4 sets + `commun.py`), scénarios standard et
      expert, ensembles `alien_vs_predator`, `standard_apex`, `clan_yautja`, images, textes FR (`textes-fr-fanmade.ts` et `public/js/...`), traits
      `XENOMORPH`, `YAUTJA`, `DEFEATED`, compteur `plasma`.
- [x] Moteur (additif) : `AfterStatusDiscardFrom.by_effect` (le message gardait l'effet sans l'exposer) ; compteur `plasma`.
- [x] `test_cards.py` 7455 OK / 0 erreur ; `verifier_prefixes.py` OK ; `verifier_appels_modules.py alien_vs_predator` OK ; `audit_cartes.py` : 4 marqueurs
      (ap001a/ap003a « Response » : fabrique `AfterUnitAttackAndDamageUnit` ; ap022 « Interrupt » : perçant en bonus d'attaque + fin d'attaque ;
      ap306 « Action » : Réponse de héros par l'arbitrage 3), tous prouvés par cas et substitution.
- [x] Cas : **122 cas `[ap]` verts**, passe tracée par `MCLCG_TRACE_CRASH` : 5 exceptions avalées, toutes la même assertion de `Reveal` dans l'ANCIEN surge
      du harnais (`fix_surge` sans `v18_surge` ; une vraie partie distribue face cachée), aussi présente sur un cas The Vault d'avant ce pack.
- [x] Substitution : voir chaque carte ; les verts restants sont expliqués carte par carte.
- [x] Plateau : `alien-vs-predator-plateau.test.ts` 6/6, calibré ROUGE sur un compteur faux.
- [x] Autoplay : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; profils prudent / équilibré / agressif) :
      0 erreur dans les 45 journaux ; journaux lus : compteur actif Reine → Warlord → Reine, Incitation 3 du Drone avec la Reine active, passage au stade 2.
- [x] `verifier_tous_les_decks.py` : **157/157 decks montent une partie** (fichiers partagés touchés : `sender_unit.py`, `card_face.py`).
- [ ] **Voile français des cartes PAYSAGE** (complots, manigances annexes) : texte juste et dans son cadre, mais ~30 % plus petit que l'imprimé ; défaut
      du composant commun `TraductionPosee.tsx` (la « largeur portrait » d'une carte couchée vaut 0,71 × sa hauteur au lieu de sa hauteur), en cours
      de modification par une autre session : NON corrigé ici, signalé.
- [ ] **Partie réelle jouée par un humain : NON FAITE.**

---


### ap001a : Alien Queen (Villain)

```
* Alien Queen (A, standard) — MECHANT. XENOMORPH. SCH 2, ATK 1, PV 18[per_hero].
[star] When Alien Queen schemes, place that threat on her side scheme instead of the main scheme, if able.
[star] Forced Response: After Alien Queen attacks and damages a character you control, shuffle a Xenomorph card into your deck.
When Defeated: Flip this card.

Cartes de reference :
 - redirection de la menace : `PlaceThreatOnCardWhenThisScheme` (Wrecking Crew 07002, bw020) ; « her side scheme » = Expanding Hive
   (« Alien Queen's Scheme ») ;
 - « attacks and damages a character you control » : `AfterUnitAttackAndDamageUnit(.., "This", "YouControlCharacter")` (27161 Kraven) ;
   « shuffle a Xenomorph card » : une carte au hasard du deck Xenomorph glisse sous elle (helper `MelangerUnXenomorph`) ;
 - « When Defeated: Flip this card » : `card.Flip` (le retournement revele la face Defeated, modele tk Bebop & Rocksteady).

⚠ Mots-pieges :
 - « if able » : Expanding Hive retiree du jeu -> la menace va au complot principal ;
 - « a character YOU control » : le joueur attaque (identite ou allie) recoit la carte, pas le premier joueur ;
 - deck Xenomorph vide : rien n'est melange (insert) ;
 - « Flip » : seulement si Predator Warlord est encore en jeu ; derniere mechante vaincue -> les joueurs gagnent (arbitrage 2).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (5 cas sujets) :
      - ap001a la Reine manigance : sa menace (2) va sur Expanding Hive, pas sur le complot ; le compteur passe au Warlord (1B)
      - ap001a « if able » : Expanding Hive absente -> la menace de la Reine va sur le complot principal
      - ap001a la Reine attaque et blesse le heros : un Alien Scout passe de sous la Reine au deck du joueur
      - ap001a contre-cas : la Reine attaque mais ne blesse pas (le heros defend) -> aucun Alien Scout melange
      - ap001a second mechant vaincu (Reine seule restante) -> les joueurs GAGNENT, sans face Defeated (arbitrage 2 du 25/10/2026)
      Preuve par substitution : **rouges 3/6** sans le module ; verts restants : « if able » (sans Hive, la menace va au complot avec ou sans module), contre-cas « defend : rien », victoire au dernier mechant (defaite NATIVE du moteur, arbitrage 2). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : deux vilains dessines ; le deck Xenomorph glisse dessous. Cas plateau : ui-app/src/board/alien-vs-predator-plateau.test.ts (6 cas verts, calibre ROUGE sur un compteur faux ; aucun correctif de plateau necessaire). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap001b : Alien Queen (Villain)

```
* Alien Queen « Defeated » (A, standard) — face B du mechant. DEFEATED. XENOMORPH.
When Revealed: Heal 4[per_hero] damage from Predator Warlord and give him a tough status card. Advance to stage 3A. Remove each
permanent side scheme and this card from the game.

Cartes de reference :
 - « Heal X damage from <mechant> and give a tough status card » : `HealthUnits` + `Faces.GiveStatus(.., "Tough")` (27150, wd028) ;
 - « Advance to stage 3A » : `World.AdvanceMainScheme(complot, face_du_stade, effect)` (saut direct, le moteur le permet par face) ;
 - « Remove ... from the game » : `Faces.RemoveAllFromGame` (Permanent ne bloque que les effets d'un AUTRE set, permanent.md).

⚠ Mots-pieges :
 - « 4[per_hero] » : 4 x nombre de joueurs ;
 - « EACH permanent side scheme » : les DEUX (Expanding Hive ET Skulls for the Taking), pas seulement celle du mechant vaincu ;
 - « and THIS card » : la face Defeated quitte la partie (le mechant vaincu ne reste pas en jeu) ;
 - Predator Warlord devient le mechant actif (3B / 4B : « Predator Warlord is the active villain »), pose ici des le retournement.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ap001b face Defeated de la Reine (ap001a vaincue, Warlord en jeu) : Warlord soigne de 4, Tenace, stade 3A puis 3B, manigances permanentes et la Reine retirees
      - ap001b la Reine vaincue AU STADE 2 : saut au stade 3 (Predator's Pursuit 3B)
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap002a : Predator Warlord (Villain)

```
* Predator Warlord (A, standard) — MECHANT. YAUTJA. SCH 1, ATK 2, PV 16[per_hero].
[star] When Predator Warlord schemes, place that threat on his side scheme instead of the main scheme, if able.
[star] Forced Interrupt: When Predator Warlord attacks, either place 2 threat on the main scheme or he gets +1 ATK for this attack.
When Defeated: Flip this card.

Cartes de reference :
 - redirection : `PlaceThreatOnCardWhenThisScheme` (07002) ; « his side scheme » = Skulls for the Taking ;
 - « either ... or ... » a l'attaque : `WhenUnitWouldAttack(ForcedInterrupt)` + `ChooseAbilities` + `GainATKForThisAttack` (21092) ;
 - « When Defeated: Flip this card » : `card.Flip` (modele tk).

⚠ Mots-pieges :
 - « When Predator Warlord ATTACKS » (pas « attacks you ») : vaut aussi contre un allie (Predator's Prey, Trophy Taken) ;
 - « place 2 threat on the MAIN scheme » : directement sur le complot, pas sur Skulls (ce n'est pas une manigance du mechant) ;
 - le joueur attaque choisit (a defaut le premier joueur) ; « for this attack » seulement.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - ap002a le Warlord manigance : sa menace (1) va sur Skulls for the Taking ; le compteur revient a la Reine
      - ap002a le Warlord attaque : le joueur choisit +1 ATK (option 2) -> 3 degats au heros
      - ap002a le Warlord attaque : option 1 -> 2 menaces sur le complot principal, attaque a 2
      Preuve par substitution : **rouges 4/4** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : deux vilains dessines. Cas plateau : ui-app/src/board/alien-vs-predator-plateau.test.ts (6 cas verts, calibre ROUGE sur un compteur faux ; aucun correctif de plateau necessaire). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap002b : Predator Warlord (Villain)

```
* Predator Warlord « Defeated » (A, standard) — face B du mechant. DEFEATED. YAUTJA.
When Revealed: Heal 4[per_hero] damage from Alien Queen and give her a tough status card. Advance to stage 4A. Remove each
permanent side scheme and this card from the game.

Cartes de reference :
 - « Heal X damage from <mechant> and give a tough status card » : `HealthUnits` + `Faces.GiveStatus(.., "Tough")` (27150, wd028) ;
 - « Advance to stage 4A » : `World.AdvanceMainScheme(complot, face_du_stade, effect)` (saut direct, le moteur le permet par face) ;
 - « Remove ... from the game » : `Faces.RemoveAllFromGame` (Permanent ne bloque que les effets d'un AUTRE set, permanent.md).

⚠ Mots-pieges :
 - « 4[per_hero] » : 4 x nombre de joueurs ;
 - « EACH permanent side scheme » : les DEUX (Expanding Hive ET Skulls for the Taking), pas seulement celle du mechant vaincu ;
 - « and THIS card » : la face Defeated quitte la partie (le mechant vaincu ne reste pas en jeu) ;
 - Alien Queen devient le mechant actif (3B / 4B : « Alien Queen is the active villain »), pose ici des le retournement.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ap002b face Defeated du Warlord (ap002a vaincu, Reine en jeu) : Reine soignee de 4, Tenace, stade 4B
      Preuve par substitution : **rouges 1/1** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap003a : Alien Queen (Villain)

```
* Alien Queen (B, expert) — MECHANT. XENOMORPH. SCH 2, ATK 2, PV 18[per_hero]. Meme texte que ap001a.
[star] When Alien Queen schemes, place that threat on her side scheme instead of the main scheme, if able.
[star] Forced Response: After Alien Queen attacks and damages a character you control, shuffle a Xenomorph card into your deck.
When Defeated: Flip this card.

Cartes de reference :
 - redirection de la menace : `PlaceThreatOnCardWhenThisScheme` (Wrecking Crew 07002, bw020) ; « her side scheme » = Expanding Hive
   (« Alien Queen's Scheme ») ;
 - « attacks and damages a character you control » : `AfterUnitAttackAndDamageUnit(.., "This", "YouControlCharacter")` (27161 Kraven) ;
   « shuffle a Xenomorph card » : une carte au hasard du deck Xenomorph glisse sous elle (helper `MelangerUnXenomorph`) ;
 - « When Defeated: Flip this card » : `card.Flip` (le retournement revele la face Defeated, modele tk Bebop & Rocksteady).

⚠ Mots-pieges :
 - « if able » : Expanding Hive retiree du jeu -> la menace va au complot principal ;
 - « a character YOU control » : le joueur attaque (identite ou allie) recoit la carte, pas le premier joueur ;
 - deck Xenomorph vide : rien n'est melange (insert) ;
 - « Flip » : seulement si Predator Warlord est encore en jeu ; derniere mechante vaincue -> les joueurs gagnent (arbitrage 2).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ap003a (expert) la Reine B manigance : sa menace (2) va sur Expanding Hive
      - ap003a (expert) la Reine B attaque et blesse le heros : un Alien Scout melange dans le deck du joueur
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : deux vilains dessines ; le deck Xenomorph glisse dessous. Cas plateau : ui-app/src/board/alien-vs-predator-plateau.test.ts (6 cas verts, calibre ROUGE sur un compteur faux ; aucun correctif de plateau necessaire). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap003b : Alien Queen (Villain)

```
* Alien Queen « Defeated » (B, expert) — face B du mechant. DEFEATED. XENOMORPH.
When Revealed: Heal 6[per_hero] damage from Predator Warlord and give him a tough status card. Advance to stage 3A. Remove each
permanent side scheme and this card from the game.

Cartes de reference :
 - « Heal X damage from <mechant> and give a tough status card » : `HealthUnits` + `Faces.GiveStatus(.., "Tough")` (27150, wd028) ;
 - « Advance to stage 3A » : `World.AdvanceMainScheme(complot, face_du_stade, effect)` (saut direct, le moteur le permet par face) ;
 - « Remove ... from the game » : `Faces.RemoveAllFromGame` (Permanent ne bloque que les effets d'un AUTRE set, permanent.md).

⚠ Mots-pieges :
 - « 6[per_hero] » : 6 x nombre de joueurs ;
 - « EACH permanent side scheme » : les DEUX (Expanding Hive ET Skulls for the Taking), pas seulement celle du mechant vaincu ;
 - « and THIS card » : la face Defeated quitte la partie (le mechant vaincu ne reste pas en jeu) ;
 - Predator Warlord devient le mechant actif (3B / 4B : « Predator Warlord is the active villain »), pose ici des le retournement.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ap003b (expert) la Reine B vaincue : le Warlord B est soigne de 6
      Preuve par substitution : **rouges 1/1** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap004a : Predator Warlord (Villain)

```
* Predator Warlord (B, expert) — MECHANT. YAUTJA. SCH 1, ATK 3, PV 16[per_hero]. Meme texte que ap002a.
[star] When Predator Warlord schemes, place that threat on his side scheme instead of the main scheme, if able.
[star] Forced Interrupt: When Predator Warlord attacks, either place 2 threat on the main scheme or he gets +1 ATK for this attack.
When Defeated: Flip this card.

Cartes de reference :
 - redirection : `PlaceThreatOnCardWhenThisScheme` (07002) ; « his side scheme » = Skulls for the Taking ;
 - « either ... or ... » a l'attaque : `WhenUnitWouldAttack(ForcedInterrupt)` + `ChooseAbilities` + `GainATKForThisAttack` (21092) ;
 - « When Defeated: Flip this card » : `card.Flip` (modele tk).

⚠ Mots-pieges :
 - « When Predator Warlord ATTACKS » (pas « attacks you ») : vaut aussi contre un allie (Predator's Prey, Trophy Taken) ;
 - « place 2 threat on the MAIN scheme » : directement sur le complot, pas sur Skulls (ce n'est pas une manigance du mechant) ;
 - le joueur attaque choisit (a defaut le premier joueur) ; « for this attack » seulement.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ap004a (expert) le Warlord B manigance : sa menace (1) va sur Skulls for the Taking
      - ap004a (expert) le Warlord B attaque, option +1 ATK : 4 degats (ATK 3 + 1)
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : deux vilains dessines. Cas plateau : ui-app/src/board/alien-vs-predator-plateau.test.ts (6 cas verts, calibre ROUGE sur un compteur faux ; aucun correctif de plateau necessaire). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap004b : Predator Warlord (Villain)

```
* Predator Warlord « Defeated » (B, expert) — face B du mechant. DEFEATED. YAUTJA.
When Revealed: Heal 6[per_hero] damage from Alien Queen and give her a tough status card. Advance to stage 4A. Remove each
permanent side scheme and this card from the game.

Cartes de reference :
 - « Heal X damage from <mechant> and give a tough status card » : `HealthUnits` + `Faces.GiveStatus(.., "Tough")` (27150, wd028) ;
 - « Advance to stage 4A » : `World.AdvanceMainScheme(complot, face_du_stade, effect)` (saut direct, le moteur le permet par face) ;
 - « Remove ... from the game » : `Faces.RemoveAllFromGame` (Permanent ne bloque que les effets d'un AUTRE set, permanent.md).

⚠ Mots-pieges :
 - « 6[per_hero] » : 6 x nombre de joueurs ;
 - « EACH permanent side scheme » : les DEUX (Expanding Hive ET Skulls for the Taking), pas seulement celle du mechant vaincu ;
 - « and THIS card » : la face Defeated quitte la partie (le mechant vaincu ne reste pas en jeu) ;
 - Alien Queen devient le mechant actif (3B / 4B : « Alien Queen is the active villain »), pose ici des le retournement.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ap004b (expert) le Warlord B vaincu : la Reine B est soignee de 6
      Preuve par substitution : **rouges 1/1** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap005a : The Ultimate Hunt (MainScheme)

```
The Ultimate Hunt (1A) — COMPLOT PRINCIPAL, stade 1.
Contents: Alien Queen (A) and Predator Warlord (A) (B instead in expert mode). Alien vs. Predator, Xenomorph deck, Apex Standard and one
  modular encounter set (Clan Yautja).
Setup: Put Skulls for the Taking and Expanding Hive into play. Place the Xenomorph deck next to Alien Queen and place the active counter
  on her.

Cartes de reference :
 - « Contents » : data/scenarios/alien_vs_predator(_expert).json (aucun code) ; les deux mechants sont mis de cote (`villain: []`) et
   mis en jeu ICI, comme Bebop & Rocksteady (tk005a) et Sinister Six (27100a) ;
 - « the active counter » : `Villains.SetRule(.., the_villain="Active")` (brique 16.3, fiche mechants-multiples.md) puis
   `Villains.SetActive` ; seul le mechant actif s'active (arbitrage 1 du 25/10/2026 : `GettingVillain` rend le mechant actif) ;
 - « Put ... into play » : `SetupCards.PutIntoPlay(name=, card_type=)` (gs161a, vt017a) ;
 - « Place the Xenomorph deck next to Alien Queen » : les 16 Alien Scout (mis de cote) sont GLISSES SOUS la Reine, face cachee
   (`TuckCardUnderHere`, fiche tuck.md) : le plateau montre la pile et son nombre.

⚠ Mots-pieges :
 - « place the active counter on HER » : la Reine commence ;
 - « Player cards that refer to "the villain" » : rien d'imprime -> regle par defaut des scenarios a compteur (Sinister Six) : le
   mechant actif, pour les cartes de rencontre comme pour les cartes joueur.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ap005a Setup (standard) : Reine et Warlord en jeu, Skulls et Expanding Hive en jeu, 16 Alien Scout sous la Reine, compteur actif sur la Reine
      - ap005a Setup (expert) : les faces B (ap003a, ap004a) sont en jeu, compteur actif sur la Reine
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : 16 Alien Scout glisses SOUS Alien Queen, face cachee. Cas plateau : ui-app/src/board/alien-vs-predator-plateau.test.ts (6 cas verts, calibre ROUGE sur un compteur faux ; aucun correctif de plateau necessaire). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap005b : The Ultimate Hunt (MainScheme)

```
The Ultimate Hunt (1B) — COMPLOT PRINCIPAL, stade 1. Seuil 8[per_hero], escalade +1[per_hero] (★), depart 0.
[star] Forced Response: After resolving step one of the villain phase, if there is no threat on each villain's side scheme, deal 2 damage
  to each villain.
Forced Response: After a villain activates, move the active counter to the next villain.
Insert « Ultimate Hunt 1B » : si Alien Queen ET Predator Warlord ont chacun 2 PV et qu'aucune de leurs manigances permanentes ne porte
  de menace, ils tombent a 0 PV ensemble et les joueurs GAGNENT.

Cartes de reference :
 - « After resolving step one of the villain phase » : `AfterResolveVillainPhaseStep(ForcedResponse, 1, op)` (07001b Breakout) ;
 - « deal 2 damage to each villain » : `DealDamage(mechants, 2)` en UNE fois (simultane) ;
 - « After a villain activates » : `AfterEnemyActivationEnd(ForcedResponse, Villain, op)` (activation = attaque OU manigance, y compris
   celles des traitrises : « The villain schemes ») ; « move the active counter » : `PasserLeCompteur` (Villains.SetActive) ;
 - mechant SONNE / DESORIENTE dont la carte d'etat remplace l'activation : `AfterStatusDiscardFrom` (la carte d'etat se defausse
   elle-meme) -> le compteur passe aussi (arbitrage du 25/10/2026 : « l'alternance ne se casse jamais »).

⚠ Mots-pieges :
 - « no threat on EACH villain's side scheme » : les deux manigances a 0 (une manigance absente ne porte pas de menace) ;
 - « EACH villain » : les deux, en meme temps : la Reine vaincue par ces degats ne fait pas soigner le Warlord AVANT qu'il prenne les
   siens ; si les deux tombent ensemble, l'insert tranche : victoire (pas de face Defeated jouee) ;
 - « do not move the active villain counter » (Advance Again, Assault, Alien Assault) : la garde est consommee par `PasserLeCompteur`.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (5 cas sujets) :
      - ap005b la Reine SONNEE au moment d'attaquer : pas d'attaque, mais le compteur passe au Warlord (arbitrage du 25/10/2026)
      - ap005b etape 1 : aucune menace sur les DEUX manigances des mechants -> 2 degats a chaque mechant
      - ap005b etape 1 contre-cas : une menace reste sur Skulls -> aucun degat aux mechants
      - ap005b insert : les deux mechants a 2 PV, manigances vides -> ils tombent ensemble et les joueurs GAGNENT
      - ap005b 1B accompli (8[per_hero] menaces) : passage au stade 2 (Battleground Earth), la partie continue
      Preuve par substitution : **rouges 3/4** sans le module ; verts restants : contre-cas « une menace sur Skulls : aucun degat ». Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap006a : Battleground Earth (MainScheme)

```
Battleground Earth (2A) — COMPLOT PRINCIPAL, stade 2.
When Revealed: Each player searches the encounter deck and discard pile for a [[YAUTJA]] minion and a [[XENOMORPH]] minion and puts them
  into play engaged with them. Shuffle the encounter deck.

Cartes de reference :
 - « search the encounter deck and discard pile for X » : `Search.EncounterCard(.., include_discard_pile=True, trait=, card_type=Minion)`
   (07001a / tk) ; « puts them into play engaged with them » : `PutIntoPlay(joueur)` + `EngagePlayer` (pd008) ;
 - « Shuffle the encounter deck » : `Worlds.GetEncounterDeck(effect).Shuffle(effect)` (07001a).

⚠ Mots-pieges :
 - « EACH player » : un sbire YAUTJA ET un sbire XENOMORPH par joueur ; rien trouve -> rien (pas de defausse) ;
 - « puts into play » (pas « reveals ») : aucun « When Revealed » des sbires (Blooded Predator, Predator Elite) ne part.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ap006a 2A : chaque joueur met en jeu, engages avec lui, un sbire YAUTJA et un sbire XENOMORPH du deck de rencontre
      Preuve par substitution : **rouges 1/1** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap006b : Battleground Earth (MainScheme)

```
Battleground Earth (2B) — COMPLOT PRINCIPAL, stade 2. Seuil « — » (aucun : ce stade ne s'accomplit pas), escalade +1[per_hero],
  depart 2[per_hero].
Forced Response: After a villain attacks, give it a facedown boost card, then move the active counter to the next villain.
Forced Response: After threat is placed here, if there is at least 4[per_hero] threat here, deal each player a facedown encounter card.
  Then, remove 2[per_hero] threat from this scheme.

Cartes de reference :
 - « After a villain attacks » : `AfterEnemyActivationEnd(ForcedResponse, Villain)` filtre sur une fin d'ATTAQUE (`message.atk_message`) ;
   « give it a facedown boost card » : `GiveFacedownBoostCardsInternal(1, ..)` (la carte attend sa prochaine activation, 60075) ;
 - mechant SONNE dont la carte remplace l'attaque : le compteur passe, PAS de carte boost (arbitrage du 25/10/2026) ;
 - « After threat is placed here » : `AfterSchemePlaceThreat(ForcedResponse, "This")` (pd026) ; « deal each player a facedown
   encounter card » : `DealEncounterCards(1)` ; « remove X threat » : `RemoveThreatFromSchemes`.

⚠ Mots-pieges :
 - au stade 2 le compteur ne bouge qu'apres une ATTAQUE (une manigance contre un alter-ego le laisse en place) ;
 - « Then, remove 2[per_hero] » fait partie du « if » (sinon la menace ne monterait jamais) ;
 - « at least 4[per_hero] » : 4 x joueurs ou plus, compte sur la carte entiere.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (5 cas sujets) :
      - ap006b le mechant actif ATTAQUE : il recoit une carte boost face cachee et le compteur passe
      - ap006b le mechant actif MANIGANCE : ni carte boost, ni deplacement du compteur (au stade 2, seule l'attaque compte)
      - ap006b la Reine SONNEE au moment d'attaquer : le compteur passe, pas de carte boost (arbitrage du 25/10/2026)
      - ap006b 4[per_hero] menaces atteintes : chaque joueur recoit une carte de rencontre face cachee, puis 2[per_hero] menaces retirees
      - ap006b contre-cas : 3 menaces seulement -> aucune carte distribuee, la menace reste
      Preuve par substitution : **rouges 3/5** sans le module ; verts restants : contre-cas « manigance : rien ne bouge » et « 3 menaces seulement ». Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap007a : Predator's Pursuit (MainScheme)

```
Predator's Pursuit (3A) — COMPLOT PRINCIPAL, stade 3 (atteint quand Alien Queen est vaincue).
When Revealed: Discard cards from the top of the encounter deck until a [[WEAPON]] attachment is discarded. Reveal it.

Cartes de reference : 01192 Masterplan (`Worlds.DiscardEncounterCardsUntil(.., trait=, card_type=Attachment)` puis `Reveal`).

⚠ Mots-pieges : un ATTACHEMENT WEAPON (pas un sbire) ; aucun dans le deck -> rien n'est revele.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ap007a 3A : la fouille revele le premier attachement WEAPON (Plasmacaster, attache au Warlord) ; ap007b : un sbire YAUTJA revele
      Preuve par substitution : **rouges 1/1** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap007b : Predator's Pursuit (MainScheme)

```
Predator's Pursuit (3B) — COMPLOT PRINCIPAL, stade 3. Seuil 8[per_hero], escalade +1[per_hero], depart 1[per_hero], Hazard.
Predator Warlord is the active villain.
When Revealed: Each player searches the encounter deck and discard pile for a [[YAUTJA]] minion and reveals it.
If this stage is completed, the players lose the game.

Cartes de reference :
 - « is the active villain » : `Villains.SetActive` a la revelation (seul mechant restant de toute facon) ;
 - « searches ... and reveals it » : `Search.EncounterCard(.., include_discard_pile=True)` + `Reveal` (le « When Revealed » du sbire part) ;
 - « the players lose » : `WhenMainSchemeStageWouldBeCompleted` + `Worlds.SetGameOver(False)` (27102b) ; sans lui le moteur
   passerait au complot suivant encore dans le deck ;
 - Hazard : `desc.Hazard`, natif (fiche hazard.md).

⚠ Mots-pieges : « EACH player » : un sbire par joueur ; « reveals » (pas « puts into play ») : son « When Revealed » part.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ap007b 3B accompli (8[per_hero] menaces) : les joueurs PERDENT (pas de passage au complot suivant)
      Preuve par substitution : **rouges 1/2** sans le module ; verts restants : « 3B accompli -> defaite » : sans module le moteur termine deja la partie par sa regle de dernier stade (constate au journal le 25/10/2026) ; le module garantit la defaite imprimee quel que soit l'etat du deck des complots. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap008a : Queen's Dominion (MainScheme)

```
Queen's Dominion (4A) — COMPLOT PRINCIPAL, stade 4 (atteint quand Predator Warlord est vaincu).
When Revealed: Discard cards from the top of the encounter deck until a [[XENOMORPH]] attachment is discarded. Reveal it.

Cartes de reference : 01192 Masterplan (`Worlds.DiscardEncounterCardsUntil(.., trait=, card_type=Attachment)` puis `Reveal`).

⚠ Mots-pieges : un ATTACHEMENT XENOMORPH (pas un sbire) ; aucun dans le deck -> rien n'est revele.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ap008a 4A : la fouille revele le premier attachement XENOMORPH (Piercing Pharynx, attache a la Reine) ; ap008b : un sbire XENOMORPH revele
      Preuve par substitution : **rouges 1/1** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap008b : Queen's Dominion (MainScheme)

```
Queen's Dominion (4B) — COMPLOT PRINCIPAL, stade 4. Seuil 8[per_hero], escalade +1[per_hero], depart 1[per_hero], Hazard.
Alien Queen is the active villain.
When Revealed: Each player searches the encounter deck and discard pile for a [[XENOMORPH]] minion and reveals it.
If this stage is completed, the players lose the game.

Cartes de reference :
 - « is the active villain » : `Villains.SetActive` a la revelation (seul mechant restant de toute facon) ;
 - « searches ... and reveals it » : `Search.EncounterCard(.., include_discard_pile=True)` + `Reveal` (le « When Revealed » du sbire part) ;
 - « the players lose » : `WhenMainSchemeStageWouldBeCompleted` + `Worlds.SetGameOver(False)` (27102b) ; sans lui le moteur
   passerait au complot suivant encore dans le deck ;
 - Hazard : `desc.Hazard`, natif (fiche hazard.md).

⚠ Mots-pieges : « EACH player » : un sbire par joueur ; « reveals » (pas « puts into play ») : son « When Revealed » part.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ap008b 4B accompli : les joueurs PERDENT
      Preuve par substitution : **rouges 1/2** sans le module ; verts restants : meme raison que ap007b. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap009 : Expanding Hive (SideScheme)

```
Expanding Hive — MANIGANCE ANNEXE. Alien Queen's Scheme. Depart 2[per_hero]. Permanent. Acceleration.
While there is no threat here, this scheme loses the [acceleration] icon.
Forced Interrupt: When a minion with 3 or more printed hit points is defeated, give it to the active villain as a facedown boost card.

Cartes de reference :
 - « Alien Queen's Scheme » : la Reine y manigance (ap001a, `PlaceThreatOnCardWhenThisScheme`) ; aucun code ici ;
 - « loses the [acceleration] icon » : `ThisGainKeyword(.., acceleration_icon=-1, change_on_event=OnEvent.Threat("This"))` (pd026) ;
 - « When a minion ... is defeated » : `WhenUnitBeDefeated(ForcedInterrupt, Minion)` ; « give it to the active villain as a facedown
   boost card » : `GiveBoostCard` (60075) au mechant actif ;
 - Permanent : natif (`desc.Permanent`).

⚠ Mots-pieges :
 - « 3 or more PRINTED hit points » : `printed_health` (un bonus de PV ne compte pas) ; Alien Scout (2) n'y va jamais ;
 - n'importe quel sbire (YAUTJA, XENOMORPH, nemesis...) ;
 - le « When Defeated » du sbire se resout ENSUITE sans reprendre la carte (arbitrage du 25/10/2026 : Drone, Young Blood,
   Blooded Predator restent en boost).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - ap009 sans menace, Expanding Hive perd son icone Acceleration (2 -> 1 en jeu)
      - ap009 ligne de base : les deux manigances permanentes portent leur icone Acceleration (2 en jeu)
      - ap009 un sbire a 3 PV imprimes (Xenomorph Drone) vaincu : donne au mechant actif comme carte boost face cachee
      - ap009 contre-cas : un sbire a 2 PV (Alien Scout) vaincu n'est PAS donne en boost
      Preuve par substitution : **rouges 2/4** sans le module ; verts restants : contre-cas « ligne de base : 2 icones » et « Alien Scout (2 PV) : pas de boost ». Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : manigance annexe permanente et sa menace. Cas plateau : ui-app/src/board/alien-vs-predator-plateau.test.ts (6 cas verts, calibre ROUGE sur un compteur faux ; aucun correctif de plateau necessaire). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap010 : Skulls for the Taking (SideScheme)

```
Skulls for the Taking — MANIGANCE ANNEXE. Predator Warlord's Scheme. Depart 2[per_hero]. Permanent. Acceleration.
While there is no threat here, this scheme loses the [acceleration] icon.
Forced Response: After an ally is defeated by an enemy attack, tuck it under here.
Insert : Trophy Taken a priorite (l'allie qu'il vainc est retire de la partie) ; quand cette manigance quitte le jeu, les allies glisses
  dessous vont a la defausse de leur proprietaire.

Cartes de reference :
 - « loses the [acceleration] icon » : `ThisGainKeyword(acceleration_icon=-1)` (pd026) ;
 - « After an ally is defeated by an enemy attack » : `AfterUnitDefeatedUnit(ForcedResponse, Enemy, Ally, is_from_attack=True)` ;
   « tuck it under here » : `TuckCardUnderHere` (fiche tuck.md) ;
 - « leaves play » (insert : allies glisses -> defausse de leur proprietaire) : NATIF, les cartes glissees sous une carte qui quitte le
   jeu partent a la defausse de leur proprietaire (mesure du 25/10/2026 : le cas « Skulls quitte le jeu » reste vert sans aucun code ;
   une capacite `WhenCardWouldLeavePlay` ecrite d'abord a ete retiree, elle faisait double emploi).

⚠ Mots-pieges :
 - « by an ENEMY attack » : pas une traitrise ni un degat indirect ; l'allie doit etre arrive a la defausse (Trophy Taken l'a retire
   du jeu avant : il n'est plus la, rien a glisser) ;
 - les allies glisses ne reviennent qu'a la sortie de la manigance.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - ap010 un allie vaincu par l'attaque d'un ennemi est glisse sous Skulls for the Taking
      - ap010 contre-cas : un allie vaincu par des degats hors attaque n'est pas glisse
      - ap010 Skulls quitte le jeu (la Reine vaincue retire les manigances permanentes) : l'allie glisse dessous va a la defausse de son proprietaire
      Preuve par substitution : **rouges 1/3** sans le module ; verts restants : contre-cas « degats hors attaque » et « allies liberes quand Skulls quitte le jeu » (NATIF : mesure du 25/10/2026, voir le script). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : manigance annexe permanente, allie glisse dessous. Cas plateau : ui-app/src/board/alien-vs-predator-plateau.test.ts (6 cas verts, calibre ROUGE sur un compteur faux ; aucun correctif de plateau necessaire). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap011 : Plasmacaster (Attachment)

```
Plasmacaster — ATTACHEMENT. WEAPON. Boost 2. Uses (3 plasma counters).
Attach to Predator Warlord. Otherwise, this card gains surge.
Uses (3 plasma counters).
[star] Forced Interrupt: When Predator Warlord attacks you, remove 1 plasma counter from here and discard the top card of your deck →
  take indirect damage equal to that card's printed cost.

Cartes de reference :
 - « Attach to X. Otherwise, surge » : `AttachToFaceWhenPutIntoPlay(CardFinder(name=), if_cannot_gain_surge=True)` (tk Accessoire) ;
 - Uses : `desc.Uses "3,plasma"`, natif (fiche uses.md : la carte part seule au dernier compteur) ; compteur `plasma` ajoute a
   `CardFace.COUNTER` et a `compteurs-fr.ts` ;
 - « When X attacks you » : `WhenUnitAttackYou(ForcedInterrupt, ..)` ; « discard the top card of your deck » : `DiscardDeckTopCards(1)` ;
   « printed cost » : `FacesCounter.GetPrintedCost` (27170) ; « indirect damage » : `DealIndirectDamage(identite, n)` (16026).

⚠ Mots-pieges :
 - « attacks YOU » : pas une attaque contre un allie ni contre un ennemi ;
 - le compteur retire est un COUT (fleche) : le 3e usage fait partir la carte (natif) apres avoir inflige ses degats ;
 - « that card's PRINTED cost » : une carte sans cout (ressource, Alien Scout distribue au lieu d'etre defausse) = 0 degat.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - ap011 Plasmacaster s'attache au Warlord avec 3 compteurs plasma
      - ap011 sans Predator Warlord, Plasmacaster gagne surge (une carte distribuee)
      - ap011 le Warlord attaque : 1 compteur plasma retire, carte du dessus du deck defaussee (Black Cat, cout 2) -> 2 degats indirects
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : attachement du Warlord et ses compteurs « plasma ». Cas plateau : ui-app/src/board/alien-vs-predator-plateau.test.ts (6 cas verts, calibre ROUGE sur un compteur faux ; aucun correctif de plateau necessaire). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap012 : Yautja Wrist Blades (Attachment)

```
* Yautja Wrist Blades — ATTACHEMENT unique. WEAPON. ATK +2. Boost 2.
Attach to Predator Warlord. If you cannot, attach to a [[YAUTJA]] minion. Otherwise, this card gains surge.
[star] Attached enemy's attacks gain piercing.
Hero Action: Spend [energy][physical] resources → discard this card.

Cartes de reference :
 - « Attach to Predator Warlord. If you cannot, attach to a [[YAUTJA]] minion. Otherwise, this card gains surge. » :
   `AttachToFaceWhenPutIntoPlay(CardFinder(name=WARLORD), if_cannot_attach_to=Select.From(sbire YAUTJA), if_cannot_gain_surge=True)` ;
 - ATK +2 : `desc.ATK+`, natif (01100) ; « attacks gain piercing » : `UnitAttackGainKeyword("AttachedEnemy", piercing=True)` (27059) ;
 - « Hero Action: Spend ... → discard this card » : `PlayerActionToDiscardThis(HeroAction).SetCost(Cost("YR"))` (01119 Klaw).

⚠ Mots-pieges :
 - [energy] = Y, [physical] = R (verifie contre les icones des cartes Y/R du core) ;
 - « attached ENEMY » : le Warlord OU le sbire YAUTJA qui la porte ; unique (✦) : nom « * », natif.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - ap012 Wrist Blades sur le Warlord : +2 ATK et attaque perforante (la Tenace du heros est ignoree) -> 4 degats
      - ap012 sans Predator Warlord, Wrist Blades s'attache a un sbire YAUTJA
      - ap012 Hero Action : depenser [energy][physical] -> Wrist Blades defaussee
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap013 : Thermal Target (Attachment)

```
Thermal Target — ATTACHEMENT. CONDITION. YAUTJA. Boost ★ (+1). Deux exemplaires (13, 14).
Attach to your identity.
Forced Response: After your turn ends, take 2 damage and place 2 threat on the main scheme.
Alter-Ego Action: Find a [[YAUTJA]] minion and reveal it → discard this card.
[star] Boost: Reveal this card.

Cartes de reference :
 - attachement a l'identite + Reponse forcee de fin de tour + action pour s'en defaire : 21029 Sap Power (`AttachToFaceWhenPutIntoPlay
   ("YourIdentity")`, `AfterPlayerTurnEnd(ForcedResponse, "You")`, `PlayerActionToDiscardThis(AlterEgoAction)`) ;
 - « Find a minion » : `Find.Find` (regle Find, pd008), « reveal it » : `Reveal` (son « When Revealed » part) ;
 - « Boost: Reveal this card » : `WhenCardBecomeBoost("This", RevealThisCard)` (tk BoostReveleCetteCarte).

⚠ Mots-pieges :
 - « take 2 damage » (pas indirect) ET « place 2 threat on the MAIN scheme » : les deux ;
 - « Find ... → discard » : trouver est le COUT ; sans sbire YAUTJA hors jeu, l'action n'est pas proposee ;
 - « thiis » sur le scan : coquille de l'auteur, aucun effet.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - ap013 Thermal Target s'attache a l'identite ; fin du tour : 2 degats et 2 menaces sur le complot principal
      - ap013 Alter-Ego Action : trouver un sbire YAUTJA et le reveler -> Thermal Target defaussee
      - ap013 Boost : la carte est revelee (attachee a l'identite)
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : attachement de rencontre sur l'identite. Cas plateau : ui-app/src/board/alien-vs-predator-plateau.test.ts (6 cas verts, calibre ROUGE sur un compteur faux ; aucun correctif de plateau necessaire). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap015 : Piercing Pharynx (Attachment)

```
* Piercing Pharynx — ATTACHEMENT unique. CONDITION. XENOMORPH. ATK +1. Boost ★ (+1). (Fichier du zip : « Inner Teeth ».)
Attach to Alien Queen and give her a tough status card. Otherwise, this card gains surge.
Alien Queen gains retaliate 1.
Hero Action: If Predator Warlord is in play, spend [energy][mental] resources → discard this card.
[star] Boost: Reveal this card.

Cartes de reference :
 - « Attach to X and give her a tough status card » : `AttachToFaceWhenPutIntoPlay(.., when_attach_operation=)` + `GiveStatus("Tough")` ;
 - « gains retaliate 1 » : `GiveKeywordToAttached(.., retaliate=1)` (01119 Klaw) ; ATK +1 : `desc.ATK+`, natif ;
 - « Hero Action: If ..., spend → discard » : `PlayerActionToDiscardThis(HeroAction, conditions=[Warlord en jeu]).SetCost(Cost("YB"))` ;
 - Boost : `RevealThisCard` (tk).

⚠ Mots-pieges :
 - la carte Tenace n'est donnee QUE si la carte s'attache (sinon surge, rien d'autre) ;
 - « IF Predator Warlord is in play » : apres sa defaite (stade 4), la carte ne peut plus etre defaussee ainsi ;
 - [energy] = Y, [mental] = B.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - ap015 Piercing Pharynx s'attache a la Reine et lui donne une carte Tenace
      - ap015 la Reine gagne riposte 1 : le heros qui l'attaque subit 1 degat
      - ap015 Hero Action (Warlord en jeu) : depenser [energy][mental] -> Piercing Pharynx defaussee
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap016 : Facehugger (Attachment)

```
Facehugger — ATTACHEMENT. CONDITION. XENOMORPH. Boost 1. Deux exemplaires (16, 17).
Attach to your identity.
Forced Response: After your turn ends, take 2 damage and place 2 threat on the main scheme.
Alter-Ego Action: Search the encounter deck and discard pile for a [[XENOMORPH]] minion and reveal it → discard this card.

Cartes de reference : 21029 Sap Power (comme ap013) ; « search the encounter deck and discard pile ... reveal it » :
  `Search.EncounterCard(.., include_discard_pile=True)` + `Reveal` (helper `ChercherEtReveler`).

⚠ Mots-pieges :
 - recherche limitee au deck ET a la defausse de RENCONTRE (pas « Find ») : les Alien Scout des decks joueurs n'y sont pas ;
 - trouver est le cout : sans sbire XENOMORPH a cet endroit, l'action n'est pas proposee.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ap016 Facehugger : fin du tour -> 2 degats et 2 menaces sur le complot
      - ap016 Alter-Ego Action : chercher un sbire XENOMORPH dans le deck de rencontre et le reveler -> Facehugger defaussee
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap018 : Xenomorph Drone (Minion)

```
Xenomorph Drone — SBIRE. XENOMORPH. SCH 0, ATK 2, PV 3. Boost 2. Deux exemplaires (18, 19).
Guard. Incite 2 (3 instead if Alien Queen is the active villain).
When Defeated: Remove 2 threat from Expanding Hive. If you cannot, shuffle Xenomorph Drone into the encounter deck.

Cartes de reference :
 - Guard, Incite 2 : `desc`, natifs (fiches guard.md, incite.md) ; « 3 instead if ... » : `ThisGainIncite(fn, incite=1)` (50094) ;
 - « Remove X threat from <manigance> » : `RemoveThreatFromSchemes` ; « shuffle into the encounter deck » :
   `Faces.ShuffleAllTo([..], "EncounterDeck")` (pd003, modele `WhenUnitBeDefeated(WhenDefeated, "This")`).

⚠ Mots-pieges :
 - « If you CANNOT » : Expanding Hive absente (retiree au stade 3/4) ou sans menace ; une seule menace retiree compte comme « pu » ;
 - le Drone (3 PV imprimes) est d'abord donne au mechant actif par Expanding Hive : il RESTE alors en boost, le melange n'a pas lieu
   (arbitrage du 25/10/2026).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (5 cas sujets) :
      - ap018 Incite 3 quand la Reine est le mechant active
      - ap018 Incite 2 quand le Warlord est le mechant actif
      - ap018 When Defeated : 2 menaces retirees d'Expanding Hive (le Drone part en boost par la Hive)
      - ap018 When Defeated sans Expanding Hive : « if you cannot », le Drone est melange dans le deck de rencontre
      - ap018 Hive sans menace : le Drone deja donne en boost par la Hive y RESTE (arbitrage du 25/10/2026)
      Preuve par substitution : **rouges 3/5** sans le module ; verts restants : Incite 2 avec le Warlord actif (valeur imprimee, native) et « reste en boost » (porte par Expanding Hive). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap020 : Xenomorph Warrior (Minion)

```
Xenomorph Warrior — SBIRE. XENOMORPH. SCH 1, ATK 2, PV 6. Boost 1.
Quickstrike.
When Defeated: Discard the top card of the encounter deck and deal 1 damage to a [[YAUTJA]] enemy for each icon ([star] and [boost]) in
  that card's boost area.

Cartes de reference : Quickstrike natif (`desc`) ; « each icon (★ and Y) in that card's boost area » : pd008 (`IconesDeBoost`) ;
  `Worlds.DiscardEncounterTopCard` ; « deal damage to an enemy » : `DealDamage` au choix du joueur (`AskChooseFace`).

⚠ Mots-pieges : « A [[YAUTJA]] enemy » : UN seul (mechant ou sbire YAUTJA), au choix du joueur qui l'a vaincu ; aucun en jeu ou 0 icone
  -> la carte est quand meme defaussee.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ap020 When Defeated : defausse le dessus du deck (Alien Praetorian, boost 3) -> 3 degats au Warlord (YAUTJA)
      Preuve par substitution : **rouges 1/1** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap021 : Alien Praetorian (Minion)

```
* Alien Praetorian — SBIRE unique. ELITE. XENOMORPH. SCH 2, ATK 2, PV 8. Boost 3.
Villainous.
Forced Response: After the villain phase begins, Alien Praetorian engages the first player.

Cartes de reference : Villainous natif (`desc`, fiche villainous.md) ; « After the villain phase begins » : `AfterPhaseBegin(ForcedResponse,
  "Villain")` (16026) ; « engages the first player » : `EngagePlayer(premier)` (21143).

⚠ Mots-pieges : deja engage avec le premier joueur -> rien ne change ; le premier joueur du round (le jeton tourne).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ap021 Alien Praetorian : au debut de la phase du mechant, il s'engage avec le premier joueur
      Preuve par substitution : **rouges 1/1** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap022 : Chestburster (Attachment)

```
Chestburster — ATTACHEMENT. CONDITION. ATK +2. Boost 2.
Attach to a [[XENOMORPH]] minion. Otherwise attach to the active villain.
[star] Forced Interrupt: When attached enemy attacks, this attack gains piercing. At the end of this attack, stun your identity and discard
  this card.

Cartes de reference :
 - « Attach to X. Otherwise attach to Y » : `AttachToFaceWhenPutIntoPlay(.., otherwise_attach_to=)` ; ATK +2 natif ;
 - « this attack gains piercing » : `UnitAttackGainKeyword("AttachedEnemy", piercing=True)` (27059) ;
 - « At the end of this attack » : `AfterUnitAttackEnd(ForcedResponse, "AttachedEnemy")` ; « stun your identity » : `GiveStatus("Stunned")`.

⚠ Mots-pieges :
 - « YOUR identity » : le joueur attaque (celui de l'allie si un allie est vise) ;
 - « Otherwise attach to the ACTIVE villain » (pas « the villain ») ; aucune cible : la carte reste sans hote (defaussee) ;
 - une seule attaque : la carte part a la fin de la premiere.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - ap022 Chestburster s'attache a un sbire XENOMORPH
      - ap022 sans sbire XENOMORPH, Chestburster s'attache au mechant actif
      - ap022 l'ennemi porteur attaque : attaque perforante (Tenace ignoree) ; a la fin, l'identite est sonnee et Chestburster defaussee
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap023 : Hive Incursion (Treachery)

```
Hive Incursion — TRAITRISE. Boost ★.
When Revealed: Discard your hand. Draw up to your hand size.
[star] Boost: Resolve the "When Revealed" ability on this card.

Cartes de reference : 27093 Fearmonger (`DiscardAllHands` + `DrawUp(hand_size)`) ; Boost qui rejoue le « When Revealed » : 16116.

⚠ Mots-pieges : « draw UP TO your hand size » : on pioche jusqu'a la taille de main (main videe -> une main pleine) ; en boost, « your » =
  le joueur attaque / qui subit la manigance.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ap023 Hive Incursion : la main est defaussee puis le joueur pioche jusqu'a sa taille de main (6 en alter-ego)
      - ap023 Boost : le « When Revealed » est resolu (main defaussee puis repiochee)
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap024 : Predator's Prize (Treachery)

```
Predator's Prize — TRAITRISE. Boost 3.
When Revealed: Choose to either give this card to the active villain as a facedown boost card, or find your identity-specific ally and remove
  it from the game.

Cartes de reference : 60075 Bullseye (« give this card to the villain as a facedown boost card » OU autre chose, `ChooseAbilities`) ;
  « identity-specific ally » : `CardFinder(card_class="IdentitySpecific")` (45015) ; « find » : `Find.Find` (regle Find).

⚠ Mots-pieges :
 - « find » : partout (main, deck, defausse, en jeu) ; aucun allie propre a l'identite -> seule l'option boost est possible ;
 - « remove from the GAME » (pas defausse) ; « the ACTIVE villain ».
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ap024 Predator's Prize, option 1 : la carte est donnee au mechant actif comme boost face cachee
      - ap024 Predator's Prize, option 2 : l'allie propre a l'identite (Black Cat) est retire de la partie
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap025 : Brood Breakout (SideScheme)

```
Brood Breakout — MANIGANCE ANNEXE. Menace 4 (fixe). Boost 3.
Forced Response: After a [[XENOMORPH]] minion enters play, give it a tough status card.
When Revealed: Discard cards from the top of the encounter deck until a [[XENOMORPH]] minion is discarded. Reveal it.

Cartes de reference : 04108 Taskmaster's Training Camp (`AfterCardEnterPlay(ForcedResponse, Minion)` + `GiveStatus("Tough")`) ; 01192
  (`DiscardEncounterCardsUntil` + `Reveal`).

⚠ Mots-pieges : le sbire revele par le « When Revealed » entre en jeu APRES la manigance : il recoit sa carte Tenace ; un Alien Scout
  (XENOMORPH) qui entre en jeu aussi.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ap025 Brood Breakout : la fouille revele un sbire XENOMORPH, qui recoit une carte Tenace en entrant en jeu
      Preuve par substitution : **rouges 1/1** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap026 : Alien Assault (Treachery)

```
Alien Assault — TRAITRISE. Boost ★ + 1.
When Revealed: If Predator Warlord is the active villain, stun your identity. If Alien Queen is the active villain, confuse your identity.
[star] Boost: After this activation ends, do not move the active counter to the next villain.

Cartes de reference : `GiveStatus("Stunned"|"Confused")` ; « do not move the active counter » : garde consommee par le deplacement du
  compteur (helper `GarderLeCompteur`, lu par 1B / 2B).

⚠ Mots-pieges : seul le mechant ACTIF compte ; au stade 3/4 il n'y a plus de deplacement (la garde ne sert a rien, elle est oubliee).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - ap026 Alien Assault, la Reine active : l'identite est desorientee
      - ap026 Alien Assault, le Warlord actif : l'identite est sonnee
      - ap026 Boost : apres cette activation, le compteur actif ne bouge pas
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap027 : Killing Ground (Treachery)

```
Killing Ground — TRAITRISE. Boost 2.
When Revealed: Move all threat from the villain's side scheme with the most threat to the main scheme. If no threat was moved this way,
  exhaust your identity. If you cannot, stun or confuse your identity.

Cartes de reference : deplacer de la menace = la retirer puis la poser (`RemoveThreatFromSchemes` + `PlaceThreatOnSchemes`, regle des
  « move » du moteur, 07042) ; « exhaust your identity » : `Faces.ExhaustAll` ; « If you cannot » : identite deja inclinee.

⚠ Mots-pieges :
 - « the villain's side scheme with the MOST threat » : Expanding Hive ou Skulls ; egalite -> le joueur choisit ; 0 partout -> rien ;
 - « If you cannot » : l'identite est deja inclinee -> le joueur choisit Sonne OU Desoriente.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - ap027 Killing Ground : toute la menace de la manigance de mechant la plus chargee (Skulls, 3) passe sur le complot
      - ap027 aucune menace deplacee : l'identite est inclinee
      - ap027 identite deja inclinee : « if you cannot », sonnee (1re option)
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap028 : Predator's Prey (Treachery)

```
Predator's Prey — TRAITRISE. Boost 1.
When Revealed: Discard cards from the top of your deck until you discard an ally, then put that ally into play under your control. The
  active villain attacks that ally. This attack gains overkill.

Cartes de reference : 21055 Summoning Spell (`DiscardDeckUntil(card_type=Ally)` puis `PutIntoPlay`) ; « attacks that ally » :
  `AttackCharacter(allie, overkill=True)` (brique 16.1).

⚠ Mots-pieges :
 - « until you discard an ally » : un Alien Scout rencontre en route est distribue face cachee au lieu d'etre defausse (sa propre
   Interruption) ; aucun allie dans le deck -> rien ;
 - « the ACTIVE villain » ; « overkill » : l'exces va a l'identite du controleur (regle de l'allie).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ap028 Predator's Prey : defausse du deck jusqu'a un allie (Black Cat), mis en jeu, attaque par le Warlord (ATK 2+1), vaincu (glisse sous Skulls), 1 degat d'exces a l'identite
      Preuve par substitution : **rouges 1/1** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap029 : Predation (Treachery)

```
Predation — TRAITRISE. Boost ★ + 2.
When Revealed: Heal 3 damage from the active villain and give them a tough status card. Deal 3 damage to an enemy whose trait does not
  match the active villain.
[star] Boost: Place 2 threat on each scheme.

Cartes de reference : `HealthUnits` + `GiveStatus("Tough")` (wd028) ; `DealDamage` a un ennemi au choix ; « each scheme » : complot +
  toutes les manigances annexes (`Worlds.GetOnFieldSchemes`).

⚠ Mots-pieges :
 - « an enemy whose trait does not match the active villain » : un ennemi SANS le trait du mechant actif (XENOMORPH pour la Reine,
   YAUTJA pour le Warlord) : l'autre mechant, ses sbires, un sbire sans trait ; au choix du joueur ;
 - « EACH scheme » : principal ET annexes (y compris les manigances permanentes).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ap029 Predation : la Reine soignee de 3 et Tenace ; 3 degats a un ennemi sans le trait XENOMORPH (le Warlord)
      - ap029 Boost : 2 menaces sur CHAQUE manigance (complot + Hive + Skulls)
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap030 : Trophy Taken (Treachery)

```
Trophy Taken — TRAITRISE. Boost 2.
When Revealed: The active villain attacks the friendly character with the fewest remaining hit points. If this attack defeats an ally,
  remove that ally from the game.
Insert : Trophy Taken a priorite sur Skulls for the Taking (l'allie retire du jeu n'est pas glisse dessous).

Cartes de reference : `AttackCharacter(cible, if_this_defeat_unit=)` (brique 16.1) ; « fewest remaining hit points » : 07016 (egalite :
  le joueur choisit) ; identite visee : `DoAttackYou(son joueur)`.

⚠ Mots-pieges :
 - « FRIENDLY character » : identites et allies de TOUS les joueurs (les joueurs sont alliés) ;
 - « remove from the GAME » (pas la defausse) : Skulls ne trouve plus l'allie et ne glisse rien.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ap030 Trophy Taken : le mechant actif attaque le personnage ami le plus bas (Black Cat) ; vaincu, il est RETIRE de la partie (pas sous Skulls)
      Preuve par substitution : **rouges 1/1** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap031 : Lethal Ambush (Treachery)

```
Lethal Ambush — TRAITRISE. Boost 2.
When Revealed: Discard the top 7 cards of the encounter deck. Put the first minion discarded this way into play engaged with you. Then, the
  villain and each minion engaged with you attacks you.

Cartes de reference : `Worlds.DiscardEncounterCards(7)` ; mise en jeu engagee : 07001a / pd008 ; « the villain ... attacks you » :
  `DoAttackYou` (16116), chaque sbire engage aussi.

⚠ Mots-pieges :
 - « the FIRST minion discarded » : le premier dans l'ordre de defausse (un seul) ;
 - « the villain » = le mechant actif (regle du scenario) ; « EACH minion engaged with you » : y compris le nouveau.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ap031 Lethal Ambush : le 1er sbire des 7 cartes defaussees entre en jeu engage ; puis le mechant ET ce sbire attaquent (1 + 2 = 3 degats)
      Preuve par substitution : **rouges 1/1** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap032 : Swarm Breaker (SideScheme)

```
Swarm Breaker — MANIGANCE ANNEXE. Menace 4 (fixe). Boost 2. Acceleration, Hazard.
Hinder 1[per_hero]. Victory 0.
When Defeated: Deal 2[per_hero] damage to each enemy.

Cartes de reference : Hinder, Victory, Acceleration, Hazard : `desc`, natifs (fiches) ; « When Defeated » d'une manigance :
  `WhenSchemeBeDefeated(WhenDefeated, "This")` (tk Bumbling Buffoons) ; « each enemy » : `Worlds.GetOnFieldEnemies`.

⚠ Mots-pieges : « EACH enemy » : les mechants ET tous les sbires ; 2[per_hero] = 2 x joueurs.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ap032 Swarm Breaker vaincue : 2[per_hero] degats a chaque ennemi
      Preuve par substitution : **rouges 1/1** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap033 : Alien Onslaught (SideScheme)

```
Alien Onslaught — MANIGANCE ANNEXE. Menace 4 (fixe). Boost 2.
Hinder 2[per_hero].
When Revealed: Each player discards the top 2[per_hero] of their deck. Place 1 acceleration token here for each [[XENOMORPH]] minion
  discarded this way.
Forced Response: After you thwart this scheme, discard the top 2[per_hero] cards of your deck.

Cartes de reference : `DiscardDeckTopCards(n)` ; jeton d'acceleration sur une manigance : `PlaceAccelerationToken` ; « After you thwart
  this scheme » : `AfterUnitThwartScheme(ForcedResponse, Unit2, "This")` (le contreur est une carte du joueur : « you »).

⚠ Mots-pieges :
 - un Alien Scout atteint par la defausse COMPTE pour un jeton ET est distribue face cachee (arbitrage 4 du 25/10/2026) : la Scout le
   signale sur l'effet (`_ap_scouts_interceptes`) ;
 - « EACH player » : chacun son deck ; 2[per_hero] = 2 x joueurs ;
 - « After YOU thwart » : contrecarrer (THW, pas un retrait de menace par une carte de rencontre).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ap033 Alien Onslaught : chaque joueur defausse 2[per_hero] cartes ; l'Alien Scout atteint est distribue ET compte 1 jeton d'acceleration
      - ap033 apres que le joueur contrecarre cette manigance : il defausse les 2[per_hero] cartes du dessus de son deck
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap101 : Alien Scout (Minion)

```
Alien Scout (01-04, 4 exemplaires) — SBIRE. XENOMORPH. SCH 1, ATK 1, PV 2. Deck Xenomorph (dos rouge).
Surge.
Forced Interrupt: When you would draw or discard this card from your deck, draw 1 card. Deal this card to yourself as a facedown encounter card.
When Defeated: Place Alien Scout in your discard pile.

Cartes de reference :
 - Surge : `desc.Surge`, natif (fiche surge.md).
 - Interruption depuis le deck du joueur : 27087b Maze of Mirrors (pioche ET defausse du deck, `SetBeInstead`, `DealEncounterCard`) ;
   carte de rencontre vivant dans un deck joueur : fiche weakness.md ;
 - « Place in your discard pile » : deplacement apres la defaite (`AfterUnitBeDefeated`) vers la defausse du joueur engage.

⚠ Mots-pieges :
 - « draw OR DISCARD this card FROM YOUR DECK » : une defausse depuis la MAIN n'est pas concernee ;
 - « your discard pile » : celle du JOUEUR (pas la defausse de rencontre) ; elle revient donc dans son deck au remelange ;
 - donnee comme boost par Expanding Hive ? Non : 2 PV imprimes (< 3).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - ap101 Alien Scout (01-04, Surge) pioche : distribue face cachee au joueur, qui pioche 1 carte a la place
      - ap101 Alien Scout DEFAUSSE du deck du joueur : distribue face cachee (pas dans la defausse) et le joueur pioche 1 carte
      - ap101 Alien Scout vaincu : il va dans la defausse du JOUEUR (pas la defausse de rencontre)
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap102 : Alien Scout (Minion)

```
Alien Scout (05-08, 4 exemplaires) — SBIRE. XENOMORPH. SCH 1, ATK 1, PV 2. Deck Xenomorph (dos rouge).
Guard.
Forced Interrupt: When you would draw or discard this card from your deck, deal this card to yourself as a facedown encounter card.
When Defeated: Place Alien Scout in your discard pile.

Cartes de reference :
 - Guard : `desc.Guard`, natif (fiche guard.md). Cette version ne fait PAS piocher.
 - Interruption depuis le deck du joueur : 27087b Maze of Mirrors (pioche ET defausse du deck, `SetBeInstead`, `DealEncounterCard`) ;
   carte de rencontre vivant dans un deck joueur : fiche weakness.md ;
 - « Place in your discard pile » : deplacement apres la defaite (`AfterUnitBeDefeated`) vers la defausse du joueur engage.

⚠ Mots-pieges :
 - « draw OR DISCARD this card FROM YOUR DECK » : une defausse depuis la MAIN n'est pas concernee ;
 - « your discard pile » : celle du JOUEUR (pas la defausse de rencontre) ; elle revient donc dans son deck au remelange ;
 - donnee comme boost par Expanding Hive ? Non : 2 PV imprimes (< 3).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ap102 Alien Scout (05-08, Guard) pioche : distribue face cachee au joueur, SANS pioche de remplacement
      - ap102 contre-cas : un Alien Scout defausse depuis la MAIN n'est pas intercepte
      Preuve par substitution : **rouges 1/2** sans le module ; verts restants : contre-cas « defausse depuis la MAIN : rien ». Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap103 : Alien Scout (Minion)

```
Alien Scout (09-12, 4 exemplaires) — SBIRE. XENOMORPH. SCH 1, ATK 1, PV 2. Deck Xenomorph (dos rouge).
Incite 1. Surge.
Forced Interrupt: When you would draw or discard this card from your deck, draw 1 card. Deal this card to yourself as a facedown encounter card.
When Defeated: Place Alien Scout in your discard pile.

Cartes de reference :
 - Incite 1, Surge : `desc`, natifs (fiches incite.md, surge.md).
 - Interruption depuis le deck du joueur : 27087b Maze of Mirrors (pioche ET defausse du deck, `SetBeInstead`, `DealEncounterCard`) ;
   carte de rencontre vivant dans un deck joueur : fiche weakness.md ;
 - « Place in your discard pile » : deplacement apres la defaite (`AfterUnitBeDefeated`) vers la defausse du joueur engage.

⚠ Mots-pieges :
 - « draw OR DISCARD this card FROM YOUR DECK » : une defausse depuis la MAIN n'est pas concernee ;
 - « your discard pile » : celle du JOUEUR (pas la defausse de rencontre) ; elle revient donc dans son deck au remelange ;
 - donnee comme boost par Expanding Hive ? Non : 2 PV imprimes (< 3).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ap103 Alien Scout (09-12, Incite 1, Surge) pioche : distribue face cachee au joueur, qui pioche 1 carte a la place
      Preuve par substitution : **rouges 1/1** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap104 : Alien Scout (Minion)

```
Alien Scout (13-16, 4 exemplaires) — SBIRE. XENOMORPH. SCH 1, ATK 2, PV 2. Deck Xenomorph (dos rouge).
Teamwork ([[XENOMORPH]]).
Forced Interrupt: When you would draw or discard this card from your deck, draw 1 card. Deal this card to yourself as a facedown encounter card.
When Defeated: Place Alien Scout in your discard pile.

Cartes de reference :
 - Teamwork (XENOMORPH) : `desc.Teamwork`, natif (fiche teamwork.md).
 - Interruption depuis le deck du joueur : 27087b Maze of Mirrors (pioche ET defausse du deck, `SetBeInstead`, `DealEncounterCard`) ;
   carte de rencontre vivant dans un deck joueur : fiche weakness.md ;
 - « Place in your discard pile » : deplacement apres la defaite (`AfterUnitBeDefeated`) vers la defausse du joueur engage.

⚠ Mots-pieges :
 - « draw OR DISCARD this card FROM YOUR DECK » : une defausse depuis la MAIN n'est pas concernee ;
 - « your discard pile » : celle du JOUEUR (pas la defausse de rencontre) ; elle revient donc dans son deck au remelange ;
 - donnee comme boost par Expanding Hive ? Non : 2 PV imprimes (< 3).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ap104 Alien Scout (13-16, Teamwork) pioche : distribue face cachee au joueur, qui pioche 1 carte a la place
      Preuve par substitution : **rouges 1/1** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap201 : Advance (Treachery)

```
Advance — TRAITRISE (Apex Standard). Boost 1.
When Revealed: The villain schemes. Place this threat on the main scheme.

Cartes de reference : 01186 Advance (`FindVillain` + `DoSchemes`) ; la redirection des deux mechants (`ManiganceSurSaManigance`) lit
  `_ap_vers_le_complot` et s'efface le temps de cette manigance.

⚠ Mots-pieges :
 - « Place THIS threat on the MAIN scheme » : malgre « When <mechant> schemes, place that threat on his/her side scheme » ;
 - « the villain » = le mechant actif (regle du scenario) ; c'est une activation : au stade 1, le compteur passe ensuite.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ap201 Advance : la Reine manigance, la menace va au complot principal (pas sur Expanding Hive) ; le compteur passe
      Preuve par substitution : **rouges 1/1** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap202 : Advance Again (Treachery)

```
Advance Again — TRAITRISE (Apex Standard). Boost 1.
When Revealed: The villain schemes. Do not move the active villain counter.

Cartes de reference : 01186 Advance ; « Do not move the active villain counter » : garde consommee par 1B (`SansDeplacerLeCompteur`).

⚠ Mots-pieges : la menace va sur la manigance du mechant (sa regle ★ s'applique, contrairement a Advance) ; le compteur reste.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ap202 Advance Again : la Reine manigance sur Expanding Hive et le compteur RESTE sur elle
      Preuve par substitution : **rouges 1/1** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap203 : Assault (Treachery)

```
Assault — TRAITRISE (Apex Standard). Boost 1.
When Revealed (Alter-Ego): This card gains surge.
When Revealed (Hero): The villain attacks you. Do not move the active villain counter.

Cartes de reference : 01187 Assault (`WhenThisRevealed("Alter-Ego"|"Hero")`, 16116) ; surge gagne : `ThisCardGainSurge` (01187) ; « do not move » :
  `SansDeplacerLeCompteur`.

⚠ Mots-pieges : en alter-ego, AUCUNE attaque (et rien a garder) ; le compteur ne bouge pas apres cette attaque (stade 1 comme 2).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ap203 Assault (heros) : la Reine attaque et le compteur RESTE sur elle
      - ap203 Assault (alter-ego) : la carte gagne surge -> une carte de rencontre distribuee, aucune attaque
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap204 : Cruel Intentions (Treachery)

```
Cruel Intentions — TRAITRISE (Apex Standard). Boost ★ + 1. Incite 1.
Incite 1.
When Revealed: Deal each player 1 facedown encounter card. Give the villain 1 facedown boost card.
[star] Boost: Deal yourself 1 facedown encounter card.

Cartes de reference : Incite natif (`desc`) ; `DealEncounterCards(1)` ; « Give the villain 1 facedown boost card » :
  `Faces.GiveFacedownBoostCards([mechant], 1)` (27150).

⚠ Mots-pieges : « EACH player » ; « the villain » = le mechant actif ; en boost, « yourself » = le joueur attaque / vise.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ap204 Cruel Intentions : chaque joueur recoit 1 carte de rencontre face cachee, le mechant actif 1 carte boost ; Incite 1
      - ap204 Boost : le joueur se distribue 1 carte de rencontre face cachee
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap205 : Overwhelming Force (Treachery)

```
Overwhelming Force — TRAITRISE (Apex Standard). Boost ★ + 2.
When Revealed: Discard the highest cost upgrade or support you control. If no card was discarded this way, this card gains surge.
[star] Boost: Give the villain 1 additional boost card for this activation.

Cartes de reference : 07034 Pile It On (`DiscardControlCards(upgrade=True, support=True, highest_cost=True)`) ; surge gagne :
  `ThisCardGainSurge` (01187) ; « 1 additional boost card for this activation » : `message.GiveBoostCardForThisActivation(Villain, 1)` (16116).

⚠ Mots-pieges : « the HIGHEST cost » (egalite : le joueur choisit, natif) ; « upgrade OR support YOU control » ; rien a defausser -> surge.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - ap205 Overwhelming Force : le soutien au cout le plus eleve (Avengers Mansion, 4) est defausse
      - ap205 rien a defausser : la carte gagne surge (la carte suivante, 01105, est revelee)
      - ap205 Boost : le mechant recoit 1 carte boost supplementaire pour cette activation (01105 retournee puis defaussee)
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap206 : Masterplan (Treachery)

Aucun module : `ability_link` vers **01192 Masterplan** (texte imprimé identique mot pour mot à la carte du core, relu sur le scan).

- [x] Étape 2 : carte de référence : 01192 Masterplan (le script officiel EST la capacité).
- [x] Étape 5 : texte-contre-code : texte imprimé comparé mot pour mot à la carte du core. Résultat : identique.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ap206 Masterplan (ability_link 01192) : 4 menaces sur CHAQUE manigance annexe (Expanding Hive et Skulls for the Taking)
      Preuve par substitution : sans objet (aucun module ; le cas prouve que le lien vers la carte du core joue). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap207 : Shadow of the Past (Treachery)

Aucun module : `ability_link` vers **01190 Shadow of the Past** (texte imprimé identique mot pour mot à la carte du core, relu sur le scan).

- [x] Étape 2 : carte de référence : 01190 Shadow of the Past (le script officiel EST la capacité).
- [x] Étape 5 : texte-contre-code : texte imprimé comparé mot pour mot à la carte du core. Résultat : identique.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ap207 Shadow of the Past (ability_link 01190) : le sbire nemesis (Vulture) et la manigance nemesis (Highway Robbery) entrent en jeu
      Preuve par substitution : sans objet (aucun module ; le cas prouve que le lien vers la carte du core joue). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap301 : Yautja Young Blood (Minion)

```
* Yautja Young Blood — SBIRE unique. YAUTJA. SCH 1, ATK 1, PV 4. Boost 1.
Patrol. Incite 2 (3 instead if Predator Warlord is the active villain).
When Defeated: Place 2 threat on The Ultimate Hunt, if you cannot shuffle Yautja Young Blood into the encounter deck.

Cartes de reference : Patrol, Incite natifs (`desc`) ; « 3 instead if ... » : `ThisGainIncite` (50094, comme ap018) ; « shuffle into the
  encounter deck » : `Faces.ShuffleAllTo(.., "EncounterDeck")` (pd003).

⚠ Mots-pieges :
 - « The Ultimate Hunt » = le complot du stade 1 (par son NOM) : aux stades 2 a 4 on ne peut pas -> melange ;
 - 4 PV imprimes : Expanding Hive le donne d'abord comme boost, il y RESTE (arbitrage du 25/10/2026).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - ap301 Yautja Young Blood : Incite 3 quand le Warlord est le mechant actif
      - ap301 Incite 2 quand la Reine est active
      - ap301 When Defeated au stade 1 : 2 menaces sur The Ultimate Hunt
      - ap301 When Defeated au stade 2, sans Expanding Hive : « if you cannot », melange dans le deck de rencontre
      Preuve par substitution : **rouges 3/4** sans le module ; verts restants : Incite 2 avec la Reine active (valeur imprimee, native). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap302 : Blooded Predator (Minion)

```
* Blooded Predator — SBIRE unique. YAUTJA. SCH 2, ATK 2, PV 4. Boost 3.
When Revealed: Stun your identity. If you are already stunned, take 3 damage.
When Defeated: Give Predator Warlord a tough status card. If you cannot, give this card to the active villain as a facedown boost card.

Cartes de reference : `GiveStatus("Stunned"|"Tough")`, `IsStunned` / `IsTough` ; « give this card ... as a facedown boost card » : 60075.

⚠ Mots-pieges :
 - « If you are ALREADY stunned » : 3 degats A LA PLACE (pas de seconde carte Sonne) ;
 - « If you cannot » : Predator Warlord absent (vaincu) ou deja Tenace ;
 - 4 PV : Expanding Hive l'a peut-etre deja donne comme boost : il y reste (arbitrage du 25/10/2026).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - ap302 Blooded Predator revele : l'identite est sonnee
      - ap302 identite deja sonnee : 3 degats a la place
      - ap302 When Defeated : le Warlord recoit une carte Tenace
      - ap302 Warlord deja Tenace (et pas d'Expanding Hive) : « if you cannot », la carte est donnee au mechant actif comme boost
      Preuve par substitution : **rouges 4/4** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap303 : Predator Elite (Minion)

```
* Predator Elite — SBIRE unique. ELITE. YAUTJA. SCH 2, ATK 2, PV 6. Boost 2.
When Revealed: Discard an upgrade or support you control.
When Defeated: Discard the top card of your deck and deal damage to a [[XENOMORPH]] enemy equal to that cards printed cost.

Cartes de reference : `DiscardControlCards(upgrade=True, support=True)` (07034, choix du joueur) ; `DiscardDeckTopCards(1)` +
  `FacesCounter.GetPrintedCost` (27170) ; degats a un ennemi au choix.

⚠ Mots-pieges :
 - « an upgrade OR support YOU control » : au choix du joueur ; rien -> rien ;
 - « YOUR deck » (When Defeated) : le joueur qui l'a vaincu ; « A [[XENOMORPH]] enemy » : un seul, au choix ; carte sans cout -> 0.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ap303 Predator Elite revele : un soutien du joueur est defausse
      - ap303 When Defeated : carte du dessus du deck (Black Cat, cout 2) -> 2 degats a un ennemi XENOMORPH (la Reine)
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap304 : Apex Predator (Minion)

```
* Apex Predator — SBIRE unique. ELITE. YAUTJA. SCH 1, ATK 3, PV 7. Boost 2.
Toughness.
[star] Apex Predator's attacks gain piercing.
Forced Response: After a character attacks Apex Predator, discard the top card of the encounter deck. If that card is a treachery, stun the
  attacker.

Cartes de reference : Toughness natif (`desc`) ; `UnitAttackGainKeyword("This", piercing=True)` (27059) ; la Reponse est mot pour mot
  55044 God of Lies (`AfterUnitAttackUnit(ForcedResponse, Hero|Ally, "This")`, `DiscardEncounterCards(1)`, `Filter.ByType(.., Treachery)`).

⚠ Mots-pieges : « a CHARACTER » : heros ou allie ; « stun the ATTACKER » (pas l'identite).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - ap304 Apex Predator attaque : perforante (la Tenace du heros est ignoree), 3 degats
      - ap304 attaque par le heros, la carte du dessus du deck de rencontre est une traitrise : l'attaquant est sonne
      - ap304 contre-cas : la carte defaussee est un sbire -> pas d'etourdissement
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap305 : The Hunt Begins (SideScheme)

```
The Hunt Begins — MANIGANCE ANNEXE. Menace 5 (fixe). Boost 2.
Allies cannot defend against enemy attacks.
Forced Response: After a [[YAUTJA]] enemy attacks, give it a tough status card.
When Defeated: Stun or confuse an enemy.

Cartes de reference : `UnitCannotDefend(Ally, Enemy, cannot_trigger_defense_ability=True)` (27152) ; « After X attacks » :
  `AfterUnitAttackEnd(ForcedResponse, ..)` ; « When Defeated » d'une manigance : `WhenSchemeBeDefeated(WhenDefeated, "This")` (tk).

⚠ Mots-pieges : « ALLIES cannot defend » (le heros, si) ; « a YAUTJA ENEMY » : mechant ou sbire YAUTJA ; « stun OR confuse AN enemy » :
  le joueur qui la vainc choisit l'ennemi ET l'etat.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (5 cas sujets) :
      - ap305 The Hunt Begins : apres l'attaque d'un ennemi YAUTJA (le Warlord), il recoit une carte Tenace
      - ap305 contre-cas : la Reine (XENOMORPH) attaque -> pas de carte Tenace
      - ap305 les allies ne peuvent pas defendre : Black Cat n'est pas un defenseur legal contre la Reine ; le heros, si
      - ap305 ligne de base : sans The Hunt Begins, Black Cat peut defendre
      - ap305 When Defeated : un ennemi est sonne (1re option)
      Preuve par substitution : **rouges 3/5** sans le module ; verts restants : contre-cas « la Reine n'est pas YAUTJA » et « ligne de base : Black Cat peut defendre ». Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### ap306 : Cloaking Device (Attachment)

```
Cloaking Device — ATTACHEMENT. WEAPON. Boost 1.
Attach to Predator Warlord. If you cannot, attach to a [[YAUTJA]] minion. Otherwise, this card gains surge.
Reduce the amount of damage attached enemy takes from each attack by 2.
Hero Action: After a hero makes a basic attack against this enemy, spend [energy][physical] resources → discard this card.

Cartes de reference : 21117 (Thanos) : `ReduceCharacterTakeDamageBy(.., from_each_attack=True)` + `AfterUnitMakeBasicAttack(HeroResponse,
  Hero, DiscardThisCard, against_who=).SetCost(Cost("YR"))` ; attachement : `AttacherAuWarlordSinonYautja` (comme ap012).

⚠ Mots-pieges :
 - « Hero Action: After ... » : formulation hybride ; arbitrage 3 du 25/10/2026 : c'est une REPONSE de heros, juste apres l'attaque de
   base contre l'ennemi equipe ;
 - « from EACH attack » : -2 par attaque (pas par source de degats) ; [energy] = Y, [physical] = R.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ap306 Cloaking Device sur le Warlord : -2 degats par attaque (l'attaque de base du heros, 2, ne lui fait rien)
      - ap306 Reponse de heros apres une attaque de base contre le porteur : depenser [energy][physical] -> Cloaking Device defaussee
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 45 parties (spider_man : alien_vs_predator 15, alien_vs_predator_expert 15, rhino témoin 15 ; 3 profils), 0 erreur dans les 45 journaux, journaux lus (alternance du compteur actif, Incitation du Drone, passage au stade 2). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).
