# Le site en deux langues, comme le jeu

**Demande de l'utilisateur, 16/09/2026** : « faire en sorte que tout soit
parfaitement bilingue. Tout, tout, tout. »

## Le constat qui a déclenché ça

Question posée le même jour : « est-ce que tout ce qui existe est en anglais et
en français ? ». Réponse : **non**.

| Partie | État |
|---|---|
| L'assistant de préparation | bilingue (`dico-en.js`) |
| Le plateau | bilingue (`dico-en.ts`) |
| Le deck builder, le salon | bilingues (ils importent le `t()` de l'assistant) |
| **Le site** (`orchestrateur.py`) | **français en dur** |

Ce n'est pas nouveau : le commit `1ca86e05` du 15/09 dit « le SITE n'avait
aucune gate, et 29 clés s'affichaient en français sur un écran anglais ». Le
sujet était connu, jamais traité au fond.

⚠ Et j'y ai ajouté du français en dur le jour même, avec la page
« Mes signalements » et son entrée dans la barre.

## L'ampleur, mesurée

**145 chaînes françaises visibles** dans `site/orchestrateur.py`, réparties
entre onze gabarits HTML (`PAGE`, `PAGE_FORMULAIRE`, `PAGE_ADMIN`,
`PAGE_SUIVI`, `PAGE_HORS_LIGNE`…) et le code lui-même.

## Le point dur : quelle langue parle ce visiteur ?

Le jeu garde son choix dans le `localStorage`, que le serveur ne voit pas. Le
site doit donc s'appuyer sur autre chose :

1. un **cookie** `nc_langue`, posé par le site et — c'est l'astuce — aussi par
   le jeu, sur le domaine parent, pour que le choix fait dans une partie suive
   sur le site ;
2. à défaut, l'en-tête **`Accept-Language`** du navigateur ;
3. à défaut, le français.

## Statut

**Commencé le 16/09/2026**, dans la foulée de la demande. Voir les commits du
jour. Ce qui est fait et ce qui reste est tenu à jour ici.
