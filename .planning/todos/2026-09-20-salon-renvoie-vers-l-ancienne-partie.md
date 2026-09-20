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
