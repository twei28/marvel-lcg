# Echo : l'observation en suspens était un vrai défaut, et la carte se joue maintenant des deux côtés

Suite du signalement n°17 (Yarro, 19/09/2026) et de la fiche
`.planning/todos/2026-09-20-echo-photographic-reflexes-ergonomie.md`, dont la
section « à instruire » est remplacée par la conclusion ci-dessous.

Branche `mode-manuel`. Aucun déploiement.

---

## 1. La conclusion demandée : ARTEFACT **et** DÉFAUT

L'observation disait : « en forme **CIVILE**, la carte glissée est rapportée
`jouable = True` ». Les deux lectures proposées étaient justes toutes les deux,
et il fallait mesurer pour le voir.

### 1a. La mesure du 20/09 était fausse, et voici pourquoi

`face.CanPlayBy(joueur)` **ne peut pas** répondre à cette question.
`HasCost.CanPlayBy` (`src/game/card/face/attribute/has_cost.py:43-57`) pose
`self.card.can_state.is_like_in_hand = True` **avant** d'appeler
`EventManager.FilterAvailableEffects`, puis le remet à `None`. Il
court-circuite donc exactement l'endroit où vit la condition de forme :
`check_tucked_playable`, branché sur le message `CheckIfFaceIsLikeInHand`.

Mesuré sur la position montée (sonde, harnais `test_capacites`) :

| état | `CanPlayBy` |
| --- | --- |
| forme héros | `True` |
| forme civile | `True` |
| retour forme héros | `True` |

`CanPlayBy` répond « oui » dans les trois cas. Il aurait répondu « oui » sur
une carte qu'aucune règle n'autorise. **Il ne mesure pas la jouabilité d'une
carte hors de la main.** C'est écrit noir sur blanc dans la docstring de
`_echo_effets_de_jeu` (`tools/test_capacites.py`), pour que personne ne refasse
cette mesure.

### 1b. Mais le moteur laissait bel et bien jouer la carte en forme civile

Même position, mesurée par le **vrai** chemin (`face.IsLikeInHand()`, qui envoie
`CheckIfFaceIsLikeInHand`, puis `FilterAvailableEffects`) :

| état | `IsLikeInHand()` | effets de jeu offerts | attendu |
| --- | --- | --- | --- |
| forme HÉROS | `True` | 1 | ✅ |
| bascule en forme CIVILE | `True` | **1** | ❌ 0 attendu |
| retour en forme HÉROS | `False` | **0** | ❌ 1 attendu |

Et, en vidant le cache à la main avant chaque lecture : `True / False / True`,
c'est-à-dire la bonne réponse.

**Cause.** `card.can_state.is_like_in_hand` est un cache qui n'est remis à zéro
qu'au **déplacement** d'une carte (`src/game/card/card.py`, `MoveToArea` ->
`can_state.Reset()`). Or la réponse de `check_tucked_playable` dépend de deux
choses qui bougent sans que la carte glissée ne bouge : la **forme** du joueur,
et la présence de **Photographic Reflexes** dans sa main. La première réponse
restait donc figée pour toute la vie de la carte sous Echo.

C'est un piège connu du moteur, et Echo était la troisième carte à tomber
dedans : Magik (`aoa/magik/45030a.py`) remet déjà `is_like_in_hand` à `None` à
la main sur les cartes du dessus de son deck, et le correctif « pack brawn » en
tête de `Card.IsLikeInHand` traite la même famille pour la Réserve.

**Et c'est ce que le joueur a vécu.** La troisième ligne du tableau dit mot pour
mot son « en prod tu ne peux rien faire » : un aller-retour en forme civile
suffisait à éteindre définitivement toutes les cartes glissées. La réserve du
20/09 (« son "en prod" porte peut-être sur une partie qu'on n'a pas sous les
yeux ») est donc levée dans l'autre sens : il n'y avait pas qu'un défaut
d'ergonomie.

**Verdict : VRAI DÉFAUT DE RÈGLE. Corrigé.**

---

## 2. Les clauses, une par une, contre le texte imprimé

Texte vérifié sur MarvelCDB (`marvelcdb.com/card/60037a`, `/60040a`) et contre
`data/cards.json`, qui porte exactement le même libellé sur les trois variantes
`60040a` / `60040b` / `60040c`.

