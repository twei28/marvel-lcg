
---

## 10. Quatre héros complets, fichier par fichier : les modèles du zip

Le dossier `modeles/` du zip contient, pour **quatre héros qui marchent en jeu**, la livraison telle qu'une IA
aurait dû la rendre (reconstituée depuis le dépôt par `outils/livraison-heros-depuis-le-depot.py`). Les fichiers de
suivi (`MANIFESTE.md`, `images.md`…) sont **générés** : ils montrent la forme attendue.

| Dossier | Héros | Pourquoi ce modèle | À regarder |
|---|---|---|---|
| `A-officiel-ant-man/` | **Ant-Man** (pack officiel `ant`, ids `12001a`…) | héros officiel **à trois formes** (`12001a`/`b`/`c`), obligation, set némésis, 25 cartes de `player_deck`, cartes d'aspect de la boîte (`set_name` vide) | `deck/starter/ant_man.json`, `12001c` |
| `B-maison-lockjaw/` | **Lockjaw** (Nugget, préfixe `lj`) | héros **maison complet** : decklist de l'auteur, obligation à choix, set némésis avec complot annexe en paysage, 13 cartes d'aspect, mot-clé maison (*Companion*) | `lj001a`/`b`, `lj013`, `lj015`, `heros-info.fragment.js` |
| `C-maison-harry-osborn/` | **Harry Osborn / Green Goblin** (préfixe `ho`) | héros maison (Dipsome) **sans decklist d'auteur** (`player_deck` vide), règle de deck-building propre (`hors_aspect`), face alter ego sans script | `deck/starter/harry_osborn.json`, `ho001a.py` |
| `D-officiel-recent-iron-fist/` | **Iron Fist** (MC64, novembre 2026) | héros officiel **partiellement publié** : ni obligation, ni némésis, `player_deck` vide, `deck_note` qui le dit ; **57 cas de test**, jeton Chi sur l'identité, gabarits `PROCESSUS-CARTE` complets | `tools/cas/iron_fist.py`, `GABARITS.md` |
| `E-questions-iron-fist/` | les questions et les cinq réponses de l'utilisateur sur Iron Fist | la forme réelle de `QUESTIONS.md` et des décisions | tout |

Les images d'exemple (`images-exemples/`) donnent les formats réels : une face héros, un alter ego, un allié, un
complot annexe de némésis en paysage.

### 10.1 Lecture guidée : le plan de cartes de Lockjaw

{{TABLECARTES:lockjaw}}

### 10.2 Lecture guidée : le plan de cartes d'Ant-Man

{{TABLECARTES:ant}}

### 10.3 Lecture guidée : le plan de cartes d'Iron Fist

{{TABLECARTES:iron_fist}}

### 10.4 Le plan de cartes de Harry Osborn

{{TABLECARTES:harry_osborn}}

### 10.5 Un gabarit de contrôle réel : Iron Fist

Le fichier `docs/packs/iron_fist_cartes.md` (annexe `annexes/M-gabarits-iron-fist.md`) contient les gabarits
`PROCESSUS-CARTE` remplis des 13 cartes. Début : le périmètre, les sources, la preuve de chaque gate, les
décisions de l'utilisateur appliquées.

{{EXTRAIT:docs/packs/iron_fist_cartes.md|1|58|markdown}}
