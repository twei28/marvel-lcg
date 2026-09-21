# Le salon renvoie les invités sur l'ANCIENNE partie

Constaté en direct le 20/09/2026, sur une table à trois. Deux symptômes, une
seule cause.

## Les symptômes

1. Un invité reste sur « Connexion à la partie… » sans jamais voir la table.
2. « Quand je relance une partie à plusieurs, on retombe sur l'ancienne. »

## La cause

`Fusion/marvel-lcg-src/public/js/salon/app.js:249-266`. Le salon interroge
`get_play_scene_name` toutes les deux secondes et bascule dès que la réponse
n'est pas vide :

```js
// Quand l'hôte lance, /get_play_scene_name cesse de rendre une chaîne vide.
// C'est le signal le moins coûteux : aucune route à ajouter.
if (nom) location.href = `/app/board.html?p=${siege}&multi=1`;
```

**Le commentaire dit l'hypothèse, et c'est elle qui est fausse** : il suppose
que la table est VIDE avant que l'hôte lance. Or l'emplacement appartient au
compte et garde sa partie précédente tant que personne ne l'a éteint. Le nom de
scène n'est donc jamais vide, et l'invité est expédié sur l'ANCIENNE partie
avant d'avoir pu choisir son héros.

Il y reste bloqué, parce que cette partie-là attend une réponse d'un siège que
plus personne ne tient. Les deux joueurs sont coincés, et rien à l'écran ne
dit pourquoi.

## Ce qu'il faut

Le signal doit distinguer LA partie attendue, pas « une partie ». Deux pistes,
par ordre de préférence :

1. **Comparer un identifiant de lancement.** L'hôte connaît la partie qu'il
   vient de lancer ; le salon devrait attendre CELLE-LÀ. Une date de début
   postérieure à l'ouverture du salon suffirait déjà.
2. **Vider la table à la création d'une nouvelle partie**, pour que
   l'hypothèse du commentaire redevienne vraie. Plus simple, mais ça déplace
   le problème sur qui doit éteindre, et quand.

⚠ Corollaire à traiter aussi : le plateau affiche **le même message**
(« Connexion à la partie… ») quand il n'est pas connecté ET quand il attend la
levée du voile d'ouverture (`ui-app/src/board.tsx:2942`). L'invité ne peut pas
distinguer « ça charge » de « j'attends les autres » ni de « je suis sur la
mauvaise partie ». Trois situations, un seul message.

## Contournement du jour

Éteindre la table avant de relancer. Fait à la main le 20/09 à 19 h 30, sur
demande : le groupe de processus du moteur reçoit un SIGTERM, l'orchestrateur
constate la mort dans la minute et libère l'emplacement.

---

## Conception, écrite le 21/09/2026

`Game.NewGame` (`src/game/game.py:128`) est le point d'entrée UNIQUE d'une
nouvelle partie lancée depuis l'assistant. Un compteur incrémenté là donne un
repère qui change à chaque partie, exposé par une petite route à part (ne pas
étendre `get_play_scene_name` : `public/js/sandbox/app.js` lit son corps en
texte brut et testerait vrai sur n'importe quoi).

Le salon compare alors au repère qu'il a relevé **en arrivant**. Tant que le
repère n'a pas changé, la partie affichée est l'ANCIENNE, et l'invité reste
sur son choix de héros.

### Le cas qui coince, et il faut le trancher

Un invité qui **recharge sa page** après le lancement relèverait le nouveau
repère comme étant le sien, ne verrait plus aucun changement, et resterait
bloqué sur le salon pendant que sa partie tourne. On aurait échangé un
symptôme contre un autre.

Trois réponses possibles, par ordre de robustesse :

1. **Le siège et son héros.** Une route qui dit quels sièges portent un héros
   dans la partie en cours, et lequel. L'invité bascule quand le héros de SON
   siège est celui qu'il vient de choisir. Insensible au rechargement,
   insensible à l'ancienne partie, insensible à un scénario homonyme. C'est la
   réponse juste, et la plus longue : il faut que le salon sache ce que
   l'invité a choisi, ce qu'il sait déjà, et une route de plus.
2. **Le repère, gardé dans `sessionStorage`.** Le rechargement conserve le
   repère d'arrivée, donc le cas coincé disparaît pour un rechargement. Il
   reste pour un onglet fermé puis rouvert. Court à écrire, couvre
   l'essentiel, ment dans un cas rare.
3. **Le repère seul.** Le plus court. Règle le problème d'aujourd'hui et crée
   celui du rechargement. À écarter.

Recommandation : la 1, parce que c'est la seule qui répond à la vraie question
(« la partie qui a commencé est-elle la MIENNE ? ») au lieu de la contourner.
La 2 si on veut un correctif ce soir.

---

## Ce qui est fait au 21/09/2026 : la piste 2, par le bouton « Quitter »

La piste 2 ci-dessus (« vider la table à la création d'une nouvelle partie »)
demandait de trancher **qui doit éteindre, et quand**. C'est tranché, et pas
par le moteur : c'est **l'hôte**, quand il quitte.

« Quitter la partie » (bouton ⌂ Menu du plateau, PC et mobile) ferme désormais
la table pour de bon : moteur éteint, emplacement rendu, mot de passe révoqué,
invités déconnectés. Décision de l'auteur, qui accepte de rouvrir une table
depuis le site pour rejouer. Le chemin : `/quitter_la_table` (moteur) →
`/api/eteindre` (site, en 127.0.0.1, jeton de partie). Rapport :
`.planning/rapports/2026-09-21-quitter-eteint-la-table.md`.

**L'hypothèse du commentaire du salon est donc vraie sur CE chemin** : l'hôte
qui a quitté n'a plus de table du tout, et celle qu'il rouvrira sera vide.

### Ce qui reste ouvert, et c'est volontaire

1. **L'hôte qui ne quitte pas.** Rien n'oblige à passer par ce bouton :
   l'écran de fin de partie propose « Menu » (`EcranFinPartie`, `onMenu`), qui
   navigue vers `/prepare.html` **sans rien fermer**, et sans confirmation.
   Un hôte qui finit une partie, revient au menu et relance retombe donc
   exactement sur le défaut d'origine.
2. **L'invité qui recharge sa page** (le cas qui coince, plus haut) : entier.
3. **Le corollaire des trois messages** (« Connexion à la partie… ») : entier.

Autrement dit : le contournement du jour est devenu un geste à portée de clic,
et le défaut ne peut plus bloquer une soirée tant que l'hôte quitte proprement.
Le signal juste (piste 1, le siège et son héros) reste à écrire.
