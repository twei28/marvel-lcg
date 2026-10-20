---

## 2. Ce qu'est une campagne dans ce jeu, de bout en bout

### 2.1 En deux phrases

Une campagne enchaîne les scénarios d'une boîte dans l'ordre du livret. Ce que les joueurs gagnent ou perdent
dans un scénario est enregistré dans un **carnet de campagne**, qui est relu automatiquement à la mise en place
du scénario suivant.

Le carnet est un **dictionnaire clé texte → valeur texte** (`{"Campaign Pool: Cosmo": "1", "Player 1 Role":
"Brawler"}`). C'est le **seul** lien entre deux parties : le moteur n'a aucune mémoire d'une partie à l'autre.

### 2.2 Les trois couches, et qui écrit quoi

| Couche | Où elle vit | Ce qu'elle fait | Qui la produit |
|---|---|---|---|
| **Données** | `data/cards.json`, `data/scenarios/`, `data/encounter_sets/`, `data/sets_info.json` | Les cartes, la composition de chaque scénario | **Toi** |
| **Moteur (Python)** | `src/cards/pack/<pack>/` (scripts de cartes + `campaign.py`) | Les capacités des cartes ; à la mise en place, applique le carnet ; à la fin de partie, relève le carnet sortant | **Toi** (sauf si le moteur lui-même doit changer : alors `BESOINS-MOTEUR.md`) |
| **Description de campagne (JSON)** | `data/campagnes/<code>.json` | L'ordre des scénarios, les champs du carnet à reporter, les textes de l'écran, les pages du livret | **Toi** |
| **Écran des campagnes (JS)** | `public/campagne.html`, `public/js/campagne/*.js` | Création, liste, scénario courant, lancement | **Claude** (générique : il lit ta description) |
| **Panneau de récompenses (React)** | `ui-app/src/board/campagne/*` | S'ouvre à la fin de partie, pré-remplit le carnet, le fait valider | **Claude** (générique) |
| **Serveur** | `src/engine/device/web/server/server_campagne.py` | Les routes qui lisent les descriptions et écrivent les campagnes du joueur | **Claude** (générique) |

Le point à retenir : **ajouter une campagne qui n'a que des mécaniques déjà connues est un travail de contenu,
pas de code d'interface.** Les écrans lisent ta description et s'adaptent. Seules les mécaniques inédites
(un écran de plus, un type de champ de carnet nouveau) demandent à Claude d'étendre l'interface : tu les
signales dans `BESOINS-MOTEUR.md`.

### 2.3 Le cycle de vie d'une campagne, étape par étape

```
 (1) /campagne.html
     le joueur choisit une BOÎTE (liste lue sur /list_campagnes_definies = data/campagnes/*.json),
     un nom, la difficulté (standard | expert) et le nombre de héros (1 à 4)
          │
 (2)      ▼  /prepare.html?campagne   (l'écran de préparation, réduit à deux étapes : Équipe, Decks)
     le joueur choisit ses héros et leurs decks ; leur identité est FIGÉE pour toute la campagne
          │
 (3)      ▼  POST /save_campagne
     la campagne du joueur est écrite : Fusion/marvel-lcg-src/campagnes/<id>.json
     { code, nom, difficulte, equipe[], termines: [], carnet: {}, tentatives: {}, partieEnCours: null }
          │
 (4)      ▼  « Lancer le scénario »    (public/js/campagne/app.js : lancerScenario)
     - écrit partieEnCours = { scenario, depuis } et tentatives[scenario] += 1
     - dépose la clé navigateur « mc-campagne-partie » = { id, scenario }
     - lance la partie avec le descripteur :
         rules             = ["mode_campaign", "v16_all", "v18_all", ...]
         campaign_json     = le fichier data/scenarios/<id>.json (ou <id>_expert.json en campagne experte)
         encounter_set_names = sets du scénario + sets modulaires DU FICHIER DE SCÉNARIO (jamais un choix du joueur)
         hero_json         = les decks de l'équipe, dans l'ordre des sièges
         campaign_log      = le CARNET de la campagne        ◄── c'est ici que le carnet entre dans le moteur
          │
 (5)      ▼  le moteur monte la partie (World.GameSetup, 16 étapes, voir §7.2)
     étape 13 « Campaign Setup » : Message.WhenCampaignSetup est émis. Les capacités de type Campaign,
     posées sur la face 1A du complot principal par CampaignSetup(niveau), relisent le carnet et en
     appliquent les conséquences (carte mise en jeu, mélangée, retirée, dégâts, etc.).
          │
 (6)      ▼  les joueurs jouent le scénario
          │
 (7)      ▼  fin de partie : Message.WhenGameOver
     la capacité WriteCampaignLogAtGameOver (posée par CampaignSetup) calcule ce que la partie a produit
     et l'écrit dans  .game/campaign_log_last.json  { players_won, scenario, suggestions: {...} }
          │
 (8)      ▼  le plateau ouvre le PANNEAU DE RÉCOMPENSES (ui-app/src/board/campagne/PanneauRecompenses.tsx)
     il pré-remplit chaque champ déclaré dans data/campagnes/<code>.json, dans cet ordre de priorité :
        1. ce que le moteur a relevé (/get_carnet_suggere)  — seulement si son estampille = ce scénario
        2. ce que les « détecteurs » déduisent de l'état du monde (detecteurs.ts)
        3. la valeur déjà présente au carnet
     le joueur corrige, choisit les vrais choix du livret, et valide
          │
 (9)      ▼  POST /save_campagne
     carnet = ancien carnet + champs validés ; termines += [scénario] ; historique[scénario] = champs ;
     partieEnCours = null  ;  perdue = true si la règle de défaite le dit
          │
(10)      ▼  retour à /campagne.html : le scénario suivant est proposé. Retour à l'étape (4).
```

