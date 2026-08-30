# Pack Patriot — fiches PROCESSUS-CARTE.md, une par card_id

Gabarit suivi : `PROCESSUS-HEROS.md` / `PROCESSUS-CARTE.md`. **23 card_id** au
total (`pt001a` à `pt022`, les faces `a`/`b` de Patriot comptant pour deux
identifiants distincts). Source : pack fan-made **CptScorp** (« Marvel Champions
Custom Project », Cycle 2) — même auteur qu'`iron_lad`, `scarlet_spider`,
`wiccan` et `speed`. 2 faces héros, 15 cartes signature, 1 obligation et
5 cartes némésis. **Set 131, préfixe `pt`.** Personnage : Elijah Bradley, le
meneur des Young Avengers, petit-fils d'Isaiah Bradley.

Les étapes 1 et 3-6 de PROCESSUS-HEROS (cards.json, deck de départ,
`data/nemesis/patriot_nemesis.json`, `data/sets_info.json`, préfixe déclaré,
23 images) ont été faites lors d'une session antérieure, **avec vérification
des 15 icônes de ressource et des 6 valeurs de bonus par découpe d'image**
(recette reproductible : `tools/importer_images_patriot.py`, `assets/pics/`
étant gitignoré). **Aucun trait ni compteur nouveau** : les 10 traits du pack
(DEFENSE, PERSONA, TACTIC, ITEM, TITLE, WEAPON, ELITE, YOUNG AVENGER, CIVILIAN,
AVENGER) étaient déjà dans l'énum — contrairement à `speed`, `card_face.py`
n'a **pas** été touché.

Cette session a couvert l'**étape 2** (les 23 scripts) et les **étapes 7 à 10**
(biographie, texte FR, règle de deck-building, validation carte par carte,
autoplay, gate finale).

---

## Le pack en une phrase : tout parle d'alliés

**12 des 17 cartes joueur dépendent d'un allié en jeu.** `pt001a` encaisse à
leur place, `pt002` leur donne +1 PV, `pt003`/`pt004` les épuisent,
`pt005`/`pt006` les désignent, `pt009` et `pt010` les servent, `pt011` les
redresse ou les soigne, `pt014` les remplace, et `pt013`/`pt015`/`pt016`
s'attachent à eux. **Sans allié en jeu, la moitié du pack est injouable : c'est
voulu, ce n'est pas un défaut à corriger.** C'est aussi la raison pour laquelle
l'utilisateur a tranché l'aspect **LEADERSHIP** le 30/08/2026, avec 4 alliés
d'aspect en plus des 2 signature (voir `metadata.aspect_note` du deck).

## La règle de la flèche, appliquée à sept cartes

`→` sépare un **COÛT** (à gauche) d'un **EFFET** (à droite), et la capacité ne
se déclenche **que si le coût est intégralement payable**. Règle officielle,
tranchée par l'utilisateur le 30/08/2026 après une erreur sur `sd021`. Elle vaut
**aussi pour une capacité FORCÉE** (`11014` Temporal Shield, `11031` Chitauri
Soldier, `16074` Biogram Image) ; quand une carte veut deux **conséquences**,
elle les relie par « and » **sans** flèche (`02021` Pumpkin Bombs).

| Carte | Coût (gauche de la flèche) | Rendu par |
|---|---|---|
| `pt001b` | incliner Elijah Bradley | `CostFunc.Exhaust("This")` |
| `pt003`/`pt004` | épuiser un allié que tu contrôles | `CostFunc.Exhaust("YourAlly")` |
| `pt005`/`pt006` | choisir un allié que tu contrôles | `.SetTarget("YourAlly", range=(1,1))` |
| `pt007` | incliner Isaiah Bradley | `CostFunc.Exhaust("This")` |
| `pt008` | incliner **et** défausser Commandeer, choisir un allié | deux `SetCostFunc` empilés + `.SetTarget(Ally)` |
| `pt009` | incliner Commander's Orders | `CostFunc.Exhaust("This")` |
| `pt010` | incliner Follow My Lead | `CostFunc.Exhaust("This")` |
| `pt011` | incliner On Your Feet | `CostFunc.Exhaust("This")` |
| `pt013` | défausser Revenge | `CostFunc.Discard("This")` |
| `pt015` | défausser Throwing Stars | `CostFunc.Discard("This")` |
| `pt016` | choisir un autre personnage ami **et** défausser Working Together | `.SetTarget(...)` + `CostFunc.Discard("This")` |
| `pt017` | défausser la carte de soutien Isaiah Bradley | `condition=` sur la `ForChoiceAbility` |
| `pt020` | dépenser [mental][energy] | `.SetCost(Cost("YB"))` |

Le point commun : **le coût est toujours porté par la capacité elle-même**, pas
recodé à la main dans le corps. Le moteur ne propose alors pas la capacité quand
le coût n'a aucune cible légale (`CostFunc.Base.HasTargets`, `cost_func.py:47`).
C'est la seule construction qui rende « coût impayable = rien ne se passe » sans
l'écrire.

Deux exceptions documentées :

- `pt017` branche 1 : la défausse d'un **soutien nommé** ne se dit pas avec un
  `CostFunc` sur une `ForChoiceAbility` sans en changer la cible ; la branche
  porte une `condition=` qui la rend **indisponible** sans `pt007` en jeu, et le
  corps re-vérifie avant d'agir. Idiome de `09027` Physical Toll et `cd014`.
- `pt013` : le coût est bien un `CostFunc.Discard`, mais l'allié porteur ne peut
  **plus** être lu par `GetBindFace()` une fois la carte défaussée (voir le bug
  n°2 plus bas).

## Arbitrages tranchés par l'utilisateur (documentés, non rediscutés)

1. **La flèche est un coût** (30/08/2026), y compris dans une capacité forcée.
   Appliquée aux 13 lignes du tableau ci-dessus.
2. **`pt014`, texte contradictoire** : « **Forced Response**: **When** an ally
   you control is used to defend… ». Forced Response résout **APRÈS**, « When »
   annonce un AVANT. **Le mot-clé en gras fait foi, « When » n'est que de
   l'anglais relâché** — donc `AbilityFactory.AfterUnitBecomeDefender`. Même cas
   que The Made Men, cité en exemple au §3 de PROCESSUS-CARTE.
3. **Aspect LEADERSHIP** pour le deck de départ, 4 alliés d'aspect en plus des
   2 signature, `29016` Patriot (l'allié officiel homonyme) explicitement exclu.
4. **`pt018` porte `Crisis`, et rien d'autre.** L'icône a été vérifiée **par
   découpe d'image** contre la carte-témoin `ag011` (dont le `desc` déclare
   `Crisis` **et** `Acceleration`), avec `hd022` (Hazard) et `hd026`
   (Acceleration) en contrôles : c'est bien un **burst noir avec « ! »**. Point
   clos, à ne pas rouvrir.

5. **`pt015` — « This attack gains piercing and ranged » porte sur l'attaque de
   l'ALLIÉ**, tranché par l'utilisateur le 30/08/2026. C'est la lecture A
   ci-dessous, celle qui était déjà appliquée : **aucune ligne de code n'a
   changé**. Détail du raisonnement juste en dessous.

## L'arbitrage `pt015`, tranché le 30/08/2026 (était la seule question ouverte)

**`pt015` Throwing Stars — « This attack gains piercing and ranged » porte sur
quoi ?**

> « **Interrupt** *(attack)*: When the attached ally attacks, discard Throwing
> Stars → deal 3 damage divided as you choose. This attack gains piercing and
> ranged. »

- **A (retenu, RAW)** : « this attack » = **l'attaque de l'allié**, la seule
  attaque de la phrase. Les 3 dégâts répartis ne sont pas une attaque et ne
  peuvent donc pas « gagner » un mot-clé d'attaque. *En jeu* : l'attaque de
  l'allié (ATQ 1 chez Mockingbird) ignore Robuste et la riposte ; les 3 dégâts
  répartis sont des dégâts nus.
- **B** : les **3 dégâts** sont perçants et à distance. *En jeu* : les 3 dégâts
  ignoreraient les jetons Robuste, ce qui est nettement plus fort.

**A est appliqué**, et **l'utilisateur l'a confirmé le 30/08/2026** : c'est la
lecture littérale **et** la moins permissive des deux (règle « écart plus
sévère, jamais plus permissif »). B aurait tenu en une ligne
(`property=AttackProperty(piercing=True, ranged=True)` au `DealDamage`) ; elle
n'a pas été retenue. **Plus aucune question n'est ouverte sur ce pack.**

⚠ Rappel indépendant de cet arbitrage : **`ranged` ignore la RIPOSTE, pas le
Garde**. `can_retaliate.py:38` est le seul lecteur d'`IsRanged()` dans tout le
moteur.

## Écarts assumés, non corrigés

| Sujet | Écart | Pourquoi, et pourquoi il n'est jamais plus permissif |
|---|---|---|
| `pt015`, libellé `(attack)` | **le libellé n'est pas posé** | `Ability.Initialize` (`ability.py:196`) n'autorise que `['defense','thwart']` sur un `AbilityType.Interrupt` ; `.SetLabel('attack')` fait **planter le setup** (trouvé par `verifier_tous_les_decks.py`). Passer en `HeroInterrupt` aurait accepté le libellé mais changé la **règle** (forme héros exigée), ce que le texte ne dit pas. Un libellé ne sert qu'à classer une capacité **de jeu** d'une carte jouée depuis la main ; celle-ci est une interruption d'une amélioration déjà en jeu. **Aucun effet en jeu.** |
| `pt010`, « upgrade attachable à un allié » | testé contre les **alliés réellement en jeu** | `Upgrade.CanAttachTo(face)` (`upgrade.py:83`) exige une **face concrète** : le moteur ne sait pas répondre « attachable à un allié » dans l'abstrait. Modèle : `45017` Suit Up, la seule carte du dépôt qui pose déjà cette question. **Sans allié en jeu, la ressource ne peut plus payer qu'un ALLIÉ** — donc plus sévère, jamais plus permissif (et de toute façon Revenge est injouable à ce moment-là). |
| `pt008`, disponibilité | la Hero Action **n'est pas proposée** s'il n'y a aucun attachement sur un ennemi | à la lettre le coût serait payable et le joueur brûlerait sa carte pour rien. Ne pas proposer l'action est le comportement habituel du moteur pour une capacité sans cible légale : **plus sévère**, jamais plus permissif. |
| `pt008`, retour de l'attachement | si l'ennemi d'origine est **mort** à la fin du round, l'attachement est **défaussé** | le texte exige qu'il quitte l'allié à la fin du round et il n'a plus de porteur légitime. Le laisser sur l'allié serait un cadeau au vilain au-delà du round. Choix technique, documenté. |
| `pt001b`, règle « Leader » | implémentée **sans cible légale aujourd'hui** | les deux seuls alliés YOUNG AVENGER du catalogue (`il002` Stature, `wc002` Hulkling) sont de classe `Hero`, donc signatures d'autres héros, interdites de deck (PROCESSUS-HEROS §10). La règle vit dans `public/js/deckbuilder/app.js` (`exemptDeLaLimiteAspect`) et ne mordra qu'à l'arrivée d'un allié YOUNG AVENGER d'aspect. **On n'invente pas de cible.** |
| `hood` / « Mister Hyde » | **rien n'est corrigé côté `hood`** | `24035` s'appelle « **Mister** Hyde », `pt019` « **Mr.** Hyde » : chaînes différentes, aucune collision moteur. Même personnage Marvel, deux cartes distinctes. |
| `29016` / `56041` « Patriot » | **exclus du deck**, aucune recherche par nom | deux alliés officiels portent déjà le nom du héros. Aucune carte du pack ne fait de `CardFinder(name="Patriot")` : `pt013` vise `"YourHero"`, `pt001a`/`pt012` visent `"This"`/`"YourIdentity"`. |

