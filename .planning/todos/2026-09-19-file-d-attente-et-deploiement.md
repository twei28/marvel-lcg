# La file d'attente, et ce qui attend d'être déployé

Écrit le 19/09/2026. **À relire et à mettre à jour juste après chaque
déploiement** : c'est le seul endroit qui dit ce qui est parti et ce qui reste.

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
