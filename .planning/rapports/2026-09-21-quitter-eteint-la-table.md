# « Quitter la partie » ferme la table

21/09/2026, branche `mode-manuel`. Trois commits :

| Hachage | Portée |
|---|---|
| `9a4adfa6` | site : `/api/eteindre`, et `eteindre_volontairement` partagée |
| `f2493533` | moteur : `POST /quitter_la_table` |
| `974f76fb` | plateau : le bouton ⌂ Menu ferme la table, et le dit |

---

## Ce qui a changé pour le joueur

L'hôte clique ⌂ Menu. La fenêtre de confirmation ne dit plus « La partie en
cours sera perdue si tu ne l'as pas sauvegardée » mais :

> **Fermer la table ?**
> La table va disparaître : la partie en cours est perdue si tu ne l'as pas
> sauvegardée, les autres joueurs sont déconnectés, et il faudra rouvrir une
> table depuis le site pour rejouer.
>
> [ Annuler ] [ **Quitter** ]

Il confirme. Le moteur s'éteint, l'emplacement est rendu, le mot de passe de
jeu est révoqué (les cookies des invités d'hier ne rouvrent plus rien), et
l'hôte atterrit sur la page **du site** qui dit « Ton jeu est éteint — rien
n'est perdu », avec son bouton « Rallumer mon jeu ».

Un **invité** ou un **spectateur** ne voit rien de tout cela : pour lui, le
bouton fait ce qu'il a toujours fait, avec l'ancien texte, et il part sans rien
détruire. Une **partie locale** (JOUER-SOLO.bat) non plus : il n'y a aucune
table à rendre à personne, et `/prepare.html` reste vivant puisque le moteur ne
s'éteint pas.

## Pourquoi ça comptait

Le salon des invités (`public/js/salon/app.js:249-266`) bascule vers le plateau
dès que la table porte une partie, quelle qu'elle soit. Son commentaire énonce
une hypothèse — « la table est vide avant que l'hôte lance » — que rien ne
rendait vraie : l'emplacement appartient au compte et garde sa partie
précédente tant que personne ne l'éteint. Les invités étaient donc expédiés sur
l'ANCIENNE partie avant d'avoir choisi leur héros, et y restaient bloqués. Deux
soirées perdues, les 19 et 20/09.

Le contournement du 20/09 était d'éteindre la table à la main, depuis le site,
avant de relancer. Ce chantier en fait un geste à portée de clic, sur le bouton
que l'hôte utilisait déjà.

La fiche du défaut (`.planning/todos/2026-09-20-salon-renvoie-vers-l-ancienne-partie.md`)
est annotée en conséquence : ce qui est couvert, et ce qui reste.

---

## Le chemin choisi, et pourquoi

Trois chemins étaient sur la table.

### 1. Le moteur relaie — **retenu**

`POST /quitter_la_table` (moteur) → `POST /api/eteindre` (site, en 127.0.0.1,
authentifié par le jeton de partie), exactement le chemin que le moteur emprunte
déjà pour le tchat, l'annonce et les rapports de bug (`_appeler_site`).

Ce qui l'emporte, et ce n'est pas le nombre de pièces :

- **Le droit de fermer se vérifie là où la preuve existe.** Côté site, le jeton
  dit de quelle TABLE vient l'appel, jamais qui a cliqué : `/api/eteindre` ne
  peut pas distinguer l'hôte d'un invité. Le cookie `seat_token_0`, lui,
  n'existe que côté moteur. Tout chemin qui laisse le site décider donne à
  n'importe quel invité le pouvoir de fermer la table de son hôte.
- **L'utilisateur vient de confirmer une fois.** Un deuxième clic sur une page
  du site pour la même décision, c'est la lui faire reprendre.
- **Aucune requête croisée, aucun assouplissement de cookie.** Le détour par
  127.0.0.1 existe précisément pour ça, et il est déjà là.
- **`/eteindre` n'est pas touchée** : ni transformée en GET, ni contournée. Son
  ordre d'opérations (révoquer, puis éteindre) est désormais écrit **une seule
  fois**, dans `eteindre_volontairement`, que `/eteindre` et `/api/eteindre`
  partagent — avec le piège du `meta refresh` documenté au même endroit.

### 2. Renvoyer vers une page du site qui porte le bouton — écarté

Minimal, mais il ajoute un clic à une décision déjà prise, et surtout il ne
résout pas la question du droit : la page du site n'aurait aucun moyen de savoir
que celui qui arrive est bien l'hôte, sinon son cookie de session — que les
invités n'ont pas, ce qui les laisserait sans aucune sortie propre.

### 3. Autre chose — mesuré, non retenu

Faire éteindre le moteur par lui-même (il connaît son PID) : il rendrait le
processus, pas l'**emplacement**. Le site tient la comptabilité des tables, la
base des comptes et le mot de passe de jeu ; un moteur qui se suicide laisse
l'emplacement marqué occupé jusqu'au passage du faucheur, et le mot de passe
des invités valable un an. C'est le contournement du 20/09, pas un correctif.

---

## Le piège d'enchaînement, et comment il est désamorcé

La question posée en ouverture — « et si le joueur restait sur une page morte
du moteur qu'on vient de tuer ? » — était juste, et elle a façonné deux
décisions.

**1. Le site répond AVANT d'éteindre.** Celui qui attend la réponse de
`/api/eteindre` est le moteur qu'on est en train de tuer. Éteindre d'abord,
c'est tuer le messager : le plateau n'obtient jamais de réponse et ne sait pas
où aller. `eteindre_volontairement(..., rendre_la_main=True)` révoque le mot de
passe tout de suite (l'ordre tient donc toujours) et reporte la seule extinction
dans un fil. Un cas mesure ce délai : la réponse doit partir en moins d'une
seconde là où l'extinction en prend une et demie.

**2. On n'atterrit jamais sur une page du moteur.** L'adresse de destination
vient du **site**, seul à connaître le domaine public placé devant les tables,
et elle ressort telle quelle jusqu'au plateau. Pas d'adresse rendue, pas de
fermeture annoncée : `fermerLaTable()` (plateau) refuse de déclarer la table
éteinte sans destination, et le joueur reste sur sa partie. C'est une gate, pas
un repli.

**3. Si la fermeture échoue, on le dit.** Le joueur vient de s'entendre annoncer
la disparition de sa table ; partir en silence vers `/prepare.html` lui
laisserait croire qu'elle a eu lieu. Il voit donc :

> **La table n'a pas pu être fermée.**
> Le site n'a pas répondu. Rien n'a été détruit : la table et les autres
> joueurs sont toujours là.
>
> [ Rester sur la partie ] [ Revenir au menu quand même ]

**4. Les invités ne restent pas sur un écran gelé.** Vérifié, et c'était déjà
en place : après cinq tentatives de reconnexion, `BandeauConnexion` affiche
« Cette table a été fermée. Ta partie n'est plus en cours. » avec un bouton
« Revenir à l'accueil » — et `lienAccueil()` retire le sous-domaine `pN.`, donc
mène au SITE, pas au moteur mort. La chaîne tient de bout en bout.

---

## Le bouton mobile

**Oui, il mène au même endroit, et un seul câblage a suffi.**
`PlateauPortrait` passe `menu={props.actionsPartie}` à `BandeauPortrait`, et
`actionsPartie` est le `.board-actions` du plateau PC rendu **tel quel**
(board.tsx:3497). Le bouton `bh-menu` de la feuille basse mobile est donc
littéralement le même nœud React, avec le même `onClick={retourMenuPrincipal}`.
Rien à écrire de plus ; c'est dit en commentaire aux deux endroits pour que
personne ne le dédouble plus tard.

---

## Les tests

| Batterie | Verdict |
|---|---|
| `site/test_parcours.py` | **0 échec** (6 cas neufs sur `/api/eteindre`) |
| `site/test_{narval,langue,places,routes_chemin,heure_locale,imports_locaux}.py` | tout vert |
| `tools/test_quitter_la_table.py` (neuf) | **TOUT PASSE**, 9 cas + 3 en mode `sans_site` |
| `tools/test_mode_manuel.py` (48 cas) | **48 VERT, 0 ROUGE** |
| `ui-app` : `quitter-la-table.test.ts` (neuf) | 11 cas verts |
| `ui-app` : `PagePartie.test.tsx` (5 cas neufs) | 25 cas verts |
| `ui-app` : la batterie entière | **1924 cas, 175 fichiers, 0 échec** |
| `npx tsc --noEmit` | silencieux |

Rouges constatés avant d'écrire le code, à chaque étage :

- site : 5 cas rouges (`404 Introuvable` sur `/api/eteindre`) ;
- moteur : 7 cas rouges (`405` : la route n'existait pas) ;
- plateau, module : le fichier ne se résolvait pas ;
- plateau, **câblage** : l'ancien `board.tsx` remis en place le temps d'une
  exécution, **4 des 5 cas neufs rouges** — dont « ferme vraiment la table de
  l'hôte » et « annonce la fermeture ». Le cinquième (« renoncer ne ferme
  rien ») passe des deux côtés : c'est un garde-fou, pas une mesure.

La batterie moteur a tourné sur `.game-src-par9`, dossier jetable créé pour
l'occasion et **supprimé ensuite** — jamais `.game` ni `.game-src`. Ports 45800+
pour ne pas croiser l'autre session (36xxx).

---

## Mes inquiétudes

1. **Rien n'est déployé, et le plateau est un bundle.** Le code TypeScript ne
   part pas en production tant que `bash ui-app/deployer.sh` n'a pas reconstruit
   le bundle, puis `deployer.ps1`. Tant que ce n'est pas fait, le bouton se
   comporte comme avant, en production. Aucun déploiement n'a été lancé, comme
   demandé.

2. **L'écran de fin de partie garde l'ancien chemin, et c'est le trou qui
   reste.** `EcranFinPartie` propose « Menu » (`onMenu={retourMenu}`), qui
   navigue vers `/prepare.html` **sans confirmation et sans rien fermer**. Un
   hôte qui termine une partie, revient au menu et relance retombe donc
   exactement sur le défaut d'origine. C'est hors de la demande (« quitter la
   partie »), et cela demande un arbitrage : à la fin d'une partie, vouloir en
   relancer une est le cas NORMAL, et fermer la table obligerait à repasser par
   le site à chaque fois. Le vrai correctif de ce cas-là est la piste 1 de la
   fiche (le salon attend le héros de SON siège), pas une fermeture de plus.

3. **Une seconde de flottement chez les invités.** Entre l'extinction et le
   bandeau « Cette table a été fermée », il s'écoule cinq tentatives de
   reconnexion. Ce n'est pas nouveau et le message final est juste, mais un
   invité qui regarde son écran à cet instant voit « Connexion perdue » et peut
   croire que c'est son réseau. Rien ne lui dit que l'hôte vient de partir.

4. **La sauvegarde avant extinction repose sur un moteur encore vivant.**
   `_sauvegarder_avant_extinction` interroge le moteur, dans le fil différé,
   juste avant de le tuer. L'ordre est bon (on sauve, puis on tue) et c'est le
   code existant, inchangé — mais l'hôte a désormais une façon très rapide de
   déclencher ça, alors qu'avant il passait par le site. Si une partie était
   perdue à la fermeture, c'est ici qu'il faudrait regarder.

5. **La prédiction côté plateau coûte un aller-retour.** Pour savoir quel texte
   afficher, le plateau lit `/get_site_url` au clic, avant la confirmation. Si
   le moteur traîne, la fenêtre met un instant à s'ouvrir. Mesuré nulle part en
   conditions réelles : c'est une requête minuscule, mais elle est dans le
   chemin d'un clic.

6. **`racine` est calculée à trois endroits dans `orchestrateur.py`** (lignes
   286, 3959, et la nouvelle route). Je n'ai pas dédupliqué : ce n'était pas
   demandé, et un helper introduit ailleurs aurait mélangé un nettoyage à une
   fonctionnalité. À faire un jour, seul.
