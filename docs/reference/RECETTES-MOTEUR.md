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

## 2. Effets

| Effet | API | Modèle | Piège |
|---|---|---|---|
| Étourdir / désorienter / robuste | `Faces.GiveStatus(cibles, "Stunned"/"Confused"/"Tough", effect)` | 05015, 01083 | cibler avec `canbe_stunned=True` etc. (un Stalwart n'est pas ciblable) |
| Icône qui VERROUILLE une cible (Garde, Patrouille, Crise) | surcharger `CanBeAttackBy` (vilain) ou `CanBeThwartBy` (complot principal), **pas seulement** la résolution | `villain.py`, `scheme_main.py` | ⚠ La Crise ne bloquait qu'à la résolution jusqu'au 11/09/2026 : la cible restait offerte et la carte partait sans effet. Un verrou de ciblage et sa résolution doivent porter **la même condition**, sinon on propose ce qu'on refuse. Une carte qui passe outre doit le **déclarer** (`.SetIgnoreKeyword('Crisis')`), un argument passé à la résolution arrive trop tard ; gate `tools/verifier_ignore_crise.py` |
| Dégâts « au nom » d'une amélioration depuis l'effet d'une AUTRE carte | `effect.this.DealDamage(...)` (la carte qui résout), jamais `amelioration.DealDamage(...)` | zeus/`__init__.py` (Skyfather) | ⚠ `upgrade.py:68` affirme `by_effect.this is self` : une amélioration ne peut infliger des dégâts que dans SON effet. `AssertionError: self=Skyfather by_effect.this=Zeus` (11/09/2026) |
| Une obligation « en jeu » chez un joueur | `joueur.obligations_area.Get()` | zeus/`__init__.py` `AlcoholProblemsDe` | `Worlds.FindCardsOnField(...)` depuis l'effet du héros ne balaie PAS `obligations_area` : la carte était « entered play » et introuvable (11/09/2026) |
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
| Fouiller le deck du joueur | `Search.PlayerCard(effect, player, include_player_deck=True, trait=..., card_type=...)` + `player.GainCard` | an001b, ok001b, ho007 | le « (Shuffle.) » est le comportement par défaut. ⚠ **UNE RECHERCHE SORT LA CARTE DU DECK** : `SelectorEnd.DoMove` la pose dans la ZONE DE TRAITEMENT pour la montrer, et c'est à l'opération appelante de la consommer (main, jeu, défausse). Toute branche qui ne la consomme pas la laissait coincée là, ni en jeu ni en défausse, pour le reste de la partie (61008, 61019, 62022 ; signalement Aghenatak du 20/09/2026). Depuis le 21/09/2026 le sas est noté par `SearchInternal.SearchForCardsInternal` **sur le `by_effect` de la carte qui cherche** (jamais sur l'effet jetable d'`AskChooseSelect`, qui finit avant que l'opération ait consommé la carte : c'est ce qui cassait `ze014`, deux recherches d'affilée), et `EffectInvoker.CloseSearchTransit` rend la carte au deck puis remélange en fin de résolution. **Ce filet ne dispense pas de consommer la carte**, il évite seulement la carte fantôme |
| Le plus au-dessus de la défausse | `player.discard_pile.FindTopmost(CardFinder2("TECH", Upgrade))` + `Faces.ReturnToHand` | 01034, ho013 | — |
| Défausser le deck rencontre | `Worlds.DiscardEncounterCards(n, effect)` | 15004, ho014 | boucle « until » : BORNER par deck+défausse (leçon Underling) |
| Révéler depuis une défausse | `face.Reveal(None, effect)` | an015, ho014 | — |
| Compter les icônes de boost | `FacesCounter.CountTotalBoostIcons([face])` | 15004, ho014 | — |
| Choix secondaire (2e cible, option) | `initiator.ChooseAbilities(effect, ForChoiceAbility("...", op).SetTarget(...))` | 08013, 16155, 14004 | prend la PREMIÈRE branche par défaut (pas de Cancel) ; `Otherwise(op)` pour « sinon » |
| « you may spend a resource » | `ForChoiceAbilityWithCost(Cost("1"), nom, op)` dans un ChooseAbilities | 50134, ho010 | — |
| « ... instead » sur un pouvoir de base | `message.SetBeInstead(effect)` sur le message `WhenUnitWould...` | aa010, ag012, av002, tg016 | ⚠ **PAS depuis `WhenUnitUseBasicPower`** : il est envoyé APRÈS le test de remplacement (`can_attack.py:151`, `can_thwart.py:105`, `can_defense.py:57`), le `SetBeInstead` arriverait toujours trop tard |
| « give X a tough status card. **If you cannot**, ... » | lire le RETOUR de `Faces.GiveStatus(...)`, qui compte les unités réellement servies (`faces.py:180`) | 19001a, tg010 | ⚠ ne PAS déclarer le repli en `SetTarget(canbe_tough=True)` : sans cible légale l'abilité ne part jamais et la branche « if you cannot » est morte (piège `ah007`) |
| Ajouter des cibles à une attaque / un contre EN COURS | `message.AddTarget(*effect.targets)` + `.SetTarget(fn, range="All")` | 25013, tg005, tg006 | ⚠ **jamais un doublon** : la résolution compte les occurrences (`FacesHelper.ListToDict`, can_attack.py:179 et can_thwart.py:122) et multiplie la valeur |

- **« Search your COLLECTION » EST IMPLEMENTABLE** : `Search.Collection`
  (`search.py:371`) interroge `CardsDB.GetPapers` (filtres `card_type`,
  `trait`, `card_class`, `card_classes`, `set_name`, `check_fn` sur le
  `Paper`), fait choisir par `AskChoosePaper` et **FABRIQUE** la carte dans la
  défausse du joueur. Modèles `44009`, `50171`, `dz031` Tribute, `bc004`.
  ⚠ La carte fabriquée arrive dans la **défausse** et n'y est PAS jouable
  (`is_like_in_hand`, `ability.py:235`) : la passer par la MAIN
  (`Faces.AddToHand`) avant `PlayCardsLikeInTurn(..., ignore_resources_cost=True)`.
  ⚠ `card_classes="Any"` ne vaut que les **cinq aspects officiels** : pour
  « basique ou d'aspect », filtrer par `check_fn` sur l'absence de la classe
  `Hero`.
  ⚠ `wd029` Multiverse Recruit assume un ÉCART sur ce même texte, faute
  d'avoir vu cette fonction : **l'écart y est évitable**.
  ⚠ **DEUX CHEMINS, ET ILS NE SE VALENT PAS.** `Search.Collection` passe par
  `AskChoosePaper`, qui rend un `card_id` **sans jamais montrer les cartes**.
  `58031` Cameo, la carte officielle, ne l'utilise pas : elle parcourt
  `CardsDB.papers` elle-même, appelle `CardFactory.GenerateCard` sur **chaque**
  candidat dans `world.area_removed`, puis `AskChooseFace` — le joueur **voit**
  ce qu'il choisit. Sur 70 candidats la différence n'est pas cosmétique.
  Modèle retenu par le pack `cameo_compliment` (`cc001`-`cc003`).

## 3. Mots-clés et bonus continus

| Texte | API | Modèle | Piège |
|---|---|---|---|
| You get +N hit points / +ATK / trait | `GiveKeywordToAttached("You", health=N, attack=N, trait="AERIAL")` | an008, 05023, ho008, ho011 | pour un SOUTIEN ou un ALLIÉ non attaché : `GiveKeywordToInPlayWhenApplyThis(<cible>, control_by="You", ...)` (an002, ho005) |
| **« NOM gets +X »** vs **« YOU get +X »** | `GiveKeywordToInPlayWhenApplyThis(**Hero**, …)` vs `(**Identity**, …)` | an002 Sera → `Hero` ; 06007 Asgard → `Identity` | ⚠ **LIRE LE MOT, pas le modèle.** « You » désigne l'identité, donc les DEUX faces. Un NOM PROPRE n'en désigne qu'UNE : « **Angela** gets +1 hand size » ne vaut qu'en forme héros, puisque l'alter-ego s'appelle Aldrif Odinsdottir. Copier `Identity` depuis Asgard donnait le bonus aussi en alter-ego. **Trouvé en partie réelle par le joueur le 1/9/2026**, jamais par les tests : le seul cas existant se plaçait en forme héros, où les deux écritures donnent le même résultat. → **Tout bonus continu d'identité exige un contre-cas dans l'AUTRE forme.** |
| perd stalwart / steady | `*GiveKeywordToAttached("Character", stalwart=-1, steady=-1)` (rend une LISTE, voir §7septies) | 50144, ho012 | un retrait sur mot-clé absent est neutre |
| gets +1 X for each <face> in play | `ThisGainKeywordForEachFaceInPlay(CardFinder(card_type=SchemeSide2), attack=1, scheme=1)` | 04125 Red Skull, 01059, ho015 | la classe des complots annexes est `SchemeSide2` — `SideScheme` N'EXISTE PAS dans cards.pack |
| gets +1 X par compteur/état dynamique | `ThisGainKeyword(fn, recover=1, change_on_event=OnEvent...)` | an001b, dt133 | — |
| attacks gain overkill/piercing/ranged | `UnitAttackGainKeyword("This"\|CardFinder(...), overkill=True, piercing=True)` | 27078, ho016 | `attacker="This"` pour ne pas toucher les homonymes |
| In expert mode ... | `expert_mode_only=True` (fabriques d'environnement) | 50089b, wd057 | les capacités `[star]` SANS « In expert mode » sont codées TOUJOURS actives (convention moteur, cf. 04125) |
| Bases automatiques (desc, AUCUN script) | `Stalwart`, `Villainous`, `Hinder` (`N*` = par joueur), `Crisis`, `Hazard`, `Acceleration`, `Temporary`, `Toughness`, `Restricted`, `MaxPerUnit`, `MaxPerDeck`, `Boost`, `GiveTo`, `Nemesis`, `StartingThreat` | fiches `mots-cles/` | Temporary : la défausse vit dans `ProcessTemporary` (world_action.py), pas dans has_temporary.py |

- **Compter des icônes de boost : DEUX fonctions, et elles ne comptent pas la
  même chose.** `FacesCounter.CountTotalBoostIcons` (`faces_counter.py:142`) ne
  somme que `CountBoostIconsInternal`, c'est-à-dire les icônes **chiffrées** ;
  l'étoile vit dans une propriété séparée, `boost_star`
  (`has_boost_icon.py:52`), qui vaut 1 dès qu'une `AbilityType.Boost` existe.
  **Seule `CountTotalBoostStarAndBoost` (`faces_counter.py:160`) additionne les
  deux.** Lire le texte imprimé : « the number of **boost** icons » →
  `CountTotalBoostIcons` (`15004`, `ho014`, `sn001b`, `sn003`) ; « each icon
  (**[star] and [boost]**) » → `CountTotalBoostStarAndBoost` (`sn014`). Une pile
  de cartes à étoile seule rend **0** avec la première. Aucune gate statique ne
  voit l'erreur.
  ⚠ Dans la zone « glissée sous » (`is_place_card_area`),
  `CountBoostIconsInternal` court-circuite tout et rend `printed_boost` : les
  effets qui modifient les icônes ne s'appliquent pas là.

| Obligation de set MODULAIRE, sans « Give to » | rien de spécial : `desc` sans `GiveTo`, elle va au joueur qui la révèle | 60184 Wanted (Cops, Fear No Evil) | ⚠ Jusqu'au 18/09/2026 le moteur l'INTERDISAIT : `obligation.py` posait `assert printed_give_to != None` dans `give_to` et `CheckPrintedValue`, alors que `OnPlayerRevealCard` savait déjà faire (`else: message.GetToPlayer()`). Corrigé (`# CORRECTIF`) |
| Attachement de rencontre à Hero Action « Spend a [x] resource OR exhaust your hero → ... » | deux `WhenInYourPlayTurn(HeroAction, op)`, l'une `.SetCost(Cost("B"))`, l'autre `.SetCostFunc(CostFunc.Exhaust("YourIdentity"))` | 60122-60125 (œuvres d'Art Museum Heist, `CapacitesDUneOeuvre`) | dans le harnais, `Puzzle.Action(id, 'HeroAction', 0)` FORCE la première sans la payer : viser l'index 1 pour prouver la branche « incliner » |
| « After this card attaches to a character, <statut> » | `AfterCardAttachTo(ForcedResponse, "This", Unit2, op)` ; `message.to_face` = le porteur | 60122/60124/60125 | part aussi pour l'attache initiale faite par `AttachToFaceWhenPutIntoPlay` (log « s'équipe de ») ; un porteur STALWART refuse stun/confuse en silence : retirer les autres œuvres avant de mesurer |
| « X is 1 more than the number of ... » (escalade dynamique d'un complot) | `EscalationThreat "0"` + `WhenCalcThisSchemeEscalation(fn)` avec `Worlds.GetPlayerNumIcon(effect) * (1 + n)` | 60121b, 16091b | `Puzzle.BeginVillainPhase()` ne POSE PAS la menace : le vérificateur envoie `Message.CalcMainSchemeEscalation(complot, 0, [], [])` et lit `escalation_threat` (`fne_escalade`) |
| « You may spend RRR to A. Otherwise, B » | `ChooseAbilities(ForChoiceAbilityWithCost(Cost("RRR"), nom, op, conditions=[payable]), Otherwise(op2))` | 60127 Tug of War, 50134 | ⚠⚠ **Otherwise n'est offerte que si AUCUNE autre option n'existe**, et la branche payante est offerte MÊME IMPAYABLE (mesure : « couvert = 2 » sur RRR) : le joueur la prend, le paiement échoue, la carte ne fait rien. La condition doit donc tester le paiement : `PeutCouvrirLeCout(joueur, effect, cout)` (`cards/pack/fne/__init__.py`, icônes imprimées de la main + réserve). Et le JOUEUR vient de la clôture du `WhenCardRevealed` : `message.GetToPlayer()` n'existe pas sur `WhenPlayerChooseAbility` (exception avalée = condition fausse = branche jamais offerte) |
| Un sbire qui ATTAQUE LE VILAIN (« it attacks the villain instead ») | `WhenUnitWouldScheme(ForcedInterrupt, "This", op)` : `message.SetBeInstead(effect)` puis `this.BasicAttack([Worlds.FindVillain(effect)], effect)` | 60182 Cop | `BasicAttack` accepte un ennemi comme cible d'un ennemi (2 dégâts mesurés sur Hammerhead) |
| Bonus dynamique « +X où X = le plus haut THW en jeu » | `ThisGainKeyword(fn, scheme=1, change_on_event=OnEvent.Form(Friend))` | 60091 Chameleon | ⚠ `OnEvent.Form` refuse une UNION de types (`'UnionType' object has no attribute 'IsType'`, avalé en partie) : passer la classe mère (`Friend`), pas `Identity|Ally` |
| Un héros qui « gains villainous » EN CONTINU (amélioration) | `*GiveKeywordToAttached(CardFinder(name=…), villainous=1)` | hc010 Outer Demons | Paramètre `villainous` ajouté à la fabrique le 11/09/2026 (`Gain` l'acceptait déjà, dd001a le posait via `GainUntilRoundEnd`). Le héros reçoit alors une carte boost à chaque **attaque** de base (`can_attack.py:264`) ; **pas au contre** (can_thwart.py n'a pas l'équivalent) : écart assumé sur les deux packs |
| Bonus dynamique « +X where X is… » sur une AUTRE carte | `*GiveKeywordToInPlayWhenApplyThis(finder, attack=1, get_new_value=fn)` | hc014 Battle for a Soul | ⚠ Rend une **LISTE** : déballage `*` obligatoire, sinon « 'list' object has no attribute 'paper' » au setup. `get_new_value(effect, face)` **remplace** la valeur (environment_helper.py:184) et est relu à chaque application |
| Obligation : « If not, discard this card » | `Faces.DiscardAll([this], effect)` explicite | hc013 Mental Episode | ⚠ Une obligation révélée **entre en jeu** et y reste : rien ne la défausse par défaut (vu au harnais, « hc013 est encore en jeu »). Coder les deux branches, `RemoveAllFromGame` ET `DiscardAll` |
| Fleeting / « discarded from play at the end of the phase » (mot-clé maison) | `WhenPhaseEnd(ForcedResponse, None, DiscardThisCard, conditions=[IsInPlay])` | 44032 The Merc with the Mouth, dt087 (`Fleeting()` de `determination/__init__.py`) | `phase_name=None` = la première fin de phase après l'entrée en jeu, pas `AfterRoundEnd` ; le harnais n'avance aucune phase : envoyer `Message.WhenPhaseEnd(phase_id, "Player", monde)` dans le vérificateur (kb_bow_fin_de_phase) |

## 3bis. « While X is in the victory display, Y gains <capacité> »

`works_in_the_victory_display` (`environment_helper.py:71-85`) existe, mais
**uniquement** via `GiveKeywordToInPlayWhenApplyThis` — un scan continu qui
n'accorde que des **mots-clés/statistiques** (§3 ci-dessus), jamais une
capacité arbitraire (`Ability(...)` posée à la main dans `GetAbilities()`).

⚠⚠ **Une capacité posée sur LA CARTE ELLE-MÊME (la manigance/le soutien qui
va en vitrine) ne se déclenchera JAMAIS une fois dans la vitrine, quelle que
soit la condition écrite à l'intérieur.** `DeckType.VictoryDisplay`
(`deck_type.py:206-210`) porte `is_out_of_play=True`, et `CardFace.IsInPlay()`
teste `self.card.IsOnField()` → `area.flags.is_in_play` (`card.py:260-261`,
`card_face.py:1021-1033`) : une carte hors jeu n'enregistre **aucune** de ses
propres capacités auprès du bus de messages, le handler n'est simplement
jamais appelé — pas une condition qui échoue, une INSCRIPTION qui n'a jamais
lieu.

**La bonne cible : un objet qui reste TOUJOURS en jeu** (l'identité du héros,
un allié permanent…), avec la vitrine relue comme simple condition externe
(`Worlds.VictoryDisplay(effect).GetAll()`, filtrée par `card_id`). Si la
cible a plusieurs FACES (héros à deux faces), poser la capacité sur **les
deux** : `CardFace.GetAbilities()` est par face, jamais partagé entre elles.

Trouvé le 23/09/2026 sur `rs009` Queen of Sogaria (pack `red_sonja`) : une
Response « draw 1 card » posée sur la manigance elle-même, jamais déclenchée
une seule fois en vitrine — le cas de test la mesurait à zéro piochée,
identique avec et sans la carte en vitrine. Déplacée sur l'identité
(`rs001a.py`/`rs001b.py`), fonction partagée `CapaciteQueenDeSogariaEnVitrine`
(`red_sonja/__init__.py`).

## 4. Ressources

| Texte | Montage | Modèle | Piège |
|---|---|---|---|
| Resource: Exhaust → generate [x] | `CanGenerateResources(type, Resources("G")).SetCostFunc(CostFunc.Exhaust("This"))` | ab007, ma005 | **UNE SEULE CanGenerateResources par carte** (assert) |
| ... generate X ou Y selon l'état | `resources_fn=fn` (évaluée au paiement) | an007 | — |
| ... la ressource imprimée d'une AUTRE carte | `resources_fn` + `FacesCounter.GetPrintedResources([face])` | 21006, ho009 | **NE PAS suivre le couple Can+Do de 31001a** : dans `DoGenerateResources`, `res` est figé AVANT le `PayCost` — un `res_fn` sur `return_exhausted_cards` lit l'état d'avant paiement (constaté sur ho009). Couleur à figer à l'annonce, coût aligné par `CostFunc.Custom` |
| ressource + effet différé sur la carte payée | `ex_operation` / `WhenYouSpendThisCardToPlay` | 54002, 32047, ah007 | — |
| Resource: Exhaust **and spend a [x] resource** → generate [y] (convertir une ressource pendant un paiement) | `CanGenerateResources(type, Resources("L")).SetCostFunc(Exhaust("This")).SetCostFunc(CostFunc.Custom(None, fn))`, où `fn` PRÉLÈVE dans `joueur.res_pool` (`Gain(Resources("Y") * -1)`) et rend False s'il n'y a rien à prélever | ze011 Mount Olympus | ⚠⚠ **PAS `CostFunc.Spend(Cost("Y"))`** (11/09/2026) : Spend ouvre un paiement DANS le paiement (`AskSpendResourcesInternal`) qui **remet le pool à zéro** : les ressources déjà générées pour la carte en cours disparaissent (« total YY » puis « total L » au journal) et la carte payée échoue. Les coûts d'une capacité de ressource sont payés juste avant `res_pool.Gain` (resources.py:404) : c'est là qu'on prélève. |
| Capacité **Special** résolue HORS de la table (depuis la main, pendant un paiement) | déclarer `WhenResolveSpecialAbility("This", op).NoOutOfPlayLimit()`, et au moment de résoudre : `if not face.effect.Find(type=Special): face.effect.RegisterTemp(*face.ability.Find(type=Special), unregister_after_exec=True)` puis `face.ResolveSpecialAbility(joueur, effect)` | zeus/`__init__.py` `ResoudreLeSpecialDe`, ze003 | Une carte en main n'a AUCUN effet enregistré : `ResolveSpecialAbility` ne trouve rien et le message ne part pas (« Zeus resolves Thunder Strike's » suivi de rien). Et sans `NoOutOfPlayLimit`, l'effet enregistré est ignoré parce que la carte est hors jeu. Dans l'opération, le joueur est `message.GetToPlayer()`, pas `effect.GetInitiator()`. |

| Ressource à coût **Custom** (défausser une carte accrochée, retirer un pion…) | `CanGenerateResources(type, Resources("B"), conditions=[dispo]).SetCostFunc(CostFunc.Custom(None, fn))` | hc001a Empowered, ze011 Mount Olympus | ⚠ **`conditions` OBLIGATOIRE** : sans elle la ressource est OFFERTE au paiement même quand son coût est impayable ; `fn` rend alors False et le moteur lève `GameSignal_UndoRequest` (resources.py:409), qui **annule toute la carte en train d'être payée**, sans motif (« Green Hell failed »). Dix cas rouges d'un coup le 11/09/2026 |

| Ressource à coût « **défausser une carte EN JEU** » + « *if X was discarded to pay for this card* » (marquer la carte PAYÉE) | `CanGenerateResources(Resource, Resources("GGG"), for_card=CardFinder(traits=["ATTACK", "THWART", "DEFENSE"], card_type=Event), ex_operation=fn).SetName(...).SetCostFunc(CostFunc.Discard("YouControlCards", card_type=Upgrade, trait="WEAPON", check_effect=lambda effect, face: face.restricted > 0)).LimitOncePerPhase()`. `fn(effect, message)` lit `message.cost_check_effect.cost_func.GetAll()` -> `return_discarded_cards` (rempli par le coût, juste avant `ex_operation`) et pose une marque sur `message.for_effect` : c'est l'effet de la carte PAYÉE, que le script de cette carte relit (`getattr(effect, ...)`) | `tc001a` Overswing, `tc002` Clap Back (pack `casey_jones`) ; modèles `34001a` Phoenix (limite par phase), `32031a` (`for_card` à traits) | `traits=[...]` est un OU. Aucune gate n'attrape une marque posée sur le mauvais objet : le cas « payée par Overswing avec une arme de Casey / d'un AUTRE héros / défaussée AVANT » (`tmnt_casey.py`) la prouve. `Resources("GGG")` = 3 wild (glyphe étoile, vérifié par découpe contre `04010`). Le Sac de Casey est PERMANENT : un `DebugRule` d'un autre set ne peut pas le déplacer (voir `mots-cles/tuck.md`). |

## 4ter. Réduire un coût « quand CETTE carte est la cible »

> ⚠ **Le moteur ne calcule un coût PAR CIBLE que si on le lui demande.**
> Par défaut, `EffectChecker.CheckCost` appelle `process_target(None)` : le
> coût est calculé **une seule fois, avant tout choix de cible**, et
> `Message.WhenCalculateEffectCost.for_targets` arrive **vide**. Une condition
> qui lit les cibles est donc toujours fausse, la réduction ne tombe jamais, et
> le seul symptôme est un `WhenPlayerInTurn failed` dans le journal —
> c'est-à-dire « coût impayable », sans un mot sur la cause.

- La bonne fabrique est `AbilityFactory.ReduceCostToPlayFaceWhen(which_card,
  valeur, which_player, conditions=[...])` (`resources.py:642`), et le **seul**
  champ qui donne les cibles est `message.for_targets`. Ni `for_face`, ni
  `for_effect` n'existent sur ce message (`sender_player.py:234`).
- `which_player="You"` passe par `Select.GetYou(effect)` : inutilisable quand
  la carte source est une **amélioration attachée à un ennemi**. Prendre
  `"AnyPlayer"` et laisser le filtre par cible borner l'effet (modèle `09039`
  * Iron Man: Tony Stark).
- **Il faut inscrire la carte dans `EffectChecker`** (`effect_checker.py`) pour
  que la boucle par cible s'allume :
  `COST_DEPENDS_ON_TARGET_CARD_IDS` si la carte est elle-même la cible,
  `COST_DEPENDS_ON_TARGET_UPGRADE_IDS` si c'est une amélioration attachée à la
  cible. Sans cette ligne, tout le reste est correct et **inerte**.
- Après coup, `AfterPlayerPlayedCard` n'a **pas** `for_targets` : les cibles
  vivent sur `message.play_effect.targets`, et la carte jouée sur
  `message.played_face`.

Constaté le 04/09/2026 sur `bk009` Portal (pack blink). Avant ce jour, la
boucle était déclenchée par un `card_id` écrit en dur dans le moteur.

## 4quater. `PlayCardsLikeInTurn(update_resources_cost=N)` : N est NÉGATIF pour réduire

> ⚠ Piège de signe, même symptôme muet que 4ter : `WhenPlayerInTurn failed`
> dans le journal, carte posée sur la table puis jamais résolue, **sans
> exception Python** (le moteur avale l'échec de `CheckBeforeActive`).

Pour « Action : ... → jouez une carte de votre main en réduisant son coût
de N », le bon appel est `joueur.PlayCardsLikeInTurn([face], effect,
update_resources_cost=-N, forced=True)` (`player_action.py:937`) —
**`-N`, pas `N`**. Le nom du paramètre suggère un delta positif pour
« réduire de N », c'est l'inverse : en interne il vaut `message.UpdateCost
(value, effect)` où `self.cost += value` (`sender_player.py:246`), donc une
valeur positive **augmente** le coût. Vérifié le 23/09/2026 en relisant
TOUS les appels existants du dépôt à ce paramètre (`ant/12024.py`,
`magneto/49017.py`, `sm/27054.py`, `vision/26036.py`,
`bp/black_panther_shuri/51001b.py`, `jj/jessica_jones/61008.py`,
`tt/enchantress/55012.py`) : tous passent une valeur négative, sans
exception. `ignore_resources_cost=True` (l'autre paramètre de la même
fabrique, modèle `ar001a` Bring the War) n'a pas ce piège : c'est un
booléen.

Pour choisir la carte à jouer : passer par le ciblage STANDARD
(`AbilityFactory.ForChoiceAbility(...).SetTarget(Event, canbe_play=True,
from_where=["YourHandCards"])` dans un `joueur.ChooseAbilities(...)`,
modèle `ar001a`), jamais un `AskChooseFace` brut hors de ce mécanisme —
`CheckBeforeActive` (`effect_checker.py:222`) relit l'état posé par le
ciblage standard ; un choix fait autrement laisse la vérification de coût
échouer en silence au moment de la résolution réelle, même quand le
paiement affiché est correctement couvert.

Constaté le 23/09/2026 sur `rs001a` She-Devil (pack `red_sonja`) : `TRACE_OPTIONS=1`
a montré le coût affiché passer de 2 à 3 (au lieu de 2 à 1) avant que le
signe ne soit corrigé.

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
- **Renvoyer une carte en main EN COÛT** : `CostFunc.ReturnToHand(name=..., card_type=..., to_who="Owner"|"Initiator")` (03006, 53002, 04004, tg001a). `to_who="Owner"` pour « to YOUR hand ».
- Coût arbitraire : `CostFunc.Custom(None, fn)` — `fn(targets, effect) ->
  bool`, False bloque le paiement (ho009).
  ⚠⚠ **MAIS `False` N'ANNULE PAS LA MISE EN JEU.** L'effet ne tombe pas, et la
  carte est quand même **jouée puis défaussée** : le joueur la perd pour rien.
  La cause est `CostFunc.Base.HasTargets` (`cost_func.py:47`), qui décide si la
  capacité est **offerte** : elle rend `True` dès que le sélecteur a une cible,
  or `Custom(None, …)` se rabat sur `Select.From("This")`, c'est-à-dire la carte
  elle-même, toujours présente. Le `False` du paiement arrive trop tard.
  **Conséquence : tout coût `Custom` dont l'échec est possible doit être doublé
  d'un `conditions=[…]` qui teste la même chose.** Modèles `58008` Ionic Belt
  (wonder_man) et les cinq capacités de `spider_man_noir` payées sur la pile
  glissée (`PileNonVide`). Constaté le 05/09/2026 par le contre-cas de `sn005`.
- « Hero form only » : `.SetPlay(hero_form_only=True)` (01009, ho012).
- **Une BRANCHE de choix qui coûte** : `ForChoiceAbilityWithCost(cost, nom)`
  (`for_choice.py:110`), le coût en **premier** argument.
  `ForChoiceAbility(...).SetCost(...)` lève un assert explicite du moteur
  (`ability.py:342`).
- **Coût mixte `Requirement` + chiffre** : `Requirement ([energy])` sur une
  carte à 3 se rend `"Y2"` — une énergie **plus** deux ressources, donc trois.
  ⚠ Le harnais lisait `len("Y2") = 2` et sous-payait d'une icône, rendant la
  carte « injouable » sans message. Corrigé le 05/09/2026 dans `payer()`.
- **Dégâts consécutifs d'un allié : la valeur est dans l'ASTÉRISQUE de
  `ATK`/`THW`**, pas dans un champ à part. `can_attack.py:47-52` fait
  `value.count('*')` : `"ATK": "2*"` = ATQ 2 **et 1 dégât consécutif**,
  `"ATK": "2"` = ATQ 2 et **aucun**.
  ⚠⚠ `Message.WhenAllyWouldTakeConsequentialDamage` n'est envoyé **que si la
  valeur imprimée est déjà > 0** (`ally.py:41-46`, garde explicite). Sur un
  allié à 0, un temp accroché à ce message ne part **jamais**, et le cas de
  test reste vert en ne mesurant rien. Pour AJOUTER des dégâts consécutifs,
  passer par la valeur : `ally.GainForThisActive(effect, would_message,
  attack_consequential_damage=N, thwart_consequential_damage=N)` (modèle
  `33016` Coordinated Attack, qui la baisse de 1 ; `bc002` la monte).
- **Deux coûts alternatifs (« A **or** B »)** : un coût est figé à la
  construction, le « or » devient donc **deux capacités** — et si les deux sont
  `Play`, le `card_id` DOIT figurer dans la liste blanche de
  `src/game/card/factory.py`, sinon **le deck ne monte plus aucune partie**
  (leçon `ls005`, modèles `an003`, `vv005`, `br004`).
- **`CostFunc.Discard(name=...)` SANS `from_where` cherche la carte EN JEU,
  jamais en main.** `Select.From(..., from_where=["Default"])` (valeur par
  défaut) résout via `get_InPlay` (`selector_where.py:197`) : « Default »
  n'est pas un synonyme de « la main », c'est littéralement la table. Un coût
  « discard X » où X est une carte normalement tenue en main (pas encore
  jouée) est donc **toujours impayable**, sans le moindre message d'erreur —
  la branche de choix qui le porte est juste écartée en silence, jamais
  offerte. Toujours préciser `from_where=["YourHandCards"]` explicitement
  quand la carte nommée vient de la main. Trouvé le 23/09/2026 sur `rs014`
  A Warrior's Burden (pack `red_sonja`) : « discard Hyrkanium Blade » ne
  déclenchait jamais, le joueur retombait systématiquement sur l'autre
  branche du choix.

⚠ `printed_cost` est un objet `Cost`, pas un entier (29/09/2026, Alias du
pack `determination`) : `ReduceCostToPlayThis(lambda effect:
effect.this.printed_cost)` lève `TypeError: unsupported operand type(s) for
*: 'int' and 'Cost'` dans la fabrique, AVALÉE par le moteur (la carte reste
simplement injouable). Écrire `effect.this.printed_cost.val` (modèles `50081`,
`50082`). Devant une réduction de coût qui « ne part jamais », lire
`/tmp/capacites_*.log`.

## 6. Ciblage

> ⚠ **`SetTarget` prend une CHAÎNE LIBRE, et une chaîne inventée ne lève
> rien.** `SetTarget("EachPlayerIdentity")` a construit sans broncher sous
> `test_cards` : le littéral n'est validé qu'à la sélection, en partie. Avant
> d'écrire un littéral de ciblage, **compter ses usages dans le dépôt** — s'il
> n'apparaît qu'une fois, et que cette fois est la vôtre, il est inventé.
> Constaté le 05/09/2026 sur `br006` Thunderstrike.
> Un événement **Team-Up** doit en outre porter `.SetTarget("TeamUp")` :
> `database.py:223` pose un assert, et son absence fait tomber **le setup du
> deck**.

> ⚠ **`range=(0, n)` ne s'écrit QUE pour un « up to n ».** Le minimum 0 rend
> la cible FACULTATIVE : l'écran s'ouvre sur « 0/1 sélectionnée(s) · nombre au
> choix » avec son bouton de confirmation ACTIF, et valider sans rien cliquer
> résout la capacité à vide (la carte partait même à la défausse). Un texte
> « Stun AN enemy » ou « Choose a status card » est une cible obligatoire :
> `SetTarget(Enemy)` sans `range`. Constaté le 04/10/2026 sur `09032` Crimson
> Bands of Cyttorak (signalement n°51). Le harnais, lui, prend le minimum : un
> `range=(0, n)` fautif y donne donc « 0 dégât, aucun statut », cas rouge.
> `09035` Vapors of Valtorr avait le même défaut, corrigé le 04/10/2026 par un
> minimum DYNAMIQUE : `range=(lambda effect: min(1, len(effect.context.all_legal_targets)), 1)`
> (obligatoire dès qu'une cible existe, 0 sinon, pour que la carte reste
> lançable à vide). Ne PAS écrire `"Zero"` comme minimum ici : il vaut
> `len(targets)`, donc exigerait de TOUT choisir quand plusieurs cibles existent.

> ### ⚠⚠ UN NOM DE CARTE UNIQUE S'ÉCRIT **SANS** L'ÉTOILE
>
> Le « ✦ » imprimé devant un nom unique **n'appartient pas au nom** :
> `cards/paper.py:45-46` fait `is_unique = name.startswith("* ")` puis
> `name = name.lstrip("* ")`. Un `CardFinder(name="* Silver Samurai")`, un
> `Find.Find(name="* X")` ou un `face.IsName("* X")` ne trouvent donc
> **JAMAIS RIEN, ET EN SILENCE** — pas d'exception, pas de log, la carte est
> simplement inerte.
>
> **Payé quatre fois** : `howard_the_duck`, `ms_america`, `patriot`, puis
> `sunfire` le 06/09/2026 — où `sf012` Silver Samurai et `sf014` Silver
> Samurai's Katana **se cherchent l'une l'autre**, si bien que l'étoile en
> tuait **deux** cartes d'un coup. Aucune gate statique ne le voit : ni
> `test_cards`, ni `verifier_appels_modules`, ni `verifier_noms_modules`.
> Seul un cas de test le montre.
>
> ### ⚠ `SetTarget("Players")` REND UNE **FACE**, PAS UN OBJET `Player`
>
> Le sélecteur rend la face d'identité du joueur choisi. Lui appliquer
> `Player.IsType(...)` lève « AttributeError: 'Hero' object has no attribute
> 'IsPlayer' » (`player.py:303`) — **avalée par le moteur**, donc une carte
> qui ne fait rien du tout. Passer par `face.GetControlByPlayer()`.
> Constaté le 06/09/2026 sur `sf002` Atomic Fire.
> ⚠ Pour la phrase exacte « the villain and each minion engaged with that
> player », le dépôt a un littéral dédié,
> `SetTarget("VillainAndEngagedSamePlayerMinion")` (04006, ho004), qui met le
> choix du joueur **dans** le sélecteur et évite la question.

- `SetTarget(Enemy, canbe_stunned=True)`, `range=(1, 2)`, `range=(1,"All")`,
  `from_where=["YouControlCards"]`, `canbe_ready=True`, `canbe_confused=True`.
- AoE « villain and each minion engaged with that player » : littéral
  `SetTarget("VillainAndEngagedSamePlayerMinion")` — le choix du joueur est
  DANS le sélecteur (04006, ho004).
- Deux types de cibles dans un même effet : première par `SetTarget`, la
  seconde par `ChooseAbilities` dans l'opération (08013, ho001a).

> ### ⚠ CORRECTIF DU 05/09/2026 : LA DÉFENSE DE BASE EST ENFIN REMPLAÇABLE
>
> `Message.WhenUnitWouldDefend` portait le commentaire « No `CanBeInstead` »
> et n'héritait donc PAS de la classe. Ses trois sœurs — `WhenUnitWouldAttack`,
> `WhenUnitWouldThwart`, `WhenUnitWouldRecovery` — l'ont toutes. **Aucune carte
> du jeu ne pouvait remplacer une DÉFENSE de base**, et une carte qui dit
> « When you would use a basic power, ... instead » laissait donc passer un
> pouvoir sur quatre, en silence.
>
> Deux lignes, calquées sur `can_attack.py:151` : `CanBeInstead` ajouté aux
> bases du message (`sender_unit.py`), et `if would_defense_message
> .is_be_instead: return None` dans `CanDefense.DefenseInternal`, **avant**
> `SetDefender`. Sans `SetDefender`, `being_atk_message.defense_messages`
> reste vide : la DEF ne réduit rien (`can_attack.py:231`) et aucun
> `AfterUnitDefendEnd` ne part.
>
> Le coût d'inclinaison, lui, reste payé — c'est le modèle **uniforme** du
> moteur pour les quatre pouvoirs (`ThisCanAttack` friend.py:99 et
> `ThisCanDefense` friend.py:236 posent tous deux `CostFunc.Exhaust("This")`
> AVANT la résolution). Le personnage est donc incliné et n'a rien fait.
>
> Trouvé en portant `tg016` Chomped (pack throg).

| Ignorer Crise/Patrouille **selon le paiement** (« if you paid using only [mental]… ignores the crisis icon ») | `.SetIgnoreKeyword('Crisis', paid_with="B")` (au moins une) ou `paid_with="B", only=True` (rien d'autre). **Jamais** `condition=` écrite à la main quand elle lit le paiement | hc006 On the Prowl, 15012 Crisis Averted | Au CIBLAGE rien n'est payé : la condition laisse la cible offerte. À la RÉSOLUTION le paiement est connu : elle tranche. ⚠ Déclarée SANS condition, l'ignorance vaut aussi à la résolution et la Crise ne mord plus jamais (témoin « payée en énergie sous Crise », 11/09/2026). La forme `paid_with` renseigne en plus le rendu : `target_payment[*].warning`, et le plateau demande confirmation avant un paiement sans effet (modale du 11/09/2026 au soir). Gate `verifier_ignore_crise.py` |
| Modifier ce qu'une carte **vaut quand on la dépense** (« treat the next card you spend as if it has double the resources ») | `AfterGenerateResources(AbilityType.Rule, "You", op)` en `RegisterTemp(unregister_after_exec=True)`, et `op` verse une seconde fois `message.res` dans `res_pool` | yd007 Jackpot! | ⚠ **PAS** `WhenCountingResourcesOnCards` : envoyée à CHAQUE lecture de `printed_resource` (rendu des options compris), elle consomme un effet « une fois » sur une simple lecture, jamais sur une dépense ; et la valeur versée à la dépense est `expected_res`, figée au rendu. Jackpot est restée inerte du 04/09 au 11/09/2026 pour cette raison. Montage harnais : `surpayer: "<card_id>"` (ne surpayer que la seconde carte jouée) |
| Réduire le coût de « la prochaine carte que tu joues **ce round** / cette phase / ce tour » | `Worlds.UpdateNextCardPlayCost(joueur, -N, effect, finder=CardFinder(...), in_this="Round"\|"Phase"\|"Turn")` | dz003 (Round), wc014 (Phase) | ⚠ `in_this` doit suivre le mot imprimé : `"Phase"` tombe à la fin de la phase des joueurs, donc une carte jouée en réaction pendant la phase du vilain n'a plus la réduction. `"Round"` ajouté le 06/10/2026 (dz003). Reste en `"Phase"` alors que le texte dit « this round » : `im001b`, `wc014` (à revoir carte par carte). Montage harnais : `Puzzle.EndPlayerPhase()` + `Puzzle.BeginVillainPhase()` en `declencher_apres`, puis `jouer_apres` (sans `EndPlayerPhase`, un cas sur la durée reste vert avec la mauvaise durée) |
| Faire raconter au cartouche de la phase du méchant un événement qu'il ne voit pas (un sbire qui entre en jeu, une carte de statut…) | `world.stat.RecordFaitMechant(world.round_id, {'genre': ..., 'phase': world.GetPhaseText(), ...})` dans le message moteur qui l'observe, sous `try/except`, gardé par `world.phase.IsVillainPhase()` (et par le point de phase si un autre fait raconte déjà la chose) ; côté plateau un type dans `world.ts`, une étape dans `deroule-phase.ts`, un titre dans `deroule-textes.ts`, une ligne dans `RecapPhaseMechant.tsx` (`PHASE_PAR_GENRE` est exhaustif) | `AfterCardEnterPlay` (sender_card.py, fait `entree`), `WhenUnitGainStatus` (sender_unit.py, fait `statut`) | ⚠ Une carte retirée de la partie (`Puzzle.Remove`) ne peut plus entrer en jeu : dans un cas harnais, faire entrer un AUTRE sbire pour la seconde mesure. Vérificateur modèle : `a3_fait_entree` |
| « Limit twice per round » | DEUX capacités identiques, chacune `.LimitOncePerRound()`, avec une condition « pas déjà fait sur cette carte » | hc001a Hellcat | ⚠ Sans la condition, les deux se déclenchent sur le MÊME événement et la limite est consommée par une seule carte |

## 7. Harnais de test (`tools/test_capacites.py`) — pièges payés

- **`[filtre]`** : `... rapport.json "ho0"` — 26 cas en 4 min. La batterie
  complète reste due quand un fichier moteur PARTAGÉ change (règle de portée
  §6bis du GUIDE).
- **Le complot principal de Rhino est `01097b` dès le montage** : *The
  Break-In!* avance à l'étape 2 avant la pioche. `SetThreat('01097a', 6)` crée
  une face fantôme et lève `AssertionError: prev_scheme.card` (11/09/2026).
- **`Puzzle.CreatePlayerDeck(a, b, c)` : la DERNIÈRE carte créée est le
  DESSUS du deck.** Un cas « défaussez les 3 du dessus » qui passait pour la
  mauvaise raison l'a montré (Total Eclipse, 11/09/2026).
- **Les clés de `payment` sont des identifiants d'EFFETS**, pas d'objets. Le
  pilote interdisait `bind_id` (l'objet joué) parmi les effets : quand les deux
  numéros coïncidaient (Precognition objet 13, effet de Thunderbolt 13), il
  manquait une ressource et la carte échouait « sans motif ». Retiré le
  11/09/2026 ; le moteur empêche déjà de se payer soi-même.
- **`TRACE_OPTIONS=1`** imprime `JOUER` (effets de jeu, jouable) et désormais
  `PAIEMENT` (liste des moyens, priorité, choisis, couvert) : c'est ce qui a
  révélé la collision ci-dessus en une ligne.
- **Un effet qui échoue écrit maintenant son motif** dans le journal
  (`player_action.py`, `MotifDEchec`) : « ... failed (check pay) ». Vide quand
  la réponse du client ne désigne aucun moyen de paiement valide.
- **`payer_avec` ne sait pas désigner une capacité de ressource EN JEU dont la
  couleur générée diffère de l'imprimée** (Mount Olympus : génère L, imprime
  R). Repli : `surpayer: True`, qui dépense tout ce qui est offert, et un ordre
  tel que la capacité passe en dernier.

### 7bis. Quatre façons de mesurer *rien* et de le croire vert

Constatées le 04-05/09/2026 (packs blink et texas_twister), chacune a produit
au moins un cas vert qui ne prouvait rien.

- **Moxie (`12016`) fausse TOUTE mesure d'attribut.** Le pilote la joue
  systématiquement en Réponse au passage en forme héros : +1 ATQ, +1 CTR,
  +1 DEF pour le round. `main_exclusive` ne vide la main qu'**après**
  `mise_en_place` : le changement de forme doit donc vivre dans `declencher`.
  Deux packs l'ont payée, l'un en vert (doctor_druid, 3 cas), l'autre en rouge.
- **`Puzzle.Thwart` ne fait RIEN sans menace sur le complot.** Pas de cible
  légale, pas de contre, pas de dégât conséquent — et « 0 dégât » ressemble
  exactement au succès qu'on cherchait. Toujours poser
  `Puzzle.SetThreat('01097b', N)` **et** un témoin de menace dans `attendu`.
  Idem pour `Puzzle.Attack` : le pilote y déclare une **défense**, qui incline
  l'identité toute seule — mesurer « l'identité est inclinée » après une
  attaque ne prouve rien.
- **`dans_deck_joueur` lit un deck LIÉ à sa défausse** (`BindDiscardPile`,
  `player.py:73`) : une carte de la défausse y figure déjà. Pour prouver qu'une
  carte a **quitté** la défausse, écrire une vérification outillée.
- **Le pilote prend le MINIMUM d'un « up to N ».** Avec `range=(0, 2)` il
  choisit zéro cible et la capacité « active » sans rien faire. Il faut
  `cibles`, **et** `choisir_option` : le repli générique n'honore `cibles` que
  pour UNE cible, seule la branche `choisir_option` applique `forcees[:maxi]`.

- **Le pilote paie le MINIMUM d'un coût X, c'est-à-dire ZÉRO.** Le moteur
  annonce `cost: 0` pour un `desc.Cost` valant « X » : la carte « active » sans
  rien faire, journal muet. La clé **`surpayer`** est obligatoire sur toute
  carte à coût X.

  > ⚠⚠ **CORRECTIF DU 08/09/2026 — cette ligne disait l'inverse.** Elle
  > affirmait que `effect.GetCostX()` compte les **cartes** dépensées et qu'une
  > seule carte-ressource donne X = 1 « même quand elle en porte deux
  > (`01090` Strength, "RR") ». C'est **faux** : la fonction rend
  > `context.paid_this_resources.val - context.paid_this_cost.true_val`
  > (`effect.py:509`), c'est-à-dire un compte d'**ICÔNES**. Une seule Strength
  > donne donc **X = 2**. Mesuré sur `sm004` Rapid Strikes (pack
  > spider_man_2099) : le journal dit « would play Rapid Strikes with (RR) »
  > puis exécute **deux** attaques. Un cas écrit sur l'ancienne lecture attend
  > donc la moitié des dégâts et échoue sans qu'on comprenne pourquoi.
- **`Puzzle.Damage` n'est pas « vous ».** Un texte « After **you** defeat an
  enemy » ne se déclenche pas : la `DebugRule` n'est pas le joueur. Faire
  achever la cible par une attaque de base du héros.

⚠ Et un `card_id` ne désigne pas un objet : deux exemplaires de la même carte
partagent l'identifiant. Un contrôle « X est encore en défausse » peut viser
l'exemplaire d'à côté. Préférer, pour ces cas, des cartes **étrangères au
deck**.
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
  (journal `.planning/todos/2026-08-31-portage-beast.md` §5). Le piège a
  continué à se reproduire malgré la prose (`.game-src` / `yd0`, 06/09/2026,
  audit C) : `main()` porte désormais son **propre garde-fou**
  (`_verifier_aucun_autre_harnais_en_cours`, ajouté le 06/09/2026), qui refuse
  de démarrer si un autre `test_capacites.py` / `verifier_tous_les_decks.py` /
  `autoplay.py` cible déjà le même dossier de jeu ; le `pgrep` manuel reste
  utile pour diagnostiquer, il n'est plus la seule protection.
- ⚠ **Une clé `attendu` inconnue d'`etat_attendu` fait désormais ÉCHOUER le
  cas** (garde-fou du 11/09/2026, `CLES_ETAT_ATTENDU`). Avant, elle était
  ignorée en silence et le cas passait au vert sans rien mesurer : `pv_max`
  et `carte_du_surge` (hellcat), `hotes` (su018/su019), `traits_de`
  (iron_patriot), `accroche_a` (ze015) vivaient dans des vérificateurs
  dédiés que ces cas n'appelaient pas. Les cinq sont absorbées dans
  `etat_attendu`. Formats : `pv_max: [[id, n]]`, `traits_de: [[id, TRAIT]]`,
  `hotes` / `accroche_a: [[carte, hôte]]`, `carte_du_surge: "id"` (semée au
  sommet du deck de rencontre, ne doit plus y être). ⚠ Le garde-fou ne joue
  que si le cas appelle `etat_attendu` DIRECTEMENT : un vérificateur dédié
  (`al_etat`, Yondu) lit ses propres clés (`fleche_sur`, `bras_sur`,
  `accroche_a` scalaire) puis délègue le reste ; lui refuser ses clés a fait
  rougir 14 cas à la batterie du 11/09/2026.
- ⚠ **Batterie complète sous charge : faux échecs « ip/port »** (le moteur
  n'est pas prêt quand le pilote se connecte). 60 échecs sur 1866 le
  11/09/2026, dont 41 verts au rejeu un par un. Toujours REJOUER les échecs
  individuellement avant de conclure (`scratchpad/rejouer-echecs.sh` lit le
  rapport et rejoue chaque nom sur un port bas).
- ⚠ **`CreateEncounterDeck` avec une carte du SET DÉJÀ EN JEU** (Sandman `01102`
  dans le scénario Rhino) : `FindOrCreateFace` reprend l'exemplaire du
  scénario et le deck semé n'en garde pas trace. Semer des cartes d'un
  AUTRE set (Klaw `01126`, `01133`).
- ⚠ **Cartes à Renfort CONDITIONNEL comme carte semée** : `01146` Repair
  Sequence et `01104` Hard to Keep Down gagnent surge par leur propre texte
  (« if no damage was healed ») quand rien n'est soigné, et enchaînent les
  révélations. Pris à tort pour un défaut du moteur le 11/09/2026 (trace :
  le mot-clé Surge est auto-attribué). Témoin moteur : cas « SURGE (moteur) ».
- ⚠ **`main` / `Puzzle.Gain` RÉUTILISE une carte existante** (`FindOrCreateFace`) :
  un `01089` listé dans `main` aspire le Genius qu'on venait de poser en
  défausse par `CreatePlayerDiscardPile`, et la recherche de Hedy Wolfe ne
  trouve plus rien (hellcat, 11/09/2026). Payer avec une AUTRE carte que celle
  qu'on veut voir en défausse.
- ⚠ **`surpayer` dépense TOUTE la main** sur la première carte jouée, y compris
  les cartes qu'on comptait jouer ensuite et les ressources d'identité
  (Empowered) : jamais avec plusieurs `jouer`. `ne_pas_depenser: ["hc001a"]`
  bloque une ressource d'identité (elle filtre les effets `is_paying` de la
  carte).
- ⚠ **`EmptyPlayerDeck` après `CreatePlayerDiscardPile` vide AUSSI la défausse** :
  un deck vide y remélange la défausse, qui est alors « retirée ». Poser une
  carte dans le deck (`CreatePlayerDeck('01057')`) avant de garnir la défausse.
- Clés : `main_exclusive`, `jouer`, `cibles`, `payer_avec`, `ne_pas_depenser`,
  `surpayer` (obligatoire pour un coût X), `accepter_choix`, `heros2`.
  **Il n'existe PAS de clé `action`** : une capacité de carte en jeu se
  déclenche par `"declencher": ["Puzzle.Action('<id>')"]` (payé sur bt010/bt011).
- **`Puzzle.Attack(card)` fait ATTAQUER `card`** — ce n'est pas la cible. Un
  `Puzzle.Attack('01094')` fait attaquer RHINO, et un cas qui attend des dégâts
  sur le vilain lit 0 sans rien comprendre (payé sur bt008).
  ⚠ **CORRECTION du 05/09/2026** : ce paragraphe conseillait
  `Puzzle.Attack('<hero>', '<vilain>')` pour faire frapper le héros. **C'est
  faux, et le second argument s'appelle `defender`** (`puzzle.py:385`, docstring
  explicite) : il fait DÉFENDRE cette carte contre l'attaque, il ne la désigne
  pas comme cible. Sur un vilain la différence ne se voit pas — il est de toute
  façon la seule cible — mais `Puzzle.Attack('<hero>', '<sbire>')` fait défendre
  le sbire pendant que le pilote choisit une autre cible. La cible se force par
  **`cibles`**, jamais par le second argument. Payé sur `tg005` et `tg012`, où
  l'attaque partait ailleurs et deux cas lisaient 0 dégât sans rien comprendre.
- **`CanBeAttackBy` n'est consulté qu'à la SÉLECTION des cibles**
  (`ability.py:956`). Une attaque montée par `Puzzle.Attack` + `cibles` passe
  bien par ce filtre ; une cible ajoutée après coup par `AddTarget`, non. Un cas
  qui veut prouver un « X cannot be attacked » doit donc laisser le pilote
  choisir, pas forcer la cible dans le message (payé sur `tg012`).
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
- ⚠ **`degats_identite_min` était une clé MORTE dans `etat_attendu`**
  (réparée le 05/09/2026). Elle n'existait que dans
  `al_frogjolnir_sur_throg`, une vérification propre au pack
  `alligator_loki` : tout cas qui l'employait avec
  `"verifier": "etat_attendu"` voyait son assertion **silencieusement
  ignorée**. Cinq cas du pack throg passaient dessus, et deux d'entre eux
  cachaient un vrai défaut — un sbire convoqué qui n'attaquait pas (le héros
  déclarait une défense, DEF 2 contre ATQ 1), et un « When the round ends »
  qui ne partait jamais. **Avant d'écrire une clé de `attendu`, vérifier
  qu'elle est lue par la fonction de vérification qu'on déclare** : la liste
  du haut de `test_capacites.py` documente des clés que toutes les
  vérifications n'implémentent pas.
- **`Puzzle.BeginVillainPhase()` n'est PAS une fin de round** : elle ouvre la
  phase du vilain. Un « When the round ends » se déclenche en envoyant le
  message à la main depuis une vérification —
  `Message.WhenRoundEnd(monde).Send()`, modèle `brawn_hulk_out_fin_de_round`
  (bw015) et `throg_chomped_fin_de_round` (tg016).
- **`traits_absents`** (ajoutée le 05/09/2026, pack throg) : le pendant négatif
  de `traits`. Sans elle on ne pouvait PAS prouver qu'un trait accordé par une
  carte ne fuit pas sur l'autre face — alors que le §3 l'exige (« tout bonus
  continu d'identité exige un contre-cas dans l'AUTRE forme », règle née du
  défaut `an002` Sera, trouvé **en partie réelle** et jamais par les tests.)
- Preuve par substitution en une commande : `tools/substituer_pack.py`.
  ⚠ **Et JAMAIS à la main.** Remplacer un module par un `return []` avec un
  simple `printf >` laisse le `__pycache__` du pack en place : le moteur
  recharge le `.pyc` de la VRAIE carte et le cas repasse au **vert**, ce qui se
  lit comme « ce cas ne prouve rien » alors qu'il prouve tout. `substituer_pack`
  appelle `purger_pycache()` avant et après chaque carte (lignes 79 et 93),
  c'est la seule différence — et elle change le verdict. Payé le 05/09/2026 sur
  `tg013`, où trois substitutions manuelles successives ont accusé à tort un
  cas correct.

- **`AfterGameSetup` est HORS DE PORTÉE DU HARNAIS.** Il écoute
  `Message.WhenGameWouldBegin`, envoyé **une seule fois** par `world.py:611` à
  la toute fin de la mise en place, donc **avant** que `test_capacites` ne
  prenne la main. Aucune commande `Puzzle.*` ne le renvoie : il faut une
  **vérification dédiée** qui l'envoie à la main
  (`Message.WhenGameWouldBegin(monde).Send()`), sur le modèle de
  `throg_chomped_fin_de_round` pour `WhenRoundEnd`. Cartes concernées :
  tout ce qui porte le mot-clé `Setup` (`cc001`-`cc003`, `58031`).
  ⚠ Et cela ne prouve **pas** que `desc.Setup = "1"` met réellement la carte en
  jeu au départ : cette base-là ne se vérifie qu'en montant une vraie partie
  avec un deck qui contient la carte (`autoplay --deck <chemin vers un deck
  jetable>`).

### 7ter. Pièges du harnais payés par le pack `fne` (bloc 1, 18/09/2026)

- **La partie commence en ALTER-EGO.** `Puzzle.Exhaust('01001a')`, `Tough`,
  `Stun` sur la face héros, ou une `Hero Action`, échouent tant qu'on n'a pas
  basculé : `Puzzle.ChangeForm('01001b')` (= « vers l'autre face ») en tête de
  `mise_en_place`. Sans cela `FindOrCreateFace('01001a')` FABRIQUE une seconde
  identité sans joueur et le rendu tombe sur `assert isinstance(owner, Player)`
  (24 cas rouges d'un coup, message vide).
- **`FindOrCreateFace` fouille le DECK RENCONTRE avant le terrain.** Pour une
  carte présente en plusieurs exemplaires dans le deck (sbires d'un set en
  cours), `Puzzle.Damage('60182', 3)` blesse la copie du deck et le sbire en
  jeu ne bronche pas. `Puzzle.EmptyEncounterDeck()` d'abord, puis
  `PutIntoPlay` crée un exemplaire neuf.
- **`main_exclusive: []` n'est PAS appliqué** (`if cas.get(...)` : liste vide =
  clé absente). Pour une main vide, donner une ressource injouable
  (`["01088"]`). Sinon le pilote joue ce qu'il a : Great Responsibility (01061)
  a encaissé en dégâts la menace que Chameleon devait poser.
- **Une carte posée à la mise en place par le SCÉNARIO** (œuvre au hasard
  d'Art Museum Heist, graine 42 = Inspiring Pottery) fausse les mesures sur le
  vilain : +1 SCH et stalwart. `Puzzle.Remove` des quatre œuvres (`ARTS_OFF`)
  avant de mesurer une stat ou un statut du vilain.
- **`Puzzle.Damage` sur un vilain Toughness** : le premier coup est absorbé ;
  `Damage(id, 1)` puis `Damage(id, 40)` pour le vaincre et faire entrer le
  stade suivant.
- **`defausse_rencontre` ne voyait pas la pile du vilain** (« defausse = [] »
  alors que le journal disait « vers EncounterDiscardPile<3> ») : la clé lit
  désormais aussi `Worlds.GetEncounterDiscardPileCards(monde)`. Et un deck
  VIDE remélange sa défausse : garder une carte au fond (`01193`) quand on
  mesure ce qui a été défaussé.
- **Le pilote DÉFEND une attaque Quickstrike avec le héros** (qui s'incline) :
  poser le sbire en alter-ego, basculer ensuite.
- **`Puzzle.Boost` = une activation du vilain contre le joueur** : son attaque
  non défendue déclenche les Réponses Forcées de la table (60121b vole une
  seconde œuvre). Compter l'effet de bord dans l'attendu.

### 7quater. Pièges payés par le pack `fne` (bloc 2, 18/09/2026)

- **Un vilain recto-verso se déclare avec ses DEUX faces dans le scénario**
  (`"villain": ["60110a,60110b"]`, virgule = faces d'une même carte, comme
  `"schemes": ["60121a,60121b"]`). Déclaré `["60110a"]`, `card.Flip` n'a pas
  de face arrière : il retourne la vilaine FACE CACHÉE, elle « n'est plus en
  jeu » et tout le set tombe (Typhoid Mary, 21 cas rouges). MaGog (`39001a`)
  n'est pas un modèle : il ne se retourne jamais, il `ResetHealth`.
- **`card.Flip` sur un attachement le DÉTACHE** (`CanAttach.OnBeforeFlip` →
  `DetachFrom2` → `MarkAsRemoved`) et ne le raccroche (`OnAfterFlip`) que si
  sa zone est encore la zone d'améliorations, ce qui n'est plus le cas : la
  face B reste dans les limbes (« Bullseye perd l'amélioration », puis plus
  rien). Mémoriser le porteur avant, `AttachTo2` la nouvelle face après
  (`RetournerLaColonne`, bullseye/__init__.py). Le Casque de Juggernaut
  (`40122a`) fait le `Flip` nu : aucun cas ne le mesure.
- **`GiveAdditionalBoostCardForThisActivation` sur le message d'ATTAQUE**
  (`WhenUnitWouldAttack`, sender_damage.py:276) enregistre une capacité Temp
  pour la PROCHAINE activation : appelé pendant la résolution des boosts
  (`WhenBoostCardWouldTurnedFaceUp`), il ne donne rien. Poser la carte face
  cachée tout de suite : `this.CastTo(CanBoost).GiveFacedownBoostCardsInternal(1,
  effect, would_atk_message)`, la boucle de `ResolveBoostCards` la retourne
  (60072 Lady Bullseye : 4 → 7 dégâts).
- **`Puzzle.Ready` / `Puzzle.Exhaust` fouillent le DECK DU JOUEUR avant le
  terrain** (`FindOrCreateFace`, puzzle.py:31) : `Puzzle.Ready('01008')`
  redressait une copie de Web-Shooter restée dans le deck, l'amélioration
  posée ne bougeait pas et l'interruption n'était jamais sollicitée.
  `Puzzle.EmptyPlayerDeck()` en tête de `mise_en_place`.
- **Un statut survit à `Puzzle.Remove` de sa source** : Impossible Object
  retirée (`ARTS_OFF`), le vilain reste Confus et sa manigance suivante est
  remplacée. `Puzzle.Confuse(id)` BASCULE le statut (retire s'il est là) avant
  de mesurer une manigance.
- **`TreatAttachedCardAsMinion` effaçait les mots-clés donnés à l'entrée en
  jeu** : `SwapCardFace` fait entrer le sbire (Purple Man lui donne Guard),
  puis `ResetKeywords()` effaçait tout et l'effet donateur, déjà appliqué, ne
  revenait pas. CORRECTIF moteur (treat.py, deux sites) : les gains venus
  d'autres faces sont sauvés avant le reset et remis après (le reset ne peut
  pas passer avant l'échange : `ResetKeyword(self)` exige une face déjà
  portée par une carte, sinon `'Minion' object has no attribute 'card'`).
  Sans témoin, `Beguiled`/`Enthralled Minion` (21178) portait le même défaut.
- **Un complot annexe Permanent n'était JAMAIS « vaincu »** :
  `EncounterSideScheme.OnBeDefeated` faisait `pass` (scheme_side.py:16), donc
  aucun `WhenSchemeBeDefeated` et un « When Defeated » muet (60113a Establish
  Trust : ni jeton, ni retournement ; « est en train d'être vaincu », puis
  plus rien). CORRECTIF : les messages partent, seule la défausse est sautée.
- **`Resources.CanPayThisCost` ne teste que la COULEUR** (rbyg.py:110) : un
  coût « 2 » y passe avec une seule carte, et la branche « Spend 2 resources »
  était offerte puis échouait (« WhenPlayerChooseAbility failed »), sans
  `Otherwise`. `PeutCouvrirLeCout` exige aussi `total.val >= cout.rbyga.total`.
- **Le Setup d'un environnement (mot-clé `Setup`) passe par `AfterGameSetup`**
  (« Resolve Character Setup Abilities »), pas `WhenCardSetup` (jamais envoyé
  à une carte posée par le mot-clé). Sous graine 42, `Rand.RandomChoice`
  retourne Typhoid Mary : la partie commence sur Bloody Mary (`60110b`), les
  cas qui veulent Typhoid font `Puzzle.Flip('60110b')`.

### 7quinquies. Pièges payés par le pack `fne` (bloc 3A : The Getaway, The Raft Breakout, Stop the Presses!, 18/09/2026)

- **`OnEvent.Counter` / `AfterSchemeRemoveThreat` prennent un TYPE, pas une chaîne.** `"MainScheme"` (chaîne, donc `Sequence`) lève `assert not isinstance(check_rule, Sequence)` dans `CheckWhichCard` (card_type.py:247), AVALÉ : pour `OnEvent.Counter` c'est 15 tracebacks par partie dès qu'un compteur bouge (60130, vu par l'agent B en autoplay, invisible à mes cas qui posaient les compteurs AVANT l'entrée en jeu → un cas « compteur posé pendant que la carte est en jeu » est obligatoire pour tout `change_on_event`). Seuls `PlaceThreatOnSchemes` / `RemoveThreatFromSchemes` acceptent le littéral `"MainScheme"`.
- **`AfterSchemeRemoveThreat` prend un TYPE, pas une chaîne.** `"MainScheme"` (chaîne, donc `Sequence`) lève `assert not isinstance(check_rule, Sequence)` dans `CheckWhichCard`, AVALÉ (`<F>` au journal seulement) : la carte est inerte. Écrire `MainScheme` (la classe), et `last_threat=True` existe pour « when the last threat is removed ». Payé sur 60129a Out Front.
- **`ForChoiceAbility` n'a PAS de `conditions=`.** Seule `ForChoiceAbilityWithCost` en a ; `ForChoiceAbility(name, op, condition=<bool>)` évalue un booléen à la CONSTRUCTION. Construire les branches au moment du choix (fonction rappelée à chaque itération) pour que la condition soit fraîche. `TypeError` avalé sinon. Payé sur 60133, 60151b, 60158.
- **`GiveAbilityToInPlayWhenApplyThis(…, abilities=[…])` ne donne la capacité que sur un événement `Faceup`** (`environment_helper2.py:213`, « Fix for 50070 ») : jamais à l'application initiale ni à l'entrée en jeu. Un sbire posé par `PutIntoPlay`, ou un allié converti, ne la reçoit pas. Pour « Each minion gains: When Defeated… », écouter `WhenUnitBeDefeated(…, Minion, op)` depuis la carte donatrice (`message.trigger` = le sbire). Payé sur 60142b.
- **Le cadre `GiveKeywordToInPlayWhenApplyThis(apply=…)` ne sait pas DÉFAIRE une conversion sbire ⇄ allié sur un événement de jeton** : après `SwapCardFace`, la face alliée est écartée par `is_setting_as`/le finder, et `OnEvent.Token(Ally)` ne voit plus qu'un sbire. `TreatAsMinion` pose en outre sur la carte donatrice des temporaires inaccessibles. Convertir inline (branche `diff == 1` de `TreatAttachedCardAsMinion`) et écouter soi-même `AfterCardPlacedToken` / `AfterCardRemovedToken` / `WhenCardLeavePlay("This")` avec des `Ability(...)` bruts (la fabrique `AfterCardPlacedToken` porte `Condition2.ThisIsTrigger`, elle ne sert qu'à « This »). PV, dégâts, jetons sont des composants de la CARTE : ils suivent la face. `Card.CheckIfCanDiscard` remet la face imprimée avant la défausse : un sbire converti vaincu retourne de lui-même dans la défausse du joueur. Payé sur 60145 Baron Zemo.
- **`AfterUnitAttackEnd` : le joueur attaqué est `GetAgainstPlayer()`** (pas d'attribut `attacked_you`). Payé sur 60146.
- **`AskChooseFace` : « you may » = `forced=False`**, pas `may=True` (`TypeError` avalé). Payé sur 60153, 60156.
- **`AfterPlayerDealEncounterCard` est un `TriggerPlayerMessage` : le joueur est `GetToPlayer()`, la carte `would_message.face`** (pas de `trigger`). Payé sur 60156.
- **`GainToughness` ne pose PAS de carte de statut** : le statut vient de `OnWhenCardEnterPlay` seulement. Un « gains toughness » en cours de partie rend `IsToughness()` vrai sans statut, ce qui est la règle. Mesuré sur 60130 (contre-cas dédié).
- **Harnais : Great Responsibility (01061) absorbe TOUTE menace posée, y compris `Puzzle.SetThreat`**, dès qu'elle est en main ; `main_exclusive` ne vide la main qu'APRÈS `mise_en_place` : mettre `main_exclusive: ["01088"]` PAR DÉFAUT sur tous les cas d'un bloc, et poser la menace dans `declencher` quand elle doit survivre à la main. Payé sur 60148, 60150, 60151b (menace « 2 » alors que 5 étaient posées).
- **Harnais : un deck de rencontre vidé par le cas remélange sa défausse** (déjà en §7ter) : pour mesurer une carte défaussée par Ben Urich / Robbie, laisser une carte au fond (`01193`).
- **`WhenCardSetup` prend deux arguments** `("This", op)` : à un seul argument, le complot 1A ne fait rien (précision du coordinateur, trois scripts corrigés).
- **Pendant qu'un autre agent édite `src/game`**, une passe peut mourir en `NameError`/`AttributeError` d'import ou de `Puzzle` (« processus mort », « 'World' object has no attribute 'world' ») : attendre un marqueur (la ligne fautive disparaît) et rejouer, ne pas conclure sur ses propres scripts.

### 7sexies. Pièges payés par le pack `fne` (bloc 3B : Drive, Disasters, Tombstone, Tracksuit Mafia, 18/09/2026)

- **`Puzzle.SetThreat(id, n)` vers le BAS est un RETRAIT** : il envoie `WhenSchemeWouldRemoveThreat` / `AfterSchemeRemoveThreat`. Sur Collapsing Bridge, `SetThreat(2)` depuis 3 déclenchait la Réponse Forcée (3 → 2 → 3) et le cas « dernière menace » ne partait jamais de 2. Descendre par des contres (`Puzzle.Thwart` d'un allié à THW 2, puis d'un second).
- **`operation=` de `TakeIndirectDamage` / `TakeDamage` n'est PAS rappelée pour une unité VAINCUE** (`can_health.py:288`, `if unit.IsInPlay()` après `Death`) : un compteur « for each ally defeated this way » y reste à zéro. Comparer la liste des alliés en jeu avant et après (60199).
- **`AfterSchemeRemoveThreat` part AVANT le contrôle de défaite d'un complot annexe** (`scheme.py:145-150`) : une Réponse Forcée qui repose de la menace rend le complot invincible sans garde `this.threat > 0` (60180).
- **`Asset2.CanAttachTo` ne teste que MaxPerUnit (et `CheckIfFaceCanAttachTo`)**, jamais la cible imprimée « Attach to … ». Celle-ci vit dans le sélecteur de `AttachToFaceWhenPutIntoPlayInternal`, exposé depuis le 18/09/2026 en `ability.attach_selector` sur l'ability `func_name="AttachToWhenEnterPlay"`. Pour « an attachment that can attach to a minion » : `attach_selector.selector_filter.CheckFinder(sbire, GameRule(face))` (modèle `PeutSAccrocherAUnSbire`, tombstone/__init__.py). ⚠ Pas `GetAllLegalTargets`, qui applique le tri `highest_*` et dépend des autres sbires en jeu. ⚠ `GameRule` n'est pas ré-exporté par `cards.pack` : import local, sinon `NameError` avalée et « aucun candidat » sans un mot au verdict.
- **Un deck rencontre épuisé par `DiscardEncounterCardsUntil` se remélange avec sa défausse** (`deck.py:483`) : `defausse_rencontre` est vide après une fouille infructueuse ; mesurer `dans_deck_rencontre`. La boucle est bornée (un seul passage).
- **Groot (`16047`) se soigne de 2 après avoir défendu** : comme Moxie, un allié à réponse fausse la mesure. Défenseur neutre à 5 PV : Brawn (`10011`).
- **Retaliate ne mord pas si le défenseur est vaincu par l'attaque** (« X ignore Retaliate sur Y » au journal, `can_retaliate`) : un cas qui veut mesurer la riposte doit laisser le sbire vivant.
- **Teamwork, règle par défaut du moteur (`v16_teamwork = False`) : TOUS les sbires au trait s'activent**, pas seulement l'entrant (Bro déjà là + Ivan = 2 + 2). Un cas Teamwork doit compter les deux.
- **`Puzzle.Attach(carte, hote)` pose BRUT dans l'inventaire** (sans `AttachTo2`) : suffisant pour « porte un attachement VEHICLE », pas pour un bonus `ATK+`.
- **Un port de la plage peut être occupé par un autre processus** (42050, deux passes de suite) : le cas rend « aucun resultat (processus mort) » et le journal dit `AssertionError: ip='127.0.0.1', port=42050`. Rejouer sur une autre base (42100, 42200) avant de conclure.
- `Puzzle.Reveal(id)` pose la carte sur le DESSUS du deck rencontre avant de la révéler : un `CreateEncounterDeck('01193', '60203', '01186')` laisse donc l'ordre [fond … 01186, carte révélée] et « discard until » défausse 01186 d'abord.

### 7septies. Pièges payés par le pack `fne` (bloc 4 : Kingpin, 18/09/2026)

- **`Puzzle.SetThreat` en `mise_en_place` est absorbé par Great Responsibility (01061)** quand elle est dans la main de départ : « WhenSchemeWouldPlaceThreat est remplacé par Great Responsibility », la menace posée manque de 1 à 3 et le héros prend les dégâts (7 cas rouges d'un coup : 60159a, 60160a, 60161b ×3, 60164, 60168). `main_exclusive` ne vide la main qu'APRÈS `mise_en_place` (§7bis) : tout `SetThreat`/`PlaceThreat` d'un cas à `main_exclusive` va dans `declencher`, en tête.
- **`Puzzle.Discard` d'une carte NEMESIS la RETIRE du jeu** (« Vulture retirée(s) », journal 2148 première passe) : sa pile de défausse « propriétaire » est la réserve nemesis. Pour la mettre en défausse de rencontre : `Puzzle.MoveTo('01167', 'EncounterDiscardPile')`.
- **`Puzzle.FindOrCreateFace` ne fouille PAS `set_aside_nemesis_sets`** (puzzle.py:21 : deck joueur, défausse, deck/défausse rencontre, `aside_deck`, `set_aside_deck`, puis le terrain) : `Puzzle.Remove('01166')` a FABRIQUÉ un doublon et la réserve est restée pleine (journal 2145 première passe). Repli : un vérificateur qui vide la réserve lui-même (`Faces.RemoveAllFromGame` + `PuzzleHelper.Exec`), `fne4_bag_sans_reserve`. Demande D4.
- **`Puzzle.EmptyEncounterDeck()` emporte les sbires UNDERLING** : « find an UNDERLING minion » ne trouve plus rien (journal 2149 première passe : « 0 UNDERLING en jeu »). Ne pas vider le deck quand la carte testée FOUILLE le deck.
- **Une carte boost donnée à la révélation (James Wesley) vient du deck À CET INSTANT** : seme le deck AVANT `Puzzle.Reveal`, sinon c'est Stilt-Man (3 icônes) qui sort et la manigance vaut 5 au lieu de 2 (journal 2115 première passe).
- **Une carte nemesis révélée peut porter Surge elle-même** (Sweeping Swoop 01168) : le témoin « pas de surge » d'un cas nominal ne prouve rien. Prouver la révélation par `defausse_rencontre` de la carte tirée.
- **Face échangée par `TreatAsAlly` : `par_id` trouve ENCORE l'ancienne face « en jeu »** (même carte, `IsInPlay()` vrai) : « le sbire 60169 est encore en jeu » alors que la conversion avait marché. Tester `trouve.card.face is trouve` / `Minion.IsType(card.face)`.
- **`GiveKeywordToAttached` rend une LISTE** (comme `GiveKeywordToInPlayWhenApplyThis`) : sans `*`, `'list' object has no attribute 'paper'` à la CONSTRUCTION du deck de rencontre, et c'est tout le scénario qui ne monte plus (70 cas rouges d'un coup, message « la partie a planté »). Le §3 de RECETTES ne le dit que pour `hc010`.
- **`UnitCannotHaveUpgradeAttached` ne cache PAS la cible** : `Message.CheckIfFaceCanAttachTo` (sender.py:205) n'est ENVOYÉ NULLE PART dans `src/game` ; seule la moitié `WhenCardWouldAttachTo` joue, l'amélioration est payée puis défaussée à l'attache (journal 2084). Vaut pour 46003, 48027, sabretooth. Demande D1.
- **Le moteur n'a aucun message « would be given a facedown boost card »** (`GiveFacedownBoostCardsInternal`, can_boost.py:9, enchaîne `PopEncounterCards` sans fenêtre) : une interruption sur ce texte se pose sur `WhenEnemyActivateAgainstYou` et retranche 1 à `property.additional_boost_card` (attaque) / `give_additional_boost` (manigance), lus à can_attack.py:265 / can_scheme.py:114 ; un compte négatif est absorbé par le `if num <= 0: return`. Demande D2.
- **Sous graine 42, Vulture (nemesis de Spider-Man) est EN JEU dès la mise en place** du scénario Kingpin (Setup de 1A) et engagé : `Puzzle.Remove('01167')` avant toute mesure « non engagé avec un sbire » ; et son ATK 3 (Quickstrike) mange le héros dès qu'on le laisse là en forme héros.

### 7octies. Pièges payés par le coordinateur (Protection Racket, campagne, fusion des blocs, 18/09/2026)

- **Plusieurs complots principaux en jeu (Protection Racket, un par joueur)** :
  le moteur les supporte (précédent Tower Defense, `GettingMainScheme`,
  `world.current_player`) à condition que CHAQUE complot réponde à
  `GetMainScheme` seulement pour SON joueur (`ComplotDuJoueur(effect, joueur)
  is this`), que l'élimination d'un joueur passe par `SetGameOver(False)` et
  que les jetons d'accélération soient reflétés sur tous. La manigance de base
  du vilain va sur le complot du joueur visé (article FFG).
- **`WhenCampaignSetup` part APRÈS la mise en place des complots** : le complot
  est déjà retourné côté 1B, `effect.this` est la face 1A. Une garde « seul le
  premier complot parle » doit comparer les CARTES (`complots[0].card is
  effect.this.card`), pas les faces (`is` sur la face est toujours faux).
  Payé sur la garde `_premier_complot` de 60134a (Mary Walker serait entrée
  N fois, les marques posées N fois).
- **Un complot annexe révélé par `Find.FindAndReveal` applique son Hinder** :
  Jackknifed Tanker Truck (2 menaces, Hinder 1) vaut 3 avant la marque de
  campagne, 4 après. Attendre 4, pas 3.
- **La partie commence en alter-ego** (§7ter) vaut aussi pour les statuts :
  « each identity gets a tough status card » se mesure sur `01001b`, pas
  `01001a`.
- **Batterie complète lancée PENDANT que d'autres agents éditent `src/`** :
  12 rouges transitoires (Venom, Webbed Up, Agent 13...) tous verts rejoués
  un par un ensuite. Un rouge de batterie n'est une régression que s'il
  se reproduit SEUL, une fois l'arbre stable ; la batterie de fin de portage
  se lance quand plus personne n'écrit.
- **Moteur, ajouts du 18/09/2026** (demandes des agents, prouvées par leurs
  cas) : `Asset2.CanAttachTo` envoie `Message.CheckIfFaceCanAttachTo` (il
  n'était envoyé nulle part) et `CanPlayThisUpgradeCard` filtre ses cibles
  par `CanAttachTo` ; `Message.WhenEnemyWouldBeGivenBoostCards` (+ fabrique
  `AbilityFactory.WhenEnemyWouldBeGivenBoostCards`, `SetNum` /
  `SetBeInstead`) envoyé par `CanBoost.GiveFacedownBoostCardsInternal` pour
  TOUTES les sources ; `Ally` hérite de `HasVillainous` (Black Cat ralliée,
  gabarit `fne_black_cat_ally`, Villainous 1) ; `ability.attach_selector`
  exposé sur « AttachToWhenEnterPlay » (Beetle) ; `Puzzle.FindOrCreateFace`
  fouille aussi `set_aside_nemesis_sets`.
- **`CanPlayThisUpgradeCard` sert AUSSI aux soutiens** (Helicarrier, « under
  a player's control ») : tout filtre ajouté à son sélecteur doit d'abord
  tester `Asset2.IsType(effect.this)`, sinon `AttributeError` avalé et le
  soutien devient injouable.

### 7nonies. `select_rule` n'est applique NULLE PART (18/09/2026, 45017 Suit Up)

- **`SelectorRule.AfterSelectTargets` (`src/game/selector/selector_rule.py`)
  ne verifie ni `DifferentType` ni `DifferentCards`** : il ne regarde que le
  NOMBRE de cibles, les couts combines et la regle `VillainAndMinions...`.
  `EffectChecker` ne s'en sert que pour compter combien de types EXISTENT
  parmi les cibles legales, jamais pour contraindre la selection. Le plateau
  lit `select_rule` (`ui-app/src/board/ask.ts`) et ne s'en sert nulle part.
  Consequence mesuree : `45017` Suit Up laissait prendre DEUX ameliorations
  la ou la carte veut un allie et une amelioration. Deux cartes concernees
  dans tout le depot : `45017` (reecrite en deux recherches successives) et
  `01042` Ancestral Knowledge (`DifferentCards`, encore ouverte).
- **Un `check_again_fn` qui refuse le choix APRES coup fait perdre la carte** :
  l'effet echoue et l'evenement part a la defausse sans rien faire. Une regle
  de selection doit ecarter la cible AVANT le choix (filtre du selecteur), pas
  juger le resultat.
- **« une amelioration attachable a CET allie » se demande au moteur** :
  `CardFinder(canbe_attach_to=<face>)` appelle `Upgrade.CanAttachTo`, qui
  relit le selecteur de la capacite « Play » de l'amelioration examinee. Deux
  `Search.PlayerCard` de suite (allie, puis amelioration filtree) rendent la
  phrase exactement ; patron `pt002` (pack patriot).
- **Harnais : une Alter-Ego Action ne demande AUCUN changement de forme.** La
  partie commence en alter-ego (§7ter) et `Puzzle.ChangeForm('01001b')`
  RETOURNE la face en jeu, donc passe en forme heros : trois cas rouges ou la
  carte restait en main.

### 7decies. La batterie complete lue de travers : 57 faux rouges (18/09/2026)

- **La copie gelee du harnais ne trouvait pas `tools/decks-de-test.json`.**
  La batterie complete se lance depuis `/tmp/test_capacites_frozen.py` (pour
  qu'une regeneration de cas ne change pas une passe en cours). Or le fichier
  des « anciennes moities d'aspect » etait resolu A COTE DU SCRIPT :
  `_decks_de_test()` rendait `{}` en silence, les decks des heros restaient
  vides, et **57 cas tombaient au rouge** sur des packs sans aucun rapport
  entre eux (spider_man_noir 13, night_thrasher 12, ms_america 6, venom 4...).
  Symptomes typiques : « X n'est pas en main », « degats sur l'identite = 0 »,
  « 1 carte(s) posee(s) sous ... (attendu 0) ».
- **Le signe qui ne trompe pas** : rejoues SEULS (ou par pack, avec un filtre),
  ces memes cas sont VERTS. Un rouge de batterie qui redevient vert a
  l'unite n'est pas une regression : c'est la batterie qu'il faut regarder.
  Deux passes completes ont ete lues de travers avant qu'on ne compare le
  chemin du script.
- **Correctif** : `_chemin_decks_de_test()` cherche a cote du script, puis
  `./tools/`, puis `../tools/` (les enfants font `os.chdir(game_dir)`, donc
  `../tools` depuis `.game-src*` retombe sur le vrai fichier).
- **Regle generale** : tout fichier annexe resolu par `__file__` dans un outil
  qu'on COPIE ailleurs doit avoir un repli, sinon il disparait sans un mot.

### 7undecies. Le harnais ne joue pas les regles d'une vraie partie (18/09/2026)

- **Une vraie partie tourne en regles v1.6** : `launcher.js` pousse `v16_all`
  des que « regles v1.6 » est coche, ce qui est le defaut, et `SetRule`
  bascule alors TOUS les `v16_*` (`world_rule.py`) : Teamwork n'active que le
  sbire qui ENTRE, un personnage sonne peut tenter d'attaquer, elimination,
  revelation, capacites referentielles...
- **Le harnais, lui, monte la scene avec `rules` VIDE** : les cas mesurent donc
  les regles d'AVANT 1.6. Constate sur Teamwork (pack `fne`, bloc 3B) : le
  harnais voit s'activer TOUS les sbires du trait (2 + 2 degats), un joueur
  n'en verrait qu'un.
- **Option ajoutee** : `REGLES_V16=1` devant `test_capacites.py` monte la scene
  avec `v16_all`. Le defaut reste inchange : basculer tout le harnais demande
  de mesurer carte par carte ce que la regle deplace. Premieres mesures :
  pack `spider_man_noir` 40/40 dans les deux regimes.

### 7duodecies. « L'exces » ne vit qu'a la defaite, et une carte inerte peut passer au vert (18/09/2026)

- **`AfterUnitAttackEnd` n'a PAS `excess_damage`** (sender_damage.py:558 : il
  porte `total_dealt_damage`, `damaged_targets`, `atk_messages`). Un
  `getattr(message, "excess_damage", 0)` y rend donc TOUJOURS 0, en silence :
  `60140` Man-Bull n'a jamais pose la moindre menace. L'exces n'existe qu'a la
  DEFAITE : `WhenUnitBeDefeated.excess_damage` (= `-health`, sender_unit.py:70),
  et la fabrique sait filtrer : `by_attack=True`, `attacker="This"`,
  `took_excess_damage=True`.
- **Une carte inerte peut avoir DEUX cas verts** : ceux de Man-Bull mesuraient
  1 menace sur le complot du joueur... que Battle in the Bodega (60134b) posait
  de son cote sur la meme attaque. Seule la preuve par SUBSTITUTION l'a vu
  (« rouges 0/2 »). Quand une carte partage la table avec une autre qui produit
  LA MEME grandeur, le cas doit se jouer ailleurs : les deux cas ont ete
  refaits sur un scenario NEUTRE (Art Museum Heist), complot remis a zero.
- **Lire un verdict de substitution** : un cas vert sans son module est
  acceptable dans trois cas seulement (contre-cas d'absence d'effet, valeur
  native lue dans `desc`, cas dont le sujet est un AUTRE fichier comme un
  helper de set). Sinon c'est un cas qui ne teste pas ce qu'il croit.
  `generateurs-fne/qui_reste_vert.py` (copie dans `.planning/todos/`) rejoue
  module par module et NOMME les cas restes verts, ce que
  `substituer_pack.py` ne fait pas.

### 7terdecies. Trois regles tranchees par le Rules Reference v1.8 (19/09/2026)

Le guide officiel est dans le depot : `assets/docs/mc01_rules_reference_v18.pdf`
(extractible avec `pypdf`, il n'y a pas de `pdftotext` ici). Trois entrees ont
servi, et elles resservent :

- **DEFEAT** : « si un complot annexe n'a plus de menace, il est vaincu », et
  **IN PLAY AND OUT OF PLAY** : « les capacites d'une carte ne peuvent etre
  declenchees ou affecter la partie que TANT QU'ELLE EST EN JEU ». D'ou :
  un complot ramene a zero est vaincu, defausse, et sa Reponse Forcee
  « posez 1 menace ici » ne peut plus rien poser (60180 Collapsing Bridge).
- **PREVENT** distingue les degats **infliges** des degats **subis** : un
  effet qui previent reduit ce que la cible SUBIT, pas ce qui lui est
  INFLIGE. D'ou : « ne peut pas SUBIR de degats » laisse jouer une
  interruption « quand X subirait des degats » (patron Armored Rhino Suit),
  alors que « ne peut pas se voir INFLIGER de degats » supprime la fenetre
  elle-meme, et l'interruption ne part pas (60131 + 60129a).
- **CANNOT** : absolu, prime sur toute autre capacite, sauf si une carte le
  contredit explicitement (Golden Rules).

### 7sexdecies bis. `ne_pas_depenser` interdisait aussi l'id de l'OBJET carte, qui peut coincider avec l'id de l'EFFET d'une autre (23/09/2026)

- **Le bug, trouve sur `rs004`/`rs007` (pack red_sonja)** : le filtre
  `ne_pas_depenser` ajoutait a `interdits` DEUX choses — les vrais ids
  d'effets payants (`effet.object_id`, corrects) ET l'id de l'OBJET CARTE
  lui-meme (`objet_id`, cense etre inoffensif : « les cles de `payment` ne
  sont jamais des ids d'objet carte », deja documente juste au-dessus dans ce
  meme fichier au sujet de `bind_id`). Objets carte et effets vivent dans
  DEUX espaces de numeros distincts, mais RIEN ne garantit leur DISJONCTION :
  ici, l'objet carte de `rs007` portait l'id `16`, qui coincidait EXACTEMENT
  avec l'id de l'effet payant d'une carte totalement differente (`01089`
  Genius, « BB ») pour cette mise en place precise. Le filtre excluait donc
  Genius EN PLUS de rs007, sans le moindre rapport, et la carte testee
  tombait injouable faute de paiement complet (`<E> ... failed`) — un rouge
  qui ressemblait a un bug de CARTE, reproductible a l'identique (memes ids a
  chaque relance), et qui a fait perdre du temps a chercher du cote de
  `rs004.py`/`Worlds.UpdateNextCardPlayCost` avant qu'une trace `TRACE_OPTIONS`
  couplee a un print temporaire de `objet.GetEffects()` ne montre le vrai
  coupable.
- **Correctif** : retirer l'ajout de `interdits.add(str(objet_id))` — il
  etait deja etabli comme inoperant pour son role annonce (filtrer par id
  d'objet carte ne matche jamais les cles de `payment`), et purement
  dangereux par coincidence numerique. Seuls les ids d'effets payants
  (`effet.object_id`, via `objet.GetEffects()` + `is_paying`) doivent
  alimenter `interdits`.
- **Piege associe, meme scenario** : une manigance a target invalide passe
  aussi le harnais sans message clair. « Remove threat from a scheme »
  n'offre jamais le complot PRINCIPAL comme cible legale a round 1, phase
  Joueur, AVANT toute phase Vilain — il n'a encore RECU AUCUNE menace
  (`StartingThreat` d'un complot annexe s'applique a LUI, pas au principal).
  Un cas qui vise le complot principal a ce moment-la voit son option de
  jeu disparaitre (`jouable = False`) sans qu'aucun message ne le dise :
  toujours viser un complot ANNEXE (avec un `StartingThreat` non nul, ou
  `Puzzle.PutIntoPlay` suffit) pour prouver un « remove threat » en debut de
  partie.
- **Le signe qui doit alerter** : un `ne_pas_depenser`/`interdits` dont on
  suspecte l'efficacite se verifie en ajoutant temporairement un `print` des
  candidats/interdits sous `TRACE_OPTIONS` (jamais en le laissant en place :
  c'est un ajout ponctuel, a retirer avant de committer) — un cas qui « passe
  au vert » alors que sa carte cible ne devrait meme pas etre affordable est
  souvent un signe que le paiement a ete couvert par un AUTRE moyen que celui
  prevu par le cas (voir aussi §7duodecies, meme famille de faux-positifs).

### 7septdecies. Pièges payés par le pack `conan` (25/09/2026)

- **Faces d'identité mises de côté : drapeau `hors_pile_identite`.** Une
  identité à 5 faces dont 2 n'existent qu'après un événement (King Conan)
  ne doit pas les offrir au changement de forme. On pose l'attribut sur la
  face (`MarquerHorsPile`, pack conan) ; le moteur l'ignore alors dans
  `player_setup.py` (conditions de `register_change_to`),
  `GetAllIdentityFace` et `identity.py` (`ChangeToOtherHeroForm`,
  `ChangeToOtherForm`). Crochet additif : sans le drapeau, rien ne change.
  Avec 5 faces, `Puzzle.ChangeForm` devient ambigu : utiliser
  `Puzzle.ChangeToFace('<depart>', '<arrivee>')` en mise en place.
- **Clé `attendu.face_identite`** (harnais) : vérifie l'id de la face
  d'identité visible à la fin du cas. Indispensable dès qu'une carte
  retourne l'identité sans changement de forme (couronnement).
- **« Discount N (TRAIT) » : réutiliser `DiscountAbility`** du pack `fne`
  (`from cards.pack.fne import DiscountAbility`, modèle 60023). Toujours
  ajouter un témoin « sans le trait et sans ressource, la carte n'est PAS
  gratuite ».
- **`verifier_appels_modules.py` ne voit que les appels typés** (`Faces.x`,
  variables issues de `CastTo`). Un `effect.this.Inexistant()` lui échappe.
  Chemin du dossier de jeu en ABSOLU. Pour le calibrer, injecter
  `Faces.MethodeQuiNExistePas()`, jamais un appel sur `effect.this`.
- **Aucune modification de `src/` pendant un harnais ou un autoplay.** Les
  dossiers `.game-src-parN` pointent sur `src/` par lien : une injection de
  calibrage dans cn010.py, faite pendant un autoplay, a produit 6
  tracebacks dans une partie qui n'avait rien à voir. Attendre la fin, ou
  travailler sur une copie dans le scratchpad.
- **« 0 ligne conan » dans un rapport statique ne prouve pas la
  couverture.** `test_cards.py`, `verifier_api_cartes.py` et
  `audit_cartes.py` ne listent que les défauts. Pour prouver qu'un pack est
  parcouru, instrumenter une COPIE de l'outil (un `print` par module du
  pack) et compter les lignes.
- **Autoplay : un « Play » impayable est déclinable** même à cible
  obligatoire. Le moteur offre toute carte en main, payable ou non
  (`CanPlayBy` vrai, `target_payment.payment` vide). Le pilote gardait
  pourtant l'option « par prudence » quand sa plage était [1, 1], et la
  partie finissait « bloquée » (graine 2, main réduite à cn003). Corrigé
  dans `tools/autoplay.py` : devant un blocage de ce genre, lire les
  options avec une copie instrumentée du pilote avant d'accuser la carte.

### 7octodecies. Pièges payés par les cartes de campagne de Skrull Menace (sk263-sk289b, 15/10/2026)

- **`main_exclusive` défausse la main de départ APRÈS `mise_en_place`** : une carte posée par `mise_en_place` réagit à cette
  défausse (Super-Skrull allié a attaché les cartes SUPERPOWER de Spider-Man, `thwart` +2 au lieu de +1). Poser la carte à
  mesurer dans `declencher`.
- **`Puzzle.CreatePlayerDeck` AJOUTE au vrai deck de 40 cartes** (il ne le remplace pas) : une recherche ou un « discard until »
  voit tout le deck et le pilote prend la première carte légale (Enhanced Spider-Sense au lieu de Lazerfist). `Puzzle.EmptyPlayerDeck()`
  d'abord, et `cibles: [card_id]` pour FORCER la carte cherchée. Un deck vidé par `DiscardDeckUntil` se remélange avec la défausse :
  la défausse est alors vide, mesurer `dans_deck_joueur`.
- **`Puzzle.SetThreat` vers le BAS est un retrait** (RECETTES §7sexies) : une manigance qui dit « threat cannot be removed » le
  refuse (Skrull Military Training reste à 3). Partir de la menace imprimée.
- **« take N damage → » en coût n'est payé que si TOUS les dégâts sont subis** (`TakeDamageOnCall`, cost_func.py) : un allié
  Ténacité (Paibok sk265) ne peut pas payer sa Réponse tant qu'il a sa carte Robuste d'entrée (elle est consommée en vain).
- **`TreatAsMinion` avec un gabarit qui porte une capacité** : `CreateFace` a DÉJÀ ajouté les capacités du module ; l'ancien bloc
  « Hack for 50171 » les ajoutait une 2e fois AVANT l'échange (plantage `'Minion' object has no attribute 'card'`, puis pioche en
  double). Corrigé dans `treat.py` (échange d'abord, enregistrement ensuite, sans doublon) : un gabarit sbire peut maintenant
  porter son texte (`skrull_war_minion`).
- **`Faces.TreatAsAlly(sbire, gabarit, joueur, effect)`** : (1) l'allié reprend le NOM, l'image, l'ATQ et SCH->CTR mais PAS les PV :
  un sbire cherché dans le deck rencontre n'a jamais eu de PV courants et l'allié (PV 0 du gabarit) est vaincu en entrant en jeu
  → paramètre `process(allie, sbire)` (ajouté) pour poser `printed_health` ; (2) `effect.this` est la carte dont la SORTIE du jeu
  rend l'allié à sa forme de sbire : donner `GameRule(sbire)` pour une conversion permanente (le complot vaincu part en pile de
  victoire juste après) ; (3) les traits du sbire se posent APRÈS l'échange (`allie.traits_internal[t] = [allie]`).
- **Alliance sur un soutien** : pas de mot-clé natif hors événement ; marquer la capacité de JEU `ability.cout_en_groupe = True`
  (sk280, modèle sk189a) ; la preuve est une MUTATION : sans la ligne, le cas « coût 4 payé à deux » tombe au rouge.
- **« Skip the villain phase »** : `World.skip_villain_phases += 1` (lu par `OnGameLoop`, saute la phase ENTIÈRE, journal
  « Phase : Villain (skipped) »). `Puzzle.EndPlayerPhase()` + lecture du drapeau prouve la Réponse ; la boucle se prouve à l'autoplay.
- **Mesurer un COÛT dynamique** : `Message.WhenCalculateEffectCost(joueur, effet_de_jeu, [])` puis `.Send()` et `.cost.val`
  (`cc_cout` dans `tools/cas/campagne_cartes.py`). Jouer la carte avec une main trop courte ne prouve rien : en alter ego,
  la ressource de Peter Parker (« Scientist ») complète le paiement.
- **`Worlds.GetIconsNum(effect, ["Crisis", "Acceleration", "Amplify", "Hazard"])`** compte les ICÔNES (une carte à deux icônes
  compte deux fois) de toutes les cartes en jeu.
- **« While X is exhausted »** : `OnEvent.TemplateTrigger(Message.AfterCardExhausted | Message.AfterCardReady, lambda e, m:
  m.trigger == e.this)` en `change_on_event` de `GiveKeywordToInPlayWhenApplyThis(..., condition=lambda e: e.this.IsExhaust())` ;
  « each minion engaged with you gets -1 SCH » : même fabrique avec `scheme=-1`, `get_new_value` (1 pour les sbires engagés avec
  le propriétaire, 0 sinon) et `OnEvent.TemplateTrigger(Message.AfterMinionEngagePlayer, ...)`.
- **Le message d'engagement s'appelle `Message.AfterMinionEngagePlayer`** (`AfterPlayerEngageMinion` n'existe que comme FABRIQUE) :
  `verifier_api_cartes.py` l'a attrapé (« Message.AfterPlayerEngageMinion n'existe pas »), pas les cas.
- **`DeclareNumber` répond la PREMIÈRE valeur (0)** : `choisir_option: ["3"]` force la valeur (cas sk271).
- **Le filtre `[filtre]` du harnais est une sous-chaîne, pas une expression régulière** (`"sk2[78]"` retient 0 cas).

### 7novemdecies. Pièges payés par le pack `venus` (TMNT Heroes, 16/10/2026)

| Mécanique / outil | Montage | Piège payé |
|---|---|---|
| « You MAY remove N <compteurs> to <effet> » (retrait = coût, facultatif) | `joueur.MayChooseOneAbility(effect, ForChoiceAbility(nom, op).SetCostFunc(CostFunc.Counter("YourIdentity", N, 'compteur')))` (modèle `01165` Eviction Notice ; helper `ProposerRetraitDragage`, `venus/__init__.py`) | Le refus est une option nommée **« Cancel »**, PAS un bouton Passer : dans un cas, `choisir_option: ["Cancel"]` ; `passer_sur_option` répond « la question n'a jamais été posée ». Branche non offerte quand le stock est insuffisant. |
| « Remove X <compteurs> → ... », X choisi, zéro compris | `DeclareNumber(0, stock)` à la main, puis `Faces.RemoveCountersOn` (`tv003` Arc Nova) | `CostFunc.Counter` refuse un retrait de 0 et un minimum 1 interdit « jouer à X = 0 » ; `CostFunc.Counter(..., (1, N), ...)` + `effect.cost_func.Get(CostFunc.Counter).return_remove_counter` reste le bon modèle quand 0 n'a pas de sens (`16006`, `cn012b`). |
| Ressource à coût de COMPTEUR (`CanGenerateResources(...).SetCostFunc(Counter)`) | `conditions=[stock >= n]` sur `CanGenerateResources` (`tv011` Dragon Scale) | Sans la condition, la ressource est offerte sans compteur et le moteur annule toute la carte en cours de paiement, sans motif. `CanPlayBy` (`venus_jouable`) NE VOIT PAS le paiement : pour prouver « impayable », jouer la carte (`jouer`) et mesurer qu'elle est restée en main. |
| « discard cards from the top of your deck until you discard X » (`seek`) | `joueur.DiscardDeckUntil(effect, card_type=..., check_face_fn=...)` ; plusieurs types = `check_face_fn` (`tv012`) | Quand la carte trouvée est la dernière du deck, le moteur REMÉLANGE la défausse dans le deck vide (règle du deck épuisé) : défausse vide, trouvée rendue quand même. Prévoir une carte de fond dans le deck d'un cas, ou assumer le remélange. |
| Harnais : `Puzzle.Gain('<card_id>')` (`main` / `main_exclusive`) | — | **PREND la carte dans le deck si elle y est** : un deck rempli de `01090` perdait ses cartes dès que la main en réclamait une (« deck 5 au lieu de 6 »). Remplir le deck avec un id absent de la main (`01073`). `main_exclusive` verse aussi la main de départ dans la défausse : ne pas mesurer la défausse « exacte » avec lui, utiliser `Puzzle.EmptyHand()`. |
| Harnais : Setup de l'alter-ego qui fouille le deck | rejouer `Setup(False)` (`venus_resetup`) | Le Setup tourne à CHAQUE départ de cas : la carte qu'il met en jeu (ici `tv014`) est déjà là. Un cas qui compte ces cartes la retire (`Puzzle.Remove`) ou la compte. |
| `substituer_pack.py` | base de ports ≤ 48000 pour ~20 cartes | 60 ports par carte, plafond 49146 (« PORT TROP HAUT ») : au-delà, tous les rapports sont « illisibles ». Le filtre est `<card_id> ` AVEC l'espace : le nom des cas doit commencer par `tvNNN `. |
### 7vicies. Pièges payés par le pack `alopex` (TMNT, 16/10/2026)

- **Une Interruption forcée « when this card leaves play, set this card aside »
  doit se garder contre sa propre sortie.** `Faces.SetAside` fait QUITTER LE JEU à la
  carte et renvoie `WhenCardLeavePlay` : l'Interruption se relançait sans fin
  (`RecursionError` AVALÉE par le moteur). La carte finissait de côté, les cas « elle
  est de côté » étaient verts, mais `AfterCardLeavePlay` n'était jamais envoyé, donc
  toute Réponse « after Prey leaves play » restait muette (Kabuki, Kama). Garde :
  drapeau posé sur la carte autour de l'appel (`ta011.py`). **Symptôme au journal du
  harnais : des centaines de lignes « [carte] s'active » suivies d'un `RecursionError`.**
- « Spend up to N [mental] resources » **dans le corps** d'un effet (pas de flèche) :
  `joueur.AskSpendResourcesInternal(Cost("BBB", up_to=True), effect)` rend les
  `Resources` dépensées (`.val`) ; `Cost("B...")` accepte mental ET wild. Le pilote du
  harnais refusait toute dépense partielle (« UpTo » exigeait la couverture totale) :
  clé `payer_jusqu_a: n` ajoutée à `test_capacites.py` (additive). Il faut aussi des
  cartes à UNE icône comme carburant (Genius 01089 = 2 icônes d'un coup).
- Un **Réponse qui part AVANT les dégâts consécutifs** (ally `1*`) : une carte Cloaked
  posée par cette Réponse absorbe aussitôt le dégât consécutif de l'allié (−2) et part.
  Mesurer `degats` de l'allié (0 avec, 1 sans), pas la présence du statut.
- La **défausse du joueur n'est jamais vide** : le harnais défausse la main de départ
  (`main_exclusive`) AVANT `declencher`. Pour « aucune carte éligible » / « exactement
  celle-ci », `Puzzle.EmptyPlayerDiscardPile()` (ajoutée) puis `CreatePlayerDiscardPile`
  DANS `declencher`, pas dans `mise_en_place`.
- `CreatePlayerDeck(a, b, c)` : la DERNIÈRE carte créée est au DESSUS du deck.
- Un deck rencontre épuisé par « discard ... until » est **remélangé aussitôt** avec sa
  défausse : ne pas asserter `defausse_rencontre` après une recherche infructueuse.
- Un sbire à Garde (01101 Hydra Mercenary) rend le vilain non ciblable : choisir le
  sbire comme cible d'un événement d'attaque.
- Une attaque d'allié sur Rhino : les cartes `Puzzle.SetThreat('01097b', 8)` dépassent
  le seuil du complot et mettent fin à la partie (l'attache échoue) : rester ≤ 6.

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


### 7quaterdecies. Mesurer la BOUCLE d'une campagne (19/09/2026)

Le harnais des capacites mesure une partie. Pour mesurer ce qui se passe ENTRE
deux parties d'une campagne — le carnet ecrit a la victoire, les cases cochees
au panneau, et la mise en place du scenario suivant — il y a
`tools/test_campagnes.py`, generique, et `tools/epreuves_campagnes.py`, qui
porte la connaissance de chaque boite.

Pieges payes en l'ecrivant, tous reutilisables :

- **L'estampille du carnet sortant DOIT egaler l'id du scenario de la campagne.**
  `WriteCampaignLogAtGameOver` la derive du `set_name` de la manigance
  principale, et le panneau de recompenses (`preremplissage.ts`) ignore TOUT
  le releve du moteur si elle differe de `lireContexte().scenario`, puis retombe
  sur le carnet ANCIEN : les gains du scenario disparaissent sans un mot. `gmw`
  ecrivait `collector_1` / `collector_2` pour `infiltrate_the_museum` /
  `escape_the_museum` : les unites des scenarios 2 et 3 n'arrivaient jamais au
  Marche (signalement n°50, 04/10/2026). Quand les deux ne coincident pas, la
  boite passe `scenario_id=` au collecteur. Une epreuve
  `"carnet_attendu": {"scenario": "<id>"}` par scenario de la boite le garde.
- **Un collecteur qui plante n'ecrit RIEN, et ne le dit qu'au journal moteur.**
  `s.GetThreatInternal()` sur un complot principal (`AttributeError`, la
  methode n'existe pas : c'est la propriete `.threat`) a prive tout le
  scenario 2 de gmw de son releve, silencieusement cote joueur. Une epreuve qui
  ne lit que le carnet ENTRANT ne le voit pas : lire le sortant.
- **Le resultat de la partie n'est pas encore pose pendant `WhenGameOver`.**
  `GameOver.SetGameOver` envoie le message PUIS affecte `players_won` : un
  collecteur qui lit `world.game_over` voit toujours « perdue ». Le collecteur
  doit recevoir le MESSAGE (`collect_fn(effect, message)`).
- **La mise en place de campagne precede la pioche.** Annexe II du guide de
  reference : etape 13 la campagne, etape 14 la main de depart. Une carte
  melangee au deck par une recompense peut donc arriver en main, et une
  recompense « cherchez une carte et mettez-la en main » n'AJOUTE rien a la
  main : elle laisse en choisir une partie.
- **Une carte cherchee par `Puzzle.PutIntoPlay('id')` deux fois est la MEME
  carte.** `FindOrCreateFace` retrouve l'existante. Pour deux exemplaires :
  `Puzzle.PutIntoPlay(Puzzle.CreateCard('id'))`.
- **Un JETON n'est pas un COMPTEUR.** `PlaceTokensOn` / `GetTokens` d'un cote,
  `PlaceCountersOn` / `GetCounters` de l'autre. Chercher une menace de jeton
  dans les compteurs rend zero a tous les coups.
- **`face.victory` est un BOOLEEN** (« cette carte a-t-elle une valeur de
  victoire »), la valeur imprimee est `printed_victory`. Les additionner
  compte les cartes, pas les points.
- **Le nom d'une identite change avec sa forme.** Relever `identity.paper.name`
  a la victoire donne « Steve Rogers » si la partie finit en alter-ego, et la
  mise en place suivante commence toujours en alter-ego. On ecrit et on relit
  `identity.GetHeroFace().paper.name`.
- **`Puzzle.AdvanceMainScheme(fois)`** (ajoute ce jour) fait avancer le complot
  principal par le chemin du moteur : un pas retourne la face A sur la face B,
  le pas suivant prend l'etape suivante. Plusieurs recompenses ne dependent que
  de l'etape atteinte.
- **Un defaut dans l'epreuve elle-meme doit echouer bruyamment.** Une exception
  levee dans le verificateur, hors `try`, laissait le fils pendu sans jamais
  rapporter : l'appel est desormais garde.


### 7quindecies. Corriger a la main une donnee GENEREE (19/09/2026)

L'editeur de palettes de heros (`/palettes-heros.html`) a posé un patron
reutilisable : comment laisser corriger a la main une donnee qu'un outil
regenere.

- **Deux fichiers, jamais un.** `data/palettes-heros.json` est reecrit en
  entier par `outils/palettes-heros.py` ; les corrections vivent dans
  `data/palettes-heros-corrections.json` et se POSENT PAR-DESSUS a la lecture
  (`PalettesHeros.Toutes()`). Une correction ecrite dans le fichier genere
  serait effacee a la passe suivante.
- **Le moteur sait deja qui est l'auteur.** `_est_administrateur`
  (server_get.py) : l'orchestrateur ne renseigne `site_admin_url` que pour la
  table de l'administrateur, et le siege 0 est celui du titulaire du compte.
  Pas besoin de relier le site au plateau pour un ecran reserve.
- **Ecriture : une entite a la fois, fichier relu a chaque fois, remplacement
  atomique, puis cache vide.** Deux onglets ne peuvent alors se marcher dessus
  que sur la meme entite, et la correction arrive au plateau sans redemarrage.
- **Le deploiement doit laisser passer le fichier corrige.** `deployer.ps1`
  l'EXCLUT de l'archive de code (sinon le poste ecraserait le travail fait en
  ligne) et le RAPATRIE apres l'envoi. Le serveur est l'endroit ou l'on
  corrige, le depot celui ou l'on garde.
- **Un apercu doit montrer le VRAI rendu.** La formule du fond de plateau vit
  en TypeScript (plateau) et en JavaScript nu (page de l'assistant) : les deux
  copies sont tenues d'accord par `ui-app/src/board/halo-heros-accord.test.ts`,
  qui compare leurs sorties.

### 7sexdecies. Une page du SITE ouverte depuis le JEU (19/09/2026)

La page de table est servie depuis `pN.<domaine>`, le site depuis `<domaine>`.
Un `window.open('/signalements')` depuis le jeu tombe donc sur le MOTEUR, qui
sert une IMAGE pour tout chemin inconnu (`handle_image_request`, la route
fourre-tout) : l'onglet s'ouvre sur rien, sans la moindre erreur. C'est ce qui
rendait « Mes signalements » introuvable depuis le 16/09/2026.

Le moteur expose desormais `/get_site_url` (lecture ouverte : c'est l'adresse
d'accueil, pas l'administration), renseignee par l'orchestrateur pour TOUTES
les tables. Tout lien du jeu vers une page du site doit passer par la.

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
| Boucle des campagnes (carnet ou mise en place touchés) | `test_campagnes.py` | ~5 min |
