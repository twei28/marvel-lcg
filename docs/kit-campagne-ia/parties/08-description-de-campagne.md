---

## 8. La description de la campagne : `data/campagnes/<code>.json`

C'est le fichier que **lisent l'écran des campagnes et le panneau de récompenses**. Il ne contient **aucune
logique** : il *déclare* (l'ordre des scénarios, les textes, les champs du carnet à reporter, les pages du
livret). La logique est dans `campaign.py` (§7). Le fichier est servi par `/get_campagne_definition?<code>` ;
`<code>` doit être **le nom du fichier sans `.json`**, **le `code` du fichier**, et **le dossier
`public/stories/<code>/`**.

### 8.1 Un exemple complet : The Mad Titan's Shadow (officielle)

Chaque scénario porte ses récompenses (`victoire`), ses pages de livret (`pages`), un résumé et un enjeu en
français. Les champs `auto` (relevés par le collecteur de `mts/campaign.py`) ne portent **ni `detection` ni
`options`** : les valeurs viennent du moteur.

{{FICHIER:Fusion/marvel-lcg-src/data/campagnes/mts.json}}

### 8.2 Un exemple complet : Web of Deceit (maison, sans collecteur, avec des choix)

Ici les gains sont des **choix du joueur** (`type: "choix"`, `obligatoire: true`) parmi des cartes (`options`) :

{{FICHIER:Fusion/marvel-lcg-src/data/campagnes/web_of_deceit.json}}

### 8.3 Toutes les clés, une par une

#### 8.3.1 Clés de premier niveau

| Clé | Type | Obligatoire | Sens |
|---|---|---|---|
| `version` | texte | oui | `"1.0"` |
| `code` | texte | oui | Le code de la campagne = nom du fichier = nom du pack le plus souvent = dossier `public/stories/<code>/`. |
| `cle_extension` | texte | oui | **La clé de `data/sets_info.json`** (`"21. The Mad Titan's Shadow"`), **au caractère près**. Le numéro devant donne l'ordre de parution. Fan-made : laisse `"A_FAIRE_CLAUDE"` (Claude attribue le numéro). |
| `nom`, `nom_en` | texte | oui | Le nom en français et en anglais. |
| `resume`, `resume_en` | texte | oui | Deux phrases pour présenter la boîte, en français puis en anglais. |
| `expert` | objet | oui | `{ "pv_persistants": true }` si, en campagne experte, les PV se reportent. `{ "note": "…" }` : texte affiché en mode expert (ordre libre). **Cette clé est informative** : le report réel des PV se fait par `victoire_commune_expert` + `ExpertCampaignSetPlayersHPToTheirRemainingHP` (§7.4). |
| `scenarios` | liste | oui | Un objet par scénario, **dans l'ordre** (§8.3.2). |
| `victoire_commune` | liste de champs | non | Champs présentés à **chaque** victoire **sauf** le scénario final (§8.3.3). |
| `victoire_commune_expert` | liste de champs | oui (peut être `[]`) | Idem, **en campagne experte seulement**. C'est là que vivent les PV restants. |
| `pages_regles` | liste de noms de fichier | oui (peut être `[]`) | Planches de règles **de la campagne** (`00-campagne-regles-1.jpg`). Tu laisses `[]` si tu n'as pas les pages ; Claude les ajoute. |
| `pages_expert` | liste | non | Planches de règles de la campagne **experte** (affichées seulement en expert). |
| `pages_intro` | liste | non | Planche(s) d'ouverture, affichée(s) **au début de la campagne** (avant le scénario 1). |
| `livret_fr` | booléen | non | `true` si `public/stories/<code>/fr/` contient les pages refaites en français ; sinon l'écran ne cherche pas. |
| `options_campagne` | liste | non | Réglages faits **au début** de la campagne (§8.5.1). |
| `marche` | objet | non | Un marché de cartes à acheter entre deux scénarios (§8.5.2). |
| `cooperation` | objet | non | La zone de coopération de Skrull Menace (§8.5.3). |
| `enquete` | objet | non | L'enquête d'Agents of S.H.I.E.L.D. (§8.5.4). |
| `bilan` | objet | non | Un score final noté **à la fin** (§8.5.5). |
| `ordre_libre`, `vilains`, `pages_vilains` | booléen, liste, liste | non | Campagne **en ordre libre** (Fear No Evil, §8.5.6). |

