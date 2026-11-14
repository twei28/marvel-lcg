
---

## 12. Référence commune aux campagnes et aux héros

Ce chapitre reprend, **mot pour mot**, les tableaux du manuel de campagne qui valent aussi pour un héros : clés d'une
carte, `desc` complet, balises du texte imprimé, icônes de ressource, mots-pièges. **Les numéros de section
(4.2, 4.5, 4.6, 4.8, 6.7) sont ceux du manuel de campagne** (annexe L), pas ceux de ce manuel. Les renvois `§N` à
l'intérieur renvoient eux aussi à l'annexe L ; là où ils parlent de scénarios ou de carnet, ignore-les.

### 12.1 Clés de premier niveau d'une carte (campagne §4.2)

{{SECTION:docs/kit-campagne-ia/KIT-CAMPAGNE-COMPLET.md|### 4.2 Clés de premier niveau|### 4.3 Les types|0}}

### 12.2 `desc` : le contenu complet (campagne §4.5)

{{SECTION:docs/kit-campagne-ia/KIT-CAMPAGNE-COMPLET.md|### 4.5 `desc`|### 4.6 Le texte|0}}

### 12.3 Le texte imprimé : balises et jetons (campagne §4.6) et cartes à plusieurs faces (§4.7)

{{SECTION:docs/kit-campagne-ia/KIT-CAMPAGNE-COMPLET.md|### 4.6 Le texte imprimé|### 4.9 Exemples|0}}

### 12.4 Mots-pièges du texte imprimé (campagne §6.7)

{{SECTION:docs/kit-campagne-ia/KIT-CAMPAGNE-COMPLET.md|### 6.7 Mots-pièges|### 6.8 Ce que tu livres|0}}

### 12.5 La surface d'un script, les types de capacité (campagne §6.2 et §6.3)

{{SECTION:docs/kit-campagne-ia/KIT-CAMPAGNE-COMPLET.md|### 6.2 Ce que le script|### 6.4 Le catalogue|0}}

### 12.6 Glossaire

| Mot | Sens ici |
|---|---|
| **Pack** | la clé d'un groupe de cartes dans `cards.json` (`lockjaw`) et le dossier `src/cards/pack/<pack>/` |
| **Set** | un groupe de cartes qui partagent un `set_name` (« Lockjaw », « Lockjaw Nemesis ») |
| **Identité** | la paire de faces `…a` (héros) / `…b` (alter ego) — éventuellement avec des formes de plus (`…c`) |
| **Face** | un côté d'une carte à deux côtés ; un script par face à capacité |
| **Signature** | une carte de classe `Hero` : elle appartient à un seul héros |
| **Deck de départ** | `deck/starter/<id>.json` : la fiche d'inscription du héros, pas un « deck de joueur » |
| **Variante** | un second deck de départ replié sous le premier (`variante_de`) ; ≠ identité alternative (`hero_alts`) |
| **Némésis** | le set `"<Héros> Nemesis"` ; son sbire est marqué `desc.Nemesis` |
| **Obligation** | une carte de rencontre « donnée » à l'alter ego (`desc.GiveTo`) |
| **Gate** | un contrôle qui doit passer pour que le travail soit terminé |
| **Cas** | un test de capacité de `tools/cas/<héros>.py` (une partie) |
| **Substitution** | la preuve qu'un cas est rouge sans le module de la carte |
| **Gabarit** | la fiche de preuves d'une carte (`PROCESSUS-CARTE`) |
| **`A_FAIRE_CLAUDE`** | le marqueur d'un manque que l'IA ne peut pas combler seule |
| **Fragment** | la part d'un fichier partagé que tu livres, à fusionner par Claude |

### 12.7 L'index des annexes du zip

| Fichier | Contenu | Quand l'ouvrir |
|---|---|---|
| `annexes/A-kit-cartes.md` | **Kit de création de cartes** : format `cards.json`, scripts, **67 exemples réels classés par mécanique**, pièges, format de livraison | pour écrire un script : chercher la carte modèle |
| `annexes/B-recettes-moteur.md` | **Recettes** : mécanique imprimée → fabrique + carte modèle + piège, et les pièges payés pack par pack | devant une mécanique inhabituelle |
| `annexes/C-mots-cles-tous.md` et `annexes/C-mots-cles/` | les **fiches de mots-clés** (officiels et maison) | dès qu'un mot-clé apparaît sur une carte |
| `annexes/D-processus-carte.md`, `D-processus-heros.md` | le processus qualité d'une carte, d'un héros | pour remplir un gabarit |
| `annexes/E-guide-creation-contenu.md` | le guide de référence (architecture, formats, validation, harnais) | pour les commandes de validation |
| `annexes/I-index-api-moteur.md` | **l'index de l'API du moteur** : chaque classe et fonction, ses arguments, sa première ligne | **pour ne rien inventer** |
| `annexes/J-architecture-et-code.md` | l'architecture du projet : couches, flux, emplacement de chaque chose | pour situer un fichier |
| `annexes/L-manuel-campagne-cartes-et-scripts.md` | le manuel de création de **campagne** (cartes, scripts, textes, pièges) | pour les chapitres généraux de cartes et de scripts |
| `annexes/M-gabarits-iron-fist.md` | les gabarits `PROCESSUS-CARTE` remplis d'un héros officiel (13 cartes) | comme modèle de preuve |
| `commun/` | les fichiers génériques du moteur, du lanceur et des outils qui font marcher un héros | pour lire le code réel |
| `reference/*.json` | les listes du jeu (ids, sets, traits, compteurs, préfixes, decks existants, cartes signature) | utilisées par le vérificateur |

### 12.8 Commandes utiles (pour Claude ; à titre d'information)

```bash
W="/home/oem/Desktop/Marvel LCG/Fusion/marvel-lcg-src"
PY="/home/oem/Desktop/Marvel LCG/.venv-linux/bin/python"                  # Python 3.10
python3 outils/verifier-livraison-heros.py <livraison> --moteur "$W"          # la forme, contre le jeu réel
python3 outils/comparer-livraison-heros-au-depot.py <livraison> <pack> <deck> # refaire un héros connu : identique / différent / manquant
cd "$W" && DECK_NOM=<deck> "$PY" tools/verifier_tous_les_decks.py             # le deck se monte (gate)
cd "$W" && CAS_PREFIX=<nom> PARALLELES=4 "$PY" tools/test_capacites.py "$W/.game-src" 31000 /tmp/rapport.json "[<deck>]"
cd "$W" && "$PY" tools/substituer_pack.py "$W/.game-src" 32000 <préfixe>      # la preuve par substitution
cd "$W" && "$PY" tools/recalculer_checksums.py "$W" data/cards.json data/sets_info.json   # PYTHONPATH=$W/src
```
