# « Quitter la partie » ferme la table

21/09/2026, branche `mode-manuel`. Six commits, en deux rondes.

| Hachage | Portée |
|---|---|
| `9a4adfa6` | site : `/api/eteindre`, et `eteindre_volontairement` partagée |
| `f2493533` | moteur : `POST /quitter_la_table` |
| `974f76fb` | plateau : le bouton ⌂ Menu ferme la table, et le dit |
| `d7f2b189` | site : le fil qui tue ne démarre qu'APRÈS la réponse |
| `2f31f1ef` | moteur : trois issues à la fermeture, jamais deux |
| `b2c91d78` | plateau : ne rien affirmer quand on ne sait pas |

La ronde de correction a porté sur un seul sujet, décliné à trois étages :
**réduire à deux ce qui en fait trois**. « C'est fermé / ce n'est pas fermé »
était faux, et faisait dire au plateau le contraire de la vérité au pire
moment. Le détail est au chapitre « Le piège d'enchaînement ».

---

## Ce qui a changé pour le joueur

L'hôte clique ⌂ Menu. La fenêtre de confirmation ne dit plus « La partie en
cours sera perdue si tu ne l'as pas sauvegardée » mais :

> **Fermer la table ?**
> La table va disparaître : les autres joueurs sont déconnectés, et il faudra
> en rouvrir une depuis le site pour rejouer. La partie en cours est mise de
> côté — le site te la proposera sous « Reprendre ».
>
> [ Annuler ] [ **Quitter** ]

(Le texte ne dit plus « perdue si tu ne l'as pas sauvegardée » : c'était faux.
`_sauvegarder_avant_extinction` écrit la partie avant de tuer le moteur et la
range dans « Reprendre ». Effrayer sur un geste déjà lourd, pour rien.)

Il confirme. Le moteur s'éteint, l'emplacement est rendu, le mot de passe de
jeu est révoqué (les cookies des invités d'hier ne rouvrent plus rien), et
l'hôte atterrit sur la page **du site** qui dit « Ton jeu est éteint — rien
n'est perdu », avec son bouton « Rallumer mon jeu ».

Un **invité** ou un **spectateur** ne voit rien de tout cela : pour lui, le
bouton fait ce qu'il a toujours fait, avec l'ancien texte, et il part sans rien
détruire. Une **partie locale** (JOUER-SOLO.bat) non plus : il n'y a aucune
table à rendre à personne, et `/prepare.html` reste vivant puisque le moteur ne
s'éteint pas.

Et quand le plateau **ne sait pas** s'il y a un site derrière (la lecture de
l'adresse a échoué), il le dit au lieu de faire comme si de rien n'était :
« Si cette table vient du site, elle va se fermer […] Le plateau n'a pas pu le
vérifier. » Puis il demande quand même au moteur, qui, lui, sait.

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

**1. Le site répond AVANT d'éteindre, et le fil qui tue ne démarre qu'ensuite.**
Celui qui attend la réponse de `/api/eteindre` est le moteur qu'on est en train
de tuer. Éteindre d'abord, c'est tuer le messager : le plateau n'obtient jamais
de réponse et ne sait pas où aller. `eteindre_volontairement(..., differer=True)`
révoque le mot de passe tout de suite — l'ordre documenté tient donc toujours —
et **rend** la fonction qui éteindra, appelée après `_repondre`. Deux témoins :
un chronomètre (la réponse part en moins d'une seconde là où l'extinction en
prend une et demie) et un **ordre** (`['repondu', 'eteint']`), parce que le
chronomètre seul passe encore si le fil démarre une ligne trop tôt.

**2. On n'atterrit jamais sur une page du moteur.** L'adresse de destination
vient du **site**, seul à connaître le domaine public placé devant les tables,
et elle ressort telle quelle jusqu'au plateau. Pas d'adresse rendue, pas de
fermeture annoncée : le plateau requalifie alors l'issue en « inconnue ». C'est
une gate, pas un repli.

**3. ⚠ Trois issues, jamais deux — et c'est la correction la plus importante de
cette ronde.** La première version écrasait tout échec en « rien n'a été
détruit : la table et les autres joueurs sont toujours là ». C'était **faux**,
et dangereusement : `/api/eteindre` révoque et lance l'extinction **avant** de
répondre, et il n'existe aucun chemin d'abandon de son côté. Passé le plafond
de dix secondes du moteur, la table disparaît quand même — on affichait donc
« rien n'a été détruit » pendant qu'elle s'en allait, et on proposait « Rester
sur la partie » sur un moteur condamné. Exactement ce que l'utilisateur venait
de redouter en cliquant.

Le moteur distingue désormais, et le plateau avec lui :

| Issue | Quand | Ce qu'on dit |
|---|---|---|
| `sans-site` | aucun site configuré : personne n'a été appelé | rien, on retourne à l'écran des héros |
| `fermee` | le site a confirmé et donné l'adresse | la table est fermée, on y va |
| `refusee` | 403 du moteur, avant tout appel | « Rien n'a été touché » — **la seule issue où l'on peut l'affirmer** |
| `inconnue` | le site a été sollicité et n'a pas confirmé | « La table est peut-être en train de se fermer […] le site, lui, le sait » + **Ouvrir le site** |

Le moteur ne pouvait pas distinguer `sans-site` d'`inconnue` avec
`_appeler_site` seule (statut 0 dans les deux cas) : il lit donc `site_interne`
et `site_jeton` **avant** d'appeler.

**4. L'adresse du site est lue au montage, plus au clic.** `urlDuSite()` était
un `fetch` sans plafond dans le chemin du bouton. Deux conséquences, et la
seconde était la mauvaise : un moteur qui traîne laissait la fenêtre ne jamais
s'ouvrir (au moment précis où ça rame, c'est-à-dire quand on cherche à partir),
et un `fetch` en échec faisait passer l'hôte pour un **joueur local** — ancienne
fenêtre, départ, table laissée debout avec l'ancienne partie dedans. **Le défaut
d'origine, rétabli en silence par un hoquet réseau.** La lecture se fait
maintenant une fois au montage, plafonnée à 2 s par un `AbortController`, et
l'échec donne un état `inconnu` qui n'est **jamais** confondu avec « aucun
site ».

