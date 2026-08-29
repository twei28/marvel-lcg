# TODO / SPEC — Jouer une campagne en ligne, à plusieurs

**Statut :** **IMPLÉMENTÉ le 2026-08-12** (jalons A à D). Plan déroulé
(`.planning/plans/2026-08-12-campagne-en-ligne.md`), tâches 1 à 7 faites, huit
commits `e596187` à `2ccd41c`, déployé et compilé. Reste le **jalon E** : le test
Playwright à deux navigateurs et l'essai en vraie partie, qui demandent un humain.
⚠️ **Cette fiche se trompait sur son point central**, voir §2.
**Date de conception :** 2026-08-12
**Origine :** demande utilisateur (« on doit trouver un moyen de jouer les campagnes en ligne »)
**Rapport à la roadmap :** hors des 7 phases de la refonte UI. Voisin du todo
`2026-07-28-serveur-permanent-multijoueur.md`, mais indépendant : ce chantier-ci
fonctionne déjà sur le multi actuel (tunnel + mot de passe).

---

## 1. Le problème

Une partie en ligne à plusieurs fonctionne (`launcher-multi.sh`). Le mode
campagne fonctionne, pour les huit boîtes, carnets remplis automatiquement. Les
deux ensemble, non : **seul celui qui a lancé la partie sait qu'il joue une
campagne.** Les autres ont un plateau ordinaire.

## 2. Ce qui existe déjà (vérifié le 12/8/2026)

**La campagne est DÉJÀ côté serveur, entièrement.** C'est le point qui change le
cadrage du chantier, et il a été vérifié dans le code avant d'écrire cette fiche :

- `src/engine/device/web/server/server_campagne.py` sert `/list_campagnes`,
  `/get_campagne`, `/get_campagne_definition`, `/get_carnet_suggere`, et écrit
  par `/save_campagne` et `/delete_campagne`.
- Les campagnes en cours sont des fichiers, `../campagnes/*.json`, hors de
  `.game` qui est reconstruit à chaque lancement. Équipe figée, difficulté,
  scénarios terminés, carnet.
- Le carnet stocké est exactement le dict `campaign_log` que le moteur consomme
  (`game/operate/campaign_logs.py`), sans traduction entre les deux.
- Le secret d'Agents of S.H.I.E.L.D. ne sort jamais : `_sans_secret()` filtre
  toute réponse de route.

**Ce que le `localStorage` porte, et c'est tout :** la clé `mc-campagne-partie`,
posée par `public/js/campagne/app.js:869` juste avant de lancer un scénario, et
lue par `ui-app/src/board/campagne/contexte.ts:71`. Elle contient deux chaînes,
`{ id, scenario }`. Aucune donnée de campagne n'y vit.

**Ce blocage est réel** : un joueur qui rejoint n'a jamais posé cette clé,
`lireContexte()` rend `null`, et son plateau ignore la campagne — ni panneau de
récompenses, ni règle de défaite, ni carnet, ni règle de reprise.

⚠️ **MAIS la phrase qui suivait ici, « donc le blocage est là et nulle part
ailleurs », était FAUSSE**, et elle a envoyé ce chantier sur une fausse piste.
Mesuré le 12/8 avant d'écrire le plan, il y a un SECOND blocage, en amont et plus
dur :

- **L'écran des campagnes lance la partie tout seul, sans jamais passer par le
  salon.** `public/js/campagne/app.js:851` compose `joueurs` depuis
  `campagne.equipe`, pose la clé, appelle `launch()`. Les mots « salon », « multi »
  et « en ligne » n'apparaissent nulle part dans ce fichier.
- **Le salon est réservé au hot-seat.** `public/js/prepare/app.js:707` fait
  `if (!state.salon.multi || state.mode.id !== "hotseat") return null`, alors que la
  campagne lance avec `mode: { id: "campaign" }`. L'écran de préparation le dit
  lui-même en commentaire ligne 474 : « Cet écran ne lance donc jamais de partie de
  campagne. »

**Conséquence : avant ce chantier, une campagne était TOUJOURS hot-seat.** Les
distants n'avaient pas « un plateau qui ignore la campagne » : rien ne les
convoquait. D'où un jalon que cette fiche n'avait pas prévu (le salon, §4.7).

**Deux inquiétudes de cette fiche se sont révélées sans objet :**

- `lireContexte()` n'a que **deux** consommateurs (`PanneauRecompenses.tsx:102` et
  `RapportBug.tsx:44`). Le passage à l'asynchrone, redouté au §4.1, a coûté trois
  lignes.
