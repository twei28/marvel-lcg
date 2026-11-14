---

## 4. Les cartes : `data/cards.json`

Toutes les valeurs de ce chapitre ont été **mesurées le 20/10/2026 sur le fichier réel** (7 713 cartes, 170
packs), pas recopiées d'un ancien document. L'annexe A (`annexes/A-kit-cartes.md`) contient, en plus, un
catalogue d'exemples réels classés par mécanique : tu t'en sers pour *écrire* les scripts (§6).

### 4.1 Structure du fichier et forme de ta livraison

`data/cards.json` est un objet : **clé = nom du pack, valeur = liste de cartes**, plus une clé finale
`checksum`. Exemple de la forme (abrégé) :

```json
{
  "core": [ {...}, {...} ],
  "web_of_deceit": [ {...}, {...} ],
  "checksum": "…"
}
```

Tu ne livres **jamais** le fichier entier. Tu livres un fragment qui ne contient que **ton** pack :

```json
{
  "<pack>": [
    { "card_id": "xx001a", "type": "Villain", ... },
    { "card_id": "xx001b", "type": "Villain", ... }
  ]
}
```

Trie les cartes par `card_id`. Indentation : 4 espaces, `ensure_ascii=False` (les accents restent des accents).
Le `checksum` n'est pas ton affaire : Claude le recalcule avec `tools/recalculer_checksums.py` (le moteur rejette
en silence un fichier dont le checksum est faux).

### 4.2 Clés de premier niveau d'une carte

| Clé | Obligatoire | Sens |
|---|---|---|
| `card_id` | oui | L'identifiant, unique dans tout le jeu (§4.4). |
| `type` | oui | Un des types du §4.3. |
| `name` | oui | Le nom **imprimé**. Préfixe `"* "` = carte **unique** (`"* Shocker"`). |
| `subtitle` | oui | Le sous-titre imprimé, `""` sinon. |
| `desc` | oui | Statistiques et mots-clés, **toutes les valeurs en chaînes** (§4.5). `{}` si rien. |
| `traits` | oui | Liste de traits **en MAJUSCULES** : `["CRIMINAL", "SCIENTIST"]`, `[]` sinon. |
| `set_name` | oui | Le set de la carte. **Décide du dossier de son script** (§6.1). `""` pour une carte d'aspect ou basique. |
| `text` | oui (même vide `""`) | Le texte imprimé, avec balises (§4.6). |
| `custom` | **oui pour tout contenu fan-made** | Le nom de l'**auteur** (`"Nugget"`, `"Kajislav"`). Jamais un booléen. Sur **toutes** les faces, identités comprises : c'est ce qui fait afficher le créateur dans le jeu. |
| `full_link` | rare | La carte est un **clone intégral** d'une autre : `{"card_id": "wd051", "full_link": "32014"}` et **rien d'autre**. Sans script, sans image propre. |
| `ability_link` | rare | Mêmes **capacités** qu'une autre carte, mais données propres (nom, traits, image différents) : `"ability_link": "53035"`. |
| `pic_id` | rare | L'image d'une **autre** carte est empruntée (cartes génériques de statut). Sinon `card_id` sert de nom de fichier. |
| `unique_also` | rare | Liste de **noms** dont la carte partage l'unicité : `["Winter Soldier"]` (Bo-Wing et Winter Soldier ne coexistent pas). |
| `multiverse_of` | rare | Carte « Multiverse » jumelle : `"ra003"`. |
| `unique` | rare | `true` : unicité forcée quand le préfixe `"* "` du nom ne suffit pas. |

Le moteur Python **ignore les clés inconnues** et ne lit que `card_id`, `pic_id`, `type`, `name`, `subtitle`,
`desc`, `traits`, `set_name`, `text`. Les clés `custom`, `unique_also`… servent au client.

### 4.3 Les types de carte

Mesuré sur le fichier (le nombre est celui des cartes existantes) :

