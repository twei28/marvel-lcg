# TODO / SPEC — Rechercher et jouer des decks MarvelCDB

**Statut :** conçu, non planifié, non implémenté
**Date de conception :** 2026-07-28
**Origine :** demande utilisateur (« quand on clique sur un héros, pouvoir chercher des decks de ce perso sur MarvelCDB »)
**Rapport à la roadmap :** hors des 7 phases de la refonte UI. À insérer quand la phase 4 (préparation de partie) sera abordée, ou avant si l'envie prime.

---

## 1. Le problème

Aujourd'hui on ne joue qu'avec les 65 decks préconstruits de `deck/starter/`. Construire un deck se fait dans `deck.html`, hors du flux de préparation, et le résultat doit être téléchargé puis rechargé à la main.

MarvelCDB héberge des dizaines de milliers de decks joueurs. On veut, depuis l'écran de préparation, cliquer sur un héros et voir les decks de ce héros, en choisir un, et lancer la partie avec.

## 2. Ce qui existe déjà (vérifié le 28/07/2026)

- **`deck.html` importe déjà un deck MarvelCDB par son identifiant** (`api/public/deck/{id}.json` pour un deck privé partagé, `api/public/decklist/{id}.json` pour une publication). Il ne remplit que `player_deck`, ne cherche rien, et vit hors du flux de préparation.
- **L'API MarvelCDB répond avec `access-control-allow-origin: *`** : le navigateur peut l'appeler directement, aucune modification du serveur Python n'est nécessaire.
- **`/read_file?<chemin>` sert n'importe quel fichier JSON du dossier de jeu**, gzippé, avec en-têtes de cache. C'est la porte d'entrée pour servir l'index : le routage par extension du serveur ne connaît pas `.json` (piège déjà documenté en phase 1), mais `read_file` le contourne sans toucher au backend.
- **`/new?data=` accepte le JSON du deck en ligne** (`hero_json`, un par joueur) : un deck importé n'a jamais besoin d'être enregistré côté serveur pour être joué.
- Aucun endpoint d'écriture de fichier n'existe côté serveur. Tout ce qui doit persister passe soit par un script côté hôte, soit par le navigateur.

## 3. La contrainte qui dicte l'architecture

**L'API publique MarvelCDB n'a aucune route de recherche.** Testé : `decklists/popular`, `decklists/hot`, `decklists/by_hero`, `decklists/recent`, `decklists/search` répondent toutes 404. La seule route de liste est :

```
GET https://marvelcdb.com/api/public/decklists/by_date/AAAA-MM-JJ.json
```

Elle renvoie les decks publiés ce jour-là, **contenu compris** (`slots`), avec `hero_code`, `hero_name`, `name`, `meta.aspect`, `tags`, `date_creation`, `user_id`.

Volume mesuré : 2 decks/jour en 2019, 8 en 2020, 16 en 2022, 30 en 2024, ~18 en 2026. Sur toute l'histoire du site (oct. 2019 → aujourd'hui) : **~2 500 jours, ~40 000 decks**.

Conséquence directe : **la recherche ne peut pas être faite à la volée, elle doit être indexée**. Et comme `by_date` contient déjà les cartes, l'index est autosuffisant : choisir un deck ne demande aucune requête supplémentaire.

Autre conséquence, à assumer : **aucun signal de popularité n'existe dans l'API** (ni votes, ni favoris, ni vues). Le seul classement possible est chronologique.

## 4. Décisions prises

| Sujet | Décision |
|---|---|
| Source de la recherche | Index local construit depuis `by_date`, **plus** un champ « coller un lien MarvelCDB » pour un deck précis ou tout juste publié |
| Où vit l'index | Fichiers servis par l'hôte, donc partagés par tous les clients y compris les joueurs distants |
| Profondeur | Historique complet, **découpé par héros** (un fichier par `hero_code`) |
| Contenu de l'index | Métadonnées **et** cartes : un deck choisi est jouable sans internet |
| Après le choix | Le deck part directement en partie ; une étoile le met en favori (mémorisé dans le navigateur) |
| Cartes absentes du jeu | Decks incomplets masqués par défaut, case « tout montrer », badge nommant les cartes manquantes |
| Filtres | Aspect, tag solo/multijoueur, recherche par nom. Tri chronologique, décroissant |
| Qui choisit | L'hôte, pour tous les sièges, comme aujourd'hui |

## 5. Architecture

Trois morceaux séparés, dont **deux survivent à la refonte UI** :

```
  [A] Indexeur                [B] Module de recherche         [C] Vue
  Python, côté hôte           JS pur, sans DOM                prepare.html puis React
  tools/marvelcdb_index.py    public/js/marvelcdb/            (jetable)
        |                             |                             |
        v                             v                             v
  data/marvelcdb/<hero>.json  --> chargement + filtres  --> liste, clic, lancement
  data/marvelcdb/_meta.json       conversion en deck moteur
```

