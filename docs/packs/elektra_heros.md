# Elektra (HÉROS, Hero Pack officiel MC63, FFG, novembre 2026) : gabarits PROCESSUS-CARTE

Chantier du 13/11/2026. Pack `elektra` (aspects 63015-63039, voir `elektra_cartes.md`), set « Elektra » (`src/cards/pack/elektra/elektra/`) et
set « Elektra Ninja » (`.../elektra_ninja/`, les trois cartes du paquet Ninja). Numéros = numéros de collection imprimés. Plan, textes
transcrits et décisions : `.planning/elektra-heros/PLAN.md`. Scans : `.planning/elektra-iron-fist-scans-marvelsimulator/` (source
play.marvelsimulator.com), posés dans `assets/pics/63001a.png` à `63014.png`.

## Décisions de l'utilisateur (13/11/2026)
1. **Comme Iron Fist** : héros + 15 cartes signature + paquet Ninja. **Mise à jour du 14/11/2026** : le set NÉMÉSIS 63029-63033 est monté (voir la
   section « Set némésis » plus bas). **L'obligation 63028 n'est PAS montée, décision de l'utilisateur du 14/11** : pas de scan officiel (seule une image
   « Unofficial preview » existe sur play.marvelsimulator.com) ; c'est la seule carte manquante. 63024-63026 : absents partout (très probablement les
   réimpressions Energy / Genius / Strength, non prouvé). Resurrection Altar : PV à 9, « trouvez votre obligation » sans effet tant qu'elle n'existe pas.
2. **Extension moteur fidèle** pour le boost d'un héros (voir ci-dessous).
3. **White Tiger 63011** : « Otherwise » = si le paquet NINJA est VIDE, Elektra reçoit 1 carte de boost face cachée.
4. **Étoiles sur THW / ATQ / DEF** : « décrit dans la capacité du héros » (le ★ Villainous) : aucun effet propre.
5. « Up to N » (63007, 63008) : règle officielle : le joueur choisit de 0 à N (`DeclareNumber`).

