# Coop locale : choisir le deck de chaque héros l'un après l'autre (07/10/2026)

**Statut : BACKLOG, demande de l'utilisateur (questions posées une à une). Rien n'est commencé.**

## Le problème constaté
Quand on joue PLUSIEURS héros en local (coop locale, 2 à 4 héros), l'étape « Decks » de l'assistant de préparation laisse passer à
l'étape suivante SANS qu'un deck ait été choisi pour chaque héros. Dans ce cas le jeu prend TOUT SEUL le deck de base du héros.
L'utilisateur ne veut pas de ce comportement : il passe sans s'en apercevoir et joue avec un deck qu'il n'a pas choisi.

## Le comportement voulu (ses mots)
« Je veux qu'on passe sur le héros 1, on valide le deck, puis héros 2, on valide le deck, etc. »
Donc : un parcours SÉQUENTIEL, un héros à la fois. On ne passe au héros suivant qu'après avoir VALIDÉ le deck du héros courant, et
l'étape suivante de l'assistant (le méchant) n'arrive qu'après le dernier héros.
**Plus aucun deck choisi automatiquement** : si l'utilisateur ne choisit pas, il ne peut pas avancer.

## Où regarder
- L'étape « DECKS » de `Fusion/marvel-lcg-src/public/prepare.html` et `public/js/prepare/` (bouton « Continuer », liste des sièges,
  sélection `tb-deck`) ; le choix par siège (« SIÈGE 1 », `tb-siege`).
- Où le deck de base est posé par défaut quand rien n'est choisi (à chercher : c'est ce repli qu'il faut supprimer en coop).
- Le solo (un seul héros) ne doit pas changer : un seul écran de deck, comme aujourd'hui.

## Questions à trancher le jour où on le fait
- Peut-on REVENIR au héros précédent pour changer son deck après l'avoir validé ?
- Un récapitulatif final (héros 1 : deck X, héros 2 : deck Y) avant de passer au méchant ?
- Le choix d'un deck « de base » reste-t-il possible, mais seulement en le CHOISISSANT explicitement (un clic), jamais par défaut ?
