# Kit de création de héros : Marvel Champions LCG (moteur `marvel-lcg`, projet « Narwhal Champions »)

> **Version du 20/10/2026.** Ce manuel est construit par `outils/construire-kit-heros.py` à partir du dépôt
> réel : chaque fichier cité en bloc de code est la **copie exacte** du fichier du projet au moment de la
> construction. Si un exemple de ce manuel et le dépôt divergent un jour, c'est le dépôt qui a raison.

## 1. Mode d'emploi et règles absolues

### 1.1 Pour qui, pour quoi

Tu es une IA chargée de **produire les fichiers d'un héros** pour ce jeu : ses cartes (les deux faces de l'identité,
les cartes signature, l'obligation, le set némésis, au besoin les cartes d'aspect du pack), son deck de départ,
les scripts de ses cartes (leurs capacités en Python), les textes français, sa biographie, la liste des images, et
les preuves (cas de test) qui vont avec. L'utilisateur te donne **les images des cartes du héros** : ce sont elles
qui font foi pour tout ce qui est imprimé.

Ce que tu produis **n'est jamais intégré tel quel**. Il est donné à **Claude**, l'assistant qui a accès au dépôt
du jeu : Claude le compare, le teste en jeu, le corrige et l'intègre. Tu n'as, toi, accès à rien d'autre que ce
manuel, ses annexes et les fichiers modèles du zip. Tout ce que tu dois savoir est donc ici.

Ce manuel couvre **toute la chaîne** d'un héros, dans cet ordre :

1. **Les cartes** (`data/cards.json`) : les faces `Hero` / `AlterEgo`, les cartes signature, l'obligation, les
   cartes némésis, et si le pack en a, les cartes d'aspect.
2. **Le deck de départ** (`deck/starter/<héros>.json`) et l'entrée de l'extension (`data/sets_info.json`).
3. **Les scripts** des cartes (`src/cards/pack/<pack>/…`).
4. **Les textes français, la biographie, la réplique de recrutement, les images, les crédits.**
5. **Les preuves** : cas de test de capacité, gabarits de contrôle par carte.

### 1.2 Les règles absolues

Elles viennent de règles posées par l'utilisateur du projet et d'erreurs déjà payées. Les enfreindre fait
échouer l'intégration, ou pire : produit un héros qui *a l'air* de marcher et ne marche pas.

1. **Fidélité à 100 % au texte imprimé.** Une carte fait exactement ce qu'elle dit, rien de moins, rien de plus.
   Pas d'approximation « recommandée ». Si le moteur ne sait pas faire ce que la carte dit, tu l'écris dans
   `A_FAIRE_CLAUDE` (règle 3) : le moteur s'étend, la carte ne s'édulcore pas.
2. **N'invente jamais une fonction, une clé, une chaîne de ciblage.** Tu n'utilises que ce qui figure dans ce
   manuel, dans ses annexes, dans l'index de l'API du moteur (`annexes/I-index-api-moteur.md`) ou dans les
   fichiers modèles. Une fonction inventée ne lève **presque jamais d'erreur** : la carte se construit, entre en
   jeu, et ne fait rien. C'est le défaut le plus fréquent et le plus silencieux de ce projet.
3. **Ce que tu ne sais pas faire s'écrit, il ne se devine pas.** Écris dans le script :

   ```python
   # A_FAIRE_CLAUDE: <ce qui manque, le texte imprimé visé, la carte de référence la plus proche>
   ```

   et continue le reste. Une carte à moitié écrite avec un `A_FAIRE_CLAUDE` honnête vaut mieux qu'une carte
   « complète » qui appelle une fonction inventée. **Un script qui renvoie une liste vide ne signifie pas que la
   carte n'a aucun effet** : si la carte a un texte de capacité, un `GetAbilities()` vide sans
   `A_FAIRE_CLAUDE` est une faute.
4. **Une question à la fois, en choix multiple, avec l'image.** Quand un texte, une icône ou une règle laisse
   place à plus d'une lecture, tu poses **une seule** question à l'utilisateur (pas un lot de dix), avec :
   l'**image de la carte concernée** (cite son fichier), l'option que tu recommandes en premier, « Autre
   (précise) » en dernier, et pour chaque option **ce que ça change en jeu**. Tu attends la réponse avant la
   question suivante. Tu ne tranches pas en silence. Cas qui déclenchent une question : §1.3.
5. **Ne touche jamais au moteur.** Tu n'écris que des cartes, des decks, leurs scripts, leurs textes et leurs
   preuves. Si une mécanique demande une modification du moteur (un compteur nouveau, un trait nouveau, un
   message nouveau), tu l'écris dans `BESOINS-MOTEUR.md` (§9.5) : ce que c'est, pourquoi, quelle carte l'exige.
6. **N'écrase jamais un fichier partagé.** `data/cards.json`, `data/sets_info.json`,
   `ui-app/src/board/textes-fr-fanmade.ts`, `tools/prefixes_fanmade.json`, `public/js/prepare/heros-info.js`
   et `public/js/prepare/repliques-heros.js` contiennent le travail de tout le monde. Tu livres des
   **fragments** à fusionner (chapitre 9), jamais le fichier entier.
7. **Les valeurs de `desc` sont toujours des chaînes** (`"HP": "14"`, jamais `14`).
8. **Une icône de ressource ne se nomme jamais « à vue ».** Elle se compare à une carte du même pack dont la
   ressource est connue. Une lecture au jugé a déjà inventé une « ressource os » sur Lockjaw : l'icône « nœuds
   reliés » était une ressource **mentale**, et quatre cartes n'ont pas rendu ce qu'elles promettent pendant cinq
   jours. Dans le doute : question (§1.3).
9. **Les textes de cartes sont en anglais** (c'est la langue des données du moteur). Le texte français se livre à
   part, dans un fragment dédié, avec le vocabulaire officiel (chapitre 7).
10. **`player_deck` reste VIDE pour un héros maison**, sauf si **l'auteur du héros fournit une decklist** imprimée
    ou dans son dossier : on la recopie alors telle quelle. Les ~25 cartes d'aspect qu'une IA « composerait » pour
    compléter un héros sont une invention, pas du contenu de l'auteur (consigne de l'utilisateur du
    06/09/2026, appliquée à 33 decks le 12/09/2026). Ne pose plus la question de l'aspect.
11. **Jamais la carte signature d'un autre héros** dans un deck. Une carte de classe `Hero` (`desc.Class =
    "Hero"`) appartient à un seul héros. Le moteur **ne valide pas** les decks de départ : c'est à toi.
12. **Ne laisse aucune trace de travail dans les livrables** : pas de `print` de debug, pas de fichier
    temporaire, pas de commentaire qui raconte ton raisonnement. Les commentaires expliquent *pourquoi* une
    carte est écrite ainsi, en français, comme dans les modèles.

### 1.3 Ce qui déclenche une question à l'utilisateur

| Situation | Exemple vécu |
|---|---|
| Mot-clé maison non défini sur les cartes fournies | « drain X » qu'aucune carte n'explique |
| Texte imprimé contradictoire | « Forced **Interrupt** : **After** X schemes or attacks » : le type et le déclencheur se contredisent |
| Valeur imprimée que le format ne sait pas exprimer | une ATK « ★ » |
| Portée ambiguë d'une phrase | « Discard this obligation » : la dernière option seulement, ou les deux ? |
| Mot-clé officiel inapplicable tel quel | `TeamUp` qui suppose deux héros en jeu |
| Contenu absent du matériel fourni | aucune liste de deck fournie pour un héros maison |
| Effet que le moteur ne peut pas rendre fidèlement | « if this attack has ranged or piercing » sur un événement |
| Icône imprimée qu'on ne reconnaît pas | l'icône « nœuds reliés » de Lockjaw, prise pour un os |
| Que devient une chose au moment du retournement d'identité ? | Iron Fist : les jetons Chi restent-ils sur l'identité quand on passe en alter ego ? (réponse : oui, décision de l'utilisateur du 20/10/2026) |
| Deux lectures valides de « a scheme » / « an enemy » | The Way of Things : deux « a scheme » indépendants, ou le même ? |
| Carte du héros qui nomme une carte absente des images fournies | une capacité qui « cherche X » où X n'est pas dans le matériel : X existe-t-elle déjà dans le jeu, ou faut-il la livrer ? |

Ne posent **pas** de question : les choix purement techniques (quelle fabrique, où ranger une aide, format
d'image). Ceux-là, tu les fais, et tu les expliques dans tes doutes si tu hésites.

Les points **non tranchables** (une capacité que tu ne sais pas coder, un comportement du moteur que tu ne peux
pas vérifier) ne sont pas des questions : ils vont dans `A_FAIRE_CLAUDE` et dans `QUESTIONS.md`.

### 1.4 Ce que tu livres (résumé ; le détail est au chapitre 9)

Un dossier `livraison/` qui **reproduit l'arborescence du projet**, plus des fichiers de suivi :

```
livraison/
  MANIFESTE.md           la liste de TOUS les fichiers livrés, une ligne chacun : chemin, rôle, nombre de cartes
  QUESTIONS.md           les questions ouvertes (une par carte ou par règle), format du §9.4
  BESOINS-MOTEUR.md      ce que le moteur ou l'interface devra apprendre (trait, compteur, message, écran...)
  A_FAIRE_CLAUDE.md      tous les marqueurs A_FAIRE_CLAUDE du code, regroupés
  GABARITS.md            un gabarit de contrôle par carte à capacité
  AUTO-VERIFICATION.md   ce que tu as vérifié toi-même, avec la sortie de `verifier-livraison-heros.py`
  images.md              card_id → fichier source
  CREDITS.md             l'auteur du héros, les sources
  integration/           l'arborescence à fusionner (data/, deck/, src/, textes-fr/, public/, tools/)
