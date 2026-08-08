# Mode campagne — conception

État au 07/08/2026. Chantier ouvert parce que le mode Campagne existant était
inutilisable : l'écran s'affichait écrasé et l'enchaînement entre scénarios
reposait entièrement sur une saisie manuelle.

## Ce qui marchait déjà (à ne pas refaire)

Le MOTEUR est bon. Vérifié à blanc sur les 5 scénarios de *The Rise of Red
Skull*, standard et expert : `mode_campaign` s'active, les améliorations du
journal arrivent en jeu, les alliés secourus retournent au deck, les pions
retard posent la menace de départ (×nb joueurs en expert), les obligations de
campagne experte sont ajoutées. Voir `src/cards/pack/trors/campaign.py` et
`src/game/ability/factory/campaign.py`.

Le contrat moteur est le dict `campaign_log` : des clés texte lues par
`CampaignLog.Get*` (`src/game/operate/campaign_logs.py`). Tout ce chantier
consiste à REMPLIR ce dict correctement et automatiquement, pas à le remplacer.

## Ce qui était cassé

1. **Mise en page.** `renderCampaignPath()` injectait ses quatre blocs comme
   enfants de `#scn-grid`, une grille de vignettes en 4 colonnes de 205 px
   plafonnée à `56vh`. Résultat mesuré : quatre colonnes de 205 px pour des
   blocs de ~1070 px, et le scan du livret réduit à une vignette de 175 px.
2. **Progression fausse.** `markCampaignDone()` était appelé dans `doLaunch()` :
   cliquer « Lancer » cochait le scénario, même en cas de défaite. Le livret dit
   l'inverse (perdre = rejouer sans pénalité).
3. **Carnet 100 % manuel.** Rien ne reportait le résultat d'une partie.
4. **Mauvaises cartes.** Le champ « Armes expérimentales » proposait
   04155–04158 — les *upgrades TECH*, cartes joueur du set Hydra Campaign. Les
   vrais attachements EXPERIMENTAL sont 04072 Laser Rifle, 04073 Energy Shield,
   04074 Power Gauntlets, 04075 Exo-Suit.
5. **PV persistants absents.** Le schéma `trors` n'avait pas de champ
   « Remaining hit points », alors que le moteur sait le consommer et que la
   campagne experte en dépend.

## Décisions

Prises avec l'auteur du jeu le 07/08/2026, après lecture des scans du livret.

| Sujet | Décision |
|---|---|
| Écran | Un seul scénario, plein écran. Aucune liste de méchants. |
| Réglages | Tout imposé : sets modulaires du livret, difficulté fixée à la création. |
| Équipe | Nombre de joueurs et héros figés. Deck modifiable entre scénarios. |
| Histoire | BD d'intro en grand, page de règles à côté, épilogue à la victoire. |
| Récompenses | Panneau sur le PLATEAU, à la victoire. |
| Carnet | Pré-rempli par le moteur, chaque case reste corrigeable. |
| Défaite | Rien n'est enregistré. On rejoue. |
| Expert | Complet : PV persistants, obligations numérotées 1-4, joueur vaincu. |
| Sauvegarde | Campagne nommée, côté serveur, plusieurs en parallèle. |
| Partie en cours | Rattachée à la campagne, reprise là où on s'est arrêté. |
| Fin de campagne | Écran de conclusion + récapitulatif + haut fait. |
| Langue | Scans anglais (le livret FR n'existe qu'en papier) + résumé français rédigé pour le jeu. Les CARTES s'affichent en français : `assets/pics-fr/` couvre les 181 cartes de la boîte. |
| Portée | Rise of Red Skull d'abord, structure générique pour les 6 autres boîtes. |

## Le livret, scénario par scénario

Source : les scans dans `public/stories/trors/` (livret officiel MC10).

### Règles générales (p3)
- Gagner les 5 scénarios **dans l'ordre**.
- **Identité figée** pour toute la campagne ; aspect et contenu du deck libres.
- Perdre : rejouer **sans pénalité**.
- Les cartes ajoutées au deck y restent, et ne comptent pas dans la taille
  minimale/maximale du deck.
- Cartes 155–162 : réservées à la campagne.

### Sc.1 Crossbones
- Sets : Crossbones, Experimental Weapons, Hydra Assault, Weapon Master,
  Legions of Hydra, Standard.
- Setup : chaque joueur note son identité (elle ne changera plus).
- Victoire : chaque joueur choisit une amélioration **TECH** (04155–04158) et
  l'ajoute à son deck ; on note chaque attachement **EXPERIMENTAL** entré en
  jeu (04072–04075).