### Un défaut latent trouvé à la relecture, et corrigé (30/08/2026)

La règle « Leader » testait le héros par un `/patriot/i` **non ancré**, calqué
sur le `/madame web/i` voisin. Le dossier `A créer/` contient un pack
**« Iron Patriot »** (dans `OneDrive_2026-08-29.zip`) qui n'est pas encore
porté : le jour de son arrivée, il aurait hérité **silencieusement** de la règle
de deck-building d'Elijah Bradley, et aurait pu embarquer des alliés
`YOUNG AVENGER` hors aspect sans que rien ne le signale. Le test est désormais
**ancré** : `/^\*?\s*patriot$/i` sur le nom détouré. Vérifié : `« * Patriot »`
et `« Patriot »` passent, `« Iron Patriot »`, `« * Iron Patriot »` et
`« Patriotic »` sont rejetés ; `node --check public/js/deckbuilder/app.js`
propre. L'étoile d'unicité est tolérée parce que `cards/paper.py` la retire côté
moteur, mais pas partout côté client.

## Outils exécutés depuis `.game-src`

| Outil | Résultat |
|---|---|
| `python3.10 -m compileall -q src` | **propre** |
| `tools/test_cards.py` (port 24521) | **4684 ok / 0 err** (4661 avant le pack), 0 `failures` |
| `tools/verifier_prefixes.py` | **OK** — 5239 cartes, 29 préfixes, 905 fan-made, aucun doublon |
| `tools/verifier_desc_mots_cles.py patriot` | **OK** — « les 23 cartes de patriot ont un desc conforme à leur texte » |
| `tools/verifier_coherence_cartes.py` | **0** carte joueur sans classe, **0** obligation sans destinataire, **0** image manquante. Seul avertissement : `dt134` (antérieur au pack) |
| `tools/verifier_noms_modules.py … patriot` | **OK** — aucun nom inconnu |
| `tools/verifier_cartes_en_jeu.py … patriot` | **OK** — « les 23 cartes de patriot portent ce que leur texte annonce » |
| `tools/verifier_api_cartes.py` (port 26050) | 5231 fichiers, **4 en faute — aucune dans `patriot`** (`sp018`, `underling/__init__`, `wd159`, `wd160`, tous antérieurs) |
| `DECK_NOM=patriot tools/verifier_tous_les_decks.py` | **`ok: true`** — « identite pt001b, main 6, deck 34 » |
| Script anti-fuite de PROCESSUS-HEROS §10 | **0 résultat** |
| `tools/test_capacites.py`, 30 cas `pt*` | **30/30** (indices 630 à 659) |
| `tools/autoplay.py --deck patriot --vilains rhino --profils equilibre --parties 8` | **0 partie bloquée**, 0 traceback |
| `launch.json` de `$W` après campagne | `['127.0.0.1:2345']` ✔ |

### Preuve par substitution, module par module

Chaque module retiré, les cas dont le **nom** commence par son `card_id` sont
relancés et doivent tous être **ROUGES** ; le module est ensuite remis.

| Module | Cas concernés | Résultat sans le module |
|---|---|---|
| `pt001a` | 630, 631 | ROUGE |
| `pt001b` | 632 | ROUGE |
| `pt002` | 633, 634 | ROUGE |
| `pt003` | 635 | ROUGE |
| `pt005` | 636 | ROUGE |
| `pt007` | 637 | ROUGE |
| `pt008` | 638 | ROUGE |
| `pt009` | 639 | ROUGE |
| `pt010` | 640, **641** | 640 ROUGE ; **641 reste VERT — c'est une contre-épreuve** |
| `pt011` | 642, 643 | ROUGE |
| `pt012` | 644, 645 | ROUGE |
| `pt013` | 646 | ROUGE |
| `pt014` | 647, 648 | ROUGE |
| `pt015` | 649 | ROUGE |
| `pt016` | 650 | ROUGE |
| `pt017` | 651, 652 | ROUGE |
| `pt018` | 653 | ROUGE |
| `pt019` | 654 | ROUGE |
| `pt020` | 655, 656 | ROUGE |
| `pt021` | 657, 658, 659 | ROUGE |

`pt004`, `pt006` et `pt022` n'ont pas de cas dédié : ce sont des **doublons de
code** de `pt003`, `pt005` et `pt021`, comptés comme tels par
`verifier_coherence_cartes.py` (même convention que `sd004`/`sd007`/`wc006`).

**Le seul vert légitime : le cas 641** (« pt010 Follow My Lead — contre-épreuve :
elle NE finance PAS une amélioration d'identité »). Il affirme que **rien** ne se
passe ; sans le module il n'y a pas non plus de ressource, donc pt012 reste hors
jeu de toute façon. Son **jumeau positif est le cas 640**, qui est bien ROUGE
sans le module. Un vert isolé de ce type n'est pas une preuve ; le couple 640/641
en est une.

## Autoplay : 8 parties, témoin `okoye`, même fournée

| Deck | Parties | Victoires | Rounds moyens | **Bloquées** | Causes de fin |
|---|---|---|---|---|---|
| **patriot** | 8 | 0 | **5,2** | **0** | 8 × « The Main Scheme was Completed » |
| `okoye` (témoin) | 8 | 0 | 4,1 | **0** | 6 × complot principal, **2 × tous les joueurs éliminés** |

Le taux de blocage absolu ne veut rien dire (le pilote se coince aussi tout
seul) : c'est l'**écart au témoin** qui compte, et il est **nul sur le blocage**
et **favorable à Patriot** sur la survie (5,2 rounds contre 4,1, et **zéro**
élimination contre 2).

⚠ **Lecture de l'écart, honnêtement** : `01093` Tenacity, seul bloqueur
d'autoplay officiel connu du projet, est **dans le deck d'okoye et pas dans
celui de Patriot** (`metadata.tenacity_note`). L'écart joue donc en faveur du
héros custom et doit être lu comme tel — ce n'est pas Patriot qui est plus
robuste, c'est son deck qui est débarrassé du piège. Cela dit, **aucune des
8 parties d'okoye n'a été bloquée non plus** : le piège ne s'est pas déclenché
cette fois, et la comparaison reste donc exploitable.

Grep exhaustif sur les **16 journaux** :

```
NameError|AttributeError|TypeError|KeyError|AssertionError  ->  0 partout
traceback|exception (insensible a la casse)                 ->  0 partout
```

**Couverture des `card_id` en partie réelle : 23/23.** Chaque carte du pack a
été vue en jeu au moins une fois hors du dump de deck (`pt001a` 8/8, `pt012` 8/8,
`pt017` 8/8, `pt010` 7/8, `pt013` 7/8, `pt008`/`pt011`/`pt016` 6/8,
`pt007`/`pt009`/`pt015` 5/8, `pt002`/`pt003`/`pt004`/`pt005`/`pt006`/`pt014`
3/8, tout le set némésis 1/8).

### Lecture ligne à ligne — le cycle allié → dégât consécutif → Will to Protect

`/tmp/autoplay_patriot_rhino_normal_equilibre_2.log`, lignes 255 à 290 :

```
255: [Vision] va attaquer [[Rhino]] (+0)
257: [Vision] would deal 2 damage to [Rhino]
260: [Rhino] perd 2♡
261: [Patriot] activates, targets [[Patriot]]
262: "WhenAllyWouldTakeConsequentialDamage" est remplacé par [Patriot]   <- SetBeInstead
263: [Patriot] would deal 1 damage to [Patriot]
266: [Patriot] perd 1♡                                                   <- le dégât est ARRIVÉ
268: [[Hawkeye]] exhausted
275: [Hawkeye] would deal 1 damage to [Hawkeye]
278: [Hawkeye] perd 1♡                                                   <- limite déjà consommée
287: [Mockingbird] would deal 1 damage to [Mockingbird]
290: [Mockingbird] perd 1♡                                               <- idem
```

Les trois alliés attaquent dans le même round. Le **premier** voit son dégât
consécutif **partir** (ligne 262, le message est *remplacé*) et **arriver** sur
Patriot (ligne 266) : le dégât est **déplacé**, pas dupliqué — l'allié finit à
0 dégât. Les **deux suivants** encaissent le leur : `.LimitOncePerRound()` fait
son travail, en partie réelle, sans qu'aucun test ne l'ait mis en scène.

### Lecture ligne à ligne — le cycle allié → défense → Aided Defense

`/tmp/autoplay_patriot_rhino_normal_equilibre_3.log`, lignes 640 à 664 :

```
640: [Rhino] va attaquer [[Patriot]] (+0)
645: [[Patriot]] exhausted            <- defense de base, DEF 2
646: [Patriot] defend contre [Rhino]
647: [[pt004 Aided Defense]] were placed on table
648: [[Vision]] exhausted ([pt004 Aided Defense])   <- LE COUT DE LA FLECHE
649: Patriot would play [pt004 Aided Defense] with ()   <- cout 0
651: [pt004 Aided Defense] activates
655: [Shocker] would count boost icons (2)   <- Rhino ATQ 2 + 2 = 4
658: [Rhino] would deal 1 damage to [Patriot]
661: [Patriot] perd 1♡
```

4 dégâts − 2 (DEF du héros) − 1 (Vision, **1 PV restant**) = **1**. Le bonus
suit bien les **points de vie restants** et non les PV imprimés. Comme des
dégâts sont passés, Vision n'est **pas** redressé : la clause « if you take no
damage » est correctement conditionnelle.

## Bugs réels trouvés et corrigés (preuve rouge/vert)

### 1. `pt015` — `.SetLabel('attack')` faisait **planter le montage de la partie**

Trouvé par `tools/verifier_tous_les_decks.py` :

```
{"deck": "patriot", "ok": false,
 "message": "setup : AssertionError: label='attack' self=(Interrupt,attack)
             [pt015] WhenUnitWouldAttack this=[(21,pt015) Throwing Stars ?]"}
```

`Ability.Initialize` (`ability.py:196`) n'autorise que `['defense','thwart']`
comme libellés d'un `AbilityType.Interrupt`. Le scan imprime pourtant
« Interrupt *(attack)* ». Le libellé a été **retiré**, avec le raisonnement écrit
dans `pt015.py` (voir « Écarts assumés »). Après correction :
`{"deck": "patriot", "ok": true, "message": "identite pt001b, main 6, deck 34"}`.

⚠ **Ni `test_cards.py`, ni `verifier_api_cartes.py`, ni `verifier_noms_modules`
ne voyaient ce défaut** : la capacité se **construit** sans erreur, elle
n'explose qu'au **montage d'une partie**. `verifier_tous_les_decks.py` est le
seul niveau qui l'attrape — exactement ce pour quoi il existe.

### 2. `pt013` Revenge — une `AssertionError` **avalée** à chaque déclenchement

Trouvé par le cas `pt013` de `test_capacites.py` (rouge : « 01067.attack=1
(imprimé 1, attendu 3) »), diagnostic par lecture du journal du cas :

```
64: [pt013 Revenge] was discarded to Patriot's DiscardPile<1>
65: [pt013 Revenge] activates, targets [[pt013 Revenge]]
<F> File ".../cards/pack/patriot/patriot/pt013.py", line 89, in revenge
<F>     allie = this.GetBindFace()
<F> File ".../game/card/face/card_face.py", line 980, in GetBindFace
<F>     assert face
<F> AssertionError
```

**Cause** : le coût (`CostFunc.Discard("This")`) est payé **avant** que le corps
ne s'exécute (`Effect.ProcessSelfCost`, `effect.py:135`, appelé en tête de
`ResolveSelfInternal`). À ce moment-là Revenge est **déjà dans la défausse**,
elle n'a plus de porteur, et `GetBindFace()` lève un `assert` sec.

