# État du backlog au 19/10/2026

Document de synthèse, établi en lecture seule le 19/10/2026 sur le commit `6b22e1c5` (tag `sauvegarde-cle-usb-2026-10-14`, branche `etat-du-backlog`). Matière : `docs/BACKLOG.md` (2 chantiers) et les 176 fiches `.planning/todos/*.md` (plus 2 fichiers non Markdown). Les sous-dossiers `.planning/todos/generateurs-fne` (générateurs de cas de test du pack Fear No Evil, avec `qui_reste_vert.py`) et `.planning/todos/pvp-simulation` (simulation jouet du mode PvP) sont des outils : ils ne contiennent aucun item à faire.

Méthode : pour chaque item ouvert candidat, vérification dans le code (`git grep`, lecture de fichiers) et dans le journal git (`git log --all --grep`). Aucun test ni serveur n'a été lancé : une preuve « présent dans le code » ne vaut donc pas « vérifié en navigateur ». Quand le statut n'a pas pu être établi, le mot « incertain » est écrit.

Deux précautions de lecture :
- La branche `master` du dépôt est un ancêtre ancien du tag (1 497 commits de retard). La référence à jour est le tag `sauvegarde-cle-usb-2026-10-14` (dernier commit du 19/10/2026 à 18h13).
- Des fiches sont de vieux journaux dont l'en-tête n'a jamais été mis à jour (voir section 3). Un audit du 07/10/2026 (commits `e7f2158f` et `6af1ab3d`) avait déjà annoté 19 statuts périmés ; ce document le prolonge.

---

## 1. Résumé

- 176 fiches lues par leur statut. 67 sont des journaux de production de cartes (39 gabarits, 15 portages, 8 relevés, 5 préparations de vague 0), tous clos sauf 4 gabarits qui portent une réserve.
- Environ 70 autres fiches sont des chantiers livrés ou des bugs corrigés : clos (comptage approximatif, section 5).
- **Items ouverts : 31** (section 2), dont 9 gros, 7 moyens, 15 petits ou « petit à moyen ».
- Par famille : plateau et phase du méchant (7), préparation, comptes et salon (4), contenu et cartes (7), infrastructure et distribution (5), mis de côté, lointain ou en attente d'une réponse de l'utilisateur (8, dont téléphone et tablette).
- **Fiches dont l'en-tête est faux (fait mais marqué ouvert) : 19** (section 3). Les plus trompeuses : éditeur de deck, salon invité, mode Legacy, mode manuel, « inviter un connecté », choix du héros 30/70, Luke Cage.
- **Incertains : 11** (section 4), surtout des choses jamais vues en navigateur ou en ligne.
- Les deux chantiers de `docs/BACKLOG.md` sont réellement ouverts : aucun code n'existe (le service worker de l'application ne garde rien en cache ; le site n'a que le français et l'anglais).
- « T18 » est annulée, téléphone et tablette sont mis de côté : ces points ne comptent pas dans les priorités.
- La fiche `2026-10-19-restes-apres-deploiement.md` est reprise telle quelle (item 1), avec une vérification de quatre de ses points.
- Les six défauts « priorité absolue » du 14/09 sont traités avec preuves ; seul l'en-tête de la fiche est resté en alerte.

---

## 2. OUVERT