### Sc.2 Absorbing Man
- Sets : Absorbing Man, Hydra Patrol, Standard.
- Setup : cartes `setup` mises en jeu ; attachements EXPERIMENTAL notés
  remélangés dans le deck de rencontre.
- Victoire : noter les **pions retard** sur la manigance principale ; chaque
  joueur peut choisir une amélioration **Basic Condition** (04159a–04162a),
  l'attacher à son identité et l'ajouter à son deck.

### Sc.3 Taskmaster
- Sets : Taskmaster, Hydra Patrol, Weapon Master, Standard. Hydra Patrol requis.
- Victoire : chaque joueur ayant secouru des alliés du set Taskmaster
  (04097–04100) les ajoute à son deck et note leur nom.

### Sc.4 Zola
- Sets : Zola, Under Attack, Standard.
- Victoire : noter chaque joueur **engagé** avec un ennemi.
- Victoire : si **Hydra Prison** est encore en jeu, les alliés placés dessous
  sont **retirés de la campagne** (interdits dans tout deck jusqu'à la fin).
- Victoire : si Hydra Prison n'est PAS en jeu, chaque joueur en forme héros
  peut remplacer son amélioration Basic par sa face **Improved** (04159b–04162b).

### Sc.5 Red Skull
- Sets : Red Skull, Hydra Assault, Hydra Patrol, Standard.
- Setup : X menace sur la manigance principale, X = pions retard notés
  (X par joueur en expert).
- Expert : joueurs notés engagés se distribuent une carte de rencontre ;
  **perdre ce scénario en expert perd la campagne**.
- Victoire : Hydra est vaincue, la campagne est gagnée.

### Campagne experte (p17)
- Quatre sets d'obligations numérotés 1-4, contenant les mêmes quatre cartes
  (04163 Zola's Algorithm, 04164 Medical Emergency, 04165 Martial Law,
  04166 Anti-Hero Propaganda). Chaque joueur reçoit un numéro à la création de
  la campagne et pioche TOUJOURS dans le set correspondant.
- **PV persistants** : les PV restants après une victoire deviennent les PV de
  départ du scénario suivant. Si les PV restants dépassent les PV de base, on
  note les PV de base.
- Un joueur vaincu pendant un scénario que ses coéquipiers gagnent ne participe
  à AUCUNE étape de victoire, mais revient au scénario suivant en ajoutant une
  obligation à son deck pour retrouver tous ses PV.

## Correspondance des scans

Les fichiers sont renommés par rôle. Deux planches servent d'épilogue d'un
scénario ET d'intro du suivant (p6, p11) : elles ne sont pas dupliquées, c'est
`data/campagnes/trors.json` qui dit quelles pages chaque scénario affiche.

| Livret | Ancien nom | Nouveau nom |
|---|---|---|
| p2 | `crossbones_1` | `00-campagne-regles-1.jpg` |
| p3 | `crossbones_2` | `00-campagne-regles-2.jpg` |
| p4 | `crossbones_3` | `01-crossbones-intro-1.jpg` |
| p5 | `crossbones_4` | `01-crossbones-regles-1.jpg` |
| p6 | `crossbones_5` | `01-crossbones-epilogue-1.jpg` |
| p7 | `absorbing_man_1` | `02-absorbing_man-regles-1.jpg` |
| p8 | `absorbing_man_2` | `02-absorbing_man-epilogue-1.jpg` |
| p9 | `absorbing_man_3` | `03-taskmaster-intro-1.jpg` |
| p10 | `taskmaster_1` | `03-taskmaster-regles-1.jpg` |
| p11 | `taskmaster_2` | `03-taskmaster-epilogue-1.jpg` |
| p12 | `zola_1` (`taskmaster_3` en doublon) | `04-zola-regles-1.jpg` |
| p13 | `zola_2` | `04-zola-epilogue-1.jpg` |
| p14 | `zola_3` | `05-red_skull-intro-1.jpg` |
| p15 | `red_skull_1` | `05-red_skull-regles-1.jpg` |
| p16 | `red_skull_2` | `05-red_skull-epilogue-1.jpg` |
| p17 | `red_skull_3` | `00-campagne-expert-1.jpg` |

Pages absentes des scans : la page du carnet de campagne (4e de couverture) —
sans objet, le carnet est tenu par le jeu.

## Avancement

### Livré (07/08/2026)

* `data/campagnes/trors.json` — la campagne décrite en données : ordre des
  scénarios, résumés français, enjeux, pages du livret par rôle, champs de
  victoire (type `auto` avec son détecteur, ou `choix` avec ses options).
* `src/engine/device/web/server/server_campagne.py` — six routes :
  `/list_campagnes_definies`, `/get_campagne_definition`, `/list_campagnes`,
  `/get_campagne`, `/save_campagne`, `/delete_campagne`. Les campagnes du
  joueur sont écrites dans `campagnes/`, à côté de `replays/`, donc hors de
  `.game` que le lanceur reconstruit à chaque démarrage.
* `public/campagne.html` + `public/js/campagne/` + `public/css/campagne/` —
  l'écran dédié : liste des campagnes, création, et LE scénario courant plein
  écran. Mesuré après coup sur un écran de 1500 px : récit 951 px, fiche de
  mission 458 px, planche de BD rendue à 951 px (contre 175 px avant), aucun
  débordement horizontal, aucune hauteur plafonnée.
* L'équipe est choisie par l'écran de préparation, en mode réduit
  (`/prepare.html?campagne`) : deux étapes, mode et nombre de héros annoncés et
  non modifiables, bouton « Valider l'équipe » au lieu de « Lancer la partie ».
  Le passage se fait par un brouillon en `localStorage`, effacé dès que la
  campagne est enregistrée.
* La tuile « Campagne » de l'écran de préparation redirige vers
  `/campagne.html`. Tout l'ancien code de campagne de `public/js/prepare/app.js`
  est donc devenu inatteignable — il est CONSERVÉ le temps de porter les
  schémas de récompenses des six autres boîtes (voir le commentaire posé sur
  `CAMPAIGN_SCHEMAS`).

Vérifié de bout en bout : création → équipe → scénario 1 → descripteur envoyé
au moteur (`mode_campaign`, les cinq sets du livret, les deux identités
résolues, `campaign_log` vide au scénario 1) → reprise du scénario en cours →
abandon et remise à zéro de la partie en cours. Le parcours normal du wizard
(hors campagne) est inchangé : cinq étapes, quatre modes, « Lancer la partie ».

### Livré (07/08/2026, second temps) — le panneau de récompenses

* `ui-app/src/board/campagne/detecteurs.ts` — six détecteurs GÉNÉRIQUES, plus
  une condition, décrits en données dans `trors.json` : `cartes_en_jeu`,
  `compteur_manigance`, `cartes_du_joueur`, `joueurs_engages`,
  `cartes_sous_complot`, `pv_restants`, et la condition `complot_absent`.
  Aucun n'encode Rise of Red Skull : les identifiants de cartes et de compteurs
  viennent du fichier de campagne.
* `ui-app/src/board/campagne/contexte.ts` — le plateau apprend qu'il joue une
  campagne par une clé `localStorage` (`mc-campagne-partie`) posée juste avant
  le lancement, et effacée à la validation. `launcher.js` la retire pour toute
  partie ordinaire, sinon une victoire hors campagne serait rattachée au
  dernier scénario joué.
* `ui-app/src/board/campagne/PanneauRecompenses.tsx` — s'ouvre dans l'écran de
  fin de partie, à la victoire seulement. Les relevés du moteur sont
  pré-cochés et marqués « relevé par le jeu », mais restent modifiables ; les
  vrais choix du livret s'affichent en CARTES (scans français, via `scanUrl`).
  Un choix obligatoire non fait bloque le bouton et dit lequel manque. Un héros
  éliminé est écarté des récompenses, comme le veut la p17.
* 33 tests sur les détecteurs, bâtis sur des descripteurs CAPTURÉS en montant
  les scénarios à blanc (sonde `ToDescriptor.World`).

#### Vérifié en jouant

Campagne créée, scénario 1 (Crossbones) joué jusqu'à la victoire, récompenses
validées, scénario 2 lancé. Constaté dans le monde du scénario 2 :

* Energy Shield (04073), la seule arme expérimentale entrée en jeu au scénario
  1, est dans le **deck de rencontre** ;
* Tactical Scanner (04156), l'amélioration choisie à la fin du scénario 1, est
  **en jeu sur le héros**.

La boucle complète tient donc : jouer → relever → valider → hériter.

#### Le bug que ce test a attrapé

La première version de `cartes_en_jeu` déclarait les QUATRE armes
expérimentales entrées en jeu alors qu'une seule l'était. Cause : le deck des
Armes Expérimentales est un **deck additionnel** (`additional_decks`), zone que
l'exclusion ne couvrait pas. Non corrigé, chacun des quatre scénarios suivants
aurait reçu trois armes de trop. Verrouillé par un test de régression portant
la forme mesurée.

### Piège de déploiement

`ui-app/deployer.sh` traite `~/marvel-work/fusion/marvel-lcg-src` comme la
SOURCE de `public/js` et `public/css`, et la `rsync --delete` par-dessus la
copie Windows. Éditer `public/js` côté Windows puis déployer SUPPRIME le
travail — c'est arrivé une fois sur ce chantier. Toute modification de
`public/js` ou `public/css` doit être poussée dans la copie WSL avant le
déploiement suivant. `patch_prepare.py` (scratchpad) rejoue les patches de
`prepare/app.js` de façon idempotente si le cas se reproduit.

### Livré (07/08/2026, troisième temps) — Sinister Motives

`data/campagnes/sm.json`, ses douze scans renommés par rôle, et trois
détecteurs génériques de plus :

* `cartes_en_pile_victoire` — les manigances Community Service déjouées ;
* `cartes_dans_zone` — les vilains encore DEBOUT à la fin des Sinistres Six ;
* `compter_trait` — les cartes ILLUSION restées dans les decks après Mysterio
  (les traits sortent préfixés `t_`, mesuré : `traits: { t_SYMBIOTE: 1 }`).

Nouveauté de structure : `victoire_commune`, des champs présentés à CHAQUE
victoire sauf la dernière. Sinister Motives en a besoin — sa piste de
Réputation et ses récompenses se reportent d'un scénario au suivant, ce que
`trors` ne demandait pas.

**Piège corrigé au passage.** L'ancien `CAMPAIGN_SCHEMAS` libellait
« Last Ones Standing » en « Sinistres Six VAINCUS ». Le livret dit l'inverse :
on note les vilains ENCORE EN JEU, et chacun revient en sbire au scénario 5.
C'est une pénalité, pas un trophée — deuxième erreur trouvée dans ce schéma
après celle des armes expérimentales.

La piste de Réputation elle-même reste une saisie manuelle : son calcul vit
dans une section « Conditions » de la piste papier, absente des scans. Le champ
l'annonce et rappelle les sept paliers.

Vérifié en jouant : Sandman gagné, Réputation à 1, Compact Darts (27182a)
choisi, validé — et au lancement de Venom, Compact Darts est **en jeu sur le
héros**.

### Ce qui BLOQUE les quatre boîtes restantes

Constat mesuré, pas déduit : sonde headless, un scénario par boîte, en mode
campagne avec un carnet pré-rempli, et on regarde si la récompense arrive.

| Boîte | Scénarios câblés | Vérifié |
|---|---|---|
| `trors` | 5 / 5 | ✅ récompenses appliquées |
| `sm` | 5 / 5 | ✅ 27182a en jeu sur le héros à Venom |
| `mts` | **2 / 5** (Ebony Maw, Thanos) | ⚠️ Hela et Loki n'appliquent RIEN |
| `mut_gen` | **0 / 5** | ❌ rien appliqué |
| `next_evol` | **0 / 5** | ❌ rien appliqué |
| `aoa` | **0 / 5** | ❌ rien appliqué |
| `gmw` | — | aucune récompense codée, séquence pure |

La cause est la même partout : `Message.WhenCampaignSetup` n'est écouté que si
la carte de manigance principale du scénario appelle `CampaignSetup(level)`
dans son `GetAbilities()`. Pour `mut_gen`, `next_evol` et `aoa`, le module
`campaign.py` existe, est complet, et **aucune carte ne l'appelle**. Le code des
récompenses est là ; le fil qui l'y relie n'a jamais été posé.

`mut_gen`, `next_evol` et `aoa` ont même un collecteur (`CollectMG`,
`CollectNeXt`, `CollectAoA`) qui sait déduire le carnet de l'état de fin de
partie — inutilisé lui aussi.

Écrire leurs fichiers de campagne maintenant produirait des écrans qui
RESSEMBLENT à des campagnes mais dont les récompenses ne feraient rien :
exactement le défaut que ce chantier corrige. Ce sera donc du travail sur le
moteur Python, carte par carte, pas de la donnée.

### Reste à faire

1. **Câbler le moteur** pour `mut_gen`, `next_evol`, `aoa` (0/5 chacune) et
   compléter `mts` (3 scénarios sur 5). Une carte de manigance principale par
   scénario à modifier. C'est le préalable à tout fichier de campagne.
2. **Identité verrouillée / deck modifiable** entre deux scénarios.
3. **Haut fait** de fin de campagne.
4. **Détecteurs restants à éprouver en jeu** : `cartes_sous_complot` et
   `pv_restants` sont testés unitairement sur des formes mesurées, mais n'ont
   pas encore été vus dans une vraie fin de scénario Zola ni en campagne
   experte.
5. **`gmw`** : jouable en séquence sans récompense, à décider si on l'expose.
6. Supprimer le code mort de `prepare/app.js` une fois toutes les boîtes
   portées.
