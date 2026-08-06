# Scans de cartes en français

**Date :** 2026-08-06
**Statut :** conçu, validé, non planifié
**Rapport à la roadmap :** hors roadmap. Demande directe, issue du dépôt d'un pack d'images OCTGN FR dans le projet.

---

## 1. Le problème

Le jeu affiche les scans anglais de toutes les cartes, quelle que soit la langue de l'interface. Le bouton 🌐 FR/EN ne traduit que les libellés du plateau et la narration du moteur : le texte de règles que le joueur lit réellement, celui imprimé sur la carte, reste en anglais.

Un pack d'images officielles françaises a été déposé dans `Fusion/marvel-lcg-src/assets/pics-fr/OCTGN_Image_pack_FR/` : 61 fichiers `.o8c` (427 Mo), qui sont des archives ZIP au format OCTGN. Elles contiennent 4 003 scans JPEG, dont 3 663 rectos, 334 versos (suffixe `.b`) et 6 troisièmes faces (suffixe `.c`).

Ces images ne sont pas utilisables telles quelles. Elles sont nommées par **GUID OCTGN** (`00c2957b-8a7e-40f9-9f52-62f4c3c175e9.jpg`), alors que le jeu résout ses images par code de carte (`01001a`). Aucun nom de carte ne figure dans les archives, et ni `data/cards.json` ni `data/translate_fr.json` ne contiennent de GUID OCTGN. La correspondance doit venir de l'extérieur.

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
| Source du mapping GUID vers code | marvelcdb (`octgn_id`) et le module OCTGN officiel, croisés |
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

**Étape 1, la table de correspondance.** Le script interroge l'API marvelcdb, qui expose `octgn_id` pour chaque carte (vérifié : `01001a` donne `18ae183c-de26-4369-8a41-424d58f01631`). Il récupère en parallèle les `set.xml` du module OCTGN officiel, qui associent le même GUID à un numéro de carte. Les deux sources sont croisées :

- GUID présent dans les deux et concordant : retenu ;
- GUID présent dans une seule : retenu, mentionné dans le rapport ;
- GUID présent dans les deux mais divergent : **écarté**, listé dans le rapport pour arbitrage humain. Un scan attribué à la mauvaise carte est pire qu'un scan manquant.

Si le module OCTGN est inaccessible, le script continue sur marvelcdb seul et l'écrit en tête du rapport, pour qu'une couverture obtenue sans recoupement ne soit jamais prise pour une couverture vérifiée.

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
| GUID divergent entre les deux sources | Écarté, la carte reste en anglais, la divergence est listée dans le rapport |
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
