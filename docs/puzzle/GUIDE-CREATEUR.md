# Créer et publier un puzzle (guide du créateur)

Un puzzle est une **situation de départ** imposée (héros, méchant, cartes en jeu, mains, decks, états) avec un
**objectif** à atteindre. Le joueur cherche la bonne suite de coups, autant d'essais qu'il veut.

## Où se trouve le créateur
Sur l'écran de départ (là où on choisit le mode), la tuile **« Puzzle »**. Elle lance l'assistant de partie **habituel** :
héros, deck, méchant, scénario. Puis le **vrai plateau** s'ouvre en **mode éditeur** (bac à sable + table manuelle : le moteur
se tait, rien ne se déclenche quand tu déplaces une carte). Le panneau orange **« Création de puzzle »**, en haut à gauche,
porte le bouton **« Enregistrer le puzzle »**.

## Arranger le plateau
Tout se fait comme à la table manuelle (clic droit sur une carte, glisser-déposer, clavier) :
- **état des cartes** : incliner / redresser, retourner, dégâts, menace, statuts (Sonné, Coriace, Désorienté…), compteurs,
  attacher ;
- **déplacer entre zones** : main, deck, défausse, en jeu, pile de victoire, mises de côté, pour les héros **et** le méchant ;
- **voir ce qui est caché** : un clic droit sur une pile (deck du héros, défausse, deck rencontre, défausse rencontre) ouvre
  sa liste, dans l'ordre réel, face visible ;
- **ajouter ou retirer des cartes** : le catalogue complet du jeu ;
- **PV, menace, stade du méchant et du complot** : même menu.

## Enregistrer
**Enregistrer le puzzle** capture le plateau tel qu'il est (le moteur le relit : zones, ordre des decks, états), puis ouvre la
fenêtre des détails : titre (obligatoire), histoire, difficulté (étoiles), **objectifs** (vaincre le méchant, survivre jusqu'à la
fin du round, terminer une manigance, ou un objectif libre que le joueur coche ; « tous requis » ou « un seul suffit »), indices
(jusqu'à 10, dévoilés un par un), phase de départ, premier joueur, **solution de référence** (texte, 4000 caractères au plus,
visible *après la partie*, *toujours* ou *jamais*) et ton pseudo. La fenêtre liste aussi **ce que la capture n'a pas pu garder**
(par exemple les ressources en réserve) : rien n'est tu.

## Tester
Résous ton puzzle toi-même avec son code (panneau « 🧩 Puzzles » → **Résoudre par code**), tel que le verra le joueur. Si tu
n'y arrives pas, il n'est pas prêt. **Recommencer** (panneau « Énoncé », en haut à droite) relance le même départ à l'identique.

## Publier
**Publier le puzzle** (dans la fenêtre des détails) envoie le puzzle au site et te donne :
- un **code** court (`PZ-XXXX`) à donner à qui veut le résoudre ;
- une **clé d'édition** secrète, affichée **une fois** et gardée dans « Mes puzzles » sur ce navigateur. Elle permet de
  **Supprimer** le puzzle (la modification d'un puzzle déjà publié par l'interface n'existe plus : republie une nouvelle version). Note-la si tu changes d'appareil : le site n'en garde que l'empreinte et ne
  peut pas la retrouver.

Règles du serveur :
- **28 jours** : un puzzle disparaît 28 jours après la dernière fois où quelqu'un l'a joué. Chaque partie remet le
  compteur à zéro ; la création compte comme un premier jeu.
- **Aucune donnée personnelle** : un pseudo libre, rien d'autre.
- Taille limitée (300 Ko, 4 héros, 200 cartes par pile, 10 indices, 6 objectifs) et **10 publications par heure**.
- Seules des commandes de **mise en place** sont acceptées ; toute carte inconnue du jeu est refusée.
- Hors ligne (jeu local), arranger le plateau marche ; publier et lire par code demandent le site.

## Résoudre par code
Panneau Puzzles → saisis le code → **Résoudre par code**. Une introduction (titre, histoire, difficulté, objectifs) s'affiche
une seule fois ; le panneau **Énoncé** garde l'histoire, les indices (un par un) et **Recommencer**.

## Ce qui n'est pas encore là
- **Solution de référence en replay** (rejouer tes coups à l'écran) : non faite ; la solution est un **texte**.
- **Modifier un puzzle déjà publié** depuis l'interface : l'ancien assistant (8 étapes) a été retiré le 24/10/2026 ; on republie.
- Ressources en réserve, aperçu en direct, mobile (l'éditeur est pensé pour l'ordinateur).
