# État du backlog au 21/10/2026 (mise à jour du rapport du 19/10)

**Ceci est une MISE À JOUR du rapport `docs/rapports/etat-du-backlog-2026-10-19.md`, pas une relecture complète à
zéro.** Entre le 19/10 (18h13) et aujourd'hui, 154 commits sont tombés sur la branche de travail
(`sauvegarde-cle-usb-2026-10-14`, HEAD au commit `5e41c99e`), dont une grosse session consacrée à finir Galactic
Storm, une vague de corrections du pack Dazzler, la refonte connexion/inscription, la coop locale, et le cadrage
de trois gros chantiers (Punisher, jeu installable, langues).

Méthode : pour chacun des 31 items OUVERT du rapport du 19/10, un `git log --since="2026-10-19 18:13"` ciblé par
mots-clés + un grep sur les fichiers cités dans la colonne « Preuve » de l'ancien rapport. Moins approfondi que
l'audit original (qui avait relu les 176 fiches une par une) : cette passe ne revérifie QUE les 31 items ouverts et
confirme/infirme leur statut, elle ne refait pas le tri des fiches « FAIT mais pas à jour » ni des « INCERTAIN ».

---

## 1. Résumé

- **Galactic Storm (ex-item 15) est CLOS** depuis le 21/10/2026 (voir section 1 bis). C'est le changement le plus
  important depuis le 19/10.
- Sur les 31 items ouverts du 19/10 : **9 sont maintenant clos** (2, 3, 7-partiel, 8, 9, 12, 15, 27, 28), **1 a
  nettement avancé sans être clos** (21, questions posées à l'utilisateur), **1 a légèrement avancé** (13, Zeus et
  Echo levés, Fleeting/Alias en question), **2 progressent côté cadrage sans code livré** (14 Punisher, 19/20
  volontairement laissés au backlog par décision du 20/10). Les 18 autres n'ont pas bougé.
- **Items ouverts restants : 20** sur les 30 non-Galactic-Storm (voir section 2), après la revue point par point
  du 21/10/2026 au soir (déploiement réel effectué le même soir, commit `6dc43bb6` puis `ad118548`) :
  - **1(i) palettes** : pas un défaut — le sens unique (serveur → dépôt) est volontaire et documenté dans
    `deployer.ps1:168-174` (l'éditeur `/palettes-heros.html` écrit sur le serveur, l'envoyer depuis le poste
    écraserait le travail en ligne). Aucun code changé.
  - **1(h) défaut d'Assaut** : clos par le déploiement réel du 21/10 au soir (le fix `147d783a` du 19/10 était déjà
    en attente de déploiement, maintenant confirmé en ligne : site et `play.` à HTTP 200, plateau identique).
  - **18 (nom de set Hunting Season)** : corrigé (`ad118548`). Vraie course entre l'appel `api.encounterSet()` et
    la pose du cookie `app_version` (un `get_version` en parallèle) : le serveur répond sa page « Version
    Mismatch » à la place du JSON, et aucun réessai n'était tenté. Un seul réessai 400 ms plus tard suffit.
  - **11 (decks absents en campagne)** clos sans code : chaîne relue (`DECKS_CAMPAGNE` → `memeHeros`), aucun
    défaut trouvé, et aucun exemple concret de deck manquant n'a jamais été fourni (décision de l'utilisateur).
  - **29 (sons mal placés)** : rien à signaler pour l'instant, reste en l'état.
  - **Bonus hors backlog, trouvé en déployant pour de vrai** : `deployer-linux.sh` avait son propre bug —
    `tar -tzf archive | grep -q motif` sous `set -o pipefail` peut échouer même quand le motif EST présent (SIGPIPE
    de `tar` qui remonte au lieu du succès de `grep`), a bloqué le tout premier essai de déploiement réel avant
    tout envoi au serveur. Corrigé (`6dc43bb6`).
- **Deux champs périmés corrigés dans `tools/prefixes_fanmade.json`** à l'occasion de cette passe : `sk` (Skrull
  Menace) disait « EN COURS, 31 cartes » alors que les 5 scénarios et les 323 cartes sont livrés depuis le 16/10 ;
  `gs` (Galactic Storm) disait « EN COURS, 35 cartes » alors que les 221 entrées de `cards.json` et le mode
  campagne complet sont maintenant clos. Commit `5e41c99e`.
