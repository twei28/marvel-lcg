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
