# Kit de création de cartes et de campagnes : Marvel Champions (moteur `marvel-lcg`)

Ce document est le **manuel complet** d'un assistant (GPT) chargé de produire
des cartes et des campagnes pour un projet de jeu Marvel Champions. Ce qu'il
produit est ensuite **relu, intégré, testé et corrigé par Claude**, qui a
accès au dépôt. Le GPT, lui, n'a accès à rien d'autre qu'à ce document : tout
ce qu'il doit savoir est ici.

Tous les exemples de ce document sont **recopiés tels quels** de fichiers réels
du projet qui fonctionnent en jeu. Le chemin d'origine est indiqué en
commentaire au-dessus de chaque bloc. Les textes de cartes sont en anglais :
c'est la langue des données du moteur (la traduction française est gérée à
part, le GPT n'a pas à s'en occuper).

---

## Sommaire

1. Rôle et règles du GPT
2. Arborescence : où va chaque fichier
3. Le format d'une carte dans `cards.json`
4. Numérotation et identifiants
5. Scénarios et sets de rencontre
6. Campagnes
7. Écrire le script d'une carte
8. Catalogue d'exemples réels, classés par mécanique
9. Pièges connus
10. Format de livraison
11. Checklist d'auto-relecture
12. Ce que le GPT ne fait pas

---

## 1. Rôle et règles du GPT

### 1.1 Ce que tu fais

