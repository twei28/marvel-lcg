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

### ⚠ Ce qui reste ouvert est le chemin le PLUS fréquent, pas le moins

1. **L'écran de fin de partie, et c'est le trou principal.** `EcranFinPartie`
   propose « Menu » (`onMenu`), qui navigue vers `/prepare.html` **sans rien
   fermer et sans confirmation**. Or c'est le déroulement NORMAL d'une
   soirée : on joue, la partie se termine, l'hôte revient au menu et relance.
   **Ce chemin-là mène toujours au défaut, et c'est le plus emprunté.** Ce qui
   est corrigé — quitter au milieu d'une partie — est le cas rare.

   Corollaire à trancher : il y a désormais **deux boutons nommés « Menu »**,
   à deux écrans d'écart. Celui du plateau détruit la table ; celui de la fin
   de partie non. Rien à l'écran ne distingue les deux.

2. **L'invité qui recharge sa page** (le cas qui coince, plus haut) : entier.
3. **Le corollaire des trois messages** (« Connexion à la partie… ») : entier.
   Adouci seulement : l'invité dont la table vient d'être fermée lit « l'hôte
   a peut-être fermé la table » au 3e essai de reconnexion (≈ 6 s) au lieu
   d'attendre 29 s, et la sortie lui est offerte au même moment.

Autrement dit : le contournement du jour est devenu un geste à portée de clic,
mais il ne couvre que la sortie en cours de partie. **Le signal juste (piste 1,
le siège et son héros) reste la vraie réponse**, et c'est la seule qui ferme le
chemin de la fin de partie sans obliger l'hôte à repasser par le site à chaque
manche.

---

## État au 21/09/2026

**Moitié faite.** « Quitter la partie » éteint désormais vraiment la table
(commits `9a4adfa6`, `f2493533`, `974f76fb`, puis deux rondes de correction).
L'hypothèse du salon redevient vraie **quand l'hôte quitte en cours de partie**.

⚠ **Mais c'est le cas RARE.** Le chemin le plus emprunté reste ouvert : on
joue, l'écran de fin s'affiche, l'hôte clique « Retour au menu » et relance.
C'est le déroulement normal d'une soirée, et le moteur porte encore la partie
qui vient de finir. L'utilisateur a tranché le 21/09 : on fait **la piste 1**.

### Deux résidus de polissage, nommés comme tels par la revue

- La sortie du bandeau de reconnexion utilise `lienAccueil()` seul alors que la
  cascade à trois rangs existe juste à côté. `site.url || lienAccueil()` serait
  strictement meilleur. Sans effet sur ce déploiement.
