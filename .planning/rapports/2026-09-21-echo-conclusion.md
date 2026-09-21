# Echo : l'observation en suspens était un vrai défaut, et la carte se joue maintenant des deux côtés

Suite du signalement n°17 (Yarro, 19/09/2026) et de la fiche
`.planning/todos/2026-09-20-echo-photographic-reflexes-ergonomie.md`, dont la
section « à instruire » est remplacée par la conclusion ci-dessous.

Branche `mode-manuel`. Aucun déploiement.

**Révisé après la ronde de relecture 1** (21/09/2026). Le diagnostic et le
mécanisme sont confirmés ; trois manques ont été comblés — une **preuve** pour
la seconde correction, qui n'en avait qu'un argument (§2a) ; **deux témoins**
pour les rafraîchissements de main, que la substitution en bloc ne distinguait
pas (§5) ; et les **quatre gabarits** `PROCESSUS-CARTE` (§6 bis), dont trois
concluent « NON ». Les points mineurs sont au §6 ter, les inquiétudes révisées
au §7.

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

**Et c'est pire que ça** (relevé à la relecture du 21/09, vérifié ligne à
ligne) : en sortant, `CanPlayBy` fait `can_state.is_like_in_hand = None`
**sans avoir sauvegardé la valeur précédente**. Il n'écrase donc pas seulement
la question, il **efface la réponse mémorisée**. C'est un instrument qui
modifie l'état qu'il prétend observer : après un appel, un `False` mémoïsé a
disparu, et la mesure suivante — par n'importe quel chemin — ne verra plus le
défaut. Une sonde bâtie sur `CanPlayBy` peut donc *guérir* la position qu'elle
examine.

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
| « **Reduce the cost to play that event by 2** » | **CORRIGÉ** (c'était une génération de ressources) | `la reduction de 2 NE COUVRE PAS l'exigence de couleur` (`28013` No Quarter) — **le seul discriminant** ; `chemin B ... coute 2 de moins` ne l'est pas, voir §2a |
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

#### Et maintenant, la preuve — parce que le raisonnement ci-dessus n'en était pas une

⚠ **Aveu de méthode.** Tel qu'écrit le 21/09 au matin, tout ce qui précède
était un **argument**, pas une mesure. Et mes deux témoins de la réduction
étaient des cas ordinaires — Haymaker à 2, main vide — que **l'ancienne
implémentation passait tout aussi bien**. C'est exactement le mode de
défaillance que ce chantier venait de corriger, reproduit sur sa seconde
moitié.

Le témoin discriminant : **`28013` No Quarter**, événement d'aspect à coût 2
portant `Requirement: R` (physique). Après réduction de 2, il ne reste que
l'exigence de couleur — qu'une **réduction** ne paie pas, et que deux **wild**
payaient. On le glisse sous Echo, on ne laisse en main que du mental
(`01089` Genius, `BB`), et on **lit** ce que le moteur accepte :

| implémentation | ce que le moteur fait | dégâts sur Rhino |
| --- | --- | --- |
| `WhenCalculateEffectCost` + `UpdateCost(-2)` (retenue) | **refuse** le rejeu, No Quarter reste glissé | 4 (ceux du premier jeu) |
| `CanGenerateResources(Resources('GG'))` (l'ancienne) | **accepte**, les deux wild couvrent l'exigence `R` | **8** |

Le témoin `la reduction de 2 NE COUVRE PAS l'exigence de couleur` est donc
**rouge sous l'ancienne implémentation, vert sous la nouvelle**. Substitution
faite non pas en retirant l'aptitude, mais en **remettant le code d'avant** :
c'est la seule qui prouve « l'aide est une réduction », et non « il y a de
l'aide ».

**Un second écart, non anticipé, est tombé de la même mesure.** Sous l'ancienne
implémentation, le cas `chemin A` rougit aussi (3 dégâts au lieu de 6) :
`check_pay_for_tucked` exigeait une Photographic Reflexes **en main** au moment
du paiement, or le chemin A l'a déjà défaussée comme coût. La génération de wild
**ne pouvait pas financer le chemin A**. La réduction portée par la zone, elle,
le finance.

Et les deux témoins « ordinaires » (chemin B à 6 dégâts, paiement avec une
Photographic Reflexes) sont restés **verts** sous l'ancienne implémentation :
confirmation mesurée qu'ils ne discriminaient rien.

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

**Conséquence non anticipée, relevée à la relecture, et tranchée.** Les deux
chemins **divergent quand le rejeu n'aboutit pas**. Sur A, `CostFunc.Discard`
défausse Photographic Reflexes **avant** `PlayOneCardLikeInTurn`, qui laisse
renoncer (`forced=False`) : la carte cliquée est perdue et rien n'est joué. Sur
B, elle ne part qu'une fois le jeu effectif.

**Arbitrage retenu : on garde ce comportement**, et on l'écrit. Un coût payé ne
se reprend pas, c'est le sens même de `SetCostFunc`, et « discard ... **to**
play » désigne bien un coût. Forcer l'aboutissement serait d'ailleurs
impossible à tenir : un événement glissé qu'on ne peut pas payer ne peut pas
être joué de force. L'arbitrage est **inscrit dans le module**
(`fne/echo/__init__.py`), dans la fiche, et ici — il n'est **pas testé**, faute
de pouvoir faire renoncer le pilote du harnais.

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

**17 cas ajoutés** dans `tools/test_capacites.py` (14 le matin, **3 de plus
après relecture**, signalés ⭐ ci-dessous) :

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
| ⭐ `60040a ... la reduction de 2 NE COUVRE PAS l'exigence de couleur` | **le seul qui distingue une réduction de deux wild** (§2a) |
| ⭐ `60037a Echo — ... quand une Photographic Reflexes ARRIVE en main` | le crochet `AfterCardEnterHand` |
| ⭐ `60037a Echo — ... quand la Photographic Reflexes QUITTE la main` | le crochet `WhenCardWouldMoveToArea` |
| `60040a ... aucune carte glissee : la carte n'offre AUCUNE action` | pas de défausse pour rien |
| `60040a ... forme CIVILE : la carte n'offre AUCUNE action` | « If you are in hero form » sur le chemin A |
| `60040a ... forme HEROS avec un evenement glisse : l'action EST offerte` | le bout positif des deux précédents |

### Le harnais a gagné trois clés, toutes additives

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

- `jouer_glissee_tolerant: [card_id]` — **le refus est le résultat attendu**.
  Même raison d'être que `declencher_tolerant` : sans elle, le seul témoin qui
  distingue une réduction d'une génération de wild n'est pas montable, puisqu'il
  repose précisément sur un jeu que le moteur doit refuser.

Les deux premières tournent **après** `declencher_apres`, volontairement : c'est
le seul moyen de changer la main entre la mise sous Echo et le rejeu, sans quoi
le témoin du §4 n'était pas montable.

### Preuve par substitution (étape 7.3 de PROCESSUS-CARTE)

| substitution | résultat |
| --- | --- |
| les 3 rafraîchissements retirés **en bloc** | **2 rouges** : `forme CIVILE` et `retour en forme HEROS`. ⚠ Cette substitution-là ne dit **pas lequel** des trois crochets mord : c'est pour ça que les trois suivantes existent. |
| **`AfterUnitChangeForm` seul** — couvert par `forme CIVILE` et `retour en forme HEROS` | (les deux rouges de la ligne précédente) |
| **`AfterCardEnterHand` seul** ⭐ | **1 rouge, et le bon** : `ARRIVE en main` (« la réponse *non* est figée »). `QUITTE la main` reste **vert**. |
| **`WhenCardWouldMoveToArea` seul** ⭐ | **1 rouge, et le bon** : `QUITTE la main` (« la réponse *oui* est figée »). `ARRIVE en main` reste **vert**. |
| **l'ancienne implémentation de la réduction remise** (`CanGenerateResources(Resources('GG'))`) ⭐ | **2 rouges** : `NE COUVRE PAS l'exigence de couleur` (8 dégâts au lieu de 4) et `chemin A` (3 au lieu de 6). Les deux témoins « ordinaires » restent verts — c'est la démonstration qu'ils ne prouvaient rien. |
| la réduction de coût retirée entièrement | **2 rouges** : chemins A et B. Prouve « il y a de l'aide au paiement », **pas** « l'aide est une réduction » : d'où la ligne précédente. |
| le module des trois variantes vidé (`return []`) | **3 rouges** : chemin A, trois variantes, et « l'action EST offerte ». |
| le drapeau `REFLEXES_DEJA_PAYEES` absent (état mesuré avant correctif) | main `['60040c']` au lieu de `['60040a', '60040c']` |

Les deux substitutions ⭐ de crochet sont **croisées** : chaque crochet a son
témoin, et chaque témoin ne mord que sur son crochet.

⚠ **Le témoin `60040a ... forme CIVILE : la carte n'offre AUCUNE action` ne
discrimine pas la clause de forme.** En forme civile, `EchoDeCeJoueur` rend déjà
`None` — l'identité visible est Maya Lopez, pas Echo — donc la condition
`il_y_a_un_evenement_glisse` échoue avant même que `AbilityType.HeroAction` ait
son mot à dire. Le cas **passerait sans la clause de forme**. Il reste utile
comme témoin de non-régression du comportement observable, il n'est pas une
preuve de la clause. Dit ici plutôt que maquillé.

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

⚠ La ronde de relecture a touché un fichier **moteur**
(`src/game/player/element/player_flag.py`, pour y déclarer le drapeau) : la
batterie a donc été **rejouée en entier**. C'est ce second chiffre qui fait foi.

`tools/test_capacites.py` **EN ENTIER**, `PARALLELES=12`, sur un dossier de jeu
jetable (`.game-src-echo2`, supprimé après la passe ; ni `.game`, ni
`.game-src`, ni aucun dossier d'une autre session n'a été touché) :

**2363 / 2368 cas passés.**

Les cinq rouges, **rejoués et comparés par leur NOM** (l'arbre est partagé, le
nombre de cas bouge : 2365 le matin, 2368 après les trois témoins ajoutés) :

| cas | rejoué seul | verdict |
| --- | --- | --- |
| `ls004` Lead The Charge | **vert** (filtre `"ls004 Lead The Charge"`, séquentiel) | **artefact de passe parallèle** : le journal montre un `AttributeError: type object 'Engine' has no attribute 'game'` dans `Engine.Initialize`, c'est-à-dire un plantage **avant** le début de la partie |
| `sg009` Squirrel Girl's Costume | — | **antérieur** |
| `sg013` Call the Squirrels | — | **antérieur** |
| `sg007` The Gatherer | — | **antérieur** |
| `sg006` The Forager | — | **antérieur** |

Les quatre `sg00x` sont **nommément** les mêmes que ceux relevés par les
rapports du 20/09 (`2026-09-20-spdr-paiement-incomplet.md`) et du 21/09
(`2026-09-21-cartes-coincees-en-resolution.md`), où ils ont été établis
antérieurs **par mesure** sur un moteur de référence. Ils vivent dans
`pack/squirrel_girl`, sans aucun rapport avec `fne/echo` ; et les trois clés
ajoutées au harnais sont strictement additives.

⚠ **Correction de méthode de la ronde 1.** La passe du matin avait rejoué
`ls004` par `CAS_INDEX=1050`, un **index**, sur un arbre où ce rapport rappelle
lui-même deux fois que le nombre de cas bouge. L'index était le mauvais outil ;
le **filtre par nom** est celui utilisé ici, et pour toutes les passes de la
ronde.

**Les 17 témoins d'Echo sont verts dans la passe complète**, comptés un par un.

**Réserve de méthode.** La passe retenue est une passe parallèle : le seul
rouge suspect a été rejoué en séquentiel, pas les 2363 verts.

## 6 bis. Les gabarits PROCESSUS-CARTE, et ce qu'ils disent

`.planning/todos/2026-09-21-echo-gabarits-processus-carte.md` porte les quatre
gabarits des cartes touchées : `60037a`, `60040a`, `60040b`, `60040c`.

**Et ils ne concluent pas tous « OUI ».**

| carte | terminée | ce qui manque |
| --- | --- | --- |
| `60037a` Echo | **OUI**, sous réserve | l'étape 8 (autoplay), et un écart de timing assumé sur `IsInProcessingArea` |
| `60040a` | **NON** | l'étape 8 bis : rien ne prouve que le nouveau bouton soit visible |
| `60040b` | **NON** | idem |
| `60040c` | **NON** | idem, plus : aucun cas ne clique `60040c` elle-même |

C'est la gate du `CLAUDE.md` du projet, et elle dit « non » sur trois cartes
sur quatre. Le moteur est juste et mesuré ; l'écran ne l'est pas.

## 6 ter. Points mineurs relevés à la relecture, et corrigés

- **`REFLEXES_DEJA_PAYEES` n'était pas déclaré dans `PlayerFlag.FLAG`** alors
  que je revendiquais l'idiome de `MAGIK_ONCE_PER_PHASE`. Il l'est maintenant
  (`src/game/player/element/player_flag.py`), au même endroit et de la même
  façon. C'est un fichier **moteur**, d'où la batterie complète rejouée.
- **`check_cout_d_une_glissee` avait perdu le contrôle du payeur**, que
  l'ancienne `check_pay_for_tucked` faisait (`message.GetToPlayer()`). Restauré
  et commenté : sans lui, un **autre** joueur qui aide à payer (cartes
  `Alliance`, « the players can pay this card's costs as a group ») aurait reçu
  la réduction d'Echo. Je ne l'avais pas dit — c'est réparé et dit.
- **Le choix d'`AbilityType.Rule` porte le sens**, et rien ne le disait. Un
  commentaire l'explique maintenant : `Rule` pose `is_ignore_game_area`, donc
  `is_ignore_out_of_play` ; avec `NonKeyword`, une aptitude portée par la face
  **héros** cesserait d'écouter dès que cette face part dans `aside_deck` —
  c'est-à-dire **pile au moment de la bascule vers la forme civile**. Le
  rafraîchissement n'aurait marché que dans un sens, en silence.
- **La portée du drapeau** (toute la résolution, pas seulement la carte jouée)
  est commentée : sans effet observable, `discard_photographic_reflexes` ne
  partant que sur une carte jouée depuis la zone glissée, et le chemin A n'en
  jouant qu'une.

## 7. Mes inquiétudes

*Révisées après la première ronde de relecture. L'inquiétude n°4 de la version
du matin (« le drapeau pourrait rester posé ») est **retirée** : elle était
surévaluée, le `try/finally` couvre par construction les exceptions que je ne
connais pas.*

1. **Le chemin A n'a pas été vu à l'écran, et c'est le vrai trou.**
   `test_capacites` prouve que le moteur offre l'action (`60040a action=True`) ;
   il ne prouve **rien** sur le bouton. Une action portée par une carte **de la
   main** est une forme que `ui-app` n'a jamais eu à rendre pour Echo. L'étape
   8 bis de `PROCESSUS-CARTE` n'est pas faite, et elle existe précisément pour
   ce cas : un pack peut être vert 32 fois sur 32 et injouable à l'œil.
   **À vérifier avant de répondre au joueur.**

2. **Le cache `is_like_in_hand` reste un piège de moteur, et je l'ai contourné,
   pas refermé.** Il sert **deux** rôles : mémo de la réponse, et **drapeau
   forcé** que `has_cost.CanPlayBy`, `player_action.py` et `PlayCardsLikeInTurn`
   posent à `True` pour jouer une carte hors de la main. On ne peut donc pas
   supprimer la mémoïsation sans casser tous les « play like in hand » du dépôt.
   Séparer les deux rôles est un chantier moteur à ouvrir sciemment.
   **La troisième carte de la famille est identifiée** :
   `fne/daredevil/60001a.py` (Sense the Top). Un grep sur
   `CheckIfFaceIsLikeInHand` ne rend que trois cartes posant une condition
   **variable** — Magik (contournée depuis longtemps), Echo (corrigée), et
   elle. Sa condition est `message.which_face == initiator.additional_deck.GetTop()` :
   quand la carte du dessus part, **la suivante devient le dessus sans bouger**,
   donc avec un `False` figé, donc jamais jouable. Même famille, même remède.
   **Non mesuré**, inscrit au backlog avec cette analyse.

3. **Un défaut ANTÉRIEUR d'Echo n'est pas corrigé** : avec **une seule**
   Photographic Reflexes en main, le joueur peut la dépenser comme
   **ressource** pour payer la carte glissée qu'elle vient d'autoriser. La
   permission est lue avant le paiement ; à l'heure de la défausse, il n'y a
   plus rien. Il obtient l'événement **et** le bénéfice de la ressource. Mon
   nouveau témoin met délibérément **deux** copies en main et passe donc à côté.
   Nommé dans la fiche et au backlog.

4. **Pas d'autoplay ciblé** (étape 8). Le deck d'Echo n'a pas été passé à
   `tools/autoplay.py` : la batterie complète et les sept substitutions ont pris
   l'essentiel du temps machine.

5. **Le multijoueur n'est pas couvert.** « After **a player** plays an aspect or
   basic event » fait glisser sous Echo l'événement d'un **autre** joueur : tous
   les témoins sont en solo (`heros2` non utilisé). Le contrôle du payeur
   restauré dans `check_cout_d_une_glissee` vise justement ce terrain (les
   cartes `Alliance`) et n'y est pas mesuré non plus.

6. **Une bévue d'outillage, pour mémoire.** J'ai rejoué `ls004` par
   `CAS_INDEX=1050`, un **index**, sur un arbre où je rappelle moi-même deux
   fois que le nombre de cas bouge. Le filtre par **nom** était le bon outil, et
   c'est celui que j'ai utilisé pour toutes les passes de cette ronde.
