
---

## 9. Ce que tu livres, exactement, et dans quel ordre travailler

### 9.1 L'ordre de travail recommandé

Livre **par lots** (un message, ou un lot de fichiers, par étape) plutôt que tout d'un coup : la relecture de Claude
est plus fiable, et une erreur de méthode se corrige au premier lot.

| Phase | Tu fais | Tu produis |
|---|---|---|
| **0. Lecture** | Regarder **toutes** les images du héros (face héros, alter ego, chaque carte signature, l'obligation, le set némésis, les éventuelles cartes d'aspect) et lire le matériel de l'auteur (decklist, notes). Compter les cartes et les exemplaires. | notes de travail (pas de livrable) |
| **1. Cadrage** | Choisir l'**identifiant de deck** (`deck/starter/<id>.json`), la **clé du pack**, proposer **deux préfixes** libres (question à choix multiple, héros maison). Vérifier que l'identifiant de deck n'existe pas (`reference/decks-existants.json`). | `QUESTIONS.md` (premières questions), `MANIFESTE.md` (squelette) |
| **2. Cartes** | Transcrire **chaque carte** (quatre par lecture de planche au plus), numéroter sans trou, remplir `desc`, `traits`, `set_name`, `custom`. | `integration/data/cards.<pack>.fragment.json`, `images.md` |
| **3. Deck et extension** | Écrire `deck/starter/<id>.json` (+ variantes), l'entrée `sets_info` et, si utile, le set némésis nommé. | `integration/deck/starter/*`, `…/sets_info.<pack>.fragment.json`, `…/nemesis/*` |
| **4. Scripts** | Un script par face de carte à capacité, **carte par carte**, avec son gabarit. | `integration/src/cards/pack/<pack>/…`, `GABARITS.md` |
| **5. Textes et habillage** | Textes français, biographie, réplique (à proposer), préfixe, crédits. | `integration/textes-fr/…`, `…/heros-info.fragment.js`, `…/repliques-heros.fragment.js`, `…/prefixes.<pack>.fragment.json`, `CREDITS.md` |
| **6. Preuves** | Les cas de test de capacité (avec les contre-cas de l'autre forme et les témoins d'épuisement). | `integration/tools/cas/<id>.py` |
| **7. Auto-vérification** | Lancer `verifier-livraison-heros.py` ; relire chaque checklist ; compter les `A_FAIRE_CLAUDE`. | `AUTO-VERIFICATION.md`, `A_FAIRE_CLAUDE.md`, `BESOINS-MOTEUR.md`, `QUESTIONS.md` à jour |

### 9.2 L'arborescence de la livraison

Elle **reproduit celle du projet** (chemins relatifs à la racine du moteur), pour que Claude fusionne sans
deviner. Voici la livraison d'une héroïne imaginaire `ma_heroine` (pack `ma_heroine`, préfixe `mh`, deck `ma_heroine`) :

```
livraison/
├── MANIFESTE.md                    la liste de TOUS les fichiers livrés (§9.3)
├── QUESTIONS.md                    les questions ouvertes (§9.4)
├── BESOINS-MOTEUR.md               ce que le moteur / l'interface devra apprendre (§9.5)
├── A_FAIRE_CLAUDE.md               tous les marqueurs A_FAIRE_CLAUDE regroupés (§9.6)
├── GABARITS.md                     un gabarit de contrôle par carte à capacité (§6.9)
├── AUTO-VERIFICATION.md            ce que tu as vérifié, avec la sortie du vérificateur (§9.7)
├── CREDITS.md                      (§7.5)
├── images.md                       card_id → fichier source (§7.2)
└── integration/
    ├── data/
    │   ├── cards.ma_heroine.fragment.json             {"ma_heroine": [ ...cartes... ]}
    │   ├── sets_info.ma_heroine.fragment.json         {"N. Custom (Ma heroine)": {...}}
    │   └── nemesis/ma_heroine_nemesis.json            (facultatif)
    ├── deck/starter/
    │   ├── ma_heroine.json
    │   └── ma_heroine_variante.json                   (une variante, §5.3)
    ├── src/cards/pack/ma_heroine/
    │   ├── __init__.py                                helpers partagés du pack
    │   ├── ma_heroine/__init__.py   mh001a.py  mh001b.py  mh002.py ...      (set « Ma Heroine »)
    │   └── ma_heroine_nemesis/__init__.py  mh014.py ...                      (set « Ma Heroine Nemesis »)
    ├── textes-fr/ma_heroine.fragment.txt              lignes pour textes-fr-fanmade.ts
    ├── public/js/prepare/
    │   ├── heros-info.fragment.js                     la biographie (clé = face héros)
    │   └── repliques-heros.fragment.js                la ligne de répliques (clé = id de deck)
    └── tools/
        ├── prefixes.ma_heroine.fragment.json          entrée de prefixes_fanmade.json
        ├── cas/ma_heroine.py                          cas de test de capacité
        └── decks-de-test.fragment.json                (facultatif, §8.4)
```

**Règles de forme** :