- `PanneauRecompenses` est monté **sans aucune condition de siège**
  (`ui-app/src/board.tsx:1384`). Sa seule garde était `lireContexte()`. Dès que le
  contexte atteint tous les sièges, le panneau s'ouvre chez tout le monde **sans
  autre travail** : la question « direct ou attente ? » du §4.3 avait donc une
  réponse gratuite.
- `parJoueur` fait déjà plus que « exister dans les définitions » : `cleCarnet()`
  (`detecteurs.ts:485`) préfixe en `Player N <clé>`, et le panneau affiche déjà une
  ligne par joueur. Il ne restait qu'à décider qui a le droit d'y écrire.

## 3. Décisions prises avec l'utilisateur (12/8/2026)

| Question | Décision |
|---|---|
| Où vit la campagne | **Côté serveur**, partagée par la table. C'est déjà le cas : rien à déplacer |
| Qui remplit le carnet | **Chacun ses champs, l'hôte valide.** Les champs personnels (amélioration, carte d'aspect) sont saisis par le joueur concerné, les champs communs par l'hôte, qui clique « Valider » pour tous |
| Comment on retrouve une campagne | **Fichier serveur, choisi dans une liste** à l'écran des campagnes. C'est déjà le cas (`/list_campagnes`) |
| **Répartition des sièges** | **Par ordre, sans écran** : le siège N tient `equipe[N]`. C'est déjà ce que fait le moteur (`launch({players: joueurs})` donne `players[0]` au siège 0) : **rien à écrire** pour l'assignation. Décidé le 12/8, absent de la version d'origine de cette fiche |
| Le mode solo | La question portait sur une prémisse fausse (« le solo vit en localStorage »). Elle est **sans objet** : il n'y a qu'une seule voie, et elle est déjà serveur. Le solo est une table à un joueur. Réponse donnée : « deux voies », à revalider si le sujet ressort |

## 4. Les chantiers

### 4.1 Le contexte de campagne doit atteindre TOUS les sièges

**État :** ✅ **FAIT** (jalon A, `e596187` + `757fe03`). Route `/get_campagne_en_cours`, qui réutilise la déduction déjà enfouie dans `secret_pour_le_moteur()`, plus `resoudreContexte()` côté plateau. **Tranché** : le localStorage reste un raccourci pour l'hôte, la route sert de recours ; `lireContexte()` reste synchrone pour le rapport de bug, qui se prend au clic.

**Le fait :** la clé du localStorage n'existe que dans le navigateur de celui qui
a lancé.

**Le travail :** une route qui répond « la partie en cours appartient à la
campagne X, scénario Y ». **Le serveur sait déjà le déduire** :
`secret_pour_le_moteur()` retrouve la campagne concernée par la `partieEnCours`
la plus récente, précisément parce que le client n'envoie pas l'identifiant de
campagne dans le descripteur de `/new` (contrat gelé). La même déduction sert ici.
`lireContexte()` interroge la route quand le localStorage est muet.

**À trancher au plan :** garder le localStorage comme raccourci pour l'hôte, ou
faire passer tout le monde par la route. Une seule voie vaut mieux, mais
`lireContexte()` est synchrone aujourd'hui et devient asynchrone.

### 4.2 Les droits d'écriture par champ

**État :** ✅ **FAIT** (jalon B, `3e830a5` + `819712d` + `3d606fc`). ⚠️ **Écart avec cette fiche** : `/save_campagne` n'a PAS été modifié. Une route étroite `/save_carnet_partiel` a été ajoutée à côté, qui ne sait que fusionner des clés de carnet — elle ne peut ni terminer un scénario, ni gagner une campagne, ni approcher le secret. Interdire par la forme de la route coûte moins cher que de vérifier partout ailleurs.

**Le fait :** `/save_campagne` écrit la campagne ENTIÈRE, sans notion de siège.
Deux joueurs qui valident s'écrasent l'un l'autre, en silence.

**Le travail :**
- Le panneau distingue les champs communs des champs personnels. L'attribut
  `parJoueur` existe déjà dans les définitions, et `verifier_campagnes.py` le
  contrôle (un `deck: "requis"` sans `parJoueur` est refusé).
- Le panneau n'ouvre à la saisie que les champs du siège courant, affiche les
  autres en lecture avec le nom de qui doit les remplir.
- `/save_campagne` **fusionne** au lieu de remplacer, sinon deux POST concurrents
  se perdent. Écriture atomique, comme le reste (`test_ecriture_atomique.py`).
- Le bouton « Valider » n'apparaît que chez le joueur 1, et refuse tant qu'un
  champ personnel obligatoire manque.

### 4.3 Ce que la table voit pendant que l'hôte remplit

