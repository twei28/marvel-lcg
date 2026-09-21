# Le salon attend SA partie, plus « une » partie

21/09/2026. Suite et fin de
`.planning/todos/2026-09-20-salon-renvoie-vers-l-ancienne-partie.md`, dont la
première moitié (« Quitter la partie » éteint vraiment la table) ne couvrait que
le cas rare. Le chemin fréquent — jouer, écran de fin, « Retour au menu »,
relancer — est celui qui est fermé ici.

**Statut : fait, prouvé, non déployé.** ⚠ **Une ronde de correction a suivi la
première livraison, et elle a trouvé un trou critique : voir le §7, qui prévaut
sur ce qui le précède quand les deux se contredisent.**

| Commit | Ce qu'il porte |
|---|---|
| `2ba88d97` | La règle pure `bascule.js` et ses 14 cas (`ui-check`) |
| `e61614db` | La route moteur `/get_heros_du_siege` et ses 13 témoins |
| `c7ff6590` | Le salon branché dessus (`public/js/salon/app.js`) |
| `b017ffd2` | Ce rapport, et la fiche de backlog |
| `4436f3de` | Ronde 1 — le repère de fraîcheur, et 25 cas |
| `1cfc1782` | Ronde 1 — `debut`, `set_choix_siege` durci, spectateur |
| `741bdacb` | Ronde 1 — la campagne dans la règle, chaque message avec sa sortie |
| `aaf0acbc` | Ronde 1 — l'identité du siège, la gate de la rotation |

---

## 1. Ce que le salon savait déjà, et c'était la moitié du problème

**Il savait presque tout.** L'invité choisit héros ET deck, et le choix part
déjà sous la forme exacte qu'il fallait :

```js
fetch("/set_choix_siege", { body: JSON.stringify({
    p: siege, hero_card_id: etat.hero.heroCardId, deck_id: deck.id, ... }) });
```

`hero_card_id` est l'identifiant de la carte héros (`01001a`). C'est
précisément la clé qui permet de se reconnaître dans une partie : le moteur, lui,
porte `scene.players[N].hero[0]` sous la forme `'01001a,01001b'` (identité héros,
puis alter-ego), et `catalog.js` fait déjà exactement ce découpage
(`d.hero[0].split(",")[0]`) pour fabriquer `heroCardId`. Les deux bouts se
rejoignent sans rien inventer.

Il savait aussi **relire** son choix au démarrage (`reprendreChoixExistant`, via
`/get_choix_sieges`), ce qui couvrait déjà le rechargement pendant l'attente.

### ⚠ Ce qu'il ne savait PAS, et le seul endroit où la conception a dû trancher

`/new` **vide** `choix_sieges` côté serveur, délibérément :

```python
# Le salon multijoueur a rempli son office : on le vide pour que la
# partie suivante ne reparte pas avec les choix de la precedente.
self.choix_sieges = {}
```

Un invité qui recharge sa page **après** le lancement ne peut donc plus rien
apprendre du serveur : ni son héros, ni son deck. Sans mémoire, il ne saurait pas
se reconnaître et resterait sur le salon pendant que sa partie tourne — on aurait
échangé un symptôme contre un autre, exactement le reproche fait au compteur de
génération.

**J'ai écarté l'archivage côté serveur**, qui avait l'air plus propre (garder les
choix « déjà joués » dans un `choix_sieges_joues`). Il rouvre le défaut : cette
archive colle à l'ancienne partie encore chargée, donc un invité tout neuf
basculerait dedans sans avoir rien choisi. **C'est précisément parce que le choix
vit dans le navigateur de l'invité qu'il distingue « moi » de « celui qui était
assis là avant moi ».** Le choix est donc retenu en `localStorage`, par siège,
horodaté, périmé au bout de six heures et effacé dès qu'il a servi.

---

## 2. Ce que le moteur publie, et pourquoi pas plus

```
GET /get_heros_du_siege?p=2   ->   {"en_jeu": true, "p": 2, "heros": "01019a"}
```

Trois champs, et c'est tout :

