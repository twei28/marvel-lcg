# Scans de cartes en français

**Date :** 2026-08-06
**Statut :** conçu, validé, non planifié
**Rapport à la roadmap :** hors roadmap. Demande directe, issue du dépôt d'un pack d'images OCTGN FR dans le projet.

---

## 1. Le problème

Le jeu affiche les scans anglais de toutes les cartes, quelle que soit la langue de l'interface. Le bouton 🌐 FR/EN ne traduit que les libellés du plateau et la narration du moteur : le texte de règles que le joueur lit réellement, celui imprimé sur la carte, reste en anglais.

Un pack d'images officielles françaises a été déposé dans `Fusion/marvel-lcg-src/assets/pics-fr/OCTGN_Image_pack_FR/` : 61 fichiers `.o8c` (427 Mo), qui sont des archives ZIP au format OCTGN. Elles contiennent 4 003 scans JPEG, dont 3 663 rectos, 334 versos (suffixe `.b`) et 6 troisièmes faces (suffixe `.c`).

Ces images ne sont pas utilisables telles quelles. Elles sont nommées par **GUID OCTGN** (`00c2957b-8a7e-40f9-9f52-62f4c3c175e9.jpg`), alors que le jeu résout ses images par code de carte (`01001a`). Aucun nom de carte ne figure dans les archives, et ni `data/cards.json` ni `data/translate_fr.json` ne contiennent de GUID OCTGN. La correspondance doit venir de l'extérieur.

### Couverture attendue, mesurée avant écriture du plan

L'extraction a été simulée en entier, sans rien écrire sur le disque, contre le catalogue réel du jeu.

| Mesure | Valeur |
|---|---|
| Images dans le pack | 4 003, pour 3 643 GUID distincts |
| GUID inconnus de marvelcdb | 80, soit 2 % |
| Cartes du jeu couvertes en français | 4 210 sur 4 670, soit 90 % |
| Cartes officielles sans scan français | 77 |
| Cartes fan-made sans scan français | 353 |
| Poids après extraction | 456 Mo |

Ces nombres sont la référence : l'outil de vérification doit les retrouver après l'extraction réelle. Un écart signifie que le script a fait autre chose que ce qui était prévu.

## 2. Périmètre

**Dans le périmètre :** l'affichage des scans de cartes, l'option qui le commande, et le texte français de repli sous l'aperçu.

**Hors périmètre, inchangé :**
- la traduction de l'interface et de la narration (`langue.ts`, `dico-en.ts`, `translate_fr.json`), qui fonctionne déjà ;
- l'option ⚙ « Textes marvelcdb (réseau) » et le proxy `/marvelcdb_card`, qui restent tels quels ;
- les dos de cartes et les textures (`player`, `encounter`, `villain`), identiques dans toutes les langues ;
- le mode PC et le mode mobile, qui partagent le même point de résolution d'image et n'ont donc rien à changer.

**Hors de portée par nature :** les packs fan-made (Cloak & Dagger, Spider-Man Rainy, Moon Knight, Jessica Jones, Agent Anti-Venom, Lockjaw, Squirrel Girl). Ils n'existent ni dans le pack OCTGN FR, ni sur marvelcdb. Ils resteront en anglais, sans texte de repli, exactement comme aujourd'hui.

## 3. Cadrage retenu

| Sujet | Décision |
|---|---|
| Déclencheur | Option ⚙ dédiée, indépendante du bouton 🌐 FR/EN. On peut jouer en interface anglaise avec des scans français, et l'inverse |
| Valeur par défaut | ON |
| Source du mapping GUID vers code | marvelcdb (`octgn_id`) fait foi ; le module OCTGN sert d'audit et ne décide de rien |
| Stockage | Extraction en JPEG renommés sur le disque, pas de lecture des archives à la volée |
| Carte sans scan FR | Le scan anglais reste affiché, complété par le texte français sous l'aperçu |
| Source du texte de repli | Dictionnaire pré-généré, figé dans le dépôt, aucun réseau en partie |
| Portée du texte de repli | Uniquement les cartes restées en scan anglais |
| Contrôle | Rapport d'extraction, plus un outil de vérification réexécutable |

### Pourquoi une option séparée et non le bouton 🌐

