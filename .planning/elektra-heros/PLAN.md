# Elektra (héros officiel, Hero Pack MC63) : plan et transcription

Décision du 13/11/2026 (utilisateur, « Go ») : monter le HÉROS Elektra. Elle annule la limite du chantier du 22/10
(`docs/packs/elektra_cartes.md` : « cartes d'aspect seulement »). Pack existant `elektra` (aspects 63015-63039) ;
le héros va dans `src/cards/pack/elektra/elektra/` (set_name « Elektra »). Processus : `docs/reference/PROCESSUS-HEROS.md`
+ `PROCESSUS-CARTE.md` par carte.

Scans (relus un par un le 13/11) : `.planning/elektra-iron-fist-scans-marvelsimulator/` (source play.marvelsimulator.com),
posés dans `assets/pics/63001a.png` à `63014.png` (300 px pour 63001a-63009, 600 px pour 63010-63014).

Obligation et set némésis : NON PUBLIÉS (63024-26 et 63028-33 absents du simulateur). Précédent Iron Fist :
héros + cartes signature seulement (`docs/packs/iron_fist_cartes.md`).

## Cartes (15 exemplaires + 6 cartes Ninja)
| card_id | Nom | Type | Coût | Texte imprimé |
|---|---|---|---|---|
| 63001a | Elektra | Hero | HP 9, main 5, THW 0★ ATK 1★ DEF 1★ | DEFENDER. MARTIAL ARTIST. ★ Villainous (quand ce personnage utilise un pouvoir de base, lui donner une carte boost). *Killer Instinct* — Interrupt : quand une carte boost donnée à Elektra est retournée face visible, annule son effet « Boost ». Puis cette carte gagne [icône boost]. |
| 63001b | Elektra Natchios | AlterEgo | HP 9, main 6, REC 3 | ASSASSIN. Elektra Natchios commence la partie avec un paquet NINJA (voir encart). *Ninja Training* — Interrupt : quand tu passes en forme héros, mélange la carte du dessus du paquet NINJA dans le paquet de rencontre. |
| 63002 | Ninja Stars (2/6) | Treachery | | NINJA. Surge. When Revealed : donne cette carte à Elektra comme carte boost face cachée. ★ Boost : si Elektra utilise un pouvoir de base, pioche 2 cartes et mélange cette carte dans le paquet NINJA. Sinon, donne-la à Elektra comme carte boost face cachée. |
| 63003 | Ninja Strike (3/6) | Treachery | | NINJA. Surge. When Revealed : idem. ★ Boost : si pouvoir de base, +3 à ce pouvoir pour cet usage et mélange cette carte dans le paquet NINJA. Sinon, donne-la comme carte boost face cachée. |
| 63004 | Ninja Vanish (5/6) | Treachery | | NINJA. Surge. When Revealed : idem. ★ Boost : si pouvoir de base, lui donner une carte statut Tough et mélanger cette carte dans le paquet NINJA. Sinon, donne-la comme carte boost face cachée. |
| 63005 | Daredevil (Matt Murdock) | Ally | 3, THW 2★ ATK 2★, icône Mental(?) vert | DEFENDER. MARTIAL ARTIST. ★ Response : après que Daredevil utilise un pouvoir de base, place une carte de la défausse de rencontre sur le dessus du paquet de rencontre. |
| 63006 | Acrobatic Prowess (2-3/15) | Event | 1, Agilité (jaune/éclair) | ACROBATIC. SKILL. Hero Action : prépare Elektra et donne-lui 1 carte boost face cachée. |
| 63007 | Killer Blow (4-5/15) | Event | 2, éclair | ATTACK. Hero Action (attack) : inflige jusqu'à 5 dégâts à un ennemi. Si cette attaque le bat, mélange la carte du dessus du paquet NINJA dans le paquet de rencontre. |
| 63008 | Move Unseen (6-7/15) | Event | 2, mental | ACROBATIC. THWART. Hero Action (thwart) : retire jusqu'à 4 menaces d'un complot. Mélange la carte du dessus du paquet NINJA dans le paquet de rencontre. |
| 63009 | Sai Strike (8-9/15) | Event | 1, physique | ATTACK. Hero Action (attack) : inflige 3 dégâts à un ennemi. Pour chaque Sai d'Elektra que tu contrôles, mélange la carte du dessus du paquet NINJA dans le paquet de rencontre. |
| 63010 | Resurrection Altar (10/15) | Support | 1, ★, mental | HAND. LOCATION. Interrupt : quand tu serais vaincu, retire cette carte du jeu → mets ton cadran de PV à 9 à la place. Trouve ton obligation et révèle-la. |
| 63011 | White Tiger (11/15) | Support | 1, ★, mental | PERSONA. Response : après que tu passes en forme héros, mélange la carte du dessus du paquet NINJA dans le paquet de rencontre. Sinon, donne 1 carte boost face cachée à Elektra. |
| 63012 | Elektra's Sai (12-13/15) | Upgrade | 2, physique | WEAPON. Restricted. Hero Action : épuise le Sai d'Elektra → inflige 1 dégât à un ennemi et réduis de 1 le coût du prochain événement ACROBATIC ou ATTACK que tu joues cette phase. |
| 63013 | History with the Hand (14/15) | Upgrade | 0, mental | CONDITION. Prerequisite (hero form). +1 taille de main. Forced Response : après que tu changes de forme, défausse cette carte. [icône hand/resource] |
| 63014 | Stealth Mastery (15/15) | Upgrade | 1, éclair | SKILL. Forced Interrupt : quand tu attaques ou es attaqué, choisis d'augmenter ou de réduire de 3 les dégâts de cette attaque. Mets Stealth Mastery sur le dessus de ton paquet. |

À LIRE ENCORE : l'encart (« See insert »), la composition exacte du paquet NINJA (6 cartes : 2 + 2 + 2), les icônes de
ressource (à comparer à une carte du même pack, jamais à vue), les traits/icônes de 63005 et 63013.

## Décisions de l'utilisateur (13/11/2026)
1. Comme Iron Fist : pas d'obligation ni de set némésis (non publiés). Altar : PV à 9, aucune obligation à révéler.
2. Boost : extension moteur FIDÈLE (effets Boost des cartes Ninja exécutés).
3. White Tiger 63011 : « Otherwise » = si le paquet Ninja est VIDE : alors Elektra reçoit 1 carte boost face cachée
   (un seul des deux effets par passage en forme héros).
4. Étoiles sur THW/ATK/DEF d'Elektra : « décrit dans la capacité du héros » (= le Villainous ★). Aucun effet propre,
   affichage seul. Elektra (forme héros) n'a pas de RÉC : le boost ne concerne que ATTAQUE, DÉJOUER, DÉFENSE.

## État (13/11, soir) : non commité
- `data/cards.json` : 15 fiches insérées (script `inserer-cartes.py`), trait ACROBATIC ajouté à `card_face.py`,
  `sets_info.json` (heroes: elektra, max_id 63014), `deck/starter/elektra.json`, dossiers `elektra/elektra/` et
  `elektra/elektra_ninja/` (set « Elektra Ninja » pour 63002-63004), checksums recalculés.
- Reste : scripts (aucun), moteur (boost THW/DEF), cas, FR, bio, gates, partie.

## Avancement (13/11, nuit) : non commité
- Scripts + cas verts ET prouvés par substitution : 63001b (2 cas), 63007 (3), 63008 (2), 63009 (2), 63012 (2). Cas dans
  `tools/cas/elektra_hero.py` (préfixe `[elektra]`, 11/11 verts). Clés harnais ajoutées : `deck_annexe`, `deck_annexe_taille`,
  `rencontre_compte` (CLES_ETAT_ATTENDU de `test_capacites.py`). Lancer : `cd Fusion/marvel-lcg-src && CAS_PREFIX=elek_
  PARALLELES=3 ../../.venv-linux/bin/python tools/test_capacites.py .game-src 36100 <rapport> "[elektra]"`.
- ⚠ Le montage HEROS (`Puzzle.ChangeToFace('63001b','63001a')`) déclenche Ninja Training : base 5 cartes Ninja / 1 en rencontre.
- Reste : 63001a, 63002-4 (Ninja), 63005, 63006, 63010, 63011, 63013, 63014 + moteur boost (THW/DEF).
- (13/11, nuit) Ajoutés et verts : 63005 (3 cas), 63006 (1), 63010 (2), 63011 (3), 63013 (5). Preuve par substitution faite pour 63010 et 63013
  (cas restés verts = contre-cas d'absence : témoin sans Autel, alter-ego sans Prerequisite, témoin main à 5). À prouver : 63005, 63006, 63011.
- NOYAU BOOST (à faire) : (1) Killer Instinct 63001a = Interruption sur `WhenBoostCardTurnedFaceUp` (modèle hc010) : annule le Boost
  de la carte donnée à Elektra + la carte gagne 1 icône boost ; (2) cartes Ninja 63002-4 : When Revealed = donner la carte à Elektra comme
  boost face cachée ; ★ Boost via `WhenCardBecomeBoost` ; (3) moteur : `can_boost.ResolveBoostCards` doit traiter les cartes de boost d'un
  HÉROS par instantané (une carte re-donnée « Otherwise » ne doit pas boucler) ; boost + résolution aussi sur DÉJOUER et DÉFENSE de base
  (aujourd'hui seulement ATTAQUE et manigance d'ENNEMI) ; (4) Stealth Mastery 63014 (±3 dégâts, attaquant OU attaqué).
- (13/11, nuit, suite) NOYAU BOOST FAIT : 63001a (Villainous natif + Killer Instinct), 63002-4 (Ninja), extension moteur
  `CanBoost.HeroBoostForBasicPower` + instantané dans `ResolveBoostCards` + `getattr(...against_player)` dans sender_card.py,
  appel dans can_thwart.py et can_defense.py. 32 cas `[elektra]` verts. Non-régression rejouée : dd0 (17), hc0 (47), ca0 (111), bc0 (29),
  88 cas des cartes qui donnent des boosts à un héros (sn013, sf011, ss011, bm018-021, dz021/23, mu002/5, ze013/16, cw, ap, fne, 27150...) : TOUT VERT.
- ⚠ Killer Instinct est une Interruption que le PILOTE prend d'office : pour mesurer les effets Boost des cartes Ninja SANS elle, les cas
  utilisent Doctor Doom / Iron Fist + `Puzzle.GiveFacedownBoost(cible, '6300x')`. Le cas « Otherwise » = boost d'un ENNEMI (Rhino) : `Puzzle.Boost`.
- ⚠ Une attaque par ÉVÉNEMENT (Killer Blow) ne retourne PAS la pile de boost du héros (c'est la carte événement qui frappe, pas le héros).
- Reste : 63014 Stealth Mastery, preuves par substitution (63001a, 63002-4, 63005, 63006, 63011), gates (verifier_tous_les_decks,
  verifier_appels_modules, test_cards), autoplay, plateau (paquet Ninja), FR (`textes-fr-fanmade.ts`), bio, doc `docs/packs/elektra_heros.md`.
