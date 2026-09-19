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

⚠ **La batterie complète des capacités tournait encore au moment du
déploiement** (fichiers moteur partagés touchés). La passe précédente donnait
2332/2341, avec les neuf rouges tous expliqués : cinq venaient du harnais et
ont été corrigés depuis, quatre sont Squirrel Girl, rouges avant cette journée.
Relire son bilan et corriger si elle sort autre chose.

## L'ordre décidé avec l'utilisateur

1. ~~**Fear No Evil**~~ — **FAIT ET DÉPLOYÉ le 19/09/2026.** Le pack, la
   campagne en ordre libre, les planches du livret et les 95 images. La boucle
   de campagne des dix boîtes est mesurée par-dessus
   (`.planning/todos/2026-09-19-boucle-de-campagne-dix-boites.md`).
2. **L'éditeur de palettes de héros** — cadré, fiche
   `2026-09-19-editeur-palettes-heros.md`. Le point dur est de faire savoir au
   plateau que le visiteur est l'auteur : l'identité vit dans le site, le
   plateau est servi par le moteur.
3. **Le mode manuel, moitié plateau** — 7 tâches sur 8 restantes, plan
   `docs/superpowers/plans/2026-09-18-mode-manuel-plateau.md`. La moitié moteur
   est finie, revue et fusionnable (16 commits, 19 cas verts).

## Ce qui reste ouvert, sans être planifié

- **Le signalement perdu du 18/09 reste inexpliqué.** Aucune trace nulle part,
  et le joueur ne se souvient pas s'il avait vu la confirmation ou une erreur.
  Le correctif `84ae2ed0` ne le répare pas : il rend le prochain cas
  diagnosticable. À rouvrir seulement si ça se reproduit.
- **« Mes signalements » reste inaccessible depuis le menu du jeu.** Le correctif
  touche l'en-tête de l'écran de préparation, là où travaille l'autre session.
  À faire dès qu'elle a fini.
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
