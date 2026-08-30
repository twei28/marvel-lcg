# Pack Speed — fiches PROCESSUS-CARTE.md, une par card_id

Gabarit suivi : `PROCESSUS-HEROS.md` / `PROCESSUS-CARTE.md`. **23 card_id** au
total (`sd001a` à `sd022`, les faces `a`/`b` de Speed comptant pour deux
identifiants distincts). Source : pack fan-made **CptScorp** (« Marvel Champions
Custom Project », Cycle 2) — même auteur qu'`iron_lad`, `scarlet_spider` et
`wiccan`. 2 faces héros, 15 cartes signature, 1 obligation et 5 cartes némésis.
Set 130, préfixe `sd`. Personnage : Tommy Shepherd, le speedster des Young
Avengers, frère jumeau de Billy Kaplan (Wiccan).

Les étapes 1 et 3-6 de PROCESSUS-HEROS (cards.json, deck de départ,
`data/nemesis/speed_nemesis.json`, `data/sets_info.json`, préfixe déclaré,
traits `ANTI HERO` / `ART` et compteur `explosive` ajoutés au moteur, 23 images)
ont été faites lors d'une session antérieure, **avec vérification des 15 icônes
de ressource et des 6 valeurs de bonus par découpe d'image** (recette
reproductible : `tools/importer_images_speed.py`, `assets/pics/` étant
gitignoré). Cette session a couvert l'étape 2 (les 23 scripts) et les étapes 7
à 10 (biographie, texte FR, validation carte par carte, autoplay, gate finale),
plus **deux correctifs moteur** rendus obligatoires par le pack (bugs n°1 et
n°2 ci-dessous).

## Mécanique centrale : les compteurs explosifs

Tout le kit tourne autour d'un mécanisme qui n'est écrit sur **aucune carte** :
il est sur l'**insert** du pack (`Speed Insert`, lu par découpe d'image).

> Speed peut poser des **explosive counters** sur un ennemi ou une manigance
> (**max 1 compteur par ennemi/manigance**). Ces compteurs sont **retirés du jeu
> à la fin de la phase des joueurs** et, **au moment où ils sont retirés** :
> retiré d'un ennemi → **1 dégât à cet ennemi** ; retiré d'une manigance →
> **1 menace retirée de cette manigance**.

Douze des vingt-trois cartes en dépendent : `sd001a` les pose, `sd002`
Quicksilver, `sd003`/`sd004` Blasting Velocity, `sd006`/`sd007` Kinetic Flurry,
`sd008`/`sd009`/`sd010` Swift Strikes, `sd011`/`sd012` Top Speed, `sd014`
Explosive Touch, `sd015` Never Ending Spark et `sd016` Quick Adaptation les
lisent ; `sd017` No Outrunning This éteint la source.

**Aucun correctif moteur n'a été nécessaire pour cette mécanique.** `Enemy`
(`game/card/face/base/enemy.py:10`) et `Scheme2`
(`game/card/face/base/scheme.py:9`) héritent **déjà** de `CanPlaceCounter` :
poser un compteur sur un ennemi ou une manigance est natif.

| Besoin | Brique |
|---|---|
| poser un compteur | `Faces.PlaceCountersOn(cibles, 1, 'explosive', effect)` (`faces.py:206`) |
| plafonner à 1 **partout** | `AbilityFactory.WhenCardWouldBePlacedCounter(NonKeyword, None, 'explosive', …)` + `message.maximum = 1` (`counter.py:178`, `can_place_counter.py:56-60`) |
| balayer à la fin de la phase des joueurs | `AbilityFactory.WhenPlayerPhaseEnd` (`turn_phase.py:258`) + `face.RemoveCountersInternal("All", 'explosive', effect, forced=True)` |
| réagir au **retrait** | `AbilityFactory.AfterCardRemovedCounter(NonKeyword, None, 'explosive', …)` (`counter.py:31`) |
| réagir à la **pose** (sd015) | `AbilityFactory.AfterCounterPlacedOn(HeroResponse, None, 'explosive', …)` (`counter.py:97`) |
| cibler « qui porte un compteur » | `.SetTarget(Enemy, has_counter='explosive')` (`ability.py:702`, `card_finder/checker.py:346`) |

La fabrique toute faite `MaxCounterHere` ne vise que « This » (une seule carte) :
le plafond global passe donc par `WhenCardWouldBePlacedCounter(which_face=None)`,
`Condition.CheckWhichCard(None, …)` rendant toujours vrai
(`condition/card_type.py:98`) — c'est l'idiome d'un écouteur global.

**Les deux règles transverses de l'insert n'appartiennent à aucune carte : elles
sont portées par l'IDENTITÉ, et sur ses DEUX FACES** (`sd001a` **et** `sd001b`),
via `ReglesDesCompteursExplosifs()` dans
`src/cards/pack/speed/speed/__init__.py`. Raison : les compteurs doivent
survivre à un changement de forme, et le balayage doit tomber **même si Speed
finit la phase des joueurs en identité civile**. Une seule des deux faces est en
jeu à la fois, la règle n'est donc jamais appliquée en double. Le cas de test
599 exerce précisément cette moitié-là, en alter-ego.

Le dégât du retrait **n'est pas une attaque** : il part de `this.DealDamage`
depuis l'identité, sans `AttackProperty`, hors de toute fenêtre
`WhenUnitWouldAttack`. Aucune riposte, aucun re-déclenchement d'« après une
attaque ». Même chose pour le retrait de menace, qui n'est pas un contre
(`RemoveThreatFromSchemes`, la brique de `10004` Sub-Orbital Leap).

**L'interrupteur de l'obligation** (`sd017`) est un drapeau nommé sur
`effect.world` (`_speed_hyperkinetic_eteint`), levé par
`EteindreHyperkineticFuel` et rabaissé par une capacité temporaire
`WhenRoundEnd` posée sur **l'identité** — jamais sur l'obligation, qui part à la
défausse dans la foulée. Voie recommandée par le §3.1 du guide (« état
persistant maison »), déjà employée par `gwenpool` et par `wiccan`. Différence
avec `wc018` : ici le texte dit « until the end of the **NEXT** round », pas
« next player phase » — la capacité temporaire **laisse passer la première fin
de round** et ne rabaisse le drapeau qu'à la seconde.

**Le couplage `sd005` ↔ `sd001a`** est la seule dépendance inter-cartes du
pack. « I'm Out » imprime « If you would resolve Speed's *Hyperkinetic Fuel*
ability when playing this event, … **instead** » : c'est donc la capacité du
HÉROS qui doit demander « la carte que je vois payer est-elle `sd005` ? », la
carte n'ayant aucun moyen de se voir en train d'être payée. Rendu par la
constante partagée `CARTES_QUI_REMPLACENT_HYPERKINETIC_FUEL` et l'aide
`RemonterUnEvenementEtPiocher` (réutilisée mot pour mot par `sd001b`, qui
imprime la même phrase).

## Arbitrage tranché par l'utilisateur (documenté, non rediscuté)

1. **Aspect AGGRESSION** pour le deck de départ, tranché le 30/08/2026 (aucune
   decklist d'aspect fournie par l'auteur). Justification complète dans
   `metadata.aspect_note` de `deck/starter/speed.json` : le kit multiplie les
   attaques de base et Hyperkinetic Fuel exige de payer des **événements** en
   ressources énergie seules — Aggression est l'aspect le plus dense en
   événements et en icônes énergie, et il corrige l'ATQ 1 imprimée.

2. **`sd022` Conflicted Feelings appartient au `nemesis_set`, pas à la clé
   `obligations`**, confirmé par l'utilisateur le 30/08/2026 sur envoi de la
   découpe des deux bas de page. Le pack contient **deux** cartes de type
   Obligation, ce qu'aucun héros officiel n'a, et ce sont leurs bas de page qui
   les séparent : `sd017` porte « SPEED » et 2 icônes de bonus, avec le gabarit
   officiel mot pour mot (« You may flip to alter-ego form. Choose: … », modèle
   `01155` Affairs of State) ; `sd022` porte « **SPEED NEMESIS (5/5)** » et 1
   icône de bonus, et ne suit pas ce gabarit. `sd022` est donc la cinquième
   carte du set némésis, mise de côté au setup et mélangée au deck de rencontre
   quand `sd017` est révélée : elle arrive avec Coat of Arms, et sa clause
   « Coat of Arms cannot be damaged » mord vraiment. Seule `sd017` est dans
   `obligations`. La lecture alternative (deux obligations mélangées au deck du
   joueur) rendrait cette clause souvent inerte, puisque la carte pourrait
   sortir avant que le sbire n'existe.

3. **`sd021` Magic Chains — la flèche est un COÛT → un EFFET**, tranché par
   l'utilisateur le 30/08/2026 (« on suit la règle »). C'est la règle
   officielle : à gauche de la flèche le coût, à droite l'effet, et la capacité
   ne se déclenche que si le coût est intégralement payable. Elle vaut aussi
   pour une capacité **forcée** : les seules cartes rencontre du dépôt qui
   impriment une flèche dans un `Forced` l'emploient ainsi — `11014` Temporal
   Shield (« discard Temporal Shield → prevent all damage »), `11031` Chitauri
   Soldier, `16074` Biogram Image. Et quand une carte veut deux **conséquences**,
   elle les relie par « and » **sans** flèche : `02021` Pumpkin Bombs
   (« discard Pumpkin Bombs **and** take 2 indirect damage »).
   Conséquence en jeu : coût impayable (identité civile, ou héros déjà étourdi,
   ou Stalwart) → **ni étourdissement, ni défausse**, et l'attachement reste en
   jeu avec son +1 ATQ. La première version du module défaussait la carte dans
   tous les cas et rendait les chaînes à usage unique.

Le point ci-dessous a été tranché par Claude au moment de l'encodage des
données, et reste ouvert à révision :

4. **`01093` Tenacity volontairement absente** du deck de Speed : c'est le seul
   bloqueur d'autoplay officiel connu du projet. Voir la lecture de l'écart
   dans la section autoplay — le témoin `okoye`, lui, la contient.

## Choix tranchés par Claude, faute d'interlocuteur (session en arrière-plan)

1. **`sd006`/`sd007` Kinetic Flurry — la couleur du coût X.** Le moteur ne sait
   PAS restreindre la couleur d'un coût variable : le littéral de `Cost`
   (`element/cost.py:38-42`) énumère `"R"`, `"B"`, `"Y"`, `"RR"`… `"0".."4"`,
   il n'existe aucun « XY ». La seule carte officielle qui imprime « you can
   only spend [physical] resources to pay for this card » (`10002` Crushing
   Blow) contourne le problème en ayant un coût **fixe**, encodé `Cost: "R"` —
   impossible ici. **Repli retenu, plus sévère que la carte et jamais plus
   permissif** : X = `paye.GetColor("Y")`, l'énergie (et le wild) réellement
   payée. Une ressource physique ou mentale glissée dans le paiement n'achète
   **aucune** attaque supplémentaire : elle est perdue. Le joueur ne peut pas
   gagner d'attaque avec une couleur interdite ; il peut seulement gaspiller,
   ce que la carte lui épargnerait. Écart assumé, commenté dans `sd006.py`.