#### 8.3.2 Un scénario (`scenarios[]`)

| Clé | Obligatoire | Sens |
|---|---|---|
| `id` | oui | L'identifiant du scénario. **Doit être dans `sets_info.json` › `scenarios` ET être un fichier `data/scenarios/<id>.json`.** C'est aussi l'**estampille** que le moteur pose au carnet sortant (§7.5) et le dernier mot du dossier de pages. |
| `catalogue` | non | Si le fichier de scénario lancé **n'est pas** `<id>.json` : l'id du fichier réellement lancé (`"kingpin_fne"`). Sinon omis. |
| `numero` | oui | 1, 2, 3… **C'est le `niveau` de `CampaignSetup(niveau)`** (§7.3). |
| `nom`, `nom_fr` | oui | Nom anglais, nom français (le français sert dans l'interface en français). |
| `resume` | oui | Ce qui se passe, **deux phrases, écrites pour un joueur**, en français. Pas de recopie du livret : un récit. |
| `enjeu` | oui | Ce que ce scénario change pour la suite, **une phrase**. « Rien à reporter : c'est le dernier scénario. » pour le dernier. |
| `final` | sur le dernier | `true` sur le dernier scénario : le panneau dit « La campagne est gagnée ! » et les champs communs sautent. |
| `defaite` | non | **Ce qui perd la campagne** (scénario final seulement) : `{"quand": "partie_perdue" \| "cle_absente", "cle": "<clé>", "expert_seulement": true, "texte": "…"}`. `partie_perdue` : perdre ce scénario perd la campagne. `cle_absente` : la campagne est perdue si `cle` manque au carnet (AoA : `Professor Saved`). `expert_seulement` : la règle ne vaut qu'en expert (**vrai partout sauf AoA**). `texte` : ce que le livret raconte. |
| `reprise` | non | **Faut-il re-préparer avant de rejouer ?** (AOS seulement) : `{"quand": "partie_perdue", "standard_seulement": true, "titre", "texte", "cle_compte", "cle_preuves"}`. |
| `defaite_continue` | non | `true` : **une défaite ne fait PAS rejouer** ce scénario (ignoré sur un scénario `final`) : elle a ses propres gains, le panneau s'ouvre aussi à la défaite et la campagne passe au suivant (Hunting Season). |
| `pages` | oui | `{ "intro": [...], "regles": [...], "epilogue": [...] }` : noms de fichiers du dossier `public/stories/<code>/`. **Tu laisses `{}`** si tu n'as pas les pages ; Claude les ajoute. Une planche qui termine un scénario ET ouvre le suivant n'est pas dupliquée. |
| `victoire` | oui (peut être `[]`) | Les **champs du carnet** notés après ce scénario (§8.3.3). |
| `manigance`, `environnement` | ordre libre | `manigance: true` = scénario interchangeable ; `environnement: "60205a,60205b"` = la carte qui entre en jeu selon l'issue. |

**Exemple d'un scénario avec défaite de campagne :**
{{SCENARIOJSON:mts|loki|pages}}

**Exemple d'un scénario avec reprise après défaite (Agents of S.H.I.E.L.D., scénario 5) :**
{{SCENARIOJSON:aos|baron_zemo|victoire,pages}}

**Exemple d'un scénario qui continue la campagne même perdu (Hunting Season) :**
{{SCENARIOJSON:hunting_season|hs_vermin|victoire,pages}}

**Exemple d'un scénario avec une défaite par clé absente (Age of Apocalypse, scénario 5) :**
{{SCENARIOJSON:aoa|en_sabah_nur|victoire,pages}}

#### 8.3.3 Un champ de victoire (élément de `victoire`, `victoire_commune`, `victoire_commune_expert`)

| Clé | Obligatoire | Sens |
|---|---|---|
| `cle` | oui | **La clé du carnet**, copiée **telle quelle** de `campaign.py` (§7.9). Pour un champ `parJoueur`, c'est la clé **sans** le préfixe `Player N`. |
| `type` | oui | **`"auto"`** : valeur **relevée par le jeu** (collecteur, détecteur ou carnet existant), affichée comme un constat, corrigeable. **`"choix"`** : **décision du joueur** (le livret dit « each player chooses ») ; jamais pré-remplie par le moteur. |
| `format` | non | `"int"` (un nombre : champ numérique) ; `"liste"` (des `card_id` joints par `;`) ; `"liste-joueurs"` (des indices de joueurs). Absent = texte libre (rôle, état). |
| `parJoueur` | non | `true` : une valeur **par héros**, stockée sous `Player N <cle>` ; chaque joueur ne saisit que **sa** case. |
| `obligatoire` | non | `choix` seulement : `true` bloque le bouton « Valider » tant qu'une case manque. |
| `libelle` | oui | Intitulé court affiché (français). |
| `aide` | oui | **Une phrase** : à quoi sert cette clé plus tard (français). |
| `options` | non | Les `card_id` proposés : **choix** → un seul (cartes cliquables) ; **auto + liste** → plusieurs (cases à cocher) ; avec `detection`, les `options` sont **les cartes que le détecteur cherche**. |
| `detection` | non | Un détecteur (§8.4). **Facultatif pour une boîte à collecteur**, **nécessaire** pour une boîte sans collecteur. |
| `parametres` | non | Paramètres du détecteur (`{"compteur": "delay"}`, `{"complot": "04122", "type": "Ally"}`). |
| `condition` | non | Le champ n'est **présenté** que si la condition est vraie. Une seule : `"complot_absent"` + `parametres.complot` (le complot **annexe** n'est plus dans `area_schemes_side`). **Une condition inconnue MASQUE le champ** : on n'accorde pas une récompense dont on ne sait pas évaluer la règle. |
| `cumulatif` | non | `true` + `format: "int"` : le carnet **cumule** ce champ d'un scénario à l'autre. Vrai pour une valeur **issue d'un détecteur** (elle est ce que la partie **ajoute**, le panneau additionne) ; une valeur relevée par le **collecteur du moteur** est déjà cumulée et n'est **pas** additionnée une seconde fois. |
| `tirage` | non | `{"cle_piste": "<clé>", "paliers": [1, 13, 21]}` : le champ se **tire au sort** à chaque palier atteint par la piste `cle_piste`. Exige `type: "auto"`, `options` non vide, `paliers` croissants d'entiers positifs, et que `cle_piste` soit déclarée **avant** ce champ. Cumulatif et irréversible. |
| `deck` | non | `"requis"` : **l'écran** refuse, au retour de « Modifier les decks », un deck qui ne contient plus la carte notée. Le drapeau ne fait que cela : **la recherche dans le deck est faite par ton script** à la mise en place suivante (modèle : `sm/campaign.py`). Exige `parJoueur`. |
| `cases` | non | Un tableau de cases à cocher : `[{"titre": "Antalya", "exigences": ["Nemesis minion", "…"]}]` ; le carnet garde `« Titre: exigence »` pour chaque case cochée (Skrull Menace). |

