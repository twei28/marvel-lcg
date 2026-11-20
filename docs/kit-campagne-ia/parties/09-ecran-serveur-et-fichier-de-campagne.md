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