* **Encodage UTF-8, fins de ligne `\n`**, JSON indenté de 4 espaces, `ensure_ascii=False`.
* **Un fichier par face de carte à capacité** ; **jamais** deux cartes dans un même script.
* Aucun fichier **hors** de cette arborescence ; aucun fichier temporaire ; **aucun** dossier `scenarios`,
  `encounter_sets` ou `campagnes` (c'est une livraison de héros).
* **Les fragments contiennent *seulement* ta part** : jamais une copie, même partielle, d'un fichier partagé.
* **Aucune modification d'un fichier existant du projet** : tout nouveau fichier ; tout ce qui doit changer dans
  un fichier existant (moteur, interface, liste blanche de traits ou compteurs) va dans `BESOINS-MOTEUR.md`.

### 9.3 `MANIFESTE.md`

Une ligne par fichier livré :

```
| Chemin (dans integration/)                         | Rôle                                  | Cartes / entrées | Statut |
|----------------------------------------------------|---------------------------------------|------------------|--------|
| data/cards.ma_heroine.fragment.json                | cartes du pack                        | 31 faces         | complet |
| src/cards/pack/ma_heroine/ma_heroine/mh001b.py     | Setup + Réponse de l'alter ego        | 1                | A_FAIRE_CLAUDE ×1 |
```

**Statut** : `complet` · `partiel (A_FAIRE_CLAUDE ×n)` · `brouillon`. À la fin du manifeste : les totaux (cartes,
faces, scripts, decks de départ, cas de test, `A_FAIRE_CLAUDE`).

### 9.4 `QUESTIONS.md` — une question par entrée, format fixe

```
### Q<n> — <card_id ou règle> : <le doute en une phrase>

Image / source : <fichier de la carte>
Texte imprimé : « … »

Lectures possibles :
  A. (recommandée) <lecture> — en jeu : <ce que ça change>
  B. <lecture> — en jeu : <ce que ça change>
  C. Autre (précise)

Lecture retenue en attendant : A  (repérée par `# QUESTION <n> :` dans <fichier>)
```

Une **seule** question à la fois est posée à l'utilisateur (règle 4, §1.2) ; ce fichier les **range** pour Claude.
Une question **tranchée** garde sa place, avec la réponse et sa date. Le dossier `modeles/E-questions-iron-fist/`
du zip contient les questions et les cinq réponses réelles du héros Iron Fist (la forme exacte attendue).

### 9.5 `BESOINS-MOTEUR.md` — format fixe

```
### B<n> — <titre court>

Image / source : <fichier de la carte>, « … »
Ce que le jeu fait déjà de plus proche : <fichier : fonction, ou « rien »>
Ce qui manque : <comportement attendu, décrit ; pas de code>
Dépend : <card_id(s), champ(s) de description>
En attendant : <A_FAIRE_CLAUDE posé dans <fichier>, ou lecture retenue>
```

Y vont **aussi** : les **traits nouveaux** (`trait nouveau : TELEPORT, porté par lj008–lj012`), les **compteurs
nouveaux** (`compteur nouveau : chi, posé sur l'identité 64001a`), les **événements à deux capacités `Play`**
(liste blanche, §8.5), les **chaînes d'interface nouvelles** avec leur traduction anglaise, les **particularités
d'habillage** (identité alternative à art différent, forme de plus, bulles de statistiques inhabituelles).

### 9.6 `A_FAIRE_CLAUDE.md`

Tous les marqueurs `# A_FAIRE_CLAUDE:` du code, regroupés : `fichier : ligne : texte imprimé visé : ce qui manque :
carte de référence la plus proche`. **Un marqueur dans le code qui n'est pas dans cette liste est une faute.**

### 9.7 `AUTO-VERIFICATION.md`

```
## Vérificateur de livraison
$ python3 verifier-livraison-heros.py livraison/
<la sortie complète, collée>

## Relectures faites (cochées seulement si faites)
- [x] §4.9 checklist des cartes du héros
- [x] §6.10 auto-relecture de chaque script
- [x] §5.2 règles de contenu du deck (aucune signature étrangère, obligation, némésis)

## Ce qui n'a PAS été vérifié (à exécuter par Claude)
- cas de test de capacité : écrits, non exécutés
- verifier_tous_les_decks : non exécuté
- aucune partie jouée
```

### 9.8 Ce que tu ne fais jamais (rappel)

Pas d'images ni de scans ; pas de checksum ; pas de commit ni de déploiement ; pas de modification du moteur ; pas de
deck de départ inventé pour un héros maison ; pas de « vert » non exécuté ; pas de chiffre de test non mesuré ;
**pas de décision de règle en silence**.

### 9.9 Quand Claude te rend son retour

Claude compare ta livraison au dépôt (`outils/comparer-livraison-heros-au-depot.py` quand le héros existe déjà,
sinon lecture carte par carte avec l'image), lance les gates du chapitre 8 et te rend : les corrections faites,
les questions qu'il pose à l'utilisateur, ce qui reste NON. Les lots suivants reprennent là où il s'est arrêté.