**Le moteur AVALE cette exception** (`effect_invoke.py:27-33` → `Log.OnCrash`) :
la partie continue, la carte est défaussée pour rien, et **aucun outil statique
ne le voit**. Seul un test qui JOUE la carte l'a trouvé.

**Correction** : l'allié porteur est lu dans `effect.targets` via la cible-chaîne
`"Attached"` — les **cibles** sont choisies avant le paiement et rangées dans
`effect.context.targets_internal`, elles survivent donc à la défausse.
Rouge sans le correctif, **VERT avec** (cas 646).

**Deux durcissements du même genre**, appliqués par prudence sur `pt016` et
`pt008` : `GetBindFace()` remplacé par `.bind_face`, qui rend `None` au lieu de
lever (`can_attach.py:114`, `card_face.py:972-980`).

### 3. Le harnais, pas les cartes : `01083` Mockingbird **étourdit Rhino** en entrant en jeu

Huit cas `pt*` étaient rouges pour une raison qui n'appartient à aucune carte du
pack. Mockingbird imprime « **Response**: After Mockingbird enters play, stun an
enemy » : le vilain arrive **étourdi**, son activation est annulée
(`"WhenEnemyWouldActivate" est remplacé par Stunned`) et **toute attaque de
Rhino déclenchée par le banc ne se produit jamais**. Le relevé montrait alors
« 0 dégât » partout, ce qui se lit exactement comme une capacité morte.

Morale du guide, vérifiée une fois de plus : **quand un cas reste rouge sans
explication, soupçonner le banc avant la carte.** Les cas qui ont besoin d'une
vraie attaque du vilain utilisent désormais `01067` Maria Hill (PV 2, ATQ 1*,
CTR 2*), dont la Response est inoffensive. Aucun code de carte n'a changé.

## Limites du harnais, explicites et non masquées

1. **La branche « surge » de `pt017`.** « If no allies were exhausted this way,
   this card gains surge » n'a **pas** de cas dédié : le surge d'une obligation
   distribue une carte de rencontre supplémentaire, et le harnais n'expose
   aucune clé pour observer cette distribution de façon déterministe
   (`ThisCardGainSurge` n'est lisible ni dans `etat_attendu`, ni via un
   compteur). Ce qui EST prouvé : la branche 2 s'exécute, épuise les alliés et
   défausse l'obligation (cas 652). Ce qui ne l'est pas : la bascule du surge
   quand il n'y a **aucun** allié à épuiser. Elle est correcte par lecture
   (`ThisCardGainSurge`, `cards/pack/__init__.py:100`, l'idiome employé par
   `il021`, `il022` et `22031`), **jamais observée**.
2. **`pt002` avec un allié YOUNG AVENGER d'aspect.** La règle « Leader » de
   `pt001b` n'a aucune cible légale aujourd'hui : impossible d'écrire un cas qui
   la fasse mordre. Elle est implémentée dans le deck-builder et lisible, pas
   testable.
3. **La biographie au survol** et **les tooltips français** : voir la gate
   finale.

---

# Fiches PROCESSUS-CARTE, une par card_id

### pt001a : * Patriot (face héros)

PV 11 / ATQ 1 / CTR 1 / DEF 2 / MNG 5, trait YOUNG AVENGER.