- **`heros`** : l'identifiant de la carte héros que tient **le siège demandé**,
  découpé sur la virgule pour coller au `heroCardId` du salon.
- **`en_jeu`** : y a-t-il un monde chargé ? Même garde que `get_play_scene_name`.
- **`p`** : le siège, pour que le client vérifie que la réponse le concerne.

**Ce que la route ne dit pas, et ne doit pas dire** : le deck, la main, le nom du
joueur, l'identité alternative, et **les autres sièges**. La docstring de
`get_campagne_en_cours` est le modèle explicite : « On ne rend que de quoi se
situer […] ; le secret n'a rien à faire ici. » Le salon n'a besoin que de se
reconnaître lui-même ; publier la composition d'une partie en cours à quiconque
demande serait une route de confort, et ce dépôt a déjà refermé deux fuites
d'information entre joueurs (15/09, puis cette semaine).

À noter : `en_jeu` vrai **avec `heros` vide** n'est pas un raté, c'est le
troisième état — « une partie tourne, mais ce siège n'y est pas ». C'est lui qui
permet de ne pas laisser un invité oublié attendre sans rien comprendre.

### ⚠ La garde s'est trompée une fois, et le test l'a rattrapée

La première version gardait la route avec `allowed_seats`, par symétrie avec
`set_choix_siege`. Le témoin d'authentification l'a prise en faute :

```
ECHEC invite : le siege d'un AUTRE lui est refuse   [code=200]
```

`allowed_seats` ouvre tout siège **qu'aucun client ne tient** (« reprise d'un
siège abandonné ») — et **avant le début d'une partie, ils le sont tous**. C'est
le piège que `get_liens_sieges` documente dix lignes plus bas, et que j'avais lu
avant de tomber dedans. La route utilise maintenant `tient_le_siege`, la garde
stricte, comme la distribution des clés. Une table sans protection de siège
(partie locale) répond, comme tout le reste du moteur.

---

## 3. La règle, et les six cas

La décision est une fonction pure, `decisionSalon` dans
`Fusion/marvel-lcg-src/public/js/salon/bascule.js`. Elle rend `attendre`,
`basculer` ou `expliquer`.

| # | Cas | Ce qu'il prouve | Verdict |
|---|---|---|---|
| 1 | Ancienne partie encore chargée, l'invité n'a rien choisi | **Le défaut du 20/09.** Sans choix, on n'est dans aucune partie : on reste sur la grille des héros | `attendre` |
| 1b | Ancienne partie chargée, choix fait, autre héros au siège | Le choix seul ne suffit pas : il faut qu'il CORRESPONDE | `attendre` |
| 2 | L'hôte lance, mon siège tient mon héros | La bascule, et sa seule condition | `basculer` |
| 3 | Rechargement pendant l'attente | Le choix est retrouvé (serveur, ou mémoire locale) : l'attente continue correctement | `attendre` + choix relu |
| 4 | Rechargement après le lancement | La mémoire locale survit là où le serveur a vidé : l'invité n'est pas coincé | `basculer` |
| 5 | Deux parties d'affilée, même scénario | `get_play_scene_name` rendrait le même texte dans les deux ; le héros du siège, lui, tranche | `attendre` puis `basculer` |
| 6 | L'hôte lance sans ce siège (3 liens, 2 joueurs) | **Le cas hors liste.** Passé 45 s, le salon explique au lieu de laisser un écran muet | `attendre` puis `expliquer` |

Quatre cas de plus gardent les bords : rien ne tourne ; on n'explique **jamais**
avant que l'invité ait choisi ; un choix trop vieux ne vaut plus rien ; un
stockage en panne fait perdre la mémoire, pas la page. Plus deux sur la
séparation des sièges et l'effacement après usage.

### Pourquoi le cas 6 « explique » au lieu d'affirmer