Tu transformes des cartes (texte, statistiques, scans décrits par
l'utilisateur, livret de règles) en **fichiers prêts à intégrer** :

- l'entrée JSON de chaque carte (`data/cards.json`) ;
- le script Python de chaque carte qui a une capacité ;
- pour un scénario : le fichier du scénario, les sets de rencontre ;
- pour une campagne : le fichier de description de la campagne et son
  `campaign.py`.

### 1.2 Règles absolues

1. **Format exact.** Respecte à la lettre les formats de ce document : noms de
   clés, majuscules, chaînes au lieu de nombres (`"HP": "10"`, jamais
   `"HP": 10`), structure des dossiers.
2. **N'invente jamais une fonction.** Tu n'utilises que les fonctions, classes,
   paramètres et chaînes de ciblage qui apparaissent dans ce document (section
   7 et exemples de la section 8). Si une mécanique ne s'y trouve pas, tu ne
   devines pas : tu écris à la place une ligne

   ```python
   # A_FAIRE_CLAUDE: <description précise de ce qui manque et du texte imprimé visé>
   ```

   et tu continues le reste de la carte. Une carte à moitié écrite avec un
   `A_FAIRE_CLAUDE` honnête vaut mieux qu'une carte complète qui appelle une
   fonction inventée : une fonction inventée ne lève souvent **aucune erreur**,
   la carte ne fait simplement rien en partie, et personne ne le voit.
3. **Une question à la fois.** Quand un texte laisse place à plus d'une
   lecture, tu poses **une seule** question, en **choix multiple**, l'option
   que tu recommandes en premier, « Autre (précise) » en dernier, et chaque
   option dit **ce que ça change en jeu**. Tu attends la réponse avant la
   question suivante. Tu ne regroupes jamais « voici mes 8 arbitrages, valide
   en bloc ».
4. **Signale chaque doute.** Chaque carte livrée se termine par la liste de
   tes doutes (section 10). « Aucun doute » est une réponse acceptable
   seulement si c'est vrai.
5. **Ne touche jamais au moteur.** Tu n'écris que des cartes, des scénarios et
   des campagnes. Si une carte demande une modification du moteur, c'est un
   `A_FAIRE_CLAUDE`.

### 1.3 Ce qui déclenche une question à l'utilisateur

| Situation | Exemple |
|---|---|
| Mot-clé maison non défini | « drain X » qu'aucune carte n'explique |
| Texte imprimé contradictoire | « Forced **Interrupt** : **After** X schemes » |
| Valeur que le format ne sait pas exprimer | une ATK imprimée « ★ » |
| Portée ambiguë d'une phrase | « Discard this obligation » : après la dernière option seulement, ou les deux ? |
| Icône que tu ne reconnais pas sur un scan | une forme inconnue dans le coin de ressource |
| Contenu absent | aucune liste de deck fournie pour un héros |

Ne posent **pas** de question : les choix purement techniques (quelle
fonction, où ranger une aide). Ceux-là, tu les fais et tu les expliques dans
tes doutes si tu hésites.

### 1.4 Icônes de ressource : jamais à vue

Une icône de ressource se lit **par comparaison** avec une carte du même pack
dont la ressource est connue : `R` physique (poing rouge), `B` mentale (nœuds
bleus), `Y` énergie (éclair jaune), `G` joker (étoile verte). Si l'utilisateur
ne te donne pas la ressource en clair et que tu ne peux pas comparer, pose la
question.

---

## 2. Arborescence : où va chaque fichier

Tous les chemins sont relatifs à la racine du moteur.

| Élément | Chemin |
|---|---|
| Données de toutes les cartes | `data/cards.json` (un objet : clé = nom du pack, valeur = liste de cartes) |
| Index des packs (scénarios, héros, sets) | `data/sets_info.json` |
| Un scénario | `data/scenarios/<id_scenario>.json` et `data/scenarios/<id_scenario>_expert.json` |
| Un set de rencontre (modulaire ou du scénario) | `data/encounter_sets/<nom_du_set>.json` |
| Un set némésis | `data/nemesis/<heros>_nemesis.json` |
| Deck de départ d'un héros | `deck/starter/<heros>.json` |
| Description d'une campagne (écran des campagnes) | `data/campagnes/<code>.json` |
| Logique de campagne (carnet, mise en place) | `src/cards/pack/<pack>/campaign.py` |
| Script d'une carte | `src/cards/pack/<pack>/<set_nettoyé>/<card_id>.py` |
| Fonctions partagées d'un pack | `src/cards/pack/<pack>/__init__.py` |
| Fonctions partagées d'un set | `src/cards/pack/<pack>/<set_nettoyé>/__init__.py` |

### 2.1 Où le moteur cherche le script d'une carte

Le moteur cherche, dans l'ordre :

1. `src/cards/pack/<pack>/<set_nettoyé>/<card_id>.py`
2. `src/cards/pack/<pack>/<card_id>.py`
3. si `set_name` finit par `Nemesis` : le dossier du set **sans** `_nemesis`.

Aucun fichier trouvé = carte sans capacité, **sans erreur**. Un script mal
rangé est donc muet : la carte entre en jeu et ne fait rien.

`<pack>` est la clé du pack dans `cards.json` (par exemple `core`, `fne`,
`web_of_deceit`). `<set_nettoyé>` est le `set_name` de la carte passé par la
règle suivante (copiée de `src/engine/file/manager.py`, fonction `CleanName`) :

```python
# Source : src/engine/file/manager.py
return name.lstrip('*').strip().lower().replace(" - ", "_").replace(" & ", "_").replace(' ', '_').replace("'", "").replace("-", "_").replace("!", "").replace("?", "").replace("(", "").replace(")", "").replace(".", "").replace(",", "").replace("\"", "").replace("&", "_").replace("#", "").replace("/", "")
```

Exemples : `"Spider-Man"` → `spider_man` ; `"Spider-Man Nemesis"` →
`spider_man_nemesis` ; `"Stop the Presses!"` → `stop_the_presses` ; `""`
(cartes d'aspect, sans set) → le script va à la racine du pack.

### 2.2 Les deux fichiers `__init__.py`

Chaque dossier de set contient un `__init__.py`. Le plus simple, une seule
ligne :

```python
# Source : src/cards/pack/core/spider_man/__init__.py
from cards.pack import *
```

Un pack peut y ranger des fonctions partagées par plusieurs cartes. Le set de
Klaw déclare ainsi la capacité commune à ses deux faces de vilain :

```python
# Source : src/cards/pack/core/klaw/__init__.py
from cards.pack import *

def GiveKlawAdditionalBoostCardWhenAttack():

    def give_additional_boost_card(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(EncounterVillain)
        Unused(this)

        message.GiveAdditionalBoostCardForThisActivation(1, effect)

    return AbilityFactory.WhenUnitWouldAttack(
        AbilityType.ForcedInterrupt,
        "This",
        give_additional_boost_card
    )
```

Et chaque script de carte commence par `from . import *`, qui importe tout ce
que le pack et le moteur exposent.

---

## 3. Le format d'une carte dans `cards.json`

### 3.1 Clés de premier niveau

| Clé | Obligatoire | Sens |
|---|---|---|
| `card_id` | oui | identifiant unique (voir section 4) |
| `type` | oui | type de carte (liste ci-dessous) |
| `name` | oui | nom imprimé ; préfixe `"* "` = carte **unique** (`"* Spider-Man"`) |
| `subtitle` | oui | sous-titre imprimé, `""` sinon |
| `desc` | oui | statistiques et mots-clés, **toutes les valeurs en chaînes** |
| `traits` | oui | liste de traits en MAJUSCULES (`["AVENGER"]`), `[]` sinon |
| `set_name` | oui | set de la carte ; `""` pour une carte d'aspect ou basique |
| `text` | oui (même vide `""`) | texte imprimé, avec balises (3.5) |
| `custom` | pour le contenu fan-made | nom de l'auteur de la carte |
| `full_link` | rare | la carte est un clone intégral d'une autre (`{"card_id": X, "full_link": Y}` et rien d'autre) |
| `ability_link` | rare | mêmes capacités qu'une autre carte, données propres |

Types existants : `Hero`, `AlterEgo`, `Ally`, `Event`, `Upgrade`, `Support`,
`Resource`, `Obligation`, `PlayerSideScheme`, `Villain`, `Minion`,
`Treachery`, `Attachment`, `Environment`, `SideScheme`, `MainScheme`,
`Leader`, `Evidence`, `Status`, `Insert`, `Challenge`.

### 3.2 Clés de `desc`

| Clé | Sens | Exemple |
|---|---|---|
| `Cost` | coût | `"3"` |
| `RES` | ressource(s) imprimée(s) : `R` physique, `B` mentale, `Y` énergie, `G` joker ; deux lettres = deux ressources | `"Y"`, `"YY"` |
| `Class` | classe : `Hero` (signature), `Basic`, `Aggression`, `Justice`, `Leadership`, `Protection`, `Determination`, `'Pool`, `Campaign`, `Encounter` ; combinaisons avec `;` (`"Campaign;Basic"`) | `"Hero"` |
| `HP` | points de vie ; `"14*"` = **par joueur** pour un vilain/sbire | `"10"`, `"14*"` |
| `ATK`, `THW`, `DEF`, `REC`, `SCH` | attaque, contre, défense, récupération, manigance | `"2"` |
| `ATK`/`THW` d'un **allié** avec `*` | `"1*"` = 1 dégât **consécutif** par usage (sens différent du « par joueur ») | `"1*"` |
| `HS` | taille de main | `"5"` |
| `Boost` | nombre d'icônes de boost d'une carte de rencontre | `"2"` |
| `ATK+`, `SCH+`, `THW+` | bonus imprimé d'un attachement au porteur | `"1"` |
| `Stage` | étape d'un vilain ou d'une manigance | `"1"`, `"2"`, `"1A"` |
| `StartingThreat`, `TargetThreat`, `EscalationThreat` | menaces d'une manigance (`"7*"` = par joueur) | `"2*"` |
| `Uses` | `"<N>,<nom du compteur>"` : la carte entre en jeu avec N compteurs et part au dernier | `"3,web"` |
| `GiveTo` | obligation : nom de l'alter-ego destinataire | `"Peter Parker"` |
| `Nemesis` | sbire némésis : nom du héros | `"Spider-Man"` |
| `MaxPerDeck`, `MaxPerUnit` | limites de deck / par cible | `"1"` |
| `Victory` | va dans la pile de victoire quand vaincue ; `"0"` n'est PAS neutre | `"1"` |
| `Requirement` | ressources obligatoires dans le paiement (pas un coût en plus) | `"B"` |
| `TeamUp` | événement Team-Up : `"Héros1;Héros2"` | `"Daredevil;Echo"` |
| `Teamwork` | trait du travail d'équipe | `"TRACKSUIT"` |
| `Linked` | nom de la carte liée | `"Specialized Training"` |
| `UnitCost` | coût en unités (campagne Galaxy's Most Wanted) | `"1"` |
| Mots-clés en compteur (`"1"`, `"2"`, `"1*"`) | `Toughness`, `Guard`, `Patrol`, `Quickstrike`, `Retaliate`, `Surge`, `Villainous`, `Hazard`, `Crisis`, `Acceleration`, `Amplify`, `Steady`, `Stalwart`, `Peril`, `Incite`, `Hinder`, `Vulnerable`, `Permanent`, `Restricted`, `Setup`, `Temporary`, `Alliance` | `"Guard": "1"`, `"Hinder": "2*"` |

### 3.3 Les mots-clés lus directement dans `desc` : AUCUN script

Les mots-clés suivants sont gérés **entièrement par le moteur** à partir de
`desc`. Tu ne les codes **jamais** dans un script : un script qui les recode
les applique deux fois.

`Toughness`, `Guard`, `Patrol`, `Quickstrike`, `Retaliate`, `Surge`,
`Villainous`, `Hazard`, `Crisis`, `Acceleration`, `Amplify`, `Steady`,
`Stalwart`, `Peril`, `Incite`, `Hinder`, `Vulnerable`, `Permanent`,
`Restricted`, `Setup` (l'entrée en jeu à la mise en place), `Temporary`,
`Teamwork`, `Alliance`, `Uses`, `Victory`, `Requirement`, `GiveTo`, `Boost`
(le nombre d'icônes), `MaxPerDeck`, `MaxPerUnit`, `Nemesis`, `TeamUp` (la
présence des deux héros).

Le script ne code que les **autres** capacités imprimées de la carte.

Rappels de sens (pour bien choisir la clé) :

- **Guard** : tant que ce sbire est engagé avec toi, tu ne peux pas attaquer
  le vilain.
- **Patrol** : tant que ce sbire est engagé avec toi, tu ne peux pas contrer
  le complot principal. Réservé aux sbires.
- **Crisis** : tant que ce complot annexe est en jeu, on ne peut pas retirer
  de menace du complot principal.
- **Hazard** : +1 carte de rencontre distribuée pendant la phase du vilain.
- **Acceleration** : +1 menace sur le complot principal au début de la phase
  du vilain. Ne pas confondre avec Hazard.
- **Hinder N** : la carte entre en jeu avec N menaces **sur elle-même**.
- **Incite N** : à la révélation, N menaces sur le **complot principal**.
- **Amplify** : ajoute des icônes de boost aux cartes de boost retournées.
- **Toughness** : entre en jeu avec une carte de statut Robuste.
- **Steady** : peut recevoir deux cartes de statut Sonné ou Désorienté.
- **Stalwart** : ne peut pas être sonné ni désorienté.
- **Vulnerable** : défaussé s'il est sonné ou désorienté.
- **Victory N** : vaincue, la carte va dans la pile de victoire. `"0"` l'y
  envoie aussi.

### 3.4 Exemples réels, un par type de carte

**Héros (recto)**

```json
{
    "card_id": "01001a",
    "type": "Hero",
    "name": "* Spider-Man",
    "subtitle": "",
    "desc": {
        "HP": "10",
        "ATK": "2",
        "THW": "1",
        "DEF": "3",
        "HS": "5"
    },
    "traits": [
        "AVENGER"
    ],
    "set_name": "Spider-Man",
    "text": "Spider-Sense — <b>Interrupt</b>: When the villain initiates an attack against you, draw 1 card."
}
```

**Alter-ego (verso)**

```json
{
    "card_id": "01001b",
    "type": "AlterEgo",
    "name": "* Peter Parker",
    "subtitle": "",
    "desc": {
        "HP": "10",
        "REC": "3",
        "HS": "6"
    },
    "traits": [
        "GENIUS"
    ],
    "set_name": "Spider-Man",
    "text": "Scientist — <b>Resource</b>: Generate a [mental] resource. (Limit once per round.)"
}
```

**Allié** (`"THW": "1*"` = 1 dégât consécutif quand il contre)

```json
{
    "card_id": "01002",
    "type": "Ally",
    "name": "* Black Cat",
    "subtitle": "Felicia Hardy",
    "desc": {
        "Cost": "2",
        "HP": "2",
        "ATK": "1",
        "THW": "1*",
        "RES": "Y",
        "Class": "Hero"
    },
    "traits": [
        "HERO FOR HIRE"
    ],
    "set_name": "Spider-Man",
    "text": "<b>Forced Response</b>: After you play Black Cat, discard the top 2 cards of your deck. Add each card with a printed [mental] resource discarded this way to your hand."
}
```

**Événement**

```json
{
    "card_id": "01005",
    "type": "Event",
    "name": "Swinging Web Kick",
    "subtitle": "",
    "desc": {
        "Cost": "3",
        "RES": "B",
        "Class": "Hero"
    },
    "traits": [
        "AERIAL",
        "ATTACK",
        "SUPERPOWER"
    ],
    "set_name": "Spider-Man",
    "text": "<b>Hero Action</b> <i>(attack)</i>: Deal 8 damage to an enemy."
}
```

**Soutien**

```json
{
    "card_id": "01006",
    "type": "Support",
    "name": "* Aunt May",
    "subtitle": "",
    "desc": {
        "Cost": "1",
        "RES": "Y",
        "Class": "Hero"
    },
    "traits": [
        "PERSONA"
    ],
    "set_name": "Spider-Man",
    "text": "<b>Alter-Ego Action</b>: Exhaust Aunt May → heal 4 damage from Peter Parker."
}
```

**Amélioration avec `Uses`**

```json
{
    "card_id": "01008",
    "type": "Upgrade",
    "name": "Web-Shooter",
    "subtitle": "",
    "desc": {
        "Cost": "1",
        "RES": "R",
        "Uses": "3,web",
        "Class": "Hero"
    },
    "traits": [
        "ITEM",
        "TECH"
    ],
    "set_name": "Spider-Man",
    "text": "Uses (3 web counters). <i>(Enters play with 3 counters. When those are gone, discard this card)</i>\n<b>Hero Resource</b>: Exhaust Web-Shooter and remove 1 web counter from it → generate a [wild] resource."
}
```

**Ressource basique** (aucun script : la ressource est lue dans `RES`)

```json
{
    "card_id": "01088",
    "type": "Resource",
    "name": "Energy",
    "subtitle": "",
    "desc": {
        "RES": "YY",
        "MaxPerDeck": "1",
        "Class": "Basic"
    },
    "traits": [],
    "set_name": "",
    "text": "Max 1 per deck."
}
```

**Vilain, une entrée par étape** (`"HP": "14*"` = 14 par joueur)

```json
{
    "card_id": "01094",
    "type": "Villain",
    "name": "* Rhino",
    "subtitle": "",
    "desc": {
        "HP": "14*",
        "ATK": "2",
        "SCH": "1",
        "Stage": "1"
    },
    "traits": [
        "BRUTE",
        "CRIMINAL"
    ],
    "set_name": "Rhino",
    "text": ""
}
```

```json
{
    "card_id": "01095",
    "type": "Villain",
    "name": "* Rhino",
    "subtitle": "",
    "desc": {
        "HP": "15*",
        "ATK": "3",
        "SCH": "1",
        "Stage": "2"
    },
    "traits": [
        "BRUTE",
        "CRIMINAL"
    ],
    "set_name": "Rhino",
    "text": "<b>When Revealed</b>: Search the encounter deck and discard pile for the Breakin' & Takin' side scheme and reveal it. Shuffle the encounter deck."
}
```

```json
{
    "card_id": "01096",
    "type": "Villain",
    "name": "* Rhino",
    "subtitle": "",
    "desc": {
        "HP": "16*",
        "ATK": "4",
        "SCH": "1",
        "Toughness": "1",
        "Stage": "3"
    },
    "traits": [
        "BRUTE",
        "CRIMINAL"
    ],
    "set_name": "Rhino",
    "text": "Toughness. <i>(This character enter play with a tough status card.)</i>\n<b>When Revealed</b>: Stun each hero."
}
```

**Complot principal, recto puis verso** (les deux faces sont deux entrées,
suffixes `a` et `b`)

```json
{
    "card_id": "01097a",
    "type": "MainScheme",
    "name": "The Break-In!",
    "subtitle": "",
    "desc": {
        "Stage": "1"
    },
    "traits": [],
    "set_name": "Rhino"
}
```

```json
{
    "card_id": "01097b",
    "type": "MainScheme",
    "name": "The Break-In!",
    "subtitle": "",
    "desc": {
        "StartingThreat": "0",
        "TargetThreat": "7*",
        "EscalationThreat": "1*",
        "Stage": "1"
    },
    "traits": [],
    "set_name": "Rhino",
    "text": "<b>If this stage is completed, the players lose the game.</b>"
}
```

**Complot principal de campagne fan-made** (étapes `"1A"` / `"1B"`)

```json
{
    "card_id": "wd002a",
    "type": "MainScheme",
    "name": "Shock Party",
    "subtitle": "",
    "desc": {
        "Stage": "1A"
    },
    "traits": [],
    "set_name": "Shocker",
    "text": "<b>Contents</b>: Shocker (A). <i>(Shocker (B) instead for expert mode.)</i> Shocker, City in Chaos, Power Drain II, and Standard III encounter sets. One modular encounter set <i>(recommended: Crime Wave)</i>.\n<b>Setup</b>: Search the encounter deck for The Long Night side scheme and reveal it. Remove each obligation card in the encounter deck from the game.",
    "custom": "Ripper3"
}
```

```json
{
    "card_id": "wd002b",
    "type": "MainScheme",
    "name": "Shock Party",
    "subtitle": "",
    "desc": {
        "StartingThreat": "0",
        "TargetThreat": "4*",
        "EscalationThreat": "1*",
        "Stage": "1B"
    },
    "traits": [],
    "set_name": "Shocker",
    "text": "<b>When Revealed</b>: Search the encounter deck and discard pile for the Vibro-Shock Gauntlets attachment and reveal it.",
    "custom": "Ripper3"
}
```

**Vilain recto-verso** (une seule carte à deux faces, fan-made)

```json
{
    "card_id": "wd001a",
    "type": "Villain",
    "name": "* Shocker",
    "subtitle": "",
    "desc": {
        "HP": "10",
        "ATK": "1",
        "SCH": "1",
        "Steady": "1"
    },
    "traits": [
        "CRIMINAL"
    ],
    "set_name": "Shocker",
    "text": "Steady.\n<b>When Defeated</b>: Remove 5 threat from a side scheme. Flip this card.",
    "custom": "Ripper3"
}
```

```json
{
    "card_id": "wd001b",
    "type": "Villain",
    "name": "* Shocker",
    "subtitle": "",
    "desc": {
        "HP": "20",
        "ATK": "2",
        "SCH": "2",
        "Retaliate": "1"
    },
    "traits": [
        "CRIMINAL",
        "MASTERS OF EVIL"
    ],
    "set_name": "Shocker",
    "text": "Retaliate 1.\n<b>When Defeated</b>: Deal 1 damage to each hero. Remove 10 threat from a side scheme. Flip this card.",
    "custom": "Ripper3"
}
```

**Complot annexe** (Boost, Hazard, menace de départ)

```json
{
    "card_id": "01107",
    "type": "SideScheme",
    "name": "Breakin' & Takin'",
    "subtitle": "",
    "desc": {
        "Boost": "2",
        "Hazard": "1",
        "StartingThreat": "2"
    },
    "traits": [],
    "set_name": "Rhino",
    "text": "<b>When Revealed</b>: Place an additional 1 [per_hero] threat here.\n<i>(Hazard Icon: Deal +1 encounter card during the villain phase.)</i>"
}
```

**Complot annexe avec Crisis**

```json
{
    "card_id": "01108",
    "type": "SideScheme",
    "name": "Crowd Control",
    "subtitle": "",
    "desc": {
        "Boost": "2",
        "Crisis": "1",
        "StartingThreat": "2*"
    },
    "traits": [],
    "set_name": "Rhino",
    "text": "<i>(Crisis Icon: While this scheme is in play, you cannot remove threat from the main scheme.)</i>"
}
```

**Complot annexe avec Hinder et Victory**

```json
{
    "card_id": "16127",
    "type": "SideScheme",
    "name": "Hujahdarian Monarch Egg",
    "subtitle": "",
    "desc": {
        "Boost": "1",
        "Acceleration": "1",
        "StartingThreat": "3",
        "Hinder": "2*",
        "Victory": "0"
    },
    "traits": [],
    "set_name": "Galactic Artifacts",
    "text": "Hinder 2[per_hero]. Victory 0.\r\n<b>When Defeated:</b> The player who defeated this scheme may ready their identity."
}
```

**Sbire** (Guard)

```json
{
    "card_id": "01101",
    "type": "Minion",
    "name": "Hydra Mercenary",
    "subtitle": "",
    "desc": {
        "HP": "3",
        "ATK": "1",
        "SCH": "0",
        "Boost": "1",
        "Guard": "1"
    },
    "traits": [
        "HYDRA"
    ],
    "set_name": "Rhino",
    "text": "Guard. <i>(While this minion is engaged with you, you cannot attack the villain.)</i>"
}
```

**Sbire avec Patrol et Vulnerable**

```json
{
    "card_id": "60103",
    "type": "Minion",
    "name": "Security Guard",
    "subtitle": "",
    "desc": {
        "HP": "4",
        "ATK": "2",
        "SCH": "0",
        "Boost": "1",
        "Patrol": "1",
        "Vulnerable": "1"
    },
    "traits": [
        "CIVILIAN",
        "INFLUENCED"
    ],
    "set_name": "Purple Man",
    "text": "Patrol. Vulnerable.\n<b>When Defeated</b>: Discard the ally with the highest ATK <i>(among allies)</i> in play."
}
```

**Traîtrise**

```json
{
    "card_id": "01104",
    "type": "Treachery",
    "name": "Hard to Keep Down",
    "subtitle": "",
    "desc": {},
    "traits": [],
    "set_name": "Rhino",
    "text": "<b>When Revealed</b>: Rhino heals 4 damage. If no damage was healed this way, this card gains surge."
}
```

**Attachement** (bonus `ATK+` et Boost)

```json
{
    "card_id": "01100",
    "type": "Attachment",
    "name": "Enhanced Ivory Horn",
    "subtitle": "",
    "desc": {
        "Boost": "2",
        "ATK+": "1"
    },
    "traits": [
        "WEAPON"
    ],
    "set_name": "Rhino",
    "text": "Attach to Rhino.\n<b>Hero Action</b>: Spend [physical] [physical] [physical] resources → discard this card"
}
```

**Obligation** (`GiveTo`)

```json
{
    "card_id": "01165",
    "type": "Obligation",
    "name": "Eviction Notice",
    "subtitle": "",
    "desc": {
        "Boost": "2",
        "GiveTo": "Peter Parker"
    },
    "traits": [],
    "set_name": "Spider-Man",
    "text": "<b><i>Give to the Peter Parker player.</i></b>\nYou may flip to alter-ego form. Choose:\n• Exhaust Peter Parker → remove Eviction Notice from the game.\n• Discard 1 card at random from your hand. This card gains surge. Discard this obligation."
}
```

**Set némésis : sbire némésis** (`Nemesis`, Quickstrike)

```json
{
    "card_id": "01167",
    "type": "Minion",
    "name": "* Vulture",
    "subtitle": "",
    "desc": {
        "HP": "4",
        "ATK": "3",
        "SCH": "1",
        "Boost": "2",
        "Quickstrike": "1",
        "Nemesis": "Spider-Man"
    },
    "traits": [
        "CRIMINAL"
    ],
    "set_name": "Spider-Man Nemesis",
    "text": "Quickstrike. <i>(After this minion engages your hero, it attacks.)</i>"
}
```

**Set némésis : complot annexe**

```json
{
    "card_id": "01166",
    "type": "SideScheme",
    "name": "Highway Robbery",
    "subtitle": "",
    "desc": {
        "Boost": "3",
        "Acceleration": "1",
        "StartingThreat": "3*"
    },
    "traits": [],
    "set_name": "Spider-Man Nemesis",
    "text": "<b>When Revealed</b>: Each player places a random card from their hand facedown here.\n<b>When Defeated</b>: Return each facedown card here to its owner's hand."
}
```

**Environnement**

```json
{
    "card_id": "60152",
    "type": "Environment",
    "name": "Daily Bugle",
    "subtitle": "",
    "desc": {},
    "traits": [],
    "set_name": "Stop the Presses!",
    "text": "<b>Alter-Ego Action</b>: Exhaust a [[Daily Bugle]] support you control → place 1 stamina counter on that support. <i>(Any player can do this.)</i>"
}
```

**Environnement avec Setup**

```json
{
    "card_id": "60112",
    "type": "Environment",
    "name": "Disturbed Psyche",
    "subtitle": "",
    "desc": {
        "Setup": "1"
    },
    "traits": [],
    "set_name": "Typhoid Mary",
    "text": "Setup.\n<b>Setup</b>: Put the villain into play on a random side <i>(and reveal it)</i>.\n<b>Forced Interrupt</b>: When the villain phase ends, flip the villain.\n<b>If there are 3 or more tokens here, the players win the game!</b>"
}
```

**Manigance du joueur** (`PlayerSideScheme`)

```json
{
    "card_id": "60024",
    "type": "PlayerSideScheme",
    "name": "* De-escalation",
    "subtitle": "",
    "desc": {
        "Cost": "0",
        "StartingThreat": "4",
        "Victory": "0",
        "RES": "R",
        "Class": "Justice"
    },
    "traits": [],
    "set_name": "",
    "text": "Victory 0.\n<b>When Defeated</b>: Remove an acceleration token from play."
}
```

**Événement Team-Up**

```json
{
    "card_id": "60055",
    "type": "Event",
    "name": "See No Evil, Hear No Evil",
    "subtitle": "",
    "desc": {
        "Cost": "2",
        "RES": "G",
        "MaxPerDeck": "1",
        "TeamUp": "Daredevil;Echo",
        "Class": "Basic"
    },
    "traits": [
        "ATTACK",
        "THWART"
    ],
    "set_name": "",
    "text": "Team-Up (Daredevil and Echo). Max 1 per deck.\n<b>Hero Action</b> <i>(attack/thwart)</i>: Choose 2 of the following (you may choose the same option twice):\n• Deal 3 damage to an enemy.\n• Remove 3 threat from a scheme."
}
```

**Amélioration de campagne** (`Permanent`, `Setup`, classe `Campaign;Basic`)

```json
{
    "card_id": "04159a",
    "type": "Upgrade",
    "name": "Basic Thwart Upgrade",
    "subtitle": "",
    "desc": {
        "Class": "Campaign;Basic",
        "Permanent": "1",
        "Setup": "1"
    },
    "traits": [
        "CONDITION"
    ],
    "set_name": "Hydra Campaign",
    "text": "Permanent. Setup.\nYou get +2 hit points.\nYour hero gets +1 THW."
}
```

### 3.5 Balises du texte imprimé (`text`)

| Balise | Sens |
|---|---|
| `<b>Hero Action</b>`, `<b>Response</b>`... | type de capacité en gras |
| `<i>(...)</i>` | texte de rappel en italique ; `<i>(attack)</i>` après le type = libellé |
| `[star]` en tête de ligne | capacité étoilée (permanente, ou effet de Boost) |
| `<hr />` | sépare le texte de la carte de son effet `[star] Boost` |
| `[boost]` | une icône de boost |
| `[per_hero]` | « par joueur » |
| `[physical]`, `[mental]`, `[energy]`, `[wild]` | icônes de ressource |
| `[crisis]`, `[acceleration]`, `[hazard]`, `[amplify]` | icônes de complot |
| `[[TRAIT]]` | un trait (`[[Tech]]`, `[[AVENGER]]`) |
| `→` | flèche de coût (« Exhaust X → effet ») |
| `•` | puce d'un « Choose one » |
| `\n` | retour à la ligne |

### 3.6 Traits

Les traits sont en MAJUSCULES, exactement comme imprimés (`"S.H.I.E.L.D"`,
`"MASTERS OF EVIL"`, `"HERO FOR HIRE"`). Si un trait n'existe pas encore dans
le jeu, écris-le quand même et signale-le dans tes doutes (« trait nouveau :
X ») : Claude l'ajoutera à la liste du moteur.

---

## 4. Numérotation et identifiants

- **Contenu officiel** : cinq chiffres, numéro du pack puis numéro de carte
  (`01001` = pack 1, carte 1). Faces : suffixe `a` / `b` (`01001a` héros,
  `01001b` alter-ego ; `01097a` / `01097b` complot).
- **Contenu fan-made** : **deux lettres** de préfixe propres à la source, puis
  trois chiffres, puis le suffixe de face éventuel : `hc001a`, `hc001b`,
  `wd002a`, `wd005`. Lettres et chiffres ne se rencontrent jamais : aucune
  collision possible avec les sorties officielles.
- **Le préfixe est choisi AVANT la première carte** et déclaré par Claude.
  Préfixes déjà pris (à ne pas réutiliser) : `aa ab ag ah al an ar as av bc
  bk bl br bt bw cc cd cn dd dr dt dz gb gp gs hc hd hk ho ht ih il im ip iw
  jj kb lj ls ma mf mk mu mw nt nv ok pt ra rg sd sf sg si sk sm sn sp sr ss
  st su sw tg th tt vp vr vv vz wc wd wx yd ze`. Propose deux préfixes libres
  à l'utilisateur, en question à choix multiple.
- **Numérotation conseillée dans un pack de campagne** (modèle `wd`) : vilain
  et complots du scénario 1 d'abord (`xx001a`, `xx001b`, `xx002a`...), puis
  ses cartes de rencontre, puis le scénario suivant, puis les sets modulaires,
  puis les cartes de campagne et de récompense. Une numérotation continue,
  sans trou.
- **Deux exemplaires d'une même carte aux ressources différentes** = deux
  identifiants (`hc007a`, `hc007b`), pas un seul.
- **Clé du pack** dans `cards.json` : un nom court en minuscules et
  soulignés (`web_of_deceit`). C'est aussi le nom du dossier
  `src/cards/pack/<pack>/`.
- **`set_name`** : le nom du set imprimé (`"Shocker"`, `"Crime Wave"`) ;
  set némésis : `"<Héros> Nemesis"`.

---

## 5. Scénarios et sets de rencontre

### 5.1 Fichier d'un scénario

`data/scenarios/<id>.json`, où `<id>` est en minuscules et soulignés
(`rhino`, `wd_shocker`). Clés, toutes obligatoires :

| Clé | Sens |
|---|---|
| `version` | toujours `"0.5.8"` |
| `name` | nom affiché du scénario |
| `villain` | les étapes du vilain en jeu, dans l'ordre : `["01094", "01095"]` (standard : étapes 1 et 2 ; expert : 2 et 3). Un vilain recto-verso s'écrit `"recto,verso"` |
| `expert` | `false` dans le fichier standard, `true` dans le fichier `_expert` |
| `schemes` | les étapes du complot principal, chacune `"recto,verso"` : `["01097a,01097b"]` |
| `set_aside` | cartes mises de côté au départ (le jeu les sortira par effet) |
| `encounters` | cartes de rencontre propres au scénario, **une entrée par exemplaire** |
| `encounter_sets` | sets de rencontre ajoutés (`"standard"`, `"expert"`, ou un set à soi) |
| `modular_sets` | set(s) modulaire(s) recommandé(s) |

Le cœur du scénario peut vivre dans `encounters` (modèle officiel Rhino) OU
dans un set à part listé dans `encounter_sets` (modèle fan-made Shocker, où
`encounters` est vide). Choisis l'une des deux, pas les deux.

**Exemple officiel, standard puis expert :**

```json
{
    "version": "0.5.8",
    "name": "Rhino",
    "villain": [
        "01094",
        "01095"
    ],
    "expert": false,
    "schemes": [
        "01097a,01097b"
    ],
    "set_aside": [
    ],
    "encounters": [
        "01098",
        "01099",
        "01099",
        "01100",
        "01101",
        "01101",
        "01102",
        "01103",
        "01104",
        "01104",
        "01105",
        "01105",
        "01106",
        "01106",
        "01106",
        "01107",
        "01108"
    ],
    "encounter_sets": [
        "standard"
    ],
    "modular_sets": [
        "bomb_scare"
    ]
}
```

```json
{
    "version": "0.5.8",
    "name": "Rhino",
    "villain": [
        "01095",
        "01096"
    ],
    "expert": true,
    "schemes": [
        "01097a,01097b"
    ],
    "set_aside": [
    ],
    "encounters": [
        "01098",
        "01099",
        "01099",
        "01100",
        "01101",
        "01101",
        "01102",
        "01103",
        "01104",
        "01104",
        "01105",
        "01105",
        "01106",
        "01106",
        "01106",
        "01107",
        "01108"
    ],
    "encounter_sets": [
        "standard",
        "expert"
    ],
    "modular_sets": [
        "bomb_scare"
    ]
}
```

**Exemple fan-made de campagne, standard puis expert** (vilain recto-verso,
trois étapes de complot, cartes mises de côté) :

```json
{
    "version": "0.5.8",
    "name": "Shocker",
    "villain": [
        "wd001a,wd001b"
    ],
    "expert": false,
    "schemes": [
        "wd002a,wd002b",
        "wd003a,wd003b",
        "wd004a,wd004b"
    ],
    "set_aside": [
        "wd030",
        "wd031",
        "wd032"
    ],
    "encounters": [],
    "encounter_sets": [
        "shocker",
        "city_in_chaos",
        "power_drain_ii",
        "standard_iii",
        "bodyguard"
    ],
    "modular_sets": [
        "crime_wave"
    ]
}
```

```json
{
    "version": "0.5.8",
    "name": "Shocker",
    "villain": [
        "wd001b,wd001a"
    ],
    "expert": true,
    "schemes": [
        "wd002a,wd002b",
        "wd003a,wd003b",
        "wd004a,wd004b"
    ],
    "set_aside": [
        "wd030",
        "wd031",
        "wd032"
    ],
    "encounters": [],
    "encounter_sets": [
        "shocker",
        "city_in_chaos",
        "power_drain_ii",
        "standard_iii",
        "bodyguard"
    ],
    "modular_sets": [
        "crime_wave"
    ]
}
```

### 5.2 Fichier d'un set de rencontre

`data/encounter_sets/<nom>.json`, une entrée par exemplaire :

```json
{
    "version": "0.5.8",
    "name": "Bomb Scare",
    "encounters": [
        "01109",
        "01110",
        "01110",
        "01111",
        "01112",
        "01112"
    ]
}
```

```json
{
    "version": "0.5.8",
    "name": "shocker",
    "encounters": [
        "wd005",
        "wd006",
        "wd007",
        "wd008",
        "wd009",
        "wd010",
        "wd011",
        "wd012",
        "wd013",
        "wd014",
        "wd014",
        "wd015"
    ]
}
```

Les sets communs : `standard` et `expert` (core), réutilisables tels quels :

```json
{
    "version": "0.5.8",
    "name": "Standard",
    "encounters": [
        "01186",
        "01186",
        "01187",
        "01187",
        "01188",
        "01189",
        "01190"
    ]
}
```

### 5.3 Set némésis d'un héros

```json
{
    "version": "0.5.8",
    "name": "Adam Warlock Nemesis",
    "encounters": [
        "21067",
        "21068",
        "21069",
        "21069",
        "21070"
    ]
}
```

### 5.4 Déclaration du pack (`sets_info.json`)

Le pack déclare ses scénarios (ids des fichiers de scénario), ses héros, ses
sets de rencontre modulaires et le plus grand identifiant. Exemple réel du
pack fan-made Web of Deceit :

```json
"120. Custom (Web of Deceit)": {"name": "web_of_deceit", "scenarios": ["wd_shocker", "wd_electro", "wd_the_lizard", "wd_vulture", "wd_kingpin", "wd_vulture_underling"], "heroes": [], "encounters": [], "max_id": "wd165"}
```

Et le pack officiel Core Set :

```json
"1. Core Set": {"name": "core", "scenarios": ["rhino", "klaw", "ultron"], "heroes": ["spider_man", "captain_marvel", "she_hulk", "iron_man", "black_panther"], "encounters": ["bomb_scare", "masters_of_evil", "under_attack", "legions_of_hydra", "the_doomsday_chair", "standard", "expert"], "max_id": "01193"}
```

Le numéro devant le nom du pack est attribué par Claude : donne seulement le
nom.

### 5.5 Deck de départ d'un héros (pour mémoire)

```json
{
    "version": "0.5.8",
    "name": "Spider-Man",
    "metadata": {
        "url": ""
    },
    "hero": [
        "01001a,01001b"
    ],
    "hero_deck": [
        "01002",
        "01003",
        "01003",
        "01004",
        "01004",
        "01005",
        "01005",
        "01005",
        "01006",
        "01007",
        "01007",
        "01008",
        "01008",
        "01009",
        "01009"
    ],
    "set_aside": [],
    "obligations": [
        "01165"
    ],
    "nemesis_set": [
        "01166",
        "01167",
        "01168",
        "01168",
        "01169"
    ],
    "player_deck": [
        "01058",
        "01059",
        "01060",
        "01060",
        "01061",
        "01061",
        "01062",
        "01062",
        "01063",
        "01063",
        "01064",
        "01064",
        "01065",
        "01065",
        "01083",
        "01084",
        "01085",
        "01086",
        "01087",
        "01088",
        "01089",
        "01090",
        "01091",
        "01092",
        "01093"
    ]
}
```

---

## 6. Campagnes

Une campagne, ce sont **trois choses** :

1. **Les scénarios** (section 5), un fichier par scénario.
2. **La description pour l'écran des campagnes** : `data/campagnes/<code>.json`.
   C'est elle qui dit l'ordre des scénarios, ce qu'on note au carnet après
   chaque partie, et les textes affichés aux joueurs.
3. **La logique de campagne** : `src/cards/pack/<pack>/campaign.py`. C'est
   elle qui, **à la mise en place** d'un scénario, relit le carnet et
   applique ses conséquences (mettre une carte en jeu, en mélanger une au
   deck rencontre, retirer des cartes...), et qui, **à la fin de la partie**,
   écrit les clés du carnet.

### 6.1 Le carnet de campagne

Le carnet est un dictionnaire **clé texte → valeur texte**. Les valeurs sont
des chaînes : `"1"` pour une case cochée, un nombre en texte, ou une liste
séparée par des `;`. Une clé **par joueur** s'écrit `"Player 1 <clé>"`
(joueurs 1 à 4).

Lecture dans le code :

| Fonction | Rend |
|---|---|
| `CampaignLog.GetStrInternal(cle, effect)` | la chaîne, `''` si absente |
| `CampaignLog.GetIntInternal(cle, effect)` | un entier, 0 si absente |
| `CampaignLog.GetListInternal(cle, effect)` | une liste (valeur coupée sur `;`) |
| `CampaignLog.GetStrByPlayer(cle, player_id, effect)` | la valeur d'un joueur |
| `CampaignLog.GetListByPlayer(cle, player_id, effect)` | la liste d'un joueur |

### 6.2 Format de `data/campagnes/<code>.json`

Exemple complet et réel (campagne officielle The Mad Titan's Shadow) :

```json
{
  "version": "1.0",
  "code": "mts",
  "cle_extension": "21. The Mad Titan's Shadow",
  "nom": "L'Ombre du Titan Fou",
  "nom_en": "The Mad Titan's Shadow",
  "resume": "Thanos cherche les Pierres d'Infinité, et chaque victoire vous laisse un allié, une dette ou une cicatrice que le scénario suivant vous réclamera.",
  "resume_en": "Thanos hunts the Infinity Stones, and every victory leaves behind an ally, a debt or a scar the next scenario will come to collect.",
  "expert": {
    "pv_persistants": true
  },
  "scenarios": [
    {
      "id": "ebony_maw",
      "numero": 1,
      "nom": "Ebony Maw",
      "nom_fr": "Ebony Maw",
      "resume": "L'émissaire de Thanos s'infiltre dans la Tour des Vengeurs et y retourne vos propres défenses. Rien n'explose, rien ne hurle : il se contente de parler, et les portes s'ouvrent.",
      "enjeu": "Ce que Maw laisse derrière lui vous suit. Une brèche de sécurité non refermée reviendra hanter le deck de rencontre du scénario suivant ; Cosmo, s'il est encore là, se battra à vos côtés.",
      "victoire": [
        {
          "cle": "Campaign Pool: Cosmo",
          "type": "auto",
          "format": "int",
          "libelle": "Cosmo rallié",
          "aide": "Cosmo entre en jeu sous votre contrôle au scénario 3 s'il est noté ici."
        },
        {
          "cle": "Campaign Pool: Security Breach",
          "type": "auto",
          "format": "int",
          "libelle": "Brèche de sécurité laissée ouverte",
          "aide": "La carte Security Breach sera mélangée au deck de rencontre des scénarios suivants."
        }
      ],
      "pages": {
        "intro": [
          "01-ebony_maw-intro-1.jpg"
        ],
        "regles": [
          "01-ebony_maw-regles-1.jpg",
          "01-ebony_maw-regles-2.jpg"
        ],
        "epilogue": [
          "01-ebony_maw-epilogue-1.jpg"
        ]
      }
    },
    {
      "id": "the_tower_defense",
      "numero": 2,
      "nom": "Tower Defense",
      "nom_fr": "La Défense de la Tour",
      "resume": "Proxima Midnight et Corvus Glaive attaquent la Tour ensemble. Deux vilains, un seul bâtiment, et personne pour vous relever.",
      "enjeu": "La Tour peut sortir debout ou éventrée de cette nuit. Ce qu'elle perd ici, aucun scénario suivant ne le lui rendra.",
      "victoire": [
        {
          "cle": "Campaign Pool: Shawarma",
          "type": "auto",
          "format": "int",
          "libelle": "Shawarma partagé",
          "aide": "Chaque joueur mélangera une copie de Shawarma dans son deck aux scénarios suivants."
        },
        {
          "cle": "Campaign Pool: Black Swan",
          "type": "auto",
          "format": "int",
          "libelle": "Black Swan en fuite",
          "aide": "Non vaincue, elle revient en jeu au scénario 3."
        },
        {
          "cle": "Avengers Tower Damaged",
          "type": "auto",
          "format": "int",
          "libelle": "Tour des Vengeurs endommagée",
          "aide": "Pénalité appliquée à la mise en place des scénarios suivants."
        }
      ],
      "pages": {
        "intro": [
          "02-the_tower_defense-intro-1.jpg"
        ],
        "regles": [
          "02-the_tower_defense-regles-1.jpg",
          "02-the_tower_defense-regles-2.jpg",
          "02-the_tower_defense-regles-3.jpg",
          "02-the_tower_defense-regles-4.jpg"
        ],
        "epilogue": [
          "02-the_tower_defense-epilogue-1.jpg"
        ]
      }
    },
    {
      "id": "thanos",
      "numero": 3,
      "nom": "Thanos",
      "nom_fr": "Thanos",
      "resume": "Le Titan descend lui-même. Il ne vient pas gagner, il vient prendre, et il a déjà compté combien de temps cela lui prendrait.",
      "enjeu": "Ce que Thanos emporte des Pierres d'Infinité décide de la puissance qu'il aura contre Hela, puis contre Loki.",
      "victoire": [
        {
          "cle": "Campaign Pool: System Shock",
          "type": "auto",
          "format": "int",
          "libelle": "Choc systémique subi",
          "aide": "Chaque joueur mélangera une copie de System Shock dans son deck aux scénarios suivants."
        },
        {
          "cle": "The Infinity Stones 1B completed",
          "type": "auto",
          "format": "int",
          "libelle": "Les Pierres d'Infinité rassemblées par Thanos",
          "aide": "Pénalité appliquée à la mise en place des scénarios 4 et 5."
        }
      ],
      "pages": {
        "intro": [
          "03-thanos-intro-1.jpg"
        ],
        "regles": [
          "03-thanos-regles-1.jpg",
          "03-thanos-regles-2.jpg"
        ],
        "epilogue": [
          "03-thanos-epilogue-1.jpg"
        ]
      }
    },
    {
      "id": "hela",
      "numero": 4,
      "nom": "Hela",
      "nom_fr": "Hela",
      "resume": "Le royaume des morts n'est plus un lieu de passage. Hela y retient Odin, et Garm garde la porte que vous devrez franchir dans les deux sens.",
      "enjeu": "Odin délivré vous suivra jusqu'à Asgard. Laissé derrière, il n'y sera pas.",
      "victoire": [
        {
          "cle": "Campaign Pool: Norn Stone",
          "type": "auto",
          "format": "int",
          "libelle": "Pierre de Norn récupérée",
          "aide": "Chaque joueur en reçoit une copie au scénario 5."
        },
        {
          "cle": "Campaign Pool: Odin",
          "type": "auto",
          "format": "int",
          "libelle": "Odin délivré",
          "aide": "Odin entre en jeu sous votre contrôle au scénario 5 s'il est noté ici."
        }
      ],
      "pages": {
        "intro": [
          "04-hela-intro-1.jpg"
        ],
        "regles": [
          "04-hela-regles-1.jpg",
          "04-hela-regles-2.jpg"
        ],
        "epilogue": [
          "04-hela-epilogue-1.jpg"
        ]
      }
    },
    {
      "id": "loki",
      "numero": 5,
      "nom": "Loki",
      "nom_fr": "Loki",
      "resume": "Loki règne sur Asgard et rien de ce que vous voyez n'est sûr d'exister. La campagne se termine ici, avec tout ce que vous y avez traîné.",
      "enjeu": "Rien à reporter : c'est le dernier scénario.",
      "final": true,
      "defaite": {"quand": "partie_perdue", "expert_seulement": true, "texte": "Loki étend son règne sur tout l'univers : la campagne est perdue."},
      "victoire": [],
      "pages": {
        "intro": [
          "05-loki-intro-1.jpg"
        ],
        "regles": [
          "05-loki-regles-1.jpg",
          "05-loki-regles-2.jpg"
        ],
        "epilogue": [
          "05-loki-epilogue-1.jpg"
        ]
      }
    }
  ],
  "victoire_commune_expert": [
    {
      "cle": "Remaining hit points",
      "parJoueur": true,
      "type": "auto",
      "format": "int",
      "detection": "pv_restants",
      "libelle": "Points de vie restants",
      "aide": "En campagne experte, vous reprenez le scénario suivant avec ces points de vie."
    }
  ],
  "pages_regles": [
    "00-campagne-regles-1.jpg"
  ]
}
```

Clés :

| Clé | Sens |
|---|---|
| `version` | `"1.0"` |
| `code` | le code de la campagne (= nom du pack) |
| `cle_extension` | la clé du pack dans `sets_info.json` (attribuée par Claude : laisse `"A_FAIRE_CLAUDE"`) |
| `nom`, `nom_en` | nom en français et en anglais |
| `resume`, `resume_en` | deux phrases pour présenter la campagne |
| `expert.pv_persistants` | `true` si, en campagne experte, les PV se reportent d'un scénario à l'autre |
| `pages_regles` | images du livret (laisse `[]`, Claude les ajoute) |
| `scenarios[]` | un objet par scénario, dans l'ordre |
| `victoire_commune_expert` | clés notées après CHAQUE scénario en expert (les PV restants, tel quel) |

Un scénario :

| Clé | Sens |
|---|---|
| `id` | id du fichier de scénario (`ebony_maw`) |
| `numero` | 1, 2, 3... |
| `nom`, `nom_fr` | nom anglais, nom français |
| `resume` | ce qui se passe, deux phrases, pour un joueur |
| `enjeu` | ce que ce scénario change pour la suite, une phrase |
| `victoire[]` | les clés du carnet notées après ce scénario |
| `pages` | images (laisse `{}`) |
| `final` | `true` sur le dernier scénario |
| `defaite` | facultatif : `{"quand": "partie_perdue", "expert_seulement": true, "texte": "..."}` |

Une clé de `victoire` :

| Clé | Sens |
|---|---|
| `cle` | le nom exact de la clé au carnet (identique dans `campaign.py`) |
| `type` | `"auto"` (calculée par `campaign.py` en fin de partie) ou `"choix"` (le joueur choisit dans `options`) |
| `format` | `"int"` (case / nombre) ou `"liste"` |
| `parJoueur` | `true` si chaque joueur a sa valeur |
| `libelle` | intitulé court affiché |
| `aide` | une phrase : à quoi sert cette clé plus tard |
| `options` | pour `"choix"` : les `card_id` proposés |
| `obligatoire` | pour `"choix"` : `true` si le joueur doit choisir |

Exemple réel d'une clé à choix (campagne fan-made Web of Deceit) :

```json
{
    "cle": "Talent Tier 1",
    "parJoueur": true,
    "type": "choix",
    "obligatoire": true,
    "libelle": "Arbre de talents — palier 1",
    "aide": "Chaque joueur prend une carte du palier 1 de SON arbre de talents. [...]",
    "options": ["wd113", "wd114", "wd123", "wd124", "wd133", "wd134", "wd143", "wd144", "wd153", "wd154"]
}
```

D'autres clés existent (`detection`, `tirage`, `cumulatif`, `marche`,
`enquete`...) : ne les utilise pas. Si une campagne en a besoin, décris le
besoin en `A_FAIRE_CLAUDE`.

### 6.3 `campaign.py` : la mise en place

Les capacités de campagne se posent sur **la face 1A du complot principal**
de chaque scénario (la face qui sert à la mise en place). Le complot appelle
une fonction du `campaign.py` du pack avec le niveau du scénario.

Côté complot (scénario 1 de The Mad Titan's Shadow) :

```python
# Source : src/cards/pack/mts/ebony_maw/21074a.py
from . import *
from cards.pack.mts.campaign import CampaignSetup
def GetAbilities() -> Sequence['Ability']:
    return [*CampaignSetup(1)]
```

Côté complot fan-made, avec sa propre mise en place en plus :

```python
# Source : src/cards/pack/web_of_deceit/shocker/wd002a.py
from . import *
from cards.pack.web_of_deceit.campaign import ChaqueJoueurRetrouveSesTalents

# Shock Party (1A)

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        # « Setup: Search the encounter deck for The Long Night side scheme and
        # reveal it. Remove each obligation card in the encounter deck from the
        # game. »
        ChercherEtReveler(effect, name="The Long Night")

        obligations = CardFinder(card_type=Obligation).Checks(
            Worlds.GetEncounterDeckCards(effect))
        if obligations:
            Faces.RemoveAllFromGame(obligations, effect)

        # Regle commune a TOUS les scenarios de la campagne (livret p.3) :
        # « Put the "Vote for Fisk" environment into play. » La face experte est
        # une carte a part, pas un dos : c'est ici qu'on choisit.
        MettreVoteForFiskEnJeu(effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place
        ),
        # Les paliers d'arbre de talents deja gagnes reviennent dans le
        # deck de leur proprietaire (voir `campaign.py`).
        ChaqueJoueurRetrouveSesTalents(),
    ]
```

Fabriques de campagne disponibles (toutes dans `AbilityFactoryCampaign`) :

| Fabrique | Effet |
|---|---|
| `WhenCampaignSetup(action, conditions=[...])` | `action(effect, message)` à la mise en place, en campagne seulement |
| `WhenCampaignSetupExpertOnly(action)` | idem, en campagne experte seulement |
| `ExpertCampaignSetPlayersHPToTheirRemainingHP()` | en expert, chaque joueur reprend ses PV notés |
| `ExpertCampaignAddRandomObligationFromExpertCampaignToHealHP([ids])` | en expert, ajouter une obligation au hasard pour se soigner |
| `ShuffleCardIntoDeck(card_id, 'EncounterDeck')` | mélanger une carte au deck rencontre |

Fabriquer une carte qui n'est dans aucun deck : `CardFactory.GenerateCard(id,
zone, effect.world)` (zone `None` = hors jeu, à mettre en jeu ensuite), ou
`CardFactory.GenerateCards([ids], player.player_deck, effect.world)`.

**Exemple complet et réel, court : campagne fan-made Web of Deceit**

```python
# Source : src/cards/pack/web_of_deceit/campaign.py
from . import *

# LE CARNET DE LA CAMPAGNE « WEB OF DECEIT »
#
# La voie a ete tranchee au §15 de la fiche : les arbres de talents passent par
# le carnet, qui sait deja poser des cartes IMPOSEES dans le deck d'un joueur
# entre deux scenarios. Un palier d'arbre est exactement cela — « ces cartes
# restent avec le joueur pour le reste de la campagne et DOIVENT figurer dans
# son deck » (livret p.2).
#
# ⚠ CE QUE CETTE VOIE NE REND PAS : l'arbre ne s'affiche pas comme un arbre. Le
# joueur voit, entre deux rencontres, la liste des cartes de son palier — les
# cinq arbres melanges, puisque le carnet ne retient pas lequel il a choisi.
# La progression est fidele, sa mise en scene ne l'est pas.

PALIERS = ("Talent Tier 0", "Talent Tier 1", "Talent Tier 2",
           "Talent Tier 3", "Talent Tier 4")


def ChaqueJoueurRetrouveSesTalents() -> 'Ability':
    """Remet dans le deck de chaque joueur les cartes de talent deja gagnees.

    Le carnet enregistre un choix par palier et par joueur (`parJoueur`), sous
    les cles listees ci-dessus. A chaque mise en place de campagne, on les relit
    et on genere les cartes dans le deck de leur proprietaire : le deck grossit
    d'une carte par scenario gagne, ce que le livret demande.
    """
    from game.operate.worlds import Worlds
    from game.operate.campaign_logs import CampaignLog
    from game.card.factory import CardFactory

    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        for player in Worlds.GetPlayers(effect):
            gagnees = []
            for cle in PALIERS:
                card_id = CampaignLog.GetStrByPlayer(cle, player.player_id, effect)
                if card_id:
                    gagnees.append(card_id)
            if gagnees:
                CardFactory.GenerateCards(gagnees, player.player_deck, effect.world)
                player.player_deck.Shuffle(effect)

    return AbilityFactoryCampaign.WhenCampaignSetup(
        action,
    )
```

**Exemple complet et réel : campagne officielle The Rise of Red Skull**

```python
# Source : src/cards/pack/trors/campaign.py
from . import *

def ShuffleEachExperimentalAttachmentIntoTheEncounterDeck() -> 'Ability':
    from game.operate.worlds import Worlds
    from game.operate.campaign_logs import CampaignLog
    from game.card.factory import CardFactory
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        card_ids = CampaignLog.GetList("Experimental Weapons added to encounter deck", effect)
        encounter_deck = Worlds.GetEncounterDeck(effect)
        CardFactory.GenerateCards(card_ids, encounter_deck, effect.world)
        encounter_deck.Shuffle(effect)

    return AbilityFactoryCampaign.WhenCampaignSetup(
        action,
    )

def EachPlayerSearchTheirDeckForSetupKeyword() -> 'Ability':
    from game.operate.worlds import Worlds
    from game.operate.campaign_logs import CampaignLog
    from game.card.factory import CardFactory
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            player_id = player.player_id
            card_id = CampaignLog.GetStrByPlayer("Tech Upgrade", player_id, effect)
            if card_id:
                card = CardFactory.GenerateCard(card_id, player.player_deck, effect.world)
                card.face.PutIntoPlay(player, effect)

        for player in Worlds.GetPlayers(effect):
            player_id = player.player_id
            card_id = CampaignLog.GetStrByPlayer("Basic Upgrade", player_id, effect)
            if card_id:
                card = CardFactory.GenerateCard(card_id, player.player_deck, effect.world)
                card.face.PutIntoPlay(player, effect)

    return AbilityFactoryCampaign.WhenCampaignSetup(
        action,
    )

def EachPlayerAddRescuedAlliesToTheirDeck() -> 'Ability':
    from game.operate.worlds import Worlds
    from game.operate.campaign_logs import CampaignLog
    from game.card.factory import CardFactory
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            player_id = player.player_id
            card_ids = CampaignLog.GetListByPlayer("Rescued Allies", player_id, effect)
            if card_ids:
                CardFactory.GenerateCards(card_ids, player.player_deck, effect.world)
                player.player_deck.Shuffle(effect)

    return AbilityFactoryCampaign.WhenCampaignSetup(
        action,
    )

def EachPlayerMayAddRandomObligationToHealHP() -> 'Ability':
    return AbilityFactoryCampaign.ExpertCampaignAddRandomObligationFromExpertCampaignToHealHP(
        ["04163", "04164", "04165", "04166"]
    )


def CampaignSetup(level: int, *,
                campaigns: List[Callable[[Effect, Message.WhenCampaignSetup], None]]=[],
                campaigns_expert: List[Callable[[Effect, Message.WhenCampaignSetup], None]]=[]) -> List['Ability']:

    abilities: List[Ability] = []

    if level >= 2:
        abilities.append(
            EachPlayerSearchTheirDeckForSetupKeyword(),
        )
        abilities.append(
            ShuffleEachExperimentalAttachmentIntoTheEncounterDeck(),
        )

    if level >= 4:
        abilities.append(
            EachPlayerAddRescuedAlliesToTheirDeck(),
        )

    for campaign in campaigns:
        abilities.append(
            AbilityFactoryCampaign.WhenCampaignSetup(campaign),
        )

    if level >= 2:
        abilities.append(
            AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP(),
        )
        abilities.append(
            EachPlayerMayAddRandomObligationToHealHP()
        )

    for campaign in campaigns_expert:
        abilities.append(
            AbilityFactoryCampaign.WhenCampaignSetupExpertOnly(campaign),
        )

    return abilities
```

### 6.4 `campaign.py` : écrire le carnet en fin de partie

La fin de partie s'écrit avec `WriteCampaignLogAtGameOver(collect)`, défini
dans le pack `mts` et réutilisable (`from cards.pack.mts.campaign import
WriteCampaignLogAtGameOver`). `collect(effect, message)` rend un dictionnaire
`{clé: valeur}` des clés à écrire. Le résultat de la partie se lit
**sur le message** : `message.players_won`.

Exemple réel complet (campagne officielle The Mad Titan's Shadow) : mise en
place par niveau, relevé du carnet par niveau, et branchement final.

```python
# Source : src/cards/pack/mts/campaign.py (lignes 1 à 61)
from . import *
import re
def InPool(name: str):
    def check(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> bool:
        return (CampaignLog.GetStrInternal(f'Campaign Pool: {name}', effect) != '')
    return check
def LogSet(name: str):
    def check(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> bool:
        return (CampaignLog.GetStrInternal(name, effect) != '')
    return check
def PutSideSchemeIntoPlay(card_id: str) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        card = CardFactory.GenerateCard(card_id, None, effect.world)
        card.face.PutIntoPlay('FirstPlayer', effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def PutIntoPlayIfPool(card_id: str, pool_name: str, *, under_control: bool = False) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        card = CardFactory.GenerateCard(card_id, None, effect.world)
        card.face.PutIntoPlay('FirstPlayer', effect, under_control=under_control)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[InPool(pool_name)])
def ShuffleIntoEncounterIfPool(card_id: str, pool_name: str) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        card = CardFactory.GenerateCard(card_id, None, effect.world)
        Faces.ShuffleAllTo([card.face], 'EncounterDeck', effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[InPool(pool_name)])
def EachPlayerShufflesCopyIfPool(card_id: str, pool_name: str) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            card = CardFactory.GenerateCard(card_id, player.player_deck, effect.world)
            Faces.ShuffleAllTo([card.face], player.player_deck, effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[InPool(pool_name)])
def EachPlayerNornStoneIfPool() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            card = CardFactory.GenerateCard('21187a,21187b', None, effect.world)
            card.SetOwner(player)
            card.face.CastTo(Upgrade).AttachTo2(player.GetIdentity(), effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[InPool('Norn Stone')])
def AvengersTowerDamagedPenalty() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            identity = player.GetIdentity()
            identity.CastTo(Unit2).TakeDamage(effect.this, 3, effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[LogSet('Avengers Tower Damaged')])
def InfinityStonesCompletedPenalty() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            half = (player.player_deck.GetSize() // 2)
            if (half > 0):
                Faces.DiscardAll(player.player_deck.GetTops(half), effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[LogSet('The Infinity Stones 1B completed')])
def ExpertMayPlaceAccelerationToHeal() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        this = effect.this.CastTo(MainScheme)
        for player in Worlds.GetPlayers(effect):
            identity = player.GetIdentity()
            def heal(targets: Sequence['CardFace']):
                this.PlaceTokensInternal(1, 'acceleration_token', effect)
                identity.CastTo(CanHealth).HealHealth('All', effect)
            player.MayChooseOneAbility(effect, AbilityFactory.ForChoiceAbility('Place 1 acceleration token on the main scheme to heal to full', heal))
    return AbilityFactoryCampaign.WhenCampaignSetupExpertOnly(action)
```

```python
# Source : src/cards/pack/mts/campaign.py (lignes 172 à 233)
def CollectMTS(level: int, effect: 'Effect') -> dict:
    updates = {}
    if (level == 1):
        if FaceExists(effect, '21180b', in_play=True):
            updates['Campaign Pool: Cosmo'] = '1'
        if ActiveMainSchemeStartswith(effect, '21075'):
            updates['Campaign Pool: Security Breach'] = '1'
    if (level == 2):
        if FaceExists(effect, '21182b'):
            updates['Campaign Pool: Shawarma'] = '1'
            if not FaceExists(effect, '21182b', in_victory=True):
                updates['Campaign Pool: Black Swan'] = '1'
        if FaceExists(effect, '21100b', in_play=True):
            updates['Avengers Tower Damaged'] = '1'
    if (level == 3):
        if not FaceExists(effect, '21184b', in_victory=True):
            updates['Campaign Pool: System Shock'] = '1'
        if ActiveMainSchemeStartswith(effect, '21115'):
            updates['The Infinity Stones 1B completed'] = '1'
    if (level == 4):
        if FaceExists(effect, '21186b'):
            updates['Campaign Pool: Norn Stone'] = '1'
        if FaceExists(effect, '21186b', in_victory=True):
            updates['Campaign Pool: Odin'] = '1'
    return updates
def CampaignSetup(level: int) -> List['Ability']:
    abilities = []
    if (level == 1):
        abilities.append(PutSideSchemeIntoPlay('21180a'))
        def shuffle_breach(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
            card = CardFactory.GenerateCard('21181', None, effect.world)
            Faces.ShuffleAllTo([card.face], 'EncounterDeck', effect)
        abilities.append(AbilityFactoryCampaign.WhenCampaignSetup(shuffle_breach))
    if (level == 2):
        abilities.append(PutSideSchemeIntoPlay('21182a'))
        abilities.append(ShuffleIntoEncounterIfPool('21181', 'Security Breach'))
    if (level == 3):
        abilities.append(PutSideSchemeIntoPlay('21184a'))
        abilities.append(PutIntoPlayIfPool('21180b', 'Cosmo', under_control=True))
        abilities.append(ShuffleIntoEncounterIfPool('21181', 'Security Breach'))
        abilities.append(EachPlayerShufflesCopyIfPool('21183', 'Shawarma'))
        abilities.append(PutIntoPlayIfPool('21182b', 'Black Swan'))
        abilities.append(AvengersTowerDamagedPenalty())
    if (level == 4):
        abilities.append(PutSideSchemeIntoPlay('21186a'))
        abilities.append(AbilityFactoryCampaign.ShuffleCardIntoDeck('21188', 'EncounterDeck'))
        abilities.append(EachPlayerShufflesCopyIfPool('21183', 'Shawarma'))
        abilities.append(EachPlayerShufflesCopyIfPool('21185', 'System Shock'))
        abilities.append(InfinityStonesCompletedPenalty())
    if (level == 5):
        abilities.append(PutSideSchemeIntoPlay('21189a'))
        abilities.append(AbilityFactoryCampaign.ShuffleCardIntoDeck('21188', 'EncounterDeck'))
        abilities.append(EachPlayerShufflesCopyIfPool('21183', 'Shawarma'))
        abilities.append(EachPlayerShufflesCopyIfPool('21185', 'System Shock'))
        abilities.append(InfinityStonesCompletedPenalty())
        abilities.append(EachPlayerNornStoneIfPool())
        abilities.append(PutIntoPlayIfPool('21139b,21139a', 'Odin', under_control=True))
    if (level >= 2):
        abilities.append(AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP())
        abilities.append(ExpertMayPlaceAccelerationToHeal())
    abilities.append(WriteCampaignLogAtGameOver(lambda effect, message: CollectMTS(level, effect)))
    return abilities
```

Et un relevé plus riche (campagne officielle Fear No Evil), qui montre comment
lire la pile de victoire et les cartes retirées de la partie :

```python
# Source : src/cards/pack/fne/campaign.py (lignes 169 à 247)
def _partie_gagnee(message: 'Message.WhenGameOver') -> bool:
    """Le resultat vient du MESSAGE, pas du monde.

    ⚠ `GameOver.SetGameOver` envoie `WhenGameOver` PUIS pose `players_won` sur
    le monde : pendant le message, `world.game_over` dit encore « perdue ».
    La version precedente lisait le monde, donc « Completed Scenarios » n'etait
    JAMAIS ecrit, meme sur une victoire. Personne ne l'avait vu parce que rien
    ne jouait la fin d'une partie (trouve le 19/09/2026 par
    `tools/test_campagnes.py`).
    """
    return bool(getattr(message, "players_won", False))


def CollectFNE(manigance: 'str|None', effect: 'Effect', message: 'Message.WhenGameOver') -> dict:
    """Le carnet sortant, releve a la fin de la partie (VICTORY du livret) :
    l'affaire gagnee rejoint « Completed Scenarios » ; « Trust Established? »
    si Disturbed Psyche a au moins 2 jetons menace ; « Mary Defeated? » si
    l'alliee est dans la pile de victoire ; les allies et soutiens UNIQUES
    retires du jeu s'ajoutent a « Allies removed from the campaign »."""
    updates = {}
    gagnee = _partie_gagnee(message)
    if manigance and gagnee:
        faits = Completed(effect)
        if manigance not in faits:
            updates[CLE_COMPLETED] = ";".join(faits + [manigance])
    if gagnee:
        psyche = Worlds.FindCardOnField(effect, name="Disturbed Psyche", card_type=Environment)
        if psyche is not None and psyche.GetTokens('threat') >= 2:
            updates[CLE_TRUST] = "1"
    for card in effect.world.object_manager.card_dict.values():
        face = card.face
        if face is not None and face.paper.card_id in ("60210a", "60210b") and card.area.flags.is_victory_display:
            updates[CLE_MARY] = "1"
    retirees = list(Retirees(effect))
    for face in effect.world.area_removed.Get(True):
        # ⚠ `paper.name` n'a PLUS l'etoile a l'execution (paper.py:45 la
        # retire et pose `is_unique`) : tester le drapeau, pas le prefixe
        # (cas « Carnet sortant » rouge le 18/09/2026, Black Cat non relevee).
        if (Ally.IsType(face) or Support.IsType(face)) and face.paper.is_unique:
            proprietaire = face.GetOwner()
            if Player.IsType(proprietaire):
                titre = face.paper.name.lstrip('* ')
                if titre not in retirees:
                    retirees.append(titre)
    if retirees and retirees != list(Retirees(effect)):
        updates[CLE_RETIREES] = ";".join(retirees)
    return updates


def CapacitesDeCampagne(manigance: str, garde=None) -> List['Ability']:
    """A poser sur la face 1A de chaque manigance interchangeable.

    `garde(effect, message) -> bool` : condition supplementaire sur les
    capacites de mise en place. Protection Racket a UN complot principal PAR
    JOUEUR (cinq copies de 60134a-60138a) : sans garde, chaque copie
    remettrait les environnements, Mary Walker et les marques de l'affaire
    (Mary entrerait N fois). La garde ne laisse parler que le premier complot
    en jeu ; le carnet de fin de partie, lui, est idempotent."""
    conditions = [garde] if garde else []
    return [
        MettreLesEnvironnements(conditions),
        RetirerLesCartesRetirees(conditions),
        MarquesDeLAffaire(manigance, conditions),
        MaryWalker(conditions),
        AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP(),
        WriteCampaignLogAtGameOver(lambda effect, message: CollectFNE(manigance, effect, message)),
    ]


def CapacitesDeCampagneKingpin() -> List['Ability']:
    """A poser sur The King's Gambit 1A (60161a)."""
    return [
        MettreLesEnvironnements(),
        RetirerLesCartesRetirees(),
        MarquesKingpin(),
        MaryWalker(),
        AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP(),
        WriteCampaignLogAtGameOver(lambda effect, message: CollectFNE(None, effect, message)),
    ]
```

### 6.5 Ce que tu livres pour une campagne

- Un fichier par scénario (standard ET expert), ses sets de rencontre.
- `data/campagnes/<code>.json` complet.
- `campaign.py` : une fonction `CampaignSetup(niveau)` qui rend la liste des
  capacités de chaque scénario, une fonction `Collect<Code>(niveau, effect)`
  qui rend les clés du carnet, et le branchement
  `WriteCampaignLogAtGameOver(...)`.
- Sur la face 1A du complot de chaque scénario : `*CampaignSetup(n)`.
- Une table qui relie **chaque clé** de `data/campagnes/<code>.json` à la
  ligne de `campaign.py` qui l'écrit (type `auto`) et à celle qui la lit à la
  mise en place. Une clé écrite et jamais lue, ou lue et jamais écrite, est
  une erreur.

---

## 7. Écrire le script d'une carte

### 7.1 Squelette

```python
from . import *

# <Nom de la carte>

def GetAbilities() -> Sequence['Ability']:

    def mon_effet(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        player = message.GetToPlayer()
        ...

    return [
        AbilityFactory.WhenThisRevealed(None, mon_effet),
    ]
```

- Toujours `from . import *` comme première instruction (les lignes « # Source : » des exemples sont des commentaires ajoutés pour ce document, ne les recopie pas).
- Une fonction `GetAbilities()` qui **rend une liste** de capacités.
- Chaque capacité est fabriquée par `AbilityFactory.<Fabrique>(...)`.
- L'opération reçoit `(effect, message)`.
  - `effect.this` : la carte qui porte la capacité ; commence par
    `.CastTo(<Type>)`.
  - `effect.targets` : les cibles choisies via `.SetTarget(...)`.
  - `effect.GetInitiator()` : le joueur qui résout.
  - `message` : dépend du déclencheur (exemples en section 8).
- Une fabrique dont le nom commence par `*` dans les exemples
  (`*AbilityFactory.GiveKeywordToAttached(...)`) rend une **liste** : il faut
  l'étoile pour la déplier dans la liste finale.

### 7.2 Types de capacité (`AbilityType`)

Valeurs réelles : `Action`, `HeroAction`, `AlterEgoAction`, `ForcedAction`,
`FirstPlayerAction`, `Interrupt`, `HeroInterrupt`, `AlterEgoInterrupt`,
`ForcedInterrupt`, `FirstPlayerInterrupt`, `Response`, `HeroResponse`,
`AlterEgoResponse`, `ForcedResponse`, `Resource`, `HeroResource`,
`AlterEgoResource`, `WhenRevealed`, `WhenDefeated`, `WhenCompleted`, `Boost`,
`Setup`, `Special`, `NonKeyword`, `NonKeywordStar` (capacité `[star]`
permanente).

Le mot imprimé en gras décide du type : « **Forced Response** » →
`ForcedResponse`, « **Hero Action** » → `HeroAction`. Ne remplace jamais un
« Forced » par sa version facultative, ni l'inverse.

### 7.3 Les fabriques (signatures réelles)

Déclencheurs du joueur et de ses cartes :

| Texte imprimé | Fabrique |
|---|---|
| Action / Hero Action / Alter-Ego Action (carte en jeu ou événement) | `WhenInYourPlayTurn(ability_type, operation, *, conditions=[])` |
| Jouer un événement | la même, suivie de `.SetPlay()` |
| After X enters play | `AfterCardEnterPlay(ability_type, which_card, operation, *, under_your_control=None, conditions=[])` |
| After you play X | `AfterPlayerPlayedCard(ability_type, which_player, which_card, operation, *, from_hand=False, conditions=[])` |
| When you play X | `WhenPlayerPlayCard(ability_type, which_player, played_card, operation, *, label=None, targets=None, using_res=None, conditions=[])` |
| After X attacks | `AfterUnitAttackEnd(ability_type, attacker, operation, *, is_basic_attack=None, damaged_who=None, against_who=None, conditions=[], would_atk_message=None)` |
| After X attacks and damages Y | `AfterUnitAttackAndDamageUnit(ability_type, attacker, who_be_attacked, operation, *, target_in_play=None, use_atk=None, dealt_more_than_damage=None, conditions=[])` |
| After X defeats Y | `AfterUnitDefeatedUnit(ability_type, who_killer, who_be_defeated, operation, *, is_from_attack=None, is_basic_attack=None, has_excess_damage=None, conditions=[])` |
| When X would take damage | `WhenUnitWouldTakeDamage(ability_type, who_take_damage, operation, *, is_from_attack=None, is_consequential_damage=None, while_defending=None, control_by=None, who_deal_damage=None, at_least_damage=1, more_than_damage=0, not_include_this_effect=None, conditions=[])` |
| When the villain initiates an attack against you | `WhenUnitInitiatesAttackAgainst(ability_type, attacker, against_player, operation, conditions=[])` |
| When an encounter card is revealed | `WhenPlayerRevealCard(ability_type, which_player, which_card, can_be_cancel, operation, *, from_encounter=None, conditions=[])` |
| Begin / end of your turn | `WhenPlayerTurnBegin(ability_type, which_player, operation, *, conditions=[])`, `WhenPlayerTurnEnd(...)` |
| End of a phase | `WhenPhaseEnd(ability_type, phase_name, operation, *, conditions=[])` |
| End of the round | `AfterRoundEnd(ability_type, operation, *, conditions=[])`, `DiscardThisWhenRoundEnd(ability_type, *, conditions=[])` |
| After a status card is placed | `AfterStatusCardPlaceOn(ability_type, place_on_who, status, operation, *, conditions=[])` |
| Obligation « Give to the X player » | `WhenThisObligationGiveToYou(operation)` |

Déclencheurs des cartes de rencontre :

| Texte imprimé | Fabrique |
|---|---|
| When Revealed | `WhenThisRevealed(condition, operation)` ; `condition` = `None`, `"Hero"` ou `"Alter-Ego"` |
| [star] Boost: ... | `WhenCardBecomeBoost(which_card, operation, *, during_scheme=False, during_attack=False, is_undefended_attack=None, attacker=None, activating_enemy=None, you_are_in_hero_from=None, conditions=[])` |
| [star] Boost: If this activation deals damage to ... | `BoostIfThisActivationDealsDamage(to_who, operation)` |
| When X attacks / would attack | `WhenUnitWouldAttack(ability_type, attacker, operation, *, against_player='AnyPlayer', attack_targets=None, is_basic_attack=None, by_effect=None, conditions=[])` |
| When X attacks you | `WhenUnitAttackYou(ability_type, attacker, operation, conditions=[])` |
| When X schemes / would scheme | `WhenUnitWouldScheme(ability_type, who_scheme, operation, *, against_player='AnyPlayer', by_effect=None, conditions=[])` |
| After X schemes | `AfterUnitSchemeEnd(ability_type, which_unit, operation, *, against_player='AnyPlayer', conditions=[])` |
| When Defeated (personnage) | `WhenUnitBeDefeated(AbilityType.WhenDefeated, which_unit, operation, ...)` |
| When X would be defeated (remplacer la défaite) | `WhenUnitWouldBeDefeated(ability_type, which_unit, operation, *, by_consequential_damage=None, conditions=[])` |
| When Defeated (complot) | `WhenSchemeBeDefeated(AbilityType.WhenDefeated, which_scheme, operation, *, has_defeating_player=None, conditions=[])` |
| Setup (face 1A d'un complot principal) | `WhenCardSetup("This", operation)` |
| Setup (carte avec le mot-clé `Setup` dans `desc`, environnement...) | `AfterGameSetup(operation)` (jamais `WhenCardSetup`) |
| Attach to X (attachement de rencontre) | `AttachToFaceWhenPutIntoPlay(target, *, highest_atk=False, ..., conditions=[])` |
| Hero Action: Spend ... → discard this card | `PlayerActionToDiscardThis(ability_type, *, conditions=[], ex_operation=...)` puis `.SetCost(Cost("RRR"))` |
| X cannot take damage | `UnitCannotTakeDamageWhile(ability_type, which_card, *, conditions=[], ...)` |
| Escalade dynamique d'un complot | `WhenCalcThisSchemeEscalation(operation)` |

Jouer une carte qui n'est pas un événement : **le moteur l'ajoute tout
seul**. Une amélioration s'attache par défaut à ton identité, un soutien se
pose chez toi, un allié et une manigance du joueur entrent en jeu. Tu
n'écris la fabrique que pour **changer** ce comportement :

| Carte | Quand l'écrire | Fabrique |
|---|---|---|
| Amélioration | « Attach to a minion / an enemy », « Play under any player's control » | `CanPlayThisUpgradeCard(target=None, conditions=[], replaced_operation=None)` avec `Minion`, `Enemy`, `"Players"`... (exemples 01007, 01009, 05023) |
| Soutien | « Play under any player's control », ou une condition | `CanPlayThisSupportCard(*, under_any_players_control=False, conditions=[])` |
| Manigance du joueur | une condition pour la jouer | `CanPlayThisSchemeCard(*, conditions=[])` (exemple 60024, qui l'écrit sans condition : sans effet, mais sans danger) |
| Allié | jamais | rien |

Bonus continus et compteurs :

| Texte imprimé | Fabrique |
|---|---|
| You get +N (amélioration attachée à toi) | `*GiveKeywordToAttached("You", health=N, attack=..., thwart=..., defense=..., recover=..., hand_size=..., retaliate=..., trait=...)` |
| Attached X gains retaliate / +ATK | `*GiveKeywordToAttached(CardFinder(name="X"), retaliate=1)` |
| Bonus à des cartes en jeu (soutien, allié...) | `*GiveKeywordToInPlayWhenApplyThis(card_finder, *, control_by=None, attack=..., ally_limit=..., ...)` |
| Bonus dynamique sur soi | `ThisGainKeyword(check_fn, *, attack=..., hand_size=..., ..., change_on_event=OnEvent...)` |
| +X pour chaque carte en jeu | `ThisGainKeywordForEachFaceInPlay(for_each_face_in_play, *, attack=..., scheme=..., change_on_event=...)` |
| Attacks gain overkill / piercing / ranged | `UnitAttackGainKeyword(attacker, target=None, *, overkill=False, ranged=False, piercing=False, ...)` |
| Enters play with N counters (sans `Uses`) | `ThisEnterPlayWithCounters(counters, name)` |
| If there are at least N counters here | `IfThereAreAtLeastCounterHere(at_least, counter_name, operation, *, conditions=[])` |
| After a token is placed here | `AfterCardPlacedToken(ability_type, which_card, token_name, operation, *, conditions=[], at_least=None)` |

Ressources :

| Texte imprimé | Fabrique |
|---|---|
| Resource: generate [x] | `CanGenerateResources(ability_type, resources=None, for_card=None, *, resources_fn=None, conditions=[], ...)` ; **une seule par carte** |
| Ressource doublée pour une classe | `DoubleResourcesThisGenerates(for_card)` |
| Réduction de coût | `ReduceCostToPlayThis(update_cost_fn, *, ...)` (voir pièges) |

Choix (« Choose one ») :

| Besoin | Fabrique |
|---|---|
| Une option | `ForChoiceAbility(name, operation=None, *, condition=True)` ; `operation(targets)` |
| Une option qui coûte | `ForChoiceAbilityWithCost(cost, name=None, operation=None, *, conditions=[])` |
| « sinon » | `Otherwise(operation)` |
| Proposer les options | `player.ChooseAbilities(effect, option1, option2, ...)` ; facultatif : `player.MayChooseOneAbility(effect, option)` |

### 7.4 Méthodes chaînées d'une capacité

```python
(AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, mon_effet)
    .SetName("Nom affiché")          # nom de la capacité (« Spider-Sense »)
    .SetPlay()                        # c'est un événement qui se JOUE
    .SetLabel('attack')               # 'attack' | 'thwart' | 'defense' ; UN SEUL appel (deux libellés : SetLabel('thwart', 'attack'))
    .SetCost(Cost("Y"))               # coût en ressources colorées ("RRR", "YBR", "1" pour une ressource quelconque)
    .SetCostFunc(CostFunc.Exhaust("This"))   # coût non monétaire, cumulable
    .SetTarget(Enemy)                 # cible
    .LimitOncePerRound())             # (Limit once per round.)
```

Autres méthodes réelles : `.SetPlay(hero_form_only=True)` (« Hero form
only »), `.SetPlay(alter_ego_form_only=True)`, `.LimitOncePerPhase()`,
`.AnyPlayerCanDoThis()` (« Any player can do this »).

### 7.5 Coûts (`CostFunc`)

| Coût imprimé | Code |
|---|---|
| Exhaust this card → | `CostFunc.Exhaust("This")` |
| Exhaust your identity / your hero | `CostFunc.Exhaust("YourIdentity")` |
| Exhaust a [[X]] support you control | `CostFunc.Exhaust(CardFinder(trait="X", card_type=Support))` |
| Remove N counters from this card | `CostFunc.Counter("This", N, "web")` |
| Discard this card | `CostFunc.Discard("This")` |
| Deal N damage to this character | `CostFunc.DealDamage(N, "This")` |
| Return X to your hand | `CostFunc.ReturnToHand(name="X", to_who="Owner")` |
| Spend [x] resources | `.SetCost(Cost("R"))` (pas un CostFunc) |
| Autre | `A_FAIRE_CLAUDE` (Claude utilise `CostFunc.Custom`, piégeux) |

### 7.6 Cibles (`SetTarget`)

Il y a deux familles de chaînes, à ne pas mélanger.

**Dans `.SetTarget(...)`** (la cible que le joueur choisit), seules ces
chaînes existent : `"This"`, `"YourIdentity"`, `"Players"`, `"Trigger"` (la
carte qui a déclenché), `"Attacker"`, `"Initiator"`, `"YouControlUnit"`,
`"YourHandCards"`, `"TeamUp"` (obligatoire sur un événement Team-Up),
`"Character"`, `"VillainAndEngagedSamePlayerMinion"`.

**Comme « qui » d'une fabrique** (le premier ou le deuxième argument :
`attacker`, `which_card`, `which_player`, `who_take_damage`...), on trouve en
plus : `"You"`, `"AnyPlayer"`, `"AttachedEnemy"`, `"AttachedMinion"`,
`"AttachedVillain"`, ou un `CardFinder(...)`, ou un type (`Villain`,
`Enemy`).

Types : `Enemy`, `Villain`, `Minion`, `Ally`, `Unit2` (tout personnage),
`Friend` (personnage ami), `Scheme2` (tout complot), `MainScheme`,
`SchemeSide2` (complot annexe), `Upgrade`, `Support`, `Event`, `Treachery`,
`Attachment`, `Environment`, `Obligation`.

Paramètres utiles : `range=(1, 2)`, `range="All"`, `range=(1, "All")`,
`canbe_stunned=True`, `canbe_confused=True`, `canbe_tough=True`,
`canbe_ready=True`, `canbe_exhaust=True`, `canbe_heal=True`,
`can_place_threat=True`, `name="X"`, `trait="X"`,
`from_where=["YouControlCards"]`, `from_where=["YourHandCards"]`.

⚠ **Une chaîne de ciblage inventée ne lève aucune erreur** : n'en utilise
aucune qui ne soit pas dans la liste ci-dessus.

⚠ `range=(0, n)` seulement pour un « up to n ». « Stun an enemy » = cible
obligatoire = `SetTarget(Enemy)` sans `range`.

### 7.7 Chercher des cartes : `CardFinder`

`CardFinder(name="Rhino")`, `CardFinder(name="Rhino", card_type=Villain)`,
`CardFinder(trait="TECH")`, `CardFinder(traits=["AVENGER"], card_type=Ally)`,
`CardFinder(non_trait="ELITE", card_type=Minion)`,
`CardFinder(has_printed_res="B")`, `CardFinder(card_class="Leadership")`.

⚠ **Le nom s'écrit SANS l'étoile d'unicité** : `CardFinder(name="Silver
Samurai")`, jamais `"* Silver Samurai"` (la seconde forme ne trouve jamais
rien, en silence).

### 7.8 Opérations courantes (toutes vues dans les exemples)

| But | Code |
|---|---|
| Infliger des dégâts | `this.DealDamage(cibles, n, effect)` |
| Subir des dégâts | `cible.TakeDamage(source, n, effect)` |
| Soigner | `this.HealthUnits(cibles, n, effect)` (rend faux si rien n'est soigné) |
| Retirer de la menace | `this.RemoveThreatFromSchemes(cibles, n, effect)` |
| Poser de la menace | `this.PlaceThreatOnSchemes(cibles, n, effect)` ; `n` peut valoir `"1*"` (par joueur) ; cibles : liste, ou `"MainScheme"` |
| Statut | `Faces.GiveStatus(cibles, "Stunned" / "Confused" / "Tough", effect)` |
| Défausser | `Faces.DiscardAll(cartes, effect)` |
| Retirer de la partie | `Faces.RemoveAllFromGame(cartes, effect)` |
| Redresser / incliner | `Faces.ReadyAll(cartes, effect)` / `Faces.ExhaustAll(cartes, effect)` |
| Compteurs | `Faces.PlaceCountersOn([carte], n, 'nom', effect)`, `carte.GetCounters('nom')` |
| Gagner Surge | `this.GainSurge(1, effect)` (raccourci : `ThisCardGainSurge`) |
| Piocher | `player.DrawUp(n, effect)` |
| Défausser au hasard | `player.DiscardRandomHandCards(n, effect)` |
| Le vilain attaque / manigance | `villain.DoAttackYou(player, effect)`, `villain.DoSchemes(player, effect)` |
| Trouver | `Worlds.FindVillain(effect)`, `Worlds.FindCardOnField(effect, name=..., card_type=...)`, `Worlds.FindCardsOnField(effect, trait=..., card_type=...)`, `Worlds.GetOnFieldHeroes(effect)`, `Worlds.GetOnFieldAllies(effect)`, `Worlds.GetOnFieldMinions(effect)`, `Worlds.GetSideSchemes(effect)`, `Worlds.FindMainScheme(this)`, `Worlds.GetFirstPlayer(effect)`, `Worlds.GetPlayers(effect)` |
| Chercher dans le deck rencontre | `Search.EncounterCard(effect, include_discard_pile=True, name=..., card_type=...)`, `Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)` |
| Révéler / mettre en jeu | `face.Reveal(player, effect)`, `face.PutIntoPlay(player, effect)` |
| Bonus temporaire | `unite.GainUntilPhaseEnd(effect, attack=2)` |
| Chaque joueur | `Players.ForEachPlayer(effect, action, valeur_initiale)` |
| Mode expert ? | `Worlds.IsExpert(effect)` |
| Joueur en forme héros ? | `player.IsHero()`, `player.IsAlterEgo()` |

Messages (selon le déclencheur) : `message.GetToPlayer()` (joueur qui révèle
ou qui est visé), `message.GetGaveToPlayer()` (obligation),
`message.PreventDamage("All", effect)`, `message.SetBeInstead(effect)`
(« ... instead »), `message.CancelWhenRevealedEffect(effect)`,
`message.GiveAdditionalBoostCardForThisActivation(1, effect)`,
`message.GainOverKill(effect)`, `message.GainBoostIcon(n, effect)`,
`message.DoSchemeInstead(effect)`, `message.MustDefendWithAlly(effect)`.

---

## 8. Catalogue d'exemples réels, classés par mécanique

Chaque exemple donne l'entrée JSON, puis le script, recopiés des fichiers du
projet.

### 8.1 Cartes de joueur

#### 8.1.1 Héros : Interruption avec nom de capacité

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01001a",
    "type": "Hero",
    "name": "* Spider-Man",
    "subtitle": "",
    "desc": {
        "HP": "10",
        "ATK": "2",
        "THW": "1",
        "DEF": "3",
        "HS": "5"
    },
    "traits": [
        "AVENGER"
    ],
    "set_name": "Spider-Man",
    "text": "Spider-Sense — <b>Interrupt</b>: When the villain initiates an attack against you, draw 1 card."
}
```

Script (`src/cards/pack/core/spider_man/01001a.py`) :

```python
# Source : src/cards/pack/core/spider_man/01001a.py
from . import *

# * Spider-Man

def GetAbilities() -> Sequence['Ability']:

    def spider_man(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)

        initiator = effect.GetInitiator()
        initiator.DrawUp(1, effect)


    return [
        AbilityFactory.WhenUnitInitiatesAttackAgainst(
            AbilityType.Interrupt,
            Villain,
            "You",
            spider_man
        ).SetName("Spider-Sense")
    ]
```


#### 8.1.2 Alter-ego : Ressource limitée une fois par round

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01001b",
    "type": "AlterEgo",
    "name": "* Peter Parker",
    "subtitle": "",
    "desc": {
        "HP": "10",
        "REC": "3",
        "HS": "6"
    },
    "traits": [
        "GENIUS"
    ],
    "set_name": "Spider-Man",
    "text": "Scientist — <b>Resource</b>: Generate a [mental] resource. (Limit once per round.)"
}
```

Script (`src/cards/pack/core/spider_man/01001b.py`) :

```python
# Source : src/cards/pack/core/spider_man/01001b.py
from . import *

# * Peter Parker

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("B")
        ).SetName("Scientist")
        .LimitOncePerRound()
    ]
```


#### 8.1.3 Héros : bonus dynamique sur soi (taille de main)

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01029a",
    "type": "Hero",
    "name": "* Iron Man",
    "subtitle": "",
    "desc": {
        "HP": "9",
        "ATK": "1",
        "THW": "2",
        "DEF": "1",
        "HS": "1"
    },
    "traits": [
        "AVENGER"
    ],
    "set_name": "Iron Man",
    "text": "You get +1 hand size for each [[Tech]] upgrade you control (to a maximum hand size of 7)."
}
```

Script (`src/cards/pack/core/iron_man/01029a.py`) :

```python
# Source : src/cards/pack/core/iron_man/01029a.py
from . import *

# * Iron Man

def GetAbilities() -> Sequence['Ability']:

    def iron_man(effect: 'Effect', ui: List['CardFace']) -> int:
        this = effect.this.CastTo(Hero)

        player = this.GetControlByPlayer()
        faces = player.GetControlCardsByType(CardFinder(trait="TECH"), upgrade=True)
        for face in faces:
            if face.HasTrait("TECH"):
                ui.append(face)
        return min(6, len(faces))

    return [
        AbilityFactory.ThisGainKeyword(
            iron_man,
            hand_size=1,
            change_on_event=OnEvent.AttachedMove(Upgrade)
        )
    ]
```


#### 8.1.4 Alter-ego : Action limitée une fois par round, regarder le deck

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01029b",
    "type": "AlterEgo",
    "name": "* Tony Stark",
    "subtitle": "",
    "desc": {
        "HP": "9",
        "REC": "3",
        "HS": "6"
    },
    "traits": [
        "GENIUS"
    ],
    "set_name": "Iron Man",
    "text": "Futurist — <b>Action</b>: Look at the top 3 cards of your deck. Add 1 to your hand and discard the others. (Limit once per round.)"
}
```

Script (`src/cards/pack/core/iron_man/01029b.py`) :

```python
# Source : src/cards/pack/core/iron_man/01029b.py
from . import *

# * Tony Stark

def GetAbilities() -> Sequence['Ability']:

    def tony_stark(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        initiator = effect.GetInitiator()

        faces = initiator.LookAtDeck(initiator.player_deck, 3, effect)
        face = initiator.AskChooseFace(faces, effect)
        if face:
            faces.remove(face)
            Faces.AddToHand([face], initiator, effect)
        Faces.DiscardAll(faces, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            tony_stark
        ).SetName("Futurist")
        .LimitOncePerRound()
    ]
```


#### 8.1.5 Allié : Réponse Forcée après l'avoir joué

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01002",
    "type": "Ally",
    "name": "* Black Cat",
    "subtitle": "Felicia Hardy",
    "desc": {
        "Cost": "2",
        "HP": "2",
        "ATK": "1",
        "THW": "1*",
        "RES": "Y",
        "Class": "Hero"
    },
    "traits": [
        "HERO FOR HIRE"
    ],
    "set_name": "Spider-Man",
    "text": "<b>Forced Response</b>: After you play Black Cat, discard the top 2 cards of your deck. Add each card with a printed [mental] resource discarded this way to your hand."
}
```

Script (`src/cards/pack/core/spider_man/01002.py`) :

```python
# Source : src/cards/pack/core/spider_man/01002.py
from . import *

# * Black Cat

def GetAbilities() -> Sequence['Ability']:

    def black_cat(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        initiator = effect.GetInitiator()

        faces = initiator.DiscardDeckTopCards(2, effect)
        faces = CardFinder(has_printed_res="B").Checks(faces)
        initiator.GainCard(faces, effect)


    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.ForcedResponse,
            "You",
            "This",
            black_cat
        )
    ]
```


#### 8.1.6 Allié : Réponse en entrant en jeu, avec cible

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01083",
    "type": "Ally",
    "name": "* Mockingbird",
    "subtitle": "Bobbi Morse",
    "desc": {
        "Cost": "3",
        "HP": "3",
        "ATK": "1*",
        "THW": "1*",
        "RES": "R",
        "Class": "Basic"
    },
    "traits": [
        "S.H.I.E.L.D",
        "SPY"
    ],
    "set_name": "",
    "text": "<b>Response</b>: After Mockingbird enters play, stun an enemy."
}
```

Script (`src/cards/pack/core/01083.py`) :

```python
# Source : src/cards/pack/core/01083.py
from . import *

# * Mockingbird: Bobbi Morse

def GetAbilities() -> Sequence['Ability']:

    def mockingbird(effect: 'Effect', message: 'Message2'):
        this = effect.this.CastTo(Ally)
        Unused(this)

        Faces.GiveStatus(effect.targets, "Stunned", effect)


    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            mockingbird
        ).SetTarget(Enemy, canbe_stunned=True)
    ]
```


#### 8.1.7 Allié : « Choose one », et défausse en fin de round

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01084",
    "type": "Ally",
    "name": "* Nick Fury",
    "subtitle": "",
    "desc": {
        "Cost": "4",
        "HP": "3",
        "ATK": "2*",
        "THW": "2*",
        "RES": "B",
        "Class": "Basic"
    },
    "traits": [
        "S.H.I.E.L.D",
        "SPY"
    ],
    "set_name": "",
    "text": "<b>Forced Response</b>: After Nick Fury enters play, choose one: remove 2 threat from a scheme, draw 3 cards, or deal 4 damage to an enemy. At the end of the round, if Nick Fury is still in play, discard him."
}
```

Script (`src/cards/pack/core/01084.py`) :

```python
# Source : src/cards/pack/core/01084.py
from . import *

# * Nick Fury

def GetAbilities() -> Sequence['Ability']:

    def nick_fury(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        initiator = effect.GetInitiator()

        def remove_2_threat_from_a_scheme(targets: Sequence['CardFace']) -> None:
            this.RemoveThreatFromSchemes(targets, 2, effect)

        def draw_3_cards(targets: Sequence['CardFace']) -> None:
            initiator.DrawUp(3, effect)

        def deal_4_damage_to_an_enemy(targets: Sequence['CardFace']) -> None:
            this.DealDamage(targets, 4, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 2 threat from a scheme",
                remove_2_threat_from_a_scheme
            ).SetTarget(Scheme2),
            AbilityFactory.ForChoiceAbility(
                "Draw 3 cards",
                draw_3_cards
            ).SetTarget("YourIdentity"),
            AbilityFactory.ForChoiceAbility(
                "Deal 4 damage to an enemy",
                deal_4_damage_to_an_enemy
            ).SetTarget(Enemy),
        )


    return [
        AbilityFactory.DiscardThisWhenRoundEnd(
            AbilityType.ForcedResponse,
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            nick_fury
        )
    ]
```


#### 8.1.8 Allié : Action avec coût en ressource, limite, choix

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01068",
    "type": "Ally",
    "name": "* Vision",
    "subtitle": "",
    "desc": {
        "Cost": "4",
        "HP": "3",
        "ATK": "2*",
        "THW": "1*",
        "RES": "R",
        "Class": "Leadership"
    },
    "traits": [
        "ANDROID",
        "AVENGER"
    ],
    "set_name": "",
    "text": "<b>Action</b>: Spend a [energy] resource → choose THW or ATK. Until the end of the phase, Vision gets +2 to the chosen power. (Limit once per round.)"
}
```

Script (`src/cards/pack/core/01068.py`) :

```python
# Source : src/cards/pack/core/01068.py
from . import *

# * Vision

def GetAbilities() -> Sequence['Ability']:

    def vision(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        initiator = effect.GetInitiator()

        def gain_2_atk(targets: Sequence['CardFace']) -> None:
            this.GainUntilPhaseEnd(effect, attack=2)
        def gain_2_thw(targets: Sequence['CardFace']) -> None:
            this.GainUntilPhaseEnd(effect, thwart=2)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "THW",
                gain_2_thw
            ),
            AbilityFactory.ForChoiceAbility(
                "ATK",
                gain_2_atk
            ),
        )


    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            vision
        ).SetCost(Cost("Y"))
        .LimitOncePerRound()
        # .SetDesc('choose THW or ATK. Until the end of the phase, Vision gets +2 to the chosen power')
    ]
```


#### 8.1.9 Allié : Réponse après avoir attaqué

Entrée de `data/cards.json` (pack `hlk`) :

```json
{
    "card_id": "10011",
    "type": "Ally",
    "name": "* Brawn",
    "subtitle": "Amadeus Cho",
    "desc": {
        "Cost": "3",
        "HP": "5",
        "ATK": "1*",
        "THW": "1*",
        "RES": "B",
        "Class": "Aggression"
    },
    "traits": [
        "CHAMPION",
        "GAMMA"
    ],
    "set_name": "",
    "text": "<b>Response</b>: After Brawn attacks, remove 1 threat from a scheme."
}
```

Script (`src/cards/pack/hlk/10011.py`) :

```python
# Source : src/cards/pack/hlk/10011.py
from . import *

# * Brawn

def GetAbilities() -> Sequence['Ability']:

    def brawn(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        this.RemoveThreatFromSchemes(effect.targets, 1, effect)


    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.Response,
            "This",
            brawn
        ).SetTarget(Scheme2)
    ]
```


#### 8.1.10 Allié : Action avec deux coûts cumulés, toutes les cibles

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01030",
    "type": "Ally",
    "name": "* War Machine",
    "subtitle": "James Rhodes",
    "desc": {
        "Cost": "4",
        "HP": "4",
        "ATK": "2*",
        "THW": "1*",
        "RES": "G",
        "Class": "Hero"
    },
    "traits": [
        "S.H.I.E.L.D",
        "SOLDIER"
    ],
    "set_name": "Iron Man",
    "text": "<b>Action</b>: Exhaust War Machine and deal 2 damage to him → deal 1 damage to each enemy."
}
```

Script (`src/cards/pack/core/iron_man/01030.py`) :

```python
# Source : src/cards/pack/core/iron_man/01030.py
from . import *

# * War Machine

def GetAbilities() -> Sequence['Ability']:

    def war_machine(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        this.DealDamage(effect.targets, 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            war_machine,
        )
        # .SetDesc("Exhaust War Machine and deal 2 damage to him → deal 1 damage to each enemy")
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.DealDamage(2, "This"))
        .SetTarget(Enemy, range=(1, "All"))
    ]
```


#### 8.1.11 Allié : Interruption payante sur une carte révélée

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01075",
    "type": "Ally",
    "name": "* Black Widow",
    "subtitle": "Natasha Romanoff",
    "desc": {
        "Cost": "3",
        "HP": "2",
        "ATK": "1*",
        "THW": "2*",
        "RES": "R",
        "Class": "Protection"
    },
    "traits": [
        "S.H.I.E.L.D",
        "SPY"
    ],
    "set_name": "",
    "text": "<b>Interrupt</b>: When a card is revealed from the encounter deck, exhaust Black Widow and spend a [mental] resource → cancel the effects of that card and discard it. Then, reveal another card from the encounter deck."
}
```

Script (`src/cards/pack/core/01075.py`) :

```python
# Source : src/cards/pack/core/01075.py
from . import *

# * Black Widow

def GetAbilities() -> Sequence['Ability']:

    def black_widow(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        player = message.GetToPlayer()

        message.CancelAllEffectsAndDiscardIt(effect)

        # If you triggered Black Widow’s ability, then you are instructed to reveal another card from the encounter deck.
        Worlds.RevealEncounterDeckTopCard(player, effect)


    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.Interrupt,
            "AnyPlayer",
            None,
            "All",
            black_widow,
            from_encounter=True,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget("Trigger")
        .SetCost(Cost("B")),
    ]
```


#### 8.1.12 Événement : Hero Action d'attaque

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01005",
    "type": "Event",
    "name": "Swinging Web Kick",
    "subtitle": "",
    "desc": {
        "Cost": "3",
        "RES": "B",
        "Class": "Hero"
    },
    "traits": [
        "AERIAL",
        "ATTACK",
        "SUPERPOWER"
    ],
    "set_name": "Spider-Man",
    "text": "<b>Hero Action</b> <i>(attack)</i>: Deal 8 damage to an enemy."
}
```

Script (`src/cards/pack/core/spider_man/01005.py`) :

```python
# Source : src/cards/pack/core/spider_man/01005.py
from . import *

