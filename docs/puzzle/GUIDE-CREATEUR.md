# Créer et publier un puzzle (guide du créateur)

Un puzzle est une **situation de départ** imposée (héros, méchant, cartes en jeu, mains, decks, états) avec un
**objectif** à atteindre. Le joueur cherche la bonne suite de coups, autant d'essais qu'il veut.

## Où se trouve le créateur
Panneau **« 🧩 Puzzles »** → **« Créer un puzzle »**. (Le bouton est débranché du site tant que la fonction n'est pas
livrée : voir `PLAN.md`.) L'assistant s'ouvre en plein écran, en orange. Chaque étape est **facultative** ; tout a une
valeur par défaut. **Retour**, **Passer** et **Suivant** se trouvent en bas, et **Tester ce puzzle** à tout moment.
Ton brouillon est gardé dans ton navigateur à chaque étape : si tu fermes, on te propose de le reprendre.

## Les 8 étapes
1. **Qui joue ?** 1 à 4 héros. Leur deck de départ est proposé (signature + moitié d'aspect) ; la main de départ est
   tirée du début de la liste.
2. **L'ennemi.** Le scénario (donc le méchant, les complots, les cartes de rencontre) ; standard ou expert.
3. **L'état de la menace.** Stade du méchant et de son complot principal, points de vie du méchant, menace posée.
4. **Les cartes des héros.** Main, deck (dessus en premier) et défausse de chaque héros. Ajoute par recherche, change
   l'ordre avec ▲ ▼, déplace d'une pile à l'autre avec la liste « → », bouton **Mélanger** pour le deck.
5. **Ce qui est en jeu.** Alliés, soutiens, sbires (engagés avec un héros), complots annexes, environnement, et
   améliorations posées sur un porteur de ton choix.
6. **Les états.** Pour chaque carte : points de vie, épuisée, cartes d'état (Sonné, Coriace, Désorienté, Exposé,
   Camouflé, Étourdi, Intensifié), compteurs nommés, menace d'un complot annexe.
7. **L'objectif.** Vaincre le méchant, survivre jusqu'à la fin du round, terminer un complot, ou un **objectif libre** que
   le joueur coche lui-même. Plusieurs objectifs : « tous requis » ou « un seul suffit ». Aucun objectif = fin de partie
   normale du moteur.
8. **Présentation et test.** Titre (obligatoire pour publier), histoire, difficulté (étoiles), indices (jusqu'à 10,
   dévoilés un par un au joueur), premier joueur, moment de départ (début de phase joueur, phase du méchant, fin de
   round), ton pseudo.

## Tester
**Tester ce puzzle** monte la table avec ton puzzle, tel que le verra le joueur. Joue-le : si tu n'y arrives pas toi-même,
le puzzle n'est pas prêt. **Recommencer** (panneau « Énoncé », en haut à droite) relance le même départ à l'identique.

## Publier
**Publier** envoie le puzzle au site et te donne :
- un **code** court (`PZ-XXXX`) à donner à qui veut le résoudre ;
- une **clé d'édition** secrète, affichée **une fois** et gardée dans « Mes puzzles » sur ce navigateur. Elle permet de
  **Modifier** (même code) ou **Supprimer**. Note-la si tu changes d'appareil : le site n'en garde que l'empreinte et ne
  peut pas la retrouver.

Règles du serveur :
- **28 jours** : un puzzle disparaît 28 jours après la dernière fois où quelqu'un l'a joué. Chaque partie remet le
  compteur à zéro ; la création compte comme un premier jeu.
- **Aucune donnée personnelle** : un pseudo libre, rien d'autre.
- Taille limitée (300 Ko, 4 héros, 200 cartes par pile, 10 indices, 6 objectifs) et **10 publications par heure**.
- Seules des commandes de **mise en place** sont acceptées ; toute carte inconnue du jeu est refusée.
- Hors ligne (jeu local), tester marche, publier et lire par code demandent le site.

## Résoudre par code
Panneau Puzzles → saisis le code → **Résoudre par code**. Une introduction (titre, histoire, difficulté, objectifs) s'affiche
une seule fois ; le panneau **Énoncé** garde l'histoire, les indices (un par un) et **Recommencer**.

## Ce qui n'est pas encore là
- **Solution de référence** (enregistrer ta solution pour la montrer après résolution) : non faite, voir `PLAN.md`.
- Glisser-déposer (l'ordre se règle avec les flèches), ressources en réserve, aperçu en direct, « Affiner sur le plateau ».
