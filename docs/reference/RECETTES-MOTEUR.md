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
| After you attack and defeat / After you defeat | `AfterUnitDefeatedUnit(type, "You", Minion\|Enemy, op)` | an001a, an004, vp001a | « attacks AND defeats » → `is_from_attack=True` ; Minion ≠ Enemy, lire le mot imprimé |
| After <allié> enters play | `AfterCardEnterPlay(Response, "This", op)` | 01083 Mockingbird, ho002 | — |
| Hero Action (attack/thwart) sur événement | `WhenInYourPlayTurn(HeroAction, op).SetPlay().SetLabel('attack')` | 05015 Tackle, ho003 | le label alimente Sonné/Désorienté |
| Hero Interrupt: When you play an [[ATTACK]] event | `WhenPlayerPlayCard(HeroInterrupt, "You", CardFinder2("ATTACK", Event), op)` | ho006 (37006, 05011 pour le message) | ≠ « when you SPEND » (32047/54002 : paiement) |
| Response: After attached character gets a status card | `AfterStatusCardPlaceOn(type, "AttachedEnemy", ["Stunned","Confused","Tough"], op)` | 50144, ho012 | — |
| Obligation « Give to the X player » | `WhenThisObligationGiveToYou(op)` + `desc.GiveTo` | an010, ho013 | « may flip » vs « must flip » : deux helpers différents |
| When Revealed (complot annexe) | `WhenThisRevealed(None, op)` | an011, ho014 | — |
| [star] Boost: ... | `WhenCardBecomeBoost("This", op, conditions=[...])` | an013, 16140, ho015, ho017 | l'attaque en cours est `message.would_atk_message`, à lire avec `getattr(..., None)` |
| Setup: ... | `WhenCardSetup("This", op)` | an001b, ok001b | — |
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
| You get +N hit points / +ATK / trait | `GiveKeywordToAttached("You", health=N, attack=N, trait="AERIAL")` | an008, 05023, ho008, ho011 | pour un SOUTIEN non attaché : `GiveKeywordToInPlayWhenApplyThis(Identity, control_by="You", ...)` (an002, ho005) |
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
- Clés : `main_exclusive`, `jouer`, `cibles`, `payer_avec`, `ne_pas_depenser`,
  `surpayer` (obligatoire pour un coût X), `accepter_choix`, `heros2`.
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