# Swinging Web Kick

def GetAbilities() -> Sequence['Ability']:

    def swinging_web_kick(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        this.DealDamage(effect.targets, 8, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            swinging_web_kick
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy)
    ]
```


#### 8.1.13 Événement : Interruption de défense (prévenir les dégâts)

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01003",
    "type": "Event",
    "name": "Backflip",
    "subtitle": "",
    "desc": {
        "Cost": "0",
        "RES": "R",
        "Class": "Hero"
    },
    "traits": [
        "DEFENSE",
        "SKILL"
    ],
    "set_name": "Spider-Man",
    "text": "<b>Interrupt</b> <i>(defense)</i>: When you would take any amount of damage from an attack, prevent all of that damage."
}
```

Script (`src/cards/pack/core/spider_man/01003.py`) :

```python
# Source : src/cards/pack/core/spider_man/01003.py
from . import *

# Backflip

def GetAbilities() -> Sequence['Ability']:

    def backflip(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        message.PreventDamage("All", effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            "You",
            backflip,
            is_from_attack=True
        ).SetPlay().SetLabel('defense')
    ]
```


#### 8.1.14 Événement : annuler un « When Revealed »

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01004",
    "type": "Event",
    "name": "Enhanced Spider-Sense",
    "subtitle": "",
    "desc": {
        "Cost": "1",
        "RES": "B",
        "Class": "Hero"
    },
    "traits": [
        "SUPERPOWER"
    ],
    "set_name": "Spider-Man",
    "text": "<b>Hero Interrupt</b>: When a treachery card is revealed from the encounter deck, cancel its \"<b>When Revealed</b>\" effects."
}
```

Script (`src/cards/pack/core/spider_man/01004.py`) :

```python
# Source : src/cards/pack/core/spider_man/01004.py
from . import *

