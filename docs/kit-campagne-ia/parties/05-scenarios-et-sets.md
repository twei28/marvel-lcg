---

## 5. Les scénarios, les sets de rencontre et l'index des packs

### 5.1 Un scénario : `data/scenarios/<id>.json` et `<id>_expert.json`

`<id>` est en minuscules et soulignés. Pour un contenu fan-made, il porte le **préfixe de la campagne** :
`wd_shocker`, `hs_vermin`, `sk_super_skrull`. Les scénarios officiels n'en ont pas (`ebony_maw`, `rhino`).
**Le fichier `<id>_expert.json` est lu automatiquement** quand la campagne est experte et que ce fichier existe.

Les neuf clés sont **toutes obligatoires**, même vides :

| Clé | Sens |
|---|---|
| `version` | Toujours `"0.5.8"`. |
| `name` | Le nom **affiché** du scénario (`"Rhino"`, `"The Lizard"`). |
| `villain` | La liste des cartes de vilain **dans l'ordre des stades**. Standard : stades 1 et 2 (`["01094", "01095"]`). Expert : stades 2 et 3 (`["01095", "01096"]`). Un vilain recto-verso s'écrit en **une chaîne** `"wd054a,wd054b"` ; en expert on **inverse** parfois l'ordre des faces (`"wd001b,wd001a"`). **`[]` pour un scénario à plusieurs vilains** (voir ci-dessous). |
| `expert` | `false` dans le fichier standard, `true` dans le fichier `_expert`. |
| `schemes` | Les complots principaux, **un par stade**, chacun une chaîne `"face A,face B"` : `["wd002a,wd002b", "wd003a,wd003b", "wd004a,wd004b"]`. **Le premier est mis en jeu au départ**, les suivants attendent l'avancée. |
| `set_aside` | Cartes **mises de côté** au départ (créées dans la zone « de côté »). Le scénario (le plus souvent le `Setup` du complot principal) les sortira par un effet. `[]` sinon. |
| `encounters` | Cartes de rencontre **propres au scénario**, **une entrée par exemplaire**. Le cœur du scénario peut vivre ici (modèle officiel) **ou** dans un set à part listé dans `encounter_sets` (modèle fan-made, `encounters: []`). Choisis l'un des deux, pas les deux. |
| `encounter_sets` | Les sets de rencontre **ajoutés** (noms de fichiers de `data/encounter_sets/`, sans extension). Tous **obligatoires** : `"standard"` (ou `"standard_iii"`), et `"expert"` dans le fichier expert. |
| `modular_sets` | Les sets **modulaires** recommandés. **En campagne, ils sont imposés** : l'écran envoie exactement ceux du fichier. |

Une clé facultative existe dans les fichiers de **défis** (`data/challenges/`) : `challenges: ["2401_..."]`
(cartes Défi). Elle n'est pas utile à une campagne.

Le moteur lit ce fichier avec `CampaignDescriptor` (`game/scene/replay/campaign.py`) : `version, name, villain,
expert, challenges, schemes, set_aside, encounters, encounter_sets, modular_sets, campaign_log`. `campaign_log`
n'est **pas** dans le fichier : il est fusionné au lancement depuis le carnet de la campagne.

**Exemples réels : un scénario officiel de campagne, standard puis expert**
{{FICHIER:Fusion/marvel-lcg-src/data/scenarios/ebony_maw.json}}
{{FICHIER:Fusion/marvel-lcg-src/data/scenarios/ebony_maw_expert.json}}

**Exemples réels : un scénario fan-made de campagne (le cœur vit dans des sets, `encounters` est vide)**
{{FICHIER:Fusion/marvel-lcg-src/data/scenarios/wd_shocker.json}}
{{FICHIER:Fusion/marvel-lcg-src/data/scenarios/wd_shocker_expert.json}}

**Un vilain recto-verso et des modulaires (The Lizard)**
{{FICHIER:Fusion/marvel-lcg-src/data/scenarios/wd_the_lizard.json}}

**Un scénario fan-made à cartes en vrac (`encounters` rempli, un seul set partagé, un modulaire) : Hunting Season**
{{FICHIER:Fusion/marvel-lcg-src/data/scenarios/hs_vermin.json}}

**Scénario à PLUSIEURS vilains (Sinister Six) : `villain` est vide, les vilains sont dans `set_aside`**
{{FICHIER:Fusion/marvel-lcg-src/data/scenarios/sinister_six.json}}