**Exemples réels, un par comportement :**

*Drapeau relevé par le moteur (aucune `detection`)* :
{{CHAMP:mts|Campaign Pool: Cosmo}}

*Un nombre par joueur détecté dans l'état du monde (PV restants, en expert)* :
{{CHAMP:mts|Remaining hit points}}

*Un choix de carte par joueur, obligatoire* :
{{CHAMP:trors|Tech Upgrade}}

*Une liste par joueur détectée parmi des options* :
{{CHAMP:trors|Rescued Allies}}

*Des cartes entrées en jeu, parmi des options* :
{{CHAMP:trors|Experimental Weapons added to encounter deck}}

*Un compteur lu sur la manigance principale* :
{{CHAMP:trors|Number of delay counters on main scheme}}

*Les joueurs encore engagés* :
{{CHAMP:trors|Players engaged with minions}}

*Des cartes posées sous un complot encore en jeu* :
{{CHAMP:trors|Allies removed from the campaign}}

*Un choix soumis à une condition (le complot est tombé)* :
{{CHAMP:trors|Basic Upgrade}}

*Un total cumulatif, détecté par six conditions de la partie* :
{{CHAMP:sm|Reputation Track}}

*Un tirage au sort aux paliers d'une piste* :
{{CHAMP:sm|Osborn Tech: Reputation Track Penalty}}

