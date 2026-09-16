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

✅ **LIVRÉ le 16/09/2026**, en « vrai suivi de tickets » (choix de l'utilisateur
parmi les trois tailles proposées). Spec :
`docs/superpowers/specs/2026-09-16-suivi-des-signalements-design.md`. Plan :
`docs/superpowers/plans/2026-09-16-suivi-des-signalements.md`.

**Les trois questions dites bloquantes ont été répondues par le CODE**, pas par
l'utilisateur : le site vit dans ce dépôt (`site/orchestrateur.py`), un rapport
ne porte l'identité de son auteur que pour le siège 0, et la réponse atteint le
joueur sur une page dédiée.

### Ce qui est en place

- Quatre états : Reçu / En cours / Corrigé / Refusé.
- Un fil dans les deux sens (`rapports_messages`), réservé au **siège 0** :
  c'est la seule identité sûre, et un rapport d'invité reste un rapport, ce que
  `/admin` dit noir sur blanc.
- `/admin` : le fil, un champ de réponse, le quatrième bouton d'état.
- `/signalements` : ses bugs, leur état, la capture, le fil, de quoi répondre.
  Deux vérifications, pas une : la page ne montre que ses tickets, et le POST
  cherche le numéro dans les tickets de celui qui parle.
- La pastille en partie passe par `/api/prives`, **sans toucher au moteur** ;
  une seconde pastille, d'une autre couleur, mène à `/signalements`.
- La purge n'efface plus la ligne : à 30 jours la capture part, le fil reste.

### Ce qui n'est PAS fait, et c'est voulu

Aucune modale sur le plateau (le pire endroit pour relire un fil), aucun ticket
ouvert sans bug, aucun courrier électronique, et le tchat retiré le 12/09 n'est
pas réveillé : le fil a sa propre table.

### Reste

Le volume : si le suivi se remplit de tickets jamais fermés, la question de
l'archivage se posera d'elle-même. Non tranchée.
