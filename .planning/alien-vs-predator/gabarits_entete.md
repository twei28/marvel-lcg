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
- [x] Cas : **122 cas `[ap]` verts**, joués avec les règles d'une vraie partie (`v16_all` + `v18_all`) et le remplissage neutre 01098 ; passe tracée par
      `MCLCG_TRACE_CRASH` : **0 exception avalée** (une assertion de l'ancien surge, propre au harnais, venait du remplissage 01105 qui s'enchaînait ;
      corrigé le 25/10/2026, The Vault compris : 84/84 cas `[vt]` verts, 0 exception).
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