Taille : petit (moins d'une demi-journée), moyen (une à trois séances), gros (plusieurs séances ou décision préalable). Les numéros servent de renvoi dans la section 6.

### 2.1 Plateau et phase du méchant

| # | Item | Source | Ce qui reste à faire | Preuve de vérification | Taille | Dépendances |
|---|---|---|---|---|---|---|
| 1 | Restes du déploiement du 19/10 (phase du méchant, trois choix) | `2026-10-19-restes-apres-deploiement.md` | (a) test ui-check `phase-sur-table-lecture.spec.ts`, cas `klaw-ameliorations` à réparer ; (b) texte d'aide « un « Suivant » par étape » à comparer au bouton ; (c) tutoiement à passer en revue ; (d) fenêtre « Choisis ta phase du méchant » à réafficher ou non (décision) ; (e) specs qui posent `mc_phase_presentation: 'bis'` ; (f) « −X PV » affiché au bilan seulement ; (g) cache téléphone/tablette de la version en ligne ; (h) défaut d'Assaut en ligne non confirmé ; (i) palettes corrigées jamais envoyées en ligne ; (j) script de déploiement Linux | (a) le cas existe, `phase-sur-table-lecture.spec.ts` ligne 9 et 64, non relancé ; (b) `FenetreReglages.tsx:308-309` contient toujours « un « Suivant » par étape » ; (c) confirmé : `public/js/prepare/app.js:1841` et `dico-en.js:989, 1019` contiennent « Tu pourras changer à tout moment… » ; (e) confirmé pour `phase-sur-table-lecture.spec.ts:24` et `phase-sur-table-multi.spec.ts:16` ; les deux autres specs citées ne posent plus `'bis'` (non revérifié plus loin) ; (i) `deploiement/deployer.ps1:174` exclut `data/palettes-heros-corrections.json` de l'archive et `:498-504` le recopie depuis le serveur ; (j) `deploiement/deployer-tout.sh` existe mais la fiche précise que la procédure du 19/10 a été manuelle | petit à moyen (10 sous-points) | décision de l'utilisateur pour (d) et (g) |
| 2 | Modale de choix : bouton de validation collé au panneau et déplacement solidaire | `2026-10-07-modale-de-choix-bouton-colle-et-deplacement-solidaire.md` | Coller le bandeau d'action au panneau « hors table » et déplacer les deux ensemble | **Partiel.** `AssistantAction.tsx:144-160` : le bandeau se déplace à la poignée (signalement Yarro du 28/09), mais rien ne le lie au panneau hors table ; aucun commit « colle » ou « solidaire » | moyen | mécanisme de glisser de `useGlisserPanneau` à réutiliser |
| 3 | Mode manuel : le volet d'aide cache l'agrandissement de la carte | `2026-10-07-mode-manuel-aide-ne-doit-pas-cacher-l-agrandissement-de-la-carte.md` | Placer l'aperçu agrandi à côté du volet d'aide ouvert | `ui-app/src/board/manuel/VoletAideManuel.css` : `z-index: 610` inchangé, aucun commit « aide / aperçu » dans le journal (le commit `8309f2d9` traite un autre cas, la fenêtre de choix de cartes) ; non vu en navigateur | petit | aucune |
| 4 | Mode manuel : restes de vérification en vraie partie | `2026-10-06-mode-manuel-comme-octgn.md`, `2026-10-07-manuel-100-pourcent-octgn.md` | Voir en vrai la table éclatée, la carte à deux faces, le chemin « Victoire », « choisir un set et le mélanger dans le deck Rencontre » (testé en unitaire seulement) | fiches : « tests unitaires seulement : aucune carte mise de côté dans la partie d'essai » ; code présent (commit `3f5171f4`) | petit | une partie jouée à la main |
| 5 | Relecture et spectateur : voir 100 % de ce que le joueur voit | `2026-10-12-relecture-fidele.md` (7 décisions prises), `2026-10-08-relecture-fidele.md` (section « Reste ») | Curseur par-dessus tout avec traînée, aperçu et contour de la carte survolée, panneaux et fenêtres rejoués, taille de vue, réglages propres au joueur, bandeau « enregistrement partiel ». Reste du 08/10 : mode manuel regardé, direct à plusieurs, survol dans une pile, curseur périmé après 5 s | `git grep` de « traînée » dans `CoucheCurseurs.tsx` et d'« enregistrement partiel » dans `ui-app/src` : aucun résultat ; seul le spectateur de base est fait (`79f879c3`) | gros | la fiche dit « après le lot 5 de la refonte de la phase du méchant » (livré) |
| 6 | Table personnalisable : choix par héros en multijoueur | `2026-10-07-table-multi-disposition-par-heros-et-zones-renommables.md` | Placer sbires et alliés héros par héros ; trancher « qui décide en multi » et la contradiction avec la règle « une brique par type » du 05/10 | Fait : zones renommables (`EditeurTable.tsx:227`), améliorations à gauche (`cote-ameliorations.ts`, `FenetreReglages.tsx:356`), éditeur ouvert sur tout plateau non mobile (`board.tsx:5401-5411`, disposition enregistrée par nombre de joueurs). Pas de trace d'une disposition par héros | moyen | arbitrage préalable de l'utilisateur |
| 7 | Animations : point 5 et retrait de la garde d'essai | `2026-09-14-animations-molles.md` | Au-delà de `MAX_VOLS = 10`, animer autrement au lieu de ne rien animer ; supprimer la garde d'essai quand l'utilisateur valide le geste | `CoucheAnimations.tsx:69` (`MAX_VOLS`), `:336` ; `ui-app/src/board/essais.ts` existe encore ; `DUREE_AVANT_ESSAIS` toujours présent | petit | validation de l'utilisateur à l'usage |

### 2.2 Préparation, comptes, salon

| # | Item | Source | Ce qui reste à faire | Preuve | Taille | Dépendances |
|---|---|---|---|---|---|---|
| 8 | Refonte connexion et inscription du site | `2026-10-09-connexion-inscription-site.md` | Style de l'assistant (en-tête fin, scène 30 %, formulaire à droite), mobile en bandeau, respect du mode sobre ; traduire « Le site est complet », remettre les accents, simplifier le pied de page | `site/orchestrateur.py:1737` : `raise ValueError(f"Le site est complet ({MAX_COMPTES} comptes).")` toujours hors `lang.t` ; aucun commit de refonte (les commits `75430bd7` et `0d8c4d6c` concernent le téléphone et le bilingue) | moyen | la fiche disait « après le mode sobre et le salon invité » : les deux sont faits |
| 9 | Coop locale : choisir le deck de chaque héros l'un après l'autre | `2026-10-07-choix-des-decks-en-coop-locale-un-heros-apres-l-autre.md` | Parcours séquentiel, plus aucun deck choisi par défaut en coop ; trois questions à trancher (retour arrière, récapitulatif, deck de base explicite) | aucun commit (`git log --grep="coop locale"` ne ressort que `d8f0e4df`, « deux tuiles de coop », sans rapport) ; comportement actuel non revu en navigateur | moyen | questions à poser une à une |
| 10 | Données des joueurs : décision en suspens | `2026-09-16-donnees-des-joueurs-ecrasees-et-jamais-sauvegardees.md` | Décider quoi dire au compte `lightningmantis` dont l'historique a été perdu | la fiche : « trois défauts corrigés, reste la décision sur `lightningmantis` » | petit | décision de l'utilisateur |
| 11 | Decks absents en campagne | `2026-09-15-decks-absents-en-campagne.md` | Obtenir la réponse « je ne les vois pas » ou « le choix ne tient pas », puis regarder le registre `DECKS_CAMPAGNE` (`prepare/app.js`, ~l.72) | « Mis de côté le 15/09/2026, rien modifié » ; les 88 decks sont bien en base | petit | une question à l'utilisateur |

### 2.3 Contenu et cartes

| # | Item | Source | Ce qui reste à faire | Preuve | Taille | Dépendances |
|---|---|---|---|---|---|---|
| 12 | Vérification des cartes hors irefrixs (pack Dazzler et suivants) | `2026-10-06-verification-cartes-hors-irefrixs.md` | dz004 à dz038 (35 cartes du pack Dazzler), autoplay ciblé Dazzler, puis les autres cartes hors irefrixs. Écart « this round » encore en « Phase » dans `im001b` et `wc014` | dz003 faite (`f7b4e6a0`) ; la fiche indique un arrêt à la carte 4 sur 40. Confirmé : `im001b.py:79` et `wc014.py:50` portent `in_this="Phase"` avec commentaire d'aveu | gros | règle de fidélité à 100 % (mémoire) : ajouter la portée « Round » au moteur (`worlds.py:815`) |
| 13 | Réserves de gabarits PROCESSUS-CARTE | `2026-09-21-echo-gabarits-processus-carte.md` (60040a/b/c : étape 8 bis, aucun cas `plateau-de-test`) ; `2026-09-11-zeus-gabarits-processus-carte.md` (boost supplémentaire non mesurable, clé `boosts_sur` absente) ; `2026-09-29-fleeting-alias-gabarits-processus-carte.md` (autoplay impossible sans deck) ; `2026-10-16-raphael-gabarits-processus-carte.md` (« Héros terminé : NON », biographie et partie humaine) | Écrire les cas manquants ou les déclarer hors périmètre | `git grep 60040a -- ui-app ui-check` : seulement des fichiers de textes, aucun test de plateau ; `git grep boosts_sur -- Fusion/marvel-lcg-src/tools` : rien | petit chacun (4) | aucune |
| 14 | Campagne Punisher MC×DC 2026 (« La ville ne dort jamais ») | `docs/packs/mcdc-2026-punisher/README.md` | Écrire le moteur (grille 3×3 de lieux, 3 territoires, pistes, CAPO à deux faces, Punisher actif), puis chaque carte par `PROCESSUS-CARTE.md` ; scénario 4 « Kingsfall » peut-être hors périmètre | relevé des 143 cartes, livret FR et maquette faits (`abe5cbf5`, `266cf257`, `ebe0bf3a`, `09d8a6e0`) ; aucun script de carte | gros | crédits du groupe MC×DC à nommer à l'intégration (mémoire `credits-mcdc-2026`) |
| 15 | Galactic Storm | `2026-08-29-plan-heros-vilains-fanmade.md`, `2026-09-06-analyse-galactic-storm-et-skrull-menace.md` | Porter la campagne (305 cartes, 5 scénarios, Binary et Quasar) | `tools/prefixes_fanmade.json` : `gs` `cartes: 0`, « matériel incomplet » ; l'analyse du 06/09 conclut « sans les cartes, il n'y a rien à porter » | gros | matériel complet à retrouver |
| 16 | Crédits des auteurs fan-made, par héros | `2026-09-16-crediter-les-auteurs-fanmade.md` | Afficher l'auteur dans la modale du héros ou l'aperçu de carte ; valider la liste des auteurs et la formulation | Fait : une liste de remerciements unique sur les écrans héros et méchants (`0256ea7c`, 17/10). Pas fait : aucune entrée « auteur » dans `data/sets_info.json` (grep sans résultat), aucun « pack créé par » dans `public/js` ni `ui-app/src` | petit | validation de la liste par l'utilisateur |
| 17 | Stan Lee : batterie « Marvelous » en pause | `2026-09-29-stan-lee-batterie-marvelous-en-pause.md` | Reprendre la batterie (reprise « prévue la semaine du 05/10 »), puis passer en français tout ce qui reste en anglais en jeu français | dernier commit lié : `bdac9eba` (29/09), `.planning/stan-lee/marvelous-partiel-0-1461.json` ; aucune reprise dans le journal | moyen | consommation de calcul de la batterie |
| 18 | Mots et textes : « Hs Feral Instincts » | `2026-10-08-portage-hunting-season.md` | La mise en place affiche l'identifiant du set mis en forme au lieu du nom | `public/js/campagne/app.js:1618-1627` : `titreSet` retombe sur l'identifiant ; le nom peut être fourni par `_nomsSets` (non vérifié en jeu) | petit | incertain (voir section 4) |

### 2.4 Infrastructure, distribution, charge

| # | Item | Source | Ce qui reste à faire | Preuve | Taille | Dépendances |
|---|---|---|---|---|---|---|
| 19 | BACKLOG n°1 : jeu « installable » sans 2,5 Go de cartes | `docs/BACKLOG.md` §1 | Tout : choix de la technique (application de bureau avec images à la demande), allègement WebP, cache et préchargement, nettoyage du cache | `Fusion/marvel-lcg-src/public/pwa/sw-plateau.js` : 0 occurrence de `caches.`, `cache.put`, `addAll` ; aucun commit de conversion WebP (seulement `a53375e6` qui sert les `.webp` existants) ; seuls commits : `f4f37227`, `732c971b` (docs) | gros | décisions : règle de nettoyage, systèmes visés (Windows seul ?), emballage du moteur |
| 20 | BACKLOG n°2 : ajouter des langues | `docs/BACKLOG.md` §2 | Choisir la langue (l'espagnol a le meilleur rapport couverture/effort selon la mesure du 18/10), importer textes MarvelCDB, textes d'interface, scans | le site est bilingue FR/EN seulement (`2026-09-16-site-bilingue.md` : 60 phrases sur 60) ; aucun dictionnaire d'une troisième langue ; seul commit : `f31e2707` (docs) | gros | chantier 1 (poids des scans, environ 1 Go par langue) ; accord éventuel de MarvelCDB |
| 21 | Mode navigateur (moteur Pyodide) : finitions | `2026-10-06-moteur-dans-le-navigateur-pyodide.md` §7 | Tester Firefox, Safari, mobile ; trancher l'ouverture publique (adresse joignable sans lien depuis le site) ; brancher `publier.py` sur `deployer.ps1` | `navigateur/` présent (`publier.py`, `construire.py`, `src/moteur-worker.js`) ; fiche §5 : « vérifié sur l'adresse en ligne (Chrome) » | moyen | lié au chantier 1 : cette brique rend possible le jeu sans serveur, ce que `BACKLOG.md` §1 dit impossible (voir section 6) |
| 22 | Tenir plus de joueurs | `2026-09-16-tenir-plus-de-joueurs.md` | Trois pistes d'optimisation du descripteur de monde (décompte seul des piles cachées, compteur de version par pile, cache par carte) ; rejouer le banc de charge | fiche : saturation du CPU vers 25 à 40 tables ; note du 06/10 : « non rejoué depuis la correction » | moyen | le mode navigateur (item 21) réduit le besoin |
| 23 | Archivage des tickets de bug | `2026-09-15-repondre-aux-rapports-de-bug.md` | Trancher l'archivage si le suivi se remplit | « question non tranchée » ; une purge existe déjà (`38867876`) | petit | aucune |

### 2.5 Mis de côté par décision ou très lointain

| # | Item | Source | Ce qui reste à faire | Preuve | Taille | Dépendances |
|---|---|---|---|---|---|---|
| 24 | Téléphone et tablette pour la phase « Sur la table » | `2026-10-19-table-telephone-tablette.md` | Mobile portrait (défilement vers les défenseurs, T13), éventail T14 au toucher, bandeau et pastille Renfort, petit écran paysage, cibles de 44 px, aperçu au toucher, vrais appareils | décision de l'utilisateur du 19/10 : « on oublie pour le moment » ; commit `723b7b14` (T13 puis retour au défilement d'origine) | gros | mis de côté |
| 25 | Mode tablette simple et mode téléphone (suite) | `2026-10-12-mode-tablette.md` (T1, T2 puis T3 « plus tard »), `2026-10-09-mode-telephone-refonte.md` (statut EN COURS ; zone 3 du plateau) | T1 détection tactile et fermeture de l'aperçu, T2 cibles de 44 px, T3 mode manuel au doigt, vrai iPad | `git grep maxTouchPoints -- ui-app/src/board/mobile` : aucun résultat, donc T1 n'est pas codée ; retours de Raven 1 à 7 faits (`959f1402`) | gros | mis de côté |
| 26 | Mode PvP Arena | `2026-10-06-mode-pvp-arena-idee.md` | Rien à développer ; si reprise : vrais bonus par aspect, relancer `pvp_sim2.py`, spécifier le « Rival » | fiche : « très lointain, aucune urgence » | gros | aucune |
| 27 | Nice-to-have de Yarro | `2026-09-28-nice-to-have-yarro.md` | Écarter des cartes pour voir dessous, assigner tous les dégâts d'un coup, raccourcis clavier des phases ; glisser-déposer pour permuter les cartes à ordonner (en plus des badges) | « aucune urgente » ; aucune trace dans le journal | petit à moyen | aucune |
| 28 | Le glisser-déposer du plateau n'est prouvé que par le typage | `2026-09-15-board-tsx-n-est-monte-par-aucun-test.md` (« défaut n°2 ») | Couvrir `onDepot` par un geste réel (Playwright) | « C'est le seul des trois qui reste ouvert » ; un test `ui-check/tests/zz-glisser-evenements.spec.ts` existe pour un autre geste (`fd54189e`) | petit | aucune |
| 29 | Revoir les sons : quels déclencheurs tombent mal | `2026-09-14-revoir-les-sons.md` | Demander à l'utilisateur lesquels sont mal placés | sons CC0 intégrés (`b175b2ef`) ; la fiche : « reste à lui faire nommer quels déclencheurs » | petit | une question à l'utilisateur |
| 30 | Revoir les couleurs du halo : validation | `2026-09-14-revoir-les-couleurs-du-halo.md` | L'utilisateur corrige les couleurs fausses ; envoyer les 75 palettes corrigées en ligne | éditeur fait le 19/09 (`2026-09-18-editeur-palettes-heros.md`) ; `eb48a5e6`, `e4ee62bf` : 75 corrections locales ; `deployer.ps1:498-504` les rapatrie du serveur sans les y pousser | petit | passe de l'utilisateur dans l'éditeur |
| 31 | Recherche de decks MarvelCDB : une vraie partie | `2026-07-28-recherche-decks-marvelcdb.md` | Jouer un tour complet avec un deck MarvelCDB importé | fiche : jamais fait ; l'import a depuis gagné les fichiers `.o8d` (`7103cc6e`) | petit | incertain si fait depuis (section 4) |

Répartition des tailles : gros = 5, 12, 14, 15, 19, 20, 24, 25, 26 (9) ; moyen = 2, 6, 8, 9, 17, 21, 22 (7) ; petit ou petit à moyen = les 15 autres (1, 3, 4, 7, 10, 11, 13, 16, 18, 23, 27, 28, 29, 30, 31).

---

## 3. FAIT mais fiche pas à jour

| # | Item et fiche | Ce que dit la fiche | Preuve que c'est fait |
|---|---|---|---|
| 1 | Mode manuel « comme OCTGN » (`2026-10-06-mode-manuel-comme-octgn.md`) | « PLANIFIÉ, RIEN CODÉ » (l'annotation du 07/10 en tête le dit déjà périmé) | `git log --grep=manuel` : `a6370398`, `4a15c9a8`, `8a88b772`, `b134cd7a`, `3f5171f4`, `a6370398` ; lots 0 à 7 déployés le 06/10 (`56349b00`) ; branche `mode-manuel` ancêtre de HEAD ; fiche sœur `2026-10-07-manuel-100-pourcent-octgn.md` : « FAIT ». Les restes sont l'item 4 de la section 2 |
| 2 | Mode manuel sans automatisation (`2026-09-14-mode-manuel-sans-automatisation.md`) | « Spec à écrire » | La fiche se clôt elle-même : « 06/10/2026 : fiche close », spec livrée le 22/09 |
| 3 | Mode Legacy (`2026-09-13-mode-legacy.md`) | « À FAIRE… RIEN N'EST ÉCRIT » | Même fiche en bas : « Livré le 13/09, déployé le 15/09 » ; `5493ea96`, `dbba4d35`, `ece47081` ; `public/js/prepare/legacy.js` présent |
| 4 | Éditeur de deck (`2026-10-09-editeur-de-deck-refonte.md`) | « PAS ENCORE CODÉE » | `d5bbc7ef` (« refait en trois colonnes »), `5f711553`, `2a54389b`, `f0363f69` ; entrée « Nouveautés » du 09/10 dans `public/js/prepare/nouveautes.js` (ligne 285) |
| 5 | Salon invité (`2026-10-09-salon-invite.md`) | « PAS ENCORE CODÉ » | `server_get.py:1007` route `get_equipe_salon` (publie héros choisi par siège sans le deck), `public/css/salon.css:123, 132` classes `.tb-scene` et `.tb-roster`, nouveautés du 09/10 (ligne 292) ; la route et le code sont arrivés par le commit de récupération `4f40f966` (14/10) |
| 6 | Choix du héros, 30 % / 70 % (`2026-10-09-choix-du-heros-plus-de-heros.md`) | « PAS ENCORE CODÉ » | `public/css/prepare/prepare.css:65` : `--affiche-scene-w:32%` (le défaut du fichier restant 58 % aux lignes 1361 et 1470, remplacé par cette variable) ; nombre exact de colonnes et de rangées non mesuré |
| 7 | Mode sobre des menus (`2026-10-09-mode-sobre-des-menus.md`) | « pas encore déployé » | `public/css/affichage-sobre-pages.css` présent ; test `ui-check/tests/affichage-sobre-pages.spec.ts` ; déploiement non établi (section 4) |
| 8 | Écran de campagne « livre ouvert » (`2026-10-09-ecran-campagne-livre-ouvert.md`) | « pas encore déployé » | `public/js/campagne/livre-pages.js` (commit `fce9ef4f`, 09/10) ; déploiement non établi |
| 9 | Inviter un connecté (`2026-10-13-inviter-un-connecte.md`) | « NON COMMITÉ, NON DÉPLOYÉ » | Commité : `efb0709b` (branche `multi-invitations`, 2 commits que HEAD ne contient pas par leur identifiant) ; mais les fichiers sont **identiques** dans HEAD (`git diff --stat HEAD multi-invitations` sur `site/orchestrateur.py`, `retour-salon.ts`, `invitations.js` : 0 ligne), arrivés par `4f40f966`. Le code est donc dans les arbres déployés des 18 et 19/10. Voir section 4 pour le déploiement et l'absence d'entrée « Nouveautés » |
| 10 | Table par briques (`2026-10-05-table-par-briques-decisions.md`) | décisions, « code lu, rien modifié » | `ui-app/src/board/table-briques.ts`, `EditeurTable.tsx:22-32` ; `3a6afcf0` ; déployé le 05/10 (`0a65abd2`) |
| 11 | Zones renommables et améliorations à gauche (`2026-10-07-table-multi-disposition-par-heros-et-zones-renommables.md`, deux premières demandes) | « Rien n'est commencé » puis « en cours de codage » | `EditeurTable.tsx:227` (double-clic pour renommer), `cote-ameliorations.ts:9`, `FenetreReglages.tsx:356` |
| 12 | Luke Cage officiel (`2026-10-10-luke-cage-audit.md`) | « RIEN CORRIGÉ », puis « Non déployé » | branche `luke-cage-correctifs` ancêtre de HEAD ; `2026-10-10-taches-en-pause.md` : déployé le 10/10 à 16h37 (« Luke Cage (9 cartes) ») ; réserves mineures : Sidewinder en multijoueur réel, ★ d'Augmented Jaws, doutes 62029 et 62014 |
| 13 | Contradiction sur la copie vivante du moteur (`2026-08-29-contradiction-copie-vivante-deployer.md`) | « Ouvert, laissé volontairement » | `docs/reference/GUIDE-CREATION-CONTENU.md` §1.1 : « RANGEMENT DU 31/08 : il n'y a plus qu'une copie » ; `ui-app/deployer.sh` n'a plus qu'une cible dans `JEUX` (lignes 17-22, 187) ; l'annotation du 07/10 le dit déjà |
| 14 | Six défauts « priorité absolue » du 14/09 (`2026-09-14-defauts-signales-en-partie.md`) | « ⛔ PRIORITÉ ABSOLUE… à re-vérifier » | La même fiche, à 22 h le 14/09 : « les six défauts sont traités et vérifiés en jeu », table de preuves (`phase-sur-table.spec.ts`, `annonce-attend-le-clic.spec.ts`, `phase-detaille-defense.spec.ts`, `ou-va-la-question.test.ts`, `DeroulePhase.test.tsx`, `marvelcdb-francais.spec.ts`) ; les fichiers de test existent dans `ui-check/tests`. Deux points hors fiche : la passe de langue et le haut du cartouche « Détaillé » en 1920×1080 (probablement dépassé par la refonte, incertain) |
| 15 | Revoir les sons (`2026-09-14-revoir-les-sons.md`) | « non commité » | `b175b2ef` (07/10) ; l'annotation du 07/10 le dit. Reste l'item 29 |
| 16 | Vérification hors irefrixs, carte dz003 (`2026-10-06-verification-cartes-hors-irefrixs.md`) | « dz003 non commité » | `f7b4e6a0` ; annotation du 07/10. Reste l'item 12 |
| 17 | Plan des héros et vilains fan-made (`2026-08-29-plan-heros-vilains-fanmade.md`) | tableau « reste » : Iron Patriot `cartes: 0`, Skrull Menace `cartes: 0` | `tools/prefixes_fanmade.json` : `ip` 39 cartes « LIVRÉ le 10/09/2026 » ; Skrull Menace : campagne terminée (`b9c7ce3f`, `3bda6c7e`, 111 cas `campagne_cartes`). Le champ `sk` du même JSON dit encore « EN COURS depuis le 15/10, 31 cartes » : à corriger aussi. Reste seulement Galactic Storm (item 15) et « Doctor Doom Alt Arts » (non revérifié) |
| 18 | Roue du hasard (`2026-10-08-roue-du-hasard.md`) | cases [ ] ouvertes en cours de fiche | toutes les cases visibles sont [x] ; `roue-hasard.spec.ts`, `roue-hasard-ecran.spec.ts` ; `8309f2d9` (Épure). Reste mineur : jamais vu à 3 ou 4 invités réels, écart de 1 à 2 s entre hôte et invité |
| 19 | Phase du méchant « à améliorer » (`2026-10-09-phase-du-mechant-a-ameliorer.md`) | « MAQUETTE À FAIRE, pas codé » | Dépassée : refonte déployée le 05/10 (`397331a5`), essai « Étape par étape » retiré le 11/10 (`940a01ba` annulé par `7eb795d6`), schéma du 12/10, puis trois choix (« Guidée », « Plateau animé », « Accéléré ») déployés le 19/10 d'après `2026-10-19-restes-apres-deploiement.md` |

---

## 4. INCERTAIN

| # | Point | Pourquoi incertain |
|---|---|---|
| 1 | Déploiement de « inviter un connecté », du mode sobre, du livre ouvert, de la roue, des sons | Le code est dans l'arbre du tag, donc dans ce qui a pu être envoyé les 18 et 19/10, mais aucun journal de déploiement lisible ici ne liste ces fonctions. `nouveautes.js` n'a aucune entrée « inviter un joueur connecté » (grep « invit » et « connect » : seulement les lignes 292, 562, 610 et 641, qui sont d'autres sujets) ; `deployer-tout.sh` exige une entrée « Nouveautés ». À confirmer sur le serveur |
| 2 | Écart assumé de « inviter un connecté » | La fiche demande la validation de l'utilisateur : l'invité garde l'écran du salon, pas `prepare.html`. Rien n'indique qu'il l'ait validé |
| 3 | « Accéléré » couvre-t-il la demande « une seule fenêtre déplaçable » ? | `2026-10-07-phase-du-mechant-tout-d-un-coup-une-seule-modale-deplacable.md` demandait une fenêtre unique avec liste de choix pour le mode « tout d'un coup ». Le bandeau de question en colonne déplaçable (`4ee2a0aa`) et les trois choix sont arrivés depuis, mais la correspondance n'a pas été vérifiée en jeu |
| 4 | Le mode navigateur (Pyodide) est-il en ligne ? | La fiche dit à la fois « NON DÉPLOYÉ » (en-tête) et « vérifié sur l'adresse en ligne » (§5) ; le README Punisher et la mémoire décrivent `navigateur/publier.py --oui` dans la procédure du 19/10, ce qui laisse penser qu'il l'est |
| 5 | « Hs Feral Instincts » | `titreSet` est inchangé mais un nom peut venir de `_nomsSets` ; seul le rendu en jeu tranche |
| 6 | Recherche de decks MarvelCDB : partie réelle | Aucune trace d'une partie jouée avec un deck importé, mais l'import a beaucoup changé depuis (`.o8d`, `7103cc6e`) |
| 7 | Le tutoiement, les textes d'aide : portée exacte | Seuls quelques écrans ont été regardés (lignes citées item 1) ; une passe complète n'a pas été faite |
| 8 | Packs TMNT et Shinobi | Hors `.planning/todos` : le suivi vit dans `.planning/tmnt/` (questions d'auteur, `decisions-phase-b.md`) et `docs/tmnt-questions-pour-inkwire-a-envoyer.md`. `prefixes_fanmade.json` donne `tk` « cartes: 0 » alors que le travail est avancé. Non audité ici |
| 9 | Test `klaw-ameliorations` | Cause « probable » de la fiche (éventail T14) non vérifiée : aucun test lancé |
| 10 | Cartouche « Détaillé » qui déborde en 1920×1080 | Point noté le 14/09 ; probablement sans objet depuis la refonte, mais non revu |
| 11 | Doctor Doom Alt Arts (16 cartes distinctes) | Mentionné dans le plan fan-made sans préfixe réservé ; aucune vérification faite |

---

## 5. CLOS

Les comptages par nom de fichier sont exacts (gabarits, portages, relevés, préparations). Les deux derniers (chantiers livrés, bugs corrigés) sont des estimations faites en lisant la ligne de statut et la fin de chaque fiche.

| Catégorie | Nombre | Vérification | Trois exemples |
|---|---|---|---|
| Gabarits PROCESSUS-CARTE | 39 fiches (35 closes, 4 avec réserve : voir item 13) | statut grepé dans les 39 fiches (« Carte terminée : OUI ») ; lecture de la fin de 5 d'entre elles | `2026-09-05-throg-gabarits-processus-carte.md` (17 cartes sur 17), `2026-09-08-superior-spider-man-gabarits-processus-carte.md` (batterie du pack 32/32), `2026-09-22-wave-gabarits-processus-carte.md` |
| Portages | 15 | statut lu pour les 15, fin lue pour Wave, Fear No Evil, Conan, Gorr, Hunting Season | `2026-08-31-portage-agatha-harkness.md`, `2026-09-22-portage-wave.md` (16 cartes sur 16 « OUI »), `2026-09-12-portage-sentinel.md` (26 cartes, `5efc5b74`) |
| Relevés de cartes | 8 | statut lu | `2026-09-09-venomized-releve-des-37-cartes.md` (pack livré), `2026-09-11-zeus-releve-des-cartes.md` (cinquième couleur livrée), `2026-09-13-releve-des-images-de-cartes.md` (outil fait ; relevé vide) |
| Préparations de vague 0 | 5 | titres et en-têtes lus | `2026-09-02-prep-vague0-hulk.md`, `2026-09-02-prep-vague0-lady-sif.md`, `2026-09-02-vague0-mode-emploi.md` |
| Chantiers et campagnes livrés (environ 28) | environ 28 | statut lu pour chacun | `2026-08-12-campagne-web-of-deceit.md` (5 scénarios), `2026-07-30-mode-bataille-civil-war.md`, `2026-09-16-site-bilingue.md` (60/60 phrases) |
| Bugs corrigés (environ 40) | environ 40 | fin lue pour 20 fiches | `2026-09-11-sp-dr-ne-monte-pas.md`, `2026-09-17-rivalite-antique-ne-redresse-pas-thor.md`, `2026-09-16-lancer-une-partie-refuse-url-trop-longue.md` |
| Décisions, idées, analyses sans reste propre (environ 15) | environ 15 | | `2026-09-01-inventaire-drive.md` (deux boîtes sorties du backlog), `2026-08-31-cas-rouges-sg-ss.md` (4 cas rouges de Squirrel Girl laissés dans le harnais, hors backlog le 13/09), `2026-09-11-autoplay-aveugle-sur-iron-patriot.md` (« ce qui reste sort du backlog ») |

Fichiers non Markdown : `2026-09-12-fenetre-d-interruption-muette-capture.png` (capture) et `2026-10-06-charge-serveur-resultats.jsonl` (résultats du banc de charge) : pièces jointes de fiches.

Réserve connue sur les comptages : quelques fiches sont à la fois journal de livraison et porteuses d'un reste (par exemple `2026-09-20-trois-signalements.md`, « rien n'est déployé » au 20/09). Elles sont classées closes parce que les arbres déployés des 18 et 19/10 contiennent leurs correctifs (non vérifié correctif par correctif).

---

## 6. Ordre de reprise proposé

Cadre : l'utilisateur teste en local et déploie lui-même ; téléphone et tablette sont mis de côté ; T18 est annulée.

1. **Fermer les restes du 19/10 (item 1), puis envoyer les palettes (item 30).** Raison : la phase du méchant vient d'être livrée, l'utilisateur est en train de la valider, et ces restes sont tous petits. Un test rouge connu, des textes à relire et une décision (réafficher la fenêtre de choix) bloquent une batterie propre. Le bénéfice est immédiat pour ce qu'il teste déjà. Ne pas toucher au cache en ligne sans concevoir les empreintes `?v=`.

2. **Fidélité des cartes : portée « Round » du moteur, `im001b`, `wc014`, puis dz004 à dz038 (item 12) et les réserves d'Echo et de Zeus (item 13).** Raison : la règle du projet est la fidélité à 100 % sans approximation (mémoire). Deux cartes affichent encore un écart documenté par leur propre commentaire. C'est un travail qui se prouve par des tests, sans besoin de l'utilisateur, et qui évite de laisser un défaut de règle chez les joueurs.

3. **Refonte connexion et inscription (item 8).** Raison : décidée, tous les styles dont elle dépendait sont faits, et c'est la première page que voit un nouveau joueur. Elle règle aussi un texte non traduit (`orchestrateur.py:1737`) et des accents manquants, qui contredisent l'objectif « parfaitement bilingue ».

4. **Coop locale : un deck par héros, l'un après l'autre (item 9).** Raison : l'utilisateur joue avec un deck qu'il n'a pas choisi sans le savoir, un défaut de confort réel pour une demande déjà formulée. Poser d'abord les trois questions de la fiche (retour arrière, récapitulatif, deck de base explicite). Dans la même séance : trancher la question de l'arbitrage multi de l'item 6.

5. **Décider la technique du jeu installable (item 19), avec une première mesure.** Raison : c'est le chantier le plus gros et le seul que l'utilisateur a explicitement cadré (jouer hors ligne, cache aussi sur PC). Avant tout code, deux préalables à clarifier : le mode navigateur (item 21) contredit la phrase « le moteur est en Python côté serveur » de `BACKLOG.md` §1 ; l'allègement WebP (mesure sur 100 cartes) est utile quelle que soit la voie. La relecture fidèle (item 5) vient juste après : décisions complètes, mais travail gros et de moindre urgence que la distribution.

Hors priorités : téléphone et tablette (items 24 et 25), PvP (26), Galactic Storm (15, matériel manquant), campagne Punisher (14, à lancer quand l'utilisateur le décide, avec les crédits MC×DC), langues (20, après le chantier 1).

À corriger au passage dans la documentation : le champ `sk` de `tools/prefixes_fanmade.json` (« EN COURS ») et les 19 en-têtes listés en section 3, pour que le prochain relevé n'ait plus à refaire ce tri.