2. **`sd019` Coat of Arms — la fenêtre du [star].** Le texte imprimé dit
   « **When** Coat of Arms attacks, **if it deals damage** ». Les deux moitiés
   sont incompatibles à la même fenêtre : « si elle inflige des dégâts » ne peut
   se savoir qu'**après** la résolution. On s'accroche donc à
   `AfterUnitAttackUnit(…, dealt_damage=True)`, la seule fenêtre où la clause
   imprimée est décidable — comme `58026` Grim Reaper (« After Grim Reaper
   attacks **and defeats** an ally ») et `47011` Chamber.
3. **`sd016` Quick Adaptation — « +1 ATK and +1 THW for that use ».** La formule
   donne LES DEUX stats, pas « la stat employée » : rendue à la lettre par un
   seul `GainForThisActive(effect, message, attack=1, thwart=1)`. En jeu le
   résultat est le même (sur une attaque de base seul l'ATQ est lu, sur un
   contre de base seul le CTR), mais le code dit ce que la carte dit.
4. ~~**`sd021` Magic Chains — la flèche.**~~ **Ce choix était FAUX et a été
   corrigé le 30/08/2026** : il lisait « stun your hero → discard this card »
   comme deux conséquences, donc la carte partait même sans héros à étourdir.
   La règle officielle dit l'inverse, et le dépôt la confirme sans exception.
   Voir l'arbitrage n°3 de la section précédente.

## Écarts assumés, non corrigés

1. **Collision de noms « Quicksilver ».** `sd002` est un ALLIÉ nommé
   « Quicksilver » ; le catalogue contient déjà le HÉROS OFFICIEL `14001a` du
   même nom, dont **cinq** cartes (`14003`, `14008`, `14009`, `14010`, `14011`)
   font un `CardFinder(name="Quicksilver")` **non borné**. **La collision
   préexiste** : `15002` (pack `scw`) est déjà un allié « * Quicksilver ». Rien
   n'a donc été corrigé côté `qsv` — mais **aucune carte de ce pack ne fait de
   recherche par nom non bornée** : `sd002` n'agit que sur « This ». Même
   prudence pour « Speed » lui-même, qui collisionne avec l'allié officiel
   `15010` et le sbire `57060` : `sd014` redresse `message.trigger`, jamais un
   `CardFinder(name="Speed")`.
2. **`sd013` Mother's Protection est un duplicat volontaire de `wc015`.**
   Même nom, même coût, même ressource, même type, même trait, même texte au
   caractère près : l'auteur a réutilisé la carte de Billy pour son frère
   jumeau. Le module est **dupliqué** et non lié par `full_link` : une
   réimpression `full_link` hériterait du `set_name` « Wiccan » et ferait de
   `sd013` une carte signature de Wiccan (visible dans son deck, et refusée par
   le contrôle §5.2 du guide). Les deux fichiers doivent rester synchronisés à
   la main — c'est écrit en tête de `sd013.py`.