- [x] Étape 2 : carte de référence : **Will to Protect** → `dt009` Savior
      Complex (pack `determination`), qui imprime le même remplacement et
      s'écrit `Ability(<type>, Message.WhenAllyWouldTakeConsequentialDamage,
      [check_your_ally], operation)` puis `message.SetBeInstead(effect)` +
      `TakeDamage`. `60007` Elektra porte le même remplacement mais sur
      elle-même (`is_local=True`), ce qui ne convient pas : la capacité écoute
      **tous** les alliés du contrôleur.
      ⚠ `ChangeDealtToTarget` (piste initiale, `59008` Amadeus Cho) vit sur
      `Message.WhenUnitWouldTakeDamage` (`sender_damage.py:848`) et **n'existe
      pas** sur `WhenAllyWouldTakeConsequentialDamage` — vérifié avant d'écrire
      une ligne, comme l'exige le guide.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`consequential`** (seul `Message.WhenAllyWouldTakeConsequentialDamage`
      est écouté ; les dégâts d'attaque subis par un allié passent par
      `WhenUnitWouldTakeDamage` et ne déclenchent **rien**) ;
      **`you control`** (`ally.GetControlByPlayer() == this.GetControlByPlayer()`) ;
      **`move`** = leçon `instead`/The Spot : `SetBeInstead` fait **partir** le
      dégât de l'allié (`ally.py:52-53`), le `TakeDamage` le fait **arriver** sur
      Patriot — sans le premier, les deux encaisseraient ;
      **`Interrupt`** nu (pas `Hero Interrupt`) ; **`(Limit once per round.)`**
      → `.LimitOncePerRound()`.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : PV 11, ATQ 1, CTR 1, DEF 2, MNG 5
      (`desc` et scan identiques, lus nativement) ; **1** fois par round ;
      aucune valeur codée en dur dans le module (le montant déplacé est
      `message.will_take_damage`).
      Résultat : conforme.
- [x] Étape 7 : deux cas, preuve par substitution :
      - `pt001a … le degat CONSECUTIF de l'allie part sur Patriot` (630) :
        allié à **0** dégât **et** identité à **1**. Un seul des deux relevés ne
        prouverait pas le déplacement. Rouge sans module, vert avec.
      - `pt001a … LIMITE une fois par round (deux allies frappent)` (631) :
        vérificateur dédié `pt001a_limite_une_fois_par_round`, qui compte les
        totaux (l'ordre des deux alliés dépend du moteur). Rouge sans module,
        vert avec.
- [x] Étape 8 : autoplay ciblé : présente dans **8/8** parties ; journal de la
      partie 2 lu ligne à ligne (extrait ci-dessus) montrant le déplacement
      **et** la limite ; 0 traceback.

Carte terminée : OUI

### pt001b : * Elijah Bradley (face alter-ego)

PV 11 / REC 3 / MNG 6, trait CIVILIAN.

- [x] Étape 2 : cartes de référence : **« Action: » nu sur une face alter-ego**
      → `AbilityType.Action` + modèles Bruce Banner `10001b`, Tony Stark
      `01029b`, Sharon Carter `ag001b`, Remy LeBeau `37001b`, Billy Kaplan
      `wc001b` (`AlterEgoAction` désigne un autre type, réservé aux cartes
      JOUEUR). **Recherche + main** → `gp007` Gwen's Room, même couple
      `Search.PlayerCard(...)` + `player.GainCard(face, effect)`.
      **« Leader »** → aucune carte de référence : ce n'est pas une capacité de
      jeu (voir plus bas).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`During deck building`** → **règle de deck-building**, pas de capacité ;
      elle vit dans `public/js/deckbuilder/app.js`, fonction
      `exemptDeLaLimiteAspect` (§14.1 du guide), là où vit déjà *Arachnophilia*.
      **Ne rien coder ici** aurait été un « mot-clé cité mais pas imprimé » à
      l'envers ; coder une capacité de jeu aurait été une capacité fantôme.
      **`the Patriot's Shield`** → ⚠ `cards/paper.py:45-46` retire le préfixe
      `« * »` : le nom effectif est **`Patriot's Shield`**, sans étoile. Un
      `name="* Patriot's Shield"` n'aurait **jamais** rien trouvé, en silence.
      **`your deck and discard pile`** → les deux zones.
      **`Shuffle your deck`** → fait par la recherche elle-même
      (`search_internal.py:61-66`, `not_shuffle=False`) : aucune ligne à
      ajouter. La recherche n'est **pas** optionnelle (`may` reste faux) : le
      texte ne dit pas « you may search ».
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : PV 11, REC 3, MNG 6 (`desc`, natifs) ;
      aucune valeur numérique dans la capacité.
      Résultat : conforme.
- [x] Étape 7 : un cas, une capacité :
      `pt001b … le Patriot's Shield sort du deck et arrive en main` (632) :
      `en_main: ["pt012"]` **et** `exhausted: ["pt001b"]` (le coût de la
      flèche). Rouge sans module, vert avec. C'est aussi le test du piège de
      l'étoile : avec `"* Patriot's Shield"` le cas serait rouge.
      La règle « Leader » n'a pas de cas : voir « Limites du harnais » n°2.
- [x] Étape 8 : autoplay ciblé : présente dans **8/8** parties (c'est la face de
      départ) ; l'action est jouée dès le tour 1 de la partie 1 (« Elijah
      Bradley exhausted » puis « Patriot gains [Patriot's Shield] ») ;
      0 traceback.

Carte terminée : OUI

### pt002 : * Hawkingbird (allié signature)

Coût 3, PV 1, ATQ 0, CTR 1*, [physical], trait YOUNG AVENGER, sous-titre
« Kate Bishop ».

- [x] Étape 2 : cartes de référence : **+1 PV aux alliés** → `50075` Destroy
      Evidence, même fabrique `GiveKeywordToInPlayWhenApplyThis` (qui donne un
      mot-clé à **toutes** les cartes en jeu répondant à un filtre, à la
      différence de `GiveKeywordToAttached`, réservée à une carte **attachée**).
      **Response d'entrée en jeu** → `29024` Vivian, même
      `AfterCardEnterPlay(<Response>, "This", ...)`.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`Allies you control`** sans « other » → `not_include_this=False` (le
      défaut) : **elle-même comprise**. Ce n'est pas un détail — à 1 PV imprimé
      elle mourrait au premier dégât. `50075` passe au contraire
      `not_include_this=True` parce que son texte dit « each OTHER » : c'est le
      contre-exemple qui prouve que le paramètre est bien lu.
      **`you control`** → `control_by="You"`.
      **`you may search`** → `may=True`.
      **`an upgrade that can be attached to allies`** → le filtre n'est **pas**
      « une amélioration » : `CardFinder(card_type=Upgrade,
      canbe_attach_to=<un allié>)` appelle `Upgrade.CanAttachTo`
      (`upgrade.py:83`), qui relit le sélecteur « Play » de l'amélioration
      examinée. `pt012`, qui se pose sur l'identité, est donc **écartée**.
      **`deck and discard pile`** → les deux zones.
      **Sous-titre « Kate Bishop »**, partagé avec l'officielle `04011`
      Hawkeye : noms différents, aucune collision — et **on ne cherche jamais
      par sous-titre**.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût 3, PV 1, ATQ 0, CTR 1* (natifs) ;
      bonus de **+1** PV.
      Résultat : conforme.
- [x] Étape 7 : deux cas, un par capacité :
      - `pt002 … +1 PV a TOUS les allies, ELLE COMPRISE` (633) :
        `attributs_carte` sur **les deux** alliés. Un seul ne départagerait pas
        `not_include_this=True` de `False`. Rouge sans module, vert avec.
      - `pt002 … elle cherche une amelioration ATTACHABLE A UN ALLIE` (634) :
        deck truqué à `pt013` (s'attache à un allié) via
        `Puzzle.CreatePlayerDeck`, `accepter_choix: True` pour exercer le
        « you may ». Rouge sans module, vert avec.
- [x] Étape 8 : autoplay ciblé : jouée dans **3/8** parties ; 0 traceback.

Carte terminée : OUI

### pt003 : Aided Defense (exemplaire 1/2)

Coût 0, [energy], trait DEFENSE.

- [x] Étape 2 : cartes de référence : **déclencheur** → `09015` Desperate
      Defense et `58033` Disarming Defense, même
      `WhenUnitDefendAgainstAttack(<HeroInterrupt>, "YourHero", …).SetPlay()`
      + `.SetLabel('defense')`. **Coût « épuiser un allié »** → `03017` Strength
      In Numbers, **seule carte du dépôt** qui incline un allié comme coût d'un
      événement, et qui relit l'allié épuisé via
      `effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards`.
      **« if you take no damage »** → `message.IfYouTakeNoDamage(action)`
      (`sender_unit.py:153-176`), brique de `09015`, `48018`, `38016`, `58033`.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **flèche** → `CostFunc.Exhaust("YourAlly")` : sans allié prêt sous
      contrôle, `HasTargets` rend faux et **la carte n'est pas proposée** ;
      **`you control`** → cible-chaîne `"YourAlly"` ;
      **`remaining hit point`** → `face.health` (PV **courants**), pas
      `printed_health` — le +1 PV de `pt002` compte donc ;
      **`the exhausted ally`** (`that <nom>`) → l'allié est relu **sur le coût**,
      jamais redemandé au joueur ;
      **`If you take no damage from that attack`** → clause conditionnelle, pas
      inconditionnelle.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût **0** ; **+1** DEF **par** PV
      restant (aucune constante : `bonus = somme des health`).
      Résultat : conforme.
- [x] Étape 7 : un cas couvrant les trois moitiés :
      `pt003 … +1 DEF par PV RESTANT de l'allie epuise, puis il est redresse`
      (635) : Rhino ATQ 2 + 1 icône (`01106`) = 3 ; DEF 2 + 2 PV de Maria Hill
      = 4 → **0 dégât**, donc la clause « ready » part aussi. Le cas contrôle
      `degats_identite: 0`, `pret: ["01067"]` (redressé après avoir été épuisé
      comme coût) et `defausse: ["pt003"]` (la carte a bien été **jouée**).
      `Puzzle.Defend` ouvre la fenêtre, le pilote joue la carte depuis la main —
      montage de `sg016` Unbeatable!. Rouge sans module, vert avec.
- [x] Étape 8 : autoplay ciblé : jouée dans **3/8** parties ; journal de la
      partie 3 lu ligne à ligne (extrait ci-dessus, exemplaire `pt004`) ;
      0 traceback.

Carte terminée : OUI

### pt004 : Aided Defense (exemplaire 2/2)

Contenu **identique** à `pt003` (doublon de code, même convention que
`sd004`/`wc006`). Toutes les vérifications de `pt003` valent mot pour mot.
Aucun cas dédié : `verifier_coherence_cartes.py` la compte comme doublon de
code. **Vue en jeu dans 3/8 parties d'autoplay**, et c'est l'exemplaire dont le
journal est cité ligne à ligne plus haut.

Carte terminée : OUI

### pt005 : Covered Fire (exemplaire 1/2)

Coût 1, [energy], trait DEFENSE.

- [x] Étape 2 : cartes de référence : **déclencheur** → `09015` Desperate
      Defense (même montage que `pt003`). **« ou »** → `60044` Choreography,
      `player.ChooseAbilities` à deux branches, chacune portant sa cible.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      ⚠ **`choose` et non `exhaust`** : à la différence de `pt003`, l'allié
      n'est **pas** incliné. Le coût de la flèche est la **désignation**,
      rendue par un `.SetTarget("YourAlly", range=(1,1))` porté par la
      capacité : sans allié, aucune cible légale, `CanPlayBy` rend faux et la
      carte reste en main. **Ne pas copier `pt003` sur `pt005`.**
      **`that ally's ATK / THW value`** → `allie.attack` / `allie.thwart`,
      valeurs **courantes** (bonus compris), pas imprimées ;
      **ce n'est pas une attaque de l'allié** : les dégâts partent de
      l'ÉVÉNEMENT (`this.DealDamage`, sans `AttackProperty`), donc **aucun**
      dégât consécutif, **aucune** riposte, **aucun** déclenchement d'« après
      une attaque ». Le retrait de menace n'est pas un contre
      (`RemoveThreatFromSchemes`, brique de `10004` Sub-Orbital Leap) ;
      **`or`** → deux branches au choix du joueur, pas les deux.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût **1** ; aucune constante de dégâts
      ni de menace (tout vient de l'allié désigné).
      Résultat : conforme.
- [x] Étape 7 : un cas :
      `pt005 … l'allie CHOISI (pas epuise) inflige ses degats d'ATQ a un ennemi`
      (636) : Maria Hill ATQ 1 → **exactement 1** dégât sur Rhino, l'allié reste
      **PRÊT** (`pret: ["01067"]`, la différence avec `pt003`) et à **0** dégât
      (pas de dégât consécutif), la carte est dans la défausse. Rouge sans
      module, vert avec.
      La branche « retirer de la menace » n'a pas de cas dédié : elle partage le
      même corps, et le pilote prend toujours la première option d'un
      `ChooseAbilities`. Le code des deux branches est symétrique et lu à
      l'étape 5.
- [x] Étape 8 : autoplay ciblé : jouée dans **3/8** parties ; 0 traceback.

Carte terminée : OUI

### pt006 : Covered Fire (exemplaire 2/2)

Contenu **identique** à `pt005` (doublon de code). Toutes les vérifications de
`pt005` valent mot pour mot. **Vue en jeu dans 3/8 parties.**

Carte terminée : OUI

### pt007 : * Isaiah Bradley (soutien signature)

Coût 1, [energy], trait PERSONA.

- [x] Étape 2 : cartes de référence : `iw003` Central City Estate (Invisible
      Woman, **officielle**) et `gp007` Gwen's Room, qui impriment **mot pour
      mot** la même structure (« You get +1 REC. » + « Alter-Ego Action: Exhaust
      X → heal N damage from <alter-ego> ») et s'écrivent
      `*GiveKeywordToAttached("You", recover=1)` +
      `WhenInYourPlayTurn(<AlterEgoAction>, …).SetCostFunc(CostFunc.Exhaust("This"))`.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`You get +1 REC`** → cible-chaîne `"You"` = l'identité du contrôleur ;
      le bonus n'a d'effet qu'en **alter-ego**, seule face à porter un REC —
      c'est voulu ;
      **flèche** → `CostFunc.Exhaust("This")` ;
      **`from Elijah Bradley`** → le texte NOMME l'alter-ego, mais la capacité
      est déjà `AlterEgoAction` : la face en jeu **est** Elijah Bradley, on passe
      donc par `initiator.GetIdentity()` plutôt que par un `CardFinder(name=…)`
      qui chercherait dans tout le monde (modèle `gp007`) ;
      ⚠ `*` obligatoire devant `GiveKeywordToAttached` : la fabrique rend une
      **liste**.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût **1** ; **+1** REC ; **2** dégâts
      soignés.
      Résultat : conforme.
- [x] Étape 7 : un cas couvrant **les deux** capacités :
      `pt007 … +1 REC continu ET Alter-Ego Action : 2 degats soignes` (637) :
      `attributs: {"recover": 1}` (REC courant contre REC imprimé, 3 → 4),
      `degats_identite: 1` (3 dégâts posés − 2 soignés) et
      `exhausted: ["pt007"]`. Rouge sans module, vert avec.
- [x] Étape 8 : autoplay ciblé : jouée dans **5/8** parties ; le journal de la
      partie 1 montre la pose (« Elijah Bradley appliquent Isaiah Bradley »)
      puis l'action (« Isaiah Bradley exhausted / activates ») ; 0 traceback.

Carte terminée : OUI

### pt008 : Commandeer (amélioration signature)

Coût 2, [physical], trait TACTIC. **La carte la plus lourde du pack** : quatre
mécaniques, dont deux qu'aucune carte du dépôt ne fait ensemble.

- [x] Étape 2 : cartes de référence :
      **déplacer un attachement déjà en jeu** → `56207` (pack `cw`), **seule
      carte du dépôt** qui le fasse : `attachement.CastTo(Attachment)
      .AttachTo2(nouveau_porteur, effect)` avec une garde
      `bind_face != cible`. `AttachTo2` (`can_attach.py:49-83`) **détache tout
      seul** de l'ancien porteur (lignes 68-69) — il ne faut **pas** appeler
      `DetachFrom2`, qui marque la carte comme retirée et laisse à l'appelant le
      soin de lui trouver une destination.
      **attacher un attachement à un allié** → `44041` ('Pool-ized), qui prouve
      que le moteur l'accepte : `Attachment.CanAttachTo`
      (`attachment.py:24-33`) ne vérifie que `max_per_unit`, **aucune**
      restriction de type de porteur.
      **texte blanc temporaire** → `29024` Vivian,
      `target.TreatAsIfBlank(effect, until_round_end=True)`.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`Exhaust AND discard`** (`and remove`, le mot-piège de `wd005`) → **les
      deux**, empilés par deux `SetCostFunc` (`ability.py:991-993` **empile**),
      comme `cd014` Lovers Quarrel ;
      **`choose an ally`** → troisième partie du coût, `.SetTarget(Ally)` ;
      **`1 attachment`** → un seul, `range=(1,1)` ;
      **`from an enemy`** → le sélecteur ne retient que les attachements dont le
      porteur est un `Enemy` ;
      **`until the end of the round`** → porte sur **le déplacement**, pas
      seulement sur le texte blanc : un `WhenRoundEnd` temporaire rend
      l'attachement ;
      **`treat as blank`** + **`treat SCH as THW`** → voir les deux mesures
      ci-dessous.
      Résultat : conforme.
      **Mesure (a) — le moteur ne sait PAS convertir SCH en THW.** Un
      attachement porte ses bonus sous `ATK+`/`SCH+`/`THW+`, lus nativement en
      `modify_atk`/`modify_sch`/`modify_thw` (`has_modify.py:16-24`) et reversés
      au porteur par un `GiveKeywordToAttached` que le moteur construit tout
      seul (lignes 33-38), **quel que soit** le porteur. **Mais** `face.Gain`
      n'applique `scheme=` que `if HasScheme.IsType(unit)`
      (`face_gain.py:120-125`), et `Ally` (`ally.py:11`) n'est **pas**
      `HasScheme` : un `SCH+` posé sur un allié est **silencieusement perdu**.
      Aucune API de conversion n'existe (ni `UseSCHAsTHW`, ni `consider_as`, qui
      ne gère que nom/trait/type). Le seul précédent SCH→THW est
      `Faces.TreatAsAlly` (`faces.py:340`, lignes 358-359), qui échange la FACE
      d'un sbire — sans rapport. **La conversion est donc écrite à la main, et
      c'est une nécessité, pas un raffinement.**
      **Mesure (b) — `TreatAsIfBlank` emporte AUSSI les bonus.**
      `on_while.py:135-146` force la valeur donnée à 0 dès que
      `is_treat_as_if_blank` est vrai. C'est exactement ce qu'il faut ici : on
      les réapplique nous-mêmes, sinon on les compterait deux fois.
      **Mesure (c) — l'attachement revient bien à l'ennemi**, et s'il est mort,
      il est défaussé (écart assumé, voir le tableau).
      Ordre retenu, et il compte : `AttachTo2` → `TreatAsIfBlank` →
      `GainUntilRoundEnd(attack=ATK+, thwart=SCH+ + THW+)` → `WhenRoundEnd`.
      ⚠ Le `WhenRoundEnd` est enregistré **sur l'allié**, pas sur Commandeer
      (défaussée par son propre coût, elle emporterait ses capacités
      temporaires) ni sur l'attachement (rendu **blanc**).
- [x] Étape 6 : nombres texte ↔ code : coût **2** ; **1** attachement ; durée
      **1 round** ; aucun bonus codé en dur (tout vient de `modify_*`).
      Résultat : conforme.
- [x] Étape 7 : un cas, vérificateur dédié :
      `pt008 … l'attachement passe du vilain a l'allie, texte blanc, SCH devenu
      CTR` (638). `04075` Exo-Suit porte **ATK+ 1 ET SCH+ 1** : c'est la seule
      façon de mesurer la conversion. `pt008_attachement_deplace` contrôle
      **quatre** choses : l'Exo-Suit est lié à l'allié, il est
      `is_treat_as_if_blank`, l'allié gagne **+1 ATQ** (l'ATK+ a suivi) **et**
      **+1 CTR** (le SCH+ converti, qu'il aurait perdu en silence), et Rhino est
      **redescendu** à son ATQ imprimée. Rouge sans module, vert avec.
- [x] Étape 8 : autoplay ciblé : jouée dans **6/8** parties ; 0 traceback.

Carte terminée : OUI

### pt009 : Commander's Orders (amélioration signature)

Coût 1, [mental], aucun trait.

- [x] Étape 2 : cartes de référence : **déclencheur** →
      `AbilityFactory.WhenUnitUseBasicPower` (`friend.py:339`), le message
      `Message.WhenUnitUseBasicPower` (`sender_unit.py:8-34`) étant envoyé par
      `can_attack.py:162` et `can_thwart.py:111` **juste après** le
      `WhenUnitWouldAttack`/`WhenUnitWouldThwart` et **avant** tout calcul : la
      fenêtre est bien une interruption. **Échange** → `message.GainValue`
      (`sender_unit.py:21-34`), qui aiguille tout seul vers
      `GainATKForThisAttack` ou `GainTHWForThisThwart` ; symétrie exacte de
      `message.UseATKInsteadTHW` (`sender_friend.py:75-89`), la méthode
      officielle employée par `jj012`, qui calcule elle aussi `diff = atk - thw`
      mais ne couvre **qu'un sens sur deux**.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`would activate`** pour un ALLIÉ = utiliser un pouvoir de base ; le mot
      « activation » désigne une activation d'**ennemi** dans le vocabulaire du
      moteur (`WhenEnemyWouldActivate`) ;
      **`an ally`** → `Ally`, pas le héros (qui a aussi DEF et REC) ;
      **`you control`** → `control_by="You"` ;
      **`powers=["ATK","THW"]`** → les deux seuls pouvoirs d'un allié
      (`IsAllyPower`) ; sans ce filtre la capacité partirait aussi sur un DEF ou
      un REC, que la carte ne mentionne pas ;
      ⚠ **`message.power` vaut `'ATK'`/`'THW'`/`'DEF'`/`'REC'`/`'SCH'`, jamais
      `'Attack'`/`'Thwart'`** — piège qui a déjà produit **deux conditions
      mortes** sur ce projet. Valeurs posées en dur aux quatre sites d'envoi ;
      **`for that activation`** → `GainValue`, jamais un changement de
      caractéristique ;
      **flèche** → `CostFunc.Exhaust("This")` ;
      ⚠ **pas de `SetPlay()`** (piège `66006`/`66007` du 4/8/2026 : `SetPlay` sur
      la capacité d'une amélioration la rend inerte une fois posée).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût **1** ; aucune constante (le `diff`
      est calculé sur les valeurs courantes de l'allié).
      Résultat : conforme.
- [x] Étape 7 : un cas :
      `pt009 … l'ATQ et le CTR de l'allie sont ECHANGES pour cette activation`
      (639) : Maria Hill ATQ 1 / CTR 2 → elle frappe pour **2**
      (`degats: [["01094", 2]]`), et `exhausted: ["pt009"]`. Une condition
      écrite avec `'Attack'` au lieu de `'ATK'` donnerait **1** : le cas
      départage. Rouge sans module, vert avec.
- [x] Étape 8 : autoplay ciblé : jouée dans **5/8** parties ; 0 traceback.

Carte terminée : OUI

### pt010 : Follow My Lead (amélioration signature)

Coût 1, [mental], aucun trait.

- [x] Étape 2 : carte de référence : `mw006` Weaving a Web (Madame Web), qui
      imprime **la même phrase amputée de sa seconde moitié** (« Resource:
      Exhaust Weaving a Web → generate a [wild] resource for an ally ») et
      s'écrit `CanGenerateResources(<Resource>, Resources("G"),
      CardFinder(card_type=Ally)).SetCostFunc(CostFunc.Exhaust("This"))`.
      Précédent du filtre « attachable à un allié » : `45017` Suit Up
      (`can_attach_to_ally`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      ⚠ **une seule `CanGenerateResources` par carte** :
      `card_player.py:82-84` porte un `assert len(resources_abilities) <= 1`.
      La restriction doit donc être portée par **une** capacité ;
      **`[wild]`** → `Resources("G")` ;
      **`for an ally or an upgrade…`** → ressource **restreinte**. Deux voies
      existaient : `for_card=CardFinder(...)`, évalué **sans `effect`**
      (`resources.py:163-166`), ce qui fait **ignorer silencieusement** un
      `check_effect_fn` (`checker.py:473-481`) — insuffisant ici ; et
      `conditions=[...]`, dont chaque entrée reçoit `(effect, message)` avec
      `message.paying_for_effect.this` = la carte payée
      (`sender_player.py:247-266`, même attribut que chez Reed Richards
      `mf001b`). **C'est la seconde qui est employée**, `for_card` restant à
      `None` (les deux filtres se cumuleraient) ;
      **`an ally`** sans « you control » → `Worlds.GetOnFieldAllies`, tous les
      joueurs ;
      **flèche** → `CostFunc.Exhaust("This")`.
      Résultat : conforme, avec l'écart documenté au tableau.
- [x] Étape 6 : nombres texte ↔ code : coût **1** ; **1** ressource générée.
      Résultat : conforme.
- [x] Étape 7 : deux cas, dont une contre-épreuve :
      - `pt010 … la ressource [wild] finance une amelioration attachable a un
        allie` (640) : `pt013` seule en main, un allié en jeu → elle entre en
        jeu et `pt010` est **incliné**. Rouge sans module, vert avec.
      - `pt010 … contre-epreuve : elle NE finance PAS une amelioration
        d'identite` (641) : `pt012` (coût 1, s'attache à l'identité) **n'entre
        jamais en jeu** et `pt010` reste **PRÊT** (la ressource n'a pas été
        dépensée). Ce cas reste **légitimement vert sans le module** : il
        affirme que RIEN ne se passe. **Son jumeau positif est le 640**, qui
        est bien rouge.
- [x] Étape 8 : autoplay ciblé : jouée dans **7/8** parties ; le journal de la
      partie 2 montre « Follow My Lead exhausted / Patriot gains resource G » ;
      0 traceback.

Carte terminée : OUI

### pt011 : On Your Feet (amélioration signature)

Coût 3, [mental], aucun trait.

- [x] Étape 2 : cartes de référence : **« choose: A or B »** → `60044`
      Choreography, `ChooseAbilities` à deux branches portant chacune sa cible ;
      **couple action + inclinaison** → `iw003` Central City Estate.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`an ally`** — le texte n'imprime **pas** « you control » (contrairement
      à `pt003`, `pt005`, `pt009`) : la cible est donc `Ally`, **tous** les
      alliés en jeu. Mot-piège `you control` appliqué **dans l'autre sens** : on
      n'ajoute pas une restriction qui n'est pas écrite ;
      **`or`** → deux branches, pas les deux ;
      filtres par branche (`canbe_ready=True`, `canbe_heal=True`) pour éviter
      les choix vides ;
      **flèche** → `CostFunc.Exhaust("This")` ;
      ⚠ **pas de `SetPlay()`**.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût **3** ; **1** dégât soigné.
      Résultat : conforme.
- [x] Étape 7 : deux cas, un par branche :
      - `pt011 … branche 1 : un allie incline est REDRESSE` (642) : le pilote
        prend la première option. Rouge sans module, vert avec.
      - `pt011 … branche 2 : 1 degat soigne sur un allie` (643) : branche
        **inatteignable** sans la clé `preferer_option` (« Heal 1 damage »), le
        pilote prenant toujours la première option. Rouge sans module, vert avec.
- [x] Étape 8 : autoplay ciblé : jouée dans **6/8** parties ; 0 traceback.

Carte terminée : OUI

### pt012 : * Patriot's Shield (amélioration signature)

Coût 1, [wild], trait ITEM. C'est la carte que `pt001b` va chercher.

- [x] Étape 2 : cartes de référence : **+1 DEF** → `03009` Captain America's
      Shield, même structure (amélioration ITEM sur l'identité) écrite
      `*GiveKeywordToAttached(..., defense=1)`. **Dégâts accumulés sur la
      carte** → `04065` Crossbones' Armor, **seul modèle du dépôt** pour « les
      dégâts vont sur cette carte, et à N dégâts elle est défaussée ».
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`move 1 OF that damage`** → **un seul point** :
      `message.PreventDamage(1, effect)` retire exactement 1 point de ce que
      l'identité va encaisser, **le reste passe**. `04065` déplace **tous** les
      dégâts (`SetBeInstead`) : le copier aurait tout annulé — lecture inverse ;
      **`move`** (leçon `instead`) → sans le `PreventDamage`, l'identité **et**
      le bouclier encaisseraient ;
      **`from an attack`** → `is_from_attack=True` : les dégâts de trahison ne
      déclenchent rien ;
      **`you may`** + **`Hero Interrupt`** → `AbilityType.HeroInterrupt` **non
      forcé** (`04065` est un `ForcedInterrupt`) ;
      **`reaches 3 damage`** → seuil **3**, pas 5 ; contrôlé dans le même
      handler, comme `04065`.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût **1** ; **+1** DEF ; **1** point
      déplacé ; seuil **3**.
      Résultat : conforme.
- [x] Étape 7 : deux cas :
      - `pt012 … +1 DEF continu ET 1 SEUL degat DEPLACE sur la carte` (644) :
        Rhino ATQ 2 + 1 icône = 3, héros **incliné** donc sans défense →
        `degats_identite: 2` **et** `compteurs: [["pt012","damage",1]]`. Si le
        point était **dupliqué** au lieu d'être déplacé, l'identité serait à 3 :
        le cas départage. Rouge sans module, vert avec.
      - `pt012 … a 3 degats elle est DEFAUSSEE` (645) : deux compteurs posés en
        mise en place, le troisième vient de l'attaque → `hors_jeu`. Rouge sans
        module, vert avec.
- [x] Étape 8 : autoplay ciblé : présente dans **8/8** parties ; 0 traceback.

Carte terminée : OUI

### pt013 : Revenge (amélioration signature)

Coût 1, [physical], `MaxPerUnit "1"`, aucun trait.

- [x] Étape 2 : cartes de référence : **attache à un allié** → `01074` Inspired,
      `03031` Enraged, `12018` Reinforced Suit (`CanPlayThisUpgradeCard(Ally)`).
      **Coût de défausse** → `mw007` Life-Support System
      (`CostFunc.Discard("This")`). **« until the end of the NEXT round »** →
      **aucun précédent officiel** ; seul précédent du dépôt : `sd017` No
      Outrunning This, qui compte les fins de round à la main.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      ⚠ **`Max 1 per ally`** → `MaxPerUnit` lu **nativement**
      (`HasMaxPer.max_per_unit`, relu par `Asset2.CanAttachTo`,
      `asset.py:69-73`) : **aucun module**, coder une capacité fantôme serait
      une faute ;
      **`When Patriot takes…`** → cible-chaîne `"YourHero"` et **jamais**
      `CardFinder(name="Patriot")` : deux alliés officiels portent déjà ce nom
      (`29016`, `56041`) ;
      **`any amount of damage`** → au moins 1 (`at_least_damage=1`, revérifié
      sur `will_take_damage`) ;
      **`from an attack`** → `is_from_attack=True` : les dégâts de trahison ne
      déclenchent rien ;
      **flèche** → `CostFunc.Discard("This")` ;
      **`until the end of the NEXT round`** → **deux** fins de round.
      `GainUntilRoundEnd` s'arrêterait à la fin du round **courant** (un round
      trop tôt) et `TemporaryGain(end_event=WhenRoundEnd)` câble sa condition
      sur `lambda: True` (`face_action.py:322-327`) : on applique donc
      `allie.Gain(effect, +1, attack=2)` et on enregistre **sur l'allié** un
      `AbilityFactory.WhenRoundEnd(<Temp2>, round_id=world.round_id + 1, …)`
      (`turn_phase.py:284-303`, `Message.WhenRoundEnd.round_id` valant
      `world.round_id`, `sender_round.py:100-106`, incrémenté au **début** de
      chaque round, `world.py:755`). Le round N ne déclenche rien, seul N+1
      rabaisse le bonus.
      ⚠ Enregistré **sur l'allié**, pas sur Revenge (défaussée par son propre
      coût, elle emporterait la capacité temporaire — leçon `sd017`).
      ⚠ **L'allié porteur est lu dans `effect.targets`** (cible-chaîne
      `"Attached"`), pas par `GetBindFace()` : voir le **bug n°2**.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût **1** ; `MaxPerUnit` **1** ; **+2**
      ATQ ; durée **round + 1**.
      Résultat : conforme.
- [x] Étape 7 : un cas :
      `pt013 … quand Patriot encaisse une attaque, l'allie porteur gagne +2 ATQ`
      (646) : héros **et** allié inclinés (seul moyen de faire arriver l'attaque
      jusqu'à l'identité) ; `attributs_carte: [["01067","attack",2]]` et
      `hors_jeu: ["pt013"]`. Rouge sans module ; **rouge aussi avec la première
      version du module** (bug n°2), vert après correction.
- [x] Étape 8 : autoplay ciblé : jouée dans **7/8** parties ; 0 traceback —
      y compris après le correctif, ce qui prouve que l'`AssertionError` avalée
      a bien disparu.

Carte terminée : OUI

### pt014 : The Chosen Leader (amélioration signature)

Coût 3, [wild], trait TITLE.

- [x] Étape 2 : cartes de référence : **« defeated by consequential damage »** →
      `38028` Med Lab (pack `rogue`, **officielle**), qui imprime la même
      restriction et s'écrit `AfterUnitBeDefeated(<Response>, Ally, …,
      by_consequential=True)`. **« used to defend »** →
      `AbilityFactory.AfterUnitBecomeDefender` (`do_attack.py:1257-1286`),
      envoyée par `DeclareDefenderInternal` (`sender_damage.py:170`), donc
      exactement « est utilisé pour se défendre » ; à distinguer de
      `AfterUnitDefendAgainstAttack` (modèle `36035` Hangar Bay), qui part
      **après** la défense résolue.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`by consequential damage`** → `by_consequential=True`
      (`defeated.py:355-358`, test `message.IsByConsequential()`,
      `sender_unit.py:116-118`). Restriction **forte** et c'est le sujet de la
      carte : un allié tué par une **attaque** ne déclenche **rien**. Coder
      `defeated` tout court aurait rendu la carte deux fois plus forte
      (mot-piège `defeated` vs `damaged`) ;
      **`an ally you control`** → cible-chaîne `"YouControlAlly"` plutôt que le
      type `Ally` nu : la fabrique bascule alors sur un
      `WhenUnitWouldBeDefeated` + capacité temporaire
      (`defeated.py:395-428`), **seul moyen** de connaître le contrôleur d'un
      allié en train de quitter le jeu ;
      **`search your deck`** → le deck **seul**, pas la défausse (différence
      avec `pt001b` et `pt002`) ;
      **`Forced Response` vs `When`** → texte **contradictoire**, arbitrage
      utilisateur du 30/08/2026 : le mot-clé en gras fait foi, donc **APRÈS**
      (voir la section « Arbitrages ») ;
      **`your identity`** (et non « your hero ») → l'identité quelle que soit sa
      forme ;
      **pas de flèche sur la seconde capacité** : c'est une conséquence forcée,
      elle ne se paie pas et ne se refuse pas ;
      ⚠ **pas de `SetPlay()`**.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût **3** ; **1** dégât à l'identité ;
      **1** allié cherché.
      Résultat : conforme.
- [x] Étape 7 : deux cas, un par capacité :
      - `pt014 … Forced Response : un allie qui DEFEND coute 1 degat a
        l'identite` (647) : `defender='01067'`, `degats_identite: 1`. Rouge sans
        module, vert avec.
      - `pt014 … Response : allie vaincu par degat CONSECUTIF -> un allie
        remonte en main` (648) : montage subtil — **deux** alliés attaquent, le
        premier consomme la limite de Will to Protect, le second (ramené à 1 PV)
        encaisse donc vraiment son dégât consécutif et meurt. La main est
        **vidée** par `main_exclusive`, donc tout allié qui s'y trouve ensuite
        vient de la recherche (vérificateur `pt014_allie_cherche`). Rouge sans
        module, vert avec.
