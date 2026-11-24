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
{{BLOC:Fusion/marvel-lcg-src/tools/cas/hala_ultimatum.py|# Cas test_capacites du scenario 3 HALA ULTIMATUM|    # ============================================================== Avancee de stade (native) garde le cote|python}}

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
{{PUZZLE:}}

⚠ **`Puzzle.*` désigne une carte par son NOM (ou son `card_id` pour les cartes de rencontre/joueur), jamais par le
`card_id` d'une identité** : `Puzzle.ChangeForm('Amadeus Cho')`, pas `Puzzle.ChangeForm('68001b')` (un `card_id`
d'identité fabrique une carte orpheline et plante le rendu). **Désigne toujours une carte par son `card_id` quand
le nom n'est pas unique** (deux « Venom Blast » existent).

{{SECTION:docs/reference/GUIDE-CREATION-CONTENU.md|Quatre clés du harnais servent|Trois commandes ajoutées|1}}

{{SECTION:docs/reference/GUIDE-CREATION-CONTENU.md|Le vérificateur générique `etat_attendu`|**Deuxième campagne du 4/8/2026**|1}}

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

{{BLOC:Fusion/marvel-lcg-src/tools/epreuves_campagnes.py|"""Les EPREUVES de boucle de campagne|EPREUVES = []|python}}

**Ce que tu livres** : `integration/tools/epreuves.<code>.fragment.py`, qui commence par `EPREUVES += [` et contient
**au moins** :

* **une épreuve par scénario** qui vérifie le **carnet sortant** (`carnet_attendu: {"gagnee", "scenario", "cles",
  "cles_presentes", "cles_absentes"}`) — **dont l'estampille `scenario`**, qui doit égaler l'`id` du scénario ;
* **une épreuve par récompense** (et par pénalité) : `partie 1` écrit la clé, `partie 2` (`suivant`) montre
  l'effet (`attendu`) — **et son témoin** (le même scénario **sans** carnet, où l'effet est **absent**) ;
* **une épreuve de défaite** : le carnet reste intact, rien n'est coché ;
* **une épreuve expert** par règle expert (PV persistants, soin contre pion, obligation de soin).

**Épreuves réelles de The Mad Titan's Shadow** (les cinq scénarios d'une boîte officielle) :
{{BLOC:Fusion/marvel-lcg-src/tools/epreuves_campagnes.py|L'Ombre du Titan Fou (mts)|Les plus recherches de la galaxie (gmw)|python}}

**Épreuves réelles de Web of Deceit** (campagne maison, sans collecteur : ne mesure que ce que le carnet *change*) :
{{BLOC:Fusion/marvel-lcg-src/tools/epreuves_campagnes.py|La Toile du Mensonge (web_of_deceit)|Hunting Season (hunting_season)|python}}

### 11.4 La boucle d'une campagne : les pièges payés en la mesurant (`RECETTES-MOTEUR.md` §7quaterdecies)

{{SECTION:docs/reference/RECETTES-MOTEUR.md|### 7quaterdecies. Mesurer la BOUCLE|### 7quindecies|1}}

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