3. **`sd018` The Real Question meule le deck de rencontre s'il ne contient
   aucun attachement.** Le set némésis de Speed n'en compte que deux (`sd020`,
   `sd021`) ; une fois posés, il peut n'en rester aucun. Le moteur **ne boucle
   pas** : `Deck.DiscardUntil` (`deck.py:470`) parcourt un **instantané** du
   deck (`self.Get()[::-1]`), donc au plus une passe, et rend `None` si le deck
   se vide. C'est exactement le comportement des deux cartes officielles qui
   impriment la même phrase (`40093` The Senator's Support, `wd104`). Aucune
   garde supplémentaire n'a été ajoutée : en ajouter une divergerait du moteur.

## Outils exécutés depuis `.game-src`

- `tools/test_cards.py` : **4661 ok / 0 err**, 542 sans `GetAbilities`
  (référence relevée avant les scripts, dans ce même worktree : **4638 ok /
  0 err**, 539 sans `GetAbilities` — +23 cartes construites, +3 `__init__.py`
  de pack).
- `tools/verifier_prefixes.py` : OK — **5216 cartes, 28 préfixes déclarés,
  882 cartes fan-made**, aucun doublon, aucun préfixe non déclaré, aucun numéro
  emprunté.
- `tools/verifier_coherence_cartes.py` : **0 carte joueur sans classe d'aspect,
  0 obligation sans destinataire, 0 image manquante** (23 images
  `assets/pics/sd*.png`). Les collisions listées par l'outil sont toutes
  antérieures au pack.
  ⚠ Sa section « couverture des packs custom » **ignore le pack** : elle saute
  les `card_id` qui ne commencent pas par un chiffre
  (`if not cid[0].isdigit(): continue`, ligne 139), donc tous les préfixes
  alphabétiques (`wc`, `sd`…). Le calcul a été refait à la main avec la même
  règle de « doublon de code » : **18 cartes sujet d'un cas dédié + 5 couvertes
  par un doublon de code strictement identique = 23/23, 0 sans couverture,
  taux exercé 100 %**.
- `tools/verifier_desc_mots_cles.py speed` : OK — les 23 cartes ont un `desc`
  conforme à leur texte.
- `tools/verifier_cartes_en_jeu.py … speed` : OK — les 23 cartes portent ce que
  leur texte annonce (compteurs d'usage, Quickstrike, Permanent, `ATK+`…).
- `tools/verifier_noms_modules.py … speed` : OK — aucun nom inconnu.
- `tools/verifier_api_cartes.py` : **5205 fichiers, 4 en faute — aucun `sd*`**
  (les 4 sont antérieurs : `spot/sp018.py`, `web_of_deceit/underling/
  __init__.py`, `wd159.py`, `wd160.py`).
- Deck de départ (`tools/verifier_tous_les_decks.py`, `DECK_NOM=speed`) :
  `{"deck": "speed", "ok": true, "message": "identite sd001a, main 7, deck 33"}`.
  Avant les scripts il échouait sur `AssertionError: face.paper.card_id='sd003'`
  (`game/card/factory.py:120` exige exactement une capacité `Play` sur un
  Event) : c'était attendu, et c'est passé au vert avec les modules.
- Script anti-fuite « jamais une carte signature d'un autre héros dans un
  deck » (PROCESSUS-HEROS §10) : **0 résultat**, sur tous les decks de départ
  du dépôt, `speed` inclus.
- `tools/test_capacites.py` : **35 cas dédiés au pack `speed`, 35/35 verts**
  (indices **651 à 685**). Les 34 premiers ont été rejoués **d'un bloc** après
  le dernier correctif de l'agent ; le 35e (`sd021` en alter-ego) a été ajouté
  le 30/08/2026 avec la correction de la flèche, et les deux cas `sd021` ont
  alors été rejoués ensemble, verts tous les deux.
  Un cas par capacité distincte, un cas partagé pour chaque lot de cartes
  physiquement dupliquées, et deux ou trois cas pour chaque carte à branche
  conditionnelle (`sd001a`, `sd002`, `sd005`, `sd011`, `sd014`, `sd015`,
  `sd016`, `sd017`, `sd018`, `sd020`, `sd021`, `sd022`).
  ⚠ **L'ajout du 35e cas décale les indices** : les `sd022` sont désormais 628
  et 629, et non 627 et 628.
- `tools/autoplay.py` : **8 parties contre `rhino`, profil `equilibre`**, plus
  8 parties du témoin `okoye` dans la même fournée (détail ci-dessous).

> ⚠ **Indices décalés de +56 depuis la fusion dans `master` (30/08/2026).**
> Les numéros de cas cités DANS LE CORPS de cette fiche sont ceux de la
> branche `worktree-okoye`, avant l'arrivée des packs `dazzler`,
> `wolverine_x23`, `superior_iron_man` et `kate_bishop` qui les précèdent
> désormais dans `CAS`. Pour retrouver un cas, ajouter 56 à l'indice écrit.

### Preuve par substitution, module par module

**21 modules retirés puis remis**, chaque cas dont le nom commence par le
`card_id` du module rejoué sans lui. Résultat : **31 des 35 cas passent au
ROUGE** sans leur module.

Les **quatre** qui restent verts sont des **contre-épreuves**, et c'est
exactement ce qui en fait des contre-épreuves — elles affirment que RIEN ne se
passe :

| cas | ce qu'il affirme | pourquoi il reste vert sans module |
|---|---|---|
| 596 | payé en physique → **aucun** compteur | sans `sd001a.py`, aucun compteur non plus |
| 602 | sans compteur → Quicksilver **encaisse** son dégât consécutif | sans `sd002.py`, il l'encaisse aussi |
| 609 | sans compteur → Top Speed ne fournit que 2, la carte à 3 reste **injouable** | sans `sd011.py`, elle en fournit 1, donc injouable aussi |
| 627 | coût impayable → Magic Chains **reste** en jeu | sans `sd021.py`, elle reste en jeu aussi |

Pour chacune, la preuve de présence du module est son cas jumeau positif (595,
601, 608, 626), qui est bien rouge sans module.

Les **5 exemplaires en double** (`sd004`, `sd007`, `sd009`, `sd010`, `sd012`)
n'ont pas de cas sujet propre : leur code est **strictement identique** à celui
de leur exemplaire de référence (diff vide hors en-tête de commentaire), ce que
le calcul de couverture vérifie mécaniquement. Convention `ok004`/`ok005`,
`il021`/`il022`, `wc003`/`wc004`.

## Autoplay : 8 parties, témoin `okoye`

**Grep exhaustif `NameError|AttributeError|TypeError|KeyError|AssertionError`
sur les 16 journaux : 0 partout.** Grep élargi `traceback|exception`
(insensible à la casse) : **0 partout aussi**. **0 partie bloquée**
(`incidents: 0` dans les deux rapports).

| | `speed` | `okoye` (témoin) |
|---|---|---|
| parties | 8 | 8 |
| victoires | 0 | 0 |
| parties bloquées | 0 | 0 |
| rounds tenus (moyenne) | 4,25 | 4,125 |
| fin par complot achevé | 4/8 | 6/8 |
| fin par élimination | 4/8 | 2/8 |
| tracebacks | 0 | 0 |

**Lecture de l'écart.** Aucun des deux ne bloque, aucun ne produit de
traceback, et les deux tiennent le même nombre de rounds (4,25 contre 4,125 :
un huitième de round d'écart sur 8 parties, c'est du bruit). La seule
différence est la **cause** de la défaite : Speed meurt plus souvent (4/8 contre
2/8) et laisse moins souvent le complot s'achever. C'est cohérent avec le kit —
Speed a **ATQ 1 / CTR 1** et un deck Aggression qui pousse à attaquer : le
pilote frappe, encaisse, et perd par élimination là où Okoye (leadership,
alliés, CTR 2) meurt de la menace. **Ce n'est pas un signal de défaut** : c'est
un profil de deck.
`01093` Tenacity, le seul bloqueur officiel connu du projet, est **dans le deck
d'Okoye et pas dans celui de Speed** — et pourtant aucun des deux ne bloque : la
comparaison n'est donc pas faussée dans le sens qui compte.

**Couverture des cartes du pack dans les journaux** (présence du `card_id`) :
`sd001a`, `sd001b`, `sd010` et `sd017` **8/8** ; `sd002`, `sd003`, `sd005`,
`sd011`, `sd013`, `sd016` 5/8 ; `sd007`, `sd012`, `sd015` 4/8 ; `sd008`,
`sd014`, `sd018`, `sd019`, `sd020`, `sd021`, `sd022` 3/8 ; `sd004`, `sd006`,
`sd009` 2/8. **Aucune carte absente des 8 journaux.**

**Lecture ligne à ligne d'un journal** (partie 5, la plus lisible) : le cycle
complet de la mécanique centrale y est visible, tel qu'écrit sur l'insert —

```
> 216: Speed would play [(14,sd008) Swift Strikes] with (YY)
> 217: [(01,sd001a) Speed] activates, targets [[(01,sd001a) Speed]]
> 218: [(49,01094) Rhino] would place 1 'explosive' counter ([(01,sd001a) Speed])
> 219: [(49,01094) Rhino] reçoit 1 compteur(s) « explosive » ([(01,sd001a) Speed])
> 220: [(14,sd008) Swift Strikes] activates, targets [[(49,01094) Rhino]]
> 223: [(01,sd001a) Speed] would deal 3 damage to [(49,01094) Rhino]
...
> --- Fin de phase : Player ---
> 249: [(49,01094) Rhino] perd 1 compteur(s) « explosive » ([(01,sd001a) Speed])
> 250: [(01,sd001a) Speed] would deal 1 damage to [(49,01094) Rhino]
> 254: [(49,01094) Rhino] perd 1♡
> 255: [(49,01094) Rhino] was defeated by [(01,sd001a) Speed]
```

Ligne 216 : Swift Strikes est payée **uniquement en énergie**. Ligne 217-219 :
Hyperkinetic Fuel se déclenche **avant** que l'événement se résolve (c'est un
Interrupt) et pose le compteur sur Rhino. Ligne 220-223 : Swift Strikes résout
ses 3 dégâts. Ligne 249-255 : **à la fin de la phase des joueurs**, le compteur
est retiré et inflige son dégât — qui achève Rhino et fait avancer le vilain
d'un stade. Pose, lecture, retrait et effet du retrait : les quatre moments de
l'insert dans une seule partie.

Le journal de la même partie liste aussi, dans les actes du pilote,
`Hyperkinetic_Fuel`, `Put_an_explosive_counter_on_an_enemy_or_scheme`,
`Generate_1_additional_[energy]_resource(s)_—_you_cannot_play_cards_for_the_rest_of_the_turn`,
`Accelerated_Perception` et
`Exhaust_Thomas_Shepherd_→_remove_No_Outrunning_This_from_the_game` : cinq
capacités du pack exercées en partie réelle, pas seulement au banc d'essai.

## Bugs réels trouvés et corrigés (preuve rouge/vert)

### 1. Bug MOTEUR : `AbilityFactory.UnitCannotTakeDamage` levait `NameError` à chaque appel

**Symptôme** : `tools/test_cards.py` **4660 ok / 1 err** —

```
"cards.pack.speed.speed_nemesis.sd022": "abilities: NameError: name 'AbilityFactory' is not defined"
```
puis, une fois ce premier nom importé :
```
"cards.pack.speed.speed_nemesis.sd022": "abilities: NameError: name 'BuffCannotTakeDamage' is not defined"
```

**Cause** : `game/ability/factory/damage.py` fait `from . import *` alors que
`game/ability/factory/__init__.py` n'a pas encore exposé `AbilityFactory`
(ligne 21, **après** l'import des sous-fabriques) ni `game.buff` (ligne 27) :
ces noms n'entrent **jamais** dans les globales du module. Toutes les autres
méthodes du fichier qui appellent `AbilityFactory` sont protégées par l'import
local de `UnitCannotTakeMoreDamageEachPhase` (ligne 195) ; `UnitCannotTakeDamage`
était **la seule sans**. Aucune carte du dépôt ne l'appelait — le défaut dormait.

**Correctif** : deux imports locaux, l'idiome du fichier.

### 2. Bug MOTEUR : `UnitCannotTakeDamage` était **inerte** une fois le plantage levé

**Symptôme** : cas `sd022 … Coat of Arms ne peut pas subir de dégâts` **rouge** :
`degats sur sd019 = 1 (attendu 0)`. La carte était bien en jeu, le buff bien
posé (`[(81,sd019)] appliquent [(82,sd022)]` dans le journal), et les dégâts
passaient quand même.

**Cause** : `BuffCannotTakeDamage` (`game/buff/buff.py:67`) est une **classe
marqueur vide**, et **aucun chemin de dégâts ne la consulte** :
`grep -rn BuffCannotTakeDamage src/` ne trouve que sa définition, son export et
cet unique appel. Son voisin `BuffCannotBeStunned`, lui, est bien lu
(`can_status.py:152`, `status/stunned.py:16`) — c'est ce qui rend l'oubli
visible. Poser le buff seul laissait la carte subir les dégâts **sans que rien
ne le signale**.

**Correctif** : la fabrique garde le buff (il porte l'affichage du plateau) et
**ajoute la vraie prévention**, par la même voie que `ThisCannotTakeDamageWhile`
(`21160` Loki), seul chemin de ce fichier qui prévient réellement. Elle rend
désormais une **liste**, d'où le `*` devant l'appel dans `sd022.py`. Aucune
carte du dépôt n'utilisait cette fabrique : la modification n'affecte rien
d'autre.

**Rouge/vert** : rouge = `degats sur sd019 = 1 (attendu 0)` ; vert = `etat
conforme`, avec `en_jeu: ["sd022"]` qui vérifie au passage que l'obligation
**reste** en jeu (modèle `28021` Weight of the World). `test_cards` : **4661 ok
/ 0 err**.

### 3. `sd016` Quick Adaptation — la chaîne « You » ne veut rien dire pour cette fabrique

**Symptôme** : cas 616 rouge (`degats sur 01094 = 1 (attendu 2)`) et 617 rouge
(`menace sur 01097b = 5 (attendu 4)`). La carte était en jeu, la cible portait
son compteur, et **rien** ne se déclenchait.

**Cause** : `WhenUnitWouldAttackOrThwart.check_trigger`
(`do_attack.py:1241-1242`) appelle `Condition.CheckWhichCard(attacker, …)`
**directement**, sans passer par `Condition.GetYouRule` — contrairement à
`AfterUnitAttackUnitInternal` (`do_attack.py:374`), qui, lui, traduit « You ».
Or `CheckWhichCard` connaît « YouPlayer », « YourIdentity », « YourHero »… mais
**pas « You »** (`condition/card_type.py:127-190`) : la condition était
**toujours fausse**.

**Correctif** : côté carte, `"YourIdentity"` au lieu de `"You"`. Pas côté
moteur : une carte n'a pas à deviner quelles fabriques traduisent « You », mais
corriger la fabrique changerait le sens de toutes celles qui l'emploient déjà.

**Rouge/vert** : rouge = 1 dégât / 5 menaces ; vert = 2 dégâts (ATQ 1 + 1) et
4 menaces (CTR 1 + 1). La paire de cas **616 / 617** couvre les deux verbes
imprimés, et le cas **607** (même montage **sans** Quick Adaptation) donne 5 :
la différence est la preuve.

### 4. `sd020` Inspirational Art — le `+1 boost` était effacé par le déplacement de la carte

**Symptôme** : cas 623 rouge, `degats sur l'identite = 1 (attendu 4)`. Le
journal montrait pourtant l'icône ajoutée, **deux lignes avant qu'elle
disparaisse** :

```
> 53: [(82,01106) Stampede ?] gains 1 boost icons
> 54: [[(82,01106) Stampede]] moved to boosting area
> 55: [(82,01106) Stampede] would count boost icons (✶)
```

**Cause** : la capacité était accrochée à `WhenBoostCardWouldTurnedFaceUp`, le
message « would » de l'étape (a) de `CanBoost.ResolveBoostCards`
(`can_boost.py:46`). Juste après, la carte est **déplacée** vers la zone de
bonus — et entrer dans une nouvelle zone déclenche `OnResetKeywords`, qui remet
le compteur `Boost` à sa valeur imprimée. Le `+1` ne survivait pas jusqu'au
comptage de l'étape (c).

**Correctif** : `WhenBoostCardTurnedFaceUp` (`boost.py:241`, modèle `08004`
Attacrobatics), envoyé **après** le déplacement et **avant** le comptage. C'est
aussi la lettre du texte imprimé : « when a boost card is **turned faceup** ».

**Rouge/vert** : rouge = 3 dégâts (Rhino ATQ 2 + 1 icône imprimée) ; vert =
4 dégâts (2 + 2 icônes). La substitution du module donne exactement 3 : le
chiffre distingue les deux situations sans ambiguïté.

### 5. `sd011`/`sd012` Top Speed — une `AssertionError` avalée en autoplay

**Symptôme** : **1 traceback** dans la partie 6 de la première fournée
d'autoplay, avalée en silence par le moteur (la partie continuait) —

```
> 37: [(17,sd011) Top Speed] activates, targets [[(17,sd011) Top Speed]]
> 38: Speed gains resource YY from [(17,sd011) Top Speed], total YY
<D> Traceback (most recent call last):
<D>   File ".../engine/controller/controller.py", line 274, in ChoiceOne
<D>     assert len(effect_descriptors) == 1 and effect_descriptors[0].target_num_range[0] == 0
<D> AssertionError: True
```

**Cause** : la question « you may » était écrite comme un choix **forcé à deux
options** (`AskChooseOneText([True, False], …)`, qui fabrique un
`ChooseAbilities(forced=True)`). Quand les **deux exemplaires** de Top Speed
financent le **même paiement**, le pilote d'autoplay voit deux fois la même
question avec la même empreinte de plateau, son garde-fou anti-répétition
(`MAX_REPETITIONS`, `tools/autoplay.py:47`) épuise ses deux options, puis
répond « 0 » — ce que `ChoiceOne` refuse sur un choix forcé à plus d'une option.

**Correctif** : une **seule** option, refusable —
`ChooseAbilities(effect, ForChoiceAbility(…).SetHasNoTargetEffect(),
forced=False)`, l'idiome du dépôt pour « you may » (modèle
`determination/__init__.py:64-71`). Répondre « 0 » devient une réponse légale du
protocole : l'assertion ne peut plus partir, et le refus est vraiment un refus.
C'est aussi une lecture **plus fidèle** du texte imprimé : « you may » n'offre
pas deux actions, il en offre une, facultative.

**Rouge/vert** : rouge = 1 traceback sur 8 journaux `speed` ; vert = **0
traceback sur les 16 journaux** de la fournée complète, et les trois cas Top
Speed (608, 609, 610) toujours verts après le changement.

## Trois limites du harnais, documentées et non masquées

1. **Aucune commande Puzzle ne fait CONTRER un héros.** `Puzzle.Attack` couvre
   l'attaque de base (`MakeBasicPowerLikeInTurn([face], …, ["ATK"])`), il n'y a
   pas d'équivalent `["THW"]`. Les moitiés « contre de base » de `sd014` et
   `sd016` sont donc exercées **par une autre carte du pack** : Swift Strikes
   (`sd008`) offre un contre de base contre une manigance marquée, et c'est lui
   qui déclenche les deux (cas 613 et 617). Ce n'est pas un contournement : le
   déclencheur exercé est bien `AfterUnitUseBasicPower(powers=["THW"])` et
   `WhenUnitWouldThwart`.
2. **Aucune commande Puzzle n'avance de phase ni de round.** Le balayage des
   compteurs (règle de l'insert) et la durée de l'interrupteur de `sd017` sont
   exercés par des **sondes in-process** : les vérificateurs renvoient dans le
   monde `Message.WhenPhaseEnd(phase_id, "Player", monde)` et
   `Message.WhenRoundEnd(monde)`, **exactement** les messages que le moteur
   émet au même moment. La seule chose court-circuitée, c'est l'attente du tour
   de jeu correspondant. Convention déjà employée par `wiccan` (cas `wc018`).
3. **Le pilote de `test_capacites` compte des RESSOURCES, pas des COULEURS.**
   `payer()` calcule `besoin = len(cout)` puis un poids `len(couleur)` par
   carte : `01088` Energy (« YY ») « couvrait » donc à lui seul un coût
   `[energy][physical]`, et le paiement partait sans le physique. Les deux cas à
   coût bicolore (`sd020`, `sd022`) financent donc avec des cartes à **une seule
   icône imprimée** (`sd003` = [energy], `sd008` = [physical], `sd005` =
   [mental]). Limite du harnais, pas des cartes — notée ici pour le prochain
   pack à coût bicolore.

---

# Fiches PROCESSUS-CARTE, une par card_id

### sd001a : * Speed (face héros)

- [x] Étape 2 : cartes de référence :
      **Hyperkinetic Fuel** → `AbilityFactory.WhenPlayerWouldPlayCard`
      (`factory/play.py:191`), la fenêtre exacte du texte : `CardPlayer.Play`
      (`card_player.py:134-139`) paie d'abord le coût (`ProcessSelfCost`),
      envoie **ensuite** `WhenPlayerWouldPlayCard`, et ne résout l'événement
      qu'après. Modèle du test de couleur : Hulk Smash (`10003`), Sub-Orbital
      Leap (`10004`), Gamma Strike (`bw006`) — tous `OnlyHasColor` pour « you
      paid for this card using only [X] resources ».
      **Cible** → `.SetTarget("Enemy|Scheme")` (`selector_target.py:36`),
      modèles `53002` Redwing et `52002` Smooth as Silk.
      **Règles de l'insert** → `WhenCardWouldBePlacedCounter` +
      `WhenPlayerPhaseEnd` + `AfterCardRemovedCounter` (voir la section
      « Mécanique centrale »), modèle du plafond : `ht001a` Human Torch
      (plafond de 3 compteurs flamme).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : **`an event`**
      (`which_card=Event` : ni allié, ni amélioration, ni soutien) ;
      **`only [energy]`** (`OnlyHasColor("Y")`, donc `y + g == total` : le WILD
      compte comme énergie, et un paiement de **0 ressource rend False**, un
      événement coût 0 ne déclenche donc jamais rien — `rbyg.py:47-55`) ;
      **`Interrupt`** (le compteur est posé AVANT la résolution de l'événement,
      c'est tout le design du pack) ; **`an enemy or scheme`** (pas seulement le
      complot principal) ; **pas de limite imprimée** (aucun
      `LimitOncePerRound`). Le « instead » de `sd005` est un **couplage
      inter-cartes** traité ici et non dans `sd005.py` : c'est la résolution de
      CETTE capacité que le texte de `sd005` remplace.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : PV 9, ATQ 1, CTR 1, DEF 2, MNG 5 (`desc`
      et scan identiques) ; **1** compteur posé ; plafond **1** par carte
      (insert) ; **1** dégât au retrait.
      Résultat : conforme.
- [x] Étape 7 : quatre cas, un par capacité ou par règle transverse :
      - `sd001a … payé UNIQUEMENT en energie` (595) : `main_exclusive` à
        `01088` (YY). Rouge sans module (`01094.explosive=0`), vert avec.
      - `sd001a … NE part PAS payé en PHYSIQUE` (596) : contre-épreuve,
        `main_exclusive` à `01090` (RR). Vert sans module **par construction**
        (voir le tableau des contre-épreuves).
      - `sd001a … PLAFOND de 1` (597) : `Puzzle.Counter(…, 5)` → 1. Rouge sans
        module (`=5`), vert avec.
      - `sd001a … balayage de fin de phase, 1 dégât` (598) : sonde
        `WhenPhaseEnd("Player")`. Rouge sans module (« le compteur explosif est
        encore là »), vert avec.
- [x] Étape 8 : autoplay ciblé : `sd001a` présente dans **8/8** parties ; le
      journal de la partie 5 montre le cycle complet pose → attaque → retrait →
      dégât (extrait cité plus haut) ; 0 traceback.

Carte terminée : OUI

### sd001b : * Thomas Shepherd (face alter-ego)

- [x] Étape 2 : cartes de référence :
      **« Action: » nu sur une face alter-ego** → `AbilityType.Action` +
      `.LimitOncePerRound()`, comme `wc001b` Billy Kaplan, `ss001b` Kaine
      Parker, `10001b` Bruce Banner et `01029b` Tony Stark. `AlterEgoAction`
      est réservé aux cartes JOUEUR qui doivent déclarer ce mode.
      **remélanger un événement + piocher** → `60014` Karen Page et `ok011`
      Upanga, même couple `Search.PlayerCard(include_discard_pile=True,
      finder=…)` + `Faces.ShuffleAllTo(…, player_deck, …)`.
      **Règles de l'insert** → mêmes trois capacités que `sd001a`, dupliquées et
      non héritées.
- [x] Étape 5 : mots-pièges : **`1 event`** (`CardFinder(card_type=Event)`, pas
      n'importe quelle carte) ; **`Then, draw 1 card`** — la pioche est
      **inconditionnelle**, pas « if you do » : une défausse sans le moindre
      événement pioche quand même ; **`Limit once per round`**
      (`.LimitOncePerRound()`). Les règles de l'insert sont posées ICI AUSSI :
      sans elles, finir la phase des joueurs en identité civile laisserait les
      compteurs en place pour toujours.
      Résultat : conforme.
- [x] Étape 6 : nombres : PV 9, REC 3, MNG 6 ; **1** événement remélangé,
      **1** carte piochée.
      Résultat : conforme.
- [x] Étape 7 : deux cas :
      - `sd001b … balayage EN ALTER-EGO, 1 menace retirée` (599) : aucun
        `ChangeToFace` (la partie démarre en alter-ego), sonde
        `WhenPhaseEnd("Player")`, complot posé à 5 → 4. Rouge sans module
        (« la règle de l'insert ne joue pas quand Speed finit la phase en
        alter-ego »), vert avec.
      - `sd001b … Accelerated Perception` (600) : `sd003` semée dans la
        défausse, `cibles` la désigne (sinon le pilote prend le premier
        événement légal, et `main_exclusive` en jette d'autres à la défausse).
        Rouge sans module (`n'offre aucune action en jeu`), vert avec.
- [x] Étape 8 : autoplay ciblé : `sd001b` présente dans **8/8** parties ;
      `Accelerated_Perception` figure dans les actes du pilote de plusieurs
      parties ; 0 traceback.

Carte terminée : OUI

### sd002 : * Quicksilver (allié signature)

- [x] Étape 2 : cartes de référence : **`* Cosmo` (`stld/17020.py`)**, seul
      allié du dépôt qui annule ses dégâts consécutifs sous condition — même
      couple `AbilityFactory.WhenUnitWouldAttackOrThwart(Interrupt, "This", …)`
      (`do_attack.py:1225`) + `message.DoesNotTakeConsequentialDamage(effect)`
      (`sender_damage.py:178` pour l'attaque, `sender_friend.py:61` pour le
      contre). Une seule fabrique couvre les deux verbes imprimés.
- [x] Étape 5 : mots-pièges : **`attacks OR thwarts`** (une fabrique, deux
      messages, jamais un `if`) ; **`an enemy or scheme WITH an explosive
      counter`** (`UneCibleDeCeMessagePorteUnCompteur`, qui lit
      `attacked_targets` sur une attaque et `schemes` sur un contre) ;
      **`for that use`** (le drapeau vit sur le message de CETTE utilisation) ;
      **`2*`** sur ATQ et CTR = 1 dégât consécutif, lu **nativement**
      (`can_attack.py:48-52`) — rien à coder pour la valeur, la capacité ne fait
      que l'annuler. Aucune recherche par nom : la collision « Quicksilver »
      est évitée par construction.
      Résultat : conforme.
- [x] Étape 6 : nombres : coût 4, PV 3, ATQ 2*, CTR 2*, ressource wild.
      Résultat : conforme.
- [x] Étape 7 : deux cas, une preuve et sa contre-épreuve :
      - `sd002 … AUCUN dégât consécutif` (601) : compteur sur Rhino,
        `Puzzle.Attack('sd002')`. Rouge sans module (`degats sur sd002 = 1`),
        vert avec (0).
      - `sd002 … contre-épreuve SANS compteur` (602) : même montage sans le
        compteur → 1 dégât consécutif. Vert sans module **par construction**.
- [x] Étape 8 : autoplay ciblé : `sd002` présente dans **5/8** parties ;
      0 traceback.

Carte terminée : OUI

### sd003 : Blasting Velocity (exemplaire 1/2)

- [x] Étape 2 : cartes de référence :
      **retrait de menace** → `10004` Sub-Orbital Leap, même
      `.SetLabel('thwart')` + `.SetTarget(Scheme2)` +
      `this.RemoveThreatFromSchemes(effect.targets, N, effect)`.
      **attaque de base offerte** → `bw024` Strong as Silk, qui imprime la même
      tournure « make a basic attack **without exhausting** » et emploie
      `face.BasicAttack(cibles, effect)`.
      **ciblage restreint** → filtre `has_counter` de `CardFinder`
      (`checker.py:346`), exposé par `SetTarget` (`ability.py:702`).
- [x] Étape 5 : mots-pièges : **`a scheme`** (`Scheme2`, jamais `MainScheme`
      seul) ; **`an enemy WITH an explosive counter on it`**
      (`has_counter=COMPTEUR_EXPLOSIF` : on ne peut pas désigner un ennemi non
      marqué) ; **`without exhausting`** (`BasicAttack` n'incline rien, et
      `IsCanAttack` — `can_attack.py:691` — ne teste PAS l'inclinaison :
      l'attaque part même héros incliné) ; **`Make a basic attack`** (l'attaque
      part du HÉROS, `joueur.GetHero()`, pour employer son ATQ — modèle
      `01053`). Garde explicite quand aucun ennemi n'est marqué : rien ne se
      passe, sans erreur. Choix imbriqué (`ChooseAbilities`) et non
      `.SetTarget2` : leçon `hd009`, le pilote n'alimente pas `effect.targets2`.
      ⚠ **Miroir de `sd008`, pas sa jumelle** : ici menace **puis** attaque, sur
      un ENNEMI marqué ; là-bas dégâts **puis** contre, sur une MANIGANCE
      marquée.
      Résultat : conforme.
- [x] Étape 6 : nombres : coût 2, ressource [energy], **3** menaces retirées.
      Résultat : conforme.
- [x] Étape 7 : un cas, les deux moitiés mesurées séparément :
      `sd003 … 3 menaces PUIS attaque de base` (603) — héros **incliné** au
      départ (preuve du « without exhausting »), paiement en PHYSIQUE pour que
      Hyperkinetic Fuel ne pose pas un second compteur, attendu = menace 6→3 et
      1 dégât sur Rhino. Rouge sans module (`menace = 6` et `degats = 0`), vert
      avec.
- [x] Étape 8 : autoplay ciblé : `sd003` présente dans **5/8** parties ;
      0 traceback.

Carte terminée : OUI

### sd004 : Blasting Velocity (exemplaire 2/2)

- [x] Étape 2 : identique à `sd003` (même texte imprimé, deux `card_id`). Code
      dupliqué à l'identique, commentaire complet sur `sd003`, pointeur bref
      ici — convention `ok004`/`ok005`, `il021`/`il022`, `wc003`/`wc004`.
- [x] Étape 5 : mêmes mots-pièges que `sd003`, vérifiés sur le même texte.
      Résultat : conforme.
- [x] Étape 6 : mêmes nombres. Résultat : conforme.
- [x] Étape 7 : couverte par le cas de `sd003` — code **strictement identique**
      (diff vide hors en-tête de commentaire), vérifié mécaniquement par le
      calcul de couverture (`sd004 = sd003`).
- [x] Étape 8 : autoplay ciblé : `sd004` présente dans **2/8** parties ;
      0 traceback.

Carte terminée : OUI

### sd005 : "I'm Out"

- [x] Étape 2 : cartes de référence :
      **annulation** → `mw009` Foresight, modèle le plus proche (un Événement,
      un Hero Interrupt, rien d'autre autour) : même
      `AbilityFactory.WhenPlayerRevealCard(HeroInterrupt, "You", None, "All", …,
      from_encounter=True)` + `message.CancelAllEffectsAndDiscardIt(effect)`.
      Le libellé imprimé est celui de Spycraft (`08018`) et Lucky Break
      (`40048`), mot pour mot.
      **branche « instead »** → aide partagée `RemonterUnEvenementEtPiocher`,
      la même que `sd001b`.
- [x] Étape 5 : mots-pièges : **`cancel THE EFFECTS`** → niveau `"All"` et non
      `"WhenRevealed"` : mots-clés et déferlement compris
      (`sender_card.py:473-476`, leçon Dazzler n°5) ; **`and discard it`**
      (`discard_it=True`) ; **`When you reveal an encounter card`**
      (`from_encounter=True`, sans quoi une révélation depuis la défausse
      compterait) ; **`instead`** — il remplace **la résolution de Hyperkinetic
      Fuel**, PAS l'annulation, qui reste due dans tous les cas ; **`when
      playing this event`** → le test appartient à `sd001a`, cette carte n'ayant
      aucun moyen de se voir en train d'être payée.
      Résultat : conforme.
- [x] Étape 6 : nombres : coût 2, ressource [mental], **1** événement remélangé,
      **1** carte piochée.
      Résultat : conforme.
- [x] Étape 7 : deux cas, un par bloc imprimé :
      - `sd005 … annulée et défaussée` (604) : `Puzzle.Reveal('sd020')` — un
        attachement qui s'attacherait au vilain s'il n'était pas annulé, donc
        son absence du jeu est la preuve. Paiement en PHYSIQUE pour rester sur
        cette branche. Rouge sans module (`sd020 est encore en jeu`), vert avec.
      - `sd005 … branche « instead »` (605) : paiement en ÉNERGIE (`01088`),
        vérificateur dédié qui contrôle les **trois** conséquences — l'événement
        remonte, **aucun compteur explosif en jeu**, et l'annulation a quand
        même eu lieu. Rouge sans module, vert avec.
- [x] Étape 8 : autoplay ciblé : `sd005` présente dans **5/8** parties ;
      0 traceback.

Carte terminée : OUI

### sd006 : Kinetic Flurry (exemplaire 1/2)

- [x] Étape 2 : cartes de référence : **`14006` Speed Cyclone**, l'événement à
      coût X de Quicksilver lui-même — seul précédent exact du dépôt pour
      `desc.Cost = "X"`. Dégâts par `this.DealDamage` (modèle `01087`
      Haymaker), qui **déclenche bien la riposte** dans ce moteur (prouvé par le
      cas `wc005` contre M.O.D.O.K.).
- [x] Étape 5 : mots-pièges : **`Choose an enemy`** puis **`that enemy`** — la
      cible est choisie UNE SEULE FOIS (`.SetTarget(Enemy)`, portée (1,1)) et
      toutes les itérations la visent ; **`X times`** → X `DealDamage`
      **séparés**, pas un paquet de 2X : chaque salve est une attaque distincte,
      une riposte mord X fois ; **`3 damage instead if…`** → condition
      **réévaluée à chaque itération** (le test est dans la boucle) ; **`only
      [energy] resources`** → écart assumé documenté plus haut (le moteur ne
      sait pas colorer un coût X). La boucle s'arrête si la cible quitte le jeu.
      Résultat : conforme.
- [x] Étape 6 : nombres : coût X, ressource [energy], **2** dégâts de base,
      **3** avec compteur.
      Résultat : conforme.
- [x] Étape 7 : un cas : `sd006 … X attaques SÉPARÉES à 3 dégâts` (606) —
      `surpayer: True` (sans quoi un coût X annonce 0 et la carte paraît
      inerte, piège du §8), `01088` fournit 2 énergies → X = 2, compteur posé →
      3 dégâts par attaque, **6 attendus**. À 2 dégâts on lirait 4 : les deux
      branches sont distinguables. Rouge sans module (`degats = 0`), vert avec.
- [x] Étape 8 : autoplay ciblé : `sd006` présente dans **2/8** parties ;
      0 traceback.

Carte terminée : OUI

### sd007 : Kinetic Flurry (exemplaire 2/2)

- [x] Étape 2 : identique à `sd006`. Code dupliqué, commentaire complet sur
      `sd006`.
- [x] Étape 5 : mêmes mots-pièges. Résultat : conforme.
- [x] Étape 6 : mêmes nombres. Résultat : conforme.
- [x] Étape 7 : couverte par le cas de `sd006` (code strictement identique,
      `sd007 = sd006`).
- [x] Étape 8 : autoplay ciblé : `sd007` présente dans **4/8** parties ;
      0 traceback.

Carte terminée : OUI

### sd008 : Swift Strikes (exemplaire 1/3)

- [x] Étape 2 : cartes de référence :
      **dégâts** → `01087` Haymaker, même structure exacte
      (`.SetPlay().SetLabel('attack').SetTarget(Enemy)` +
      `this.DealDamage(effect.targets, 3, effect)`).
      **contre de base offert** → `heros.BasicThwart(cibles, effect)`
      (`can_thwart.py:188`), pendant exact du `BasicAttack` de `bw024`.
      **ciblage restreint** → `has_counter` sur `Scheme2`.
- [x] Étape 5 : mots-pièges : **`a scheme WITH an explosive counter`**
      (`Scheme2` + `has_counter`, pas `MainScheme`) ; **`without exhausting`**
      (`BasicThwart` n'incline rien, `IsCanThwart` ne teste pas l'inclinaison) ;
      **`Make a basic thwart`** (part du HÉROS, pour employer son CTR) ; garde
      explicite quand aucune manigance n'est marquée. ⚠ **Miroir de `sd003`** :
      dégâts d'abord, CONTRE ensuite ; ressource imprimée **PHYSIQUE** ici, donc
      Swift Strikes ne pose un compteur que si on la paie **avec autre chose que
      sa propre icône**.
      Résultat : conforme.
- [x] Étape 6 : nombres : coût 2, ressource [physical], **3** dégâts.
      Résultat : conforme.
- [x] Étape 7 : un cas : `sd008 … 3 dégâts PUIS contre de base` (607) — héros
      **incliné** au départ, complot à 6 → 5 (CTR 1), Rhino à 3 dégâts. Rouge
      sans module (`menace = 6`, `degats = 0`), vert avec. Le cas 617 rejoue
      **exactement ce montage avec Quick Adaptation en jeu** et lit 4 : la paire
      prouve le +1 CTR.
- [x] Étape 8 : autoplay ciblé : `sd008` présente dans **3/8** parties ;
      0 traceback.

Carte terminée : OUI

### sd009 : Swift Strikes (exemplaire 2/3)

- [x] Étape 2 : identique à `sd008`. Code dupliqué, commentaire complet sur
      `sd008`.
- [x] Étape 5 : mêmes mots-pièges. Résultat : conforme.
- [x] Étape 6 : mêmes nombres. Résultat : conforme.
- [x] Étape 7 : couverte par le cas de `sd008` (`sd009 = sd008`).
- [x] Étape 8 : autoplay ciblé : `sd009` présente dans **2/8** parties ;
      0 traceback.

Carte terminée : OUI

### sd010 : Swift Strikes (exemplaire 3/3)

- [x] Étape 2 : identique à `sd008`. Code dupliqué.
- [x] Étape 5 : mêmes mots-pièges. Résultat : conforme.
- [x] Étape 6 : mêmes nombres. Résultat : conforme.
- [x] Étape 7 : couverte par le cas de `sd008` (`sd010 = sd008`).
- [x] Étape 8 : autoplay ciblé : `sd010` présente dans **8/8** parties ;
      0 traceback.

Carte terminée : OUI

### sd011 : Top Speed (exemplaire 1/2)

- [x] Étape 2 : cartes de référence : **`58006` Energy Siphon** (Wonder Man) —
      « When you spend this card, take up to 3 damage → this card generates 1
      additional [energy] resource for each damage taken this way ». Même forme
      au mot près : une ressource dont le RENDEMENT est décidé au moment où on
      la dépense. Même couple
      `DoDiscardThisToGenerateResources(Interrupt, res_fn=…)` +
      `.SetCostFunc(CostFunc.Custom(None, …))` **et**
      `CheckThisCanDropPay(…)` (sans cette seconde capacité, le moteur ne
      proposerait jamais la carte pour un coût de 2 ou 3, et le bonus serait
      inatteignable). Choix refusable : `determination/__init__.py:64-71`.
      **Restriction** → `AbilityFactory.PlayersCannotPlayCardWhile`
      (`factory/player.py:8`), en temporaire sur l'identité,
      `until_turn_end=True`.
- [x] Étape 5 : mots-pièges : **`you may`** (choix refusable, `forced=False` —
      voir le bug n°5) ; **`an additional [energy] resource`** → **en plus** de
      l'icône imprimée, d'où `Resources("Y" * (1 + supplement))` ;
      **`[energy][energy] instead`** → le supplément vaut **2 au lieu de 1**,
      jamais « jusqu'à 2 » ; **`in play`** → n'importe où en jeu, rien n'exige
      que le compteur soit sur une cible du joueur de Speed ; **`If you do`** →
      la restriction n'est posée **que** si le supplément est pris ; **`for the
      rest of the TURN`** (`until_turn_end`, pas `until_round_end`).
      ⚠ Une carte n'a droit qu'à **une** `CanGenerateResources`
      (`card_player.py:83-84`) : ni `DiscardPay` ni `CheckThisCanDropPay` ne
      portent ce nom de fonction, l'assert n'est pas touché.
      Résultat : conforme.
- [x] Étape 6 : nombres : aucun coût (c'est une ressource), ressource
      imprimée [energy], supplément **1** ou **2**.
      Résultat : conforme.
- [x] Étape 7 : trois cas :
      - `sd011 … AVEC compteur : 1 + 2 ressources` (608) : preuve **par
        insuffisance** — Never Ending Spark coûte 3 et Top Speed est la SEULE
        ressource en main. Rouge sans module (`sd015 n'est pas en jeu`), vert
        avec.
      - `sd011 … SANS compteur, la carte à 3 reste injouable` (609) :
        contre-épreuve. Vert sans module **par construction**.
      - `sd011 … la carte qu'on paie part QUAND MÊME` (610) : LE point risqué.
        Vérificateur dédié qui contrôle les deux moitiés — `sd014` bien entrée
        en jeu, et `sd013` (coût 1, finançable par le `01088` encore en main)
        **plus jouable**. Rouge sans module, vert avec.
- [x] Étape 8 : autoplay ciblé : `sd011` présente dans **5/8** parties ;
      l'acte `Generate_1_additional_[energy]_resource(s)…` figure dans les
      journaux ; **c'est ce test qui a trouvé le bug n°5** ; 0 traceback après
      correctif.

Carte terminée : OUI

### sd012 : Top Speed (exemplaire 2/2)

- [x] Étape 2 : identique à `sd011`. Code dupliqué, commentaire complet sur
      `sd011`.
- [x] Étape 5 : mêmes mots-pièges. Résultat : conforme.
- [x] Étape 6 : mêmes nombres. Résultat : conforme.
- [x] Étape 7 : couverte par les cas de `sd011` (`sd012 = sd011`). Les deux
      exemplaires financent d'ailleurs le **même paiement** dans la partie 6
      d'autoplay : c'est précisément cette situation qui a révélé le bug n°5.
- [x] Étape 8 : autoplay ciblé : `sd012` présente dans **4/8** parties ;
      0 traceback.

Carte terminée : OUI

### sd013 : Mother's Protection

- [x] Étape 2 : cartes de référence : **`wc015`** (pack `wiccan`) — la MÊME
      carte, réutilisée par l'auteur pour le frère jumeau. Module dupliqué à
      l'identique. Modèle d'origine : `bkw/04004.py` Mockingbird pour le couple
      « payer un coût → prévenir », et `CostFunc.Custom(None, …)` pour le
      remélange (aucune `CostFunc` du moteur ne fait ce trajet).
- [x] Étape 5 : mots-pièges : **`your identity`** (et non « your hero » : la
      protection joue aussi en forme civile, d'où `"YourIdentity"`) ; **`any
      amount of damage`** (aucun filtre `is_from_attack` : trahisons et dégâts
      indirects couverts) ; **`shuffle … back into your deck`** = un coût
      **réel**, payé avant le handler (`ProcessSelfCost`) ; **`prevent 3`**
      (valeur imprimée, pas `"All"` comme Mockingbird).
      ⚠ **Pas de `full_link`** vers `wc015` : il traînerait le `set_name`
      « Wiccan » et ferait de la carte une signature de Wiccan.
      Résultat : conforme.
- [x] Étape 6 : nombres : coût 1, ressource [mental], **3** dégâts prévenus.
      Résultat : conforme.
- [x] Étape 7 : un cas : `sd013 … 3 dégâts prévenus` (611) — 5 dégâts infligés,
      3 prévenus → **2 encaissés**, et la carte a quitté le jeu (le coût est
      réel). Rouge sans module (`sd013 est encore en jeu ; degats = 5`), vert
      avec.
- [x] Étape 8 : autoplay ciblé : `sd013` présente dans **5/8** parties ;
      0 traceback.

Carte terminée : OUI

### sd014 : Explosive Touch

- [x] Étape 2 : cartes de référence :
      **déclencheur** → `AbilityFactory.AfterUnitUseBasicPower(HeroResponse,
      "You", …, powers=["ATK", "THW"])` (`factory/friend.py:373`), la fabrique
      du dépôt pour « after you basic attack / basic thwart ».
      **coût + effet** → `27009` Web-Bracelet, même
      `.SetCostFunc(CostFunc.Exhaust("This"))` et même `AbilityType.HeroResponse`
      (CORRECTIF documenté : 124 des 134 cartes « Hero Response » du dépôt
      emploient le sous-type dédié, pas `Response` nu).
- [x] Étape 5 : mots-pièges : **`basic attack OR basic thwart`**
      (`powers=["ATK", "THW"]` — ⚠ les codes du moteur sont `'ATK'`/`'THW'`,
      **jamais** `'Attack'`/`'Thwart'` : ce piège a déjà produit deux conditions
      mortes sur ce projet) ; **`that HAS an explosive counter`** (au présent,
      lu APRÈS le pouvoir de base) ; **`exhaust Explosive Touch`** (coût réel) ;
      **`ready Speed`** → `Faces.ReadyAll([message.trigger], effect)`, l'unité
      qui vient d'employer son pouvoir de base — **aucune recherche par nom**,
      le catalogue contenant déjà un allié `15010` « * Speed » et un sbire
      `57060`. ⚠ **Ne pas fusionner avec `sd016`** : Response contre Interrupt,
      inclinaison contre bonus de stats.
      Résultat : conforme.
- [x] Étape 6 : nombres : coût 1, ressource [energy].
      Résultat : conforme.
- [x] Étape 7 : deux cas, un par verbe imprimé :
      - `sd014 … après une ATTAQUE de base` (612) : une attaque de base incline
        le héros (c'est son coût) ; le retrouver **prêt** ne peut venir que de
        la Response, et `sd014` doit être **incliné**. Rouge sans module, vert
        avec.
      - `sd014 … après un CONTRE de base (via sd008)` (613) : l'API Puzzle n'a
        pas de commande de contre — on passe par le contre de base offert par
        Swift Strikes (voir « limites du harnais » n°1). Héros incliné au
        départ, prêt à la fin. Rouge sans module, vert avec.
- [x] Étape 8 : autoplay ciblé : `sd014` présente dans **3/8** parties ;
      0 traceback.

Carte terminée : OUI

### sd015 : Never Ending Spark

- [x] Étape 2 : cartes de référence :
      **Response sur la pose d'un compteur** →
      `AbilityFactory.AfterCounterPlacedOn(HeroResponse, None, 'explosive', …)`
      (`counter.py:97`), `which_card=None` rendant « on AN ENEMY OR SCHEME ».
      **capacité Resource** → `48005` Prehensile Tail et `54002` Cybernetic Arm,
      même `CanGenerateResources(Resource, Resources("Y"))
      .SetCostFunc(CostFunc.Exhaust("This"))` (celles-là restreignent la carte
      financée, pas Never Ending Spark : le texte ne dit rien de tel, donc pas
      de `for_card=`).
- [x] Étape 5 : mots-pièges : **deux capacités imprimées distinctes**, deux
      blocs, deux cas ; **`an enemy or scheme`** (aucun filtre de type) ;
      **`ready THIS card`** (pas Speed : c'est `sd014` qui redresse le héros) ;
      **`Resource:`** nu → `AbilityType.Resource`, sans restriction de forme.
      `Faces.ReadyAll` tolère une carte déjà redressée (no-op), cas nominal
      quand un compteur est posé alors que la Spark n'a pas encore servi.
      ⚠ La boucle Spark → énergie → événement → compteur → Spark redressée est
      **voulue et finie** : chaque tour exige de payer un événement à son coût
      plein, et le plafond de 1 compteur par carte limite les cibles utiles. Un
      compteur posé **en plein paiement** (Hyperkinetic Fuel est un Interrupt
      sur `WhenPlayerWouldPlayCard`, donc après `ProcessSelfCost`) redresse la
      Spark juste après qu'elle a été dépensée — intention de l'auteur.
      ⚠ Une seule `CanGenerateResources` par carte (`card_player.py:83-84`).
      Résultat : conforme.
- [x] Étape 6 : nombres : coût 3, ressource [energy], **1** ressource générée.
      Résultat : conforme.
- [x] Étape 7 : deux cas, un par capacité :
      - `sd015 … la carte inclinée est REDRESSÉE` (614) : inclinée au départ,
        `Puzzle.Counter(…)`. Rouge sans module, vert avec.
      - `sd015 … elle finance seule une carte à coût 1` (615) : la main ne
        contient QUE `sd013`, la ressource ne peut venir que de la Spark, et son
        inclinaison prouve le coût. Rouge sans module (`sd013 n'est pas en
        jeu ; sd015 n'est pas incliné`), vert avec.
- [x] Étape 8 : autoplay ciblé : `sd015` présente dans **4/8** parties ;
      0 traceback.

Carte terminée : OUI

### sd016 : Quick Adaptation

- [x] Étape 2 : cartes de référence :
      `AbilityFactory.WhenUnitWouldAttackOrThwart(HeroInterrupt,
      "YourIdentity", …, is_basic_power=True)` (`do_attack.py:1225`), la même
      fabrique que `sd002` — elle couvre les deux verbes imprimés en une seule
      capacité. Bonus par `Unit2.GainForThisActive(effect, message, attack=1,
      thwart=1)` (`unit.py:89`), le canal du « for that use » qu'emploient sous
      le capot `GainATKForThisAttack` et `GainTHWForThisThwart`.
- [x] Étape 5 : mots-pièges : **`basic`** (`is_basic_power=True` : un événement
      d'attaque ne déclenche rien) ; **`for that use`** (borné au message
      courant) ; **`+1 ATK AND +1 THW`** (les deux stats, rendues à la lettre) ;
      **`WITH an explosive counter`** — lu **AVANT** le pouvoir de base (c'est
      un Interrupt), donc un compteur posé par cette même attaque n'y serait pas
      encore. ⚠ **`"YourIdentity"` et surtout pas `"You"`** : voir le bug n°3.
      ⚠ **Ne pas fusionner avec `sd014`**.
      Résultat : conforme.
- [x] Étape 6 : nombres : coût 2, ressource wild, **+1** ATQ, **+1** CTR.
      Résultat : conforme.
- [x] Étape 7 : deux cas, un par verbe imprimé :
      - `sd016 … +1 ATQ` (616) : ATQ imprimée 1, attaque de base à **2** dégâts.
        Le vérificateur contrôle aussi que la carte **ne s'incline pas** (c'est
        `sd014` qui s'incline), pour ne pas confondre les deux cartes. Rouge
        sans module (1 dégât), vert avec.
      - `sd016 … +1 CTR (via sd008)` (617) : montage **identique** au cas 607,
        plus Quick Adaptation en jeu : la manigance tombe à **4** au lieu de 5.
        Rouge sans module (5), vert avec.
- [x] Étape 8 : autoplay ciblé : `sd016` présente dans **5/8** parties ;
      **c'est le cas de test qui a trouvé le bug n°3** ; 0 traceback.

Carte terminée : OUI

### sd017 : No Outrunning This (obligation)

- [x] Étape 2 : cartes de référence : **`wc018` Avoiding the Demiurge** (même
      auteur, pack frère) et **`09027` Physical Toll** (précédent officiel) —
      même triplet `WhenThisObligationGiveToYou` +
      `YouMayFlipToYourAlterEgoForm(player, effect)` + `player.ChooseAbilities`
      à DEUX branches, et même `condition=player.IsAlterEgo()` sur la branche
      qui incline l'alter-ego.
- [x] Étape 5 : mots-pièges : **`Exhaust Thomas Shepherd`** — le texte NOMME
      l'alter-ego (contrairement à `wc018`, qui dit « your identity ») ; d'où la
      condition `IsAlterEgo()`, sans quoi on inclinerait Thomas Shepherd alors
      qu'il n'est pas sur la table ; **`Discard this obligation`** appartient à
      la SECONDE puce seulement (la première se termine par « remove … from the
      game », exclusif d'une défausse) ; **`until the end of the NEXT round`**
      — un round de **plus** que `wc018` : la capacité temporaire laisse passer
      la première fin de round ; **aucune capacité `Boost`** n'est imprimée
      (seulement deux icônes, lues nativement depuis `desc.Boost`) — ne pas
      coder de capacité fantôme.
      Résultat : conforme.
- [x] Étape 6 : nombres : **2** icônes de bonus (relevées par découpe d'image),
      `GiveTo` = « Thomas Shepherd », **1** round laissé passer.
      Résultat : conforme.
- [x] Étape 7 : deux cas, un par branche :
      - `sd017 … branche 1` (618) : le pilote prend toujours la première option
        d'un `ChooseAbilities` (convention `il017`/`ok019`/`wc018`).
        L'obligation quitte le jeu, Thomas Shepherd est incliné. Rouge sans
        module, vert avec.
      - `sd017 … branche 2` (619) : atteinte par `preferer_option`. Le
        vérificateur contrôle l'interrupteur **et surtout sa durée** : encore
        levé après la PREMIÈRE fin de round, rabaissé à la SECONDE. Rouge sans
        module, vert avec.
- [x] Étape 8 : autoplay ciblé : `sd017` présente dans **8/8** parties (c'est
      l'obligation, elle est toujours dans le deck de rencontre) ; l'acte
      `Exhaust_Thomas_Shepherd_→_remove_No_Outrunning_This_from_the_game`
      figure dans les journaux ; 0 traceback.

Carte terminée : OUI

### sd018 : The Real Question (manigance annexe némésis)

- [x] Étape 2 : cartes de référence :
      **When Revealed** → `40093` The Senator's Support et `wd104`
      "Legitimate Business", qui impriment la MÊME phrase et emploient
      `Worlds.DiscardEncounterCardsUntil(effect, card_type=Attachment)` puis
      `face.Reveal(player, effect)`. `24030` Ruination donne la même forme sur
      un When Revealed.
      **« attachments gain Permanent »** →
      `*AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(
      card_type=Attachment), permanent=1)` (`environment.py:66`, paramètre
      `permanent` ligne 106), forme de `15024` The Next Evolution et `ss018`
      Assassins Guild.
      **`StartingThreat "2*"`** → `01108` Crowd Control, lu nativement.
- [x] Étape 5 : mots-pièges : **`until AN ATTACHMENT is discarded`**
      (`card_type=Attachment`) ; **`Reveal that attachment`** (`Reveal`, pas
      `PutIntoPlay`) ; **`While this scheme is in play`** (la fabrique s'éteint
      d'elle-même quand la manigance quitte le jeu) ; **`gain Permanent`** — on
      **donne** le mot-clé, on ne recode **jamais** le blocage de sortie de jeu
      (`docs/reference/mots-cles/permanent.md`, `HasPermanent
      .OnWhenCardLeavePlay`) ; **`2*`** = par joueur, aucune ligne de code.
      Le cas « aucun attachement dans le deck » est traité en écart assumé n°3.
      Résultat : conforme.
- [x] Étape 6 : nombres : **3** icônes de bonus, menace de départ **2 par
      joueur** (relevées par découpe d'image).
      Résultat : conforme.
- [x] Étape 7 : deux cas, un par phrase imprimée :
      - `sd018 … défausse jusqu'à un attachement, qui est REVÉLÉ` (620) : deck
        de rencontre truqué avec `sd020` sur le dessus, qui doit finir **en jeu
        attaché au vilain**. Rouge sans module (`sd020 n'est pas en jeu`), vert
        avec.
      - `sd018 … les attachements gagnent Permanent` (621) : l'attachement entre
        en jeu **APRÈS** la manigance — le chemin le plus fragile de
        `GiveKeywordToInPlayWhenApplyThis`. Le vérificateur lit le **mot-clé**
        sur la carte, pas le texte. Rouge sans module (« ne porte PAS le mot-clé
        Permanent »), vert avec.
- [x] Étape 8 : autoplay ciblé : `sd018` présente dans **3/8** parties (aléa du
      tirage du set némésis) ; 0 traceback.

Carte terminée : OUI

### sd019 : * Coat of Arms (sbire némésis)

- [x] Étape 2 : cartes de référence : **`58026` Grim Reaper** et **`60061`
      Kingpin** — sbires némésis à capacité étoilée, même convention `ATK "N*"`.
      `AfterUnitAttackUnit(NonKeywordStar, "This", None, …, dealt_damage=True)`
      (`do_attack.py:552`), fenêtre justifiée dans les arbitrages.
- [x] Étape 5 : mots-pièges : **`Quickstrike.`** → **AUCUN code**, lu
      nativement depuis `desc.Quickstrike` (`CanQuickstrike.ResolveQuickstrike`
      appelé par `Minion.OnEngagePlayer`) ; coder l'attaque à la main serait une
      capacité fantôme (fiche `mots-cles/quickstrike.md`) ; **`ATK 1*`** →
      l'étoile alimente `printed_attack_consequential_damage`, sans effet sur un
      sbire (seuls les ALLIÉS subissent des dégâts consécutifs) : convention du
      dépôt, rien à coder ; **`if it deals damage`** (`dealt_damage=True` : une
      attaque entièrement défendue ou prévenue ne déclenche rien) ; **`each
      character YOU control`** → « you » = le joueur **attaqué**, lu sur
      `message.to_player` et **jamais** `message.GetToPlayer()`, dont le repli
      contient un `assert card_id == "44014"` (`sender_damage.py:535`) qui
      ferait planter la partie ; « each character » = l'identité **et** les
      alliés, y compris celui qui vient d'encaisser l'attaque ; **ce n'est pas
      une attaque** (`DealDamage` sans `AttackProperty`, hors fenêtre
      d'attaque) : aucun re-déclenchement d'« après une attaque ».
      Résultat : conforme.
- [x] Étape 6 : nombres : PV 4, ATQ 1*, MNG 2, **2** icônes de bonus,
      Quickstrike **1**, `Nemesis` = « Thomas Shepherd », trait `ANTI HERO`
      (ajouté au moteur).
      Résultat : conforme.
- [x] Étape 7 : un cas : `sd019 … 1 dégât de plus à CHAQUE personnage` (622) —
      le sbire est mis en jeu **avant** le passage en forme héros (sinon
      Quickstrike déclencherait une attaque de plus), identité **et** allié
      **inclinés** (sinon le pilote déclare un défenseur : constaté, Quicksilver
      encaissait l'attaque à la place du héros). ATQ 1 → l'identité encaisse
      1 puis 1 de supplément = **2**, l'allié **1** : la portée « each character
      you control » est vérifiée sur DEUX personnages. Rouge sans module
      (`degats sur sd002 = 0 ; degats sur l'identite = 1`), vert avec.
- [x] Étape 8 : autoplay ciblé : `sd019` présente dans **3/8** parties ;
      0 traceback.

Carte terminée : OUI

### sd020 : Inspirational Art (attachement némésis)

- [x] Étape 2 : cartes de référence : **`01100` Enhanced Ivory Horn** et
      **`04072` Laser Rifle** — même triplet « attacher + capacité passive +
      Hero Action de défausse à coût de ressources » ;
      `AttachToFaceWhenPutIntoPlay(Villain)` et
      `PlayerActionToDiscardThis(HeroAction).SetCost(Cost("YR"))` viennent
      directement de `04072`. **Fenêtre de bonus** → `08004` Attacrobatics,
      seul autre utilisateur de `WhenBoostCardTurnedFaceUp`.
- [x] Étape 5 : mots-pièges : **`Attach to the villain`** ; **`during a VILLAIN
      activation`** (`boost_for_card=Villain` : l'activation d'un sbire ne
      déclenche rien) ; **`EACH boost card gets +1`** — la fabrique se déclenche
      une fois **par carte de bonus** retournée, on ajoute l'icône à
      `message.trigger` : toutes y passent, une par une ; **`turned faceup`** →
      c'est bien cette fenêtre-là et pas le message « would » qui la précède
      (bug n°4) ; **`Spend [energy][physical]`** → coût relevé par **découpe
      d'image** (`art_cout.png`), jamais à vue (leçon Lockjaw).
      ⚠ **Collision Permanent avec `sd018`** : une carte Permanente ne peut pas
      être défaussée, et `CardFace.DiscardInternal` (`card_face.py:473-483`)
      contient un `assert` sur ce chemin. La Hero Action devient donc
      **indisponible** (condition) tant que The Real Question est en jeu, au
      lieu d'échouer — intention lisible de l'auteur : battre la manigance
      d'abord.
      Résultat : conforme.
- [x] Étape 6 : nombres : **3** icônes de bonus, **+1** icône par carte de
      bonus, coût **[energy][physical]**, trait `ART` (ajouté au moteur).
      Résultat : conforme.
- [x] Étape 7 : trois cas :
      - `sd020 … chaque carte de bonus gagne +1 icône` (623) : deck truqué à
        `01106` Stampede (1 icône imprimée), héros incliné pour qu'il ne
        défende pas. Rhino ATQ 2 + 1 = **3** sans l'attachement, **4** avec :
        la valeur exacte est la preuve. `en_jeu` contrôle au passage l'attache
        au vilain. Rouge sans module (3), vert avec (4).
      - `sd020 … Hero Action` (624) : financée par deux cartes à **une seule
        icône imprimée** (voir « limites du harnais » n°3). Rouge sans module
        (`n'offre aucune action en jeu`), vert avec.
      - `sd020 … Hero Action INDISPONIBLE avec The Real Question` (625) : le
        vérificateur interroge le filtre du gestionnaire d'événements
        exactement comme `Puzzle.Action`, **et exige que l'action soit bien
        DÉCLARÉE** — sans quoi le cas resterait vert quand le module est retiré
        (une capacité absente est aussi « indisponible »). Rouge sans module,
        vert avec.
- [x] Étape 8 : autoplay ciblé : `sd020` présente dans **3/8** parties ;
      **c'est le cas 623 qui a trouvé le bug n°4** ; 0 traceback.

Carte terminée : OUI

### sd021 : Magic Chains (attachement némésis)

- [x] Étape 2 : cartes de référence : **`04029` Crossfire's Rifle** et
      **`04064` Crossbones' Machine Gun**, qui impriment la même tournure
      « Attach to X. Otherwise, attach to the villain » —
      `AttachToFaceWhenPutIntoPlay(CardFinder(name=…),
      if_cannot_attach_to=Villain)`.
      **Forced Response** → `AfterUnitAttackUnit(ForcedResponse,
      "AttachedEnemy", None, …, dealt_damage=True)` ; `"AttachedEnemy"` est une
      cible-chaîne du moteur (`condition/card_type.py:38` et 184) qui désigne
      l'ennemi PORTEUR, donc Coat of Arms ou le vilain selon où la carte a
      atterri.
- [x] Étape 5 : mots-pièges : **`ATK+`** et jamais `ATK` — sur un attachement
      c'est un BONUS donné au porteur, `ATK` en ferait une carte à 1 d'attaque ;
      clé vérifiée dans `cards.json` ; **`THE ATTACHED enemy`** (pas « un
      ennemi ») ; **`if the attack deals damage`** (`dealt_damage=True`) ;
      **`stun YOUR hero`** = le héros du joueur que l'ennemi attaché vient
      d'attaquer, lu sur `message.to_player` ; **`→ discard this card`** — la
      flèche lie un **COÛT** à un **EFFET** (règle officielle, arbitrage n°3 de
      l'utilisateur du 30/08/2026) : coût impayable, donc **ni étourdissement ni
      défausse**, et la carte reste en jeu avec son +1 ATQ. Deux cas concrets :
      identité civile (aucun héros à étourdir) et héros **déjà** étourdi ou
      Stalwart (`CanbeStunned()` faux, un personnage ne portant pas deux fois le
      même statut).
      Résultat : conforme.
- [x] Étape 6 : nombres : **1** icône de bonus, `ATK+ 1`, traits `WEAPON` /
      `MYSTIC` (relevés par découpe d'image).
      Résultat : conforme.
- [x] Étape 7 : deux cas, un par branche de la flèche :
      - `sd021 … elle étourdit le héros puis se défausse` (626) — coût
        **payable**. Le sbire est posé avant le passage en forme héros
        (Quickstrike) et le héros est incliné (sinon il défend et l'attaque
        n'inflige rien). Les deux moitiés sont contrôlées : statut Sonné ET
        carte défaussée. L'attache conditionnelle est prouvée par le fait que le
        Forced Response part sur l'attaque de **Coat of Arms**, pas du vilain.
        Rouge sans module (« le héros n'est pas Sonné »), vert avec.
      - `sd021 … en ALTER-EGO le coût de la flèche est impayable : la carte
        RESTE` (627) — même montage **sans** le passage en forme héros. Aucun
        héros à étourdir, donc rien ne se passe : `sd021` toujours en jeu et
        personne de Sonné. **Contre-épreuve**, donc verte aussi sans module (une
        carte sans script ne se défausse pas non plus) ; sa preuve de présence
        est son jumeau positif 626, rouge sans module. Ce cas a été ajouté le
        30/08/2026 en même temps que la correction de la flèche.
- [x] Étape 8 : autoplay ciblé : `sd021` présente dans **3/8** parties ;
      0 traceback.

Carte terminée : OUI

### sd022 : Conflicted Feelings (obligation du set némésis)

- [x] Étape 2 : cartes de référence : **`28021` Weight of the World** (Nova) —
      le seul précédent du dépôt d'une obligation qui **reste en jeu** :
      « While this card is in play, … » + une Action qui la retire. Même forme
      exactement, y compris l'absence de `WhenThisObligationGiveToYou` (c'est
      elle qui fait rester la carte : `Obligation.OnWhenCardRevealed`
      — `obligation.py:86-99` — la met dans `obligations_area` et n'en défausse
      que le cas `is_dealt_encounter`).
      **« cannot be damaged »** → `AbilityFactory.UnitCannotTakeDamage`
      (`damage.py:255`), **corrigée pour cette carte** (bugs n°1 et n°2).
      **Alter-Ego Action** → `PlayerActionToDiscardThis(AlterEgoAction)
      .SetCost(Cost("YB"))`, la fabrique de `01100`/`04072`/`sd020`.
- [x] Étape 5 : mots-pièges : **`While this obligation is in play`** (la
      protection tombe avec l'obligation : les capacités d'une carte ne sont
      actives qu'en jeu) ; **`Coat of Arms`** (nom unique du set, écrit SANS
      l'étoile d'unicité que `cards/paper.py:45` retire) ; **`discard this
      card`** et non « remove from the game » comme `28021` : la carte retourne
      dans la défausse rencontre et peut revenir ; **`Spend
      [energy][mental]`** → coût relevé par **découpe d'image**
      (`cf_cout.png`). ⚠ Elle appartient au `nemesis_set`, pas à la clé
      `obligations`.
      Résultat : conforme.
- [x] Étape 6 : nombres : **1** icône de bonus, `GiveTo` = « Thomas Shepherd »,
      coût **[energy][mental]**.
      Résultat : conforme.
- [x] Étape 7 : deux cas, un par phrase imprimée :
      - `sd022 … Coat of Arms ne peut pas subir de dégâts` (627) :
        `Puzzle.Damage` ne fait **rien** sur un sbire (piège documenté du
        guide), on passe donc par une vraie attaque de base du héros. ATQ 1 →
        **1** dégât attendu sans l'obligation, **0** avec. `en_jeu: ["sd022"]`
        contrôle au passage que l'obligation **reste** en jeu. Rouge sans module
        (1 dégât), vert avec. **C'est ce cas qui a trouvé les bugs n°1 et n°2.**
      - `sd022 … Alter-Ego Action` (628) : financée par deux cartes à une seule
        icône imprimée. Rouge sans module (`n'offre aucune action en jeu`), vert
        avec.
- [x] Étape 8 : autoplay ciblé : `sd022` présente dans **3/8** parties ;
      0 traceback.

Carte terminée : OUI

## Gate finale (PROCESSUS-HEROS)

- [x] **Étapes 1 à 8 complètes** : `cards.json` (23 cartes), scripts
      (23 modules + 3 `__init__.py`), deck de départ, `data/nemesis/
      speed_nemesis.json`, `data/sets_info.json` (130), `tools/
      prefixes_fanmade.json`, 23 images (+ recette `tools/
      importer_images_speed.py`), **biographie** (`sd001a` dans
      `public/js/prepare/heros-info.js`), **texte français** (23 entrées dans
      `ui-app/src/board/textes-fr-fanmade.ts`).
- [x] **Un `PROCESSUS-CARTE.md` rempli et « Carte terminée : OUI » pour chaque
      carte du pack** : `sd001a`, `sd001b`, `sd002`, `sd003`, `sd004`, `sd005`,
      `sd006`, `sd007`, `sd008`, `sd009`, `sd010`, `sd011`, `sd012`, `sd013`,
      `sd014`, `sd015`, `sd016`, `sd017`, `sd018`, `sd019`, `sd020`, `sd021`,
      `sd022` — **23/23**.
- [ ] **Une partie complète jouée avec le héros** : **NON**, et ce n'est pas une
      omission qu'on peut combler ici. Une partie humaine dans le navigateur est
      hors de portée de cette session : elle demande d'ouvrir
      `http://127.0.0.1:2345/`, de cliquer et de juger. **Je ne l'ai pas jouée
      et je ne peux pas la jouer.** Ce qui a été fait à la place : 8 parties
      d'autoplay complètes (0 bloquée, 0 traceback), 35 cas de comportement
      verts avec preuve rouge/vert module par module, et le montage de partie
      vérifié.

**Ce que ces outils ne peuvent pas voir** — à vérifier lors de la première
partie humaine, précisément :

1. **La biographie au survol.** PROCESSUS-HEROS §7 exige une preuve visuelle :
   survoler Speed dans le wizard et constater que le panneau affiche bien le
   texte, pas seulement le grand visuel. L'entrée est indexée par `sd001a`
   comme prescrit et le fichier passe `node --check`, mais **la preuve visuelle
   n'a pas été faite**.
2. **Les tooltips français.** Les 23 entrées sont écrites, mais rien n'apparaît
   dans le jeu tant que **`ui-app/deployer.sh` n'a pas tourné** (§11.1 du
   guide). **Il n'a pas été lancé dans cette session.** ⚠ Attention au piège
   documenté au §10 : `deployer.sh` recopie `public/js` depuis le vestige WSL
   avec `--delete` et peut **écraser la biographie** — vérifier
   `public/js/prepare/heros-info.js` après le déploiement.
3. **Le confort des compteurs explosifs.** Le plateau reçoit bien les compteurs
   (`CanPlaceCounter.GetInfoDict` les expose sous `c_explosive`), mais **rien
   ne dit à quoi ressemble un compteur `explosive` à l'écran** ni s'il est
   distinguable des autres. Le pack fournit un jeton dédié
   (`Explosive Token.png`) qui n'est pas intégré à l'UI : question de
   cosmétique, pas de règles.
4. **La lisibilité de la fenêtre « you may » de Top Speed.** Le choix est
   proposé **pendant le paiement d'une autre carte** : c'est un moment
   inhabituel pour une question, et seul un joueur peut dire si le plateau la
   présente clairement.
5. **`sd018` The Real Question avec un deck de rencontre sans attachement.**
   Aucune des 8 parties d'autoplay ne l'a révélée dans cette configuration : le
   comportement « meule tout et ne révèle rien » est prouvé par lecture du
   moteur (`deck.py:470`, parcours d'un instantané), **jamais observé en
   partie**.
