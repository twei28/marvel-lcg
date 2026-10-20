
---

## 3. La liste maîtresse des fichiers d'un héros

Chemins relatifs à la racine du moteur (`Fusion/marvel-lcg-src/`) sauf mention. **A** = tu le produis dans
`livraison/integration/`. **C** = Claude le génère ou le met à jour (tu ne le livres pas).

### 3.1 Ce que tu produis (A)

| # | Fichier livré (dans `integration/`) | Contenu | Obligatoire | Chapitre |
|---|---|---|---|---|
| 1 | `data/cards.<pack>.fragment.json` | `{"<pack>": [ …toutes les cartes du pack… ]}` | oui | 4 |
| 2 | `data/sets_info.<pack>.fragment.json` | `{"N. Custom (<Nom>)": {name, scenarios: [], heroes: ["<héros>"], encounters: [], max_id}}` | oui | 5.5 |
| 3 | `deck/starter/<héros>.json` | le deck de départ (+ un fichier par **variante**) | oui | 5 |
| 4 | `data/nemesis/<héros>_nemesis.json` | le set némésis comme set nommé | non | 5.4 |
| 5 | `src/cards/pack/<pack>/__init__.py` | helpers partagés du pack (peut être minimal) | oui | 6.1 |
| 6 | `src/cards/pack/<pack>/<set_nettoyé>/__init__.py` | un par dossier de set | oui | 6.1 |
| 7 | `src/cards/pack/<pack>/<set_nettoyé>/<card_id>.py` | **un script par face de carte à capacité** | oui | 6 |
| 8 | `textes-fr/<pack>.fragment.txt` | lignes `'<card_id>': "texte français",` pour `textes-fr-fanmade.ts` | **oui** (fan-made) | 7.1 |
| 9 | `public/js/prepare/heros-info.fragment.js` | l'entrée de biographie, indexée par la face héros | **oui** (fan-made) | 7.3 |
| 10 | `public/js/prepare/repliques-heros.fragment.js` | la ligne de répliques, indexée par l'id de deck | non (à proposer) | 7.4 |
| 11 | `tools/prefixes.<pack>.fragment.json` | l'entrée de `prefixes_fanmade.json` | **oui** (fan-made) | 4.8 |
| 12 | `tools/cas/<héros>.py` | cas de test de capacité | recommandé | 8.2 |
| 13 | `tools/decks-de-test.fragment.json` | moitié d'aspect **de test** (harnais seulement) | non | 8.4 |
| 14 | `MANIFESTE.md` `QUESTIONS.md` `BESOINS-MOTEUR.md` `A_FAIRE_CLAUDE.md` `GABARITS.md` `AUTO-VERIFICATION.md` `images.md` `CREDITS.md` | le suivi | oui | 9 |

**Un héros officiel** (extension imprimée par l'éditeur) : mêmes fichiers, sans la clé `custom`, sans préfixe
(ids à cinq chiffres), sans fichier 8 si le texte français est déjà fourni par le jeu — mais un héros *récent*
(Iron Fist, MC64) a bien ses textes français dans `textes-fr-fanmade.ts` : vérifie dans les modèles.

### 3.2 Ce que Claude touche (C), à titre d'information

| Fichier | Quoi |
|---|---|
| `data/cards.json` | fusion de ton fragment ; **checksum recalculé** (un checksum faux est journalisé comme `Mismatch` par le moteur et fait refuser l'envoi de rejeux au serveur : le fichier fusionné doit donc être recalculé) |
| `data/sets_info.json` | fusion de ton fragment ; numéro `N.` attribué |
| `assets/pics/<card_id>.<jpg\|png\|webp>` | les images que l'utilisateur donne, uniformisées (`outils/uniformiser-scans.py`) |
| `ui-app/src/board/textes-fr-fanmade.ts` | fusion de ton fragment texte |
| `public/js/prepare/heros-info.js` / `repliques-heros.js` | fusion de tes fragments |
| `tools/prefixes_fanmade.json` | fusion de ton fragment |
| `ui-app/src/components/stat-bubbles/positions.ts`, `data/palettes-heros.json`, `data/identites.json` | générés depuis les images |
| `tools/test_capacites.py` (cas), `tools/substituer_pack.py`, `tools/verifier_tous_les_decks.py` | lancés ; ton fichier `tools/cas/<héros>.py` y est chargé automatiquement |
| `docs/packs/<héros>_cartes.md` | tes gabarits, relus et complétés par Claude |

### 3.3 Ce que tu ne livres jamais

Des images ; un checksum ; une copie (même partielle) d'un fichier partagé ; un fichier hors de l'arborescence ;
un fichier temporaire ; une modification du moteur ; un `player_deck` inventé pour un héros maison ; un commit.

### 3.4 Les trois formes de héros que le jeu connaît (pour te situer)

| Forme | Exemple | Ce qui change |
|---|---|---|
| **Héros simple** : une paire `a`/`b` | Lockjaw `lj001a`/`lj001b`, Iron Fist `64001a`/`64001b` | le cas normal |
| **Héros à formes multiples** : `a` héros, `b` alter ego, `c` (… `e`) autres formes | Ant-Man `12001a`/`b`/`c` (forme Géant), Conan `cn001a`…`cn001e`, Moon Knight `mk001a`…`mk001e` | `hero` dans le deck cite **toutes** les faces ; chaque face a ses propres stats et son script |
| **Identité liée** : deux identités pilotées par un joueur | Cloak & Dagger (`linked_identity`) | un mini-deck complet dans `linked_identity` (§5.6) ; un seul pack du jeu à ce jour |

Une **identité alternative** (même deck, autres faces : The Thing Guardian `th001c,th001d`) se déclare dans
`metadata.hero_alts` (§5.3) ; un **second deck de héros** (Hellcat / She-Hulk) est une **variante** (§5.3).