# Enhanced Spider-Sense

def GetAbilities() -> Sequence['Ability']:

    def enhanced_spider_sense(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.CancelWhenRevealedEffect(effect)

    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt,
            "AnyPlayer",
            Treachery,
            "WhenRevealed",
            enhanced_spider_sense,
            from_encounter=True,
        ).SetPlay()
    ]
```


#### 8.1.15 Événement : Action de soin

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01086",
    "type": "Event",
    "name": "First Aid",
    "subtitle": "",
    "desc": {
        "Cost": "1",
        "RES": "B",
        "Class": "Basic"
    },
    "traits": [],
    "set_name": "",
    "text": "<b>Action</b>: Heal 2 damage from any character."
}
```

Script (`src/cards/pack/core/01086.py`) :

```python
# Source : src/cards/pack/core/01086.py
from . import *

# First Aid

def GetAbilities() -> Sequence['Ability']:

    def first_aid(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        this.HealthUnits(effect.targets, 2, effect)


    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            first_aid
        ).SetPlay()
        .SetTarget(Unit2, canbe_heal=True)
    ]
```


#### 8.1.16 Événement : Interruption de contre, effet temporaire

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01085",
    "type": "Event",
    "name": "Emergency",
    "subtitle": "",
    "desc": {
        "Cost": "0",
        "RES": "Y",
        "Class": "Basic"
    },
    "traits": [
        "THWART"
    ],
    "set_name": "",
    "text": "<b>Interrupt</b> <i>(thwart)</i>: When the villain schemes, reduce the amount of threat placed on the scheme by 1."
}
```

Script (`src/cards/pack/core/01085.py`) :

```python
# Source : src/cards/pack/core/01085.py
from . import *

