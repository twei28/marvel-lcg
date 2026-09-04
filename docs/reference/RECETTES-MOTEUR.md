# Recettes moteur — mécanique imprimée → fabrique + carte modèle

**Pourquoi ce fichier.** Sur les portages venompool, angela et harry_osborn,
la plus grosse part du temps (~40 %) est partie à RETROUVER les mêmes
choses : quelle fabrique rend « After you attack an enemy », quelle carte
sert de modèle, quel piège attend au tournant. Ce fichier capitalise ces
réponses, vérifiées en jeu par les cas de `tools/test_capacites.py`.

**Ce qu'il ne remplace PAS.** L'étape 2 de `PROCESSUS-CARTE.md` (carte de
référence, avec le POURQUOI) reste obligatoire : la recette donne le point de
départ, pas la dispense de lire la carte modèle et de vérifier le texte
contre le code. Aucune gate ne saute.

**Entretien.** Chaque portage qui découvre une recette ou un piège NOUVEAU
l'ajoute ici (une ligne suffit), comme les fiches de `mots-cles/`.

---

## 1. Déclencheurs (côté joueur)

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

## 2. Effets

| Effet | API | Modèle | Piège |
|---|---|---|---|
| Étourdir / désorienter / robuste | `Faces.GiveStatus(cibles, "Stunned"/"Confused"/"Tough", effect)` | 05015, 01083 | cibler avec `canbe_stunned=True` etc. (un Stalwart n'est pas ciblable) |
| Retirer un statut (coût ou effet) | `face.DiscardStunned/DiscardConfused/DiscardTough(effect, rule=1)` | wd005, ho001a | plusieurs statuts → le CHOIX revient au joueur (`ChooseAbilities`) |
| Dégâts | `this.DealDamage(cibles, n, effect)` | partout | `if_this_attack_defeats=fn` appelé PAR unité vaincue (ag006, th009) |
| Dégâts « X » | `effect.GetCostX()` | 14006, ho004 | dans les cas de test, `surpayer: True` sinon X=0 |
| +1 dégât à un événement | `RegisterTemp(WhenUnitWouldAttack(Temp0, "You", DealAdditionalDamage), until_resolve_effect=message.played_effect)` | 32047, 54002, ho006 | — |
| Retirer de la menace | `this.RemoveThreatFromSchemes(cibles, n, effect)` | an004, vp001a | `ignore_crisis=True` existe (si007) ; « from THAT scheme » = même cible, pas un second choix |
| Poser de la menace | `this.PlaceThreatOnSchemes(cibles\|"EachSideScheme"\|"MainScheme", n, effect)` | 50134, ho015 | littéraux moteur : card_face.py:621 |
| Redresser | `Faces.ReadyAll(faces, effect)` | an001a, 31009, ho011 | — |
| Incliner plusieurs cartes et compter celles qui l'ont vraiment été | `Faces.ExhaustAll(faces, effect)` — c'est le RETOUR qu'on compte | bt004 | **`CanBeExhaust` N'EXISTE PAS** sur une face (`AttributeError` en pleine partie) : la méthode est `CanExhaust()`, sans argument, et `ExhaustAll` fait déjà le tri |
| Effet différé « après la fin de cette attaque » | `RunAt.AfterEnemyActivationEnd(effect, message.would_atk_message, fn)` | bt004 | `RegisterTemp` + `AbilityType.Temp0` sur `AfterUnitDefendAgainstAttack` **ne se déclenche jamais** (constaté 1/9/2026) ; relever les PV avant l'attaque pour tester « 0 dégât » |
| Pool hors-deck qui alimente le deck | `BeginGameWithSetAside([...])` + `Rand.RandomChoice(pool, effect)` + `Faces.ShuffleAllTo([face], player.player_deck, effect)` | bt001b, bt006 (36001b pour le pool) | `RandomChoice` est déterministe sous `disable_shuffle` mais **ne rend pas forcément le 1er id du deck de départ** : compter le pool plutôt que nommer la carte tirée |
| Poser une carte sur le dessus du deck | `Faces.MoveAllToDeck([face], deck, "Top", effect)` | ag001b, bt011 | la position est un ARGUMENT POSITIONNEL, pas un `to_top=` |
| Fouiller le deck du joueur | `Search.PlayerCard(effect, player, include_player_deck=True, trait=..., card_type=...)` + `player.GainCard` | an001b, ok001b, ho007 | le « (Shuffle.) » est le comportement par défaut |
| Le plus au-dessus de la défausse | `player.discard_pile.FindTopmost(CardFinder2("TECH", Upgrade))` + `Faces.ReturnToHand` | 01034, ho013 | — |
| Défausser le deck rencontre | `Worlds.DiscardEncounterCards(n, effect)` | 15004, ho014 | boucle « until » : BORNER par deck+défausse (leçon Underling) |
| Révéler depuis une défausse | `face.Reveal(None, effect)` | an015, ho014 | — |
| Compter les icônes de boost | `FacesCounter.CountTotalBoostIcons([face])` | 15004, ho014 | — |
| Choix secondaire (2e cible, option) | `initiator.ChooseAbilities(effect, ForChoiceAbility("...", op).SetTarget(...))` | 08013, 16155, 14004 | prend la PREMIÈRE branche par défaut (pas de Cancel) ; `Otherwise(op)` pour « sinon » |
| « you may spend a resource » | `ForChoiceAbilityWithCost(Cost("1"), nom, op)` dans un ChooseAbilities | 50134, ho010 | — |

## 3. Mots-clés et bonus continus

| Texte | API | Modèle | Piège |
|---|---|---|---|
| You get +N hit points / +ATK / trait | `GiveKeywordToAttached("You", health=N, attack=N, trait="AERIAL")` | an008, 05023, ho008, ho011 | pour un SOUTIEN ou un ALLIÉ non attaché : `GiveKeywordToInPlayWhenApplyThis(<cible>, control_by="You", ...)` (an002, ho005) |
| **« NOM gets +X »** vs **« YOU get +X »** | `GiveKeywordToInPlayWhenApplyThis(**Hero**, …)` vs `(**Identity**, …)` | an002 Sera → `Hero` ; 06007 Asgard → `Identity` | ⚠ **LIRE LE MOT, pas le modèle.** « You » désigne l'identité, donc les DEUX faces. Un NOM PROPRE n'en désigne qu'UNE : « **Angela** gets +1 hand size » ne vaut qu'en forme héros, puisque l'alter-ego s'appelle Aldrif Odinsdottir. Copier `Identity` depuis Asgard donnait le bonus aussi en alter-ego. **Trouvé en partie réelle par le joueur le 1/9/2026**, jamais par les tests : le seul cas existant se plaçait en forme héros, où les deux écritures donnent le même résultat. → **Tout bonus continu d'identité exige un contre-cas dans l'AUTRE forme.** |
| perd stalwart / steady | `GiveKeywordToAttached("Character", stalwart=-1, steady=-1)` | 50144, ho012 | un retrait sur mot-clé absent est neutre |
| gets +1 X for each <face> in play | `ThisGainKeywordForEachFaceInPlay(CardFinder(card_type=SchemeSide2), attack=1, scheme=1)` | 04125 Red Skull, 01059, ho015 | la classe des complots annexes est `SchemeSide2` — `SideScheme` N'EXISTE PAS dans cards.pack |
| gets +1 X par compteur/état dynamique | `ThisGainKeyword(fn, recover=1, change_on_event=OnEvent...)` | an001b, dt133 | — |
| attacks gain overkill/piercing/ranged | `UnitAttackGainKeyword("This"\|CardFinder(...), overkill=True, piercing=True)` | 27078, ho016 | `attacker="This"` pour ne pas toucher les homonymes |
| In expert mode ... | `expert_mode_only=True` (fabriques d'environnement) | 50089b, wd057 | les capacités `[star]` SANS « In expert mode » sont codées TOUJOURS actives (convention moteur, cf. 04125) |
| Bases automatiques (desc, AUCUN script) | `Stalwart`, `Villainous`, `Hinder` (`N*` = par joueur), `Crisis`, `Hazard`, `Acceleration`, `Temporary`, `Toughness`, `Restricted`, `MaxPerUnit`, `MaxPerDeck`, `Boost`, `GiveTo`, `Nemesis`, `StartingThreat` | fiches `mots-cles/` | Temporary : la défausse vit dans `ProcessTemporary` (world_action.py), pas dans has_temporary.py |

## 4. Ressources

| Texte | Montage | Modèle | Piège |
|---|---|---|---|
| Resource: Exhaust → generate [x] | `CanGenerateResources(type, Resources("G")).SetCostFunc(CostFunc.Exhaust("This"))` | ab007, ma005 | **UNE SEULE CanGenerateResources par carte** (assert) |
| ... generate X ou Y selon l'état | `resources_fn=fn` (évaluée au paiement) | an007 | — |
| ... la ressource imprimée d'une AUTRE carte | `resources_fn` + `FacesCounter.GetPrintedResources([face])` | 21006, ho009 | **NE PAS suivre le couple Can+Do de 31001a** : dans `DoGenerateResources`, `res` est figé AVANT le `PayCost` — un `res_fn` sur `return_exhausted_cards` lit l'état d'avant paiement (constaté sur ho009). Couleur à figer à l'annonce, coût aligné par `CostFunc.Custom` |
| ressource + effet différé sur la carte payée | `ex_operation` / `WhenYouSpendThisCardToPlay` | 54002, 32047, ah007 | — |

## 4bis. Libellés de capacité (`SetLabel`)

- `Ability.LABEL` vaut `'attack' | 'thwart' | 'defense'`, et **un seul appel**
  à `SetLabel` est permis : le chaîner lève `assert self.labels == []`
  (ability.py:380). Deux libellés = `SetLabel('thwart', 'attack')`.
- Chaque type de capacité n'accepte qu'un sous-ensemble (`check_sub_type`,
  ability.py:169). Un libellé hors liste **fait tomber le montage du deck** en
  `AssertionError: label='...'`, pas la partie : le héros devient injouable.
- Un type ABSENT de la chaîne tombe sur `elif self.is_play`, qui n'autorise
  **aucun** libellé. Deux correctifs déjà posés pour cette raison :
  `AlterEgoResponse` (4/8/2026) et **`ForcedInterrupt` (1/9/2026, bt016)**.
  Devant un `AssertionError: label=` sur un type peu courant, vérifier d'abord
  s'il figure dans la chaîne.

## 5. Coûts

- Chaînage : `.SetCostFunc(a).SetCostFunc(b)` — les deux s'ajoutent (31009,
  ho005, ho009).
- `CostFunc.Exhaust("This" | "YourIdentity" | card_type=/trait=/range=)` :
  garde la trace dans `return_exhausted_cards`.
- Ressources colorées : `.SetCost(Cost("RB"))` (wd005).
- Coût arbitraire : `CostFunc.Custom(None, fn)` — `fn(targets, effect) ->
  bool`, False bloque le paiement (ho009).
- « Hero form only » : `.SetPlay(hero_form_only=True)` (01009, ho012).

## 6. Ciblage

- `SetTarget(Enemy, canbe_stunned=True)`, `range=(1, 2)`, `range=(1,"All")`,
  `from_where=["YouControlCards"]`, `canbe_ready=True`, `canbe_confused=True`.
- AoE « villain and each minion engaged with that player » : littéral
  `SetTarget("VillainAndEngagedSamePlayerMinion")` — le choix du joueur est
  DANS le sélecteur (04006, ho004).
- Deux types de cibles dans un même effet : première par `SetTarget`, la
  seconde par `ChooseAbilities` dans l'opération (08013, ho001a).

## 7. Harnais de test (`tools/test_capacites.py`) — pièges payés

- **`[filtre]`** : `... rapport.json "ho0"` — 26 cas en 4 min. La batterie
  complète reste due quand un fichier moteur PARTAGÉ change (règle de portée
  §6bis du GUIDE).
- **JAMAIS deux harnais en parallèle** (test_capacites, verifier_tous_les_decks,
  autoplay) : chaque fils réécrit `.game-src/launch.json` → AssertionError
  ip/port fantômes, quelles que soient les plages.
- **`PARALLELES=4` accélère test_capacites ×4** (ajouté le 1/9/2026). Chaque
  fils reçoit SON dossier de jeu (`.game-src-par0`…), donc son `launch.json` :
  c'est ce fichier unique, et lui seul, qui interdisait le parallèle. Peu
  coûteux, `.game-src` ne pesant que 20 Ko de liens symboliques **relatifs**,
  recopiés tels quels dans un dossier frère (`os.readlink`, jamais un chemin
  recalculé). Mesuré sur les 28 cas du pack `bt` : **270 s → 67 s**, verdicts
  ET messages identiques un à un. Batterie complète : 2 h 15 → ~34 min.
  Défaut à `1`, donc rien ne change sans la variable.
  ⚠ Le port suit le **rang global**, jamais le rang dans le pool : sinon on
  recrée exactement les faux échecs ip/port ci-dessus.
  ⚠ Ne lève PAS la règle précédente : `autoplay.py` et
  `verifier_tous_les_decks.py` écrivent toujours dans le `launch.json` commun.
- **Le port de base doit tenir dans la plage TCP, cas compris.** Chaque cas
  prend `port + rang`, donc une batterie complète va jusqu'à `port + 907`.
  Au-delà de 65535 le serveur web ne se lie à rien, `manager_web.httpds` reste
  vide, et **chaque** cas meurt sur `IndexError: list index out of range`
  (`web_device.py:53`). Le rapport annonce alors **« 0/908 »**, ce qui ressemble
  à une régression massive du contenu alors que **rien n'a été testé**. Payé le
  1/9/2026 : une batterie complète lancée sur le port 67000 a brûlé 25 minutes
  pour rien. Un garde-fou refuse désormais la commande d'entrée, avec la borne
  maximale calculée. **Base usuelle : 40000.**
- **Avant de lancer un harnais : `pgrep -af test_capacites`**, jamais `ss` sur
  les ports. Chaque cas ouvre puis referme SON port : entre deux cas, la plage
  paraît libre alors qu'une passe complète tourne. Le rapport JSON n'est écrit
  qu'à la FIN : son absence ne prouve pas non plus que rien ne tourne. Payé le
  31/08/2026, deux batteries lancées en parallèle pendant 8 minutes
  (journal `.planning/todos/2026-08-31-portage-beast.md` §5).
- Clés : `main_exclusive`, `jouer`, `cibles`, `payer_avec`, `ne_pas_depenser`,
  `surpayer` (obligatoire pour un coût X), `accepter_choix`, `heros2`.
  **Il n'existe PAS de clé `action`** : une capacité de carte en jeu se
  déclenche par `"declencher": ["Puzzle.Action('<id>')"]` (payé sur bt010/bt011).
- **`Puzzle.Attack(card)` fait ATTAQUER `card`** — ce n'est pas la cible. Pour
  que le héros frappe : `Puzzle.Attack('<hero>', '<vilain>')`. Un
  `Puzzle.Attack('01094')` fait attaquer RHINO, et un cas qui attend des dégâts
  sur le vilain lit 0 sans rien comprendre (payé sur bt008).
- Clés de vérification pour les zones hors-jeu : `dans_deck_joueur`,
  `mis_de_cote`, `taille_mis_de_cote` (ajoutées le 1/9/2026 pour le pool
  Discovery de Beast) — sans elles, une carte mélangée dans le deck n'est ni en
  jeu, ni en main, ni dans la défausse : **aucune clé ne la voit**.
- **`mulligan: "all" | [card_id, …]`** (ajoutée le 1/9/2026, bt001b) : écarte
  des cartes pendant l'étape 15 de `World.Setup`. Sans elle le pilote répond
  toujours « je ne défausse rien » (`premiere_option_jouable` donne le nombre
  MINIMAL de cibles, soit zéro), et **aucune capacité ne peut réagir au
  mulligan**. L'option porte le nom exact « Resolve Mulligans ». Préférer
  `"all"` : la main de départ dépend du mélange, nommer des card_id n'est pas
  déterministe.
- **`TRACE_OPTIONS=1`** avec `CAS_INDEX=<n>` : affiche les options reçues, y
  compris en phase d'attente (`ATTENTE-ASK`). C'est ainsi qu'on trouve le NOM
  exact d'une décision à piloter, plutôt que de le deviner.
- **Une carte repêchée en main est souvent JOUÉE dans la foulée** par le pilote,
  et le cas ne la trouve plus en main : repêcher une **ressource**, que le
  pilote ne peut pas jouer (payé sur bt001a). Même famille de piège que la
  chaîne aval : bt005 redressait l'allié qui venait de payer, faisant échouer
  le cas de bt014.
- Un sbire à 3 PV qui encaisse 4 dégâts **disparaît** : `degats_min` ne trouve
  plus la carte, prouver la mort par `hors_jeu` (payé sur bt015).
- `cibles` FORCE la sélection : sur un sélecteur AoE, forcer `['01094']`
  EXCLUT les sbires (payé sur ho004).
- `Puzzle.Exhaust`/`FindCommandCards` attrape la PREMIÈRE carte par id, y
  compris une copie du DECK : pour manipuler une carte en jeu, choisir une
  carte ABSENTE du deck de départ du cas (payé sur ho009/05017 → 31019).
- Les `Response` se déclenchent toutes seules et `ChooseAbilities` prend la
  première branche : les cas AVAL doivent intégrer la chaîne (convention
  an001a Frenzy, cinq cas harry_osborn).
- Un contre-cas qui vérifie une ABSENCE d'effet reste vert sous substitution :
  l'assumer dans le journal (vp014/vp015, ho017).
- `Puzzle.Defend(defenseur, attaquant)` fait défendre : pour prouver un dégât
  qui passe, prendre un ALLIÉ défenseur (pas la DEF 2 de l'identité — payé
  sur ho016).
- Preuve par substitution en une commande : `tools/substituer_pack.py`.

## 8. Données (`data/cards.json`) — conventions

- Pack en QUEUE de fichier, `"custom": "Arnaud"`, `set_name` = nom du
  personnage (civil si le nom de héros collisionne : `Kate Bishop`,
  `Harry Osborn`), némésis = `"<set> Nemesis"`.
- **Le module d'une carte est cherché dans le dossier du `set_name`, PAS du
  pack** : `cards.pack.<pack>.<CleanName(set_name)>.<card_id>`, puis
  `cards.pack.<pack>.<card_id>` (database.py:195). Un `set_name` « X Nemesis »
  cherche AUSSI dans le dossier `x`, mais **jamais l'inverse**. Une obligation
  au `set_name` du héros rangée dans `<pack>_nemesis/` n'est donc **jamais
  chargée, en silence** : la carte entre en jeu et ne fait rien. Payé sur
  `bt019` le 1/9/2026 ; le test `substituer_pack.py` la voyait pourtant, il lit
  les FICHIERS.
- Deux exemplaires d'une même carte aux ressources DIFFÉRENTES = deux card_id
  suffixés (`01043a/b/c/d` Wakanda Forever!, `bt007a/b` Multi-Tasking). Ne
  jamais présumer que deux scans de même nom sont des copies : **comparer les
  coins**.
- Ressource double : `RES` à deux lettres (`"YY"` 01088, `"GG"` 01044,
  `"YB"` bt009).
- Écriture en `ensure_ascii=True, indent=4` (le fichier est échappé ascii) ;
  TOUJOURS recalculer les checksums après (`tools/recalculer_checksums.py`),
  sinon rejet SILENCIEUX.
- `[star]` en tête de ligne = capacité étoile ; `<hr />` sépare le texte
  carte du texte Boost ; `[[TRAIT]]`, `[boost]`, `[per_hero]`, `•` pour les
  puces ; `→` pour la flèche de coût.
- Icônes : « + » sur carte inclinée = **hazard** ; « + » sur maison
  soulignée = **acceleration** ; « ! » en étoile = **crisis** — TOUJOURS par
  comparaison d'image, jamais à vue (leçon Lockjaw).
- Ressources : coin de carte → `RES` : R physique (poing rouge), B mental
  (nœuds bleus), Y énergie (éclair jaune), G wild (étoile verte).
- Un trait inconnu de l'énum `TRAITS` (card_face.py) s'y AJOUTE (EARTH-6160,
  EXTREMIS...).

## 9. Le chemin outillé, de bout en bout

| Étape | Commande | Durée vue |
|---|---|---|
| Légalité des decks (signatures étrangères) | bloc python du §10 de PROCESSUS-HEROS | 2 s |
| Un deck + témoin | `DECK_NOM=<pack> ... verifier_tous_les_decks.py` | ~40 s |
| Les 107 decks (fichier partagé touché) | passe complète | ~20 min |
| Cas du pack | `test_capacites.py ... "<prefixe>"` | ~10 s/cas |
| Substitutions du pack | `substituer_pack.py` | ~30 s/carte |
| Statique | `test_cards.py`, `verifier_api_cartes.py`, `audit_cartes.py` | ~2 min chacun |
| Autoplay ciblé | `autoplay.py --deck <pack> --parties 8` + témoin | ~3 min |
| Batterie complète (fichier partagé touché) | `test_capacites.py` sans filtre | ~2 h, en fond |