- [x] Étape 8 : autoplay ciblé : jouée dans **3/8** parties ; 0 traceback.

Carte terminée : OUI

### pt015 : Throwing Stars (amélioration signature)

Coût 1, [physical], `MaxPerUnit "1"`, trait WEAPON.

- [x] Étape 2 : cartes de référence : **attache à un allié** → `01074`, `03031`,
      `12018`. **Interruption sur l'attaque du porteur** → `04072` Laser Rifle,
      qui emploie `"AttachedVillain"` de la même façon que `"AttachedAlly"` ici.
      **Répartition** → `15011` Wiccan (officielle) et `13006` Wasp Sting, même
      `ForChoiceAbility(...).SetTarget(Enemy, range=(1,n),
      repeat_rules="Health")`. **piercing + ranged depuis un interrupt** →
      `dt099` Marrow, qui appelle les deux (`sender_damage.py:95` et `107`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      ⚠ **`Max 1 per ally`** → `MaxPerUnit` natif, aucun module ;
      **flèche** → `CostFunc.Discard("This")` ;
      **`divided as you choose`** → **vraie** répartition, `repeat_rules="Health"`
      (un clic = une attribution, il en faut trois ; les doublons de
      `all_legal_targets` sont du **sens**, pas du bruit — §10 du guide) ;
      **ces 3 dégâts ne sont pas une attaque** : ils partent de l'amélioration,
      sans `AttackProperty`, donc ni riposte ni dégât consécutif, et ils
      **s'ajoutent** à l'attaque de l'allié ;
      **`This attack gains piercing and ranged`** → **question ouverte**, voir la
      section dédiée ; lecture RAW appliquée ;
      ⚠ **`ranged` ignore la RIPOSTE, pas le Garde** (`can_retaliate.py:38`) ;
      ⚠ **le libellé `(attack)` n'est pas posé** → écart technique, voir le
      tableau et le bug n°1.
      Résultat : conforme, avec l'écart et la question documentés.
- [x] Étape 6 : nombres texte ↔ code : coût **1** ; `MaxPerUnit` **1** ; **3**
      dégâts répartis.
      Résultat : conforme.
- [x] Étape 7 : un cas :
      `pt015 … 3 degats REPARTIS en plus de l'attaque de l'allie porteur` (649) :
      Mockingbird ATQ 1 + 3 répartis = **4** dégâts sur Rhino
      (`cibles` répétées quatre fois), et `hors_jeu: ["pt015"]`. Un effet qui
      infligerait 3 dégâts **sur une seule cible** donnerait le même total ici
      (une seule cible en jeu) ; ce que le cas prouve, c'est que les **trois
      attributions** sont bien demandées et honorées — sans `repeat_rules`, le
      sélecteur n'accepterait qu'un seul clic et le total serait 2. Rouge sans
      module, vert avec.
- [x] Étape 8 : autoplay ciblé : jouée dans **5/8** parties ; 0 traceback.

Carte terminée : OUI

### pt016 : Working Together (amélioration signature)

Coût 1, [mental], `MaxPerUnit "1"`, trait TACTIC.

- [x] Étape 2 : cartes de référence : **attache à un allié** → `01074`, `03031`,
      `12018`. **Interruption de contre du porteur** →
      `WhenUnitWouldThwart(..., "AttachedAlly", …, is_basic_thwart=True)`.
      **Cible « another »** → `29024` Vivian, qui calcule sa liste de cibles par
      une fonction plutôt que par une chaîne.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      ⚠ **`Max 1 per ally`** → natif ;
      **`is_basic_thwart=True`** n'est pas arbitraire : `GainTHWForThisThwart`
      (`sender_friend.py:69-73`) porte un `assert self.IsBasicThwart()`, un
      contre non basique ferait **planter** la carte. Un allié ne contre de
      toute façon que par son pouvoir de base ;
      **`another`** → l'allié porteur est **exclu** ; `exclude=["This"]` ne
      conviendrait pas (« This » désigne l'**amélioration**, pas son porteur),
      d'où la fonction de cible ;
      **`friendly character`** nu → identités **et** alliés de **tous** les
      joueurs (`Worlds.GetOnFieldFriendlyCharacters`, ce que rend la
      cible-chaîne `"Friend"`) ;
      **flèche à DEUX parties** (`choose … AND discard`) → `.SetTarget(...)`
      obligatoire **et** `CostFunc.Discard("This")` : sans autre personnage ami,
      l'interruption n'est pas proposée ;
      **`THW value`** → valeur **courante** (`face.thwart`), garde
      `HasThwart.IsType`.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût **1** ; `MaxPerUnit` **1** ; aucune
      constante (la valeur vient du personnage choisi).
      Résultat : conforme.
- [x] Étape 7 : un cas :
      `pt016 … le CTR d'un AUTRE personnage ami s'ajoute au contre de l'allie`
      (650) : 6 menaces − 1 (Mockingbird) − 1 (Patriot) = **4**, et
      `hors_jeu: ["pt016"]`. En solo, Patriot est le **seul** choix légal :
      c'est aussi la preuve que le porteur est bien exclu. Rouge sans module,
      vert avec.
- [x] Étape 8 : autoplay ciblé : jouée dans **6/8** parties ; 0 traceback.

Carte terminée : OUI

### pt017 : MGH Addiction (obligation)

`Boost 2`, `GiveTo "Elijah Bradley"`. Set **`Patriot`** (numérotée sans mention
némésis sur le scan) : elle vit dans la clé `obligations` du deck de départ,
**pas** dans le `nemesis_set`.

- [x] Étape 2 : cartes de référence : `wc018` Avoiding the Demiurge et `sd017`
      No Outrunning This (même auteur, packs frères), et `09027` Physical Toll
      (le précédent officiel) : même triplet
      `WhenThisObligationGiveToYou` + `YouMayFlipToYourAlterEgoForm` +
      `ChooseAbilities` à deux branches. **Branche conditionnelle** →
      `condition=` de `09027` et `cd014`. **Surge** → `ThisCardGainSurge`
      (`cards/pack/__init__.py:100`), idiome de `il021`, `il022`, `22031`.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`GiveTo`** → exigé par `Obligation.CheckPrintedValue`
      (`obligation.py:50-52`), porte le nom de la face **alter-ego** ;
      **flèche, branche 1** → sans `pt007` en jeu **sous le contrôle du
      joueur**, l'option est **indisponible** (`condition=`) ; le soutien est
      cherché dans `player.GetControlCards()` et non sur tout le terrain (un
      `Worlds.FindCardOnField` attraperait l'exemplaire d'un autre joueur) ;
      nom écrit **sans l'étoile** ;
      **`If no allies were exhausted this way`** → « exhausted **THIS WAY** » :
      on lit le **retour** de `Faces.ExhaustAll`, pas le nombre d'alliés en
      jeu ; un allié **déjà incliné** ne compte pas, et un joueur qui n'a que
      des alliés inclinés déclenche donc le surge ;
      **`Discard this obligation`** → portée : la **seconde** puce seulement (la
      première se termine par « remove … from the game », exclusif d'une
      défausse) — même lecture que `wc018`, `sd017`, `ok019`, `il017` ;
      **pas de capacité `Boost`** : le scan n'imprime aucun `[star] Boost:`,
      seulement les **deux icônes**, lues nativement depuis `desc.Boost`.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : `Boost` **2** (natif) ; aucune autre
      valeur.
      Résultat : conforme.
- [x] Étape 7 : deux cas :
      - `pt017 … branche 1 : defausser Isaiah Bradley retire l'obligation DU
        JEU` (651) : `hors_jeu: ["pt017", "pt007"]`, **les deux**. Rouge sans
        module, vert avec.
      - `pt017 … branche 2 : tous les allies sont EPUISES, pas de surge` (652) :
        sans `pt007` en jeu, la première branche est indisponible, seule la
        seconde est proposée ; `exhausted: ["01083"]` et `hors_jeu: ["pt017"]`.
        Rouge sans module, vert avec.
      La bascule du **surge** n'a pas de cas : voir « Limites du harnais » n°1.
- [x] Étape 8 : autoplay ciblé : révélée dans **8/8** parties (elle est mise de
      côté au montage, `AsideDeck<5>`) ; 0 traceback.

Carte terminée : OUI

### pt018 : Mr. Hyde's Lab (manigance annexe némésis)

`StartingThreat "2*"` (2 **par joueur**), `Boost 2`, **`Crisis "1"`**.

- [x] Étape 2 : cartes de référence : **déclencheur** → `jj012` Always a Bigger
      Conspiracy, même `WhenSchemeBeDefeated(<WhenDefeated>, "This", …)`.
      **« X attacks you. If no attack was made this way… »** → `02040` Tail
      Sweep et `22031` Old Rivals, mêmes
      `enemy.DoAttackYou(player, effect, if_no_attack_was_made=action)` **et**
      `else: action()` quand l'ennemi n'est pas en jeu.
      **Recherche + mise en jeu** → `60060` (pack `fne`) et `bw021` Namor.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      ⚠ **`Crisis`** lu **nativement** dans `desc` (`CanCrisis`) : aucun module,
      et **l'icône a été vérifiée par découpe d'image** contre `ag011`, avec
      `hd022` et `hd026` en contrôles — point clos ;
      ⚠ **`StartingThreat "2*"`** : l'étoile est le marqueur « par joueur », lu
      nativement ;
      ⚠ **`SideScheme` en JSON = classe `EncounterSideScheme`** dans le script
      (piège §10 du guide) ;
      **`attacks you`** → `message.defeating_player` (`sender_scheme.py:175-184`),
      repli sur le premier joueur (comme `jj012`) ;
      **`If no attack was made this way`** → part aussi quand Mr. Hyde n'est
      **pas en jeu du tout** : c'est le cas nominal, et c'est ce qui donne son
      sens à la carte (elle **fait venir** le sbire) ;
      **`the encounter deck and encounter discard pile`** → **deux** zones. La
      carte ne dit **pas** « and set aside cards », contrairement à `pt019` :
      on ne recopie pas une carte sur l'autre.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : `StartingThreat` **2\*** ; `Boost` **2** ;
      `Crisis` **1** — tous natifs.
      Résultat : conforme.
- [x] Étape 7 : un cas :
      `pt018 … Mr. Hyde n'est pas la, il est CHERCHE et mis en jeu` (653) : le
      sbire est placé dans le deck Rencontre par le banc (au montage il vit dans
      la réserve du joueur, **hors de portée** d'une recherche « encounter deck
      + discard pile ») ; la manigance est ramenée à 1 menace pour qu'un seul
      contre de base la batte. `en_jeu: ["pt019"]`, `hors_jeu: ["pt018"]`.
      Rouge sans module, vert avec.
- [x] Étape 8 : autoplay ciblé : vue en jeu dans **1/8** parties (le set némésis
      n'arrive qu'après l'obligation) ; 0 traceback.

Carte terminée : OUI

### pt019 : * Mr. Hyde (sbire némésis)

PV 5, ATQ 2, MNG 2, `Boost 3`, **`Toughness 1`**, `Nemesis "Elijah Bradley"`,
trait ELITE.

- [x] Étape 2 : cartes de référence : **recherche + attache** → `21177` Seduced
      (pack `mts`) et `57001` (pack `synthezoid`), tous deux en
      `Search.EncounterCard(..., include_discard_pile=…, include_set_aside=True,
      name=…, card_type=Attachment)` puis `face.AttachTo2(cible, effect)`.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      ⚠ **`Toughness`** et **`Nemesis`** lus **nativement** dans `desc` :
      aucun module, coder une capacité fantôme serait une faute
      (PROCESSUS-CARTE §5, « bases automatiques ») ;
      **`encounter deck, encounter discard pile AND SET ASIDE CARDS`** →
      **TROIS** zones (`include_discard_pile=True`, `include_set_aside=True`).
      `pt018`, elle, n'en cite que deux ;
      **`attach it to Mr. Hyde`** → à **CE** sbire (`effect.this`), pas au
      premier « Mr. Hyde » trouvé sur le terrain ;
      nom cherché **sans l'étoile** ;
      **collision** : `24035` s'appelle « **Mister** Hyde » — chaîne différente,
      aucune collision, rien à corriger côté `hood` ;
      le trait **ELITE** n'est pas décoratif : il met le sbire hors de portée
      des effets `CardFinder(non_trait="ELITE")`.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : PV 5, ATQ 2, MNG 2, `Boost` 3,
      `Toughness` 1 — tous natifs.
      Résultat : conforme.
- [x] Étape 7 : un cas, vérificateur dédié :
      `pt019 … le MGH Drug est cherche dans TROIS zones et attache a lui` (654) :
      `pt019_mgh_drug_attachee` contrôle que l'attachement est **lié au sbire**,
      pas seulement en jeu. Rouge sans module, vert avec.
- [x] Étape 8 : autoplay ciblé : vu en jeu dans **1/8** parties ; 0 traceback.

Carte terminée : OUI

### pt020 : MGH Drug (attachement némésis)

`ATK+ "1"`, `Boost "0"` + une capacité de bonus étoilée.

- [x] Étape 2 : cartes de référence : **attache conditionnelle** → `04029`
      Crossfire's Rifle et `04064` Crossbones' Machine Gun, qui impriment la
      même tournure (`AttachToFaceWhenPutIntoPlay(CardFinder(name=…),
      if_cannot_attach_to=Villain)`) ; `sd021` Magic Chains fait de même dans le
      pack frère. **`[star] … gain overkill`** → `57007` Superhuman Strength,
      `UnitAttackGainKeyword(..., overkill=True)`. **Hero Action à coût coloré**
      → `04073` Energy Shield, qui imprime « Hero Action: Spend
      [energy][mental] resources → discard this card » et s'écrit
      `PlayerActionToDiscardThis(<HeroAction>).SetCost(Cost("YB"))` ;
      `04072` Laser Rifle avec `Cost("YR")`. **`[star] Boost: Reveal this
      card`** → `RevealThisCard`, idiome de `16140`, `56144`, `56145`, `57007`.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      ⚠ **la clé est `ATK+`, jamais `ATK`** : sur un attachement c'est un
      **bonus au porteur**, lu nativement (`has_modify.py:22`) et reversé par un
      `GiveKeywordToAttached` que le moteur construit seul — **rien à coder** ;
      **`Boost "0"`** : zéro icône imprimée, mais une capacité `[star] Boost`
      (modèle `wd005`) ;
      **`if able` / `If you cannot`** → `if_cannot_attach_to=Villain` ;
      **`Attached ENEMY's attacks`** → `"AttachedEnemy"` et non
      `"AttachedCharacter"` : la carte peut atterrir sur le sbire **ou** sur le
      vilain ;
      **`Spend [mental][energy]`** → **relevé par découpe d'image** : B =
      [mental], Y = [energy] (`element/cost.py:29-46`), donc `Cost("YB")` ;
      **`.SetCost` et non `.SetCostFunc`** : un coût en **ressources** se
      déclare par `SetCost` (`ability.py:320`), `SetCostFunc` étant réservé aux
      coûts d'action.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : `ATK+` **1** ; `Boost` **0** ; coût
      **1 [mental] + 1 [energy]**.
      Résultat : conforme.
- [x] Étape 7 : deux cas :
      - `pt020 … Hero Action : depenser [mental][energy] la defausse` (655) :
        même limite du pilote que `sd020` — deux cartes à **une** icône (`pt009`
        [mental] et `pt003` [energy]). L'attache conditionnelle est contrôlée au
        passage : sans elle la carte ne serait même pas en jeu. Rouge sans
        module, vert avec.
      - `pt020 … [star] : les attaques de l'ennemi porteur gagnent OVERKILL`
        (656) : l'overkill n'est observable qu'avec un **défenseur qui meurt**.
        Maria Hill ramenée à 1 PV encaisse, l'excès passe à l'identité : Rhino
        ATQ 2 + 1 (l'`ATK+`) + 1 icône = 4, moins 1 PV = **3** sur l'identité.
        Sans overkill, l'identité ne prendrait **rien**. Rouge sans module,
        vert avec.
      La capacité `[star] Boost: Reveal this card` n'a pas de cas dédié : c'est
      l'idiome partagé `RevealThisCard`, déjà couvert par les cas des packs
      `cw`, `synthezoid` et `wiccan`.
- [x] Étape 8 : autoplay ciblé : vu en jeu dans **1/8** parties ; 0 traceback.

Carte terminée : OUI

### pt021 : Bulldozing Charge (exemplaire 1/2)

`Boost 1` + une capacité de bonus étoilée.

- [x] Étape 2 : cartes de référence : **When Revealed** → `02040` Tail Sweep,
      qui imprime **exactement** la même structure et s'écrit
      `Worlds.FindCardOnField` → `DoAttackYou(..., if_no_attack_was_made=…)` →
      `else: action()` ; `22031` Old Rivals fait de même.
      **`[star] Boost` overkill** → `16134` Kree Private et `wd066` Scaly
      Setback, `WhenCardBecomeBoost("This", fn, during_attack=True)` +
      `message.would_atk_message.GainOverKill(effect)`.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`If no attack was made this way`** → part dans **deux** cas : Mr. Hyde
      n'est pas en jeu, **ou** il l'est mais l'attaque n'a pas eu lieu ;
      **`attacks you`** → `message.GetToPlayer()`, le joueur à qui la carte est
      distribuée ;
      **`each friendly character`** → identités **et** alliés de **tous** les
      joueurs ; le texte ne dit ni « your », ni « you control » (mot-piège
      `each` : ne pas restreindre une portée qui ne l'est pas). En solo la
      différence est nulle, en multijoueur elle est majeure ;
      **`during_attack=True`** porte la condition « si cette carte se résout
      pendant une attaque » : hors d'une attaque la fabrique ne déclenche rien
      et `would_atk_message` n'est jamais lu — d'où l'absence de garde dans le
      corps.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : `Boost` **1** ; **1** dégât par
      personnage ami.
      Résultat : conforme.
- [x] Étape 7 : trois cas :
      - `pt021 … When Revealed SANS Mr. Hyde : 1 degat a CHAQUE personnage ami`
        (657) : `degats: [["01083", 1]]` **et** `degats_identite: 1` — l'allié
        **et** l'identité, ce qui prouve la portée non restreinte. Rouge sans
        module, vert avec.
      - `pt021 … AVEC Mr. Hyde en jeu : il attaque, l'allie ne prend RIEN` (658) :
        **contre-épreuve** ; héros **et** allié inclinés pour que personne ne
        défende ; vérificateur `pt021_hyde_a_frappe` (allié intact **et**
        identité touchée). Rouge sans module, vert avec.
      - `pt021 … capacite Boost : l'attaque en cours gagne OVERKILL` (659) : la
        trahison est posée sur le **dessus** du deck Rencontre, elle devient
        donc la carte de bonus de l'attaque ; 1 icône → Rhino 2 + 1 = 3, moins
        1 PV du défenseur = **2** sur l'identité. Sans la capacité Boost,
        l'identité ne prendrait **rien**. Rouge sans module, vert avec.
- [x] Étape 8 : autoplay ciblé : vue en jeu dans **1/8** parties ; 0 traceback.

Carte terminée : OUI

### pt022 : Bulldozing Charge (exemplaire 2/2)

Contenu **identique** à `pt021` (doublon de code). Toutes les vérifications de
`pt021` valent mot pour mot. **Vue en jeu dans 1/8 parties.**

Carte terminée : OUI

---

## Gate finale (PROCESSUS-HEROS)

- [x] **Étapes 1 à 8 complètes** : `cards.json` (23 cartes), scripts
      (23 modules + 3 `__init__.py`), deck de départ, `data/nemesis/
      patriot_nemesis.json`, `data/sets_info.json` (131),
      `tools/prefixes_fanmade.json`, 23 images (+ recette
      `tools/importer_images_patriot.py`), **biographie** (`pt001a` dans
      `public/js/prepare/heros-info.js`), **texte français** (23 entrées dans
      `ui-app/src/board/textes-fr-fanmade.ts`), **règle de deck-building**
      (`public/js/deckbuilder/app.js`, `exemptDeLaLimiteAspect`).
- [x] **Un `PROCESSUS-CARTE.md` rempli et « Carte terminée : OUI » pour chaque
      carte du pack** : `pt001a`, `pt001b`, `pt002`, `pt003`, `pt004`, `pt005`,
      `pt006`, `pt007`, `pt008`, `pt009`, `pt010`, `pt011`, `pt012`, `pt013`,
      `pt014`, `pt015`, `pt016`, `pt017`, `pt018`, `pt019`, `pt020`, `pt021`,
      `pt022` — **23/23**.
- [ ] **Une partie complète jouée avec le héros** : **NON**, et ce n'est pas une
      omission qu'on peut combler ici. Une partie humaine dans le navigateur est
      hors de portée de cette session : elle demande d'ouvrir
      `http://127.0.0.1:2345/`, de cliquer et de juger. **Je ne l'ai pas jouée
      et je ne peux pas la jouer.** Ce qui a été fait à la place : 8 parties
      d'autoplay complètes (0 bloquée, 0 traceback, 23/23 cartes vues en jeu),
      30 cas de comportement verts avec preuve rouge/vert module par module, et
      le montage de partie vérifié (`ok: true`).

**Ce que ces outils ne peuvent pas voir** — à vérifier lors de la première
partie humaine, précisément :

1. **La biographie au survol.** PROCESSUS-HEROS §7 exige une preuve visuelle :
   survoler Patriot dans le wizard et constater que le panneau affiche bien le
   texte, pas seulement le grand visuel. L'entrée est indexée par `pt001a` comme
   prescrit, mais **la preuve visuelle n'a pas été faite**.
2. **Les tooltips français.** Les 23 entrées sont écrites, mais rien n'apparaît
   dans le jeu tant que **`ui-app/deployer.sh` n'a pas tourné** (§11.1 du
   guide). **Il n'a pas été lancé dans cette session** (et `ui-app/node_modules`
   est absent : ni `tsc` ni `vite` ne sont installés, la compilation TypeScript
   n'a donc pas pu être vérifiée — seule la validité **syntaxique** des 23
   chaînes a été contrôlée). ⚠ Attention au piège du §10 : `deployer.sh`
   recopie `public/js` depuis le vestige WSL avec `--delete` et peut **écraser
   la biographie** — vérifier `public/js/prepare/heros-info.js` après le
   déploiement.
3. **La règle « Leader » dans le deck-builder.** `exemptDeLaLimiteAspect` a été
   étendue, mais **aucune carte du catalogue ne la déclenche aujourd'hui** :
   impossible de la voir agir, ni en test ni en partie.
4. **Le confort de la question de `pt008`.** Le joueur doit désigner un allié
   **puis** un attachement, et le résultat (texte blanc + statistiques
   déplacées) n'est visible que sur le plateau : seul un joueur peut dire si
   c'est lisible.
5. **`pt015` — l'arbitrage `piercing`/`ranged`.** Voir la question ouverte : la
   lecture RAW est appliquée, l'utilisateur n'a pas encore tranché.
6. **La branche « surge » de `pt017`.** Voir « Limites du harnais » n°1 :
   correcte par lecture, jamais observée.