Règles importantes de ce cycle :

* **Une défaite n'écrit rien** : le scénario se rejoue sans pénalité. Exceptions déclarées *dans la description
  de campagne* : `defaite_continue` (la défaite a ses propres gains, la campagne passe au suivant), `defaite`
  (perdre le scénario final perd la campagne), `reprise` (il faut re-préparer quelque chose avant de rejouer).
* **Les sets modulaires viennent du fichier de scénario**, jamais d'un choix du joueur.
* **Entre deux scénarios, le joueur peut modifier le contenu de ses decks** (pas l'identité). Ce que le carnet
  *impose* dans un deck (une carte de récompense) doit y rester : `"deck": "requis"` dans la description.
* **Plusieurs joueurs** : chaque champ `parJoueur` appartient au siège qu'il nomme ; tout le reste appartient à
  l'hôte, seul à pouvoir valider. Les clés par joueur s'écrivent `Player N <clé>` (N de 1 à 4).
* **Mode expert** : un seul choix à la création, valable pour tous les scénarios. En expert, le moteur lit
  `data/scenarios/<id>_expert.json` ; les PV restants se reportent (`victoire_commune_expert`) ; la règle de
  défaite finale s'applique selon `expert_seulement`.

### 2.4 Les fichiers qui décrivent une campagne et leurs liens (carte des références)

```
data/sets_info.json
  "N. Custom (Nom)": { name: <pack>, scenarios: [<id scénario>...], heroes: [...], encounters: [<id set>...], max_id }
        │                                   │                                     │
        │ cle_extension (même texte)        ▼                                     ▼
        ▼                         data/scenarios/<id>.json            data/encounter_sets/<id set>.json
data/campagnes/<code>.json            villain / schemes / set_aside /        encounters: [card_id...]
  scenarios[].id  ───────────────►    encounters / encounter_sets /
  champs[].cle ───► (lus par) ───►    modular_sets  (tous des card_id ou ids de sets)
        │                                   │
        ▼                                   ▼
src/cards/pack/<pack>/campaign.py     data/cards.json  ◄── pack "<pack>": [ {card_id, type, name, ... set_name} ]
  CampaignSetup(niveau)                     │ set_name  ──(nettoyé)──►  src/cards/pack/<pack>/<set_nettoyé>/<card_id>.py
  CollectXXX(niveau)                        │ card_id   ──────────────►  assets/pics/<card_id>.jpg
        ▲                                   │ card_id   ──────────────►  ui-app/src/board/textes-fr-fanmade.ts
        │ appelé par                        ▼
src/cards/pack/<pack>/<scénario>/<id 1A>.py   (la face 1A du complot principal appelle *CampaignSetup(niveau))
```

Trois conséquences pratiques :

1. **Le nom de la clé du carnet est le contrat.** Il apparaît à trois endroits qui doivent être **strictement
   identiques** : dans `campaign.py` (écriture et lecture), dans la description de campagne (`champ.cle`) et,
   le cas échéant, dans un script de carte. Une clé mal orthographiée **ne lève aucune erreur** : le moteur lit
   une valeur vide et la récompense disparaît en silence. `verifier_campagnes.py` (§11) compare ces trois endroits.
2. **Le `set_name` d'une carte décide du dossier de son script.** Un script rangé au mauvais endroit est muet.
3. **L'identifiant d'une carte est une clé partout** : image, texte français, script, scénario, carnet. On ne le
   change jamais une fois livré.