**[A] et [B] sont le socle durable.** [C] est la seule partie que la phase 4 réécrira.

### [A] L'indexeur — `tools/marvelcdb_index.py`

Script Python autonome (pas dans le moteur, pas d'import du moteur), lancé à la main ou branché sur le launcher.

1. Lit `data/marvelcdb/_meta.json` pour connaître la dernière date aspirée. Absent = premier passage, on part de `2019-10-01`.
2. Pour chaque jour manquant jusqu'à hier : `GET by_date/<date>.json`, avec un délai de 200 ms entre les appels et un User-Agent identifiant le projet. Un jour en erreur est réessayé une fois puis journalisé et sauté, sans arrêter le passage.
3. Regroupe les decks par `hero_code`, calcule pour chacun la jouabilité (voir §7), écrit un fichier par héros.
4. Met à jour `_meta.json` (dernière date, nombre de decks, date du passage).

Premier passage : ~2 500 requêtes, environ 15 minutes. Passages suivants : un appel par jour écoulé depuis le dernier, donc quelques secondes.

Le script est **incrémental et rejouable** : l'interrompre puis le relancer reprend au jour suivant le dernier écrit.

### [B] Le module de recherche — `public/js/marvelcdb/`

JavaScript sans DOM, donc testable et réutilisable tel quel par la future UI React :

- `index.js` — `chargerHeros(heroCode)` : `fetch('/read_file?data/marvelcdb/<code>.json')`, mémorisation en mémoire pour la session.
- `filtres.js` — `filtrer(decks, {aspect, tag, texte, masquerIncomplets})` : fonction pure, tri chronologique décroissant.
- `conversion.js` — `versDeckMoteur(deckIndex, heroJsonDuJeu)` : produit le JSON attendu par `/new` (voir §6).
- `favoris.js` — lecture/écriture des favoris dans `localStorage`, clé `marvelcdb_favoris`, valeur = liste d'identifiants de decks.
- `lien.js` — `depuisLien(texte)` : extrait un identifiant d'une URL ou d'un identifiant brut collé, appelle `decklist/{id}.json` puis `deck/{id}.json` en repli, et retourne une entrée au même format que l'index.

### [C] La vue

Dans `prepare.html`, au niveau de la sélection de deck de chaque joueur : à côté du choix actuel, une entrée « Decks MarvelCDB » qui ouvre un panneau listant les decks du héros déjà sélectionné, avec les trois filtres, la case « tout montrer », l'étoile de favori, et le champ « coller un lien ».

La phase 4 refera ce panneau en React **sans toucher à [A] ni [B]** : le contrat est `chargerHeros` → `filtrer` → `versDeckMoteur`.

## 6. Conversion d'un deck MarvelCDB en deck moteur

Un deck MarvelCDB est un dictionnaire `slots` de 40 cartes qui **mélange les cartes signature du héros et la pioche du joueur**. Le moteur, lui, sépare `hero_deck` (signature) de `player_deck`.

Vérifié sur un deck réel (Wasp 63358) : `slots` = 40 cartes dont les 15 signature `13002`→`13006`, et le deck starter du jeu contient bien `hero_deck` 15 + `player_deck` 25.

Règle de conversion :

1. `hero_code` du deck → deck starter du jeu correspondant, via une table construite en lisant `deck/starter/*.json` (champ `hero[0]`, avant la virgule). Exemple : `13001a` → `wasp.json`.
2. On récupère ce deck starter par `/get_hero_json?<nom>` et on garde tel quel : `hero`, `hero_deck`, `obligations`, `nemesis_set`, `set_aside`.
3. `player_deck` = toutes les cartes de `slots`, répétées selon leur quantité, **en excluant les cartes de classe `Hero`** (elles sont déjà dans `hero_deck`). C'est exactement la règle appliquée aujourd'hui par `deck.html`, y compris son cas particulier `26002`, à reprendre à l'identique.
4. `name` = nom du deck MarvelCDB, `metadata.url` = son URL, pour que la partie garde la trace de son origine.

Contrôle de cohérence à l'import : `len(player_deck)` doit valoir `total slots - len(hero_deck)`. Un écart signale une carte signature non reconnue et fait basculer le deck en « incomplet ».

## 7. Jouabilité d'un deck

Calculée **au moment de l'indexation**, pas dans le navigateur : le script lit `data/cards.json` (base du jeu) et compare les identifiants de `slots`.

- Toutes les cartes connues → `jouable: true`.
- Sinon → `jouable: false` et `cartes_absentes: ["<id>", ...]`.

L'interface s'appuie sur ce champ, sans jamais recalculer. Quand du contenu est ajouté au jeu (nouveau pack), relancer l'indexeur avec `--recalculer` refait ce seul calcul sur l'index existant, sans réaspirer quoi que ce soit.

## 8. Format des fichiers

`data/marvelcdb/13001a.json` :

```json
{
  "hero_code": "13001a",
  "hero_name": "Wasp",
  "deck_starter": "wasp",
  "genere_le": "2026-07-28",
  "decks": [
    {
      "id": 63358,
      "nom": "Hives are Stronger Together",
      "aspect": "protection",
      "tags": ["solo"],
      "date": "2026-07-01",
      "auteur": 1234,
      "cartes": { "01088": 2, "13002": 1 },
      "jouable": true,
      "cartes_absentes": []
    }
  ]
}
```

`data/marvelcdb/_meta.json` :

```json
{
  "derniere_date": "2026-07-27",
  "genere_le": "2026-07-28",
  "total_decks": 40213,
  "jours_en_erreur": []
}
```

Taille attendue : ~1,5 ko par deck, donc de quelques dizaines de ko (héros récents) à ~3 Mo (Spider-Man, Captain Marvel). Repli prévu si un fichier dépasse 3 Mo : découpe par année (`13001a-2024.json`), le module [B] concatène.

## 9. Cas d'erreur

| Situation | Comportement |
|---|---|
| Index absent pour ce héros | Le panneau affiche « aucun deck indexé pour ce héros, lance l'indexeur » et le champ « coller un lien » reste utilisable |
| `read_file` renvoie une erreur | Message clair, la préparation reste utilisable avec les decks standard |
| MarvelCDB injoignable pendant l'indexation | Le jour est journalisé dans `jours_en_erreur` et retenté au passage suivant |
| Lien collé invalide ou deck privé non partagé | Message reprenant la distinction publication / deck privé déjà présente dans `deck.html` |
| Deck incomplet lancé volontairement | Impossible : les decks incomplets sont visibles mais non sélectionnables ; le clic affiche les cartes manquantes |
| Héros MarvelCDB inconnu du jeu | Ignoré à l'indexation, avec un compteur en fin de passage |

## 10. Tests

**Indexeur** (pytest, sans réseau) : trois journées `by_date` figées en fixtures →
regroupement par héros correct, détection des cartes absentes, second passage
incrémental qui n'écrit que les nouveaux jours, jour en erreur qui n'interrompt rien.

**Conversion** (le test qui compte) : un deck MarvelCDB figé → `versDeckMoteur` →
la charge produite doit respecter `ui-check/contrat-nouvelle-partie.json`, puis
`npm run lancement` doit atteindre le plateau avec ce deck. Le harnais de la
phase 1 fait déjà exactement ça pour un deck starter.

**Filtres** : fonctions pures, tests unitaires sur un jeu de 20 decks (aspect, tag,
texte, masquage des incomplets, tri).

**Non-régression visuelle** : `prepare.html` est un des 6 écrans sous captures de
référence. Ajouter le panneau **change forcément** la référence
`preparation-nouvelle` : passer par `npm run captures:valider`, jamais par
`--update-snapshots`.

**Vérification finale** : une vraie partie lancée avec un deck MarvelCDB importé,
menée jusqu'au plateau, plus un passage du bot d'autoplay sans traceback.

## 11. Ce qui reste à trancher au démarrage du chantier

1. **Le moment.** Recommandation : écrire [A] et [B] dès maintenant (ils ne dépendent d'aucune décision de la refonte) et poser [C] en version minimale dans `prepare.html`, quitte à ce que la phase 4 la refasse. L'alternative, tout attendre la phase 4, retarde l'usage sans rien économiser sur le socle.
2. **Le déclenchement de l'indexeur.** À la main pour commencer ; le brancher sur `launcher_fast.py` (rafraîchissement silencieux en arrière-plan au démarrage) est une amélioration ultérieure, à ne faire que si le passage incrémental reste court.
3. **Le dossier `data/`** est un lien symbolique dans `.game/` : vérifier que l'écriture de `data/marvelcdb/` par le script se fait bien dans les sources et non dans le dossier compilé.

## 12. Estimation

| Morceau | Charge |
|---|---|
| [A] Indexeur + tests | 1 séance |
| [B] Module de recherche + conversion + tests | 1 séance |
| [C] Panneau dans `prepare.html` + captures | 1 séance |
| Premier passage d'indexation | ~15 min de machine, sans surveillance |

## 13. Hors périmètre, volontairement

- Choix du deck par chaque joueur depuis son siège (demanderait un salon d'attente partagé, que le moteur n'a pas : chantier à part entière, à traiter avec le serveur permanent).
- Classement par popularité (aucune donnée dans l'API).
- Édition d'un deck importé (`deck.html` existe pour ça).
- Publication de decks vers MarvelCDB.