La langue de l'interface et la langue des scans répondent à deux besoins différents. Un joueur peut connaître les cartes sous leur nom anglais, référence de tous les guides et de marvelcdb, tout en voulant une interface française. Coupler les deux lui retirerait ce choix. L'option séparée coûte une case à cocher et une clé `localStorage`.

### Pourquoi extraire plutôt que lire les archives

Servir une image depuis un ZIP demande d'ouvrir l'archive, de localiser l'entrée et de décompresser, à chaque première demande, dans le processus qui fait tourner la partie. L'extraction paie ce coût une fois et rend le chemin de service identique à celui des scans anglais, donc sans code nouveau côté moteur. Le prix est 430 Mo de disque, dans un dossier `Fusion/` déjà non versionné et qui pèse déjà 521 Mo de scans anglais.

## 4. Architecture

```
  61 fichiers .o8c            API marvelcdb            module OCTGN
  (GUID.jpg)                  (octgn_id, texte FR)     (set.xml)
        │                            │                       │
        └────────────┬───────────────┴───────────────────────┘
                     ▼
        importer_scans_fr.py   (one-shot, hors partie)
                     │
      ┌──────────────┼────────────────────┬──────────────────┐
      ▼              ▼                    ▼                  ▼
 assets/pics-fr/  scans-fr-liste.ts   textes-fr.ts      rapport-scans-fr.md
 fr_01001a.jpg    (codes en FR)       (textes FR)       (couverture, trous)
      │              │                    │
      ▼              ▼                    ▼
 cache.py        scans-fr.ts         ApercuMarvelcdb
 (+1 dossier)    (choix d'URL)       (repli texte)
```

Le principe directeur : **tout le travail est fait une fois, hors partie**. En jeu, il ne reste qu'un choix de nom de fichier.

### 4.1 Le script d'import

`Fusion/marvel-lcg-src/tools/importer_scans_fr.py`, exécuté à la main, jamais pendant une partie.

**Étape 1, la table de correspondance.** Le script interroge `https://fr.marvelcdb.com/api/public/cards/?encounter=1`, une seule requête de 7,6 Mo qui rend 4 375 cartes, dont 4 373 avec leur `octgn_id` et leur texte français. C'est la source de vérité.

Un point mesuré, contre-intuitif et structurant : **la correspondance GUID vers code n'est pas biunivoque**. Une carte de rencontre réimprimée d'une boîte à l'autre garde un seul GUID OCTGN mais reçoit un code marvelcdb par boîte. L'obligation `01088` compte ainsi 47 codes pour une seule image. À l'inverse, une carte à deux faces partage un GUID entre `01001a` et `01001b`, que seul le suffixe du nom de fichier distingue.

La règle d'attribution est donc :

- fichier `<GUID>.jpg` : tous les codes du GUID dont le suffixe de face est vide ou `a` ;
- fichier `<GUID>.b.jpg` : les codes en `b` ; `<GUID>.c.jpg` : les codes en `c` ;
- et, dans tous les cas, **filtrage sur le catalogue du jeu** : un code absent de `cards.json` n'est pas écrit. C'est ce filtre qui empêche les réimpressions d'inonder le dossier.

Une même carte peut recevoir une image depuis plusieurs archives (24 cas mesurés). Le script retient le fichier le plus lourd, choix déterministe qui privilégie la meilleure définition.