*Un choix qui exige que la carte reste dans le deck* :
{{CHAMP:sm|Planning Ahead: Reputation Track Reward}}

### 8.4 Les détecteurs disponibles (`ui-app/src/board/campagne/detecteurs.ts`)

Un **détecteur** lit l'état du monde (le descripteur de fin de partie) et rend la valeur **dans la forme exacte du
carnet** (`"id1;id2"`, `"3"`). **Tous sont génériques** : aucun n'a de boîte en dur. Une `detection` **inconnue
ne lève rien** : le champ reste vide et la récompense disparaît en silence — `verifier_campagnes.py` refuse un nom
inexistant. **N'invente pas de détecteur** : s'il en manque un, `A_FAIRE_CLAUDE` dans `BESOINS-MOTEUR.md`.

| `detection` | Rend | Paramètres | Source de vérité |
|---|---|---|---|
| `cartes_en_jeu` | parmi `options`, celles **entrées en jeu** pendant la partie (hors decks, zones mises de côté et decks additionnels) | — | Armes expérimentales de Crossbones |
| `compteur_manigance` | la valeur d'un compteur sur la manigance principale (le **maximum** si plusieurs) | `compteur` (`"delay"`) | Pions retard de Zola |
| `cartes_du_joueur` | parmi `options`, celles que **ce joueur possède** désormais (où qu'elles soient) | — | Alliés secourus de Taskmaster |
| `joueurs_engages` | les **indices** (`"0"`, `"1"`) des joueurs encore engagés avec au moins un ennemi | — | Joueurs engagés de Zola |
| `cartes_sous_complot` | les cartes **posées sous** un complot **annexe** encore en jeu (le code ne cherche que dans `area_schemes_side`, jamais sous une manigance principale ; même zone, `bind_object_id` = id du complot ; `parametres.type` est comparé au `card_type`) | `complot` (card_id), `type` | Prison d'Hydra |
| `pv_restants` | les PV de l'identité, **plafonnés** aux PV imprimés ; rien pour un héros éliminé | — | Livret p.17 |
| `cartes_en_pile_victoire` | parmi `options`, celles dans la **pile de victoire** | — | Community Service de sm |
| `cartes_dans_zone` | parmi `options`, celles présentes dans une **zone nommée** du descripteur de monde (clé du monde : `area_villain`, `area_schemes_main`, `area_schemes_side`, `area_environment`, `area_set_aside`… ; sm utilise `area_villain`) | `zone` | Vilains encore en jeu de sm |
| `compter_trait` | le **nombre** de cartes portant un trait dans les decks, mains et défausses des joueurs | `trait` (`"ILLUSION"`) | Cartes ILLUSION de sm |
| `conditions_reputation` | le total des **six conditions** de la piste de réputation de sm | — | sm p.22 |

Faits mesurés sur les descripteurs réels, à ne pas re-deviner : les **compteurs** sortent en `info.c_<nom>`
(`c_delay`), les **jetons** en `info.k_<nom>` (`k_threat`, `k_acceleration_token`) ; les **traits** en
`traits.t_<NOM>` ; une carte posée sous un complot est dans **la même zone** que lui, avec `bind_object_id` égal à
l'`id` du complot ; les PV de l'identité sont `info.health` / `info.max_health` sur `players[i].area_hero[0]` ;
le deck des Armes Expérimentales est un **deck additionnel** (`additional_decks`).

### 8.5 Les blocs spéciaux (mécaniques déjà gérées par l'écran)

Ces blocs existent parce qu'une boîte les a exigés. **Si ta campagne a la même mécanique, déclare le bloc comme
dans le modèle ; sinon ne les utilise pas** ; une mécanique inédite = `BESOINS-MOTEUR.md`.

#### 8.5.1 `options_campagne` : des réglages faits au début

Deux types : `"case"` (`carnet[cle]` = `"1"` ou `"0"`) et `"siege"` (`carnet[cle]` = numéro du héros, 1 à 4).
Modifiables tant qu'aucun scénario n'est joué. `expert_seulement: true` : n'apparaît qu'en campagne experte.
{{JSONCLE:Fusion/marvel-lcg-src/data/campagnes/hunting_season.json|options_campagne}}

#### 8.5.2 `marche` : acheter des cartes entre deux scénarios

Entre deux scénarios, chaque héros dépense ses unités (ou son expérience) pour ajouter des cartes à son deck.
Elles y restent jusqu'à la fin de la campagne (le moteur les remet à chaque mise en place, depuis le carnet) ;
**une seule copie de chaque carte pour toute l'équipe**. Le coût est lu **dans le texte de la carte**
(`motif_cout`, expression régulière ; par défaut `Unit Cost (\d+)`). Voir `gmw` (plage `premiere_carte`…
`derniere_carte`) et `hunting_season` (liste `cartes`, `verrous`, `ouvert_apres_premier`, `unite`) :
{{JSONCLE:Fusion/marvel-lcg-src/data/campagnes/gmw.json|marche}}
{{JSONCLE:Fusion/marvel-lcg-src/data/campagnes/hunting_season.json|marche}}

#### 8.5.3 `cooperation` : la zone de coopération (Skrull Menace)

Une zone de cartes de campagne partagées, un tableau de progression à cases, un journal par scénario. Les clés du
carnet (`Cooperation Area`, `Cooperation Progress`, `Player N Cooperation Deck`, `Next Skrull Elite`…) sont
écrites par `skrull_menace/campaign.py`. **Mécanique propre à cette boîte** : voir
`modeles/D-patrons-de-campaign-py/skrull_menace/` et `data/campagnes/skrull_menace.json`. Le bloc :
{{JSONCLE:Fusion/marvel-lcg-src/data/campagnes/skrull_menace.json|cooperation}}

#### 8.5.4 `enquete` : la grille de déduction (Agents of S.H.I.E.L.D.)

27 combinaisons (9 par membre), 9 cartes de preuve en 3 séries ; chaque preuve obtenue raye les combinaisons qui
la contiennent. **La combinaison secrète vit côté serveur et ne sort jamais** (`_sans_secret`). Mécanique propre à
cette boîte :
{{JSONCLE:Fusion/marvel-lcg-src/data/campagnes/aos.json|enquete}}

#### 8.5.5 `bilan` : un score final saisi à la fin

`{ "titre", "cle", "aide", "libelle_ajout", "aide_ajout" }` : après le dernier scénario, le joueur peut ajouter
un dernier calcul à la piste cumulée du carnet (`cle`). Facultatif de bout en bout (Sinister Motives) :
{{JSONCLE:Fusion/marvel-lcg-src/data/campagnes/sm.json|bilan}}

#### 8.5.6 Ordre libre (`ordre_libre: true`, Fear No Evil)

Cinq « affaires » jouables dans l'ordre choisi, chacune contre un vilain ; avant chaque partie **deux affaires non
résolues progressent au hasard** ; à trois marques, l'affaire est perdue ; Kingpin quand tout est résolu. Les
règles pures sont dans `public/js/campagne/ordre-libre.js`. Déclaration : `ordre_libre: true`, `vilains: [{id, nom,
ordre}]`, `pages_vilains`, des scénarios `manigance: true` (plus un `final: true` avec `catalogue`). **Mécanique
propre à cette boîte** (`data/campagnes/fne.json`) :
{{JSONCLE:Fusion/marvel-lcg-src/data/campagnes/fne.json|vilains}}
{{JSONCLE:Fusion/marvel-lcg-src/data/campagnes/fne.json|pages_vilains}}

### 8.6 Les types (TypeScript) que l'écran applique

Les trois types qui *décrivent exactement* ce fichier, tels qu'ils sont dans le code :

{{BLOC:ui-app/src/board/campagne/contexte.ts|export type ScenarioCampagne|export type Campagne = {|typescript}}

{{BLOC:ui-app/src/board/campagne/detecteurs.ts|export type ChampVictoire|const SEP = ';'|typescript}}

### 8.7 Ce que le panneau fait des champs : l'ordre de priorité du pré-remplissage

Pour chaque champ `auto`, la valeur proposée est la **première** disponible parmi :

1. **le moteur** (`/get_carnet_suggere`) — **seulement si** l'estampille `scenario` du fichier sortant est égale à
   l'`id` du scénario joué (sinon le relevé du moteur est ignoré **en bloc**) ;
2. **le détecteur** déclaré (`detection`) ;
3. **la valeur déjà au carnet** (cumulée, jamais perdue).

Un champ `choix` n'est **jamais** pré-rempli par le moteur. À la validation, le carnet de la campagne devient
`{ ...ancien carnet, ...champs validés }` : **seules les clés déclarées dans la description sont reportées.** Un
champ `auto`/`int` **sans `detection`** est un **drapeau** : la valeur `"0"` ou vide est **retirée** avant
l'enregistrement (sinon le moteur lirait `"0"` comme vrai). Seul `pv_restants` peut produire `"0"` (une vraie mesure,
gardée) ; `compteur_manigance` et `compter_trait` ne rendent rien quand la valeur est 0 : la clé reste absente. Un champ
`parJoueur` est **sauté pour un héros éliminé**, qui échappe aussi à `obligatoire`.

Le panneau est **le même** pour toutes les campagnes et à plusieurs : chaque champ `parJoueur` est saisi par son
siège, tout le reste par l'hôte, seul à valider (`droits-carnet.ts`).

### 8.8 Règles d'écriture (ce que Claude va vérifier : `verifier-livraison-campagne.py` pour la forme, `tools/verifier_campagnes.py` pour les clés)

- [ ] `code` = nom du fichier = dossier de `public/stories/` ; `cle_extension` = clé de `sets_info.json`.
- [ ] `scenarios[].id` : chacun est dans `sets_info.json › scenarios`, a un fichier `data/scenarios/<id>.json`
      (**sans** `_expert` dans l'id) et, si `catalogue`, le fichier cité existe.
- [ ] `numero` : 1, 2, 3… sans trou, **égal au niveau appelé par la face 1A** (§7.3). **Un seul** `final`, sur le dernier.
- [ ] Chaque `victoire[].cle` existe **écrite** dans `campaign.py` (ou est choisie par le joueur) **et lue** par
      `CampaignSetup` (§7.10).
- [ ] Chaque `detection` figure dans la liste du §8.4 ; chaque `condition` est `complot_absent`.
- [ ] `tirage` : paliers croissants, `options` non vide, piste déclarée avant, `type: "auto"`.
- [ ] `deck: "requis"` ⇒ `parJoueur: true`.
- [ ] `options` ne contiennent que des `card_id` qui existent ; les `cases` sont bien formées.
- [ ] Pas de `detection` sur un champ `choix`.
- [ ] `resume`, `enjeu`, `libelle`, `aide` en français ; `nom_en`, `resume_en` en anglais.
- [ ] `pages` : `{}` ou noms conformes à §10.6.