# Emergency

def GetAbilities() -> Sequence['Ability']:

    def emergency(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        this.effect.RegisterTemp(
            AbilityFactory.WhenSchemeWouldPlaceThreat(
                AbilityType.Temp0,
                None,
                lambda effect, message:
                    message.ReduceThreat(1, effect),
                by_scheme=message
            ),
            unregister_after_exec=True,
            until_event_end=message
        )


    return [
        AbilityFactory.WhenUnitWouldScheme(
            AbilityType.Interrupt,
            Villain,
            emergency,
        ).SetPlay().SetLabel('thwart')
    ]
```


#### 8.1.17 Événement : bonus à tous les personnages d'un joueur

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01070",
    "type": "Event",
    "name": "Lead from the Front",
    "subtitle": "",
    "desc": {
        "Cost": "2",
        "RES": "Y",
        "Class": "Leadership"
    },
    "traits": [
        "TACTIC"
    ],
    "set_name": "",
    "text": "<b>Hero Action</b>: Choose a player. Each character that player controls gets +1 THW and +1 ATK until the end of the phase."
}
```

Script (`src/cards/pack/core/01070.py`) :

```python
# Source : src/cards/pack/core/01070.py
from . import *

# Lead from the Front

def GetAbilities() -> Sequence['Ability']:

    def lead_from_the_front(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        player = effect.targets[0].GetControlByPlayer()

        Players.EachCharacterGetsUntilPhaseEnd(
            player,
            effect,
            attack=+1,
            thwart=+1,
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            lead_from_the_front
        ).SetPlay()
        .SetTarget("Players")
    ]
```


#### 8.1.18 Soutien : Action d'alter-ego avec coût « Exhaust »

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01006",
    "type": "Support",
    "name": "* Aunt May",
    "subtitle": "",
    "desc": {
        "Cost": "1",
        "RES": "Y",
        "Class": "Hero"
    },
    "traits": [
        "PERSONA"
    ],
    "set_name": "Spider-Man",
    "text": "<b>Alter-Ego Action</b>: Exhaust Aunt May → heal 4 damage from Peter Parker."
}
```

Script (`src/cards/pack/core/spider_man/01006.py`) :

```python
# Source : src/cards/pack/core/spider_man/01006.py
from . import *

