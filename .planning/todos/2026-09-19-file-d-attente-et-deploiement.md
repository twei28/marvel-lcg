# La file d'attente, et ce qui attend d'être déployé

Écrit le 19/09/2026. **À relire et à mettre à jour juste après chaque
déploiement** : c'est le seul endroit qui dit ce qui est parti et ce qui reste.

## DÉPLOYÉ le 05/10/2026 : phase du méchant en carré au milieu (commit `397331a5`)

Parti en production le 05/10/2026 vers 10 h 36 (heure locale), après une annonce
de 10 minutes aux joueurs, sur l'accord explicite de l'utilisateur (déploiement
même avec des joueurs en ligne, pour ce lot seulement). Contenu : tout ce qui
était « PRÊT, PAS DÉPLOYÉ » du 04/10 (`461093ec`) ET la refonte du cartouche en
carré 760×570 centré et déplaçable, le fait moteur « sonné », le total de
sbires, les choix du moteur traduits, la main visible et cliquable.
- Bundle plateau : `board-DFpkPvbG.js` (md5 `c4fa08ac…`), `board-GL_Eqa95.css`
  (md5 `86d7f0d6…`), identiques en local et sur le serveur.
- Site HTTP 200, service `narwhal` actif, faits moteur présents sur le serveur
  (`sbire_en_cours` dans `world_stat.py`). Annonce retirée après coup.
- `deployer.ps1` exclut désormais `.game-essai*` de l'archive (tar échouait sur
  ces liens). Moteur local 2345 relancé, moteur d'essai 2347, `.game-essai` et
  `launcher_essai.py` supprimés.
- NON VÉRIFIÉ : aucun écran de la production n'a été regardé après coup (pas de
  partie jouée sur le site) ; le rendu du carré n'a été vu que sur la planche
  locale et en vitest.
- Reste : `launcher_fast_essai_salon.py` et `.game-essai-undofix` (à demander à
  l'utilisateur), chantier « Sur la table », exemples au survol des Réglages,
  refonte du téléphone.

## ANCIEN « PRÊT, PAS DÉPLOYÉ » (04/10/2026), PARTI LE 05/10/2026 : frise de la phase du méchant, table personnalisable, boutons BD

Commité le 04/10/2026 au soir (`461093ec`, branche `mode-manuel`, 370 fichiers,
point d'étape avant la refonte du cartouche, sur « Oui, un commit maintenant »).
Toujours PAS déployé. Laissés hors commit : archives de scans et PNG à la
racine, `.tmb-captures/`, `.planning/captures-carrousel/`,
`ui-check/captures-tmp/`, `ui-check/salon-*.png`, `.game-essai*`,
`launcher_essai.py`, `launcher_fast_essai_salon.py`,
`deck/custom/SP_dr_Suit_Peni_Parker_Prebuilt_copie.json`, `RAPPORT-SCANS-FR.md`.

### Frise d'onglets (A4, spec du 03/10 ci-dessous, décisions postérieures appliquées)
- 6 onglets officiels numérotés + Bilan (`frise-phase.ts`), rouges passés et en
  cours, gris à venir, une seule ligne ; résultat court sous chaque onglet passé
  (« 4 dégâts », « +1 menace », « aucun ») ; un onglet vide n'est plus barré.
- Temps vides dits par une étape courte avec Suivant (« Aucun sbire engagé »,
  « Rien à révéler »…), jamais avant le premier temps connu ; insérés sans
  retrier (le rythme des accusés en dépend).
- Plus de « tout dérouler » (Échap ne fait plus rien).
- Relecture d'un onglet passé en lecture seule (liste des coups, détail au
  clic, « Revenir à l'étape en cours », Entrée y ramène), rien n'est acquitté.
- Renfort : surtitre « Renfort de X », « → Renfort : une autre carte est révélée »
  sur la précédente, chaîne maillon par maillon.
- Carte découverte en grand au-dessus du texte (17vh, 11vh sur téléphone).
- ⚠ MOTEUR TOUCHÉ (faits publiés, aucune règle changée) : `annule_par` sur une
  activation remplacée (`SetBeInstead` retient l'effet), `annulee_par` sur une
  carte révélée annulée (`WhenEffectBeCancel`), fait `stade` (manigance ou
  méchant qui change de stade EN pleine phase, `WorldStat.RecordStade`),
  `etoile` sur un boost à capacité (★). Plateau : « → Annulée par Sonné »,
  étape « La manigance passe au stade suivant : X » (carte en grand), ligne
  « ★ X : son effet de boost s'applique ».
- Hors phase : une activation datée du tour d'un joueur sort de la phase du
  méchant (elle s'y glissait au même round) et ouvre `CoupHorsPhase` pour ce
  seul coup (« Continuer »). Moteur : cas `A4 hors phase` (publié, « Player 1
  Turn »). ⚠ NON VU À L'ÉCRAN : `Puzzle.Boost` par la sandbox en plein tour
  bloque le moteur (« En attente de Spider-Man »), artefact du chemin de test.
- Téléphone : pastilles numérotées, seul l'onglet en cours garde son nom.
- « Revoir la phase du méchant » dans le journal du volet (`RevuePhase`, phase
  du round précédent, noms en français).
- Tests : plateau 2238/2238 + tsc ; cas moteur `A4 annulee par` 2/2, `A4 stade`
  1/1 (rouge par substitution), `A4 boost etoile` 2/2, `A4 hors phase` 1/1,
  A2 16/16, A3 7/7 ; autoplay Spider-Man vs Rhino et Ultron, 16 parties, 0
  bloquée, 0 erreur ; batterie complète (PARALLELES=4) 2635/2641 : les 6 rouges
  sont sg006, sg007, sg009, sg013, statistiques (déjà rouges avant ce chantier)
  et 60152, vert rejoué seul (artefact du parallèle). Vu à l'écran : frise PC et téléphone, relecture, bilan,
  revue, boutons. Vu au passage (antérieur) : sur téléphone, la fiche
  d'événement du bas couvre le titre de l'étape.

### Table personnalisable (B)
- `disposition.ts` : les 9 zones en données (origine = bande-manigances.css, un
  test compare les deux), grille d'édition 12 x 8 aimantée, minimums par zone,
  déplacer / redimensionner refusés s'ils chevauchent ou sortent, taille des
  cartes 60-160 % (`--taille-zone`, `zoom`).
- `EditeurTable.tsx` : Réglages → « Modifier la table » (PC seulement) ; zones
  encadrées, on les glisse ; poignée bas-droit = leur place (emprise), poignée
  haut-droit = taille des cartes (aussi au clavier) ; fantôme vert / rouge ;
  « Terminer », « Disposition d'origine », « Annuler » (Échap).
  Choix d'interprétation à confirmer : « la place » = l'emprise de la zone, le
  déplacement se fait en glissant la zone elle-même.
- `table-perso.ts` : une disposition par nombre de joueurs (`table-1`…`table-4`),
  navigateur + compte (le compte fait foi). ⚠ SERVEUR TOUCHÉ :
  `_table_valide` (12x8, 9 zones, bornes, sans chevauchement),
  `test_preferences_serveur.py` 17/17. Garde-fou : une table illisible revient
  à l'origine.
- Vu à l'écran : origine, éditeur (glisser, refus rouge), taille 120 %,
  enregistrement, 1920 / 1600 / 1366 / 1280, garde-fou, 2 joueurs (la table solo
  ne s'y applique pas), 3 et 4 joueurs, « Disposition d'origine ».

### Boutons de la question de défense (décidé le 04/10/2026, questions une à une)
- « Défendre avec X (DÉF 2 + 1 Bouclier) » et « Ne pas défendre (ATQ 2 + 3 Charge
  + 1 carte boost) » sur une ligne chacun, au même niveau ; la petite ligne sous
  le refus est retirée. Chaque bonus est nommé avec sa carte, deux au plus ;
  au-delà, « + N autres » en points, détail complet en infobulle ; les boosts
  toujours dits, jamais de total.
- ⚠ MOTEUR TOUCHÉ : le descripteur d'une carte publie `bonus` (ATK/DEF par carte
  source, `CardFace.BonusParSource`). Cas `A5 bonus publies` (Charge +3 réel),
  rouge par substitution. Plateau : `ligne-attaque.ts`, DemandeCentrale.
- Vu à l'écran (moteur d'essai, Charge sur Rhino) : « Défendre avec Spider-Man
  (DÉF 3) », « Ne pas défendre (ATQ 2 + 3 Charge + 1 carte boost) ».
- Plateau 2243/2243, tsc propre. Il faut relancer le moteur local pour voir les
  bonus (sans lui, le bouton montre l'ATQ actuelle seule).

### Barre du haut et Réglages (décidé le 04/10/2026, questions une à une)
- Plus de fenêtre « Plus d'options » : ⚙️ ouvre directement les Réglages, ⏸
  Mettre en pause a son bouton (visible quand la pause est possible), FR/EN a
  le sien ; le journal reste sur sa languette. Téléphone inchangé (« … »).
- Réglages agrandis (1000 x 760 au plus, hauteur fixe, texte 16 px), aide
  visible sous chaque intitulé. Onglets Apparence / Son / Jeu / Avancé ;
  intitulés : Style d'affichage (Normal / Sobre, gardé), Couleur de la table,
  Placement des zones, Animations, Météo et décor, Langue, Cartes en français,
  Texte des cartes en français, Annonce des exploits ; Bruitages, Musique de
  fond ; Phase du méchant (Étape par étape / D'un coup), Carte révélée en
  grand, groupe « Le jeu agit pour moi quand il n'y a qu'un choix » (Choisir
  la seule cible possible, Valider sans demander, Payer avec la seule carte
  possible, Finir mon tour quand je ne peux plus rien jouer), Sauvegarde à
  chaque phase ; Nouveau plateau, Aide quand je joue une carte (Courte /
  Détaillée), Pointeurs des autres joueurs, Table complète comme sur PC.
- Tests plateau 2245/2245, tsc propre. Vu à l'écran (moteur d'essai) : barre,
  les 4 onglets, hauteur 762 px partout.

### Signalements du 04/10/2026 (soir)
- **Limitless Strength (hk012) « Injouable · Une carte ne peut pas payer son
  propre coût »** alors qu'elle se joue. Cause : la passe INTERNE du coût
  (`CheckPlayerCanPayCost`) écrasait `world.render.derniers_refus`, et le refus
  juste de sa propre ressource partait au plateau comme raison. ⚠ MOTEUR
  TOUCHÉ (`game/event/manager.py`, le canal n'est plus écrasé par cette passe).
  Cas « hk012 … AUCUN refus … » (main exacte du signalement) rouge avant, vert
  après ; pack hk0 22/22, cas « refus » 13/13. Non vu à l'écran (moteur d'essai
  compilé avant le correctif).
- **Aperçu agrandi passé à gauche** : la borne « à gauche de la manigance
  principale » datait de la colonne de droite ; avec la bande des manigances
  (zone en haut à gauche) elle rejetait l'aperçu à gauche. Borne limitée au
  plateau sans bande (`Board.tsx`). Vu à l'écran : aperçu à droite (x 1544 et
  1244 sur 1900).
- **Écran de fin en onomatopée BD** (`fin-partie-bd.css`) : éclat à pointes
  derrière « DÉFAITE ! » (rouge) / « VICTOIRE ! » (bleu et jaune), petit choc
  à l'arrivée (coupé en sobre, sans animations, mouvement réduit), cartouche et
  boutons à coins coupés. Vu à l'écran (Puzzle.Lose / Puzzle.Win) : en
  victoire de campagne, l'éclat recouvrait le haut du panneau des récompenses ;
  éclat réduit et carte bornée dans ce cas (`:has(.camp-recomp)`).
- **« → 0 dégât annoncé »** (Klaw I, ATQ 0 + 2 boosts) : faisait croire à un
  coup sans effet. Plus aucun chiffre sur une attaque annoncée (le bouton
  « Ne pas défendre (ATQ …) » le dit déjà) ; la menace annoncée reste.
- **Réponse de héros pendant l'attaque d'un sbire** (capture Hulk / Klaw) : le
  ciblage se jouait dans la scène du cartouche ET l'assistant d'action reposait
  la même question hors de la scène, à moitié dessous. Prop
  `choixDansLaScene` : l'assistant se tait au ciblage et à la confirmation,
  reste pour payer un coût. (Provisoire : la refonte ci-dessous l'absorbe.)
- **Défenseurs l'un sous l'autre** (Hulk, Black Widow, refus) : la rangée était
  bornée à 640 px et passait à la ligne. `flex-wrap: nowrap`, les choix se
  partagent la largeur, le texte d'un bouton passe sur deux lignes ; à
  plusieurs défenseurs le titre passe au-dessus. Verrous sur la feuille
  (`deroule-question-rangee.test.ts`). Vu à l'écran à 1024 et 1600 (quatre
  choix sur une ligne, dans le cadre).
- Plateau 2253/2253, tsc propre, reconstruit (`deployer.sh`). Pas déployé.

### EN COURS : refonte du cartouche de la phase du méchant (décidé le 04/10/2026, 40 questions une à une)
- Décisions et gabarit unique : `.planning/todos/2026-10-04-refonte-phase-mechant-decisions.md`.
  Cartouche collé en bas (hauteur de la main, déplaçable), frise en pastilles +
  titre court sur une ligne, une rangée unique (acteur, boosts, total, cibles,
  refus), sous-cadre pour interruptions / réponses / ciblage / paiement, carte
  révélée en grand à gauche, bilan en trois colonnes, glissement entre les
  temps, clavier 1-9 / Espace / Échap. Mode « Étape par étape » seulement ;
  « Sur la table » sera le chantier suivant ; téléphone inchangé.
- Validation exigée : planche de 15 captures sur le moteur d'essai, regardée
  par l'utilisateur avant tout déploiement.
- 04/10 au soir : questions 41 à 43 posées après cartographie du code
  (pagination dans le cadre, réglage « Carte révélée en grand » grisé en
  Étape par étape, commit préalable). Plan final (trois plans jugés) dans le
  scratchpad de session `plans/PLAN-FINAL.md` : 7 lots (0 gates, 1 faits
  moteur E1-E8, 2 modèle TS pur, 3 cartouche sans question, 4 sous-cadre et
  questions, 5 relecture / hors phase / transitions, 6 planche et ménage).
  Réalisation lancée, vérification adverse après chaque lot, sans
  déploiement ni commit.
- 05/10 matin : **lots 0 à 6 faits et vérifiés, PAS commités, PAS déployés.**
  Plateau 2493/2493, tsc propre, gate du rythme verte (DeroulePhase.tsx
  445-1048 et cartouche-a-jour.ts intacts). Moteur : faits E1-E8 (cas A6 8/8,
  A3 récrits, batterie 2649/2654, 4 rouges sg préexistants). Planche envoyée
  (`scratchpad/planche-cartouche.jpg`) : 13 états sur 15, boîte 1872 x 224
  partout sans défilement. Le 2347 sert `ui-app/dist` (lien
  `.game-essai/public` remplacé, `voir-sur-2347.sh --restaurer` à la fin).
  Non capturables : état 4 (un méchant Sonné ne publie aucun fait) et état 9
  (aucun Renfort observé). À trancher : texte FR de la carte révélée quand le
  résumé manque (états 08, 15c), options du moteur en anglais (« Take 2
  damage »), à 1280 x 720 le cartouche couvre le bas de la carte du héros.
  Après « déploie » : relancer le 2345 pour les faits E1-E8.
- **Halo rouge autour de la main : retiré** (demandé le même soir). Une seule
  règle en cause, `.deroule-question .plateau-scene .zone-main` (board.css) :
  ombre et fond rgba(166, 0, 0, …) posés sur toute la boîte de la main dès
  qu'une question est logée dans la scène, invisibles sur le noir d'origine,
  nappe pourpre sur une table teintée. Les deux déclarations sont retirées, le
  `z-index` qui sort la main du voile reste. Verrou `halo-main.test.ts`
  (rouge avant, vert après). Plateau 2262/2262, tsc propre, reconstruit.
- Reste en attente derrière : les exemples au survol dans les Réglages
  (images `public/img/reglages/` à refaire : phase-etape, phase-coup,
  aide-courte, aide-detaillee).

### Boutons des questions en style BD (C)
- `boutons-bd.css` (question centrale, assistant, cartouche ; pas les menus de
  carte) : coins coupés, Bangers, plus d'arrondi ni de liseré blanc ; refus
  gris ; `.tonalite-ability` en ambre. Vu à l'écran (défense, Sens d'Araignée).

## FAIT le 04/10/2026, spec d'origine (voir « PRÊT, PAS DÉPLOYÉ (04/10/2026) » plus haut) (décidé le 03/10/2026, questions une à une) : phase du méchant, frise d'onglets

Inspirée de quincarter (frise) et de marvelsimulator.com (une phrase par étape,
carte en grand, étapes vides dites). Vaut en console comme au centre.
- Frise de 6 onglets : Menace, Méchant, Sbires, Distribution, Révélation,
  Bilan (le bilan devient un onglet). Chacun : nom + résultat court (total par
  effet : « 3 dégâts · +1 menace », « aucun »), vert fini, coloré en cours.
- Clic sur un onglet passé : relecture en lecture seule, bouton « Revenir à
  l'étape en cours » ; plusieurs coups listés, clic sur une ligne = détail.
  Pas de récapitulatif numéroté en plus. Téléphone : pastilles numérotées,
  seul l'onglet en cours détaillé. Après la phase : « Revoir la phase du
  méchant » en haut de la console (lecture seule).
- Pas à pas strict, AUCUN bouton « tout dérouler ».
- Temps vides annoncés par une étape courte avec Suivant : aucune menace posée,
  le méchant ne s'active pas (raison si connue), pas de sbire engagé, rien à
  révéler.
- Carte découverte en pleine largeur au-dessus du texte (boosts côte à côte,
  carte révélée) ; méchant et héros restent en surbrillance sur la table.
- Carte révélée qui fait attaquer / manigancer : sous la carte ; si décision,
  question actuelle (Défendre / Passer) inchangée. Effet ★ d'un boost : ligne
  sous l'attaque. Carte annulée : son étape reste, « → Annulée par X ».
- Renfort : nouvelle étape « Renfort de X » en surtitre, la précédente finit par
  « → Renfort : une autre carte est révélée » ; chaîne maillon par maillon.
- Changement de stade (manigance ou méchant) en pleine phase : étape à part,
  nouvelle carte en grand.
- Hors phase du méchant (pendant le tour du joueur) : une attaque / manigance
  du méchant ouvre le cartouche pour ce seul coup (faits moteur à publier hors
  phase, à vérifier).

## FAIT le 04/10/2026, spec d'origine (voir « PRÊT, PAS DÉPLOYÉ (04/10/2026) » plus haut) (décidé le 04/10/2026) : boutons des questions en style BD

- Tous les panneaux de question (cartouche du méchant + questions du tour),
  pas les menus de carte : coins coupés, police Bangers, plus d'arrondi ni de
  gros liseré blanc.
- Couleur par type d'action conservée ; capacités : mauve -> AMBRE (comme
  « jouer une carte », choix assumé) ; refus (Passer / Ne pas …) gris discret.
- Codé le 04/10/2026.

## FAIT le 04/10/2026, spec d'origine (voir « PRÊT, PAS DÉPLOYÉ (04/10/2026) » plus haut) (décidé le 04/10/2026, questions une à une) : table personnalisable

- Réglages → « Modifier la table » : zones encadrées avec poignées, « Terminer »
  enregistre, « Disposition d'origine » remet tout.
- Grille AIMANTÉE, aucun chevauchement ; TOUTES les zones déplaçables, main
  comprise.
- Deux poignées par zone : la place, et la taille des cartes.
- Une disposition par nombre de joueurs (solo, 2, 3, 4), suit le compte
  (nouvelle préférence serveur bornée). Téléphone inchangé (onglets).
- Ordre proposé : (1) étape 2 de la teinte (préparation + pages du site),
  (2) zones décrites par des données sans changement visible, (3) éditeur +
  enregistrement, (4) vérification écran tailles / nombres de joueurs.
- Corrigés le 04/10 : `--fond` rattaché aux panneaux (texte du bouton actif
  illisible sur table claire), « Pile de défausse » foncée sur table claire.
  REVUS À L'ÉCRAN le 04/10 (moteur d'essai, gris clair 200,6,60 et sable
  clair 40,14,52) : texte du bouton actif rgb(58,62,65) sur ambre, environ
  6:1 ; « Pile de défausse » lisible.

