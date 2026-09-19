# La file d'attente, et ce qui attend d'être déployé

Écrit le 19/09/2026. **À relire et à mettre à jour juste après chaque
déploiement** : c'est le seul endroit qui dit ce qui est parti et ce qui reste.

## ⚠ Prêt, commité, PAS déployé

Trois correctifs sur la branche `mode-manuel`, tous testés :

| Commit | Quoi |
|---|---|
| `9ec8f6b9` | Un lien **Accueil** dans la barre du site. Sans lui, les pages du site sont un cul-de-sac : le site s'installe en application (`display: standalone`), donc sans bouton Précédent. Signalé par un joueur. |
| `bd9ff080` | « Mes signalements » montre **tout ce qui vient de ses tables**, quel que soit le siège, en nommant le siège et l'auteur. L'autorisation de RÉPONDRE, elle, reste au siège 0. |
| `84ae2ed0` | Un signalement dont l'envoi échoue est **gardé** et rendu à la réouverture du panneau ; et le moteur trace chaque tentative de relais dans le journal. |

**Deux choses à ne pas oublier au déploiement :**

1. **Reconstruire le plateau** (`bash ui-app/deployer.sh`) avant de déployer :
   le correctif du panneau de signalement vit dans `ui-app`, et `deployer.ps1`
   ne reconstruit pas le bundle. Vérifier le hash du bundle après.
2. **Le déploiement envoie le DOSSIER DE TRAVAIL**, pas la branche : commité ou
   non ne change rien. Tant que le chantier Fear No Evil est en cours sur le
   disque, déployer l'emporte aussi. D'où l'attente.

## L'ordre décidé avec l'utilisateur

1. **Fear No Evil** (autre session) — en cours, on attend qu'elle finisse.
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
