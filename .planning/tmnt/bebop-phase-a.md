# Bebop & Rocksteady (TMNT Villains, Inkwire), préfixe `tk`

Source : zip `TMNT Enemies -20261014T200338Z-1-001.zip`, dossier « Bebop & Rocksteady v3/ » (53 PNG dont
l'encart de règles). Scans réduits en JPEG 615 px (`tools/importer_images_bebop_rocksteady.py`) dans
`Fusion/marvel-lcg-src/assets/pics/` (gitignoré) ET `.planning/tmnt/pics-bebop/` (40 fichiers versionnés).
Pack `bebop_rocksteady`, set 192, auteur `Inkwire` (champ `custom`). Questions ouvertes :
`.planning/tmnt/bebop-questions.md`.

## Structure du scénario

- **Un seul stade de complot** : `tk005a` (1A : Contenu + Mise en place) / `tk005b` (1B : menace 7 par
  joueur, +1 par joueur, départ 0). Il ne se perd JAMAIS par la menace : à l'accomplissement, la menace
  est retirée à la place et les deux vilains attaquent chaque joueur.
- **Deux vilains, chacun à deux faces ALERT / K.O.** (cartes recto-verso `tk001a/b` Bebop A1/A2,
  `tk002a/b` Bebop B1/B2, `tk003a/b` Rocksteady A1/A2, `tk004a/b` Rocksteady B1/B2). Normal = A1,
  expert = B1 : deux fichiers de scénario (`bebop_rocksteady`, `bebop_rocksteady_expert`), `villain: []`
  et les deux vilains dans `set_aside` (montage de Sinister Six `27100a`), mis en jeu par le Setup de `tk005a`.
- **Chaque vilain porte un attachement permanent « Temper » à deux faces** (`tk007a/b` Hog Wild /
  Headfirst pour Bebop, `tk008a/b` Rhino Rage / Headstrong pour Rocksteady) qui porte les jetons
  `knucklehead` (compteur ajouté à l'énumération `COUNTER`).
- **L'environnement Destructive Dunderheads** (`tk006a/b`) fait activer les deux vilains, fait choisir « le
  vilain », met de côté un vilain vaincu et se retourne en attachement Gone Berserk sur le survivant.
- **Insert de règles = RÈGLE codée** (décision utilisateur pour les inserts TMNT) : aucune carte. Dodgy,
  les FAQ (priorité des cartes d'état, plus de retournement K.O. après une défaite) sont dans les scripts.
- **Ensembles** : « Bebop & Rocksteady » (20 cartes de rencontre, `data/encounter_sets/bebop_rocksteady.json`),
  « Concrete Jungle » (module FIXE : `tk101` de côté, 4 cartes Linked, `concrete_jungle.json` = 2 Road to
  Ruin + 2 Fallen Empires), « Rock the Block » (module recommandé, `rock_the_block.json`).
  Les scénarios utilisent `tmnt_standard` / `tmnt_expert` (ensembles `te`), basculés à la fusion du 16/10/2026.

## card_id (`tk` + 100 x module + numéro imprimé)

Copies identiques (même scan, seul le numéro imprimé change) = UN card_id : tk016 (16-17), tk018 (18-19),
tk020 (20-21), tk022 (22-23), tk024 (24-25), tk026 (26-27), tk102 (2-3), tk104 (4-5), tk201 (1-2), tk203 (3-4).
Les trois Bumbling Buffoons (13, 14, 15) ont trois illustrations : tk013, tk014, tk015. Bebop et Rocksteady
existent aussi comme SBIRES du scénario Shredder (préfixe `ts`) : tout le code compare des card_id, des
types (`card_type=Villain`) ou `NomDuVilain`, jamais le nom seul.

## Icônes vérifiées par découpe contre des cartes officielles

Boost = `01111`/`01122` (icône rouge) ; étoile de boost = `01121` ; Accélération = `01109` (maison+) ;
Aléa = `01107` ; Crise = `01108` ; Amplification = `16054` (avion+) ; ressource wild des cartes Linked = `43034`
(étoile verte). Relevés : Bumbling Buffoons = Accélération ; Collision Course/Olé! = Accélération ; Toro!
Toro! = Aléa ; Get Your Swell On = Amplification ; Gone Berserk = Crise + Amplification + Aléa ; Welcome to
the Jungle = Accélération. (Les étoiles « ★ » imprimées après un ATQ/SCH/MNG ne sont pas encodables : le `desc`
porte le chiffre seul.)

## Fichiers moteur PARTAGÉS touchés (additifs, commentés `AJOUT`)

- `src/game/message/sender/sender.py` : `GettingVillain.by_effect` (paramètre optionnel) et NOUVEAU message
  `GettingVillainsToActivate`.
- `src/game/player/scenario.py` : `GetVillain(game_area, by_effect=None)`.
- `src/game/operate/worlds.py` : `FindVillain` passe `by_effect`.
- `src/game/operate/enemies.py` : `DoActivateAgainstYouInternal` active la liste rendue par
  `GettingVillainsToActivate` (sinon le vilain unique d'avant).
- `src/game/card/face/card_face.py` : traits ALERT, K.O., HOG, RHINO, ROWDY, TEMPER, ENRAGED, BESTIES,
  BERSERK, FERAL, SUNGLASSES, HELMET, STREETS, VELOCIRAPTOR, WARTHOG, RHINOCEROS ; compteur `knucklehead`.
- `tools/prefixes_fanmade.json` (`tk`), `tools/traits_fr_maison.json` + traits-fr générés,
  `ui-app/src/board/compteurs-fr.ts` (`knucklehead` = « andouille »), `ui-app/src/board/textes-fr-fanmade.ts`
  (40 entrées) + copie `public/js/traduction/*` régénérée, `public/js/prepare/mechants-info.js` (bios),
  `vilains-bios.md`, `data/cards.json` (pack `bebop_rocksteady`), `data/sets_info.json` (set 190).
- Outillage : `tools/cas/tmnt_bebop.py` (cas). `tools/autoplay.py` : version de la branche de sauvegarde conservée à la fusion (`--deck a+b`).

## Preuves

- **Cas `test_capacites`** : `tools/cas/tmnt_bebop.py`, 119 cas, tous verts (`[bebop]`). Batterie COMPLÈTE
  (fichiers moteur partagés touchés) : 4542/4551 ; les 9 échecs sont étrangers : 4 cas `sg0*` Squirrel Girl
  (rouges aussi sur la base `cff5cfaf`, vérifié dans un worktree propre) et 5 cas `fnefin` (chemin
  `campaign_log` Windows `/mnt/c/...` hérité du `launch.json`).
- **Substitution** (`tools/substituer_pack.py <game_dir> 20100 tk`) : 40/40 cartes ont au moins un cas rouge sans
  leur module (empreinte du pack identique avant/après). Les cas qui restent verts sous le stub sont des
  CONTRE-CAS d'absence (« pas de Réponse forcée sur la face K.O. », « rien ne se retourne si... », « Dodgy
  refusé », « sans jeton »), des mécaniques NATIVES lues dans `desc` (Hinder de tk018, Toughness de tk028,
  `ATK+` de tk007b, Crise de tk006b, Linked de tk101) ou la VICTOIRE (native sans tk006a, prouvée par le
  cas `tk006b`). La priorité de la carte Étourdi (tk001b, tk008b) est prouvée par MUTATION : rendre
  `EtourdiPrioritaire` faux fait rougir les deux cas (vu le 16/10/2026).
- **Gates** : `verifier_appels_modules.py` calibré (rouge sur `this.PlaceThreatOn` et `Faces.GetAll` inventés
  dans un `tk999.py` jetable, vert sur le pack) ; `test_cards.py` 6455 ok / 0 err ; `audit_cartes.py`,
  `verifier_api_cartes.py` : aucune ligne `bebop_rocksteady` ; `verifier_tous_les_decks.py` 145/145 ;
  `verifier_coherence_cartes.py` : aucune entrée du pack (sa couverture ne lit pas `tools/cas/*.py`).
- **Parties jouées** (`tools/autoplay.py`, profil équilibre, 8 parties, graines 1-8, journaux grepés
  `NameError|AttributeError|TypeError|KeyError|AssertionError|Traceback` = **0** partout) :
  solo spider_man : normal 0 V / 8 D (2,8-3,4 rounds), expert 0 V / 8 D ; solo black_panther : 0 V / 8 D ;
  2 joueurs (spider_man + black_panther) : normal 6 D + 2 « bloquée », expert 6 D + 2 « bloquée » ;
  2 joueurs inversés : 7 D + 1 « bloquée ». Témoin Rhino : solo 0 V / 8 D (6,9 rounds) ; 2 joueurs 6 D / 2
  « bloquée » sur 8 (le pilote, qui ne coordonne pas deux joueurs, se coince aussi sur le scénario officiel).
  Le scénario est brutal pour un héros de départ seul (2-3 rounds) : chaque dégât à un vilain pose un jeton
  Andouille qui lui donne +1 ATQ, par conception.
- **Plateau** : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts ; gate vue rouge par mutation du
  `bind_object_id` de Gone Berserk) ; `vitest` complet 3594/3597 (les 3 échecs : arts alternatifs de héros,
  images absentes de la copie de travail, étrangers au pack) ; `tsc --noEmit` vert.
- **Non prouvé** : une partie jouée par un humain dans le navigateur ; l'ordre des deux activations (Q8) ;
  les lectures Q1-Q7 ; le rendu des scans (icônes) autrement que par découpe ; l'exposition des quatre
  cartes `Linked` (Basic) dans le deck-builder, comme les cartes Linked officielles.

## Gabarits par carte (PROCESSUS-CARTE.md)

### tk001a : Bebop (Villain)

- [x] Étape 2 : carte(s) de référence : Interruption de début de phase : `nt011` (night_thrasher, `WhenVillainPhaseBegin`) ; choix « A ou B » du premier joueur : `27111` / `Otherwise` (RECETTES §2). Réponse forcée « après des dégâts » : `bw019` (`AfterUnitTookDamage`). `Special` résolu par une autre carte : `27100a` (Sinister Six, `ResolveSpecialAbility`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (3) : tk001a Bebop ALERT : debut de phase, sans compteur -> 1 menace sur le complot (et Rocksteady : 1 degat); tk001a Bebop ALERT : debut de phase avec compteurs -> retire 1 compteur (option par defaut), pas de menace; tk001a Bebop ALERT : le choix « menace » est possible meme avec des compteurs
      Substitution (`tools/substituer_pack.py`) : rouges 3/3
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk001b : Bebop (Villain)

- [x] Étape 2 : carte(s) de référence : Remplacement d'activation : `status/stunned.py` (`WhenEnemyWouldActivate` + `SetBeInstead`) ; retournement d'un vilain : `60112` Disturbed Psyche (`card.Flip`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (5) : tk001b Bebop K.O. : PAS de Reponse Forcee (le texte n'est imprime que sur la face ALERT); tk001b Bebop K.O. : activation = retire 1 compteur a la place (pas d'attaque), reste K.O. s'il en reste; tk001b Bebop K.O. : dernier compteur retire -> se retourne sur ALERT; tk001b Bebop K.O. : sans aucun compteur, l'activation le reveille aussi; tk001b Bebop K.O. ET etourdi : le statut passe d'abord (la carte Etourdi est retiree, les compteurs restent)
      Substitution (`tools/substituer_pack.py`) : rouges 3/5 ⚠ un cas reste vert sans module
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk002a : Bebop (Villain)

- [x] Étape 2 : carte(s) de référence : Interruption de début de phase : `nt011` (night_thrasher, `WhenVillainPhaseBegin`) ; choix « A ou B » du premier joueur : `27111` / `Otherwise` (RECETTES §2). Réponse forcée « après des dégâts » : `bw019` (`AfterUnitTookDamage`). `Special` résolu par une autre carte : `27100a` (Sinister Six, `ResolveSpecialAbility`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (1) : tk002a Bebop ALERT (expert) : 2 menaces sur le complot
      Substitution (`tools/substituer_pack.py`) : rouges 1/1
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk002b : Bebop (Villain)

- [x] Étape 2 : carte(s) de référence : Remplacement d'activation : `status/stunned.py` (`WhenEnemyWouldActivate` + `SetBeInstead`) ; retournement d'un vilain : `60112` Disturbed Psyche (`card.Flip`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (1) : tk002b Bebop K.O. (expert) : retire 2 compteurs
      Substitution (`tools/substituer_pack.py`) : rouges 1/1
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk003a : Rocksteady (Villain)

- [x] Étape 2 : carte(s) de référence : Interruption de début de phase : `nt011` (night_thrasher, `WhenVillainPhaseBegin`) ; choix « A ou B » du premier joueur : `27111` / `Otherwise` (RECETTES §2). Réponse forcée « après des dégâts » : `bw019` (`AfterUnitTookDamage`). `Special` résolu par une autre carte : `27100a` (Sinister Six, `ResolveSpecialAbility`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (4) : tk003a Rocksteady ALERT : debut de phase -> carte Robuste + 1 degat au premier joueur (aucun compteur); tk003a Rocksteady ALERT : avec un compteur Rhino Rage -> le retire (defaut), aucun degat; tk003a Rocksteady ALERT : apres 1 degat, Special de Rhino Rage = 1 compteur; tk003a Rocksteady ALERT : une Reponse par EVENEMENT de degats (2 evenements -> 2 compteurs)
      Substitution (`tools/substituer_pack.py`) : rouges 4/4
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk003b : Rocksteady (Villain)

- [x] Étape 2 : carte(s) de référence : Remplacement d'activation : `status/stunned.py` (`WhenEnemyWouldActivate` + `SetBeInstead`) ; retournement d'un vilain : `60112` Disturbed Psyche (`card.Flip`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (1) : tk003b Rocksteady K.O. : retire 1 compteur de Rhino Rage et reste K.O.
      Substitution (`tools/substituer_pack.py`) : rouges 1/1
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk004a : Rocksteady (Villain)

- [x] Étape 2 : carte(s) de référence : Interruption de début de phase : `nt011` (night_thrasher, `WhenVillainPhaseBegin`) ; choix « A ou B » du premier joueur : `27111` / `Otherwise` (RECETTES §2). Réponse forcée « après des dégâts » : `bw019` (`AfterUnitTookDamage`). `Special` résolu par une autre carte : `27100a` (Sinister Six, `ResolveSpecialAbility`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (1) : tk004a Rocksteady ALERT (expert) : 2 degats au premier joueur
      Substitution (`tools/substituer_pack.py`) : rouges 1/1
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk004b : Rocksteady (Villain)

- [x] Étape 2 : carte(s) de référence : Remplacement d'activation : `status/stunned.py` (`WhenEnemyWouldActivate` + `SetBeInstead`) ; retournement d'un vilain : `60112` Disturbed Psyche (`card.Flip`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (1) : tk004b Rocksteady K.O. (expert) : 2 compteurs d'un coup, 1 seul disponible -> se reveille
      Substitution (`tools/substituer_pack.py`) : rouges 1/1
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk005a : Demolition Crew (MainScheme)

- [x] Étape 2 : carte(s) de référence : Mise en place de vilains mis de côté : `27100a` (Sinister Synchronization, `skip_put_villain_into_play`) ; cartes de côté mises en jeu : `sp001a` (Spot).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (1) : tk005a mise en place : deux vilains, environnement, annexe, deux Temper accroches
      Substitution (`tools/substituer_pack.py`) : rouges 1/1
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. (rien de visible ajouté : jauge/menace/dégâts déjà couverts)

Carte terminée : OUI

### tk005b : Demolition Crew (MainScheme)

- [x] Étape 2 : carte(s) de référence : `sk145b` / `39002b` : `WhenMainSchemeStageWouldBeCompleted` + `SetBeInstead` + `RemoveThreatFromSchemes("All")` ; attaque « même en alter ego » : `DoAttackYou`.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (3) : tk005b Demolition Crew : menace atteinte -> remise a 0 a la place, et les DEUX vilains attaquent; tk005b Demolition Crew : en ALTER-EGO le joueur est quand meme ATTAQUE (pas de manigance); tk005b Demolition Crew : A DEUX joueurs, chacun est attaque par les deux vilains (3 chacun)
      Substitution (`tools/substituer_pack.py`) : rouges 3/3
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. (rien de visible ajouté : jauge/menace/dégâts déjà couverts)

Carte terminée : OUI

### tk006a : Destructive Dunderheads (Environment)

- [x] Étape 2 : carte(s) de référence : Plusieurs vilains : `27100a` (`AbilityFactory.GetVillain`) ; mise de côté d'un vilain vaincu : `SinisterSixWhenDefeated` (`27100`). Hooks moteur ajoutés : `GettingVillainsToActivate`, `GettingVillain.by_effect`.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (10) : tk006a Dunderheads (Double Trouble) : les DEUX vilains s'activent contre le joueur (phase du mechant); tk006a Dunderheads : a DEUX joueurs, chaque vilain s'active contre CHAQUE joueur (+2 sur le premier joueur par rapport au BASELINE); tk006a Dunderheads : « the villain » -> le joueur choisit UN vilain (overkill sur un sbire : 4 degats a celui choisi); tk006a Dunderheads : Bebop vaincu -> lui et son Temper sont MIS DE COTE, Rocksteady reste ALERT et Gone Berserk l'equipe; tk006a Dunderheads : Bebop vaincu alors que Rocksteady est K.O. -> Rocksteady repasse ALERT; tk006a Dunderheads : Rocksteady vaincu -> Bebop (ALERT, +12 PV) et son Temper restent ...
      Substitution (`tools/substituer_pack.py`) : rouges 6/10 ⚠ un cas reste vert sans module
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk006b : Gone Berserk! (Attachment)

- [x] Étape 2 : carte(s) de référence : `32147` Magneto's Helmet (`UnitCannotBeConfused`) ; `27103` (`GiveKeywordToAttached(Villain, ...)`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (7) : tk006b Gone Berserk : +12 PV PAR joueur (2 joueurs : Rocksteady 17x2 + 12x2 = 58); tk006b Gone Berserk : le vilain ne peut plus etre desoriente; tk006b Gone Berserk : contre-cas, SANS Gone Berserk Rocksteady se laisse desorienter; tk006b Gone Berserk : Crise -> on ne peut plus retirer de menace du complot principal (3 -> 3); tk006b Gone Berserk : CONTRE-CAS sans Gone Berserk le complot peut etre contre (3 -> 2); tk006b Gone Berserk : le DERNIER vilain vaincu fait GAGNER les joueurs (le premier est de cote, le moteur ne le verrait pas) ...
      Substitution (`tools/substituer_pack.py`) : rouges 4/7 ⚠ un cas reste vert sans module
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk007a : Hog Wild (Attachment)

- [x] Étape 2 : carte(s) de référence : `bw015` (`GiveKeywordToAttached(get_new_value, ex_change_on_event=OnEvent.Counter)`) ; retournement d'un attachement : `ip002a` ; `27100b`/`WhenResolveSpecialAbility`.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (4) : tk007a Hog Wild : +1 ATK a Bebop par compteur knucklehead (2 compteurs -> ATK 2); tk007a Hog Wild : sans compteur, ATK 0 (ligne de base); tk007a Hog Wild : Special = 1 compteur (apres 1 degat sur Bebop); tk007a Hog Wild : a 3 compteurs il se retourne sur Headfirst (ENRAGED, +3 ATK, trait ENRAGED au vilain)
      Substitution (`tools/substituer_pack.py`) : rouges 3/4 ⚠ un cas reste vert sans module
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk007b : Headfirst (Attachment)

- [x] Étape 2 : carte(s) de référence : `bw015` (`GiveKeywordToAttached(get_new_value, ex_change_on_event=OnEvent.Counter)`) ; retournement d'un attachement : `ip002a` ; `27100b`/`WhenResolveSpecialAbility`.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (4) : tk007b Headfirst : Special = 1 degat a l'identite (apres 1 degat sur Bebop), AUCUN compteur de plus; tk007b Headfirst : +3 ATK a Bebop SEUL (Rocksteady ENRAGED absent) : Bebop attaque pour 3, rien ne se retourne; tk007b Headfirst : Bebop ENRAGED + Headstrong en jeu -> quand Bebop devrait s'activer, les deux vilains passent K.O., les deux Temper ROWDY; tk007b Headfirst : l'activation qui declenche le retournement est une activation K.O. (1 compteur retire a Hog Wild)
      Substitution (`tools/substituer_pack.py`) : rouges 3/4 ⚠ un cas reste vert sans module
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk008a : Rhino Rage (Attachment)

- [x] Étape 2 : carte(s) de référence : `bw015` (`GiveKeywordToAttached(get_new_value, ex_change_on_event=OnEvent.Counter)`) ; retournement d'un attachement : `ip002a` ; `27100b`/`WhenResolveSpecialAbility`.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (4) : tk008a Rhino Rage : s'accroche a Rocksteady (et PAS a Bebop); tk008a Rhino Rage : +1 ATQ a Rocksteady par jeton Andouille (2 jetons -> ATQ 1 + 2 = 3); tk008a Rhino Rage : sans jeton, ATQ de base (1); tk008a Rhino Rage : a 3 jetons, se retourne sur Headstrong (ENRAGED, +3 ATQ) : ATQ 1 + 3 = 4
      Substitution (`tools/substituer_pack.py`) : rouges 3/4 ⚠ un cas reste vert sans module
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk008b : Headstrong (Attachment)

- [x] Étape 2 : carte(s) de référence : `bw015` (`GiveKeywordToAttached(get_new_value, ex_change_on_event=OnEvent.Counter)`) ; retournement d'un attachement : `ip002a` ; `27100b`/`WhenResolveSpecialAbility`.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (3) : tk008b Headstrong : Special = 1 menace sur le complot (apres 1 degat sur Rocksteady); tk008b Headstrong : Rocksteady ENRAGED s'active, Headfirst en jeu -> les deux vilains passent K.O.; tk008b Headstrong : Rocksteady ETOURDI et ENRAGED : la carte Etourdi passe d'abord, rien ne se retourne
      Substitution (`tools/substituer_pack.py`) : rouges 2/3 ⚠ un cas reste vert sans module
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk009 : Shutter Shades (Attachment)

- [x] Étape 2 : carte(s) de référence : `01119` Solid-Sound Body, `04029` (attache au vilain) ; `AttachToFaceWhenPutIntoPlay(if_cannot_gain_surge)` ; `AfterCardFlip` brute.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (4) : tk009 Shutter Shades : revelee, Bebop ALERT -> s'attache a Bebop, Bebop STEADY, 1 compteur sur Hog Wild; tk009 Shutter Shades : Bebop K.O. -> NE S'ATTACHE PAS (la carte gagne Renfort), le When Revealed place quand meme son compteur; tk009 Shutter Shades : apres que Bebop passe K.O., la carte (ATTACHEE) est defaussee; tk009 Shutter Shades : Steady -> il faut DEUX etourdissements pour etre etourdi (1 carte ne suffit pas)
      Substitution (`tools/substituer_pack.py`) : rouges 4/4
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk010 : Aviator Cap (Attachment)

- [x] Étape 2 : carte(s) de référence : `01119` Solid-Sound Body, `04029` (attache au vilain) ; `AttachToFaceWhenPutIntoPlay(if_cannot_gain_surge)` ; `AfterCardFlip` brute.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (3) : tk010 Aviator Cap : revelee, Rocksteady ALERT -> s'attache, STEADY, 1 compteur sur Rhino Rage; tk010 Aviator Cap : Rocksteady passe K.O. -> la carte (ATTACHEE) est defaussee; tk010 Aviator Cap : Rocksteady K.O. -> pas d'attache, la carte gagne Renfort (la carte suivante est revelee)
      Substitution (`tools/substituer_pack.py`) : rouges 3/3
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk011 : Roberta (Attachment)

- [x] Étape 2 : carte(s) de référence : `01119` Solid-Sound Body, `04029` (attache au vilain) ; `AttachToFaceWhenPutIntoPlay(if_cannot_gain_surge)` ; `AfterCardFlip` brute.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (3) : tk011 Roberta : l'attaque de Bebop est PERCANTE (la carte Robuste saute ET les degats passent); tk011 Roberta : CONTRE-CAS sans Roberta, la carte Robuste absorbe l'attaque; tk011 Roberta : Bebop passe K.O. -> Roberta (ATTACHEE) defaussee
      Substitution (`tools/substituer_pack.py`) : rouges 2/3 ⚠ un cas reste vert sans module
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk012 : Juniper (Attachment)

- [x] Étape 2 : carte(s) de référence : `01119` Solid-Sound Body, `04029` (attache au vilain) ; `AttachToFaceWhenPutIntoPlay(if_cannot_gain_surge)` ; `AfterCardFlip` brute.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (3) : tk012 Juniper : l'attaque de Rocksteady a OVERKILL (1 degat d'exces sur l'allie va a l'identite); tk012 Juniper : CONTRE-CAS sans Juniper, l'exces est perdu; tk012 Juniper : Rocksteady passe K.O. -> Juniper (ATTACHEE) defaussee
      Substitution (`tools/substituer_pack.py`) : rouges 2/3 ⚠ un cas reste vert sans module
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk013 : Bumbling Buffoons (SideScheme)

- [x] Étape 2 : carte(s) de référence : Assault (`has_assault.py`) pour Dodgy ; `22031` (`DoAttackYou`) et `60004` (redirection de dégâts, `WhenUnitWouldTakeDamage` temporaire) ; `Briefing Room ag007` pour le déclencheur de révélation.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (3) : tk013 Bumbling Buffoons : Dodgy accepte (DEF 3 au lieu de THW 1) : 4 -> 1; tk013 Bumbling Buffoons : vaincue -> l'ennemi choisi t'attaque (Bebop ATK 2 -> 2 degats), sans redirection; tk013 Bumbling Buffoons : vaincue, redirection ACCEPTEE -> les degats de l'attaque vont a un AUTRE ennemi
      Substitution (`tools/substituer_pack.py`) : rouges 3/3
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. (rien de visible ajouté : jauge/menace/dégâts déjà couverts)

Carte terminée : OUI

### tk014 : Bumbling Buffoons (SideScheme)

- [x] Étape 2 : carte(s) de référence : Assault (`has_assault.py`) pour Dodgy ; `22031` (`DoAttackYou`) et `60004` (redirection de dégâts, `WhenUnitWouldTakeDamage` temporaire) ; `Briefing Room ag007` pour le déclencheur de révélation.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (1) : tk014 Bumbling Buffoons (illustration 2/3) : meme Dodgy
      Substitution (`tools/substituer_pack.py`) : rouges 1/1
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. (rien de visible ajouté : jauge/menace/dégâts déjà couverts)

Carte terminée : OUI

### tk015 : Bumbling Buffoons (SideScheme)

- [x] Étape 2 : carte(s) de référence : Assault (`has_assault.py`) pour Dodgy ; `22031` (`DoAttackYou`) et `60004` (redirection de dégâts, `WhenUnitWouldTakeDamage` temporaire) ; `Briefing Room ag007` pour le déclencheur de révélation.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (1) : tk015 Bumbling Buffoons (illustration 3/3) : meme Dodgy
      Substitution (`tools/substituer_pack.py`) : rouges 1/1
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. (rien de visible ajouté : jauge/menace/dégâts déjà couverts)

Carte terminée : OUI

### tk016 : Collision Course (SideScheme)

- [x] Étape 2 : carte(s) de référence : `60004`/`27103` (`WhenSchemeBeDefeated`, `Faces.GiveStatus`) ; Dodgy : voir tk013.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (2) : tk016 Collision Course : revelee -> 1 compteur sur CHAQUE Temper; tk016 Collision Course : vaincue -> chaque vilain est ETOURDI
      Substitution (`tools/substituer_pack.py`) : rouges 2/2
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. (rien de visible ajouté : jauge/menace/dégâts déjà couverts)

Carte terminée : OUI

### tk018 : Olé! (SideScheme)

- [x] Étape 2 : carte(s) de référence : `60004`/`27103` (`WhenSchemeBeDefeated`, `Faces.GiveStatus`) ; Dodgy : voir tk013.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (5) : tk018 Ole! : Hinder 1 par joueur (menace de depart 2 + 1 = 3, solo); tk018 Ole! : Hinder 1 par joueur a DEUX joueurs (2 + 2 = 4); tk018 Ole! : vaincue -> 2 degats PAR joueur a chaque vilain ; seul le vilain ENRAGED blesse est etourdi; tk018 Ole! : a DEUX joueurs, 4 degats a chaque vilain; tk018 Ole! : les degats aux deux vilains se resolvent UN PAR UN : Bebop (1 PV) meurt, Gone Berserk donne +12 PV a Rocksteady (1 PV) qui survit
      Substitution (`tools/substituer_pack.py`) : rouges 3/5 ⚠ un cas reste vert sans module
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. (rien de visible ajouté : jauge/menace/dégâts déjà couverts)

Carte terminée : OUI

### tk020 : Toro! Toro! (SideScheme)

- [x] Étape 2 : carte(s) de référence : `60004`/`27103` (`WhenSchemeBeDefeated`, `Faces.GiveStatus`) ; Dodgy : voir tk013.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (3) : tk020 Toro! Toro! : Dodgy ACCEPTE -> le heros manigance avec sa DEF (3) au lieu de sa THW (1) : 4 -> 1; tk020 Toro! Toro! : Dodgy REFUSE (facultatif) -> THW 1 : 4 -> 3; tk020 Toro! Toro! : vaincue -> 2 compteurs sur un Temper
      Substitution (`tools/substituer_pack.py`) : rouges 2/3 ⚠ un cas reste vert sans module
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. (rien de visible ajouté : jauge/menace/dégâts déjà couverts)

Carte terminée : OUI

### tk022 : Lay the Beatdown (Treachery)

- [x] Étape 2 : carte(s) de référence : `01122` Klaw's Vengeance (When Revealed alter ego / hero), `ChooseAbilities` + `ForChoiceAbility(condition=...)` (option impossible non offerte), `27109` (`DiscardControlCards(highest_cost=True)`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (4) : tk022 Lay the Beatdown (ALTER-EGO) : l'identite est DESORIENTEE; tk022 Lay the Beatdown (HEROS) : par defaut 2 degats indirects au heros; tk022 Lay the Beatdown (HEROS) : l'autre option etourdit le heros (et ne blesse pas); tk022 Lay the Beatdown : en HEROS, rien ne desoriente (contre-cas de la branche alter-ego)
      Substitution (`tools/substituer_pack.py`) : rouges 3/4 ⚠ un cas reste vert sans module
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. (rien de visible ajouté : jauge/menace/dégâts déjà couverts)

Carte terminée : OUI

### tk024 : Pummel (Treachery)

- [x] Étape 2 : carte(s) de référence : `01122` Klaw's Vengeance (When Revealed alter ego / hero), `ChooseAbilities` + `ForChoiceAbility(condition=...)` (option impossible non offerte), `27109` (`DiscardControlCards(highest_cost=True)`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (3) : tk024 Pummel : par defaut, degats egaux a l'ATK d'un vilain (Bebop ATK 2 -> 2); tk024 Pummel : l'autre option defausse la carte de plus haut cout (Helicarrier 3 > Aunt May 1); tk024 Pummel : sans amelioration ni soutien, l'option defausse n'est PAS offerte (la premiere reste)
      Substitution (`tools/substituer_pack.py`) : rouges 3/3
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. (rien de visible ajouté : jauge/menace/dégâts déjà couverts)

Carte terminée : OUI

### tk026 : Trample (Treachery)

- [x] Étape 2 : carte(s) de référence : `01122` Klaw's Vengeance (When Revealed alter ego / hero), `ChooseAbilities` + `ForChoiceAbility(condition=...)` (option impossible non offerte), `27109` (`DiscardControlCards(highest_cost=True)`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (4) : tk026 Trample (ALTER-EGO) : defausse 1 carte de la main; tk026 Trample (HEROS) : un vilain attaque le personnage ami aux PV restants les plus bas (allie a 3 PV, pas l'identite a 10); tk026 Trample (HEROS) : sans allie, c'est l'identite qui est visee; tk026 Trample : « [star] Boost: Deal 1 damage to an ally you control »
      Substitution (`tools/substituer_pack.py`) : rouges 4/4
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. (rien de visible ajouté : jauge/menace/dégâts déjà couverts)

Carte terminée : OUI

### tk028 : Anchovy (Minion)

- [x] Étape 2 : carte(s) de référence : `32167` Bastion (boost : se donner la carte face cachée), `45076` (`message.AfterThisActivation`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (3) : tk028 Anchovy : entre en jeu avec une carte Robuste (Toughness); tk028 Anchovy : vaincu -> REMELANGE dans le deck rencontre (apres sa carte Robuste); tk028 Anchovy : « [star] Boost: After this activation resolves, deal this card to the first player as a facedown encounter card »
      Substitution (`tools/substituer_pack.py`) : rouges 2/3 ⚠ un cas reste vert sans module
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. (rien de visible ajouté : jauge/menace/dégâts déjà couverts)

Carte terminée : OUI

### tk101 : Welcome to the Jungle (SideScheme)

- [x] Étape 2 : carte(s) de référence : `43021` Specialized Training / `49020` New Recruits : « When Defeated » + cartes mises de côté (`Linked`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (3) : tk101 Welcome to the Jungle : vaincue -> le joueur met en jeu UNE carte NYC mise de cote (Eastman Theater choisi); tk101 Welcome to the Jungle : A DEUX joueurs, CHAQUE joueur en choisit une (deux cartes en jeu); tk101 Welcome to the Jungle : Linked -> les 4 cartes sont de cote (ni en jeu ni dans un deck) au depart
      Substitution (`tools/substituer_pack.py`) : rouges 2/3 ⚠ un cas reste vert sans module
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk102 : Road to Ruin (SideScheme)

- [x] Étape 2 : carte(s) de référence : `01122` Klaw's Vengeance (When Revealed alter ego / hero), `ChooseAbilities` + `ForChoiceAbility(condition=...)` (option impossible non offerte), `27109` (`DiscardControlCards(highest_cost=True)`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (4) : tk102 Road to Ruin (ALTER-EGO) : sans LOCATION, aucune option -> rien (pas de « Stun your hero » hors forme heros); tk102 Road to Ruin (HEROS) : sans LOCATION, le heros est etourdi; tk102 Road to Ruin (HEROS) : avec une LOCATION, la premiere option la defausse; tk102 Road to Ruin : vaincue -> etourdit un ennemi
      Substitution (`tools/substituer_pack.py`) : rouges 3/4 ⚠ un cas reste vert sans module
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. (rien de visible ajouté : jauge/menace/dégâts déjà couverts)

Carte terminée : OUI

### tk104 : Fallen Empires (Treachery)

- [x] Étape 2 : carte(s) de référence : `01122` Klaw's Vengeance (When Revealed alter ego / hero), `ChooseAbilities` + `ForChoiceAbility(condition=...)` (option impossible non offerte), `27109` (`DiscardControlCards(highest_cost=True)`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (3) : tk104 Fallen Empires : sans LOCATION, defausse 1 carte de la main; tk104 Fallen Empires : avec une LOCATION, la defausse par defaut; tk104 Fallen Empires : « [star] Boost: Discard 1 card from your hand »
      Substitution (`tools/substituer_pack.py`) : rouges 3/3
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. (rien de visible ajouté : jauge/menace/dégâts déjà couverts)

Carte terminée : OUI

### tk106 : Channel 6 News (Support)

- [x] Étape 2 : carte(s) de référence : `ag007` Briefing Room (`AfterPlayerRevealCard`, `Exhaust`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (2) : tk106 Channel 6 News : apres la revelation d'une manigance annexe NYC, s'epuise -> retire 2 menaces (4 -> 2); tk106 Channel 6 News : une manigance annexe SANS le trait NYC ne declenche rien
      Substitution (`tools/substituer_pack.py`) : rouges 1/2 ⚠ un cas reste vert sans module
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk107 : Eastman Theater (Support)

- [x] Étape 2 : carte(s) de référence : `sk279` (`AfterSchemeBeDefeated(HeroResponse).SetCostFunc(Exhaust)`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (1) : tk107 Eastman Theater : apres la defaite d'une manigance annexe NYC, s'epuise -> redresse un heros ami
      Substitution (`tools/substituer_pack.py`) : rouges 1/1
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk108 : Powder Keg (PlayerSideScheme)

- [x] Étape 2 : carte(s) de référence : `ip002a` (drapeau `not_count_player_side_scheme_limit` à l'entrée en jeu).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (2) : tk108 Powder Keg : vaincue -> 2 degats a chaque ennemi, 4 si l'ennemi est etourdi ou desoriente; tk108 Powder Keg : ne compte PAS dans la limite de manigances joueur (drapeau pose a l'entree en jeu)
      Substitution (`tools/substituer_pack.py`) : rouges 2/2
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk109 : Power Play (PlayerSideScheme)

- [x] Étape 2 : carte(s) de référence : `ag007` Briefing Room (`AfterPlayerRevealCard`, `Exhaust`). Retrait « par vous » : `AfterSchemeRemoveThreat` + condition sur l'initiateur.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (4) : tk109 Power Play : apres avoir retire de la menace, defausse 1 carte -> retire 2 menaces de plus (6 -1 -2 = 3); tk109 Power Play : sans carte a defausser, la Reponse est impayable (6 - 1 = 5); tk109 Power Play : la Reponse se REPETE tant qu'on retire de la menace et qu'on a des cartes (3 cartes : 6 -1 -2 -2 -2 -> 0, vaincue); tk109 Power Play : vaincue -> le joueur peut etourdir ET desorienter un ennemi
      Substitution (`tools/substituer_pack.py`) : rouges 3/4 ⚠ un cas reste vert sans module
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. cas plateau : `ui-app/src/board/tmnt-bebop-plateau.test.ts` (14 cas verts, gate vue rouge par mutation)

Carte terminée : OUI

### tk201 : Hittin' the Town (Treachery)

- [x] Étape 2 : carte(s) de référence : `sk145b` (`DiscardEncounterCardsUntil` + `Reveal`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (2) : tk201 Hittin' the Town : defausse du deck rencontre jusqu'a une manigance annexe ou un attachement, et la REVELE; tk201 Hittin' the Town : rien a trouver (ni attachement ni manigance annexe) -> ne boucle pas
      Substitution (`tools/substituer_pack.py`) : rouges 1/2 ⚠ un cas reste vert sans module
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. (rien de visible ajouté : jauge/menace/dégâts déjà couverts)

Carte terminée : OUI

### tk203 : Jägerbombs (Treachery)

- [x] Étape 2 : carte(s) de référence : `01122` Klaw's Vengeance (When Revealed alter ego / hero), `ChooseAbilities` + `ForChoiceAbility(condition=...)` (option impossible non offerte), `27109` (`DiscardControlCards(highest_cost=True)`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (2) : tk203 Jagerbombs : par defaut, etourdit l'identite; tk203 Jagerbombs : l'autre option desoriente l'identite
      Substitution (`tools/substituer_pack.py`) : rouges 2/2
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. (rien de visible ajouté : jauge/menace/dégâts déjà couverts)

Carte terminée : OUI

### tk205 : Get Your Swell On (SideScheme)

- [x] Étape 2 : carte(s) de référence : `01122` Klaw's Vengeance (When Revealed alter ego / hero), `ChooseAbilities` + `ForChoiceAbility(condition=...)` (option impossible non offerte), `27109` (`DiscardControlCards(highest_cost=True)`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : each / either / instead / unless / if (alert/K.O.) / « the villain » / « you » / « your identity » / « may » / « first player » / before-after (Interruption vs Réponse). Résultat : voir `.planning/tmnt/bebop-questions.md` pour les lectures non tranchées (Q1-Q8) ; le reste est littéral.
- [x] Étape 6 : nombres texte ↔ code : valeurs `desc` relevées sur le scan (PV, ATQ, SCH, coût, menace, icônes de boost) ; contrôlées par les cas. Résultat : conforme.
- [x] Étape 7 : cas `test_capacites` sujets (1) : tk205 Get Your Swell On : soigne 1 degat a chaque ennemi ET leur donne une carte Robuste
      Substitution (`tools/substituer_pack.py`) : rouges 1/1
- [x] Étape 7 bis : limite imprimée ? NON (aucun « Limit » imprimé)
- [x] Étape 8 : autoplay ciblé : solo et 2 joueurs, normal et expert : voir bilan ci-dessous ; témoin Rhino, grep tracebacks : 0.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. (rien de visible ajouté : jauge/menace/dégâts déjà couverts)

Carte terminée : OUI