## PRÊT, PAS DÉPLOYÉ (03/10/2026) : console, phase du méchant revue, rapports Yarro n°43 à 47

- **Onglets de la phase du méchant** : intitulés officiels numérotés FR/EN
  (1, 2a, 2b, 3, 4), rouges passés et en cours (en cours souligné), gris à venir,
  bande oblique retirée (`deroule-onglets.css`). Compteur « 1 → 3 / 7 » en Anton
  (Bangers dessinait le 7 comme un 1). Rappel de règle retiré du cartouche.
  Question de défense : plus de bandeau « À toi de jouer » (la frise sert de
  poignée), « Défendre avec X », carte au-dessus du bouton, plus de « → Rhino »
  ni de texte de capacité ; l'onglet suit la phase réelle (`tempsDeLaQuestion` :
  2a méchant, 2b sbire).
- **Question à un seul choix, sans « Passer »** (« Fin de phase pour Domino ») :
  le titre recopiait le bouton, il est retiré et le bandeau devient une fine
  barre de prise (`est-poignee-seule`, DemandeCentrale). Les réactions gardent
  leur titre.
- **Mulligan lisible comme facultatif** (AssistantAction, tous les modes) :
  titre « Mulligan », consigne « Sélectionne les cartes que tu veux changer
  (facultatif) » puis « N cartes sélectionnées », bouton unique « Garder ma
  main » / « Défausser N cartes », plus d'« Annuler ».
- **MOTEUR, Hercules et decks mélangés** (fiche
  `2026-10-04-hercules-travaux-et-sbire-nemesis.md`) : Travaux/Dons mélangés
  (59001b) ; sbire némésis seul (IsNemesis, Face the Past, Shadow of the Past,
  37 héros officiels concernés) + mention Nemesis sur bl013/rs016/65012 ; decks
  Show (Spiral), Experimental Weapons, Gemmes mélangés ; fouille facultative
  refusée remélange le deck. Batterie 2627/2633, les 6 rouges hors chantier.
  À répondre au joueur après déploiement.
- **Couleur du fond (étape 1 : plateau + fenêtre d'accueil)** : roue de teintes
  ternes (saturation 0-18 %) + luminosité 6-62 %, fond + bandeaux + panneaux,
  halo du héros par-dessus en Normal. `board/teinte.ts` (jumeau
  `public/js/prepare/teinte-choix.js`), `styles/teinte.css`, `RoueTeinte.tsx`
  dans Réglages (direct, « Couleur d'origine », compte prévenu au repos 600 ms),
  roue + aperçu + « Valider » dans la fenêtre d'accueil. ⚠ SERVEUR TOUCHÉ :
  préférence `teinte` (« h,s,l » bornés, `test_preferences_serveur.py` 14/14).
  Vu à l'écran : 5 teintes x Normal/Sobre, Réglages, accueil.
  ÉTAPE 2 FAITE (04/10) : `public/js/teinte-page.js` + `css/teinte-pages.css`
  sur 12 pages ; la préparation l'applique en direct après « Valider » et après
  la synchro du compte (`appliquerTeintePage`, app.js). Ajouts après capture :
  variables `--fond/--panneau/--carte/--bord` (deck-builder, salon, rejoindre),
  `--w-*` (scene), `--hf-panneau` et bandeaux `.hf-barre`/`.w-topbar` teintés,
  dégradé sans répétition (bandes vues sur salon et replay). Vu à l'écran :
  12 pages x 2 teintes + préparation après « Valider » (capture
  `ui-check/scripts/capture-teinte-pages.spec.ts`, 25/25). Tests lanceur
  teinte + affichage 18/18. Les vignettes noires des cartes de deck.html
  restent noires (cadres de carte, pas un fond).
- **Fenêtre « Choisis ton affichage »** à la préparation (app.js
  `demanderLAffichage`, `doitProposerLeChoix`) : une fois, pour tout joueur qui
  n'a jamais choisi ; deux aperçus réels (`public/img/affichage/*.jpg`, pris sur
  une question de la phase du méchant). Vue à l'écran (PC et téléphone). Nouveau
  dossier `public/img` : aucune exclusion dans `deployer.ps1`, il part avec
  l'archive (servi en `.jpg`, le moteur ne sert pas les `.webp` par chemin).
- **Boutons d'un même choix sur la même ligne** (question dans le cartouche
  de phase, `deroule-onglets.css`) : alignés par le bas, la carte reste
  au-dessus de son bouton. Vu à l'écran (Spider-Sense / Ne pas utiliser).
- **Nom français des capacités nommées** (`nomDeCapacite`, `estNomDeCapacite`) :
  « Sens d'Araignée » et « Ne pas utiliser Sens d'Araignée » au lieu de
  « Spider-Sense » / « Spider-Man ». Un nom technique (`Generate_Mental`) ou un
  type (`Interrupt`, `Defense`) garde le nom de la carte.
- **Table calée sur le récit de la phase du méchant** (`table-calee.ts`,
  `onEtapeAffichee` de DeroulePhase) : la table dessine le monde de l'étape
  affichée, plus le plus récent. Cause : le cartouche relâche les trames sans
  nouvelle étape, dont le retournement du boost / de la carte rencontre. Une
  question au joueur rend le monde réel. Non vu à l'écran.
- **« Passer » renommé** (DemandeCentrale `libelleRefus`) : « Ne pas défendre »
  + ligne « ATQ 3 + 1 carte boost » (ce qui est connu avant de défendre, jamais
  un total : RR v1.8, boost face cachée avant la déclaration ; `ligne-attaque.ts`),
  « Ne pas jouer X » (carte en main), « Ne pas utiliser X » (capacité en jeu),
  « Ne rien jouer » (plusieurs), « Passer » ailleurs.
- **Fin de tour lisible** (même panneau que le mulligan) : titre « Fin de
  tour », « Sélectionne les cartes que tu veux défausser (facultatif). Tu
  repioches jusqu'à N », ou « Défausse au moins 1 carte : ta main est limitée
  à N », bouton unique, plus d'« Annuler ». ⚠ MOTEUR TOUCHÉ :
  `to_descriptor.py` publie `hand_size` par joueur (0 pendant la mise en
  place, l'identité y est un `Insert`). Cas 62034 rejoués : 2/2.
- **Texte français sous les arts alternatifs** (scans anglais) : l'aperçu
  agrandi affiche le texte FR (`artAlternatif` dans card-model, ApercuMarvelcdb
  charge textes-fr-complets à la demande).
- **Essais ouverts en local** (`essais.ts`, `estHoteLocal`) : sur `localhost` ou
  `127.0.0.1`, le plateau montre ce que voit l'administrateur en ligne (halo du
  héros, animations). Aucun effet en production.
- **Console : ABANDONNÉE le 03/10/2026 au soir** (choix de l'utilisateur :
  « remettre les phases et les questions au milieu comme avant, on peut
  quand même les bouger »). Retirés : `ConsolePartie`, `fenetres.ts`, le réglage
  « Fenêtres » et la clé de préférence `fenetres`. GARDÉS : la **bande des
  manigances** (`bande-manigances.css`, prop `bandeManigances` de Board : méchant
  collé au deck rencontre, principale puis annexes sur toute la largeur du haut,
  centrées sur le méchant, alignées malgré le badge « Crise », chevauchement
  au-delà de la place, plus de colonne à droite) ; le **journal compact**
  (`JournalConsole.tsx`, `journal-compact.ts`) dans le volet à languette ;
  pas de voile sur la table pendant la phase.