**5. Les invités attendaient vingt-neuf secondes, pas une.** Correction d'un
chiffre faux du premier rapport : `DELAIS_RECONNEXION = [2, 4, 8, 15, 30]` et
`ESSAIS_AVANT_TABLE_FERMEE = 5`, donc 2+4+8+15 ≈ **29 s** de « Connexion
perdue » avant que le bandeau ne dise la vérité. Acceptable quand seul un
déploiement pouvait fermer une table ; plus du tout maintenant que l'hôte le
fait d'un bouton, en cours de soirée. Un palier intermédiaire a été ajouté
(`ESSAIS_AVANT_DOUTE = 3`, ≈ 6 s) : le bandeau ajoute « — l'hôte a peut-être
fermé la table » et **offre la sortie** dès cet instant. Le seuil d'affirmation
reste à cinq essais : une vraie coupure met le même temps à revenir, et déclarer
la fermeture à six secondes serait faux une fois sur deux.

**6. Les invités ne restent pas sur un écran gelé.** Vérifié, et c'était déjà
en place : `BandeauConnexion` finit par afficher « Cette table a été fermée. Ta
partie n'est plus en cours. » avec « Revenir à l'accueil » — et `lienAccueil()`
retire le sous-domaine `pN.`, donc mène au SITE, pas au moteur mort. Cette
fonction a déménagé dans `quitter-la-table.ts` : c'est la même question (« où
aller quand le moteur n'est plus là ? »), et le départ volontaire s'en sert
comme dernier recours quand personne n'a su donner d'adresse.

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
| `site/test_parcours.py` | **0 échec** (7 cas neufs sur `/api/eteindre`) |
| `site/test_{narval,langue,places,routes_chemin,heure_locale,imports_locaux}.py` | tout vert |
| `tools/test_quitter_la_table.py` (neuf) | **TOUT PASSE** : 11 cas + 3 `sans_site` + 3 `site_muet` |
| `tools/test_mode_manuel.py` (48 cas) | **48 VERT, 0 ROUGE** (relancée après la ronde de correction) |
| `ui-app` : `quitter-la-table.test.ts` (neuf) | 18 cas verts |
| `ui-app` : `PagePartie.test.tsx` | 30 cas verts, dont 10 neufs |
| `ui-app` : la batterie entière | **1936 cas, 175 fichiers, 0 échec** |
| `npx tsc --noEmit` | silencieux |

Rouges constatés avant d'écrire le code, à chaque étage et à chaque ronde :

- site : 5 cas rouges (`404 Introuvable` sur `/api/eteindre`) ;
- site, ordre du fil : l'appel remis **avant** `_repondre` le temps d'une
  exécution → `['eteint', 'repondu']`, rouge, puis remis en place ;
