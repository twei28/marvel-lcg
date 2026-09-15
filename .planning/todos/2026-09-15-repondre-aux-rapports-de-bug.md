# Répondre aux rapports de bug, et peut-être des tickets

**Idée de l'utilisateur, 15/09/2026** : « quand les gens m'envoient un bug,
s'ils ont un compte, j'aimerais que quand je corrige ou que je réponde, il y ait
une petite modale qui s'ouvre pour voir ma réponse (et donc il faudrait me
permettre de mettre une réponse), voire développer tout un truc de tickets ».

## Ce qui existe déjà

- **Le rapport part du plateau** : `ui-app/src/board/RapportBug.tsx` et
  `rapport-bug.ts` (module pur : journal, écran, siège, capture).
- **Le moteur le relaie, il ne le stocke pas** :
  `server_get.py:910`, `post_rapport_bug` poste vers `/api/bug` du SITE, avec
  `nom`, `description`, `journal`, `ecran`, `siege`, `capture`. Vingt secondes
  de délai, parce que la capture pèse lourd.
- ⚠ **Aucune réserve de siège** : n'importe qui à la table peut signaler, invité
  compris. C'est écrit noir sur blanc dans le code, et c'est voulu : « ce sont
  justement ceux qui n'ont aucun autre moyen de le dire ». Une réponse adressée
  à un compte ne doit pas casser ça.

## Le point dur, à trancher avant tout

**Les rapports vivent sur le SITE, pas dans ce dépôt.** Le moteur ne fait que
poster. Donc :

- où est le code du site, et qu'est-ce qu'il sait déjà des comptes ?
- un rapport porte-t-il aujourd'hui l'identité de son auteur, ou seulement un
  nom libre et un siège ?
- la réponse doit-elle atteindre le joueur **en partie** (une modale sur le
  plateau, donc un canal moteur → client) ou **sur le site** (une page « mes
  signalements ») ?

Tant que ces trois-là ne sont pas répondus, il n'y a pas de chantier, il y a
une intention.

## Les deux tailles possibles

1. **Le petit bout utile** : une réponse texte de l'admin attachée au rapport,
   et une modale au prochain passage du joueur qui a un compte. Pas de statut,
   pas de fil, pas de liste.
2. **Le vrai suivi** : des tickets avec statut (reçu / en cours / corrigé /
   refusé), un fil de messages, une liste côté joueur, des notifications. C'est
   un produit, pas une fonction.

⚠ Mon avis, à confirmer avec lui : commencer par 1. On saura très vite si le
besoin est « savoir que c'est corrigé » ou « discuter du bug », et ce n'est pas
le même logiciel.

## Statut

Notée le 15/09/2026, **à cadrer**. Aucune ligne de code, et les trois questions
ci-dessus passent avant.