| clause imprimée | verdict | témoin |
| --- | --- | --- |
| « After a player plays an aspect or basic event, **tuck that event under here from that player's discard pile** » | **juste** | `Watch and Learn : l'evenement basique joue est glisse sous Echo` (glissé, et absent de la défausse) |
| « if there are **more than 3** tucked cards here, **discard all but 3** » | **juste** | `une 4e carte glissee, on defausse jusqu'a 3` (4 événements joués, 3 restent) |
| « **If you are in hero form** » | **CORRIGÉ** (c'était le défaut du §1) | `forme CIVILE : la carte glissee n'est PAS offerte` et `retour en forme HEROS` |
| « you can **discard Photographic Reflexes from your hand** to play » | **juste**, et désormais offert dans les deux sens | `chemin A`, `chemin B`, `trois variantes` |
| « **Reduce the cost to play that event by 2** » | **CORRIGÉ** (c'était une génération de ressources) | `chemin B : la carte glissee coute 2 de moins` (Haymaker coût 2, joué sans une ressource en main) |
| « You **cannot trigger** Echo's *Watch and Learn* ability **for that event** » | **juste**, sur les deux chemins | `Watch and Learn ne re-glisse PAS l'evenement joue depuis sous Echo` |
| Photographic Reflexes se défausse, et **les trois variantes** | **juste**, avec un correctif : voir §3c | `trois variantes en main : c'est CELLE qu'on clique qui part` |

### 2a. La réduction de 2 : ce n'en était pas une

C'était `CanGenerateResources(AbilityType.Resource, Resources('GG'), ...)` :
Echo **offrait deux ressources wild** au lieu de **réduire le coût**. Le montant
sorti de la main est le même dans le cas ordinaire, ce qui explique que
personne ne l'ait vu. Ce n'est pourtant pas la même règle :

- deux **wild** couvrent une exigence de couleur (`Requirement`) qu'une
  réduction de coût laisserait à payer ;
- elles comptent comme des ressources **dépensées**, donc toute carte qui lit
  le paiement (« if you paid for this using at least 1 [physical] », `47021`
  Multitalented, ou le bonus d'Ashley Barton `mw023`) est faussée ;
- le coût **affiché** au joueur reste le coût plein.

L'idiome du dépôt pour cette tournure exacte est `WhenCalculateEffectCost` +
`message.UpdateCost(-N, effect)` : c'est ce que font `dz014` Lightbringr et
`aa002` Scarlet Witch, qui portent **la même phrase imprimée** (« Reduce the
cost ... by 1 »). Echo est passée dessus.

Bénéfice secondaire : la réduction vit maintenant à **un seul endroit**, donc
les chemins A et B paient rigoureusement la même chose.

### 2b. Ce que j'ai lu en ligne, et ce que je n'ai pas trouvé

- `marvelcdb.com/card/60040a` : texte confirmé mot pour mot, type **Hero
  Event**, coût **X**. La page ne porte **aucune** review ni ruling
  (« No review yet for this card ») : rien sur « défausser est-il un coût »,
  rien sur la réduction.
- `marvelcdb.com/card/60037a` : texte de *Watch and Learn* confirmé, et une
  review qui décrit la boucle « jouer / enregistrer / rejouer » sans trancher de
  point de règle.
- L'annonce FFG « Watch and Learn » du 30/04/2026 est en **HTTP 403** depuis
  ici : je ne l'ai pas lue, et je ne m'appuie donc pas dessus.
- Recherche ciblée « ruling discard from hand to play tucked event » : aucun
  ruling officiel trouvé.

**Conclusion de la recherche : aucun ruling ne contredit le texte, et le texte
suffit.** Le seul point que j'ai tranché sans source externe est traité au §3b
ci-dessous, et il est annoncé comme un arbitrage.

---

## 3. Ce qui a été construit : Photographic Reflexes devient cliquable

Décision de l'auteur : **les deux chemins, aucun retiré.**

- **Chemin A (nouveau)** : on clique Photographic Reflexes en main, le moteur
  demande quel événement glissé jouer, le coût est réduit de 2, et c'est la
  carte cliquée qui part.
- **Chemin B (conservé intact)** : on clique la carte glissée, Photographic
  Reflexes part toute seule.

### 3a. Comment le chemin A est monté

`src/cards/pack/fne/echo/__init__.py` porte le constructeur commun aux trois
variantes ; `60040a.py`, `60040b.py` et `60040c.py` ne font que l'appeler (ils
étaient vides).

```
AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, photographic_reflexes,
                                  conditions=[il_y_a_un_evenement_glisse])
    .SetCostFunc(CostFunc.Discard("This"))
    .CanWorkOnlyInHand()
```

Cartes de référence : `an006` Angelic Ribbons et `al014` Lurking
(« discard this card → » est un **coût**, `CostFunc.Discard("This")`) ;
`21185` System Shock et `21032` Pip the Troll (une capacité déclenchée **depuis
la main**, `CanWorkOnlyInHand()`) ; `16130` Crystal Ball (« may play a card ...
reducing its resource cost » → `player.PlayOneCardLikeInTurn`, qui demande
laquelle puis la joue en payant vraiment).

`AbilityType.HeroAction` porte à lui seul le « If you are in hero form »
(`Ability.GetAbilityTypeCondition` : `effect.GetInitiator().IsHero()`), et la
condition `il_y_a_un_evenement_glisse` fait que la carte n'est **pas** cliquable
quand il n'y a rien sous Echo — sans quoi on recréait le défaut d'origine sous
une autre forme (une carte qui a l'air morte en main).

### 3b. Un arbitrage, annoncé comme tel

Le texte dit « **discard** Photographic Reflexes ... **to play** an event », pas
« play Photographic Reflexes ». Le chemin A la défausse donc comme **coût**
d'une action, et non comme un événement joué. C'est ce qui distingue les deux
dans les règles : une carte simplement défaussée ne déclenche pas les
« after you play an event ». Le montage choisi (`CostFunc.Discard("This")` sur
une `HeroAction`) est fidèle à cette lecture.

Je n'ai trouvé **aucun ruling** pour la confirmer ou l'infirmer ; c'est une
lecture littérale du texte imprimé, pas une source.

### 3c. Un défaut créé, mesuré, corrigé dans la foulée

Première version du chemin A : trois Photographic Reflexes en main, on clique
`60040b`, **il en reste une seule**. Le chemin A défausse la carte cliquée comme
coût, et la règle d'Echo (`discard_photographic_reflexes`, chemin B) en
défaussait une **seconde** parce qu'une carte venait d'être jouée depuis la zone
glissée. Corrigé par un drapeau `REFLEXES_DEJA_PAYEES` posé pendant le rejeu
(idiome repris de Magik, `initiator.flag`). Témoin dédié : `trois variantes en
main : c'est CELLE qu'on clique qui part`, qui vérifie que `60040a` et `60040c`
sont **encore en main**.

---

## 4. Le correctif du cache, et son risque

`rafraichir_les_glissees` (`60037a.py`) vide `can_state.is_like_in_hand` sur les
cartes **encore** dans la zone glissée, sur trois déclencheurs :

- `AfterUnitChangeForm(Rule, 'You', ...)` — la forme change ;
- `AfterCardEnterHand(Rule, CardFinder(name='Photographic Reflexes'), ...)` ;
- `WhenCardWouldMoveToArea(Rule, CardFinder(name='Photographic Reflexes'), ...)`
  quand elle **quitte la main**.

**Le risque, et sa mesure.** Rafraîchir en plein milieu d'un jeu de carte
pourrait effacer le drapeau que `PlayCardsLikeInTurn` **force** pendant la
résolution, et faire avorter le coup. Deux garde-fous :

1. on ne touche que les cartes **encore** dans la zone glissée — celle qu'on
   joue l'a déjà quittée pour la zone de résolution ;
2. un témoin dédié le met à l'épreuve au pire moment :
   `la carte glissee payee AVEC une Photographic Reflexes de la main`. Hit and
   Run coûte 3, soit 1 après réduction, et il ne reste **que** des Photographic
   Reflexes en main : le rafraîchissement part donc **pendant le paiement**.
   Vert : 4 dégâts sur Rhino, la carte part.

---

## 5. Les témoins ajoutés — le pack n'en avait AUCUN

`fne/echo` n'avait pas un seul cas de comportement avant aujourd'hui. C'est ce
trou qui a laissé vivre le défaut : rien ne regardait la forme.

**14 cas ajoutés** dans `tools/test_capacites.py` :

| cas | ce qu'il prouve |
| --- | --- |
| `60037a Echo — Watch and Learn : l'evenement basique joue est glisse sous Echo` | la carte est glissée et n'est pas restée en défausse |
| `60037a Echo — forme HEROS et Photographic Reflexes en main : la carte glissee est offerte` | le positif, + contre-bout : la défausse n'est PAS offerte |
| `60037a Echo — forme CIVILE : la carte glissee n'est PAS offerte` | **le témoin du défaut** |
| `60037a Echo — retour en forme HEROS : la carte glissee redevient offerte` | l'aller-retour complet, lu à chaque étape |
| `60037a Echo — sans Photographic Reflexes en main, la carte glissee n'est PAS offerte` | la troisième condition |
| `60037a Echo — Watch and Learn : une 4e carte glissee, on defausse jusqu'a 3` | la limite de 3 |
| `60037a Echo — Watch and Learn ne re-glisse PAS l'evenement joue depuis sous Echo` | « You cannot trigger ... for that event » |
| `60040a ... chemin B : la carte glissee coute 2 de moins et defausse Photographic Reflexes` | la réduction ET la défausse automatique |
| `60040a ... chemin A : on clique la carte EN MAIN, elle joue l'evenement glisse` | le geste que le joueur cherchait |
| `60040b ... trois variantes en main : c'est CELLE qu'on clique qui part` | le §3c |
| `60040a ... la carte glissee payee AVEC une Photographic Reflexes de la main` | le §4 |
| `60040a ... aucune carte glissee : la carte n'offre AUCUNE action` | pas de défausse pour rien |
| `60040a ... forme CIVILE : la carte n'offre AUCUNE action` | « If you are in hero form » sur le chemin A |
| `60040a ... forme HEROS avec un evenement glisse : l'action EST offerte` | le bout positif des deux précédents |

### Le harnais a gagné deux clés, toutes deux additives

- `jouer_glissee: [card_id]` — joue une carte **glissée** par le vrai chemin :
  `effect.Find("Play")` + `FilterAvailableEffects` + `ChooseEffects`. Ni
  `jouer_carte` (qui ne regarde que la main) ni `PlayCardsLikeInTurn` (qui
  **force** `is_like_in_hand` et court-circuite donc la question mesurée) ne
  savaient le faire.
- `action_en_main: [card_id]` — déclenche une action portée par une carte **en
  main**, désignée par `card_id`. `Puzzle.Action` ne sait pas viser la main :
  `FindOrCreateFace` cherche par **nom** dans le deck puis la défausse, et sur
  Photographic Reflexes (six exemplaires dans le deck héros) il attrapait la
  copie du deck.

Les deux tournent **après** `declencher_apres`, volontairement : c'est le seul
moyen de changer la main entre la mise sous Echo et le rejeu, sans quoi le
témoin du §4 n'était pas montable.

### Preuve par substitution (étape 7.3 de PROCESSUS-CARTE)

| substitution | résultat |
| --- | --- |
| les 3 rafraîchissements retirés de `60037a.py` | **2 rouges** : `forme CIVILE` (« le moteur OFFRE de la jouer, attendu refusée ») et `retour en forme HEROS` (« la réponse *jouable* est figée »). Les 7 autres verts. |
| la réduction de coût retirée | **2 rouges** : chemins A et B (« 3 dégâts au lieu de 6 », la carte glissée n'est plus payable). Les 4 autres verts. |
| le module des trois variantes vidé (`return []`) | **3 rouges** : chemin A, trois variantes, et « l'action EST offerte ». |
| le drapeau `REFLEXES_DEJA_PAYEES` absent (état mesuré avant correctif) | main `['60040c']` au lieu de `['60040a', '60040c']` |

⚠ **Deux contre-cas restent verts sous substitution** et c'est normal : `aucune
carte glissee : la carte n'offre AUCUNE action` et `forme CIVILE : la carte
n'offre AUCUNE action` affirment une **absence** d'effet. Ils sont assumés ici
plutôt que maquillés, comme le demande l'étape 7.3 ; c'est le cas positif
(`forme HEROS ... l'action EST offerte`) qui les rend discriminants.

⚠ **Un premier essai de substitution a été jeté** : le remplacement avait avalé
le `]` de fermeture de la liste, le module ne se chargeait plus du tout et les
**sept** cas d'Echo rougissaient. Un module qui ne compile pas ne prouve rien
sur la ligne qu'on voulait retirer ; la substitution a été refaite
syntaxiquement valide.

⚠ **Le témoin d'aller-retour a dû être réécrit.** Deux `Puzzle.ChangeForm` à la
suite, sans lecture entre les deux, laissent le cache sur sa valeur de forme
héros : le cas passait au vert **même sans le correctif**. Le vérificateur
`echo_aller_retour` fait donc les bascules lui-même et **lit** à chaque étape —
c'est ce que fait le plateau à chaque rafraîchissement, et c'est pour ça que le
joueur, lui, l'a vu.

---

## 6. Verdict de la batterie

`tools/test_capacites.py` **EN ENTIER**, `PARALLELES=12`, sur un dossier de jeu
jetable (`.game-src-echo`, supprimé après la passe ; ni `.game`, ni `.game-src`,
ni aucun dossier d'une autre session n'a été touché) :

**2360 / 2365 cas passés.**

Les cinq rouges, **rejoués et comparés par leur NOM** (jamais par les totaux :
l'arbre est partagé et le nombre de cas bouge) :

| cas | rejoué seul | verdict |
| --- | --- | --- |
| `ls004` Lead The Charge | **vert** (`CAS_INDEX=1050`, séquentiel) | **artefact de passe parallèle** : le journal montre un `AttributeError: type object 'Engine' has no attribute 'game'` dans `Engine.Initialize`, c'est-à-dire un plantage **avant** le début de la partie |
| `sg009` Squirrel Girl's Costume | — | **antérieur** |
| `sg013` Call the Squirrels | — | **antérieur** |
| `sg007` The Gatherer | — | **antérieur** |
| `sg006` The Forager | — | **antérieur** |

Les quatre `sg00x` sont **nommément** les mêmes que ceux relevés par les
rapports du 20/09 (`2026-09-20-spdr-paiement-incomplet.md`) et du 21/09
(`2026-09-21-cartes-coincees-en-resolution.md`), où ils ont été établis
antérieurs **par mesure** sur un moteur de référence. Ils vivent dans
`pack/squirrel_girl`, sans aucun rapport avec `fne/echo` ; et les deux clés
ajoutées au harnais sont strictement additives (aucun cas existant ne les
définit).

**Les 14 témoins d'Echo sont verts dans la passe complète**, comptés un par un.

**Réserve de méthode.** La passe retenue est une passe parallèle : le seul
rouge suspect a été rejoué en séquentiel, pas les 2360 verts.

---

## 7. Mes inquiétudes

1. **Le cache `is_like_in_hand` reste un piège de moteur, et je ne l'ai pas
   refermé.** Je l'ai contourné sur Echo, comme Magik le contourne chez elle.
   Le vrai correctif serait dans le moteur, mais `can_state.is_like_in_hand`
   sert **deux** rôles à la fois : mémo de la réponse, et **drapeau forcé** que
   `has_cost.CanPlayBy`, `player_action.py` et `PlayCardsLikeInTurn` posent à
   `True` pour jouer une carte hors de la main. On ne peut donc pas simplement
   supprimer la mémoïsation sans casser tous les « play like in hand » du
   dépôt. Séparer les deux rôles est un chantier moteur à part entière, à
   ouvrir sciemment — pas en passant.
   **Toute autre carte qui pose une condition VARIABLE sur
   `CheckIfFaceIsLikeInHand` porte le même défaut.** J'en vois une :
   `fne/daredevil/60001a.py` (Sense the Top), dont la condition est
   `message.which_face == initiator.additional_deck.GetTop()` — le dessus d'une
   pile qui bouge. Je ne l'ai pas mesurée.

2. **Le chemin A n'a pas été vu à l'écran.** `test_capacites` prouve ce que le
   moteur fait, pas ce que le plateau dessine (étape 8 bis). Une action portée
   par une carte **en main** est une forme que je n'ai pas vérifiée côté
   `ui-app` : rien ne garantit que le bouton apparaisse. C'est le point à
   regarder en premier avant de répondre au joueur.

3. **Pas d'autoplay ciblé** (étape 8). Le deck d'Echo n'a pas été passé à
   `tools/autoplay.py`, faute de temps de machine : la batterie complète et les
   quatre substitutions ont déjà pris l'essentiel de la session.

4. **Le drapeau `REFLEXES_DEJA_PAYEES` est un compteur par joueur.** Si le
   chemin A était un jour interrompu par une exception hors du `finally`, il
   resterait posé et Echo cesserait de défausser sur le chemin B. Le `finally`
   couvre ce que je sais atteindre, pas ce que je ne sais pas.

5. **Le multijoueur n'est pas couvert.** « After **a player** plays an aspect or
   basic event » fait glisser sous Echo l'événement d'un **autre** joueur : tous
   les témoins sont en solo (`heros2` non utilisé).