| `type` | Nombre | Sert à | Remarques |
|---|---|---|---|
| `Villain` | 350 | un vilain, **une carte par stade** | `Stage`, `HP` (souvent `"16*"` = par joueur ; `"INF"` = infini), `ATK`, `SCH` |
| `MainScheme` | 346 | complot principal, **une carte par face** (`…a` / `…b`) | `Stage` (`"1A"`, `"1B"`, `"2"`), `StartingThreat`, `TargetThreat`, `EscalationThreat` |
| `SideScheme` | 565 | complot annexe. **Dans les scripts, cette classe s'appelle `EncounterSideScheme`.** | `StartingThreat`, `Boost`, icônes `Acceleration`/`Hazard`/`Crisis`/`Amplify`, `Hinder` |
| `Minion` | 790 | sbire | `HP`, `ATK`, `SCH`, `Boost`, mots-clés |
| `Treachery` | 698 | traîtrise | `Boost`, parfois `Surge` |
| `Attachment` | 510 | attachement de rencontre | `Boost`, `ATK+`/`SCH+`/`THW+`/`DEF+` |
| `Environment` | 155 | environnement | `Boost`, `Setup`, `Permanent`, `Uses` |
| `Obligation` | 206 | obligation d'un héros | `GiveTo` (nom de l'alter-ego) |
| `Hero` / `AlterEgo` | 160 / 156 | les deux faces d'une identité (`…a` héros, `…b` alter-ego) | héros : `HP ATK THW DEF HS` ; alter-ego : `HP REC HS` |
| `Ally` `Event` `Upgrade` `Support` `Resource` | 649 / 1142 / 973 / 341 / 134 | cartes **joueur** | `Cost`, `RES`, `Class` |
| `PlayerSideScheme` | 66 | complot annexe de **joueur** | `StartingThreat`, `Class` |
| `Leader` | 24 | chef (mode bataille) | `Stage` |
| `Evidence` | 9 | preuve (campagne Agents of S.H.I.E.L.D.) | `Subtype` (`Means` / `Motive` / `Opportunity`) |
| `Path` | 12 | voie Shinobi (TMNT) | `Permanent`, `Class` |
| `Status` `Insert` `Challenge` `PlayerMinion` | 7 / 4 / 26 / 1 | cartes d'état, d'insert, de défi, sbire de joueur | rares |

Une carte de **campagne** qui récompense les joueurs (un allié, une amélioration, une ressource, un événement…)
est une carte joueur ordinaire dont `desc.Class` vaut **`"Campaign"`**, **`"Campaign;Basic"`** ou
**`"Campaign;<aspect>"`** (`"Campaign;Leadership"`, `"Campaign;'Pool"`…) et dont le `set_name` est celui de la
boîte : `"The Mad Titan's Shadow Campaign"`, `"Web of Deceit Rewards"`. Elles n'entrent dans un deck que par la
mise en place de la campagne (voir §7).

### 4.4 Identifiants : numérotation et préfixes

* **Contenu officiel** : **cinq chiffres** — numéro du pack puis numéro de carte (`01001` = pack 1, carte 1).
  Faces : suffixe `a` / `b` / `c` (`01001a` héros, `01001b` alter-ego ; `01097a`/`01097b` complot).
* **Contenu fan-made** : **deux lettres de préfixe propres à la source**, puis **trois chiffres**, puis le
  suffixe de face éventuel : `wd001a`, `hs164`, `sk289b`. Lettres et chiffres ne se rencontrent jamais :
  aucune collision possible avec les sorties officielles (qui vont jusqu'à 60 et au-delà).
* **Le préfixe est choisi AVANT la première carte.** Il est déclaré dans `tools/prefixes_fanmade.json`
  (le vérificateur `verifier_prefixes.py` refuse tout préfixe non déclaré). **Propose deux préfixes libres**
  à l'utilisateur, en question à choix multiple, et attends sa réponse. Préfixes **déjà pris** (liste exacte,
  lue dans le registre au moment de la construction du kit ; elle est aussi dans `reference/prefixes-pris.json`) :

{{PREFIXES:}}

* **Numérotation conseillée pour un pack de campagne** (modèle `wd`, `sk`) : le vilain et les complots du
  scénario 1 d'abord (`xx001a`, `xx001b`, `xx002a`…), puis ses cartes de rencontre ; puis le scénario suivant ;
  puis les sets modulaires ; puis les cartes de campagne et de récompense. **Numérotation continue, sans trou.**
  Le plus grand identifiant se déclare dans `sets_info.json` (`max_id`).