- En partie LOCALE, l'affirmation forte « Cette table a été fermée » n'est pas
  gardée alors que la phrase faible l'est, et son bouton mène à la racine du
  moteur, qui n'a aucune route `/` : 404 s'il vit, connexion refusée s'il est
  mort. Pas une régression (c'était `http://0.0.1/` avant), et aucune
  destination correcte n'existe sans site. Le geste juste serait de masquer ce
  bouton quand l'origine est connue et vide.

---

## Fait le 21/09/2026 : la piste 1, le siège et son héros

**Le défaut est fermé sur le salon ordinaire.** Le salon n'interroge plus
`/get_play_scene_name` mais une route neuve, `/get_heros_du_siege?p=N`, et ne
bascule que quand le héros de SON siège, dans la partie en cours, est celui que
l'invité vient de choisir. Insensible à l'ancienne partie encore chargée, au
rechargement, à l'onglet rouvert et à deux parties du même scénario.

Commits : `2ba88d97` (la règle pure et ses 14 cas), `e61614db` (la route moteur
et ses 13 témoins), `c7ff6590` (le salon branché dessus). Rapport :
`.planning/rapports/2026-09-21-salon-attend-sa-partie.md`.

Verdicts : 14/14 (`npm run bascule-salon`), 11/11 (`tools/test_heros_du_siege.py`),
15/15 + 3/3 (`tools/test_authentification.py`), **48/48 VERT**
(`tools/test_mode_manuel.py` en entier).

Trois décisions prises au passage, pour qu'on ne les redécouvre pas :

1. **Le choix de l'invité est retenu dans SON navigateur** (`localStorage`, par
   siège, périmé à six heures, effacé dès qu'il a servi). `/new` vide
   `choix_sieges` côté serveur — et c'est voulu — donc un invité qui recharge
   après le lancement n'a plus que cette trace. Un archivage côté serveur des
   choix « déjà joués » a été écarté : il collerait à l'ancienne partie encore
   chargée et rouvrirait le défaut.
2. **La route est gardée par `tient_le_siege`, pas `allowed_seats`.** La
   première version prenait `allowed_seats` et le témoin d'authentification l'a
   prise en faute : un invité du siège 1 lisait le siège 2, parce que
   `allowed_seats` ouvre les sièges orphelins et qu'avant le lancement ils le
   sont tous.
3. **On ne publie qu'un siège et un identifiant de carte héros.** Pas de deck,
   pas de main, pas les autres sièges.

### ⚠ Ce qui reste ouvert

1. **Le corollaire des trois messages** (« Connexion à la partie… ») : entier.
2. **Rien n'est déployé.**

---

## Ronde de correction 1, le 21/09/2026 : le héros seul ne suffisait pas

⚠ **Cette section prévaut sur celle du dessus partout où elles se
contredisent.** Rapport complet au §7 de
`.planning/rapports/2026-09-21-salon-attend-sa-partie.md`.

**Le trou : rejouer une manche AVEC LE MÊME HÉROS**, ce que fait la majorité des
joueurs. Entre deux manches, le moteur porte encore le monde de la précédente
avec le héros de l'invité à son siège ; `/new` ayant vidé `choix_sieges`,
l'invité re-choisit le même héros et son siège « tient son héros » dans
l'ANCIENNE partie. Il y repartait. Le 20/09 à l'identique, sur le chemin même que
le correctif visait. Aucune mémoire n'était en cause : le choix est refait en
direct.

⚠ **Et la note du dessus qui dit que la mémoire locale distingue « moi » de
« celui qui était assis là avant moi » est FAUSSE.** Elle distingue un héros
d'un autre héros, rien de plus. L'arbitrage (écarter l'archivage serveur) reste
bon : il aurait eu le même angle mort.

**Le remède : DEUX signaux, dont aucun ne tient seul.** Le héros (« ce siège est
à moi ») et la fraîcheur (« cette partie a commencé après que je me suis posé »).
Le repère de fraîcheur est `debut = game_uid:game_id`, la clé que le plateau
emploie déjà pour la même question (`clePartie`) — donc aucune convention neuve.
Il est relevé **au moment du choix** et retenu **avec lui**, ce qui le fait
survivre au rechargement.

**La CAMPAGNE est fermée aussi, et la piste notée plus haut était fausse.**
Traduire `membre.heros` en `heroCardId` ne laisserait pas le défaut ouvert, ça le
**garantirait** : l'équipe est fixe d'une manche à l'autre, donc le siège N tient
toujours le même héros. (Et `server_campagne.py` ne publie jamais `identite`,
donc une équipe à variante ne correspondrait jamais.) En campagne, seule la
fraîcheur peut servir de signal — et elle y suffit seule.

**Deux gardes réparées** : `/set_choix_siege` était resté sur `allowed_seats` (un
invité du siège 1 écrivait le choix du siège 2, rouge constaté), et le spectateur
n'était pas mesuré sur `/get_heros_du_siege`.

**Chaque message a maintenant sa sortie** : « Rejoindre avec *X* » quand le siège
joue un autre héros, « Rejoindre cette partie » quand elle est indatable. Un
message honnête sans issue n'était un progrès qu'à moitié.

Commits : `4436f3de`, `1cfc1782`, `741bdacb`, `aaf0acbc`.
Verdicts : 25/25 (`npm run bascule-salon`), 16/16 (`test_heros_du_siege.py`),
19/19 + 3/3 (`test_authentification.py`), **48/48 VERT** (`test_mode_manuel.py`).

### Ce qui reste après la ronde

1. **⚠ Rien n'a été vu à l'écran**, et c'est la zone qui contenait les deux
   défauts d'assemblage ci-dessus. Les règles, la route et les gardes sont
   prouvées ; l'assemblage ne l'est pas.
2. **Le repère change aussi quand l'hôte ANNULE un geste** (`LoadScene` passe par
   `SetScene`). Si l'hôte annule dans la manche précédente pendant qu'un invité
   attend **et** que son siège y tient son héros, l'invité basculerait à tort.
   Cas très étroit, non mesuré.
3. **Le corollaire des trois messages** : entier.
4. **Rien n'est déployé.**