**État :** ✅ **FAIT, et la question était plus simple que prévu** : le panneau étant monté sans condition de siège, le **direct** est gratuit. L'hôte recharge la campagne toutes les 3 s et ne reprend QUE les cases des autres (`cleDUnAutreSiege`) — sans ce filtre, une case qu'il vient d'effacer réapparaissait toutes les 3 s.

**À trancher :** le panneau s'ouvre-t-il chez tout le monde à la fin de partie
(chacun voit le carnet se remplir en direct), ou les joueurs distants
attendent-ils la validation ? Le direct demande une diffusion, l'attente demande
un écran d'attente honnête (« l'hôte valide les récompenses »).

### 4.4 Enchaîner le scénario suivant

**État :** ✅ **FAIT** (jalon D, `2ccd41c`). Aucune route nouvelle : les distants relisent `/get_campagne_en_cours` et rechargent quand le scénario change. Deux pièges verrouillés par les tests : entre validation et relancement, `partieEnCours` vaut `null` et la route rend un scénario VIDE (recharger là mènerait à un plateau mort) ; et sans scénario courant connu, tout changement paraîtrait en être un.

Après validation, l'hôte relance une partie. Les autres doivent suivre sans
naviguer à la main. À définir avec 4.3.

### 4.5 Le secret d'A.I.M. en multi

**État :** ⏳ **NON FAIT, et assumé.** La route neuve ne rend ni carnet ni preuve, et le test le vérifie sur la chaîne de réponse (pas seulement sur l'objet). Mais « la combinaison ne se déduit pas d'un carnet partagé vu par plusieurs » reste à éprouver : c'est une campagne de tests à soi seule, et elle avait besoin des jalons A à D pour exister.

`_sans_secret()` protège déjà les routes. À vérifier : que la combinaison ne se
déduise pas du carnet partagé vu par plusieurs joueurs, et que la fermeture de la
fuite du 12/8 (§17 de `docs/rapports/CAMPAGNES.md`, une preuve n'est fabriquée qu'au
moment du droit de la voir) tienne à quatre sièges et pas seulement à un.

### 4.6 Tests

**État :** ✅ **FAIT côté automatisé** (`5e2f990`). 434 cas vitest, 29 vérifications Python, les deux routes sondées en **HTTP réel**, et `ui-check/tests/campagne-multi.spec.ts` : deux contextes de navigateur, une vraie partie à deux héros, le siège 1 qui voit le panneau **sans avoir jamais eu la clé**, les droits par champ, « Valider » réservé à l'hôte, et le carnet relu portant les deux saisies. Vérifié par mutation. Le test a révélé un défaut, corrigé : le panneau listait aux distants des cases à remplir qui ne leur appartenaient pas. ⏳ Reste l'essai humain, le salon n'étant atteint par rien d'automatisé.

Le pilote de campagne sait déjà **servir tous les sièges**
(`ui-check/pilote-campagne.ts`, §13 de `docs/rapports/CAMPAGNES.md`). C'est lui qui rend
ce chantier testable en vraie partie : une campagne à deux sièges, carnet écrit
par les deux, relu par les deux.

### 4.7 Le salon doit dire la vérité (chantier ABSENT de cette fiche)

✅ **FAIT** (jalon C, `a9c24e8`). Découvert en sondant le code : un invité arrivait
sur « Choisis ton héros » alors que l'équipe est figée depuis la création de la
campagne. Son choix aurait été écrasé au lancement et il aurait joué autre chose.
Le salon interroge maintenant `/get_campagne_en_cours` au démarrage et affiche
« Tu tiens <héros> ». Une route indisponible fait retomber sur le salon ordinaire
plutôt que de bloquer l'invité.

## 5. Comment on saura que c'est fait

Une campagne menée à deux en ligne, sur deux navigateurs, du lancement du
scénario 1 à la validation des récompenses : les deux joueurs voient le panneau,
chacun remplit ses champs, l'hôte valide, le carnet relu contient les deux
saisies, et le scénario 2 lit ce que le scénario 1 a écrit.

**Atteint par l'automatisation, pas par un humain.** `campagne-multi.spec.ts` mène
une vraie partie à deux sièges et relit le carnet. Ce qu'il reste :

1. ~~`ui-check/tests/campagne-multi.spec.ts`~~ **FAIT** (`5e2f990`), 2/2 verts, sans
   régression sur les 26 autres cas de campagne.
2. L'essai humain : le salon qui dit « Tu tiens <héros> », puis un scénario mené à
   deux, validé, et le suivant lancé pour voir le second navigateur suivre seul.
3. Une prémisse restée **non mesurée** : ce que voyait un invité au salon quand
   l'hôte lançait une campagne AVANT ce chantier. La réponse n'a plus d'importance
   pratique, mais elle dit si cette fiche décrivait un bug ou une absence.