* **Plusieurs exemplaires** d'une même carte dans un deck de rencontre : **un seul `card_id`**, répété dans la
  liste du set (§5.2). **Deux exemplaires aux ressources différentes** = **deux** identifiants.
* **Une carte vue sur plusieurs boîtes** (réimpression) : un seul script (modèle de référence), plusieurs
  `card_id` si les numéros imprimés diffèrent, reliés par `ability_link` ou `full_link`.
* **Clé du pack** : nom court en minuscules et soulignés (`web_of_deceit`). C'est aussi le nom du dossier
  `src/cards/pack/<pack>/`.
* **`set_name`** : le nom du set imprimé (`"Shocker"`, `"Crime Wave"`). Set némésis d'un héros :
  `"<Héros> Nemesis"`.

### 4.5 `desc` : le contenu complet

**Toutes les valeurs sont des chaînes.** `"HP": "10"`, jamais `"HP": 10`.

#### 4.5.1 Statistiques et coûts

| Clé | Sens | Formes mesurées |
|---|---|---|
| `Cost` | coût | `"0"`…`"7"`, `"X"` (20 cartes), `"1*"` (variable), `"-1"` |
| `RES` | ressource(s) imprimée(s) : `R` physique, `B` mentale, `Y` énergie, `G` joker (wild) ; plusieurs lettres = plusieurs ressources | `"Y"`, `"BB"`, `"RY"`, `"YYY"`… |
| `Class` | classe | `Hero` (signature d'un héros), `Basic`, `Aggression`, `Justice`, `Leadership`, `Protection`, `Determination`, `'Pool`, `Venomized`, `Campaign`, `Campaign;Basic`, `Campaign;<aspect>`, `Encounter`… ; plusieurs valeurs séparées par `;` |
| `HP` | points de vie | `"10"` ; `"14*"` = **par joueur** (14 × nombre de joueurs) pour un vilain/sbire ; `"INF"` = infini |
| `ATK` `THW` `DEF` `REC` `SCH` | attaque, contre, défense, récupération, manigance | `"2"` ; `"1*"` sur `ATK`/`THW` d'un **allié** = **dégâts consécutifs** (1 dégât à l'allié par usage) — **un sens différent** du « par joueur » |
| `HS` | taille de main | `"5"` |
| `Boost` | nombre d'icônes de boost d'une carte de rencontre | `"0"`…`"4"` |
| `ATK+` `SCH+` `THW+` `DEF+` | bonus (ou malus) imprimé d'un attachement/amélioration à son porteur | `"1"`, `"-1"` |
| `Stage` | étape d'un vilain ou d'un complot | vilain : `"1"` `"2"` `"3"`, ou `"I"` `"II"` `"III"`, ou `"A"` `"B"` ; complot : `"1A"` `"1B"` `"2A"` … ou `"1"` `"2"` `"3"` |
| `StartingThreat` `TargetThreat` `EscalationThreat` | menaces d'un complot | `"7*"` = par joueur. Complot principal : `StartingThreat` souvent `"0"`/`"1*"`, `TargetThreat` `"7*"`…`"12*"`, `EscalationThreat` `"1*"` |
| `Uses` | `"<N>,<compteur>"` : la carte entre en jeu avec N compteurs et part quand le dernier est retiré | `"3,web"`, `"2*,ammo"` (`*` = par joueur), `"1+1*,fury"` |
| `GiveTo` | obligation : nom de l'alter-ego destinataire | `"Peter Parker"` |
| `Nemesis` | sbire némésis : nom du héros | `"Spider-Man"` |
| `MaxPerDeck` `MaxPerUnit` | limites de deck / par cible | `"1"` |
| `Victory` | points de victoire ; la carte va dans la pile de victoire quand vaincue. **`"0"` y envoie aussi la carte : ce n'est pas « neutre »** | `"0"` `"1"` `"2"` `"-1"` |
| `Requirement` | ressources obligatoires dans le paiement | `"B"`, `"YBR"` |
| `TeamUp` | événement Team-Up : les deux héros | `"Ant-Man;Wasp"` |
| `Teamwork` | trait du travail d'équipe | `"AVENGER"` |
| `Linked` | nom de la carte liée | `"Specialized Training"` |
| `UnitCost` | coût en unités (marché de campagne) | `"1"`…`"6"` |
| `ThreatLevel` | niveau de menace (mot-clé maison de Threat Level) | `"1"`…`"5"` |
| `Form` | forme (Spectrum) | `"Energy"`, `"Mass"`, `"Suit"` |
| `Subtype` | sous-type d'une preuve | `"Means"`, `"Motive"`, `"Opportunity"` |
| `CorrespondingCard` | complot annexe lié à un vilain précis | `"Wrecker"` |
| `Assault` | mot-clé Assaut | `"1"` |

#### 4.5.2 Mots-clés lus **directement** dans `desc` : AUCUN script

Ces mots-clés sont gérés **entièrement par le moteur** à partir de `desc`. **Tu ne les codes jamais dans un
script** : un script qui les recode les applique deux fois.

`Toughness`, `Guard`, `Patrol`, `Quickstrike`, `Retaliate`, `Surge`, `Villainous`, `Hazard`, `Crisis`,
`Acceleration`, `Amplify`, `Steady`, `Stalwart`, `Peril`, `Incite`, `Hinder`, `Vulnerable`, `Permanent`,
`Restricted`, `Setup` (entrée en jeu à la mise en place), `Temporary`, `Teamwork`, `Alliance`, `Uses`,
`Victory`, `Requirement`, `GiveTo`, `Boost` (le nombre d'icônes), `MaxPerDeck`, `MaxPerUnit`, `Nemesis`,
`TeamUp`, `Assault`.

Valeurs mesurées : `Toughness`/`Guard`/`Retaliate`/`Patrol`/`Quickstrike`… `"1"`, `"2"` (un compteur) ;
`Hinder` `"1*"` `"2*"` `"3*"` (par joueur) ; `Surge` `"1"` ; `Setup` `"1"` ; `Permanent` `"1"`.

Rappels de sens (pour choisir la bonne clé) :

* **Guard** : tant que ce sbire est engagé avec toi, tu ne peux pas attaquer le vilain.
* **Patrol** : tant que ce sbire est engagé avec toi, tu ne peux pas contrer le complot principal.
* **Crisis** : tant que ce complot annexe est en jeu, on ne peut pas retirer de menace du complot principal.
* **Hazard** : +1 carte de rencontre distribuée pendant la phase du vilain. **Acceleration** : +1 menace sur le
  complot principal au début de la phase du vilain. **Ne pas confondre.**
* **Hinder N** : la carte entre en jeu avec N menaces **sur elle-même**. **Incite N** : à la révélation, N
  menaces sur le **complot principal**.
* **Amplify** : ajoute des icônes de boost aux cartes de boost retournées. **Toughness** : entre en jeu avec une
  carte de statut Robuste (Tough). **Steady** : peut recevoir deux cartes de statut Sonné/Désorienté.
  **Stalwart** : ne peut pas être sonné ni désorienté. **Vulnerable** : défaussé s'il est sonné/désorienté.

**Ne mets pas un mot-clé dans `desc` si le texte imprimé de CETTE carte ne le porte pas**, et inversement : le
vérificateur `verifier_desc_mots_cles.py` compare texte et `desc`. Piège classique : « Uses (3 tactic counters) »
dans le texte sans `"Uses": "3,tactic"` dans `desc` → la carte entre en jeu **sans compteur** et son action reste
**grisée pour toujours**, sans aucun message.

⚠ Certains attributs n'existent que pour certains types (`Uses` : Upgrade/Support/Attachment/Obligation/
Environment ; `Villainous` : Minion). Le mettre ailleurs **empêche la carte de se générer** (KeyError).

#### 4.5.3 Quelles clés `desc` pour quel type (mesuré)

| Type | Clés attendues (fréquence) |
|---|---|
| Villain | `HP` 100 %, `Stage` 99 %, `SCH` 98 %, `ATK` 97 %, puis `Toughness`, `Steady`, `Retaliate`, `Stalwart`, `Victory` |
| MainScheme | `Stage` 100 %, `StartingThreat`, `TargetThreat`, `EscalationThreat` (~50 % : seules les faces « A » les portent) |
| SideScheme | `StartingThreat` 98 %, `Boost` 83 %, `Hinder`, `Acceleration`, `Hazard`, `Crisis`, `Amplify`, `Victory` |
| Minion | `HP` 100 %, `ATK`, `SCH`, `Boost` 76 %, `Nemesis`, `Toughness`, `Villainous`, `Quickstrike`, `Guard`, `Retaliate`, `Patrol`, `Victory` |
| Treachery | `Boost` 75 %, parfois `Surge` |
| Attachment | `Boost` 68 %, `ATK+` 37 %, `SCH+` 18 %, `Permanent`, `Uses` |
| Environment | `Boost` 21 %, `Surge`, `Setup`, `Permanent`, `Uses` |
| Obligation | `GiveTo` 92 %, `Boost` 89 % |
| Hero | `HP ATK THW DEF HS` (100 %) ; AlterEgo : `HP REC HS` |
| Ally | `HP` 100 %, `ATK` `THW` `Cost` `RES` `Class` |
| Event | `Cost` `Class` `RES` (100 %), `MaxPerDeck`, `TeamUp` |
| Upgrade / Support | `Class`, `RES`, `Cost`, `Uses`, `MaxPerUnit`, `Restricted`, `Permanent` |
| Resource | `RES`, `Class`, `MaxPerDeck` |
| PlayerSideScheme | `Class`, `StartingThreat`, `Cost`, `RES`, `Victory` |

#### 4.5.4 Traits et compteurs : listes blanches du moteur

* **Les traits** sont en MAJUSCULES, exactement comme imprimés (`"S.H.I.E.L.D"`, `"MASTERS OF EVIL"`). Le typage
  du moteur les liste (`CardFace.TRAITS`, `reference/traits.json` du zip) mais **aucun contrôle ne les lit à
  l'exécution** : un trait neuf ne casse pas une partie. **Tu l'écris quand même** et tu le signales dans
  `BESOINS-MOTEUR.md` (« trait nouveau : X, porté par xx012 ») : Claude l'ajoute à la liste.
* **Les compteurs** (`desc.Uses` : `"3,web"`) **ne sont PAS libres.** Le nom du compteur doit être dans l'énum
  `CardFace.COUNTER` (`reference/compteurs.json`) : sinon `desc.Uses` **lève une assertion** et la carte ne se
  construit pas. Un compteur neuf va dans `BESOINS-MOTEUR.md` ; Claude l'ajoute avant tout test.
* **Les jetons** (`k_threat`, `k_damage`, `k_acceleration_token`, `k_first_player_token`) et leurs noms
  `TOKEN` sont fixes.

### 4.6 Le texte imprimé (`text`) : balises et jetons

Le texte est en **anglais**, tel qu'imprimé, avec ces balises (mesurées sur tout le fichier) :

| Balise | Sens | Fréquence |
|---|---|---|
| `<b>…</b>` | gras : type de capacité (`<b>Response</b>`, `<b>When Revealed</b>`, `<b>Forced Interrupt</b>`…) | 8 335 |
| `<i>…</i>` | italique : rappel de règle, récit | 2 763 |
| `<hr />` | sépare le texte de la carte de son effet `[star] Boost` | 645 |
| `<em>…</em>` | emphase (rare) | 5 |
| `\n` | retour à la ligne (certains textes ont `\r\n` : sans importance) | — |
| `[star]` | étoile en tête de ligne : capacité étoilée (permanente, ou effet de Boost) | 1 651 |
| `[per_hero]` | « par joueur » | 371 |
| `[energy]` `[mental]` `[physical]` `[wild]` | icônes de ressource | |
| `[boost]` | une icône de boost | |
| `[crisis]` `[acceleration]` `[hazard]` `[amplify]` | icônes de complot | |
| `[consequential]` | dégâts consécutifs | |
| `[[TRAIT]]` | un trait, **entre doubles crochets** (`[[Tech]]`, `[[AVENGER]]`) | |
| `→` | flèche de coût (« Exhaust X → effet ») | |
| `•` | puce d'un « Choose one » | |

Les icônes de complot (`[crisis]`, `[acceleration]`, `[hazard]`, `[amplify]`) ont une **forme qui varie d'un
auteur à l'autre** : voir §4.8 et §14.5 (piège 53). Ne les nomme jamais à vue.

### 4.7 Cartes à plusieurs faces

* Un **complot principal** est **toujours** une paire `…a` (face A) / `…b` (face B). Il y a une paire par
  **stade**. La face A porte `StartingThreat`/`TargetThreat`/`EscalationThreat` ; la B est la face « avancée ».
* Un **vilain** a une carte **par stade** (`wd035`, `wd036`, `wd037` pour Electro I, II, III) ; un vilain
  **recto-verso** (Shocker, The Lizard) est une paire `…a`/`…b` écrite `"wd001a,wd001b"` dans le scénario.
* Les **faces d'identité** : `…a` héros, `…b` alter-ego (même carte, deux faces).
* Une face = **un fichier de script** si elle a des capacités (§6).

### 4.8 Icônes de ressource et de complot : jamais à vue

Une icône de **ressource** se lit **par comparaison** avec une carte du **même pack** dont la ressource est
connue : `R` physique (poing), `B` mentale (nœuds bleus), `Y` énergie (éclair), `G` joker (étoile verte). Si
l'utilisateur ne te donne pas la ressource en clair et que tu ne peux pas comparer, **pose la question**.

Les icônes de **complot** (Crisis, Acceleration, Hazard, Amplify) **n'ont pas la même forme chez tous les
auteurs** : chaque pack a ses conventions, validées par l'utilisateur (§14.5, piège 53). Compare à une carte du
**même pack** dont l'icône est connue. Les icônes **inconnues** vont dans `QUESTIONS.md`.

### 4.9 Exemples réels, un par type

Tous recopiés du fichier réel. **Web of Deceit** (campagne maison) :

**Vilain recto-verso, face A (wd001a) et B (wd001b)**
{{CARTE:wd001a}}
{{CARTE:wd001b}}

**Complot principal, faces A et B (wd002a / wd002b)**
{{CARTE:wd002a}}
{{CARTE:wd002b}}

**Complot annexe (wd015 The Long Night : permanent, victoire à la dernière menace retirée)**
{{CARTE:wd015}}

**Sbire unique (wd006)**
{{CARTE:wd006}}

**Traîtrise (wd012)**
{{CARTE:wd012}}

**Attachement (wd005)**
{{CARTE:wd005}}

**Environnement (wd030)**
{{CARTE:wd030}}

**Obligation (wd105)**
{{CARTE:wd105}}

**Récompense de campagne : allié (wd113), soutien (wd112), amélioration (wd125), ressource (wd128), complot annexe de joueur (wd140)**
{{CARTE:wd113}}
{{CARTE:wd112}}
{{CARTE:wd125}}
{{CARTE:wd128}}
{{CARTE:wd140}}

**The Mad Titan's Shadow** (campagne officielle) : un vilain, un complot principal, et des cartes de campagne.
{{CARTE:21071}}
{{CARTE:21074a}}
{{CARTE:21074b}}
{{CARTE:21183}}
{{CARTE:21185}}

### 4.10 Checklist de relecture d'une carte (à faire avant de livrer)

- [ ] `card_id` : préfixe déclaré, 3 chiffres, suffixe de face ; **aucun doublon** ; numérotation sans trou.
- [ ] `type` dans la liste du §4.3 ; `name` exact (préfixe `"* "` si unique) ; `custom` renseigné (fan-made).
- [ ] `desc` : **toutes les valeurs en chaînes** ; chaque mot-clé du texte est dans `desc` (et inversement) ;
      chaque nombre imprimé est identique dans `desc` et dans le script.
- [ ] `traits` en MAJUSCULES, exacts ; traits nouveaux signalés.
- [ ] `set_name` identique pour toutes les cartes d'un même set ; dossier de script = nom nettoyé (§6.1).
- [ ] `text` : balises du §4.6 ; icônes de ressource **comparées**, pas devinées.
- [ ] Une carte à capacité a un script **ou** un `A_FAIRE_CLAUDE` ; une carte sans capacité n'a pas de script.
- [ ] Une image `card_id` existe dans `images.md` ; un texte français existe dans le fragment du §10.3.