```

Avant de livrer, tu lances **`verifier-livraison-heros.py`** (fourni dans le zip, à la racine, Python 3 sans
dépendance ; il charge `verifier-livraison-campagne.py` placé à côté) sur ton dossier. Il attrape les erreurs de
forme que Claude attraperait de toute façon, mais que tu peux corriger toi-même sans attendre : une face qui
manque, un deck de départ qui cite une carte absente ou la signature d'un autre héros, une obligation sans
`GiveTo`, un script rangé dans le mauvais dossier, une capacité imprimée sans script, une biographie indexée par
le nom. **Il ne remplace pas le jeu** : un script qui passe ce contrôle peut encore ne rien faire en partie.
C'est pourquoi les règles 2 et 3 comptent plus que tout le reste.

### 1.5 Comment lire ce manuel

| Si tu dois... | Lis |
|---|---|
| comprendre ce qu'est un héros ici et comment il entre en partie | chapitre 2 |
| savoir quels fichiers produire | chapitre 3 (la liste maîtresse) |
| écrire ou vérifier les cartes du héros | chapitre 4, puis l'annexe A (kit de cartes) et le chapitre 12 |
| écrire le deck de départ, le set némésis, une variante | chapitre 5 |
| écrire le script d'une carte, une face d'identité | chapitre 6, annexes A, B (recettes) et C (mots-clés) |
| textes français, images, biographie, réplique, crédits | chapitre 7 |
| prouver que ça marche | chapitre 8 |
| préparer la livraison | chapitre 9 |
| voir quatre héros complets, fichier par fichier | chapitre 10 et le dossier `modeles/` du zip |
| éviter les pièges déjà payés | chapitre 11 |
| les tableaux de référence communs aux campagnes et aux héros | chapitre 12 |



---

## 2. Un héros dans le jeu : ce que c'est, et son voyage du fichier à la table

### 2.1 Un héros, ce sont six choses

| # | Quoi | Où | Qui s'en sert |
|---|---|---|---|
| 1 | **Les cartes** : deux faces d'identité, ~15 cartes signature, 1 obligation, 5 cartes némésis (et, pour un héros officiel, les cartes d'aspect de la boîte) | `data/cards.json`, clé = le **pack** | le moteur, le plateau, le deck-builder |
| 2 | **Le deck de départ** : l'identité, les cartes signature, l'obligation, le set némésis, l'éventuelle moitié d'aspect | `deck/starter/<héros>.json` | le moteur (partie), le lanceur (la **liste des héros**) |
| 3 | **L'extension** : à quelle boîte le héros appartient | `data/sets_info.json`, liste `heroes` | le lanceur, le deck-builder |
| 4 | **Les scripts** : ce que font les cartes | `src/cards/pack/<pack>/…` | le moteur |
| 5 | **Les textes et l'habillage** : français, biographie, réplique de recrutement, images, crédits | `ui-app/src/board/textes-fr-fanmade.ts`, `public/js/prepare/heros-info.js`, `repliques-heros.js`, `assets/pics/` | le plateau, le lanceur |
| 6 | **Les preuves** : cas de test, gabarits | `tools/cas/…`, `docs/packs/<héros>_cartes.md` | Claude |

⚠ **Le deck de départ n'est pas un « deck de joueur » : c'est la fiche d'inscription du héros.** Sans lui, le
héros n'apparaît **nulle part**, pas même dans le deck-builder, parce que `catalog.heroes()`
(`public/js/prepare/catalog.js`) construit la liste des héros **en lisant `deck/starter/*.json`**. On l'écrit donc
toujours, avec **ce qui est imprimé et rien d'autre**.

### 2.2 Le voyage, étape par étape

1. **Le lanceur** (`public/prepare.html`, `public/js/prepare/`) lit `deck/starter/*.json` : un fichier = une tuile
   de héros. Il range chaque héros dans son **extension** grâce à la liste `heroes` de `data/sets_info.json`. Une
   extension dont la clé contient « Custom » (`117. Custom (Lockjaw)`) (ou un héros sans extension) est rangée parmi les héros **fan-made**
   (`isHomebrew`, `catalog.js`) et affiche le nom du créateur (champ `custom` de la face héros, `auteur.js`).
2. **Au survol d'une tuile**, le lanceur affiche la **biographie** (`public/js/prepare/heros-info.js`, indexée par le
   `card_id` de la **face héros**). Au recrutement, une **réplique** s'affiche sur la carte
   (`public/js/prepare/repliques-heros.js`, indexée par l'**identifiant de deck**).
3. **Le joueur choisit** un deck de héros (la modale du héros propose les **variantes** : autre deck de héros,
   autre identité, autre art), construit ou choisit sa moitié d'aspect dans le **deck-builder** — le
   `player_deck` du fichier n'en est que le *deck par défaut* —, puis lance la partie.
4. **Le moteur** charge le fichier (`SceneLoader` → `FileManager.FindJsonPath('Hero', …)` cherche dans `./deck/`
   puis `./deck/starter`) et en fait un `HeroDescriptor` par joueur.
5. **La mise en place du joueur** — `PlayerSetup.SelectIdentity` (extrait ci-dessous) :
   * les faces de `hero` sont fabriquées, **la face `b` (alter ego) d'abord** : le héros **commence en alter
     ego** ;
   * `obligations` et `nemesis_set` sont fabriqués et **mis de côté** (`set_aside_obligations`,
     `set_aside_nemesis_sets`) ; chaque carte némésis est **marquée** `nemesis_of_player` ;
   * `hero_deck` (cartes signature) et `player_deck` sont fabriqués et **mélangés** en un seul deck.
6. **En partie**, le héros alterne ses formes (`ChangeToForm`) ; les capacités imprimées sur les faces `a` et `b`
   sont des scripts comme les autres ; ATK / THW / DEF / REC de base et la taille de main viennent de `desc` et
   sont **automatiques**.

*Extrait de `Fusion/marvel-lcg-src/src/game/player/element/player_setup.py` (de « def SelectIdentity » a « # CORRECTIF (02/09/2026) : marquer »).*

```python
    def SelectIdentity(self, name: str, hero_names: Sequence[str], hero_deck: Sequence[str], obligations: Sequence[str], nemesis_set: Sequence[str], player_deck: Sequence[str]) -> None:
        from game.effect.rule import GameRule
        from game.message import Message
        from game.card.factory import CardFactory

        player = self.player

        player.hero_name = name

        def move_b_to_front(s: str):
            parts = s.split(',')
            b_part = [part for part in parts if part.endswith('b')]
            other_parts = [part for part in parts if not part.endswith('b')]
            result = b_part + other_parts
            return ','.join(result)
        if hero_names[0].startswith(HACK_HERO_ID):
            hero_names = ["31002a,31002b"]
        else:
            hero_names = [move_b_to_front(s) for s in hero_names]
        CardFactory.GenerateCards(hero_names, player.set_aside_deck, player.world)

        hero_card = player.set_aside_deck.GetAll()[0]
        rule = GameRule(hero_card)
        hero_card.PutIntoPlay(player, rule)

        # hero_card.Reset(False)
        # hero_card.ResetHealth(GameRule(hero_card))
        # We do this by effect

        if player.world.is_game_over:
            return

        # CardFactory.GenerateCards(set_aside, player.set_aside_deck, player.world)
        select_message = Message.WhenPlayerSelectHero(player, player.GetIdentity())
        select_message.Send()

        # After set aside is create for `HACK_HERO_ID`
        if hero_card.card.back_faces:
            # hero_card.ChangeToForm(AlterEgo, GameRule(hero_card))
            self.SetupPlayerAbility(hero_card)

        # ~~3. Select First Player~~
        # We don't need this

        # 4. Set Aside Obligation
        player.set_aside_obligations = []
        player.set_aside_obligations += CardFactory.GenerateCards(obligations, player.set_aside_nemesis_sets, player.world)

        # 5. Set Aside Nemesis Sets
        cartes_nemesis = CardFactory.GenerateCards(nemesis_set, player.set_aside_nemesis_sets, player.world)
```

⚠ `HeroDescriptor` (`src/game/scene/replay/hero.py`) ne connaît **que** : `version`, `name`, `hero`, `hero_deck`,
`obligations`, `nemesis_set`, `player_deck`, `linked_identity`, `team`. **Le champ `set_aside` du fichier de deck
n'est pas lu en vraie partie.** Une carte qu'un héros « met de côté à la mise en place » doit être créée par le
héros lui-même (`AbilityFactory.BeginGameWithSetAside([...])` sur la face alter ego, §6.4).

*Fichier `Fusion/marvel-lcg-src/src/game/scene/replay/hero.py` (copie exacte, lue dans le depot au moment de la construction).*

```python
from core import *

@dataclass
class HeroDescriptor:
    version: str
    name: str
    hero: List[str]
    hero_deck: List[str]
    obligations: List[str]
    nemesis_set: List[str]
    player_deck: List[str] = field(default_factory=lambda: [])
    # IDENTITE LIEE. Certains packs physiques font piloter DEUX heros par un
    # seul joueur (Cloak & Dagger) : chaque identite garde son mini-deck, sa
    # main et sa defausse. Le moteur sait deja tenir cela pour deux JOUEURS ;
    # l'identite liee est donc developpee en un second joueur au chargement
    # (voir `SceneLoader.NewFromJson`), ce qui evite de redefinir ce que
    # `player.GetIdentity()` renvoie dans les ~770 endroits qui l'appellent.
    linked_identity: Dict[str, Any] = field(default_factory=lambda: {})
    # CAMP. 0 en partie ordinaire : tous les joueurs sont dans la meme zone
    # de jeu et rien ne change. En mode competitif (livret mc56 p.14), 0 est
    # l'equipe qui joue en premier chaque round et 1 l'equipe adverse ;
    # chaque camp a sa zone, son leader et son deck rencontre.
    team: int = 0

    def UpdateVersion(self):
        pass

```

### 2.3 Ce que le jeu contient déjà (mesuré le 20/10/2026)

| Mesure sur les 152 decks de départ | Valeurs : nombre de decks |
|---|---|
| cartes dans `hero_deck` | 7 : 1, 15 : 145, 16 : 5, 19 : 1 |
| plus grand nombre d'exemplaires d'un même card_id | 1 : 12, 2 : 44, 3 : 86, 4 : 8, 5 : 2 |
| cartes dans `obligations` | 0 : 1, 1 : 148, 2 : 2, 4 : 1 |
| cartes dans `nemesis_set` | 0 : 2, 2 : 1, 4 : 3, 5 : 145, 8 : 1 |
| cartes dans `player_deck` | 0 : 53, 15 : 1, 24 : 4, 25 : 90, 26 : 2, 27 : 2 |
| faces listées dans `hero` | 2 : 144, 3 : 5, 5 : 2, 6 : 1 |
| héros dont la face héros porte `custom` (fan-made ; `cards.json` + `cards_custom.json`) | 79 |
| decks qui sont des **variantes** (`variante_de`) | 2 |
| clés de `metadata` les plus courantes | `url` ×152, `author` ×68, `deck_note` ×53, `collision_note` ×25, `nemesis_note` ×16, `aspect_note` ×12, `auteur` ×12, `note` ×11 |

### 2.4 Ce qui existe en plus, et que tu ne produis pas

Ces fichiers touchent aussi un héros, mais **Claude** les génère ou les met à jour (tu n'as pas à les écrire, et
tu ne dois pas les inventer) : positions des bulles de statistiques (`ui-app/src/components/stat-bubbles/positions.ts`,
générées par `ui-app/outils/calibrer-stat-bubbles.py` à partir de l'image), palette du héros
(`data/palettes-heros.json`, `outils/palettes-heros.py`), annuaire d'identités (`data/identites.json`,
`outils/annuaire-identites.py`), arts alternatifs cosmétiques (`ARTS_HEROS`), checksums de `cards.json` /
`sets_info.json` (`tools/recalculer_checksums.py`), numéro d'extension (`N.` dans la clé de `sets_info`), entrée de
nouveautés. Si ton héros a besoin d'une de ces choses de façon particulière (une identité alternative, un art),
**dis-le dans `BESOINS-MOTEUR.md`**.



---

## 3. La liste maîtresse des fichiers d'un héros

Chemins relatifs à la racine du moteur (`Fusion/marvel-lcg-src/`) sauf mention. **A** = tu le produis dans
`livraison/integration/`. **C** = Claude le génère ou le met à jour (tu ne le livres pas).

### 3.1 Ce que tu produis (A)

| # | Fichier livré (dans `integration/`) | Contenu | Obligatoire | Chapitre |
|---|---|---|---|---|
| 1 | `data/cards.<pack>.fragment.json` | `{"<pack>": [ …toutes les cartes du pack… ]}` | oui | 4 |
| 2 | `data/sets_info.<pack>.fragment.json` | `{"N. Custom (<Nom>)": {name, scenarios: [], heroes: ["<héros>"], encounters: [], max_id}}` | oui | 5.5 |
| 3 | `deck/starter/<héros>.json` | le deck de départ (+ un fichier par **variante**) | oui | 5 |
| 4 | `data/nemesis/<héros>_nemesis.json` | le set némésis comme set nommé | non | 5.4 |
| 5 | `src/cards/pack/<pack>/__init__.py` | helpers partagés du pack (peut être minimal) | oui | 6.1 |
| 6 | `src/cards/pack/<pack>/<set_nettoyé>/__init__.py` | un par dossier de set | oui | 6.1 |
| 7 | `src/cards/pack/<pack>/<set_nettoyé>/<card_id>.py` | **un script par face de carte à capacité** | oui | 6 |
| 8 | `textes-fr/<pack>.fragment.txt` | lignes `'<card_id>': "texte français",` pour `textes-fr-fanmade.ts` | **oui** (fan-made) | 7.1 |
| 9 | `public/js/prepare/heros-info.fragment.js` | l'entrée de biographie, indexée par la face héros | **oui** (fan-made) | 7.3 |
| 10 | `public/js/prepare/repliques-heros.fragment.js` | la ligne de répliques, indexée par l'id de deck | non (à proposer) | 7.4 |
| 11 | `tools/prefixes.<pack>.fragment.json` | l'entrée de `prefixes_fanmade.json` | **oui** (fan-made) | 4.8 |
| 12 | `tools/cas/<héros>.py` | cas de test de capacité | recommandé | 8.2 |
| 13 | `tools/decks-de-test.fragment.json` | moitié d'aspect **de test** (harnais seulement) | non | 8.4 |
| 14 | `MANIFESTE.md` `QUESTIONS.md` `BESOINS-MOTEUR.md` `A_FAIRE_CLAUDE.md` `GABARITS.md` `AUTO-VERIFICATION.md` `images.md` `CREDITS.md` | le suivi | oui | 9 |

**Un héros officiel** (extension imprimée par l'éditeur) : mêmes fichiers, sans la clé `custom`, sans préfixe
(ids à cinq chiffres), sans fichier 8 si le texte français est déjà fourni par le jeu — mais un héros *récent*
(Iron Fist, MC64) a bien ses textes français dans `textes-fr-fanmade.ts` : vérifie dans les modèles.

### 3.2 Ce que Claude touche (C), à titre d'information

| Fichier | Quoi |
|---|---|
| `data/cards.json` | fusion de ton fragment ; **checksum recalculé** (un checksum faux est journalisé comme `Mismatch` par le moteur et fait refuser l'envoi de rejeux au serveur : le fichier fusionné doit donc être recalculé) |
| `data/sets_info.json` | fusion de ton fragment ; numéro `N.` attribué |
| `assets/pics/<card_id>.<jpg\|png\|webp>` | les images que l'utilisateur donne, uniformisées (`outils/uniformiser-scans.py`) |
| `ui-app/src/board/textes-fr-fanmade.ts` | fusion de ton fragment texte |
| `public/js/prepare/heros-info.js` / `repliques-heros.js` | fusion de tes fragments |
| `tools/prefixes_fanmade.json` | fusion de ton fragment |
| `ui-app/src/components/stat-bubbles/positions.ts`, `data/palettes-heros.json`, `data/identites.json` | générés depuis les images |
| `tools/test_capacites.py` (cas), `tools/substituer_pack.py`, `tools/verifier_tous_les_decks.py` | lancés ; ton fichier `tools/cas/<héros>.py` y est chargé automatiquement |
| `docs/packs/<héros>_cartes.md` | tes gabarits, relus et complétés par Claude |

### 3.3 Ce que tu ne livres jamais

Des images ; un checksum ; une copie (même partielle) d'un fichier partagé ; un fichier hors de l'arborescence ;
un fichier temporaire ; une modification du moteur ; un `player_deck` inventé pour un héros maison ; un commit.

### 3.4 Les trois formes de héros que le jeu connaît (pour te situer)

| Forme | Exemple | Ce qui change |
|---|---|---|
| **Héros simple** : une paire `a`/`b` | Lockjaw `lj001a`/`lj001b`, Iron Fist `64001a`/`64001b` | le cas normal |
| **Héros à formes multiples** : `a` héros, `b` alter ego, `c` (… `e`) autres formes | Ant-Man `12001a`/`b`/`c` (forme Géant), Conan `cn001a`…`cn001e`, Moon Knight `mk001a`…`mk001e` | `hero` dans le deck cite **toutes** les faces ; chaque face a ses propres stats et son script |
| **Identité liée** : deux identités pilotées par un joueur | Cloak & Dagger (`linked_identity`) | un mini-deck complet dans `linked_identity` (§5.6) ; un seul pack du jeu à ce jour |

Une **identité alternative** (même deck, autres faces : The Thing Guardian `th001c,th001d`) se déclare dans
`metadata.hero_alts` (§5.3) ; un **second deck de héros** (Hellcat / She-Hulk) est une **variante** (§5.3).



---

## 4. Les cartes du héros : `data/cards.json`

Les règles générales du format d'une carte (clés de premier niveau, toutes les clés `desc`, balises du texte
imprimé, listes blanches de traits et de compteurs) sont dans le manuel de campagne fourni en **annexe L**
(`annexes/L-manuel-campagne-cartes-et-scripts.md`) et rappelées au **chapitre 12**. Ce chapitre ne dit que ce qui
est **propre à un héros**. Toutes les valeurs ont été **mesurées le 20/10/2026 sur le fichier réel**.

### 4.1 Forme de ta livraison

Tu ne livres **jamais** `data/cards.json` entier. Tu livres un fragment qui ne contient que **ton** pack, cartes
triées par `card_id`, indentation de 4 espaces, `ensure_ascii=False` :

```json
{
  "<pack>": [
    { "card_id": "xx001a", "type": "Hero", ... },
    { "card_id": "xx001b", "type": "AlterEgo", ... }
  ]
}
```

La **clé du pack** est un nom court en minuscules et soulignés (`lockjaw`, `iron_fist`) ; c'est aussi le nom du
dossier `src/cards/pack/<pack>/` et la valeur de `name` dans l'entrée de `sets_info`. Le `checksum` n'est pas
ton affaire.

### 4.2 Les cartes d'un pack de héros, dans l'ordre où on les numérote

Mesuré : Iron Fist compte 13 cartes, Harry Osborn 18, Lockjaw 31, Ant-Man 35 (avec ses cartes d'aspect). La
numérotation suit **l'ordre imprimé de la boîte** (numéro de collection). Le tableau ci-dessous est celui de Lockjaw ; une boîte
officielle mêle les rangs (Ant-Man : signature `12002`–`12010`, aspect `12011`–`12024`, obligation `12025`, némésis
`12026`–`12029`, puis d'autres cartes d'aspect `12030`–`12033`) :

| Rang | Cartes | `type` | `set_name` | Exemple (Lockjaw) |
|---|---|---|---|---|
| 1 | l'identité : face héros `…001a`, face alter ego `…001b`, (formes de plus `…001c`…) | `Hero`, `AlterEgo` | le nom du héros | `lj001a`, `lj001b` |
| 2 | les **cartes signature** : une carte = un `card_id`, plusieurs exemplaires = le même id répété dans le deck | `Ally` `Event` `Upgrade` `Support` `Resource` | le nom du héros | `lj002`–`lj012` (11 titres, 15 exemplaires) |
| 3 | l'**obligation** (1) | `Obligation` | le nom du héros | `lj013` |
| 4 | les **cartes némésis** (en général 5 exemplaires) | `Minion` `SideScheme` `Attachment` `Treachery` | **`"<Héros> Nemesis"`** | `lj014`–`lj017` |
| 5 | les **cartes d'aspect** que la boîte ou l'auteur fournit (facultatif) | `Ally` `Event` `Upgrade`… | le nom du héros (classe = l'aspect) | `lj018`–`lj030` |

* **Héros officiel** : ids à cinq chiffres, `<n° de pack><n° de carte>` (`12001a` Ant-Man, `64001a` Iron Fist) ;
  le numéro de carte est le **numéro de collection imprimé** (1A/1B, 2 à 12…). Les cartes d'aspect de la boîte ont
  un `set_name` vide (`""`) et une classe d'aspect (`Leadership`, `Basic`…).
* **Héros fan-made** : **deux lettres de préfixe**, trois chiffres, suffixe de face (`lj001a`). Le préfixe est
  choisi **avant la première carte** et déclaré dans `tools/prefixes_fanmade.json` (§4.8).
* **Numérotation continue, sans trou.** Le plus grand identifiant du pack se déclare dans `sets_info` (`max_id`).

### 4.3 Les deux faces de l'identité

Une identité est une **paire** : face `a` = **héros** (type `Hero`), face `b` = **alter ego** (type `AlterEgo`).
**Le jeu commence toujours sur la face `b`** (alter ego) ; le joueur passe en héros en retournant la carte.

| Face | `type` | `desc` obligatoire | Notes |
|---|---|---|---|
| héros `…a` | `Hero` | `HP` `ATK` `THW` `DEF` `HS` | `ATK` (attaque), `THW` (contre-manigance), `DEF` (défense), `HS` (taille de main) |
| alter ego `…b` | `AlterEgo` (exception unique : `31001b` de SP//dr est un `Support`) | `HP` `REC` `HS` | `REC` (récupération) ; **pas** de `ATK` `THW` `DEF` |

* Le **nom** commence par `"* "` (carte unique) sur **les deux faces** (une seule exception : `21001a` Spectrum) : `"* Lockjaw"`, `"* Scott Lang"`.
* Les **traits** diffèrent d'une face à l'autre (`["INHUMAN", "PET AVENGER"]` côté héros, `["INHUMAN", "GOOD BOY"]`
  côté alter ego).
* Les deux faces ont **le même `set_name`** (le nom du héros) et, pour un héros maison, la **même clé `custom`**.
* Les capacités imprimées sur la face (`Setup`, `Response`, `Action`…) vont dans le `text` ; les statistiques de
  base **ne sont pas** des capacités : elles sont automatiques.
* **Formes de plus** : une face `c` (Ant-Man Géant : `12001c`, type `Hero`, ses propres `HP ATK THW DEF HS`), `d`,
  `e` (Conan, Moon Knight). Elles se déclarent dans `hero` du deck de départ (§5.2). Une forme de plus est de type
  `Hero` ou `AlterEgo` selon ce qu'elle est.
* **Taille d'image** : voir §7.2.

```json
{
    "card_id": "lj001a",
    "type": "Hero",
    "name": "* Lockjaw",
    "subtitle": "",
    "desc": {
        "HP": "14",
        "ATK": "2",
        "THW": "1",
        "DEF": "2",
        "HS": "4"
    },
    "traits": [
        "INHUMAN",
        "PET AVENGER"
    ],
    "set_name": "Lockjaw",
    "text": "<i>Fetch!</i> — <b>Action</b>: Exhaust Lockjaw and spend a [mental] resource → choose a non-resource card in any players' discard pile and add it to their owner's hand. <i>(Limit once per round.)</i>",
    "custom": "Nugget"
}
```

```json
{
    "card_id": "lj001b",
    "type": "AlterEgo",
    "name": "* Lockjaw",
    "subtitle": "",
    "desc": {
        "HP": "14",
        "REC": "3",
        "HS": "5"
    },
    "traits": [
        "INHUMAN",
        "GOOD BOY"
    ],
    "set_name": "Lockjaw",
    "text": "<b>Setup</b>: Search your deck, hand and discard pile for Tuning Fork and put it into play.\n<i>Cheer Up</i> — <b>Response</b>: After you change to this form, ready a friendly character.",
    "custom": "Nugget"
}
```

Un héros officiel avec **trois formes** (Ant-Man) — notez que la forme Géant a des stats inverses (ATK 3, THW 1,
DEF 3, HS 4) :

```json
{
    "card_id": "12001c",
    "type": "Hero",
    "name": "* Ant-Man",
    "subtitle": "",
    "desc": {
        "HP": "12",
        "ATK": "3",
        "THW": "1",
        "DEF": "3",
        "HS": "4"
    },
    "traits": [
        "AVENGER",
        "GIANT"
    ],
    "set_name": "Ant-Man",
    "text": "<i>Giant Nuisance</i> — <b>Response:</b> After you change to this form, deal 1 damage to an enemy."
}
```

### 4.4 Les cartes signature

* `desc.Class` = **`"Hero"`** (exceptions réelles : les signatures à double classe `Hero;Aggression`… des decks TMNT Shinobi, et un alias `full_link` sans `Class`, `13007`). C'est ce qui en fait la carte *de ce héros* : le deck-builder s'en sert pour les
  proposer, et le contrôle « jamais la signature d'un autre héros » (règle 11) s'appuie dessus.
* `set_name` = **le nom du héros**, exactement comme sur la face héros (« Lockjaw ») ; 17 cartes de `hero_deck` du jeu ont un autre `set_name` (cas particuliers : en cas de doute, question).
* `desc` classique d'une carte joueur : `Cost`, `RES` (lettres `R` physique, `B` mentale, `Y` énergie, `G` joker),
  `HP`/`ATK`/`THW` pour un allié (`"ATK": "4*"` = dégâts consécutifs), `MaxPerDeck` si imprimé.
* **15 exemplaires** au total dans `hero_deck` pour 145 des 152 héros du jeu (§5.2).
* Les **icônes de ressource** se comparent à une carte connue du même pack (règle 8) : jamais « à vue ».
* Un **trait nouveau** (`TELEPORT`, `GOOD BOY`) n'empêche rien (la liste `TRAITS` du moteur n'est qu'un typage), mais
  se signale dans `BESOINS-MOTEUR.md` pour que Claude l'ajoute. Un **compteur nouveau** (`desc.Uses`, par
  exemple `"3,chi"`) **fait échouer la construction de la carte** s'il n'est pas dans l'enum `COUNTER` du
  moteur : voir `reference/compteurs.json`, et signale-le **avant** tout.

```json
{
    "card_id": "lj003",
    "type": "Upgrade",
    "name": "* Tuning Fork",
    "subtitle": "",
    "desc": {
        "Cost": "1",
        "RES": "Y",
        "Class": "Hero"
    },
    "traits": [
        "ITEM"
    ],
    "set_name": "Lockjaw",
    "text": "You may play [[LOCATION]] supports from your discard pile during your turn <i>(paying their resource costs)</i>.\n<b>Resource</b>: Exhaust Tuning Fork → generate a [wild] resource.",
    "custom": "Nugget"
}
```

```json
{
    "card_id": "lj010",
    "type": "Event",
    "name": "Zooming Around",
    "subtitle": "",
    "desc": {
        "Cost": "2",
        "RES": "Y",
        "Class": "Hero"
    },
    "traits": [
        "TELEPORT",
        "SKILL"
    ],
    "set_name": "Lockjaw",
    "text": "<b>Hero Action</b>: Choose a player. Deal 1 damage to each enemy engaged with that player. Remove 1 threat from each scheme. If you paid for this card using a [mental] resource, you may change your form.",
    "custom": "Nugget"
}
```

### 4.5 L'obligation

* `type` = `Obligation`, `set_name` = le nom du héros.
* **`desc.GiveTo` = le nom de l'ALTER EGO** (sans l'étoile) : `"Lockjaw"`. C'est ce qui l'adresse au bon joueur.
  Contrôle du vérificateur : `GiveTo` doit être le nom de la face `b` (148 decks sur 152 ont **une** obligation ;
  trois seulement ont un `GiveTo` qui diffère du nom de l'alter ego : Iron Lad, SP//dr et Stan Lee, dont
  l'obligation `01165` est donnée à « Peter Parker »).
* `desc.Boost` : le nombre d'icônes de boost (l'obligation est aussi une carte de rencontre).
* Le texte commence par `<b><i>Give to the <Héros> player.</i></b>`.

```json
{
    "card_id": "lj013",
    "type": "Obligation",
    "name": "Canine Urges",
    "subtitle": "",
    "desc": {
        "Boost": "2",
        "GiveTo": "Lockjaw"
    },
    "traits": [],
    "set_name": "Lockjaw",
    "text": "<b><i>Give to the Lockjaw player.</i></b>\nYou may flip to alter-ego form. Choose:\n• Exhaust Lockjaw and Tuning Fork → remove Canine Urges from the game.\n• Discard all [[TELEPORT]] events in your hand. If no events were discarded this way, this card gains surge. Discard this obligation.",
    "custom": "Nugget"
}
```

### 4.6 Le set némésis

* `set_name` = **`"<Héros> Nemesis"`** pour **toutes** les cartes du set (42 entrées de `nemesis_set` du jeu font autrement : sets **empruntés** à un autre héros, ou `set_name` vide).
* En général **5 cartes** (145 decks sur 152) : un **sbire némésis** (`Minion`, souvent `ELITE`), un **complot
  annexe** (`SideScheme`, image **paysage**), des sbires ou attachements/traîtrises de renfort. Les quantités se
  déclarent dans `nemesis_set` du deck de départ (id répété = exemplaires multiples).
* **Le sbire némésis porte `desc.Nemesis`** (`"Lockjaw"` : le nom du héros ; sur 158 sbires marqués des sets némésis du jeu, exemplaires comptés, 109 portent exactement
  le nom de la face héros, les autres un autre nom — celui du deck, de l'alter ego : en cas de doute, question). C'est ce marqueur qui dit au moteur
  « celui-ci est *le* sbire némésis » (cartes du type « mettez en jeu le sbire némésis de ce joueur »). Sans lui,
  le jeu retombe sur une comparaison de noms de sets, fragile : correctif du 04/10/2026 sur Hercules.
* Un héros dont l'éditeur n'a **pas publié** l'obligation ni le set némésis (Iron Fist au 20/10/2026) a
  `obligations: []` et `nemesis_set: []` : tu le dis dans `QUESTIONS.md` — jamais une obligation inventée.

```json
{
    "card_id": "lj014",
    "type": "SideScheme",
    "name": "Dognapped!",
    "subtitle": "",
    "desc": {
        "StartingThreat": "2*",
        "Boost": "3"
    },
    "traits": [],
    "set_name": "Lockjaw Nemesis",
    "text": "<b>Forced Response</b>: After a [[TELEPORT]] event is played, place 1 threat here.",
    "custom": "Nugget"
}
```

```json
{
    "card_id": "lj015",
    "type": "Minion",
    "name": "* Annihilus",
    "subtitle": "",
    "desc": {
        "HP": "5",
        "SCH": "2",
        "ATK": "3",
        "Boost": "3",
        "Nemesis": "Lockjaw"
    },
    "traits": [
        "ARTHROSIAN",
        "ELITE"
    ],
    "set_name": "Lockjaw Nemesis",
    "text": "<b>Forced Interrupt</b>: When Annihilus would be defeated, shuffle him into the encounter deck instead.\n[star] <b>Boost</b>: After this activation ends, shuffle this card into the encounter deck.",
    "custom": "Nugget"
}
```

### 4.7 Les cartes d'aspect du pack (si elles existent)

Quand l'auteur ou la boîte fournit des cartes d'aspect (Lockjaw : `lj018`–`lj030`, classes `Aggression`,
`Protection`…), elles sont des **cartes joueur ordinaires** : `Class` = l'aspect, `set_name` = le nom du héros
(fan-made) ou `""` (boîte officielle). **Elles ne sont dans aucun `hero_deck`.** Elles n'entrent dans un deck que
par le `player_deck` **fourni par l'auteur** ou par le deck-builder.

### 4.8 Identifiants, préfixes (héros fan-made)

Le préfixe est **choisi avant la première carte** : propose **deux préfixes libres** à l'utilisateur (question à
choix multiple) et attends sa réponse. Préfixes **déjà pris** (lus dans le registre au moment de la construction ;
aussi dans `reference/prefixes-pris.json`) :

  `aa`, `ab`, `ag`, `ah`, `al`, `an`, `ar`, `as`, `av`, `bc`, `bk`, `bl`, `br`, `bt`, `bw`, `cc`, `cd`, `cn`, `dd`, `dr`, `dt`, `dz`, `gb`, `gp`, `gs`, `hc`, `hd`, `hk`, `ho`, `hs`, `ht`, `ih`, `il`, `im`, `ip`, `iw`, `jj`, `kb`, `lj`, `ls`, `ma`, `mf`, `mk`, `mu`, `mw`, `nt`, `nv`, `ok`, `pt`, `pu`, `ra`, `rg`, `rs`, `sa`, `sb`, `sc`, `sd`, `se`, `sf`, `sg`, `sh`, `si`, `sj`, `sk`, `sm`, `sn`, `sp`, `sr`, `ss`, `st`, `su`, `sw`, `ta`, `tc`, `td`, `te`, `tg`, `th`, `tj`, `tk`, `tl`, `tm`, `tr`, `ts`, `tt`, `tv`, `tx`, `ua`, `ub`, `ud`, `uj`, `ul`, `up`, `vp`, `vr`, `vv`, `vz`, `wc`, `wd`, `wx`, `yd`, `ze`

L'entrée à livrer dans `tools/prefixes.<pack>.fragment.json` (modèle : celle de Lockjaw) :

```json
{
  "lj": {
    "pack": "lockjaw",
    "libelle": "117. Custom (Lockjaw)",
    "cartes": 31,
    "depuis": "2026-08-12"
  }
}
```

### 4.9 Checklist de relecture des cartes d'un héros (à faire avant de livrer)

* [ ] chaque face d'identité a son `type` (`Hero` / `AlterEgo`), son `set_name`, son `*` dans le nom et sa clé `custom` ;
* [ ] face héros : `HP ATK THW DEF HS` ; alter ego : `HP REC HS` (des chaînes) ;
* [ ] toutes les cartes signature ont `Class: "Hero"` et le `set_name` du héros ;
* [ ] l'obligation a `GiveTo` = nom de l'alter ego, et un `Boost` ;
* [ ] les cartes némésis ont `set_name` = `"<Héros> Nemesis"`, le sbire némésis a `desc.Nemesis` ;
* [ ] aucun trou de numérotation ; `max_id` = le plus grand id ;
* [ ] les ressources (`RES`) ont été comparées, pas lues à vue ; chaque doute est une question ;
* [ ] les textes sont ceux de l'image, mot pour mot, balises comprises (`<b>`, `<i>`, `[[TRAIT]]`, `[mental]`, `[star]`…) ;
* [ ] tous les traits et compteurs nouveaux sont dans `BESOINS-MOTEUR.md` ;
* [ ] `verifier-livraison-heros.py` ne donne aucune ERREUR.



---

## 5. Le deck de départ, le set némésis, les variantes, l'extension

### 5.1 Le fichier `deck/starter/<héros>.json`, clé par clé

Le nom du fichier (`lockjaw.json`) est **l'identifiant du héros** : minuscules, chiffres, `_`. Il est unique dans
le jeu (voir `reference/decks-existants.json`, 152 identifiants). C'est aussi la clé de la réplique de recrutement.

| Clé | Type | Contenu | Mesuré sur les 152 decks |
|---|---|---|---|
| `version` | texte | `"0.5.8"` ou `"0.5.9"` (sans effet) | 0.5.8 ×132, 0.5.9 ×20 |
| `name` | texte | le nom **affiché** du héros | toujours |
| `metadata` | objet | `url` (source, ou `""`), `author`/`auteur`, `note`/`deck_note`, variantes, règles de deck-building (§5.3, §5.7) | toujours |
| `hero` | liste d'**une** chaîne | `"<face a>,<face b>[,<forme de plus>…]"` : héros d'abord, alter ego ensuite | toujours |
| `hero_deck` | liste de card_id | les cartes signature, **un id par exemplaire** (id répété = plusieurs exemplaires) | 15 cartes pour 145 decks |
| `set_aside` | liste | `[]` pour toi : **le moteur ne le lit pas en partie** (§2.2) ; le lanceur et le deck-builder le recopient, 34 decks anciens l'ont rempli | présent dans 150 |
| `obligations` | liste de card_id | l'obligation (UNE) | 1 pour 148 decks |
| `nemesis_set` | liste de card_id | le set némésis, exemplaires comptés | 5 pour 145 decks |
| `player_deck` | liste de card_id | la moitié d'aspect **fournie par l'auteur** ; **`[]` sinon** (règle 10) | `[]` pour 53 decks, 25 cartes pour 90, 24 à 27 pour 8, 15 pour 1 |
| `linked_identity` | objet | seulement Cloak & Dagger (§5.6) | 1 |

Un deck **complet** d'un héros maison **avec la decklist de l'auteur** (Lockjaw) :

*Fichier `Fusion/marvel-lcg-src/deck/starter/lockjaw.json` (copie exacte, lue dans le depot au moment de la construction).*

```json
{
    "version": "0.5.8",
    "name": "Lockjaw",
    "metadata": {
        "url": "https://drive.google.com/drive/folders/1kG_qSxUH4rf0wgXxoLr0HPcLtOqEqtAN",
        "author": "Nugget",
        "note": "Decklist officielle du scan StarterDeck-Lockjaw.png (aspect Protection). Le pack fournit aussi 13 cartes d'aspect « Lockjaw and the Pet Avengers » (lj018-lj030), dont Zabu / Throg / Redwing qui ne sont pas dans ce deck mais restent disponibles au deck-builder."
    },
    "hero": [
        "lj001a,lj001b"
    ],
    "hero_deck": [
        "lj002",
        "lj003",
        "lj004",
        "lj005",
        "lj006",
        "lj007",
        "lj008",
        "lj008",
        "lj009",
        "lj009",
        "lj010",
        "lj010",
        "lj011",
        "lj011",
        "lj012"
    ],
    "set_aside": [],
    "obligations": [
        "lj013"
    ],
    "nemesis_set": [
        "lj014",
        "lj015",
        "lj016",
        "lj016",
        "lj017"
    ],
    "player_deck": [
        "lj021",
        "lj022",
        "09012",
        "09014",
        "01079",
        "01079",
        "09019",
        "lj023",
        "lj023",
        "lj023",
        "lj024",
        "lj024",
        "lj026",
        "lj025",
        "lj029",
        "lj027",
        "lj028",
        "lj028",
        "01088",
        "01089",
        "01090",
        "lj030",
        "01091",
        "01092",
        "05033"
    ]
}
```

Un héros **officiel dont l'éditeur n'a pas tout publié** (Iron Fist, 20/10/2026) : `obligations` et `nemesis_set`
vides, `player_deck` vide, et une `deck_note` qui dit ce qui manque et pourquoi.

*Fichier `Fusion/marvel-lcg-src/deck/starter/iron_fist.json` (copie exacte, lue dans le depot au moment de la construction).*

```json
{
    "version": "0.5.9",
    "name": "Iron Fist",
    "metadata": {
        "url": "https://www.fantasyflightgames.com/way-of-the-iron-fist/",
        "deck_note": "Hero Pack officiel MC64EN (sortie novembre 2026). Seul ce qui est imprime et publie : identite et 15 cartes signature. Obligation et set nemesis : non publies au 20/10/2026, laisses vides. player_deck vide (PROCESSUS-HEROS etape 3)."
    },
    "hero": [
        "64001a,64001b"
    ],
    "hero_deck": [
        "64002",
        "64002",
        "64002",
        "64003",
        "64004",
        "64004",
        "64005",
        "64005",
        "64006",
        "64007",
        "64008",
        "64009",
        "64010",
        "64011",
        "64012"
    ],
    "set_aside": [],
    "obligations": [],
    "nemesis_set": [],
    "player_deck": []
}
```

### 5.2 Règles de contenu (toutes contrôlées par `verifier-livraison-heros.py`)

1. **`hero`** : la première face est de type `Hero`, la deuxième de type `AlterEgo` ; une forme de plus (`c`…)
   se liste **après** (Ant-Man : `"12001a,12001b,12001c"`). Les trois (ou cinq) faces existent dans `cards.json`.
2. **`hero_deck`** : ne contient que des cartes **de classe `Hero` de CE héros** (même `set_name`). **Jamais la
   carte signature d'un autre héros** (règle 11). Compte attendu : 15 (145 decks sur 152) ; un autre total se
   **justifie** dans `QUESTIONS.md` (le deck imprimé est-il vraiment différent ?).
3. **Exemplaires** : le plus grand nombre d'exemplaires d'un même `card_id` vaut 3 dans 86 decks, 2 dans 44, 1 dans 12, 4 dans 8, 5 dans 2. Si la carte
   imprime `MaxPerDeck`, c'est la limite. Plus de 3 sans `MaxPerDeck` → vérifie l'image.
4. **`obligations`** : une carte de type `Obligation`, avec `desc.GiveTo` = nom de l'alter ego.
5. **`nemesis_set`** : des cartes de rencontre (jamais des cartes joueur), de `set_name` `"<Héros> Nemesis"` ;
   un sbire marqué `desc.Nemesis`. Un set **emprunté** à un autre héros (Viv Vision emprunte le modulaire Zzzax)
   est possible : c'est une décision, à écrire dans `metadata.nemesis_note`.
6. **`player_deck`** : **vide** pour un héros maison, **sauf** si l'auteur fournit sa decklist ; alors
   `metadata.note` le dit (« Decklist officielle du scan StarterDeck-… »), chaque id existe, aucune signature
   d'un autre héros, 24 à 27 cartes. Héros **officiel** : le deck imprimé dans la boîte.
7. **`metadata.author`** (ou `auteur`) = la clé `custom` des cartes du héros maison.

### 5.3 Variantes d'un héros

Un héros n'a qu'**une tuile** dans le lanceur. Ce qu'il a de particulier se choisit dans une **modale** au clic
(version du deck de héros, identité alternative, art, ressources). Trois mécanismes, à ne pas confondre :

| Le héros a… | Où le déclarer | Exemple |
|---|---|---|
| un autre **deck de héros** (allié signature, alter ego avec sa propre obligation) | un **second** `deck/starter/<id>.json` **complet**, avec `metadata.variante_de: "<id de base>"` et `metadata.variante_nom` ; **la base porte aussi son `variante_nom`** | `hellcat.json` + `hellcat_she_hulk.json` |
| une autre **identité** dans le même deck (mêmes cartes, autres faces) | `metadata.hero_alts` du deck de base : `[{"name": "…", "hero": ["xx001c,xx001d"], "url": "…"}]` | The Thing Guardian (`th001c,th001d`) |
| un **art** alternatif | `ARTS_HEROS` (côté Claude, `BESOINS-MOTEUR.md`) | M3T4LB0X |

Le fichier de variante reste un deck **montable** (même contrôle que le deck de base). C'est le catalogue qui le
replie sous sa base, pas le moteur. **Ne crée jamais un deuxième deck de départ pour une identité alternative**
(`hero_alts`) : un deuxième héros apparaîtrait dans la grille.

Les deux exemples réels, côté métadonnées seulement :

*Extrait de `Fusion/marvel-lcg-src/deck/starter/hellcat_she_hulk.json` (de « "metadata" » a « "hero": [ »).*

```json
 "metadata": {
  "url": "",
  "auteur": "jakxin",
  "note": "Deck de depart IMPRIME par l'auteur (HellcatStarterDecklist.png), recopie tel quel. Black Cat (custom, listee) absente du dossier : laissee de cote sur decision utilisateur du 11/09/2026, d'ou 24 cartes au lieu de 25. Reskins hc023-hc026 = doublons avec l'art de jakxin (decision utilisateur).",
  "variante": "She-Hulk a la place d'Iron Man : alliee signature alternative ajoutee par l'auteur « sur demande ». Deuxieme deck de depart sur decision utilisateur du 11/09/2026.",
  "variante_de": "hellcat",
  "variante_nom": "Miss Hulk (alliée signature)"
 },
```

*Extrait de `Fusion/marvel-lcg-src/deck/starter/the_thing.json` (de « "metadata" » a « "hero": [ »).*

```json
    "metadata": {
        "author": "DesignHacker",
        "url": "https://drive.google.com/drive/folders/10dzfME7sX4EDR5CbjsI48X3hAzZVUv5w",
        "hero_alts": [
            {
                "name": "The Thing (Guardian)",
```

### 5.4 `data/nemesis/<héros>_nemesis.json` (facultatif)

⚠ **Ce n'est pas la source du set némésis** : le `nemesis_set` utilisé vient du **deck de départ**, et le moteur le lit au même endroit.
Le lanceur liste bien ces fichiers (classés « nemesis », puis filtrés : ils ne s'affichent pas). Le fichier sert à
charger le set némésis **comme un set de rencontre nommé** (`data/nemesis/` figure dans les dossiers de sets de
rencontre du moteur) : utile le jour où une carte ou un scénario le réclame par son nom. 72 des 152 decks n'ont pas
de fichier `<id>_nemesis.json` et fonctionnent : il est facultatif. Si tu le livres, `encounters` = **exactement** `nemesis_set` :

*Fichier `Fusion/marvel-lcg-src/data/nemesis/lockjaw_nemesis.json` (copie exacte, lue dans le depot au moment de la construction).*

```json
{
    "version": "0.5.8",
    "name": "Lockjaw Nemesis",
    "encounters": [
        "lj014",
        "lj015",
        "lj016",
        "lj016",
        "lj017"
    ]
}
```

### 5.5 L'entrée de l'extension : `data/sets_info.<pack>.fragment.json`

La liste `heroes` de l'entrée est ce qui range le héros dans son extension. Pour un pack de héros : `scenarios`
et `encounters` sont **vides** ; `name` = la clé du pack ; `max_id` = le plus grand `card_id`. La clé est
`"N. Custom (<Nom>)"` pour un héros maison (`N` est attribué par Claude : laisse la lettre `N`) ; pour un héros
officiel, `"<n° du pack>. <Nom>"`.

```json
{
  "117. Custom (Lockjaw)": {
    "name": "lockjaw",
    "scenarios": [],
    "heroes": [
      "lockjaw"
    ],
    "encounters": [],
    "max_id": "lj030"
  }
}
```

```json
{
  "64. Iron Fist": {
    "name": "iron_fist",
    "scenarios": [],
    "heroes": [
      "iron_fist"
    ],
    "encounters": [],
    "max_id": "64012"
  }
}
```

### 5.6 L'identité liée (Cloak & Dagger) — pour information

Un pack qui fait piloter **deux identités par un seul joueur** déclare, dans le deck, une clé `linked_identity` :
une identité complète (`hero`, `hero_deck`, `set_aside`, `obligations`, `nemesis_set`, `player_deck`) que le
moteur développe en un **second joueur** au chargement. C'est le **seul** pack construit ainsi : n'invente pas ce
mécanisme pour un héros ordinaire ; si le héros que tu livres l'exige, **question** et `BESOINS-MOTEUR.md`.

### 5.7 Règles de deck-building propres au héros : `metadata.deckbuilding`

Certaines identités changent les règles de construction (autant d'aspects que l'on veut, N cartes d'autres aspects
pourvu qu'elles aient tel trait…). Le deck-builder les applique ; **le moteur ne valide jamais un deck** — ces
règles n'existent que dans le deck-builder, et un deck de départ écrit à la main les contourne. On les déclare dans
`metadata.deckbuilding`, **accompagnées d'une `deckbuilding_note`** qui cite le texte imprimé. Dix decks du jeu
en ont :

```json
{
  "ares": {
    "hors_aspect": {
      "max": 5,
      "traits": [
        "TACTIC"
      ],
      "types": [
        "Upgrade"
      ],
      "label": "5 améliorations TACTIC d’autres aspects (Lord of War)"
    }
  },
  "binary": {
    "ressources_egales": {
      "couleurs": [
        "Y",
        "B",
        "R"
      ],
      "label": "autant de cartes à ressource imprimée [énergie], [mentale] et [physique] (Carol Danvers)"
    }
  },
  "doctor_doom": {
    "aspects": {
      "min": 1,
      "max": 1
    },
    "hors_aspect": {
      "max": 6,
      "traits": [
        "TECH",
        "SPELL"
      ],
      "label": "6 cartes TECH/SPELL d’autres aspects"
    },
    "types_interdits": [
      "Ally"
    ],
    "note": "dd001b : « You cannot include any additional allies in your deck » + « Master of Magic and Technology — up to 6 TECH and/or SPELL cards from aspects other than your chosen aspect »."
  },
  "gamora": {
    "hors_aspect": {
      "max": 6,
      "traits": [
        "ATTACK",
        "THWART"
      ],
      "types": [
        "Event"
      ],
      "label": "6 événements ATTACK/THWART d’autres aspects (Skilled Tactician)"
    }
  },
  "harry_osborn": {
    "hors_aspect": {
      "max": 3,
      "compte": "titres",
      "traits": [
        "TECH"
      ],
      "types": [
        "Upgrade"
      ],
      "label": "3 améliorations TECH d’autres aspects (Harry Osborn)"
    }
  },
  "iron_patriot": {
    "types_interdits_aspect": [
      "Ally"
    ]
  },
  "jennika": {
    "path": {
      "nom": "Sosaiken",
      "types": [
        "Bushido",
        "Ninjutsu",
        "Kuji-Kiri",
        "Taijutsu"
      ],
      "aspects_max": 0,
      "basic": true
    }
  },
  "maria_hill": {
    "hors_aspect": {
      "max": 3,
      "compte": "titres",
      "traits": [
        "S.H.I.E.L.D."
      ],
      "types": [
        "Support"
      ],
      "label": "3 supports S.H.I.E.L.D. d’autres aspects (Maria Hill)"
    }
  },
  "night_thrasher": {
    "hors_aspect": {
      "max": 4,
      "traits": [
        "SKILL"
      ],
      "label": "4 cartes SKILL d’autres aspects (Tech Deck)"
    }
  },
  "red_sonja": {
    "hors_aspect": {
      "max": 6,
      "types": [
        "Event"
      ],
      "label": "6 événements d’autres aspects (Red Sonja)"
    }
  }
}
```

Les clés reconnues (`public/js/deckbuilder/regles.js`) : `aspects {min, max, label}`, `hors_aspect {max, traits,
types, compte, label}` (`"compte": "titres"` compte des titres et non des exemplaires), `types_interdits`,
`types_interdits_aspect`, `ressources_egales {couleurs, label}`, `path {…}` (voies TMNT Shinobi). `note` (texte libre) est tolérée. Toute autre
clé est une **erreur**. Une règle que ces clés ne savent pas dire → `BESOINS-MOTEUR.md`.



---

## 6. Les scripts des cartes du héros (`src/cards/pack/<pack>/…`)

Un script est un fichier Python qui définit **`GetAbilities()`** et renvoie la liste des capacités de **une face de
carte**. Les règles générales (surface utilisable, types de capacité, fabriques, coûts, cibles, 67 exemples réels
classés par mécanique) sont dans l'**annexe A** (`annexes/A-kit-cartes.md`), les **recettes mécanique par
mécanique** dans l'**annexe B**, les **mots-clés** dans l'**annexe C**, et **l'index de tout ce que le moteur
sait faire** dans l'**annexe I**. Ce chapitre dit ce qui est **propre à un héros**.

### 6.1 Où ranger un script, et les `__init__.py`

Le moteur cherche le script d'une carte dans **`src/cards/pack/<pack>/<set_nettoyé>/<card_id>.py`**, puis, à
défaut, dans **`src/cards/pack/<pack>/<card_id>.py`** (racine du pack). `<set_nettoyé>` est le `set_name` de la
carte passé dans `CleanName` (minuscules, espaces → `_`, apostrophes et ponctuation retirées) :

*Extrait de `outils/verifier-livraison-campagne.py` (de « def clean_name » a « def lire_json »).*

```python
def clean_name(nom):
    """Copie de `FileManager.CleanName` (src/engine/file/manager.py)."""
    return (nom.lstrip("*").strip().lower().replace(" - ", "_").replace(" & ", "_").replace(" ", "_")
            .replace("'", "").replace("-", "_").replace("!", "").replace("?", "").replace("(", "").replace(")", "")
            .replace(".", "").replace(",", "").replace('"', "").replace("&", "_").replace("#", "").replace("/", ""))

```

| `set_name` de la carte | Dossier du script |
|---|---|
| `Lockjaw` | `src/cards/pack/lockjaw/lockjaw/` |
| `Lockjaw Nemesis` | `src/cards/pack/lockjaw/lockjaw_nemesis/` |
| `Iron Fist` | `src/cards/pack/iron_fist/iron_fist/` |
| `""` (carte d'aspect d'une boîte officielle) | la racine du pack : `src/cards/pack/ant/12011.py` |

⚠ **Un dossier de set sans `__init__.py` rend TOUTES ses cartes muettes, sans la moindre erreur.** Un script
rangé dans le mauvais dossier est muet aussi. `verifier-livraison-heros.py` les attrape tous les deux.

Les trois `__init__.py` d'un pack de héros réel (Lockjaw). Le premier est celui du pack, le deuxième celui du set
`lockjaw/`, le troisième celui du set `lockjaw_nemesis/` :

*Fichier `Fusion/marvel-lcg-src/src/cards/pack/lockjaw/__init__.py` (copie exacte, lue dans le depot au moment de la construction).*

```python
from cards.pack import *
```

*Fichier `Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw_nemesis/__init__.py` (copie exacte, lue dans le depot au moment de la construction).*

```python
from cards.pack import *

from cards.pack.lockjaw.lockjaw import Companion, PayeAvecMental
```

*Fichier `Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw/__init__.py` (copie exacte, lue dans le depot au moment de la construction).*

```python
from cards.pack import *

# Fabriques partagées du pack custom « Lockjaw » (Nugget, Marvel Champions
# Custom Project, Cycle I).
#
# Le pack tourne autour du trait TELEPORT : la plupart des cartes signature
# font changer de forme, et plusieurs cartes récompensent le paiement avec la
# ressource « os » du Tuning Fork. Le moteur n'ayant que quatre couleurs, cet
# os est rendu par [wild] (G) : le Tuning Fork en génère, et les cartes qui
# demandent « if you paid using a [os] resource » testent la couleur G.
# Écart documenté dans GUIDE-CREATION-CONTENU.md §9.


def Companion() -> List['Ability']:
    """« Companion » : hors limite d'alliés, et ne peut pas défendre.

    Mot-clé maison du pack, sans équivalent dans le moteur : il se compose de
    deux règles déjà existantes.
    """
    return [
        *AbilityFactory.ThisNotCountAllyLimit(),
        *AbilityFactory.UnitCannotDefend(
            "This",
            None,
            cannot_trigger_defense_ability=True,
        ),
    ]


def PayeAvecMental(effect: 'Effect') -> bool:
    """« If you paid for this card using a [mental] resource ».

    CORRECTIF (9/8/2026) — signale en jeu : « Ruff Ambush n'a fait que 5 degats
    alors que j'ai paye en mental ». La fonction s'appelait `PayeAvecMental` et
    testait la couleur "G", c'est-a-dire une ressource WILD. L'icone des
    scans avait ete prise pour un os : ce sont des noeuds relies, l'icone de
    la ressource MENTALE de ce pack. Verification faite en comparant a
    l'icone imprimee de lj005 Kamala's Room, dont la fiche porte RES=B — meme
    forme, sur fond bleu — et a celle de lj002 Black Bolt, RES=G, qui est une
    ETOILE verte, tout autre.

    Quatre cartes reposaient sur cette lecture : lj001a Fetch!, lj009 Fast
    Travel, lj010 Zooming Around et lj011 Ruff Ambush. Leur clause bonus ne
    partait jamais quand le joueur payait comme la carte le demande.
    """
    return effect.GetPaidResources().HasColor("B")


# CORRECTIF 4/8/2026 : `ChangerDeForme` et `YouMayChangeForm` etaient appeles
# par Teleport To Safety lj008, Fast Travel lj009 et lj010, mais definis NULLE
# PART. Les trois cartes levaient un NameError et se defaussaient sans rien
# faire. Trouve en ecrivant le premier cas de comportement de Fast Travel.
def ChangerDeForme(joueur: 'Player', effect: 'Effect') -> None:
    """Fait changer de forme l'identite du joueur vise."""
    identite = joueur.GetIdentity()
    if identite is not None:
        identite.ChangeToOtherIdentityForm(effect)


def YouMayChangeForm(joueur: 'Player', effect: 'Effect') -> None:
    """« You may change your form » : le changement reste au choix du joueur."""
    joueur.MayChooseOneAbility(
        effect,
        AbilityFactory.ForChoiceAbility(
            "Change your form",
            lambda targets: ChangerDeForme(joueur, effect),
        ).SetHasNoTargetEffect(),
    )
```

⚠ Le commentaire d'en-tête de ce dernier fichier est **historique** : il parle d'une « ressource os » rendue par
`[wild]`. C'est faux depuis le 9/8/2026 : l'icône imprimée est une ressource **mentale** (`B`), et c'est ce que
teste `PayeAvecMental`. Le code, lui, est exact. (Leçon de la règle 8 : une icône lue à vue.)

Chaque script commence par **`from . import *`**.

### 6.2 Une face d'identité = un script, avec **seulement les capacités imprimées**

* Les **statistiques** de base (ATK, THW, DEF, REC, taille de main) viennent de `desc` et sont **automatiques** :
  jamais dans un script.
* Chaque **face** (`a`, `b`, et les formes de plus) qui imprime une capacité a **son propre fichier**
  (`lj001a.py`, `lj001b.py`). Une face sans capacité imprimée n'a **pas** de script (Harry Osborn n'a pas de
  `ho001b.py`).
* Le **commentaire d'en-tête** de chaque script recopie le texte imprimé de la carte, cite les **cartes de
  référence** (celles dont tu as copié la fabrique) et liste les **mots-pièges** du texte (§6.8). Ce n'est pas
  décoratif : c'est ce que Claude relit pour décider si ton script est fidèle.

La face **héros** et la face **alter ego** d'un héros à capacité de fouille et de mise en jeu (Lockjaw) :

*Fichier `Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw/lj001a.py` (copie exacte, lue dans le depot au moment de la construction).*

```python
from . import *

# * Lockjaw (face héros) — custom « Nugget »
# Fetch! — Action: Exhaust Lockjaw and spend a [wild] resource → choose a
#   non-resource card in any players' discard pile and add it to their owner's
#   hand. (Limit once per round.)


def GetAbilities() -> Sequence['Ability']:

    def fetch(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        initiator = effect.GetInitiator()

        candidats: List['CardFace'] = []
        for joueur in Worlds.GetPlayers(effect):
            candidats += [
                x for x in joueur.discard_pile.Get()
                if not Resource.IsType(x)
            ]
        if not candidats:
            return

        # CORRECTIF : `ChooseAbilities` + `Select.From(faces=...)` ne
        # restreignait RIEN sur des cartes hors jeu : le choix tombait sur la
        # MANIGANCE PRINCIPALE, qui partait dans la main de Lockjaw puis dans
        # la defausse. Plus de manigance, donc IndexError a la fin de partie.
        choisie = initiator.AskChooseFace(
            candidats,
            effect,
            prompt="Add a non-resource card from a discard pile to its owner's hand",
        )
        if choisie is None:
            return

        from game.player import Player
        # CORRECTIF (4/8/2026) : `GetOwner` peut rendre le SCENARIO (cartes
        # cote Rencontre), pas un joueur.
        proprietaire = choisie.GetOwner()
        if not isinstance(proprietaire, Player):
            proprietaire = initiator
        proprietaire.GainCard(choisie, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            fetch,
        ).SetName("Fetch!")
        # CORRECTIF (9/8/2026) : l'icone du texte est une MENTALE, pas un wild.
        # Voir PayeAvecMental pour la verification sur les scans.
        .SetCost(Cost("B"))
        .SetCostFunc(CostFunc.Exhaust("This"))
        .LimitOncePerRound(),
    ]
```

*Fichier `Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw/lj001b.py` (copie exacte, lue dans le depot au moment de la construction).*

```python
from . import *

# * Lockjaw (face alter-ego) — custom « Nugget »
# Setup: Search your deck, hand and discard pile for Tuning Fork and put it
#   into play.
# Cheer Up — Response: After you change to this form, ready a friendly
#   character.


def GetAbilities() -> Sequence['Ability']:

    def setup(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        initiator = effect.GetInitiator()

        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            include_player_hand_cards=True,
            name="Tuning Fork",
            card_type=Upgrade,
        )
        if face:
            face.PutIntoPlay(initiator, effect)

    def cheer_up(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            setup
        ),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            cheer_up,
            to_this_form=True,
        ).SetName("Cheer Up")
        .SetTarget(Friend, canbe_ready=True),
    ]
```

Les deux faces d'un héros officiel à **compteurs** (Iron Fist : le jeton Chi vit **sur l'identité**) :

*Fichier `Fusion/marvel-lcg-src/src/cards/pack/iron_fist/iron_fist/64001a.py` (copie exacte, lue dans le depot au moment de la construction).*

```python
from . import *

# * Iron Fist (face heros, 1A) — DEFENDER. K'UN-LUN. MARTIAL ARTIST.
# PV 10, ATQ 2, CTR 1, DEF 2, main 5.
# Martial Arts Master — Response: After you play a card, place 1 chi counter here.
# Forced Response: After the player phase ends, remove all but 4 chi counters from here
#   and heal 1 damage for each chi counter removed this way.
#
# CARTES DE REFERENCE
#  - « After you play a card » (toute carte) : `fne/60027` Move in Shadow
#    (`AfterPlayerPlayedCard(Response, "You", None, op)` : `None` = n'importe quelle carte).
#  - compteur pose sur l'identite : `venus/tv001a` (`Faces.PlaceCountersOn([identite], n, 'dredge', effect)`).
#  - « After the player phase ends » : `aos/maria_hill/50029` Press Conference et
#    `michelangelo/tm009` (`AfterPhaseEnd(ForcedResponse, "Player", op)`).
#  - soin de soi : `jubilee/47012` (`this.HealthUnits([this], n, effect)`).
#
# TEXTE CONTRE CODE
#  ⚠ « Response » nu (pas « Hero Response ») mais imprime sur la face HEROS : la capacite
#    n'existe que quand cette face est visible ; Danny Rand ne pose pas de chi.
#  ⚠ « play a card » : une carte JOUEE (paiement compris), pas « mise en jeu » (Meditation,
#    Book of the Iron Fist ne declenchent rien) ; toute carte, tout type.
#  ⚠ « here » = cette carte, l'identite : les compteurs restent au retournement (decision n°5).
#  ⚠ « remove all BUT 4 » : on garde 4, on retire le SURPLUS (rien si 4 ou moins).
#  ⚠ « heal 1 damage for EACH chi counter removed THIS WAY » : soin = nombre retire par cet
#    effet, sur Iron Fist (« heal » sans cible = le personnage qui porte la capacite).
#  ⚠ Forced Response : aucune question ; ne part que s'il y a un surplus (sinon rien a faire).


def GetAbilities() -> Sequence['Ability']:

    def poser_un_chi(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Hero)
        Unused(message)
        Faces.PlaceCountersOn([this], 1, CHI, effect)

    def surplus(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> bool:
        return Chi(effect.this) > CHI_CONSERVES

    def fin_de_phase(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        this = effect.this.CastTo(Hero)
        Unused(message)
        retires = Chi(this) - CHI_CONSERVES
        if retires <= 0:
            return
        Faces.RemoveCountersOn([this], retires, CHI, effect)
        this.HealthUnits([this], retires, effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            None,
            poser_un_chi,
        ).SetName("Martial Arts Master"),
        AbilityFactory.AfterPhaseEnd(
            AbilityType.ForcedResponse,
            "Player",
            fin_de_phase,
            conditions=[surplus],
        ),
    ]
```

*Fichier `Fusion/marvel-lcg-src/src/cards/pack/iron_fist/iron_fist/64001b.py` (copie exacte, lue dans le depot au moment de la construction).*

```python
from . import *

# * Danny Rand (face alter ego, 1B) — CIVILIAN. PV 10, REC 4, main 6.
# Your Technique cards lose temporary.
# Meditation — Action: Search your deck and discard pile for a Technique card. Put that
#   card into play. (Limit once per phase.)
#
# CARTES DE REFERENCE
#  - « lose(s) the temporary keyword » en continu : `cyclops/33004` Field Commander
#    (`GiveKeywordToInPlayWhenApplyThis(CardFinder(...), temporary=-1)`).
#  - « Search your deck and discard pile for X and put it into play » : `bp/51025` Heart of the
#    Panther et `kate_bishop/kb001b` (`Search.PlayerCard(..., include_player_deck=True,
#    include_discard_pile=True)` puis `face.PutIntoPlay(joueur, effect)`).
#  - « (Limit once per phase.) » : `phoenix/34001a` (`LimitOncePerPhase()`).
#
# TEXTE CONTRE CODE
#  ⚠ « YOUR Technique cards » : `control_by="You"` ; le trait, jamais le nom.
#  ⚠ « lose temporary » : capacite CONTINUE de la face Danny Rand seulement. Au retournement en
#    Iron Fist, la face qui la porte n'est plus visible : les Techniques redeviennent Temporary et
#    partent a la fin du round (`ProcessTemporary`) — decision utilisateur n°2.
#  ⚠ « Put that card into play » : sans paiement ; une amelioration sans cible imprimee s'attache a
#    l'identite du joueur (selecteur par defaut de `CanPlayThisUpgradeCard`, play.py) — decision n°1.
#  ⚠ « deck AND discard pile » : les deux zones ; deck remelange (comportement par defaut).
#  ⚠ « Action » nue imprimee sur l'alter ego : utilisable en forme Danny Rand seulement (la face).
#  ⚠ « Limit once per phase » : temoin d'epuisement dans les cas.


def GetAbilities() -> Sequence['Ability']:

    def meditation(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            trait=TRAIT_TECHNIQUE,
        )
        if face:
            face.PutIntoPlay(joueur, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Upgrade, trait=TRAIT_TECHNIQUE),
            control_by="You",
            temporary=-1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            meditation,
        ).SetName("Meditation")
        .LimitOncePerPhase(),
    ]
```

### 6.3 Les accroches propres aux identités (recettes vérifiées)

| Texte imprimé sur l'identité | Fabrique | Carte modèle | À savoir |
|---|---|---|---|
| **Setup:** … | `AbilityFactory.WhenCardSetup("This", op)` — **deux arguments** | `lj001b`, `an001b`, `ok001b` | à un seul argument la capacité ne fait rien |
| After you change to this form | `AfterUnitChangeForm(type, "You", op, to_this_form=True)` | `01019a`, `12001a`, `bt001b` | |
| After you attack an enemy | `AfterUnitAttackEnd(type, "You", op, against_who=Enemy)` | `iw001a`, `ho001a` | le champ du message est `attacked_targets`, pas `attacked` |
| After you play a card | `AfterPlayerPlayedCard(Response, "You", None, op)` | `64001a`, `fne/60027` | « jouer » ≠ « mettre en jeu » |
| After the player phase ends | `AfterPhaseEnd(ForcedResponse, "Player", op)` | `64001a`, `aos/50029` | |
| Your <Trait> cards lose Temporary / gain X (continu) | `*GiveKeywordToInPlayWhenApplyThis(CardFinder(card_type=…, trait=…), control_by="You", …)` | `64001b`, `cyclops/33004` | un `CardFinder` à trait doit porter aussi `card_type` |
| Un compteur sur l'identité | `…CostFunc.Counter("YourIdentity", n, 'chi')` | `64006`, `64010`–`64012` | sans la condition « au moins n », la capacité est offerte impayable |
| Mettre une carte **de côté** à la mise en place | `AbilityFactory.BeginGameWithSetAside([ids], op)` sur la **face alter ego** | `bt001b`, `09001b`, `al001b`, `36001b` | voir §6.4 |

### 6.4 Les cartes « mises de côté » : `set_aside` n'est pas lu

Le champ `set_aside` du deck de départ **n'est pas lu par le moteur en vraie partie** (§2.2). Une carte qui doit
exister « à côté » (un pool de cartes Discovery, une forme de plus, un compagnon) se crée par
`AbilityFactory.BeginGameWithSetAside([...])` **dans le script de la face alter ego**, puis se relit par
`set_aside_deck.Get()`. Modèle commenté : `bt001b` (Beast). Le harnais de test, lui, fait exister cette carte avec
`Puzzle.CreatePlayerAdditionalDeck` : **un cas vert ne prouve pas** que la carte existe en vraie partie
(piège payé sur Alligator Loki).

### 6.5 Les cartes signature, l'obligation, les cartes némésis

* **Cartes signature** : l'étiquette `Hero Action` / `Hero Response` / `Hero Interrupt` n'autorise la carte que
  **sous la forme héros** ; une carte sans cette étiquette se joue sous les deux formes. Cherche la mécanique
  dans le catalogue de l'annexe A (§8), jamais dans ta mémoire de l'ancien jeu.
* **Obligation** : c'est une carte de rencontre « donnée » au joueur ; son script porte le texte imprimé
  (« You may flip to alter-ego form. Choose: … »).
* **Cartes némésis** : des cartes de rencontre ordinaires (sbire, complot annexe, attachement) rangées dans
  `<set> Nemesis` ; leurs mots-clés lus dans `desc` (`Surge`, `Boost`…) ne demandent **aucun** script.

Quatre scripts réels, de l'événement le plus simple à l'obligation à choix :

*Fichier `Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw/lj008.py` (copie exacte, lue dans le depot au moment de la construction).*

```python
from . import *

# Teleport To Safety — custom « Nugget »
# Interrupt: When an identity would take any amount of damage from an attack,
#   change that identity's form → prevent all of that damage.


def GetAbilities() -> Sequence['Ability']:

    def teleporter(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        victime = message.trigger
        joueur = victime.GetControlByPlayer()
        if joueur is not None:
            ChangerDeForme(joueur, effect)
        message.PreventDamage("All", effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            Identity,
            teleporter,
            is_from_attack=True,
        ).SetPlay(),
    ]
```

*Fichier `Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw/lj010.py` (copie exacte, lue dans le depot au moment de la construction).*

```python
from . import *

# Zooming Around — custom « Nugget »
# Hero Action: Choose a player. Deal 1 damage to each enemy engaged with that
#   player. Remove 1 threat from each scheme. If you paid for this card using
#   a [wild] resource, you may change your form.


def GetAbilities() -> Sequence['Ability']:

    def zoomer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()

        for cible in effect.targets:
            joueur = cible.GetControlByPlayer()
            if joueur is None:
                continue
            # « chaque ennemi engage avec ce joueur » = le vilain plus les
            # sbires engages, montage de la carte officielle Energy Daggers
            # (01046) : le moteur n'expose pas d'engagement pour le vilain.
            vilain = Worlds.FindVillain(effect)
            ennemis = ([vilain] if vilain else []) + joueur.GetEngagedMinions()
            ennemis = [x for x in ennemis if not x.IsDefeated()]
            if ennemis:
                this.DealDamage(ennemis, 1, effect)

        schemes = Worlds.FindCardsOnField(effect, card_type=Scheme2)
        if schemes:
            this.RemoveThreatFromSchemes(schemes, 1, effect)

        if PayeAvecMental(effect):
            YouMayChangeForm(initiator, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            zoomer,
        ).SetPlay()
        .SetTarget("Players"),
    ]
```

*Fichier `Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw/lj013.py` (copie exacte, lue dans le depot au moment de la construction).*

```python
from . import *

# Canine Urges — custom « Nugget » (obligation de Lockjaw)
# Give to the Lockjaw player. You may flip to alter-ego form. Choose:
# - Exhaust Lockjaw and Tuning Fork -> remove Canine Urges from the game.
# - Discard all TELEPORT events in your hand. If no events were discarded this
#   way, this card gains surge. Discard this obligation.


def GetAbilities() -> Sequence['Ability']:

    def canine_urges(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(player, effect)

        fourchette = [
            x for x in Worlds.FindCardsOnField(effect, name="Tuning Fork", card_type=Upgrade)
            if x.GetControlByPlayer() == player
        ]

        def defausser_les_teleports(targets: Sequence['CardFace']) -> None:
            evenements = [
                x for x in player.hand_cards.GetAll()
                if Event.IsType(x) and x.HasTrait("TELEPORT")
            ]
            if evenements:
                Faces.DiscardAll(evenements, effect)
            else:
                ThisCardGainSurge(effect)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Lockjaw and Tuning Fork → remove Canine Urges from the game",
                lambda t: Faces.RemoveAllFromGame([this], effect),
                condition=(player.IsAlterEgo() and len(fourchette) > 0),
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))
            .SetCostFunc(CostFunc.Exhaust(
                name="Tuning Fork",
                card_type=Upgrade,
                from_where=["YouControlCards"])),
            AbilityFactory.ForChoiceAbility(
                "Discard all TELEPORT events in your hand. Discard this obligation",
                defausser_les_teleports,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            canine_urges
        )
    ]
```

*Fichier `Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw_nemesis/lj015.py` (copie exacte, lue dans le depot au moment de la construction).*

```python
from . import *

# * Annihilus — custom « Nugget » (némésis de Lockjaw)
# Forced Interrupt: When Annihilus would be defeated, shuffle him into the
#   encounter deck instead.
# [star] Boost: After this activation ends, shuffle this card into the
#   encounter deck.


def GetAbilities() -> Sequence['Ability']:

    def survit(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        message.SetBeInstead(effect)
        Faces.ShuffleAllTo([this], "EncounterDeck", effect)

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.ForcedInterrupt,
            "This",
            survit,
        ),
        # CORRECTIF 4/8/2026 : le handler appelait
        # `ShuffleThisCardIntoEncounterDeckAfterActivation`, qui n'existe pas,
        # sous une garde `in globals()`. La branche etait donc morte et le repli
        # melangeait la carte IMMEDIATEMENT au lieu d'attendre la fin de
        # l'activation. Le moteur a la fabrique exacte, employee par Monster
        # 02025.
        AbilityFactory.WhenBoostShuffleThisIntoEncounterDeckAfterActivationEnd(),
    ]
```

### 6.6 Un héros complet commenté : les recettes payées par Iron Fist (MC64)

<!-- extrait de docs/reference/RECETTES-MOTEUR.md -->
#### 14. Iron Fist officiel (MC64EN, `64001a`-`64012`, 20/10/2026) : ce que ce pack a payé

| Mécanique imprimée | Fabrique / chemin | Carte modèle | Piège |
|---|---|---|---|
| « Your X cards lose temporary » (continu, sur une face d'identité) | `*GiveKeywordToInPlayWhenApplyThis(CardFinder(card_type=Upgrade, trait="X"), control_by="You", temporary=-1)` | `64001b`, `cyclops/33004` | un `CardFinder` à trait DOIT porter aussi `card_type` (assert `len(params) == 2`, environment.py) ; au retournement la face cesse d'appliquer, la carte redevient Temporary (fin de round = `monde.ProcessTemporary(...)` dans le vérificateur) |
| « <NOM> gains retaliate X, X = compteurs sur cette carte » | `*GiveKeywordToInPlayWhenApplyThis(Hero, control_by="You", retaliate=1, get_new_value=fn, change_on_event=OnEvent.Counter("This", 'chi'))` | `64009`, `sm/27067` | le NOM de la face héros : `Hero`, jamais `"You"` (contre-cas alter ego) |
| « When you attack ... increase the amount of damage that attack deals by 1 (by 2 instead if basic) » | `WhenUnitWouldAttack(HeroInterrupt, "You", op)` + `message.DealAdditionalDamage(2 if message.IsBasicAttack() else 1, effect)` | `64008`, `54002` | un événement à plusieurs « Deal N damage » envoie UNE attaque PAR coup : l'Interruption est proposée à chaque coup — c'est la bonne lecture (Q1 tranchée par l'utilisateur le 20/10/2026, ruling des cartes à phrases répétées type Dance of Death) |
| « Discard ... until you discard an <Héros> card » | `joueur.DiscardDeckUntil(effect, set_name="<Héros>")` puis `Faces.AddToHand` | `64002` | « carte <Héros> » = bandeau du set signature (`set_name`), pas un trait ni un nom |
| « Remove N <compteurs> from <identité> → » (coût) | `.SetCostFunc(CostFunc.Counter("YourIdentity", n, 'chi'))` + `conditions=[AuMoinsChi(n)]` | `64006`, `64010`-`64012` | sans la condition, la capacité est offerte impayable (RECETTES §5) |

Harnais : `main_exclusive` DÉFAUSSE la main de départ APRÈS `mise_en_place` ; avec un deck de départ fait de cartes signature, la défausse se remplit de cartes du pack. Toute défausse construite pour un cas (fouille « deck and discard pile », « top card of your discard pile ») se pose donc dans `declencher`, après `Puzzle.EmptyPlayerDiscardPile()`. `cibles` : le pilote vise la PREMIÈRE cible listée encore en jeu à chaque choix (les trois coups de Fists of Fury sur la même), d'où le montage « sbire à 1 PV » pour prouver des choix indépendants. Lancer le harnais avec `CAS_PREFIX=<nom>` : sans préfixe, les journaux `/tmp/capacites_<index>.log` se mêlent à ceux des autres sessions.

### 6.7 Les déclencheurs côté joueur (recettes, §1 de l'annexe B)

<!-- extrait de docs/reference/RECETTES-MOTEUR.md -->
#### 1. Déclencheurs (côté joueur)

| Texte imprimé | Fabrique | Modèle | Piège |
|---|---|---|---|
| After you attack an enemy | `AfterUnitAttackEnd(type, "You", op, against_who=Enemy)` | iw001a, ho001a | le champ du message est `attacked_targets`, PAS `attacked` |
| After you attack and defeat / After you defeat | `AfterUnitDefeatedUnit(type, "You", Minion\|Enemy, op)` | an001a, an004, vp001a | « attacks AND defeats » → `is_from_attack=True` ; Minion ≠ Enemy, lire le mot imprimé ; **limite → lire l'encadré ci-dessous** |

> ⚠ **`AfterUnitDefeatedUnit` + « Limit once per round/phase », défaut moteur
> corrigé le 03/09/2026.** Cette fabrique ne rend PAS la Réponse demandée :
> elle rend une enveloppe `DelayAbility` branchée sur
> `WhenFaceWouldDealDamage` (`factory/defeated.py:330`) qui **fabrique une
> capacité interne neuve à chaque défaite**. La limite était posée sur
> l'enveloppe, dont tous les drapeaux de type valent `False` — donc
> `Effect.SetHasSpellInPhase` (`effect.py:161`) ne l'inscrivait jamais au
> registre, alors qu'il inscrivait l'interne, différente à chaque fois.
> `LimitOncePerRound()` était **silencieusement inerte** sur toute la famille.
>
> Corrigé dans `src/game/ability/condition/once_per.py` (`GetForDelayAbility`),
> où les deux lignes nécessaires existaient **en commentaire** avec un mauvais
> chemin d'attribut (`ability.type` au lieu de `ability.flags`).
>
> Signalé en jeu sur `angela`. Trois cartes portaient le défaut : `an001a`,
> `an009`, `vp001a` — et `vp001a` était justement la carte de référence citée
> par `an001a`, donc le montage cassé s'est recopié tout seul. Chacune a
> désormais son **témoin d'épuisement** dans `test_capacites.py`, exigé par
> l'étape 7 bis de `PROCESSUS-CARTE.md`.

> ⚠ **`world.stat.IsOncePerPhasePerPlayer` ne s'alimente pas tout seul.**
> Une carte qui écrit sa propre condition « Limit once per player per phase »
> sur ce registre (faute de pouvoir passer par le générateur du moteur, cf.
> `once_per.py`) doit appeler `world.stat.RecordEffectWithPlayer(effect,
> joueur)` **elle-même**, au moment où elle consomme son unique usage — sinon
> la limite est inerte : LIRE le registre sans jamais l'ALIMENTER revient à
> ne poser aucune limite. Le moteur le fait tout seul dans
> `Effect.SetHasSpellInPhase` (`effect.py:172-177`), mais UNIQUEMENT quand
> `self.bind_message` est une `TriggerNonePlayerMessage` — un message comme
> `AfterUnitAttackEnd` (hérité de `TriggerUnitMessage`) n'en est pas.
>
> Payé sur `gb020` You Are My God (pack Gorr) : sans l'appel, la Réponse
> Forcée se redéclenchait sur elle-même sans fin (10 dégâts constatés en une
> seule activation au lieu de 4). Corrigé en appelant
> `RecordEffectWithPlayer` **avant** de déclencher la seconde attaque (le
> moteur ne peut pas le faire à la place de la carte pour ce type de
> message). Commit `ea980b97`, témoin `tools/test_capacites.py` « gb020 You
> Are My God ».
| After <allié> enters play | `AfterCardEnterPlay(Response, "This", op)` | 01083 Mockingbird, ho002 | — |
| Hero Action (attack/thwart) sur événement | `WhenInYourPlayTurn(HeroAction, op).SetPlay().SetLabel('attack')` | 05015 Tackle, ho003 | le label alimente Sonné/Désorienté |
| Hero Interrupt: When you play an [[ATTACK]] event | `WhenPlayerPlayCard(HeroInterrupt, "You", CardFinder2("ATTACK", Event), op)` | ho006 (37006, 05011 pour le message) | ≠ « when you SPEND » (32047/54002 : paiement) |
| Response: After attached character gets a status card | `AfterStatusCardPlaceOn(type, "AttachedEnemy", ["Stunned","Confused","Tough"], op)` | 50144, ho012 | — |
| Obligation « Give to the X player » | `WhenThisObligationGiveToYou(op)` + `desc.GiveTo` | an010, ho013 | « may flip » vs « must flip » : deux helpers différents |
| When Revealed (complot annexe) | `WhenThisRevealed(None, op)` | an011, ho014 | — |
| [star] Boost: ... | `WhenCardBecomeBoost("This", op, conditions=[...])` | an013, 16140, ho015, ho017 | l'attaque en cours est `message.would_atk_message`, à lire avec `getattr(..., None)` |
| Setup: ... | `WhenCardSetup("This", op)` | an001b, ok001b | — |
| When you take 0 damage when defending | `AfterUnitDefendAgainstAttack(type, "You", op, take_no_damage=True)` | bt001a | le drapeau EXISTE déjà (do_attack.py:288), aucune carte officielle ne l'employait ; le message porte aussi `taken_damage` |
| After defending an attack (sans condition de dégâts) | même fabrique, SANS `take_no_damage` | bt012 | — |
| After you change to this form | `AfterUnitChangeForm(type, "You", op, to_this_form=True)` | 01019a, 12001a, bt001b | — |
| Whenever you draw a carte de type X | `AfterPlayerDrewCards(type, "You", X, op)` | bt023 | le filtre `which_card` porte sur les cartes PIOCHÉES : inutile de relire la main |
| Après avoir résolu son propre mulligan | `AfterPlayerResolveMulligans(type, op)` | bt001b | **AJOUTÉ le 1/9/2026** : le moteur n'avait aucune prise sur le mulligan (`WhenPlayerResolveMulligans` existait mais n'était jamais `.Send()`) |
| Réponse à une capacité spéciale nommée | `WhenResolveSpecialAbility(CardFinder(...), op)` | ab007 | — |
| After you use a basic power | `AfterUnitUseBasicPower(type, "This"\|"You", op, powers=["ATK","THW","DEF"])` | 14001a, 04032, tt001a, tg001a | le `[star]` d'une face héros est une convention d'IMPRESSION, pas un `NonKeywordStar` |
| When you use a basic power (+N à ce pouvoir) | `WhenUnitUseBasicPower(type, CardFinder(name=...), op)` + `message.GainValue(+1, effect)` | 20010, al012, tg009 | `GainValue` route seul vers ATK/THW/DEF/REC/SCH (`sender_unit.py:21`) |
| After you make a basic recovery | `AfterUnitMakeRecovery(type, "You", op, is_basic_recovery=True)` | 45015, tg007 | `AlterEgoResponse` si le texte le dit, sinon un allié qui récupère déclenche aussi |
| After you engage a minion | `AfterPlayerEngageMinion(type, "You", op)` | 56041, tg010 | un sbire posé par `Puzzle.PutIntoPlay` **s'engage toujours** (`minion.py:61`) : c'est le déclencheur le plus court à monter en cas |

- ⚠⚠ **UN FILTRE VA DANS `conditions`, JAMAIS DANS LE CORPS DE
  L'OPÉRATION.** Une capacité OPTIONNELLE (Response, Interrupt) branchée sur un
  message fréquent — `AfterCardDiscard`, `AfterCardsMoved`,
  `WhenBoostIconsWouldBeCount` — est **proposée au joueur** dès que le message
  part : le moteur pose la question *avant* d'exécuter l'opération, donc un
  `return` en tête de corps ne l'évite pas. Mesuré le 05/09/2026 sur `bc010`
  Ill Gotten Gains : **250 questions « Response » sur 8 parties d'autoplay**,
  dont 243 pour cette seule carte. Les trois tests déplacés dans `conditions`
  donnent **exactement le même résultat de jeu** et ramènent le compte à 10.
  ⚠ **Aucune gate statique et aucun cas de test ne voit ce défaut** : seule
  une partie réellement jouée le montre. C'est la raison d'être de l'étape
  autoplay.

### 6.8 Mots-pièges du texte imprimé, à chercher sur **chaque** carte

Avant d'écrire une ligne, relis le texte de la carte et cherche ces mots (étape 5 de `PROCESSUS-CARTE.md`) : ils
changent le sens. Le détail est au chapitre 12 (« Mots-pièges »). Les plus coûteux sur des cartes de héros :

* **« a »** (un) contre **« that »** (ce) : « remove 1 status from THAT enemy » (coût) contre « deal 2 damage to AN
  enemy » (effet) — deux cibles différentes ;
* **« play »** contre **« put into play »** ; **« after »** contre **« when »** ; **Response** contre **Interrupt** ;
* **« once per round »** (limite par round) contre **« once per phase »** ; **« Limit »** s'écrit `LimitOncePerRound()`
  sur la capacité (voir `lj001a`) ;
* **« each »** / **« all »** / **« any number »** ; **« up to »** ; **« may »** (facultatif) ;
* les **mots répétés** (« deal 1 damage ... deal 1 damage ») : une attaque PAR coup ;
* **« this card »** / **« here »** (= la carte qui porte le texte, souvent l'identité) ;
* **« your identity »** contre **« your hero »** (sous la forme alter ego, un « hero » n'existe pas).

### 6.9 Le gabarit de contrôle d'une carte (à remplir pour chaque carte à capacité)

Le fichier `GABARITS.md` de ta livraison contient **un gabarit par carte à capacité** : c'est la trace que tu as
fait les contrôles de `PROCESSUS-CARTE.md` à ta portée (étapes 1, 2, 3, 5, 6). Les étapes qui demandent **de
jouer** (7 : cas de test, 8 : autoplay) sont celles de Claude : tu y mets `à exécuter par Claude`, jamais « OK ».

<!-- extrait de docs/reference/PROCESSUS-CARTE.md -->
#### Gabarit à copier, une fois par carte

```
### <card_id> : <nom de la carte>

- [ ] Étape 2 : carte(s) de référence : ...
- [ ] Étape 5 : texte-contre-code : mots-pièges vérifiés (lister) : ...
      Résultat : ...
- [ ] Étape 6 : nombres texte ↔ code : ...
      Résultat : ...
- [ ] Étape 7 : cas test_capacites par capacité, preuve par substitution :
      capacité 1 : cas <nom>, rouge sans module / vert avec : capacité 2 : ...
      Résultat : ...
- [ ] Étape 7 bis : limite imprimée ? OUI / NON. Si OUI, témoin d'épuisement :
      cas <nom>, deux déclenchements dans le même round/phase, chiffre mesuré
      au second : ...
      Résultat : ...
- [ ] Étape 8 : autoplay ciblé : N parties, témoin <héros>, grep tracebacks : 0,
      lecture du journal : ...
      Résultat : ...
- [ ] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse,
      compteur, statut, mise de côté, changement de zone) ? OUI / NON.
      Si OUI, cas plateau : <fichier>, vu ROUGE sans le correctif : ...
      Résultat : ...

Carte terminée : OUI / NON : si NON, ce qui manque et pourquoi.
```

### 6.10 Auto-relecture d'un script

* [ ] `from . import *` en tête ; `GetAbilities()` défini ;
* [ ] le commentaire d'en-tête recopie le texte imprimé, cite 1 à 3 cartes de référence **qui existent** (le
  fichier existe dans le zip ou dans l'annexe A) et liste les mots-pièges rencontrés ;
* [ ] **chaque fonction appelée figure dans l'annexe I** (index de l'API) ou dans un modèle du zip ;
* [ ] `CardFinder(name="…")` **sans** l'étoile des cartes uniques ;
* [ ] aucune entrée-sortie (`open`, `os`, `subprocess`, `socket`, `exec`, `eval`), aucun `print` ;
* [ ] ce qui manque est un `# A_FAIRE_CLAUDE:` listé dans `A_FAIRE_CLAUDE.md` ;
* [ ] la face alter ego et la face héros ont chacune leur fichier si leur texte imprime une capacité.



---

## 7. Textes français, images, biographie, réplique de recrutement, crédits

### 7.1 Le texte français de chaque carte fan-made — **obligatoire à chaque pack**

Un pack livré sans ce texte laisse **toutes ses cartes sans tooltip français, et rien ne le signale**. Le plateau
cherche le français d'une carte dans cet ordre : (1) un scan français ; (2) le texte officiel (généré, ne jamais
l'éditer) ; (3) **`ui-app/src/board/textes-fr-fanmade.ts`**, écrit à la main ; (4) marvelcdb en ligne (sans effet
sur du fan-made). Pour une carte fan-made, la ligne (3) est le seul français que le joueur verra dessus.

**Ta livraison** : `integration/textes-fr/<pack>.fragment.txt`, **une entrée par `card_id`, y compris pour les
exemplaires en double** (recopie le même texte), au format exact du fichier :

```
  // <pack> — <Nom de la carte> (<Type>)
  '<card_id>': "texte français avec <b>balises</b>, [star], [[TRAIT]]…",
```

Les entrées réelles de Lockjaw (la face héros et la face alter ego) :

```typescript
  // lockjaw — Lockjaw (Hero)
  'lj001a': "<i>Rapporte !</i> — <b>Action</b> : inclinez Lockjaw et dépensez une ressource [mental] → choisissez une carte qui n'est pas une ressource dans la pile de défausse de n'importe quel joueur et ajoutez-la à la main de son propriétaire. <i>(Limite d'une fois par round.)</i>",
  // lockjaw — Lockjaw (AlterEgo)
  'lj001b': "<b>Mise en place</b> : cherchez Tuning Fork dans votre deck, votre main et votre pile de défausse, et mettez-la en jeu.\n<i>Réconfort</i> — <b>Réponse</b> : après être passé à cette forme, redressez un personnage allié.",
```

Les entrées d'Iron Fist (héros officiel récent : il a aussi ses textes dans ce fichier) :

```typescript
  // des que fr.marvelcdb.com l'aura, puis retirer ces entrees.
  '64001a': "<i>Maître des arts martiaux</i> — <b>Réponse</b> : après que vous avez joué une carte, placez 1 jeton Chi ici.\n<b>Réponse forcée</b> : après la fin de la phase des Joueurs, retirez d'ici tous les jetons Chi sauf 4 et soignez 1 dégât pour chaque jeton Chi ainsi retiré.",
  '64001b': "Vos cartes [[Technique]] perdent le mot-clé Temporaire.\n<i>Méditation</i> — <b>Action</b> : cherchez une carte [[Technique]] dans votre deck et votre défausse. Mettez cette carte en jeu. (Limite d'une fois par phase.)",
```

<!-- extrait de docs/kit-campagne-ia/KIT-CAMPAGNE-COMPLET.md -->
**Vocabulaire officiel (Guide de référence v1.8 FR) — la gate `vocabulaire-statuts.test.ts` échoue sinon :**

| Anglais | Français | **Interdit** |
|---|---|---|
| Stunned / Confused | Sonné / Désorienté | « étourdi » |
| Tough (carte d'état) / Toughness | carte d'état **Tenace** / **Ténacité** | « Robustesse » |
| Stalwart | **Robuste** | « Inébranlable » |
| Steady | **Solide** | « Stable » |
| Surge / Overkill | Renfort / Déferlement | |
| Piercing / Ranged | Perçant / Distance | |
| Villainous | Vilenie | |
| Incite X / Hinder X | Incitation X / Entrave X | |
| When Revealed | **Une fois révélée** (manigance, traîtrise) | |
| When Defeated (personnage) | **Une fois vaincu** | |
| When Defeated (manigance) | **Une fois déjouée** | |
| Forced Interrupt / Forced Response | Interruption forcée / Réponse forcée | |
| Hero Action / Hero Response / Alter-Ego Action | Action de héros / Réponse de héros / Action d'alter ego | |
| ATK / THW / DEF / REC / SCH | ATQ / CTR / DEF / REC / MNG | |
| counter / token | **jeton** (compteur de carte) ; « pion Accélération » ; « compteur polyvalent » (all-purpose) | |
| stage | stade (« achevé ») | |
| boost / star icon | champ de boost / icône d'étoile | |
| Aggression / Justice / Leadership / Protection | Agressivité / Justice / Leadership / Protection | |
| deck / encounter deck / victory display | deck / deck Rencontre / pile de victoire | |
| exhaust / ready | incliner / redresser | |

* **Noms propres et traits `[[…]]` laissés en ANGLAIS** : le joueur a la carte anglaise sous les yeux.
* **Jetons recopiés tels quels** : `[mental]`, `[physical]`, `[energy]`, `[wild]`, `[star]`, `[per_hero]`,
  `[crisis]`, `[acceleration]`, `[hazard]`, `[amplify]`, `[boost]`.
* Cherche **toujours** comment une phrase équivalente est rendue sur une carte **officielle**
  (`ui-app/src/board/textes-fr-complets.ts`) avant d'écrire la tienne ; les textes d'ambiance (italiques de
  récit) se traduisent comme le reste.
* « est censé(e) » (jamais « devrait ») ; « n'importe quelle quantité de dégâts » ; « perd le texte imprimé dans
  sa boîte de texte » ; « choisissez : soit vous inclinez…, soit vous… ».

Le vérificateur refuse les tournures interdites de ce tableau (« Robustesse », « Inébranlable », « statut Robuste »,
« Résistance. », « étourdi »), signale tout `card_id` sans texte, et tout texte pour un `card_id` absent.

### 7.2 Les images

Tu **ne produis pas** d'image. L'utilisateur te donne les images des cartes du héros ; tu t'en sers pour **lire**
les cartes (c'est la source de vérité de tout ce qui est imprimé) et tu livres `images.md` : un tableau
`card_id → fichier source`.

* Dans le jeu : **`assets/pics/<card_id>.<jpg|png|webp>`** — l'extension est obligatoire, le nom est le `card_id`
  (`lj001a.png`). Une face d'identité a **une image par face** ; une carte `full_link` n'a pas d'image propre.
* Tailles mesurées : cartes de héros maison **615 × 882** (png, jpg ou webp) ; cartes officielles récentes
  **300 × ~430**, parfois **600 × 860** (les cartes custom existent aussi en 600 × 840). Les **complots annexes de rencontre** sont **en paysage** (882 × 615) :
  l'image est stockée **couchée** telle quelle, le serveur la redresse à la lecture (`TryRotateImage`). N'ajuste rien : Claude
  uniformise les scans (`outils/uniformiser-scans.py`) et calibre les bulles de statistiques d'après l'image.
* **Lecture des planches** : si l'utilisateur te donne des planches de plusieurs cartes, ne transcris pas plus de
  **quatre cartes par lecture** : au-delà, le texte d'encart n'est plus fiable. Une carte lue à moitié se pose en
  question (§1.3), pas en supposition.
* `images.md` : une ligne par `card_id` (faces comprises), le fichier source et la taille si tu la connais :

```
| card_id | fichier | taille |
|---|---|---|
| lj001a | lockjaw-hero.png | 615x882 |
| lj001b | lockjaw-alter-ego.png | 615x882 |
```

### 7.3 La biographie (survol du héros dans le lanceur)

Le lanceur affiche, au survol de la tuile du héros, une fiche qui décrit le **personnage** (jamais sa mécanique
de jeu). Elle est indexée par le **`card_id` de la face héros** et jamais par le nom (`01001a` Peter Parker et
`27030a` Miles Morales s'appellent tous deux « Spider-Man »).

<!-- extrait de docs/reference/PROCESSUS-HEROS.md -->
#### Étape 7 : Biographie *(case à cocher avec preuve, pas une ligne qu'on oublie)*

Le wizard affiche, au survol du héros, une fiche qui décrit le personnage
(lecture de `HEROS_INFO[h.heroCardId]` dans `public/js/prepare/app.js`) : c'est de la culture
Marvel, jamais sa mécanique de jeu.

Ajouter une entrée dans `public/js/prepare/heros-info.js`, **indexée par le
`card_id` de la face héros** et jamais par le nom (`01001a` Peter Parker et
`27030a` Miles Morales s'appellent tous les deux « Spider-Man ») :

```js
"ht001a": {
    bio:   "3 ou 4 phrases : origine, pouvoirs, ce qui définit le personnage.",
    bioEn: "Same, in English.",
    civil: "Johnny Storm",
    base: "New York (Baxter Building)",
    equipes: "Quatre Fantastiques, Vengeurs",
    equipesEn: "Fantastic Four, Avengers",
    ennemis: "Fatalis, l'Homme-Taupe",
    ennemisEn: "Doctor Doom, Mole Man",
    apparition: "Fantastic Four #1 (1961)",
},
```

Règles : tout champ optionnel sauf `bio`/`bioEn` (mieux vaut omettre que
d'inventer ; un champ absent disparaît simplement de la fiche) ; les `*En`
seulement si la traduction diffère (« New York » ou « Thanos » se passent
de doublon, en anglais un `*En` absent affiche la version française) ;
**`civilEn` et `baseEn` existent aussi** (`app.js`, autour de la ligne 3204), même si le
gabarit ci-dessus ne les montre pas — utile pour « Institut Xavier » /
« Xavier Institute » (constaté au portage `bt001a`, 31/08/2026) ;
viser 3-4 phrases (panneau étroit, 314 px) ; libellés affichés via `t()`
dans `public/js/prepare/dico-en.js` (voir §11 de `GUIDE-CREATION-CONTENU.md`).
Ce fichier vit hors du dépôt du moteur : on l'édite directement dans la copie
vivante, il n'y a aucune recopie à faire (voir §1.3 de
`GUIDE-CREATION-CONTENU.md`).
Un héros sans entrée retombe silencieusement sur l'ancien affichage :
rien ne casse, mais la fiche manque, donc **preuve obligatoire** = confirmer
au survol du héros dans le wizard que le panneau affiche bien le texte
attendu, pas juste le grand visuel seul.

Ne pas ajouter de biographie pour une identité alternative purement
cosmétique (voir Étape 10 ci-dessous) : le panneau s'indexe sur la face du
deck de base, une entrée pour la variante resterait orpheline.

L'entrée réelle de Lockjaw (modèle de forme ; tu livres **seulement ta part** dans
`public/js/prepare/heros-info.fragment.js`) :

*Entrée `lj001a` de `Fusion/marvel-lcg-src/public/js/prepare/heros-info.js`.*

```javascript
    "lj001a": {
        bio: "Lockjaw est un chien géant de la Cité des Inhumains, gros comme un poney, avec un diapason planté sur le crâne et le pouvoir de se téléporter n'importe où avec quiconque le touche. Compagnon inséparable de la famille royale inhumaine et de la jeune Kamala Khan, il sert de taxi, de garde du corps et de peluche à toute une équipe. Personne ne sait vraiment s'il est un Inhumain transformé ou simplement un très bon chien : lui-même s'en moque, du moment qu'on lui lance quelque chose à rapporter.",
        bioEn: "Lockjaw is a giant dog from the Inhuman city, the size of a pony, with a tuning fork on his skull and the power to teleport anywhere with whoever touches him. The inseparable companion of the Inhuman royal family and of young Kamala Khan, he serves as taxi, bodyguard and cuddly toy for a whole team. Nobody is quite sure whether he is a transformed Inhuman or simply a very good boy: he does not care either way, as long as somebody throws something for him to fetch.",
        civil: "Lockjaw",
        base: "Attilan / New Attilan, New York",
        equipes: "Famille royale inhumaine, Pet Avengers",
        equipesEn: "Inhuman Royal Family, Pet Avengers",
        ennemis: "Annihilus, Maximus le Fou",
        ennemisEn: "Annihilus, Maximus the Mad",
        apparition: "Fantastic Four #45 (1965)",
    },
```

Les clés autorisées : `bio` et `bioEn` (**obligatoires**), `civil`, `civilEn`, `base`, `baseEn`, `equipes`,
`equipesEn`, `ennemis`, `ennemisEn`, `apparition`. Le vérificateur refuse toute autre clé en avertissement, et
une biographie qui parle de mécanique de jeu (« Action », « Response »…). **Ne remplis que ce que tu sais ;
n'invente pas une équipe ou une némésis.** Sans entrée, le héros retombe silencieusement sur l'ancien affichage :
rien ne casse, la fiche manque.

### 7.4 La réplique de recrutement (facultative, à proposer)

Au recrutement, une phrase s'affiche sur la carte. Plusieurs par héros, tirées au sort sans répéter la dernière.
Elle est indexée par l'**identifiant de deck** (le nom du fichier `deck/starter/<id>.json`), **jamais par le nom**
(« Spider-Man » désigne quatre decks). Un héros sans réplique retombe sur l'onomatopée propre à son id dans `ONOMATOPEES` (`app.js`), puis sur
« BAM ! ». Les répliques sont des **répliques** (comics, films), gardées en anglais avec leur casse et leur
ponctuation : **ne les traduis pas** ; les onomatopées de pouvoirs restent dans le style « MOT ! ». **Ne les
invente pas** : si tu n'en connais pas de véritable, demande à l'utilisateur (c'est lui qui établit la liste).
Tu livres **une seule ligne** dans `public/js/prepare/repliques-heros.fragment.js` :

*Ligne de `Fusion/marvel-lcg-src/public/js/prepare/repliques-heros.js`.*

```javascript
    lockjaw: ["Woof."],
```

*Ligne de `Fusion/marvel-lcg-src/public/js/prepare/repliques-heros.js`.*

```javascript
    ant_man: ["You can call me Ant.", "Does anyone have any orange slices?", "I'm gonna call him Antony.", "Why don't you pick on someone your own size?", "Do you guys just put the word quantum in front of everything?"],
```

### 7.5 Les crédits

* **Héros maison** : la clé `custom` (nom de l'auteur) sur **toutes** les cartes du héros, **identités comprises**.
  C'est ce qui fait afficher « Lockjaw (Nugget) » dans la grille (`public/js/prepare/auteur.js`) et le
  remerciement du filtre fan-made. `metadata.author` du deck porte le même nom.
* `CREDITS.md` de ta livraison : l'auteur et ses liens (`metadata.url`), le dossier source, les remerciements que
  l'auteur demande, et le nom de toute personne qui a fourni des scans. Rien d'autre.
* **Héros officiel** : pas de `custom`, pas de crédits d'auteur.

### 7.6 Ce que tu n'écris pas dans cette chaîne

Les positions de bulles de statistiques, la palette du héros, l'annuaire d'identités, les arts alternatifs
cosmétiques, la page « nouveautés » : tout cela est généré ou rédigé par Claude à partir des images et du
déroulé. Demande-le dans `BESOINS-MOTEUR.md` si ton héros a une particularité (une identité alternative à
l'art différent, par exemple).



---

## 8. Prouver que ça marche : les gates, les cas de test, le deck montable

⚠ Une gate qui répond « OK » ne prouve rien tant qu'on ne l'a pas vue **échouer** (`PROCESSUS-CARTE.md`, §9). Les
contrôles de ta livraison (`verifier-livraison-heros.py`) ont été calibrés ainsi : 45 casses volontaires dans des
livraisons réelles, 45 détectées (`outils/test_verifier_livraison_heros.py`). Mais ils lisent des fichiers ; ils ne
**jouent** pas.

### 8.1 Les six niveaux de preuve d'un héros

| # | Niveau | Qui | Ce que ça prouve |
|---|---|---|---|
| 1 | `verifier-livraison-heros.py` | **toi**, avant de livrer | la **forme** : faces, deck, obligation, némésis, scripts présents et bien rangés, textes, biographie |
| 2 | les gates statiques du dépôt (`test_cards.py`, `verifier_prefixes.py`, `verifier_api_cartes.py`, `verifier_appels_modules.py`) | Claude | chaque carte **se construit** ; aucun appel à une fonction inexistante ; préfixe déclaré |
| 3 | **cas de test de capacité** (`tools/cas/<héros>.py`, `test_capacites.py`) | toi (tu les écris), Claude (il les joue) | la capacité **fait ce que la carte dit** dans une position réelle |
| 4 | **preuve par substitution** (`tools/substituer_pack.py`) | Claude | le cas est **rouge sans le module** de la carte et vert avec : il mesure bien la carte |
| 5 | **`verifier_tous_les_decks.py`** : le deck du héros se **monte** | Claude | la gate qui attrape les asserts de construction du deck complet (§8.5) |
| 6 | autoplay ciblé + une **partie complète** avec le héros | Claude, puis l'utilisateur | aucun traceback sur 8 parties ; le héros se joue de bout en bout |

Tu ne peux pas exécuter les niveaux 2 à 6. Tu écris ce qu'il faut pour que Claude les exécute, et tu **le dis**
dans `AUTO-VERIFICATION.md` : « cas écrits, non exécutés ». **Jamais « OK » pour ce que tu n'as pas joué.**

### 8.2 Écrire les cas de test : `tools/cas/<héros>.py`

Le fichier est **découvert automatiquement** (`glob` de `tools/cas/*.py`). Il expose `CAS = [...]` et, si besoin,
`VERIFICATIONS = r'''...'''` (du code Python de vérification). Les noms de cas sont préfixés (`[iron_fist]`) pour
pouvoir les filtrer. **Un cas = un processus** : monte une position, déclenche, mesure l'état du monde.

* Le **`card_id` de la carte apparaît dans le NOM du cas** (c'est le « sujet » que `substituer_pack.py` filtre).
* **Un cas par capacité distincte** (chaque bloc Action / Response / Interrupt / Forced… séparé sur le texte).
* **Un cas va jusqu'au bout de ce que la carte annonce** : si elle fait deux choses, il mesure les deux. Ne
  retire jamais une assertion parce qu'elle échoue.
* **Toute limite imprimée** (« once per round ») exige un **témoin d'épuisement** : deux déclenchements dans le
  même round, un chiffre mesuré au second.
* Un **contre-cas dans l'autre forme** (la Réponse de la face héros ne se déclenche pas en alter ego) est la
  moitié du travail pour une identité.
* Le héros de test d'un héros dont le deck est vide est complété par le harnais (`remplir_les_decks_vides`) ; une
  carte précise en main se donne par `main_exclusive`.

Le **fichier de cas réel d'un héros officiel** (Iron Fist, 57 cas) — début du fichier, conventions de montage et
quatre cas de l'identité :

*Extrait de `Fusion/marvel-lcg-src/tools/cas/iron_fist.py`, lignes 1 a 63.*

```python
# Cas test_capacites du heros officiel IRON FIST (Hero Pack MC64EN, set « Iron Fist », 64001a-64012) :
# noms prefixes « [iron_fist] ». Un cas par capacite, sujet = le card_id dans le nom (substituer_pack.py
# filtre dessus). Gabarits PROCESSUS-CARTE : docs/packs/iron_fist_cartes.md. Decisions de l'utilisateur :
# .planning/iron-fist-officiel/lecture-reponses.md.
#
# Rappels de montage :
#  - Iron Fist demarre en ALTER EGO (64001b Danny Rand) ; `Puzzle.ChangeToFace('64001b', '64001a')` le passe
#    en forme HEROS ;
#  - le deck de depart a un `player_deck` VIDE : le harnais le complete (remplir_les_decks_vides) ;
#    `main_exclusive` dit avec QUOI on paie (01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR) ;
#  - ⚠ en forme heros, la Reponse de 64001a (« After you play a card, place 1 chi counter here ») part a
#    CHAQUE carte jouee par le cas : les comptes de chi l'incluent (« +1 de la Reponse ») ;
#  - Rhino 01094 (14 PV) est le vilain, 01097b son complot principal, 01101 Hydra Mercenary le sbire ;
#  - `choisir_option: ["N"]` force la reponse N a `DeclareNumber` ; `"Cancel"` passe un choix facultatif.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('64001b', '64001a')"
CIVIL = "Puzzle.ChangeToFace('64001a', '64001b')"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
COMPLOT = "01097b"
FIN_DE_PHASE = "Puzzle.EndPlayerPhase()"
# ⚠ `main_exclusive` DEFAUSSE la main de depart (pleine de cartes signature, Techniques comprises) APRES
# `mise_en_place` : une defausse construite pour un cas se fait donc dans `declencher`, apres ce vidage.
VIDER_DEFAUSSE = "Puzzle.EmptyPlayerDiscardPile()"


def chi(face, n):
    return f"Puzzle.Counter('{face}', 'chi', {n})"


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[iron_fist] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "iron_fist"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "if_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ 64001a Iron Fist : Response (Martial Arts Master)
    _c("64001a Iron Fist : Response, jouer une carte pose 1 chi sur l'identite (Feel the Flow jouee -> 1)",
       "« Martial Arts Master — Response: After you play a card, place 1 chi counter here »",
       [HEROS], [], {"en_jeu": ["64010"], "compteurs_identite": [["chi", 1]]},
       main_exclusive=["64010", "01090"], jouer=["64010"]),
    _c("64001a Iron Fist : Response, deux cartes jouees -> 2 chi (une par carte, evenement compris)",
       "« After you play A card » : chaque carte jouee, tout type (amelioration puis evenement Fists of Fury)",
       [HEROS], [], {"compteurs_identite": [["chi", 2]], "degats": [["01094", 3]]},
       main_exclusive=["64010", "64004", "01090"], jouer=["64010", "64004"]),
    _c("64001a Iron Fist : Response ABSENTE en alter ego (Danny joue une carte : 0 chi)",
       "contre-cas dans l'AUTRE forme : la Reponse est imprimee sur la face heros seulement",
       [], [], {"en_jeu": ["64010"], "compteurs_identite": [["chi", 0]]},
       main_exclusive=["64010", "01090"], jouer=["64010"]),
    _c("64001a Iron Fist : une carte MISE en jeu (pas jouee) ne pose pas de chi",
       "« play a card » ≠ « put into play » : PutIntoPlay de Feel the Flow, 0 chi",
       [HEROS, *en_jeu("64010")], [], {"en_jeu": ["64010"], "compteurs_identite": [["chi", 0]]},
       main_exclusive=["01090"]),
```

Et la fonction de vérification propre au héros (les clés d'`attendu` qu'il ajoute) :

*Extrait de `Fusion/marvel-lcg-src/tools/cas/iron_fist.py` (de « VERIFICATIONS = r''' » a « def if_fin_de_round »).*

```python
VERIFICATIONS = r'''
CLES_IRON_FIST = {'main_ids', 'attrs', 'techniques_en_jeu', 'defausse_avec'}


def if_etat(monde, aides):
    """etat_attendu + cles propres : main_ids (ensemble exact de la main), attrs [[card_id, attribut, valeur]],
    techniques_en_jeu (nombre exact de cartes TECHNIQUE en jeu), defausse_avec (card_id presents dans la defausse)."""
    cas = aides["cas"]
    attendu = dict(cas.get("attendu") or {})
    propres = {k: attendu.pop(k) for k in list(attendu) if k in CLES_IRON_FIST}
    j = monde.players[0]
    soucis = []
    if "main_ids" in propres:
        vu = sorted(getattr(f.paper, "card_id", "?") for f in j.hand_cards.GetAll())
        if vu != sorted(propres["main_ids"]):
            soucis.append(f"main = {vu} (attendu {sorted(propres['main_ids'])})")
    if "defausse_avec" in propres:
        pile = [getattr(f.paper, "card_id", "?") for f in j.discard_pile.Get()]
        for cid in propres["defausse_avec"]:
            if cid not in pile:
                soucis.append(f"{cid} absent de la defausse (defausse = {pile})")
    for cid, attr, voulu in propres.get("attrs") or []:
        face = aides["par_id"](monde, cid)
        if face is None:
            soucis.append(f"{cid} introuvable en jeu (attrs)")
        elif getattr(face, attr) != voulu:
            soucis.append(f"{cid}.{attr} = {getattr(face, attr)} (attendu {voulu})")
    if "techniques_en_jeu" in propres:
        n = 0
        for objet in monde.object_manager.card_dict.values():
            face = objet.face
            if face is not None and face.IsInPlay() and face.HasTrait("TECHNIQUE"):
                n += 1
        if n != propres["techniques_en_jeu"]:
            soucis.append(f"{n} Technique(s) en jeu (attendu {propres['techniques_en_jeu']})")
    sauvegarde = cas["attendu"]
    cas["attendu"] = attendu
    try:
        ok, msg = etat_attendu(monde, aides)
    finally:
        cas["attendu"] = sauvegarde
    if not ok:
        soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, msg

```

### 8.2 bis Les clés d'un cas et les clés d'`attendu` (extrait du manuel de campagne, §11.2)

<!-- extrait de docs/kit-campagne-ia/KIT-CAMPAGNE-COMPLET.md -->
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
```text
Puzzle.FindOrCreateFace(card)
Puzzle.CreateCard(card_name)
Puzzle.FindCommandCards(*cards)
Puzzle.CreateEncounterDiscardPile(*cards)
Puzzle.EmptyEncounterDeck()
Puzzle.EmptyEncounterDiscardPile()
Puzzle.RemoveNemesisAside()
Puzzle.CreateEncounterDeck(*cards)
Puzzle.CreateHandCards(*cards)
Puzzle.CreatePlayerDiscardPile(*cards)
Puzzle.EmptyPlayerDeck()
Puzzle.EmptyPlayerDiscardPile()
Puzzle.EmptyPlayerAdditionalDeck()
Puzzle.CreatePlayerDeck(*cards)
Puzzle.EmptyHand()
Puzzle.EmptyAdditionalDeck()
Puzzle.PutOnAdditionalDeckTop(*cards)
Puzzle.CreatePlayerAdditionalDeck(*cards)
Puzzle.Gain(*cards, call_back=None)
Puzzle.Draw(num)
Puzzle.Ready(*cards)
Puzzle.Exhaust(*cards)
Puzzle.Discard(*cards)
Puzzle.Remove(*cards)
Puzzle.Flip(*cards)
Puzzle.Heal(card, val)
Puzzle.Damage(card, val, source=None)
Puzzle.PlaceCounters(card, name, val)
Puzzle.Confuse(card)
Puzzle.Stun(card)
Puzzle.Tough(card)
Puzzle.AddTough(card, n=1)
Puzzle.Expose(card)
Puzzle.Cloak(card)
Puzzle.Daze(card)
Puzzle.RevealDealtCards()
Puzzle.RemoveMinionsInPlay()
Puzzle.AddCloak(card, n=1)
Puzzle.AddStatus(card, name, n=1)
Puzzle.Intensify(card, n=1)
Puzzle.ChangeToFace(card, to)
Puzzle.ChangeForm(card, rule='')
Puzzle.PlaceThreat(card, val)
Puzzle.SetThreat(card, val)
Puzzle.Counter(card, name, size=3)
Puzzle.Token(card, name, size=3)
Puzzle.Reveal(card, call_back=None, by=None)
Puzzle.PutIntoPlay(card, under_control=False, exhaust=False, player=None)
Puzzle.PlaceUnder(card, host, face_up=False)
Puzzle.TurnEncounterTopFaceUp()
Puzzle.Boost(card)
Puzzle.Deal(card, joueur=None)
Puzzle.FindFaceInPlay(card)
Puzzle.Attack(card, defender=None, against=None)
Puzzle.EnemyAttacks(card, target, defender=None, overkill_to=None, joueur=None)
Puzzle.ProtectFromPlayerCards(card, attached_to=None, trait=None)
Puzzle.SetVillainRule(the_villain='Active', player_cards='TheVillain')
Puzzle.SetActiveVillain(card)
Puzzle.RemoveVillain(card)
Puzzle.BuildVillainDeck(*cards)
Puzzle.RevealNextVillain()
Puzzle.Defend(card, attacker)
Puzzle.Thwart(card)
Puzzle.EndPlayerTurn()
Puzzle.EndPlayerPhase()
Puzzle.EndVillainPhase()
Puzzle.RunVillainPhase()
Puzzle.BeginVillainPhase()
Puzzle.Scheme(card)
Puzzle.Action(card, type=None, index=0)
Puzzle.MoveTo(card, zone, position='Top', player=0, siege=None, face_cachee=False)
Puzzle.ShuffleDiscardIntoDeck(zone, player=0, siege=None)
Puzzle.DrawUpToHandSize(player=0, siege=None)
Puzzle.EndRound()
Puzzle.SwapWithDeckTop(card, player=0, siege=None)
Puzzle.Mulligan(*cards, player=0, siege=None)
Puzzle.Shuffle(zone, player=0, siege=None)
Puzzle.Attach(card, cible)
Puzzle.AttachReel(card, cible)
Puzzle.Engage(card, player=0, siege=None)
Puzzle.PutIntoDeck(*cards)
Puzzle.AdvanceMainScheme(fois=1, to=None)
Puzzle.AdvanceVillain()
Puzzle.Win()
Puzzle.Lose()
Puzzle.End(message='')
```

⚠ **`Puzzle.*` désigne une carte par son NOM (ou son `card_id` pour les cartes de rencontre/joueur), jamais par le
`card_id` d'une identité** : `Puzzle.ChangeForm('Amadeus Cho')`, pas `Puzzle.ChangeForm('68001b')` (un `card_id`
d'identité fabrique une carte orpheline et plante le rendu). **Désigne toujours une carte par son `card_id` quand
le nom n'est pas unique** (deux « Venom Blast » existent).

<!-- extrait de docs/reference/GUIDE-CREATION-CONTENU.md -->
Quatre clés du harnais servent à rendre un cas DÉTERMINISTE. Sans elles, la
relecture du pack `madame_web` serait passée à côté de deux vrais défauts :

| Clé | À quoi elle sert |
|---|---|
| `main_exclusive` | **Vide la main** puis y dépose les cartes listées. Avec `main` seul, la main de départ reste là et le pilote y pioche ses ressources : le bonus « payé uniquement en [physical] » d'Ashley Barton se testait avec un paiement `R Y`, donc jamais. |
| `cibles` | Désigne des cibles précises, par `card_id`. Indispensable dès que le minimum de cibles est 0 (« exhaust up to X allies ») : le pilote envoie toujours le MINIMUM, donc rien. |
| `surpayer` | `True` : dépense tout ce qui est disponible, dès le PREMIER paiement du cas. Sans cela, une carte à **coût X** annonce un coût nul, le pilote ne paie rien, X vaut 0 et la carte paraît inerte alors qu'elle est correcte. `"<card_id>"` (ou une liste, depuis le 11/09/2026) : ne surpaie QUE le jeu de cette carte, ce qui permet de payer une première carte normalement (avec `payer_avec`) puis d'en surpayer une seconde : indispensable à tout effet qui se lit sur la carte dépensée SUIVANTE (yd007 Jackpot!). |
| `payer_avec` | Impose quelles cartes financent le coût. Utile quand la ressource dépensée a elle-même un effet (The Power of Forgiveness) — mais elle ne peut que PRIORISER parmi les candidats proposés par le moteur : pour un contrôle total, préférer `main_exclusive`. |

<!-- extrait de docs/reference/GUIDE-CREATION-CONTENU.md -->
Le vérificateur générique `etat_attendu` couvre la majorité des cas sans écrire
une seule fonction. Clés disponibles : `attributs`, `traits`, `en_jeu`,
`hors_jeu`, `compteurs`, `jetons`, `compteurs_total`, `menace`,
`attributs_carte`, `degats`, `degats_min`, `degats_identite`,
`dans_deck_rencontre`, `forme`, `en_jeu_trait`, `exhausted`, `pret`,
`statuts`, `taille_main`, `en_main`, `defausse`, `defausse_joueur`.
Deux pièges : **`jetons` et `compteurs` sont deux stocks distincts** (la menace
posée sur une carte joueur, façon Beat Cop, est un JETON `threat` — la
contrôler avec `compteurs` renvoie toujours 0, donc un test qui passe pour de
mauvaises raisons) ; et **`defausse` est le seul moyen de prouver qu'un
événement a été JOUÉ**, puisqu'une carte restée en main n'est pas « en jeu »
non plus et satisfait donc `hors_jeu`.

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

Le code du vérificateur générique `etat_attendu` et la liste **complète** de ses clés sont dans le zip :
`commun/outils/test_capacites.extraits.py`. Une clé inconnue fait **échouer** le cas quand il utilise directement `"verifier": "etat_attendu"` (elle était
ignorée en silence jusqu'au 11/09/2026 ; un vérificateur maison qui appelle `etat_attendu` lit ses propres clés) : n'invente pas de clé, ajoute un `VERIFICATIONS` propre au héros comme
`if_etat` d'Iron Fist.

### 8.3 Tout ce que le montage d'un cas peut utiliser : l'API `Puzzle`

Les chaînes de `mise_en_place` et de `declencher` sont des appels à cette API (`src/game/puzzle/puzzle.py`,
générée à la construction du kit — **n'en utilise aucune autre**) :

```text
Puzzle.FindOrCreateFace(card)
Puzzle.CreateCard(card_name)
Puzzle.FindCommandCards(*cards)
Puzzle.CreateEncounterDiscardPile(*cards)
Puzzle.EmptyEncounterDeck()
Puzzle.EmptyEncounterDiscardPile()
Puzzle.RemoveNemesisAside()
Puzzle.CreateEncounterDeck(*cards)
Puzzle.CreateHandCards(*cards)
Puzzle.CreatePlayerDiscardPile(*cards)
Puzzle.EmptyPlayerDeck()
Puzzle.EmptyPlayerDiscardPile()
Puzzle.EmptyPlayerAdditionalDeck()
Puzzle.CreatePlayerDeck(*cards)
Puzzle.EmptyHand()
Puzzle.EmptyAdditionalDeck()
Puzzle.PutOnAdditionalDeckTop(*cards)
Puzzle.CreatePlayerAdditionalDeck(*cards)
Puzzle.Gain(*cards, call_back=None)
Puzzle.Draw(num)
Puzzle.Ready(*cards)
Puzzle.Exhaust(*cards)
Puzzle.Discard(*cards)
Puzzle.Remove(*cards)
Puzzle.Flip(*cards)
Puzzle.Heal(card, val)
Puzzle.Damage(card, val, source=None)
Puzzle.PlaceCounters(card, name, val)
Puzzle.Confuse(card)
Puzzle.Stun(card)
Puzzle.Tough(card)
Puzzle.AddTough(card, n=1)
Puzzle.Expose(card)
Puzzle.Cloak(card)
Puzzle.Daze(card)
Puzzle.RevealDealtCards()
Puzzle.RemoveMinionsInPlay()
Puzzle.AddCloak(card, n=1)
Puzzle.AddStatus(card, name, n=1)
Puzzle.Intensify(card, n=1)
Puzzle.ChangeToFace(card, to)
Puzzle.ChangeForm(card, rule='')
Puzzle.PlaceThreat(card, val)
Puzzle.SetThreat(card, val)
Puzzle.Counter(card, name, size=3)
Puzzle.Token(card, name, size=3)
Puzzle.Reveal(card, call_back=None, by=None)
Puzzle.PutIntoPlay(card, under_control=False, exhaust=False, player=None)
Puzzle.PlaceUnder(card, host, face_up=False)
Puzzle.TurnEncounterTopFaceUp()
Puzzle.Boost(card)
Puzzle.Deal(card, joueur=None)
Puzzle.FindFaceInPlay(card)
Puzzle.Attack(card, defender=None, against=None)
Puzzle.EnemyAttacks(card, target, defender=None, overkill_to=None, joueur=None)
Puzzle.ProtectFromPlayerCards(card, attached_to=None, trait=None)
Puzzle.SetVillainRule(the_villain='Active', player_cards='TheVillain')
Puzzle.SetActiveVillain(card)
Puzzle.RemoveVillain(card)
Puzzle.BuildVillainDeck(*cards)
Puzzle.RevealNextVillain()
Puzzle.Defend(card, attacker)
Puzzle.Thwart(card)
Puzzle.EndPlayerTurn()
Puzzle.EndPlayerPhase()
Puzzle.EndVillainPhase()
Puzzle.RunVillainPhase()
Puzzle.BeginVillainPhase()
Puzzle.Scheme(card)
Puzzle.Action(card, type=None, index=0)
Puzzle.MoveTo(card, zone, position='Top', player=0, siege=None, face_cachee=False)
Puzzle.ShuffleDiscardIntoDeck(zone, player=0, siege=None)
Puzzle.DrawUpToHandSize(player=0, siege=None)
Puzzle.EndRound()
Puzzle.SwapWithDeckTop(card, player=0, siege=None)
Puzzle.Mulligan(*cards, player=0, siege=None)
Puzzle.Shuffle(zone, player=0, siege=None)
Puzzle.Attach(card, cible)
Puzzle.AttachReel(card, cible)
Puzzle.Engage(card, player=0, siege=None)
Puzzle.PutIntoDeck(*cards)
Puzzle.AdvanceMainScheme(fois=1, to=None)
Puzzle.AdvanceVillain()
Puzzle.Win()
Puzzle.Lose()
Puzzle.End(message='')
```

### 8.4 La moitié d'aspect de TEST (`tools/decks-de-test.fragment.json`, facultatif)

Un héros maison à `player_deck` vide a, pour le harnais **seulement**, une moitié d'aspect de test : sans elle, la
main de départ n'est faite que de cartes signature et le pilote déclenche leurs interruptions au milieu de la
mise en place. Le harnais complète lui-même un deck vide (`remplir_les_decks_vides`) avec cette moitié ; depuis le 13/09/2026
un deck absent de ce fichier reste vide (le repli « 25 ressources » a été retiré). **Tu n'as pas à la composer** : si un de tes cas a besoin d'une carte
précise en main, il la donne par `main_exclusive`.

### 8.5 La gate qui rend un héros jouable : `verifier_tous_les_decks.py`

> ### ⚠ POURQUOI C'EST UNE GATE (leçon `ls005`, 3/9/2026)
>
> Le constructeur de cartes (`factory.py`) pose des **asserts de construction** qu'aucun autre outil ne déclenche :
> un événement à deux capacités `Play` (un « Choose one », ou une Action civile + une Action héros sur la même
> carte) doit être **déclaré dans une liste blanche**, sinon la partie plante **au setup**. `test_cards` ne monte
> pas de partie ; `test_capacites` et `substituer_pack` ne montent que les positions écrites à la main. **Seul
> `verifier_tous_les_decks` l'attrape.** Mesuré : le deck `lady_sif` était **injouable depuis son portage de la
> veille**, ses gabarits cochés, ses 22 cas verts et ses 18 cartes prouvées par substitution.

Ce que ça veut dire pour toi : **toute carte qui a deux capacités `Play` sur le même événement** se signale dans
`BESOINS-MOTEUR.md` (« événement à deux capacités Play : liste blanche à compléter »), parce que c'est la seule
chose que tu ne peux pas régler seul.

### 8.6 Le chemin outillé de Claude, avec les durées vues

<!-- extrait de docs/reference/RECETTES-MOTEUR.md -->
#### 9. Le chemin outillé, de bout en bout

| Étape | Commande | Durée vue |
|---|---|---|
| Légalité des decks (signatures étrangères) | bloc python du §10 de PROCESSUS-HEROS | 2 s |
| Un deck + témoin | `DECK_NOM=<pack> ... verifier_tous_les_decks.py` | ~40 s |
| Tous les decks (152 au 20/10/2026 ; fichier partagé touché) | passe complète | ~20 min |
| Cas du pack | `test_capacites.py ... "<prefixe>"` | ~10 s/cas |
| Substitutions du pack | `substituer_pack.py` | ~30 s/carte |
| Statique | `test_cards.py`, `verifier_api_cartes.py`, `audit_cartes.py` | ~2 min chacun |
| Autoplay ciblé | `autoplay.py --deck <pack> --parties 8` + témoin | ~3 min |
| Batterie complète (fichier partagé touché) | `test_capacites.py` sans filtre | ~2 h, en fond |
| Boucle des campagnes (carnet ou mise en place touchés) | `test_campagnes.py` | ~5 min |

### 8.7 Ce que Claude exécute, dans l'ordre, sur ta livraison

1. `verifier-livraison-heros.py` (le même que le tien) et la **comparaison** avec le dépôt si le héros est déjà
   intégré (`outils/comparer-livraison-heros-au-depot.py`) : *identique / différent / manquant / en trop*.
2. Fusion des fragments (cartes, `sets_info`, textes français, biographie, réplique, préfixe) ; recalcul des
   checksums ; images posées ; bulles de statistiques et palette générées.
3. Les gates statiques (niveau 2), puis les cas (niveau 3) et la substitution (niveau 4).
4. `DECK_NOM=<héros> verifier_tous_les_decks.py` avec un héros témoin (niveau 5).
5. Autoplay ciblé, 8 parties minimum contre le même vilain qu'un héros témoin, avec grep exhaustif des
   tracebacks (niveau 6), puis le rendu du plateau (« étape 8 bis » : ce que la carte *dessine* — compteur sur
   l'identité, carte attachée, statut).
6. Une partie complète jouée avec le héros.

Aucune carte n'est « terminée » tant qu'il reste une capacité sans cas sujet et sans preuve par substitution, ni une
limite imprimée sans témoin d'épuisement. **Si une seule carte du pack manque son « Carte terminée : OUI », le
héros entier reste NON.**



---

## 9. Ce que tu livres, exactement, et dans quel ordre travailler

### 9.1 L'ordre de travail recommandé

Livre **par lots** (un message, ou un lot de fichiers, par étape) plutôt que tout d'un coup : la relecture de Claude
est plus fiable, et une erreur de méthode se corrige au premier lot.

| Phase | Tu fais | Tu produis |
|---|---|---|
| **0. Lecture** | Regarder **toutes** les images du héros (face héros, alter ego, chaque carte signature, l'obligation, le set némésis, les éventuelles cartes d'aspect) et lire le matériel de l'auteur (decklist, notes). Compter les cartes et les exemplaires. | notes de travail (pas de livrable) |
| **1. Cadrage** | Choisir l'**identifiant de deck** (`deck/starter/<id>.json`), la **clé du pack**, proposer **deux préfixes** libres (question à choix multiple, héros maison). Vérifier que l'identifiant de deck n'existe pas (`reference/decks-existants.json`). | `QUESTIONS.md` (premières questions), `MANIFESTE.md` (squelette) |
| **2. Cartes** | Transcrire **chaque carte** (quatre par lecture de planche au plus), numéroter sans trou, remplir `desc`, `traits`, `set_name`, `custom`. | `integration/data/cards.<pack>.fragment.json`, `images.md` |
| **3. Deck et extension** | Écrire `deck/starter/<id>.json` (+ variantes), l'entrée `sets_info` et, si utile, le set némésis nommé. | `integration/deck/starter/*`, `…/sets_info.<pack>.fragment.json`, `…/nemesis/*` |
| **4. Scripts** | Un script par face de carte à capacité, **carte par carte**, avec son gabarit. | `integration/src/cards/pack/<pack>/…`, `GABARITS.md` |
| **5. Textes et habillage** | Textes français, biographie, réplique (à proposer), préfixe, crédits. | `integration/textes-fr/…`, `…/heros-info.fragment.js`, `…/repliques-heros.fragment.js`, `…/prefixes.<pack>.fragment.json`, `CREDITS.md` |
| **6. Preuves** | Les cas de test de capacité (avec les contre-cas de l'autre forme et les témoins d'épuisement). | `integration/tools/cas/<id>.py` |
| **7. Auto-vérification** | Lancer `verifier-livraison-heros.py` ; relire chaque checklist ; compter les `A_FAIRE_CLAUDE`. | `AUTO-VERIFICATION.md`, `A_FAIRE_CLAUDE.md`, `BESOINS-MOTEUR.md`, `QUESTIONS.md` à jour |

### 9.2 L'arborescence de la livraison

Elle **reproduit celle du projet** (chemins relatifs à la racine du moteur), pour que Claude fusionne sans
deviner. Voici la livraison d'une héroïne imaginaire `ma_heroine` (pack `ma_heroine`, préfixe `mh`, deck `ma_heroine`) :

```
livraison/
├── MANIFESTE.md                    la liste de TOUS les fichiers livrés (§9.3)
├── QUESTIONS.md                    les questions ouvertes (§9.4)
├── BESOINS-MOTEUR.md               ce que le moteur / l'interface devra apprendre (§9.5)
├── A_FAIRE_CLAUDE.md               tous les marqueurs A_FAIRE_CLAUDE regroupés (§9.6)
├── GABARITS.md                     un gabarit de contrôle par carte à capacité (§6.9)
├── AUTO-VERIFICATION.md            ce que tu as vérifié, avec la sortie du vérificateur (§9.7)
├── CREDITS.md                      (§7.5)
├── images.md                       card_id → fichier source (§7.2)
└── integration/
    ├── data/
    │   ├── cards.ma_heroine.fragment.json             {"ma_heroine": [ ...cartes... ]}
    │   ├── sets_info.ma_heroine.fragment.json         {"N. Custom (Ma heroine)": {...}}
    │   └── nemesis/ma_heroine_nemesis.json            (facultatif)
    ├── deck/starter/
    │   ├── ma_heroine.json
    │   └── ma_heroine_variante.json                   (une variante, §5.3)
    ├── src/cards/pack/ma_heroine/
    │   ├── __init__.py                                helpers partagés du pack
    │   ├── ma_heroine/__init__.py   mh001a.py  mh001b.py  mh002.py ...      (set « Ma Heroine »)
    │   └── ma_heroine_nemesis/__init__.py  mh014.py ...                      (set « Ma Heroine Nemesis »)
    ├── textes-fr/ma_heroine.fragment.txt              lignes pour textes-fr-fanmade.ts
    ├── public/js/prepare/
    │   ├── heros-info.fragment.js                     la biographie (clé = face héros)
    │   └── repliques-heros.fragment.js                la ligne de répliques (clé = id de deck)
    └── tools/
        ├── prefixes.ma_heroine.fragment.json          entrée de prefixes_fanmade.json
        ├── cas/ma_heroine.py                          cas de test de capacité
        └── decks-de-test.fragment.json                (facultatif, §8.4)
```

**Règles de forme** :

* **Encodage UTF-8, fins de ligne `\n`**, JSON indenté de 4 espaces, `ensure_ascii=False`.
* **Un fichier par face de carte à capacité** ; **jamais** deux cartes dans un même script.
* Aucun fichier **hors** de cette arborescence ; aucun fichier temporaire ; **aucun** dossier `scenarios`,
  `encounter_sets` ou `campagnes` (c'est une livraison de héros).
* **Les fragments contiennent *seulement* ta part** : jamais une copie, même partielle, d'un fichier partagé.
* **Aucune modification d'un fichier existant du projet** : tout nouveau fichier ; tout ce qui doit changer dans
  un fichier existant (moteur, interface, liste blanche de traits ou compteurs) va dans `BESOINS-MOTEUR.md`.

### 9.3 `MANIFESTE.md`

Une ligne par fichier livré :

```
| Chemin (dans integration/)                         | Rôle                                  | Cartes / entrées | Statut |
|----------------------------------------------------|---------------------------------------|------------------|--------|
| data/cards.ma_heroine.fragment.json                | cartes du pack                        | 31 faces         | complet |
| src/cards/pack/ma_heroine/ma_heroine/mh001b.py     | Setup + Réponse de l'alter ego        | 1                | A_FAIRE_CLAUDE ×1 |
```

**Statut** : `complet` · `partiel (A_FAIRE_CLAUDE ×n)` · `brouillon`. À la fin du manifeste : les totaux (cartes,
faces, scripts, decks de départ, cas de test, `A_FAIRE_CLAUDE`).

### 9.4 `QUESTIONS.md` — une question par entrée, format fixe

```
### Q<n> — <card_id ou règle> : <le doute en une phrase>

Image / source : <fichier de la carte>
Texte imprimé : « … »

Lectures possibles :
  A. (recommandée) <lecture> — en jeu : <ce que ça change>
  B. <lecture> — en jeu : <ce que ça change>
  C. Autre (précise)

Lecture retenue en attendant : A  (repérée par `# QUESTION <n> :` dans <fichier>)
```

Une **seule** question à la fois est posée à l'utilisateur (règle 4, §1.2) ; ce fichier les **range** pour Claude.
Une question **tranchée** garde sa place, avec la réponse et sa date. Le dossier `modeles/E-questions-iron-fist/`
du zip contient les questions et les cinq réponses réelles du héros Iron Fist (la forme exacte attendue).

### 9.5 `BESOINS-MOTEUR.md` — format fixe

```
### B<n> — <titre court>

Image / source : <fichier de la carte>, « … »
Ce que le jeu fait déjà de plus proche : <fichier : fonction, ou « rien »>
Ce qui manque : <comportement attendu, décrit ; pas de code>
Dépend : <card_id(s), champ(s) de description>
En attendant : <A_FAIRE_CLAUDE posé dans <fichier>, ou lecture retenue>
```

Y vont **aussi** : les **traits nouveaux** (`trait nouveau : TELEPORT, porté par lj008–lj012`), les **compteurs
nouveaux** (`compteur nouveau : chi, posé sur l'identité 64001a`), les **événements à deux capacités `Play`**
(liste blanche, §8.5), les **chaînes d'interface nouvelles** avec leur traduction anglaise, les **particularités
d'habillage** (identité alternative à art différent, forme de plus, bulles de statistiques inhabituelles).

### 9.6 `A_FAIRE_CLAUDE.md`

Tous les marqueurs `# A_FAIRE_CLAUDE:` du code, regroupés : `fichier : ligne : texte imprimé visé : ce qui manque :
carte de référence la plus proche`. **Un marqueur dans le code qui n'est pas dans cette liste est une faute.**

### 9.7 `AUTO-VERIFICATION.md`

```
## Vérificateur de livraison
$ python3 verifier-livraison-heros.py livraison/
<la sortie complète, collée>

## Relectures faites (cochées seulement si faites)
- [x] §4.9 checklist des cartes du héros
- [x] §6.10 auto-relecture de chaque script
- [x] §5.2 règles de contenu du deck (aucune signature étrangère, obligation, némésis)

## Ce qui n'a PAS été vérifié (à exécuter par Claude)
- cas de test de capacité : écrits, non exécutés
- verifier_tous_les_decks : non exécuté
- aucune partie jouée
```

### 9.8 Ce que tu ne fais jamais (rappel)

Pas d'images ni de scans ; pas de checksum ; pas de commit ni de déploiement ; pas de modification du moteur ; pas de
deck de départ inventé pour un héros maison ; pas de « vert » non exécuté ; pas de chiffre de test non mesuré ;
**pas de décision de règle en silence**.

### 9.9 Quand Claude te rend son retour

Claude compare ta livraison au dépôt (`outils/comparer-livraison-heros-au-depot.py` quand le héros existe déjà,
sinon lecture carte par carte avec l'image), lance les gates du chapitre 8 et te rend : les corrections faites,
les questions qu'il pose à l'utilisateur, ce qui reste NON. Les lots suivants reprennent là où il s'est arrêté.



---

## 10. Quatre héros complets, fichier par fichier : les modèles du zip

Le dossier `modeles/` du zip contient, pour **quatre héros qui marchent en jeu**, la livraison telle qu'une IA
aurait dû la rendre (reconstituée depuis le dépôt par `outils/livraison-heros-depuis-le-depot.py`). Les fichiers de
suivi (`MANIFESTE.md`, `images.md`…) sont **générés** : ils montrent la forme attendue.

| Dossier | Héros | Pourquoi ce modèle | À regarder |
|---|---|---|---|
| `A-officiel-ant-man/` | **Ant-Man** (pack officiel `ant`, ids `12001a`…) | héros officiel **à trois formes** (`12001a`/`b`/`c`), obligation, set némésis, 25 cartes de `player_deck`, cartes d'aspect de la boîte (`set_name` vide) | `deck/starter/ant_man.json`, `12001c` |
| `B-maison-lockjaw/` | **Lockjaw** (Nugget, préfixe `lj`) | héros **maison complet** : decklist de l'auteur, obligation à choix, set némésis avec complot annexe en paysage, 13 cartes d'aspect, mot-clé maison (*Companion*) | `lj001a`/`b`, `lj013`, `lj015`, `heros-info.fragment.js` |
| `C-maison-harry-osborn/` | **Harry Osborn / Green Goblin** (préfixe `ho`) | héros maison (Dipsome) **sans decklist d'auteur** (`player_deck` vide), règle de deck-building propre (`hors_aspect`), face alter ego sans script | `deck/starter/harry_osborn.json`, `ho001a.py` |
| `D-officiel-recent-iron-fist/` | **Iron Fist** (MC64, novembre 2026) | héros officiel **partiellement publié** : ni obligation, ni némésis, `player_deck` vide, `deck_note` qui le dit ; **57 cas de test**, jeton Chi sur l'identité, gabarits `PROCESSUS-CARTE` complets | `tools/cas/iron_fist.py`, `GABARITS.md` |
| `E-questions-iron-fist/` | les questions et les cinq réponses de l'utilisateur sur Iron Fist | la forme réelle de `QUESTIONS.md` et des décisions | tout |

Les images d'exemple (`images-exemples/`) donnent les formats réels : une face héros, un alter ego, un allié, un
complot annexe de némésis en paysage.

### 10.1 Lecture guidée : le plan de cartes de Lockjaw

| card_id | type | nom | classe | coût | ressource | set_name |
|---|---|---|---|---|---|---|
| lj001a | Hero | * Lockjaw |  |  |  | Lockjaw |
| lj001b | AlterEgo | * Lockjaw |  |  |  | Lockjaw |
| lj002 | Ally | * Black Bolt | Hero | 3 | G | Lockjaw |
| lj003 | Upgrade | * Tuning Fork | Hero | 1 | Y | Lockjaw |
| lj004 | Upgrade | Jaw Lock | Hero | 3 | R | Lockjaw |
| lj005 | Support | * Kamala's Room | Hero | 2 | B | Lockjaw |
| lj006 | Support | * New Attilan | Hero | 1 | B | Lockjaw |
| lj007 | Support | * Doc Jaw's Lab | Hero | 1 | B | Lockjaw |
| lj008 | Event | Teleport To Safety | Hero | 1 | B | Lockjaw |
| lj009 | Event | Fast Travel | Hero | 1 | Y | Lockjaw |
| lj010 | Event | Zooming Around | Hero | 2 | Y | Lockjaw |
| lj011 | Event | Ruff Ambush | Hero | 2 | R | Lockjaw |
| lj012 | Event | Psionic Tracking | Hero | 0 | B | Lockjaw |
| lj013 | Obligation | Canine Urges |  |  |  | Lockjaw |
| lj014 | SideScheme | Dognapped! |  |  |  | Lockjaw Nemesis |
| lj015 | Minion | * Annihilus |  |  |  | Lockjaw Nemesis |
| lj016 | Minion | Dog Catcher |  |  |  | Lockjaw Nemesis |
| lj017 | Attachment | Provoked |  |  |  | Lockjaw Nemesis |
| lj018 | Ally | * Zabu | Aggression | 1 | R | Lockjaw |
| lj019 | Ally | * Throg | Justice | 1 | Y | Lockjaw |
| lj020 | Ally | * Redwing | Leadership | 1 | B | Lockjaw |
| lj021 | Ally | * Hairball | Protection | 1 | G | Lockjaw |
| lj022 | Ally | * Lockheed | Protection | 2 | R | Lockjaw |
| lj023 | Event | Protect The Pack | Protection | 0 | G | Lockjaw |
| lj024 | Event | Wet Slobbering Kiss | Protection | 2 | B | Lockjaw |
| lj025 | Ally | * Ms. Lion | Basic | 1 | G | Lockjaw |
| lj026 | Ally | * Ms. Marvel | Basic | 3 | B | Lockjaw |
| lj027 | Event | Animals Unleashed | Basic | 1 | G | Lockjaw |
| lj028 | Event | Companionship | Basic | 0 | B | Lockjaw |
| lj029 | Event | Inhuman's Best Friend | Basic | 1 | Y | Lockjaw |
| lj030 | Support | * Central Park | Basic | 1 | R | Lockjaw |

### 10.2 Lecture guidée : le plan de cartes d'Ant-Man

| card_id | type | nom | classe | coût | ressource | set_name |
|---|---|---|---|---|---|---|
| 12001a | Hero | * Ant-Man |  |  |  | Ant-Man |
| 12001b | AlterEgo | * Scott Lang |  |  |  | Ant-Man |
| 12001c | Hero | * Ant-Man |  |  |  | Ant-Man |
| 12002 | Ally | * Wasp | Hero | 3 | G | Ant-Man |
| 12003 | Event | Giant Stomp | Hero | 3 | Y | Ant-Man |
| 12004 | Event | Hive Mind | Hero | 2 | R | Ant-Man |
| 12005 | Event | Resize | Hero | 0 | R | Ant-Man |
| 12006 | Resource | Pym Particles | Hero |  | G | Ant-Man |
| 12007 | Support | Army of Ants | Hero | 1 | R | Ant-Man |
| 12008 | Upgrade | * Ant-Man's Helmet | Hero | 3 | B | Ant-Man |
| 12009 | Upgrade | Giant Strength | Hero | 1 | Y | Ant-Man |
| 12010 | Upgrade | Wrist Gauntlets | Hero | 1 | B | Ant-Man |
| 12011 | Ally | * Ant-Man | Leadership | 0 | B |  |
| 12012 | Ally | * Giant-Man | Leadership | 5 | R |  |
| 12013 | Ally | * Ronin | Leadership | 3 | Y |  |
| 12014 | Ally | * Stinger | Leadership | 1 | Y |  |
| 12015 | Event | Call for Aid | Leadership | 0 | R |  |
| 12016 | Event | Moxie | Leadership | 0 | B |  |
| 12017 | Upgrade | Power Gloves | Leadership | 1 | B |  |
| 12018 | Upgrade | Reinforced Suit | Leadership | 1 | Y |  |
| 12019 |  |  |  |  |  |  |
| 12020 | Event | Swarm Tactics | Basic | 1 | B |  |
| 12021 |  |  |  |  |  |  |
| 12022 |  |  |  |  |  |  |
| 12023 |  |  |  |  |  |  |
| 12024 | Support | Team-Building Exercise | Basic | 2 | R |  |
| 12025 | Obligation | Care for Cassie |  |  |  | Ant-Man |
| 12026 | SideScheme | Tech Theft |  |  |  | Ant-Man Nemesis |
| 12027 | Minion | * Yellowjacket |  |  |  | Ant-Man Nemesis |
| 12028 | Attachment | Size Increase |  |  |  | Ant-Man Nemesis |
| 12029 | Treachery | Yellowjacket's Plan |  |  |  | Ant-Man Nemesis |
| 12030 | Event | Moment of Triumph | Aggression | 0 | Y |  |
| 12031 | Event | Lay Down the Law | Justice | 1 | B |  |
| 12032 | Event | Muster Courage | Protection | 3 | R |  |
| 12033 | Event | Assess the Situation | Basic | 0 | B |  |

### 10.3 Lecture guidée : le plan de cartes d'Iron Fist

| card_id | type | nom | classe | coût | ressource | set_name |
|---|---|---|---|---|---|---|
| 64001a | Hero | * Iron Fist |  |  |  | Iron Fist |
| 64001b | AlterEgo | * Danny Rand |  |  |  | Iron Fist |
| 64002 | Event | Deep Breathing | Hero | 0 | B | Iron Fist |
| 64003 | Event | Dragon Punch | Hero | 2 | Y | Iron Fist |
| 64004 | Event | Fists of Fury | Hero | 1 | R | Iron Fist |
| 64005 | Event | The Way of Things | Hero | 1 | B | Iron Fist |
| 64006 | Support | * Lei Kung | Hero | 1 | Y | Iron Fist |
| 64007 | Upgrade | * Book of the Iron Fist | Hero | 2 | R | Iron Fist |
| 64008 | Upgrade | Channel the Iron Fist | Hero | 0 | Y | Iron Fist |
| 64009 | Upgrade | Embody the Dragon | Hero | 0 | R | Iron Fist |
| 64010 | Upgrade | Feel the Flow | Hero | 0 | B | Iron Fist |
| 64011 | Upgrade | Keep 'Em Coming | Hero | 0 | R | Iron Fist |
| 64012 | Upgrade | Redirect Chi | Hero | 0 | G | Iron Fist |

### 10.4 Le plan de cartes de Harry Osborn

| card_id | type | nom | classe | coût | ressource | set_name |
|---|---|---|---|---|---|---|
| ho001a | Hero | * Green Goblin |  |  |  | Harry Osborn |
| ho001b | AlterEgo | * Harry Osborn |  |  |  | Harry Osborn |
| ho002 | Ally | * Spider-Man | Hero | 4 | Y | Harry Osborn |
| ho003 | Event | Repulsor Blast | Hero | 2 | R | Harry Osborn |
| ho004 | Event | Pumpkin Bomb | Hero | X | B | Harry Osborn |
| ho005 | Support | * Gwen Stacy Osborn | Hero | 2 | G | Harry Osborn |
| ho006 | Support | * Norman Osborn | Hero | 1 | G | Harry Osborn |
| ho007 | Support | * Otto Octavius | Hero | 2 | Y | Harry Osborn |
| ho008 | Upgrade | * Goblin Armor | Hero | 3 | B | Harry Osborn |
| ho009 | Upgrade | * Goblin Helmet | Hero | 2 | R | Harry Osborn |
| ho010 | Upgrade | Powered Gauntlets | Hero | 2 | Y | Harry Osborn |
| ho011 | Upgrade | * Goblin Glider | Hero | 3 | R | Harry Osborn |
| ho012 | Upgrade | “That Had to Hurt” | Hero | 1 | R | Harry Osborn |
| ho013 | Obligation | Risky Business |  |  |  | Harry Osborn |
| ho014 | SideScheme | Ruler of Manhattan |  |  |  | Harry Osborn Nemesis |
| ho015 | Minion | * Kingpin |  |  |  | Harry Osborn Nemesis |
| ho016 | Minion | * Bullseye |  |  |  | Harry Osborn Nemesis |
| ho017 | SideScheme | Refrain From Argument |  |  |  | Harry Osborn Nemesis |

### 10.5 Un gabarit de contrôle réel : Iron Fist

Le fichier `docs/packs/iron_fist_cartes.md` (annexe `annexes/M-gabarits-iron-fist.md`) contient les gabarits
`PROCESSUS-CARTE` remplis des 13 cartes. Début : le périmètre, les sources, la preuve de chaque gate, les
décisions de l'utilisateur appliquées.

*Extrait de `docs/packs/iron_fist_cartes.md`, lignes 1 a 58.*

```markdown
# Iron Fist (Hero Pack officiel MC64EN, FFG, novembre 2026) : gabarits PROCESSUS-CARTE

Preuves du 20/10/2026, branche `iron-fist-officiel`. Pack `iron_fist`, set « Iron Fist », 13 card_id :
`64001a` Iron Fist, `64001b` Danny Rand, `64002`-`64012` (11 cartes signature, 15 exemplaires). Numérotation
officielle (série 64 libre dans `data/cards.json` : Jessica Jones 61, Luke Cage 62, Wave fan-made 65) ;
numéro de carte = numéro de collection imprimé (1A/1B, 2 à 12).
Périmètre (décision du 20/10/2026) : héros + cartes signature. PAS les cartes d'aspect du pack ni les cartes
de rencontre (obligation, némésis : non publiées).

Sources : `.planning/iron-fist-officiel/` (relevé Hall of Heroes, lecture, cinq décisions de l'utilisateur
`lecture-reponses.md`, question ouverte `creation-questions.md`). Chaque carte relue sur son image avant le
code (`hoh-iron-fist/c1`-`c11-1`, `s1`, `s2`) : aucun écart avec le relevé.

**Cas** : `Fusion/marvel-lcg-src/tools/cas/iron_fist.py`, préfixe `[iron_fist]`, **57 cas, 57 verts**
(`CAS_PREFIX=ironfist_ PARALLELES=4 test_capacites.py .game-src 31000 <rapport> "[iron_fist]"`).
**Substitution** : `tools/substituer_pack.py .game-src 32000 640`, **13/13** cartes rouges sans leur module,
empreinte md5 du pack identique avant/après (`6d6a74b3…`). Les cas restés verts sous substitution sont tous
des témoins d'ABSENCE (coût impayable, autre forme, « pas jouée ») ou des valeurs imprimées (`desc`), listés
carte par carte.

**Autres gates** : `test_cards` 6810 ok / 0 erreur ; `verifier_prefixes` OK ; `verifier_appels_modules
iron_fist` OK (calibré : une sonde `Faces.MethodeInexistanteIronFist` le fait tomber, puis retirée) ;
`verifier_api_cartes` : aucun problème dans `iron_fist` (13 problèmes préexistants ailleurs) ;
`DECK_NOM=iron_fist verifier_tous_les_decks` : « identite 64001b, main 6, deck 9 » (témoin spider_man OK) ;
légalité des decks : 0 carte signature étrangère, exemplaires = `MaxPerDeck`. Plateau (étape 8 bis) :
`ui-app/src/board/iron-fist-plateau.test.ts`, 10 cas verts ; sensibilité prouvée (sonde `c_chi` renommé :
3 rouges). Aucun correctif de plateau nécessaire : le rendu générique des compteurs dessine déjà le chi.

**Autoplay** (étape 8) : `autoplay.py --deck iron_fist --vilains rhino --profils equilibre --parties 8` :
0 victoire / 8 (4,0 rounds), 0 blocage, **0 traceback** (grep NameError|AttributeError|TypeError|KeyError|
AssertionError|Traceback sur les 8 journaux) ; témoin `spider_man` même fournée : 0 / 8 (6,9 rounds),
0 blocage. Iron Fist n'a que ses 15 cartes signature (`player_deck` vide, PROCESSUS-HEROS étape 3) : la
défaite rapide est attendue. Seconde fournée `--vilains rhino,klaw --profils prudent,agressif --parties 4` : 0 / 16, 0 blocage, 0 traceback.
Cartes que le pilote n'exerce JAMAIS sur 24 parties : Deep Breathing (jouée), l'Action du Livre, la Ressource
de Redirect Chi ; la Forced Response de 64001a et la riposte d'Embody ne se sont pas présentées non plus
(couvertes par les cas).

Icônes de ressource : découpées et comparées à Luke Cage (MC62, même maquette 2026, `desc.RES` déclaré) :
62004 R (poing rouge), 62005 B (bleu), 62006 Y (éclair jaune), 62002 G (étoile verte). Aucune carte du pack
Iron Fist n'a de `RES` déjà déclaré : comparaison « même pack » impossible, à refaire au scan HD. Le glyphe
« ✱ ✱ » du texte de Redirect Chi est le glyphe [wild] (identique à 60043 American Sign Language, FNE 2026).

Décisions de l'utilisateur appliquées : (1) Technique mise en jeu par Danny Rand / le Livre attachée à
l'identité ; (2) au retournement en héros, les Techniques redeviennent Temporary et partent en fin de round ;
(3) The Way of Things : deux « a scheme » indépendants ; (4) Deep Breathing sans carte Iron Fist : tout le
deck défaussé, rien ajouté ; (5) les chi restent sur l'identité au retournement.
Aucune partie humaine n'a été jouée dans le navigateur.

### 64001a : * Iron Fist (face héros)

- [x] Étape 2 : carte(s) de référence : Response « After you play a card » → `fne/60027` Move in Shadow
      (`AfterPlayerPlayedCard(Response, "You", None, op)`) ; compteur sur l'identité → `venus/tv001a` ;
      « After the player phase ends » → `aos/50029`, `michelangelo/tm009` (`AfterPhaseEnd(ForcedResponse,
      "Player", op)`) ; soin de soi → `jubilee/47012`.
- [x] Étape 5 : texte-contre-code : « Response » nu imprimé sur la face héros (absent en Danny, cas) ; « play a
      card » ≠ « put into play » (cas) ; « here » = la carte d'identité ; « all BUT 4 » (surplus seulement,
      cas 3 chi) ; « heal 1 for EACH removed THIS WAY » (cas 7 → 4, 5 → 2 dégâts) ; Forced Response sans
      question. Résultat : OK.
```



---

## 11. Les pièges déjà payés, classés — **lis-les avant d'écrire**

Chaque ligne est une erreur qui a déjà coûté du temps sur ce projet. Les pièges **communs** aux campagnes et aux
héros (données, scripts, textes, méthode) sont repris en fin de chapitre, tels qu'ils figurent dans le manuel de
campagne (annexe L).

### 11.1 Le deck de départ et l'extension

| Piège | Ce qui se passe | Parade |
|---|---|---|
| Pas de `deck/starter/<héros>.json` | le héros n'apparaît **nulle part**, pas même dans le deck-builder | toujours écrire le fichier, avec ce qui est imprimé |
| `player_deck` composé par l'IA pour un héros maison | 33 decks « générés » ont dû être vidés le 12/09/2026 | vide, sauf decklist de l'auteur citée dans `metadata.note` |
| Carte signature d'un autre héros dans un deck | le moteur ne valide pas : la carte entre dans la partie | contrôle de classe `Hero` + `set_name` (le vérificateur le fait) |
| `set_aside` rempli dans le deck | **ignoré** en vraie partie ; un cas de test vert peut cacher une carte absente en jeu réel | `BeginGameWithSetAside` sur l'alter ego (§6.4) |
| Bio ou réplique indexée par le **nom** | « Spider-Man » désigne **trois** héros (`01001a`, `27030a`, un troisième) | bio : `card_id` de la face héros ; réplique : id du deck |
| Variante d'un deck sans `variante_nom` sur la base | la modale du héros ne replie pas la variante | `variante_nom` **des deux côtés** |
| Un deuxième deck de départ pour une identité alternative | un deuxième héros apparaît dans la grille | `metadata.hero_alts` (§5.3) |
| Règle de deck-building non déclarée | le moteur ne la connaît pas, le deck-builder laisse tout passer | `metadata.deckbuilding` + `deckbuilding_note` |
| Set némésis emprunté sans le dire | les cartes qui cherchent « le sbire némésis » ne trouvent pas le bon | `metadata.nemesis_note`, et un sbire marqué `desc.Nemesis` |
| `sets_info.heroes` oublié ou faux | le héros n'est dans aucune extension | `heroes: ["<id du deck>"]`, `scenarios` et `encounters` vides |
| Total de `hero_deck` ≠ 15 sans explication | en général une carte oubliée ou un exemplaire de trop | recompte sur les images ; sinon `QUESTIONS.md` |

### 11.2 Les cartes

| Piège | Ce qui se passe | Parade |
|---|---|---|
| Icône de ressource lue à vue | « ressource os » inventée sur Lockjaw : 4 cartes fausses cinq jours | comparer à une carte connue du même pack ; sinon question |
| `desc.GiveTo` = nom du héros au lieu de l'alter ego | l'obligation n'est pas donnée au bon joueur | nom de l'**alter ego**, sans étoile |
| `custom` absent d'une face d'identité | le créateur ne s'affiche pas | sur **toutes** les faces |
| Valeur de `desc` en nombre | refusé / mal lu | chaînes partout |
| `Uses` avec un compteur inconnu | **assertion à la construction** : la carte ne se construit pas | `reference/compteurs.json`, sinon `BESOINS-MOTEUR.md` **avant tout** |
| Trait inconnu de la liste typée | aucun effet à l'exécution | à signaler tout de même (`BESOINS-MOTEUR.md`) |
| Texte avec « Uses (3 counters) » mais `desc.Uses` absent | la carte entre sans compteur, l'action reste grisée | `desc.Uses: "3,<compteur>"` |
| `Victory` à `"0"` | la carte va quand même dans la pile de victoire | ne l'écris que si imprimé |
| Face héros sans les cinq stats ; alter ego avec ATK/THW/DEF | stats absentes ou parasites | face héros : HP ATK THW DEF HS ; alter ego : HP REC HS |
| Complot annexe de némésis en portrait | image tournée à l'envers | les complots annexes sont **paysage** (le serveur tourne l'image) |

### 11.3 Les scripts

| Piège | Ce qui se passe | Parade |
|---|---|---|
| Fonction ou clé inventée | la carte se construit et ne fait rien, **sans erreur** | annexe I ; aucune fabrique qui n'y est pas |
| `from . import *` absent / dossier de set sans `__init__.py` | toutes les cartes du set muettes | contrôlé par le vérificateur |
| Script dans le mauvais dossier | muet | `<pack>/<set_nettoyé>/<id>.py` |
| `CardFinder(name="* Carte")` | ne trouve **jamais** rien | le nom **sans** l'étoile |
| `CardFinder(trait=…)` sans `card_type` | assertion à la construction | toujours les deux |
| `WhenCardSetup` à **un** argument | la capacité ne fait rien | `("This", op)` |
| « Hero » écrit `"You"` dans un bonus continu | contre-cas alter ego faux | le nom de la face : `Hero` |
| « Limit once per round » oubliée | la capacité se répète | `LimitOncePerRound()` + témoin d'épuisement |
| Fabrique d'un modèle qui a **le même défaut** | `an001a` copiait `vp001a`, qui avait déjà une limite muette | une carte modèle se vérifie par un test, pas par ressemblance |
| `GetAbilities()` vide « parce que la carte est simple » | une capacité imprimée sans effet | `# A_FAIRE_CLAUDE:` ou un script réel |
| « play a card » écrit comme « put into play » | la capacité se déclenche pour les cartes mises en jeu | deux accroches différentes |
| Compteur « here » posé ailleurs que sur l'identité | le décompte ne se voit pas, la cible est fausse | `CostFunc.Counter("YourIdentity", n, '<compteur>')` |
| Un jeton de forme : que devient-il au retournement ? | décision de règle | le Rules Reference : le personnage **garde** dégâts, statuts, attachements, **jetons**, état prêt/épuisé |

### 11.4 Les tests

| Piège | Ce qui se passe | Parade |
|---|---|---|
| Cas qui s'arrête avant le point de rupture | le moteur **avale** l'exception ; 338 occurrences invisibles par fournée | le cas mesure **tout** ce que la carte annonce |
| `main_exclusive` défausse la main **après** la mise en place | une défausse préparée pour le cas est vidée | la poser dans `declencher` |
| Cas d'une carte « mise de côté » vert, carte absente en jeu réel | `Puzzle.CreatePlayerAdditionalDeck` fait exister la carte | vérifier le `BeginGameWithSetAside` du script |
| Pilote qui joue une carte du deck et fausse la mesure | Moxie donnait +1/+1/+1 et sauvait trois cas | écrire la ligne de base dans le cas |
| Un deck « prouvé » mais injouable (`lady_sif`) | assert de construction non exercé | **`verifier_tous_les_decks`** est une gate |
| Une gate qui répond OK sans avoir jamais échoué | aucune information | la voir échouer une fois |

### 11.5 Textes et habillage

| Piège | Ce qui se passe | Parade |
|---|---|---|
| Aucun texte français | aucun tooltip français, rien ne le signale | `textes-fr/<pack>.fragment.txt`, une entrée par `card_id` (doublons compris) |
| « Robustesse », « Inébranlable », « étourdi »… | la gate `vocabulaire-statuts` échoue | tableau du §7.1 |
| Biographie qui décrit la mécanique | hors sujet | le personnage seulement |
| Réplique **traduite** ou inventée | ce sont des répliques de comics / films | telles quelles, en anglais ; sinon demander |

### 11.6 Pièges communs aux campagnes et aux héros (extrait du manuel de campagne, annexe L)

Les renvois `§N` de cet extrait renvoient au **manuel de campagne** (annexe L), pas à ce manuel.

<!-- extrait de docs/kit-campagne-ia/KIT-CAMPAGNE-COMPLET.md -->
###### 14.1 Données (`cards.json`, scénarios, sets)

1. **Toutes les valeurs de `desc` sont des chaînes** (`"HP": "10"`).
2. **Un compteur de `desc.Uses` absent de l'énum `COUNTER` du moteur fait lever une assertion** : la carte ne se
   construit pas. Signale-le dans `BESOINS-MOTEUR.md` *avant* de livrer (`reference/compteurs.json`).
3. **Un mot-clé du texte absent de `desc` (ou l'inverse)** : « Uses (3 tactic counters) » sans `"Uses": "3,tactic"` →
   la carte entre en jeu sans compteur, son action reste **grisée pour toujours**, sans message. Certains attributs
   n'existent que pour certains types (`Uses` : Upgrade/Support/Attachment/Obligation/Environment ; `Villainous` :
   Minion) : le mettre ailleurs **empêche la carte de se générer**.
4. **`Victory: "0"` envoie la carte dans la pile de victoire** : ce n'est pas « neutre ».
5. **Le `*` n'a pas le même sens partout** : `HP`/menaces = « par joueur » ; `ATK`/`THW` d'un **allié** = dégâts
   consécutifs ; `SCH` avec `*` = multiplié par le nombre de joueurs (constat Skrull Menace : un `SCH` plein
   s'écrit `"2"`, jamais `"2*"`).
6. **`type: "SideScheme"` dans le JSON, `EncounterSideScheme` dans les scripts.**
7. **Le dossier d'un script est le `set_name` « nettoyé »** (`CleanName`) ; un dossier de set **sans
   `__init__.py`** rend toutes ses cartes **muettes, sans erreur** ; un script mal rangé aussi.
8. **L'extension de l'image est obligatoire** ; **les complots restent stockés en paysage** (le serveur les pivote).
9. **Un set de rencontre cité dans un scénario mais sans fichier se charge VIDE, sans erreur.**
10. **Les checksums** de `cards.json` et `sets_info.json` : un fichier au checksum faux est rejeté **en silence**.
11. **Un `card_id` est une clé partout** (image, texte français, script, scénario, carnet) : on ne le renomme pas.
12. **Un préfixe fan-made non déclaré, un numéro officiel emprunté, un identifiant en double** : le second écrase
    le premier, sans un mot.
13. **`full_link`** : la carte ne porte **rien d'autre** que `card_id` et `full_link`. **`ability_link`** : mêmes
    capacités, données propres. **Avant d'écrire un script, cherche si la carte existe déjà** (Web of Deceit :
    six `ability_link` à la place de six scripts).
14. **Le nom d'un set de rencontre (`name`) s'affiche tel quel** : casse normale.
15. **`_expert` ne figure jamais dans l'`id` d'un scénario de campagne** : l'écran prend la variante tout seul.
16. **Les stades** : le `villain` standard liste les stades 1-2, l'expert 2-3 ; les complots principaux sont une paire
    a/b **par stade**.

###### 14.2 Scripts de cartes

17. **Aucune fonction, aucune chaîne de ciblage inventée** : une chaîne inventée ne lève **rien**, la carte est inerte.
18. **`CardFinder(name="* X")` ne trouve jamais rien** : le nom s'écrit sans l'étoile.
19. **Les mots-clés de `desc` ne se recodent pas** (Toughness, Surge, Guard… appliqués deux fois).
20. **Un filtre va dans `conditions`**, jamais en tête de l'opération : une capacité facultative est **proposée**
    dès que son message part.
21. **Les fabriques qui rendent une LISTE** (`GiveKeywordToAttached`, `GiveKeywordToInPlayWhenApplyThis`) : sans
    `*` pour la déplier, la carte se construit avec une liste dans sa liste et le moteur plante **à la
    génération** — **`test_cards` ne le voit pas**, seule une vraie partie l'attrape (Web of Deceit, deux fois).
22. **Le `Setup` d'une carte à mot-clé `Setup`** se code `AfterGameSetup` ; **`WhenCardSetup("This", …)` est
    réservé à la face 1A du complot principal.**
23. **Les PV sont portés par la CARTE, pas par la face** : une carte retournée à 0 PV arrive sur sa nouvelle face
    **déjà vaincue** et le moteur redéclenche la défaite pendant le retournement (Shocker se retournait sans fin :
    A → B → A…). Rends les PV à la face avant de retourner.
24. **Les capacités d'une carte dans la pile de victoire ne se déclenchent jamais** (hors jeu).
25. **Une obligation révélée reste en jeu** si le script ne la défausse pas : code toutes les branches.
26. **Ne réimplémente jamais le choix de face standard/expert** : la carte le fait (`StandardModeOnly()` /
    `ExpertModeOnly()`).
27. **Une limite imprimée (« once per round ») sur un déclencheur de défaite** : piège moteur connu, signale-le.
28. **`Puzzle.PutIntoPlay` sur une carte d'un paquet de scénario spécial ne l'attache pas** : utilise
    `Puzzle.Reveal` (chemin réel).
29. **L'unicité d'une FAMILLE de cartes** (WEB-WARRIOR ou « Spider » dans le titre) : `UniqueRuleNotApplyTo` ne sait
    viser qu'une carte : une capacité écrite à la main (écart assumé, écrit).
30. **Le résultat de fin de partie se lit dans le message** (`message.players_won`), jamais dans le monde.

<!-- extrait de docs/kit-campagne-ia/KIT-CAMPAGNE-COMPLET.md -->
###### 14.4 Textes, images, interface

44. **Un pack sans texte français est muet en français sans que rien ne le signale.**
45. **Vocabulaire officiel** ; jamais « étourdi », « Inébranlable », « Robustesse », « carte de statut Robuste » : une gate
    échoue.
46. **Noms propres et traits restent en anglais** dans le texte français.
47. **Les biographies de vilain s'indexent par le `card_id` de la première face**, jamais par le nom.
48. **Une planche posée en tête de la colonne de récit** de l'écran de campagne en ordre libre **pousse le carnet hors
    de l'écran** : un test d'écran vérifie la présence, pas la place ; regarde une capture.
49. **Les pages du livret sont carrées, 975 × 975** ; les pages françaises vont dans `fr/` ; `livret_fr: true` sinon
    l'écran ne les cherche pas.
50. **Une chaîne d'interface nouvelle sans entrée dans `dico-en`** reste en français dans l'interface anglaise.

###### 14.5 Méthode et fidélité

51. **Transcris une planche de 4 cartes par lecture** : au-delà, le texte d'encart n'est plus sûr.
52. **Les fichiers de l'auteur font foi, pas les captures de son livret** (la page 15 du livret de Web of Deceit
    montre un Shocker que la carte du dossier ne porte plus).
53. **Les icônes de complot n'ont pas la même forme chez tous les auteurs.** Conventions **validées par l'utilisateur**,
    **propres à leur pack** : *Skrull Menace* (Kajislav) — Crise = « ! » dans une explosion ; Accélération = croix +
    pointe + barre ; Aléas (Hazard) = croix sur carte penchée ; Amplify = croix + avion ; « Y » rouge = icône de
    boost ordinaire ; ★ = renvoi au texte. *MC/DC Punisher 2026* — « !! » = Crise ; croix à trois pointes + = Amplify ;
    triangle « toit de maison » + = Accélération ; carré « carte + » = Aléas. **Compare toujours à une carte du
    MÊME pack dont l'icône est connue ; une icône inconnue → `QUESTIONS.md`.**
54. **Une carte « impr. Interrupt » dont le texte dit « After »** : question à l'utilisateur, **pas de correction
    silencieuse** (Swarmed by Rats, Hunting Season).
55. **« Je n'ai pas lancé » ≠ « c'est vert »** : écris-le. Une livraison antérieure ne devait pas être déclarée
    jouable avec des points ouverts.
56. **Une gate qui répond OK n'est pas une preuve tant qu'on ne l'a pas vue échouer** ; ne retire jamais une assertion
    parce qu'elle échoue (le défaut revient en jeu).
57. **Un cas de test peut être vert en n'exerçant rien** (une carte du deck paie à elle seule le coût ; le pilote décline
    les choix facultatifs) : fixe la main (`main_exclusive`), mesure un **chiffre**.



---

## 12. Référence commune aux campagnes et aux héros

Ce chapitre reprend, **mot pour mot**, les tableaux du manuel de campagne qui valent aussi pour un héros : clés d'une
carte, `desc` complet, balises du texte imprimé, icônes de ressource, mots-pièges. **Les numéros de section
(4.2, 4.5, 4.6, 4.8, 6.7) sont ceux du manuel de campagne** (annexe L), pas ceux de ce manuel. Les renvois `§N` à
l'intérieur renvoient eux aussi à l'annexe L ; là où ils parlent de scénarios ou de carnet, ignore-les.

### 12.1 Clés de premier niveau d'une carte (campagne §4.2)

<!-- extrait de docs/kit-campagne-ia/KIT-CAMPAGNE-COMPLET.md -->
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

### 12.2 `desc` : le contenu complet (campagne §4.5)

<!-- extrait de docs/kit-campagne-ia/KIT-CAMPAGNE-COMPLET.md -->
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

### 12.3 Le texte imprimé : balises et jetons (campagne §4.6) et cartes à plusieurs faces (§4.7)

<!-- extrait de docs/kit-campagne-ia/KIT-CAMPAGNE-COMPLET.md -->
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

### 12.4 Mots-pièges du texte imprimé (campagne §6.7)

<!-- extrait de docs/kit-campagne-ia/KIT-CAMPAGNE-COMPLET.md -->
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

### 12.5 La surface d'un script, les types de capacité (campagne §6.2 et §6.3)

<!-- extrait de docs/kit-campagne-ia/KIT-CAMPAGNE-COMPLET.md -->
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

<!-- extrait de docs/reference/KIT-CHATGPT-CREATION.md -->
#### 7.1 Squelette

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

#### 7.2 Types de capacité (`AbilityType`)

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

#### 7.3 Les fabriques (signatures réelles)

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

#### 7.4 Méthodes chaînées d'une capacité

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

#### 7.5 Coûts (`CostFunc`)

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

#### 7.6 Cibles (`SetTarget`)

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

#### 7.7 Chercher des cartes : `CardFinder`

`CardFinder(name="Rhino")`, `CardFinder(name="Rhino", card_type=Villain)`,
`CardFinder(trait="TECH")`, `CardFinder(traits=["AVENGER"], card_type=Ally)`,
`CardFinder(non_trait="ELITE", card_type=Minion)`,
`CardFinder(has_printed_res="B")`, `CardFinder(card_class="Leadership")`.

⚠ **Le nom s'écrit SANS l'étoile d'unicité** : `CardFinder(name="Silver
Samurai")`, jamais `"* Silver Samurai"` (la seconde forme ne trouve jamais
rien, en silence).

#### 7.8 Opérations courantes (toutes vues dans les exemples)

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

### 12.6 Glossaire

| Mot | Sens ici |
|---|---|
| **Pack** | la clé d'un groupe de cartes dans `cards.json` (`lockjaw`) et le dossier `src/cards/pack/<pack>/` |
| **Set** | un groupe de cartes qui partagent un `set_name` (« Lockjaw », « Lockjaw Nemesis ») |
| **Identité** | la paire de faces `…a` (héros) / `…b` (alter ego) — éventuellement avec des formes de plus (`…c`) |
| **Face** | un côté d'une carte à deux côtés ; un script par face à capacité |
| **Signature** | une carte de classe `Hero` : elle appartient à un seul héros |
| **Deck de départ** | `deck/starter/<id>.json` : la fiche d'inscription du héros, pas un « deck de joueur » |
| **Variante** | un second deck de départ replié sous le premier (`variante_de`) ; ≠ identité alternative (`hero_alts`) |
| **Némésis** | le set `"<Héros> Nemesis"` ; son sbire est marqué `desc.Nemesis` |
| **Obligation** | une carte de rencontre « donnée » à l'alter ego (`desc.GiveTo`) |
| **Gate** | un contrôle qui doit passer pour que le travail soit terminé |
| **Cas** | un test de capacité de `tools/cas/<héros>.py` (une partie) |
| **Substitution** | la preuve qu'un cas est rouge sans le module de la carte |
| **Gabarit** | la fiche de preuves d'une carte (`PROCESSUS-CARTE`) |
| **`A_FAIRE_CLAUDE`** | le marqueur d'un manque que l'IA ne peut pas combler seule |
| **Fragment** | la part d'un fichier partagé que tu livres, à fusionner par Claude |

### 12.7 L'index des annexes du zip

| Fichier | Contenu | Quand l'ouvrir |
|---|---|---|
| `annexes/A-kit-cartes.md` | **Kit de création de cartes** : format `cards.json`, scripts, **67 exemples réels classés par mécanique**, pièges, format de livraison | pour écrire un script : chercher la carte modèle |
| `annexes/B-recettes-moteur.md` | **Recettes** : mécanique imprimée → fabrique + carte modèle + piège, et les pièges payés pack par pack | devant une mécanique inhabituelle |
| `annexes/C-mots-cles-tous.md` et `annexes/C-mots-cles/` | les **fiches de mots-clés** (officiels et maison) | dès qu'un mot-clé apparaît sur une carte |
| `annexes/D-processus-carte.md`, `D-processus-heros.md` | le processus qualité d'une carte, d'un héros | pour remplir un gabarit |
| `annexes/E-guide-creation-contenu.md` | le guide de référence (architecture, formats, validation, harnais) | pour les commandes de validation |
| `annexes/I-index-api-moteur.md` | **l'index de l'API du moteur** : chaque classe et fonction, ses arguments, sa première ligne | **pour ne rien inventer** |
| `annexes/J-architecture-et-code.md` | l'architecture du projet : couches, flux, emplacement de chaque chose | pour situer un fichier |
| `annexes/L-manuel-campagne-cartes-et-scripts.md` | le manuel de création de **campagne** (cartes, scripts, textes, pièges) | pour les chapitres généraux de cartes et de scripts |
| `annexes/M-gabarits-iron-fist.md` | les gabarits `PROCESSUS-CARTE` remplis d'un héros officiel (13 cartes) | comme modèle de preuve |
| `commun/` | les fichiers génériques du moteur, du lanceur et des outils qui font marcher un héros | pour lire le code réel |
| `reference/*.json` | les listes du jeu (ids, sets, traits, compteurs, préfixes, decks existants, cartes signature) | utilisées par le vérificateur |

### 12.8 Commandes utiles (pour Claude ; à titre d'information)

```bash
W="/home/oem/Desktop/Marvel LCG/Fusion/marvel-lcg-src"
PY="/home/oem/Desktop/Marvel LCG/.venv-linux/bin/python"                  # Python 3.10
python3 outils/verifier-livraison-heros.py <livraison> --moteur "$W"          # la forme, contre le jeu réel
python3 outils/comparer-livraison-heros-au-depot.py <livraison> <pack> <deck> # refaire un héros connu : identique / différent / manquant
cd "$W" && DECK_NOM=<deck> "$PY" tools/verifier_tous_les_decks.py             # le deck se monte (gate)
cd "$W" && CAS_PREFIX=<nom> PARALLELES=4 "$PY" tools/test_capacites.py "$W/.game-src" 31000 /tmp/rapport.json "[<deck>]"
cd "$W" && "$PY" tools/substituer_pack.py "$W/.game-src" 32000 <préfixe>      # la preuve par substitution
cd "$W" && "$PY" tools/recalculer_checksums.py "$W" data/cards.json data/sets_info.json   # PYTHONPATH=$W/src
```

