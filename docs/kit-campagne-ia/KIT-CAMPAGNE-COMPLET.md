# Kit de création de campagne : Marvel Champions LCG (moteur `marvel-lcg`, projet « Narwhal Champions »)

> **Version du 20/10/2026.** Ce manuel est construit par `outils/construire-kit-campagne.py` à partir du dépôt
> réel : chaque fichier cité en bloc de code est la **copie exacte** du fichier du projet au moment de la
> construction. Si un exemple de ce manuel et le dépôt divergent un jour, c'est le dépôt qui a raison.

## 1. Mode d'emploi et règles absolues

### 1.1 Pour qui, pour quoi

Tu es une IA chargée de **produire les fichiers d'une campagne** pour ce jeu : les cartes, les scénarios, les
sets de rencontre, la description de la campagne, la logique de carnet, les scripts des cartes, les textes
français, la liste des images, et les preuves (cas de test) qui vont avec.

Ce que tu produis **n'est jamais intégré tel quel**. Il est donné à **Claude**, l'assistant qui a accès au dépôt
du jeu : Claude le compare, le teste en jeu, le corrige et l'intègre. Tu n'as, toi, accès à rien d'autre que ce
manuel, ses annexes et les fichiers modèles du zip. Tout ce que tu dois savoir est donc ici.

Ce manuel couvre **toute la chaîne** d'une campagne, dans cet ordre :

1. **Les cartes** (`data/cards.json`) : vilains, complots principaux et annexes, sbires, traîtrises,
   attachements, environnements, cartes de campagne, récompenses, et au besoin héros et cartes joueur.
2. **Les scénarios et les sets de rencontre** (`data/scenarios`, `data/encounter_sets`, `data/sets_info.json`).
3. **Les scripts** des cartes (`src/cards/pack/<pack>/...`), c'est-à-dire leurs capacités en Python.
4. **La logique de campagne côté moteur** (`src/cards/pack/<pack>/campaign.py`) : ce que le carnet change à la
   mise en place du scénario suivant, et ce que le jeu relève à la fin d'un scénario.
5. **La description de la campagne** (`data/campagnes/<code>.json`) : ce que l'écran des campagnes montre et ce
   que le panneau de récompenses fait reporter au carnet.
6. **Les textes français, les images, les pages du livret, les crédits, les preuves de test.**

### 1.2 Les règles absolues

Elles viennent de règles posées par l'utilisateur du projet et d'erreurs déjà payées. Les enfreindre fait
échouer l'intégration, ou pire : produit une campagne qui *a l'air* de marcher et ne marche pas.

1. **Fidélité à 100 % au texte imprimé.** Une carte fait exactement ce qu'elle dit, rien de moins, rien de plus.
   Pas d'approximation « recommandée ». Si le moteur ne sait pas faire ce que la carte dit, tu l'écris dans
   `A_FAIRE_CLAUDE` (règle 3) : le moteur s'étend, la carte ne s'édulcore pas.
2. **N'invente jamais une fonction, une clé, une chaîne de ciblage.** Tu n'utilises que ce qui figure dans ce
   manuel, dans ses annexes, dans l'index de l'API du moteur (`annexes/I-index-api-moteur.md`) ou dans les
   fichiers modèles. Une fonction inventée ne lève **presque jamais d'erreur** : la carte se construit, entre en
   jeu, et ne fait rien. C'est le défaut le plus fréquent et le plus silencieux de ce projet.
3. **Ce que tu ne sais pas faire s'écrit, il ne se devine pas.** Écris dans le script :

   ```python
   # A_FAIRE_CLAUDE: <ce qui manque, le texte imprimé visé, la carte de référence la plus proche>
   ```

   et continue le reste. Une carte à moitié écrite avec un `A_FAIRE_CLAUDE` honnête vaut mieux qu'une carte
   « complète » qui appelle une fonction inventée. **Un script qui renvoie une liste vide ne signifie pas que la
   carte n'a aucun effet** : si la carte a un texte de capacité, un `GetAbilities()` vide sans
   `A_FAIRE_CLAUDE` est une faute.
4. **Une question à la fois, en choix multiple.** Quand un texte, une icône ou une règle laisse place à plus
   d'une lecture, tu poses **une seule** question à l'utilisateur (pas un lot de dix), avec : l'option que tu
   recommandes en premier, « Autre (précise) » en dernier, et pour chaque option **ce que ça change en jeu**.
   Tu cites le fichier image de la carte concernée. Tu attends la réponse avant la question suivante. Tu ne
   tranches pas en silence. Détail et cas qui déclenchent une question : §1.3.
5. **Ne touche jamais au moteur.** Tu n'écris que des cartes, des scénarios, des campagnes, leurs scripts, leurs
   textes et leurs preuves. Si une mécanique demande une modification du moteur (un compteur nouveau, un trait
   nouveau, un message nouveau, un type de champ de carnet nouveau, un écran nouveau), tu l'écris dans
   `BESOINS-MOTEUR.md` (§12.4) : ce que c'est, pourquoi, quelle carte l'exige.
6. **N'écrase jamais un fichier partagé.** `data/cards.json`, `data/sets_info.json`,
   `ui-app/src/board/textes-fr-fanmade.ts` et `tools/prefixes_fanmade.json` contiennent le travail de tout le
   monde. Tu livres des **fragments** à fusionner (§12), jamais le fichier entier.
7. **Les valeurs de `desc` sont toujours des chaînes** (`"HP": "10"`, jamais `10`).
8. **Une icône de ressource ne se nomme jamais « à vue ».** Elle se compare à une carte du même pack dont la
   ressource est connue (§4.6). Une lecture au jugé a déjà inventé une « ressource os » (sur Lockjaw) : quatre
   cartes n'ont pas rendu ce qu'elles promettent jusqu'au 9/8/2026.
9. **Les textes de cartes sont en anglais** (c'est la langue des données du moteur). Le texte français se livre à
   part, dans un fragment dédié, avec le vocabulaire officiel (§10.3).
10. **Ne laisse aucune trace de travail dans les livrables** : pas de `print` de debug, pas de fichier
    temporaire, pas de commentaire qui raconte ton raisonnement. Les commentaires expliquent *pourquoi* une
    carte est écrite ainsi, en français, comme dans les modèles.

### 1.3 Ce qui déclenche une question à l'utilisateur

| Situation | Exemple vécu |
|---|---|
| Mot-clé maison non défini sur les cartes fournies | « drain X » qu'aucune carte n'explique |
| Texte imprimé contradictoire | « Forced **Interrupt** : **After** X schemes or attacks » : le type et le déclencheur se contredisent |
| Valeur imprimée que le format ne sait pas exprimer | une ATK « ★ » |
| Portée ambiguë d'une phrase | « Discard this obligation » : la dernière option seulement, ou les deux ? |
| Mot-clé officiel inapplicable tel quel | `TeamUp` qui suppose deux héros en jeu |
| Contenu absent du matériel fourni | aucune liste de deck fournie pour un héros |
| Effet que le moteur ne peut pas rendre fidèlement | « if this attack has ranged or piercing » sur un événement |
| Icône imprimée qu'on ne reconnaît pas | l'icône « nœuds reliés » de Lockjaw, prise pour un os pendant cinq jours |
| Règle du livret qui ne dit pas quoi faire d'un cas limite | une défaite au scénario 3 : se rejoue-t-il, ou la campagne continue-t-elle ? |

Ne posent **pas** de question : les choix purement techniques (quelle fabrique, où ranger une aide, format
d'image). Ceux-là, tu les fais, et tu les expliques dans tes doutes si tu hésites.

Les points **non tranchables** (une capacité que tu ne sais pas coder, un comportement du moteur que tu ne peux
pas vérifier) ne sont pas des questions : ils vont dans `A_FAIRE_CLAUDE` et dans `QUESTIONS.md`.

### 1.4 Ce que tu livres (résumé ; le détail est au §12)

Un dossier `livraison/` qui **reproduit l'arborescence du projet**, plus quatre fichiers de suivi :

```
livraison/
  MANIFESTE.md           la liste de TOUS les fichiers livrés, une ligne chacun : chemin, rôle, nombre de cartes
  QUESTIONS.md           les questions ouvertes (une par carte ou par règle), format du §1.3
  BESOINS-MOTEUR.md      ce que le moteur ou l'interface devra apprendre (trait, compteur, message, écran...)
  AUTO-VERIFICATION.md   ce que tu as vérifié toi-même, avec la sortie de `verifier-livraison-campagne.py`
  integration/           l'arborescence à fusionner (data/..., src/..., tools/..., textes-fr/..., images.md)
```

Avant de livrer, tu lances **`verifier-livraison-campagne.py`** (fourni dans le zip, à la racine, Python 3 sans
dépendance) sur ton dossier. Il attrape les erreurs de forme que Claude attraperait de toute façon, mais que tu
peux corriger toi-même sans attendre : clés manquantes, identifiants en double, scénario qui référence une
carte absente, script rangé dans le mauvais dossier, clé de carnet qui n'existe nulle part, vocabulaire
français interdit. **Il ne remplace pas le jeu** : un script qui passe ce contrôle peut encore ne rien faire en
partie. C'est pourquoi les règles 2 et 3 comptent plus que tout le reste.

### 1.5 Comment lire ce manuel

| Si tu dois... | Lis |
|---|---|
| comprendre ce qu'est une campagne ici et comment tout s'enchaîne | §2 |
| savoir quels fichiers produire | §3 (la liste maîtresse) |
| écrire ou vérifier une carte | §4 puis l'annexe A (kit de cartes, catalogue d'exemples réels) |
| écrire un scénario et ses sets | §5 |
| écrire le script d'une carte | §6, annexes A, B (recettes) et C (mots-clés) |
| écrire la logique de carnet | §7 |
| écrire `data/campagnes/<code>.json` | §8 |
| comprendre ce que fait l'écran | §9 |
| les images, textes français, pages du livret, crédits | §10 |
| prouver que ça marche | §11 |
| préparer la livraison | §12 |
| voir deux campagnes complètes, fichier par fichier | §13 et le dossier `modeles/` du zip |
| éviter les pièges déjà payés | §14 |


---

## 2. Ce qu'est une campagne dans ce jeu, de bout en bout

### 2.1 En deux phrases

Une campagne enchaîne les scénarios d'une boîte dans l'ordre du livret. Ce que les joueurs gagnent ou perdent
dans un scénario est enregistré dans un **carnet de campagne**, qui est relu automatiquement à la mise en place
du scénario suivant.

Le carnet est un **dictionnaire clé texte → valeur texte** (`{"Campaign Pool: Cosmo": "1", "Player 1 Role":
"Brawler"}`). C'est le **seul** lien entre deux parties : le moteur n'a aucune mémoire d'une partie à l'autre.

### 2.2 Les trois couches, et qui écrit quoi

| Couche | Où elle vit | Ce qu'elle fait | Qui la produit |
|---|---|---|---|
| **Données** | `data/cards.json`, `data/scenarios/`, `data/encounter_sets/`, `data/sets_info.json` | Les cartes, la composition de chaque scénario | **Toi** |
| **Moteur (Python)** | `src/cards/pack/<pack>/` (scripts de cartes + `campaign.py`) | Les capacités des cartes ; à la mise en place, applique le carnet ; à la fin de partie, relève le carnet sortant | **Toi** (sauf si le moteur lui-même doit changer : alors `BESOINS-MOTEUR.md`) |
| **Description de campagne (JSON)** | `data/campagnes/<code>.json` | L'ordre des scénarios, les champs du carnet à reporter, les textes de l'écran, les pages du livret | **Toi** |
| **Écran des campagnes (JS)** | `public/campagne.html`, `public/js/campagne/*.js` | Création, liste, scénario courant, lancement | **Claude** (générique : il lit ta description) |
| **Panneau de récompenses (React)** | `ui-app/src/board/campagne/*` | S'ouvre à la fin de partie, pré-remplit le carnet, le fait valider | **Claude** (générique) |
| **Serveur** | `src/engine/device/web/server/server_campagne.py` | Les routes qui lisent les descriptions et écrivent les campagnes du joueur | **Claude** (générique) |

Le point à retenir : **ajouter une campagne qui n'a que des mécaniques déjà connues est un travail de contenu,
pas de code d'interface.** Les écrans lisent ta description et s'adaptent. Seules les mécaniques inédites
(un écran de plus, un type de champ de carnet nouveau) demandent à Claude d'étendre l'interface : tu les
signales dans `BESOINS-MOTEUR.md`.

### 2.3 Le cycle de vie d'une campagne, étape par étape

```
 (1) /campagne.html
     le joueur choisit une BOÎTE (liste lue sur /list_campagnes_definies = data/campagnes/*.json),
     un nom, la difficulté (standard | expert) et le nombre de héros (1 à 4)
          │
 (2)      ▼  /prepare.html?campagne   (l'écran de préparation, réduit à deux étapes : Équipe, Decks)
     le joueur choisit ses héros et leurs decks ; leur identité est FIGÉE pour toute la campagne
          │
 (3)      ▼  POST /save_campagne
     la campagne du joueur est écrite : Fusion/marvel-lcg-src/campagnes/<id>.json
     { code, nom, difficulte, equipe[], termines: [], carnet: {}, tentatives: {}, partieEnCours: null, creee }
          │
 (4)      ▼  « Lancer le scénario »    (public/js/campagne/app.js : lancerScenario)
     - écrit partieEnCours = { scenario, depuis } et tentatives[scenario] += 1
     - dépose la clé navigateur « mc-campagne-partie » = { id, scenario }
     - lance la partie avec le descripteur :
         rules             = ["mode_campaign", "v16_all", "v18_all", ...]
         campaign_json     = le fichier data/scenarios/<id>.json (ou <id>_expert.json en campagne experte)
         encounter_set_names = sets du scénario + sets modulaires DU FICHIER DE SCÉNARIO (jamais un choix du joueur)
         hero_json         = les decks de l'équipe, dans l'ordre des sièges
         campaign_log      = le CARNET de la campagne        ◄── c'est ici que le carnet entre dans le moteur
          │
 (5)      ▼  le moteur monte la partie (World.GameSetup, 16 étapes, voir §7.2)
     étape 13 « Campaign Setup » : Message.WhenCampaignSetup est émis. Les capacités de type Campaign,
     posées sur la face 1A du complot principal par CampaignSetup(niveau), relisent le carnet et en
     appliquent les conséquences (carte mise en jeu, mélangée, retirée, dégâts, etc.).
          │
 (6)      ▼  les joueurs jouent le scénario
          │
 (7)      ▼  fin de partie : Message.WhenGameOver
     la capacité WriteCampaignLogAtGameOver (posée par CampaignSetup) calcule ce que la partie a produit
     et l'écrit dans  .game/campaign_log_last.json  { players_won, scenario, suggestions: {...} }
          │
 (8)      ▼  le plateau ouvre le PANNEAU DE RÉCOMPENSES (ui-app/src/board/campagne/PanneauRecompenses.tsx)
     il pré-remplit chaque champ déclaré dans data/campagnes/<code>.json, dans cet ordre de priorité :
        1. ce que le moteur a relevé (/get_carnet_suggere)  — seulement si son estampille = ce scénario
        2. ce que les « détecteurs » déduisent de l'état du monde (detecteurs.ts)
        3. la valeur déjà présente au carnet
     le joueur corrige, choisit les vrais choix du livret, et valide
          │
 (9)      ▼  POST /save_campagne
     carnet = ancien carnet + champs validés ; termines += [scénario] ; historique[scénario] = champs ;
     partieEnCours = null  ;  perdue = true si la règle de défaite le dit
          │
(10)      ▼  retour à /campagne.html : le scénario suivant est proposé. Retour à l'étape (4).
```

Règles importantes de ce cycle :

* **Une défaite n'écrit rien** : le scénario se rejoue sans pénalité. Exceptions déclarées *dans la description
  de campagne* : en **ordre libre** (Fear No Evil), l'écran enregistre lui-même la défaite au carnet (marque, affaire échouée, perte de campagne) ; `defaite_continue` (la défaite a ses propres gains, la campagne passe au suivant), `defaite`
  (perdre le scénario final perd la campagne), `reprise` (il faut re-préparer quelque chose avant de rejouer).
* **Les sets modulaires viennent du fichier de scénario**, jamais d'un choix du joueur.
* **Entre deux scénarios, le joueur peut modifier le contenu de ses decks** (pas l'identité). Ce que le carnet
  *impose* dans un deck (une carte de récompense) doit y rester : `"deck": "requis"` dans la description.
* **Plusieurs joueurs** : chaque champ `parJoueur` appartient au siège qu'il nomme ; tout le reste appartient à
  l'hôte, seul à pouvoir valider. Les clés par joueur s'écrivent `Player N <clé>` (N de 1 à 4).
* **Mode expert** : un seul choix à la création, valable pour tous les scénarios. En expert, le moteur lit
  `data/scenarios/<id>_expert.json` ; les PV restants se reportent (`victoire_commune_expert`) ; la règle de
  défaite finale s'applique selon `expert_seulement`.

### 2.4 Les fichiers qui décrivent une campagne et leurs liens (carte des références)

```
data/sets_info.json
  "N. Custom (Nom)": { name: <pack>, scenarios: [<id scénario>...], heroes: [...], encounters: [<id set>...], max_id }
        │                                   │                                     │
        │ cle_extension (même texte)        ▼                                     ▼
        ▼                         data/scenarios/<id>.json            data/encounter_sets/<id set>.json
data/campagnes/<code>.json            villain / schemes / set_aside /        encounters: [card_id...]
  scenarios[].id  ───────────────►    encounters / encounter_sets /
  champs[].cle ───► (lus par) ───►    modular_sets  (tous des card_id ou ids de sets)
        │                                   │
        ▼                                   ▼
src/cards/pack/<pack>/campaign.py     data/cards.json  ◄── pack "<pack>": [ {card_id, type, name, ... set_name} ]
  CampaignSetup(niveau)                     │ set_name  ──(nettoyé)──►  src/cards/pack/<pack>/<set_nettoyé>/<card_id>.py
  CollectXXX(niveau)                        │ card_id   ──────────────►  assets/pics/<card_id>.jpg
        ▲                                   │ card_id   ──────────────►  ui-app/src/board/textes-fr-fanmade.ts
        │ appelé par                        ▼
src/cards/pack/<pack>/<scénario>/<id 1A>.py   (la face 1A du complot principal appelle *CampaignSetup(niveau))
```

Trois conséquences pratiques :

1. **Le nom de la clé du carnet est le contrat.** Il apparaît à trois endroits qui doivent être **strictement
   identiques** : dans `campaign.py` (écriture et lecture), dans la description de campagne (`champ.cle`) et,
   le cas échéant, dans un script de carte. Une clé mal orthographiée **ne lève aucune erreur** : le moteur lit
   une valeur vide et la récompense disparaît en silence. `tools/verifier_campagnes.py` (§11) compare les `cle` déclarées aux chaînes littérales du pack (`src/cards/pack/<code>/`, donc **le pack porte le même nom que `code`**) ; la lecture par `CampaignSetup` est contrôlée par `verifier-livraison-campagne.py` et par les épreuves.
2. **Le `set_name` d'une carte décide du dossier de son script.** Un script rangé au mauvais endroit est muet.
3. **L'identifiant d'une carte est une clé partout** : image, texte français, script, scénario, carnet. On ne le
   change jamais une fois livré.


---

## 3. La liste maîtresse des fichiers d'une campagne

Tous les chemins sont **relatifs à la racine du moteur** (`Fusion/marvel-lcg-src/` dans le dépôt) sauf mention
contraire (`ui-app/`, `docs/`, `outils/` sont à la racine du projet, à côté de `Fusion/`).

Légende de la colonne **Livraison** :

* **NEUF** : un fichier nouveau, que tu livres tel quel à son chemin ;
* **FRAGMENT** : un fichier partagé par tout le monde : tu livres **seulement ta part**, Claude la fusionne ;
* **CLAUDE** : fichier que tu ne produis pas (générique, généré, ou touchant le moteur) ; je le liste pour que tu
  saches qu'il existe et ce qui s'y branche ;
* **OPTION** : utile, pas bloquant.

### 3.1 Données (`data/`)

| # | Chemin | Rôle | Livraison | Obligatoire | Modèle (zip) | Détail |
|---|---|---|---|---|---|---|
| D1 | `data/cards.json` | Toutes les cartes du jeu, rangées par pack : `{"<pack>": [carte, ...]}` | **FRAGMENT** `integration/data/cards.<pack>.fragment.json` = `{"<pack>": [...]}` | oui | `modeles/*/data/cards.*.fragment.json` | §4 |
| D2 | `data/sets_info.json` | L'index des packs : clé `N. Custom (Nom)` → scénarios, héros, sets modulaires, plus grand id | **FRAGMENT** `integration/data/sets_info.<pack>.fragment.json` | oui | `modeles/*/data/sets_info.*.fragment.json` | §5.4 |
| D3 | `data/scenarios/<id>.json` | Un scénario : vilain(s), complot(s) principal(aux), sets de rencontre | **NEUF** | oui, un par scénario | `modeles/*/data/scenarios/` | §5.1 |
| D4 | `data/scenarios/<id>_expert.json` | La variante experte du scénario | **NEUF** | oui si la campagne a un mode expert (toutes les officielles en ont un) | idem | §5.1 |
| D5 | `data/encounter_sets/<set>.json` | Un set de rencontre (modulaire ou propre à un scénario) | **NEUF** | un par set | `modeles/*/data/encounter_sets/` | §5.2 |
| D6 | `data/campagnes/<code>.json` | **La description de la campagne** (écran + panneau de récompenses) | **NEUF** | **oui** | `modeles/*/data/campagnes/` | §8 |
| D7 | `data/nemesis/<héros>_nemesis.json` | Set némésis d'un héros nommable | **NEUF** | option (héros seulement) | `modeles/A-*/` | §5.3 |
| D8 | `deck/starter/<héros>.json` | Deck de départ d'un héros (fait apparaître le héros dans le jeu) | **NEUF** | seulement si la campagne apporte des héros | `commun/` + §5.5 | §5.5 |
| D9 | `data/cards_custom.json` | Second catalogue (anciennes cartes d'auteurs) | **CLAUDE** | ne pas utiliser pour un pack neuf | — | — |
| D10 | `data/arts_alternatifs.json`, `data/images_cartes.json`, `data/identites.json`, `data/palettes-heros.json` | Cosmétique (arts alternatifs, relevé des illustrations, couleurs de héros) | **CLAUDE** | non | — | — |

### 3.2 Moteur : scripts Python (`src/cards/pack/<pack>/`)

`<pack>` est la clé du pack dans `cards.json` : un nom court en minuscules et soulignés (`web_of_deceit`, `mts`,
`skrull_menace`). C'est aussi le nom du dossier.

| # | Chemin | Rôle | Livraison | Obligatoire | Détail |
|---|---|---|---|---|---|
| M1 | `src/cards/pack/<pack>/__init__.py` | Fonctions partagées par plusieurs sets du pack (`from cards.pack import *` en tête) | **NEUF** | option | §6.1 |
| M2 | `src/cards/pack/<pack>/<set_nettoyé>/__init__.py` | **Obligatoire dans chaque dossier de set** : sans lui, les cartes du set n'ont aucune capacité, sans erreur | **NEUF** | **oui** | §6.1 |
| M3 | `src/cards/pack/<pack>/<set_nettoyé>/<card_id>.py` | Le script d'**une face** qui a une capacité imprimée | **NEUF** | une par face à capacité | §6 |
| M4 | `src/cards/pack/<pack>/campaign.py` | **La logique de carnet** : `CampaignSetup(niveau)` (mise en place) + `Collect...` (carnet sortant) | **NEUF** | **oui** | §7 |
| M5 | `src/cards/pack/<pack>/<scénario>/<id_1A>.py` | La face **1A du complot principal** de chaque scénario *appelle* `*CampaignSetup(niveau)` : c'est ce qui branche le carnet | **NEUF** | **oui**, un par scénario (sauf le 1er si rien à appliquer) | §7.3 |
| M6 | `src/game/card/face/card_face.py` | Listes blanches de traits et de compteurs | **CLAUDE** → tu écris tes besoins dans `BESOINS-MOTEUR.md` | — | §4.5 |
| M7 | `src/game/**`, `src/engine/**` | Le moteur lui-même | **CLAUDE** | jamais toi | — |

### 3.3 Registre, textes, interface

| # | Chemin | Rôle | Livraison | Obligatoire | Détail |
|---|---|---|---|---|---|
| R1 | `tools/prefixes_fanmade.json` | Registre des préfixes de `card_id` fan-made (2 lettres) | **FRAGMENT** `integration/tools/prefixes.<pack>.fragment.json` | oui si fan-made | §4.4 |
| T1 | `ui-app/src/board/textes-fr-fanmade.ts` | **Le texte français de chaque carte fan-made** (seul français que le joueur verra dessus) | **FRAGMENT** `integration/textes-fr/<pack>.fragment.txt` (lignes `'id': "texte",`) | oui si fan-made | §10.3 |
| T2 | `public/js/traduction/textes-fr-fanmade.js` | Copie générée du précédent | **CLAUDE** (généré) | — | §10.3 |
| T3 | `public/js/prepare/mechants-info.js` | Mini-biographie du vilain (survol dans le choix du méchant) | **FRAGMENT** `integration/public/js/prepare/mechants-info.fragment.js` | option | §10.5 |
| T4 | `public/js/prepare/heros-info.js` | Biographie d'un héros | **FRAGMENT** | seulement pour un héros | §10.5 |
| T5 | `ui-app/src/board/dico-en.ts`, `public/js/prepare/dico-en.js` | Dictionnaire français → anglais des chaînes de l'interface | **CLAUDE** | — | §10.4 |
| T6 | `public/js/deckbuilder/regles.js` (`SETS_RESERVES_A_LA_CAMPAGNE`) | Cartes qui ne peuvent entrer dans un deck que par la campagne (cartes de campagne) | **CLAUDE** → signale-le dans `BESOINS-MOTEUR.md` | si la campagne a des cartes « réservées » | §14 |
| T7 | `public/campagne.html`, `public/js/campagne/*.js`, `ui-app/src/board/campagne/*` | Écran des campagnes et panneau de récompenses | **CLAUDE** | non | §9 |
| T8 | `src/engine/device/web/server/server_campagne.py` | Routes de campagne | **CLAUDE** | non | §9 |

### 3.4 Images

Toutes ces images sont **fournies par l'utilisateur** (scans, PDF de l'auteur). Tu ne les produis pas : tu
livres **`integration/images.md`**, un tableau `card_id → fichier source → orientation → remarque`, et la liste
des pages de livret attendues.

| # | Chemin | Rôle | Format | Obligatoire | Détail |
|---|---|---|---|---|---|
| I1 | `assets/pics/<card_id>.<jpg\|png\|webp>` | L'image de chaque face de carte. L'extension est **obligatoire**. | portrait ≈ 600×840 ; complots en **paysage** ≈ 840×600 | oui, une par `card_id` | §10.1 |
| I2 | `assets/vignettes/` | Miniatures de la table | généré par `tools/generer_vignettes.py` | **CLAUDE** | §10.1 |
| I3 | `assets/pics-fr/<card_id>.jpg` | Scans français officiels | seulement le contenu officiel | **CLAUDE** | — |
| I4 | `assets/textures/sets/<cle_extension>.webp` | L'image de la boîte (écran des campagnes, choix du méchant) | pochette | oui | §10.2 |
| I5 | `public/img/prepare/boites/<n>.webp` | Pochette recadrée de la boîte | générée par `outils/pochettes-boites.py` | **CLAUDE** | §10.2 |
| I6 | `public/stories/<code>/00-couverture.jpg` | Couverture du livret | carré 975×975 | option (repli : l'image de la boîte) | §10.6 |
| I7 | `public/stories/<code>/<NN>-<scénario>-<intro\|regles\|epilogue>-<n>.jpg` | Planches du livret, par scénario | carré 975×975 | option, mais l'écran les affiche | §10.6 |
| I8 | `public/stories/<code>/fr/<même nom>.jpg` | Pages du livret refaites en français | idem | option ; active seulement si `livret_fr: true` | §10.6 |

### 3.5 Preuves et documentation

| # | Chemin | Rôle | Livraison | Obligatoire | Détail |
|---|---|---|---|---|---|
| P1 | `tools/cas/<bloc>.py` | Les **cas de test de capacité** des cartes (un cas par capacité, avec preuve par substitution) | **NEUF** | **oui** pour chaque carte à capacité | §11.2 |
| P2 | `tools/epreuves_campagnes.py` | Les **épreuves de boucle de campagne** (partie 1 gagnée → carnet → partie 2) | **FRAGMENT** `integration/tools/epreuves.<code>.fragment.py` (`EPREUVES += [...]`) | **oui** | §11.3 |
| P3 | `tools/test_capacites.py` | Le harnais (il découvre `tools/cas/*.py` tout seul) | **CLAUDE** | — | §11.2 |
| P4 | `ui-check/tests/campagne-<code>.spec.ts` | Test d'écran Playwright | **CLAUDE** | non | — |
| P5 | `docs/packs/<code>/` | Dossier de conception : relevé des cartes, livret FR, décisions | **NEUF** | option | §12 |
| P6 | `docs/packs/<code>/GABARITS.md` | Un gabarit `PROCESSUS-CARTE` par carte, preuves réelles | **NEUF** | **oui** | §11.1 |

### 3.6 Le strict minimum pour qu'une campagne apparaisse et se joue

Dans l'ordre : D1 (cartes) → D3/D4/D5 (scénarios, sets) → D2 (index) → D6 (campagne) → I1 (images) → M2/M3
(scripts) → M4+M5 (carnet) → T1 (français) → P1/P2 (preuves). Sans D2, la campagne n'apparaît nulle part ; sans
D6, elle n'est pas une campagne (juste des scénarios isolés) ; sans M4/M5, le carnet est ignoré **en silence**.

### 3.7 Comment une campagne apparaît dans le jeu : ce qui est lu automatiquement

* `/list_campagnes_definies` lit **tous** les `data/campagnes/*.json` et les trie par le numéro de
  `cle_extension` (« 21. The Mad Titan's Shadow » → 21). Ajouter un fichier suffit : rien à enregistrer ailleurs.
* L'écran charge ensuite `catalog.scenariosForExtension(cle_extension)` : il cherche **dans `sets_info.json` la
  clé exactement égale** à `cle_extension` et en lit la liste `scenarios`. Une clé qui diffère d'un seul
  caractère → « scénario introuvable dans le catalogue ».
* Le scénario réel lancé est `data/scenarios/<id>.json`, ou `<id>_expert.json` si la campagne est experte **et**
  que ce fichier existe.
* `tools/cas/*.py` est découvert par un `glob` : déposer le fichier suffit.
* L'image de la boîte est `/sets/<cle_extension>` → `assets/textures/sets/<cle_extension>.webp`.


---

## 4. Les cartes : `data/cards.json`

Toutes les valeurs de ce chapitre ont été **mesurées le 20/10/2026 sur le fichier réel** (7 713 cartes, 170
packs), pas recopiées d'un ancien document. L'annexe A (`annexes/A-kit-cartes.md`) contient, en plus, un
catalogue d'exemples réels classés par mécanique : tu t'en sers pour *écrire* les scripts (§6).

### 4.1 Structure du fichier et forme de ta livraison

`data/cards.json` est un objet : **clé = nom du pack, valeur = liste de cartes**, plus une clé finale
`checksum`. Exemple de la forme (abrégé) :

```json
{
  "core": [ {...}, {...} ],
  "web_of_deceit": [ {...}, {...} ],
  "checksum": "…"
}
```

Tu ne livres **jamais** le fichier entier. Tu livres un fragment qui ne contient que **ton** pack :

```json
{
  "<pack>": [
    { "card_id": "xx001a", "type": "Villain", ... },
    { "card_id": "xx001b", "type": "Villain", ... }
  ]
}
```

Trie les cartes par `card_id`. Indentation : 4 espaces, `ensure_ascii=False` (les accents restent des accents).
Le `checksum` n'est pas ton affaire : Claude le recalcule avec `tools/recalculer_checksums.py` (le moteur rejette
en silence un fichier dont le checksum est faux).

### 4.2 Clés de premier niveau d'une carte

| Clé | Obligatoire | Sens |
|---|---|---|
| `card_id` | oui | L'identifiant, unique dans tout le jeu (§4.4). |
| `type` | oui | Un des types du §4.3. |
| `name` | oui | Le nom **imprimé**. Préfixe `"* "` = carte **unique** (`"* Shocker"`). |
| `subtitle` | oui | Le sous-titre imprimé, `""` sinon. |
| `desc` | oui | Statistiques et mots-clés, **toutes les valeurs en chaînes** (§4.5). `{}` si rien. |
| `traits` | oui | Liste de traits **en MAJUSCULES** : `["CRIMINAL", "SCIENTIST"]`, `[]` sinon. |
| `set_name` | oui | Le set de la carte. **Décide du dossier de son script** (§6.1). `""` pour une carte d'aspect ou basique. |
| `text` | oui (même vide `""`) | Le texte imprimé, avec balises (§4.6). |
| `custom` | **oui pour tout contenu fan-made** | Le nom de l'**auteur** (`"Nugget"`, `"Kajislav"`). Jamais un booléen. Sur **toutes** les faces, identités comprises : c'est ce qui fait afficher le créateur dans le jeu. |
| `full_link` | rare | La carte est un **clone intégral** d'une autre : `{"card_id": "wd051", "full_link": "32014"}` et **rien d'autre**. Sans script, sans image propre. |
| `ability_link` | rare | Mêmes **capacités** qu'une autre carte, mais données propres (nom, traits, image différents) : `"ability_link": "53035"`. |
| `pic_id` | rare | L'image d'une **autre** carte est empruntée (cartes génériques de statut). Sinon `card_id` sert de nom de fichier. |
| `unique_also` | rare | Liste de **noms** dont la carte partage l'unicité : `["Winter Soldier"]` (Bo-Wing et Winter Soldier ne coexistent pas). |
| `multiverse_of` | rare | Carte « Multiverse » jumelle : `"ra003"`. |
| `unique` | rare | `true` : unicité forcée quand le préfixe `"* "` du nom ne suffit pas. |

Le moteur Python **ignore les clés inconnues** et ne lit que `card_id`, `pic_id`, `type`, `name`, `subtitle`,
`desc`, `traits`, `set_name`, `text`. Les clés `custom`, `unique_also`… servent au client.

### 4.3 Les types de carte

Mesuré sur le fichier (le nombre est celui des cartes existantes) :

| `type` | Nombre | Sert à | Remarques |
|---|---|---|---|
| `Villain` | 350 | un vilain, **une carte par stade** | `Stage`, `HP` (souvent `"16*"` = par joueur ; `"INF"` = infini), `ATK`, `SCH` |
| `MainScheme` | 346 | complot principal, **une carte par face** (`…a` / `…b`) | `Stage` (`"1A"`, `"1B"`, `"2"`), `StartingThreat`, `TargetThreat`, `EscalationThreat` |
| `SideScheme` | 565 | complot annexe. **Dans les scripts, cette classe s'appelle `EncounterSideScheme`.** | `StartingThreat`, `Boost`, icônes `Acceleration`/`Hazard`/`Crisis`/`Amplify`, `Hinder` |
| `Minion` | 790 | sbire | `HP`, `ATK`, `SCH`, `Boost`, mots-clés |
| `Treachery` | 698 | traîtrise | `Boost`, parfois `Surge` |
| `Attachment` | 510 | attachement de rencontre | `Boost`, `ATK+`/`SCH+`/`THW+`/`DEF+` |
| `Environment` | 155 | environnement | `Boost`, `Setup`, `Permanent`, `Uses` |
| `Obligation` | 206 | obligation d'un héros | `GiveTo` (nom de l'alter-ego) |
| `Hero` / `AlterEgo` | 160 / 156 | les deux faces d'une identité (`…a` héros, `…b` alter-ego) | héros : `HP ATK THW DEF HS` ; alter-ego : `HP REC HS` |
| `Ally` `Event` `Upgrade` `Support` `Resource` | 649 / 1142 / 973 / 341 / 134 | cartes **joueur** | `Cost`, `RES`, `Class` |
| `PlayerSideScheme` | 66 | complot annexe de **joueur** | `StartingThreat`, `Class` |
| `Leader` | 24 | chef (mode bataille) | `Stage` |
| `Evidence` | 9 | preuve (campagne Agents of S.H.I.E.L.D.) | `Subtype` (`Means` / `Motive` / `Opportunity`) |
| `Path` | 12 | voie Shinobi (TMNT) | `Permanent`, `Class` |
| `Status` `Insert` `Challenge` `PlayerMinion` | 7 / 4 / 26 / 1 | cartes d'état, d'insert, de défi, sbire de joueur | rares |

Une carte de **campagne** qui récompense les joueurs (un allié, une amélioration, une ressource, un événement…)
est une carte joueur ordinaire dont `desc.Class` vaut **`"Campaign"`**, **`"Campaign;Basic"`** ou
**`"Campaign;<aspect>"`** (`"Campaign;Leadership"`, `"Campaign;'Pool"`…) et dont le `set_name` est celui de la
boîte : `"The Mad Titan's Shadow Campaign"`, `"Web of Deceit Rewards"`. Elles n'entrent dans un deck que par la
mise en place de la campagne (voir §7).

### 4.4 Identifiants : numérotation et préfixes

* **Contenu officiel** : **cinq chiffres** — numéro du pack puis numéro de carte (`01001` = pack 1, carte 1).
  Faces : suffixe `a` / `b` / `c` (`01001a` héros, `01001b` alter-ego ; `01097a`/`01097b` complot).
* **Contenu fan-made** : **deux lettres de préfixe propres à la source**, puis **trois chiffres**, puis le
  suffixe de face éventuel : `wd001a`, `hs164`, `sk289b`. Lettres et chiffres ne se rencontrent jamais :
  aucune collision possible avec les sorties officielles (qui vont jusqu'à 60 et au-delà).
* **Le préfixe est choisi AVANT la première carte.** Il est déclaré dans `tools/prefixes_fanmade.json`
  (le vérificateur `verifier_prefixes.py` refuse tout préfixe non déclaré). **Propose deux préfixes libres**
  à l'utilisateur, en question à choix multiple, et attends sa réponse. Préfixes **déjà pris** (liste exacte,
  lue dans le registre au moment de la construction du kit ; elle est aussi dans `reference/prefixes-pris.json`) :

  `aa`, `ab`, `ag`, `ah`, `al`, `an`, `ar`, `as`, `av`, `bc`, `bk`, `bl`, `br`, `bt`, `bw`, `cc`, `cd`, `cn`, `dd`, `dr`, `dt`, `dz`, `gb`, `gp`, `gs`, `hc`, `hd`, `hk`, `ho`, `hs`, `ht`, `ih`, `il`, `im`, `ip`, `iw`, `jj`, `kb`, `lj`, `ls`, `ma`, `mf`, `mk`, `mu`, `mw`, `nt`, `nv`, `ok`, `pt`, `pu`, `ra`, `rg`, `rs`, `sa`, `sb`, `sc`, `sd`, `se`, `sf`, `sg`, `sh`, `si`, `sj`, `sk`, `sm`, `sn`, `sp`, `sr`, `ss`, `st`, `su`, `sw`, `ta`, `tc`, `td`, `te`, `tg`, `th`, `tj`, `tk`, `tl`, `tm`, `tr`, `ts`, `tt`, `tv`, `tx`, `ua`, `ub`, `ud`, `uj`, `ul`, `up`, `vp`, `vr`, `vv`, `vz`, `wc`, `wd`, `wx`, `yd`, `ze`

* **Numérotation conseillée pour un pack de campagne** (modèle `wd`, `sk`) : le vilain et les complots du
  scénario 1 d'abord (`xx001a`, `xx001b`, `xx002a`…), puis ses cartes de rencontre ; puis le scénario suivant ;
  puis les sets modulaires ; puis les cartes de campagne et de récompense. **Numérotation continue, sans trou.**
  Le plus grand identifiant se déclare dans `sets_info.json` (`max_id`).
* **Plusieurs exemplaires** d'une même carte dans un deck de rencontre : **un seul `card_id`**, répété dans la
  liste du set (§5.2). **Deux exemplaires aux ressources différentes** = **deux** identifiants.
* **Une carte vue sur plusieurs boîtes** (réimpression) : un seul script (modèle de référence), plusieurs
  `card_id` si les numéros imprimés diffèrent, reliés par `ability_link` ou `full_link`.
* **Clé du pack** : nom court en minuscules et soulignés (`web_of_deceit`). C'est aussi le nom du dossier
  `src/cards/pack/<pack>/`.
* **`set_name`** : le nom du set imprimé (`"Shocker"`, `"Crime Wave"`). Set némésis d'un héros :
  `"<Héros> Nemesis"`.

### 4.5 `desc` : le contenu complet

**Toutes les valeurs sont des chaînes.** `"HP": "10"`, jamais `"HP": 10`.

#### 4.5.1 Statistiques et coûts

| Clé | Sens | Formes mesurées |
|---|---|---|
| `Cost` | coût | `"0"`…`"7"`, `"X"` (20 cartes), `"1*"` (variable), `"-1"` |
| `RES` | ressource(s) imprimée(s) : `R` physique, `B` mentale, `Y` énergie, `G` joker (wild) ; plusieurs lettres = plusieurs ressources | `"Y"`, `"BB"`, `"RY"`, `"YYY"`… |
| `Class` | classe | `Hero` (signature d'un héros), `Basic`, `Aggression`, `Justice`, `Leadership`, `Protection`, `Determination`, `'Pool`, `Venomized`, `Campaign`, `Campaign;Basic`, `Campaign;<aspect>`, `Encounter`… ; plusieurs valeurs séparées par `;` |
| `HP` | points de vie | `"10"` ; `"14*"` = **par joueur** (14 × nombre de joueurs) pour un vilain/sbire ; `"INF"` = infini |
| `ATK` `THW` `DEF` `REC` `SCH` | attaque, contre, défense, récupération, manigance | `"2"` ; `"1*"` sur `ATK`/`THW` d'un **allié** = **dégâts consécutifs** (1 dégât à l'allié par usage) — **un sens différent** du « par joueur » |
| `HS` | taille de main | `"5"` |
| `Boost` | nombre d'icônes de boost d'une carte de rencontre | `"0"`…`"4"` |
| `ATK+` `SCH+` `THW+` `DEF+` | bonus (ou malus) imprimé d'un attachement/amélioration à son porteur | `"1"`, `"-1"` |
| `Stage` | étape d'un vilain ou d'un complot | vilain : `"1"` `"2"` `"3"`, ou `"I"` `"II"` `"III"`, ou `"A"` `"B"` ; complot : `"1A"` `"1B"` `"2A"` … ou `"1"` `"2"` `"3"` |
| `StartingThreat` `TargetThreat` `EscalationThreat` | menaces d'un complot | `"7*"` = par joueur. Complot principal : `StartingThreat` souvent `"0"`/`"1*"`, `TargetThreat` `"7*"`…`"12*"`, `EscalationThreat` `"1*"` |
| `Uses` | `"<N>,<compteur>"` : la carte entre en jeu avec N compteurs et part quand le dernier est retiré | `"3,web"`, `"2*,ammo"` (`*` = par joueur), `"1+1*,fury"` |
| `GiveTo` | obligation : nom de l'alter-ego destinataire | `"Peter Parker"` |
| `Nemesis` | sbire némésis : nom du héros | `"Spider-Man"` |
| `MaxPerDeck` `MaxPerUnit` | limites de deck / par cible | `"1"` |
| `Victory` | points de victoire ; la carte va dans la pile de victoire quand vaincue. **`"0"` y envoie aussi la carte : ce n'est pas « neutre »** | `"0"` `"1"` `"2"` `"-1"` |
| `Requirement` | ressources obligatoires dans le paiement | `"B"`, `"YBR"` |
| `TeamUp` | événement Team-Up : les deux héros | `"Ant-Man;Wasp"` |
| `Teamwork` | trait du travail d'équipe | `"AVENGER"` |
| `Linked` | nom de la carte liée | `"Specialized Training"` |
| `UnitCost` | coût en unités (marché de campagne) | `"1"`…`"6"` |
| `ThreatLevel` | niveau de menace (mot-clé maison de Threat Level) | `"1"`…`"5"` |
| `Form` | forme (Spectrum) | `"Energy"`, `"Mass"`, `"Suit"` |
| `Subtype` | sous-type d'une preuve | `"Means"`, `"Motive"`, `"Opportunity"` |
| `CorrespondingCard` | complot annexe lié à un vilain précis | `"Wrecker"` |
| `Assault` | mot-clé Assaut | `"1"` |

#### 4.5.2 Mots-clés lus **directement** dans `desc` : AUCUN script

Ces mots-clés sont gérés **entièrement par le moteur** à partir de `desc`. **Tu ne les codes jamais dans un
script** : un script qui les recode les applique deux fois.

`Toughness`, `Guard`, `Patrol`, `Quickstrike`, `Retaliate`, `Surge`, `Villainous`, `Hazard`, `Crisis`,
`Acceleration`, `Amplify`, `Steady`, `Stalwart`, `Peril`, `Incite`, `Hinder`, `Vulnerable`, `Permanent`,
`Restricted`, `Setup` (entrée en jeu à la mise en place), `Temporary`, `Teamwork`, `Alliance`, `Uses`,
`Victory`, `Requirement`, `GiveTo`, `Boost` (le nombre d'icônes), `MaxPerDeck`, `MaxPerUnit`, `Nemesis`,
`TeamUp`, `Assault`.

Valeurs mesurées : `Toughness`/`Guard`/`Retaliate`/`Patrol`/`Quickstrike`… `"1"`, `"2"` (un compteur) ;
`Hinder` `"1*"` `"2*"` `"3*"` (par joueur) ; `Surge` `"1"` ; `Setup` `"1"` ; `Permanent` `"1"`.

Rappels de sens (pour choisir la bonne clé) :

* **Guard** : tant que ce sbire est engagé avec toi, tu ne peux pas attaquer le vilain.
* **Patrol** : tant que ce sbire est engagé avec toi, tu ne peux pas contrer le complot principal.
* **Crisis** : tant que ce complot annexe est en jeu, on ne peut pas retirer de menace du complot principal.
* **Hazard** : +1 carte de rencontre distribuée pendant la phase du vilain. **Acceleration** : +1 menace sur le
  complot principal au début de la phase du vilain. **Ne pas confondre.**
* **Hinder N** : la carte entre en jeu avec N menaces **sur elle-même**. **Incite N** : à la révélation, N
  menaces sur le **complot principal**.
* **Amplify** : ajoute des icônes de boost aux cartes de boost retournées. **Toughness** : entre en jeu avec une
  carte de statut Robuste (Tough). **Steady** : peut recevoir deux cartes de statut Sonné/Désorienté.
  **Stalwart** : ne peut pas être sonné ni désorienté. **Vulnerable** : défaussé s'il est sonné/désorienté.

**Ne mets pas un mot-clé dans `desc` si le texte imprimé de CETTE carte ne le porte pas**, et inversement : le
vérificateur `verifier_desc_mots_cles.py` compare texte et `desc`. Piège classique : « Uses (3 tactic counters) »
dans le texte sans `"Uses": "3,tactic"` dans `desc` → la carte entre en jeu **sans compteur** et son action reste
**grisée pour toujours**, sans aucun message.

⚠ Certains attributs n'existent que pour certains types (`Uses` : Upgrade/Support/Attachment/Obligation/
Environment ; `Villainous` : Minion). Le mettre ailleurs **empêche la carte de se générer** (KeyError).

#### 4.5.3 Quelles clés `desc` pour quel type (mesuré)

| Type | Clés attendues (fréquence) |
|---|---|
| Villain | `HP` 100 %, `Stage` 99 %, `SCH` 98 %, `ATK` 97 %, puis `Toughness`, `Steady`, `Retaliate`, `Stalwart`, `Victory` |
| MainScheme | `Stage` 100 %, `StartingThreat`, `TargetThreat`, `EscalationThreat` (~50 % : seules les faces « A » les portent) |
| SideScheme | `StartingThreat` 98 %, `Boost` 83 %, `Hinder`, `Acceleration`, `Hazard`, `Crisis`, `Amplify`, `Victory` |
| Minion | `HP` 100 %, `ATK`, `SCH`, `Boost` 76 %, `Nemesis`, `Toughness`, `Villainous`, `Quickstrike`, `Guard`, `Retaliate`, `Patrol`, `Victory` |
| Treachery | `Boost` 75 %, parfois `Surge` |
| Attachment | `Boost` 68 %, `ATK+` 37 %, `SCH+` 18 %, `Permanent`, `Uses` |
| Environment | `Boost` 21 %, `Surge`, `Setup`, `Permanent`, `Uses` |
| Obligation | `GiveTo` 92 %, `Boost` 89 % |
| Hero | `HP ATK THW DEF HS` (100 %) ; AlterEgo : `HP REC HS` |
| Ally | `HP` 100 %, `ATK` `THW` `Cost` `RES` `Class` |
| Event | `Cost` `Class` `RES` (100 %), `MaxPerDeck`, `TeamUp` |
| Upgrade / Support | `Class`, `RES`, `Cost`, `Uses`, `MaxPerUnit`, `Restricted`, `Permanent` |
| Resource | `RES`, `Class`, `MaxPerDeck` |
| PlayerSideScheme | `Class`, `StartingThreat`, `Cost`, `RES`, `Victory` |

#### 4.5.4 Traits et compteurs : listes blanches du moteur

* **Les traits** sont en MAJUSCULES, exactement comme imprimés (`"S.H.I.E.L.D"`, `"MASTERS OF EVIL"`). Le typage
  du moteur les liste (`CardFace.TRAITS`, `reference/traits.json` du zip) mais **aucun contrôle ne les lit à
  l'exécution** : un trait neuf ne casse pas une partie. **Tu l'écris quand même** et tu le signales dans
  `BESOINS-MOTEUR.md` (« trait nouveau : X, porté par xx012 ») : Claude l'ajoute à la liste.
* **Les compteurs** (`desc.Uses` : `"3,web"`) **ne sont PAS libres.** Le nom du compteur doit être dans l'énum
  `CardFace.COUNTER` (`reference/compteurs.json`) : sinon `desc.Uses` **lève une assertion** et la carte ne se
  construit pas. Un compteur neuf va dans `BESOINS-MOTEUR.md` ; Claude l'ajoute avant tout test.
* **Les jetons** (`k_threat`, `k_damage`, `k_acceleration_token`, `k_first_player_token`) et leurs noms
  `TOKEN` sont fixes.

### 4.6 Le texte imprimé (`text`) : balises et jetons

Le texte est en **anglais**, tel qu'imprimé, avec ces balises (mesurées sur tout le fichier) :

| Balise | Sens | Fréquence |
|---|---|---|
| `<b>…</b>` | gras : type de capacité (`<b>Response</b>`, `<b>When Revealed</b>`, `<b>Forced Interrupt</b>`…) | 8 335 |
| `<i>…</i>` | italique : rappel de règle, récit | 2 763 |
| `<hr />` | sépare le texte de la carte de son effet `[star] Boost` | 645 |
| `<em>…</em>` | emphase (rare) | 5 |
| `\n` | retour à la ligne (certains textes ont `\r\n` : sans importance) | — |
| `[star]` | étoile en tête de ligne : capacité étoilée (permanente, ou effet de Boost) | 1 651 |
| `[per_hero]` | « par joueur » | 371 |
| `[energy]` `[mental]` `[physical]` `[wild]` | icônes de ressource | |
| `[boost]` | une icône de boost | |
| `[crisis]` `[acceleration]` `[hazard]` `[amplify]` | icônes de complot | |
| `[consequential]` | dégâts consécutifs | |
| `[[TRAIT]]` | un trait, **entre doubles crochets** (`[[Tech]]`, `[[AVENGER]]`) | |
| `→` | flèche de coût (« Exhaust X → effet ») | |
| `•` | puce d'un « Choose one » | |

Les icônes de complot (`[crisis]`, `[acceleration]`, `[hazard]`, `[amplify]`) ont une **forme qui varie d'un
auteur à l'autre** : voir §4.8 et §14.5 (piège 53). Ne les nomme jamais à vue.

### 4.7 Cartes à plusieurs faces

* Un **complot principal** est **toujours** une paire `…a` (face A) / `…b` (face B). Il y a une paire par
  **stade**. La face A porte `StartingThreat`/`TargetThreat`/`EscalationThreat` ; la B est la face « avancée ».
* Un **vilain** a une carte **par stade** (`wd035`, `wd036`, `wd037` pour Electro I, II, III) ; un vilain
  **recto-verso** (Shocker, The Lizard) est une paire `…a`/`…b` écrite `"wd001a,wd001b"` dans le scénario.
* Les **faces d'identité** : `…a` héros, `…b` alter-ego (même carte, deux faces).
* Une face = **un fichier de script** si elle a des capacités (§6).

### 4.8 Icônes de ressource et de complot : jamais à vue

Une icône de **ressource** se lit **par comparaison** avec une carte du **même pack** dont la ressource est
connue : `R` physique (poing), `B` mentale (nœuds bleus), `Y` énergie (éclair), `G` joker (étoile verte). Si
l'utilisateur ne te donne pas la ressource en clair et que tu ne peux pas comparer, **pose la question**.

Les icônes de **complot** (Crisis, Acceleration, Hazard, Amplify) **n'ont pas la même forme chez tous les
auteurs** : chaque pack a ses conventions, validées par l'utilisateur (§14.5, piège 53). Compare à une carte du
**même pack** dont l'icône est connue. Les icônes **inconnues** vont dans `QUESTIONS.md`.

### 4.9 Exemples réels, un par type

Tous recopiés du fichier réel. **Web of Deceit** (campagne maison) :

**Vilain recto-verso, face A (wd001a) et B (wd001b)**
```json
{
    "card_id": "wd001a",
    "type": "Villain",
    "name": "* Shocker",
    "subtitle": "",
    "desc": {
        "HP": "10",
        "ATK": "1",
        "SCH": "1",
        "Steady": "1"
    },
    "traits": [
        "CRIMINAL"
    ],
    "set_name": "Shocker",
    "text": "Steady.\n<b>When Defeated</b>: Remove 5 threat from a side scheme. Flip this card.",
    "custom": "Ripper3"
}
```
```json
{
    "card_id": "wd001b",
    "type": "Villain",
    "name": "* Shocker",
    "subtitle": "",
    "desc": {
        "HP": "20",
        "ATK": "2",
        "SCH": "2",
        "Retaliate": "1"
    },
    "traits": [
        "CRIMINAL",
        "MASTERS OF EVIL"
    ],
    "set_name": "Shocker",
    "text": "Retaliate 1.\n<b>When Defeated</b>: Deal 1 damage to each hero. Remove 10 threat from a side scheme. Flip this card.",
    "custom": "Ripper3"
}
```

**Complot principal, faces A et B (wd002a / wd002b)**
```json
{
    "card_id": "wd002a",
    "type": "MainScheme",
    "name": "Shock Party",
    "subtitle": "",
    "desc": {
        "Stage": "1A"
    },
    "traits": [],
    "set_name": "Shocker",
    "text": "<b>Contents</b>: Shocker (A). <i>(Shocker (B) instead for expert mode.)</i> Shocker, City in Chaos, Power Drain II, and Standard III encounter sets. One modular encounter set <i>(recommended: Crime Wave)</i>.\n<b>Setup</b>: Search the encounter deck for The Long Night side scheme and reveal it. Remove each obligation card in the encounter deck from the game.",
    "custom": "Ripper3"
}
```
```json
{
    "card_id": "wd002b",
    "type": "MainScheme",
    "name": "Shock Party",
    "subtitle": "",
    "desc": {
        "StartingThreat": "0",
        "TargetThreat": "4*",
        "EscalationThreat": "1*",
        "Stage": "1B"
    },
    "traits": [],
    "set_name": "Shocker",
    "text": "<b>When Revealed</b>: Search the encounter deck and discard pile for the Vibro-Shock Gauntlets attachment and reveal it.",
    "custom": "Ripper3"
}
```

**Complot annexe (wd015 The Long Night : permanent, victoire à la dernière menace retirée)**
```json
{
    "card_id": "wd015",
    "type": "SideScheme",
    "name": "The Long Night",
    "subtitle": "",
    "desc": {
        "StartingThreat": "10*",
        "Permanent": "1",
        "Hinder": "15"
    },
    "traits": [],
    "set_name": "Shocker",
    "text": "Permanent. Hinder 15[per_hero].\nThe players cannot win unless they survive the night.\n<b>Response</b>: After a CRIMINAL minion is defeated, remove 2 threat from The Long Night.\n<b>Forced Interrupt</b>: When the last threat is removed from this scheme, the players survive the night and win the game.",
    "custom": "Ripper3"
}
```

**Sbire unique (wd006)**
```json
{
    "card_id": "wd006",
    "type": "Minion",
    "name": "* Sandman",
    "subtitle": "",
    "desc": {
        "HP": "5",
        "ATK": "2",
        "SCH": "2",
        "Boost": "3",
        "Toughness": "1"
    },
    "traits": [
        "CRIMINAL"
    ],
    "set_name": "Shocker",
    "text": "Toughness.\n[star] <b>Forced Response</b>: After Sandman attacks or engages you, discard the top 6 cards of the encounter deck.",
    "custom": "Ripper3"
}
```

**Traîtrise (wd012)**
```json
{
    "card_id": "wd012",
    "type": "Treachery",
    "name": "The Getaway",
    "subtitle": "",
    "desc": {
        "Boost": "2"
    },
    "traits": [],
    "set_name": "Shocker",
    "text": "<b>When Revealed</b>: Choose one:\n• Heal 3 damage from Shocker. Shocker schemes.\n• If the Vibro-Shock Gauntlets attachment is not in play, search the encounter deck and discard pile for it and reveal it.",
    "custom": "Ripper3"
}
```

**Attachement (wd005)**
```json
{
    "card_id": "wd005",
    "type": "Attachment",
    "name": "Vibro-Shock Gauntlets",
    "subtitle": "",
    "desc": {
        "ATK+": "1",
        "Boost": "0"
    },
    "traits": [
        "TECH",
        "WEAPON"
    ],
    "set_name": "Shocker",
    "text": "Attach to Shocker.\n[star] <b>Forced Response</b>: After Shocker attacks and damages you, discard a card from your hand.\n<b>Hero Action</b>: Spend [physical] [mental] resources and remove a stunned or confused status card from Shocker → discard Vibro-Shock Gauntlets.\n<hr />\n[star] <b>Boost</b>: Reveal this card.",
    "custom": "Ripper3"
}
```

**Environnement (wd030)**
```json
{
    "card_id": "wd030",
    "type": "Environment",
    "name": "\"Vote for Fisk\"",
    "subtitle": "",
    "desc": {},
    "traits": [],
    "set_name": "Web of Deceit",
    "text": "<i>Standard Mode Only.</i>\n[star] <b>Forced Response</b>: After the villain schemes, place 1 threat on the side scheme with the lowest amount of threat.",
    "custom": "Ripper3"
}
```

**Obligation (wd105)**
```json
{
    "card_id": "wd105",
    "type": "Obligation",
    "name": "FBI Investigation",
    "subtitle": "",
    "desc": {
        "Boost": "2",
        "Acceleration": "1",
        "GiveTo": ""
    },
    "traits": [],
    "set_name": "Kingpin",
    "text": "<b>Forced Response</b>: After a card you control defeats a side scheme, place 1 clue counter here. Then, if there are at least 3 clue counters here, discard this card and place 1 pursuit counter on Pursued by the Past.",
    "custom": "Ripper3"
}
```

**Récompense de campagne : allié (wd113), soutien (wd112), amélioration (wd125), ressource (wd128), complot annexe de joueur (wd140)**
```json
{
    "card_id": "wd113",
    "type": "Ally",
    "name": "* Spider-Girl",
    "subtitle": "Mayday Parker",
    "desc": {
        "Cost": "3",
        "HP": "3",
        "ATK": "2*",
        "THW": "2*",
        "RES": "G",
        "Class": "Campaign;Basic"
    },
    "traits": [
        "WEB-WARRIOR"
    ],
    "set_name": "Web of Deceit Rewards",
    "text": "<b>Response</b>: After Spider-Girl enters play or leaves play, choose:\n• Ready your hero.\n• Heal 1 damage from your alter-ego.",
    "custom": "Ripper3"
}
```
```json
{
    "card_id": "wd112",
    "type": "Support",
    "name": "Great Web Strand",
    "subtitle": "",
    "desc": {
        "Cost": "1",
        "RES": "Y",
        "Class": "Campaign;Basic",
        "Setup": "1"
    },
    "traits": [
        "WEB-WARRIOR"
    ],
    "set_name": "Web of Deceit Rewards",
    "text": "Setup.\n<b>Hero Response</b>: After you change form, discard Great Web Strand → search your deck and discard pile for a WEB-WARRIOR ally or an ally with “Spider” in its title and add it to your hand.",
    "custom": "Ripper3"
}
```
```json
{
    "card_id": "wd125",
    "type": "Upgrade",
    "name": "Spider-Healing Factor",
    "subtitle": "",
    "desc": {
        "Cost": "3",
        "RES": "B",
        "Class": "Campaign;'Pool"
    },
    "traits": [
        "SUPERPOWER"
    ],
    "set_name": "Web of Deceit Rewards",
    "text": "You get +3 hit points.\n<b>Response</b>: After your turn begins, exhaust Spider-Healing Factor → heal 1 damage from your identity.\n<i>(This card is both a Web of Deceit Campaign Reward card and a 'Pool card.)</i>",
    "custom": "Ripper3"
}
```
```json
{
    "card_id": "wd128",
    "type": "Resource",
    "name": "Radioactive Power",
    "subtitle": "",
    "desc": {
        "RES": "RY",
        "Class": "Campaign;Basic"
    },
    "traits": [
        "SUPERPOWER"
    ],
    "set_name": "Web of Deceit Rewards",
    "text": "",
    "custom": "Ripper3"
}
```
```json
{
    "card_id": "wd140",
    "type": "PlayerSideScheme",
    "name": "* See the Future",
    "subtitle": "",
    "desc": {
        "Cost": "0",
        "RES": "B",
        "Class": "Campaign;Basic",
        "StartingThreat": "5",
        "Victory": "0"
    },
    "traits": [],
    "set_name": "Web of Deceit Rewards",
    "text": "Victory 0.\n<b>When Defeated</b>: Each player draws 2 cards. Until the end of the round, play with the top card of the encounter deck faceup.",
    "custom": "Ripper3"
}
```

**The Mad Titan's Shadow** (campagne officielle) : un vilain, un complot principal, et des cartes de campagne.
```json
{
    "card_id": "21071",
    "type": "Villain",
    "name": "* Ebony Maw",
    "subtitle": "",
    "desc": {
        "HP": "14*",
        "ATK": "1",
        "SCH": "2",
        "Stage": "1"
    },
    "traits": [
        "BLACK ORDER",
        "MYSTIC"
    ],
    "set_name": "Ebony Maw",
    "text": "[star] <b>Forced Interrupt</b>: When Ebony Maw activates against you, remove an invocation counter from each [[Spell]] card in your play area."
}
```
```json
{
    "card_id": "21074a",
    "type": "MainScheme",
    "name": "Attack on Knowhere",
    "subtitle": "",
    "desc": {
        "Stage": "1"
    },
    "traits": [],
    "set_name": "Ebony Maw",
    "text": ""
}
```
```json
{
    "card_id": "21074b",
    "type": "MainScheme",
    "name": "Attack on Knowhere",
    "subtitle": "",
    "desc": {
        "StartingThreat": "1*",
        "TargetThreat": "6*",
        "EscalationThreat": "1*",
        "Stage": "1"
    },
    "traits": [],
    "set_name": "Ebony Maw",
    "text": "<b>When Revealed:</b> Each player discards cards from the top of the encounter deck until they discard a [[Spell]] card and puts that card into play in their play area. Shuffle the encounter discard pile into the encounter deck."
}
```
```json
{
    "card_id": "21183",
    "type": "Resource",
    "name": "Shawarma",
    "subtitle": "",
    "desc": {
        "RES": "RBY",
        "Class": "Campaign;Basic",
        "MaxPerDeck": "3"
    },
    "traits": [],
    "set_name": "The Mad Titan's Shadow Campaign",
    "text": ""
}
```
```json
{
    "card_id": "21185",
    "type": "Obligation",
    "name": "System Shock",
    "subtitle": "",
    "desc": {
        "GiveTo": ""
    },
    "traits": [],
    "set_name": "The Mad Titan's Shadow Campaign",
    "text": "You cannot choose to discard this card from your hand.\nWhile this card is in your hand, it gains: \"<b>Alter-Ego Action</b>: Spend a [mental] resource → remove this card from the game.\""
}
```

### 4.10 Checklist de relecture d'une carte (à faire avant de livrer)

- [ ] `card_id` : préfixe déclaré, 3 chiffres, suffixe de face ; **aucun doublon** ; numérotation sans trou.
- [ ] `type` dans la liste du §4.3 ; `name` exact (préfixe `"* "` si unique) ; `custom` renseigné (fan-made).
- [ ] `desc` : **toutes les valeurs en chaînes** ; chaque mot-clé du texte est dans `desc` (et inversement) ;
      chaque nombre imprimé est identique dans `desc` et dans le script.
- [ ] `traits` en MAJUSCULES, exacts ; traits nouveaux signalés.
- [ ] `set_name` identique pour toutes les cartes d'un même set ; dossier de script = nom nettoyé (§6.1).
- [ ] `text` : balises du §4.6 ; icônes de ressource **comparées**, pas devinées.
- [ ] Une carte à capacité a un script **ou** un `A_FAIRE_CLAUDE` ; une carte sans capacité n'a pas de script.
- [ ] Une image `card_id` existe dans `images.md` ; un texte français existe dans le fragment du §10.3.


---

## 5. Les scénarios, les sets de rencontre et l'index des packs

### 5.1 Un scénario : `data/scenarios/<id>.json` et `<id>_expert.json`

`<id>` est en minuscules et soulignés. Pour un contenu fan-made, il porte le **préfixe de la campagne** :
`wd_shocker`, `hs_vermin`, `sk_super_skrull`. Les scénarios officiels n'en ont pas (`ebony_maw`, `rhino`).
**Le fichier `<id>_expert.json` est lu automatiquement** quand la campagne est experte et que ce fichier existe.

Les neuf clés sont **toutes obligatoires**, même vides :

| Clé | Sens |
|---|---|
| `version` | `"0.5.8"` (132 decks, 226 scénarios) ; les fichiers récents portent parfois `"0.5.9"` : **aucun effet** (`UpdateVersion()` ne fait rien). Écris `"0.5.8"`. |
| `name` | Le nom **affiché** du scénario (`"Rhino"`, `"The Lizard"`). |
| `villain` | La liste des cartes de vilain **dans l'ordre des stades**. Standard : stades 1 et 2 (`["01094", "01095"]`). Expert : stades 2 et 3 (`["01095", "01096"]`). Un vilain recto-verso s'écrit en **une chaîne** `"wd054a,wd054b"` ; en expert on **inverse** parfois l'ordre des faces (`"wd001b,wd001a"`). **`[]` pour un scénario à plusieurs vilains** (voir ci-dessous). |
| `expert` | `false` dans le fichier standard, `true` dans le fichier `_expert`. |
| `schemes` | Les complots principaux, **un par stade**, chacun une chaîne `"face A,face B"` : `["wd002a,wd002b", "wd003a,wd003b", "wd004a,wd004b"]`. **Le premier est mis en jeu au départ**, les suivants attendent l'avancée. |
| `set_aside` | Cartes **mises de côté** au départ (créées dans la zone « de côté »). Le scénario (le plus souvent le `Setup` du complot principal) les sortira par un effet. `[]` sinon. |
| `encounters` | Cartes de rencontre **propres au scénario**, **une entrée par exemplaire**. Le cœur du scénario peut vivre ici (modèle officiel) **ou** dans un set à part listé dans `encounter_sets` (modèle fan-made, `encounters: []`). Choisis l'un des deux, pas les deux. |
| `encounter_sets` | Les sets de rencontre **ajoutés** (noms de fichiers de `data/encounter_sets/`, sans extension). Tous **obligatoires** : `"standard"` (ou `"standard_iii"`), et `"expert"` dans le fichier expert. |
| `modular_sets` | Les sets **modulaires** recommandés. **En campagne, ils sont imposés** : l'écran envoie exactement ceux du fichier. |

Une clé facultative existe dans les fichiers de **défis** (`data/challenges/`) : `challenges: ["2401_..."]`
(cartes Défi). Elle n'est pas utile à une campagne.

Le moteur lit ce fichier avec `CampaignDescriptor` (`game/scene/replay/campaign.py`) : `version, name, villain,
expert, challenges, schemes, set_aside, encounters, encounter_sets, modular_sets, campaign_log`. `campaign_log`
n'est **pas** dans le fichier : il est fusionné au lancement depuis le carnet de la campagne.

**Exemples réels : un scénario officiel de campagne, standard puis expert**
*Fichier `Fusion/marvel-lcg-src/data/scenarios/ebony_maw.json` (copie exacte, lue dans le depot au moment de la construction).*

```json
{
    "version": "0.5.8",
    "name": "Ebony Maw",
    "villain": [
        "21071",
        "21072"
    ],
    "expert": false,
    "schemes": [
        "21074a,21074b",
        "21075a,21075b"
    ],
    "set_aside": [
    ],
    "encounters": [
        "21076",
        "21076",
        "21077",
        "21077",
        "21078",
        "21078",
        "21079",
        "21079",
        "21080",
        "21080",
        "21081",
        "21081",
        "21081",
        "21082",
        "21083",
        "21084",
        "21084"
    ],
    "encounter_sets": [
        "standard"
    ],
    "modular_sets": [
        "armies_of_titan",
        "black_order"
    ]
}
```
*Fichier `Fusion/marvel-lcg-src/data/scenarios/ebony_maw_expert.json` (copie exacte, lue dans le depot au moment de la construction).*

```json
{
    "version": "0.5.8",
    "name": "Ebony Maw",
    "villain": [
        "21072",
        "21073"
    ],
    "expert": true,
    "schemes": [
        "21074a,21074b",
        "21075a,21075b"
    ],
    "set_aside": [
    ],
    "encounters": [
        "21076",
        "21076",
        "21077",
        "21077",
        "21078",
        "21078",
        "21079",
        "21079",
        "21080",
        "21080",
        "21081",
        "21081",
        "21081",
        "21082",
        "21083",
        "21084",
        "21084"
    ],
    "encounter_sets": [
        "standard",
        "expert"
    ],
    "modular_sets": [
        "armies_of_titan",
        "black_order"
    ]
}
```

**Exemples réels : un scénario fan-made de campagne (le cœur vit dans des sets, `encounters` est vide)**
*Fichier `Fusion/marvel-lcg-src/data/scenarios/wd_shocker.json` (copie exacte, lue dans le depot au moment de la construction).*

```json
{
    "version": "0.5.8",
    "name": "Shocker",
    "villain": [
        "wd001a,wd001b"
    ],
    "expert": false,
    "schemes": [
        "wd002a,wd002b",
        "wd003a,wd003b",
        "wd004a,wd004b"
    ],
    "set_aside": [
        "wd030",
        "wd031",
        "wd032"
    ],
    "encounters": [],
    "encounter_sets": [
        "shocker",
        "city_in_chaos",
        "power_drain_ii",
        "standard_iii",
        "bodyguard"
    ],
    "modular_sets": [
        "crime_wave"
    ]
}
```
*Fichier `Fusion/marvel-lcg-src/data/scenarios/wd_shocker_expert.json` (copie exacte, lue dans le depot au moment de la construction).*

```json
{
    "version": "0.5.8",
    "name": "Shocker",
    "villain": [
        "wd001b,wd001a"
    ],
    "expert": true,
    "schemes": [
        "wd002a,wd002b",
        "wd003a,wd003b",
        "wd004a,wd004b"
    ],
    "set_aside": [
        "wd030",
        "wd031",
        "wd032"
    ],
    "encounters": [],
    "encounter_sets": [
        "shocker",
        "city_in_chaos",
        "power_drain_ii",
        "standard_iii",
        "bodyguard"
    ],
    "modular_sets": [
        "crime_wave"
    ]
}
```

**Un vilain recto-verso et des modulaires (The Lizard)**
*Fichier `Fusion/marvel-lcg-src/data/scenarios/wd_the_lizard.json` (copie exacte, lue dans le depot au moment de la construction).*

```json
{
    "version": "0.5.8",
    "name": "The Lizard",
    "villain": [
        "wd054a,wd054b"
    ],
    "expert": false,
    "schemes": [
        "wd055a,wd055b",
        "wd056a,wd056b"
    ],
    "set_aside": [
        "wd030",
        "wd031",
        "wd032"
    ],
    "encounters": [],
    "encounter_sets": [
        "the_lizard",
        "standard_iii",
        "bodyguard"
    ],
    "modular_sets": [
        "city_sewers",
        "down_to_earth"
    ]
}
```

**Un scénario fan-made à cartes en vrac (`encounters` rempli, un seul set partagé, un modulaire) : Hunting Season**
*Fichier `Fusion/marvel-lcg-src/data/scenarios/hs_vermin.json` (copie exacte, lue dans le depot au moment de la construction).*

```json
{
  "version": "0.5.8",
  "name": "Vermin",
  "villain": [
    "hs001",
    "hs002"
  ],
  "expert": false,
  "schemes": [
    "hs004a,hs004b",
    "hs005a,hs005b"
  ],
  "set_aside": [],
  "encounters": [
    "hs006",
    "hs007",
    "hs008",
    "hs009",
    "hs010",
    "hs011",
    "hs012",
    "hs013",
    "hs014",
    "hs015",
    "hs016",
    "hs017",
    "hs018",
    "hs019",
    "hs020",
    "hs021",
    "hs022",
    "hs023",
    "hs024",
    "hs025",
    "hs026",
    "hs027",
    "hs028",
    "hs029"
  ],
  "encounter_sets": [
    "standard"
  ],
  "modular_sets": [
    "hs_feral_instincts"
  ]
}
```

**Scénario à PLUSIEURS vilains (Sinister Six) : `villain` est vide, les vilains sont dans `set_aside`**
*Fichier `Fusion/marvel-lcg-src/data/scenarios/sinister_six.json` (copie exacte, lue dans le depot au moment de la construction).*

```json
{
    "version": "0.5.8",
    "name": "Sinister Six",
    "villain": [
    ],
    "expert": false,
    "schemes": [
        "27100a,27100b",
        "27101a,27101b"
    ],
    "set_aside": [
        "27094",
        "27095",
        "27096",
        "27097",
        "27098",
        "27099",
        "27102a,27102b"
    ],
    "encounters": [
        "27103",
        "27103",
        "27104",
        "27104",
        "27105",
        "27106",
        "27107",
        "27108",
        "27109",
        "27110",
        "27111",
        "27111",
        "27111",
        "27112",
        "27112",
        "27112"
    ],
    "encounter_sets": [
        "guerrilla_tactics",
        "standard"
    ],
    "modular_sets": [
    ]
}
```

Pour un scénario à plusieurs vilains, c'est le `Setup` du complot principal qui les met en jeu, après avoir posé
`message.skip_put_villain_into_play = True` (voir les recettes de l'annexe B, « scénario à plusieurs vilains »).
Un vilain à **deux faces** (ALERT / K.O.) est une carte `"idA,idB"` du `set_aside`.

**Règle d'or : les stades.** Le `villain` standard liste les stades **1 et 2** ; l'expert les stades **2 et 3**.
Le complot principal est **le plus souvent le même** dans les deux fichiers (les mêmes `schemes`) : vérifie sur le livret. C'est le **set**
`expert` (ajouté à `encounter_sets`) qui apporte les cartes expert. Pour un vilain en trois stades, vérifie
sur le livret quels stades sont proposés en standard et en expert.

### 5.2 Un set de rencontre : `data/encounter_sets/<set>.json`

Le nom du fichier (sans `.json`) est **l'identifiant du set** : c'est lui qui apparaît dans `encounter_sets`
et `modular_sets` des scénarios et dans `sets_info.json`. Une entrée par exemplaire :

```json
{
    "version": "0.5.8",
    "name": "Feral Instincts",
    "encounters": ["hs141", "hs142", "hs143", "hs144", "hs145"]
}
```

* **`name`** est **le titre affiché au joueur** (écran de mise en place). Écris-le en casse normale
  (`"Feral Instincts"`). Un fichier existant (`shocker.json`) a hérité d'un `name` en minuscules : n'imite pas
  ce défaut.
* **`encounters`** : les `card_id`, **un par exemplaire**. Une carte en deux exemplaires apparaît deux fois.
* **Facultatif — `random_pick`** : ne garder qu'une **partie** des cartes, tirées au hasard à la formation du
  deck de rencontre : `[{"from": ["id1","id2","id3"], "count": 1}, ...]`. Les cartes d'aucun groupe sont toujours
  gardées ; l'ordre du set est conservé (module `game/card/factory.py`, `RandomPick`).

Les sets communs `standard` et `expert` (core) se réutilisent tels quels :
*Fichier `Fusion/marvel-lcg-src/data/encounter_sets/standard.json` (copie exacte, lue dans le depot au moment de la construction).*

```json
{
    "version": "0.5.8",
    "name": "Standard",
    "encounters": [
        "01186",
        "01186",
        "01187",
        "01187",
        "01188",
        "01189",
        "01190"
    ]
}
```
*Fichier `Fusion/marvel-lcg-src/data/encounter_sets/expert.json` (copie exacte, lue dans le depot au moment de la construction).*

```json
{
    "version": "0.5.8",
    "name": "Expert",
    "encounters": [
        "01191",
        "01192",
        "01193"
    ]
}
```

**Un set de scénario fan-made, un modulaire officiel, un modulaire fan-made :**
*Fichier `Fusion/marvel-lcg-src/data/encounter_sets/shocker.json` (copie exacte, lue dans le depot au moment de la construction).*

```json
{
    "version": "0.5.8",
    "name": "shocker",
    "encounters": [
        "wd005",
        "wd006",
        "wd007",
        "wd008",
        "wd009",
        "wd010",
        "wd011",
        "wd012",
        "wd013",
        "wd014",
        "wd014",
        "wd015"
    ]
}
```
*Fichier `Fusion/marvel-lcg-src/data/encounter_sets/black_order.json` (copie exacte, lue dans le depot au moment de la construction).*

```json
{
    "version": "0.5.8",
    "name": "Black Order",
    "encounters": [
        "21085",
        "21086",
        "21087",
        "21088"
    ]
}
```
*Fichier `Fusion/marvel-lcg-src/data/encounter_sets/crime_wave.json` (copie exacte, lue dans le depot au moment de la construction).*

```json
{
    "version": "0.5.8",
    "name": "crime_wave",
    "encounters": [
        "wd016",
        "wd016",
        "wd017",
        "wd017",
        "wd018",
        "wd019"
    ]
}
```

**Un set avec `random_pick`** (Galactic Storm, Imperial Guard) :
*Fichier `Fusion/marvel-lcg-src/data/encounter_sets/gs_imperial_guard.json` (copie exacte, lue dans le depot au moment de la construction).*

```json
{
  "version": "0.5.8",
  "name": "Imperial Guard",
  "encounters": [
    "gs091",
    "gs092",
    "gs093",
    "gs094",
    "gs095",
    "gs096",
    "gs097",
    "gs098",
    "gs099",
    "gs100",
    "gs101",
    "gs102",
    "gs103",
    "gs104",
    "gs105",
    "gs106",
    "gs107",
    "gs108",
    "gs109",
    "gs110",
    "gs111",
    "gs112",
    "gs113"
  ],
  "random_pick": [
    {
      "from": [
        "gs091",
        "gs092",
        "gs093"
      ],
      "count": 1
    },
    {
      "from": [
        "gs094",
        "gs095",
        "gs096",
        "gs097",
        "gs098",
        "gs099",
        "gs100",
        "gs101",
        "gs102",
        "gs103",
        "gs104",
        "gs105",
        "gs106",
        "gs107",
        "gs108",
        "gs109",
        "gs110",
        "gs111"
      ],
      "count": 6
    }
  ]
}
```

⚠ **Chaque set nommé dans `encounter_sets` ou `modular_sets` d'un scénario doit avoir son fichier.** Un set sans
fichier se charge **vide, sans erreur** (`LoadEncounterSet` rend `[]`) : le scénario se monte avec un deck de
rencontre incomplet et rien ne le dit. L'écran de campagne lit aussi chaque fichier pour en afficher le `name` dans
« Mise en place » (à défaut, il affiche un titre déduit de l'identifiant).

### 5.3 Le set némésis d'un héros (si la campagne apporte un héros)

`data/nemesis/<héros>_nemesis.json`, même forme qu'un set de rencontre (`name` : `"Adam Warlock Nemesis"`).
**Facultatif** : le set némésis réellement joué vient du **deck de départ** du héros (`nemesis_set`). Le fichier
sert seulement à charger ce set comme un set nommé.

### 5.4 L'index des packs : `data/sets_info.json`

Chaque pack déclare ses scénarios (les **identifiants de fichier** de scénario), ses héros, ses sets de
rencontre modulaires et son plus grand identifiant. La **clé** est de la forme `N. Nom`, où `N` est un numéro
d'ordre de parution :

* officiel : `"21. The Mad Titan's Shadow"`
* fan-made : `"120. Custom (Web of Deceit)"`, `"143. Custom (Skrull Menace)"`, `"178. Custom (Hunting Season)"`.

**Le numéro est attribué par Claude** (il doit être unique : le vérificateur `verifier_prefixes.py` refuse un
doublon, et il sert de rang de tri). Donne seulement le **nom**.

**Cette clé est celle de `cle_extension` dans `data/campagnes/<code>.json`**, et le nom du fichier de l'image
de boîte : `assets/textures/sets/<clé>.webp`. Les trois doivent être **strictement identiques**, au caractère
près (apostrophes comprises).

Champs d'une entrée : `name` (clé du pack), `scenarios`, `heroes`, `encounters`, `max_id` ; facultatifs :
`underlings`/`manigances` (campagne en ordre libre), `indisponible: true` (extension mise de côté : l'interface
ne la montre plus, les tests continuent).

**Entrée d'une campagne officielle, puis d'une campagne fan-made :**
```json
{
  "21. The Mad Titan's Shadow": {
    "name": "mts",
    "scenarios": [
      "ebony_maw",
      "the_tower_defense",
      "thanos",
      "hela",
      "loki"
    ],
    "heroes": [
      "spectrum",
      "adam_warlock"
    ],
    "encounters": [
      "black_order",
      "armies_of_titan",
      "children_of_thanos",
      "infinity_gauntlet",
      "legions_of_hel",
      "frost_giants",
      "enchantress"
    ],
    "max_id": "21193"
  }
}
```
```json
{
  "120. Custom (Web of Deceit)": {
    "name": "web_of_deceit",
    "scenarios": [
      "wd_shocker",
      "wd_electro",
      "wd_the_lizard",
      "wd_vulture",
      "wd_kingpin",
      "wd_vulture_underling"
    ],
    "heroes": [],
    "encounters": [],
    "max_id": "wd165"
  }
}
```
```json
{
  "143. Custom (Skrull Menace)": {
    "name": "skrull_menace",
    "scenarios": [
      "sk_skrull_empire",
      "sk_super_skrull",
      "sk_paibok",
      "sk_secret_invasion",
      "sk_skrull_pantheon"
    ],
    "heroes": [
      "hulkling_kajislav",
      "lyja"
    ],
    "encounters": [
      "sk_army_of_skrulls",
      "sk_skrull_society",
      "sk_kree_skrull_war",
      "sk_paibok",
      "sk_new_revengers",
      "sk_secret_invasion",
      "sk_skrull_pantheon",
      "sk_dard_van_sect",
      "sk_shaper_of_worlds",
      "sk_skrull_elite_crusader",
      "sk_skrull_elite_jazinda",
      "sk_skrull_elite_skymax",
      "sk_skrull_elite_war_skrull",
      "sk_skrull_elite_xavin",
      "standard_skrull",
      "expert_skrull"
    ],
    "max_id": "sk289b"
  }
}
```

* `scenarios` : les `id` des scénarios **sans** `_expert`, dans l'ordre de la campagne.
* `encounters` : **tous** les sets de rencontre **modulaires** du pack (ceux qu'un joueur peut combiner à
  d'autres scénarios), **pas** les sets propres à un scénario s'ils ne sont pas jouables seuls.
* `max_id` : le **plus grand `card_id`** du pack (`"wd165"`, `"sk289b"`).

### 5.5 Deck de départ d'un héros (seulement si la campagne apporte des héros)

`deck/starter/<héros>.json` — c'est ce fichier qui fait **apparaître** le héros dans le jeu (le catalogue lit
`deck/starter/*.json`). Pour un héros fan-made, **`player_deck` reste vide** sauf si l'auteur fournit une
decklist imprimée (décision du projet : on n'invente pas les cartes d'aspect). Voir `PROCESSUS-HEROS.md`
(annexe D) pour tout ce qu'un héros demande.

```json
{
    "version": "0.5.8",
    "name": "Spider-Man",
    "metadata": { "url": "" },
    "hero": ["01001a,01001b"],
    "hero_deck": ["01002", "01003", "01003", "..."],
    "set_aside": [],
    "obligations": ["01165"],
    "nemesis_set": ["01166", "01167", "01168", "01168", "01169"],
    "player_deck": ["01058", "01059", "..."]
}
```

⚠ **Le moteur ne valide PAS les decks de départ.** Une carte de classe `Hero` (signature) ne doit jamais se
trouver dans le deck d'un autre héros.

### 5.6 La mise en place : ce que le moteur fait des champs du scénario

Dans l'ordre (`World.Initialize`, `game/world/world.py`) : choix des identités ; **8.** le scénario est choisi :
`schemes` → le premier complot est mis en jeu, les autres attendent (`main_schemes_deck`), `villain` → deck de
vilain ; message `WhenGameBeginSetup` ; **9.** le vilain est mis en jeu et ses PV posés ; **10.** le deck de
rencontre est formé : `encounters` + chaque set de `encounter_sets` (via `LoadEncounterSet`), les obligations des
héros posées dessus, mélange ; `set_aside` → zone « de côté » ; **11.** cartes `Setup` mises en jeu ; **12.**
`When Revealed`/`Setup` du complot et du vilain ; **13. Campaign Setup** (§7.2) ; 14. pioche ; 15. mulligans ;
15 bis. `WhenCampaignSetupAfterMulligans` ; 16. capacités de `Setup` des personnages.

### 5.7 Checklist de relecture d'un scénario

- [ ] Les 9 clés sont toutes présentes, `version` = `"0.5.8"` (ou `"0.5.9"`).
- [ ] Chaque `card_id` cité existe dans ta livraison **ou** dans `reference/ids-existants.json`.
- [ ] Chaque set de `encounter_sets` et de `modular_sets` existe (ton fragment ou `reference/sets-existants.json`).
- [ ] `schemes` : une chaîne `"a,b"` par stade ; `villain` : stades corrects pour standard et expert.
- [ ] Le fichier `_expert.json` existe et **diffère** du standard (stades, `expert`, set `expert`).
- [ ] L'entrée `sets_info.json` liste ce scénario (id **sans** `_expert`).
- [ ] Le scénario est joué en **solo ET à 2 joueurs** (les valeurs « par joueur » ne se voient qu'en multi).


---

## 6. Les scripts des cartes (`src/cards/pack/<pack>/…`)

Une carte dont le texte imprime une **capacité** (Action, Response, Interrupt, When Revealed, Boost étoilé,
effet `[star]`…) a un **script Python**. Une carte qui n'a que des statistiques et des mots-clés lus dans `desc`
(§4.5.2) **n'a pas de script**.

Ce chapitre reprend, tel quel, les paragraphes du kit de cartes (annexe A) qui disent **où ranger** un script et
**comment l'écrire** — après les avoir **recontrôlés contre le moteur actuel le 20/10/2026** (53 noms de
fabriques cités, tous trouvés ; tous les paramètres cités existent). Les sous-sections reprises gardent la
numérotation de l'annexe A (7.1 à 7.8).

### 6.1 Où ranger un script

<!-- extrait de docs/reference/KIT-CHATGPT-CREATION.md -->
#### 2.1 Où le moteur cherche le script d'une carte

Le moteur cherche, dans l'ordre :

1. `src/cards/pack/<pack>/<set_nettoyé>/<card_id>.py`
2. `src/cards/pack/<pack>/<card_id>.py`
3. si `set_name` finit par `Nemesis` : le dossier du set **sans** `_nemesis`.

Aucun fichier trouvé = carte sans capacité, **sans erreur**. Un script mal
rangé est donc muet : la carte entre en jeu et ne fait rien.

`<pack>` est la clé du pack dans `cards.json` (par exemple `core`, `fne`,
`web_of_deceit`). `<set_nettoyé>` est le `set_name` de la carte passé par la
règle suivante (copiée de `src/engine/file/manager.py`, fonction `CleanName`) :

```python
# Source : src/engine/file/manager.py
return name.lstrip('*').strip().lower().replace(" - ", "_").replace(" & ", "_").replace(' ', '_').replace("'", "").replace("-", "_").replace("!", "").replace("?", "").replace("(", "").replace(")", "").replace(".", "").replace(",", "").replace("\"", "").replace("&", "_").replace("#", "").replace("/", "")
```

Exemples : `"Spider-Man"` → `spider_man` ; `"Spider-Man Nemesis"` →
`spider_man_nemesis` ; `"Stop the Presses!"` → `stop_the_presses` ; `""`
(cartes d'aspect, sans set) → le script va à la racine du pack.

#### 2.2 Les deux fichiers `__init__.py`

Chaque dossier de set contient un `__init__.py`. Le plus simple, une seule
ligne :

```python
# Source : src/cards/pack/core/spider_man/__init__.py
from cards.pack import *
```

Un pack peut y ranger des fonctions partagées par plusieurs cartes. Le set de
Klaw déclare ainsi la capacité commune à ses deux faces de vilain :

```python
# Source : src/cards/pack/core/klaw/__init__.py
from cards.pack import *

def GiveKlawAdditionalBoostCardWhenAttack():

    def give_additional_boost_card(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(EncounterVillain)
        Unused(this)

        message.GiveAdditionalBoostCardForThisActivation(1, effect)

    return AbilityFactory.WhenUnitWouldAttack(
        AbilityType.ForcedInterrupt,
        "This",
        give_additional_boost_card
    )
```

Et chaque script de carte commence par `from . import *`, qui importe tout ce
que le pack et le moteur exposent.

### 6.1 bis Les fichiers `__init__.py`

<!-- extrait de docs/reference/KIT-CHATGPT-CREATION.md -->
#### 2.2 Les deux fichiers `__init__.py`

Chaque dossier de set contient un `__init__.py`. Le plus simple, une seule
ligne :

```python
# Source : src/cards/pack/core/spider_man/__init__.py
from cards.pack import *
```

Un pack peut y ranger des fonctions partagées par plusieurs cartes. Le set de
Klaw déclare ainsi la capacité commune à ses deux faces de vilain :

```python
# Source : src/cards/pack/core/klaw/__init__.py
from cards.pack import *

def GiveKlawAdditionalBoostCardWhenAttack():

    def give_additional_boost_card(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(EncounterVillain)
        Unused(this)

        message.GiveAdditionalBoostCardForThisActivation(1, effect)

    return AbilityFactory.WhenUnitWouldAttack(
        AbilityType.ForcedInterrupt,
        "This",
        give_additional_boost_card
    )
```

Et chaque script de carte commence par `from . import *`, qui importe tout ce
que le pack et le moteur exposent.

À retenir pour une campagne : le **`__init__.py` à la racine du pack** (`src/cards/pack/<pack>/__init__.py`)
commence par `from cards.pack import *` et porte les fonctions partagées par **plusieurs sets** ; chaque
**`__init__.py` de set** commence par `from cards.pack.<pack> import *` (voir `web_of_deceit/shocker/__init__.py`
dans les modèles) ou, pour un set sans helper, par `from cards.pack import *`. Un pack sans `__init__.py` à sa
racine ne peut pas importer ses propres helpers.

### 6.2 Ce que le script d'une carte peut utiliser (« la surface »)

Un script commence par `from . import *`. Ce `import *` apporte **tout** ce que `src/cards/pack/__init__.py`
expose (voir le fichier dans `commun/moteur/`) : `AbilityFactory`, `AbilityFactoryCampaign`, `AbilityType`,
`CardFinder`, `CostFunc`, `Cost`, `Resources`, `Message`, `Effect`, les types de cartes (`Villain`, `Minion`,
`MainScheme`, `Hero`, `AlterEgo`, `Upgrade`…), `Faces`, `FacesCounter`, `Filter`, `Effects`, `Search`, `Find`,
`Players`, `CampaignLog`, `Utility`, `RunAt`, `SetupCards`, `Worlds`, `AsideModularSet`, `Stores`,
`CardFactory`, `Deck`, `Select`, `Player`, `Scenario`, `Form`, `GameArea`, `OnEvent`, `Condition`, `Rand`,
`DamageProperty`, `PlayerCardImmunity`, `Villains`, `IsCounter`, `IsTrait`, plus quelques fonctions partagées
(`ShuffleThisCardIntoEncounter`, `ThisCardGainSurge`, `DiscardThisCard`, `RemoveThisFromGame`…).

**Ce qui n'est pas dans cette liste n'existe pas pour une carte.** L'index complet de l'API
(`annexes/I-index-api-moteur.md`) donne, pour chaque classe et fonction du moteur, ses arguments et sa première
ligne de commentaire : **c'est ta référence pour ne rien inventer.** Si tu cherches une fonction qui n'y est pas :
`A_FAIRE_CLAUDE`.

### 6.3 Squelette, types de capacité, fabriques, coûts, cibles, opérations (annexe A, §7)

<!-- extrait de docs/reference/KIT-CHATGPT-CREATION.md -->
#### 7.1 Squelette

```python
from . import *

# <Nom de la carte>

def GetAbilities() -> Sequence['Ability']:

    def mon_effet(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        player = message.GetToPlayer()
        ...

    return [
        AbilityFactory.WhenThisRevealed(None, mon_effet),
    ]
```

- Toujours `from . import *` comme première instruction (les lignes « # Source : » des exemples sont des commentaires ajoutés pour ce document, ne les recopie pas).
- Une fonction `GetAbilities()` qui **rend une liste** de capacités.
- Chaque capacité est fabriquée par `AbilityFactory.<Fabrique>(...)`.
- L'opération reçoit `(effect, message)`.
  - `effect.this` : la carte qui porte la capacité ; commence par
    `.CastTo(<Type>)`.
  - `effect.targets` : les cibles choisies via `.SetTarget(...)`.
  - `effect.GetInitiator()` : le joueur qui résout.
  - `message` : dépend du déclencheur (exemples en section 8).
- Une fabrique dont le nom commence par `*` dans les exemples
  (`*AbilityFactory.GiveKeywordToAttached(...)`) rend une **liste** : il faut
  l'étoile pour la déplier dans la liste finale.

#### 7.2 Types de capacité (`AbilityType`)

Valeurs réelles : `Action`, `HeroAction`, `AlterEgoAction`, `ForcedAction`,
`FirstPlayerAction`, `Interrupt`, `HeroInterrupt`, `AlterEgoInterrupt`,
`ForcedInterrupt`, `FirstPlayerInterrupt`, `Response`, `HeroResponse`,
`AlterEgoResponse`, `ForcedResponse`, `Resource`, `HeroResource`,
`AlterEgoResource`, `WhenRevealed`, `WhenDefeated`, `WhenCompleted`, `Boost`,
`Setup`, `Special`, `NonKeyword`, `NonKeywordStar` (capacité `[star]`
permanente).

Le mot imprimé en gras décide du type : « **Forced Response** » →
`ForcedResponse`, « **Hero Action** » → `HeroAction`. Ne remplace jamais un
« Forced » par sa version facultative, ni l'inverse.

#### 7.3 Les fabriques (signatures réelles)

Déclencheurs du joueur et de ses cartes :

| Texte imprimé | Fabrique |
|---|---|
| Action / Hero Action / Alter-Ego Action (carte en jeu ou événement) | `WhenInYourPlayTurn(ability_type, operation, *, conditions=[])` |
| Jouer un événement | la même, suivie de `.SetPlay()` |
| After X enters play | `AfterCardEnterPlay(ability_type, which_card, operation, *, under_your_control=None, conditions=[])` |
| After you play X | `AfterPlayerPlayedCard(ability_type, which_player, which_card, operation, *, from_hand=False, conditions=[])` |
| When you play X | `WhenPlayerPlayCard(ability_type, which_player, played_card, operation, *, label=None, targets=None, using_res=None, conditions=[])` |
| After X attacks | `AfterUnitAttackEnd(ability_type, attacker, operation, *, is_basic_attack=None, damaged_who=None, against_who=None, conditions=[], would_atk_message=None)` |
| After X attacks and damages Y | `AfterUnitAttackAndDamageUnit(ability_type, attacker, who_be_attacked, operation, *, target_in_play=None, use_atk=None, dealt_more_than_damage=None, conditions=[])` |
| After X defeats Y | `AfterUnitDefeatedUnit(ability_type, who_killer, who_be_defeated, operation, *, is_from_attack=None, is_basic_attack=None, has_excess_damage=None, conditions=[])` |
| When X would take damage | `WhenUnitWouldTakeDamage(ability_type, who_take_damage, operation, *, is_from_attack=None, is_consequential_damage=None, while_defending=None, control_by=None, who_deal_damage=None, at_least_damage=1, more_than_damage=0, not_include_this_effect=None, conditions=[])` |
| When the villain initiates an attack against you | `WhenUnitInitiatesAttackAgainst(ability_type, attacker, against_player, operation, conditions=[])` |
| When an encounter card is revealed | `WhenPlayerRevealCard(ability_type, which_player, which_card, can_be_cancel, operation, *, from_encounter=None, conditions=[])` |
| Begin / end of your turn | `WhenPlayerTurnBegin(ability_type, which_player, operation, *, conditions=[])`, `WhenPlayerTurnEnd(...)` |
| End of a phase | `WhenPhaseEnd(ability_type, phase_name, operation, *, conditions=[])` |
| End of the round | `AfterRoundEnd(ability_type, operation, *, conditions=[])`, `DiscardThisWhenRoundEnd(ability_type, *, conditions=[])` |
| After a status card is placed | `AfterStatusCardPlaceOn(ability_type, place_on_who, status, operation, *, conditions=[])` |
| Obligation « Give to the X player » | `WhenThisObligationGiveToYou(operation)` |

Déclencheurs des cartes de rencontre :

| Texte imprimé | Fabrique |
|---|---|
| When Revealed | `WhenThisRevealed(condition, operation)` ; `condition` = `None`, `"Hero"` ou `"Alter-Ego"` |
| [star] Boost: ... | `WhenCardBecomeBoost(which_card, operation, *, during_scheme=False, during_attack=False, is_undefended_attack=None, attacker=None, activating_enemy=None, you_are_in_hero_from=None, conditions=[])` |
| [star] Boost: If this activation deals damage to ... | `BoostIfThisActivationDealsDamage(to_who, operation)` |
| When X attacks / would attack | `WhenUnitWouldAttack(ability_type, attacker, operation, *, against_player='AnyPlayer', attack_targets=None, is_basic_attack=None, by_effect=None, conditions=[])` |
| When X attacks you | `WhenUnitAttackYou(ability_type, attacker, operation, conditions=[])` |
| When X schemes / would scheme | `WhenUnitWouldScheme(ability_type, who_scheme, operation, *, against_player='AnyPlayer', by_effect=None, conditions=[])` |
| After X schemes | `AfterUnitSchemeEnd(ability_type, which_unit, operation, *, against_player='AnyPlayer', conditions=[])` |
| When Defeated (personnage) | `WhenUnitBeDefeated(AbilityType.WhenDefeated, which_unit, operation, ...)` |
| When X would be defeated (remplacer la défaite) | `WhenUnitWouldBeDefeated(ability_type, which_unit, operation, *, by_consequential_damage=None, conditions=[])` |
| When Defeated (complot) | `WhenSchemeBeDefeated(AbilityType.WhenDefeated, which_scheme, operation, *, has_defeating_player=None, conditions=[])` |
| Setup (face 1A d'un complot principal) | `WhenCardSetup("This", operation)` |
| Setup (carte avec le mot-clé `Setup` dans `desc`, environnement...) | `AfterGameSetup(operation)` (jamais `WhenCardSetup`) |
| Attach to X (attachement de rencontre) | `AttachToFaceWhenPutIntoPlay(target, *, highest_atk=False, ..., conditions=[])` |
| Hero Action: Spend ... → discard this card | `PlayerActionToDiscardThis(ability_type, *, conditions=[], ex_operation=...)` puis `.SetCost(Cost("RRR"))` |
| X cannot take damage | `UnitCannotTakeDamageWhile(ability_type, which_card, *, conditions=[], ...)` |
| Escalade dynamique d'un complot | `WhenCalcThisSchemeEscalation(operation)` |

Jouer une carte qui n'est pas un événement : **le moteur l'ajoute tout
seul**. Une amélioration s'attache par défaut à ton identité, un soutien se
pose chez toi, un allié et une manigance du joueur entrent en jeu. Tu
n'écris la fabrique que pour **changer** ce comportement :

| Carte | Quand l'écrire | Fabrique |
|---|---|---|
| Amélioration | « Attach to a minion / an enemy », « Play under any player's control » | `CanPlayThisUpgradeCard(target=None, conditions=[], replaced_operation=None)` avec `Minion`, `Enemy`, `"Players"`... (exemples 01007, 01009, 05023) |
| Soutien | « Play under any player's control », ou une condition | `CanPlayThisSupportCard(*, under_any_players_control=False, conditions=[])` |
| Manigance du joueur | une condition pour la jouer | `CanPlayThisSchemeCard(*, conditions=[])` (exemple 60024, qui l'écrit sans condition : sans effet, mais sans danger) |
| Allié | jamais | rien |

Bonus continus et compteurs :

| Texte imprimé | Fabrique |
|---|---|
| You get +N (amélioration attachée à toi) | `*GiveKeywordToAttached("You", health=N, attack=..., thwart=..., defense=..., recover=..., hand_size=..., retaliate=..., trait=...)` |
| Attached X gains retaliate / +ATK | `*GiveKeywordToAttached(CardFinder(name="X"), retaliate=1)` |
| Bonus à des cartes en jeu (soutien, allié...) | `*GiveKeywordToInPlayWhenApplyThis(card_finder, *, control_by=None, attack=..., ally_limit=..., ...)` |
| Bonus dynamique sur soi | `ThisGainKeyword(check_fn, *, attack=..., hand_size=..., ..., change_on_event=OnEvent...)` |
| +X pour chaque carte en jeu | `ThisGainKeywordForEachFaceInPlay(for_each_face_in_play, *, attack=..., scheme=..., change_on_event=...)` |
| Attacks gain overkill / piercing / ranged | `UnitAttackGainKeyword(attacker, target=None, *, overkill=False, ranged=False, piercing=False, ...)` |
| Enters play with N counters (sans `Uses`) | `ThisEnterPlayWithCounters(counters, name)` |
| If there are at least N counters here | `IfThereAreAtLeastCounterHere(at_least, counter_name, operation, *, conditions=[])` |
| After a token is placed here | `AfterCardPlacedToken(ability_type, which_card, token_name, operation, *, conditions=[], at_least=None)` |

Ressources :

| Texte imprimé | Fabrique |
|---|---|
| Resource: generate [x] | `CanGenerateResources(ability_type, resources=None, for_card=None, *, resources_fn=None, conditions=[], ...)` ; **une seule par carte** |
| Ressource doublée pour une classe | `DoubleResourcesThisGenerates(for_card)` |
| Réduction de coût | `ReduceCostToPlayThis(update_cost_fn, *, ...)` (voir pièges) |

Choix (« Choose one ») :

| Besoin | Fabrique |
|---|---|
| Une option | `ForChoiceAbility(name, operation=None, *, condition=True)` ; `operation(targets)` |
| Une option qui coûte | `ForChoiceAbilityWithCost(cost, name=None, operation=None, *, conditions=[])` |
| « sinon » | `Otherwise(operation)` |
| Proposer les options | `player.ChooseAbilities(effect, option1, option2, ...)` ; facultatif : `player.MayChooseOneAbility(effect, option)` |

#### 7.4 Méthodes chaînées d'une capacité

```python
(AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, mon_effet)
    .SetName("Nom affiché")          # nom de la capacité (« Spider-Sense »)
    .SetPlay()                        # c'est un événement qui se JOUE
    .SetLabel('attack')               # 'attack' | 'thwart' | 'defense' ; UN SEUL appel (deux libellés : SetLabel('thwart', 'attack'))
    .SetCost(Cost("Y"))               # coût en ressources colorées ("RRR", "YBR", "1" pour une ressource quelconque)
    .SetCostFunc(CostFunc.Exhaust("This"))   # coût non monétaire, cumulable
    .SetTarget(Enemy)                 # cible
    .LimitOncePerRound())             # (Limit once per round.)
```

Autres méthodes réelles : `.SetPlay(hero_form_only=True)` (« Hero form
only »), `.SetPlay(alter_ego_form_only=True)`, `.LimitOncePerPhase()`,
`.AnyPlayerCanDoThis()` (« Any player can do this »).

#### 7.5 Coûts (`CostFunc`)

| Coût imprimé | Code |
|---|---|
| Exhaust this card → | `CostFunc.Exhaust("This")` |
| Exhaust your identity / your hero | `CostFunc.Exhaust("YourIdentity")` |
| Exhaust a [[X]] support you control | `CostFunc.Exhaust(CardFinder(trait="X", card_type=Support))` |
| Remove N counters from this card | `CostFunc.Counter("This", N, "web")` |
| Discard this card | `CostFunc.Discard("This")` |
| Deal N damage to this character | `CostFunc.DealDamage(N, "This")` |
| Return X to your hand | `CostFunc.ReturnToHand(name="X", to_who="Owner")` |
| Spend [x] resources | `.SetCost(Cost("R"))` (pas un CostFunc) |
| Autre | `A_FAIRE_CLAUDE` (Claude utilise `CostFunc.Custom`, piégeux) |

#### 7.6 Cibles (`SetTarget`)

Il y a deux familles de chaînes, à ne pas mélanger.

**Dans `.SetTarget(...)`** (la cible que le joueur choisit), seules ces
chaînes existent : `"This"`, `"YourIdentity"`, `"Players"`, `"Trigger"` (la
carte qui a déclenché), `"Attacker"`, `"Initiator"`, `"YouControlUnit"`,
`"YourHandCards"`, `"TeamUp"` (obligatoire sur un événement Team-Up),
`"Character"`, `"VillainAndEngagedSamePlayerMinion"`.

**Comme « qui » d'une fabrique** (le premier ou le deuxième argument :
`attacker`, `which_card`, `which_player`, `who_take_damage`...), on trouve en
plus : `"You"`, `"AnyPlayer"`, `"AttachedEnemy"`, `"AttachedMinion"`,
`"AttachedVillain"`, ou un `CardFinder(...)`, ou un type (`Villain`,
`Enemy`).

Types : `Enemy`, `Villain`, `Minion`, `Ally`, `Unit2` (tout personnage),
`Friend` (personnage ami), `Scheme2` (tout complot), `MainScheme`,
`SchemeSide2` (complot annexe), `Upgrade`, `Support`, `Event`, `Treachery`,
`Attachment`, `Environment`, `Obligation`.

Paramètres utiles : `range=(1, 2)`, `range="All"`, `range=(1, "All")`,
`canbe_stunned=True`, `canbe_confused=True`, `canbe_tough=True`,
`canbe_ready=True`, `canbe_exhaust=True`, `canbe_heal=True`,
`can_place_threat=True`, `name="X"`, `trait="X"`,
`from_where=["YouControlCards"]`, `from_where=["YourHandCards"]`.

⚠ **Une chaîne de ciblage inventée ne lève aucune erreur** : n'en utilise
aucune qui ne soit pas dans la liste ci-dessus.

⚠ `range=(0, n)` seulement pour un « up to n ». « Stun an enemy » = cible
obligatoire = `SetTarget(Enemy)` sans `range`.

#### 7.7 Chercher des cartes : `CardFinder`

`CardFinder(name="Rhino")`, `CardFinder(name="Rhino", card_type=Villain)`,
`CardFinder(trait="TECH")`, `CardFinder(traits=["AVENGER"], card_type=Ally)`,
`CardFinder(non_trait="ELITE", card_type=Minion)`,
`CardFinder(has_printed_res="B")`, `CardFinder(card_class="Leadership")`.

⚠ **Le nom s'écrit SANS l'étoile d'unicité** : `CardFinder(name="Silver
Samurai")`, jamais `"* Silver Samurai"` (la seconde forme ne trouve jamais
rien, en silence).

#### 7.8 Opérations courantes (toutes vues dans les exemples)

| But | Code |
|---|---|
| Infliger des dégâts | `this.DealDamage(cibles, n, effect)` |
| Subir des dégâts | `cible.TakeDamage(source, n, effect)` |
| Soigner | `this.HealthUnits(cibles, n, effect)` (rend faux si rien n'est soigné) |
| Retirer de la menace | `this.RemoveThreatFromSchemes(cibles, n, effect)` |
| Poser de la menace | `this.PlaceThreatOnSchemes(cibles, n, effect)` ; `n` peut valoir `"1*"` (par joueur) ; cibles : liste, ou `"MainScheme"` |
| Statut | `Faces.GiveStatus(cibles, "Stunned" / "Confused" / "Tough", effect)` |
| Défausser | `Faces.DiscardAll(cartes, effect)` |
| Retirer de la partie | `Faces.RemoveAllFromGame(cartes, effect)` |
| Redresser / incliner | `Faces.ReadyAll(cartes, effect)` / `Faces.ExhaustAll(cartes, effect)` |
| Compteurs | `Faces.PlaceCountersOn([carte], n, 'nom', effect)`, `carte.GetCounters('nom')` |
| Gagner Surge | `this.GainSurge(1, effect)` (raccourci : `ThisCardGainSurge`) |
| Piocher | `player.DrawUp(n, effect)` |
| Défausser au hasard | `player.DiscardRandomHandCards(n, effect)` |
| Le vilain attaque / manigance | `villain.DoAttackYou(player, effect)`, `villain.DoSchemes(player, effect)` |
| Trouver | `Worlds.FindVillain(effect)`, `Worlds.FindCardOnField(effect, name=..., card_type=...)`, `Worlds.FindCardsOnField(effect, trait=..., card_type=...)`, `Worlds.GetOnFieldHeroes(effect)`, `Worlds.GetOnFieldAllies(effect)`, `Worlds.GetOnFieldMinions(effect)`, `Worlds.GetSideSchemes(effect)`, `Worlds.FindMainScheme(this)`, `Worlds.GetFirstPlayer(effect)`, `Worlds.GetPlayers(effect)` |
| Chercher dans le deck rencontre | `Search.EncounterCard(effect, include_discard_pile=True, name=..., card_type=...)`, `Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)` |
| Révéler / mettre en jeu | `face.Reveal(player, effect)`, `face.PutIntoPlay(player, effect)` |
| Bonus temporaire | `unite.GainUntilPhaseEnd(effect, attack=2)` |
| Chaque joueur | `Players.ForEachPlayer(effect, action, valeur_initiale)` |
| Mode expert ? | `Worlds.IsExpert(effect)` |
| Joueur en forme héros ? | `player.IsHero()`, `player.IsAlterEgo()` |

Messages (selon le déclencheur) : `message.GetToPlayer()` (joueur qui révèle
ou qui est visé), `message.GetGaveToPlayer()` (obligation),
`message.PreventDamage("All", effect)`, `message.SetBeInstead(effect)`
(« ... instead »), `message.CancelWhenRevealedEffect(effect)`,
`message.GiveAdditionalBoostCardForThisActivation(1, effect)`,
`message.GainOverKill(effect)`, `message.GainBoostIcon(n, effect)`,
`message.DoSchemeInstead(effect)`, `message.MustDefendWithAlly(effect)`.

### 6.4 Le catalogue d'exemples réels (annexe A, §8) : où trouver la carte modèle

L'annexe A contient **67 exemples réels** : l'entrée JSON et le script de la carte, côte à côte. **Avant d'écrire
une capacité, cherche son équivalent dans cette liste**, puis lis la carte modèle (le `card_id` est donné) dans
le dossier `modeles/` ou dans l'annexe. Index :

- 8.1 Cartes de joueur
  - 8.1.1 Héros : Interruption avec nom de capacité
  - 8.1.2 Alter-ego : Ressource limitée une fois par round
  - 8.1.3 Héros : bonus dynamique sur soi (taille de main)
  - 8.1.4 Alter-ego : Action limitée une fois par round, regarder le deck
  - 8.1.5 Allié : Réponse Forcée après l'avoir joué
  - 8.1.6 Allié : Réponse en entrant en jeu, avec cible
  - 8.1.7 Allié : « Choose one », et défausse en fin de round
  - 8.1.8 Allié : Action avec coût en ressource, limite, choix
  - 8.1.9 Allié : Réponse après avoir attaqué
  - 8.1.10 Allié : Action avec deux coûts cumulés, toutes les cibles
  - 8.1.11 Allié : Interruption payante sur une carte révélée
  - 8.1.12 Événement : Hero Action d'attaque
  - 8.1.13 Événement : Interruption de défense (prévenir les dégâts)
  - 8.1.14 Événement : annuler un « When Revealed »
  - 8.1.15 Événement : Action de soin
  - 8.1.16 Événement : Interruption de contre, effet temporaire
  - 8.1.17 Événement : bonus à tous les personnages d'un joueur
  - 8.1.18 Soutien : Action d'alter-ego avec coût « Exhaust »
  - 8.1.19 Soutien : choisir un joueur
  - 8.1.20 Soutien : ressource calculée
  - 8.1.21 Soutien : bonus continu (limite d'alliés)
  - 8.1.22 Ressource doublée pour une classe
  - 8.1.23 Amélioration attachée à un sbire, Interruption Forcée
  - 8.1.24 Amélioration avec `Uses` et Ressource payée en compteur
  - 8.1.25 Amélioration sur un ennemi, « Hero form only », « instead »
  - 8.1.26 Amélioration : +PV au joueur qui la reçoit
  - 8.1.27 Amélioration : bonus continu ET Action payante
  - 8.1.28 Amélioration : coût en ressource + se défausser
  - 8.1.29 Manigance du joueur, Victory 0, When Defeated
  - 8.1.30 Obligation : retournement facultatif, puis choix
  - 8.1.31 Obligation : choix avec « sinon » (`Otherwise`)
- 8.2 Cartes de rencontre
  - 8.2.1 Vilain étape 1 : capacité [star] permanente (fonction du set)
  - 8.2.2 Vilain étape 2 : When Revealed, chercher et révéler un complot
  - 8.2.3 Vilain étape 3 : When Revealed sur tous les héros (Toughness lu dans `desc`)
  - 8.2.4 Vilain fan-made qui se retourne au lieu d'être vaincu
  - 8.2.5 Complot principal 1A : mise en place
  - 8.2.6 Complot principal 1B : When Revealed
  - 8.2.7 Complot annexe : When Revealed avec menace par joueur (Hazard lu dans `desc`)
  - 8.2.8 Complot annexe avec Acceleration (lu dans `desc`)
  - 8.2.9 Complot annexe avec Crisis seule : aucun script
  - 8.2.10 Complot annexe : Hinder, Victory 0, When Defeated
  - 8.2.11 Sbire avec Guard seule : aucun script
  - 8.2.12 Sbire : When Revealed
  - 8.2.13 Sbire : When Defeated (Patrol et Vulnerable lus dans `desc`)
  - 8.2.14 Sbire avec Surge (lu dans `desc`) et [star] Boost : entrer en jeu
  - 8.2.15 Sbire avec Patrol, [star] Boost conditionnel (si l'activation est une manigance)
  - 8.2.16 Sbire avec Guard et Stalwart, [star] Boost conditionnel (si c'est une attaque)
  - 8.2.17 Sbire : capacité [star] permanente et [star] Boost
  - 8.2.18 Sbire : Forced Response après avoir manigancé, jeton d'accélération
  - 8.2.19 Sbire : « X cannot take damage » (Guard lu dans `desc`)
  - 8.2.20 Sbire : « Choose one » sur la révélation
  - 8.2.21 Traîtrise : gagne Surge si rien n'est soigné
  - 8.2.22 Traîtrise : When Revealed différent en héros et en alter-ego
  - 8.2.23 Traîtrise : choix avec coût en ressources, et [star] Boost
  - 8.2.24 Traîtrise standard : le vilain manigance
  - 8.2.25 Traîtrise du set expert
  - 8.2.26 Attachement : prend les dégâts à la place du vilain, compteurs
  - 8.2.27 Attachement : [star] Interruption Forcée, puis effet différé
  - 8.2.28 Attachement : Hero Action payante pour le défausser
  - 8.2.29 Attachement : donne Retaliate au vilain
  - 8.2.30 Set némésis : complot annexe avec Acceleration, When Revealed et When Defeated
  - 8.2.31 Set némésis : traîtrise avec [star] Boost « si cette activation inflige des dégâts »
  - 8.2.32 Environnement : Alter-Ego Action, coût en inclinaison ciblée, compteurs
  - 8.2.33 Environnement : entre en jeu avec un compteur, Action pour n'importe quel joueur
  - 8.2.34 Environnement : se retourne à N compteurs par joueur
  - 8.2.35 Environnement avec Setup : mise en place, fin de phase, victoire
  - 8.2.36 Attachement fan-made : condition ET coût d'une Hero Action

L'annexe B (`annexes/B-recettes-moteur.md`, ~1 800 lignes) est l'index **mécanique imprimée → fabrique + carte
modèle + piège** : c'est la première chose à ouvrir devant une mécanique inhabituelle (scénario à plusieurs
vilains, vilain qui se retourne, jeton maison, paquet de scénario, icône de complot dynamique…). Les **fiches de
mots-clés** (annexe C, `mots-cles/`) disent, pour chaque mot-clé officiel **ou maison**, ce que le moteur en
fait ; **un mot-clé rencontré sur une carte s'ouvre avant d'écrire une ligne de code** ; absent → tu écris
`A_FAIRE_CLAUDE` et tu poses la question.

### 6.5 Les capacités propres à un scénario : ce qui se pose où

| Ce que le texte dit | Où et comment |
|---|---|
| **Setup** du complot principal (face 1A) : « Setup : … » | `AbilityFactory.WhenCardSetup("This", opération)` sur la **face 1A** du complot principal du scénario. **Ce n'est PAS `AfterGameSetup`**, réservé aux cartes à mot-clé `Setup` dans `desc`. |
| **When Revealed** d'un complot, d'un sbire, d'une traîtrise | `AbilityFactory.WhenThisRevealed(None, opération)` ; `None`, `"Hero"` ou `"Alter-Ego"` pour une condition de forme. |
| **[star] Boost : …** | `AbilityFactory.WhenCardBecomeBoost(...)`. |
| **When Defeated** d'un personnage / d'un complot | `WhenUnitBeDefeated(AbilityType.WhenDefeated, …)` / `WhenSchemeBeDefeated(AbilityType.WhenDefeated, …)`. |
| Une capacité **imprimée sur le vilain** valable pour plusieurs stades | une fonction du `__init__.py` du set, appelée par chaque script de stade (modèle : `core/klaw/__init__.py`). |
| **Branchement du carnet** (la face 1A appelle la campagne) | `return [*CampaignSetup(niveau), …]` : voir §7.3. |
| Mise en jeu d'une carte à la **fin** de mise en place | `RunAt` / `AbilityFactoryCampaign.WhenCampaignSetupAfterMulligans` (§7). |
| Le vilain avance de stade ; le complot avance | gérés par le moteur ; une capacité « Advance » se fait par `Puzzle`/`Scenario` (voir annexe B, « avancée de stade »). |
| **Expert seulement** (« In expert mode… ») | `AbilityFactory.ExpertModeOnly()` / `AbilityFactory.StandardModeOnly()` **portés par la carte** ; ou `Worlds.IsExpert(effect)` dans une condition. **Ne réimplémente jamais le choix de face selon le mode à la mise en place** : la carte s'en charge (voir §14, piège « Public Outcry »). |

### 6.6 Pièges des scripts (annexe A, §9)

<!-- extrait de docs/reference/KIT-CHATGPT-CREATION.md -->
#### 9. Pièges connus

Chacun de ces pièges a déjà cassé une carte du projet, souvent **sans aucune
erreur visible**.

1. **Le nom sans étoile.** `CardFinder(name="* X")` ne trouve jamais rien.
   Écris `name="X"`.
2. **Les mots-clés de `desc` ne se recodent pas** (3.3). Un script qui pose
   Toughness ou Surge en plus les applique deux fois.
3. **Une chaîne de ciblage inventée ne lève rien** : la carte est inerte.
4. **Un filtre va dans `conditions`, jamais en tête de l'opération.** Une
   capacité facultative (Response, Interrupt) est **proposée au joueur** dès
   que son message part ; un `return` en début d'opération ne l'empêche pas
   d'être proposée. Mets la condition dans `conditions=[lambda effect,
   message: ...]` (exemples 01006, 01033).
5. **« You » contre un nom propre.** « You get +1 » = l'identité (les deux
   faces) ; « Angela gets +1 » = la face héros seulement.
6. **`range=(0, n)`** rend la cible facultative : seulement pour « up to n ».
7. **Un seul `SetLabel`** par capacité ; deux libellés dans le même appel.
8. **Une seule `CanGenerateResources` par carte.**
9. **Le Setup d'une carte à mot-clé `Setup`** se code `AfterGameSetup`,
   jamais `WhenCardSetup` (réservé à la face 1A du complot principal).
10. **Une obligation révélée reste en jeu** si le script ne la défausse pas :
    code toutes les branches (défausser ou retirer de la partie).
11. **Les capacités d'une carte dans la pile de victoire ne se déclenchent
    jamais** (la carte est hors jeu). Un effet « tant que X est dans la pile
    de victoire » se pose sur une carte qui reste en jeu : `A_FAIRE_CLAUDE`.
12. **`printed_cost` est un objet, pas un nombre** : `face.printed_cost.val`.
13. **Réduction de coût : signe négatif.** Réduire de 1 = `-1`.
14. **Une recherche dans le deck sort la carte du deck** : l'opération doit
    la mettre quelque part (main, jeu, défausse).
15. **« A or B » sur un coût** = deux capacités, une par coût :
    `A_FAIRE_CLAUDE` si ce sont deux façons de **jouer** la carte (le moteur
    demande une inscription spéciale).
16. **Les dégâts consécutifs d'un allié** sont dans l'astérisque de
    `ATK`/`THW` (`"2*"`), pas dans un script.
17. **Ne code jamais la sortie de jeu d'une carte `Uses`** : le moteur la
    défausse au dernier compteur.
18. **Limite « once per round » sur un déclencheur de défaite**
    (`AfterUnitDefeatedUnit`) : piège moteur connu, signale-le en doute.
19. **Une capacité [star] sans « In expert mode »** est toujours active.
20. **Résultat de fin de partie** : lis `message.players_won`, jamais l'état
    du monde.

### 6.7 Mots-pièges du texte imprimé, à chercher sur **chaque** carte (`PROCESSUS-CARTE.md`, étape 5)

| Mot ou tournure | Piège concret déjà rencontré |
|---|---|
| `each`, `for each` | rendu par erreur « chaque joueur » au lieu de « chaque héros » |
| `against you`, `your` | portée oubliée ou élargie |
| `you control` | la cible peut viser une carte hors du contrôle du joueur, y compris celle du vilain |
| `unless`, `otherwise`, `without` | branche alternative non codée |
| `instead` | « instead » veut dire que la chose **part** d'un endroit et **arrive** ailleurs, pas qu'elle est dupliquée |
| `once per round per player` | à ne pas coder comme une limite globale |
| `if you cannot` | vérifier que le cas testé est réellement atteignable |
| `that <nom>` | vérifier que la cible est bien **la même** carte que celle nommée plus haut |
| `equal number` | vérifier le sens exact du décompte |
| `attacks` / `attacks or engages` / `attacks and damages` | trois déclencheurs différents |
| `and remove` (coût à plusieurs parties) | qu'**aucune** partie ne soit oubliée |
| `defeated` vs `damaged` | ne jamais coder l'un pour l'autre |
| **Response** / **Interrupt** + `After` | le déclencheur est un vrai message du moteur avec fenêtre |
| **Forced Interrupt** vs **Forced Response** | l'un résout **avant** l'événement, l'autre **après** |
| **Hero Response** / **Hero Action** | sous-type dédié, pas le type nu |
| un second Interrupt/Response/mot-clé annoncé | vérifier qu'il a vraiment un module |
| mot-clé cité mais pas imprimé sur **cette** carte | ne pas coder de capacité fantôme |
| icône de ressource | à vérifier contre une carte du **même pack**, jamais à vue |

### 6.8 Ce que tu livres pour **chaque** carte à capacité : le gabarit

Une carte n'est **jamais** « terminée » parce qu'elle est écrite. Elle l'est quand son gabarit est rempli **avec
des preuves réelles**. Tu remplis la partie « statique » (étapes 2, 5, 6) ; Claude remplit les étapes qui
exigent le jeu (7, 8, 8 bis). **Tu laisses les cases non exécutées décochées, avec la mention `à exécuter par
Claude`** : ne coche jamais une preuve que tu n'as pas produite.

```
### <card_id> : <nom de la carte>

- [ ] Étape 2 : carte(s) de référence : <card_id modèle> (<nom>) : comparable parce que ...
- [ ] Étape 5 : texte-contre-code : mots-pièges vérifiés (lister) : ...
      Résultat : ...
- [ ] Étape 6 : nombres texte ↔ code : <chaque nombre imprimé> = desc <...> = script <...>
      Résultat : ...
- [ ] Étape 7 : cas test_capacites par capacité (écrit dans tools/cas/<bloc>.py ; à exécuter par Claude) :
      capacité 1 : cas <nom du cas> ... ; capacité 2 : ...
- [ ] Étape 7 bis : limite imprimée ? OUI / NON. Si OUI : témoin d'épuisement : cas <nom> (deux déclenchements
      dans le même round/phase, chiffre mesuré au second)
- [ ] Étape 8 / 8 bis : à exécuter par Claude (autoplay ; la carte dessine-t-elle quelque chose de nouveau ?)

Carte terminée : NON (à compléter par Claude) / OUI si aucune capacité et rien à prouver.
```

Un **doute de lecture** (§1.3) s'écrit dans `QUESTIONS.md` **avant** le script ; le script prend alors la lecture
**recommandée**, repérée par un commentaire `# QUESTION <n> :` pour que Claude retrouve le point.

### 6.9 Auto-relecture d'une carte (annexe A, §11)

<!-- extrait de docs/reference/KIT-CHATGPT-CREATION.md -->
#### 11. Checklist d'auto-relecture avant livraison

Pour chaque carte :

- [ ] `card_id` unique, bon préfixe, bon suffixe de face.
- [ ] `name` : `"* "` si et seulement si la carte est unique.
- [ ] Toutes les valeurs de `desc` sont des **chaînes**.
- [ ] `"*"` de « par joueur » sur `HP` / menaces quand la carte l'imprime ;
      `"*"` de dégâts consécutifs sur `ATK` / `THW` d'un allié.
- [ ] Chaque mot-clé imprimé est dans `desc` (3.3), **et absent** du script.
- [ ] `RES` vérifiée par comparaison, pas à vue.
- [ ] `set_name` cohérent avec le dossier du script (2.1).
- [ ] Le texte imprimé est recopié avec ses balises (3.5).
- [ ] Chaque capacité imprimée a SA fabrique, du BON type
      (Forced / facultatif, Hero / Alter-Ego).
- [ ] Chaque « (Limit once per round.) » a son `.LimitOncePerRound()`.
- [ ] Chaque nombre du texte se retrouve dans le code, et réciproquement.
- [ ] Aucune fonction, aucune chaîne de ciblage absente de ce document.
- [ ] Aucun `CardFinder(name="* ...")`.
- [ ] Les filtres des capacités facultatives sont dans `conditions`.
- [ ] Chaque branche d'une obligation défausse ou retire la carte.
- [ ] Les doutes sont listés.

Pour un scénario et une campagne :

- [ ] Chaque carte de `encounters` / des sets existe dans tes blocs de cartes,
      avec le bon nombre d'exemplaires.
- [ ] Fichier standard ET fichier `_expert` (étapes de vilain décalées, set
      `expert` ajouté).
- [ ] Chaque clé du carnet est écrite ET lue.
- [ ] La face 1A de chaque complot porte `*CampaignSetup(n)` avec le bon `n`.


---

## 7. La logique de campagne côté moteur : le carnet, `campaign.py`, `CampaignSetup`

C'est le chapitre le plus important pour qu'une campagne **soit réellement une campagne**. Une récompense qui
est notée au carnet mais que personne ne relit à la mise en place suivante **disparaît en silence** : c'est
arrivé à deux récompenses de Sinister Motives, à huit récompenses d'autres boîtes (audit du 19/09/2026) et à
l'allié « Captive » de Mutant Genesis (les quatre captifs se retrouvaient dans la main de départ).

### 7.1 Le carnet : le format exact

* Un **dictionnaire `str → str`**. Toutes les valeurs sont des **chaînes**.
* Une **case cochée** : `"1"`. Une **case non cochée** : la clé est **absente** (jamais `"0"` : le moteur teste
  `!= ''`, et `"0"` est non vide). **Exception** : les réglages `options_campagne` de type `case` écrivent `"0"`
  quand le joueur clique « Non » : pour ces clés, ton script teste `== "1"` (ou `entier > 0`), jamais `!= ''`.
* Un **nombre** : sa représentation décimale en texte (`"3"`).
* Une **liste** : les éléments séparés par `;` (`"21181;21183"`). Vide = clé absente.
* Une clé **par joueur** : `Player N <clé>` (N de 1 à 4 : `Player 1 Role`, `Player 2 Tech Upgrade`). Le moteur
  accepte aussi la forme `<clé> P<N>`. Le panneau écrit toujours la première.
* Une clé **d'état à valeurs fixes** : un texte parmi une liste (`In play`, `In the victory display`,
  `Removed from campaign`) — voir Skrull Menace.
* Une clé **« pool »** : `Campaign Pool: <Nom>` = `"1"` quand la récompense `<Nom>` est acquise (convention de
  Mad Titan's Shadow, reprise par plusieurs boîtes).

**Lecture dans le code** (module `game/operate/campaign_logs.py`, classe `CampaignLog`, déjà importée par
`from . import *`) :

| Fonction | Rend |
|---|---|
| `CampaignLog.GetStrInternal(cle, effect)` | la chaîne, `''` si absente |
| `CampaignLog.GetIntInternal(cle, effect)` | un entier, `0` si absente (lève `ValueError` si la valeur n'est pas un nombre) |
| `CampaignLog.GetListInternal(cle, effect)` | une liste (valeur coupée sur `;`), `[]` si absente |
| `CampaignLog.GetStrByPlayer(cle, player_id, effect)` | la valeur du joueur (`player_id` **de 0 à 3**) |
| `CampaignLog.GetListByPlayer(cle, player_id, effect)` | la liste du joueur |
| `CampaignLog.GetIntByPlayer(cle, player_id, effect)` | l'entier du joueur |
| `CampaignLog.GetStr` / `GetInt` / `GetList` | idem, mais **typées** pour les clés historiques de The Rise of Red Skull et Sinister Motives (les `Literal` du fichier) : à l'exécution elles acceptent toute clé, mais pour une clé neuve **utilise les variantes `…Internal`** |
| `CampaignLog.SetStr(cle, valeur, world)` | **écrit** au carnet du monde (utilisé pour débiter une dépense de mise en place, ou noter une preuve en cours de partie) |

**Écriture** : le carnet est écrit à **la fin de la partie** par le collecteur (§7.5) ; il peut aussi l'être
pendant la partie par `CampaignLog.SetStr` (Agents of S.H.I.E.L.D. note une preuve gagnée en cours de partie ;
Hunting Season débite l'expérience dépensée à la mise en place). Tout ce qui est dans le store du monde est
recopié au carnet sortant.

**Le fichier réel :**
*Fichier `Fusion/marvel-lcg-src/src/game/operate/campaign_logs.py` (copie exacte, lue dans le depot au moment de la construction).*

```python
from typing import TypeAlias
from . import *

PLAYER_LIST_KEY: TypeAlias = Literal[
    "Obligations",
    "Rescued Allies",
    "Aspect Advantage: Reputation Track Reward",
]

PLAYER_STR_KEY: TypeAlias = Literal[
    "Tech Upgrade",
    "Basic Upgrade",
    "S.H.I.E.L.D. Tech: Reputation Track Reward",
    "Planning Ahead: Reputation Track Reward",
]

PLAYER_INT_KEY: TypeAlias = Literal[
    "Remaining hit points",
]

LOG_LIST_KEY: TypeAlias = Literal[
    "Experimental Weapons added to encounter deck",
    "Players engaged with minions",
    "Allies removed from the campaign",
    "Community Service: Victory for Scenarios #1-4",
    "Osborn Tech: Reputation Track Penalty",
    "Last Ones Standing: Victory for Scenario #4 - The Sinister Six",
]

LOG_INT_KEY: TypeAlias = Literal[
    "Number of delay counters on main scheme",
    "Reputation Track",
    "Waking Nightmare: Victory for Scenario #3 - Mysterio",
]

LOG_STR_KEY: TypeAlias = Literal[
    ""
]

class CampaignLog:

    @staticmethod
    def GetStrInternal(key: str, by_effect: 'Effect') -> str:
        if Stores.HasKey(key, by_effect):
            return Stores.GetStr(key, by_effect)
        else:
            return ""

    @staticmethod
    def GetIntInternal(key: str, by_effect: 'Effect') -> int:
        value = CampaignLog.GetStrInternal(key, by_effect)
        if value:
            return int(value)
        return 0

    @staticmethod
    def GetListInternal(key: str, by_effect: 'Effect') -> List[str]:
        value = CampaignLog.GetStrInternal(key, by_effect)
        if value:
            return value.split(";")
        else:
            return []

    ################################################################################
    #
    @staticmethod
    def GetStr(key: LOG_STR_KEY, by_effect: 'Effect') -> str:
        return CampaignLog.GetStrInternal(key, by_effect)

    @staticmethod
    def GetInt(key: LOG_INT_KEY, by_effect: 'Effect') -> int:
        return CampaignLog.GetIntInternal(key, by_effect)

    @staticmethod
    def GetList(key: LOG_LIST_KEY, by_effect: 'Effect') -> List[str]:
        return CampaignLog.GetListInternal(key, by_effect)

    ################################################################################
    #
    @staticmethod
    def GetStrByPlayer(key: PLAYER_STR_KEY, player_id: Literal[0, 1, 2, 3], by_effect: 'Effect') -> str:
        player_keys = [f"Player {player_id+1} {key}", f"{key} P{player_id+1}"]
        for player_key in player_keys:
            value = CampaignLog.GetStrInternal(player_key, by_effect)
            if value:
                return value
        return ""

    @staticmethod
    def GetListByPlayer(key: PLAYER_LIST_KEY, player_id: Literal[0, 1, 2, 3], by_effect: 'Effect') -> List[str]:
        player_keys = [f"Player {player_id+1} {key}", f"{key} P{player_id+1}"]
        for player_key in player_keys:
            value = CampaignLog.GetListInternal(player_key, by_effect)
            if value:
                return value
        return []

    @staticmethod
    def GetIntByPlayer(key: PLAYER_INT_KEY, player_id: Literal[0, 1, 2, 3], by_effect: 'Effect') -> int:
        player_keys = [f"Player {player_id+1} {key}", f"{key} P{player_id+1}"]
        for player_key in player_keys:
            value = CampaignLog.GetIntInternal(player_key, by_effect)
            if value:
                return value
        return 0

    @staticmethod
    def SetStr(key: str, value: str, world: 'World'):
        world.store.SetStr(key, value)

```

### 7.2 Où le carnet entre dans une partie, et à quel moment

1. L'écran de campagne lance la partie avec `campaign_log = carnet de la campagne` (§2.3, étape 4).
2. À la construction du monde (`World.__init__`), chaque entrée est copiée dans le **store du monde** (`CampaignLog.SetStr`, `game/world/world.py`).
3. À la mise en place, **étape 13 « Campaign Setup »**, le moteur émet `Message.WhenCampaignSetup`. Toutes les
   capacités de type `AbilityType.Campaign` écoutent ce message. **Une capacité ne l'écoute que si la carte qui
   la porte existe dans la partie** : d'où le branchement sur la face 1A du complot principal (§7.3).
4. **Étape 15 bis** : `Message.WhenCampaignSetupAfterMulligans`, pour ce qui doit se résoudre **après** les
   mulligans (les preuves d'Agents of S.H.I.E.L.D. cherchent une carte dans le deck et l'ajoutent à la main : avant
   la pioche, elles feraient piocher une carte de moins ; avant le mulligan, le mulligan pourrait la défausser).
5. À la fin de la partie, `Message.WhenGameOver` : le collecteur écrit le carnet **sortant** (§7.5).

Ordre complet de la mise en place (extrait de `World.Initialize`) :
*Extrait de `Fusion/marvel-lcg-src/src/game/world/world.py` (de « # [x] 11. Put Setup Cards » a « # [x] 16. Resolve Character »).*

```python
        # [x] 11. Put Setup Cards Into Play
        # A card with the setup keyword begins the game in play.
        decks = [x.player_deck for x in self.const_players] + \
                [x.set_aside_nemesis_sets for x in self.const_players] + \
                [self.GetScenario().encounter_deck] + \
                ([second_encounter_deck] if second_encounter_deck else []) + \
                self.additional_decks
        faces = [x for y in decks for x in y.GetAll() if HasSetup.IsType(x) and x.printed_setup > 0]
        faces +=self.CartesSetupOptionnelles(campaign, message.encounter_set_names)
        for face in faces:
            face.ProcessSetup(game_start_effect)

        if self.is_game_over:
            return

        # [x] 12. Resolve Scenario Setup and When Revealed abilities
        self.phase.SetState(Phase.State.ScenarioSetup)
        for scheme in Worlds.GetAllMainSchemes(self):
            # Deja montree avant l'etape 11 ; sans effet si elle l'a ete. Une
            # principale arrivee depuis passe ici avant ses capacites (12a).
            if self.rule.confirm_scheme_setup_order:
                self.ConfirmMainSchemeReveal(scheme)
            scheme.Setup(False)
            scheme.Advance(None, game_start_effect) # Has already reveal here

        for villain in Worlds.GetAllVillains(self):
            villain.Setup(False)
            villain.Reveal(None, game_start_effect)

        # Evidence
        faces = [x for y in decks for x in y.GetAll() if Evidence.IsType(x)]
        for face in faces:
            face.Setup(False)

        if self.is_game_over:
            return

        # [x] 13. Campaign Setup
        campaign_message = Message.WhenCampaignSetup(self)
        campaign_message.Send()

        # [x] 14. Draw Cards
        Message.TextRender("\n--- Draw Cards ---", self)
        if not self.rule.disable_setup_draw_cards:
            for player in self.const_players:
                player.DrawUp("Max", game_start_effect)

        # [x] 15. Resolve Mulligans
        self.phase.SetState(Phase.State.ResolveMulligans)
        Message.TextRender("\n--- Resolve Mulligans ---", self)
        if not self.rule.disable_resolve_mulligans:
            def process_player(player: 'Player'):
                player.phase.ResolveMulligans(Message.WhenPlayerResolveMulligans(player))
            JobManager.Simultaneous(process_player, self.const_players)

        if self.rule.additional_resolve_mulligans:
            def process_player(player: 'Player'):
                player.phase.ResolveMulligans(Message.WhenPlayerResolveMulligans(player))
            JobManager.Simultaneous(process_player, self.const_players)

        # [x] 15 bis. Campaign Setup, la part qui attend la fin des mulligans
        # Les encarts des scenarios 2 a 5 d'Agents of S.H.I.E.L.D. le disent
        # mot pour mot : « After resolving mulligans, resolve the "Setup"
        # ability of each evidence card the players have earned ». C'est le
        # seul endroit ou une carte peut chercher dans le deck et l'ajouter a
        # une main deja piochee et deja mulliganee.
        campaign_message = Message.WhenCampaignSetupAfterMulligans(self)
        campaign_message.Send()

        if self.is_game_over:
            return
```

### 7.3 Brancher le carnet : `CampaignSetup(niveau)` sur la face 1A du complot principal

**Le mécanisme.** Les capacités de campagne d'un pack ne se déclenchent que si la **face 1A du complot principal**
du scénario appelle `CampaignSetup(niveau)` dans son `GetAbilities()` et en dépose le résultat dans la liste
retournée. **Sans cet appel, `Message.WhenCampaignSetup` n'a aucun auditeur et le carnet est ignoré, en silence.**

Le `niveau` est **le numéro du scénario dans la campagne**, de 1 à N (le `numero` de la description de campagne).

**Cas simple** (le complot n'avait aucune autre capacité) — `src/cards/pack/mts/ebony_maw/21074a.py` :
*Fichier `Fusion/marvel-lcg-src/src/cards/pack/mts/ebony_maw/21074a.py` (copie exacte, lue dans le depot au moment de la construction).*

```python
from . import *
from cards.pack.mts.campaign import CampaignSetup
def GetAbilities() -> Sequence['Ability']:
    return [*CampaignSetup(1)]
```

**Cas d'un complot qui a déjà ses capacités** : on **ajoute l'import** et on **préfixe** la liste retournée —
`src/cards/pack/mts/the_tower_defense/21098a.py` :
*Fichier `Fusion/marvel-lcg-src/src/cards/pack/mts/the_tower_defense/21098a.py` (copie exacte, lue dans le depot au moment de la construction).*

```python
from . import *
from cards.pack.mts.campaign import CampaignSetup

# Under Siege

def GetAbilities() -> Sequence['Ability']:

    def under_siege_game_start(effect: 'Effect', message: 'Message.WhenGameBeginSetup') -> None:
        first_player = Worlds.GetFirstPlayer(effect)

        villains = Worlds.GetScenario(effect).villain_deck.FindCards(name="Proxima Midnight", card_type=Villain)
        villain = sorted(villains, key=lambda face: face.printed_stage)[0]
        villain.PutIntoPlay(first_player, effect)

        villains = Worlds.GetScenario(effect).villain_deck.FindCards(name="Corvus Glaive", card_type=Villain)
        villain = sorted(villains, key=lambda face: face.printed_stage)[0]
        villain.PutIntoPlay(first_player, effect)

        message.skip_put_villain_into_play = True

    def under_siege(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)

        first_player = Worlds.GetFirstPlayer(effect)

        scheme = Worlds.MainSchemesDeck(effect).Get()[0]
        assert scheme
        scheme.Reveal(first_player, effect)


    return [
        *CampaignSetup(2),
        AbilityFactory.WhenGameBeginSetup(
            under_siege_game_start
        ),
        AbilityFactory.WhenCardSetup(
            "This",
            under_siege
        ),
    ]

```

**Cas d'une campagne maison (Web of Deceit), où la fonction de campagne s'appelle autrement** —
`src/cards/pack/web_of_deceit/shocker/wd002a.py` :
*Fichier `Fusion/marvel-lcg-src/src/cards/pack/web_of_deceit/shocker/wd002a.py` (copie exacte, lue dans le depot au moment de la construction).*

```python
from . import *
from cards.pack.web_of_deceit.campaign import ChaqueJoueurRetrouveSesTalents

# Shock Party (1A)

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        # « Setup: Search the encounter deck for The Long Night side scheme and
        # reveal it. Remove each obligation card in the encounter deck from the
        # game. »
        ChercherEtReveler(effect, name="The Long Night")

        obligations = CardFinder(card_type=Obligation).Checks(
            Worlds.GetEncounterDeckCards(effect))
        if obligations:
            Faces.RemoveAllFromGame(obligations, effect)

        # Regle commune a TOUS les scenarios de la campagne (livret p.3) :
        # « Put the "Vote for Fisk" environment into play. » La face experte est
        # une carte a part, pas un dos : c'est ici qu'on choisit.
        MettreVoteForFiskEnJeu(effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place
        ),
        # Les paliers d'arbre de talents deja gagnes reviennent dans le
        # deck de leur proprietaire (voir `campaign.py`).
        ChaqueJoueurRetrouveSesTalents(),
    ]
```

Règles à respecter, toutes mesurées :

1. **Un appel par scénario**, sur **la face 1A** (la face `a` du **premier** complot de `schemes`). Pas sur 1B, pas
   sur un stade suivant : la 1A est la face mise en jeu au départ, et c'est là que **tous** les modèles posent
   l'appel (une capacité de campagne ne part que si la carte qui la porte existe dans la partie).
2. L'import se fait depuis **`cards.pack.<pack>.campaign`** (le module `campaign.py` du pack), même quand le
   fichier de la carte est dans un sous-dossier.
3. **Le scénario 1 n'a pas toujours besoin de l'appel.** Dans The Rise of Red Skull, le scénario 1 (`crossbones`)
   n'appelle pas `CampaignSetup` : le carnet est vide, toutes les branches de `CampaignSetup` sont gardées par
   `if level >= 2`, et il n'y a pas de collecteur à poser. **Mais** si ton `CampaignSetup` pose le **collecteur**
   (`WriteCampaignLogAtGameOver`), l'appel au niveau 1 est **obligatoire** : sans lui, le carnet sortant du
   scénario 1 n'est jamais écrit et le scénario 2 n'a rien à lire (cas de NeXt Evolution).
4. **Le niveau doit être le bon.** Un niveau faux applique les récompenses d'un autre scénario, **sans erreur**.
   `verifier-livraison-campagne.py` compare, pour chaque scénario, le niveau appelé par sa 1A au `numero` de la
   description de campagne.
5. Le même `CampaignSetup(niveau)` sert en **standard et en expert** : la branche expert se déclare à
   l'intérieur (`WhenCampaignSetupExpertOnly`, `Worlds.IsExpert`).
6. **Ne réimplémente jamais le choix d'une face selon le mode** (standard/expert) dans la mise en place : une
   carte « Standard Mode Only » / « Expert Mode Only » se retourne **toute seule** à son entrée en jeu
   (`AbilityFactory.StandardModeOnly()` / `AbilityFactory.ExpertModeOnly()`, portés par la carte). C'est une erreur de
   lecture qui a déjà coûté une demi-journée (Public Outcry de Sinister Motives).

### 7.4 Les fabriques de campagne (`AbilityFactoryCampaign`) — le fichier réel

C'est **toute** la surface moteur dédiée aux campagnes. Tu n'en utilises **que** ces fonctions pour poser une
capacité de campagne ; tout le reste est du code Python ordinaire qui appelle les opérations du §6.

*Fichier `Fusion/marvel-lcg-src/src/game/ability/factory/campaign.py` (copie exacte, lue dans le depot au moment de la construction).*

```python
from . import *

class AbilityFactoryCampaign:

    @staticmethod
    def WhenCampaignSetup(operation: OperationType[Message.WhenCampaignSetup],
                        *,
                        conditions: ConditionsType[Message.WhenCampaignSetup]=[],
                        ) -> 'Ability':
        from game.operate.worlds import Worlds
        return Ability(
            AbilityType.Campaign,
            Message.WhenCampaignSetup,
            [
                lambda effect, message:
                    Worlds.IsCampaign(effect),
                *conditions
            ],
            operation
        )

    @staticmethod
    def WhenCampaignSetupAfterMulligans(operation: OperationType[Message.WhenCampaignSetupAfterMulligans],
                                        *,
                                        conditions: ConditionsType[Message.WhenCampaignSetupAfterMulligans]=[],
                                        ) -> 'Ability':
        """Etape 15 bis : ce que le livret place APRES les mulligans.

        Voir `Message.WhenCampaignSetupAfterMulligans` pour le pourquoi.
        """
        from game.operate.worlds import Worlds
        return Ability(
            AbilityType.Campaign,
            Message.WhenCampaignSetupAfterMulligans,
            [
                lambda effect, message:
                    Worlds.IsCampaign(effect),
                *conditions
            ],
            operation
        )

    @staticmethod
    def WhenCampaignSetupExpertOnly(operation: OperationType[Message.WhenCampaignSetup],
                                    *,
                                    conditions: ConditionsType[Message.WhenCampaignSetup]=[],
                                    ) -> 'Ability':
        from game.operate.worlds import Worlds
        return AbilityFactoryCampaign.WhenCampaignSetup(
            operation,
            conditions=[
                lambda effect, message:
                    Worlds.IsExpert(effect),
                *conditions
            ],
        )

    @staticmethod
    def ExpertCampaignSetPlayersHPToTheirRemainingHP() -> 'Ability':
        from game.operate.worlds import Worlds
        from game.operate.campaign_logs import CampaignLog
        def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
            for player in Worlds.GetPlayers(effect):
                player_id = player.player_id
                value = CampaignLog.GetIntByPlayer("Remaining hit points", player_id, effect)
                if value:
                    player.GetIdentity().SetHealth(value, effect)

        return AbilityFactoryCampaign.WhenCampaignSetupExpertOnly(
            action,
        )

    @staticmethod
    def PutCardIntoPlay(card_id: str, under_control: Literal["FirstPlayer"]|None=None) -> 'Ability':
        from game.card.factory import CardFactory
        def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
            card = CardFactory.GenerateCard(card_id, None, effect.world)
            face = card.face
            face.PutIntoPlay("FirstPlayer", effect, under_control=under_control != None)
        return AbilityFactoryCampaign.WhenCampaignSetup(action)

    @staticmethod
    def ShuffleCardIntoDeck(card_id: str, deck: Literal["EncounterDeck"]) -> 'Ability':
        from game.card.factory import CardFactory
        from game.operate.faces import Faces
        def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
            card = CardFactory.GenerateCard(card_id, None, effect.world)
            Faces.ShuffleAllTo([card.face], deck, effect)
        return AbilityFactoryCampaign.WhenCampaignSetup(action)

    @staticmethod
    def ChooseCardAtRandomAndShuffleIntoEncounterDeck(card_ids: List[str]) -> 'Ability':
        from game.card.factory import CardFactory
        from engine.lib import Random
        from game.operate.campaign_logs import CampaignLog
        from game.operate.faces import Faces
        def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
            checked_ids = CampaignLog.GetList("Community Service: Victory for Scenarios #1-4", effect)
            card_id = Random.RandomChoice([x for x in card_ids if x not in checked_ids])
            card = CardFactory.GenerateCard(card_id, None, effect.world)
            Faces.ShuffleAllTo([card.face], "EncounterDeck", effect)
        return AbilityFactoryCampaign.WhenCampaignSetup(action)

    @staticmethod
    def ExpertCampaignEachPlayerMayDealFacedownEncounterCardYpHealHP(size: int) -> 'Ability':
        from game.operate.worlds import Worlds
        from game.ability.factory import AbilityFactory
        def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
            this = effect.this

            for player in Worlds.GetPlayers(effect):
                def action(targets: Sequence['CardFace']):
                    player.DealEncounterCards(size, effect)
                    this.HealthUnits(targets, "All", effect)

                player.MayChooseOneAbility(
                    effect,
                    AbilityFactory.ForChoiceAbility(
                        f"may deal themself {size} facedown encounter card from the encounter deck to set their hit point dial to their identity's printed hit point value",
                        action,
                    ).SetTarget([player.GetIdentity()], canbe_heal=True)
                )

        return AbilityFactoryCampaign.WhenCampaignSetupExpertOnly(
            action,
        )

    @staticmethod
    def ExpertCampaignAddRandomObligationFromExpertCampaignToHealHP(obligations: Sequence[str]) -> 'Ability':
        from game.operate.worlds import Worlds
        from game.operate.campaign_logs import CampaignLog
        from game.card.factory import CardFactory
        from game.ability.factory import AbilityFactory
        from engine.lib import Random
        def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
            this = effect.this

            rest_obligations: Dict[Player, List[str]] = {}

            for player in Worlds.GetPlayers(effect):
                player_id = player.player_id
                card_ids = CampaignLog.GetListByPlayer("Obligations", player_id, effect)
                rest_obligations[player] = [x for x in obligations if x not in card_ids]
                if card_ids:
                    CardFactory.GenerateCards(card_ids, player.player_deck, effect.world)
                    player.player_deck.Shuffle(effect)

            for player in Worlds.GetPlayers(effect):
                def action(targets: Sequence['CardFace']):
                    card_id = Random.RandomChoice(rest_obligations[player])
                    CardFactory.GenerateCard(card_id, player.player_deck, effect.world)
                    this.HealthUnits(targets, "All", effect)
                    player.player_deck.Shuffle(effect)

                player.MayChooseOneAbility(
                    effect,
                    AbilityFactory.ForChoiceAbility(
                        "Add 1 random obligation from expert campaign set to their deck to heal their identity to its full hit point value",
                        action,
                        condition=rest_obligations[player] != []
                    ).SetTarget([player.GetIdentity()], canbe_heal=True)
                )

        return AbilityFactoryCampaign.WhenCampaignSetupExpertOnly(
            action,
        )

```

En résumé :

| Fabrique | Quand elle part |
|---|---|
| `WhenCampaignSetup(operation, conditions=[])` | étape 13, **à chaque campagne** (standard et expert) |
| `WhenCampaignSetupExpertOnly(operation, conditions=[])` | étape 13, **campagne experte seulement** |
| `WhenCampaignSetupAfterMulligans(operation, conditions=[])` | étape 15 bis, après les mulligans |
| `ExpertCampaignSetPlayersHPToTheirRemainingHP()` | expert : remet les PV de chaque joueur à `Player N Remaining hit points` |
| `PutCardIntoPlay(card_id, under_control)` | met une carte en jeu à la mise en place |
| `ShuffleCardIntoDeck(card_id, "EncounterDeck")` | mélange une carte dans le deck de rencontre |
| `ChooseCardAtRandomAndShuffleIntoEncounterDeck(card_ids)` | tire une carte au hasard parmi celles non encore au carnet |
| `ExpertCampaignEachPlayerMayDealFacedownEncounterCardYpHealHP(n)` | expert : soin contre une carte rencontre face cachée |
| `ExpertCampaignAddRandomObligationFromExpertCampaignToHealHP(obligations)` | expert : soin contre une obligation aléatoire du set expert |

La **signature d'une opération** est toujours `def action(effect: 'Effect', message: 'Message.WhenCampaignSetup')`.
Une opération peut : générer une carte (`CardFactory.GenerateCard(id, deck_ou_None, effect.world)`), la mettre en
jeu (`card.face.PutIntoPlay('FirstPlayer', effect, under_control=…)`), la mélanger
(`Faces.ShuffleAllTo([face], 'EncounterDeck' | deck_du_joueur, effect)`), l'attacher
(`face.CastTo(Upgrade).AttachTo2(identite, effect)`), infliger des dégâts, défausser le dessus d'un deck, retirer
une carte de la partie (`Faces.RemoveAllFromGame`), poser des jetons (`PlaceTokensInternal`), ou poser une
question à un joueur (`player.MayChooseOneAbility`, `AskChooseOneText`).

### 7.5 Le carnet sortant : `WriteCampaignLogAtGameOver`

**Ce que c'est.** Une capacité (`AbilityType.Campaign`, message `WhenGameOver`) que **ton `CampaignSetup`
ajoute à sa liste** (dernière ligne : `abilities.append(WriteCampaignLogAtGameOver(lambda effect, message:
CollectXXX(level, effect)))`). À la fin de **chaque** partie de campagne (victoire comme défaite), elle écrit
`.game/campaign_log_last.json` :

```json
{ "players_won": true, "scenario": "ebony_maw", "suggestions": { "Campaign Pool: Cosmo": "1", "Player 1 Remaining hit points": "7", "Player 1 Identity": "Spider-Man" } }
```

* `suggestions` = **tout ce qui est dans le store du monde** (le carnet entrant + tout ce qui y a été écrit
  pendant la partie) **moins** les clés secrètes, **plus** `Player N Remaining hit points` et `Player N Identity`
  (ajoutés automatiquement), **plus** ce que renvoie ta fonction `collect_fn`.
* `collect_fn(effect, message)` renvoie un `dict` de mises à jour : `{clé: valeur}` ajoute/remplace, `{clé: None}`
  **retire** la clé.
* **Le résultat de la partie se lit dans `message.players_won`, JAMAIS dans l'état du monde** : le message est
  émis *avant* que `world.game_over` soit posé, un collecteur qui lit le monde voit toujours « perdue ». (c'est ainsi que Fear No
  Evil ne cochait jamais l'affaire à la victoire, trouvé le 19/09/2026 par `tools/test_campagnes.py`.)
* `scenario` (l'**estampille**) : le panneau **ignore en bloc** les suggestions dont l'estampille diffère de
  l'`id` du scénario joué. Par défaut l'estampille est le `set_name` du **premier complot principal** (`schemes[0]`), en minuscules, espaces
  remplacés par des soulignés, **tout caractère hors `[a-z0-9_]` supprimé** (`'Ebony Maw'` → `ebony_maw`,
  `'Stop the Presses!'` → `stop_the_presses`). **Elle doit être égale à l'`id` du scénario dans
  `data/campagnes/<code>.json`.** Quand `set_name` ne suffit pas (`gmw` : `collector_1` pour le scénario
  `infiltrate_the_museum` ; Hunting Season : `hs_vermin`), passe-la explicitement :
  `WriteCampaignLogAtGameOver(collect, scenario_id='hs_vermin')`.
* **Où est la fonction ?** Dans `cards/pack/mts/campaign.py` (partagée par toutes les boîtes). Un autre pack
  l'importe : `from cards.pack.mts.campaign import WriteCampaignLogAtGameOver, ActiveMainSchemeStartswith`.
* Le collecteur est **facultatif**. Les boîtes **sans** collecteur (`trors`, `sm`, `web_of_deceit`) laissent le
  panneau déduire les valeurs par des **détecteurs** déclarés dans `data/campagnes/<code>.json` (§8.4) ou faire
  saisir le joueur. **Préfère un collecteur** dès que la récompense se lit dans l'état de fin de partie : c'est
  plus fidèle et testable (`FIN_DE_PARTIE=1` à la sonde).

**Exemple complet : le collecteur de Mad Titan's Shadow** (tout `campaign.py` est plus bas, §7.6) :
*Extrait de `Fusion/marvel-lcg-src/src/cards/pack/mts/campaign.py` (de « def CollectMTS » a « def CampaignSetup »).*

```python
def CollectMTS(level: int, effect: 'Effect') -> dict:
    updates = {}
    if (level == 1):
        if FaceExists(effect, '21180b', in_play=True):
            updates['Campaign Pool: Cosmo'] = '1'
        if ActiveMainSchemeStartswith(effect, '21075'):
            updates['Campaign Pool: Security Breach'] = '1'
    if (level == 2):
        if FaceExists(effect, '21182b'):
            updates['Campaign Pool: Shawarma'] = '1'
            if not FaceExists(effect, '21182b', in_victory=True):
                updates['Campaign Pool: Black Swan'] = '1'
        if FaceExists(effect, '21100b', in_play=True):
            updates['Avengers Tower Damaged'] = '1'
    if (level == 3):
        if not FaceExists(effect, '21184b', in_victory=True):
            updates['Campaign Pool: System Shock'] = '1'
        if ActiveMainSchemeStartswith(effect, '21115'):
            updates['The Infinity Stones 1B completed'] = '1'
    if (level == 4):
        if FaceExists(effect, '21186b'):
            updates['Campaign Pool: Norn Stone'] = '1'
        if FaceExists(effect, '21186b', in_victory=True):
            updates['Campaign Pool: Odin'] = '1'
    return updates
```

### 7.6 Un `campaign.py` complet, officiel : The Mad Titan's Shadow

C'est le **modèle de départ** recommandé : un collecteur, des `CampaignSetup` par niveau, des fonctions
d'application du carnet. Lis-le en entier ; les noms de ses fonctions (`InPool`, `LogSet`,
`PutIntoPlayIfPool`…) sont des briques réutilisables (importe-les depuis `cards.pack.mts.campaign`).

*Fichier `Fusion/marvel-lcg-src/src/cards/pack/mts/campaign.py` (copie exacte, lue dans le depot au moment de la construction).*

```python
from . import *
import re
def InPool(name: str):
    def check(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> bool:
        return (CampaignLog.GetStrInternal(f'Campaign Pool: {name}', effect) != '')
    return check
def LogSet(name: str):
    def check(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> bool:
        return (CampaignLog.GetStrInternal(name, effect) != '')
    return check
def PutSideSchemeIntoPlay(card_id: str) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        card = CardFactory.GenerateCard(card_id, None, effect.world)
        card.face.PutIntoPlay('FirstPlayer', effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def PutIntoPlayIfPool(card_id: str, pool_name: str, *, under_control: bool = False) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        card = CardFactory.GenerateCard(card_id, None, effect.world)
        card.face.PutIntoPlay('FirstPlayer', effect, under_control=under_control)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[InPool(pool_name)])
def ShuffleIntoEncounterIfPool(card_id: str, pool_name: str) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        card = CardFactory.GenerateCard(card_id, None, effect.world)
        Faces.ShuffleAllTo([card.face], 'EncounterDeck', effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[InPool(pool_name)])
def EachPlayerShufflesCopyIfPool(card_id: str, pool_name: str) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            card = CardFactory.GenerateCard(card_id, player.player_deck, effect.world)
            Faces.ShuffleAllTo([card.face], player.player_deck, effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[InPool(pool_name)])
def EachPlayerNornStoneIfPool() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            card = CardFactory.GenerateCard('21187a,21187b', None, effect.world)
            card.SetOwner(player)
            card.face.CastTo(Upgrade).AttachTo2(player.GetIdentity(), effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[InPool('Norn Stone')])
def AvengersTowerDamagedPenalty() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            identity = player.GetIdentity()
            identity.CastTo(Unit2).TakeDamage(effect.this, 3, effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[LogSet('Avengers Tower Damaged')])
def InfinityStonesCompletedPenalty() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            half = (player.player_deck.GetSize() // 2)
            if (half > 0):
                Faces.DiscardAll(player.player_deck.GetTops(half), effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[LogSet('The Infinity Stones 1B completed')])
def ExpertMayPlaceAccelerationToHeal() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        this = effect.this.CastTo(MainScheme)
        for player in Worlds.GetPlayers(effect):
            identity = player.GetIdentity()
            def heal(targets: Sequence['CardFace']):
                this.PlaceTokensInternal(1, 'acceleration_token', effect)
                identity.CastTo(CanHealth).HealHealth('All', effect)
            player.MayChooseOneAbility(effect, AbilityFactory.ForChoiceAbility('Place 1 acceleration token on the main scheme to heal to full', heal))
    return AbilityFactoryCampaign.WhenCampaignSetupExpertOnly(action)
def FaceExists(effect: 'Effect', card_id: str, *, in_play: 'bool|None' = None, in_victory: 'bool|None' = None) -> bool:
    world = effect.world
    victory = world.victory_display.Get()
    for card in world.object_manager.card_dict.values():
        face = card.face
        if (face == None) or (face.paper.card_id != card_id):
            continue
        if (in_victory != None):
            if ((face in victory) != in_victory):
                continue
        if (in_play != None):
            if (face.IsInPlay() != in_play):
                continue
        return True
    return False
def ActiveMainSchemeStartswith(effect: 'Effect', prefix: str) -> bool:
    return any(s.paper.card_id.startswith(prefix) for s in Worlds.GetAllMainSchemes(effect.world))
# Cles du carnet que le SERVEUR injecte et que le joueur ne doit jamais lire.
# `server_new_game.py` remet la combinaison de la taupe d'Agents of S.H.I.E.L.D.
# dans le carnet juste avant `NewGame` : elle se retrouve donc dans le store du
# monde comme n'importe quelle autre cle. Sans ce filtre elle ressortait deux
# fois — au fichier sortant, que l'ecran relit et propose au joueur, et au
# journal de partie rendu plus bas — ce qui revenait a ouvrir l'enveloppe
# A.I.M. devant lui.
# Les deux cles d'aos qui ne doivent JAMAIS sortir au carnet : la combinaison de la
# taupe, et le compte des preuves gagnees hors campagne (une cle de travail, voir
# `cards/pack/aos/campaign.py`). Ecrites en litteral ici pour ne pas importer aos
# depuis mts, qui n'en sait rien par ailleurs.
CLES_SECRETES = ('A.I.M. Envelope', 'A.I.M. Envelope Gained')


def WriteCampaignLogAtGameOver(collect_fn, scenario_id: 'str|None'=None) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenGameOver'):
        import json
        world = effect.world
        out = {k: v for k, v in world.store.dic.items()
               if isinstance(v, str) and k not in CLES_SECRETES}
        for player in Worlds.GetPlayers(effect):
            identity = player.GetIdentity()
            hp = (identity.health if identity else 0)
            out[f'Player {(player.player_id + 1)} Remaining hit points'] = str(max(0, hp))
            # player.GetHero() leve une AssertionError (pas None) des que le
            # joueur est cote Alter Ego, ce qui est l'etat normal en fin de
            # partie. On lit donc la face heros via GetHeroFace(), qui la
            # retrouve quelle que soit la forme active du joueur ; elle aussi
            # leve si la carte n'a vraiment aucune face heros, d'ou le garde.
            # Une identite illisible ne doit couter que sa propre cle, pas
            # faire perdre le reste du carnet.
            if identity:
                try:
                    hero_face = identity.GetHeroFace()
                except AssertionError:
                    hero_face = None
                if hero_face:
                    out[f'Player {(player.player_id + 1)} Identity'] = hero_face.paper.name.lstrip('* ')
        # ⚠ LE RESULTAT DE LA PARTIE N'EST PAS ENCORE POSE SUR LE MONDE.
        # `GameOver.SetGameOver` envoie ce message PUIS affecte
        # `self.players_won` (game_over.py:85-90) : un collecteur qui lisait
        # `world.game_over` pendant le message voyait donc TOUJOURS « perdue ».
        # Fear No Evil, qui ne coche l'affaire qu'a la victoire, n'inscrivait
        # jamais rien — trouve le 19/09/2026 par `tools/test_campagnes.py`, la
        # premiere gate a jouer la FIN d'une partie. Le collecteur recoit donc
        # le message, seul porteur de la verite a cet instant.
        updates = collect_fn(effect, message)
        for key, value in updates.items():
            if (value == None):
                out.pop(key, None)
            else:
                out[key] = value
        # Estampille du scenario : sans elle, ce carnet reste au fichier apres
        # la fin de partie et une AUTRE boite, jouee plus tard sur la meme
        # place, le lirait comme sien (voir preremplissage.ts, qui compare
        # cette valeur au scenario du contexte de campagne avant d'utiliser
        # quoi que ce soit d'ici). Derivee du set_name de la manigance
        # principale active, deja la facon etablie d'identifier « quel
        # scenario » dans ce fichier (voir ActiveMainSchemeStartswith
        # ci-dessus) : 'Ebony Maw' -> 'ebony_maw', ce qui correspond
        # exactement a l'id de scenario dans data/campagnes/mts.json.
        # ⚠ `scenario_id` PASSE PAR LA BOITE QUAND LE set_name NE SUFFIT PAS
        # (signalement n°50, 04/10/2026). Le set_name de la manigance principale
        # n'est l'id du scenario que pour les boites ou ils coincident ;
        # `gmw` ecrit « collector_1 » et « collector_2 » pour les scenarios
        # `infiltrate_the_museum` et `escape_the_museum`. Le panneau de
        # recompenses ignore alors tout le releve du moteur (estampille
        # differente) et les unites gagnees ne parviennent jamais au Marche.
        stamp = scenario_id
        schemes = Worlds.GetAllMainSchemes(effect.world)
        if stamp is None and schemes:
            set_name = schemes[0].paper.set_name
            if set_name:
                # CORRECTIF (18/09/2026, Fear No Evil) : « Stop the Presses! »
                # donnait « stop_the_presses! », qui ne correspond a aucun id
                # de scenario. On ne garde que [a-z0-9_].
                stamp = re.sub(r'[^a-z0-9_]', '', set_name.lower().replace(' ', '_'))
        try:
            from engine.config import ConfigVariables
            chemin = ConfigVariables.File('campaign_log_last_file', './campaign_log_last.json').value
            # Tout-ou-rien : une lecture concurrente de /get_carnet_suggere
            # tombait sur du JSON tronque, la route avalait l'erreur et rendait
            # un carnet VIDE. Pour mts, dont aucune cle n'a de detecteur de
            # secours, la recompense etait perdue sans un mot.
            from engine.ecriture_atomique import ecrire_json
            ecrire_json(chemin, {'players_won': message.players_won,
                                 'scenario': stamp, 'suggestions': out})
        except OSError:
            pass
        Message.TextRender('\n--- Campaign Log (suggestions) ---', world)
        for key in sorted(out):
            Message.TextRender(f'{key} = {out[key]}', world)
    return Ability(AbilityType.Campaign, Message.WhenGameOver, [lambda e, m: Worlds.IsCampaign(e)], action)
def CollectMTS(level: int, effect: 'Effect') -> dict:
    updates = {}
    if (level == 1):
        if FaceExists(effect, '21180b', in_play=True):
            updates['Campaign Pool: Cosmo'] = '1'
        if ActiveMainSchemeStartswith(effect, '21075'):
            updates['Campaign Pool: Security Breach'] = '1'
    if (level == 2):
        if FaceExists(effect, '21182b'):
            updates['Campaign Pool: Shawarma'] = '1'
            if not FaceExists(effect, '21182b', in_victory=True):
                updates['Campaign Pool: Black Swan'] = '1'
        if FaceExists(effect, '21100b', in_play=True):
            updates['Avengers Tower Damaged'] = '1'
    if (level == 3):
        if not FaceExists(effect, '21184b', in_victory=True):
            updates['Campaign Pool: System Shock'] = '1'
        if ActiveMainSchemeStartswith(effect, '21115'):
            updates['The Infinity Stones 1B completed'] = '1'
    if (level == 4):
        if FaceExists(effect, '21186b'):
            updates['Campaign Pool: Norn Stone'] = '1'
        if FaceExists(effect, '21186b', in_victory=True):
            updates['Campaign Pool: Odin'] = '1'
    return updates
def CampaignSetup(level: int) -> List['Ability']:
    abilities = []
    if (level == 1):
        abilities.append(PutSideSchemeIntoPlay('21180a'))
        def shuffle_breach(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
            card = CardFactory.GenerateCard('21181', None, effect.world)
            Faces.ShuffleAllTo([card.face], 'EncounterDeck', effect)
        abilities.append(AbilityFactoryCampaign.WhenCampaignSetup(shuffle_breach))
    if (level == 2):
        abilities.append(PutSideSchemeIntoPlay('21182a'))
        abilities.append(ShuffleIntoEncounterIfPool('21181', 'Security Breach'))
    if (level == 3):
        abilities.append(PutSideSchemeIntoPlay('21184a'))
        abilities.append(PutIntoPlayIfPool('21180b', 'Cosmo', under_control=True))
        abilities.append(ShuffleIntoEncounterIfPool('21181', 'Security Breach'))
        abilities.append(EachPlayerShufflesCopyIfPool('21183', 'Shawarma'))
        abilities.append(PutIntoPlayIfPool('21182b', 'Black Swan'))
        abilities.append(AvengersTowerDamagedPenalty())
    if (level == 4):
        abilities.append(PutSideSchemeIntoPlay('21186a'))
        abilities.append(AbilityFactoryCampaign.ShuffleCardIntoDeck('21188', 'EncounterDeck'))
        abilities.append(EachPlayerShufflesCopyIfPool('21183', 'Shawarma'))
        abilities.append(EachPlayerShufflesCopyIfPool('21185', 'System Shock'))
        abilities.append(InfinityStonesCompletedPenalty())
    if (level == 5):
        abilities.append(PutSideSchemeIntoPlay('21189a'))
        abilities.append(AbilityFactoryCampaign.ShuffleCardIntoDeck('21188', 'EncounterDeck'))
        abilities.append(EachPlayerShufflesCopyIfPool('21183', 'Shawarma'))
        abilities.append(EachPlayerShufflesCopyIfPool('21185', 'System Shock'))
        abilities.append(InfinityStonesCompletedPenalty())
        abilities.append(EachPlayerNornStoneIfPool())
        abilities.append(PutIntoPlayIfPool('21139b,21139a', 'Odin', under_control=True))
    if (level >= 2):
        abilities.append(AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP())
        abilities.append(ExpertMayPlaceAccelerationToHeal())
    abilities.append(WriteCampaignLogAtGameOver(lambda effect, message: CollectMTS(level, effect)))
    return abilities
```

### 7.7 Deux autres modèles complets : le style « niveau croissant » et une campagne maison

**The Rise of Red Skull** : pas de collecteur ; `CampaignSetup(level, campaigns=[...], campaigns_expert=[...])`
accepte des fonctions propres au scénario (utilisées par `red_skull/04128a.py`) :

*Fichier `Fusion/marvel-lcg-src/src/cards/pack/trors/campaign.py` (copie exacte, lue dans le depot au moment de la construction).*

```python
from . import *

def ShuffleEachExperimentalAttachmentIntoTheEncounterDeck() -> 'Ability':
    from game.operate.worlds import Worlds
    from game.operate.campaign_logs import CampaignLog
    from game.card.factory import CardFactory
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        card_ids = CampaignLog.GetList("Experimental Weapons added to encounter deck", effect)
        encounter_deck = Worlds.GetEncounterDeck(effect)
        CardFactory.GenerateCards(card_ids, encounter_deck, effect.world)
        encounter_deck.Shuffle(effect)

    return AbilityFactoryCampaign.WhenCampaignSetup(
        action,
    )

def EachPlayerSearchTheirDeckForSetupKeyword() -> 'Ability':
    from game.operate.worlds import Worlds
    from game.operate.campaign_logs import CampaignLog
    from game.card.factory import CardFactory
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            player_id = player.player_id
            card_id = CampaignLog.GetStrByPlayer("Tech Upgrade", player_id, effect)
            if card_id:
                card = CardFactory.GenerateCard(card_id, player.player_deck, effect.world)
                card.face.PutIntoPlay(player, effect)

        for player in Worlds.GetPlayers(effect):
            player_id = player.player_id
            card_id = CampaignLog.GetStrByPlayer("Basic Upgrade", player_id, effect)
            if card_id:
                card = CardFactory.GenerateCard(card_id, player.player_deck, effect.world)
                card.face.PutIntoPlay(player, effect)

    return AbilityFactoryCampaign.WhenCampaignSetup(
        action,
    )

def EachPlayerAddRescuedAlliesToTheirDeck() -> 'Ability':
    from game.operate.worlds import Worlds
    from game.operate.campaign_logs import CampaignLog
    from game.card.factory import CardFactory
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            player_id = player.player_id
            card_ids = CampaignLog.GetListByPlayer("Rescued Allies", player_id, effect)
            if card_ids:
                CardFactory.GenerateCards(card_ids, player.player_deck, effect.world)
                player.player_deck.Shuffle(effect)

    return AbilityFactoryCampaign.WhenCampaignSetup(
        action,
    )

def EachPlayerMayAddRandomObligationToHealHP() -> 'Ability':
    return AbilityFactoryCampaign.ExpertCampaignAddRandomObligationFromExpertCampaignToHealHP(
        ["04163", "04164", "04165", "04166"]
    )


def CampaignSetup(level: int, *,
                campaigns: List[Callable[[Effect, Message.WhenCampaignSetup], None]]=[],
                campaigns_expert: List[Callable[[Effect, Message.WhenCampaignSetup], None]]=[]) -> List['Ability']:

    abilities: List[Ability] = []

    if level >= 2:
        abilities.append(
            EachPlayerSearchTheirDeckForSetupKeyword(),
        )
        abilities.append(
            ShuffleEachExperimentalAttachmentIntoTheEncounterDeck(),
        )

    if level >= 4:
        abilities.append(
            EachPlayerAddRescuedAlliesToTheirDeck(),
        )

    for campaign in campaigns:
        abilities.append(
            AbilityFactoryCampaign.WhenCampaignSetup(campaign),
        )

    if level >= 2:
        abilities.append(
            AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP(),
        )
        abilities.append(
            EachPlayerMayAddRandomObligationToHealHP()
        )

    for campaign in campaigns_expert:
        abilities.append(
            AbilityFactoryCampaign.WhenCampaignSetupExpertOnly(campaign),
        )

    return abilities

```

**Web of Deceit** (campagne maison, arbres de talents) : **aucun collecteur** ; les gains sont **choisis par le
joueur** dans le panneau (champs `type: "choix"`) et le moteur les **remet dans le deck de chaque joueur** à
chaque mise en place :

*Fichier `Fusion/marvel-lcg-src/src/cards/pack/web_of_deceit/campaign.py` (copie exacte, lue dans le depot au moment de la construction).*

```python
from . import *

# LE CARNET DE LA CAMPAGNE « WEB OF DECEIT »
#
# La voie a ete tranchee au §15 de la fiche : les arbres de talents passent par
# le carnet, qui sait deja poser des cartes IMPOSEES dans le deck d'un joueur
# entre deux scenarios. Un palier d'arbre est exactement cela — « ces cartes
# restent avec le joueur pour le reste de la campagne et DOIVENT figurer dans
# son deck » (livret p.2).
#
# ⚠ CE QUE CETTE VOIE NE REND PAS : l'arbre ne s'affiche pas comme un arbre. Le
# joueur voit, entre deux rencontres, la liste des cartes de son palier — les
# cinq arbres melanges, puisque le carnet ne retient pas lequel il a choisi.
# La progression est fidele, sa mise en scene ne l'est pas.

PALIERS = ("Talent Tier 0", "Talent Tier 1", "Talent Tier 2",
           "Talent Tier 3", "Talent Tier 4")


def ChaqueJoueurRetrouveSesTalents() -> 'Ability':
    """Remet dans le deck de chaque joueur les cartes de talent deja gagnees.

    Le carnet enregistre un choix par palier et par joueur (`parJoueur`), sous
    les cles listees ci-dessus. A chaque mise en place de campagne, on les relit
    et on genere les cartes dans le deck de leur proprietaire : le deck grossit
    d'une carte par scenario gagne, ce que le livret demande.
    """
    from game.operate.worlds import Worlds
    from game.operate.campaign_logs import CampaignLog
    from game.card.factory import CardFactory

    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        for player in Worlds.GetPlayers(effect):
            gagnees = []
            for cle in PALIERS:
                card_id = CampaignLog.GetStrByPlayer(cle, player.player_id, effect)
                if card_id:
                    gagnees.append(card_id)
            if gagnees:
                CardFactory.GenerateCards(gagnees, player.player_deck, effect.world)
                player.player_deck.Shuffle(effect)

    return AbilityFactoryCampaign.WhenCampaignSetup(
        action,
    )
```

### 7.8 La bibliothèque de motifs : ce que les douze campagnes savent déjà faire

Chaque ligne = une fonction de `campaign.py` qui **existe, est testée** (`tools/epreuves_campagnes.py`), et que tu
peux imiter. Les fichiers entiers sont dans `modeles/D-patrons-de-campaign-py/` du zip.

| Besoin | Fonction modèle | Fichier |
|---|---|---|
| Une carte entre en jeu **si** une récompense est au carnet | `PutIntoPlayIfPool` | `mts/campaign.py` |
| Une carte est mélangée au **deck de rencontre** si… | `ShuffleIntoEncounterIfPool`, `ShuffleEachExperimentalAttachmentIntoTheEncounterDeck` | `mts`, `trors` |
| **Chaque joueur** mélange une copie d'une carte dans **son** deck | `EachPlayerShufflesCopyIfPool` | `mts` |
| Une carte est **attachée** à l'identité de chaque joueur | `EachPlayerNornStoneIfPool` | `mts` |
| Une **pénalité** de mise en place (dégâts, moitié du deck défaussée) | `AvengersTowerDamagedPenalty`, `InfinityStonesCompletedPenalty` | `mts` |
| Expert : un pion Accélération contre un soin complet | `ExpertMayPlaceAccelerationToHeal` | `mts` |
| Remettre dans **le deck de chaque joueur** les cartes qu'il a gagnées (liste par joueur) | `EachPlayerAddRescuedAlliesToTheirDeck`, `ChaqueJoueurRetrouveSesTalents`, `CartesAjoutees` | `trors`, `web_of_deceit`, `hunting_season` |
| Rôle / amélioration différente selon un **rôle** choisi en jeu | `EachPlayerRoleUpgrade`, `PutRoleUpgradeIntoPlay` | `mut_gen` |
| **Alliés captifs** libérés : le joueur choisit dans quel deck (ou aucun) | `ShuffleCaptiveAlliesIntoDeck` | `mut_gen` |
| Environnements « gagnés » qui entrent en jeu au scénario suivant | `PutEarnedEnvironmentsIntoPlay` | `next_evol` |
| Mission tirée parmi plusieurs, jamais deux fois | `SetupMissionAndOverseer` | `aoa` |
| **Solde** de points/unités et **marché** | `Experience`, `PoserExperience`, `GainsDExperience` ; `EachPlayerMarketCardsIntoDeck` | `hunting_season` ; `gmw` |
| **Enquête** à secret côté serveur | `PoserLeConseil`, `PreuveEnJeu`, `NoterPreuveGagnee` | `aos` |
| **Zone** partagée entre scénarios, tableau de progression, tirage d'« Élites » | `_cartes_de_la_zone`, `AssignerLaProgression`, `_elites` | `skrull_menace` |
| Carnet **par affaire** en ordre libre, retrait de cartes du deck | `MettreLesEnvironnements`, `RetirerLesCartesRetirees` | `fne` |
| Compteur de **menace reporté** (pions retard) | `the_rise_of_the_red_skull_place_threat` | `trors/red_skull/04128a.py` |
| **PV persistants** en expert | `AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP` | moteur |

### 7.9 Règles d'écriture des clés du carnet

1. **Copie le vocabulaire du livret** pour nommer une clé (`Allies removed from the campaign`, `Hunter Mode`) :
   l'écran et les rapports s'y retrouvent.
2. **Une clé = une signification, un format.** Ne réutilise pas une clé pour deux choses.
3. **Une clé écrite doit être lue, une clé lue doit être écrite.** Dresse la table (§7.10) et vérifie-la.
4. **Les clés « par joueur »** se lisent par `…ByPlayer` ou par `f'Player {player.player_id + 1} {cle}'` (jamais
   en dur).
5. **Un identifiant de carte** noté au carnet est un `card_id` complet (`'wd113'`), pas un nom : le nom change de
   langue, pas l'identifiant.
6. **Jamais de caractère `;` dans une valeur** de liste (c'est le séparateur) ; jamais de chaîne vide : retire la
   clé.
7. **Les clés secrètes** (que le joueur ne doit jamais lire, comme la combinaison de la taupe d'Agents of
   S.H.I.E.L.D.) se gardent **côté serveur** : demande-le à Claude (`BESOINS-MOTEUR.md`).

### 7.10 La table des clés du carnet — **livrable obligatoire** (`CARNET-CLES.md`)

Tu livres, pour **chaque** clé du carnet de ta campagne, une ligne :

| Clé | Format | Par joueur ? | Écrite par (fichier : fonction) | Lue par (fichier : fonction) | Déclarée dans la description de campagne (scénario, `type`, `detection`) | Source du livret (page) |
|---|---|---|---|---|---|---|
| `Campaign Pool: Cosmo` | drapeau `"1"` | non | `mts/campaign.py : CollectMTS` (niveau 1) | `mts/campaign.py : CampaignSetup` (niveau 3, `PutIntoPlayIfPool`) | `mts.json`, scénario `ebony_maw`, `auto`, `int` | « Campaign Log », p.12 |

Une ligne sans « lue par » est une **récompense qui disparaît en silence**. Une ligne sans « déclarée dans la
description » est une clé que **le panneau ne reportera jamais** (il ne garde que les clés déclarées).

### 7.11 Pièges propres à la logique de campagne (tous payés)

* **`player.GetHero()` lève une `AssertionError` (au lieu de rendre `None`) dès que le joueur est en forme Alter
  Ego** — ce qui est l'état normal en fin de partie. Pour le nom du héros : `identity.GetHeroFace()` (avec garde).
  Cette assertion avait coupé en silence toute écriture du carnet des quatre boîtes câblées.
* **`Faces.ShuffleAllTo` ne mélange que s'il a déplacé quelque chose.** Une carte générée **directement dans**
  `player_deck` ne « bouge » pas : le mélange ne part pas et la carte reste **sur le dessus**. Génère la carte
  **hors deck** (`CardFactory.GenerateCard(id, None, world)`), puis `ShuffleAllTo`.
* **« May » / « any player »** : « Each CAPTIVE ally recorded in the campaign log **may** be shuffled into **any**
  player's deck » = le joueur **choisit** (y compris « aucun ») ; ne mélange jamais d'office dans le deck du
  joueur 1.
* **L'état « fin de partie » n'est pas posé quand le collecteur tourne** (voir §7.5) : `message.players_won`.
* **Un carnet partiellement d'un autre scénario est pire qu'un carnet vide** : c'est pourquoi l'estampille compte.
* **Un livret en retard sur le carnet officiel** : le `campaign.py` dit ce que le moteur **fait**, le carnet
  imprimé dit ce que le livret **demande** ; **seul le second fait autorité**. Lis le carnet imprimé **avant**
  d'écrire la définition (cas de Mutant Genesis : deux lignes d'alliés dans le carnet officiel, une seule
  collectée au départ).
* **Un deck qui doit contenir une carte** : si le livret fait **chercher** une carte **dans le deck** du joueur
  (« Planning Ahead »), le joueur peut avoir retiré la carte entre deux scénarios ; la récompense disparaît alors
  en silence. Déclare le champ avec `"deck": "requis"` (§8.3) : l'écran refusera un deck qui ne la contient plus.
* **La carte de récompense n'est pas écrite dans le deck enregistré** : elle vit **au carnet** et le moteur la
  **génère** à chaque mise en place (`CardFactory.GenerateCard(id, player.player_deck, world)`). C'est ce qui rend
  possible « hors limite min/max du deck ».
* **Chaque capacité de campagne doit être idempotente vis-à-vis d'une défaite** : une défaite n'écrit rien au
  carnet, le scénario se rejoue avec **le même** carnet entrant.


---

## 8. La description de la campagne : `data/campagnes/<code>.json`

C'est le fichier que **lisent l'écran des campagnes et le panneau de récompenses**. Il ne contient **aucune
logique** : il *déclare* (l'ordre des scénarios, les textes, les champs du carnet à reporter, les pages du
livret). La logique est dans `campaign.py` (§7). Le fichier est servi par `/get_campagne_definition?<code>` ;
`<code>` doit être **le nom du fichier sans `.json`**, **le `code` du fichier**, et **le dossier
`public/stories/<code>/`**.

### 8.1 Un exemple complet : The Mad Titan's Shadow (officielle)

Chaque scénario porte ses récompenses (`victoire`), ses pages de livret (`pages`), un résumé et un enjeu en
français. Les champs `auto` (relevés par le collecteur de `mts/campaign.py`) ne portent **ni `detection` ni
`options`** : les valeurs viennent du moteur.

*Fichier `Fusion/marvel-lcg-src/data/campagnes/mts.json` (copie exacte, lue dans le depot au moment de la construction).*

```json
{
  "version": "1.0",
  "code": "mts",
  "cle_extension": "21. The Mad Titan's Shadow",
  "nom": "L'Ombre du Titan Fou",
  "nom_en": "The Mad Titan's Shadow",
  "resume": "Thanos cherche les Pierres d'Infinité, et chaque victoire vous laisse un allié, une dette ou une cicatrice que le scénario suivant vous réclamera.",
  "resume_en": "Thanos hunts the Infinity Stones, and every victory leaves behind an ally, a debt or a scar the next scenario will come to collect.",
  "expert": {
    "pv_persistants": true
  },
  "scenarios": [
    {
      "id": "ebony_maw",
      "numero": 1,
      "nom": "Ebony Maw",
      "nom_fr": "Ebony Maw",
      "resume": "L'émissaire de Thanos s'infiltre dans la Tour des Vengeurs et y retourne vos propres défenses. Rien n'explose, rien ne hurle : il se contente de parler, et les portes s'ouvrent.",
      "enjeu": "Ce que Maw laisse derrière lui vous suit. Une brèche de sécurité non refermée reviendra hanter le deck de rencontre du scénario suivant ; Cosmo, s'il est encore là, se battra à vos côtés.",
      "victoire": [
        {
          "cle": "Campaign Pool: Cosmo",
          "type": "auto",
          "format": "int",
          "libelle": "Cosmo rallié",
          "aide": "Cosmo entre en jeu sous votre contrôle au scénario 3 s'il est noté ici."
        },
        {
          "cle": "Campaign Pool: Security Breach",
          "type": "auto",
          "format": "int",
          "libelle": "Brèche de sécurité laissée ouverte",
          "aide": "La carte Security Breach sera mélangée au deck de rencontre des scénarios suivants."
        }
      ],
      "pages": {
        "intro": [
          "01-ebony_maw-intro-1.jpg"
        ],
        "regles": [
          "01-ebony_maw-regles-1.jpg",
          "01-ebony_maw-regles-2.jpg"
        ],
        "epilogue": [
          "01-ebony_maw-epilogue-1.jpg"
        ]
      }
    },
    {
      "id": "the_tower_defense",
      "numero": 2,
      "nom": "Tower Defense",
      "nom_fr": "La Défense de la Tour",
      "resume": "Proxima Midnight et Corvus Glaive attaquent la Tour ensemble. Deux vilains, un seul bâtiment, et personne pour vous relever.",
      "enjeu": "La Tour peut sortir debout ou éventrée de cette nuit. Ce qu'elle perd ici, aucun scénario suivant ne le lui rendra.",
      "victoire": [
        {
          "cle": "Campaign Pool: Shawarma",
          "type": "auto",
          "format": "int",
          "libelle": "Shawarma partagé",
          "aide": "Chaque joueur mélangera une copie de Shawarma dans son deck aux scénarios suivants."
        },
        {
          "cle": "Campaign Pool: Black Swan",
          "type": "auto",
          "format": "int",
          "libelle": "Black Swan en fuite",
          "aide": "Non vaincue, elle revient en jeu au scénario 3."
        },
        {
          "cle": "Avengers Tower Damaged",
          "type": "auto",
          "format": "int",
          "libelle": "Tour des Vengeurs endommagée",
          "aide": "Pénalité appliquée à la mise en place des scénarios suivants."
        }
      ],
      "pages": {
        "intro": [
          "02-the_tower_defense-intro-1.jpg"
        ],
        "regles": [
          "02-the_tower_defense-regles-1.jpg",
          "02-the_tower_defense-regles-2.jpg",
          "02-the_tower_defense-regles-3.jpg",
          "02-the_tower_defense-regles-4.jpg"
        ],
        "epilogue": [
          "02-the_tower_defense-epilogue-1.jpg"
        ]
      }
    },
    {
      "id": "thanos",
      "numero": 3,
      "nom": "Thanos",
      "nom_fr": "Thanos",
      "resume": "Le Titan descend lui-même. Il ne vient pas gagner, il vient prendre, et il a déjà compté combien de temps cela lui prendrait.",
      "enjeu": "Ce que Thanos emporte des Pierres d'Infinité décide de la puissance qu'il aura contre Hela, puis contre Loki.",
      "victoire": [
        {
          "cle": "Campaign Pool: System Shock",
          "type": "auto",
          "format": "int",
          "libelle": "Choc systémique subi",
          "aide": "Chaque joueur mélangera une copie de System Shock dans son deck aux scénarios suivants."
        },
        {
          "cle": "The Infinity Stones 1B completed",
          "type": "auto",
          "format": "int",
          "libelle": "Les Pierres d'Infinité rassemblées par Thanos",
          "aide": "Pénalité appliquée à la mise en place des scénarios 4 et 5."
        }
      ],
      "pages": {
        "intro": [
          "03-thanos-intro-1.jpg"
        ],
        "regles": [
          "03-thanos-regles-1.jpg",
          "03-thanos-regles-2.jpg"
        ],
        "epilogue": [
          "03-thanos-epilogue-1.jpg"
        ]
      }
    },
    {
      "id": "hela",
      "numero": 4,
      "nom": "Hela",
      "nom_fr": "Hela",
      "resume": "Le royaume des morts n'est plus un lieu de passage. Hela y retient Odin, et Garm garde la porte que vous devrez franchir dans les deux sens.",
      "enjeu": "Odin délivré vous suivra jusqu'à Asgard. Laissé derrière, il n'y sera pas.",
      "victoire": [
        {
          "cle": "Campaign Pool: Norn Stone",
          "type": "auto",
          "format": "int",
          "libelle": "Pierre de Norn récupérée",
          "aide": "Chaque joueur en reçoit une copie au scénario 5."
        },
        {
          "cle": "Campaign Pool: Odin",
          "type": "auto",
          "format": "int",
          "libelle": "Odin délivré",
          "aide": "Odin entre en jeu sous votre contrôle au scénario 5 s'il est noté ici."
        }
      ],
      "pages": {
        "intro": [
          "04-hela-intro-1.jpg"
        ],
        "regles": [
          "04-hela-regles-1.jpg",
          "04-hela-regles-2.jpg"
        ],
        "epilogue": [
          "04-hela-epilogue-1.jpg"
        ]
      }
    },
    {
      "id": "loki",
      "numero": 5,
      "nom": "Loki",
      "nom_fr": "Loki",
      "resume": "Loki règne sur Asgard et rien de ce que vous voyez n'est sûr d'exister. La campagne se termine ici, avec tout ce que vous y avez traîné.",
      "enjeu": "Rien à reporter : c'est le dernier scénario.",
      "final": true,
      "defaite": {"quand": "partie_perdue", "expert_seulement": true, "texte": "Loki étend son règne sur tout l'univers : la campagne est perdue."},
      "victoire": [],
      "pages": {
        "intro": [
          "05-loki-intro-1.jpg"
        ],
        "regles": [
          "05-loki-regles-1.jpg",
          "05-loki-regles-2.jpg"
        ],
        "epilogue": [
          "05-loki-epilogue-1.jpg"
        ]
      }
    }
  ],
  "victoire_commune_expert": [
    {
      "cle": "Remaining hit points",
      "parJoueur": true,
      "type": "auto",
      "format": "int",
      "detection": "pv_restants",
      "libelle": "Points de vie restants",
      "aide": "En campagne experte, vous reprenez le scénario suivant avec ces points de vie."
    }
  ],
  "pages_regles": [
    "00-campagne-regles-1.jpg"
  ]
}
```

### 8.2 Un exemple complet : Web of Deceit (maison, sans collecteur, avec des choix)

Ici les gains sont des **choix du joueur** (`type: "choix"`, `obligatoire: true`) parmi des cartes (`options`) :

*Fichier `Fusion/marvel-lcg-src/data/campagnes/web_of_deceit.json` (copie exacte, lue dans le depot au moment de la construction).*

```json
{
    "version": "1.0",
    "code": "web_of_deceit",
    "cle_extension": "120. Custom (Web of Deceit)",
    "nom": "La Toile du Mensonge",
    "nom_en": "Web of Deceit",
    "resume": "Cinq rencontres au service d'un seul homme : le Caïd. Entre chacune, votre héros descend un ARBRE DE TALENTS — cinq voies au choix, dix cartes chacune, une par palier.",
    "resume_en": "Five encounters serving one man: the Kingpin. Between each, your hero walks down a TALENT TREE — five paths, ten cards each, one per tier.",
    "pages_regles": [],
    "scenarios": [
        {
            "id": "wd_shocker",
            "numero": 1,
            "nom": "Shocker",
            "nom_fr": "Shocker",
            "resume": "Le Tireur cambriole la ville pendant la nuit la plus longue de sa carrière. Il ne meurt jamais vraiment : le vaincre le renvoie dans la mêlée, et la seule façon d'en finir est de survivre jusqu'au matin.",
            "enjeu": "Chaque héros choisit son ARBRE DE TALENTS et en prend le palier 0, puis le palier 1 une fois Shocker mis à terre.",
            "pages": {},
            "victoire": [
                {
                    "cle": "Talent Tier 0",
                    "parJoueur": true,
                    "type": "choix",
                    "obligatoire": true,
                    "libelle": "Arbre de talents — palier 0",
                    "aide": "⚠ Sur table, ce palier se prend AVANT le scénario 1 : c'est lui qui déclare l'arbre choisi. Le carnet ne note les gains qu'APRÈS une rencontre, alors il est demandé ici — prenez-le dès votre première partie. Chaque joueur prend la carte de palier 0 de SON arbre de talents. Les cinq arbres sont proposés ensemble : le carnet ne sait pas retenir lequel a été choisi, c'est à vous de rester dans le vôtre. Les cartes gagnées restent pour toute la campagne et DOIVENT figurer dans le deck ; elles ne comptent pas dans sa taille minimale (livret p.2).",
                    "options": [
                        "wd112",
                        "wd122",
                        "wd132",
                        "wd142",
                        "wd152"
                    ]
                },
                {
                    "cle": "Talent Tier 1",
                    "parJoueur": true,
                    "type": "choix",
                    "obligatoire": true,
                    "libelle": "Arbre de talents — palier 1",
                    "aide": "Chaque joueur prend une carte du palier 1 de SON arbre de talents. Les cinq arbres sont proposés ensemble : le carnet ne sait pas retenir lequel a été choisi, c'est à vous de rester dans le vôtre. Les cartes gagnées restent pour toute la campagne et DOIVENT figurer dans le deck ; elles ne comptent pas dans sa taille minimale (livret p.2).",
                    "options": [
                        "wd113",
                        "wd114",
                        "wd123",
                        "wd124",
                        "wd133",
                        "wd134",
                        "wd143",
                        "wd144",
                        "wd153",
                        "wd154"
                    ]
                }
            ]
        },
        {
            "id": "wd_electro",
            "numero": 2,
            "nom": "Electro",
            "nom_fr": "Electro",
            "resume": "Electro et ses clones siphonnent le réseau électrique de New York avec l'aide de l'A.I.M. et l'argent du Caïd. Tant que vous n'êtes pas équipés, il est intouchable.",
            "enjeu": "Palier 2 de l'arbre : trois cartes proposées, une à prendre.",
            "pages": {},
            "victoire": [
                {
                    "cle": "Talent Tier 2",
                    "parJoueur": true,
                    "type": "choix",
                    "obligatoire": true,
                    "libelle": "Arbre de talents — palier 2",
                    "aide": "Chaque joueur prend une carte du palier 2 de SON arbre de talents. Les cinq arbres sont proposés ensemble : le carnet ne sait pas retenir lequel a été choisi, c'est à vous de rester dans le vôtre. Les cartes gagnées restent pour toute la campagne et DOIVENT figurer dans le deck ; elles ne comptent pas dans sa taille minimale (livret p.2).",
                    "options": [
                        "wd115",
                        "wd116",
                        "wd117",
                        "wd125",
                        "wd126",
                        "wd127",
                        "wd135",
                        "wd136",
                        "wd137",
                        "wd145",
                        "wd146",
                        "wd147",
                        "wd155",
                        "wd156",
                        "wd157"
                    ]
                }
            ]
        },
        {
            "id": "wd_the_lizard",
            "numero": 3,
            "nom": "The Lizard",
            "nom_fr": "Le Lézard",
            "resume": "Curt Connors a repris le dessus sur la bête, mais elle veille. Le vaincre ne suffit pas : il faut lui rendre sa raison avant qu'elle ne revienne.",
            "enjeu": "Palier 3 de l'arbre : trois cartes proposées, une à prendre.",
            "pages": {},
            "victoire": [
                {
                    "cle": "Talent Tier 3",
                    "parJoueur": true,
                    "type": "choix",
                    "obligatoire": true,
                    "libelle": "Arbre de talents — palier 3",
                    "aide": "Chaque joueur prend une carte du palier 3 de SON arbre de talents. Les cinq arbres sont proposés ensemble : le carnet ne sait pas retenir lequel a été choisi, c'est à vous de rester dans le vôtre. Les cartes gagnées restent pour toute la campagne et DOIVENT figurer dans le deck ; elles ne comptent pas dans sa taille minimale (livret p.2).",
                    "options": [
                        "wd118",
                        "wd119",
                        "wd120",
                        "wd128",
                        "wd129",
                        "wd130",
                        "wd138",
                        "wd139",
                        "wd140",
                        "wd148",
                        "wd149",
                        "wd150",
                        "wd158",
                        "wd159",
                        "wd160"
                    ]
                }
            ]
        },
        {
            "id": "wd_vulture",
            "numero": 4,
            "nom": "Vulture",
            "nom_fr": "Le Vautour",
            "resume": "Le Vautour a couvert la ville de pigeons-espions pour le compte de Fisk. Sans prendre les airs, vous ne l'atteindrez pas.",
            "enjeu": "Palier 4 de l'arbre, le dernier : une seule carte, la plus forte.",
            "pages": {},
            "victoire": [
                {
                    "cle": "Talent Tier 4",
                    "parJoueur": true,
                    "type": "choix",
                    "obligatoire": true,
                    "libelle": "Arbre de talents — palier 4",
                    "aide": "Chaque joueur prend une carte du palier 4 de SON arbre de talents. Les cinq arbres sont proposés ensemble : le carnet ne sait pas retenir lequel a été choisi, c'est à vous de rester dans le vôtre. Les cartes gagnées restent pour toute la campagne et DOIVENT figurer dans le deck ; elles ne comptent pas dans sa taille minimale (livret p.2).",
                    "options": [
                        "wd121",
                        "wd131",
                        "wd141",
                        "wd151",
                        "wd161"
                    ]
                }
            ]
        },
        {
            "id": "wd_kingpin",
            "numero": 5,
            "nom": "Kingpin",
            "nom_fr": "Le Caïd",
            "resume": "Wilson Fisk, maire de New York. Chaque carte de votre deck peut devenir l'une de ses manigances, et son costume encaisse ce que vous lui donnez.",
            "enjeu": "Rien de plus à gagner : c'est la dernière rencontre de la campagne.",
            "pages": {},
            "final": true,
            "victoire": [
                {
                    "cle": "Remaining hit points",
                    "parJoueur": true,
                    "type": "auto",
                    "format": "int",
                    "detection": "pv_restants",
                    "libelle": "Points de vie restants",
                    "aide": "La campagne s'achève : ce chiffre n'est là que pour le récit."
                }
            ]
        }
    ],
    "expert": {
        "pv_persistants": false,
        "note": "En expert, « Vote for Fisk » entre en jeu sur sa face experte et un gobelin expert est mêlé au deck rencontre dès qu'on joue à plusieurs (livret p.3). Chaque scénario a sa propre variante experte, sélectionnable à la création de la partie."
    },
    "victoire_commune_expert": []
}
```

### 8.3 Toutes les clés, une par une

#### 8.3.1 Clés de premier niveau

| Clé | Type | Obligatoire | Sens |
|---|---|---|---|
| `version` | texte | oui | `"1.0"` |
| `code` | texte | oui | Le code de la campagne = nom du fichier = nom du pack le plus souvent = dossier `public/stories/<code>/`. |
| `cle_extension` | texte | oui | **La clé de `data/sets_info.json`** (`"21. The Mad Titan's Shadow"`), **au caractère près**. Le numéro devant donne l'ordre de parution. Fan-made : laisse `"A_FAIRE_CLAUDE"` (Claude attribue le numéro). |
| `nom`, `nom_en` | texte | oui | Le nom en français et en anglais. |
| `resume`, `resume_en` | texte | oui | Deux phrases pour présenter la boîte, en français puis en anglais. |
| `expert` | objet | oui | `{ "pv_persistants": true }` si, en campagne experte, les PV se reportent. `{ "note": "…" }` : texte affiché en mode expert (ordre libre). **Cette clé est informative** : le report réel des PV se fait par `victoire_commune_expert` + `ExpertCampaignSetPlayersHPToTheirRemainingHP` (§7.4). |
| `scenarios` | liste | oui | Un objet par scénario, **dans l'ordre** (§8.3.2). |
| `victoire_commune` | liste de champs | non | Champs présentés à **chaque** victoire **sauf** le scénario final (§8.3.3). |
| `victoire_commune_expert` | liste de champs | oui (peut être `[]`) | Idem, **en campagne experte seulement**. C'est là que vivent les PV restants. |
| `pages_regles` | liste de noms de fichier | oui (peut être `[]`) | Planches de règles **de la campagne** (`00-campagne-regles-1.jpg`). Tu laisses `[]` si tu n'as pas les pages ; Claude les ajoute. |
| `pages_expert` | liste | non | Planches de règles de la campagne **experte** (affichées seulement en expert). |
| `pages_intro` | liste | non | Planche(s) d'ouverture, affichée(s) **au début de la campagne** (avant le scénario 1). |
| `livret_fr` | booléen | non | `true` si `public/stories/<code>/fr/` contient les pages refaites en français ; sinon l'écran ne cherche pas. |
| `options_campagne` | liste | non | Réglages faits **au début** de la campagne (§8.5.1). |
| `marche` | objet | non | Un marché de cartes à acheter entre deux scénarios (§8.5.2). |
| `cooperation` | objet | non | La zone de coopération de Skrull Menace (§8.5.3). |
| `enquete` | objet | non | L'enquête d'Agents of S.H.I.E.L.D. (§8.5.4). |
| `bilan` | objet | non | Un score final noté **à la fin** (§8.5.5). |
| `ordre_libre`, `vilains`, `pages_vilains` | booléen, liste, liste | non | Campagne **en ordre libre** (Fear No Evil, §8.5.6). |

#### 8.3.2 Un scénario (`scenarios[]`)

| Clé | Obligatoire | Sens |
|---|---|---|
| `id` | oui | L'identifiant du scénario. **Doit être dans `sets_info.json` › `scenarios` ET être un fichier `data/scenarios/<id>.json`.** C'est aussi l'**estampille** que le moteur pose au carnet sortant (§7.5) et le dernier mot du dossier de pages. |
| `catalogue` | non | Si le fichier de scénario lancé **n'est pas** `<id>.json` : l'id du fichier réellement lancé (`"kingpin_fne"`). Sinon omis. |
| `numero` | oui | 1, 2, 3… **C'est le `niveau` de `CampaignSetup(niveau)`** (§7.3). |
| `nom`, `nom_fr` | oui | Nom anglais, nom français (le français sert dans l'interface en français). |
| `resume` | oui | Ce qui se passe, **deux phrases, écrites pour un joueur**, en français. Pas de recopie du livret : un récit. |
| `enjeu` | oui | Ce que ce scénario change pour la suite, **une phrase**. « Rien à reporter : c'est le dernier scénario. » pour le dernier. |
| `final` | sur le dernier | `true` sur le dernier scénario : le panneau dit « La campagne est gagnée ! » et les champs communs sautent. |
| `defaite` | non | **Ce qui perd la campagne** (scénario final seulement) : `{"quand": "partie_perdue" \| "cle_absente", "cle": "<clé>", "expert_seulement": true, "texte": "…"}`. `partie_perdue` : perdre ce scénario perd la campagne. `cle_absente` : la campagne est perdue si `cle` manque au carnet (AoA : `Professor Saved`). `expert_seulement` : la règle ne vaut qu'en expert (**vrai partout sauf AoA**). `texte` : ce que le livret raconte. |
| `reprise` | non | **Faut-il re-préparer avant de rejouer ?** (AOS seulement) : `{"quand": "partie_perdue", "standard_seulement": true, "titre", "texte", "cle_compte", "cle_preuves"}`. |
| `defaite_continue` | non | `true` : **une défaite ne fait PAS rejouer** ce scénario (ignoré sur un scénario `final`) : elle a ses propres gains, le panneau s'ouvre aussi à la défaite et la campagne passe au suivant (Hunting Season). |
| `pages` | oui | `{ "intro": [...], "regles": [...], "epilogue": [...] }` : noms de fichiers du dossier `public/stories/<code>/`. **Tu laisses `{}`** si tu n'as pas les pages ; Claude les ajoute. Une planche qui termine un scénario ET ouvre le suivant n'est pas dupliquée. |
| `victoire` | oui (peut être `[]`) | Les **champs du carnet** notés après ce scénario (§8.3.3). |
| `manigance`, `environnement` | ordre libre | `manigance: true` = scénario interchangeable ; `environnement: "60205a,60205b"` = la carte qui entre en jeu selon l'issue. |

**Exemple d'un scénario avec défaite de campagne :**
```json
{
  "id": "loki",
  "numero": 5,
  "nom": "Loki",
  "nom_fr": "Loki",
  "resume": "Loki règne sur Asgard et rien de ce que vous voyez n'est sûr d'exister. La campagne se termine ici, avec tout ce que vous y avez traîné.",
  "enjeu": "Rien à reporter : c'est le dernier scénario.",
  "final": true,
  "defaite": {
    "quand": "partie_perdue",
    "expert_seulement": true,
    "texte": "Loki étend son règne sur tout l'univers : la campagne est perdue."
  },
  "victoire": []
}
```

**Exemple d'un scénario avec reprise après défaite (Agents of S.H.I.E.L.D., scénario 5) :**
```json
{
  "id": "baron_zemo",
  "numero": 5,
  "nom": "Baron Zemo",
  "nom_fr": "Le Baron Zemo",
  "resume": "Zemo tire les fils depuis le début et achève de retourner le Conseil. Un membre à quatre secrets le rejoint ; s'ils basculent tous les trois, la partie est perdue.",
  "enjeu": "Fin de la campagne : démasquer la taupe et laver votre nom.",
  "final": true,
  "defaite": {
    "quand": "partie_perdue",
    "expert_seulement": true,
    "texte": "Les héros sont arrêtés par le S.H.I.E.L.D. et condamnés : la campagne est perdue."
  },
  "reprise": {
    "quand": "partie_perdue",
    "standard_seulement": true,
    "cle_compte": "Scenarios With A Cleared Board Member",
    "cle_preuves": "Evidence Gained",
    "titre": "L'enquête repart de zéro",
    "texte": "Vous êtes démasqués avant d'avoir pu prouver quoi que ce soit. Pour rejouer ce scénario, le livret fait re-préparer les preuves comme au début d'une campagne : une nouvelle taupe, une nouvelle enveloppe. Votre grille de déduction est donc à refaire. Vous récupérez une preuve par scénario où au moins un membre du Conseil avait fini sans secret."
  }
}
```

**Exemple d'un scénario qui continue la campagne même perdu (Hunting Season) :**
```json
{
  "id": "hs_vermin",
  "numero": 1,
  "nom": "Vermin",
  "nom_fr": "Vermin",
  "resume": "Affrontez Vermin et appliquez les instructions de campagne du livret.",
  "enjeu": "Victoire ou défaite, la campagne continue : le résultat change l'expérience gagnée, l'allié de récompense et le deck rencontre de Kraven.",
  "defaite_continue": true
}
```

**Exemple d'un scénario avec une défaite par clé absente (Age of Apocalypse, scénario 5) :**
```json
{
  "id": "en_sabah_nur",
  "numero": 5,
  "nom": "En Sabah Nur",
  "nom_fr": "En Sabah Nur",
  "resume": "En Sabah Nur, à la source. Tout ce que la campagne vous a laissé sert ici.",
  "enjeu": "Fin de la campagne.",
  "final": true,
  "defaite": {
    "quand": "cle_absente",
    "cle": "Professor Saved",
    "texte": "Le Professeur X n'a pas été sauvé : la campagne est perdue."
  }
}
```

#### 8.3.3 Un champ de victoire (élément de `victoire`, `victoire_commune`, `victoire_commune_expert`)

| Clé | Obligatoire | Sens |
|---|---|---|
| `cle` | oui | **La clé du carnet**, copiée **telle quelle** de `campaign.py` (§7.9). Pour un champ `parJoueur`, c'est la clé **sans** le préfixe `Player N`. |
| `type` | oui | **`"auto"`** : valeur **relevée par le jeu** (collecteur, détecteur ou carnet existant), affichée comme un constat, corrigeable. **`"choix"`** : **décision du joueur** (le livret dit « each player chooses ») ; jamais pré-remplie par le moteur. |
| `format` | non | `"int"` (un nombre : champ numérique) ; `"liste"` (des `card_id` joints par `;`) ; `"liste-joueurs"` (des indices de joueurs). Absent = texte libre (rôle, état). |
| `parJoueur` | non | `true` : une valeur **par héros**, stockée sous `Player N <cle>` ; chaque joueur ne saisit que **sa** case. |
| `obligatoire` | non | `choix` seulement : `true` bloque le bouton « Valider » tant qu'une case manque. |
| `libelle` | oui | Intitulé court affiché (français). |
| `aide` | oui | **Une phrase** : à quoi sert cette clé plus tard (français). |
| `options` | non | Les `card_id` proposés : **choix** → un seul (cartes cliquables) ; **auto + liste** → plusieurs (cases à cocher) ; avec `detection`, les `options` sont **les cartes que le détecteur cherche**. |
| `detection` | non | Un détecteur (§8.4). **Facultatif pour une boîte à collecteur**, **nécessaire** pour une boîte sans collecteur. |
| `parametres` | non | Paramètres du détecteur (`{"compteur": "delay"}`, `{"complot": "04122", "type": "Ally"}`). |
| `condition` | non | Le champ n'est **présenté** que si la condition est vraie. Une seule : `"complot_absent"` + `parametres.complot` (le complot **annexe** n'est plus dans `area_schemes_side`). **Une condition inconnue MASQUE le champ** : on n'accorde pas une récompense dont on ne sait pas évaluer la règle. |
| `cumulatif` | non | `true` + `format: "int"` : le carnet **cumule** ce champ d'un scénario à l'autre. Vrai pour une valeur **issue d'un détecteur** (elle est ce que la partie **ajoute**, le panneau additionne) ; une valeur relevée par le **collecteur du moteur** est déjà cumulée et n'est **pas** additionnée une seconde fois. |
| `tirage` | non | `{"cle_piste": "<clé>", "paliers": [1, 13, 21]}` : le champ se **tire au sort** à chaque palier atteint par la piste `cle_piste`. Exige `type: "auto"`, `options` non vide, `paliers` croissants d'entiers positifs, et que `cle_piste` soit déclarée **avant** ce champ. Cumulatif et irréversible. |
| `deck` | non | `"requis"` : **l'écran** refuse, au retour de « Modifier les decks », un deck qui ne contient plus la carte notée. Le drapeau ne fait que cela : **la recherche dans le deck est faite par ton script** à la mise en place suivante (modèle : `sm/campaign.py`). Exige `parJoueur`. |
| `cases` | non | Un tableau de cases à cocher : `[{"titre": "Antalya", "exigences": ["Nemesis minion", "…"]}]` ; le carnet garde `« Titre: exigence »` pour chaque case cochée (Skrull Menace). |

**Exemples réels, un par comportement :**

*Drapeau relevé par le moteur (aucune `detection`)* :
```json
{
  "cle": "Campaign Pool: Cosmo",
  "type": "auto",
  "format": "int",
  "libelle": "Cosmo rallié",
  "aide": "Cosmo entre en jeu sous votre contrôle au scénario 3 s'il est noté ici."
}
```

*Un nombre par joueur détecté dans l'état du monde (PV restants, en expert)* :
```json
{
  "cle": "Remaining hit points",
  "parJoueur": true,
  "type": "auto",
  "format": "int",
  "detection": "pv_restants",
  "libelle": "Points de vie restants",
  "aide": "En campagne experte, vous reprenez le scénario suivant avec ces points de vie."
}
```

*Un choix de carte par joueur, obligatoire* :
```json
{
  "cle": "Tech Upgrade",
  "parJoueur": true,
  "type": "choix",
  "obligatoire": true,
  "libelle": "Amélioration technologique",
  "aide": "Chaque héros choisit une amélioration TECH du set Hydra Campaign et l'ajoute à son deck pour le reste de la campagne.",
  "options": [
    "04155",
    "04156",
    "04157",
    "04158"
  ]
}
```

*Une liste par joueur détectée parmi des options* :
```json
{
  "cle": "Rescued Allies",
  "parJoueur": true,
  "type": "auto",
  "format": "liste",
  "detection": "cartes_du_joueur",
  "libelle": "Alliés secourus",
  "aide": "Ils sont mélangés au deck du héros au début de chaque scénario suivant.",
  "options": [
    "04097",
    "04098",
    "04099",
    "04100"
  ]
}
```

*Des cartes entrées en jeu, parmi des options* :
```json
{
  "cle": "Experimental Weapons added to encounter deck",
  "type": "auto",
  "format": "liste",
  "detection": "cartes_en_jeu",
  "libelle": "Armes expérimentales entrées en jeu",
  "aide": "Elles seront remélangées dans le deck de rencontre de chaque scénario suivant.",
  "options": [
    "04072",
    "04073",
    "04074",
    "04075"
  ]
}
```

*Un compteur lu sur la manigance principale* :
```json
{
  "cle": "Number of delay counters on main scheme",
  "type": "auto",
  "format": "int",
  "detection": "compteur_manigance",
  "parametres": {
    "compteur": "delay"
  },
  "libelle": "Pions retard sur la manigance principale",
  "aide": "Crâne Rouge commencera son scénario avec autant de menace (par joueur en campagne experte)."
}
```

*Les joueurs encore engagés* :
```json
{
  "cle": "Players engaged with minions",
  "type": "auto",
  "format": "liste-joueurs",
  "detection": "joueurs_engages",
  "libelle": "Héros engagés avec un ennemi à la fin",
  "aide": "En campagne experte, ils se distribueront une carte de rencontre au début du scénario de Crâne Rouge."
}
```

*Des cartes posées sous un complot encore en jeu* :
```json
{
  "cle": "Allies removed from the campaign",
  "type": "auto",
  "format": "liste",
  "detection": "cartes_sous_complot",
  "parametres": {
    "complot": "04122",
    "type": "Ally"
  },
  "libelle": "Alliés retirés de la campagne",
  "aide": "Les alliés encore prisonniers sous la Prison d'Hydra sont retirés de tous les decks jusqu'à la fin de la campagne."
}
```

*Un choix soumis à une condition (le complot est tombé)* :
```json
{
  "cle": "Basic Upgrade",
  "parJoueur": true,
  "type": "choix",
  "obligatoire": false,
  "libelle": "Amélioration de base",
  "aide": "Chaque héros PEUT choisir une amélioration Basic du set Hydra Campaign, l'attacher à son identité et l'ajouter à son deck.",
  "options": [
    "04159a",
    "04160a",
    "04161a",
    "04162a"
  ]
}
```

*Un total cumulatif, détecté par six conditions de la partie* :
```json
{
  "cle": "Reputation Track",
  "type": "auto",
  "format": "int",
  "detection": "conditions_reputation",
  "cumulatif": true,
  "libelle": "Piste de Réputation (total cumulé)",
  "aide": "Relevé par le jeu : les six conditions de la piste sont comptées sur la partie qui vient de finir (points de victoire, aucun sbire, aucune manigance annexe, aucune menace sur la manigance principale, aucun pion accélération, aucune identité vaincue), puis ajoutées aux nœuds déjà marqués. Corrigeable si tu joues avec une piste papier. C'est elle qui déclenche récompenses ET pénalités : matériel S.H.I.E.L.D. dès 1, mulligan supplémentaire à 5, carte d'aspect à 9, version améliorée à 13, carte de départ en main à 17, Helicarrier à 21, Symbiote Suit à 25."
}
```

*Un tirage au sort aux paliers d'une piste* :
```json
{
  "cle": "Osborn Tech: Reputation Track Penalty",
  "type": "auto",
  "format": "liste",
  "tirage": {
    "cle_piste": "Reputation Track",
    "paliers": [
      1,
      13,
      21
    ]
  },
  "options": [
    "27147",
    "27148",
    "27149",
    "27150",
    "27151",
    "27152"
  ],
  "libelle": "Pénalité de réputation — matériel Osborn",
  "aide": "Tiré au sort par le jeu, comme le livret le demande (« Choose one Osborn Tech attachment at random »), aux paliers 1, 13 et 21 de la piste. Cumulatif : une carte tirée le reste pour toute la campagne, et elle sera mélangée au deck de rencontre à chaque mise en place. Corrigeable si tu préfères tirer toi-même."
}
```

*Un choix qui exige que la carte reste dans le deck* :
```json
{
  "cle": "Planning Ahead: Reputation Track Reward",
  "parJoueur": true,
  "deck": "requis",
  "type": "choix",
  "libelle": "Récompense Réputation 17 — carte de départ en main",
  "aide": "À saisir quand la piste atteint 17 : l'identifiant de la carte de ton deck que tu veux avoir en main dès la mise en place."
}
```

### 8.4 Les détecteurs disponibles (`ui-app/src/board/campagne/detecteurs.ts`)

Un **détecteur** lit l'état du monde (le descripteur de fin de partie) et rend la valeur **dans la forme exacte du
carnet** (`"id1;id2"`, `"3"`). **Tous sont génériques** : aucun n'a de boîte en dur. Une `detection` **inconnue
ne lève rien** : le champ reste vide et la récompense disparaît en silence — `verifier_campagnes.py` refuse un nom
inexistant. **N'invente pas de détecteur** : s'il en manque un, `A_FAIRE_CLAUDE` dans `BESOINS-MOTEUR.md`.

| `detection` | Rend | Paramètres | Source de vérité |
|---|---|---|---|
| `cartes_en_jeu` | parmi `options`, celles **entrées en jeu** pendant la partie (hors decks, zones mises de côté et decks additionnels) | — | Armes expérimentales de Crossbones |
| `compteur_manigance` | la valeur d'un compteur sur la manigance principale (le **maximum** si plusieurs) | `compteur` (`"delay"`) | Pions retard de Zola |
| `cartes_du_joueur` | parmi `options`, celles que **ce joueur possède** désormais (où qu'elles soient) | — | Alliés secourus de Taskmaster |
| `joueurs_engages` | les **indices** (`"0"`, `"1"`) des joueurs encore engagés avec au moins un ennemi | — | Joueurs engagés de Zola |
| `cartes_sous_complot` | les cartes **posées sous** un complot **annexe** encore en jeu (le code ne cherche que dans `area_schemes_side`, jamais sous une manigance principale ; même zone, `bind_object_id` = id du complot ; `parametres.type` est comparé au `card_type`) | `complot` (card_id), `type` | Prison d'Hydra |
| `pv_restants` | les PV de l'identité, **plafonnés** aux PV imprimés ; rien pour un héros éliminé | — | Livret p.17 |
| `cartes_en_pile_victoire` | parmi `options`, celles dans la **pile de victoire** | — | Community Service de sm |
| `cartes_dans_zone` | parmi `options`, celles présentes dans une **zone nommée** du descripteur de monde (clé du monde : `area_villain`, `area_schemes_main`, `area_schemes_side`, `area_environment`, `area_set_aside`… ; sm utilise `area_villain`) | `zone` | Vilains encore en jeu de sm |
| `compter_trait` | le **nombre** de cartes portant un trait dans les decks, mains et défausses des joueurs | `trait` (`"ILLUSION"`) | Cartes ILLUSION de sm |
| `conditions_reputation` | le total des **six conditions** de la piste de réputation de sm | — | sm p.22 |

Faits mesurés sur les descripteurs réels, à ne pas re-deviner : les **compteurs** sortent en `info.c_<nom>`
(`c_delay`), les **jetons** en `info.k_<nom>` (`k_threat`, `k_acceleration_token`) ; les **traits** en
`traits.t_<NOM>` ; une carte posée sous un complot est dans **la même zone** que lui, avec `bind_object_id` égal à
l'`id` du complot ; les PV de l'identité sont `info.health` / `info.max_health` sur `players[i].area_hero[0]` ;
le deck des Armes Expérimentales est un **deck additionnel** (`additional_decks`).

### 8.5 Les blocs spéciaux (mécaniques déjà gérées par l'écran)

Ces blocs existent parce qu'une boîte les a exigés. **Si ta campagne a la même mécanique, déclare le bloc comme
dans le modèle ; sinon ne les utilise pas** ; une mécanique inédite = `BESOINS-MOTEUR.md`.

#### 8.5.1 `options_campagne` : des réglages faits au début

Deux types : `"case"` (`carnet[cle]` = `"1"` ou `"0"`) et `"siege"` (`carnet[cle]` = numéro du héros, 1 à 4).
Modifiables tant qu'aucun scénario n'est joué. `expert_seulement: true` : n'apparaît qu'en campagne experte.
```json
{
  "options_campagne": [
    {
      "cle": "Hunter Mode",
      "type": "case",
      "expert_seulement": true,
      "libelle": "Mode Hunter",
      "aide": "Campagne experte uniquement : un environnement par scénario rend la chasse bien plus dure."
    },
    {
      "cle": "Master Hunter",
      "type": "siege",
      "libelle": "Master Hunter",
      "aide": "Il départage les égalités et désigne qui reçoit l'allié de récompense quand l'équipe hésite."
    }
  ]
}
```

#### 8.5.2 `marche` : acheter des cartes entre deux scénarios

Entre deux scénarios, chaque héros dépense ses unités (ou son expérience) pour ajouter des cartes à son deck.
Elles y restent jusqu'à la fin de la campagne (le moteur les remet à chaque mise en place, depuis le carnet) ;
**une seule copie de chaque carte pour toute l'équipe**. Le coût est lu **dans le texte de la carte**
(`motif_cout`, expression régulière ; par défaut `Unit Cost (\d+)`). Voir `gmw` (plage `premiere_carte`…
`derniere_carte`) et `hunting_season` (liste `cartes`, `verrous`, `ouvert_apres_premier`, `unite`) :
```json
{
  "marche": {
    "premiere_carte": "16150",
    "derniere_carte": "16177",
    "cle_unites": "Unspent Units",
    "cle_cartes": "Market Cards",
    "titre": "Le Marché",
    "aide": "Entre deux scénarios, chaque héros dépense ses unités pour ajouter des cartes à son deck. Elles y restent jusqu'à la fin de la campagne et ne comptent pas dans sa taille."
  }
}
```
```json
{
  "marche": {
    "cartes": [
      "hs164",
      "hs165",
      "hs166",
      "hs167",
      "hs168",
      "hs169",
      "hs170",
      "hs171",
      "hs172",
      "hs173",
      "hs174",
      "hs175",
      "hs176",
      "hs177",
      "hs178",
      "hs179",
      "hs180",
      "hs181",
      "hs182",
      "hs183",
      "hs184",
      "hs185",
      "hs186",
      "hs187",
      "hs188",
      "hs189",
      "hs190",
      "hs191",
      "hs192",
      "hs193",
      "hs194",
      "hs195",
      "hs196",
      "hs197",
      "hs198",
      "hs199"
    ],
    "motif_cout": "Experience Cost (\\d+)",
    "verrous": {
      "hs168": "Gibbon unlocked"
    },
    "ouvert_apres_premier": true,
    "cle_unites": "Experience",
    "cle_cartes": "Cards added to deck",
    "titre": "Le Lodge",
    "unite": "XP",
    "libelle_solde": "XP non dépensée",
    "aide": "Entre deux scénarios, chaque héros dépense son expérience pour ajouter des cartes du Lodge à son deck. Elles y restent jusqu'à la fin de la campagne et ne comptent pas dans sa taille. Une seule copie de chaque exemplaire pour toute l'équipe."
  }
}
```

#### 8.5.3 `cooperation` : la zone de coopération (Skrull Menace)

Une zone de cartes de campagne partagées, un tableau de progression à cases, un journal par scénario. Les clés du
carnet (`Cooperation Area`, `Cooperation Progress`, `Player N Cooperation Deck`, `Next Skrull Elite`…) sont
écrites par `skrull_menace/campaign.py`. **Mécanique propre à cette boîte** : voir
`modeles/D-patrons-de-campaign-py/skrull_menace/` et `data/campagnes/skrull_menace.json`. Le bloc :
```json
{
  "cooperation": {
    "titre": "Coopération",
    "titre_en": "Cooperation",
    "aide": "La zone de coopération et le tableau « Cooperation Progress » de votre campagne, tels que le carnet les garde.",
    "cle_zone": "Cooperation Area",
    "cle_progres": "Cooperation Progress",
    "colonnes": [
      {
        "titre": "Alliés",
        "titre_en": "Allies",
        "ids": [
          "sk263",
          "sk264",
          "sk265",
          "sk266",
          "sk267",
          "sk268",
          "sk269"
        ]
      },
      {
        "titre": "Complots annexes de joueur",
        "titre_en": "Player side schemes",
        "ids": [
          "sk270",
          "sk271",
          "sk272",
          "sk273",
          "sk274",
          "sk275",
          "sk276"
        ]
      },
      {
        "titre": "Ressources",
        "titre_en": "Resources",
        "ids": [
          "sk230a",
          "sk230b",
          "sk230c",
          "sk230d"
        ]
      },
      {
        "titre": "Soutiens",
        "titre_en": "Supports",
        "ids": [
          "sk277",
          "sk278",
          "sk279",
          "sk280",
          "sk281",
          "sk282"
        ]
      },
      {
        "titre": "Améliorations",
        "titre_en": "Upgrades",
        "ids": [
          "sk283",
          "sk284",
          "sk285",
          "sk286",
          "sk287",
          "sk288"
        ]
      }
    ],
    "tableau": [
      {
        "carte": "sk277",
        "titre": "Antalya",
        "exigences": [
          "Nemesis minion",
          "Seeking a Suitable World"
        ],
        "ajoutees": [
          "sk277"
        ]
      },
      {
        "carte": "sk278",
        "titre": "Cadre K",
        "exigences": [
          "Non-ELITE minion",
          "Hijacked",
          "GENIUS minion"
        ],
        "ajoutees": [
          "sk278"
        ]
      },
      {
        "carte": "sk279",
        "titre": "Pool-o-Vision",
        "exigences": [
          "ELITE non-SKRULL minion",
          "ELITE SKRULL minion",
          "Non-ELITE SKRULL minion"
        ],
        "ajoutees": [
          "sk279"
        ]
      },
      {
        "carte": "sk280",
        "titre": "Princess Anelle",
        "exigences": [
          "Cloning Program",
          "Emperor's Throne"
        ],
        "ajoutees": [
          "sk280"
        ]
      },
      {
        "carte": "sk281",
        "titre": "Skrull Battleship",
        "exigences": [
          "SOLDIER minion",
          "Hijacked",
          "Seeking a Suitable World"
        ],
        "ajoutees": [
          "sk281"
        ]
      },
      {
        "carte": "sk282",
        "titre": "Skrull Kill Crew",
        "exigences": [
          "Skrull Spy",
          "Skrull Warrior",
          "Skrull Soldier",
          "Skrull Commander"
        ],
        "ajoutees": [
          "sk282"
        ]
      },
      {
        "carte": "sk283",
        "titre": "3-D Man's Goggles",
        "exigences": [
          "ELITE minion",
          "Non-SKRULL minion",
          "Player side scheme",
          "Non-unique minion"
        ],
        "ajoutees": [
          "sk283"
        ]
      },
      {
        "carte": "sk284",
        "titre": "Inhibitor Mask",
        "exigences": [
          "Plotting Revenge",
          "Non-ELITE non-SKRULL minion"
        ],
        "ajoutees": [
          "sk284"
        ]
      },
      {
        "carte": "sk285",
        "titre": "Nullifier",
        "exigences": [
          "Nemesis side scheme"
        ],
        "ajoutees": [
          "sk285"
        ]
      },
      {
        "carte": "sk286",
        "titre": "Reverting Device",
        "exigences": [
          "Skrull Spy",
          "Skrull Scientist",
          "Skrull Warrior",
          "Skrull Telepath"
        ],
        "ajoutees": [
          "sk286"
        ]
      },
      {
        "carte": "sk287",
        "titre": "Skrull Shapeshifter",
        "exigences": [
          "Unique minion",
          "Plotting Revenge",
          "SKRULL minion"
        ],
        "ajoutees": [
          "sk287"
        ]
      },
      {
        "carte": "sk288",
        "titre": "Sy-Torak Gem",
        "exigences": [
          "Jazinda",
          "Stealing for the Empire"
        ],
        "ajoutees": [
          "sk288"
        ]
      },
      {
        "carte": "sk230",
        "titre": "Cosmic Cube Fragment",
        "exigences": [
          "Cosmic Cube Creation"
        ],
        "ajoutees": [
          "sk230a",
          "sk230b",
          "sk230c",
          "sk230d"
        ]
      }
    ],
    "journal": [
      {
        "cle": "Shaper of Worlds Game Area",
        "libelle": "Shaper of Worlds",
        "libelle_en": "Shaper of Worlds"
      },
      {
        "cle": "Cosmic Cube Creation Game Area",
        "libelle": "Cosmic Cube Creation",
        "libelle_en": "Cosmic Cube Creation"
      },
      {
        "cle": "Skrull Elite: Crusader",
        "libelle": "Elite Crusader",
        "libelle_en": "Elite Crusader"
      },
      {
        "cle": "Skrull Elite: Jazinda",
        "libelle": "Elite Jazinda",
        "libelle_en": "Elite Jazinda"
      },
      {
        "cle": "Skrull Elite: Skymax",
        "libelle": "Elite Skymax",
        "libelle_en": "Elite Skymax"
      },
      {
        "cle": "Skrull Elite: War Skrull",
        "libelle": "Elite War Skrull",
        "libelle_en": "Elite War Skrull"
      },
      {
        "cle": "Skrull Elite: Xavin",
        "libelle": "Elite Xavin",
        "libelle_en": "Elite Xavin"
      }
    ],
    "cle_deck": "Cooperation Deck",
    "cle_elite_annoncee": "Next Skrull Elite",
    "elites": [
      {
        "nom": "Crusader",
        "cle": "Skrull Elite: Crusader",
        "sbire": "sk231"
      },
      {
        "nom": "Jazinda",
        "cle": "Skrull Elite: Jazinda",
        "sbire": "sk236"
      },
      {
        "nom": "Skymax",
        "cle": "Skrull Elite: Skymax",
        "sbire": "sk241"
      },
      {
        "nom": "War Skrull",
        "cle": "Skrull Elite: War Skrull",
        "sbire": "sk245"
      },
      {
        "nom": "Xavin",
        "cle": "Skrull Elite: Xavin",
        "sbire": "sk250"
      }
    ]
  }
}
```

#### 8.5.4 `enquete` : la grille de déduction (Agents of S.H.I.E.L.D.)

27 combinaisons (9 par membre), 9 cartes de preuve en 3 séries ; chaque preuve obtenue raye les combinaisons qui
la contiennent. **La combinaison secrète vit côté serveur et ne sort jamais** (`_sans_secret`). Mécanique propre à
cette boîte :
```json
{
  "enquete": {
    "titre": "L'enquête",
    "aide": "Un des trois membres du Conseil est une taupe. Sa combinaison — moyen, mobile, occasion — dort dans l'enveloppe A.I.M. Chaque preuve obtenue raye toutes les combinaisons qui la contiennent : ce qui reste est encore possible.",
    "cle_preuves": "Evidence Gained",
    "series": [
      {
        "cle": "moyen",
        "libelle": "Moyen"
      },
      {
        "cle": "mobile",
        "libelle": "Mobile"
      },
      {
        "cle": "occasion",
        "libelle": "Occasion"
      }
    ],
    "preuves": [
      {
        "id": "50185",
        "serie": "moyen",
        "nom": "Dossiers médicaux",
        "nom_en": "Medical Records",
        "court": "Dossiers",
        "teinte": "#e8a06a"
      },
      {
        "id": "50186",
        "serie": "moyen",
        "nom": "Écoute téléphonique",
        "nom_en": "Wiretap",
        "court": "Écoute",
        "teinte": "#7cc4ea"
      },
      {
        "id": "50187",
        "serie": "moyen",
        "nom": "Scanner de sécurité",
        "nom_en": "Security Scanner",
        "court": "Scanner",
        "teinte": "#e79ab0"
      },
      {
        "id": "50188",
        "serie": "mobile",
        "nom": "Argent",
        "nom_en": "Money",
        "court": "Argent",
        "teinte": "#9ed093"
      },
      {
        "id": "50189",
        "serie": "mobile",
        "nom": "Chantage",
        "nom_en": "Blackmail",
        "court": "Chantage",
        "teinte": "#6b6b6b"
      },
      {
        "id": "50190",
        "serie": "mobile",
        "nom": "Idéologie",
        "nom_en": "Ideology",
        "court": "Idéologie",
        "teinte": "#eed473"
      },
      {
        "id": "50191",
        "serie": "occasion",
        "nom": "Habilitation",
        "nom_en": "Security Clearance",
        "court": "Habilitation",
        "teinte": "#b79ccb"
      },
      {
        "id": "50192",
        "serie": "occasion",
        "nom": "Voyages",
        "nom_en": "Travel",
        "court": "Voyages",
        "teinte": "#ea8d80"
      },
      {
        "id": "50193",
        "serie": "occasion",
        "nom": "Autorité",
        "nom_en": "Authority",
        "court": "Autorité",
        "teinte": "#8aa6d4"
      }
    ],
    "membres": [
      {
        "cle": "Chief Medical Officer",
        "nom": "Médecin en chef",
        "combinaisons": [
          "50185;50188;50191",
          "50185;50188;50192",
          "50185;50189;50191",
          "50185;50189;50193",
          "50185;50190;50192",
          "50186;50188;50191",
          "50186;50188;50192",
          "50186;50189;50191",
          "50187;50188;50191"
        ]
      },
      {
        "cle": "Chief Surveillance Officer",
        "nom": "Chef de la surveillance",
        "combinaisons": [
          "50185;50189;50192",
          "50186;50188;50193",
          "50186;50189;50192",
          "50186;50189;50193",
          "50186;50190;50191",
          "50186;50190;50192",
          "50187;50189;50192",
          "50187;50189;50193",
          "50187;50190;50192"
        ]
      },
      {
        "cle": "Chief Tactical Officer",
        "nom": "Chef tactique",
        "combinaisons": [
          "50185;50188;50193",
          "50185;50190;50191",
          "50185;50190;50193",
          "50186;50190;50193",
          "50187;50188;50192",
          "50187;50188;50193",
          "50187;50189;50191",
          "50187;50190;50191",
          "50187;50190;50193"
        ]
      }
    ]
  }
}
```

#### 8.5.5 `bilan` : un score final saisi à la fin

`{ "titre", "cle", "aide", "libelle_ajout", "aide_ajout" }` : après le dernier scénario, le joueur peut ajouter
un dernier calcul à la piste cumulée du carnet (`cle`). Facultatif de bout en bout (Sinister Motives) :
```json
{
  "bilan": {
    "titre": "Score de réputation final",
    "cle": "Reputation Track",
    "aide": "Facultatif, livret p.17 : après la victoire sur Venom Goblin, l'équipe peut calculer une dernière fois la section « Conditions » de sa piste, marquer les nœuds gagnés, et noter le total. Plus il est haut, mieux vous avez joué.",
    "libelle_ajout": "Dernier calcul des conditions",
    "aide_ajout": "Les points de cette dernière partie, à ajouter au total cumulé de la piste. Laisser à 0 pour reporter la piste telle quelle."
  }
}
```

#### 8.5.6 Ordre libre (`ordre_libre: true`, Fear No Evil)

Cinq « affaires » jouables dans l'ordre choisi, chacune contre un vilain ; avant chaque partie **deux affaires non
résolues progressent au hasard** ; à trois marques, l'affaire est perdue ; Kingpin quand tout est résolu. Les
règles pures sont dans `public/js/campagne/ordre-libre.js`. Déclaration : `ordre_libre: true`, `vilains: [{id, nom,
ordre}]`, `pages_vilains`, des scénarios `manigance: true` (plus un `final: true` avec `catalogue`). **Mécanique
propre à cette boîte** (`data/campagnes/fne.json`) :
```json
{
  "vilains": [
    {
      "id": "hammerhead",
      "nom": "Hammerhead",
      "ordre": 1
    },
    {
      "id": "bullseye",
      "nom": "Bullseye",
      "ordre": 2
    },
    {
      "id": "electro",
      "nom": "Electro",
      "ordre": 3
    },
    {
      "id": "purple_man",
      "nom": "Purple Man",
      "ordre": 4
    },
    {
      "id": "typhoid_mary",
      "nom": "Typhoid Mary",
      "ordre": 4
    }
  ]
}
```
```json
{
  "pages_vilains": [
    "00-vilains-1.jpg",
    "00-vilains-2.jpg"
  ]
}
```

### 8.6 Les types (TypeScript) que l'écran applique

Les trois types qui *décrivent exactement* ce fichier, tels qu'ils sont dans le code :

*Extrait de `ui-app/src/board/campagne/contexte.ts` (de « export type ScenarioCampagne » a « export type Campagne = { »).*

```typescript
export type ScenarioCampagne = {
  id: string
  numero: number
  nom: string
  nom_fr?: string
  resume?: string
  enjeu?: string
  final?: boolean
  /** Ce qui perd la campagne sur ce scénario. Seul le scénario final en porte une. */
  defaite?: RegleDefaite
  /** Ce qu'il faut re-préparer avant de rejouer ce scénario après une défaite. */
  reprise?: RegleReprise
  /**
   * Une défaite NE fait PAS rejouer ce scénario : elle a ses propres gains,
   * notés au carnet, et la campagne passe au suivant (Hunting Season, livret
   * p.4 à 9 : « LOSS » donne de l'expérience et des pénalités). Le panneau
   * s'ouvre donc aussi sur une défaite, montre les champs et valide le scénario.
   */
  defaite_continue?: boolean
  pages?: { intro?: string[]; regles?: string[]; epilogue?: string[] }
  victoire?: ChampVictoire[]
}

export type DefinitionCampagne = {
  code: string
  nom: string
  nom_en?: string
  cle_extension: string
  scenarios: ScenarioCampagne[]
  /** Champs présentés à CHAQUE victoire, sauf le scénario final. */
  victoire_commune?: ChampVictoire[]
  victoire_commune_expert?: ChampVictoire[]
  expert?: { pv_persistants?: boolean; obligations?: string[] }
}
```

*Extrait de `ui-app/src/board/campagne/detecteurs.ts` (de « export type ChampVictoire » a « const SEP = ';' »).*

```typescript
export type ChampVictoire = {
  cle: string
  type: 'auto' | 'choix'
  format?: 'liste' | 'int' | 'liste-joueurs'
  parJoueur?: boolean
  obligatoire?: boolean
  detection?: string
  condition?: string
  /**
   * Le carnet CUMULE ce champ d'un scénario à l'autre : la valeur détectée est
   * ce que la partie vient d'ajouter, pas le total. Voir `preRemplir`.
   */
  cumulatif?: boolean
  /**
   * Ce champ se TIRE AU SORT, aux paliers d'une piste chiffrée du carnet.
   *
   * Le livret de Sinister Motives (piste de réputation, p.22) dit trois fois
   * « Choose one "Osborn Tech" attachment at random » : ce n'est pas une décision
   * du joueur, c'est un tirage, donc le jeu peut le faire. `paliers` donne les
   * valeurs de piste qui déclenchent chacun un tirage, et `cle_piste` la clé qui
   * porte le total.
   */
  tirage?: {
    cle_piste: string
    paliers: number[]
  }
  parametres?: {
    compteur?: string
    complot?: string
    type?: string
    zone?: string
    trait?: string
  }
  libelle: string
  aide?: string
  options?: string[]
  /**
   * Un tableau de cases à cocher (« Cooperation Progress » de Skrull Menace) : une ligne par carte,
   * une case par exigence. Le carnet garde « Titre: exigence » pour chaque case cochée.
   */
  cases?: Array<{ titre: string; exigences: string[] }>
}
```

### 8.7 Ce que le panneau fait des champs : l'ordre de priorité du pré-remplissage

Pour chaque champ `auto`, la valeur proposée est la **première** disponible parmi :

1. **le moteur** (`/get_carnet_suggere`) — **seulement si** l'estampille `scenario` du fichier sortant est égale à
   l'`id` du scénario joué (sinon le relevé du moteur est ignoré **en bloc**) ;
2. **le détecteur** déclaré (`detection`) ;
3. **la valeur déjà au carnet** (cumulée, jamais perdue).

Un champ `choix` n'est **jamais** pré-rempli par le moteur. À la validation, le carnet de la campagne devient
`{ ...ancien carnet, ...champs validés }` : **seules les clés déclarées dans la description sont reportées.** Un
champ `auto`/`int` **sans `detection`** est un **drapeau** : la valeur `"0"` ou vide est **retirée** avant
l'enregistrement (sinon le moteur lirait `"0"` comme vrai). Seul `pv_restants` peut produire `"0"` (une vraie mesure,
gardée) ; `compteur_manigance` et `compter_trait` ne rendent rien quand la valeur est 0 : la clé reste absente. Un champ
`parJoueur` est **sauté pour un héros éliminé**, qui échappe aussi à `obligatoire`.

Le panneau est **le même** pour toutes les campagnes et à plusieurs : chaque champ `parJoueur` est saisi par son
siège, tout le reste par l'hôte, seul à valider (`droits-carnet.ts`).

### 8.8 Règles d'écriture (ce que Claude va vérifier : `verifier-livraison-campagne.py` pour la forme, `tools/verifier_campagnes.py` pour les clés)

- [ ] `code` = nom du fichier = dossier de `public/stories/` ; `cle_extension` = clé de `sets_info.json`.
- [ ] `scenarios[].id` : chacun est dans `sets_info.json › scenarios`, a un fichier `data/scenarios/<id>.json`
      (**sans** `_expert` dans l'id) et, si `catalogue`, le fichier cité existe.
- [ ] `numero` : 1, 2, 3… sans trou, **égal au niveau appelé par la face 1A** (§7.3). **Un seul** `final`, sur le dernier.
- [ ] Chaque `victoire[].cle` existe **écrite** dans `campaign.py` (ou est choisie par le joueur) **et lue** par
      `CampaignSetup` (§7.10).
- [ ] Chaque `detection` figure dans la liste du §8.4 ; chaque `condition` est `complot_absent`.
- [ ] `tirage` : paliers croissants, `options` non vide, piste déclarée avant, `type: "auto"`.
- [ ] `deck: "requis"` ⇒ `parJoueur: true`.
- [ ] `options` ne contiennent que des `card_id` qui existent ; les `cases` sont bien formées.
- [ ] Pas de `detection` sur un champ `choix`.
- [ ] `resume`, `enjeu`, `libelle`, `aide` en français ; `nom_en`, `resume_en` en anglais.
- [ ] `pages` : `{}` ou noms conformes à §10.6.


---

## 9. L'écran, le serveur et le fichier d'une campagne en cours

Ce chapitre décrit ce que **Claude** maintient et que tu **n'écris pas**. Tu le lis pour savoir **ce que ta
description de campagne déclenche** et **où tes clés atterrissent**. Les fichiers eux-mêmes sont dans
`commun/ecran/`, `commun/plateau/` et `commun/serveur/` du zip.

### 9.1 Les routes de campagne (`src/engine/device/web/server/server_campagne.py`)

| Route | Méthode | Rôle |
|---|---|---|
| `/list_campagnes_definies` | GET | Les **boîtes** : un en-tête par `data/campagnes/*.json` (`code`, `nom`, `nom_en`, `cle_extension`, `resume`, `resume_en`, `nb_scenarios`), **triées par le numéro de `cle_extension`**. L'écran présélectionne la première (la plus ancienne). |
| `/get_campagne_definition?<code>` | GET | La **description complète** d'une boîte (ton fichier, tel quel), **cherchée par le NOM DE FICHIER** (`data/campagnes/<code>.json`), pas par le `code` interne : d'où l'égalité obligatoire des deux. 404 si inconnu. |
| `/get_carnet_suggere` | GET | Le contenu de `.game/campaign_log_last.json` (§7.5) : `{players_won, scenario, suggestions}`. Fichier absent : 200 avec un carnet vide. |
| `/list_campagnes` | GET | Les campagnes **du joueur**, la plus récente en tête. |
| `/get_campagne?<id>` | GET | Une campagne du joueur. |
| `/get_campagne_en_cours` | GET | La campagne à laquelle appartient la partie en cours (pour **tous** les sièges d'une partie en ligne). |
| `/save_campagne` | POST | Écrit (ou remplace) une campagne du joueur (400 sans `campagne.code`) ; l'`id` vient du nom nettoyé (`[^a-zA-Z0-9_-]` → `_`, 60 caractères, suffixe `_2`, `_3` si pris) ; recalcule `derniere_activite` ; évalue les hauts faits. |
| `/save_carnet_partiel` | POST | **Fusionne** des clés de carnet (un siège distant n'écrit que **ses** champs) : étroit par construction, il ne peut ni terminer un scénario ni gagner une campagne. |
| `/delete_campagne` | POST | Supprime une campagne. |
| `/reinitialiser_enquete` | POST | **Propre à AOS** : nouvelle taupe, preuves rendues. |

### 9.2 Le fichier d'une campagne **en cours** (écrit par `/save_campagne`)

Dossier : `Fusion/marvel-lcg-src/campagnes/<id>.json` (hors de `.game`, qui est reconstruit à chaque lancement).
Le **carnet** qu'il contient est **exactement** le dictionnaire `campaign_log` que le moteur consomme : aucune
traduction entre les deux.

```json
{
  "id": "Hunting_Season",
  "code": "hunting_season",
  "nom": "Hunting Season",
  "difficulte": "standard",
  "equipe": [ { "heros": "spider_man", "nomHeros": "Spider-Man", "identite": ["01001a,01001b"], "deck": { "…": "le deck de départ du joueur" } } ],
  "termines": ["hs_vermin"],
  "carnet": { "Master Hunter": "1", "Player 1 Experience": "3" },
  "tentatives": { "hs_vermin": 1 },
  "partieEnCours": { "scenario": "hs_scorpion", "depuis": "2026-10-09T10:02:45.273Z" },
  "historique": { "hs_vermin": { "Experience": "3" } },
  "perdue": false,
  "scoreFinal": 12,
  "tirage": null,
  "creee": "2026-10-09T10:02:27.588Z",
  "derniere_activite": "2026-10-09T12:02:45"
}
```

| Clé | Sens |
|---|---|
| `termines` | les `id` des scénarios gagnés (ou perdus avec `defaite_continue`) ; la campagne est **finie** quand tous les `scenarios[].id` y sont (sauf règle de défaite) |
| `carnet` | le carnet cumulé |
| `tentatives` | nombre de parties lancées par scénario |
| `partieEnCours` | posée **avant** le lancement, effacée à la validation ; permet de proposer « Reprendre le scénario » |
| `historique` | pour chaque scénario gagné, les champs qu'il a notés (une colonne du carnet imprimé) |
| `perdue` | la règle de défaite l'a perdue ; une campagne perdue ne se rejoue pas |
| `scoreFinal` | le bilan saisi à la fin (`bilan`) |
| `tirage` | **ordre libre** : la progression tirée avant la partie, gardée jusqu'au lancement |
| `secret_aim` | **côté serveur seulement** (AOS) : n'atteint jamais le navigateur |

### 9.3 Le parcours dans l'écran (`public/js/campagne/app.js`, 1 865 lignes)

* **Liste** : une carte par campagne du joueur (couverture du livret + illustration de la boîte, équipe, jauge
  « Étape n / N », difficulté).
* **Création** : boîte, nom, difficulté, nombre de héros. Le bouton « Choisir l'équipe » dépose un **brouillon**
  (`localStorage['mc-campagne-brouillon']`) et envoie sur `/prepare.html?campagne`.
* **Vue campagne (linéaire)** : le **livre ouvert** (pages du livret, voir §10.6), « Ce qui est en jeu » (`resume`,
  `enjeu`), « Mise en place » (la liste des **sets** du scénario : `encounter_sets` + `modular_sets`, par leur
  `name`), les boutons « Lancer le scénario », « Modifier les decks », et — selon la description — « Le Marché »,
  « Cartes de la zone », « Coopération », « L'enquête ».
* **Vue conclusion** : bilan (boîte, difficulté, équipe, scénarios gagnés, parties jouées), `bilan` éventuel.
* **Vue ordre libre** (Fear No Evil) : tableau des affaires, tirage, choix du vilain.
* **Lancement** (`lancerScenario`) : voir §2.3 étape 4. Les modulaires sont **imposés** par le fichier de scénario.
* **« Modifier les decks »** : renvoie à la préparation ; au retour, **l'identité ne doit pas avoir changé** et les
  cartes `deck: "requis"` doivent toujours être dans le deck, sinon refus.

### 9.4 Le panneau de récompenses (plateau, `PanneauRecompenses.tsx`)

S'ouvre à la **victoire**, et à la **défaite** seulement dans trois cas (en ordre libre, la défaite est enregistrée par l'écran des campagnes, pas par ce panneau) : la défaite perd la campagne (`defaite`),
elle demande une re-préparation (`reprise`), ou le scénario a `defaite_continue`. Le panneau **n'existe que si le
monde est de campagne** (`mode_campaign` : règle posée par le lancement), jamais sur une partie ordinaire.

* Il charge la campagne, sa description, le carnet suggéré, puis pré-remplit (§8.7).
* **À plusieurs** : « Envoyer mes champs » (distants) / « Valider et continuer la campagne » (hôte).
* **Mode manuel** : le moteur ne surveille plus la table ; les cases « relevé par le jeu » restent à remplir à la
  main (le panneau le dit).
* Il affiche les **planches d'épilogue** du scénario gagné (`pages.epilogue`).

### 9.5 Ce que tu peux déclarer sans toucher à l'interface, et ce qui demande Claude

| Tu veux… | Possible tel quel ? |
|---|---|
| un nouveau scénario, de nouvelles cartes, de nouvelles récompenses de carnet | **oui** |
| reporter un compteur, une liste de cartes, un drapeau, les PV | **oui** (champs `auto`/`choix`, détecteurs du §8.4) |
| un choix de carte par joueur, un tirage au sort sur une piste, un total cumulé | **oui** |
| des réglages de début de campagne (case, siège) | **oui** (`options_campagne`) |
| un marché ou un solde d'expérience | **oui** (`marche`, comme `gmw` ou `hunting_season`) |
| une défaite qui n'arrête pas la campagne, ou qui la perd | **oui** (`defaite_continue`, `defaite`) |
| un nouveau **détecteur**, un nouveau type de champ, une nouvelle **condition** | **non** → `BESOINS-MOTEUR.md` |
| un **écran** nouveau (carte de la ville, arbre de talents visuel, grille de lieux…) | **non** → `BESOINS-MOTEUR.md`, avec une description de ce que le joueur doit voir |
| un nouveau compteur, trait, message du moteur | **non** → `BESOINS-MOTEUR.md` |
| des cartes qui ne peuvent entrer dans un deck que par la campagne | **non** (liste `SETS_RESERVES_A_LA_CAMPAGNE`) → `BESOINS-MOTEUR.md` |

**Quand tu écris un `BESOINS-MOTEUR.md`**, une entrée = *ce que le livret exige* (page), *ce que le jeu fait déjà de
plus proche*, *ce qui manque*, *la carte ou le champ qui en dépend*, et *ce que tu as fait en attendant* (un
`A_FAIRE_CLAUDE`). Ne propose pas de code d'interface : décris le **comportement attendu**.


---

## 10. Images, textes français, pages du livret, biographies et crédits

Les images sont **fournies par l'utilisateur** : tu ne les produis pas. Tu livres les **tableaux** qui permettent à
Claude de les placer sans ambiguïté, et tous les **textes**.

### 10.1 Les images de cartes : `assets/pics/<card_id>.<jpg|png|webp>`

* **Une image par `card_id`**, nommée exactement comme l'identifiant. **L'extension est obligatoire** (le
  chargeur `engine/file/cache.py` cherche `.webp`, `.jpg`, `.png`). Une face = une image (`wd001a.jpg`, `wd001b.jpg`).
* Une carte `full_link` **n'a pas d'image propre**. Une carte `pic_id` emprunte celle d'une autre.
* **Format** : portrait ≈ **600 × 840** (le petit côté est ramené à 600–615 px). **Les complots (principaux et
  annexes) sont stockés en PAYSAGE** (largeur > hauteur, ≈ 840 × 600 ou 882 × 615), texte à l'horizontale :
  **le serveur les fait pivoter en portrait en les servant** (`ImageLib.TryRotateImage`) et le plateau les
  retourne à l'affichage. **Ne les pré-tourne pas.**
* Les **miniatures** de la table (`assets/vignettes/`, `tools/generer_vignettes.py`) sont **générées** : rien à livrer.
* Les scans de **haute définition** (`/hd/…`) et **français** (`assets/pics-fr/`) ne concernent que le contenu officiel.

**Ton livrable : `integration/images.md`**, un tableau (une ligne par face) :

| `card_id` | Fichier source (nom dans le dossier de l'auteur) | Orientation | Remarque (recto/verso, copie, art alternatif, qualité) |
|---|---|---|---|
| `wd001a` | `Scenarios/Shocker/1A Shocker.png` | portrait | |
| `wd002a` | `Scenarios/Shocker/2A Shock Party.png` | **paysage** | complot principal |

**Une carte en plusieurs exemplaires physiques n'a qu'une image** (celle du `card_id` répété dans les sets).

### 10.2 L'image de la boîte : `assets/textures/sets/<cle_extension>.webp`

Le nom du fichier est **exactement** la `cle_extension` (`21. The Mad Titan's Shadow.webp`,
`120. Custom (Web of Deceit).webp`). C'est elle que l'écran des campagnes affiche en illustration de la boîte
(`/sets/<clé>`). Pour une campagne maison, l'utilisateur fournit la pochette ou une illustration ; indique-le
dans `images.md`. La pochette recadrée (`public/img/prepare/boites/<n>.webp`) est **générée** par
`outils/pochettes-boites.py` : Claude ajoute le rectangle de recadrage.

### 10.3 Le texte français de chaque carte fan-made — **obligatoire à chaque pack**

Un pack livré sans ce texte laisse **toutes ses cartes sans tooltip français, et rien ne le signale**. Le plateau
cherche le français d'une carte dans cet ordre : (1) un scan français (`assets/pics-fr/`) ; (2) le texte officiel
(`textes-fr.ts`, **généré**, ne jamais éditer) ; (3) **`ui-app/src/board/textes-fr-fanmade.ts`**, **écrit à la
main** ; (4) marvelcdb en ligne (coupé par défaut et sans effet sur du fan-made). **Une carte fan-made n'a ni scan
français ni page marvelcdb : la ligne (3) est le seul français que le joueur verra dessus.**

**Ta livraison** : `integration/textes-fr/<pack>.fragment.txt`, **une entrée par `card_id`, y compris pour les
exemplaires en double** (recopie le même texte), au format exact du fichier :

```
  // <pack> — <Nom de la carte> (<Type>)
  '<card_id>': "texte français avec <b>balises</b>, [star], [[TRAIT]]…",
```

**Entrées réelles de Hunting Season** (modèle de forme ; Web of Deceit a aussi ses 176 entrées `wd…`) :
```typescript
  // hunting_season — Vermin (Villain)
  'hs001': "[star] <b>Réponse forcée</b> : après que Vermin s'est activé contre vous, défaussez la carte du dessus du deck Rencontre. Si un sbire [[RAT]] a été défaussé de cette façon, mettez-le en jeu engagé avec vous.",
  // hunting_season — Vermin (Villain)
  'hs002': "[star] <b>Réponse forcée</b> : après que Vermin s'est activé contre vous, défaussez les 2 cartes du dessus du deck Rencontre. Mettez en jeu engagé avec vous le premier sbire [[RAT]] défaussé de cette façon.",
  // hunting_season — Vermin (Villain)
  'hs003': "[star] <b>Réponse forcée</b> : après que Vermin s'est activé contre vous, défaussez les 2 cartes du dessus du deck Rencontre. Mettez en jeu engagé avec vous chaque sbire [[RAT]] défaussé de cette façon. Résolvez l'effet \"Spécial\" d'Even More Rats.",
  // hunting_season — Rats and More Rats (MainScheme)
  'hs004a': "<b>Contenu</b> : Vermin (I) et Vermin (II). <i>(Vermin (II) et Vermin (III) à la place en mode expert.)</i> Sets de rencontre Vermin et Standard. Un set de rencontre modulaire <i>(recommandé : Feral Instincts)</i>.\n<b>Mise en place</b> : mettez en jeu l'environnement Even More Rats. Mettez en jeu un sbire Regular Rats engagé avec chaque joueur. Mélangez le deck Rencontre. Passez à l'étape 1B.",
  // hunting_season — Rats and More Rats (MainScheme)
  'hs004b': "[star] <b>Réponse forcée</b> : après l'étape 1 de la phase du méchant, placez 1 menace sur chaque sbire [[RAT]]. Résolvez l'effet \"Spécial\" d'Even More Rats.",
  // hunting_season — Rats, Rats and More Rats (MainScheme)
  'hs005a': "<b>Une fois révélée</b> : cherchez Bringer of Plague dans le deck Rencontre et la pile de défausse, et révélez-la. Passez à l'étape 2B.",
```

**Vocabulaire officiel (Guide de référence v1.8 FR) — la gate `vocabulaire-statuts.test.ts` échoue sinon :**

| Anglais | Français | **Interdit** |
|---|---|---|
| Stunned / Confused | Sonné / Désorienté | « étourdi » |
| Tough (carte d'état) / Toughness | carte d'état **Tenace** / **Ténacité** | « Robustesse » |
| Stalwart | **Robuste** | « Inébranlable » |
| Steady | **Solide** | « Stable » |
| Surge / Overkill | Renfort / Déferlement | |
| Piercing / Ranged | Perçant / Distance | |
| Villainous | Vilenie | |
| Incite X / Hinder X | Incitation X / Entrave X | |
| When Revealed | **Une fois révélée** (manigance, traîtrise) | |
| When Defeated (personnage) | **Une fois vaincu** | |
| When Defeated (manigance) | **Une fois déjouée** | |
| Forced Interrupt / Forced Response | Interruption forcée / Réponse forcée | |
| Hero Action / Hero Response / Alter-Ego Action | Action de héros / Réponse de héros / Action d'alter ego | |
| ATK / THW / DEF / REC / SCH | ATQ / CTR / DEF / REC / MNG | |
| counter / token | **jeton** (compteur de carte) ; « pion Accélération » ; « compteur polyvalent » (all-purpose) | |
| stage | stade (« achevé ») | |
| boost / star icon | champ de boost / icône d'étoile | |
| Aggression / Justice / Leadership / Protection | Agressivité / Justice / Leadership / Protection | |
| deck / encounter deck / victory display | deck / deck Rencontre / pile de victoire | |
| exhaust / ready | incliner / redresser | |

* **Noms propres et traits `[[…]]` laissés en ANGLAIS** : le joueur a la carte anglaise sous les yeux.
* **Jetons recopiés tels quels** : `[mental]`, `[physical]`, `[energy]`, `[wild]`, `[star]`, `[per_hero]`,
  `[crisis]`, `[acceleration]`, `[hazard]`, `[amplify]`, `[boost]`.
* Cherche **toujours** comment une phrase équivalente est rendue sur une carte **officielle**
  (`ui-app/src/board/textes-fr-complets.ts`) avant d'écrire la tienne ; les textes d'ambiance (italiques de
  récit) se traduisent comme le reste.
* « est censé(e) » (jamais « devrait ») ; « n'importe quelle quantité de dégâts » ; « perd le texte imprimé dans
  sa boîte de texte » ; « choisissez : soit vous inclinez…, soit vous… ».

### 10.4 Les textes de l'interface de la description de campagne

`resume`, `enjeu`, `libelle`, `aide`, `nom_fr` sont **en français** (ce sont les clés de traduction). Pour
l'interface **en anglais**, l'écran passe ces chaînes à `t()` (dictionnaire français → anglais :
`public/js/prepare/dico-en.js`, `ui-app/src/board/dico-en.ts`). **Une chaîne sans entrée reste en français**
dans l'interface anglaise. Liste, dans `BESOINS-MOTEUR.md`, les chaînes **nouvelles** avec leur traduction
anglaise : Claude les ajoute au dictionnaire.

### 10.5 Biographies (survol dans l'écran de choix)

* **Vilain** — `public/js/prepare/mechants-info.js`, indexé par le **`card_id` de la première face du vilain**
  du scénario (jamais par le nom : plusieurs vilains partagent un nom). Texte sur le **personnage**, jamais sur
  sa mécanique. Tout champ est facultatif sauf `bio`/`bioEn` ; mieux vaut omettre que d'inventer :

```js
"hs001": {
    bio:   "3 ou 4 phrases : origine, pouvoirs, ce qui définit le personnage.",
    bioEn: "Same, in English.",
    civil: "Joseph",
    equipes: "Maggia",       equipesEn: "Maggia",
    ennemis: "Spider-Man",   ennemisEn: "Spider-Man",
    apparition: "The Amazing Spider-Man #113 (1972)",
},
```

  Tu livres `integration/public/js/prepare/mechants-info.fragment.js` (les entrées seules).
* **Héros** — `public/js/prepare/heros-info.js`, indexé par le `card_id` de la **face héros** (même forme + `base`,
  `civilEn`, `baseEn`) ; seulement si la campagne apporte un héros.

### 10.6 Les pages du livret : `public/stories/<code>/`

L'écran affiche le livret en **double page** qu'on tourne. Les pages sont des **images carrées de 975 × 975 px**
(rendues depuis le PDF du livret : les livrets officiels sont des PDF vectoriels aux pages carrées de 540 points,
facteur 1,806). Nommage **par rôle** :

| Fichier | Rôle |
|---|---|
| `00-couverture.jpg` | couverture du livret (page 1 d'un livret officiel) ; à défaut, l'illustration de la boîte |
| `00-campagne-intro-<n>.jpg` | planche d'ouverture de la campagne (référencée par `pages_intro`) |
| `00-campagne-regles-<n>.jpg` | règles générales de la campagne (`pages_regles`) |
| `00-campagne-expert-<n>.jpg` | règles de la campagne experte (`pages_expert`) |
| `<NN>-<scénario>-intro-<n>.jpg` | planche de bande dessinée d'ouverture du scénario `NN` (numéro sur 2 chiffres) |
| `<NN>-<scénario>-regles-<n>.jpg` | page de règles du scénario |
| `<NN>-<scénario>-epilogue-<n>.jpg` | planche de fin (montrée par le panneau après la victoire) |
| `fr/<même nom>.jpg` | la même page **refaite en français** (active si `livret_fr: true`) |
| `00-vilains-<n>.jpg` | portraits des sous-fifres (ordre libre) |

Dans un livret, la page **paire** porte la bande dessinée et la page **impaire** d'en face les règles du même
scénario. Une planche qui termine un scénario **et** ouvre le suivant n'est **pas dupliquée** : elle garde son
nom d'épilogue et le scénario suivant la référence comme intro.

**Ton livrable : `integration/livret-pages.md`**, au format que lit `tools/pages_livret.py` (`CARTES`), qui dit
**quelle page du PDF joue quel rôle** (c'est « le vrai travail » de cet outil) :

```python
"<code>": {
    "pdf": "<fichier du livret>.pdf",
    "regles_campagne": [4, 5],            # pages de règles de la campagne
    "scenarios": [                        # (id, numero, page_intro, [pages_regles], page_epilogue)
        ("ebony_maw", 1, 5, [6, 7], 8),
        ("the_tower_defense", 2, 9, [10, 11, 12, 13], 14),
        ("hs_vermin", 1, None, [4], None),   # pas de planche : le récit et les règles partagent la page
    ],
},
```

**Exemple réel** (Hunting Season, livret fan-made à pages portrait, sans planche de BD) :
*Extrait de `Fusion/marvel-lcg-src/tools/pages_livret.py` (de « "hunting_season": { » a « "next_evol": { »).*

```python
    "hunting_season": {
        # Livret fan-made (Nugget), portrait, livre dans le zip du pack. Pas de
        # planches de BD : le recit et les instructions partagent la page du
        # scenario, d'ou des scenarios sans intro ni epilogue a part.
        "pdf_depot": ".planning/hunting-season/reference/HuntingSeason_Campaign_Booklet.pdf",
        # p2 : regles du mode campagne. p3 : mode Hunter, experience, Lodge.
        # La p11 (regles de la campagne experte) finit le scenario de Kraven.
        "regles_campagne": [2, 3],
        "scenarios": [
            ("hs_vermin", 1, None, [4], None),
            ("hs_scorpion", 2, None, [5], None),
            ("hs_the_lizard", 3, None, [6, 7], None),
            ("hs_vulture", 4, None, [8, 9], None),
            ("hs_kraven_the_hunter", 5, None, [10, 11], None),
        ],
    },
```

Le livret **français** d'une campagne fan-made est refait par `tools/livret_fr.py` à partir d'un fichier de
traductions `tools/livrets_fr/<code>.json` (une entrée par bloc de texte du PDF, `p<page>b<bloc>`) : si tu
traduis le livret, livre ce fichier ; sinon laisse `livret_fr` à `false`.

### 10.7 Le préfixe : `tools/prefixes_fanmade.json`

Fragment à livrer (`integration/tools/prefixes.<pack>.fragment.json`) ; **forme exacte** (entrée du préfixe `hs`) :
```json
{
  "hs": {
    "pack": "hunting_season",
    "libelle": "178. Custom (Hunting Season)",
    "cartes": 239,
    "depuis": "2026-10-08",
    "note": "Auteur Nugget. Campagne en cinq scenarios (Vermin, Scorpion, The Lizard, Vulture, Kraven), 239 entrees JSON pour 226 cartes physiques, Lodge, mode expert et Hunter. Portage du 08/10/2026, dossier source .planning/hunting-season/."
  }
}
```

`cartes` = nombre de **faces** du pack ; `depuis` = date ; `note` = auteur, contenu, particularités.

### 10.8 Crédits

Les **créateurs** sont crédités **automatiquement** par la clé `custom` de chaque carte (§4.2) : filtre
« Fan-made » de l'écran de préparation, pastille CUSTOM du deck-builder, remerciements. **Renseigne `custom` sur
toutes les cartes, faces d'identité comprises.** Livre en plus `integration/CREDITS.md` : l'auteur de la
campagne (nom exact et pseudonyme), l'équipe (organisateurs, développeurs, testeurs, traducteurs, éditeur du
livret français), le lieu et la date de l'événement s'il y en a un, et les **illustrateurs** imprimés sur les
cartes. Claude les place dans les remerciements du jeu.

### 10.9 Ce que tu **n'écris pas** dans cette chaîne

Les checksums de `cards.json`/`sets_info.json` ; les vignettes ; les scans HD/FR ; `textes-fr.ts` ;
`public/js/traduction/*` (générés) ; `dico-en` ; `data/translate_fr.json` (narration du moteur, traduite par
gabarit) ; l'éditeur de pochettes ; les hauts faits.


---

## 11. Prouver que ça marche : les gates, les cas de test, les épreuves de campagne

**Tu ne peux pas lancer le moteur.** Claude le lance. Mais tu **écris** ce qui permet de le prouver : les cas de
test de chaque capacité et les épreuves de la boucle de campagne. Ce chapitre dit **ce que Claude exécutera**, pour
que tu écrives des preuves **exécutables du premier coup**, et ce que tu dois **ne jamais prétendre**.

> **Règle de tout le projet : une gate qui répond « OK » n'est pas une preuve tant qu'on ne l'a pas vue ÉCHOUER.**
> Un test qui ne peut pas échouer ne prouve rien. Pour chaque cas que tu écris, indique **ce qui doit être
> rouge** si la capacité est absente (« preuve par substitution »).
>
> **Tu ne coches jamais « vert »** : tu n'as exécuté aucun test. Dans `AUTO-VERIFICATION.md`, tu écris ce que
> tu as vérifié **statiquement** (forme, cohérence, vérificateur de livraison) et ce qui reste **à exécuter par
> Claude**. (Une livraison antérieure a prétendu des tests en jeu à partir d'une simple vérification statique : ne
> le refais pas.)

### 11.1 Les cinq niveaux de preuve d'une campagne

| Niveau | Quoi | Outil | Qui |
|---|---|---|---|
| **1. Forme** | JSON valides, clés, références croisées, préfixes, noms de dossiers, vocabulaire FR | `verifier-livraison-campagne.py` (zip) ; `verifier_prefixes.py` ; `verifier_coherence_cartes.py` ; `verifier_desc_mots_cles.py` | **toi** (le premier) puis Claude |
| **2. Construction** | Chaque carte se génère ; chaque script compile ; aucun appel inexistant | `test_cards.py`, `verifier_api_cartes.py`, `verifier_appels_modules.py`, `compileall` | Claude |
| **3. Capacité** | Chaque capacité fait **exactement** ce que dit le texte, vérifiée sur une position réelle | `tools/test_capacites.py` (cas dans `tools/cas/<bloc>.py`) + substitution | toi écris, Claude exécute |
| **4. Boucle de campagne** | Le carnet est écrit à la victoire, relu à la mise en place **suivante** | `tools/test_campagnes.py` (épreuves dans `tools/epreuves_campagnes.py`) | toi écris, Claude exécute |
| **5. Partie jouée** | Aucune partie ne plante ni ne se fige ; la clé de carnet atterrit | `tools/autoplay.py`, `tools/sonde_campagne.py`, puis un humain dans le navigateur | Claude, puis l'utilisateur |

### 11.2 Niveau 3 : un cas de test de capacité (`tools/cas/<bloc>.py`)

Le fichier est **découvert automatiquement** (`glob` de `tools/cas/*.py`). Il expose `CAS = [...]` et, si besoin,
`VERIFICATIONS = r'''...'''` (du code Python de vérification). Les noms des cas sont préfixés (`[hu]`) pour
pouvoir les filtrer. **Un cas = un processus** (le moteur est un singleton) : monte une position, déclenche,
mesure l'état du monde.

**Un fichier réel complet de cas** (Hala Ultimatum, Galactic Storm), pour la forme :
*Extrait de `Fusion/marvel-lcg-src/tools/cas/hala_ultimatum.py` (de « # Cas test_capacites du scenario 3 HALA ULTIMATUM » a « # ============================================================== Avancee de stade (native) garde le cote »).*

```python
# Cas test_capacites du scenario 3 HALA ULTIMATUM de Galactic Storm (gs138-gs155), lot GS-6 (20/10/2026).
# Format identique a tools/cas/kree_sentry.py ; noms prefixes `[hu]` (filtre : `[hu]`, ou `[hu] gs144 ` pour
# une carte).
#
# Conventions de ce fichier :
#  - le heros de test (Spider-Man, 01001) demarre en ALTER EGO ; `HEROS` le met en heros.
#  - la mise en place REELLE du scenario tourne a chaque cas (scenario=SC) : Hala (gs143) en jeu, Kree
#    Leader (I) (gs138a, HIDDEN) en jeu.
#  - priorite donnee a la mecanique HIDDEN (les deux moities, le flip, l'avancee de stade qui garde le
#    cote DISCOVERED) : c'est le coeur neuf du lot. Les autres cartes (attachements, sbires, manigances
#    annexes, traitrises) ont un cas de construction/texte chacune, sans aller jusqu'a la preuve par
#    substitution systematique faute de temps (consigne dans le rapport de fin de lot).
SC = "gs_hala_ultimatum"
HEROS = "Puzzle.ChangeForm('01001b')"
DECK_NEUTRE = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01186', '01186', '01186', '01186')"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[hu] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "hu_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ============================================================== HIDDEN, moitie attaque (NEUF)
    _c("gs138a HIDDEN, moitie attaque : le mechant attaque le heros -> aucun degat, 1 carte de rencontre "
       "face cachee distribuee",
       "« whenever a player would be attacked by the villain, that player is dealt a facedown encounter "
       "card » : Message.WhenUnitWouldAttack + SetBeInstead (modele AbilityFactoryEnemy.EnemyCannotActivate) "
       "+ Player.DealEncounterCards (modele ar012 Ares)",
       DECK_NEUTRE + [HEROS], ["Puzzle.Attack('gs138a')"],
       {"degats_identite": 0, "cartes_distribuees": 1}),
    _c("gs138a HIDDEN, moitie attaque, TEMOIN (sans HEROS en forme heros, meme attaque) : toujours aucun "
       "degat, une carte distribuee",
       "la redirection ne depend pas de la forme du joueur vise",
       DECK_NEUTRE, ["Puzzle.Attack('gs138a')"],
       {"degats_identite": 0, "cartes_distribuees": 1}),
    # ============================================================== HIDDEN, moitie immunite (wiring)
    # NOTE : la moitie immunite (CannotBeAffectedByPlayerCards) est deja testee en general par
    # briques_communes.py (14 cas, filtre [briques][immunite]) ; ce cablage (while_fn=HasTrait('HIDDEN'))
    # n'a PAS de cas dedie ici — `Puzzle.Stun`/`Puzzle.Tough` passent par `DebugRule`, qui CONTOURNE la
    # protection par construction (c'est voulu : le harnais doit pouvoir forcer un etat pour construire un
    # scenario de test), donc inadapte a la preuve. A verifier en partie reelle avec une vraie carte joueur
    # ciblant le mechant HIDDEN (voir questions du lot).
    _c("gs138a HIDDEN, attachements indiscutables : un Grand-High Pursuer attache ne peut pas etre "
       "defausse tant que le mechant est HIDDEN",
       "« Attachments attached to the villain cannot be discarded » : WhenCardWouldDiscard + SetBeInstead "
       "(modele skrull_menace/paibok RegleDesPouvoirs)",
       ["Puzzle.PutIntoPlay('gs144')"], ["Puzzle.Discard('gs144')"], {"en_jeu": ["gs144"], "attaches": [["gs138a", "gs144"]]}),
    _c("gs138a HIDDEN, attachements indiscutables, TEMOIN : une fois DISCOVERED (Tanalth), le meme "
       "attachement SE DEFAUSSE normalement",
       "la protection est imprimee seulement sur la face HIDDEN : elle tombe au retournement",
       ["Puzzle.PutIntoPlay('gs144')", "Puzzle.Flip('gs138a')"], ["Puzzle.Discard('gs144')"],
       {"hors_jeu": ["gs144"]}),
    # ============================================================== Flip HIDDEN -> DISCOVERED (gs142a)
    _c("gs142a When Revealed : flip le mechant vers DISCOVERED, met Hala de cote, chaque joueur pioche 1 "
       "carte — attachements et degats du stade HIDDEN sont CONSERVES (meme carte)",
       "« Flip the villain to its DISCOVERED side and set the Hala environment aside. Each player draws 1 "
       "card » : villain.card.Flip(effect) (modele gob/risky_business 02006a, sk189a Veranke) ; "
       "Faces.SetAside (Hala) ; Players.ForEachPlayer + DrawUp",
       ["Puzzle.PutIntoPlay('gs144')", "Puzzle.Damage('gs138a', 3)"], ["Puzzle.AdvanceMainScheme(1)"],
       {"en_jeu": ["gs138b"], "hors_jeu": ["gs138a", "gs143"], "attaches": [["gs138b", "gs144"]],
        "degats": [["gs138b", 3]]}),
```

**Les clés d'un cas :**

| Clé | Sens |
|---|---|
| `nom` | **commence par le préfixe du bloc** ; **contient le `card_id` testé** (« le cas doit être sujet ») |
| `pourquoi` | la phrase imprimée visée et la fabrique/carte modèle utilisée |
| `scenario` | le scénario monté (`data/scenarios/<id>.json`) |
| `heros` | un deck de départ ; `heros2` : un second joueur (obligatoire pour « any player », « each player ») |
| `mise_en_place` | commandes `Puzzle.*` exécutées **avant** le déclenchement (seul `ChangeForm` va ici, avec les créations de decks) |
| `declencher` | commandes `Puzzle.*` qui provoquent la capacité |
| `verifier` | le nom de la fonction de vérification (`etat_attendu` par défaut) |
| `attendu` | l'état attendu (ci-dessous) |

**Les commandes `Puzzle.*` réellement disponibles** (lues dans `game/puzzle/puzzle.py`) :
```text
Puzzle.FindOrCreateFace(card)
Puzzle.CreateCard(card_name)
Puzzle.FindCommandCards(*cards)
Puzzle.CreateEncounterDiscardPile(*cards)
Puzzle.EmptyEncounterDeck()
Puzzle.EmptyEncounterDiscardPile()
Puzzle.RemoveNemesisAside()
Puzzle.CreateEncounterDeck(*cards)
Puzzle.CreateHandCards(*cards)
Puzzle.CreatePlayerDiscardPile(*cards)
Puzzle.EmptyPlayerDeck()
Puzzle.EmptyPlayerDiscardPile()
Puzzle.EmptyPlayerAdditionalDeck()
Puzzle.CreatePlayerDeck(*cards)
Puzzle.EmptyHand()
Puzzle.EmptyAdditionalDeck()
Puzzle.PutOnAdditionalDeckTop(*cards)
Puzzle.CreatePlayerAdditionalDeck(*cards)
Puzzle.Gain(*cards, call_back=None)
Puzzle.Draw(num)
Puzzle.Ready(*cards)
Puzzle.Exhaust(*cards)
Puzzle.Discard(*cards)
Puzzle.Remove(*cards)
Puzzle.Flip(*cards)
Puzzle.Heal(card, val)
Puzzle.Damage(card, val, source=None)
Puzzle.PlaceCounters(card, name, val)
Puzzle.Confuse(card)
Puzzle.Stun(card)
Puzzle.Tough(card)
Puzzle.AddTough(card, n=1)
Puzzle.Expose(card)
Puzzle.Cloak(card)
Puzzle.Daze(card)
Puzzle.RevealDealtCards()
Puzzle.RemoveMinionsInPlay()
Puzzle.AddCloak(card, n=1)
Puzzle.AddStatus(card, name, n=1)
Puzzle.Intensify(card, n=1)
Puzzle.ChangeToFace(card, to)
Puzzle.ChangeForm(card, rule='')
Puzzle.PlaceThreat(card, val)
Puzzle.SetThreat(card, val)
Puzzle.Counter(card, name, size=3)
Puzzle.Token(card, name, size=3)
Puzzle.Reveal(card, call_back=None, by=None)
Puzzle.PutIntoPlay(card, under_control=False, exhaust=False, player=None)
Puzzle.PlaceUnder(card, host, face_up=False)
Puzzle.TurnEncounterTopFaceUp()
Puzzle.Boost(card)
Puzzle.Deal(card, joueur=None)
Puzzle.FindFaceInPlay(card)
Puzzle.Attack(card, defender=None, against=None)
Puzzle.EnemyAttacks(card, target, defender=None, overkill_to=None, joueur=None)
Puzzle.ProtectFromPlayerCards(card, attached_to=None, trait=None)
Puzzle.SetVillainRule(the_villain='Active', player_cards='TheVillain')
Puzzle.SetActiveVillain(card)
Puzzle.RemoveVillain(card)
Puzzle.BuildVillainDeck(*cards)
Puzzle.RevealNextVillain()
Puzzle.Defend(card, attacker)
Puzzle.Thwart(card)
Puzzle.EndPlayerTurn()
Puzzle.EndPlayerPhase()
Puzzle.EndVillainPhase()
Puzzle.RunVillainPhase()
Puzzle.BeginVillainPhase()
Puzzle.Scheme(card)
Puzzle.Action(card, type=None, index=0)
Puzzle.MoveTo(card, zone, position='Top', player=0, siege=None, face_cachee=False)
Puzzle.ShuffleDiscardIntoDeck(zone, player=0, siege=None)
Puzzle.DrawUpToHandSize(player=0, siege=None)
Puzzle.EndRound()
Puzzle.SwapWithDeckTop(card, player=0, siege=None)
Puzzle.Mulligan(*cards, player=0, siege=None)
Puzzle.Shuffle(zone, player=0, siege=None)
Puzzle.Attach(card, cible)
Puzzle.AttachReel(card, cible)
Puzzle.Engage(card, player=0, siege=None)
Puzzle.PutIntoDeck(*cards)
Puzzle.AdvanceMainScheme(fois=1, to=None)
Puzzle.AdvanceVillain()
Puzzle.Win()
Puzzle.Lose()
Puzzle.End(message='')
```

⚠ **`Puzzle.*` désigne une carte par son NOM (ou son `card_id` pour les cartes de rencontre/joueur), jamais par le
`card_id` d'une identité** : `Puzzle.ChangeForm('Amadeus Cho')`, pas `Puzzle.ChangeForm('68001b')` (un `card_id`
d'identité fabrique une carte orpheline et plante le rendu). **Désigne toujours une carte par son `card_id` quand
le nom n'est pas unique** (deux « Venom Blast » existent).

<!-- extrait de docs/reference/GUIDE-CREATION-CONTENU.md -->
Quatre clés du harnais servent à rendre un cas DÉTERMINISTE. Sans elles, la
relecture du pack `madame_web` serait passée à côté de deux vrais défauts :

| Clé | À quoi elle sert |
|---|---|
| `main_exclusive` | **Vide la main** puis y dépose les cartes listées. Avec `main` seul, la main de départ reste là et le pilote y pioche ses ressources : le bonus « payé uniquement en [physical] » d'Ashley Barton se testait avec un paiement `R Y`, donc jamais. |
| `cibles` | Désigne des cibles précises, par `card_id`. Indispensable dès que le minimum de cibles est 0 (« exhaust up to X allies ») : le pilote envoie toujours le MINIMUM, donc rien. |
| `surpayer` | `True` : dépense tout ce qui est disponible, dès le PREMIER paiement du cas. Sans cela, une carte à **coût X** annonce un coût nul, le pilote ne paie rien, X vaut 0 et la carte paraît inerte alors qu'elle est correcte. `"<card_id>"` (ou une liste, depuis le 11/09/2026) : ne surpaie QUE le jeu de cette carte, ce qui permet de payer une première carte normalement (avec `payer_avec`) puis d'en surpayer une seconde : indispensable à tout effet qui se lit sur la carte dépensée SUIVANTE (yd007 Jackpot!). |
| `payer_avec` | Impose quelles cartes financent le coût. Utile quand la ressource dépensée a elle-même un effet (The Power of Forgiveness) — mais elle ne peut que PRIORISER parmi les candidats proposés par le moteur : pour un contrôle total, préférer `main_exclusive`. |

<!-- extrait de docs/reference/GUIDE-CREATION-CONTENU.md -->
Le vérificateur générique `etat_attendu` couvre la majorité des cas sans écrire
une seule fonction. Clés disponibles : `attributs`, `traits`, `en_jeu`,
`hors_jeu`, `compteurs`, `jetons`, `compteurs_total`, `menace`,
`attributs_carte`, `degats`, `degats_min`, `degats_identite`,
`dans_deck_rencontre`, `forme`, `en_jeu_trait`, `exhausted`, `pret`,
`statuts`, `taille_main`, `en_main`, `defausse`, `defausse_joueur`.
Deux pièges : **`jetons` et `compteurs` sont deux stocks distincts** (la menace
posée sur une carte joueur, façon Beat Cop, est un JETON `threat` — la
contrôler avec `compteurs` renvoie toujours 0, donc un test qui passe pour de
mauvaises raisons) ; et **`defausse` est le seul moyen de prouver qu'un
événement a été JOUÉ**, puisqu'une carte restée en main n'est pas « en jeu »
non plus et satisfait donc `hors_jeu`.

**Ce qu'un bon cas respecte** (`PROCESSUS-CARTE.md`, étape 7) :

1. **Sujet** : le `card_id` est dans le nom du cas.
2. **Preuve par substitution** : retirer le module → **rouge** ; le remettre → **vert**. (Un contre-cas d'*absence*
   d'effet reste vert sous substitution : écris-le dans le gabarit.)
3. **Un cas va jusqu'au bout** de ce que la carte annonce : si elle fait deux choses, il mesure les deux.
4. **Se méfier des effets de la partie, pas seulement de la carte** : une carte du deck jouée par le pilote peut
   fausser la mesure ; fixe la main (`main_exclusive`).
5. **Toute limite imprimée** (« once per round ») exige un **témoin d'épuisement** : deux déclenchements dans le
   même round, et un **chiffre** mesuré au second.
6. **Une capacité de tour de jeu** : `Puzzle.Attack` / `Puzzle.Scheme` / `Puzzle.Action`.

### 11.3 Niveau 4 : une épreuve de boucle de campagne (`tools/epreuves_campagnes.py`)

Une **épreuve** enchaîne **deux parties** dans le même processus : la partie 1 est montée en mode campagne avec
un carnet entrant ; on pose l'état que la récompense exige (`avant`) ; on **termine** la partie à la demande
(`Puzzle.Win()` / `Puzzle.Lose()`) ; on relit le carnet **sortant** ; on y fusionne ce que le joueur **coche**
(`choix`, comme le ferait le panneau) ; la partie 2 est montée avec ce carnet, et on mesure ce qu'il a changé.

*Extrait de `Fusion/marvel-lcg-src/tools/epreuves_campagnes.py` (de « """Les EPREUVES de boucle de campagne » a « EPREUVES = [] »).*

```python
"""Les EPREUVES de boucle de campagne, boite par boite.

Lue par `tools/test_campagnes.py`, qui est generique : ce fichier-ci est la
connaissance de chaque boite — ce qu'une victoire laisse au carnet, et ce que
le carnet doit changer a la mise en place SUIVANTE.

Forme d'une epreuve
-------------------
    {
      "nom":       ce qui sera lu au rapport ; commence par le code de la boite
      "scenario":  le scenario de la partie 1 (data/scenarios/<id>.json)
      "heros":     un nom de deck de depart, ou une liste pour le multijoueur
      "carnet":    le carnet ENTRANT de la partie 1 (facultatif)
      "avant":     commandes `Puzzle.*` posant l'etat que la recompense exige
      "fin":       "Win" (defaut) ou "Lose"
      "carnet_attendu": {gagnee, scenario, cles, cles_presentes, cles_absentes}
      "choix":     ce que le JOUEUR coche au panneau, fusionne au carnet sortant
      "suivant":   le scenario de la partie 2 (absent = on s'arrete au carnet)
      "attendu":   l'etat attendu APRES la mise en place de la partie 2
    }

`attendu` connait : en_jeu, main, deck, defausse, retirees, victoire, de_cote
(et leur negation `pas_<zone>`), en_jeu_trait, compteurs, statuts, menace,
taille_main, taille / taille_min / taille_max (par pile, « deck », « deck@2 »),
compteurs_total, perdue (la mise en place perd la partie),
parmi (la carte est dans l'une des piles citees), un_parmi / aucune_parmi
(au moins une, ou aucune, des cartes citees dans une pile), menace_max, et la zone
« rencontres_recues » (cartes rencontre distribuees face cachee),
pv_identite, degats_identite, degats (sur une carte quelconque). Une entree de zone peut etre
`[card_id, joueur]` pour viser un autre siege.
"""
```

**Ce que tu livres** : `integration/tools/epreuves.<code>.fragment.py`, qui commence par `EPREUVES += [` et contient
**au moins** :

* **une épreuve par scénario** qui vérifie le **carnet sortant** (`carnet_attendu: {"gagnee", "scenario", "cles",
  "cles_presentes", "cles_absentes"}`) — **dont l'estampille `scenario`**, qui doit égaler l'`id` du scénario ;
* **une épreuve par récompense** (et par pénalité) : `partie 1` écrit la clé, `partie 2` (`suivant`) montre
  l'effet (`attendu`) — **et son témoin** (le même scénario **sans** carnet, où l'effet est **absent**) ;
* **une épreuve de défaite** : le carnet reste intact, rien n'est coché ;
* **une épreuve expert** par règle expert (PV persistants, soin contre pion, obligation de soin).

**Épreuves réelles de The Mad Titan's Shadow** (les cinq scénarios d'une boîte officielle) :
*Extrait de `Fusion/marvel-lcg-src/tools/epreuves_campagnes.py` (de « L'Ombre du Titan Fou (mts) » a « Les plus recherches de la galaxie (gmw) »).*

```python
# ================================== L'Ombre du Titan Fou (mts) — 5 scenarios
#
# La boite la plus riche en recompenses AUTOMATIQUES : le moteur
# (`cards/pack/mts/campaign.py`, `CollectMTS`) regarde l'etat de la table a la
# fin de la partie et en deduit tout seul ce que le joueur emporte. Deux
# familles :
#   — « Campaign Pool: X » : un renfort (Cosmo, Black Swan, Odin, Norn Stone)
#     ou une nuisance (Security Breach, Shawarma, System Shock) verse a la
#     reserve de campagne, relu par `InPool` a la mise en place suivante ;
#   — les deux PUNITIONS (« Avengers Tower Damaged », « The Infinity Stones 1B
#     completed »), relues par `LogSet`, qui frappent des la mise en place.
# Chaque epreuve joue la partie qui PRODUIT la cle, puis monte la partie qui
# la SUBIT : c'est la chaine entiere, pas la moitie.
EPREUVES += [
    {
        "nom": "mts — Cosmo libere au scenario 1 : le carnet le note, et il entre en jeu sous controle au scenario 3",
        "scenario": "ebony_maw",
        "heros": "captain_america",
        # 21180a « Secure the Landing Pad » vaincu se retourne sur 21180b
        # « * Cosmo » : c'est cette face que CollectMTS cherche en jeu.
        "avant": ["Puzzle.PutIntoPlay('21180b', under_control=True)"],
        "carnet_attendu": {
            "gagnee": True,
            "cles": {"Campaign Pool: Cosmo": "1"},
            "cles_absentes": ["Campaign Pool: Security Breach"],
        },
        "suivant": "thanos",
        "attendu": {"en_jeu": ["21180b"]},
    },
    {
        "nom": "mts — Cosmo NON libere : rien au carnet, et aucun allie de campagne au scenario 3",
        "scenario": "ebony_maw",
        "heros": "captain_america",
        "carnet_attendu": {"gagnee": True, "cles_absentes": ["Campaign Pool: Cosmo"]},
        "suivant": "thanos",
        "attendu": {"pas_en_jeu": ["21180b"]},
    },
    {
        "nom": "mts — la Pierre de Puissance atteinte au scenario 1 : la breche de securite est melangee au deck rencontre du scenario 2",
        "scenario": "ebony_maw",
        "heros": "captain_america",
        # Deux pas : 21074a se retourne sur 21074b, puis l'etape 2 (21075a
        # « The Power Stone ») prend sa place. C'est l'etape que CollectMTS lit.
        "avant": ["Puzzle.AdvanceMainScheme(2)"],
        "carnet_attendu": {"cles": {"Campaign Pool: Security Breach": "1"}},
        "suivant": "the_tower_defense",
        "attendu": {"pas_en_jeu": ["21181"], "deck_rencontre": ["21181"]},
    },
    {
        "nom": "mts — Shawarma ET Black Swan au scenario 2 : la carte rejoint le deck du joueur et l'alliee entre en jeu au scenario 3",
        "scenario": "the_tower_defense",
        "heros": "captain_america",
        # 21182a « Save the Shawarma Place » retourne sur 21182b « * Black
        # Swan » : la carte existe (Shawarma), et elle n'est pas dans la pile
        # de victoire (Black Swan reste avec vous).
        "avant": ["Puzzle.PutIntoPlay('21182b')"],
        "carnet_attendu": {
            "cles": {"Campaign Pool: Shawarma": "1", "Campaign Pool: Black Swan": "1"},
        },
        "suivant": "thanos",
        # La mise en place de campagne precede la pioche (annexe II du guide
        # de reference, etapes 13 puis 14) : le shawarma peut deja etre en main.
        "attendu": {"parmi": [["21183", ["deck", "main"]]], "en_jeu": ["21182b"]},
    },
    {
        "nom": "mts — Black Swan mise en pile de victoire : le shawarma reste, mais l'alliee ne revient pas",
        "scenario": "the_tower_defense",
        "heros": "captain_america",
        "avant": [
            "Puzzle.PutIntoPlay('21182b')",
            "Puzzle.MoveTo('21182b', 'VictoryDisplay')",
        ],
        "carnet_attendu": {
            "cles": {"Campaign Pool: Shawarma": "1"},
            "cles_absentes": ["Campaign Pool: Black Swan"],
        },
        "suivant": "thanos",
        "attendu": {"parmi": [["21183", ["deck", "main"]]], "pas_en_jeu": ["21182b"]},
    },
    {
        "nom": "mts — la Tour des Vengeurs endommagee au scenario 2 : chaque identite subit 3 degats a la mise en place du scenario 3",
        "scenario": "the_tower_defense",
        "heros": "captain_america",
        "avant": ["Puzzle.PutIntoPlay('21100b')"],
        "carnet_attendu": {"cles": {"Avengers Tower Damaged": "1"}},
        "suivant": "thanos",
        "attendu": {"degats_identite": 3},
    },
    {
        "nom": "mts — les protocoles defensifs NON vaincus au scenario 3 : le court-circuit est melange au deck du joueur au scenario 4",
        "scenario": "thanos",
        "heros": "captain_america",
        # Rien a poser : 21184b « Defensive Protocols » absent de la pile de
        # victoire suffit, et c'est le cas par defaut.
        "carnet_attendu": {"cles": {"Campaign Pool: System Shock": "1"}},
        "suivant": "hela",
        "attendu": {"parmi": [["21185", ["deck", "main"]]]},
    },
    {
        "nom": "mts — les protocoles defensifs VAINCUS : aucun court-circuit au scenario suivant",
        "scenario": "thanos",
        "heros": "captain_america",
        "avant": [
            "Puzzle.PutIntoPlay('21184b')",
            "Puzzle.MoveTo('21184b', 'VictoryDisplay')",
        ],
        "carnet_attendu": {"cles_absentes": ["Campaign Pool: System Shock"]},
        "suivant": "hela",
        "attendu": {"pas_deck": ["21185"], "pas_main": ["21185"]},
    },
    {
        "nom": "mts — la balance des Pierres atteinte au scenario 3 : le joueur defausse la moitie de son deck a la mise en place du scenario 4",
        "scenario": "thanos",
        "heros": "captain_america",
        # 21115 « Balance the Scales » : l'etape que CollectMTS lit pour
        # « The Infinity Stones 1B completed ».
        "avant": ["Puzzle.AdvanceMainScheme(2)"],
        "carnet_attendu": {"cles": {"The Infinity Stones 1B completed": "1"}},
        "suivant": "hela",
        "attendu": {"taille_min": {"defausse": 10}},
    },
    {
        "nom": "mts — sans la balance des Pierres : le deck du scenario 4 est intact, la defausse vide",
        "scenario": "thanos",
        "heros": "captain_america",
        "carnet_attendu": {"cles_absentes": ["The Infinity Stones 1B completed"]},
        "suivant": "hela",
        "attendu": {"taille": {"defausse": 0}},
    },
    {
        "nom": "mts — la pierre de Norn rapportee au scenario 4 : elle est attachee a l'identite au scenario 5",
        "scenario": "hela",
        "heros": "captain_america",
        # 21186b « Retrieve Odin's Armor » existe (la quete a ete retournee)
        # mais n'est pas en pile de victoire : la pierre, pas l'armure.
        "avant": ["Puzzle.PutIntoPlay('21186b')"],
        "carnet_attendu": {
            "cles": {"Campaign Pool: Norn Stone": "1"},
            "cles_absentes": ["Campaign Pool: Odin"],
        },
        "suivant": "loki",
        "attendu": {"en_jeu": ["21187a"]},
    },
    {
        "nom": "mts — l'armure d'Odin recuperee au scenario 4 : Odin entre en jeu sous controle au scenario 5",
        "scenario": "hela",
        "heros": "captain_america",
        "avant": [
            "Puzzle.PutIntoPlay('21186b')",
            "Puzzle.MoveTo('21186b', 'VictoryDisplay')",
        ],
        "carnet_attendu": {
            "cles": {"Campaign Pool: Norn Stone": "1", "Campaign Pool: Odin": "1"},
        },
        "suivant": "loki",
        "attendu": {"en_jeu": ["21139b", "21187a"]},
    },
]

```

**Épreuves réelles de Web of Deceit** (campagne maison, sans collecteur : ne mesure que ce que le carnet *change*) :
*Extrait de `Fusion/marvel-lcg-src/tools/epreuves_campagnes.py` (de « La Toile du Mensonge (web_of_deceit) » a « Hunting Season (hunting_season) »).*

```python
# ============================ La Toile du Mensonge (web_of_deceit) — maison
#
# Campagne maison, une seule mecanique de report : les ARBRES DE TALENTS. A
# chaque rencontre gagnee, chaque joueur prend une carte du palier suivant de
# son arbre ; ces cartes restent dans son deck jusqu'a la fin de la campagne et
# doivent y figurer (livret maison p.2). Le carnet retient un choix par palier
# et par joueur, et la mise en place les remet toutes dans le deck.
EPREUVES += [
    {
        "nom": "web_of_deceit — le talent de palier 0 choisi est dans le deck des la rencontre suivante",
        "scenario": "wd_shocker",
        "heros": "spider_man",
        "choix": {"Player 1 Talent Tier 0": "wd112"},
        "suivant": "wd_electro",
        "attendu": {"parmi": [["wd112", ["deck", "main"]]]},
    },
    {
        "nom": "web_of_deceit — les paliers S'ACCUMULENT : trois talents gagnes, trois cartes dans le deck",
        "scenario": "wd_the_lizard",
        "heros": "spider_man",
        "choix": {"Player 1 Talent Tier 0": "wd112",
                  "Player 1 Talent Tier 1": "wd113",
                  "Player 1 Talent Tier 2": "wd115"},
        "suivant": "wd_vulture",
        "attendu": {"parmi": [["wd112", ["deck", "main"]],
                              ["wd113", ["deck", "main"]],
                              ["wd115", ["deck", "main"]]]},
    },
    {
        "nom": "web_of_deceit — TEMOIN : sans talent au carnet, aucune carte de campagne ne s'invite dans le deck",
        "scenario": "wd_shocker",
        "heros": "spider_man",
        "suivant": "wd_electro",
        "attendu": {"aucune_parmi": [["deck", ["wd112", "wd113", "wd115"]],
                                     ["main", ["wd112", "wd113", "wd115"]]]},
    },
    {
        "nom": "web_of_deceit — les talents suivent jusqu'a la derniere rencontre",
        "scenario": "wd_vulture",
        "heros": "spider_man",
        "choix": {"Player 1 Talent Tier 0": "wd112",
                  "Player 1 Talent Tier 4": "wd121"},
        "suivant": "wd_kingpin",
        "attendu": {"parmi": [["wd112", ["deck", "main"]], ["wd121", ["deck", "main"]]]},
    },
]

```

### 11.4 La boucle d'une campagne : les pièges payés en la mesurant (`RECETTES-MOTEUR.md` §7quaterdecies)

<!-- extrait de docs/reference/RECETTES-MOTEUR.md -->
#### 7quaterdecies. Mesurer la BOUCLE d'une campagne (19/09/2026)

Le harnais des capacites mesure une partie. Pour mesurer ce qui se passe ENTRE
deux parties d'une campagne — le carnet ecrit a la victoire, les cases cochees
au panneau, et la mise en place du scenario suivant — il y a
`tools/test_campagnes.py`, generique, et `tools/epreuves_campagnes.py`, qui
porte la connaissance de chaque boite.

Pieges payes en l'ecrivant, tous reutilisables :

- **L'estampille du carnet sortant DOIT egaler l'id du scenario de la campagne.**
  `WriteCampaignLogAtGameOver` la derive du `set_name` de la manigance
  principale, et le panneau de recompenses (`preremplissage.ts`) ignore TOUT
  le releve du moteur si elle differe de `lireContexte().scenario`, puis retombe
  sur le carnet ANCIEN : les gains du scenario disparaissent sans un mot. `gmw`
  ecrivait `collector_1` / `collector_2` pour `infiltrate_the_museum` /
  `escape_the_museum` : les unites des scenarios 2 et 3 n'arrivaient jamais au
  Marche (signalement n°50, 04/10/2026). Quand les deux ne coincident pas, la
  boite passe `scenario_id=` au collecteur. Une epreuve
  `"carnet_attendu": {"scenario": "<id>"}` par scenario de la boite le garde.
- **Un collecteur qui plante n'ecrit RIEN, et ne le dit qu'au journal moteur.**
  `s.GetThreatInternal()` sur un complot principal (`AttributeError`, la
  methode n'existe pas : c'est la propriete `.threat`) a prive tout le
  scenario 2 de gmw de son releve, silencieusement cote joueur. Une epreuve qui
  ne lit que le carnet ENTRANT ne le voit pas : lire le sortant.
- **Le resultat de la partie n'est pas encore pose pendant `WhenGameOver`.**
  `GameOver.SetGameOver` envoie le message PUIS affecte `players_won` : un
  collecteur qui lit `world.game_over` voit toujours « perdue ». Le collecteur
  doit recevoir le MESSAGE (`collect_fn(effect, message)`).
- **La mise en place de campagne precede la pioche.** Annexe II du guide de
  reference : etape 13 la campagne, etape 14 la main de depart. Une carte
  melangee au deck par une recompense peut donc arriver en main, et une
  recompense « cherchez une carte et mettez-la en main » n'AJOUTE rien a la
  main : elle laisse en choisir une partie.
- **Une carte cherchee par `Puzzle.PutIntoPlay('id')` deux fois est la MEME
  carte.** `FindOrCreateFace` retrouve l'existante. Pour deux exemplaires :
  `Puzzle.PutIntoPlay(Puzzle.CreateCard('id'))`.
- **Un JETON n'est pas un COMPTEUR.** `PlaceTokensOn` / `GetTokens` d'un cote,
  `PlaceCountersOn` / `GetCounters` de l'autre. Chercher une menace de jeton
  dans les compteurs rend zero a tous les coups.
- **`face.victory` est un BOOLEEN** (« cette carte a-t-elle une valeur de
  victoire »), la valeur imprimee est `printed_victory`. Les additionner
  compte les cartes, pas les points.
- **Le nom d'une identite change avec sa forme.** Relever `identity.paper.name`
  a la victoire donne « Steve Rogers » si la partie finit en alter-ego, et la
  mise en place suivante commence toujours en alter-ego. On ecrit et on relit
  `identity.GetHeroFace().paper.name`.
- **`Puzzle.AdvanceMainScheme(fois)`** (ajoute ce jour) fait avancer le complot
  principal par le chemin du moteur : un pas retourne la face A sur la face B,
  le pas suivant prend l'etape suivante. Plusieurs recompenses ne dependent que
  de l'etape atteinte.
- **Un defaut dans l'epreuve elle-meme doit echouer bruyamment.** Une exception
  levee dans le verificateur, hors `try`, laissait le fils pendu sans jamais
  rapporter : l'appel est desormais garde.

### 11.5 Niveau 5 : la sonde de campagne (`tools/sonde_campagne.py`)

Monte une partie complète sans navigateur, applique un carnet, exécute des `Puzzle.*` et rend **le descripteur
de monde tel que le plateau le reçoit**. C'est l'outil qui prouve **où atterrit réellement une carte** et si un
détecteur la verra. Variables : `CAMPAIGN_LOG` (le carnet entrant, JSON), `RULES` (défaut `["mode_campaign"]`),
`PUZZLE` (commandes après la mise en place), `RAPPORT`, `FIN_DE_PARTIE=1` (force la fin et capture le carnet
sortant sous `carnet_sortant`), `CHOIX` (index de l'option retenue à chaque question : sert à prouver qu'une
question offre vraiment plusieurs réponses).

```bash
cd "$W" && RAPPORT=/tmp/sonde.json \
  CAMPAIGN_LOG='{"Player 1 Role":"Brawler","Captive Allies":"32089"}' \
  "$PY" tools/sonde_campagne.py "$PWD" master_mold captain_america 4801
```

⚠ **La sonde exécute `.game`, pas `src/`** : copier un `.py` ne suffit pas, il faut `launcher_fast.py
--build-only` avant de sonder (sinon on mesure l'ancien code et on croit avoir prouvé le nouveau).

### 11.6 Les vérificateurs statiques du dépôt (ce que Claude lance, et ce qu'ils attrapent)

| Outil | Ce qu'il refuse |
|---|---|
| `tools/verifier_campagnes.py` | une **clé** de `data/campagnes/*.json` absente des chaînes du moteur (`campaign.py`, `campaign_logs.py`, `factory/campaign.py`, `mts/campaign.py`, **tout** le pack) ; une `detection` inconnue ; un `tirage` mal formé ; un `deck` sans `parJoueur` ; un `cumulatif` non `int` |
| `tools/verifier_prefixes.py` | un `card_id` en double ; un préfixe fan-made non déclaré ; un `card_id` fan-made qui emprunte un numéro officiel ; un numéro de set en double dans `sets_info.json` |
| `tools/verifier_desc_mots_cles.py <pack>` | un texte imprimé dont le `desc` ne dit pas la même chose (Uses, Toughness, Restricted, Retaliate, MaxPerDeck, MaxPerUnit, Setup, Victory, Permanent, Alliance, Villainous, Requirement) |
| `tools/verifier_coherence_cartes.py` | cohérence des données, couverture des tests, collisions de noms |
| `tools/verifier_noms_modules.py` / `verifier_appels_modules.py` / `verifier_api_cartes.py` | un script mal rangé ; un appel de fonction ou un nom de méthode inexistant dans un script |
| `tools/verifier_traductions_fr.py`, `ui-app/src/board/vocabulaire-statuts.test.ts` | un texte français manquant ou au vocabulaire interdit |
| `tools/verifier_scenes_campagne.py` | la mise en place des scènes de campagne |
| `tools/verifier_tous_les_decks.py` | **la création de partie pour chaque deck de départ** (une construction que seul ce contrôle exerce : liste blanche d'événements à deux capacités `Play`, etc.) — **obligatoire dès qu'un fichier partagé ou un deck bouge** |

### 11.7 Ce que Claude exécute, dans l'ordre (pour que tu saches à quoi tes fichiers seront soumis)

1. Fusion des fragments (`cards.json`, `sets_info.json`, `textes-fr-fanmade.ts`, `prefixes_fanmade.json`) ; images ;
   recalcul des checksums (`tools/recalculer_checksums.py`).
2. `compileall`, `verifier_prefixes`, `verifier_campagnes`, `verifier_desc_mots_cles`, `verifier_coherence_cartes`.
3. `test_cards.py` (construction de **toutes** les cartes), `verifier_api_cartes.py`, `verifier_appels_modules.py`.
4. **`tools/cas/<bloc>.py`** par `test_capacites.py` ; **preuve par substitution** par `substituer_pack.py`.
5. **`tools/test_campagnes.py`** (la boucle) — **obligatoire dès qu'on touche un `campaign.py`, une clé de carnet,
   `data/campagnes/*.json` ou une mise en place de scénario**.
6. `autoplay.py` : ≥ 8 parties par scénario, contre un héros témoin, **0 traceback** (`NameError`,
   `AttributeError`, `TypeError`, `KeyError`, `AssertionError`) ; le journal des parties qui touchent les cartes
   neuves est **lu ligne à ligne**.
7. `verifier_tous_les_decks.py` si un fichier partagé a bougé.
8. **Un humain joue** un scénario complet dans le navigateur (le seul juge de « est-ce que la carte est agréable
   et fait ce qu'elle promet »). Si ce point n'est pas fait, il est écrit noir sur blanc.


---

## 12. Ce que tu livres, exactement, et dans quel ordre travailler

### 12.1 L'ordre de travail recommandé

Pour une grosse campagne, **livre scénario par scénario** (un message, ou un lot de fichiers, par scénario) plutôt
que tout d'un coup : la relecture de Claude est plus fiable et une erreur de méthode se corrige au premier lot.

| Phase | Tu fais | Tu produis |
|---|---|---|
| **0. Lecture** | Lire le livret de campagne **en entier** (règles de campagne, carnet imprimé, encarts SETUP / VICTORY / DEFEAT de chaque scénario) et les cartes fournies. Le **carnet imprimé** fait autorité sur le code : lis-le **avant** d'écrire une définition. | notes de travail (pas de livrable) |
| **1. Cadrage** | Choisir le **code** de la campagne, le **nom du pack**, proposer **deux préfixes** libres (question à choix multiple). Lister **tous** les contenus déjà présents dans le jeu (Standard, Expert, sets modulaires officiels réutilisés, héros officiels cités). | `QUESTIONS.md` (premières questions), `MANIFESTE.md` (squelette) |
| **2. Cartes** | Transcrire **chaque carte** (une planche de 4 cartes par lecture : au-delà le texte d'encart n'est plus sûr), numéroter sans trou, remplir `desc`. | `integration/data/cards.<pack>.fragment.json`, `images.md` |
| **3. Scénarios et sets** | Écrire les fichiers de scénario (standard **et** expert), les sets de rencontre, l'entrée `sets_info`. | `integration/data/scenarios/*`, `…/encounter_sets/*`, `…/sets_info.<pack>.fragment.json` |
| **4. Description + carnet** | Écrire `data/campagnes/<code>.json` et la **table des clés** (`CARNET-CLES.md`). | `integration/data/campagnes/<code>.json`, `CARNET-CLES.md` |
| **5. Scripts** | Les scripts de cartes, **scénario par scénario**, avec leur gabarit. | `integration/src/cards/pack/<pack>/…`, `GABARITS.md` |
| **6. Logique de campagne** | `campaign.py` + l'appel `*CampaignSetup(n)` sur chaque face 1A. | `integration/src/cards/pack/<pack>/campaign.py` |
| **7. Textes et métadonnées** | Textes français, biographies, préfixe, crédits, pages du livret. | `integration/textes-fr/…`, `…/mechants-info.fragment.js`, `…/prefixes.<pack>.fragment.json`, `CREDITS.md`, `livret-pages.md` |
| **8. Preuves** | Les cas de test de capacité et les épreuves de boucle. | `integration/tools/cas/<bloc>.py`, `integration/tools/epreuves.<code>.fragment.py` |
| **9. Auto-vérification** | Lancer `verifier-livraison-campagne.py` ; relire chaque checklist ; compter les `A_FAIRE_CLAUDE`. | `AUTO-VERIFICATION.md`, `A_FAIRE_CLAUDE.md`, `BESOINS-MOTEUR.md`, `QUESTIONS.md` à jour |

### 12.2 L'arborescence de la livraison

Elle **reproduit celle du projet** (chemins relatifs à la racine du moteur), pour que Claude fusionne sans deviner.
Voici la livraison d'une campagne imaginaire `ma_campagne` (pack `ma_campagne`, préfixe `mc`, code `ma_campagne`) :

```
livraison/
├── MANIFESTE.md                    la liste de TOUS les fichiers livrés (§12.3)
├── QUESTIONS.md                    les questions ouvertes (§12.4)
├── BESOINS-MOTEUR.md               ce que le moteur / l'interface devra apprendre (§12.5)
├── A_FAIRE_CLAUDE.md               tous les marqueurs A_FAIRE_CLAUDE regroupés (§12.6)
├── CARNET-CLES.md                  la table des clés du carnet (§7.10)
├── GABARITS.md                     un gabarit PROCESSUS-CARTE par carte à capacité (§6.8)
├── AUTO-VERIFICATION.md            ce que tu as vérifié, avec la sortie du vérificateur (§12.7)
├── CREDITS.md                      (§10.8)
├── images.md                       card_id → fichier source (§10.1)
├── livret-pages.md                 quelle page du PDF joue quel rôle (§10.6)
└── integration/
    ├── data/
    │   ├── cards.ma_campagne.fragment.json            {"ma_campagne": [ ...cartes... ]}
    │   ├── sets_info.ma_campagne.fragment.json         {"N. Custom (Ma campagne)": {...}}
    │   ├── campagnes/ma_campagne.json
    │   ├── scenarios/mc_scenario_1.json    mc_scenario_1_expert.json    ...
    │   └── encounter_sets/mc_set_a.json    mc_set_b.json                ...
    ├── src/cards/pack/ma_campagne/
    │   ├── __init__.py                                  helpers partagés du pack
    │   ├── campaign.py                                  §7
    │   └── <set_nettoyé>/__init__.py   <card_id>.py     ... un dossier par set
    ├── textes-fr/ma_campagne.fragment.txt              lignes pour textes-fr-fanmade.ts
    ├── public/js/prepare/mechants-info.fragment.js     biographies des vilains
    └── tools/
        ├── prefixes.ma_campagne.fragment.json           entrée de prefixes_fanmade.json
        ├── cas/ma_campagne.py                           cas de test de capacité
        └── epreuves.ma_campagne.fragment.py             EPREUVES += [ ... ]
```

**Règles de forme** :

* **Encodage UTF-8, fins de ligne `\n`**, JSON indenté de 4 espaces, `ensure_ascii=False`.
* **Un fichier par face de carte à capacité** ; **jamais** deux cartes dans un même script.
* Aucun fichier **hors** de cette arborescence ; aucun fichier temporaire.
* **Les fragments contiennent *seulement* ta part** : jamais une copie, même partielle, d'un fichier partagé qui
  contiendrait les cartes des autres.
* **Aucune modification d'un fichier existant du projet** : tout nouveau fichier ; tout ce qui doit changer dans
  un fichier existant (moteur, interface, liste blanche de traits ou compteurs) va dans `BESOINS-MOTEUR.md`.

### 12.3 `MANIFESTE.md`

Une ligne par fichier livré :

```
| Chemin (dans integration/)                         | Rôle                                  | Cartes / entrées | Statut |
|----------------------------------------------------|---------------------------------------|------------------|--------|
| data/cards.ma_campagne.fragment.json               | cartes du pack                        | 176 faces        | complet |
| src/cards/pack/ma_campagne/shocker/mc002a.py       | Setup du complot 1A + CampaignSetup   | 1                | A_FAIRE_CLAUDE ×1 |
```

**Statut** : `complet` · `partiel (A_FAIRE_CLAUDE ×n)` · `brouillon`. À la fin du manifeste : les totaux (cartes,
faces, scénarios, sets, scripts, cas de test, épreuves, `A_FAIRE_CLAUDE`).

### 12.4 `QUESTIONS.md` — une question par entrée, format fixe

```
### Q<n> — <card_id ou règle> : <le doute en une phrase>

Image / source : <fichier de la carte, page du livret>
Texte imprimé : « … »

Lectures possibles :
  A. (recommandée) <lecture> — en jeu : <ce que ça change>
  B. <lecture> — en jeu : <ce que ça change>
  C. Autre (précise)

Lecture retenue en attendant : A  (repérée par `# QUESTION <n> :` dans <fichier>)
```

Une **seule** question à la fois est posée à l'utilisateur (règle 4, §1.2) ; ce fichier les **range** pour Claude.

### 12.5 `BESOINS-MOTEUR.md` — format fixe

```
### B<n> — <titre court>

Livret : page <p>, « … »
Ce que le jeu fait déjà de plus proche : <fichier : fonction, ou « rien »>
Ce qui manque : <comportement attendu, décrit ; pas de code>
Dépend : <card_id(s), clé(s) de carnet, champ(s) de description>
En attendant : <A_FAIRE_CLAUDE posé dans <fichier>, ou lecture retenue>
```

Y vont **aussi** : les **traits nouveaux** (`trait nouveau : X, porté par mc012`), les **compteurs nouveaux**
(`compteur nouveau : knucklehead, desc.Uses de mc044`), les **chaînes d'interface nouvelles** avec leur traduction
anglaise, les cartes réservées à la campagne (`SETS_RESERVES_A_LA_CAMPAGNE`), les écrans inédits.

### 12.6 `A_FAIRE_CLAUDE.md`

Tous les marqueurs `# A_FAIRE_CLAUDE:` du code, regroupés : `fichier : ligne : texte imprimé visé : ce qui manque :
carte de référence la plus proche`. **Un marqueur dans le code qui n'est pas dans cette liste est une faute.**

### 12.7 `AUTO-VERIFICATION.md`

```
## Vérificateur de livraison
$ python3 verifier-livraison-campagne.py livraison/
<la sortie complète, collée>

## Relectures faites (cochées seulement si faites)
- [x] §4.10 checklist de carte : toutes les cartes
- [x] §5.7 checklist de scénario : chaque scénario
- [x] §8.8 checklist de description de campagne
- [x] §7.10 table des clés : chaque clé écrite ET lue

## Ce qui n'a PAS été vérifié (à exécuter par Claude)
- cas de test de capacité : écrits, non exécutés
- épreuves de boucle : écrites, non exécutées
- aucune partie jouée
```

### 12.8 Ce que tu ne fais jamais (rappel)

Pas d'images ni de scans ; pas de checksum ; pas de commit ni de déploiement ; pas de modification du moteur ;
pas de deck de départ inventé pour un héros ; pas de « vert » non exécuté ; pas de chiffre de test non mesuré ;
**pas de décision de règle en silence**.

### 12.9 Exemple de livraison réelle : Hunting Season (Nugget)

Une campagne maison a déjà été livrée par ce même procédé (auteur : Nugget ; intégrée par Claude). Son dossier de
livraison est dans `modeles/C-livraison-exemple-hunting-season/` : `LIRE_D_ABORD.md` (état réel), `PROMPT_POUR_CLAUDE.md`
(instruction de reprise), `SPECIFICATIONS.md` (règles spéciales), `POINTS_OUVERTS.md` (décisions à prendre),
`VERIFICATION.json` (contrôles statiques effectués), `integration/` (données et scripts, **brouillons partiels**,
chaque `A_FAIRE_CLAUDE` honnête), `reference/` (carnet : `campaign_log_contract.json`, `campaign_rules.py`).

Ce qui a bien fonctionné dans cette livraison : un **inventaire carte par carte** (239 entrées pour 226 cartes
physiques, l'écart expliqué) ; des **fragments** à fusionner sans écraser ; une **décision d'utilisateur par point
ouvert**, jamais en silence (« Swarmed by Rats » : la carte imprime *Interrupt* mais décrit un déclencheur *After* →
question, pas de correction silencieuse) ; un calculateur pur des règles de campagne séparé du moteur.


---

## 13. Les modèles : deux campagnes complètes, fichier par fichier

Le zip contient, dans `modeles/`, **deux campagnes réelles déjà intégrées et jouées**, reconstituées **dans le
format exact d'une livraison** (§12) : tu y trouves ce que tu dois produire, au même endroit, avec les mêmes noms.
Ouvre-les **avant** d'écrire ta première carte.

| Dossier du zip | Campagne | Pourquoi ce modèle |
|---|---|---|
| `modeles/A-officielle-the-mad-titans-shadow/` | **The Mad Titan's Shadow** (officielle, 5 scénarios) | une campagne **officielle** avec **collecteur** : tout est relevé par le moteur ; le plus simple à imiter |
| `modeles/B-maison-web-of-deceit/` | **La Toile du Mensonge / Web of Deceit** (fan-made, 5 scénarios) | une campagne **maison** : préfixe `wd`, auteur (`custom`), sets modulaires fan-made, récompenses **choisies par le joueur** (arbres de talents) |
| `modeles/C-livraison-exemple-hunting-season/` | **Hunting Season** (fan-made, 5 scénarios) | la **vraie livraison d'une autre IA** (ce que Claude a reçu, avec ses brouillons et ses points ouverts) |
| `modeles/D-patrons-de-campaign-py/` | les **douze** `campaign.py` du jeu | un motif pour chaque mécanique (§7.8) |

Chaque `modeles/A-…` et `modeles/B-…` contient : `livraison/` (l'arborescence à produire), `images-exemples/` (quelques
vraies images et pages de livret, pour fixer les formats) et `README.md`.

### 13.1 Modèle A — The Mad Titan's Shadow (officielle)

| Élément | Contenu |
|---|---|
| Cartes (faces) | **214** : SideScheme 26, Attachment 23, Treachery 21, Villain 21, Ally 19, Minion 19, Event 16, MainScheme 16, Environment 12, Upgrade 11, Resource 6, Obligation 3, Hero 2, AlterEgo 2, Support 2 |
| Sets (`set_name`) | (aspect / sans set) (27); Adam Warlock (12); Adam Warlock Nemesis (4); Armies of Titan (3); Black Order (4); Children of Thanos (4); Ebony Maw (16); Enchantress (3); Frost Giants (3); Hela (20); Infinity Gauntlet (7); Legions of Hel (4); Loki (18); Spectrum (12); Spectrum Nemesis (4); Thanos (16); The Mad Titan's Shadow Campaign (20); The Tower Defense (22) |
| Scénarios | 10 fichiers : `ebony_maw`, `ebony_maw_expert`, `hela`, `hela_expert`, `loki`, `loki_expert`, `thanos`, `thanos_expert`, `the_tower_defense`, `the_tower_defense_expert` |
| Sets de rencontre propres au pack | 7 : `armies_of_titan`, `black_order`, `children_of_thanos`, `enchantress`, `frost_giants`, `infinity_gauntlet`, `legions_of_hel` |
| Scripts de cartes | **183** fichiers dans 18 dossiers de set |
| Textes français | **aucune entrée** (manque connu) |
| Épreuves de boucle | 12 |

**Ce qu'il faut y voir :**

* **`data/campagnes/mts.json`** — chaque scénario déclare des champs `auto` **sans `detection`** (`Campaign Pool:
  Cosmo`…) : ils sont relevés par `CollectMTS`. Les **PV restants** sont déclarés en `victoire_commune_expert`
  avec le détecteur `pv_restants`. Le dernier scénario porte `final: true` et une `defaite` (`partie_perdue`,
  `expert_seulement`).
* **`src/cards/pack/mts/campaign.py`** — `InPool` / `LogSet` (lecture d'une clé), les briques `PutIntoPlayIfPool`,
  `ShuffleIntoEncounterIfPool`, `EachPlayerShufflesCopyIfPool` (application), `CollectMTS` (relevé),
  `CampaignSetup(level)` (assemblage par niveau). **Les clés écrites par `CollectMTS` sont celles que lit
  `CampaignSetup`** : vérifie-le à la main sur la table `CARNET-CLES.md` de ce modèle.
* **Les faces 1A** (`ebony_maw/21074a.py`, `the_tower_defense/21098a.py`, `thanos/…`, `hela/…`, `loki/…`) appellent
  `*CampaignSetup(n)` avec **n = numéro du scénario**.
* **Les cartes de campagne** (`set_name` « The Mad Titan's Shadow Campaign », classe `Campaign;Basic`) : Shawarma,
  System Shock (une obligation), Norn Stone, Odin… sont **générées au carnet**, pas dans un deck enregistré.
* **Les épreuves** (`tools/epreuves.mts.fragment.py`) : une par récompense, avec son **témoin** (sans carnet).

### 13.2 Modèle B — Web of Deceit (maison)

| Élément | Contenu |
|---|---|
| Cartes (faces) | **176** : Minion 24, Treachery 23, Attachment 19, MainScheme 18, Upgrade 17, Villain 16, SideScheme 16, Event 12, Environment 8, Support 7, Ally 7, Resource 7, Obligation 1, PlayerSideScheme 1 |
| Sets (`set_name`) | Bodyguard (4); City Sewers (5); Crime Wave (4); Electro (21); Kingpin (17); Kraven the Hunter (5); Power Drain II (6); Shocker (19); The Lizard (18); Underling (4); Vulture (18); Web of Deceit (5); Web of Deceit Rewards (50) |
| Scénarios | 12 fichiers : `wd_electro`, `wd_electro_expert`, `wd_kingpin`, `wd_kingpin_expert`, `wd_shocker`, `wd_shocker_expert`, `wd_the_lizard`, `wd_the_lizard_expert`, `wd_vulture`, `wd_vulture_expert`, `wd_vulture_underling`, `wd_vulture_underling_expert` |
| Sets de rencontre propres au pack | 11 : `bodyguard`, `city_sewers`, `crime_wave`, `electro`, `kingpin`, `kraven_the_hunter`, `power_drain_ii`, `shocker`, `the_lizard`, `underling`, `vulture` |
| Scripts de cartes | **164** fichiers dans 12 dossiers de set |
| Textes français | 176 entrées |
| Épreuves de boucle | 4 |

**Ce qu'il faut y voir :**

* **Un pack complet avec un préfixe** : `wd001a`… `wd165`, `custom: "Ripper3"` sur chaque carte, entrée
  `120. Custom (Web of Deceit)` dans `sets_info`, entrée `wd` dans `prefixes_fanmade.json`.
* **Les sets réutilisés plutôt que recopiés** : *Power Drain II* est le set officiel *Power Drain* plus une carte :
  six **`ability_link`** à la place de six scripts (même fidélité que le moteur officiel). *Standard III* est une
  réimpression : **rien à créer**. **Avant d'écrire un script, cherche si la carte existe déjà dans le jeu.**
* **Une mécanique de livret que le moteur ne connaissait pas** — les **arbres de talents** (chaque joueur, après
  chaque scénario gagné, ajoute une carte de son arbre à son deck) — **résolue sans toucher au moteur** :
  des champs `type: "choix"`, `obligatoire: true`, `parJoueur: true`, dont les `options` sont les cartes du palier,
  et **un seul** `campaign.py` de 45 lignes qui **génère dans le deck de chaque joueur** les cartes notées au
  carnet (`ChaqueJoueurRetrouveSesTalents`, appelée par **chaque** face 1A). **Écart assumé et écrit** : l'arbre ne
  s'affiche pas comme un arbre (le joueur voit la liste de son palier). **C'est le bon réflexe quand une
  mécanique inédite peut se ramener à un mécanisme existant : on l'écrit, on n'invente pas.**
* **Un vilain qui se retourne au lieu d'être vaincu** (Shocker), des
  environnements mis de côté qui entrent en jeu par un effet (`set_aside` : « Vote for Fisk », « The Great Web »).
* **Ce que ce modèle n'a PAS (et qu'il faut avoir)** : **pas de collecteur** (donc pas d'estampille à tester) ; la `custom` y est bien.

Le **journal de portage** complet (`annexes/G-journal-portage-web-of-deceit.md`, 1 500 lignes) est le meilleur
récit de ce qu'une campagne maison demande : inventaire du Drive, croisement avec l'existant, scénario par
scénario, **trois écarts assumés** par lot, mesures. Lis au moins les §7 à §12 et §14.

### 13.3 Modèle C — Hunting Season : la vraie livraison d'une IA

| Élément | Contenu |
|---|---|
| Cartes (faces) | **239** : Treachery 52, Minion 43, Attachment 33, MainScheme 20, Villain 18, Event 15, Upgrade 15, SideScheme 14, Obligation 10, Ally 9, Environment 8, Support 2 |
| Sets (`set_name`) | Expert Campaign Set (16); Feral Instincts (5); Hunt Campaign Set (6); Hunter Mode (5); Kraven The Hunter (23); Lizard Thralls (5); Red Vulture (6); Savage Six (7); Scorpion (26); The Lizard (32); The Lodge (36); Trap (16); Vermin (31); Vulture (25) |
| Scénarios | 10 fichiers : `hs_kraven_the_hunter`, `hs_kraven_the_hunter_expert`, `hs_scorpion`, `hs_scorpion_expert`, `hs_the_lizard`, `hs_the_lizard_expert`, `hs_vermin`, `hs_vermin_expert`, `hs_vulture`, `hs_vulture_expert` |
| Sets de rencontre propres au pack | 4 : `hs_feral_instincts`, `hs_lizard_thralls`, `hs_red_vulture`, `hs_savage_six` |
| Scripts de cartes | **239** fichiers dans 14 dossiers de set |
| Textes français | 239 entrées |
| Épreuves de boucle | 19 |

Le dossier `modeles/C-livraison-exemple-hunting-season/` contient ce que Claude a **reçu** de l'IA de Nugget :

* `LIRE_D_ABORD.md` — **l'état réel du dossier** (« les 226 cartes physiques sont représentées par 239 entrées JSON :
  les dix complots principaux ont deux faces et les trois cartes de vilain Lizard aussi »), la liste des fichiers,
  et la phrase clé : « *Ce pack ne doit pas être déclaré jouable tant que ces points sont ouverts.* »
* `PROMPT_POUR_CLAUDE.md` — l'instruction de reprise (ne pas réutiliser aveuglément d'anciens identifiants ; ne pas
  coder à la place des mots-clés lus dans `desc` ; **ne pas corriger en silence une carte dont le texte se contredit**).
* `SPECIFICATIONS.md` — les **règles spéciales** de la campagne (expérience, Lodge, paquet Trap, vilain recto-verso…).
* `POINTS_OUVERTS.md` — les décisions à prendre, chacune avec l'image de la carte concernée.
* `VERIFICATION.json` — les contrôles **statiques** faits, **sans simulation du jeu**, et le disent.
* `integration/` — les fragments de données et les scripts, **partiels et honnêtes** (`A_FAIRE_CLAUDE`).
* `reference/` — `campaign_log_contract.json` (les clés du carnet et les besoins d'interface),
  `campaign_rules.py` (le calcul pur de l'expérience, des achats, des soins : **un modèle de travail, pas une extension
  autorisée du schéma natif**), `card_manifest.json` (chaque carte : id, source, état du script).

**Ce que cette livraison a bien fait** : inventaire exact, fragments sans écrasement, un point ouvert par
décision, calcul des règles **séparé** du moteur. **Ce qu'il fallait faire de plus** (et que ce kit exige) : la table
des clés du carnet **écrite/lue** (§7.10), l'appel `*CampaignSetup(n)` sur chaque 1A, les cas de test et les
épreuves de boucle, le texte français, un `custom` sur **chaque** carte. Constat du 20/10/2026 : **les 239
cartes de Hunting Season n'ont pas de clé `custom`** dans `cards.json` : n'imite pas cet oubli.

### 13.4 Les douze `campaign.py` (`modeles/D-patrons-de-campaign-py/`)

| Campagne | Fichier | Lignes | Style | Ce qu'on y apprend |
|---|---|---|---|---|
| The Rise of Red Skull | `trors/campaign.py` | 100 | niveaux croissants, **sans collecteur** | `CampaignSetup(level, campaigns=…)` ; détecteurs côté JSON |
| Sinister Motives | `sm/campaign.py` | 202 | sans collecteur ; piste de réputation | total **cumulatif**, **tirage** aux paliers, deck **requis** |
| The Mad Titan's Shadow | `mts/campaign.py` | 233 | **collecteur** ; clés « pool » | **le modèle**, et la source de `WriteCampaignLogAtGameOver` |
| Mutant Genesis | `mut_gen/campaign.py` | 234 | collecteur ; **rôle** choisi en jeu | alliés captifs, rôle persistant |
| NeXt Evolution | `next_evol/campaign.py` | 271 | collecteur ; environnements gagnés | effets propres à chaque niveau |
| Age of Apocalypse | `aoa/campaign_setup.py` | 178 | collecteur ; **missions** | une mission jamais deux fois ; défaite par clé absente |
| Galaxy's Most Wanted | `gmw/campaign.py` | 388 | collecteur ; **marché** d'unités | solde, estampille explicite (`scenario_id=`) |
| Agents of S.H.I.E.L.D. | `aos/campaign.py` | 597 | collecteur ; **enquête à secret serveur** | `CampaignLog.SetStr` en cours de partie, `WhenCampaignSetupAfterMulligans` |
| Fear No Evil | `fne/campaign.py` | 247 | collecteur ; **ordre libre** | carnet par affaire, retrait de cartes du deck |
| Hunting Season | `hunting_season/campaign.py` | 377 | collecteur ; **expérience**, Lodge | défaite qui continue la campagne, dépenses de mise en place |
| Skrull Menace | `skrull_menace/campaign.py` | 682 | collecteur ; **zone de coopération** | tableau de progression, tirage d'Élites, ensembles alternatifs |
| Web of Deceit | `web_of_deceit/campaign.py` | 45 | **sans collecteur**, gains **choisis** | le minimum viable d'une campagne maison |

### 13.5 Le brief que Claude donne à ses propres agents (Skrull Menace) — ce que tu dois savoir aussi

`annexes/K-skrull-menace-brief-agents.md` est le brief que Claude a rédigé pour des agents travaillant en parallèle sur
un coffret : les **recettes de rangement des images**, le **vocabulaire français**, les **pièges déjà payés**, le
**format d'un livrable de lot**. `annexes/K-skrull-menace-campagne-mode.md` est le tableau **règle par règle du livret
→ implémentation → cas de test** d'une campagne complète : **le modèle de la preuve** (chaque règle du livret a sa
ligne, son fichier et son cas qui la prouve).


---

## 14. Les pièges déjà payés, classés — **lis-les avant d'écrire**

Chacun de ces pièges a déjà cassé une carte, un scénario ou une campagne du projet, **presque toujours sans
aucune erreur visible**. La source est indiquée entre parenthèses (annexes du zip).

### 14.1 Données (`cards.json`, scénarios, sets)

1. **Toutes les valeurs de `desc` sont des chaînes** (`"HP": "10"`).
2. **Un compteur de `desc.Uses` absent de l'énum `COUNTER` du moteur fait lever une assertion** : la carte ne se
   construit pas. Signale-le dans `BESOINS-MOTEUR.md` *avant* de livrer (`reference/compteurs.json`).
3. **Un mot-clé du texte absent de `desc` (ou l'inverse)** : « Uses (3 tactic counters) » sans `"Uses": "3,tactic"` →
   la carte entre en jeu sans compteur, son action reste **grisée pour toujours**, sans message. Certains attributs
   n'existent que pour certains types (`Uses` : Upgrade/Support/Attachment/Obligation/Environment ; `Villainous` :
   Minion) : le mettre ailleurs **empêche la carte de se générer**.
4. **`Victory: "0"` envoie la carte dans la pile de victoire** : ce n'est pas « neutre ».
5. **Le `*` n'a pas le même sens partout** : `HP`/menaces = « par joueur » ; `ATK`/`THW` d'un **allié** = dégâts
   consécutifs ; `SCH` avec `*` = multiplié par le nombre de joueurs (constat Skrull Menace : un `SCH` plein
   s'écrit `"2"`, jamais `"2*"`).
6. **`type: "SideScheme"` dans le JSON, `EncounterSideScheme` dans les scripts.**
7. **Le dossier d'un script est le `set_name` « nettoyé »** (`CleanName`) ; un dossier de set **sans
   `__init__.py`** rend toutes ses cartes **muettes, sans erreur** ; un script mal rangé aussi.
8. **L'extension de l'image est obligatoire** ; **les complots restent stockés en paysage** (le serveur les pivote).
9. **Un set de rencontre cité dans un scénario mais sans fichier se charge VIDE, sans erreur.**
10. **Les checksums** de `cards.json` et `sets_info.json` : un fichier au checksum faux est rejeté **en silence**.
11. **Un `card_id` est une clé partout** (image, texte français, script, scénario, carnet) : on ne le renomme pas.
12. **Un préfixe fan-made non déclaré, un numéro officiel emprunté, un identifiant en double** : le second écrase
    le premier, sans un mot.
13. **`full_link`** : la carte ne porte **rien d'autre** que `card_id` et `full_link`. **`ability_link`** : mêmes
    capacités, données propres. **Avant d'écrire un script, cherche si la carte existe déjà** (Web of Deceit :
    six `ability_link` à la place de six scripts).
14. **Le nom d'un set de rencontre (`name`) s'affiche tel quel** : casse normale.
15. **`_expert` ne figure jamais dans l'`id` d'un scénario de campagne** : l'écran prend la variante tout seul.
16. **Les stades** : le `villain` standard liste les stades 1-2, l'expert 2-3 ; les complots principaux sont une paire
    a/b **par stade**.

### 14.2 Scripts de cartes

17. **Aucune fonction, aucune chaîne de ciblage inventée** : une chaîne inventée ne lève **rien**, la carte est inerte.
18. **`CardFinder(name="* X")` ne trouve jamais rien** : le nom s'écrit sans l'étoile.
19. **Les mots-clés de `desc` ne se recodent pas** (Toughness, Surge, Guard… appliqués deux fois).
20. **Un filtre va dans `conditions`**, jamais en tête de l'opération : une capacité facultative est **proposée**
    dès que son message part.
21. **Les fabriques qui rendent une LISTE** (`GiveKeywordToAttached`, `GiveKeywordToInPlayWhenApplyThis`) : sans
    `*` pour la déplier, la carte se construit avec une liste dans sa liste et le moteur plante **à la
    génération** — **`test_cards` ne le voit pas**, seule une vraie partie l'attrape (Web of Deceit, deux fois).
22. **Le `Setup` d'une carte à mot-clé `Setup`** se code `AfterGameSetup` ; **`WhenCardSetup("This", …)` est
    réservé à la face 1A du complot principal.**
23. **Les PV sont portés par la CARTE, pas par la face** : une carte retournée à 0 PV arrive sur sa nouvelle face
    **déjà vaincue** et le moteur redéclenche la défaite pendant le retournement (Shocker se retournait sans fin :
    A → B → A…). Rends les PV à la face avant de retourner.
24. **Les capacités d'une carte dans la pile de victoire ne se déclenchent jamais** (hors jeu).
25. **Une obligation révélée reste en jeu** si le script ne la défausse pas : code toutes les branches.
26. **Ne réimplémente jamais le choix de face standard/expert** : la carte le fait (`StandardModeOnly()` /
    `ExpertModeOnly()`).
27. **Une limite imprimée (« once per round ») sur un déclencheur de défaite** : piège moteur connu, signale-le.
28. **`Puzzle.PutIntoPlay` sur une carte d'un paquet de scénario spécial ne l'attache pas** : utilise
    `Puzzle.Reveal` (chemin réel).
29. **L'unicité d'une FAMILLE de cartes** (WEB-WARRIOR ou « Spider » dans le titre) : `UniqueRuleNotApplyTo` ne sait
    viser qu'une carte : une capacité écrite à la main (écart assumé, écrit).
30. **Le résultat de fin de partie se lit dans le message** (`message.players_won`), jamais dans le monde.

### 14.3 Logique de campagne

31. **Une clé de carnet mal orthographiée ne lève rien** : la récompense disparaît en silence.
32. **Une face 1A qui n'appelle pas `*CampaignSetup(n)`** : le carnet est ignoré en silence ; **un `n` faux** applique les
    récompenses d'un autre scénario.
33. **Un collecteur qui plante n'écrit RIEN** et ne le dit qu'au journal du moteur (`s.GetThreatInternal()` n'existe
    pas : c'est la propriété `.threat`).
34. **L'estampille du carnet sortant doit égaler l'`id` du scénario** : sinon le panneau ignore **tout** le relevé du
    moteur (les unités de gmw n'arrivaient jamais au Marché).
35. **`player.GetHero()` lève une assertion en forme Alter Ego** ; utilise `identity.GetHeroFace()`.
36. **`Faces.ShuffleAllTo` ne mélange que s'il a déplacé quelque chose** : une carte générée directement dans le deck
    reste sur le dessus (les captifs de Mutant Genesis arrivaient dans la main de départ).
37. **La mise en place de campagne précède la pioche** (étape 13 puis 14) : une carte mélangée au deck par une
    récompense peut arriver en main ; « cherchez une carte et mettez-la en main » n'AJOUTE rien à la main.
38. **« may » / « any player's deck »** : le joueur choisit ; ne jamais mélanger d'office dans le deck du joueur 1.
39. **Une carte que le livret fait CHERCHER dans le deck** : déclare `deck: "requis"` ; sinon, si le joueur l'a retirée,
    la récompense disparaît.
40. **Le livret imprimé et le carnet imprimé font foi, pas le code** (Mutant Genesis : deux lignes d'alliés au carnet
    officiel, une seule collectée).
41. **Un champ `int` sans `detection` est un drapeau** : `"0"` est retiré avant l'enregistrement. Un champ `int` avec
    `detection` garde son `"0"` (vraie mesure).
42. **Une condition de champ inconnue MASQUE le champ** ; **une `detection` inconnue le laisse vide** : tous deux en
    silence.
43. **Ne garde que des clés déclarées** : le panneau ne reporte que celles de la description.

### 14.4 Textes, images, interface

44. **Un pack sans texte français est muet en français sans que rien ne le signale.**
45. **Vocabulaire officiel** ; jamais « étourdi », « Inébranlable », « Robustesse », « carte de statut Robuste » : une gate
    échoue.
46. **Noms propres et traits restent en anglais** dans le texte français.
47. **Les biographies de vilain s'indexent par le `card_id` de la première face**, jamais par le nom.
48. **Une planche posée en tête de la colonne de récit** de l'écran de campagne en ordre libre **pousse le carnet hors
    de l'écran** : un test d'écran vérifie la présence, pas la place ; regarde une capture.
49. **Les pages du livret sont carrées, 975 × 975** ; les pages françaises vont dans `fr/` ; `livret_fr: true` sinon
    l'écran ne les cherche pas.
50. **Une chaîne d'interface nouvelle sans entrée dans `dico-en`** reste en français dans l'interface anglaise.

### 14.5 Méthode et fidélité

51. **Transcris une planche de 4 cartes par lecture** : au-delà, le texte d'encart n'est plus sûr.
52. **Les fichiers de l'auteur font foi, pas les captures de son livret** (la page 15 du livret de Web of Deceit
    montre un Shocker que la carte du dossier ne porte plus).
53. **Les icônes de complot n'ont pas la même forme chez tous les auteurs.** Conventions **validées par l'utilisateur**,
    **propres à leur pack** : *Skrull Menace* (Kajislav) — Crise = « ! » dans une explosion ; Accélération = croix +
    pointe + barre ; Aléas (Hazard) = croix sur carte penchée ; Amplify = croix + avion ; « Y » rouge = icône de
    boost ordinaire ; ★ = renvoi au texte. *MC/DC Punisher 2026* — « !! » = Crise ; croix à trois pointes + = Amplify ;
    triangle « toit de maison » + = Accélération ; carré « carte + » = Aléas. **Compare toujours à une carte du
    MÊME pack dont l'icône est connue ; une icône inconnue → `QUESTIONS.md`.**
54. **Une carte « impr. Interrupt » dont le texte dit « After »** : question à l'utilisateur, **pas de correction
    silencieuse** (Swarmed by Rats, Hunting Season).
55. **« Je n'ai pas lancé » ≠ « c'est vert »** : écris-le. Une livraison antérieure ne devait pas être déclarée
    jouable avec des points ouverts.
56. **Une gate qui répond OK n'est pas une preuve tant qu'on ne l'a pas vue échouer** ; ne retire jamais une assertion
    parce qu'elle échoue (le défaut revient en jeu).
57. **Un cas de test peut être vert en n'exerçant rien** (une carte du deck paie à elle seule le coût ; le pilote décline
    les choix facultatifs) : fixe la main (`main_exclusive`), mesure un **chiffre**.


---

## 15. Glossaire et index des annexes

### 15.1 Les mots du projet

| Mot | Sens ici |
|---|---|
| **Boîte** | une campagne livrée en une extension (« The Mad Titan's Shadow ») ; son fichier `data/campagnes/<code>.json` |
| **Pack** | la clé d'un groupe de cartes dans `cards.json` (`mts`, `web_of_deceit`) et le dossier `src/cards/pack/<pack>/` |
| **Set** | un groupe de cartes qui partagent un `set_name` (« Shocker », « Crime Wave ») ; un **set de rencontre** est un fichier `data/encounter_sets/<id>.json` |
| **Modulaire** | un set de rencontre que le livret recommande d'ajouter à un scénario (`modular_sets`) |
| **Scénario** | un fichier `data/scenarios/<id>.json` (et `_expert`) : un vilain, ses complots, ses sets |
| **Carnet** | le dictionnaire clé→texte qui voyage d'un scénario au suivant (`campaign_log`) |
| **Carnet entrant / sortant** | celui qu'on donne à la mise en place / celui que la fin de partie écrit |
| **Collecteur** | la fonction `Collect…(level, effect)` qui calcule le carnet sortant (`WriteCampaignLogAtGameOver`) |
| **Détecteur** | une règle de `detecteurs.ts` qui lit le monde de fin de partie et propose une valeur de carnet |
| **Champ de victoire** | un élément de `victoire` : une clé du carnet que le panneau propose de reporter |
| **Panneau de récompenses** | l'écran de fin de partie où le joueur valide ce qui est reporté |
| **Estampille** | l'`id` de scénario que le collecteur écrit dans `campaign_log_last.json` |
| **Niveau** | le numéro de scénario passé à `CampaignSetup(niveau)` |
| **Face 1A** | la face A du premier complot principal du scénario : porte le branchement de campagne |
| **`A_FAIRE_CLAUDE`** | le marqueur d'un manque que l'IA ne peut pas combler seule |
| **Épreuve** | un test de boucle de campagne (deux parties) de `tools/epreuves_campagnes.py` |
| **Cas** | un test de capacité de `tools/cas/<bloc>.py` (une partie) |
| **Gabarit** | la fiche de preuves d'une carte (`PROCESSUS-CARTE`) |
| **Sonde** | `tools/sonde_campagne.py` : monte une partie et rend l'état tel que le plateau le voit |

### 15.2 Anglais → français (statuts, mots-clés, types) — référence de traduction

Voir le tableau du §10.3. Compléments : **Hero/Alter-Ego** (Héros/Alter ego), **Ally** (Allié), **Event**
(Événement), **Upgrade** (Amélioration), **Support** (Soutien), **Resource** (Ressource), **Obligation**,
**Minion** (Sbire), **Treachery** (Traîtrise), **Attachment** (Attachement), **Environment** (Environnement),
**Main Scheme** (Manigance principale), **Side Scheme** (Manigance annexe), **Villain** (Méchant), **Encounter
deck** (deck Rencontre), **Boost card** (carte de boost), **Threat** (menace), **Acceleration token** (pion
Accélération), **Hazard** (Aléas), **Crisis** (Crise), **Campaign log** (carnet de campagne), **Setup**
(mise en place), **Standard / Expert** (Standard / Expert), **Round** (round).

### 15.3 L'index des annexes du zip

| Fichier | Contenu | Quand l'ouvrir |
|---|---|---|
| `annexes/A-kit-cartes.md` | **Kit de création de cartes** (6 100 lignes) : format `cards.json`, scripts, **67 exemples réels classés par mécanique**, pièges, format de livraison | pour écrire un script : chercher la carte modèle |
| `annexes/B-recettes-moteur.md` | **Recettes** : mécanique imprimée → fabrique + carte modèle + piège, et les pièges payés pack par pack | devant une mécanique inhabituelle |
| `annexes/C-mots-cles-tous.md` et `annexes/C-mots-cles/` | les **fiches de mots-clés** (officiels et maison) : ce que le moteur en fait | dès qu'un mot-clé apparaît sur une carte |
| `annexes/D-processus-carte.md`, `D-processus-heros.md` | le processus qualité d'une carte, d'un héros | pour remplir un gabarit ; si la campagne apporte un héros |
| `annexes/E-guide-creation-contenu.md` | le guide de référence (architecture, formats, validation, harnais) | pour les commandes de validation, le harnais |
| `annexes/F-campagnes-etat-des-lieux.md` | l'**état des lieux du mode campagne** (07/08/2026, + audit texte-vs-code, bilan) | pour l'historique et les mesures |
| `annexes/G-journal-portage-web-of-deceit.md` | le **journal** de la campagne maison, 1 500 lignes | comme récit de méthode |
| `annexes/H-boucle-de-campagne-dix-boites.md` | la boucle de campagne mesurée sur dix boîtes (huit défauts trouvés) | pour comprendre les épreuves |
| `annexes/I-index-api-moteur.md` | **l'index de l'API du moteur** : chaque classe et fonction, ses arguments, sa première ligne | **pour ne rien inventer** |
| `annexes/J-architecture-et-code.md` | l'architecture du projet : couches, flux, emplacement de chaque chose | pour situer un fichier |
| `annexes/J2-carte-du-code-juillet.md` | les 7 documents de cartographie du code du 28/07/2026 (**datés**) | en complément |
| `annexes/K-skrull-menace-*.md` | le tableau règle-par-règle d'une campagne complète et le brief des agents | comme modèle de preuve |
| `commun/` | les **fichiers génériques** du moteur, du serveur, de l'écran et du plateau qui font marcher une campagne | pour lire le code réel |
| `reference/*.json` | les listes du jeu (ids, sets, traits, compteurs, préfixes, clés de carnet, noms d'API) | utilisées par le vérificateur |

### 15.4 Commandes utiles (pour Claude ; à titre d'information)

```bash
W="/home/oem/Desktop/Marvel LCG/Fusion/marvel-lcg-src"
PY="/home/oem/Desktop/Marvel LCG/.venv-linux/bin/python"           # Python 3.10
python3 outils/verifier-livraison-campagne.py <livraison> --moteur "$W"   # la forme, contre le jeu réel
python3 outils/comparer-livraison-au-depot.py <livraison> <pack> <code>  # refaire une campagne connue : identique / différent / manquant
cd "$W" && "$PY" tools/verifier_campagnes.py                       # les clés de campagne
cd "$W" && RELEASE=1 PARALLELES=4 CAS_PREFIX=cz "$PY" tools/test_campagnes.py "$W/.game-src" 48000 /tmp/rapport-campagnes.json
cd "$W" && "$PY" tools/test_capacites.py "$W/.game-src" 25600 /tmp/rapport-capacites.json "[filtre]"
cd "$W" && "$PY" tools/recalculer_checksums.py "$W" data/cards.json data/sets_info.json   # PYTHONPATH=$W/src
```