- **Phase du méchant** (rapport n°46 + choix de l'utilisateur) : pas à pas
  toujours (réglage « Avance toute seule » retiré) ; conséquences d'une carte
  révélée rangées sous elle (`rangerLesConsequences`, corrige aussi l'ordre :
  la manigance déclenchée s'affichait AVANT la révélation) ; cartes concernées
  allumées sur la table sans mouvement (`surbrillance-etape.ts`).
- **Choix d'art (préparation)** : flèches hors de l'image (une paire par carte ;
  en « même série », une seule paire à l'extérieur des deux cartes, l'alter ego
  fait défiler la face héros), boules retirées, alter ego plus assombri.
  Téléphone : deux flèches par face. Vu à l'écran (PC et téléphone).
- **Aperçu en jeu** : l'autre face (alter ego) prend l'art choisi
  (`autresFacesDe`, `card-model.ts`), test vu rouge sans le correctif.
- **n°43 Ben Urich** : choix de défausse sans intitulé (60153 `prompt`), « Cancel »
  et « Discard one » traduits. Même défaut sur Robbie Robertson 60156 : CORRIGÉ
  le 04/10 (`prompt="Discard it and deal another"`, traduit « La défausser et
  en distribuer une autre »), gabarit ci-dessous. Nouvelle clé du harnais
  `options_attendues` (le `prompt` d'un `AskChooseFace` devient le NOM de
  l'option, pas `prompt_text` : `prompts_attendus` ne pouvait pas le voir).
- **n°44 Typhoid Mary** : jetons de dégâts d'une carte sans PV (Disturbed Psyche)
  désormais affichés (`card-model.ts`).
- **n°45 Ivan Banionis** : jetons d'accélération affichés (`card-model.ts`).
- **n°47 Hugin & Munin** (53017) : la réponse n'était proposée que s'il y avait un
  personnage incliné ; la fouille est le coût, corrigé sur le modèle 53012.
- Tests : plateau 2085/2085, préférences 12/12, cas test_capacites des cartes
  60153, 60110a, 60200, 53017 verts avec substitution, autoplays ciblés 0 erreur.
- Vu à l'écran : console PC (1600 et 1366), annexes 0 à 7, phase du méchant.
  Non vérifié : téléphone, multijoueur. Après déploiement : marquer n°43 à 47
  « traités » dans /admin.

  ### 53017 : Hugin & Munin (signalement Yarro n°47, 03/10/2026)
  
  - [x] Étape 2 : carte de référence : 53012 Talon Line (« for each icon → ready a character you control », un `ChooseAbilities` + `ForChoiceAbility(...).SetTarget("YouControlUnit", canbe_ready=True)` par icône, APRÈS le calcul). Fouille-coût : inchangée (`CostFunc.SearchForCard(Minion, "PutIntoPlayEngagedYou", encounter_deck_top=10)`, modèle 56007 / ar001a).
  - [x] Étape 5 : texte-contre-code : « → » (coût / effet), « for each icon ([star] and [boost]) » (`CountTotalBoostStarAndBoost` compte étoile ET icônes), « you control », « ready ». Cause : la cible `canbe_ready, range=(1,"All")` posée AU DÉCLENCHEMENT empêchait la réponse quand aucun personnage n'était incliné (cas du signalement : Echo, Vivian, Hugin redressés).
  - [x] Étape 6 : nombres : top 10, coût 2, 2 PV, ATK/THW 1 : identiques desc / script.
  - [x] Étape 7 : 3 cas « 53017 » : tous redressés (la fouille a lieu), 1 icône (Hydra Bomber redresse Peter Parker incliné), témoin 0 icône (Goblin : Peter reste incliné). Nouveau script 3/3 ; ancien script 2/3 (le cas du signalement ROUGE : « 01110 n'est pas en jeu ») ; module vide 0/3 ; restauré 3/3.
  - [x] Étape 7 bis : limite imprimée : NON.
  - [x] Étape 8 : autoplay 8 parties falcon vs Rhino + témoin spider_man 8 parties : 8/8 et 8/8 terminées, 0 bloquée, grep erreurs 0 partout. Journal lu : fouille, sbire engagé, icônes comptées, Sam Wilson redressé (parties 5, 7) ; sans personnage incliné la partie continue (partie 8).
  - [x] Étape 8 bis : NON (un sbire entre en jeu par une voie déjà dessinée).
  
  Carte terminée : OUI.

  ### 60156 : Robbie Robertson (même défaut que Ben Urich n°43, 04/10/2026)

  - [x] Étape 2 : carte de référence : 60153 Ben Urich (même pack, même `AskChooseFace(..., forced=False, prompt=...)`), 45036 Magik (« Discard one »).
  - [x] Étape 5 : texte-contre-code : « look at that encounter card. You may discard it and deal that player another facedown encounter card » : `AskChooseFace([carte], forced=False)` puis `DiscardAll` + `DealEncounterCards(1)` au joueur visé (« that player »), inchangés. Seul ajout : l'intitulé du choix. Résultat : conforme.
  - [x] Étape 6 : nombres : Uses 3 stamina, retire 1, 1 carte distribuée : inchangés (cas existants : stamina 2 après usage).
  - [x] Étape 7 : cas « 60156 … le choix s'intitule « Discard it and deal another » » (`options_attendues`) : ROUGE sans le `prompt` (options vues : « Robbie Robertson: look at that encounter card, you may discard it », « Cancel »), VERT avec ; 3/3 cas 60156. Plateau : test `vocabulaire-moteur.test.ts` vu rouge puis vert.
  - [x] Étape 7 bis : limite imprimée : NON (Uses, déjà couvert).
  - [x] Étape 8 : autoplay 8 parties Spider-Man vs `stop_the_presses_hammerhead` + témoin Black Panther 8 parties : 8/8 et 8/8 terminées, 0 bloquée, grep erreurs 0 partout. Journal lu (partie 5) : Robbie incliné, -1 stamina, option « Discard_it_and_deal_another » choisie, Eviction Notice défaussée, Caught Off Guard distribuée puis révélée.
  - [x] Étape 8 bis : NON (un intitulé, rien de nouveau dessiné).

  Carte terminée : OUI.

## PRÊT, PAS DÉPLOYÉ (03/10/2026) : affichage sobre + volet du journal (retour Aghenatak « mal aux yeux »)

- Réglage « Affichage : Normal / Sobre » : bouton à côté du FR/EN dans la
  préparation (`affichage.js`, `affichage-choix.js`), ligne « Affichage » dans
  Réglages > Image et son du plateau (`board/affichage.ts`). Clé
  `mc_affichage_v1`, + compte via routes neuves `/get_preferences` et
  `/save_preferences` (`server_get.py`, fichier `preferences-serveur-N.json`
  dérivé de celui des arts, aucune config à changer ; ajouté à
  `deploiement/sauvegarde.sh`, donc scripts serveur à redéployer).
- Sobre = `styles/affichage-sobre.css` (hors couche, tout préfixé
  `html[data-affichage='sobre']`) : palette ternie, fond gris uni, contours
  sans lueur, cartouche du méchant gris, pulsations et transitions coupées,
  réglage Animations forcé à non, halo du héros retiré ; `mouvementReduit()`
  remplace les six tests `prefers-reduced-motion` en JS.
  Revu sur captures (choix de l'utilisateur) : bouton principal des questions
  (`.assistant-confirmer`, `.dc-continue`) gris clair à texte foncé, survol
  compris (il était jaune vif, `#ffe488` en dur) ; bandeau « Phase du méchant »
  gris, sans halo ni éclair. Vu à l'écran en vraie partie.
- Languette « Journal » en bas à droite : volet par-dessus les manigances
  (`board/VoletJournal.tsx` + `.css`), plein écran sur téléphone. Remplace la
  fenêtre « Partie » (`ModalePartie` supprimée) ; le bouton « Partie » du
  menu ⚙ ouvre le volet.
  Revu le 03/10/2026 : le volet ne contenait que les TROIS BOUTONS de
  l'ancienne fenêtre (Historique ouvrait encore un panneau flottant). Désormais
  onglets Historique / Journal du héros affichés DANS le volet
  (`ContenuHistorique` remplace le panneau flottant `HistoriquePartie`, panneau
  `.panneau-journal` retiré de board.tsx), « Log de la partie » en tête.
  Vu à l'écran en vraie partie (PC et téléphone, normal et sobre). CSS
  `.historique-panneau` / `.panneau-journal` désormais sans usage (board.css,
  menus-mobile.css), laissé en place.
- ⚠ `ui-check/tests/menus-mobile.spec.ts` (s24) échoue dès sa mise en place
  (`.portrait-menu .bh-options` introuvable) : périmé depuis la refonte de
  l'en-tête du 24/09 (Réglages dans « Plus d'options »), pas par le volet.
- Tests : vitest 2113/2113 (plateau 2070/2070 après la reprise du volet), tsc propre, lanceur 100/100,
  `tools/test_preferences_serveur.py` 11/11. Captures avant/après prises en
  vraie partie (moteur de dev 2346, arrêté).
- Non vérifié : la mémoire sur un vrai compte (aucun compte en local), le
  multijoueur, et les écrans legacy/campagne en sobre.

## PRÊT, PAS DÉPLOYÉ (03/10/2026) : audit des règles de construction, tous les héros

Crible du texte imprimé de toutes les identités (20 avec une règle de
construction), puis batterie : 95 decks de départ (aucun nouveau refus) et 4180
decks publiés sur marvelcdb (refus 375 → 153, chaque refus restant examiné :
decks réellement illégaux, marvelcdb ne vérifie ni l'unicité, ni l'égalité de
Spider-Woman, ni les cartes Permanent hors des 40). Tests lanceur 100/100, dont
14 vus rouges sur l'ancien `regles.js`.
- Règles ajoutées : Cyclops (alliés X-MEN), Kate Bishop (SKILL), Wonder Man
  (événements énergie), Harry Osborn (3 titres TECH), Night Thrasher (4 SKILL),
  Red Sonja (6 événements), Iron Patriot (aucun allié d'aspect, clé neuve
  `types_interdits_aspect`), Adam Warlock (1 exemplaire, 4 aspects égaux),
  Spider-Woman (aspects égaux), Moon Knight (coût ≤ 2, 4 cartes par aspect).
- Rules Reference : copie = titre ET sous-titre (Madame Web refusée à tort),
  unicité vérifiée (une carte unique, pas de correspondance, identité comprise).
- Bug : les signatures « Hero;Aggression » de Spider-Woman faisaient refuser
  TOUS ses decks marvelcdb (`classeDeConstruction`, `conversion.js`).
- Carte `62034` Size Advantage : classe Justice → Aggression (scan + marvelcdb).
- Deck de départ Jubilee : 2 « Unlikely Duo » (Max 1 per deck) → 1, et X-Gene 2 → 3,
  ce qui redonne exactement les quantités du pack (le 2e Unlikely Duo sert à Wolverine).
- Non traité : Cloak & Dagger (deux mini-decks, « 2 aspects » laissé tel quel).
- Commentaire mort corrigé dans `regles.js` (`outils/verifier-marvelcdb.mjs`
  n'existe pas).

### 62034 : Size Advantage (modification de la classe seulement)

- [x] Étape 2 : sans objet, le script `luke_cage/62034.py` n'est pas modifié.
- [x] Étape 5 : texte-contre-code : texte imprimé identique à `text` ; mots-pièges
      « instead » (6 au lieu de 3, codé), « remaining hit points » (`health`).
      Résultat : conforme.
- [x] Étape 6 : nombres : coût 2, RES énergie (icône du scan), 3 / 6 dégâts : identiques
      dans `desc` et le script. Classe imprimée AGGRESSION, `desc.Class` valait Justice :
      corrigé. Résultat : conforme.
- [x] Étape 7 : deux cas ajoutés (la carte n'en avait aucun) : « 62034 Size Advantage
      — sans GIANT et avec moins de PV que l'ennemi : 3 degats » et « — plus de PV
      restants que l'ennemi : 6 degats ». Substitution (effet retiré) : 0/2, dégâts
      0 et 5 au lieu de 3 et 11 ; module restauré (identique à HEAD) : 2/2.
- [x] Étape 7 bis : limite imprimée : NON.
- [x] Étape 8 : autoplay 8 parties contre Rhino, deck Hulk + 3 Size Advantage, témoin
      Hulk d'origine 8 parties : 8/8 et 8/8 terminées, 0 bloquée, grep erreurs : 0 et 0.
      Journal lu (3 parties tracées) : la carte est jouée, cible Rhino, inflige 6
      (Hulk 18 PV > Rhino 14), puis va à la défausse.
- [x] Étape 8 bis : la carte ne change pas ce qu'on voit : NON.

Carte terminée : OUI.

## PRÊT, PAS DÉPLOYÉ (03/10/2026) : import refusé du deck Maria Hill marvelcdb 64390 (Aghenatak)

Cause : sa face alter ego (50001b) autorise « the maximum number of copies of 3
S.H.I.E.L.D. supports » d'autres aspects, règle absente. Correctif : clé neuve
`hors_aspect.compte: "titres"` dans `regles.js` (le quota compte des titres, le
point final du trait « S.H.I.E.L.D » est ignoré), déclarée dans
`deck/starter/maria_hill.json`. Tests lanceur 78/78 ; vrai deck 64390 + vrai
catalogue : légal chez Maria Hill, refusé chez un autre héros.

## ✅ DÉPLOYÉ le 03/10/2026 (service actif, site 200) : signalement Yarro n°42, cartouche du méchant qui réapparaît après un Undo

Cause : l'Undo rejoue la partie, le monde n'a plus aucun fait, mais (1) le repli
de `etapesDeroule` relisait le journal local du même round et (2) la mémoire de
`DeroulePhase` gardait la phase annulée. Correctif : `entreesPourRepli`
(`deroule-phase.ts`, appelé par `board.tsx`) ne passe le journal que pendant la
phase du méchant, et `DeroulePhase.tsx` vide sa mémoire quand le round recule ou
que le même round n'a plus rien à raconter hors phase. Batterie plateau 2055/2055,
typecheck propre. Non reproduit en vraie partie. Après déploiement : marquer
#37 à #42 « traités » dans /admin.

## ✅ DÉPLOYÉ le 03/10/2026 (service actif, site 200) : carrousel d'arts de héros par face, mémorisé sur le compte

Non vérifié en prod : la mémoire sur le compte (aucun compte testable en local) et le plateau en partie. Le premier passage `.bat` a échoué (tar : avertissement transformé en erreur par `2>&1`), relancé en direct avec `deployer.ps1` : cause à corriger dans `DEPLOYER.bat`. ⚠ Corrigé le 03/10/2026 (PRÊT, PAS ESSAYÉ) : plus de `2>&1 | Tee-Object`, `-File .\deployer.ps1`, construction du plateau journalisée dans `construction-plateau.log`. À valider au prochain déploiement par le `.bat`.

- Wizard : carrousel par face (héros, alter ego) dans la modale du héros,
  case « même série pour les deux faces », moitié d'écran sur ordinateur,
  plein écran sur téléphone. Fichiers : `app.js` (`?v=20261003c`),
  `arts-heros-choix.js` (nouveau), `prefs.js`, `dico-en.js`, `prepare.css`
  (`?v=20261003c`), `prepare.html`.
- Serveur : `server_get.py` (`/get_arts_heros`, `/save_arts_heros`),
  `tools/config_serveur.py` (`arts_heros_file`), `deploiement/sauvegarde.sh`.
  Le moteur de chaque place doit être relancé et sa config `launch-N.json`
  régénérée pour que le compte soit reconnu.
- Plateau : `variantes.ts` lit `<héros>b` pour l'alter ego, bundle reconstruit.
- Tests passés : `arts-heros-choix` 9/9 (74/74 du dossier), `test_arts_heros_serveur`
  12/12, `test_config_serveur` 59/59, `arts-heros.test.ts` 8/8.

## ✅ DÉPLOYÉ le 03/10/2026 (md5 de app.js, nouveautes.js, prepare.html, palettes-heros.json, bundle du plateau et 3 images identiques en prod, 172 images `_cb/_rog` présentes, site HTTP 200) : arts alternatifs de héros, Conan dans les nouveautés et la palette

- 170 arts (`assets/pics/<id>_{cb,rog,rog2}.jpg`, + 2 copies du scan de
  Rogue héros sous rog/rog2) et leurs vignettes. Tables `ARTS_HEROS` dans
  `ui-app/src/board/variantes.ts` (par face, + `HEROS_DE_LA_CARTE`) et
  `public/js/prepare/app.js` (69 héros). Plateau reconstruit
  (`bash ui-app/deployer.sh`), `prepare.html` passé à `app.js?v=20261002a`.
- Écartés pour texte différent : War Machine AE `cb`, Wolverine AE `cb`,
  Rogue héros `rog`. Elektra et Iron Fist du zip : héros absents du jeu.
  Album Flickr : 25 photos sur 28 récupérées (les 3 dernières ne s'affichent
  pas sans compte).
- PREVIEWS.zip : rien de nouveau (93 images déjà en jeu).
- Conan : entrée de nouveautés + palette `cn001a-e` (seul ajout gardé de la
  régénération, qui aurait aussi modifié Jessica Jones).
- Tests : `arts-heros.test.ts` 5/5, `resources-art-packs-custom` 25/25,
  `tsc` propre, `test_palettes_heros.py` vert. Wizard et plateau NON
  vérifiés à l'écran.

## ✅ DÉPLOYÉ le 02/10/2026 (md5 de 59002, 59003, 62022, lj002, iw004 et cards.json identiques en prod, site HTTP 200) : 7 plantages préexistants relevés par l'autoplay, Dynamic Duo, 59003 et 59002

Chaque correctif a un cas rouge avant, vert après dans `tools/test_capacites.py`.
- lj002 Black Bolt : `Deck2.DiscardTopCards` n'existe pas, remplacé par `Worlds.DiscardEncounterCards`.
- iw004 : `AddGainedATK` inexistant, remplacé par `GainUntilTurnEnd(thwart=1 / attack=1)`.
- iw016 / iw017 : `IsScheme` / `IsAttack` inexistants, remplacés par `sch_message` / `atk_message` ; iw016 : `TakeIndirectDamage` s'appelle sur l'identité, pas sur le joueur.
- iw005 Flying Disk : `OnEvent.Form("You")` non reconnu (AssertionError dans `card_type.py:247` à chaque changement de forme) devenu `"AttachedIdentity"`. Aucun cas du harnais ne peut rougir (l'erreur est avalée) : preuve par l'autoplay Invisible Woman, 11 AssertionError avant, 0 après.
- iw015 Emotional Masterplan : deux défauts. `"EachPlayer"` n'est pas une règle de `PlayersCannotChangeForms` (le blocage de forme ne s'appliquait jamais) devenu `"AnyPlayer"` ; l'Action « Resist Manipulation » plantait (`TemporaryGain` avec le message courant) et dure maintenant jusqu'à la fin du tour (`WhenPlayerTurnEnd`).
- lj001a Lockjaw « Fetch! » : `Select.From(faces=...)` ne restreint rien sur des cartes hors jeu, la capacité récupérait la MANIGANCE PRINCIPALE (partie sans manigance, donc IndexError dans `game_over.py:104`). Remplacé par `AskChooseFace`. Le cas Fetch! vérifie désormais que la manigance reste là.
- `game_over.py` lui-même n'est PAS modifié : la gate est le cas Fetch!, pas un repli.
- Batteries : `iw` 31/31, `lj` 52/52. Autoplay (étape 8) : Invisible Woman 16 parties, Lockjaw 8 parties (Rhino, Klaw, normal), 0 Traceback, 0 AssertionError, 0 IndexError.
- À surveiller : `Select.From(faces=...)` dans une capacité de choix sur des cartes hors jeu, même piège possible ailleurs (déjà noté dans sg002).
- 62022 Dynamic Duo (signalement joueur « va chercher la carte en équipe mais pas l'allié »). Cause : `Search.SearchForCards` sans filtre ne renvoie PAS la liste des candidats, mais la carte CHOISIE (une seule, n'importe laquelle) ; le script filtrait ensuite ce résultat sur « Team-Up », donc la Team-Up était rarement trouvée, et l'allié ne suivait que si elle l'était. La lecture du mot-clé dans le texte ratait aussi les Team-Up dont le texte est en italique (`<i>(...)</i>`, 61027 et 62023 du pack Luke Cage) et celles à noms entre parenthèses (kb015). Réécrit : une recherche filtrée (`check_effect_fn`) de la Team-Up, puis une recherche filtrée de l'allié nommé (nom ou sous-titre, attribut `TeamUp` en priorité, repli sur le texte), les deux dans le deck et la défausse, puis mélange. 3 cas ajoutés (14018 + Quicksilver, 61027 + Jessica Jones, jj022 + Jessica Jones), rouges avant, verts après. Batterie `620` 15/15 ; autoplay Luke Cage 8 parties, 0 erreur.
- 59003 Embody Pathos et 59002 Defeat the Hydra (signalements Aghenatak du 02/10 : « les alliés peuvent participer aux travaux d'Hercules » et « le troisième travail (buter un sbire) : pas moyen de le valider »). Log de la table 10 lu en production (`replays/serveur-10`, partie de 14:52 à 15:23) : les Travaux 59004 et 59003 se valident bien en vrai (Don après chacun), le 59002 est révélé à la fin et le log s'arrête avant toute attaque sur la Hydre. Deux causes trouvées en local. (1) 59003 : `check_not_hercules` cherchait l'identité de l'INITIATEUR du retrait ; avec un allié, l'initiateur est quand même le joueur d'Hercules, donc l'allié passait pour Hercules. Corrigé en lisant `message.by_face` (la carte qui retire la menace). (2) 59002 : `after_leave` lisait `GetControlByOrOwner()`, qui rend le VILAIN pour un Travail attaché à un sbire (`GetOwner()` aussi) ; `Player.IsType` était faux, donc l'Atonement n'était JAMAIS appelé quand la Hydre mourait : Travail défaussé, pas de Don. Corrigé en retrouvant le joueur par son identité (Hercules). Le « allié blesse le sbire » n'est PAS reproduit (cas vert avec l'ancien script aussi) : à ne pas annoncer comme corrigé. 7 cas dans `tools/test_capacites.py` (590 : 7/7 deux fois ; le cas de validation de 59002 est rouge avant, vert après ; il attend le Don 59007, celui du dessus dans ce harnais, donc à revoir si l'ordre de la pile de Dons change). Autoplay Hercules : 6 parties, 0 erreur. Non vérifié : la partie réelle d'Aghenatak après le pas 80.
- À noter, non corrigé : 8 Team-Up n'ont pas d'attribut `TeamUp` dans `cards.json` (seulement le texte) : 60031, jj022, bw024, bw025, il023, wc017, tt019, hc022 ; le moteur ne peut donc pas imposer « ne se joue que si les deux personnages sont en jeu » pour elles. À vérifier carte par carte.

## ✅ DÉPLOYÉ le 02/10/2026 (md5 de cards.json, nouveautes.js et 61007.py identiques en prod, site HTTP 200) : audit des alliés (dégât consécutif) et signalement #42 (61007 compte dans la limite de manigances)

- Audit : 312 alliés MarvelCDB sur 317 corrects (source `attack_cost` / `thwart_cost`). 5 Luke Cage corrigés : 62002 ATK `2*`, 62012 `2*/1*`, 62014 `2*/1*`, 62020 ATK `2**`, 62021 `2**/2**`.
- 14 alliés fan-made corrigés (astérisque posé sur ATK et THW d'après les scans) : lj002, lj018, lj019, lj020, lj021, lj022, lj025, il002, ok002, ok003, ok017, ok018, 65002, rs002. `lj026` Ms. Marvel NE reçoit PAS d'astérisque : son script donne déjà 1 dégât consécutif (la première version le doublait, vu en test et retiré).
- 46 cas ajoutés à `tools/test_capacites.py` (filtre `consecutif(s)`), rouge avant, vert après.
- #42 : 61007 Piecing It All Together comptait dans la limite. Cause : drapeau `not_count_player_side_scheme_limit` posé sur `WhenCardSetup` (mise en place seulement), donc jamais posé quand la carte est jouée. Corrigé sur `WhenCardEnterPlay` (PAS `AfterCardEnterPlay` : la limite est contrôlée avant). 2 cas ajoutés (exemption + témoin 61039 qui, lui, compte), rouge puis vert.
- Relecture visuelle des 175 autres alliés hors MarvelCDB (4 lecteurs, scan par scan) : 5 écarts corrigés, rouge avant et vert après : 60139 Shop Proprietor `1*/1*` devenu `1**/1**`, vp002 Black Cat THW `1*` devenu `1` (étoile de texte, pas de consécutif), sw002 Madame Web ATK `0**` devenu `0*`, si003 Teen Abomination THW `0` devenu `0*`, mf002 Invisible Woman THW `1` devenu `1*`. 170 conformes.
- Non vérifiables faute de scan (cartes générées par le moteur, un personnage transformé en allié) : fne_black_cat_ally, registered_ally, phoenix_controlled_ally, karma_controlled_ally, redemption_redeemed_ally, tah_hellbender_ally. Leurs scripts n'ont pas été relus.
- Batterie `consecutif(s)` : 55/55. Batterie `610` : 34/34. Autoplay étape 8 (Luke Cage, Lockjaw, Okoye, Iron Lad, Red Sonja, Madame Web, Invisible Woman, Black Cat ; Rhino et Klaw, 4 parties chacun) : sans lien avec ce lot mais plantages relevés, scripts NON modifiés par ce lot, donc déjà en prod : lj002 Lockjaw (`deck.DiscardTopCards` n'existe pas), iw004 (`AddGainedATK` sur `AfterUnitChangeForm`), iw016 et iw017 (`IsScheme`/`IsAttack` sur `AfterUnitAttackEnd`), `AssertionError` dans une condition de carte (Invisible Woman), `IndexError` dans `game_over.py` à l'élimination d'un héros. À traiter à part.
- Déployé sur ordre explicite « deploie maintenant » après que le serveur ne s'est jamais vidé (17 à 55 connexions HTTPS, table 2360 active) : la partie en cours a été coupée.
- À marquer « traité » par l'utilisateur dans /admin : #37 à #42.

## ✅ DÉPLOYÉ le 02/10/2026 (10:05 UTC, md5 de cards.json, nouveautes.js et 61012.py identiques en prod, site HTTP 200) : pack Jessica Jones revérifié (signalement #41, Squirrel Girl sans dégât consécutif)

Cause du #41 : astérisques de dégât consécutif absents de `cards.json` (`desc.ATK` / `desc.THW`). Même défaut sur les 6 alliés : 61017 `1*/1*`, 61003 `2**/2**`, 61015 ATQ `3**` CTR `2*`, 61016 `2**/2**`, 61025 `2*/2*`, 61038 `1*/1*`.
Audit carte par carte du pack (sources MC4DB / MarvelCDB), tout corrigé avec cas rouge avant, vert après dans `tools/test_capacites.py` (filtre `610` : 32/32) :
- 61019 Strategy Session : ressource `Y` devenue `B` (mentale).
- Menace de départ : 61020 `4*`, 61021 / 61028 / 61039 `3*` (par héros), 61029 `3*` devenu `3`, 61032 `2*` devenu `2`.
- Scripts : 61012 Ticked Off réécrit (réponse forcée en fin d'activation du vilain, repasse en forme héros, 5 dégâts au vilain et aux sbires engagés), 61013 (`HeroInterrupt`), 61024 (déclencheur « contre un complot du vilain » au lieu de `None`).
- Autoplay (étape 8) : 16 parties JJ + 16 parties témoin Spider-Man (Rhino, Klaw, normal), 0 incident, 0 traceback sur les 32 journaux. Aucune victoire des deux côtés (pilote simple). JJ tient moins longtemps (3,4 et 4,8 rounds contre 4,9 et 6,9), non comparé à l'état d'avant correctif.
- Doutes non traités : 61016 Spider-Woman (`SetPlay()` en Action), 61027 Unbreakable Bond (répartition du soin), astérisques inoffensifs de 61001a.
- Images : les 43 scans sont présents en local et en prod. Les cartes grises du joueur viennent de faux « sans image » générés puis gardés dans `assets/cache` de la prod (20/09 et 02/10 07:21) et/ou en mémoire d'une table déjà lancée. Fait au déploiement : `61*.jpg` supprimés de `assets/cache` en prod (21 fichiers restent, aucun JJ), tables redémarrées. Scans non testés en HTTP (aucune table lancée juste après le redémarrage), 43 scans JJ présents dans `assets/pics`. Déployé malgré deux autres adresses connectées (une table 2351 active), sur accord explicite de l'utilisateur.
- `nouveautes.js` : 5 entrées parties (JJ, Storm météo, bandeau « Voir la table », « Injouable », pièces rejouées).
À marquer « traité » par l'utilisateur dans /admin : #37 à #41.

## ✅ DÉPLOYÉ le 02/10/2026 (md5 board.html et board-DuKAfvXJ.js identiques en prod) : languettes PILES et MAIN déplaçables (signalement #40 de Yarro)

Sur téléphone, la languette PILES cachait le badge REC du héros. Décision avec
l'utilisateur : appui long (450 ms) sur la languette, puis glisser en
hauteur ; les deux languettes, chacune retient sa place dans `localStorage`
(`marvel-encoche-gauche` / `-droite`). Sans place retenue, rien ne change.
Tap et swipe vers l'intérieur ouvrent toujours. Fichiers : `Encoche.tsx`,
`portrait.css`, `v2-mobile.css` (`touch-action: none` sur la V2), test
`Encoche.test.tsx` (7 cas). Vérifié dans Chromium : appui long + glissé de
250 px, place gardée après rechargement. Pas essayé avec un vrai doigt.
Déployé malgré une table active (autre joueur sur le 2351), sur accord explicite
de l'utilisateur. Reste #40 à marquer « traité » dans /admin par l'utilisateur.

## ✅ DÉPLOYÉ le 01/10/2026 (nuit) : météo de Storm, cartes non utilisées SOUS la carte en jeu

Demande : « les cartes climat non utilisées doivent aller sous celle qui est en cours d'utilisation ». `zones.ts` : les cartes du deck Weather deviennent les `attachees` de la météo en jeu (empilées derrière, comme des améliorations, chacune se survole), le deck n'a plus de pile propre tant qu'une météo est en jeu (sans météo en jeu, il reste une pile). L'éventail au survol (`.pile-eventail`) est retiré. Test : `board/deck-weather-storm.test.ts` (6 cas). Vu au navigateur sur fixture temporaire (supprimée). Déployé après le « déploie » (md5 de board.html identique, HTTP 200).

## ✅ DÉPLOYÉ le 01/10/2026 (soir) : header et météo de Storm (la météo a été refaite ensuite, voir plus bas)

- Header : le bandeau « ROUND / Tour de… / À toi de jouer » était centré en absolu sur la barre et passait SOUS le groupe de boutons (~880 px) sur une fenêtre moyenne (capture de l'utilisateur, 1620 px). `board.css` : marges auto (au milieu de la place libre à gauche des boutons) par défaut, centrage absolu seulement à partir de 2200 px. Vérifié par la CSS seule, pas mesuré au navigateur (la fixture `?etat=` n'a pas de header).
- Météo de Storm : la carte Weather EN JEU (trait `t_WEATHER`) sort des soutiens et se pose dans la case Weather, à côté de son deck ; au survol de la case, un éventail montre toutes les cartes Weather (en jeu + deck). `zones.ts` (`meteoEnJeu`, `eventail`), `Board.tsx` (`.pile-eventail`), `board.css`, test `board/deck-weather-storm.test.ts`. Mesuré au navigateur sur une fixture temporaire (supprimée) : 4 cartes dans l'éventail. Limité au trait Weather, les autres decks spéciaux (Invocation...) gardent leur disposition.
- Déployé après le « déploie » (build local + `deployer.ps1 -Code`, HTTP 200).

## ✅ DÉPLOYÉ le 01/10/2026 (après le « déploie ») : encart « Injouable » retiré des cartes d'identité (attend le « déploie »)

Capture d'Ororo Munroe (alter ego de Storm) avec « Injouable : Jouable seulement sous forme de héros ». Cause : `Effect.Render(by_effect)` rend le `bind_id` de `by_effect`, donc pendant « Resolve Mulligans » ou le Setup, le refus d'une carte de la main se collait sur l'identité. Correctif : `Controller.RendreLesRefus` écarte tout refus dont le `bind_id` est une identité (`src/engine/controller/controller.py`). Gate : `tools/verifier_raisons_refus.py` échoue maintenant si un refus tombe sur une identité (vue rouge sur storm/spider_man/captain_marvel, puis verte). Moteur seul, aucun changement de plateau.

Aussi déployé : la pile du deck spécial (Blizzard du deck Weather) est calée au même niveau que le héros voisin (`board.css`, `.zone-deck-special .plateau-cartes` : `align-items: flex-start; padding-top: 6px`, titre à `top: -9px`). Mesuré dans le navigateur : 445 px des deux côtés (écart avant : 13 px), titre visible. `.zone-reserve` et `.zone-rising-tide` gardent leur ancien calage (non demandé). Embarqué avec le prochain « déploie » (reconstruire d'abord : `bash ui-app/deployer.sh`).

## ✅ DÉPLOYÉ le 01/10/2026 (md5 world.py, board.html et board-ByT9plY4.js identiques en prod ; batterie complète test_capacites encore en cours au moment du déploiement, à relire) : suite des retours sur « Voir la table »

Retours de l'utilisateur après essai en prod : bouton à mettre en haut à côté de « ⌂ Menu », et fenêtre des étapes du méchant impossible à bouger.
- `BoutonVoirLaTable` est dans l'en-tête `.board-actions`, juste après « ⌂ Menu » (grisé tant qu'aucune fenêtre n'est ouverte).
- `DeroulePhase` : le bandeau rouge (`.deroule-chrono`) est une poignée `poignee-glisser`, repliée comme dépliée.
- Cause réelle du « je ne peux pas la bouger » : `useGlisserPanneau` ne posait la capture qu'après 6 px, dans le `onPointerMove` de la poignée ; une poignée mince est quittée avant, la fenêtre ne bougeait pas. Le suivi se fait maintenant par écouteurs `window` posés au `pointerdown`. Mesuré à la vraie souris : -150/-200 px, position conservée après « Suivant ».
- Garde durable : `cd ui-check && npm run glisser-fenetre-etapes` (nécessite un serveur sur le baseURL, vraie souris, aucune partie lancée).
- Vérifié : tsc propre, vitest 2070 verts, `npm run build` fait.
- Pour déployer : vérifier qu'il n'y a personne en ligne, `bash ui-app/deployer.sh`, `deploiement/deployer.ps1 -Code`, comparer les md5 de `board.html`, `board-*.js`, `board-*.css`.
- Signalement #37 : à marquer « Traité » par l'utilisateur dans /admin.
- Signalements #38/#39 (Yarro, 30/09) : #38 avait raison, le moteur avait tort. Rules Reference p.18, « End of Player Phase » etape 3 : « Ready each exhausted encounter card ». `PlayersEndPhase` ne relevait que `GetControlCards()` : une obligation ou un attachement de rencontre epuise (ex. « Serve. » de Purple Man, Hypnotic Suggestion de Lady Sif) restait epuise pour toujours, donc sa Forced Action ne servait qu'une fois. Corrige dans `world.py` (`ReadyEncounterCardsAtEndOfPlayerPhase`, appelee apres la pioche et le relever des joueurs, toutes cartes de rencontre, decision de l'utilisateur). Cas `60107 "Serve." ... fin de phase joueur` dans `tools/test_capacites.py` (rouge sans le correctif, vert avec). Batterie complete lancee le 01/10 (`/tmp/cap-batterie-38.log`), PAS deployee. #39 n'est pas un second bug : meme etat de partie, 23 s apres, autre image ; le formulaire n'accepte qu'une image.

## ✅ DÉPLOYÉ LE 01/10/2026 : fenêtre principale déplaçable + « Voir la table »

Sur « déploie » conditionnel de l'utilisateur (« s'il n'y a personne en ligne
à part moi »). Aucune connexion sur les ports 2345..2400. `bash ui-app/deployer.sh`
(bundle `board-Da6pgeQM.js`) puis `deployer.ps1 -Code` : même bundle en prod,
service `narwhal` actif, site en 200. ⚠ Depuis WSL, `ssh` refuse la clé
(permissions 0444 sur /mnt/c) : utiliser `ssh.exe -i 'C:\...\cle_narwhal'`.
Règles de permission SSH/deployer ajoutées dans `.claude/settings.local.json`.
Le bouton n'a toujours pas été vu dans une vraie partie : à regarder.

Détail du chantier (écrit avant le déploiement) :

Signalement Yarro du 30/09 (« je peux bouger la fenêtre du fond mais pas la
fenêtre principale »). Cause : le cartouche de question de `DeroulePhase.tsx`
(bandeau rouge « À toi de jouer ») avait été oublié par le chantier « toutes les
fenêtres » du 28/09. Correctif : poignée sur le bandeau (`translate`, qui
compose avec le `translateX(-50%)` existant). Ajout demandé : bouton « Voir la
table » (`BoutonVoirLaTable.tsx`), bascule globale, fenêtres à 15 % et table
cliquable à travers, en haut à gauche (le coin droit est au journal).
Mesuré : 2069 tests unitaires verts, typecheck propre, `npm run voir-la-table`
(2 cas, vrai CSS, `elementFromPoint`) vert sur `ui-app/dist`. Pas vu dans une
vraie partie : à regarder au déploiement (emplacement du bouton). Rien commité.

## ✅ DÉPLOIEMENT du 30/09/2026 (soir) : tout l'arbre de travail, « à jour à 100 % »

Sur « déploie » de l'utilisateur, aucune connexion sur les tables 2351..2380.
`bash ui-app/deployer.sh` (bundle `board-DXiVGHed.js`, inchangé) puis
`deployer.ps1 -Code` sans stash : tout l'état brut du disque est parti (dont
`controller.py` et `player_action.py` restaurés, 31007 SP//dr, `orchestrateur.py`,
packs non commités). md5 local = prod pour ces 6 fichiers, service actif,
site en 200. Le Caddyfile de prod n'est pas réécrit par le script (corrigé à la
main, voir plus bas) ; ses autres écarts avec le dépôt subsistent.

## ✅ DÉPLOIEMENT du 30/09/2026 (après-midi) : signalements 30 à 35, Wiccan, points à placer

Sur « déploie » de l'utilisateur, personne en partie (aucune connexion établie
sur la table 2364). `bash ui-app/deployer.sh` puis `deployer.ps1 -Code` : bundle
`board-DXiVGHed.js` et `15011.py` (Wiccan) identiques à la prod (md5), service
actif, site en 200. Contenu : Passer, encart Injouable, bulles, vocabulaire,
n°30 et n°32, Wiccan obligatoire (une cible libre par icône, « (1/3) »), compteur
« reste N à placer » et avertissement à la validation d'une sélection répartie.
✅ **Caddyfile de prod corrigé à la main le 30/09 (soir)** : `'self'` ajouté aux deux
`frame-ancestors` (lignes 37 et 307), sauvegarde `/etc/caddy/Caddyfile.bak-30-09`,
`caddy validate` OK, rechargé, service actif. Voile blanc de la météo levé.
À noter : d'autres écarts existaient déjà entre ce Caddyfile et `deploiement/Caddyfile`
(ex. routes p1..p20 en prod contre p1..p30 dans le dépôt), non touchés. ✅ **Wiccan clôturé** (30/09, soir) : les 3 parties en
minuteur (Rhino 5 et 6, Klaw 6) venaient du pilote `tools/autoplay.py`, pas du
moteur : pour le jeu gratuit de Chaos Magic (15003), la demande affiche un coût
« * » (déjà annulé) et `executable()` le lisait comme impayable, donc répondait
« passer » à une demande obligatoire (assert `controller.py:515` en boucle). Le
pilote traite maintenant « * » comme gratuit ; les 3 parties se terminent, cas
Wiccan du harnais 9/9. Signalement n°36 (Venom) : pas un bug, règle du scénario
Grand Collection (Symbiote Enragé vaincu = 5e carte de La Collection = défaite) ;
réponse courte donnée à l'utilisateur pour Phocéa, rapport NON marqué traité.
⚠ Le 30/09, un test A/B a écrasé par erreur `controller.py` et `player_action.py`
(copies jetables faites de liens vers `src`) : restaurés depuis la prod, diff vs
HEAD identique. **Ne jamais écrire dans une copie `.game-src-*` sans vérifier
qu'elle ne contient pas de liens vers `src`.**

## ✅ DÉPLOIEMENT du 29/09/2026 (midi) : règles MC4DB, Multiverse, titres FR

Envoi `-Code`, trois commits : `c2b7d4f3` (10 cartes officielles, Multiverse,
Fleeting/Alias, mots-clés maison alignés sur MC4DB), `3bec5a15` (titres français
des boîtes et campagnes), `bdac9eba` (outillage Stan Lee et import d'images).
31 fichiers vérifiés par md5 contre `/opt/narwhal` après coup, service actif,
site en 200. La table Discord active (port 2351) a été coupée par le
redémarrage (aucune autre table). Pas de batterie complète de cartes avant
l'envoi (demande de l'utilisateur, la consommation) : les cas `[mc4db]` et
`[dt]` étaient verts, et `CanBeInstead` de `WhenMinionWouldEngagePlayer` est
la retouche moteur partagée à surveiller. `cards.json` est committé en entier
(embarque wave, conan, red_sonja déjà en prod). Reste hors dépôt : ui-app,
`site/orchestrateur.py` (hors Discord) et des fichiers moteur d'autres sessions,
déjà en prod mais jamais committés.

## ✅ SECOND DÉPLOIEMENT du 22/09/2026

Envoi `-Code` : un seul commit, `1c7add23`.

**`fix(manuel): le menu de clic droit reste entier dans l'écran`** — signalé
en jeu juste après le premier déploiement du jour : le menu contextuel d'un
PERSONNAGE (bien plus d'entrées qu'une carte ordinaire) ouvrait avec son bas
hors écran, sans aucun moyen de l'atteindre. L'ancien calcul devinait une
hauteur fixe de 340px, qui ne suffisait qu'aux petits menus.

- `MenuTriche.tsx` mesure désormais la VRAIE hauteur rendue
  (`getBoundingClientRect` via `useLayoutEffect`) au lieu de la deviner.
- `board.css` pose un filet de sécurité (`max-height` + `overflow-y: auto`
  sur `.menu-triche`) : même un écran plus bas que le menu entier laisse
  chaque entrée atteignable en défilant.
- 3 témoins ajoutés, 2 rouges constatés sans le correctif.

Cette fois, **annonce posée aux joueurs** (2 minutes, message de préavis par
défaut) avant le redémarrage — à la demande explicite de l'utilisateur,
contrairement au premier déploiement du jour où l'unique connexion (Yarro)
avait déjà été vérifiée déconnectée. Posée directement en base
(`narwhal.db`, table `annonces`) via SSH, faute d'accès à `/admin` : même
DELETE+INSERT que `poser_annonce()` côté orchestrateur, mêmes formats de
champs.

175/175 fichiers (1957 tests), typecheck propre. Vérification finale :
`https://narwhalchampions.com/` → 200.

## ✅ DÉPLOYÉ le 22/09/2026

Envoi `-Code` : 101 commits partis d'un coup (`04fcf37e..7de85377`), le plus
gros déploiement depuis Fear No Evil. Personne d'autre en ligne (Yarro
déconnecté, vérifié par l'utilisateur avant le feu vert). Vérification finale :
`https://narwhalchampions.com/` → 200.

Par chantier, pas par commit (la liste complète est dans `git log`) :

- **Le mode manuel, les DEUX moitiés, enfin complet et fusionné.** Pause en
  cours de partie (bandeau, qui/depuis quand, Passer la question), glisser-
  déposer libre vers n'importe quelle pile, raccourcis clavier calqués sur
  Tabletop Simulator, catalogue de recherche, annulation (Ctrl+Z) qui rejoue
  au bon rang, sélecteur de héros, fin de partie déclarée, refus visibles côté
  moteur ET plateau, spectateur fermé aux routes POST et aux gestes de pause,
  section « gestes manuels » du rapport de bug avec sa propre alerte
  d'incomplétude.
- **SP//dr, paiement incomplet (`ab0b6e7e`)** : le défaut était dans le moteur
  (`EffectChecker.check_pay`), pas la carte — 107 cartes concernées, corrigé
  pour toutes.
- **Jessica Jones, cartes coincées en résolution (`54462b83`)** : une carte
  cherchée puis refusée retourne enfin dans son deck.
- **Le salon attend SA partie, pas « une » partie** : repère de fraîcheur
  (`game_uid`), rejoindre avec le bon héros, la campagne dans la règle.
- **Quitter la partie ferme la table (`f2493533`, `974f76fb`)**, pour de bon,
  avec un bouton « Déconnexion complète » séparé du simple retour au menu
  (`d97454ed`).
- **Fixé aujourd'hui, trouvé en revue de tout ce qui précède** :
  - `5c8aa59d` Cable peut enfin construire un deck autour de ses manigances
    annexes (elles ne comptaient pas dans la limite d'aspect).
  - `dad5232b` six messages du salon manquaient à l'anglais.
  - `4bcba8a8` la bande de couleur du héros ressort plus (demande directe).
  - `6ad07257` le lâcher réel sur une pile VIDE ne visait pas sa pile — le
    correctif `ca02560f` de la veille ne marchait qu'à l'essai, pas au vrai
    glisser (aucun `.scan-card` sous le point).
  - `7de85377` le deck spécial (Invocation, Réserve…) fantomait pour TOUS les
    héros, y compris ceux qui n'ont pas ce mécanisme — signalé en jeu par
    l'utilisateur sur Angel puis Cable, corrigé dans la foulée.

Batteries avant envoi : mode manuel **48/48 VERT**, plateau **1954/1954**
tests (175 fichiers), typecheck propre, `test_capacites.py` filtré sur
« paiement » (13/13) et « recherche » (8/8).

⚠ **Mis de côté, PAS déployé** : un chantier inachevé sur `server_get.py` /
`test_heros_du_siege.py` (une course entre `debut` et le monde au moment où
une partie est annoncée mais pas encore montée). Marqué « CONSTAT ROUGE
TEMPORAIRE » par son auteur, 7 échecs mesurés sur la nouvelle batterie — un
rouge délibéré de TDD, pas une régression. Laissé dans le dossier de travail,
volontairement écarté de l'archive envoyée (`git stash` le temps de l'envoi).
À reprendre et à finir dans une prochaine session.

## ✅ DÉPLOYÉ le 19/09/2026 à 12:30

Le serveur tourne sur ce code. Ce qui est parti, en six commits :

| Commit | Quoi |
|---|---|
| `9ec8f6b9` | Un lien **Accueil** dans la barre du site. |
| `bd9ff080` | « Mes signalements » montre tout ce qui vient de ses tables. |
| `84ae2ed0` | Un signalement dont l'envoi échoue est gardé et rendu. |
| `c9ba70af` | Plateau : deck et défausse à la hauteur du héros, les deux faces des héros maison, sélection de cibles qui respecte « DifferentCards ». |
| `6947446f` | **Fear No Evil** : 146 cartes, cinq affaires interchangeables, Kingpin, campagne en ordre libre. |
| `da85b1ea` | **La boucle de campagne mesurée** (115 épreuves, dix boîtes), neuf récompenses oubliées réparées, couvertures de livret dans l'écran des campagnes. |

Détails du déploiement :

- bundle du plateau reconstruit avant l'envoi (`board-CSUE6ZwU` → `board-CdTJ1KkH`),
  vérifié sur le serveur ;
- 171 scans de Fear No Evil uniformisés (615 px de petit côté), sauvegardés
  d'abord dans `sauvegardes-serveur/scans-originaux`, puis envoyés ; vignettes
  et scans HD régénérés sur place ;
- **les planches de livret ne sont PAS dans le dépôt** (`public/stories` est
  dans le `.gitignore`) : elles vivent sur ce disque et sur le serveur. Les
  regénérer demande les PDF officiels, dont les URL sont en tête de
  `tools/pages_livret.py` ;
- une copie mal enracinée (`Fusion/marvel-lcg-src/LCG/Fusion/...`, 20 fichiers
  d'une version du 18/09 à 18:44, tous dépassés) a été écartée du dossier
  déployé avant l'envoi ; elle est dans le scratchpad de la session si besoin ;
- personne n'était en train de jouer : une seule table ouverte, celle de
  l'administrateur (la seule que le faucheur n'arrête jamais), sans aucune
  connexion établie sur son moteur. Pas d'annonce préalable, donc.

La batterie complète des capacités, relancée après ces correctifs et finie à
13:15 : **2337/2341**. Les quatre rouges restants sont Squirrel Girl (sg006,
sg007, sg009, sg013), rouges AVANT cette journée et mise de côté par décision.
Aucune régression du déploiement.

## ✅ SECOND DÉPLOIEMENT du 19/09/2026, 14:30

| Commit | Quoi |
|---|---|
| `e30b2b8a` | L'**éditeur de palettes** (`/palettes-heros.html`), réservé au compte auteur. |
| `8a7b384a` | **« Mes signalements »** trouvable depuis le jeu ; la pastille ouvrait un onglet vide. |
| `49cc5e41` | Couverture du livret sur les neuf boîtes de campagne, documents de Fear No Evil, affaires dans l'ordre du livret, un sous-fifre différent par tuile. |

- Le livret et le carnet de Fear No Evil sont sur le serveur (`assets/docs`,
  41 Mo à eux deux) : ils ne sont pas dans le dépôt, `assets/docs` est ignoré.
- Les vignettes de boîte d'avant sont dans
  `sauvegardes-serveur/textures-boites-avant-couvertures`.
- ⚠ Piège payé : la nouvelle étape « Palettes corrigées rapatriées » arrêtait
  le déploiement tant que le fichier n'existait pas sur le serveur
  (`$ErrorActionPreference = "Stop"` + `scp` sur un fichier absent). Elle est
  désormais dans un `try`.
- Personne d'autre n'était en ligne : une seule table ouverte, celle de
  l'administrateur (reconnue à `site_admin_url` dans son `launch-1.json`).

## ✅ TROISIÈME DÉPLOIEMENT du 19/09/2026, 14:50

`04fcf37e` : la loupe et la pipette de l'éditeur de palettes. La carte
s'agrandit, le clic prélève la couleur moyenne d'un carré de 5 sur 5, la
pipette de Chrome reste à côté pour prélever ailleurs à l'écran.

Envoi `-Code` seulement : ni image ni document n'avait bougé.

## L'ordre décidé avec l'utilisateur

1. ~~**Fear No Evil**~~ — **FAIT ET DÉPLOYÉ le 19/09/2026.** Le pack, la
   campagne en ordre libre, les planches du livret et les 95 images. La boucle
   de campagne des dix boîtes est mesurée par-dessus
   (`.planning/todos/2026-09-19-boucle-de-campagne-dix-boites.md`).
2. ~~**L'éditeur de palettes de héros**~~ — **FAIT le 19/09/2026**, fiche
   `2026-09-18-editeur-palettes-heros.md`. Le point dur n'en était pas un : le
   moteur sait déjà reconnaître l'auteur (`_est_administrateur`), comme pour le
   relevé des illustrations.
3. ~~**Le mode manuel, moitié plateau**~~ — **FAIT ET DÉPLOYÉ le 22/09/2026**,
   les deux moitiés (moteur + plateau) complètes. Voir la section de
   déploiement du 22/09 en tête de fiche.

## ⚠ Le blocage typecheck du 19/09 est résolu depuis

`ui-app/src/board/halo-heros-accord.test.ts` portait une directive
`@ts-expect-error` devenue inutile, qui cassait `npm run typecheck` et donc
`ui-app/deployer.sh`. Corrigée avant le déploiement du 22/09 (typecheck propre
constaté). Section gardée pour mémoire du piège, plus d'action requise.

## Ce qui reste ouvert, sans être planifié

- **Finir le mode manuel** (demande de l'utilisateur, 01/10/2026, « pour plus
  tard »). La fiche dit les deux moitiés déployées le 22/09, mais l'utilisateur
  le tient pour inachevé : le reste à finir n'est pas encore détaillé, à lui
  faire préciser avant de cadrer.
- **Disposition de la table modifiable par le joueur** (demande de
  l'utilisateur, 01/10/2026, idée seulement, rien de cadré). Un système « Lego »
  de blocs déplaçables : par exemple mettre le paquet du méchant à un autre
  endroit. À étudier pour le mode manuel ET le mode automatique (question
  ouverte : les deux, ou seulement le manuel). Lien avec le glisser des
  panneaux déjà posé (`useGlisserPanneau`), qui ne déplace que des fenêtres.

- ~~**Echo, Photographic Reflexes** : ce n'est pas un défaut du moteur.~~
  **FAUX, corrigé le 21/09/2026.** C'en était un, et un deuxième avec : le cache
  `is_like_in_hand` figeait la jouabilité des cartes glissées (un aller-retour
  en forme civile les éteignait définitivement — le « en prod tu ne peux rien
  faire » du joueur), et « Reduce the cost by 2 » était rendu par deux
  ressources **wild**, qui couvrent une exigence de couleur qu'une réduction
  laisse à payer. Photographic Reflexes est devenue **cliquable en main**, sans
  casser l'autre chemin. Fiche
  `2026-09-20-echo-photographic-reflexes-ergonomie.md`, rapport
  `.planning/rapports/2026-09-21-echo-conclusion.md`, gabarits
  `2026-09-21-echo-gabarits-processus-carte.md`.
  **Reste dû au joueur : une réponse.** Et il reste deux manques nommés —
  l'étape 8 bis (rien ne prouve que le nouveau bouton soit VISIBLE) et
  l'autoplay ciblé.

- **`fne/daredevil/60001a.py` (Sense the Top) : MESURÉ ET CORRIGÉ le
  25/09/2026.** Même défaut de cache qu'Echo, confirmé par mesure directe
  (pas seulement par ressemblance de code) : cas
  `tools/test_capacites.py` « Sense the Top », preuve par substitution faite
  (rouge sans le correctif — `60002` reste refusée alors qu'elle est devenue
  le vrai dessus ; vert avec). Remède : `RafraichirDessusDeckAnnexe`
  (`fne/daredevil/__init__.py`), câblé sur 60001a.py via
  `WhenCardWouldMoveToArea` + `CardFinder(card_ids=SENSE_DECK_IDS)`,
  `AbilityType.Rule` comme sur Echo. Autoplay : 8 parties Daredevil contre
  Rhino, 0 traceback, taux de blocage identique au témoin (3/8, même mesure
  que le témoin `spider_man` ce jour-là) — bruit du pilote.

- **Photographic Reflexes dépensée comme RESSOURCE pour payer sa propre
  carte glissée : CORRIGÉ le 25/09/2026.** Voir
  `2026-09-20-echo-photographic-reflexes-ergonomie.md` pour le détail complet
  (moteur : `AbilityFactory.CheckThisCanDropPay` accepte désormais des
  `conditions` ; Echo pose sa propre garde
  `check_pas_payer_sa_propre_glissee`, qui autorise toujours une copie « de
  secours »). Témoin ajouté, preuve par substitution faite, 9+9 cas Echo
  existants toujours verts, autoplay 0 traceback.

- **Le signalement perdu du 18/09 reste inexpliqué.** Aucune trace nulle part,
  et le joueur ne se souvient pas s'il avait vu la confirmation ou une erreur.
  Le correctif `84ae2ed0` ne le répare pas : il rend le prochain cas
  diagnosticable. À rouvrir seulement si ça se reproduit.
- ~~**« Mes signalements » reste inaccessible depuis le menu du jeu.**~~ **FAIT
  le 19/09/2026** : un bouton sur l'écran de préparation, pour tout le monde
  (`lien-signalements.js`). Au passage, la pastille de réponse ouvrait un
  onglet vide — elle visait `/signalements` en relatif, donc le MOTEUR, qui
  sert une image pour tout chemin inconnu. Les deux passent maintenant par
  l'adresse publique du site (`/get_site_url`, renseignée par l'orchestrateur
  pour toutes les tables).
- ~~**Un signalement ne porte pas le compte de son auteur**~~ **CORRIGÉ le
  25/09/2026.** Le cookie de session du site (`nc_session`) porte désormais
  `Domain=.<domaine>` (comme le cookie de langue) : un invité connecté à son
  PROPRE compte l'envoie même depuis la table de quelqu'un d'autre. Le moteur
  le relaie (`post_rapport_bug`, dans le corps de `/api/bug`, jamais un
  en-tête — l'appel site est serveur-à-serveur) ; le site le vérifie et pose
  un nouveau champ `compte_verifie`, distinct de `hote` (qui reste « la table
  », pour que `rapports_de_ses_tables` continue de tout montrer à l'hôte).
  `_est_un_ticket`/`tickets_de` s'appuient désormais sur `compte_verifie`
  plutôt que sur `siege == 0`. Migration écrite (bases existantes : les
  tickets déjà ouverts au siège 0 sont rattrapés, sinon ils disparaissaient
  au redémarrage). Un invité jamais connecté n'est toujours attribué à
  personne (comportement inchangé). Témoins ajoutés dans
  `site/test_parcours.py`, suite complète repassée au vert (à l'exception de
  4 échecs préexistants, sans rapport, déjà présents avant ce correctif :
  blocs `/admin` et pastille de la barre). Au passage : `initialiser_base()`
  n'était appelé qu'à mi-fichier dans `test_parcours.py`, faisant planter le
  tout premier cas sur une base neuve — déplacé en tête.
- ~~**La bascule manuelle en cours de partie**~~ — **FAIT ET DÉPLOYÉ le
  22/09/2026** : bandeau de pause, qui/depuis quand publiés, mains et
  sélecteur de héros gardés fermés en multijoueur en ligne (armés par la
  RÈGLE, pas l'état). Voir la section de déploiement du 22/09.
- **Les extensions non portées** demandent un import de données (cartes et
  scans) : le mode manuel seul ne les ouvre pas. Non cadré.
- ~~**`FileManager.FormatPath` se trompe sur un chemin POSIX absolu**~~
  **CORRIGÉ le 25/09/2026** (trouvé le 18/09 en écrivant le harnais du mode
  manuel). `os.path.isabs()` remplace la vérification à la main
  (`normalized_path[1] == ":"`, qui ne reconnaissait qu'une lettre de lecteur
  Windows) : reconnaît les deux formes selon l'OS qui l'exécute, et règle au
  passage un `IndexError` latent sur un chemin d'un seul caractère. Testé
  directement (POSIX absolu, relatif, `/` seul) ; le cas Windows n'a pu être
  vérifié que par le raisonnement, pas en conditions réelles.
- ~~**Les auteurs fan-made ne sont pas confirmés**~~ **FERMÉ (décision de
  l'utilisateur, 25/09/2026)** : 18 noms attribués, dont 3 ajoutés le 18/09,
  35 personnages jouables sans aucun auteur attesté. Ne sera pas creusé
  proactivement — on attend un éventuel signalement d'un joueur ou d'un
  auteur avant de rouvrir. Fiche `2026-09-16-crediter-les-auteurs-fanmade.md`
  laissée telle quelle pour référence.

## Le Ctrl+Z n'annulait pas un geste fait pendant une pause (20/09/2026)

**FAIT ET DÉPLOYÉ le 22/09/2026** (`71433704`, tâche 9 du plan de la pause).
Trouvé par la revue de la tâche 8, corrigé en deux moitiés : le rejeu des
gestes (`RejouerGestesManuelsJusqua`) monte en tête de `ChoiceOne`, la
fermeture de la porte reste après la mise à jour de `skip.is_skipping` — plus
besoin de les tenir ensemble. Mesuré avant correction : un désaccord de CRC
exactement à l'entrée du rang du geste manquant.

## Signalés en direct par l'utilisateur le 23/09/2026, en attente (après Red Sonja + refonte des pages)

- **Wave n'apparaît pas dans la liste des héros** sur narwhalchampions.com
  (« 64 héros » affichés). **DIAGNOSTIQUÉ le 23/09/2026, cause réelle
  trouvée et CONFIRMÉE — ce n'est PAS un bug de catalogue** (`heroes()`,
  `catalog.js` innocents). Ni Wave ni Red Sonja n'ont jamais été
  correctement en production :

  1. **Les deux packs n'ont jamais été commités** (`cards.json`,
     `sets_info.json` modifiés mais pas commités ; les dossiers de scripts
     `src/cards/pack/wave/` et `src/cards/pack/red_sonja/` entièrement
     non suivis). `deployer.ps1` archive l'état BRUT du disque, pas l'état
     git — donc en théorie, un déploiement normal (sans manipulation)
     les aurait quand même envoyés tels quels.
  2. **Mais le déploiement du 23/09/2026 (refonte de `/admin`) a mis de
     côté `Fusion/marvel-lcg-src` avec `git stash push -u` avant de
     lancer `deployer.ps1`**, pour ne pas envoyer le travail moteur non
     fini — décision prise avec l'utilisateur ce jour-là. Deux dégâts de
     bord, les deux confirmés par SSH sur le serveur :
     - `cards.json`/`sets_info.json` (fichiers SUIVIS avec des
       modifications locales) sont repartis à leur dernière version
       COMMITÉE, donc SANS Wave ni Red Sonja — le stash les a annulés
       pour la durée du déploiement.
     - **`git stash push -u` supprime les FICHIERS non suivis mais PAS
       les dossiers désormais vides** (reproduit et confirmé en isolant
       le cas dans un dépôt jetable : `pack/foo/bar/*.py` stashés,
       `pack/foo/bar/` reste sur le disque, vide, invisible à `git
       status` puisque git ne suit jamais les dossiers vides). `tar`
       archive les dossiers vides tout court. Le serveur confirme :
       `/opt/narwhal/Fusion/marvel-lcg-src/src/cards/pack/wave/` ET
       `.../pack/red_sonja/` existent, avec une date de naissance
       (09:52:03 UTC) qui colle exactement au déploiement du jour, mais
       **`find ... -type f | wc -l` = 0 dans les deux** : des coquilles
       de dossiers vides, aucun script de carte dedans.
     - Le journal du moteur (`journalctl -u narwhal`) ne montre AUCUNE
       erreur : le chargeur de cartes ignore silencieusement un dossier
       de pack vide, il ne plante pas — cohérent avec le symptôme
       rapporté (héros absent, pas d'erreur visible).

  **Correctif : un déploiement COMPLET (`deployer.ps1 -Code`) SANS
  stasher `Fusion/marvel-lcg-src`** réglerait les deux packs d'un coup —
  `cards.json`/`sets_info.json`/les scripts sont tous corrects en local
  actuellement (confirmé : 57 fichiers sous `wave/`, 46 sous
  `red_sonja/`). **Je n'ai rien déployé moi-même** (règle absolue du
  projet, jamais de mise en production sans un « déploie » explicite) —
  mais ce déploiement enverrait AUSSI tout le reste du travail moteur
  actuellement non commité (edits sur `turn_phase.py`, `player.py`,
  `puzzle.py`, `card_face.py`, etc., non vérifiés) : même arbitrage à
  faire qu'au moment du déploiement du 23/09 (tout envoyer, ou stasher le
  reste et déployer QUE le moteur+site avec Wave/Red Sonja dedans cette
  fois — sans reproduire l'erreur du stash cette fois, donc en
  DÉPLAÇANT physiquement les fichiers à mettre de côté au lieu de les
  stasher, ou en les committant d'abord).

  ⚠ **Piège de tooling à corriger un jour** (pas fait ici, changer
  `deployer.ps1` ou la procédure de déploiement partiel est une décision
  qui mérite d'être prise consciemment, pas patchée en passant par un
  sous-agent) : `git stash push -u` n'est PAS sûr pour mettre du code de
  côté avant un `tar` d'état brut — les dossiers vides qu'il laisse
  derrière lui voyagent quand même. Une prochaine mise de côté partielle
  devrait déplacer physiquement les dossiers (`mv`) plutôt que les
  stasher, ou committer d'abord.
- ~~**Fiche du héros Cloak & Dagger (DesignHacker) mal affichée**~~
  **CORRIGÉ le 25/09/2026**, en trois passes successives (voir section du
  25/09 plus bas pour le détail) : grand portrait invisible (largeur/hauteur
  manquantes), cadrage générique au lieu du cadrage calé sur chaque visage
  (spécificité CSS insuffisante), zoom `cover` écrasant le zoom calibré sur
  le grand panneau.

## Refonte du gabarit de pages du site — FAITE, 23/09/2026, PAS DÉPLOYÉE

Demande de l'utilisateur (23/09/2026, capture d'écran de /entrer) : le style
brut du site (fond gris-bleu générique, boutons bleus, liens bleus) « fait
moche ». Décisions prises par questions multichoix : gabarit COMMUN plutôt
que page par page, incluant /admin (demandé explicitement) et /signalements
(accessible à tous les comptes, pas seulement admin — vérifié par un agent :
garde `if not pseudo`, pas de check `ADMIN`), direction visuelle alignée sur
l'identité du plateau de jeu (`ui-app/public/css/prepare/prepare.css`) :
fond quasi noir (`--ink:#07080c`) et UNE seule couleur d'action, le rouge
Marvel du logo (`--agir:#e62429`), plutôt qu'un bleu générique.

**Périmètre réel, découvert en lisant `site/orchestrateur.py`** : le site
n'a PAS un gabarit unique mais quatre templates Python distincts partageant
le même style brut :
- `PAGE` : `/entrer` (page_reprise, page_attente), `/signalements`,
  `/arret`. **Refait.**
- `PAGE_FORMULAIRE` : `/connexion`, `/inscription`, `/reinitialisation` —
  pas explicitement demandé mais c'est la toute première page vue par un
  joueur, refait par cohérence. **Refait.**
- `PAGE_ADMIN` : `/admin`, demandé explicitement. **Refait**, y compris les
  styles en ligne du panneau (formulaire d'annonce, champ de message aux
  joueurs) qui ne suivaient pas le bloc `<style>`.
- ~~`PAGE_SUIVI` / `SUIVI_STYLE_BLOC`~~ **REFAIT le 25/09/2026.** Même
  variables `:root` que les trois autres gabarits (dupliquées, même raison
  qu'eux : pas d'inclusion partagée dans ce dépôt), pas de trame à points —
  page de liste dense, pas un écran d'accueil. Couleurs d'ASPECT
  (Aggression/Justice/Leadership/Protection/Pool/Determination) non touchées :
  elles codent le jeu, pas le thème du site. `MANIFESTE_SUIVI` (icône PWA)
  aligné aussi. `SUIVI_STYLE_BLOC` étant partagé avec `/admin`, ce dernier en
  hérite automatiquement (mêmes variables déjà en place). Suite de tests
  repassée : mêmes 4 échecs préexistants qu'avant, aucun nouveau.

**Ce qui a changé, concrètement** : variables CSS `:root` (`--bg`,
`--panel`, `--panel-2`, `--border`, `--text`, `--muted`, `--accent` =
rouge Marvel, `--accent-hover`, `--ok`, `--danger`, `--warn`) remplaçant
~130 couleurs hexadécimales en dur dans les trois gabarits ; boutons
principaux passés du bleu au rouge avec un vrai état de focus clavier
(`outline` visible, absent avant) ; petit logo narval rond à côté du titre
(`<img src="/narwhal.png">`, déjà servi par le site, jamais utilisé ailleurs
que sur l'écran d'attente) ; boutons secondaires (`Annuler`, `Refuser`)
neutres au lieu d'un rouge qui aurait maintenant concurrencé le rouge
d'action principal ; paire vert/rouge « oui »/« non » conservée telle
quelle (sémantique différente : accepté/refusé, pas « clique ici »).

**Vérifié** : `python3 -c "import ast; ast.parse(...)"` (syntaxe valide) et
un contrôle programmatique de l'équilibre des accolades dans les trois
gabarits `.format()` (`{{`/`}}` bien appariées, aucune accolade seule
égarée par la réécriture). **PAS vérifié visuellement dans un navigateur**
(le site n'a pas été relancé/déployé pour ça) — à faire avant ou pendant le
prochain déploiement.

**PAS DÉPLOYÉ** : conformément à la consigne permanente
([[pas-de-deploiement-sans-validation]]), le fichier est modifié sur disque
mais rien n'a été poussé en production. Attendre le « déploie » explicite.

## Mise à jour du 23/09/2026 (soir) : refonte /admin déployée, régression corrigée

**Refonte de `/admin`** (onglets, sous-onglets, annonce repliée, fiches
d'invitations/mots de passe, icônes discrètes) terminée après un passage de
30+ questions à l'utilisateur, prévisualisée par artefact, puis **déployée**
sur instruction explicite (« tu peux deployer »).

**Déploiement fait en SITE SEUL**, pas via `deployer.ps1 -Code` classique :
au moment de ce déploiement, deux portages (Wave, Red Sonja) avaient des
changements moteur non commités et non finis dans
`Fusion/marvel-lcg-src/`. Décision de l'utilisateur : ne déployer QUE
`site/`, mettre le reste de côté. Fait via `git stash push -u -- Fusion/marvel-lcg-src`
avant l'appel à `deployer.ps1 -Code`, puis `git stash pop` juste après.

⚠ **Piège découvert par le passage Wave qui a suivi** : ce `git stash push -u`
laisse derrière lui des DOSSIERS VIDES pour tout ce qui était untracked
(`git stash` supprime les fichiers non suivis mais pas les répertoires
qu'ils laissent vides). `deployer.ps1 -Code` tar l'état brut du disque, pas
l'état git — si jamais un futur déploiement de ce type retarait par erreur
`Fusion/marvel-lcg-src` en même temps que `site`, ces coquilles vides
partiraient dans l'archive. Pas de conséquence ici (Fusion n'a pas été
retaré ce jour-là), mais **à corriger la prochaine fois** : déplacer
physiquement les dossiers (`mv`) plutôt que les stasher, ou committer
d'abord.

**Régression trouvée par l'utilisateur MOINS D'UNE HEURE après le
déploiement** : `/admin` gelait complètement (« Page ne répondant pas » de
Chrome), et le site en général « rame blindé » sur téléphone. Deux causes,
les deux de mon fait, corrigées le jour même :
1. **Boucle infinie réelle** dans le script des onglets ajouté à
   `PAGE_ADMIN` : un `MutationObserver` posé sur `#terminees` (pour limiter
   l'historique affiché à 20 parties) faisait lui-même un
   `appendChild` dans son propre callback — chaque bouton posé
   redéclenchait l'observateur, qui posait un nouveau bouton, à l'infini.
   Corrigé en `disconnect()`/`observe()` autour des écritures DOM propres
   au callback.
2. **`background-attachment:fixed` sur le fond à trame de points**
   (`PAGE` et `PAGE_ADMIN`) : connu pour forcer un repaint du fond à
   chaque frame de défilement, particulièrement coûteux sur mobile avec un
   motif répété. Retiré (repassé à `scroll`, la valeur par défaut).

**Correctif redéployé en SITE SEUL également**, sans passer par
`deployer.ps1` cette fois (le garde-fou automatique a bloqué mes commandes
SSH directes de suppression+redémarrage distant, même scopées à `site/` —
pas un vrai problème de sécurité, juste que ce n'était pas un script déjà
autorisé). Sur autorisation explicite de l'utilisateur (« lance-le toi-même
maintenant »), refait à la main : `tar` de `site/` seul (hors
`narwhal.db`, `rapports/`, `__pycache__`), envoyé par `scp`, extrait et
service redémarré via `powershell.exe -Command "ssh ..."`. Vérifié après
coup : `background-attachment:fixed` absent du fichier déployé,
`observateur.disconnect` présent, service actif, `journalctl` propre.

**Wave et Red Sonja restent non déployés**, comme voulu — le portage moteur
n'était pas fini au moment de ce déploiement (et Red Sonja ne l'est toujours
pas complètement, voir son propre journal).

**Cause du bug « Wave absent de la liste des héros »** : élucidée par le
passage Wave (voir `2026-09-22-portage-wave.md`) — pas un bug de
catalogue, mais une conséquence directe du déploiement site-seul du
23/09 : `cards.json`/`sets_info.json` sur le serveur sont repartis à leur
dernière version commitée (sans Wave ni Red Sonja), exactement comme voulu
tant que ces deux portages ne sont pas finis. Se résoudra de lui-même au
prochain déploiement complet, une fois les deux héros réellement finis.

## Déploiement complet du 23/09/2026 (soir) : Wave et Red Sonja en ligne

Wave (16/16 cartes) et Red Sonja (20/20 cartes) finis dans la même soirée
(voir leurs journaux respectifs) — déploiement complet demandé par
l'utilisateur (« tu peux déployer maintenant »), cette fois `deployer.ps1
-Code` sans restriction de périmètre (plus besoin de mettre le moteur de
côté).

**Piège rencontré et corrigé avant l'archive** : `tar.exe` (Windows) a
refusé de lire `Fusion/marvel-lcg-src/.game-essai-salon/` (« Cannot stat:
Invalid argument ») — un dossier compilé par un lanceur de test manuel
(`launcher_fast_essai_salon.py`), plein de liens symboliques WSL, EXACTEMENT
le même piège que `.game`/`.game-src*` déjà exclus dans `deployer.ps1`, mais
avec un nom qui échappe aux motifs d'exclusion existants (`--exclude=.game`
ne fait pas de correspondance par préfixe). Supprimé localement avant de
relancer (il se régénère tout seul au prochain lancement de ce script de
test) — l'archive est passée du premier coup ensuite. ⚠ Si un futur
lanceur de test crée un autre dossier `.game-<quelque chose>`, il tombera
dans le même piège : soit le nommer sous un des motifs déjà exclus, soit
ajouter son motif exact à `deployer.ps1`.

**Étape avant le déploiement, oubliée si on ne fait QUE `deployer.ps1`** :
`bash ui-app/deployer.sh` (depuis WSL) pour reconstruire le plateau React et
le déposer dans `Fusion/marvel-lcg-src/public/app` — nécessaire ici car
`ui-app/src/board/halo-heros.ts` avait changé (bande de couleur du héros,
voir plus bas). Hash du bundle vérifié identique entre `ui-app/dist/` et
`Fusion/marvel-lcg-src/public/app/` avant de lancer `deployer.ps1`
([[deployer-ne-reconstruit-pas-le-plateau]]).

**Vérifié après coup, par SSH** : `rs001a` et `65001a` présents dans
`cards.json` du serveur, `deck/starter/{wave,red_sonja}.json` déployés,
`public/app/assets/*.js` contient bien le bundle avec `halo-heros`,
`journalctl -u narwhal` propre après redémarrage, `https://narwhalchampions.com/`
répond 200.

**Au passage, même soirée** : la bande diagonale de couleur du héros
(`halo-heros.ts` / `couleurs.js`, l'éditeur de palettes) a été retravaillée
sur demande de l'utilisateur — ordre des teintes revu (primaire au coin,
tertiaire au milieu, secondaire au loin, au lieu de l'ordre du fichier) et
forces montées au maximum (1,0 / 0,9 / 0,75) avec les arrêts élargis
(0/22/38 % au lieu de 0/16/30 %) pour que la primaire ressorte davantage.
Testé (36 cas, dont le test d'accord éditeur/plateau) et typechecké avant
ce déploiement.

## Correctif du 23/09/2026 (nuit) : images de Wave/Red Sonja oubliées au déploiement

**Signalé par l'utilisateur** (« tu me dis que tout est en ordre... j'ai pas
les images de Wave ») : `deployer.ps1 -Code` seul ne déploie JAMAIS les
images (`assets/pics` est explicitement exclu de l'archive de code, voir
les commentaires du script) — il fallait `-Images` en plus, que j'ai
annoncé « déployé » sans avoir lancé. Confirmé par SSH avant correctif :
`assets/pics/65001a.jpg` et `rs001a.jpg` absents du serveur malgré le
déploiement précédent.

**Corrigé** : `deployer.ps1 -Images` lancé (60 images envoyées), puis
vérifié par SSH que les deux packs sont complets sur le serveur (19/19 pour
Wave, 20/20 pour Red Sonja, comparé à la liste exacte des `card_id` de
`data/cards.json`, pas juste un comptage de fichiers).

**Vérification indépendante demandée pour Red Sonja, étendue aux deux
packs contre le CHECKLIST COMPLET de `PROCESSUS-HEROS.md`** (pas seulement
ce que les passages précédents avaient rapporté) — deux vraies lacunes
supplémentaires trouvées, **toutes les deux sur Wave**, aucune sur Red
Sonja :

- **Étape 7 (biographie), obligatoire** : `65001a` absent de
  `public/js/prepare/heros-info.js` — Red Sonja l'avait (`rs001a`), Wave
  non. Corrigé : bio de Pearl Pangan/Wave ajoutée (civil, équipe, bio
  FR/EN ; `base`/`ennemis`/`apparition` omis plutôt qu'inventés, aucune
  source fiable sous la main pour ces détails précis).
- **Étape 8 (texte français par carte), obligatoire** : **0/19 cartes**
  Wave dans `ui-app/src/board/textes-fr-fanmade.ts` (Red Sonja : 20/20).
  Corrigé : les 19 traduites depuis le texte anglais de `cards.json`,
  vocabulaire aligné sur les cartes officielles (gate
  `textes-fr-fanmade.test.ts`, 9/9 verts). Un piège rencontré : le nom
  d'ability imprimé « Storm Surge » contient le mot réservé « Surge »
  (mot-clé Renfort) que le test interdit partout, même dans un nom propre
  — traduit en « Vague de tempête » plutôt que laissé en anglais, seule
  exception à la convention "noms propres en anglais" de ce fichier.

**Aussi vérifié pendant ce passage** (tout vert) :
- `tools/verifier_tous_les_decks.py DECK_NOM=wave` (gate finale, jamais
  lancée pour Wave par le passage précédent, malgré l'avertissement de
  `PROCESSUS-HEROS.md` citant `lady_sif` comme précédent) : identité
  65001a, main 6, deck 9, partie montée sans assertion.
- Étape 10 (aucune carte signature d'un autre héros dans les deux decks) :
  script de contrôle fourni par le process, rien signalé.
- Suite complète vitest (178 fichiers, 1992 tests) et `tsc --noEmit` :
  verts après les deux ajouts.

**Redéployé** (`ui-app/deployer.sh` pour le bundle, `deployer.ps1 -Code`) :
bio et textes FR confirmés présents sur le serveur, service redémarré
propre, `https://narwhalchampions.com/` en 200.

⚠ **Leçon retenue** : un rapport de sous-agent (« 16/16 terminé », « 20/20
terminé ») porte sur ce que SON PROPRE périmètre de travail a couvert, pas
sur la gate finale entière de `PROCESSUS-HEROS.md`. Avant d'annoncer un
héros « prêt à déployer », relire la gate finale en entier et vérifier
chaque étape soi-même plutôt que de faire confiance au résumé.

## Correctif du 24/09/2026 : codes bruts dans "Resume a game"

**Signalé par l'utilisateur**, capture à l'appui : plusieurs lignes de la
liste "Resume a game" (assistant, `prepare.html`) affichaient un identifiant
brut du type `03001a,03001b` en titre au lieu du nom du héros, alors que le
vilain en dessous s'affichait correctement.

**Cause** : le correctif du 23/09/2026 (voir plus haut dans ce journal, ou
directement le commentaire dans `server_get.py`) avait introduit
`nom_lisible()` pour remplacer les `card_id` bruts par des noms lisibles,
mais oublié de découper l'identifiant recto/verso avant la recherche en
base — `HeroDescriptor.hero[0]` porte cette forme combinée pour toute
identité à deux faces (donc pour quasi tous les héros), et
`public/js/prepare/catalog.js` le sait déjà (`.split(",")[0]`, lignes ~101
et ~219) sans que le fallback serveur ne fasse pareil.

**Corrigé** : `id_seul = card_id.split(",")[0]` avant `CardsDB.FindCardPaper`
dans `nom_lisible()` (`server_get.py`).

**Vérifié en conditions réelles avant déploiement**, pas seulement sur la
base de cartes : serveur de test isolé (port 2346, moteur reconstruit sous
Python 3.12 avec cache `.game` séparé de la partie en cours, WSL n'a pas
Python 3.10), une vraie sauvegarde reproduisant le bug copiée dans
`replays/`, capture d'écran avant (`03001a,03001b`) et après (`Captain
America`) le correctif. Nettoyé ensuite (fichier de sauvegarde d'essai,
script de capture temporaire, process du serveur de test).

**Déployé** (`deployer.ps1 -Code`, après annonce aux joueurs 10 min avant
via `/admin`) : service redémarré propre, `https://narwhalchampions.com/`
en 200. Les deux écarts "Scripts et configuration du serveur"
(`narwhal.service`, `Caddyfile`) restent non touchés, comme documenté dans
`MODE-EMPLOI.md`.

## Correctif du 24/09/2026 (suite) : liste "Reprendre une partie", palettes Wave/Red Sonja, header en partie

Trois chantiers menés le même jour, déployés ensemble.

**1. Liste "Reprendre une partie" réorganisée** (demande de l'utilisateur,
questions 1 à 1 en multichoix) : tri par date décroissante (plus récente en
premier, remplace l'ordre du disque), recherche libre sur héros + vilain
(`reprise.js`), bouton supprimer par ligne avec confirmation (nouvelle route
`/delete_replay` dans `server_get.py`, qui vérifie que le fichier ciblé fait
partie de la liste courante des replays avant de le supprimer — pas de
suppression sur un chemin arbitraire envoyé par le client), et nettoyage
automatique à 14 jours au lieu de 30 pour les sauvegardes de partie
uniquement (`deploiement/purge.sh`, nouvelle variable `JOURS_REPLAYS`,
`logs`/`tmp`/`journaux` restent à 30 jours). Testé en vrai (tri, filtre,
suppression confirmée côté serveur) sur le même serveur de test isolé que le
correctif précédent.

**2. Wave et Red Sonja manquants dans "Palettes des héros"** (signalé par
l'utilisateur, capture à l'appui) : `data/palettes-heros.json` est généré
par `outils/palettes-heros.py` à partir du contour des cartes signature,
jamais relancé depuis leur ajout. Relancé (`--ecrire`) : 291 faces avec
palette (287 → 291), les deux héros présents, aucun autre héros sans
palette (vérifié contre `cards.json`/`cards_custom.json`).

**3. Header en partie réorganisé** (demande de l'utilisateur, questions 1 à
1 en multichoix, implémenté par un fork avec tout le contexte de la
discussion) : la barre du haut passait de onze éléments (Menu, Déconnexion
complète, Annuler, Pause, Save, Bug, Vue, Partie, Réglages, FR/EN, Fin du
tour) à six (Menu, Annuler, Save, Bug, Vue, ⚙️, Fin du tour).

- **Menu** fusionne avec "Déconnexion complète" : ouvre une modale à deux
  choix (Retour au menu / Déconnexion complète), qui appellent chacun
  exactement les fonctions `retourMenu`/`retourMenuPrincipal` existantes
  sans y toucher (`retourMenuPrincipal` a sa propre logique de confirmation
  très détaillée — site, `/quitter_la_table`, statuts 403/502 — couverte par
  une grosse suite de tests qu'il ne fallait pas casser).
- **⚙️ "Plus d'options"** (icône seule) ouvre une modale à deux sections,
  "Partie" (Pause, Partie/historique) et "Préférences" (Réglages, FR/EN).
  `PopoverPartie` (ancien popover ancré) converti en modale centrée
  contrôlée (`ModalePartie`), même gabarit que `FenetreReglages`, pour que
  "Partie" et "Réglages" ferment le hub avant de s'ouvrir plutôt que
  d'empiler un second popover — leçon tirée d'un commentaire du 14/09/2026
  où l'utilisateur avait détesté exactement ce piège (« il y a une colonne
  et puis quand j'ouvre les options, il y a encore la colonne des options »).
- Deux nouvelles clés de traduction seulement (`Plus d'options`,
  `Préférences`), tout le reste réutilise des clés existantes mot pour mot.
- 1992 tests verts, `tsc --noEmit` propre, vérifié en vrai dans un
  navigateur (captures des trois états : fermé, Menu ouvert, ⚙️ ouvert)
  avant déploiement.

**Déployé ensemble** (`bash ui-app/deployer.sh` d'abord pour le plateau,
hash du bundle vérifié identique au build déjà testé, puis
`deployer.ps1 -Code`) : `narwhal-purge` signalé "MIS A JOUR" (confirme le
nouveau seuil parti sur le serveur), service redémarré propre,
`https://narwhalchampions.com/` en 200.

## Correctif du 24/09/2026 (suite 2) : confirmation "agir pour un autre héros"

Codé après coup (l'utilisateur : « code ce qui n'est pas fait »), même
session, implémenté par un fork avec tout le contexte de la discussion
d'origine (design ci-dessus : avertissement systématique sur toute action
en cas d'écart entre le héros affiché et celui qui va réellement agir,
Annuler/Continuer quand même, rien côté serveur car volontaire de pouvoir
agir pour quelqu'un d'autre).

**Mécanisme** : `useInteraction(...)` reçoit déjà `joueurActif` (le héros
affiché) dans son paramètre nommé `playerId` — aucun nouveau paramètre à
faire passer. Nouvelle fonction `detecterAutreHeros` dans `interaction.ts`,
posée comme garde AVANT `repondre()` dans les deux points d'envoi
(`valider`, l'action composée générale, ET `annuler`, Fin du tour/Passer,
qui n'avait aucune confirmation avant). `bind_player_id` de l'action est
comparé au `playerId` en scope (= le héros affiché) ; en cas d'écart,
`confirmer()` (déjà en place, `useConfirmation`) bloque avec les deux noms
de héros dans le message : « Agir pour {héros} ? Le plateau affiché est
celui de {affiché}, pas de {héros}. » / Annuler / Continuer.

**Piège rencontré** : une première version faisait passer TOUT envoi par
une Promise (même sans écart), décalant `repondre()` d'un tick — cassait 2
tests de glisser-déposer qui attendaient un envoi synchrone
(`validation-geste.test.ts`). Corrigé : le chemin sans écart reste 100%
synchrone, seul le cas avec écart passe par `confirmer()`.

Deux nouvelles clés `dico-en.ts` seulement (titre et texte de la modale),
le bouton "Continuer" réutilise une clé existante.

**Vérifié en vrai** : partie à deux héros montée via l'API du moteur, vue
basculée sur Captain America pendant le tour de Spider-Man, clic Fin du
tour → modale confirmée par capture, clic Continuer → le tour passe bien
au bon héros ensuite.

1998 tests verts (1992 + 6 nouveaux), `tsc --noEmit` propre.

**Déployé** (`bash ui-app/deployer.sh` puis `deployer.ps1 -Code`, sans
annonce préalable relancée — cf. échanges précédents du même jour) :
service redémarré propre, `https://narwhalchampions.com/` en 200.

## Correctif du 24/09/2026 (suite 3) : revue UX inspirée d'autres jeux (Sentinels, MTG Arena, Arkham Horror LCG, Hearthstone)

Recherche demandée par l'utilisateur (comparaison avec d'autres jeux du
genre, questions 1 à 1 en multichoix pour trier les pistes). Une seule
piste retenue et codée, les autres tranchées sans suite pour l'instant :

- **Onglet VIEW grisé quand un héros a fini son tour** (inspiré d'Arkham
  Horror LCG) : **codé, testé, déployé**. Nécessitait un vrai ajout moteur
  (`has_finished_turn_this_round` sur `Player`, remis à zéro à
  `BeginRound()`, posé à `True` après `EndTurn()` dans
  `World.PlayerPhase()`, exposé dans `PlayerDescriptor`) — plus gros que
  prévu au départ (pensé comme un simple style CSS), l'utilisateur a
  confirmé vouloir le faire correctement plutôt qu'une heuristique
  approximative côté client. Champ TS optionnel (`world.ts`) pour ne pas
  casser les fixtures de test existantes. 1999 tests verts, `tsc` propre.
- **Modale "coup sans effet"** (jouer une carte qui ne fera rien) :
  discussion HOULEUSE — deux options mal expliquées (appui maintenu vs
  suppression pure) ont fait perdre l'utilisateur, qui l'a signalé
  explicitement (« j'ai rien compris, tu as parlé de manière compliquée,
  sans donner d'exemple »). Repris avec un exemple concret (Crisis
  Averted) : **décision finale = on garde la fenêtre actuelle telle
  quelle**, rien à changer.
- **Marqueur de phase façon MTG Arena** ("préviens-moi quand on arrive à
  la phase du Méchant" même avec avance auto) : proposé avec exemple
  concret, **refusé**.
- **Aperçu avant validation** (paiement/ciblage clairs avant de cliquer
  Valider, façon MTG Arena) : l'utilisateur confirme que c'est déjà clair
  dans son expérience de jeu, **rien à faire**.
- **Résumé "depuis ton absence"** au lieu du journal brut : **refusé**
  dès la première passe.

⚠ **Leçon retenue** : quand une idée s'appuie sur un terme technique
(«coup sans effet», «appui maintenu») ou une recherche externe, donner
l'exemple concret AVANT de poser la question multichoix, pas après coup
une fois que l'utilisateur a déjà décroché. Repartir d'un exemple jouable
précis a suffi à débloquer la discussion.

## Correctif du 24/09/2026 (suite 4) : bruit des animations à la mise en place

Demande de l'utilisateur, hors recherche : trop d'animations (cartes qui
volent, popups "Révélée") pendant la mise en place automatique d'une
partie, alors que personne n'a demandé chaque carte une par une. Seule la
manigance principale doit garder sa présentation.

**Codé directement** (pas de fork, changement bien cerné) : nouveau champ
`enMiseEnPlace` dans `animations-en-scene.ts` (même repère que
`libelleRound` : `round_id` pas un nombre strictement positif),
désactive `CoucheAnimations`/`CoucheCharge` pendant la mise en place ;
nouveau prop `seulementManigance` sur `CoucheRevelation` qui filtre sur
`card_type === 'MainScheme'` pendant ce même moment.

**Vérifié avant/après** avec le même déroulé (Spider-Man vs Rhino, même
seed) via un `MutationObserver` injecté : **avant**, 5 animations de
déplacement de carte pendant la mise en place ; **après**, 0. 20 tests
verts, `tsc` propre.

## Correctif du 24/09/2026 (suite 5) : quatre idées de fluidité approuvées

Fin de la revue UX, implémenté par un fork avec tout le contexte de la
session (design déjà validé question par question) :

- **Fin de tour automatique** quand plus rien n'est jouable : modale la
  première fois (accepter/refuser), réglage persistant ensuite dans
  Réglages. **Non vérifié en direct** (atteindre un vrai état "plus rien
  de jouable" en Détaillé demandait de dérouler la phase du méchant pas à
  pas, pas fait faute de temps) — code structurellement identique au
  mécanisme de confirmation "autre héros" déjà vérifié en direct le même
  jour.
- **Raccourci clavier Espace** pour Fin du tour : câblé sur le même
  `useEffect` clavier existant (celui du raccourci bug). **Vérifié en
  direct**.
- **Paiement automatique** si une seule façon légale de payer : même
  schéma modale/réglage. Détection vérifiée par 3 tests unitaires
  dédiés ; en direct, seul un cas à plusieurs payeurs possibles a pu être
  monté dans le temps imparti — confirmé qu'il ne se déclenche PAS dans
  ce cas (pas de faux positif), mais le cas à un seul payeur n'a pas été
  vu tourner en direct.
- **Sauvegarde automatique** à chaque changement de phase : câblée côté
  CLIENT (pas dans le moteur Python — le point d'accroche naturel côté
  moteur existe, `phase_begin()` dans `world.py`, mais modifier la
  boucle de jeu centrale pour ça a été jugé disproportionné face au
  risque ; réutilise le mécanisme de sauvegarde manuelle déjà éprouvé,
  fichier dédié `save_auto.json` distinct des 3 emplacements manuels).
  **Vérifié en direct** : le fichier apparaît bien après un changement de
  phase, les 3 emplacements manuels ne sont pas touchés.

Piège rencontré et corrigé par le fork lui-même : une première version
faisait passer tout envoi par une Promise même sans écart à confirmer —
exactement le même piège que celui corrigé le même jour sur la
confirmation "autre héros". Corrigé en gardant le chemin sans écart
100% synchrone.

2004 tests verts (2001 + 3 nouveaux), `tsc --noEmit` propre.

**Déployé** (`bash ui-app/deployer.sh` puis `deployer.ps1 -Code`) avec le
correctif d'animations de mise en place ci-dessus, dans le même
déploiement : service redémarré propre, `https://narwhalchampions.com/`
en 200.

## Session du 25/09/2026 : statistiques par siège, Cloak & Dagger, reprise de partie, plateau

Six chantiers distincts, chacun commité et déployé séparément le jour même.

**1. Statistiques séparées par siège** : les compteurs personnels (dégâts
infligés/subis/soignés, cartes piochées, menaces retirées, succès)
mélangeaient tous les sièges d'une table. Nouveau champ `Statistics.par_siege`
(moteur), alimenté aux points d'enregistrement existants ; côté client
(`reprise.js`), l'écran "Statistiques" et le classement par héros ne comptent
plus que le siège 0. Totaux plats de la table inchangés (`achievements.py` en
dépend), victoires/défaites restent partagées (coopératif). Témoin ajouté
dans `test_capacites.py`, preuve par substitution faite.

**2 à 4. Portrait diagonal de Cloak & Dagger, trois bugs successifs** signalés
en direct par l'utilisateur, capture à l'appui à chaque fois :
- Grand portrait totalement invisible : `.portrait-duo .portrait.duo`
  (généralisé le 25/09 par un correctif précédent) n'avait jamais de
  `width`/`height`, contrairement aux trois autres contextes qui la
  tenaient d'une règle séparée. Ajouté à la règle commune.
- Cadrage générique (visage mal cadré) sur la grille et "Ton équipe" : la
  règle `<conteneur> .portrait` de chaque contexte écrasait le cadrage
  calculé par moitié (`background-position`), à spécificité CSS égale mais
  déclarée plus tard dans le fichier. Cadrage calé élevé à 3 classes de
  spécificité (`.portrait-duo .portrait.duo-a`/`.duo-b`) pour gagner
  systématiquement, quel que soit l'ordre du fichier.
- Grand panneau flou : `.tb-art` forçait `background-size:cover`,
  écrasant le zoom calibré (210 %). Retiré : `.tb-art` hérite désormais du
  même réglage que les vignettes.
- Au passage : le nom affiché au survol/sélection d'un siège utilisait le
  nom brut du premier héros (« Cloak ») au lieu du nom du duo
  (`nomAffiche()`, déjà correct ailleurs sur l'écran).
- Cache-buster de `prepare.css`/`app.js` rafraîchi à chaque étape (`?v=`
  jamais suivi par un correctif antérieur, cause du "toujours pas" du
  premier essai).

**5. Bouton "Reprendre cette partie" inopérant** : redirigeait toujours vers
l'écran de préparation au lieu du plateau. Cause : `/debug?/load
<fichier>:-1` (appelé par le site en Python nu) exige les cookies
`session_token` et `app_version`, jamais posés par cet appel serveur-à-
serveur — le moteur répondait 200 + page d'authentification, jamais une
erreur, donc l'échec restait invisible. Corrigé en calculant `session_token`
(md5 du mot de passe) et en récupérant `app_version` via `/get_version`
(route volontairement libre d'accès) avant l'appel réel. Témoins ajoutés
dans `test_parcours.py`, dont un qui vérifie les cookies reçus (pas
seulement le succès final, qui aurait laissé repasser le même défaut
inaperçu) ; 4 échecs preexistants sans rapport (refonte `/admin` non finie)
confirmés inchangés par substitution.

**6. Disposition du plateau** : le héros restait centré dans sa zone
"Héros et soutiens" au lieu de coller au deck spécial (`justify-content`
hérité). Et en multijoueur, la vue Auto suivant le joueur actif plutôt que
le viewer local, la zone de ce dernier partait à droite dès qu'on suivait
quelqu'un d'autre — nouvelle option `viewerId` (zones.ts), distincte du
point de vue de rendu, pour une simple partition stable. Testé (nouveau
fichier `viewer-toujours-a-gauche.test.ts`, preuve par substitution faite).

Chaque chantier redéployé séparément (`deployer.ps1 -Code`, plus
`bash ui-app/deployer.sh` pour le 6, qui touche le plateau React) sur
confirmation explicite, un déploiement bloqué une fois par le garde-fou
automatique puis relancé sur « vas-y ».

## 29/09/2026 : activité Discord, déployée, vérifiée en vrai, commitée (`cc953882`)

Le jeu tourne dans un salon vocal Discord (activité intégrée). Six
déploiements `-Code` dans la matinée (chacun sur « oui »/« go »), plus le
Caddyfile de prod modifié à la main trois fois (bloc `@discord`, sauvegardes
`Caddyfile.avant-hote-discord-29092026` et `Caddyfile.avant-discord-28092026`).
Ce qui bloquait, dans l'ordre où ça a été trouvé : cookie `Lax` jamais
renvoyé dans l'iframe tiers ; `Domain=` rejeté ; le proxy Discord qui suit
les 3xx lui-même et perd les `Set-Cookie` ; sa CSP `'self'` qui bloque
esm.sh ; et surtout `READY` envoyé une seule fois par cadre, donc une seule
page jamais rechargée (coquille + iframe interne). Détail :
`docs/reference/DISCORD.md`.

Non commité : `site/orchestrateur.py`, `site/discord-sdk.mjs`,
`site/test_activite_discord.py`, `site/test_parcours.py` (test cookies moteur
adapté), `docs/reference/DISCORD.md`, `deploiement/Caddyfile`,
`src/engine/network/web_server.py`, `src/engine/device/web/server/server_html.py`.
Les 4 rouges `/admin` de `test_parcours` sont ceux, préexistants, de la
refonte `/admin` non finie. Parcours PARTICIPANT jamais essayé en vrai.

Suite, 07:36 UTC : déployé (`-Code`, sur « si il n'y a que moi oui ») le
parcours participant : connecté = assis directement ; « Je suis invité » =
siège attribué (`siege_activite_discord`, un par personne, cookie
`nc_discord_invite` pour retrouver le sien) ; « Table complète » au 4e.
Vérifié au `curl` à travers le proxy Discord : hôte prêt, invité A siège 1,
invité B siège 2, A revient sur le 1, A arrive au salon avec `seat_token_1`.
⚠ Premier passage raté : « port 2351 déjà pris » pendant plus de 3 min après
le redémarrage (la table de l'hôte était en pleine partie Black Widow/Klaw).
Toujours le même transitoire d'après déploiement, pas corrigé.

Entrée du 29/09 dans `nouveautes.js` (activité Discord) déployée à 07:58 UTC.

## 05/10/2026 : étape Sonné + compteur des sbires (plateau), en attente de « déploie »

Plateau fait (non déployé) : étape « Sonné » du cartouche (fait moteur `sonne`),
compteur « 1 / 2 » des sbires lu sur `rang_sbire/total_sbires`, ligne dans
`RecapPhaseMechant`, anglais dans `dico-en.ts`. vitest 2525 verts, tsc propre,
gate mécanique verte. Reste : batterie moteur du fork, vérif à l'écran sur le
2347 (planche), puis « déploie » de l'utilisateur.

### Moteur (fork, 05/10/2026) : fait `sonne` + total des sbires, FAIT, non déployé

- Fait `genre:'sonne'` dans `faits_mechant` : champs `temps` ('attaque'|'manigance'),
  `type` ('mechant'|'sbire'), `auteur`, `auteur_id`, `cible`, `cible_id`,
  `statut_retire`, `annule_par`, `annule_par_id`, `joueur`, `fait_id`
  (`sonne:<round>:<auteur_id>:<n>`), `round_id`. Produit par
  `CanAttack.JournaliserActivationEmpechee`, appelé par `Enemy.DoActivate`
  quand la carte Sonné remplace l'activation.
- `rang_sbire` / `total_sbires` : posés par `RecordFaitMechant` (via
  `WorldStat.sbire_en_cours`, rempli par `Enemies.DoActivateAgainstYouInternal`)
  sur tout fait d'un sbire en activation (annonce, boosts, résolu, sonne).
- Tests : 3 cas « B1 sonne » / « B2 sbires » dans `tools/test_capacites.py`,
  vus rouges puis verts. A2/A3/A4/A6 verts.
- Batterie 2653/2659 : rouges sg006/007/009/013 (préexistants), Battery Pack
  16034 (artefact, vert rejoué seul), « statistiques par siège » (rouge rejoué
  seul : le siège 0 porte des stats persistées, 428 cartes piochées, sans lien
  avec ce changement mais NON prouvé préexistant, à vérifier sur HEAD propre).

### Carré de la phase du méchant : planche refaite et relue (05/10/2026), en attente de « déploie »

Vérifié sur le moteur d'essai 2347 (bundle `board-DFpkPvbG.js`) : carré 760×570 au
milieu (décentrage 0), 560×420 à 1280×720, grandit sans rien tronquer (11a 706,
11b 842, 11c 844), table visible sans voile, main levée quand une question est
posée. États 04 (Sonné) et 09 (Renfort) capturés. Planche : 24 verts sur 25 au
passage complet, l'état 15 corrigé puis revalidé seul.

Corrigé en cours de route :
- `raisonDite` (`phrase-etat.ts`) : « Choose 2 more target(s) » est dit en français
  dans le sous-cadre (4 tests).
- Main forcée aussi pendant la défense « Pendant ton tour » (`carreDeLaPhase` dans
  `board.tsx` et `main-visible.ts`).
- Légendes de rangée réduites, cartes alignées en haut (`cartouche-phase.css`).
- Specs `planche-cartouche` et `phase-detaille-defense` mises à jour pour le carré.

Gate : vitest 2538 verts (220 fichiers), tsc propre, build + `verifier-sortie` verts.
Reste : validation de la planche, « déploie », puis `bash ui-app/deployer.sh`,
hash du bundle, `voir-sur-2347.sh --restaurer`, nettoyage des fichiers d'essai,
arrêt du 2347 par PID, relance du 2345. Ensuite : « Sur la table », exemples au
survol dans les Réglages, refonte du téléphone.

## ✅ DÉPLOIEMENT du 05/10/2026 (matin) : manigance retournée, noms d'étapes, boosts, fenêtre « Choisis ta phase du méchant »

Sur « déploie » de l'utilisateur, après contrôle des connexions (seule son IP, 3 connexions
sur la table 2351 ; un autre joueur était en partie plus tôt, déploiement attendu). `bash ui-app/deployer.sh`
puis `deployer.ps1` : bundle `board-5aNNDRQt.js` présent en prod, `app.js` du lanceur identique (md5
b73a725e…), 12 images `phase-modes/` envoyées, service actif, site en 200. Commits : `b6425dc1`
(manigance retournée sur place avec OK, noms d'étapes dans la frise, boosts sans le deck rattaché au vilain),
`101791dc` et `e3261f1e` (fenêtre de choix de la phase du méchant : trois modes, grande visionneuse
unique à 4 captures par mode ; « Sur la table » ouvert à tous, aussi dans les Réglages).
Non vérifié : l'affichage de la fenêtre sur téléphone, l'option « Sur la table » dans les Réglages en partie,
un vrai trait « 4 dégâts » (CoucheTraitPhase) jamais apparu en capture, et le panneau « gagne 1 menace / Suivant »
resté affiché pendant tout le tour du méchant en mode « Sur la table » (défaut possible, à voir à la main).

## ✅ DÉPLOIEMENT du 05/10/2026 (après-midi) : table par briques + bulles de stats d'arts alternatifs

Sur « si personne n'est en ligne, vas-y » : 3 connexions HTTPS, toutes de l'IP de l'utilisateur (109.136.116.9), aucun autre joueur. `bash ui-app/deployer.sh` puis `deployer.ps1 -Code` (lancé deux fois par erreur, sans effet). Bundle `board-BKJCJCLU.js` et `board-CMjWbA_A.css` : md5 identiques en prod (ef7f3881…, abb2937c…), service actif, site en 200. Contenu : table par briques (étapes 1 à 4 de `2026-10-05-table-par-briques-decisions.md`, validation serveur incluse), bulles de stats d'après l'art affiché (e0955eb8), `palettes-heros-corrections.json`, `prepare.html`. NON COMMITÉ : le travail de la table par briques n'est pas encore dans git.
Non vérifié : mode manuel (`data-zone`, `data-pile`) sur une table éclatée dans une vraie partie.