- moteur : 7 cas rouges (`405` : la route n'existait pas), puis 4 de plus à la
  ronde de correction (`issue` absente : `sans-site`, `inconnue`, l'adresse du
  site) ;
- plateau, module : 18 cas rouges (les fonctions n'existaient pas sous cette
  forme) ;
- plateau, **câblage** : l'ancien `board.tsx` remis en place le temps d'une
  exécution, **4 des 5 cas d'alors rouges** ;
- plateau, **bandeau** : `ESSAIS_AVANT_DOUTE` remis à 5 (l'ancien
  comportement) → le cas du 3e essai rouge, celui du 2e vert. Le palier mesure
  bien ce qu'il prétend.

Deux témoins passent des deux côtés, et c'est assumé : « renoncer ne ferme
rien » et le refus du **spectateur** (`SpectateurPeutEcrire` refusait déjà par
défaut). Ce sont des garde-fous contre une régression future, pas des mesures
d'un changement. Le témoin du spectateur combine exprès le cookie `spectateur`
**et** la clé de l'hôte : c'est le double verrou qu'il garde.

La batterie moteur a tourné sur `.game-src-par9`, dossier jetable créé pour
l'occasion et **supprimé ensuite** — jamais `.game` ni `.game-src`. Ports
45700-45900 pour ne pas croiser l'autre session (36xxx).

---

## Mes inquiétudes

1. **Rien n'est déployé, et le plateau est un bundle.** Le code TypeScript ne
   part pas en production tant que `bash ui-app/deployer.sh` n'a pas reconstruit
   le bundle, puis `deployer.ps1`. Tant que ce n'est pas fait, le bouton se
   comporte comme avant, en production. Aucun déploiement n'a été lancé, comme
   demandé.

2. **⚠ L'écran de fin de partie garde l'ancien chemin, et c'est le chemin le
   PLUS fréquent — pas le moins.** Rectification de ce que disait la première
   version de ce rapport. `EcranFinPartie` propose « Menu »
   (`onMenu={retourMenu}`), qui navigue vers `/prepare.html` **sans
   confirmation et sans rien fermer**. Or le déroulement normal d'une soirée
   est : on joue, la partie se termine, l'hôte revient au menu et relance.
   **Ce chemin-là mène toujours au défaut.** Quitter au milieu d'une partie,
   ce que ce chantier corrige, est le cas rare.

   Ne pas y toucher reste le bon choix de portée — fermer la table à chaque
   fin de manche obligerait à repasser par le site entre deux parties —, mais
   il ne faut pas le lire comme « le défaut ne peut plus bloquer une soirée ».
   Le vrai correctif de ce cas-là est la piste 1 de la fiche (le salon attend
   le héros de SON siège).

   Corollaire à trancher, et c'est une question d'interface : **il y a
   désormais deux boutons nommés « Menu », à deux écrans d'écart. L'un détruit
   la table, l'autre non, et rien ne le dit.**

3. **Les invités attendent six secondes pour un soupçon, vingt-neuf pour la
   certitude.** Le palier ajouté (« l'hôte a peut-être fermé la table », plus
   la sortie offerte) tombe au 3e essai. C'est mieux que la demi-minute
   précédente, mais ce n'est toujours pas une notification : personne ne
   PRÉVIENT les invités. Le seul moyen honnête de faire mieux serait que l'hôte
   annonce son départ avant de partir, ce qui demande un canal que ce chantier
   n'ouvre pas.

4. **La sauvegarde avant extinction repose sur un moteur encore vivant.**
   `_sauvegarder_avant_extinction` interroge le moteur, dans le fil différé,
   juste avant de le tuer. L'ordre est bon (on sauve, puis on tue) et c'est le
   code existant, inchangé — mais la fenêtre de confirmation en fait désormais
   une **promesse** (« le site te la proposera sous Reprendre »), alors que la
   fonction est au mieux-effort : elle n'écrit rien si le moteur ne répond pas
   dans les dix secondes, et ne lève jamais. La promesse est celle du mécanisme,
   pas une garantie. Si une partie manquait à l'appel après une fermeture,
   c'est là qu'il faudrait regarder.

5. **`racine` est calculée à trois endroits dans `orchestrateur.py`** (lignes
   286, ~3980, et la nouvelle route). Je n'ai pas dédupliqué : ce n'était pas
   demandé, et un helper introduit ailleurs aurait mélangé un nettoyage à une
   fonctionnalité. À faire un jour, seul.

6. **`lienAccueil` a déménagé** de `board.tsx` vers `quitter-la-table.ts`. Le
   bandeau de reconnexion l'importe désormais. C'est cohérent (même question :
   où aller quand le moteur n'est plus là) mais c'est un déplacement que
   personne n'a demandé ; il rend simplement le dernier recours disponible au
   départ volontaire.