# * Aunt May

def GetAbilities() -> Sequence['Ability']:

    def aunt_may(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        this.HealthUnits(effect.targets, 4, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            aunt_may,
            conditions=[
                lambda effect, message:
                    effect.GetInitiator().GetAlterEgo().CanHeath()
            ],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget("YourIdentity")
    ]
```


#### 8.1.19 Soutien : choisir un joueur

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01091",
    "type": "Support",
    "name": "Avengers Mansion",
    "subtitle": "",
    "desc": {
        "Cost": "4",
        "RES": "B",
        "MaxPerUnit": "1",
        "Class": "Basic"
    },
    "traits": [
        "AVENGER",
        "LOCATION"
    ],
    "set_name": "",
    "text": "Max 1 per player.\n<b>Action</b>: Exhaust Avengers Mansion → choose a player. That player draws 1 card."
}
```

Script (`src/cards/pack/core/01091.py`) :

```python
# Source : src/cards/pack/core/01091.py
from . import *

# Avengers Mansion

def GetAbilities() -> Sequence['Ability']:

    def avengers_mansion(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        Players.DrawUp(effect.targets, 1, effect)


    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            avengers_mansion
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget("Players")
        # .SetDesc("Exhaust Avengers Mansion → choose a player. That player draws 1 card")
    ]
```


#### 8.1.20 Soutien : ressource calculée

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01033",
    "type": "Support",
    "name": "* Pepper Potts",
    "subtitle": "",
    "desc": {
        "Cost": "3",
        "RES": "R",
        "Class": "Hero"
    },
    "traits": [
        "PERSONA"
    ],
    "set_name": "Iron Man",
    "text": "<b>Resource</b>: Exhaust Pepper Potts → generate the resources of the top card in your discard pile."
}
```

Script (`src/cards/pack/core/iron_man/01033.py`) :

```python
# Source : src/cards/pack/core/iron_man/01033.py
from . import *

# * Pepper Potts

def GetAbilities() -> Sequence['Ability']:

    def petter_potts(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources|None':
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator.discard_pile.GetSize() > 0:
            face = initiator.discard_pile.Get(True)[0]
            res = FacesCounter.GetPrintedResources([face])
            return res

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            resources_fn=petter_potts,
            conditions=[
                lambda effect, message:
                    effect.this.GetControlByPlayer().discard_pile.GetSize() > 0
            ],
        ).SetCostFunc(CostFunc.Exhaust("This"))
    ]
```


#### 8.1.21 Soutien : bonus continu (limite d'alliés)

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01073",
    "type": "Support",
    "name": "* The Triskelion",
    "subtitle": "",
    "desc": {
        "Cost": "1",
        "RES": "Y",
        "Class": "Leadership"
    },
    "traits": [
        "LOCATION",
        "S.H.I.E.L.D"
    ],
    "set_name": "",
    "text": "Increase your ally limit by 1. <i>(This allows you to control more than 3 allies.)</i>"
}
```

Script (`src/cards/pack/core/01073.py`) :

```python
# Source : src/cards/pack/core/01073.py
from . import *

# * The Triskelion

def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            ally_limit=1,
        )
    ]
```


#### 8.1.22 Ressource doublée pour une classe

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01072",
    "type": "Resource",
    "name": "The Power of Leadership",
    "subtitle": "",
    "desc": {
        "RES": "G",
        "MaxPerDeck": "2",
        "Class": "Leadership"
    },
    "traits": [],
    "set_name": "",
    "text": "Max 2 per deck.\nDouble the number of resources this card generates while paying for a Leadership <i>(blue)</i> card."
}
```

Script (`src/cards/pack/core/01072.py`) :

```python
# Source : src/cards/pack/core/01072.py
from . import *

# The Power of Leadership

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.DoubleResourcesThisGenerates(
            CardFinder(card_class="Leadership")
        ),
    ]
```


#### 8.1.23 Amélioration attachée à un sbire, Interruption Forcée

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01007",
    "type": "Upgrade",
    "name": "Spider-Tracer",
    "subtitle": "",
    "desc": {
        "Cost": "1",
        "RES": "Y",
        "Class": "Hero"
    },
    "traits": [
        "ITEM",
        "TECH"
    ],
    "set_name": "Spider-Man",
    "text": "Attach to a minion.\n<b>Forced Interrupt</b>: When attached minion is defeated, remove 3 threat from a scheme."
}
```

Script (`src/cards/pack/core/spider_man/01007.py`) :

```python
# Source : src/cards/pack/core/spider_man/01007.py
from . import *

# Spider-Tracer

def GetAbilities() -> Sequence['Ability']:

    def spider_tracer(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        this.RemoveThreatFromSchemes(effect.targets, 3, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(Minion),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.ForcedInterrupt,
            "AttachedMinion",
            spider_tracer
        ).SetTarget(Scheme2)
    ]
```


#### 8.1.24 Amélioration avec `Uses` et Ressource payée en compteur

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01008",
    "type": "Upgrade",
    "name": "Web-Shooter",
    "subtitle": "",
    "desc": {
        "Cost": "1",
        "RES": "R",
        "Uses": "3,web",
        "Class": "Hero"
    },
    "traits": [
        "ITEM",
        "TECH"
    ],
    "set_name": "Spider-Man",
    "text": "Uses (3 web counters). <i>(Enters play with 3 counters. When those are gone, discard this card)</i>\n<b>Hero Resource</b>: Exhaust Web-Shooter and remove 1 web counter from it → generate a [wild] resource."
}
```

Script (`src/cards/pack/core/spider_man/01008.py`) :

```python
# Source : src/cards/pack/core/spider_man/01008.py
from . import *

# Web-Shooter

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G")
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, "web"))
    ]
```


#### 8.1.25 Amélioration sur un ennemi, « Hero form only », « instead »

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01009",
    "type": "Upgrade",
    "name": "Webbed Up",
    "subtitle": "",
    "desc": {
        "Cost": "4",
        "RES": "R",
        "MaxPerUnit": "1",
        "Class": "Hero"
    },
    "traits": [
        "CONDITION"
    ],
    "set_name": "Spider-Man",
    "text": "Hero form only. Attach to an enemy. Max 1 per enemy.\n<b>Forced Interrupt</b>: When attached enemy would attack, discard Webbed Up instead. Then, stun that enemy."
}
```

Script (`src/cards/pack/core/spider_man/01009.py`) :

```python
# Source : src/cards/pack/core/spider_man/01009.py
from . import *

# Webbed Up

def GetAbilities() -> Sequence['Ability']:

    def webbed_up(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.SetBeInstead(effect)
        this = effect.this.CastTo(Upgrade)
        Faces.DiscardAll([this], effect)
        Faces.GiveStatus(effect.targets, "Stunned", effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            Enemy,
        ).SetPlay(hero_form_only=True),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            "AttachedEnemy",
            webbed_up
        ).SetTarget("Trigger")
    ]
```


#### 8.1.26 Amélioration : +PV au joueur qui la reçoit

Entrée de `data/cards.json` (pack `msm`) :

```json
{
    "card_id": "05023",
    "type": "Upgrade",
    "name": "Endurance",
    "subtitle": "",
    "desc": {
        "Cost": "1",
        "RES": "Y",
        "MaxPerUnit": "1",
        "Class": "Basic"
    },
    "traits": [
        "CONDITION"
    ],
    "set_name": "",
    "text": "Play under any player's control. Max 1 per player.\nYou get +3 hit points."
}
```

Script (`src/cards/pack/msm/05023.py`) :

```python
# Source : src/cards/pack/msm/05023.py
from . import *

# Endurance

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            "Players",
        ),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=3,
        ),
    ]
```


#### 8.1.27 Amélioration : bonus continu ET Action payante

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01039",
    "type": "Upgrade",
    "name": "Rocket Boots",
    "subtitle": "",
    "desc": {
        "Cost": "1",
        "RES": "B",
        "Class": "Hero"
    },
    "traits": [
        "ARMOR",
        "TECH"
    ],
    "set_name": "Iron Man",
    "text": "You get +1 hit point.\n<b>Hero Action</b>: Exhaust Rocket Boots and spend a [mental] resource → gain the [[Aerial]] trait until the end of the phase."
}
```

Script (`src/cards/pack/core/iron_man/01039.py`) :

```python
# Source : src/cards/pack/core/iron_man/01039.py
from . import *

# Rocket Boots

def GetAbilities() -> Sequence['Ability']:

    def rocket_boots(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        initiator = effect.GetInitiator()
        hero = initiator.GetIdentity()

        hero.GainUntilPhaseEnd(effect, trait="AERIAL")


    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            rocket_boots
        ).SetCost(Cost("B"))
        .SetCostFunc(CostFunc.Exhaust("This"))
    ]
```


#### 8.1.28 Amélioration : coût en ressource + se défausser

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01093",
    "type": "Upgrade",
    "name": "Tenacity",
    "subtitle": "",
    "desc": {
        "Cost": "2",
        "RES": "Y",
        "Class": "Basic"
    },
    "traits": [
        "CONDITION"
    ],
    "set_name": "",
    "text": "<b>Hero Action</b>: Spend a [physical] resource and discard this card → ready your hero."
}
```

Script (`src/cards/pack/core/01093.py`) :

```python
# Source : src/cards/pack/core/01093.py
from . import *

# Tenacity

def GetAbilities() -> Sequence['Ability']:

    def tenacity(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        Faces.ReadyAll(effect.targets, effect)


    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            tenacity
        ).SetCost(Cost("R"))
        .SetCostFunc(CostFunc.Discard("This"))
        .SetTarget("YourIdentity", canbe_ready=True)
    ]
```


#### 8.1.29 Manigance du joueur, Victory 0, When Defeated

Entrée de `data/cards.json` (pack `fne`) :

```json
{
    "card_id": "60024",
    "type": "PlayerSideScheme",
    "name": "* De-escalation",
    "subtitle": "",
    "desc": {
        "Cost": "0",
        "StartingThreat": "4",
        "Victory": "0",
        "RES": "R",
        "Class": "Justice"
    },
    "traits": [],
    "set_name": "",
    "text": "Victory 0.\n<b>When Defeated</b>: Remove an acceleration token from play."
}
```

Script (`src/cards/pack/fne/60024.py`) :

```python
# Source : src/cards/pack/fne/60024.py
from . import *

# * De-escalation
# Victory 0.
# When Defeated: Remove an acceleration token from play.
#
# CORRECTIF 4/8/2026 : `Worlds.RemoveAccelerationToken` n'existe pas, la
# capacite plantait a chaque fois que la manigance etait vaincue. On passe par
# les faces qui PORTENT un jeton (`GetAccelerationTokenFaces`) et par le
# retrait de jeton standard.

def GetAbilities() -> Sequence['Ability']:

    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this)

        porteurs = [x for x in Worlds.GetAccelerationTokenFaces(effect)
                    if x.acceleration_token > 0]
        if porteurs:
            Faces.RemoveTokensOn(porteurs[:1], 1, 'acceleration_token', effect)

    return [
        AbilityFactory.CanPlayThisSchemeCard(),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated),
    ]
```


#### 8.1.30 Obligation : retournement facultatif, puis choix

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01165",
    "type": "Obligation",
    "name": "Eviction Notice",
    "subtitle": "",
    "desc": {
        "Boost": "2",
        "GiveTo": "Peter Parker"
    },
    "traits": [],
    "set_name": "Spider-Man",
    "text": "<b><i>Give to the Peter Parker player.</i></b>\nYou may flip to alter-ego form. Choose:\n• Exhaust Peter Parker → remove Eviction Notice from the game.\n• Discard 1 card at random from your hand. This card gains surge. Discard this obligation."
}
```

Script (`src/cards/pack/core/spider_man/01165.py`) :

```python
# Source : src/cards/pack/core/spider_man/01165.py
from . import *

# Eviction Notice

def GetAbilities() -> Sequence['Ability']:

    def eviction_notice(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this)
        player = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(player, effect)

        def discard_random_handcards_and_surge(targets: Sequence['CardFace']) -> None:
            player.DiscardRandomHandCards(1, effect)
            this.GainSurge(1, effect)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Peter Parker → remove Eviction Notice from the game",
                lambda targets:
                    Faces.RemoveAllFromGame([this], effect),
                condition=player.IsAlterEgo(),
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
            AbilityFactory.ForChoiceAbility(
                "Discard 1 card at random from your hand. This card gains surge. Discard this obligation",
                discard_random_handcards_and_surge
            )
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            eviction_notice
        )
    ]
```


#### 8.1.31 Obligation : choix avec « sinon » (`Otherwise`)

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01170",
    "type": "Obligation",
    "name": "Business Problems",
    "subtitle": "",
    "desc": {
        "Boost": "2",
        "GiveTo": "Tony Stark"
    },
    "traits": [],
    "set_name": "Iron Man",
    "text": "<b><i>Give to the Tony Stark player.</i></b>\nYou may flip to alter-ego form. Choose:\n• Exhaust Tony Stark → remove Business Problems from the game.\n• Exhaust each upgrade you control. Discard this obligation."
}
```

Script (`src/cards/pack/core/iron_man/01170.py`) :

```python
# Source : src/cards/pack/core/iron_man/01170.py
from . import *

# Business Problems

def GetAbilities() -> Sequence['Ability']:

    def business_problems(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this)
        player = message.GetGaveToPlayer()

        def exhaust_each_upgrade_you_control_discard_this_obligation(targets: Sequence['CardFace']) -> None:
            Faces.ExhaustAll(targets, effect)
            Faces.DiscardAll([this], effect)

        YouMayFlipToYourAlterEgoForm(player, effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Tony Stark → remove Business Problems from the game",
                lambda targets:
                    Faces.RemoveAllFromGame([this], effect),
                condition=player.IsAlterEgo(),
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
            AbilityFactory.ForChoiceAbility(
                "Exhaust each upgrade you control. Discard this obligation",
                exhaust_each_upgrade_you_control_discard_this_obligation
            ).SetTarget(Upgrade, canbe_exhaust=True,
                range="All", from_where=["YouControlCards"]),
            AbilityFactory.Otherwise(
                lambda targets:
                    Faces.DiscardAll([this], effect)
            )
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            business_problems
        )
    ]
```


### 8.2 Cartes de rencontre

#### 8.2.1 Vilain étape 1 : capacité [star] permanente (fonction du set)

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01113",
    "type": "Villain",
    "name": "* Klaw",
    "subtitle": "",
    "desc": {
        "HP": "12*",
        "ATK": "0",
        "SCH": "2",
        "Stage": "1"
    },
    "traits": [
        "MASTERS OF EVIL"
    ],
    "set_name": "Klaw",
    "text": "[star] <b>Forced Interrupt</b>: When Klaw attacks, give him 1 additional boost card for this activation."
}
```

Script (`src/cards/pack/core/klaw/01113.py`) :

```python
# Source : src/cards/pack/core/klaw/01113.py
from . import *

# * Klaw (I)

def GetAbilities() -> Sequence['Ability']:

    return [
        GiveKlawAdditionalBoostCardWhenAttack()
    ]
```


La fonction `GiveKlawAdditionalBoostCardWhenAttack` est celle du
`__init__.py` du set montré en 2.2.

#### 8.2.2 Vilain étape 2 : When Revealed, chercher et révéler un complot

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01095",
    "type": "Villain",
    "name": "* Rhino",
    "subtitle": "",
    "desc": {
        "HP": "15*",
        "ATK": "3",
        "SCH": "1",
        "Stage": "2"
    },
    "traits": [
        "BRUTE",
        "CRIMINAL"
    ],
    "set_name": "Rhino",
    "text": "<b>When Revealed</b>: Search the encounter deck and discard pile for the Breakin' & Takin' side scheme and reveal it. Shuffle the encounter deck."
}
```

Script (`src/cards/pack/core/rhino/01095.py`) :

```python
# Source : src/cards/pack/core/rhino/01095.py
from . import *

# * Rhino (II)

def GetAbilities() -> Sequence['Ability']:

    def rhino(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterVillain)
        Unused(this)

        face = Search.EncounterCard(
            effect,
            include_discard_pile=True,
            name="Breakin' & Takin'",
            card_type=SchemeSide2,
        )
        if face:
            face.Reveal(None, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            rhino
        )
    ]
```


#### 8.2.3 Vilain étape 3 : When Revealed sur tous les héros (Toughness lu dans `desc`)

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01096",
    "type": "Villain",
    "name": "* Rhino",
    "subtitle": "",
    "desc": {
        "HP": "16*",
        "ATK": "4",
        "SCH": "1",
        "Toughness": "1",
        "Stage": "3"
    },
    "traits": [
        "BRUTE",
        "CRIMINAL"
    ],
    "set_name": "Rhino",
    "text": "Toughness. <i>(This character enter play with a tough status card.)</i>\n<b>When Revealed</b>: Stun each hero."
}
```

Script (`src/cards/pack/core/rhino/01096.py`) :

```python
# Source : src/cards/pack/core/rhino/01096.py
from . import *

# * Rhino (III)

def GetAbilities() -> Sequence['Ability']:

    def rhino(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterVillain)
        Unused(this)
        
        heroes = Worlds.GetOnFieldHeroes(effect)
        Faces.GiveStatus(heroes, "Stunned", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            rhino
        )
    ]
```


#### 8.2.4 Vilain fan-made qui se retourne au lieu d'être vaincu

Entrée de `data/cards.json` (pack `web_of_deceit`) :

```json
{
    "card_id": "wd001a",
    "type": "Villain",
    "name": "* Shocker",
    "subtitle": "",
    "desc": {
        "HP": "10",
        "ATK": "1",
        "SCH": "1",
        "Steady": "1"
    },
    "traits": [
        "CRIMINAL"
    ],
    "set_name": "Shocker",
    "text": "Steady.\n<b>When Defeated</b>: Remove 5 threat from a side scheme. Flip this card.",
    "custom": "Ripper3"
}
```

Script (`src/cards/pack/web_of_deceit/shocker/wd001a.py`) :

```python
# Source : src/cards/pack/web_of_deceit/shocker/wd001a.py
from . import *

# * Shocker (A)

def GetAbilities() -> Sequence['Ability']:

    def shocker(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(EncounterVillain)

        # « When Defeated: Remove 5 threat from a side scheme. Flip this card. »
        #
        # Shocker n'est JAMAIS vaincu pour de bon : le vaincre le retourne sur
        # sa face experte, et la partie ne se gagne que par The Long Night. On
        # interrompt donc la defaite au lieu de la laisser terminer la partie.
        message.SetBeInstead(effect)
        RetournerShocker(effect, this, 5)

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.ForcedInterrupt,
            "This",
            shocker,
        ),
    ]
```


(`RetournerShocker` est une fonction du `__init__.py` du set ; quand une
mécanique demande une aide partagée, décris-la et laisse Claude l'écrire.)

#### 8.2.5 Complot principal 1A : mise en place

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01116a",
    "type": "MainScheme",
    "name": "Underground Distribution",
    "subtitle": "",
    "desc": {
        "Stage": "1"
    },
    "traits": [],
    "set_name": "Klaw"
}
```

Script (`src/cards/pack/core/klaw/01116a.py`) :

```python
# Source : src/cards/pack/core/klaw/01116a.py
from . import *

# Underground Distribution - 1A

def GetAbilities() -> Sequence['Ability']:

    def underground_distribution(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)

        SetupCards.Reveal(
            effect,
            name="Defense Network",
            card_type=SchemeSide2,
        )

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            underground_distribution
        )
    ]
```


#### 8.2.6 Complot principal 1B : When Revealed

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01116b",
    "type": "MainScheme",
    "name": "Underground Distribution",
    "subtitle": "",
    "desc": {
        "StartingThreat": "0",
        "TargetThreat": "6*",
        "EscalationThreat": "1*",
        "Stage": "1"
    },
    "traits": [],
    "set_name": "Klaw",
    "text": "<b>When Revealed</b>: Discard cards from the encounter deck until a minion is discarded. Put that minion into play engaged with the first player."
}
```

Script (`src/cards/pack/core/klaw/01116b.py`) :

```python
# Source : src/cards/pack/core/klaw/01116b.py
from . import *

# Underground Distribution - 1B

def GetAbilities() -> Sequence['Ability']:

    def underground_distribution(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:

        first_player = Worlds.GetFirstPlayer(effect)

        face = Worlds.DiscardEncounterCardsUntil(
            effect,
            card_type=Minion
        )
        if face:
            face.PutIntoPlay(first_player, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            underground_distribution
        )
    ]
```


#### 8.2.7 Complot annexe : When Revealed avec menace par joueur (Hazard lu dans `desc`)

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01107",
    "type": "SideScheme",
    "name": "Breakin' & Takin'",
    "subtitle": "",
    "desc": {
        "Boost": "2",
        "Hazard": "1",
        "StartingThreat": "2"
    },
    "traits": [],
    "set_name": "Rhino",
    "text": "<b>When Revealed</b>: Place an additional 1 [per_hero] threat here.\n<i>(Hazard Icon: Deal +1 encounter card during the villain phase.)</i>"
}
```

Script (`src/cards/pack/core/rhino/01107.py`) :

```python
# Source : src/cards/pack/core/rhino/01107.py
from . import *

# Breakin' & Takin'

def GetAbilities() -> Sequence['Ability']:

    def breakin_and_takin(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)

        this.PlaceThreatOnSchemes([this], "1*", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            breakin_and_takin
        )
    ]
```


#### 8.2.8 Complot annexe avec Acceleration (lu dans `desc`)

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01109",
    "type": "SideScheme",
    "name": "Bomb Scare",
    "subtitle": "",
    "desc": {
        "Boost": "2",
        "Acceleration": "1",
        "StartingThreat": "2"
    },
    "traits": [],
    "set_name": "Bomb Scare",
    "text": "<b>When Revealed</b>: Place an additional 1 [per_hero] threat here.\n<i>(Acceleration Icon: Place +1 threat on the main scheme at the start of the villain phase.)</i>"
}
```

Script (`src/cards/pack/core/bomb_scare/01109.py`) :

```python
# Source : src/cards/pack/core/bomb_scare/01109.py
from . import *