Pour un scénario à plusieurs vilains, c'est le `Setup` du complot principal qui les met en jeu, après avoir posé
`message.skip_put_villain_into_play = True` (voir les recettes de l'annexe B, « scénario à plusieurs vilains »).
Un vilain à **deux faces** (ALERT / K.O.) est une carte `"idA,idB"` du `set_aside`.

**Règle d'or : les stades.** Le `villain` standard liste les stades **1 et 2** ; l'expert les stades **2 et 3**.
Le complot principal est **le plus souvent le même** dans les deux fichiers (les mêmes `schemes`) : vérifie sur le livret. C'est le **set**
`expert` (ajouté à `encounter_sets`) qui apporte les cartes expert. Pour un vilain en trois stades, vérifie
sur le livret quels stades sont proposés en standard et en expert.

### 5.2 Un set de rencontre : `data/encounter_sets/<set>.json`

Le nom du fichier (sans `.json`) est **l'identifiant du set** : c'est lui qui apparaît dans `encounter_sets`
et `modular_sets` des scénarios et dans `sets_info.json`. Une entrée par exemplaire :

```json
{
    "version": "0.5.8",
    "name": "Feral Instincts",
    "encounters": ["hs141", "hs142", "hs143", "hs144", "hs145"]
}
```

* **`name`** est **le titre affiché au joueur** (écran de mise en place). Écris-le en casse normale
  (`"Feral Instincts"`). Un fichier existant (`shocker.json`) a hérité d'un `name` en minuscules : n'imite pas
  ce défaut.
* **`encounters`** : les `card_id`, **un par exemplaire**. Une carte en deux exemplaires apparaît deux fois.
* **Facultatif — `random_pick`** : ne garder qu'une **partie** des cartes, tirées au hasard à la formation du
  deck de rencontre : `[{"from": ["id1","id2","id3"], "count": 1}, ...]`. Les cartes d'aucun groupe sont toujours
  gardées ; l'ordre du set est conservé (module `game/card/factory.py`, `RandomPick`).

Les sets communs `standard` et `expert` (core) se réutilisent tels quels :
{{FICHIER:Fusion/marvel-lcg-src/data/encounter_sets/standard.json}}
{{FICHIER:Fusion/marvel-lcg-src/data/encounter_sets/expert.json}}

**Un set de scénario fan-made, un modulaire officiel, un modulaire fan-made :**
{{FICHIER:Fusion/marvel-lcg-src/data/encounter_sets/shocker.json}}
{{FICHIER:Fusion/marvel-lcg-src/data/encounter_sets/black_order.json}}
{{FICHIER:Fusion/marvel-lcg-src/data/encounter_sets/crime_wave.json}}

**Un set avec `random_pick`** (Galactic Storm, Imperial Guard) :
{{FICHIER:Fusion/marvel-lcg-src/data/encounter_sets/gs_imperial_guard.json}}

⚠ **Chaque set nommé dans `encounter_sets` ou `modular_sets` d'un scénario doit avoir son fichier.** Un set sans
fichier se charge **vide, sans erreur** (`LoadEncounterSet` rend `[]`) : le scénario se monte avec un deck de
rencontre incomplet et rien ne le dit. L'écran de campagne lit aussi chaque fichier pour en afficher le `name` dans
« Mise en place » (à défaut, il affiche un titre déduit de l'identifiant).

### 5.3 Le set némésis d'un héros (si la campagne apporte un héros)

`data/nemesis/<héros>_nemesis.json`, même forme qu'un set de rencontre (`name` : `"Adam Warlock Nemesis"`).
**Facultatif** : le set némésis réellement joué vient du **deck de départ** du héros (`nemesis_set`). Le fichier
sert seulement à charger ce set comme un set nommé.

### 5.4 L'index des packs : `data/sets_info.json`

Chaque pack déclare ses scénarios (les **identifiants de fichier** de scénario), ses héros, ses sets de
rencontre modulaires et son plus grand identifiant. La **clé** est de la forme `N. Nom`, où `N` est un numéro
d'ordre de parution :

* officiel : `"21. The Mad Titan's Shadow"`
* fan-made : `"120. Custom (Web of Deceit)"`, `"143. Custom (Skrull Menace)"`, `"178. Custom (Hunting Season)"`.

**Le numéro est attribué par Claude** (il doit être unique : le vérificateur `verifier_prefixes.py` refuse un
doublon, et il sert de rang de tri). Donne seulement le **nom**.

**Cette clé est celle de `cle_extension` dans `data/campagnes/<code>.json`**, et le nom du fichier de l'image
de boîte : `assets/textures/sets/<clé>.webp`. Les trois doivent être **strictement identiques**, au caractère
près (apostrophes comprises).

Champs d'une entrée : `name` (clé du pack), `scenarios`, `heroes`, `encounters`, `max_id` ; facultatifs :
`underlings`/`manigances` (campagne en ordre libre), `indisponible: true` (extension mise de côté : l'interface
ne la montre plus, les tests continuent).

**Entrée d'une campagne officielle, puis d'une campagne fan-made :**
{{SETSINFO:21. The Mad Titan's Shadow}}
{{SETSINFO:120. Custom (Web of Deceit)}}
{{SETSINFO:143. Custom (Skrull Menace)}}

* `scenarios` : les `id` des scénarios **sans** `_expert`, dans l'ordre de la campagne.
* `encounters` : **tous** les sets de rencontre **modulaires** du pack (ceux qu'un joueur peut combiner à
  d'autres scénarios), **pas** les sets propres à un scénario s'ils ne sont pas jouables seuls.
* `max_id` : le **plus grand `card_id`** du pack (`"wd165"`, `"sk289b"`).

### 5.5 Deck de départ d'un héros (seulement si la campagne apporte des héros)

`deck/starter/<héros>.json` — c'est ce fichier qui fait **apparaître** le héros dans le jeu (le catalogue lit
`deck/starter/*.json`). Pour un héros fan-made, **`player_deck` reste vide** sauf si l'auteur fournit une
decklist imprimée (décision du projet : on n'invente pas les cartes d'aspect). Voir `PROCESSUS-HEROS.md`
(annexe D) pour tout ce qu'un héros demande.

```json
{
    "version": "0.5.8",
    "name": "Spider-Man",
    "metadata": { "url": "" },
    "hero": ["01001a,01001b"],
    "hero_deck": ["01002", "01003", "01003", "..."],
    "set_aside": [],
    "obligations": ["01165"],
    "nemesis_set": ["01166", "01167", "01168", "01168", "01169"],
    "player_deck": ["01058", "01059", "..."]
}
```

⚠ **Le moteur ne valide PAS les decks de départ.** Une carte de classe `Hero` (signature) ne doit jamais se
trouver dans le deck d'un autre héros.

### 5.6 La mise en place : ce que le moteur fait des champs du scénario

Dans l'ordre (`World.Initialize`, `game/world/world.py`) : choix des identités ; **8.** le scénario est choisi :
`schemes` → le premier complot est mis en jeu, les autres attendent (`main_schemes_deck`), `villain` → deck de
vilain ; message `WhenGameBeginSetup` ; **9.** le vilain est mis en jeu et ses PV posés ; **10.** le deck de
rencontre est formé : `encounters` + chaque set de `encounter_sets` (via `LoadEncounterSet`), les obligations des
héros posées dessus, mélange ; `set_aside` → zone « de côté » ; **11.** cartes `Setup` mises en jeu ; **12.**
`When Revealed`/`Setup` du complot et du vilain ; **13. Campaign Setup** (§7.2) ; 14. pioche ; 15. mulligans ;
15 bis. `WhenCampaignSetupAfterMulligans` ; 16. capacités de `Setup` des personnages.

### 5.7 Checklist de relecture d'un scénario

- [ ] Les 9 clés sont toutes présentes, `version: "0.5.8"`.
- [ ] Chaque `card_id` cité existe dans ta livraison **ou** dans `reference/ids-existants.json`.
- [ ] Chaque set de `encounter_sets` et de `modular_sets` existe (ton fragment ou `reference/sets-existants.json`).
- [ ] `schemes` : une chaîne `"a,b"` par stade ; `villain` : stades corrects pour standard et expert.
- [ ] Le fichier `_expert.json` existe et **diffère** du standard (stades, `expert`, set `expert`).
- [ ] L'entrée `sets_info.json` liste ce scénario (id **sans** `_expert`).
- [ ] Le scénario est joué en **solo ET à 2 joueurs** (les valeurs « par joueur » ne se voient qu'en multi).