## Extension moteur (touche le moteur : cas de non-régression rejoués)
- `can_boost.py` : `BoostContext`, `CanBoost.HeroBoostForBasicPower(would_message, "THW"|"DEF")`, et `ResolveBoostCards` par **instantané** pour un héros
  (une carte re-donnée « Otherwise » ne boucle pas ; les ennemis gardent la boucle d'origine).
- `can_thwart.py` / `can_defense.py` : appel après `WhenUnitUseBasicPower`. Avant : seules l'ATTAQUE (héros) et l'attaque/manigance d'un ENNEMI résolvaient
  une pile de boost ; une carte donnée à un héros pour un DÉJOUER ou une DÉFENSE restait posée (limite documentée dans `doctor_doom/dd001a.py`).
- `sender_card.py` : `getattr(property, 'against_player', None)` dans les trois messages de boost (un déjouer / une défense n'a pas de joueur visé).
- `card_face.py` : trait `ACROBATIC` (lu par Elektra's Sai 63012).
- Harnais `tools/test_capacites.py` : clés `deck_annexe`, `deck_annexe_taille`, `rencontre_compte` (additives).
- **Non-régression** (tout vert) : `dd0` 17, `hc0` 47, `ca0` 111, `bc0` 29 + 88 cas des cartes qui donnent des boosts à un héros (`sn013 sf011 ss011 bm018-021 dz021/23
  mu002/5 ze013/16 56150-56159 56091/56210 ap006b ap009 60094 60165 60175 27150 Scarlet Villainous`).

## Pièges notés
- Le montage `Puzzle.ChangeToFace('63001b','63001a')` DÉCLENCHE Ninja Training : base 5 cartes Ninja / 1 en rencontre dans les cas.
- Killer Instinct est une Interruption que le PILOTE prend d'office : les effets Boost des cartes Ninja sont mesurés SANS elle sur Doctor Doom / Iron Fist
  (`Puzzle.GiveFacedownBoost(cible, '6300x')`) ; le cas « Otherwise » = boost d'un ENNEMI (`Puzzle.Boost`).
- Une attaque par ÉVÉNEMENT (Killer Blow) ne retourne pas la pile de boost du héros : c'est la carte événement qui frappe, pas le héros.
- `unite.GetControlByPlayer()` ASSERT sur un ennemi : lire le joueur par `message.GetAgainstPlayer()` quand la carte sert de boost à un ennemi.
- `Puzzle.PutIntoPlay('X')` deux fois rend la MÊME carte : pour deux exemplaires, `CreatePlayerDeck` puis `PutIntoPlay` à chaque fois.
- Un fichier nommé comme un deck dans `.game-src/` (rapport de `verifier_api_cartes`) est pris par l'autoplay pour un deck : le supprimer.

## Cartes (15 + 3 Ninja) : cas `[elektra]` (tools/cas/elektra_hero.py), 39 cas verts
Preuve par substitution (`tools/substituer_pack.py ... 6300|6301`) : **chaque carte a au moins un cas qui tombe au ROUGE sans son module**. Cas restés verts sans module =
contre-cas d'ABSENCE d'effet (assumés) : 63005 (défausse de rencontre vide), 63010 (témoin sans Autel), 63011 (alter-ego), 63013 (alter-ego sans Prerequisite, témoin main à 5).

| card_id | Carte | Cas | Rouges sans module |
|---|---|---|---|
| 63001a | Elektra (Villainous, Killer Instinct) | 3 | 2/2 |
| 63001b | Elektra Natchios (paquet Ninja, Ninja Training) | 2 | 2/2 |
| 63002 | Ninja Stars | 1 | 1/1 |
| 63003 | Ninja Strike | 5 | 4/4 (cas Killer Instinct renommé 63001a) |
| 63004 | Ninja Vanish | 1 | 1/1 |
| 63005 | Daredevil (allié) | 3 | 2/3 |
| 63006 | Acrobatic Prowess | 1 | 1/1 |
| 63007 | Killer Blow (up to 5, 3 cas) | 3 | 3/3 |
| 63008 | Move Unseen (up to 4) | 2 | 2/2 |
| 63009 | Sai Strike | 2 | 2/2 |
| 63010 | Resurrection Altar | 2 | 1/2 |
| 63011 | White Tiger (« Otherwise » = paquet vide) | 3 | 2/3 |
| 63012 | Elektra's Sai | 2 | 2/2 |
| 63013 | History with the Hand | 5 | 3/5 |
| 63014 | Stealth Mastery (attaque / attaqué, ±3) | 5 | 4/5 |

## Autres gates (13/11/2026)
- `test_cards` : **8364 ok / 0 erreur** ; `verifier_prefixes` OK ; `verifier_appels_modules elektra` OK **calibré** (une sonde `Faces.MethodeInexistanteElektra` le fait
  tomber, puis retirée) ; `verifier_api_cartes` : 9426 fichiers, 0 en faute.
- `DECK_NOM=elektra verifier_tous_les_decks` : « identité 63001a, main 6, deck 9 » (témoin spider_man : main 6, deck 34).
- **Autoplay** : `autoplay.py --deck elektra --vilains rhino --profils equilibre --parties 8` : 0 victoire / 8 (3,6 rounds), 0 blocage, **0 traceback** sur les 8 journaux ;
  témoin `spider_man` même fournée : 0 / 8 (7,0 rounds), 0 blocage. Elektra n'a que ses 15 cartes signature (`player_deck` vide, PROCESSUS-HEROS étape 3) : la défaite rapide est
  attendue. Les journaux montrent le flux réel : Ninja révélée → donnée à Elektra comme boost → retournée avec Killer Instinct (« appliquent / n'appliquent plus »).
- Écran (Chromium, moteur de test local, 13/11) : Elektra dans la sélection (visuel, DEFENDER · MARTIAL ARTIST · ASSASSIN, PV 9), biographie au survol, deck proposé choisi, partie lancée ;
  le paquet Ninja est dessiné à côté de l'identité (6 cartes, dessus visible).

## Set némésis 63029-63033 (14/11/2026) : gabarits PROCESSUS-CARTE
Set « Elektra Nemesis », `src/cards/pack/elektra/elektra_nemesis/`, déclaré dans `deck/starter/elektra.json`. Scans anglais :
`.planning/elektra-iron-fist-scans-mc4db/` et `-marvelsimulator/`, posés dans `assets/pics/`. Cas : `tools/cas/elektra_nemesis.py`, préfixe
`[elektra_nem]`, **18 cas verts** (filtre `[elektra` : 57/57). Fiches mots-clés lues : `quickstrike`, `ranged`, `hazard`, `boost`.

**Correctif moteur lié** (`boost.py`, `check_cette_carte_est_le_boost`) : un ★ Boost ne vaut que pour la carte retournée ; avant, Aka EN JEU se
distribuait lui-même à chaque autre carte de boost. Fiche `docs/reference/mots-cles/boost.md`. Cas dédiés `tools/cas/boost_carte_en_jeu.py`
(`[boost_en_jeu]`) : 6/6 verts avec le correctif, 3/6 rouges sans (les trois cas « EN JEU »). Cartes touchées rejouées : `62029`, `62030`, `62032`, `60062`.

| card_id | Carte | Étape 2 (modèle) | Étape 5 (mots lus) | Cas (7) | Rouges sans module | 7 bis | 8 (écran FR) | 8 bis | Terminée |
|---|---|---|---|---|---|---|---|---|---|
| 63029 | Aka (sbire némésis, Quickstrike) | `62029` Cottonmouth | « shuffle into the encounter deck » si vaincu ; ★ Boost : donné face cachée au joueur Elektra | 4 | 2/4 (verts : valeurs imprimées, cas EN JEU porté par le moteur) | OUI (boost.py, ci-dessus) | voile FR vu | NON | OUI |
| 63030 | The Fist Fits in the Hand (manigance annexe, Hazard) | manigances annexes à bonus de trait | « each HAND minion gets +1 ATK and +1 SCH » | 4 | 1/4 (verts : témoin, sbire sans trait, icône imprimée) | NON | voile FR vu (paysage : `ZONES_MANUELLES` + `VOILE_UNI`) | NON | OUI |
| 63031 | Hand Katana (attachement) | attachements « otherwise attach to the villain » | sbire HAND aux PV les plus hauts, sinon le méchant (`Villain`) ; +2 ATQ ; Hero Action 2 ressources | 3 | 3/3 | NON | voile FR vu | NON | OUI |
| 63032 | Hand Blademaster (sbire) | sbires à bonus conditionnel | +1/+1 tant qu'un AUTRE sbire HAND est en jeu ; mélangé si vaincu | 5 | 2/5 (verts : ligne de base, témoin de ranged, retour à 1/1) | NON | voile FR vu | NON | OUI |
| 63033 | Hand Archer (sbire, Ranged) | `ranged` (fiche) | attaque sans riposte ; mélangé si vaincu | 2 | 2/2 | NON | voile FR vu | NON | OUI |

Gates du 14/11 : `verifier_appels_modules elektra iron_fist` OK ; `test_cards` 8373 ok / 0 erreur ; `verifier_api_cartes` 9437 fichiers, 0 en faute ;
`DECK_NOM=elektra verifier_tous_les_decks` : « identité 63001a, main 6, deck 9 » ; autoplay 8 parties contre Rhino : 0 traceback, 0 victoire, 1 partie
arrêtée par le garde anti-répétition du pilote sur Killer Instinct (graine 2, pas une carte némésis). Les cartes némésis ne sont JAMAIS sorties en
autoplay (mises de côté) : leur preuve est dans les cas. Écran (Chromium, FR) : les 5 cartes affichent le voile français ; en anglais, le scan brut.
Voile des scans paysage basse résolution à filigrane : zones posées à la main (`zones-corrections.ts`, `ZONES_MANUELLES` + `VOILE_UNI`).

## Ce qui reste NON vérifié (à dire clairement)
- **Aucune partie jouée par un humain** avec Elektra. La pile de boost du HÉROS (cartes données et en attente) n'a pas été regardée à l'écran : seul le paquet Ninja l'a été.
- **L'obligation 63028 n'est pas montée** (décision du 14/11, pas de scan officiel) : Resurrection Altar ne révèle rien. Le set némésis n'a été vu ni en autoplay ni en partie humaine.
- Traits `ACROBATIC` : pas de traduction française officielle connue (affiché en anglais). Textes français des 15 cartes : PROVISOIRES (`textes-fr-fanmade.ts`).
- Les ★ de THW/ATQ/DEF : interprétation de l'utilisateur, aucun effet propre.
- **Héros terminé : NON** tant que la partie humaine et l'obligation 63028 ne sont pas faites ; tous les gabarits ci-dessus sont verts.