# Bomb Scare

def GetAbilities() -> Sequence['Ability']:

    def bomb_scare(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)

        this.PlaceThreatOnSchemes([this], "1*", effect)


    return [
        AbilityFactory.WhenThisRevealed(
            None,
            bomb_scare
        ),
    ]
```


#### 8.2.9 Complot annexe avec Crisis seule : aucun script

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01108",
    "type": "SideScheme",
    "name": "Crowd Control",
    "subtitle": "",
    "desc": {
        "Boost": "2",
        "Crisis": "1",
        "StartingThreat": "2*"
    },
    "traits": [],
    "set_name": "Rhino",
    "text": "<i>(Crisis Icon: While this scheme is in play, you cannot remove threat from the main scheme.)</i>"
}
```

Aucun script : tout est lu dans `desc`.


#### 8.2.10 Complot annexe : Hinder, Victory 0, When Defeated

Entrée de `data/cards.json` (pack `gmw`) :

```json
{
    "card_id": "16127",
    "type": "SideScheme",
    "name": "Hujahdarian Monarch Egg",
    "subtitle": "",
    "desc": {
        "Boost": "1",
        "Acceleration": "1",
        "StartingThreat": "3",
        "Hinder": "2*",
        "Victory": "0"
    },
    "traits": [],
    "set_name": "Galactic Artifacts",
    "text": "Hinder 2[per_hero]. Victory 0.\r\n<b>When Defeated:</b> The player who defeated this scheme may ready their identity."
}
```

Script (`src/cards/pack/gmw/galactic_artifacts/16127.py`) :

```python
# Source : src/cards/pack/gmw/galactic_artifacts/16127.py
from . import *

# Hujahdarian Monarch Egg

def GetAbilities() -> Sequence['Ability']:

    def hujahdarian_monarch_egg(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)

        player = message.killer.GetControlBy()
        if Player.IsType(player):
            player.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Ready your identity",
                    lambda targets:
                        Faces.ReadyAll(targets, effect)
                ).SetTarget("YourIdentity", canbe_ready=True)
            )


    return [
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            hujahdarian_monarch_egg,
        ),
    ]
```


#### 8.2.11 Sbire avec Guard seule : aucun script

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01101",
    "type": "Minion",
    "name": "Hydra Mercenary",
    "subtitle": "",
    "desc": {
        "HP": "3",
        "ATK": "1",
        "SCH": "0",
        "Boost": "1",
        "Guard": "1"
    },
    "traits": [
        "HYDRA"
    ],
    "set_name": "Rhino",
    "text": "Guard. <i>(While this minion is engaged with you, you cannot attack the villain.)</i>"
}
```

Aucun script : tout est lu dans `desc`.


#### 8.2.12 Sbire : When Revealed

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01103",
    "type": "Minion",
    "name": "* Shocker",
    "subtitle": "",
    "desc": {
        "HP": "3",
        "ATK": "2",
        "SCH": "1",
        "Boost": "2"
    },
    "traits": [
        "CRIMINAL"
    ],
    "set_name": "Rhino",
    "text": "<b>When Revealed</b>: Deal 1 damage to each hero."
}
```

Script (`src/cards/pack/core/rhino/01103.py`) :

```python
# Source : src/cards/pack/core/rhino/01103.py
from . import *

# * Shocker

def GetAbilities() -> Sequence['Ability']:

    def shocker(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)

        heroes = Worlds.GetOnFieldHeroes(effect)
        this.DealDamage(heroes, 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            shocker
        )
    ]
```


#### 8.2.13 Sbire : When Defeated (Patrol et Vulnerable lus dans `desc`)

Entrée de `data/cards.json` (pack `fne`) :

```json
{
    "card_id": "60103",
    "type": "Minion",
    "name": "Security Guard",
    "subtitle": "",
    "desc": {
        "HP": "4",
        "ATK": "2",
        "SCH": "0",
        "Boost": "1",
        "Patrol": "1",
        "Vulnerable": "1"
    },
    "traits": [
        "CIVILIAN",
        "INFLUENCED"
    ],
    "set_name": "Purple Man",
    "text": "Patrol. Vulnerable.\n<b>When Defeated</b>: Discard the ally with the highest ATK <i>(among allies)</i> in play."
}
```

Script (`src/cards/pack/fne/purple_man/60103.py`) :

```python
# Source : src/cards/pack/fne/purple_man/60103.py
from . import *

# Security Guard (CIVILIAN, INFLUENCED) — Patrol, Vulnerable : bases.
# When Defeated: Discard the ally with the highest ATK (among allies) in play.

def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        allie = Filter.One(Worlds.GetOnFieldAllies(effect), effect, highest_atk=True)
        if allie:
            Faces.DiscardAll([allie], effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
```


#### 8.2.14 Sbire avec Surge (lu dans `desc`) et [star] Boost : entrer en jeu

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01121",
    "type": "Minion",
    "name": "Weapons Runner",
    "subtitle": "",
    "desc": {
        "HP": "2",
        "ATK": "1",
        "SCH": "1",
        "Surge": "1"
    },
    "traits": [
        "MERCENARY"
    ],
    "set_name": "Klaw",
    "text": "Surge. <i>(After this card is revealed, reveal 1 additional encounter card.)</i>\n<hr />\n[star] <b>Boost</b>: Put Weapons Runner into play engaged with you."
}
```

Script (`src/cards/pack/core/klaw/01121.py`) :

```python
# Source : src/cards/pack/core/klaw/01121.py
from . import *

# Weapons Runner

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            PutThisIntoPlay,
        )
    ]
```


#### 8.2.15 Sbire avec Patrol, [star] Boost conditionnel (si l'activation est une manigance)

Entrée de `data/cards.json` (pack `gmw`) :

```json
{
    "card_id": "16119",
    "type": "Minion",
    "name": "Badoon Lieutenant",
    "subtitle": "",
    "desc": {
        "HP": "6",
        "ATK": "2",
        "SCH": "2",
        "Boost": "1",
        "Patrol": "1"
    },
    "traits": [
        "BADOON"
    ],
    "set_name": "Band Of Badoon",
    "text": "Patrol. <i>(While this minion is engaged with you, you cannot thwart the main scheme.)</i>\r\n<hr />\r\n[star] <b>Boost</b>: If this activation is a scheme, this card gets +2 boost icons ([boost][boost]) for this activation."
}
```

Script (`src/cards/pack/gmw/band_of_badoon/16119.py`) :

```python
# Source : src/cards/pack/gmw/band_of_badoon/16119.py
from . import *

# Badoon Lieutenant

def GetAbilities() -> Sequence['Ability']:

    def badoon_lieutenant_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        message.GainBoostIcon(2, effect)


    return [
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            badoon_lieutenant_boost,
            during_scheme=True
        ),
    ]
```


#### 8.2.16 Sbire avec Guard et Stalwart, [star] Boost conditionnel (si c'est une attaque)

Entrée de `data/cards.json` (pack `gmw`) :

```json
{
    "card_id": "16133",
    "type": "Minion",
    "name": "Kree Lieutenant",
    "subtitle": "",
    "desc": {
        "HP": "7",
        "ATK": "1",
        "SCH": "2",
        "Guard": "1",
        "Stalwart": "1"
    },
    "traits": [
        "KREE",
        "SOLDIER"
    ],
    "set_name": "Kree Militants",
    "text": "Guard. Stalwart. <i>(This character cannot be stunned or confused.)</i>\r\n<hr />\r\n[star] <b>Boost</b>: If this activation is an attack, this card gets +3 boost icons ([boost][boost][boost]) for this activation."
}
```

Script (`src/cards/pack/gmw/kree_militants/16133.py`) :

```python
# Source : src/cards/pack/gmw/kree_militants/16133.py
from . import *

# Kree Lieutenant

def GetAbilities() -> Sequence['Ability']:

    def kree_lieutenant_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        message.GainBoostIcon(3, effect)


    return [
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            kree_lieutenant_boost,
            during_attack=True,
        ),
    ]
```


#### 8.2.17 Sbire : capacité [star] permanente et [star] Boost

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01132",
    "type": "Minion",
    "name": "* Melter",
    "subtitle": "",
    "desc": {
        "HP": "5",
        "ATK": "3",
        "SCH": "1"
    },
    "traits": [
        "MASTERS OF EVIL"
    ],
    "set_name": "Masters of Evil",
    "text": "[star] The engaged player must defend against Melter's attacks with an ally they control, if able.\n<hr />\n[star] <b>Boost</b>: Exhaust each ally you control."
}
```

Script (`src/cards/pack/core/masters_of_evil/01132.py`) :

```python
# Source : src/cards/pack/core/masters_of_evil/01132.py
from . import *

# * Melter

def GetAbilities() -> Sequence['Ability']:

    def melter_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        player = message.GetToPlayer()

        Faces.ExhaustAll(player.GetControlAllies(), effect)

    return [
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            melter_boost
        ),
        AbilityFactory.WhenUnitAttackYou(
            AbilityType.NonKeywordStar,
            "This",
            lambda effect, message:
                message.MustDefendWithAlly(effect),
        )
    ]
```


#### 8.2.18 Sbire : Forced Response après avoir manigancé, jeton d'accélération

Entrée de `data/cards.json` (pack `fne`) :

```json
{
    "card_id": "60200",
    "type": "Minion",
    "name": "* Ivan Banionis",
    "subtitle": "",
    "desc": {
        "HP": "5",
        "ATK": "2",
        "SCH": "0",
        "Boost": "2",
        "Teamwork": "TRACKSUIT"
    },
    "traits": [
        "CRIMINAL",
        "TRACKSUIT"
    ],
    "set_name": "Tracksuit Mafia",
    "text": "Teamwork ([[Tracksuit]]).\n<b>When Revealed</b>: Place 1 acceleration token here.\n[star] <b>Forced Response</b>: After Ivan Banionis schemes, place 1 acceleration token here."
}
```

Script (`src/cards/pack/fne/tracksuit_mafia/60200.py`) :

```python
# Source : src/cards/pack/fne/tracksuit_mafia/60200.py
from . import *

# * Ivan Banionis (CRIMINAL, TRACKSUIT) — Teamwork (TRACKSUIT) : base desc.
# When Revealed: Place 1 acceleration token here.
# [star] Forced Response: After Ivan Banionis schemes, place 1 acceleration
#   token here.
# PlaceAccelerationToken (50081 Abduct Superhumans).

def GetAbilities() -> Sequence['Ability']:

    def accelere(effect: 'Effect', message: 'Message') -> None:
        this = effect.this.CastTo(Minion)
        this.PlaceAccelerationToken(1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, accelere),
        AbilityFactory.AfterUnitSchemeEnd(AbilityType.ForcedResponse, "This", accelere),
    ]
```


#### 8.2.19 Sbire : « X cannot take damage » (Guard lu dans `desc`)

Entrée de `data/cards.json` (pack `fne`) :

```json
{
    "card_id": "60063",
    "type": "Minion",
    "name": "Kingpin's Henchman",
    "subtitle": "",
    "desc": {
        "HP": "4",
        "ATK": "2",
        "SCH": "1",
        "Boost": "1",
        "Guard": "1"
    },
    "traits": [
        "CRIMINAL"
    ],
    "set_name": "Echo Nemesis",
    "text": "Guard.\nKingpin cannot take damage."
}
```

Script (`src/cards/pack/fne/echo_nemesis/60063.py`) :

```python
# Source : src/cards/pack/fne/echo_nemesis/60063.py
from . import *
def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.UnitCannotTakeDamageWhile(AbilityType.NonKeyword, CardFinder(name='Kingpin'))]
```


#### 8.2.20 Sbire : « Choose one » sur la révélation

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01110",
    "type": "Minion",
    "name": "Hydra Bomber",
    "subtitle": "",
    "desc": {
        "HP": "2",
        "ATK": "1",
        "SCH": "1",
        "Boost": "1"
    },
    "traits": [
        "HYDRA"
    ],
    "set_name": "Bomb Scare",
    "text": "<b>When Revealed</b>: Choose to either take 2 damage or place 1 threat on the main scheme."
}
```

Script (`src/cards/pack/core/bomb_scare/01110.py`) :

```python
# Source : src/cards/pack/core/bomb_scare/01110.py
from . import *

# Hydra Bomber

def GetAbilities() -> Sequence['Ability']:

    def hydra_bomber(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        player = message.GetToPlayer()

        def take_2_damage(targets: Sequence['CardFace']) -> None:
            for target in targets:
                if Unit2.IsType(target):
                    target.TakeDamage(this, 2, effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Take 2 damage",
                take_2_damage
            ).SetTarget("YourIdentity"),
            AbilityFactory.ForChoiceAbility(
                "Place 1 threat on the main scheme",
                lambda targets:
                    this.PlaceThreatOnSchemes(targets, 1, effect)
            ).SetTarget(MainScheme, can_place_threat=True)
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            hydra_bomber
        )
    ]
```


#### 8.2.21 Traîtrise : gagne Surge si rien n'est soigné

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01104",
    "type": "Treachery",
    "name": "Hard to Keep Down",
    "subtitle": "",
    "desc": {},
    "traits": [],
    "set_name": "Rhino",
    "text": "<b>When Revealed</b>: Rhino heals 4 damage. If no damage was healed this way, this card gains surge."
}
```

Script (`src/cards/pack/core/rhino/01104.py`) :

```python
# Source : src/cards/pack/core/rhino/01104.py
from . import *

# Hard to Keep Down

def GetAbilities() -> Sequence['Ability']:

    def hard_to_keep_down(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        if this.HealthUnits(effect.targets, 4, effect):
            pass
        else:
            this.GainSurge(1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            hard_to_keep_down
        ).SetTarget(Villain)
    ]
```


#### 8.2.22 Traîtrise : When Revealed différent en héros et en alter-ego

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01106",
    "type": "Treachery",
    "name": "Stampede",
    "subtitle": "",
    "desc": {
        "Boost": "1"
    },
    "traits": [],
    "set_name": "Rhino",
    "text": "<b>When Revealed (Alter-Ego)</b>: This card gains surge.\n<b>When Revealed (Hero)</b>: Rhino attacks you. If a character is damaged by this attack, that character is stunned."
}
```

Script (`src/cards/pack/core/rhino/01106.py`) :

```python
# Source : src/cards/pack/core/rhino/01106.py
from . import *

# Stampede

def GetAbilities() -> Sequence['Ability']:

    def stampede_hero(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        player = message.GetToPlayer()

        villain = Worlds.FindCardOnField(
            effect,
            name="Rhino",
            card_type=Villain
        )

        if villain:
            villain.DoAttackYou(player, effect,
                if_characters_damaged_by_this=lambda units:
                    Faces.GiveStatus(units, "Stunned", effect)
            )

    return [
        AbilityFactory.WhenThisRevealed(
            "Hero",
            stampede_hero
        ),
        AbilityFactory.WhenThisRevealed(
            "Alter-Ego",
            ThisCardGainSurge
        )
    ]
```


#### 8.2.23 Traîtrise : choix avec coût en ressources, et [star] Boost

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01123",
    "type": "Treachery",
    "name": "Sonic Boom",
    "subtitle": "",
    "desc": {},
    "traits": [],
    "set_name": "Klaw",
    "text": "<b>When Revealed</b>: Either spend [energy] [mental] [physical] resources or exhaust each character you control.\n<hr />\n[star] <b>Boost</b>: If this activation deals damage to you, exhaust your hero."
}
```

Script (`src/cards/pack/core/klaw/01123.py`) :

```python
# Source : src/cards/pack/core/klaw/01123.py
from . import *

# Sonic Boom

def GetAbilities() -> Sequence['Ability']:

    def sonic_boom_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        player = message.GetToPlayer()

        def exhaust_each_characters(targets: Sequence['CardFace']) -> None:
            Faces.ExhaustAll(targets, effect)

        player.ChooseAbilities(
            effect,
            # TODO: Sonic Boom is a choice, but you must choose an option that you can fulfill. If you cannot fulfill either option, then you must do as much as you can, which typically means discarding one or two different resource icons from your hand.
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("YBR"),
            ),
            AbilityFactory.ForChoiceAbility(
                "Exhaust each character you control",
                exhaust_each_characters
            ).SetTarget("YouControlUnit", range="All", canbe_exhaust=True)
        )

    def sonic_boom_boost(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        # if message.deal_damage > 0 and not message.trigger.IsDefeated():
        this = effect.this.CastTo(Treachery)
        Unused(this)

        player = message.trigger.GetControlByPlayer()
        if player.IsHero():
            Faces.ExhaustAll([player.GetHero()], effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            sonic_boom_revealed
        ),
        AbilityFactory.BoostIfThisActivationDealsDamage(
            "You",
            sonic_boom_boost,
        )
    ]
```


#### 8.2.24 Traîtrise standard : le vilain manigance

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01186",
    "type": "Treachery",
    "name": "Advance",
    "subtitle": "",
    "desc": {},
    "traits": [],
    "set_name": "Standard",
    "text": "<b>When Revealed</b>: The villain schemes."
}
```

Script (`src/cards/pack/core/standard/01186.py`) :

```python
# Source : src/cards/pack/core/standard/01186.py
from . import *

# Advance

def GetAbilities() -> Sequence['Ability']:

    def advance(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        player = message.GetToPlayer()
        villain = Worlds.FindVillain(effect)
        if villain:
            villain.DoSchemes(player, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            advance
        )
    ]
```


#### 8.2.25 Traîtrise du set expert

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01191",
    "type": "Treachery",
    "name": "Exhaustion",
    "subtitle": "",
    "desc": {
        "Boost": "2",
        "Surge": "1"
    },
    "traits": [],
    "set_name": "Expert",
    "text": "Surge.\n<b>When Revealed</b>: Exhaust your identity card."
}
```

Script (`src/cards/pack/core/expert/01191.py`) :

```python
# Source : src/cards/pack/core/expert/01191.py
from . import *

# Exhaustion

def GetAbilities() -> Sequence['Ability']:

    def exhaustion(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        player = message.GetToPlayer()
        identity = player.GetIdentity()
        Faces.ExhaustAll([identity], effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            exhaustion
        )
    ]
```


#### 8.2.26 Attachement : prend les dégâts à la place du vilain, compteurs

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01098",
    "type": "Attachment",
    "name": "Armored Rhino Suit",
    "subtitle": "",
    "desc": {},
    "traits": [
        "ARMOR"
    ],
    "set_name": "Rhino",
    "text": "Attach to Rhino.\n<b>Forced Interrupt</b>: When any amount of damage would be dealt to Rhino, place it here instead. Then, if there is at least 5 damage here, discard Armored Rhino Suit."
}
```

Script (`src/cards/pack/core/rhino/01098.py`) :

```python
# Source : src/cards/pack/core/rhino/01098.py
from . import *

# Armored Rhino Suit

def GetAbilities() -> Sequence['Ability']:

    def armored_rhino_suit(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Attachment)
        damage = message.PreventDamage("All", effect)
        Faces.PlaceCountersOn([this], damage, 'damage', effect)
        if this.GetCounters('damage') >= 5:
            Faces.DiscardAll([this], effect)


    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name="Rhino")
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            CardFinder(name="Rhino"),
            armored_rhino_suit
        )
    ]
```


#### 8.2.27 Attachement : [star] Interruption Forcée, puis effet différé

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01099",
    "type": "Attachment",
    "name": "Charge",
    "subtitle": "",
    "desc": {
        "Boost": "2",
        "ATK+": "3"
    },
    "traits": [],
    "set_name": "Rhino",
    "text": "Attach to Rhino.\n[star] <b>Forced Interrupt</b>: When Rhino attacks, the attack gains overkill. <i>(Excess damage to an ally from this attack is dealt to that ally's controller.)</i> At the end of this attack, discard Charge."
}
```

Script (`src/cards/pack/core/rhino/01099.py`) :

```python
# Source : src/cards/pack/core/rhino/01099.py
from . import *

# Charge

def GetAbilities() -> Sequence['Ability']:

    def charge(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(this)

        message.GainOverKill(effect)

        def disacard_this() -> None:
            Faces.DiscardAll([this], effect)

        RunAt.AfterEnemyActivationEnd(effect, message, disacard_this)


    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name="Rhino")
        ),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            CardFinder(name="Rhino"),
            charge
        )
    ]
```


#### 8.2.28 Attachement : Hero Action payante pour le défausser

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01100",
    "type": "Attachment",
    "name": "Enhanced Ivory Horn",
    "subtitle": "",
    "desc": {
        "Boost": "2",
        "ATK+": "1"
    },
    "traits": [
        "WEAPON"
    ],
    "set_name": "Rhino",
    "text": "Attach to Rhino.\n<b>Hero Action</b>: Spend [physical] [physical] [physical] resources → discard this card"
}
```

Script (`src/cards/pack/core/rhino/01100.py`) :

```python
# Source : src/cards/pack/core/rhino/01100.py
from . import *

# Enhanced Ivory Horn

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name="Rhino")
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("RRR"))
    ]
```


#### 8.2.29 Attachement : donne Retaliate au vilain

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01119",
    "type": "Attachment",
    "name": "Solid-Sound Body",
    "subtitle": "",
    "desc": {
        "Boost": "3"
    },
    "traits": [
        "CONDITION"
    ],
    "set_name": "Klaw",
    "text": "Attach to Klaw.\nKlaw gains retaliate 1. <i>(After this character is attacked, deal 1 damage to the attacking character.)</i>\n<b>Hero Action</b>: Spend [energy] [mental] [physical] resources → discard this card."
}
```

Script (`src/cards/pack/core/klaw/01119.py`) :

```python
# Source : src/cards/pack/core/klaw/01119.py
from . import *

# Solid-Sound Body

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name="Klaw")
        ),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Klaw"),
            retaliate=1,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("YBR"))
    ]
```


#### 8.2.30 Set némésis : complot annexe avec Acceleration, When Revealed et When Defeated

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01166",
    "type": "SideScheme",
    "name": "Highway Robbery",
    "subtitle": "",
    "desc": {
        "Boost": "3",
        "Acceleration": "1",
        "StartingThreat": "3*"
    },
    "traits": [],
    "set_name": "Spider-Man Nemesis",
    "text": "<b>When Revealed</b>: Each player places a random card from their hand facedown here.\n<b>When Defeated</b>: Return each facedown card here to its owner's hand."
}
```

Script (`src/cards/pack/core/spider_man_nemesis/01166.py`) :

```python
# Source : src/cards/pack/core/spider_man_nemesis/01166.py
from . import *

