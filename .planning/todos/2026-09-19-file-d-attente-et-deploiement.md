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
