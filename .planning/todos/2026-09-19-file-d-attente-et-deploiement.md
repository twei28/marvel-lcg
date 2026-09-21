# La file d'attente, et ce qui attend d'être déployé

Écrit le 19/09/2026. **À relire et à mettre à jour juste après chaque
déploiement** : c'est le seul endroit qui dit ce qui est parti et ce qui reste.

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
3. **Le mode manuel, moitié plateau** — 7 tâches sur 8 restantes, plan
   `docs/superpowers/plans/2026-09-18-mode-manuel-plateau.md`. La moitié moteur
   est finie, revue et fusionnable (16 commits, 19 cas verts).

## ⚠ Le déploiement est BLOQUÉ par un fichier d'une autre session

`ui-app/src/board/halo-heros-accord.test.ts` porte une directive
`@ts-expect-error` devenue inutile, livrée le 19/09 avec l'éditeur de palettes.
Elle casse `npm run typecheck`, **et le typecheck casse la construction du
plateau** : `ui-app/deployer.sh` ne peut plus construire. Constaté le 20/09 en
montant un serveur local, qui a dû contourner la ligne puis restaurer le
fichier. Une ligne à retirer, dans le fichier d'une autre session.

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

- **`fne/daredevil/60001a.py` (Sense the Top) porte probablement le MÊME défaut
  de cache**, et c'est cerné : un grep sur `CheckIfFaceIsLikeInHand` ne rend que
  **trois** cartes posant une condition variable — Magik (`aoa/magik/45030a.py`,
  qui vide le cache à la main depuis longtemps), Echo (corrigée le 21/09) et
  Daredevil. Sa condition est
  `message.which_face == initiator.additional_deck.GetTop()` : quand la carte du
  dessus part, **la suivante devient le dessus sans bouger**, donc avec la
  réponse `False` figée par le cache — elle ne serait jamais jouable. Même
  famille, même remède (rafraîchir les cartes de la pile concernée). **Non
  mesuré**, hors du chantier d'Echo.

- **Une seule Photographic Reflexes en main peut être dépensée comme
  RESSOURCE** pour payer la carte glissée qu'elle vient d'autoriser : la
  permission est lue avant le paiement, et au moment où Echo veut la défausser
  il n'y a plus rien. Le joueur obtient l'événement **et** le bénéfice de la
  ressource, sans rien perdre d'autre. **Défaut ANTÉRIEUR**, non corrigé : il ne
  vient pas du chantier du 21/09, mais le témoin ajouté ce jour-là
  (`la carte glissee payee AVEC une Photographic Reflexes de la main`) met
  délibérément **deux** copies en main et passe donc à côté.

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
- **Un signalement ne porte pas le compte de son auteur**, seulement le jeton de
  la table et le nom tapé. Conséquence : un signalement envoyé depuis un second
  appareil est désormais visible, mais reste sans conversation possible. Le
  réparer vraiment demande de toucher le client du jeu et le relais.
- **La bascule manuelle en cours de partie** (pause sur place, échappatoire,
  traces au journal) : cadrée en avenant à
  `docs/superpowers/specs/2026-09-18-mode-manuel-design.md`, pas planifiée.
  Reste à trancher : qui peut la déclencher en multijoueur, et ce que voient les
  autres pendant ce temps.
- **Les extensions non portées** demandent un import de données (cartes et
  scans) : le mode manuel seul ne les ouvre pas. Non cadré.
- **`FileManager.FormatPath` se trompe sur un chemin POSIX absolu** sans lettre
  de lecteur (trouvé le 18/09 en écrivant le harnais du mode manuel). Invisible
  sous Windows, donc sans effet en production. Contourné côté harnais, moteur
  non touché.
- **Les auteurs fan-made ne sont pas confirmés** : 18 noms attribués, dont 3
  ajoutés le 18/09, et 35 personnages jouables sans aucun auteur attesté. Fiche
  `2026-09-16-crediter-les-auteurs-fanmade.md`. Rien ne doit s'afficher dans le
  jeu avant validation ligne par ligne.

## Le Ctrl+Z n'annule pas un geste fait pendant une pause (20/09/2026)

Trouvé par la revue de la tâche 8 du plan de la pause manuelle, ANTÉRIEUR à ce
chantier, non corrigé volontairement.

`DoGetInput` jette le retour de `DrainSandboxCommands`, là où `World.ManualLoop`
l'enregistre dans `scene.manuel_commands`. Conséquence en deux temps :

1. Les gestes manuels faits pendant une question ouverte **n'entrent pas dans
   la sauvegarde**.
2. `AnnulerDernierGeste` s'appuyant sur cette même liste, **le Ctrl+Z ne peut
   pas annuler un geste fait pendant une pause de partie ordinaire**.

C'est visible par le joueur : il corrige sa table, se trompe, fait Ctrl+Z, et
rien ne se passe. À traiter à part, parce que la correction touche le même
chemin que la tâche 8 et mérite ses propres cas.