# Highway Robbery

def GetAbilities() -> Sequence['Ability']:

    def highway_robbery_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        def action(player: 'Player'):
            return player.GetRandomHandCards(1)

        faces: List['CardFace'] = Players.ForEachPlayer(effect, action, [])

        this.PlaceCardHere(faces, False, effect)

    def highway_robbery_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        
        faces = this.GetPlacedCardArea().Get(True)
        Faces.ReturnToHand(faces, "Owner", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            highway_robbery_revealed
        ),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            highway_robbery_defeated
        )
    ]
```


#### 8.2.31 Set némésis : traîtrise avec [star] Boost « si cette activation inflige des dégâts »

Entrée de `data/cards.json` (pack `core`) :

```json
{
    "card_id": "01168",
    "type": "Treachery",
    "name": "Sweeping Swoop",
    "subtitle": "",
    "desc": {},
    "traits": [],
    "set_name": "Spider-Man Nemesis",
    "text": "<b>When Revealed</b>: Stun your hero. If Vulture is in play, this card gains surge.\n<hr />\n[star] <b>Boost</b>: If this activation deals damage to a friendly character, stun that character."
}
```

Script (`src/cards/pack/core/spider_man_nemesis/01168.py`) :

```python
# Source : src/cards/pack/core/spider_man_nemesis/01168.py
from . import *

# Sweeping Swoop

def GetAbilities() -> Sequence['Ability']:

    def sweeping_swoop(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        player = message.GetToPlayer()
        if player.IsHero():
            Faces.GiveStatus([player.GetHero()], "Stunned", effect)

        vulture = Worlds.FindCardOnField(
            effect,
            name="Vulture",
            card_type=Minion
        )
        if vulture:
            this.GainSurge(1, effect)

    def sweeping_swoop_boost(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        Faces.GiveStatus([message.trigger], "Stunned", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            sweeping_swoop
        ),
        AbilityFactory.BoostIfThisActivationDealsDamage(
            Friend,
            sweeping_swoop_boost
        ),
    ]
```


#### 8.2.32 Environnement : Alter-Ego Action, coût en inclinaison ciblée, compteurs

Entrée de `data/cards.json` (pack `fne`) :

```json
{
    "card_id": "60152",
    "type": "Environment",
    "name": "Daily Bugle",
    "subtitle": "",
    "desc": {},
    "traits": [],
    "set_name": "Stop the Presses!",
    "text": "<b>Alter-Ego Action</b>: Exhaust a [[Daily Bugle]] support you control → place 1 stamina counter on that support. <i>(Any player can do this.)</i>"
}
```

Script (`src/cards/pack/fne/stop_the_presses/60152.py`) :

```python
# Source : src/cards/pack/fne/stop_the_presses/60152.py
from . import *

# Daily Bugle (environment)
# Alter-Ego Action: Exhaust a DAILY BUGLE support you control -> place 1
#   stamina counter on that support. (Any player can do this.)
# CostFunc.Exhaust(finder) puis `return_exhausted_cards` pour viser CE soutien.

def GetAbilities() -> Sequence['Ability']:
    inclinaison = CostFunc.Exhaust(CardFinder(trait="DAILY BUGLE", card_type=Support))

    def recharge(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        for face in inclinaison.return_exhausted_cards:
            Faces.PlaceCountersOn([face], 1, 'stamina', effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, recharge)
            .SetName("Exhaust a Daily Bugle support you control: place 1 stamina counter on it")
            .SetCostFunc(inclinaison),
    ]
```


#### 8.2.33 Environnement : entre en jeu avec un compteur, Action pour n'importe quel joueur

Entrée de `data/cards.json` (pack `next_evol`) :

```json
{
    "card_id": "40191b",
    "type": "Environment",
    "name": "Safehouse Established",
    "subtitle": "",
    "desc": {},
    "traits": [],
    "set_name": "Next Evolution Campaign",
    "text": "Enters play with 1 safehouse counter on it.\n<b>Action</b>: Remove 1 safehouse counter from here → the first player puts the Safehouse support into play under their control. <i>(Safehouse is a campaign card.)</i>"
}
```

Script (`src/cards/pack/next_evol/next_evolution_campaign/40191b.py`) :

```python
# Source : src/cards/pack/next_evol/next_evolution_campaign/40191b.py
from . import *
def GetAbilities() -> Sequence['Ability']:
    def safehouse_established(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Environment)
        Unused(this)
        player = Worlds.GetFirstPlayer(effect)
        card = CardFactory.GenerateCard('40197', player.additional_discard_pile, effect.world)
        card.face.CastTo(Support).PutIntoPlay(player, effect, under_control=True)
    return [AbilityFactory.ThisEnterPlayWithCounters(1, 'safehouse'),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, safehouse_established).SetCostFunc(CostFunc.Counter('This', 1, 'safehouse')).AnyPlayerCanDoThis()]
```


#### 8.2.34 Environnement : se retourne à N compteurs par joueur

Entrée de `data/cards.json` (pack `mojo`) :

```json
{
    "card_id": "39003a",
    "type": "Environment",
    "name": "The Champion",
    "subtitle": "",
    "desc": {},
    "traits": [
        "BOOING CROWD"
    ],
    "set_name": "Magog",
    "text": "If there are at least 5[per_hero] ratings counters here, flip this environment <i>(without removing ratings counters)</i>."
}
```

Script (`src/cards/pack/mojo/magog/39003a.py`) :

```python
# Source : src/cards/pack/mojo/magog/39003a.py
from . import *

# The Champion

def GetAbilities() -> Sequence['Ability']:

    def the_champion_revealed(effect: 'Effect', message: 'Message.AfterCardPlacedCounter') -> None:
        this = effect.this.CastTo(Environment)
        Unused(this)

        this.card.Flip(effect)


    return [
        AbilityFactory.IfThereAreAtLeastCounterHere(
            "5*",
            'ratings',
            the_champion_revealed
        ),
    ]
```


#### 8.2.35 Environnement avec Setup : mise en place, fin de phase, victoire

Entrée de `data/cards.json` (pack `fne`) :

```json
{
    "card_id": "60112",
    "type": "Environment",
    "name": "Disturbed Psyche",
    "subtitle": "",
    "desc": {
        "Setup": "1"
    },
    "traits": [],
    "set_name": "Typhoid Mary",
    "text": "Setup.\n<b>Setup</b>: Put the villain into play on a random side <i>(and reveal it)</i>.\n<b>Forced Interrupt</b>: When the villain phase ends, flip the villain.\n<b>If there are 3 or more tokens here, the players win the game!</b>"
}
```

Script (`src/cards/pack/fne/typhoid_mary/60112.py`) :

```python
# Source : src/cards/pack/fne/typhoid_mary/60112.py
from . import *

# Disturbed Psyche (environment) — Setup (base desc : commence en jeu).
# Setup: Put the villain into play on a random side (and reveal it).
# Forced Interrupt: When the villain phase ends, flip the villain.
# If there are 3 or more tokens here, the players win the game!
#
# Le scenario met deja le vilain en jeu (stade unique 60110a / 60111a) : le
# Setup se contente de le retourner une fois sur deux (Rand), la revelation
# etant celle de la mise en place. ⚠ Hors de portee du harnais (WhenGameWouldBegin
# part une fois, avant lui) : verificateur dedie `fne_setup_psyche`.
# Retournement : card.Flip (modele 45101a),
# a la fin de la phase du mechant (WhenPhaseEnd "Villain"). Victoire :
# Worlds.SetGameOver(True) (32130), verifiee a chaque jeton pose ici.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        vilain = TrouverMary(effect)
        if vilain and Rand.RandomChoice([True, False], effect):
            vilain.card.Flip(effect)

    def fin_de_phase(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        vilain = TrouverMary(effect)
        if vilain:
            vilain.card.Flip(effect)

    def jeton(effect: 'Effect', message: 'Message.AfterCardPlacedToken') -> None:
        VerifierVictoire(effect)

    return [
        # Une carte Setup (desc) n'a PAS de message WhenCardSetup (envoye pour
        # les complots) : sa capacite Setup vit sur AfterGameSetup (cc001, 58031).
        AbilityFactory.AfterGameSetup(mise_en_place),
        AbilityFactory.WhenPhaseEnd(AbilityType.ForcedInterrupt, "Villain", fin_de_phase),
        AbilityFactory.AfterCardPlacedToken(AbilityType.ForcedResponse, "This", None, jeton),
    ]
```


`TrouverMary` et `VerifierVictoire` sont des fonctions du `__init__.py` du
set (`fne/typhoid_mary/__init__.py`) :

```python
# Source : src/cards/pack/fne/typhoid_mary/__init__.py (lignes 12 à 47)
def TrouverMary(effect: 'Effect') -> 'Villain|None':
    """La face active, quelle qu'elle soit."""
    for nom in ("Typhoid Mary", "Bloody Mary"):
        v = Worlds.FindCardOnField(effect, name=nom, card_type=Villain)
        if v:
            return v
    return None


def TrouverDisturbedPsyche(effect: 'Effect') -> 'Environment|None':
    return Worlds.FindCardOnField(effect, name="Disturbed Psyche", card_type=Environment)


def TrouverMaryWalker(effect: 'Effect') -> 'Attachment|None':
    return Worlds.FindCardOnField(effect, name="Mary Walker", card_type=Attachment)


def MaryActive(effect: 'Effect', nom: str) -> bool:
    """« If Typhoid Mary is activating » / « If Bloody Mary is activating » :
    la face VISIBLE du vilain porte ce nom."""
    v = TrouverMary(effect)
    return v is not None and v.IsName(nom)


def JetonsPsyche(effect: 'Effect') -> int:
    env = TrouverDisturbedPsyche(effect)
    if env is None:
        return 0
    return env.GetTokens('damage') + env.GetTokens('threat')


def VerifierVictoire(effect: 'Effect') -> None:
    """If there are 3 or more tokens here, the players win the game!"""
    if JetonsPsyche(effect) >= 3 and not Worlds.IsGameOver(effect):
        Worlds.SetGameOver(True, effect)

```

#### 8.2.36 Attachement fan-made : condition ET coût d'une Hero Action

Entrée de `data/cards.json` (pack `web_of_deceit`) :

```json
{
    "card_id": "wd005",
    "type": "Attachment",
    "name": "Vibro-Shock Gauntlets",
    "subtitle": "",
    "desc": {
        "ATK+": "1",
        "Boost": "0"
    },
    "traits": [
        "TECH",
        "WEAPON"
    ],
    "set_name": "Shocker",
    "text": "Attach to Shocker.\n[star] <b>Forced Response</b>: After Shocker attacks and damages you, discard a card from your hand.\n<b>Hero Action</b>: Spend [physical] [mental] resources and remove a stunned or confused status card from Shocker → discard Vibro-Shock Gauntlets.\n<hr />\n[star] <b>Boost</b>: Reveal this card.",
    "custom": "Ripper3"
}
```

Script (`src/cards/pack/web_of_deceit/shocker/wd005.py`) :

```python
# Source : src/cards/pack/web_of_deceit/shocker/wd005.py
from . import *

# Vibro-Shock Gauntlets

def GetAbilities() -> Sequence['Ability']:

    def blesse(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        # « After Shocker attacks and damages you, discard a card from your hand. »
        joueur = message.attacked.GetControlByPlayer()
        joueur.AskDiscardFaces(joueur.hand_cards.Get(), (1, 1), effect)

    def shocker_sonne(effect: 'Effect') -> 'CardFace|None':
        # Le vilain de ce scenario EST Shocker : la carte lui est attachee.
        villain = effect.this.CastTo(Attachment).attached_face
        if villain is None:
            return None
        return villain if villain.HasStatus("Stunned") or villain.HasStatus("Confused") else None

    def a_un_statut(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        # ⚠ LA MOITIE DU COUT MANQUAIT. « and remove a stunned or confused
        # status card from Shocker » n'est pas un decor : c'est une CONDITION
        # (il faut d'abord le sonner ou le desorienter) et un COUT (le statut
        # part). Sans elle, les gants se defaussaient pour deux ressources.
        return shocker_sonne(effect) is not None

    def retirer_le_statut(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        villain = shocker_sonne(effect)
        if villain is None:
            return
        sonne = villain.HasStatus("Stunned")
        desoriente = villain.HasStatus("Confused")

        def enlever_sonne(cibles: 'Sequence[CardFace]') -> None:
            villain.DiscardStunned(effect, rule=1)

        def enlever_desoriente(cibles: 'Sequence[CardFace]') -> None:
            villain.DiscardConfused(effect, rule=1)

        # « a stunned OR confused status card » : quand les deux sont poses,
        # c'est au joueur de dire lequel il sacrifie — les deux ne bloquent pas
        # la meme chose.
        if sonne and desoriente:
            effect.GetInitiator().ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Remove the stunned status card", enlever_sonne),
                AbilityFactory.ForChoiceAbility(
                    "Remove the confused status card", enlever_desoriente),
            )
        elif sonne:
            enlever_sonne([])
        else:
            enlever_desoriente([])

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            Villain
        ),
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            "AttachedVillain",
            "YourIdentity",
            blesse
        ),
        # « Hero Action: Spend [physical][mental] resources and remove a stunned
        # or confused status card from Shocker -> discard Vibro-Shock Gauntlets. »
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
            conditions=[a_un_statut],
            ex_operation=retirer_le_statut,
        ).SetCost(Cost("RB")),
    ]
```


---

## 9. Pièges connus

Chacun de ces pièges a déjà cassé une carte du projet, souvent **sans aucune
erreur visible**.

1. **Le nom sans étoile.** `CardFinder(name="* X")` ne trouve jamais rien.
   Écris `name="X"`.
2. **Les mots-clés de `desc` ne se recodent pas** (3.3). Un script qui pose
   Toughness ou Surge en plus les applique deux fois.
3. **Une chaîne de ciblage inventée ne lève rien** : la carte est inerte.
4. **Un filtre va dans `conditions`, jamais en tête de l'opération.** Une
   capacité facultative (Response, Interrupt) est **proposée au joueur** dès
   que son message part ; un `return` en début d'opération ne l'empêche pas
   d'être proposée. Mets la condition dans `conditions=[lambda effect,
   message: ...]` (exemples 01006, 01033).
5. **« You » contre un nom propre.** « You get +1 » = l'identité (les deux
   faces) ; « Angela gets +1 » = la face héros seulement.
6. **`range=(0, n)`** rend la cible facultative : seulement pour « up to n ».
7. **Un seul `SetLabel`** par capacité ; deux libellés dans le même appel.
8. **Une seule `CanGenerateResources` par carte.**
9. **Le Setup d'une carte à mot-clé `Setup`** se code `AfterGameSetup`,
   jamais `WhenCardSetup` (réservé à la face 1A du complot principal).
10. **Une obligation révélée reste en jeu** si le script ne la défausse pas :
    code toutes les branches (défausser ou retirer de la partie).
11. **Les capacités d'une carte dans la pile de victoire ne se déclenchent
    jamais** (la carte est hors jeu). Un effet « tant que X est dans la pile
    de victoire » se pose sur une carte qui reste en jeu : `A_FAIRE_CLAUDE`.
12. **`printed_cost` est un objet, pas un nombre** : `face.printed_cost.val`.
13. **Réduction de coût : signe négatif.** Réduire de 1 = `-1`.
14. **Une recherche dans le deck sort la carte du deck** : l'opération doit
    la mettre quelque part (main, jeu, défausse).
15. **« A or B » sur un coût** = deux capacités, une par coût :
    `A_FAIRE_CLAUDE` si ce sont deux façons de **jouer** la carte (le moteur
    demande une inscription spéciale).
16. **Les dégâts consécutifs d'un allié** sont dans l'astérisque de
    `ATK`/`THW` (`"2*"`), pas dans un script.
17. **Ne code jamais la sortie de jeu d'une carte `Uses`** : le moteur la
    défausse au dernier compteur.
18. **Limite « once per round » sur un déclencheur de défaite**
    (`AfterUnitDefeatedUnit`) : piège moteur connu, signale-le en doute.
19. **Une capacité [star] sans « In expert mode »** est toujours active.
20. **Résultat de fin de partie** : lis `message.players_won`, jamais l'état
    du monde.

---

## 10. Format de livraison

### 10.1 Une carte = un bloc, toujours dans cet ordre

Gabarit vide :

````
### CARTE <card_id> : <nom>

**1. Entrée `data/cards.json`** (pack `<pack>`)

```json
{ ... }
```

**2. Script** : `src/cards/pack/<pack>/<set_nettoyé>/<card_id>.py`

```python
from . import *

# <nom>

def GetAbilities() -> Sequence['Ability']:
    ...
```

(ou : « Aucun script : tout est dans `desc`. »)

**3. Texte imprimé** (transcription exacte de la carte, en anglais)

> ...

**4. Doutes**

- ...
- Exemple réel le plus proche utilisé : `<card_id>` (pourquoi).
````

Exemple rempli (carte réelle 01110 Hydra Bomber) :

````
### CARTE 01110 : Hydra Bomber

**1. Entrée `data/cards.json`** (pack `core`)

```json
{
    "card_id": "01110",
    "type": "Minion",
    "name": "Hydra Bomber",
    "subtitle": "",
    "desc": {
        "HP": "2",
        "ATK": "1",
        "SCH": "1",
        "Boost": "1"
    },
    "traits": [
        "HYDRA"
    ],
    "set_name": "Bomb Scare",
    "text": "<b>When Revealed</b>: Choose to either take 2 damage or place 1 threat on the main scheme."
}
```

**2. Script** : `src/cards/pack/core/bomb_scare/01110.py`

```python
# Source : src/cards/pack/core/bomb_scare/01110.py
from . import *

# Hydra Bomber

def GetAbilities() -> Sequence['Ability']:

    def hydra_bomber(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        player = message.GetToPlayer()

        def take_2_damage(targets: Sequence['CardFace']) -> None:
            for target in targets:
                if Unit2.IsType(target):
                    target.TakeDamage(this, 2, effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Take 2 damage",
                take_2_damage
            ).SetTarget("YourIdentity"),
            AbilityFactory.ForChoiceAbility(
                "Place 1 threat on the main scheme",
                lambda targets:
                    this.PlaceThreatOnSchemes(targets, 1, effect)
            ).SetTarget(MainScheme, can_place_threat=True)
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            hydra_bomber
        )
    ]
```

**3. Texte imprimé**

> When Revealed: Choose to either take 2 damage or place 1 threat on the main scheme.

**4. Doutes**

- « take 2 damage » : appliqué à l'identité du joueur qui révèle, pas à un
  allié (lecture du texte, à confirmer si l'auteur pensait autrement).
- Exemple réel le plus proche utilisé : 01084 Nick Fury (choix entre
  plusieurs options avec `ChooseAbilities`).
````

### 10.2 Une campagne

Dans cet ordre :

1. **Préfixe et clé du pack** proposés (question à l'utilisateur si besoin).
2. **Liste des cartes** : tableau `card_id | nom | type | set` pour tout le
   pack, avant le détail.
3. **Un bloc par carte** (10.1).
4. **Un fichier par scénario**, standard puis `_expert`.
5. **Un fichier par set de rencontre**.
6. **`data/campagnes/<code>.json`** complet.
7. **`campaign.py`** complet.
8. **La table des clés du carnet** : `clé | écrite par (ligne de campaign.py) |
   lue par (ligne de campaign.py) | type | format`.
9. **La liste de tous les `A_FAIRE_CLAUDE`**, regroupés, avec la carte
   concernée.
10. **Les questions encore ouvertes**.

Pour une grosse campagne, livre **scénario par scénario** (un message par
scénario) plutôt que tout d'un coup.

---

## 11. Checklist d'auto-relecture avant livraison

Pour chaque carte :

- [ ] `card_id` unique, bon préfixe, bon suffixe de face.
- [ ] `name` : `"* "` si et seulement si la carte est unique.
- [ ] Toutes les valeurs de `desc` sont des **chaînes**.
- [ ] `"*"` de « par joueur » sur `HP` / menaces quand la carte l'imprime ;
      `"*"` de dégâts consécutifs sur `ATK` / `THW` d'un allié.
- [ ] Chaque mot-clé imprimé est dans `desc` (3.3), **et absent** du script.
- [ ] `RES` vérifiée par comparaison, pas à vue.
- [ ] `set_name` cohérent avec le dossier du script (2.1).
- [ ] Le texte imprimé est recopié avec ses balises (3.5).
- [ ] Chaque capacité imprimée a SA fabrique, du BON type
      (Forced / facultatif, Hero / Alter-Ego).
- [ ] Chaque « (Limit once per round.) » a son `.LimitOncePerRound()`.
- [ ] Chaque nombre du texte se retrouve dans le code, et réciproquement.
- [ ] Aucune fonction, aucune chaîne de ciblage absente de ce document.
- [ ] Aucun `CardFinder(name="* ...")`.
- [ ] Les filtres des capacités facultatives sont dans `conditions`.
- [ ] Chaque branche d'une obligation défausse ou retire la carte.
- [ ] Les doutes sont listés.

Pour un scénario et une campagne :

- [ ] Chaque carte de `encounters` / des sets existe dans tes blocs de cartes,
      avec le bon nombre d'exemplaires.
- [ ] Fichier standard ET fichier `_expert` (étapes de vilain décalées, set
      `expert` ajouté).
- [ ] Chaque clé du carnet est écrite ET lue.
- [ ] La face 1A de chaque complot porte `*CampaignSetup(n)` avec le bon `n`.

---

## 12. Ce que le GPT ne fait pas

- **Pas d'images** : ni scans, ni vignettes, ni illustrations.
- **Pas de tests** : Claude écrit et lance les tests en jeu.
- **Pas de modification du moteur** : rien hors des fichiers de cartes, de
  scénarios et de campagnes. Si le moteur doit changer, `A_FAIRE_CLAUDE`.
- **Pas de checksum** : les fichiers JSON du projet portent une clé
  `checksum` que Claude recalcule.
- **Pas de traduction française** des cartes : gérée à part.
- **Pas de déploiement**, pas de commit.
- **Pas de deck inventé** pour un héros : un deck n'est écrit que si l'auteur
  en fournit la liste.
