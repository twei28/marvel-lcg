---

## 6. Les scripts des cartes (`src/cards/pack/<pack>/…`)

Une carte dont le texte imprime une **capacité** (Action, Response, Interrupt, When Revealed, Boost étoilé,
effet `[star]`…) a un **script Python**. Une carte qui n'a que des statistiques et des mots-clés lus dans `desc`
(§4.5.2) **n'a pas de script**.

Ce chapitre reprend, tel quel, les paragraphes du kit de cartes (annexe A) qui disent **où ranger** un script et
**comment l'écrire** — après les avoir **recontrôlés contre le moteur actuel le 20/10/2026** (53 noms de
fabriques cités, tous trouvés ; tous les paramètres cités existent). Les sous-sections reprises gardent la
numérotation de l'annexe A (7.1 à 7.8).

### 6.1 Où ranger un script

{{SECTION:docs/reference/KIT-CHATGPT-CREATION.md|### 2.1 Où le moteur cherche|---|1}}

### 6.1 bis Les fichiers `__init__.py`

{{SECTION:docs/reference/KIT-CHATGPT-CREATION.md|### 2.2 Les deux fichiers|---|1}}

À retenir pour une campagne : le **`__init__.py` à la racine du pack** (`src/cards/pack/<pack>/__init__.py`)
commence par `from cards.pack import *` et porte les fonctions partagées par **plusieurs sets** ; chaque
**`__init__.py` de set** commence par `from cards.pack.<pack> import *` (voir `web_of_deceit/shocker/__init__.py`
dans les modèles) ou, pour un set sans helper, par `from cards.pack import *`. Un pack sans `__init__.py` à sa
racine ne peut pas importer ses propres helpers.

### 6.2 Ce que le script d'une carte peut utiliser (« la surface »)

Un script commence par `from . import *`. Ce `import *` apporte **tout** ce que `src/cards/pack/__init__.py`
expose (voir le fichier dans `commun/moteur/`) : `AbilityFactory`, `AbilityFactoryCampaign`, `AbilityType`,
`CardFinder`, `CostFunc`, `Cost`, `Resources`, `Message`, `Effect`, les types de cartes (`Villain`, `Minion`,
`MainScheme`, `Hero`, `AlterEgo`, `Upgrade`…), `Faces`, `FacesCounter`, `Filter`, `Effects`, `Search`, `Find`,
`Players`, `CampaignLog`, `Utility`, `RunAt`, `SetupCards`, `Worlds`, `AsideModularSet`, `Stores`,
`CardFactory`, `Deck`, `Select`, `Player`, `Scenario`, `Form`, `GameArea`, `OnEvent`, `Condition`, `Rand`,
`DamageProperty`, `PlayerCardImmunity`, `Villains`, `IsCounter`, `IsTrait`, plus quelques fonctions partagées
(`ShuffleThisCardIntoEncounter`, `ThisCardGainSurge`, `DiscardThisCard`, `RemoveThisFromGame`…).

**Ce qui n'est pas dans cette liste n'existe pas pour une carte.** L'index complet de l'API
(`annexes/I-index-api-moteur.md`) donne, pour chaque classe et fonction du moteur, ses arguments et sa première
ligne de commentaire : **c'est ta référence pour ne rien inventer.** Si tu cherches une fonction qui n'y est pas :
`A_FAIRE_CLAUDE`.

### 6.3 Squelette, types de capacité, fabriques, coûts, cibles, opérations (annexe A, §7)

{{SECTION:docs/reference/KIT-CHATGPT-CREATION.md|### 7.1 Squelette|## 8. Catalogue|1}}

### 6.4 Le catalogue d'exemples réels (annexe A, §8) : où trouver la carte modèle

L'annexe A contient **67 exemples réels** : l'entrée JSON et le script de la carte, côte à côte. **Avant d'écrire
une capacité, cherche son équivalent dans cette liste**, puis lis la carte modèle (le `card_id` est donné) dans
le dossier `modeles/` ou dans l'annexe. Index :

{{TITRES:docs/reference/KIT-CHATGPT-CREATION.md|## 8. Catalogue|## 9. Pièges connus}}

L'annexe B (`annexes/B-recettes-moteur.md`, ~1 800 lignes) est l'index **mécanique imprimée → fabrique + carte
modèle + piège** : c'est la première chose à ouvrir devant une mécanique inhabituelle (scénario à plusieurs
vilains, vilain qui se retourne, jeton maison, paquet de scénario, icône de complot dynamique…). Les **fiches de
mots-clés** (annexe C, `mots-cles/`) disent, pour chaque mot-clé officiel **ou maison**, ce que le moteur en
fait ; **un mot-clé rencontré sur une carte s'ouvre avant d'écrire une ligne de code** ; absent → tu écris
`A_FAIRE_CLAUDE` et tu poses la question.

### 6.5 Les capacités propres à un scénario : ce qui se pose où

| Ce que le texte dit | Où et comment |
|---|---|
| **Setup** du complot principal (face 1A) : « Setup : … » | `AbilityFactory.WhenCardSetup("This", opération)` sur la **face 1A** du complot principal du scénario. **Ce n'est PAS `AfterGameSetup`**, réservé aux cartes à mot-clé `Setup` dans `desc`. |
| **When Revealed** d'un complot, d'un sbire, d'une traîtrise | `AbilityFactory.WhenThisRevealed(None, opération)` ; `None`, `"Hero"` ou `"Alter-Ego"` pour une condition de forme. |
| **[star] Boost : …** | `AbilityFactory.WhenCardBecomeBoost(...)`. |
| **When Defeated** d'un personnage / d'un complot | `WhenUnitBeDefeated(AbilityType.WhenDefeated, …)` / `WhenSchemeBeDefeated(AbilityType.WhenDefeated, …)`. |
| Une capacité **imprimée sur le vilain** valable pour plusieurs stades | une fonction du `__init__.py` du set, appelée par chaque script de stade (modèle : `core/klaw/__init__.py`). |
| **Branchement du carnet** (la face 1A appelle la campagne) | `return [*CampaignSetup(niveau), …]` : voir §7.3. |
| Mise en jeu d'une carte à la **fin** de mise en place | `RunAt` / `AbilityFactoryCampaign.WhenCampaignSetupAfterMulligans` (§7). |
| Le vilain avance de stade ; le complot avance | gérés par le moteur ; une capacité « Advance » se fait par `Puzzle`/`Scenario` (voir annexe B, « avancée de stade »). |
| **Expert seulement** (« In expert mode… ») | `AbilityFactory.ExpertModeOnly()` / `AbilityFactory.StandardModeOnly()` **portés par la carte** ; ou `Worlds.IsExpert(effect)` dans une condition. **Ne réimplémente jamais le choix de face selon le mode à la mise en place** : la carte s'en charge (voir §14, piège « Public Outcry »). |

### 6.6 Pièges des scripts (annexe A, §9)

{{SECTION:docs/reference/KIT-CHATGPT-CREATION.md|## 9. Pièges connus|## 10. Format de livraison|2}}

### 6.7 Mots-pièges du texte imprimé, à chercher sur **chaque** carte (`PROCESSUS-CARTE.md`, étape 5)

| Mot ou tournure | Piège concret déjà rencontré |
|---|---|
| `each`, `for each` | rendu par erreur « chaque joueur » au lieu de « chaque héros » |
| `against you`, `your` | portée oubliée ou élargie |
| `you control` | la cible peut viser une carte hors du contrôle du joueur, y compris celle du vilain |
| `unless`, `otherwise`, `without` | branche alternative non codée |
| `instead` | « instead » veut dire que la chose **part** d'un endroit et **arrive** ailleurs, pas qu'elle est dupliquée |
| `once per round per player` | à ne pas coder comme une limite globale |
| `if you cannot` | vérifier que le cas testé est réellement atteignable |
| `that <nom>` | vérifier que la cible est bien **la même** carte que celle nommée plus haut |
| `equal number` | vérifier le sens exact du décompte |
| `attacks` / `attacks or engages` / `attacks and damages` | trois déclencheurs différents |
| `and remove` (coût à plusieurs parties) | qu'**aucune** partie ne soit oubliée |
| `defeated` vs `damaged` | ne jamais coder l'un pour l'autre |
| **Response** / **Interrupt** + `After` | le déclencheur est un vrai message du moteur avec fenêtre |
| **Forced Interrupt** vs **Forced Response** | l'un résout **avant** l'événement, l'autre **après** |
| **Hero Response** / **Hero Action** | sous-type dédié, pas le type nu |
| un second Interrupt/Response/mot-clé annoncé | vérifier qu'il a vraiment un module |
| mot-clé cité mais pas imprimé sur **cette** carte | ne pas coder de capacité fantôme |
| icône de ressource | à vérifier contre une carte du **même pack**, jamais à vue |

### 6.8 Ce que tu livres pour **chaque** carte à capacité : le gabarit

Une carte n'est **jamais** « terminée » parce qu'elle est écrite. Elle l'est quand son gabarit est rempli **avec
des preuves réelles**. Tu remplis la partie « statique » (étapes 2, 5, 6) ; Claude remplit les étapes qui
exigent le jeu (7, 8, 8 bis). **Tu laisses les cases non exécutées décochées, avec la mention `à exécuter par
Claude`** : ne coche jamais une preuve que tu n'as pas produite.

```
### <card_id> : <nom de la carte>

- [ ] Étape 2 : carte(s) de référence : <card_id modèle> (<nom>) : comparable parce que ...
- [ ] Étape 5 : texte-contre-code : mots-pièges vérifiés (lister) : ...
      Résultat : ...
- [ ] Étape 6 : nombres texte ↔ code : <chaque nombre imprimé> = desc <...> = script <...>
      Résultat : ...
- [ ] Étape 7 : cas test_capacites par capacité (écrit dans tools/cas/<bloc>.py ; à exécuter par Claude) :
      capacité 1 : cas <nom du cas> ... ; capacité 2 : ...
- [ ] Étape 7 bis : limite imprimée ? OUI / NON. Si OUI : témoin d'épuisement : cas <nom> (deux déclenchements
      dans le même round/phase, chiffre mesuré au second)
- [ ] Étape 8 / 8 bis : à exécuter par Claude (autoplay ; la carte dessine-t-elle quelque chose de nouveau ?)

Carte terminée : NON (à compléter par Claude) / OUI si aucune capacité et rien à prouver.
```

Un **doute de lecture** (§1.3) s'écrit dans `QUESTIONS.md` **avant** le script ; le script prend alors la lecture
**recommandée**, repérée par un commentaire `# QUESTION <n> :` pour que Claude retrouve le point.

### 6.9 Auto-relecture d'une carte (annexe A, §11)

{{SECTION:docs/reference/KIT-CHATGPT-CREATION.md|## 11. Checklist d'auto-relecture|## 12. Ce que le GPT ne fait pas|2}}