- Les 19 fiches à en-tête périmé (section 3 du rapport du 19/10) **n'ont pas été corrigées dans cette passe**
  (hors budget de cette mise à jour) : la liste reste valable telle quelle, reportée section 3 ci-dessous sans
  changement.
- Les 11 points « INCERTAIN » (section 4 du rapport du 19/10) n'ont pas été revérifiés non plus : reportés tels
  quels en section 4.

---

## 1 bis. Galactic Storm (item 15), détail de la clôture

Terminé le 21/10/2026, preuves :
- **13/13 cartes de campagne** (gs224-gs236) prouvées par substitution 1/1 chacune (`tools/substituer_pack.py`),
  y compris gs224 Rick Jones et gs226 Lauri-Ell dont la preuve restait non concluante au 20/10 (deux pièges de cas
  de test corrigés, et un vrai bug trouvé dans `gs226.py` : `message.damage_targets` n'existe pas, corrigé en
  `took_damage_targets`).
- **Mode campagne complet** : `data/campagnes/galactic_storm.json` + `src/cards/pack/galactic_storm/campaign.py`,
  les 5 scénarios reliés (`*CampaignSetup(N)` sur chaque manigance principale 1A), retrait réel de l'Imperial
  Guard déjà utilisée, remplacement d'allié ciblé. `tools/epreuves_campagnes.py` : 5/5 épreuves de boucle vertes.
- **Autoplay enchaîné des 5 scénarios** (`tools/jouer_campagne_galactic_storm.py`, nouveau) : joue sans planter
  (scénarios 1-3 confirmés, scénario 4 dépasse le minuteur en solo — parties longues déjà connues et acceptées).
  A débusqué un vrai bug moteur (`game/card/card_finder/checker.py`, `AttributeError` sur un Attachement
  « consider_as » Enemy) corrigé au passage — pas spécifique à Galactic Storm, aurait pu toucher n'importe quel
  pack avec le même patron.
- **Pages du livret** (intro/règles/épilogue) découpées depuis le rulebook 1.2 et reliées à l'écran de campagne
  pour les 5 scénarios.