**Le module OCTGN sert d'audit, pas d'arbitre.** Le dépôt [twistedsistem/OCTGN-Marvel-Champions](https://github.com/twistedsistem/OCTGN-Marvel-Champions) porte le même identifiant de jeu que les archives (`055c536f-adba-4bc2-acbf-9aefb9756046`) et associe GUID et `CardNumber` dans ses `set.xml`. Mesure faite : il ne couvre que 33 sets sur 61 et ne rattrape qu'un seul des 80 GUID inconnus de marvelcdb. Il reste utile pour une seule chose, signaler les désaccords : sur 1 609 GUID connus des deux sources, 5 divergent, dont `24031` et `24032` qui sont **inversés** entre elles. Le script pose quand même le scan selon marvelcdb et écrit ces cas dans le rapport, à vérifier à l'œil.

Si le module est inaccessible, le script continue sans lui et l'écrit en tête du rapport : une extraction non auditée ne doit jamais passer pour une extraction vérifiée.

**Étape 2, l'extraction.** Pour chaque `.o8c`, chaque entrée `<GUID>[.b|.c].jpg` est traduite en code de carte. Le suffixe de face est reporté sur le code : `GUID.jpg` donne `01001a` quand la carte a deux faces, `01003` quand elle n'en a qu'une, et `GUID.b.jpg` donne `01001b`. Les faces sont celles déclarées par marvelcdb, jamais devinées. Le fichier est écrit tel quel, sans réencodage, sous `assets/pics-fr/fr_<code>.jpg`. Les entrées non-image (`Thumbs.db`) sont ignorées.

Les `.o8c` d'origine ne sont pas supprimés. Ils restent la source, et une réexécution du script est toujours possible.

**Étape 3, le dictionnaire de textes.** Le script relève le texte français de chaque carte sur marvelcdb et écrit `ui-app/src/board/textes-fr.ts`. Seul le champ de texte de règles est retenu, nettoyé des balises autres que `b`, `i`, `em`, `strong`, `br`, comme le fait déjà `ApercuMarvelcdb`.

**Étape 4, les sorties.** Le script écrit `ui-app/src/board/scans-fr-liste.ts` (le tableau des codes disponibles en français) et `RAPPORT-SCANS-FR.md` à la racine : nombre d'images placées, GUID non résolus, GUID divergents, et la liste des cartes du catalogue sans scan français, séparées en cartes officielles et cartes fan-made.

### 4.2 Le moteur

Une ligne dans `Fusion/marvel-lcg-src/src/engine/file/cache.py` :

```python
IMAGE_FOLDERS = ConfigVariables.Folders('image_folders', ["./assets/pics/", "./assets/pics-fr/"])
```

Aucune route nouvelle, aucune logique de langue côté serveur. C'est le préfixe `fr_` dans le nom du fichier qui distingue les deux collections. Trois conséquences utiles :

- le cache d'images du serveur est indexé par nom de fichier, donc `01001a` et `fr_01001a` ne se remplacent jamais l'un l'autre ;
- en multijoueur, deux joueurs réglés sur des langues différentes reçoivent chacun leurs images sans que le cache les mélange ;
- le cache du navigateur distingue les deux URL de la même façon.

### 4.3 Le plateau

**`ui-app/src/board/scans-fr.ts`**, module nouveau, seul détenteur de la règle :

- `scansFrActifs(): boolean`, lecture de `localStorage` sur la clé `marvel-board-scans-fr`, **absent vaut ON** ;
- `aScanFr(picId): boolean`, appartenance à la liste générée ;
- `picIdFr(picId): string`, qui renvoie `fr_<picId>` quand l'option est active et le scan existe, sinon `picId` inchangé.

Le nom `picIdAffiche` est déjà pris par `variantes.ts`, d'où `picIdFr`. Les deux ne font pas la même chose et ne se confondent pas.

**`card-model.ts`** applique ce choix dans `scanUrl()`, qui est le point unique par lequel passent le mode PC, le mode mobile, les dos de cartes et les autres faces d'une carte multi-faces. Aucun composant d'affichage n'est modifié pour l'image elle-même.

**Priorité sur les arts alternatifs.** `picIdAffiche` de `variantes.ts` substitue déjà le `pic_id` quand le joueur a choisi un art alternatif de héros ou une collection de ressources (`01088_dh_drax`). Ces variantes n'existent pas en français. La règle est que **la liste fait foi** : `picIdFr` s'applique après `picIdAffiche`, et comme `fr_01088_dh_drax` n'est pas dans la liste, le préfixe n'est pas posé. L'art choisi par le joueur est donc conservé, sans règle de priorité à écrire.

Note d'implémentation : `pic_id` et `card_id` coïncident sauf pour 19 entrées du catalogue (dos génériques `player`, `encounter`, `villain`, et le cas `01144` qui pointe vers `01144a`). Ces entrées ne figurent pas dans la liste FR, donc `picIdFr` les laisse passer sans les toucher.

**Le texte de repli.** `ApercuMarvelcdb` dans `Board.tsx` gagne une source locale et prioritaire :

1. si l'option scans FR est active **et** que la carte n'a pas de scan français, le texte vient du dictionnaire hors ligne ;
2. sinon, le comportement actuel est conservé à l'identique, y compris l'option réseau marvelcdb, qui reste OFF par défaut.

Le dictionnaire pèse environ 1 Mo. Il est chargé par `import()` dynamique, donc Vite en fait un morceau séparé, téléchargé seulement à la première carte concernée. Le plateau ne s'alourdit pas au démarrage.

**L'option ⚙** est ajoutée à côté de « Textes marvelcdb (réseau) » dans `board.tsx`, avec sa traduction dans `dico-en.ts`. Libellé : « Scans en français », détail : « Images des cartes en français quand elles existent ».

### 4.4 L'outil de vérification

`outils/verifier-scans-fr.mjs`, sur le modèle de `verifier-tutoriel-etat.mjs` et `verifier-salon-etat.mjs`. Il sort en erreur si :

- un code de `scans-fr-liste.ts` n'a pas son fichier dans `assets/pics-fr/` ;
- un fichier de `assets/pics-fr/` n'est pas dans la liste ;
- un code de la liste n'existe pas dans le catalogue.

Il affiche par ailleurs la couverture, cartes officielles et cartes fan-made séparées, sans échouer dessus. Une carte fan-made sans scan français est un fait, pas un défaut.

## 5. Erreurs et cas limites

| Situation | Comportement |
|---|---|
| `assets/pics-fr/` vide ou absent | La liste générée est vide, `picIdAffiche` ne change jamais rien, le jeu se comporte comme avant. Aucune requête perdue |
| Fichier effacé à la main après génération | La liste le croit présent, le serveur ne le trouve pas et l'image manque. C'est précisément ce que `verifier-scans-fr.mjs` détecte |
| Carte fan-made | Scan anglais, pas de texte de repli. Silencieux, comme aujourd'hui |
| Carte officielle trop récente pour le pack OCTGN | Scan anglais, texte français de repli si marvelcdb la connaissait à la génération |
| GUID divergent entre les deux sources | marvelcdb l'emporte, le scan est posé, la divergence est listée dans le rapport pour arbitrage à l'œil |
| GUID inconnu de marvelcdb | Image non extraite, GUID listé dans le rapport. Mesuré : 80 sur 3 643 |
| Option coupée en cours de partie | Le choix se fait au rendu, l'affichage suit au rafraîchissement suivant sans rechargement |
| Multijoueur, langues différentes | Chaque client choisit ses URL, le serveur sert les deux collections, les caches ne se croisent pas |

## 6. Tests

**Unitaires (vitest), sur `scans-fr.ts` :**
- option absente du `localStorage` : le mode FR s'applique (défaut ON) ;
- option coupée : `picIdFr` rend le `picId` inchangé, même pour une carte présente en français ;
- option active, carte présente en français : préfixe `fr_` appliqué ;
- option active, carte absente : `picId` inchangé ;
- `picId` non conforme au format code de carte (`player`, `encounter`) : inchangé dans tous les cas ;
- art alternatif actif (`01088_dh_drax`) avec option FR active : `picId` inchangé, l'art choisi survit.

**Unitaires, sur le repli texte :**
- carte avec scan français : aucun texte de repli, même en mode FR ;
- carte sans scan français, mode FR : le texte du dictionnaire s'affiche ;
- carte inconnue du dictionnaire : rien ne s'affiche, aucune erreur ;
- option scans FR coupée : le comportement marvelcdb réseau existant est intact.

**Vérification de données :** `verifier-scans-fr.mjs` sur le dossier réellement extrait.

**Non-régression :** la suite de tests existante du plateau doit passer sans modification. Le mode anglais est le chemin par défaut de `picIdAffiche`, donc toute régression sur les scans anglais est un échec de test.

## 7. Ce que la spec ne fait pas

- Traduire les cartes fan-made. Elles n'ont pas de scan français et n'en auront pas.
- Traduire les noms de cartes dans l'interface (historique, menus, journal). Seuls le scan et le texte de règles passent en français.
- Mettre à jour le dictionnaire ou les scans automatiquement. Le script est relancé à la main quand un pack officiel sort.
- Supprimer les archives `.o8c`. Décision laissée à l'utilisateur, hors du script.
