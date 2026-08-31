> ⚠️ **DOCUMENT HISTORIQUE, ARCHIVÉ LE 31/08/2026.** Il décrit l'époque (juillet-début août 2026)
> où la copie vivante du jeu était `~/marvel-work/fusion/marvel-lcg-src`. Ce n'est plus vrai :
> la copie vivante est `Fusion/marvel-lcg-src` dans ce dépôt (voir GUIDE-CREATION-CONTENU.md §1).
> Aucun chemin cité ici ne fait foi.

# TODO — Marvel LCG (état au 27/07/2026 nuit)

## Contexte express
- Source du jeu 100 % reconstruit (bytecode-identique, voir REPRISE.md). Ne JAMAIS toucher `~/marvel-work/boot/`.
- Jeu jouable : `cd ~/marvel-work/fusion/marvel-lcg-src && ~/marvel-work/python/bin/python3.10 launcher.py`
  (compile ~2 min, ouvre le navigateur tout seul sur http://127.0.0.1:2345).
- **Daredevil ET Echo (pack fne) ajoutés et jouables** : données `data/cards.json` section `fne` (68 cartes),
  modules `src/cards/pack/fne/` (+ `echo/`, `echo_nemesis/`), decks `deck/starter/daredevil.json` + `echo.json`.
  La galerie de héros (scene.html) est DYNAMIQUE : elle liste `deck/starter/*.json` via `/list_starter_deck` — rien à éditer.
- Après toute modif : relancer launcher.py (recrée `.game/`), re-zipper vers `Fusion/` (procédure dans REPRISE.md).
- Baseline tests : `test_cards` = **3754 ok / 0 échec** (RELEASE=1 obligatoire sinon ModuleNotFoundError editor).
  Partie test : PLAYERS: 1 pour echo, daredevil, god_of_lies, wonder_man, hercules, she_hulk_pvp ET
  vision_pvp (l'AttributeError 'identity' en introspection est un artefact du script, pas un bug).

## Méthode « ajouter un héros » (rodée avec Daredevil)
1. Données MarvelCDB : `https://marvelcdb.com/api/public/cards/<pack>.json` → générer les entrées
   `data/cards.json` (format : desc Cost/HP/ATK/THW/DEF/REC/HS/RES/Boost/StartingThreat/Class ;
   RES : physical→R, mental→B, energy→Y, wild→G ; nom unique préfixé `* ` ; étoiles = conséq.).
2. Déclarer le pack dans `data/sets_info.json` (`heroes: [...]`, `max_id`).
3. **Recalculer les checksums** des 2 JSON : sha256(json.dumps(obj sans 'checksum', default=o.__dict__,
   sort_keys=True) + ' ' + CODE_KEY) — CODE_KEY dans `src/core/utility/types.py`.
4. Modules : `src/cards/pack/<pack>/<set>/<card_id>.py` avec `GetAbilities()` (mapping :
   `cards.pack.<pack>.<CleanName(set_name)>.<card_id>` puis fallback `cards.pack.<pack>.<card_id>`).
   Modèles : Doctor Strange (deck annexe via additional_deck + BeginGameWithSetAside), tout le pack fne.
5. Deck : `deck/starter/<hero>.json` (hero/hero_deck/set_aside/obligations/nemesis_set/player_deck).
6. Images : `assets/pics/<card_id>.jpg` (jeu original + fusion + .game). Sources : marvelcdb
   `/bundles/cards/<id>.jpg`, cerebro `cerebrodatastorage.blob.core.windows.net/cerebro-cards/official/<ID>.jpg`,
   Hall of Heroes (`hallofheroeslcg.com/<pack>/`, images `mc60_card_<slug>.png`). Sinon générer des
   proxies (script PIL utilisé pour Daredevil, layout dans l'historique — refaire pareil).
7. Tests : import+GetAbilities de chaque carte dans boot_sub, `tools/test_cards.py` (0 échec),
   partie test `SceneLoader.NewScene('rhino', None, ['<hero>'], 42)` → PLAYERS: 1,
   **ET `tools/test_generate_cards.py <boot_sub> <port> <préfixes>`** : génère RÉELLEMENT chaque carte
   (CardFactory.GenerateCard) — attrape les asserts de construction que test_cards/PLAYERS:1 NE VOIENT PAS
   (ex. « 1 seule resource ability par carte » card_player.py:50, noms de compteurs du desc `Uses` devant
   être dans CardFace.COUNTER_LIST). PLAYERS: 1 ne valide PAS la génération des decks (le setup headless
   attend le client web).
   **ET `tools/test_autoplay.py <boot_sub> <port> <scenario> <hero> [max_asks]`** : BOT qui joue une
   partie complète in-process (patch DeviceManager.DoGetInput/DoWaitConnect/DoWaitSync — répond aux asks
   en cyclant les options valides, id 0 en dernier recours). Déroule setup + phases + activations vilain +
   When Revealed sur plusieurs rounds. Vérifier : 0 Traceback dans /tmp/autoplay_<sc>_<hero>.log.
   Leçons du 28/07 : GiveTo est OBLIGATOIRE sur toute Obligation (desc GiveTo "" = « au joueur qui la
   révèle », assert printed_give_to sinon) ; from_where des SetTarget = clés de selector_where.py
   ('YourHandCards', PAS 'YourHand').

## FAIT le 27/07/2026 soir : Echo (pack fne) ✅
- 31 entrées ajoutées à cards.json (60037a→60064), dont 5 `full_link` (60051→32014 Powerful Punch,
  60056→40059 Superpower Training, 60057/58/59→01088/89/90 ressources) — les full_link n'ont NI module NI image.
- Checksums cards.json + sets_info.json recalculés (formule validée par reproduction des checksums existants).
- Photographic Reflexes (60040a/b/c) : cartes elles-mêmes = `return []` ; TOUTE la mécanique est sur le héros
  60037a : YouMayPlayCardLikeInHand (events tuckés jouables si PR en main + forme héros), WhenPlayerPlayCard
  Rule (défausse auto d'un PR de la main), CanGenerateResources('GG', is_play_card) conditionné au play
  d'une carte tuckée (= réduction 2). Tuck = TuckCardUnderHere / GetPlacedCardArea (modèle 60030).
- Piège appris : suffixe `*` sur Cost dans desc = « par joueur » (FormatPlayerNumValue), PAS « +1 par allié » →
  Army of One/In Harm's Way ont Cost "1"/"3" + ability WhenCalculateEffectCost.UpdateCost(+alliés).CanWorkOnlyInHand().
- Ronin : GiveKeywordToAttached(get_new_value=…, ex_change_on_event=OnEvent.CardInPlay(Ally)) (modèle x23/43019).
- Innate Reflexes « Starting » : WhenGameBeginSetup + NoOutOfPlayLimit → carte déplacée du deck vers la main
  au setup (aucun autre précédent du mot-clé dans le jeu).
- Images : 15 réelles (12 Hall of Heroes 300×426 + mc60_card_daredevil.png = l'ALLY 60039, pas le héros ;
  60040b/c = copie du 60040a) + 12 proxies PIL (script `~/marvel-work/tools/make_echo_pics.py`).
  Déployées vers les 3 assets/pics (fusion, .game, Jeux original).
- boot_sub synchronisé : modules compilés en .pyc sourceless + data + deck (voir méthode).

### Raffinements Echo v1 → v2 — ✅ FAIT 28/07/2026 (2)
- 60052 The Best Offense : DEF remplace ATK/THW — WhenUnitUseBasicPower ForcedInterrupt sur le héros
  attaché + `message.GainValue(hero.defense - valeur_courante)`. Validé chirurgicalement : DEF 2→3,
  attaque basique 3 dégâts, thwart basique -3, retour à 2 sans la carte. NOTE : en test direct,
  PutIntoPlay n'attache PAS un upgrade — l'attache vient du PLAY normal (CanPlayThisUpgradeCard
  → selector défaut 'YourIdentity' → AttachTo2) ; en chirurgical utiliser `AttachTo2(identity, effect)`.
- 60060 : « You cannot deal damage to Kingpin » — UnitCannotTakeDamageWhile(Kingpin) + condition
  source.GetControlBy() == GetGaveToPlayer(). Validé : dégâts bloqués avec l'obligation, passent sans.
- 60039 : réduction -1 event désormais « this round » (RegisterTemp until_round_end, copie inline
  d'UpdateNextCardPlayCost qui ne supporte que Phase/Turn).
- 60043 ASL : `.AnyPlayerCanDoThis()` ajouté (ressource pour l'event de n'importe quel joueur).
- Défausse PR : choix du joueur entre exemplaires DIFFÉRENTS (a/b/c) en main via ChooseAbilities ;
  défausse auto si exemplaires identiques.
- BONUS — 2 bugs latents corrigés : 32177 Brawler comparait `message.power == 'Defense'` et 59014
  Golden Mace `== 'Attack'` alors que le moteur envoie 'DEF'/'ATK'/'THW'/'REC'/'SCH' → leurs buffs ne
  se déclenchaient JAMAIS. (Piège : toujours comparer aux codes courts.)
- Vérifier en jeu réel : tuck Watch and Learn (timing défausse post-play), jouer un event tucké via PR
  (permission + défausse + réduction 2), Innate Reflexes en main de départ, boost Master Manipulator (reveal).
- 12 proxies à remplacer quand les scans sortiront : 60038, 60042, 60044, 60045, 60047, 60052, 60054, 60060–60064
  (+ re-télécharger 60037a/b et les autres en HD quand marvelcdb/cerebro les auront).

## FAIT le 27/07/2026 nuit : 75 cartes campagne/PVP manquantes ✅
- Ajoutées aux sections mts (16), mut_gen (29), next_evol (12), aoa (2), cw (16) de cards.json,
  checksum recalculé. 4 duplicatas MG en `ability_link` (32181→32176, 32186→32177, 32191→32187, 32192→32182).
- 67 modules : campagne MTS (Norn Stones, Shawarma, Black Swan, Jormungand…), campagne MG (Metro P.D.,
  Rescue Captives, Magneto's Power…), 16 rôles MG (Brawler/Commander/Defender/Peacekeeper),
  campagne NeXt Evol (6 player side schemes + 6 environments à compteurs), Mission Team AoA,
  16 basic PVP Civil War (attaques leader vs leader via BasicAttack + GetEnemyLeader).
- Patterns clés appris : flip recto/verso = `this.card.Flip(effect)` puis `this.card.face` (nouvelle face)
  + PutIntoPlay/Reveal ; `FirstPlayerControlThis()` ; `ThisNotCountAllyLimit()` ; CanGenerateResources
  ex_operation pour les « Hero Resource : … puis effet » ; engage = Faces.MoveAllTo([minion],
  player.engaged_minions) ; défausse choisie = ForChoiceAbility.SetTarget('YourHandCards', canbe_discard=True) ;
  CardsDB importable via `from cards.database import CardsDB` (import local).
- Images : 75/75 trouvées sur marvelcdb (imagesrc) — AUCUN proxy. Déployées vers les 3 assets/pics.
- Tests : 3585 ok / 0 échec, PLAYERS: 1, serveur relancé, re-zippé (5266 fichiers) vers Fusion/.
- ~~Limites v1 : l'enchaînement de campagne n'est pas câblé~~ → **✅ FAIT 28/07/2026, voir la section
  « hooks de campagne » ci-dessous.**
  Détails omis : deck Future Past (MG, pas de support moteur), « mission attempt » AoA (45171a option B),
  overkill Coup de Grâce, prevent exact Brazen Defense (approx -3 dégâts), redirections leader 56133/56207
  (texte seul), effets post-spend des 4 ressources PVP CW (texte seul, icônes GG fonctionnelles),
  « does not count against side scheme limit » des player side schemes NeXt.

## FAIT le 27/07/2026 nuit (2) : scénario God of Lies (Trickster Takeover) jouable ✅
- Constat : le jeu original ne livrait la boîte 55 qu'avec Enchantress ; le set God of Lies n'avait que
  7 cartes (55037-42, 55047), un stub `PlaceShatterCountersOnTheAvatarOfLokivillain` VIDE (pass), ni
  fichier `data/scenarios/god_of_lies.json` ni vilains/schemes. Raison : c'est le scénario ÉPIQUE
  multi-tables (pods/groups) non supporté par le moteur.
- **Adaptation 1 groupe/1 table** (choix maison documentés ici) : 30 entrées ajoutées (55027a/b Loki GoL,
  55028a/b Worlds Collide, 55029-32a/b les 4 Avatars↔Fading Figment, 55033a/b Mischief and Mayhem,
  55034a/b Intense/Total Focus, 55035-36, 55043-46, 55048-55). Sources données : marvelcdb
  **`api/public/cards/tt.json?encounter=1`** (le paramètre encounter=1 expose les cartes rencontre !)
  + lecture des scans cerebro. `data/scenarios/god_of_lies.json` (villain: [] + set_aside, modèle mts/loki)
  + `data/encounter_sets/god_of_lies.json`.
- Mécanique : M&M 1A setup (WhenCardSetupBeforePutSetupCards → avatar aléatoire Reveal + GoL en jeu +
  4 environments Synergy + reveal du 2e main scheme Worlds Collide via MainSchemesDeck, modèle 21098a).
  Avatar vaincu → SetBeInstead + 5*/joueur shatter + Flip + ShatterTheIllusion (dégâts à GoL = compteurs,
  synergy sur l'env lié, rotation vers un avatar aléatoire via SwapCard). GoL : WhenEnemyWouldActivate
  SetBeInstead (n'active jamais), dégâts bloqués sauf source 'Fading Figment', flip à ≤10*/joueur HP
  (+ attache Intense Focus + discards), mort → Worlds.SetGameOver(True). M&M complété → menace retirée
  + 1 threat sur Worlds Collide (WhenMainSchemeWouldAdvance SetBeInstead) ; héros vaincu → alter-ego +
  SetHealth(1) + 1 threat WC. WC : menace non retirable, complété (2*/joueur) = défaite.
- Fichiers refidélisés modifiés VOLONTAIREMENT (à marquer si audit bytecode) : tt/god_of_lies/__init__.py
  (stub rempli + helpers, signature +effect), 55047.py (appel patché).
- Simplifications v1 : boost-response du Rascal texte seul ; « after you resolve a treachery » ≈ WhenRevealed ;
  « 2 resources of the same type » ≈ Cost('2') ; Feigned Retreat ne couvre que les attaques ; expert non fait
  (god_of_lies_expert.json absent) ; « Shatter the Illusion » (carte d'aide non numérotée) intégrée en dur.
- Images : 37 scans cerebro (55027a→55055) déployés vers les 3 assets/pics.
- Tests : 3615 ok / 0 échec, partie god_of_lies PLAYERS: 1 sans exception, serveur relancé
  (god_of_lies listé), re-zippé (5336 fichiers) vers Fusion/.
- ✅ VALIDÉ PAR TEST CHIRURGICAL 28/07 (dégâts létaux in-process sur l'avatar, 4 bris enchaînés) :
  cycle shatter complet (5 shatter → dégâts à GoL → synergy sur le bon env → rotation d'avatar via
  SwapCard), flip de GoL à ≤10 PV/joueur + Intense Focus attaché (+2 PV, suit les rotations),
  VICTOIRE à 0 PV (GameLoop se termine proprement). Correctifs apportés pendant la validation :
  interrupt avatar réécrit sans passage par la face Figment (le flip pendant la fenêtre de défaite
  déclenchait l'« advance » de stage) ; dégâts du bris en TakeDamageNoDeath + SetGameOver(True)
  explicite (la défaite « naturelle » du vilain final bloquait le moteur) ; protection de GoL élargie
  aux sources à trait AVATAR OF LOKI ; 55032a Wretch : buff via RegisterTemp until_turn_end
  (GainForThisActive incompatible avec WhenEnemyWouldActivate) ; 55055 Unified Front : ajout du
  DoGenerateResources explicite (les Environment ne sont pas des ClassCard → pas d'auto-ajout,
  IndexError sinon — piège pour TOUT CanGenerateResources sur carte non-joueur).

## FAIT le 28/07/2026 : campagne d'autoplay (tests en jeu automatisés) ✅
- Nouveau `tools/test_autoplay.py` : bot in-process qui répond aux questions du jeu → parties entières.
  **v2 : le bot PAIE les cartes** (resources = pay-effect ids depuis target_payment, surenchère par retry)
  → il joue réellement 10-45 cartes par partie.
- 7 combos testés + contrôle spider_man : **0 traceback partout**, 2-12 rounds, fins de partie propres.
- Mécaniques signature OBSERVÉES dans les logs : Ionic Physiology setup+equip et Ionic Blast payé (WM),
  decks Labor/Gift construits + Protect Humanity révélée/en jeu (Hercules), avatar aléatoire révélé par
  M&M (GoL), Dense attaché puis FLIPPÉ après phase vilain (Vision), Superhuman Strength attaché (She-Hulk).
- **Bot v3 « stratège »** : score les options (Play > Attack > Defense…), lit sa MAIN et le monde
  in-process (résolution des object_ids en cartes → cible le Villain/Leader à l'attaque), suit sa forme
  (le jeu DÉMARRE EN HÉROS), accepte les réponses optionnelles, surpaie les events overpay de WM.
- ✅ OBSERVÉS avec le bot v3 : **tuck Watch and Learn d'Echo** (In Harm's Way joué en héros → tucké sous
  Echo → récupéré en main par Muscle Memory !), **tuck Ionic Physiology de WM** (3 events energy tuckés,
  dont un event Justice via le deck-building d'Ionic Energy Being), shatter counters par When Defeated
  (Fenris Wolf), Stories and Lies (swap d'avatar + attaque du Rascal), Intense Focus qui suit les swaps.
- Restent à voir en vraie partie (mineur) : Photographic Reflexes de bout en bout (jouer un event
  DEPUIS le tuck), Atonement complet (labor au victory display), paliers Son of Zeus multi-gifts.
- 4 bugs réels trouvés et corrigés : 60030 Contingency Planning (from_where 'YourHand' invalide →
  'YourHandCards') ; obligations sans GiveTo (21185, 32174b, 57063, 57072 → GiveTo "" ; 59004 → "Hercules").
- boot_sub ASSAINI : recompilation INTÉGRALE des 4633 .py de fusion/src vers boot_sub (des vieux pyc de la
  récupération ChatGPT traînaient encore : achievement.py NameError, event/manager.py UnboundLocalError —
  jamais exercés avant car l'initialisation headless s'arrêtait à l'attente client).

## FAIT le 28/07/2026 (2) : 4 passifs Daredevil v2 ✅
- **60007 Elektra** : Forced Interrupt (Hero) — Ability BRUTE (pas de factory, précédent 53038) sur
  `Message.WhenAllyWouldTakeConsequentialDamage` : `SetBeInstead(effect)` + `TakeDamage` sur l'identité
  du contrôleur (condition `player.IsInHeroForm()`).
- **60021 Dagger** : `GiveKeywordToInPlayWhenApplyThis(CardFinder(name='Cloak', card_type=Ally),
  acceleration_icon=-1)` + `WhenAllyWouldTakeConsequentialDamage('This', update_damage=callable)` (-1 si
  Cloak en jeu, modèle angel 42020). **DONNÉE corrigée** : l'ally Cloak 60020 avait PERDU son icône
  accélération (MarvelCDB `scheme_acceleration: 1`, champ non repris à la génération) → desc
  `"Acceleration": "1"` ajouté + checksum cards.json recalculé.
- **60029 Stick** : 2 abilities Interrupt `WhenUnitUseBasicPower` sur `CardFinder2('MARTIAL ARTIST', Friend)`,
  opération `message.GainValue(±1, effect)` (couvre ATK/THW/DEF/REC/SCH), +1 avec
  `SetCostFunc(CostFunc.Exhaust('This'))`, -1 avec `Faces.ReadyAll`. **PIÈGE** : `.SetTarget('Trigger')`
  OBLIGATOIRE sur un interrupt visant l'unité du message (sans lui, target_range=(1,1) et le contrôleur
  rejette la réponse — AssertionError controller.py:179 ; pattern 52013 Scarlet Spider). Simplification :
  le « choose one » n'est pas exclusif (les 2 interrupts peuvent être pris sur le même usage, net 0, sans exploit).
- **60034 Deadliest Man Alive** : `WhenUnitWouldAttack(ForcedInterrupt, CardFinder(name='Bullseye'))` +
  `message.GiveAdditionalBoostCardForThisActivation(1, effect)` (modèle Hysteria 02020 / Klaw 01113).
- Tests : chirurgical in-process (~/.claude/jobs .../test_dd_v2_surgical.py, port rotatif) — 6 checks OK :
  icône Cloak 1→0→1 (pose/défausse de Dagger), Dagger 1 seul dégât conséquent, Elektra hp intact +
  Daredevil -1, Stick +1 (vilain -3, exhaust) et -1 (vilain -1, ready), Bullseye « gains … as boost card
  ([Deadliest Man Alive]) ». Puis test_cards **3754 ok / 0 échec**, GEN 68/68 (préfixe 600),
  autoplay rhino/daredevil 0 traceback. Re-zip (5674 fichiers) copié dans Fusion/, serveur relancé.

## FAIT le 28/07/2026 (5) : hooks de campagne MTS / MG / NeXt / AoA ✅
Modèle trors/sm : `cards/pack/<pack>/campaign.py` (aoa : `campaign_setup.py`, le set « Campaign » de la
boîte occupait déjà `cards/pack/aoa/campaign/`) avec `CampaignSetup(level)` étalé dans le main scheme 1a
de chaque scénario. Le moteur LIT le campaign log (saisi côté client, `mode_campaign` coché) via
`CampaignLog.GetStrInternal` ; le bookkeeping de victoire reste MANUEL (comme trors/sm). Règles extraites
des livrets officiels (PDF Hall of Heroes rendus en PNG via PyMuPDF — installé dans ~/marvel-work/python).
- **Baseline test_cards : 3756 ok / 0 échec** (+2 modules créés : 21074a, 21114a).
- **MTS** (21074a/21098a/21114a/21138a/21165a, niveaux 1-5) : side scheme campagne du scénario +
  Security Breach/Summoned Back au deck rencontre + clés `Campaign Pool: Cosmo|Security Breach|Shawarma|
  Black Swan|System Shock|Norn Stone|Odin`, `Avengers Tower Damaged` (3 dégâts chacun),
  `The Infinity Stones 1B completed` (défausse moitié du deck). Norn Stone attachée au héros (21187a),
  Odin face King (21139b). Validé chirurgicalement (ebony_maw, hela, loki).
- **MG** (32063a/32087a/32112a/32125a/32141a) : rôles (`Player N Role` = Brawler/Commander/Defender/
  Peacekeeper, demandé au setup S1 si absent, upgrade ALÉATOIRE du set de rôle attaché au héros),
  récompenses conditionnées par `Frightened Police|Enemy of My Enemy|Find the Prisoners|Surprise Attack
  Defeated`, `Campaign Pool: Jubilee` (32088b), `Captive Allies` (liste d'ids `;`) mélangés au deck du
  1er joueur, side scheme campagne révélé (32171a→32175a). **Deck Future Past NON supporté** (documenté).
- **NeXt** (40077a/40103a/40121a/40139a/40166a) : choix d'un player side scheme campagne par scénario
  (exclut `Chose: <nom>` et `Removed: <nom>`) + sa carte rencontre liée (mapping du campaign log :
  Assemble→Malice, Safehouse→Vanisher, Gear Up→Overburdened, Mission Prep→Scrambler,
  Practice→Lady Mastermind, Defenses→Under Pressure) ; environnements gagnés (`Campaign Pool: <env>`)
  remis en jeu ; cartes rencontre des schemes déjà choisis re-mélangées. Marauders/Morlocks/Hope
  Summers : bookkeeping manuel non câblé.
- **AoA** (45062a/45085a/45121a/45103a/45147a ; ordre corrigé : Apocalypse=3, Dark Beast=4) :
  modular AoA mélangé, Mission Team 45171a au 1er joueur, recherche d'allié → main,
  `Player N Campaign Ally`, `Campaign Pool: Desperate Measures|Panicked Refugees|North American Sea Wall`.
  **✅ MISSIONS IMPLÉMENTÉES 28/07/2026 (v2)** — voir section suivante.

## FAIT le 28/07/2026 (6) : sous-système missions AoA ✅
**Nouvelle baseline test_cards : 3766 ok / 0 échec** (+10 entrées : missions 45166a-45170a StartingThreat
5*, trait MISSION, set Campaign ; overseers 45179a-45183a HP 5*, Victory 5, ELITE/OVERSEER, set Prelates ;
checksum recalculé ; 10 proxies PIL déployés vers les 3 assets/pics).
- **Découverte** : le moteur original avait STUBBÉ la mission area (`Worlds.ScenarioArea` →
  `raise NotImplemented`) — le choix « Add to the mission area » du 45164 original CRASHAIT.
  CORRECTIF dans 45164 (choix proposé seulement si mission en jeu, via MinionToMission).
- **Design (adaptation sans nouvelle aire moteur)** : « à la mission » = compteur `mission` sur la carte
  (le nom était déjà dans COUNTER_LIST !). Alliés à la mission : treat_as_blank + hors limite d'alliés
  (Message.CheckIfAllyCountLimit + SetNotCountAlly, NoOutOfPlayLimit, until_this_leave_play).
  Minions/overseers à la mission : engagés 1er joueur mais INERTES (WhenEnemyWouldActivate SetBeInstead)
  et INTOUCHABLES sauf par la tentative (UnitCannotTakeDamageWhile ; source = Mission Team autorisée
  seulement si aucun AUTRE minion à la mission — règle Overseer). ATTENTION : poser le compteur APRÈS
  PutIntoPlay (le reset d'entrée en jeu purge les compteurs).
- **cards/pack/aoa/missions.py** : GetMissionScheme/Team/Allies/Minions, AllyToMission, MinionToMission,
  DoMissionAttempt (défausse X du deck, matching icônes avec wild des deux côtés + contrainte Mister
  Sinister « même icône max 1 allié », pool de dégâts = ATK des participants → minions non-OVERSEER
  d'abord, retrait de menace = THW plafonné à menace-1 tant qu'un minion est à la mission, Forced
  Response : +1 compteur `mission` sur le scheme + 1 dégât par allié, échec à 4 compteurs), Mission
  Responses des overseers (Shadow King +2 menace/[B], Abyss confisque les [G] défaussées, Sugar Man
  heal 3/[R], Mikhail 1 dégât/[Y]), EndMission (succès : cartes joueur remélangées + FLIP de Mission
  Team vers 45171b + scheme retiré ; échec : Mission Team retirée du jeu). Bookkeeping campagne manuel
  (`Mission Done: <nom>`, `Overseer Defeated: <nom>` excluent des tirages suivants).
- **45171a Mission Team** : les 2 options du texte (réduction -2 prochain allié / Make a mission attempt,
  exhaust) + réponse « Send this ally to the mission » après chaque allié joué (si mission en jeu).
- **45166a-45170a** : menace non retirable sauf par la tentative (WhenSchemeWouldRemoveThreat SetBeInstead
  sauf by_effect.this = Mission Team). Setup auto à la sélection : Evacuate Survivors → Panicked Refugees
  chacun ; Sabotage the Sea Wall → Sea Wall au deck rencontre. Protect the Professor réservé au scénario 5.
- **Piège numpy** : `Random.RandomChoice` = numpy.random.choice → REFUSE les listes de tuples (« a must
  be 1-dimensional ») ; tirer un index.
- Tests : chirurgical complet (setup campagne → mission+overseer posés/marqués/inertes, Panicked Refugees
  au deck, allié envoyé, 3 tentatives : pool/menace/compteurs/dégâts exacts, overseer intouchable hors
  mission puis victory display, chemin SUCCÈS avec flip 45171b ET chemin ÉCHEC 4 compteurs), test_cards
  3766/0, GEN 107/107 (préfixe 451), autoplay four_horsemen hors campagne 0 traceback.
- Simplifications documentées : l'assignation des cartes défaussées est AUTOMATIQUE (matching glouton,
  pas de choix joueur) ; l'allié rejoint la mission APRÈS résolution de son entrée en jeu ; les faces b
  des missions (états accompli/échoué) non intégrées (retrait du jeu à la place).
- Expert campagne : reprise des PV (`ExpertCampaignSetPlayersHPToTheirRemainingHP`, clés
  `Player N Remaining hit points`) + heal complet contre 1 token accélération (MTS/MG/NeXt) ou
  3 menaces (AoA) sur le main scheme.
- Test : `tmp/test_campaign_surgical.py` (NewFromJson + rules=['mode_campaign'] + campaign_log dict).
  Contre-épreuve : sabretooth HORS campagne = zéro injection, autoplay 0 traceback.
- **✅ V2 ÉCRITURE DU LOG (28/07/2026, 9)** : en fin de partie campagne, une ability
  `WriteCampaignLogAtGameOver` (Message.WhenGameOver, gardée IsCampaign, wired dans chaque
  CampaignSetup) écrit `campaign_log_last.json` dans le dossier du jeu = log courant repris +
  suggestions calculées (PV restants par joueur, et par boîte : MTS Cosmo/Shawarma/Black Swan/System
  Shock/Norn Stone/Odin/tour endommagée/1B complété via faces flip, victory display et main scheme
  actif ; MG side schemes vaincus via face b en jeu + Jubilee ; NeXt Chose:/Removed:/environnements
  gagnés — le choix du scénario est tracé au setup via SetStr ; AoA Mission Done/résultat
  (EndMission trace accomplished/failed)/récompenses-pénalités par mission/Overseers au victory
  display). Les clés temporaires (Current Mission/Overseer, Mission Result) sont purgées. Suggestions
  aussi affichées dans le log de jeu (« --- Campaign Log (suggestions) --- »). Côté client
  (public/scene.html) : formulaires de campaign log AJOUTÉS pour les 4 boîtes (le mode campagne
  n'était même pas cochable sans formulaire !), nouveau type `flag` (case unique → '1'),
  lecture des flags dans read_campaign_log, et PRÉREMPLISSAGE auto du formulaire depuis
  `/read_file?campaign_log_last.json` (fetch no-store) — le joueur vérifie/ajuste puis lance.
  Ce qui reste manuel : rôles MG au choix initial (préremplis ensuite), Captive Allies MG,
  choix d'ally « Find Lost Mutants » AoA, et toute correction du joueur.
  Testé : partie campagne Ebony Maw jouée jusqu'au game over → fichier écrit avec reprise du log
  (Shawarma conservée), PV, et « Security Breach » détectée via l'avancement du main scheme.
- **✅ VRAIS CAMPAIGN LOGS (28/07/2026, 10)** : formulaires client alignés sur les fiches OFFICIELLES
  (PDF Hall of Heroes : mts-campaign-log, mutant-genesis-campaign-log, next/aoa déjà extraits) —
  identités par joueur partout (auto-remplies par le writer), et NOUVELLES mécaniques câblées d'après
  les livrets :
  - **MG** : `Player N Role Upgrades Removed` (les upgrades de rôle EN JEU en fin de scénario sont
    retirées de la campagne : exclues du tirage aléatoire suivant, liste écrite automatiquement) ;
    `Jubilee removed` (case du log S3/S4 — bloque sa mise en jeu même si pool ; écrite auto si Jubilee
    absente en fin de partie alors qu'elle était au pool) ; champs informatifs Future Past (non simulés).
  - **NeXt** (spécificités réelles par scénario, livret p11/14/16/18) : S2 On the Run —
    `Marauders Defeated` (titres) RETIRÉS du deck vilains AVANT le setup (les minions homonymes
    restent : vérifié, Arclight minion présent + tough), `Morlocks Saved` = N recherches → main,
    env gagné → tough sur chaque ennemi ; S3 Juggernaut — 1 momentum counter/env + distribution
    facedown Black Tom Cassidy/Creeping Willow (1 par joueur, reste au deck) ; S4 Mister Sinister —
    +1[par joueur] menace/env sur Teleported Away + CHOIX `Hope Summers's Damage Scenario 3` (dégâts
    sur Hope OU menace sur Teleported Away) ; S5 Stryfe — menace/env sur Stryfe's Grasp + choix
    Hope S4 + défausse du deck rencontre jusqu'à minion/attachment PSIONIC révélé par joueur +
    re-mélange ; expert S3/S5 : heal = se distribuer 1 carte rencontre facedown (factory existante).
    Le writer enregistre `Hope Summers's Damage Scenario 3|4` (3 - PV restants de l'alliée 40130).
  Vérifié chirurgicalement : MG (tirage restreint à War Cry seule candidate, Jubilee removed) ;
  NeXt S2 (Arclight/Blockbuster vilains absents, 2 recherches, tough) ; S4 (menace env + 2 dégâts
  sur Hope via le choix + Overburdened re-mélangée). Baseline 3766/0.

## FAIT le 28/07/2026 (11) : étapes 4/1/3/6 (raffinements, recheck FNE, expert GoL, campagnes) ✅
- **Étape 4 — raffinements texte seul** : Coup de Grâce 32176 gagne l'overkill ; les 4 ressources
  post-spend Civil War câblées (56132 tough Iron Man, 56136 +2 energy sur Energy Channel, 56210 boost
  facedown Captain America, 56214 +2 skill sur Finesse — AfterYouSpendThisCard) ; les 2 redirections
  leader câblées (56133 Provoked Response → attaque le leader Captain Marvel, cap 3 dégâts via
  SetCannotTakeMoreThanDamage ; 56207 No, You Move! → attache Cap's Shield + résout sur le leader CA ;
  garde défenseur comme 59004) ; **11 boosts étoilés Synthezoid** câblés (57010/14/17/18/19/25/29/30/
  38/62/67 — exhaust/tough/stun/confuse/dégâts leader/boost additionnel/attache/défausse/GainBoostIcon/
  défausse main/exhaust identité) ; **Atonement limité à 1×/phase** (flag store + RunAt.TheEndOfThePhase).
  Constats : Ares 59036 et Olympic Feud 59038 étaient DÉJÀ câblés ; Brazen Defense 32178 était fidèle.
  ~~Non fait : limite player side scheme NeXt, mode compétitif PVP 2 équipes~~ → **✅ les deux corrigés
  le 28/07/2026, voir la section FAIT (13)**.
- **✅ Jet Belt 58008 (28/07/2026, 12)** : les 2 modes FUSIONNÉS en une seule resource ability (l'assert
  card_player.py:50 interdit 2 CanGenerateResources par carte) — condition : event → mode 1 simple ;
  sinon exiger une carte tuckée ; coût : Exhaust + CostFunc.Custom qui défausse une tuckée au choix
  (pattern closure-state d'Energy Siphon). GEN 123/123, autoplay 0 traceback (mode 2 à observer en
  partie humaine).
- **✅ Choosing Sides 57039a (28/07/2026, 12)** : la Forced Response manquante câblée (dernière menace
  retirée → 1 carte rencontre face cachée distribuée à chaque joueur, adaptation coop du « enemy team
  searches ») ; le cap « 2 dégâts max par attaque sur l'enemy leader » était déjà en place.
  57039b Now It's Personal : implémenté le 28/07/2026 avec la variante compétitive (section FAIT (13)).
- **Étape 1 — recheck Fear No Evil** : toujours 66 cartes sur marvelcdb (?encounter=1), AUCUN vilain —
  scénarios Kingpin/Electro/Mysterio non publiés au 28/07/2026. Recheck ultérieur.
- **Étape 3 — mode expert God of Lies** : `data/scenarios/god_of_lies_expert.json` créé (expert:true +
  set 'expert') ; Dirty Trick 55050 inflige 3 en expert (Worlds.IsExpert) + son boost étoilé câblé
  (1 dégât indirect par personnage) ; boost-response du Rascal 55029a câblé (treachery boost → deal
  facedown ou dépenser 1 ressource, WhenCardBecomeBoost activating_enemy='This') ; en expert le flip de
  GoL attache TOTAL Focus (55034b, +3 PV) et révèle Dark Scepter. Partie bot expert : 0 traceback.
- **Étape 6 — campagnes** : **deck Future Past MG câblé pour de vrai** (les 5 cartes 32166-32170
  existaient dans le jeu !) : setup selon le log (`Future Past in Encounter Deck` → mélangées ;
  `in Victory Display` → retirées ; reste = deck FP en aside), tirage aléatoire d'une carte FP au
  When Defeated des 5 side schemes campagne (32171a-32175a, no-op hors campagne), écriture auto des
  deux listes en fin de partie ; **Captive Allies auto-écrits** (alliés trait CAPTIVE en jeu fin de S2) ;
  **choix d'allié campagne « Find Lost Mutants »** (à l'accomplissement de la mission, chaque joueur
  choisit Destiny/Blink/Morph/X-Man → `Player N Campaign Ally` écrit). Vérifié chirurgicalement
  (FP setup 3 états, choix d'allié en fin de mission). Baseline 3766/0, autoplay témoin 0 traceback.

## FAIT le 28/07/2026 (13) : les 2 limites moteur corrigées ✅
- **Limite player side scheme NeXt** : `game/world/limit_monitor/player_side_scheme_limit.py` patché
  (divergence volontaire commentée CORRECTIF) — les faces marquées `not_count_player_side_scheme_limit`
  sont exclues du décompte ; `next_evol/campaign.py` pose le flag sur les player side schemes de
  campagne avant PutIntoPlay. Validé chirurgicalement (morlock_siege : Assemble the Team + Focus the
  Senses coexistent en solo, la limite 1 reste active pour les schemes normaux).
- **Mode compétitif Synthezoid (variante « table compétitive »)** : le livret mc57 (p4) officialise notre
  adaptation coop ; chaque table du compétitif = exactement nos scénarios pvp. Implémenté :
  - 2 scénarios `she_hulk_pvp_competitive.json` / `vision_pvp_competitive.json` (copies + les 4 cartes
    basiques du leader de l'ÉQUIPE en set_aside : Vision 57074-57077 contre She-Hulk, She-Hulk
    57032-57035 contre Vision) ; ajoutés aux scenarios du set 57 dans sets_info.json (checksum recalculé).
  - Détection compétitive = `GetSetAsideLeaderBasics` (helper dans `synthezoid/__init__.py`, avec
    `EarnLeaderBasicCards` : choix ciblé + SetOwner + AddToHand) — AUCUN changement moteur, les
    scénarios coop sont inchangés (vérifié : 0 mention de Choosing Sides en autoplay coop).
  - Setup : les main schemes stage 1 (57005a Registration, 57044a Resistance) génèrent et révèlent
    Choosing Sides `57039a,57039b` (2 faces) si des basiques de leader sont en set-aside.
  - 57039a RÉÉCRIT sur `AfterSchemeRemoveThreat(..., last_threat=True)` (modèle Spiral 39016 — l'ancien
    combo WhenSchemeWouldRemoveThreat + RunAt.AfterEventEnd crashait assert run_at.py:68 sur les retraits
    hors thwart) : à la défaite → 1 carte rencontre face cachée par joueur + si compétitif : chaque
    joueur choisit 2 basiques du leader → main (p15 du livret), puis flip vers 57039b (la carte part
    ensuite en RemovedArea, l'exception same-set de HasPermanent autorise le leave play).
  - 57039b Now It's Personal implémenté (Action : retirer du jeu → chaque joueur prend 2 basiques
    set-aside en main) — filet si l'obligation entre en jeu par un autre flux, no-op en coop.
  - Validé : test chirurgical sur les 2 tables (setup + défaite + 2 cartes en main), test_cards 3766/0,
    GEN synthezoid 88/0, autoplay complet 0 traceback sur les 2 compétitifs + coop témoin.
  - Limite restante (assumée) : le cross-table réel (2 tables threadées, leader vs leader) reste hors
    moteur — la variante ne simule qu'une table, ce que le livret p4 permet.

## FAIT le 28/07/2026 (14) : micro-restes « texte seul » soldés ✅
- **Teenage Superheroes 57058** : fidélité complète — copie exacte de Mighty Avengers 56076 (texte
  IDENTIQUE dans le jeu original) : `Faces.ResolveAbility(minions, player, AbilityType.WhenRevealed,
  effect)`, surge seulement si aucun When Revealed résolu. Validé chirurgicalement (sans minion →
  surge ; avec Patriot en jeu → son WR résolu : tough sur Vision, pas de surge).
- **Spellcasting 57063** : l'annulation manquante câblée — modèle Counterspell 09030 :
  `WhenPlayerWouldPlayCard` (ForcedInterrupt) + `message.CancelEffects(effect, discard_it=True)` +
  condition `not message.be_cancel`. Validé chirurgicalement en partie bot : Backflip annulé
  (le joueur a bien pris les dégâts ensuite), les deux cartes défaussées.
- **Boosts étoilés du set némésis Hercules** : note PÉRIMÉE — tout était DÉJÀ câblé (59036 scheme-star
  AfterUnitSchemeEnd, 59039 attack-star auto-défausse, 59042/43/44 All Versus All aussi). Vérifié
  contre les champs `*_star` MarvelCDB. Rien à faire.
- **Mr. Hollywood 58009 — limite « once per card » VÉRIFIÉE empiriquement (28/07/2026)** : test
  chirurgical (wonder_man, 58009 attaché, UpdatePayResources sur le play de Surveillance Team coût 2) →
  Mr. Hollywood apparaît EXACTEMENT 1 fois dans les effets payables d'un même paiement
  (add_to_pay_list ne propose chaque pay-effect qu'une fois, available_times_fn=None) ; pas de
  CostFunc.Exhaust → réutilisable pour la carte suivante, conforme au texte. Rien à implémenter.
  Lenience restante (mineure, en faveur du joueur) : la ressource peut payer le coût de base et pas
  seulement l'overpay.
- **Coordinated Effort 58032 ✅ FAIT (28/07/2026, après coup)** : le paiement partagé EXISTE dans le
  moteur — c'est la voie du mot-clé **Alliance** (events Civil War) dans les deux `check_can_pay` de
  `game/ability/factory/resources.py` (CheckThisCanDropPay pour les cartes en main, CanGenerateResources
  pour les générateurs en jeu). CORRECTIF (divergence volontaire commentée) : helper
  `CheckAnyPlayerMayHelpPay(paying_for_face)` = un « Coordinated Effort » dans
  `GetAttachedUpgrades()` de la carte payée → `return True` aux 2 sites, juste après le check
  alliance. Aucun état à gérer (check par nom, vivant : détaché = fini). Validé chirurgicalement à
  2 joueurs (Experimental Weapons 04075, coût YBR : AVANT = 6 cartes payables de Spider-Man seul ;
  APRÈS attache = + les 6 cartes de la main de Captain Marvel). Non-régression : test_cards 3766/0,
  **GEN COMPLET 4331/0**, autoplay rhino 0 traceback. Piège de test : ne PAS envoyer un
  CheckPlayerCanPayCost synthétique (KeyError GetCost(None)) — passer par
  `effect.checker.UpdatePayResources(player)` puis lire `cost_for_different_target.GetPayment(None)`.
- Tests : test_cards 3766/0, GEN synthezoid 88/0, autoplay vision_pvp 0 traceback, livré (zip Fusion/).

## À FAIRE

### 1. RANGEMENT DU DOSSIER PROJET (état des lieux du 7/8/2026)

Constat demandé par l'utilisateur ce jour-là. **Rien n'a été modifié**, c'est un
relevé. Chemin concerné :
`C:\Users\arnau\Desktop\Marvel LCG last try\Jeu Marvel Champions\`

**Poids total : ~2,1 Go**, dont 1,5 Go de scans (`assets/`, légitime) et
**~650 Mo d'archives et de sauvegardes devenues inutiles**.

#### 1.a — La CAUSE, à traiter en premier : git est inexploitable

`git status` rend **971 fichiers non suivis**, parce que le `.gitignore` ne
couvre que `node_modules/`, `ui-check/` et le mode serveur. Ni `assets/`
(1,5 Go), ni les `.zip`, ni `.game/` (19 Mo de bytecode) n'y figurent.
Conséquence : on ne peut pas lire ce qu'on a changé, donc **on ne s'appuie pas
sur git — et on sauvegarde à la main**. Tout le désordre ci-dessous en découle.

**Correctif proposé** — étendre `.gitignore` :
```
assets/
*.zip
*.apk
*.mp3
Fusion/marvel-lcg-src/.game/
Fusion/marvel-lcg-src/data/*.bak-*
```
⚠ Vérifier d'abord qu'aucun de ces chemins n'est DÉJÀ suivi par git (sinon
`git rm --cached` est nécessaire, l'ignore seul ne suffit pas).

#### 1.b — Symptômes : le versionnage manuel

- **11 sauvegardes à la main** dans `Fusion/marvel-lcg-src/data/` :
  `cards.json.bak-campagne`, `.bak-cloakdagger`, `.bak-daredevil`, `.bak-echo`,
  `.bak-godoflies`, `.bak-herc`, `.bak-madameweb`, `.bak-syn`, `.bak-wm`, plus
  `sets_info.json.bak-daredevil`, `.bak-echo`, `.bak-madameweb`.
  Une par pack livré. ~2,2 Mo pièce.
- **2 backups de zip** dans `Fusion/` : `marvel-lcg-src-fusion.zip.bak-avant-phase1`
  (88 Mo) et `.bak-avant-ui` (53 Mo) — chantiers terminés depuis longtemps.
- `Fusion/marvel-lcg-src/public/js/prepare/launcher.js.bak`
- `sauvegarde-packs-supprimes-2026-08-05.tar.gz` à la racine.

À supprimer **seulement après 1.a**, une fois que git joue son rôle.

#### 1.c — ~420 Mo posés à la racine, sans rapport avec le code

| Fichier | Poids | Nature |
|---|---|---|
| `MarvelChampions.apk` | 175 Mo | appli Android |
| `Avengers Campus Ambiance ....mp3` | 83 Mo | musique d'ambiance |
| `PURPLE MAN (3.0)-20260807T081239Z-1-001.zip` | 63 Mo | pack Drive brut |
| `Brawn-20260807T065409Z-1-001.zip` | 57 Mo | pack Drive brut (livré le 7/8) |
| `Agent 13-20260807T065416Z-1-001.zip` | 41 Mo | pack Drive brut |
| `marvel_champions_stat_badges.zip` | ~1 Mo | ressources graphiques |
| `squirrel_girl_complete_custom_hero_pack_....md` | ~1 Mo | brief d'un pack, seul de son espèce |

**Proposition** : un dossier `sources-drive/` pour les zips de packs (ils servent
de référence quand on doit relire une carte), et sortir l'APK et le MP3 du
projet.

⚠ Les zips PURPLE MAN et Agent 13 sont des packs **non encore intégrés** :
ne pas les jeter, ce sont les sources de deux héros à faire.

#### 1.d — Dispersion, moins grave mais gênante

- **8 fichiers `.md` à la racine** (`GUIDE-CREATION-CONTENU.md`,
  `GUIDE-STRATEGIE-JEU.md`, `MULTIJOUEUR.md`, `CAMPAGNES.md`,
  `RAPPORT-AUDIT-CARTES.md`, `RAPPORT-SCANS-FR.md`, `BRIEF-REFONTE-PLATEAU.md`,
  le brief squirrel_girl) alors que `docs/` existe mais ne contient que
  `superpowers/`. Garder les deux GUIDES à la racine si on les ouvre souvent,
  déplacer le reste.
- **Trois dossiers d'outils** : `outils/` (racine, 5 scripts de vérification),
  `ui-app/outils/` (4 scripts), `Fusion/marvel-lcg-src/tools/` (les tests du
  moteur). Chacun se défend, mais on ne sait pas où chercher.

#### 1.e — Ce qui va bien, à ne PAS toucher

- L'arborescence du moteur suit le guide : `data/`, `deck/`,
  `src/cards/pack/<pack>/`, `assets/pics/`.
- La double copie WSL + miroir Windows est **voulue** (§1.1 du guide).
- `.game/` (bytecode) à côté de `src/` est **voulu** aussi (§8), même si c'est
  un piège connu — ne jamais tester sur `.game/`.

**Ordre conseillé** : 1.a d'abord (gain maximal, risque nul), puis 1.c, puis
1.d, et 1.b en dernier.

### 1bis. Traduction FR du pack `brawn` — ✅ FAITE le 7/8/2026

Les 26 cartes (77001a-77025) ont leur texte français dans
`ui-app/src/board/textes-fr-fanmade.ts`, doublons compris (chaque `card_id` est
une clé). Conventions FFG respectées : ATQ/CTR/DEF/REC/MNG, Renfort,
Déferlement, Ténacité, Patrouille, Entrave, riposte ; noms propres et traits
`[[...]]` laissés en anglais ; jetons `[mental]`/`[physical]`/`[star]`/
`[per_hero]` recopiés tels quels ; « Team-Up » gardé en anglais comme sur les
autres packs.

Vocabulaire fixé pour ce pack : **réserve**, **compteur de rage**, **jeton
d'accélération**.

Vérifié : 26/26 traduites, `tsc` propre, 158 tests du plateau au vert,
`deployer.sh` passé sur les deux installations.

**La leçon est passée dans le guide** : la checklist « nouveau héros » (§5) a
désormais une étape 8 obligatoire, et une section §11.1 explique où vit le texte
français des cartes fan-made et pourquoi c'est le seul français que le joueur
verra. Le §11 ne parlait que de l'interface, d'où l'oubli.

### 2. Images Daredevil manquantes (15 proxies à remplacer quand les scans sortiront)
- 60011 Raising Hell, 60014 Karen Page, 60016 Sister Maggie, 60017 Billy Club, 60020 Cloak,
  60021 Dagger, 60022 Ghost Rider, 60025 Chance Encounter, 60027 Move in Shadow, 60029 Stick,
  60030 Contingency Planning, 60032 Sensory Overload, 60033–60036 (sauf 60033 fait) : Deadliest Man
  Alive, Stolen Sai, Eye on the Target.
- Re-tester périodiquement marvelcdb/cerebro (les scans arrivent quelques semaines après la sortie),
  puis remplacer les fichiers dans les 3 assets/pics et purger `assets/cache/600*`.

### 3bis. Vérifs en vraie partie — ✅ FAITES 28/07/2026 (7)
- **Photographic Reflexes depuis le tuck (Echo)** ✅ : cycle complet observé en partie bot — event
  aspect tucké par Watch and Learn, détucké par Muscle Memory, RE-joué DEPUIS le tuck pendant la
  fenêtre de défense (permission = PR en main OK), puis re-tucké. Lenience documentée : si les PR en
  main sont DÉPENSÉES comme ressources pour ce même play, la défausse-règle ne trouve plus de PR
  (double usage possible) ; la réduction GG (pay-effect du héros) est construite mais n'a pas été
  choisie par le bot (à observer en partie humaine).
- **Atonement jusqu'au victory display (Hercules)** ✅ : Protect Humanity révélée depuis le deck Labor,
  3 labor counters retirés → part au VICTORY DISPLAY (Victory « 0 » fonctionne, printed_victory=0)
  → Atonement : top Gift (Sword of Peleus) mise en jeu + Hercules ready + fenêtre de flip.
- **Paliers Son of Zeus (Hercules)** ✅ : le filtre du palier 1 (`IsClass('IdentitySpecific')` +
  upgrade épuisée) trouve bien Golden Mace épuisée ; paliers 2/3 = GiveStatus/DrawUp triviaux.
- **Sense deck (Daredevil)** ✅ : voir section 4 (5 bugs corrigés).

### 3. Héros/vilains/packs manquants (audit AFFINÉ du 27/07/2026 nuit, vs api/public/cards/ complet)
**Vilains/scénarios anciens : COMPLETS.** Toutes les boîtes 1→56 + Ronan modular + 25 Weekly Challenges
ont leurs scénarios dans sets_info (Core 3, GG 2, RoRS 5, Kang, GMW 5, MTS 5, Hood, SM 5, MG 5, Mojo 3,
NeXt Evol 5, AoA 5, AoS 5, Trickster 2, Civil War 4). L'API MarvelCDB n'expose pas les cartes rencontre,
donc pas d'audit carte-par-carte possible des rencontres, mais aucun scénario ne manque à l'appel.

**Cartes joueur/campagne absentes** : ✅ TOUTES AJOUTÉES le 27/07/2026 nuit (voir section « FAIT » ci-dessus) —
MTS 16, Mutant Genesis 29, NeXt Evolution 12, AoA 2, Civil War 16. Reste :
- **Wonder Man** : ✅ FAIT 27/07/2026 nuit — héros complet jouable (25 entrées : 58001a/b→58011,
  58022-58034, 58023=full_link 01088), deck/starter/wonder_man.json (précon Justice approximé : les 8
  dernières cartes complétées avec des staples Justice core 01060-01065, liste officielle inconnue),
  sets_info « 58. Wonder Man » créé, 34 images marvelcdb. Mécanique clé : tuck sous Ionic Physiology
  (mis en jeu au setup via BeginGameWithSetAside — le champ set_aside des starters est IGNORÉ par le
  loader, HeroDescriptor ne le lit pas) + « overpay » energy (helper EnergyOverpaid = min(energy payées,
  total-coût, cap)). V2 : Energy Siphon (bonus au spend) texte seul, Swordsman response défenseur texte
  seul, Cameo (search collection) texte seul, Coordinated Effort (paiement partagé) texte seul,
  Disarming Defense sans le discard d'attachment conditionnel, Mr. Hollywood sans limite once-per-card,
  boost ability de Death Cannot Die non implémentée. Tests : 3639 ok / 0 échec, PLAYERS: 1.
  **V2 ✅ FAIT 28/07/2026 (3)** : Energy Siphon 58006 (paire DoDiscardThisToGenerateResources
  res_fn + CheckThisCanDropPay, modèle 50014 ; CostFunc.Custom → DeclareNumber 0-3 dégâts en forme
  héros, +1 [energy] par dégât ; validé en partie bot — payé sans crash) ; Swordsman 58022
  (WhenBoostCardTurnedFaceUp HeroResponse + being_message.DeclareDefender + ReadyAll : défend sans
  s'épuiser, WM ne prend rien — validé chirurgicalement ; ATTENTION le nom d'option est
  'Hero_Response', pas 'Response') ; boost Death Cannot Die 58029 (WhenCardBecomeBoost +
  RunAt.AfterEnemyActivationEnd → Grim Reaper active après l'activation — validé chirurgicalement) ;
  Disarming Defense 58033 (réécrit modèle Desperate Defense 09015 : GainDEFForThisAttack(2) +
  IfYouTakeNoDamage → discard attachment 'Hero Action/Response' via GetAttachedAttachments, modèle
  56130) ; Cameo 58031 (AfterGameSetup — PAS WhenGameBeginSetup qui part AVANT la pioche, ni
  WhenCardSetup jamais envoyé aux cartes joueur Setup : world.py ne appelle Setup(False) que pour
  schemes/vilains/Evidence/identités — génère les ~58 alliés signature des héros absents via CardsDB,
  AskChooseFace, shuffle au deck, défausse 2, remove ; validé en partie bot de bout en bout).
  Restent texte seul : Coordinated Effort 58032 (paiement partagé, no-op en solo), limite « once per
  card » de Mr. Hollywood 58009 (déjà limitée de fait : un pay-effect n'est offert qu'une fois par
  paiement).
  CORRECTIF 28/07 : Jet Belt (58008) faisait crasher le lancement de partie (2 abilities resource sur une
  carte → assert card_player.py:50 à la génération du hero deck) — réduit à la 1re ability (energy pour un
  event, exhaust) ; le 2e mode (exhaust+défausse tuckée → energy libre) passe en texte seul v2.
  Même session : 59004 Protect Humanity avait Uses "3,labor" → 'labor' pas dans COUNTER_LIST → "3,counter".
  Nouveau test tools/test_generate_cards.py ajouté à la méthode (étape 7).
  ~~À noter : 10 cartes du JEU ORIGINAL échouent à la génération directe~~ → **✅ RÉSOLU 28/07/2026 (8)** :
  ces échecs venaient des vieux pyc ChatGPT de boot_sub, corrigés par la recompilation intégrale du
  28/07 (le TODO n'avait pas été re-vérifié après). Confirmation : **GEN COMPLET toutes cartes =
  4331 ok / 0 échec** (aucun préfixe, `test_generate_cards.py <boot_sub> <port>` sans argument).
- **Hercules** : ✅ FAIT 27/07/2026 nuit — héros complet jouable (39 entrées dont 7 full_link :
  59027→31023, 59029-31→01088-90, 59032→58034, 59033→01092, 59034→08023), deck/starter/hercules.json
  (précon Leadership approximé, complété avec 01069/01070/01074 core), sets_info « 59. Hercules » créé
  avec le modular **All Versus All** (encounter_sets/all_versus_all.json, sélectionnable comme modulaire).
  Mécanique clé : les DEUX decks annexes (Labor + Gift) vivent dans le MÊME additional_deck, filtrés par
  trait LABOR/GIFT (helpers GetAdditionalDeckTop/CountGifts) ; « Atonement » porté par les 3 cartes Labor
  (AfterCardLeavePlay → top Gift en jeu + ready + may flip) ; « Appeal to Athena » neutralise les Gifts
  via le helper CountGifts. Tests : 3671 ok / 0 échec, PLAYERS: 1.
  **V2 ✅ FAIT 28/07/2026 (4)** : redirects d'attaque câblés — Protect Humanity 59004 (ForcedInterrupt
  WhenUnitWouldAttack(Villain) + ChooseAbilities ally + ChangeDealtToTarget modèle 34033, garde « si un
  défenseur est déclaré, pas de redirection » ; décrément du labor counter via RunAt.AfterEventEnd si
  GetDefender()==Hercules — la dépletion des Uses envoie la carte au victory display via
  HasUses.RemoveCountersInternal, ce qui déclenche l'Atonement AfterCardLeavePlay) ; Amadeus Cho 59008
  (même pattern, minions → Cho) ; Golden Mace overkill (`message.would_message.GainOverKill`) ; Prince
  of Power heal = `message.excess_damage` (AfterUnitDefeatedUnit l'expose) ; Gilgamesh coût confuse
  (CostFunc.Custom + GainStatus('Confused'), skip si trait ETERNAL — validé en partie bot) ; Lernean
  Hydra choix spend R / heal 2 (ForChoiceAbilityWithCost(Cost('R')), modèle Intimidation 02035) ;
  Ares's Axe auto-défausse (IfUnitTakeDamageFromThisAttack + RunAt.AfterEventEnd, non testé en jeu).
  Le tout validé par test chirurgical (6 checks) + autoplay. **2 BUGS latents corrigés** (exposés par le
  fix 'ATK'/'DEF' de la veille) : 59014 et 32177 passaient `message` (WhenUnitUseBasicPower) à
  TemporaryGain → AttributeError AddGainedATK ; le bon idiome (carte originale 34034) est
  `message.would_message`. Restent texte seul : boost abilities étoilées du set némésis, limite
  « once per phase » de l'Atonement.
- **Synthezoid Smackdown** : ✅ FAIT 28/07/2026 — boîte PVP complète (88 entrées dans la nouvelle section
  `synthezoid`, dont 5 full_link 57078-57081→57036-57039 copies 2e équipe). Ce ne sont PAS des héros
  jouables : Vision et She-Hulk sont des LEADERS ennemis (type Leader I-IV) → 2 scénarios
  `she_hulk_pvp` / `vision_pvp` sur le modèle Civil War (villain I/II + mains schemes
  Registration/Resistance + deck du leader + side scheme du leader en set-aside révélé au setup
  coopératif). 9 encounter sets créés : standard_pvp (inclus dans les 2 scénarios), shield_ops,
  thunderbolts, taskmaster_pvp, deadly_duo (camp She-Hulk) ; young_avengers, scarlet_twins,
  moon_knight_pvp, royal_guard (camp Vision) — tous sélectionnables comme modulaires.
  Mécanique Vision : attachment double face Dense↔Intangible flippé après chaque phase vilain.
  sets_info « 57. Synthezoid Smackdown ». Images : 78 scans marvelcdb/cerebro + 5 proxies
  (57036-57039a/b Standard PVP, pas de scans). V2 : « your leader » = no-op en coop solo (GetYourTeamLeader
  None), Choosing Sides/Now It's Personal (mode compétitif) non jouables, Teenage Superheroes simplifié
  (surge si pas de minion), boost abilities étoilées non implémentées, Spellcasting défausse sans annuler.
  Tests : 3754 ok / 0 échec, GEN 88/88, DECKS 72/72, PLAYERS: 1 ×2.
- **Scénarios Fear No Evil** (Kingpin, Electro, Mysterio) : toujours PAS sur MarvelCDB, même avec
  `?encounter=1` (fne.json?encounter=1 → 66 cartes, seulement les 10 rencontre némésis déjà intégrées).
  Recheck périodique. Images déjà partiellement sur Hall of Heroes (kingpin-a1/a2, electro-1, mysterio,
  rhino, the-raft-breakout…) et scans cerebro à tester (60065+).
- Faux manque à ignorer : 10098 Shang-Chi (= 04098 dans le jeu, renuméroté par MarvelCDB).
- Méthode d'audit : télécharger `api/public/cards/` + `api/public/packs/`, comparer les codes aux
  card_id du jeu (tester code et code+'a'), PUIS vérifier les « manquants » par NOM (renumérotations
  et full_link possibles) en se méfiant des homonymes (ally Hercules 06011 ≠ héros 59001a).

### 4. Raffinements Daredevil (v1 → v2, optionnel)
- ✅ FAIT 28/07/2026 : les 4 passifs « texte seul » sont implémentés et validés (voir section FAIT).
- ✅ VÉRIFS EN JEU FAITES 28/07/2026 (7) — **5 vrais bugs Sense deck trouvés et corrigés** :
  1) le Sense deck n'était JAMAIS peuplé (60001b : il manquait le `ShuffleWithDiscardPile` du modèle
  Doctor Strange 09001b quand additional_deck est vide — BeginGameWithSetAside génère dans
  l'additional_discard_pile) ; 2) la redirection « leave play → bas du Sense deck » interceptait TOUTES
  les destinations (même l'entrée en jeu) → restreinte à `into_area.flags.is_discards`, avec
  `card.MoveToBottom` + re-flip du top via RunAt.AfterEventEnd ; 3) les 5 modules Sense passaient un
  CardFinder à `AttachToFaceWhenPutIntoPlayInternal` (crash GetAllLegalTargets) ET l'ability Play auto
  de la classe Upgrade ré-attachait la carte au HÉROS → remplacé par
  `CanPlayThisUpgradeCard(<finder>)` qui génère l'attache correcte ; 4) 60005/60006 : conditions sur
  `message.targets` inexistant (AfterUnitAttackUnit → `.attacked`, AfterUnitThwartScheme → `.scheme`) ;
  5) 60022 Ghost Rider : idem → `.took_damage_targets`. Validé en partie bot : Man Without Fear et
  Deposition jouent des Senses gratuitement (attaches vilain/scheme correctes), response de Superior
  Taste puis retour AU BAS du deck observés, top face visible maintenu, 0 traceback.

### 5. Divers
- `cache_max_age` réduit à 3600 s dans les launch.json (fix « vieilles images en cache navigateur »).
  Si un utilisateur voit encore de vieilles images : vider le cache navigateur une fois.
- Le launcher ouvre le navigateur automatiquement (attente jusqu'à 5 min).
- Sauvegardes des données pré-Daredevil : `data/cards.json.bak-daredevil`, `data/sets_info.json.bak-daredevil`.

## FAIT le 2/8/2026 : vague 2 — audit « texte seul » et multi-vilains ✅
- Audit : PLUSIEURS entrées ci-dessus étaient PÉRIMÉES (déjà câblées par des sessions précédentes,
  le TODO n'avait pas suivi) : Jet Belt 58008 2e mode (les deux modes vivent dans UNE ability avec
  check_mode+pay_tucked, l'assert 1-resource est contourné), Coup de Grâce 32176 (GainOverKill présent),
  boost-response du Rascal 55029a (WhenCardBecomeBoost + activating_enemy='This' présent).
- Nouveaux câblages du jour :
  * Stolen Sai 60035 : capacité Boost réelle (« attack gains piercing ») via
    WhenCardBecomeBoost('This', during_attack=True) + would_atk_message.GainPiercing — modèle Crossfire 04027.
  * Brazen Defense 32178 : vraie PRÉVENTION (WhenUnitWouldTakeDamage + PreventDamage(3), modèle Backflip)
    au lieu du -3 sur l'attaque ; compatible RR 1.8.
  * Labors Hercules 59002/03/04 : Atonement limité once per phase (.LimitOncePerPhase()).
  * Lightning Strike 61005 (custom Thor JF) : le stun payé « only energy » est désormais un CHOIX du joueur.
- Multi-vilains VALIDÉ sur parties réelles enregistrées (Sinister Six + Wrecking Crew, snapshots
  /get_world) : jusqu'à 4 EncounterVillain simultanés dans area_villain, attente en area_set_aside,
  villain_deck vide ; zones.ts documenté et répartition des phases groupée par nom.
- Restent volontairement texte seul (PVP/compétitif non jouable) : redirections leader 56133/56207,
  post-spend des 4 ressources PVP CW, Synthezoid « your leader », Choosing Sides / Now It's Personal,
  Spellcasting, Teenage Superheroes simplifié ; Mr. Hollywood 58009 (limite de fait) ;
  mission attempt AoA 45171a option B ; deck Future Past.

## FAIT le 2/8/2026 : fin de vague 6 + vague 7
- Bouton 🌐 FR/EN dans le header du wizard ET du plateau (demande utilisateur) :
  localStorage marvel-langue + route /set_language?fr|en (bascule à chaud de
  TransText, server_get.py) + reload. Dictionnaires FR→EN : ui-app
  src/board/dico-en.ts (263 entrées, t() partout) ; wizard
  public/js/prepare/dico-en.js (249 entrées) + regleEn/contrainteEn dans
  defis-info.js + t() local dans reprise.js (script non-module).
- Vague 7 : onglet « Défis » 🏆 dans l'étape Scénario (24 défis mensuels +
  Wild, extension synthétique dans catalog.js, badge DÉFI, règle FR/EN au
  survol depuis defis-info.js) ; bouton « 🧩 Puzzles » (liste
  /list_puzzle_files + /get_puzzle_json, lancement /load_puzzle → board).
  Testé serveur .game-test port 24519 : défi 2416 en jeu avec Rhino,
  puzzle 01071 chargé (Peter Parker/Rhino), bascule langue aller-retour OK.
  NOTE : client_ack.py exige maintenant le cookie app_version (get_version).

## FAIT le 2/8/2026 : vague 8 + début vague 9
- Météo de Storm sur le nouveau plateau (CoucheMeteo.tsx, iframe
  effects/weather, cartes 36003/04/05, bouton + marvel-board-meteo).
- Musique d'ambiance optionnelle (musique.ts) : cherche
  /musique-<slug-mechant>.mp3 puis /musique-plateau.mp3 (assets/sounds),
  OFF par défaut (marvel-board-musique). Aucun mp3 livré.
- Écran de fin enrichi : héros contre méchants, rounds, confettis victoire
  (coupés par Anim). Passe responsive tablette (media queries board.css) ;
  VALIDATION VISUELLE SUR TABLETTE DUE.
- Vague 9 (en cours) : PanneauOptions ⚙ regroupe Animations/Sons/Musique/
  Météo/Cartes révélées ; header allégé, 🌐 reste toujours visible.
- Vague 9 (suite) : raccourcis clavier E (fin du tour simple) / U (undo) +
  note dans le panneau ⚙ ; auto-ciblage quand une seule cible légale
  (interaction.ts, marvel-board-auto-cible, désactivable) ; curseurs des
  autres joueurs en multi (routes /set_cursor POST + /get_cursors dans
  server_get.py, périmés en 5 s ; CoucheCurseurs.tsx, throttle 150 ms,
  poll 700 ms, marvel-board-curseurs). Testé HTTP : ok.
  RESTE (écarté pour l'instant) : dégâts prévisionnels (21) — l'ATQ imprimée
  ignorerait les modificateurs, risque d'induire en erreur.
- Vague 11 : historique de partie PERSISTANT (sessionStorage
  marvel-historique-partie, purge auto si nouveau round_id plus petit) ;
  lien « Voir sur marvelcdb » dans le menu carte (codes \d{5}[a-z]?, les
  customs 5 chiffres peuvent 404 sur marvelcdb, sans gravité) ; textes
  officiels FR sous l'aperçu via proxy /marvelcdb_card?<code> (server_get.py,
  cache mémoire, timeout 6 s, testé : 01001a → « Sens d'Araignée... »).
  Option « Textes marvelcdb (réseau) » OFF par défaut dans le panneau ⚙.
- Vague 10 (agent, vérifié) : bloc « Avancé » de l'étape finale (seed + 🎲 +
  copier, temps par décision, premier joueur avec rotation dans launcher.js,
  interrupteur règles v16) + mémoire des choix (Récents dans l'étape Équipe,
  dernier deck par héros, dernier scénario présélectionné). Descripteur par
  défaut inchangé (testé).
- Vague 12 (en cours) : bannière de succès sur le plateau (CoucheSucces.tsx,
  Achievement: FIRST_BLOOD... → Premier sang..., option ⚙ marvel-board-succes)
  + tuiles Succès dans l'écran Stats (reprise.js, si > 0). Galerie de cartes
  en agent (public/galerie.html).
- Vague 12 terminée : galerie de cartes moderne (agent, vérifié) :
  public/galerie.html + css/galerie.css + js/galerie/app.js (4399 cartes,
  filtres type/extension/fan-made, aperçu + lien marvelcdb, lots de 60,
  images via cardImageUrl de api.js SANS extension) + bouton 🃏 Galerie
  (js/prepare/lien-galerie.js, hook dans prepare.html). Tout synchronisé
  vers Windows. LES 12 VAGUES DU PROGRAMME SONT LIVRÉES.
  Redémarrage serveur nécessaire pour les nouvelles routes
  (/set_language, /set_cursor, /get_cursors, /marvelcdb_card).
- Corrections cartes Rescue (Rainy) le 2/8/2026 :
  90121 First Responder : declencheur restreint aux personnages amis
  (identites + allies) ; RAW « personnage » inclurait le Mechant mais spam.
  90114a Rescue « Rapid Responder » : powers="DEF" -> powers=["DEF"]
  (CheckBasicPower itere la valeur : une chaine se decoupe en lettres et ne
  matche jamais -> la Reponse apres defense de base ne partait jamais).
  test_cards : 3851 ok / 0 err.

## FAIT le 2/8/2026 : audit de coherence de TOUTES les cartes
- Outil pérenne : tools/audit_cartes.py (texte imprime <-> capacites
  construites : types d'arguments AST, marqueurs Response/Interrupt/Action/
  WhenRevealed/WhenDefeated/Resource/Setup/Boost, couts d'inclinaison,
  cartes texte-seul ; liens full_link/ability_link resolus).
- 123 suspicions relues une par une (4 agents + revue) : 113 faux positifs,
  10 VRAIES discordances + 3 erreurs de donnees. TOUTES corrigees, marquees
  # CORRECTIF. Detail complet : RAPPORT-AUDIT-CARTES.md a la racine du projet.
  Scripts : 04162b, 55041, 55003, 55022, 56177, 40187, 45160, 57068, 27009,
  41013. Donnees cards.json : 16062a, 09014, 38031 (+ checksum recalcule ;
  integrite verifiee contre le miroir Windows : seules ces 3 cartes different).
- PIEGE MAJEUR CORRIGE : .game/ ne contient quasiment que du BYTECODE
  (4339 .pyc / 8 .py). Tester dessus validait une photo figee du moteur.
  Nouveau banc .game-src/ : cards/core/engine/game/editor/main.py sont des
  LIENS vers src/. C'est LUI qu'il faut viser pour test_cards et audit_cartes.
  Ex : python3.10 tools/test_cards.py .game-src 24521
- Etat final : test_cards 3866 ok / 0 err ; audit 0 type, 0 cout manquant,
  0 texte-seul, 0 construction impossible, 115 suspicions toutes expliquees.
- Harnais de tests de COMPORTEMENT cree : tools/test_capacites.py.
  Detourne DeviceManager.DoGetInput (technique de test_autoplay), monte une
  position via l'API Puzzle, declenche, verifie l'etat du monde. 1 cas =
  1 processus (moteur singleton). 3 cas verts couvrant 3 des corrections du
  jour : 56177 (Boost pose un statut), 55041 (When Defeated pose 3 shatter),
  04162b (cout Exhaust declare).
  VALIDE PAR L'EPREUVE INVERSE : bugs remis -> 0/3 ; bugs corriges -> 3/3.
  PIEGE : designer les cartes par CARD_ID, jamais par nom (deux « Venom
  Blast » : 04035 et 56177 ; le test visait la mauvaise carte au depart).
  Lancement : python3.10 tools/test_capacites.py .game-src 24540

## FAIT le 2/8/2026 (suite) : missions AoA, batterie de tests, alerte rsync
- Missions Age d'Apocalypse : les CONSEQUENCES de fin de mission (portees
  officiellement par les faces verso 45166b-45170b, non modelisees) n'etaient
  PAS implementees. Ajoutees dans missions.py -> MissionOutcome() :
  45166 Desperate Measures / 2 menaces par heros ; 45167 recherche / carte
  rencontre face cachee ; 45168 Sea Wall retire + 3 degats / Sea Wall revele ;
  45169 allie de campagne en main / defausse 1 ; 45170 recherche allie /
  DEFAITE. Plus le retrait des sbires de la zone de mission.
  Texte des 5 cartes 4516xa complete pour annoncer ces consequences.
  Verifie en jeu (3 branches testees, script /tmp/claude-1000/verif_mission.py).
- Batterie de comportement portee a 38 cas, tous verts (tools/test_capacites.py).

## !!! ALERTE OUTILLAGE : rsync --delete est DANGEREUX ici !!!
Les deux installations DIVERGENT : le pack `invisible_woman` (heros custom
WIP, 65001a-65018, 23 fichiers) n'existait que cote WINDOWS. Un
`rsync -a --delete src/` WSL -> Windows tente de le SUPPRIMER a chaque passage
(il n'a survecu que parce que __pycache__, exclu, empechait la suppression du
dossier). NE PLUS JAMAIS utiliser --delete pour src/ : faire
  rsync -a --exclude='__pycache__' <src>/ <dest>/
et verifier avec `diff -rq --exclude=__pycache__` avant tout nettoyage.
Le pack a ete rapatrie cote WSL : les deux cotes sont desormais identiques.
- 4 cartes du pack invisible_woman ne se construisaient pas (API inexistantes,
  travail en cours) : 65004 AfterIdentityChangedForm -> AfterUnitChangeForm ;
  65007 Character/control_by -> SetTarget(Friend, ...) ; 65018 WhenRevealed ->
  WhenThisRevealed(None, ...). test_cards : 3886 ok / 0 err.
- BUGS TROUVES PAR LA BATTERIE, NON CORRIGES (a arbitrer) : 64012 Hydro-Man
  (maximum=0 ecrase par `or` dans can_place_counter.py:52) ; 63011 Rules of the
  Universe (hazard jamais recalcule, change_on_event manquant) ; 90126 Board
  Meeting (identity.IsHero() n'existe pas sur une face -> crash a chaque
  revelation) ; 64009 Radiate (2 capacites Play, refuse hors RELEASE=1).
- Les 4 bugs trouves par la batterie sont CORRIGES (2/8/2026) :
  * MOTEUR can_place_counter.py : `maximum = would_message.maximum or maximum`
    avalait la valeur 0 (fausse en Python). Une carte posant maximum=0
    (64012 Hydro-Man) voyait son plafond ignore ET ecrasait le plafond global
    de 64001a. Passe en `is not None`.
  * MOTEUR card/factory.py : 64009 Radiate ajoute a la liste blanche des
    evenements a 2 capacites Play (le heros Human Torch ne se chargeait pas
    hors RELEASE=1).
  * 63011 Rules of the Universe : change_on_event=OnEvent.Threat("This")
    ajoute, l'icone hazard n'etait jamais recalculee.
  * 90126 Board Meeting : identity.IsHero() -> Hero.IsType(identity)
    (IsHero n'existe que sur Player : plantage a chaque revelation).
  Les 3 cas de test retires par l'agent ont ete REMIS et servent de gardes.
  Batterie : 41/41 verts. test_cards : 3886 ok / 0 err.

## FAIT le 2/8/2026 : pack Invisible Woman COMPLET et jouable
- Scans recuperes depuis 3 dossiers Drive (SEALED / HERO DECK / ENCOUNTER SET),
  25 images, liste de deck officielle incluse.
- COLLISION D'IDENTIFIANTS : les scripts utilisaient 65001a-65018, deja pris
  par le pack mister_fantastic. Tout renumerote en 66001a-66018 (66 etait libre).
- Livre : 20 cartes dans cards.json (groupe invisible_woman) + checksum,
  deck/starter/invisible_woman.json (40 cartes), sets_info « 104. Custom
  (Invisible Woman) », 20 images dans assets/pics/66xxx, traits INVISIBLE et
  TRAANIAN ajoutes a la liste blanche (# CORRECTIF).
- Heros A TROIS FACES : 66001a forme INVISIBLE (THW2/ATQ1/DEF2, main 5),
  66001b alter ego Sue Storm (REC3, main 6), 66001c forme PSIONIC
  (THW1/ATQ2/DEF2, main 4), 8 PV partout.
- 5 ecarts scan/script corriges : 66005 Flying Disk (AERIAL conditionne a la
  forme PSIONIC), 66013 Family Time (retrait du jeu au lieu de defausse +
  bascule alter ego proposee), 66016/66017 (attachement sur Psycho-Man, Renfort
  si impossible), 66018 (revelation limitee aux 2 attachements).
- SUBSTITUTIONS DANS LE DECK : 4 cartes de base de la liste d'origine sont
  absentes de notre collection (Human Torch - Johnny Storm, Powerhouse -
  Franklin Richards, Better Together, Flaming Force) ; remplacees par des
  basiques equivalentes, note dans metadata du deck.
- RESTE A FAIRE : 66007 Force Shields est incomplete cote script (le scan
  impose « defausser X cartes a ressource physique » et cible X personnages ;
  le script n'a qu'un cout d'inclinaison et cible tous les allies).
- A NOTER : mister_fantastic (65xxx) a ses donnees et ses scripts mais AUCUN
  deck de depart, donc il n'apparait pas non plus dans le wizard.
- Tests : test_cards 3904 ok / 0 err, test_capacites 43/43.

## FAIT le 2/8/2026 : arts alternatifs (heros + ressources)
- ARTS DE HEROS (nouveau) : meme mecanique que les ressources, cle localStorage
  mc_hero_art_v1, table ARTS_HEROS dans ui-app/src/board/variantes.ts ET dans
  public/js/prepare/app.js (a garder alignees). Selecteur « Carte de héros »
  ajoute a cote de celui des ressources (blocArtHeros).
  Source : PDF hallofheroeslcg.com « Alternate Art Hero Cards by M3T4LB0X »,
  planche 3x3 a 600 dpi, decoupee (cartes 1500x2100).
  RETENUS (6) : 01001a Spider-Man, 01010a Captain Marvel, 01019a She-Hulk,
  01029a Iron Man, 03001a Captain America, 04001a Hawkeye -> *_m3t.jpg
  ECARTES, car l'art afficherait des valeurs FAUSSES en jeu :
   * Wasp de la planche : DEF 1 / PV 10 / AERIAL, alors que 13001a est
     DEF 2 / PV 11 / TINY et 13001c DEF 3 / PV 11 / GIANT ;
   * Beta Ray Bill : c'est un autre heros, pas un art de Thor ;
   * Spider-Man « Bombastic Bag-Man » : trait imprime FANTASTIC FOUR au lieu
     d'AVENGER (le moteur, lui, garde AVENGER).
- ARTS DE RESSOURCES : 16 collections « DesignHacker » ajoutees depuis le
  Dropbox de l'auteur (2021 x12, 2022 x4), 48 images *_dh_*.jpg.
  Identification faite a l'oeil sur planche-contact ; dh_12 et dh_14 sont
  restes NON IDENTIFIES et portent un nom neutre (a renommer si besoin).
  Les 45 fichiers « RESOURCE copy N.jpg » de la racine du zip n'ont pas ete
  traites : nommage generique, identification visuelle une par une necessaire.
- NON FAIT : l'album Imgur (mc-custom-alt-arts) est rendu en JavaScript et ne
  livre aucune liste exploitable, ni en direct ni via la vue integree. Il
  faudrait les liens i.imgur.com ou un export zip.
- Les 45 fichiers « RESOURCE copy N.jpg » de la racine du zip Dropbox sont
  identifies : ce sont les promos officielles FFG « Play-and-Share » AU
  COMPLET, 15 heros x 3 ressources, dans l'ordre alphabetique du zip
  (Black Panther, Captain America, Captain Marvel, Doctor Strange, Hawkeye,
  Hulk, Iron Man, Ms. Marvel, She-Hulk, Spider-Man, Spider-Woman, Thor,
  Ant-Man, Black Widow, Wasp ; chaque triplet = Energy, Genius, Strength).
  * 7 NOUVELLES collections : ds, hk, hu, sw, am, bw, wa.
  * 8 existantes AMELIOREES : elles etaient en 225x320, remplacees par la
    source haute resolution (969x1387 reduite a 400x572).
  Total : 31 collections de ressources + 6 arts de heros.
- Arts alternatifs, finitions : survol qui agrandit (heros + ressources, les
  TROIS cartes pour une collection), ecran « Face a face » et apercu de heros
  qui montrent l'art choisi, pastille « ART ALT » sur les cartes concernees
  (sous les PV, les deux coins hauts etant pris), liste triee alphabetiquement
  apres Standard/Aleatoire, tailles d'apercu HARMONISEES (les regles CSS
  utilisaient max-height, qui ne fait que reduire : chaque image sortait a sa
  resolution native). Les deux collections non identifiees sont resolues :
  dh_12 = War Machine, dh_14 = Spectrum (Monica Rambeau).