- **Bug de données pré-existant trouvé et corrigé en chemin** : `gs120b` (Shi'ar Throne face B) n'avait aucun
  `desc.Class`, ce qui faisait planter la mise en place complète du scénario 2 — jamais détecté avant faute d'un
  test qui montait cette mise en place en entier.
- **Entrée « Nouveautés »** ajoutée pour les joueurs (`public/js/prepare/nouveautes.js`, 20/10/2026) — absente
  jusque-là contrairement à Skrull Menace et Hunting Season.
- Commits (branche `gs7-earth-under-siege`, poussée sur `master` les 20 et 21/10) : `63419a9f`, `22e3b0bc`,
  `8c768f78`, `716db68d`, `7d4ccf86`, `ba20f4a8`, `5e41c99e`.

Résidus non bloquants, déjà actés avec l'utilisateur plus tôt : 0 % de victoire en solo (IA modeste contre un
contenu pensé pour 2-4 joueurs tournant 3 identités, pas de rééquilibrage demandé), partie manuelle complète par
un humain pas encore jouée (reportée par l'utilisateur).

---

## 2. OUVERT (mis à jour)

Items du rapport du 19/10 reconduits tels quels sauf mention « → MAJ 21/10 ». Les items clos sont retirés du
tableau et listés en tête de chaque sous-section.

### 2.1 Plateau et phase du méchant

**Clos depuis le 19/10** : item 2 (modale de choix collée au panneau hors table — `choix de cibles hors table : le
panneau d'action est collé au-dessus du sélecteur et les deux se déplacent ensemble`, cas mixte traité) ; item 3
(mode manuel, l'agrandissement de la carte se range à gauche du volet d'aide ouvert, captures avant/après).

| # | Item | → MAJ 21/10 | Taille | Dépendances |
|---|---|---|---|---|
| 1 | Restes du déploiement du 19/10 | **Largement fait**, et encore avancé le 21/10 au soir : test `klaw-ameliorations` réparé, texte d'aide aligné sur les boutons, specs corrigées, fenêtre « Choisis ta phase » tranchée, script de déploiement Linux livré ET éprouvé en réel (`deployer-linux.sh`). (h) défaut d'Assaut : **clos**, confirmé en ligne par le déploiement réel du 21/10. (i) palettes : **pas un défaut**, sens unique volontaire (voir section 1, Résumé). **Reste** : (f) « −X PV » affiché au bilan seulement — identifié (constructeur d'étapes animables de `deroule-phase.ts`, pas un simple oubli), reporté après déploiement ; (g) cache téléphone/tablette — mis de côté ; passe complète du tutoiement non faite | petit (2 sous-points) | (g) mis de côté |
| ~~4~~ | ~~Mode manuel : restes de vérification en vraie partie~~ | **CLOS le 21/10/2026** (`ui-check/tests/mode-manuel.spec.ts` rejoué contre un serveur local) : table éclatée OK, carte à deux faces OK, chemin Victoire OK. Un défaut trouvé en route (geste manuel via menu triche appliqué PENDANT une pause sur question ouverte comme le mulligan, jamais publié à l'écran) a été jugé trop pointu par l'utilisateur pour être suivi : abandonné, voir `2026-10-07-manuel-100-pourcent-octgn.md` | — | — |
| ~~5~~ | ~~Relecture et spectateur : voir 100 % de ce que le joueur voit~~ | **RETIRÉ le 21/10/2026**, décision de l'utilisateur. Rien n'avait été commencé | — | — |
| 6 | Table personnalisable : choix par héros en multijoueur | Inchangé, arbitrage utilisateur toujours en attente | moyen | arbitrage préalable de l'utilisateur |
| ~~7~~ | ~~Animations : point 5 et retrait de la garde d'essai~~ | **CLOS le 21/10/2026.** Point 5 fait (au-delà de dix mouvements, un vol groupé au lieu de ne rien animer) et déjà SANS garde pour tout le monde (vérifié dans le code : `CoucheAnimations` n'est conditionné par aucun drapeau d'essai). La garde `essaisOuverts()` restante ne protège en réalité QUE la couleur du halo/des marques (héros + méchant) — pas les animations. Décision de l'utilisateur : la garde reste en place (couleurs encore fausses pour certains héros, item 30 retiré sans correction) | — | — |

### 2.2 Préparation, comptes, salon

**Clos depuis le 19/10** : item 8 (refonte connexion/inscription — en-tête fin, scène 30 %, bandeau mobile,
accents remis sur toutes les pages, « le site est complet » traduit) ; item 9 (coop locale : parcours séquentiel un
héros après l'autre, retour arrière, récapitulatif, repère « Dernier utilisé » — les 3 questions de la fiche
semblent toutes tranchées par le code, à confirmer en jeu).

| # | Item | → MAJ 21/10 | Taille | Dépendances |
|---|---|---|---|---|
| 10 | Données des joueurs : décision en suspens (`lightningmantis`) | Inchangé | petit | décision de l'utilisateur |

### 2.3 Contenu et cartes

**Clos depuis le 19/10** : item 12 (vérification des cartes hors irefrixs — dz004 à dz038 intégralement vérifiées
et corrigées en 6 lots, `im001b` et `wc014` corrigés en portée Round, gabarits PROCESSUS-CARTE et RECETTES §15
écrits).

| # | Item | → MAJ 21/10 | Taille | Dépendances |
|---|---|---|---|---|
| ~~13~~ | ~~Réserves de gabarits PROCESSUS-CARTE~~ | **CLOS le 21/10/2026.** Zeus, Echo et Fleeting/Alias : les trois réserves levées. Fleeting/Alias : les deux questions du 20/10 (`2026-10-20-backlog-13-questions.md`) ont été tranchées PAR L'UTILISATEUR le jour même (Q1→A, Q2→A) et appliquées (deck de test jetable `tools/decks-de-test/fleeting-alias-determination.json`, 24 parties d'autoplay, 2 défauts trouvés et corrigés sur dt105/dt106) : la fiche dit maintenant « Cartes terminées : OUI » pour les 5 cartes (dt087, dt100, dt105, dt106, dt107). **Raphael (biographie)** : vérifiée en vrai (serveur local) le 21/10/2026, s'affiche correctement — dernier point de l'item, désormais clos. Note en passant (hors périmètre de cet item, non corrigée) : `dt112` Spiral et `dt126` Rage partagent le même défaut `change_on_event` que les cartes Fleeting, documenté mais jamais traité, aucun cas | — | — |
| 14 | Campagne Punisher MC×DC 2026 | Cadrage avancé : lot PU-0 (préfixe, mots-clés, données simples), réponses utilisateur aux 8 décisions P1-P8. **Toujours aucun script de carte ni moteur de scénario écrit** | gros | crédits MC×DC à nommer à l'intégration |
| 16 | Crédits des auteurs fan-made, par héros | Inchangé pour `sets_info.json` (toujours aucune entrée « auteur »). **Nuance nouvelle** : les decks fan-made eux-mêmes portent maintenant `metadata.author` (53 decks, commit du 20/10) — une pièce adjacente, mais ne remplace pas l'affichage dans la modale héros demandé par la fiche | petit | validation de la liste par l'utilisateur |
| 17 | Stan Lee : batterie « Marvelous » en pause | Toujours en pause (`marvelous-partiel-0-1461.json` inchangé depuis le 29/09). Un commit sans rapport (« phrase et citation du scan ajoutées ») a touché le même sujet Stan Lee mais pas la batterie elle-même | moyen | consommation de calcul de la batterie |
| ~~18~~ | ~~Mots et textes : « Hs Feral Instincts »~~ | **CLOS le 21/10/2026** (`ad118548`) : course avec le cookie `app_version`, un réessai suffit | — | — |

### 2.4 Infrastructure, distribution, charge

| # | Item | → MAJ 21/10 | Taille | Dépendances |
|---|---|---|---|---|
| 19 | BACKLOG n°1 : jeu « installable » | **Décision du 20/10 : laissé au backlog, pas maintenant** (cadrage fusionné avec Punisher et Galactic Storm dans un même lot de décisions, `docs(cadrage)` du 20/10). Aucun code | gros | décisions déjà actées, reste à lancer le jour venu |
| 20 | BACKLOG n°2 : ajouter des langues | **Décision du 20/10 : espagnol choisi en premier, mais chantier laissé au backlog**, cohérent avec `docs/BACKLOG.md` §2. Aucun code | gros | chantier 19 (poids des scans) |
| 21 | Mode navigateur (Pyodide) : finitions | **Clos le 21/10/2026 au soir**, les 5 questions tranchées (`2026-10-20-backlog-21-questions.md`) : Safari/iPhone hors périmètre (pas d'appareil), Firefox lent accepté tel quel, téléphone réel confirmé OK par l'utilisateur, ouverture publique pas encore, et Q5 (brancher `publier.py`) s'est révélée déjà réglée — `deployer-linux.sh` publie automatiquement play. à chaque déploiement du site, contrairement à l'ancien `deployer.ps1` | — | — |
| ~~22~~ | ~~Tenir plus de joueurs~~ | **CLOS le 21/10/2026**, retiré du backlog par décision de l'utilisateur (« ça marche bien comme ça »). Optimisation faite : `asdict` exact et masqué en une passe, -18 % de CPU par table (commit perf du 20/10), banc de charge du descripteur ajouté. Le banc de charge complet (25-40 tables) n'a jamais été rejoué — il ne donne des chiffres fiables que lancé contre le vrai serveur, hors heures de jeu, bots sur une autre machine (fiche `2026-09-16-tenir-plus-de-joueurs.md`) ; jugé pas nécessaire pour l'instant | — | — |
| 23 | Archivage des tickets de bug | Inchangé | petit | aucune |

### 2.5 Mis de côté par décision ou très lointain

**Clos depuis le 19/10** : item 27 (nice-to-have Yarro — points a, b, c, d tous faits : écarter des cartes, dégâts
en un coup, raccourcis clavier, glisser-déposer pour permuter) ; item 28 (glisser-déposer du plateau — `onDepot`
maintenant couvert par un vrai geste Playwright, dépôt réussi et refus affiché).

| # | Item | → MAJ 21/10 | Taille | Dépendances |
|---|---|---|---|---|
| 24 | Téléphone et tablette pour la phase « Sur la table » | Inchangé, toujours mis de côté | gros | mis de côté |
| 25 | Mode tablette simple et mode téléphone (suite) | Inchangé, toujours mis de côté | gros | mis de côté |
| ~~26~~ | ~~Mode PvP Arena~~ | **RETIRÉ le 21/10/2026**, décision de l'utilisateur. Très lointain, rien commencé | — | — |
| ~~29~~ | ~~Revoir les sons : quels déclencheurs tombent mal~~ | **RETIRÉ le 21/10/2026**, décision de l'utilisateur. La question ne sera pas posée | — | — |
| ~~30~~ | ~~Revoir les couleurs du halo : validation et envoi des palettes~~ | **RETIRÉ le 21/10/2026**, décision de l'utilisateur. « Jamais envoyées au serveur » n'était pas un défaut (voir item 1(i), sens unique volontaire) ; la passe de validation des couleurs encore fausses ne sera pas faite | — | — |
| ~~31~~ | ~~Recherche de decks MarvelCDB : une vraie partie~~ | **RETIRÉ le 21/10/2026**, décision de l'utilisateur. L'import depuis MarvelCDB fonctionne déjà (confirmé par l'utilisateur) | — | — |

**Items clos ou retirés depuis le rapport du 19/10** : 2, 3, 4, 5, 8, 9, 12, 13, 15, 18, 21, 22, 26, 27, 28, 29,
30, 31 (18 items), plus la moitié de l'item 7 (reste un sous-point). **12 items encore ouverts** : 1, 6, 7, 10,
14, 16, 17, 19, 20, 23, 24, 25.

---

## 3. FAIT mais fiche pas à jour (reporté sans changement)

Les 19 entrées du rapport du 19/10 n'ont pas été revérifiées ni corrigées dans cette passe (hors budget). La liste
reste celle du rapport du 19/10 : mode manuel « comme OCTGN », mode manuel sans automatisation, mode Legacy,
éditeur de deck, salon invité, choix du héros 30/70, mode sobre des menus, écran de campagne « livre ouvert »,
inviter un connecté, table par briques, zones renommables, Luke Cage officiel, contradiction copie vivante,
six défauts priorité absolue du 14/09, revoir les sons, dz003, plan héros/vilains fan-made (à corriger : Skrull
Menace et Galactic Storm y sont maintenant bien marqués FAIT, c'est `prefixes_fanmade.json` qui avait le retard,
corrigé ce jour), roue du hasard, phase du méchant « à améliorer ».

**À faire la prochaine fois** : corriger ces 19 en-têtes pour que le prochain relevé n'ait plus à refaire ce tri.

---

## 4. INCERTAIN (reporté sans changement)

Les 11 points du rapport du 19/10 n'ont pas été revérifiés dans cette passe : déploiement effectif de plusieurs
fonctions livrées les 18-19/10, écart assumé « inviter un connecté », couverture du mode « Accéléré », le mode
navigateur en ligne (partiellement clarifié par l'item 21 ci-dessus, mais l'ouverture publique reste une
décision), « Hs Feral Instincts », recherche MarvelCDB, portée exacte du tutoiement, packs TMNT et Shinobi (hors
`.planning/todos`, non audités ici), test `klaw-ameliorations` (**résolu depuis**, voir item 1), cartouche
« Détaillé » qui déborde, Doctor Doom Alt Arts.

---

## 5. CLOS (mis à jour)

Catégorie « Chantiers et campagnes livrés » : **+1** depuis le 19/10 (Galactic Storm, voir section 1 bis).
Les autres comptages (gabarits, portages, relevés, préparations, bugs corrigés) n'ont pas été revérifiés dans
cette passe — reportés tels quels du rapport du 19/10.

---

## 6. Ordre de reprise proposé (mis à jour)

L'ordre du 19/10 reste globalement valable, Galactic Storm en moins (clos) et avec les nouveaux éléments connus :

1. **Fermer le reste de l'item 1** (−X PV au bilan, confirmer le défaut d'Assaut en ligne, envoyer enfin les
   palettes corrigées au serveur — items 1(i) et 30 sont le même défaut). Petit, presque fini.
2. **Réponses aux 5 questions du mode navigateur Pyodide (item 21)** : bloque une décision d'ouverture publique
   qui ne demande plus que des réponses de l'utilisateur, le travail technique est fait.
3. **Refonte connexion/inscription (item 8) : CLOSE**, retirée de cet ordre.
4. **Coop locale (item 9) : CLOSE**, retirée de cet ordre. Reste à confirmer en jeu que les 3 questions sont bien
   résolues comme le code le suggère.
5. **Décider la technique du jeu installable (item 19)** : toujours le plus gros chantier, toujours en attente des
   arbitrages de l'utilisateur, inchangé depuis le 19/10.

Hors priorités, inchangé : téléphone/tablette (24, 25), campagne Punisher (14, cadrage avancé mais à
lancer), langues (20, après le chantier 19).

À corriger au passage dans la documentation (reporté du 19/10, pas fait cette fois) : les 19 en-têtes de fiches
listées en section 3.