« Mon siège ne tient pas mon héros » est **exactement** ce que dit aussi une
ancienne partie encore chargée — c'est-à-dire l'état ordinaire pendant toute
l'attente. Le salon n'a aucun moyen de départager les deux sans un second signal
(l'âge de la partie en cours), que j'ai refusé de publier pour une nuance de
formulation. Il dit donc la vérité telle qu'il la connaît :

> Une partie est en cours sur cette table, mais ton siège n'y tient pas ton
> héros. Soit l'hôte n'a pas encore lancé la tienne, soit il a lancé sans toi :
> préviens-le.

Le message s'efface tout seul si le désaccord se dissipe, et le délai de 45 s
évite de crier à chaque soirée pendant que l'hôte finit de préparer.

---

## 4. Le moule de test, et pourquoi celui-là

**`ui-check/tests/bascule-salon.spec.ts`, sur le modèle de
`sondage-salon.spec.ts`** : des fonctions pures exportées par le vrai module,
appelées dans la page via `page.evaluate` + `import`, sans moteur derrière (un
serveur statique sur `public/` suffit, `UI_CHECK_BASE` + `WSLENV`).

C'est le bon moule parce que `public/js/salon/` est du JavaScript nu servi par le
moteur, pas du TypeScript de `ui-app` : il n'a pas de banc de test propre, et
`sondage-salon.spec.ts` a déjà tranché comment on éprouve une règle de ce dossier.
Le moule des captures (`references/`) ne dirait rien ici : il n'y a aucun pixel en
jeu. Et un test bout-en-bout du salon exigerait un moteur avec sièges protégés,
deux navigateurs et une vraie partie — pour mesurer une décision qui tient en
cinq lignes.

Ce que ce moule NE prouve pas est dit plus bas, dans mes inquiétudes.

### La séquence rouge → vert

Le module a d'abord été écrit avec la règle **d'origine**, extraite telle quelle
(`return enJeu ? "basculer" : "attendre"`), et la batterie lancée dessus :

```
11 failed   ...  3 passed (13.6s)
[pc] › ancienne partie chargee, rien de choisi : on ne bascule pas
[pc] › deux parties du meme scenario : le heros tranche, pas le scenario
[pc] › lance sans ce siege : passe le delai, on explique
...
```

Le premier échec **est** le défaut du 20/09, reproduit. Puis la vraie règle :
`14 passed (5.4s)`.

---

## 5. Les verdicts

| Batterie | Résultat |
|---|---|
| `ui-check/tests/bascule-salon.spec.ts` (`npm run bascule-salon`) | **14 / 14** |
| `tools/test_heros_du_siege.py` (nouveau) | **11 / 11 — TOUT PASSE** |
| `tools/test_authentification.py` (table protégée) | **15 / 15 — TOUT PASSE** (13 avant, 2 ajoutés) |
| `tools/test_authentification.py ouvert` (table locale) | **3 / 3 — TOUT PASSE** |
| `tools/test_mode_manuel.py` **EN ENTIER** | **48 / 48 VERT** |
| `python -m compileall -q src` | aucune erreur |

La batterie moteur a tourné sur `.game-src-par10`, dossier jetable créé pour
l'occasion et **supprimé ensuite** — jamais `.game` ni `.game-src`. Ports
45200-45247 et 46200-46800, tous sous 49152. Contrôle après coup :
`launch.json` de la racine porte bien `['127.0.0.1:2345']`.

---

## 6. Mes inquiétudes

1. **⚠ La campagne garde l'ancien signal, et le défaut avec.** En campagne
   l'invité ne choisit rien — l'équipe est fixée par le livret — donc il n'a
   aucun choix à reconnaître et la règle ne s'applique pas telle quelle.
   `surveillerLeLancementCampagne` bascule toujours dès qu'une partie tourne.
   **Un invité de campagne qui arrive sur une table portant encore la manche
   précédente sera encore expédié dedans.** C'est déclaré dans le code et
   réinscrit dans la fiche. La piste existe (le salon peut traduire
   `membre.heros` en `heroCardId` par le catalogue, sans rien publier de plus),
   mais je ne pouvais pas l'éprouver ici et je n'ai pas voulu risquer de bloquer
   un invité de campagne pour un chemin que je ne mesure pas.

2. **⚠ Le témoin de la bascule est une règle pure, pas un écran.** La leçon du
   15/09 vaut ici aussi : moteur vert ne prouve rien sur le rendu. Rien dans ce
   chantier n'a été vu à l'écran — ni le message d'explication, ni le
   rechargement, ni la bascule. Ce qui est prouvé : la décision, la route, et la
   garde. Ce qui ne l'est pas : que le salon affiche bien ce message, et qu'il
   passe bien `monChoix` là où il faut. **Une partie à deux sur une vraie table
   reste le seul juge de ce dernier pouce.**

3. **⚠ La rotation « premier joueur » décale les sièges, et ce n'est pas mon
   fait.** `launcher.js` fait tourner les joueurs pour placer le premier joueur
   en tête (`ordre = retenus.slice(pj).concat(...)`). Si l'hôte choisit un
   premier joueur autre que le siège 0, le siège N du salon ne correspond plus au
   joueur N du moteur — et cela vaut déjà pour `board.html?p=N`, indépendamment
   de ce chantier. Mon correctif ne l'aggrave pas et ne le corrige pas : dans ce
   cas, l'invité ne reconnaîtra pas son héros et **lira le message du cas 6** au
   lieu de basculer. C'est bruyant mais honnête, là où l'ancien code l'envoyait
   silencieusement sur le mauvais siège. À traiter à part.

4. **Le corollaire des trois messages reste entier.** Le plateau affiche toujours
   « Connexion à la partie… » pour trois situations différentes
   (`ui-app/src/board.tsx`). Hors périmètre, et toujours ouvert dans la fiche.

5. **Rien n'est déployé.** `public/js/salon/` est servi tel quel par le moteur
   (pas de bundle à reconstruire pour ces fichiers), mais la mise en production
   n'a pas été lancée, comme demandé.

6. **La mémoire de six heures est un jugement, pas une mesure.** Assez long pour
   couvrir n'importe quelle attente de salon, assez court pour ne pas traverser
   deux soirées. Si un choix oublié devait quand même mordre, il faudrait le
   même siège ET le même héros ET la partie de la veille encore chargée — très
   loin du défaut d'origine, mais pas zéro.

---

# 7. Ronde de correction 1 — le héros seul ne suffisait pas

⚠ **Cette section prévaut sur les §1 à §5 partout où elles se contredisent.**
La première livraison avait un trou critique, et le raisonnement du §1 était
faux sur son point central.

## 7.1 CRITIQUE — le septième cas : rejouer une manche avec LE MÊME héros

Le chemin même que ce correctif visait était intégralement rouvert.

Déroulé : on joue la manche 1, écran de fin, « Retour au menu » (qui ne ferme
rien), l'hôte relance. Entre les deux, le moteur porte encore le monde de la
manche 1, **avec le héros de l'invité à son siège**. `/new` ayant vidé
`choix_sieges`, l'invité re-choisit dans le salon — et il reprend **le même
héros**, ce que fait la majorité des joueurs. `monChoix` est posé, le sondage
tombe dans les deux secondes, la règle voit `heros === monChoix` sur l'ANCIEN
monde et renvoie `basculer`. Le 20/09 à l'identique.

**Aucune mémoire locale n'est en cause** : le choix est refait en direct.

### Ce que cela corrige dans mon raisonnement du §1

J'y écrivais que la mémoire locale « distingue *moi* de *celui qui était assis
là avant moi* ». **C'est faux.** Elle distingue un héros d'un autre héros. Dès
que le héros coïncide d'une manche à l'autre, elle est aveugle. L'arbitrage
(écarter l'archivage serveur) reste bon — cet archivage aurait eu exactement le
même angle mort — mais la raison donnée ne tenait pas.

Mon test le plus proche ne pouvait pas l'attraper : « deux parties du même
scénario » choisissait la seule variante où le héros **change** entre les
manches. Le trou était dans le choix du cas, pas dans la mécanique de test.

### Le remède : deux signaux, dont aucun ne tient seul

- **Le héros** dit « ce siège est à moi » — aveugle quand il ne change pas.
- **La fraîcheur** dit « cette partie a commencé après que je me suis posé » —
  aveugle au rechargement si on la relève à l'arrivée, ce qui avait fait écarter
  le compteur de génération.

Ensemble ils tiennent, parce que **le repère est relevé AU MOMENT DU CHOIX et
retenu AVEC lui** : il voyage donc dans la mémoire du navigateur et survit au
rechargement.

La règle devient : `heros === monChoix` **ET** `debut !== debutAuChoix`.

### Le repère n'a rien coûté au moteur

`GameSession` tient déjà `game_uid` et `game_id`, et `ui-app/src/board/moteur.ts`
les combine déjà en `clePartie()` pour répondre à **la même question** (« mon
journal appartient-il encore à la partie affichée ? »). La route rend donc
`debut = "<game_uid>:<game_id>"` : aucune convention nouvelle, aucun compteur
ajouté dans `Game.NewGame`.

**Bénéfice collatéral** : le cas 6 cesse d'être une devinette à 45 s. Si le
repère a changé et que mon siège n'a pas mon héros, on peut l'**affirmer** tout
de suite — lancé sans moi, ou héros changé.

## 7.2 CRITIQUE — la campagne, et pourquoi ma piste était fausse

J'avais laissé la campagne sur l'ancien signal en proposant, pour plus tard, de
traduire `membre.heros` en `heroCardId` par le catalogue. **Cette piste ne peut
pas aboutir, pour deux raisons indépendantes** :

1. **En campagne, l'équipe est fixe d'une manche à l'autre** — c'est la
   définition du mode. Le siège N tient donc toujours le même héros. Comparer
   les héros ne laisserait pas le défaut ouvert : il le **garantirait**, avec
   bascule immédiate sur la manche précédente à chaque chargement du salon.
2. `server_campagne.py` ne publie jamais `identite`. Sur une équipe portant une
   variante, la traduction rendrait la carte de base et ne correspondrait
   jamais.

**En campagne, le héros ne peut pas servir de signal. Seule la fraîcheur le
peut, et elle y suffit seule** : l'invité n'a rien choisi, la seule question est
« une partie a-t-elle démarré depuis que je suis arrivé ? ». Un seul mécanisme
ferme donc les deux chemins. `surveillerLeLancementCampagne` a été supprimée :
la campagne passe par la même boucle, avec `sansChoix: true`, et relève son
repère à la première réponse de la table (qu'elle mémorise, pour survivre au
rechargement comme un invité ordinaire).

## 7.3 IMPORTANT — `/set_choix_siege` était resté sur `allowed_seats`

Même piège que celui que mon témoin avait rattrapé **en lecture**, laissé en
place **en écriture** : un invité du siège 1 pouvait poser le choix du siège 2.
Et mon correctif l'aggravait — avant, la victime partait avec le deck du voisin ;
après, son `monChoix` ne correspondait plus jamais à ce que le moteur avait reçu
et elle restait bloquée dans le salon.

Passée sur `tient_le_siege`. **Rouge constaté avant correction** :

```
ECHEC invite : le choix d'un AUTRE siege lui est refuse   [code=200]
```

## 7.4 IMPORTANT — l'état `expliquer` était un cul-de-sac

Il remplaçait le statut, masquait le bandeau et disait « préviens-le », sans
aucune sortie. L'ancien code envoyait l'invité au mauvais endroit ; le mien ne
l'envoyait nulle part. Désormais **chaque avertissement porte sa sortie quand il
y en a une** :

| Situation | Ce que l'invité lit | Ce qu'il peut faire |
|---|---|---|
| Lancée, mon siège joue un AUTRE héros | « ton siège n'y joue pas le héros que tu avais choisi. Il joue *X*. » | bouton **Rejoindre avec *X*** |
| Lancée sans ce siège | « L'hôte a lancé la partie sans ce siège. Préviens-le. » | rien à rejoindre ; la grille reste ouverte |
| Aucun repère, partie indatable | « Impossible de savoir d'ici si c'est la tienne » | bouton **Rejoindre cette partie** |

Et `statutAvantExplication` a disparu : le statut ordinaire est **recalculé**
(`statutNormal()`) au lieu d'être mis de côté, sans quoi un texte périmé revenait
quand l'invité changeait d'avis entre-temps.

## 7.5 Les témoins ajoutés

- **Spectateur** sur `/get_heros_du_siege` : `SpectateurPeutLire` ouvre par
  préfixe `/get_`, donc **seul `tient_le_siege` l'arrête** — c'est la classe
  exacte de la fuite du 15/09, et elle est maintenant mesurée (deux cas).
- **Écriture d'un siège voisin** sur `/set_choix_siege` (le rouge ci-dessus).
- **`debut` change d'une manche à l'autre alors que le héros ne change pas** :
  le cas 7 prouvé côté MOTEUR, en rejouant la même équipe dans une seconde
  scène.
- **`debut` vaut `""` quand aucune partie ne tourne**, et **`p=-1` → 400**.

⚠ À savoir, et c'est une limite du dispositif : `test_heros_du_siege.py` tourne
avec `seat_passwords: []`, donc **il ne mesure jamais la garde**. Toute la
protection de siège repose sur les quatre assertions de
`test_authentification.py`.

## 7.6 Les mineurs traités

- **`appliquerChoixSalon` remet `joueur.identity` à `null`.** `launcher.js`
  préfère l'identité alternative au héros du deck ; laissée en place, celle d'un
  héros précédent partait au moteur sans que personne ne l'ait choisie — et,
  avec la nouvelle règle, l'invité ne s'y reconnaissait plus et restait dehors.
- **`buildDescriptor` a sa propre garde** sur la rotation « premier joueur » :
  en multi par sièges, aucune rotation. L'écran grisait déjà le sélecteur, mais
  c'est une politesse d'interface ; la garde vit maintenant là où le descripteur
  se fabrique. Le solo est strictement inchangé (`state.salon.multi` faux).
- **`p < 0` reçoit le même 400 que `p=abc`.**

## 7.7 Verdicts après la ronde

| Batterie | Résultat |
|---|---|
| `ui-check` `bascule-salon` | **25 / 25** (dont le cas 7, constaté **rouge** d'abord) |
| `tools/test_heros_du_siege.py` | **16 / 16 — TOUT PASSE** |
| `tools/test_authentification.py` (protégée) | **19 / 19 — TOUT PASSE** |
| `tools/test_authentification.py ouvert` | **3 / 3 — TOUT PASSE** |
| `tools/test_mode_manuel.py` **EN ENTIER** | **48 / 48 VERT** |
| `compileall -q src` | aucune erreur |

Dossier jetable `.game-src-par11`, supprimé ensuite. Ports 45300-45347 et
46900-47100, tous sous 49152.

## 7.8 Ce qui reste, après la ronde

1. **⚠ Toujours rien vu à l'écran, et c'est la zone qui contenait les deux
   défauts d'assemblage ci-dessus.** Le jugement « sérieux » porté sur cette
   inquiétude est confirmé par les faits : `set_choix_siege` et l'impasse de
   l'avertissement sont exactement le genre de choses qu'une partie à deux aurait
   montrées en trente secondes. Les règles, la route et les gardes sont prouvées ;
   **l'assemblage ne l'est pas.**
2. **Le repère change aussi quand l'hôte ANNULE un geste** (`LoadScene` passe par
   `SetScene`, qui réattribue `game_uid` et incrémente `game_id`). Si l'hôte
   annule un geste dans la manche précédente pendant qu'un invité attend au
   salon **et** que son siège y tient son héros, l'invité basculerait à tort.
   Cas très étroit — l'hôte devrait être dans l'assistant, pas dans l'ancienne
   partie — mais réel, et non mesuré.
3. **Le corollaire des trois messages** (« Connexion à la partie… ») : entier.
4. **Rien n'est déployé.**
