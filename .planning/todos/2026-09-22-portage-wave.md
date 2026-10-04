# Portage de Wave (Pearl Pangan)

Demande de l'utilisateur, 22/09/2026, dossier Google Drive « Wave (Pearl
Pangan) » (auteur : Mysteltainn, `jamesfvfleming@gmail.com`).

## ⚠⚠ CORRECTIF D'IDENTIFIANTS, 22/09/2026 (avant toute écriture dans
`cards.json`)

La première version de cette fiche assignait `40001`-`40020` à Wave —
**une confusion avec les vrais identifiants de CABLE** (pack `next_evol`,
QUI OCCUPE DÉJÀ TOUTE LA TRANCHE 40001-40204 : `40001a/b` Cable/Nathan
Summers, `40002` Bodyslide, `40006` Technovirus Purge, etc. — vus de mes
propres yeux dans le rapport de bug Spider-Man/Technovirus Purge du même
jour). Aucune donnée n'avait encore été écrite, donc aucune collision
réelle n'a eu lieu, mais la règle du guide (§9, entrée `moon_knight`) est
explicite : **« TOUJOURS vérifier les doublons de `card_id` sur TOUTE la
collection avant de choisir une tranche »**, précisément le contrôle que
j'avais sauté.

Vérifié par balayage de `data/cards.json` ET `data/cards_custom.json` :
**`65001`-`65099` est entièrement libre** (le grand vide entre `62037`,
dernière carte officielle, et `90001`, un pack fan-made isolé de 5 cartes).
Tranche retenue pour Wave : **`65001`-`65019`**.

## Ce qui a été lu (texte exact des 24 images du dossier, vérifié à l'image
directe pour toutes les cartes portant des chiffres) — identifiants
CORRIGÉS ci-dessous

**Identité**
- `65001a` * Wave (Hero) : THW 1, ATK 2, DEF 2, HP 10, HS 5. Traits ATLAS,
  TRIUMPH DIVISION. « Storm Surge — Response: After you discard cards from
  your hand to pay for a cost, place 1 of those cards in your Rising Tide
  area. »
- `65001b` * Pearl Pangan (AlterEgo) : REC 3, HP 10, HS 6. Traits ATHLETE,
  CIVILIAN. « Setup: You begin the game with a Rising Tide area (see
  insert). Champion Swimmer — Action: Place the top card of your deck faceup
  in the Rising Tide area (limit once per phase). »

**15 signatures, 9 cartes uniques** (WAVE 1/15 à 15/15 — recompté : 1+3+2+2+2+2+1+1+1 = 15)
1. `65002` * Sea Hunter (Ally) — Cost 2, THW 1, ATK 1, HP 3. ATLAS. SIRENA.
   MaxPerDeck 1 (une seule copie imprimée). « Response: After Sea Hunter
   attacks or thwarts, flip a faceup card in your Rising Tide area and pay
   the printed cost of an event in your discard pile → play that event as
   though it were in your hand. »
2-4. `65003` Crashing Wave (Event) ×3 — Cost 1. ATTACK. SUPERPOWER.
   MaxPerDeck 3. « Hero Action (attack): Deal 1 damage to an enemy. Flip up
   to 3 faceup cards in your Rising Tide area facedown → deal 2 additional
   damage for each card flipped facedown this way. »
5-6. `65004` Marine Patrol (Event) ×2 — Cost 1. THWART. SUPERPOWER.
   MaxPerDeck 2. « Hero Action (thwart): Remove 2 threat from a scheme. Flip
   up to 2 cards in your Rising Tide area facedown. For each card flipped
   this way, choose (max 1 each): remove 2 threat from a scheme. draw 1. »
7-8. `65005` Instinctive Flow (Event) ×2 — Cost 1. SUPERPOWER. MaxPerDeck 2.
   « Hero Action: Flip up to 3 faceup cards in your Rising Tide area
   facedown. For each card flipped facedown this way, choose (max 1 each):
   deal 2 damage to an enemy. remove 2 threat from a scheme. stun an enemy. »
9-10. `65006` Ocean's Fury (Event) ×2 — Cost 1. SUPERPOWER. Max 1 per round.
   MaxPerDeck 2. « Hero Action: Until the end of the round, after Wave
   defeats an enemy or removes the last threat from a scheme, draw 1 card
   and flip a facedown card in your Rising Tide area faceup. »
11-12. `65007` Tide Wall (Event) ×2 — Cost 0. DEFENSE. SUPERPOWER.
   MaxPerDeck 2. « Hero Interrupt (defense): When you would take any damage,
   prevent up to 3 of that damage. For each point of damage prevented this
   way, place the top card of your deck faceup in the Rising Tide area. »
13. `65008` * Pearl's Lolo (Support) — Cost 1. PERSONA. MaxPerDeck 1.
   « Alter-Ego Action: Flip a faceup card in your Rising Tide area facedown
   → heal 3 damage. »
14. `65009` * Wave's Swords (Upgrade) — Cost 1. Restricted. TECH. WEAPON.
   MaxPerDeck 1. « Hero Action: Exhaust Wave's Swords and flip a faceup card
   in your Rising Tide area facedown → ready Wave. »
15. `65010` * Wave's Crown (Upgrade) — Cost 2. TECH. MaxPerDeck 1.
   « Wave gains +1 THW. You may play cards tucked under here as if they were
   in your hand. Action: Exhaust Wave's Crown → tuck 1 faceup card in your
   Rising Tide area under here (max 2). »

**Némésis (6 cartes, WAVE NEMESIS 1/5 à 5/5 + obligation)**
`65011` (1/5) Alontech's Greatest Achievement (SideScheme) — menace 2 par
   joueur (icône « 2 + silhouette »). « Increase the cost of the first event
   each player plays each turn by 1. »
`65012` (2/5) The Reyna Sirena (Minion) — SCH 2, ATK 2, HP 5. ALONTECH.
   ELITE. SIRENA. « As an additional cost for the engaged player to play an
   event, that player must take 1 damage. » Boost : You are stunned.
   (Wave's nemesis minion — désigné comme tel dans le texte imprimé.)
`65013` (3/5 et 4/5, ×2) Alontech Hybrid (Minion) — SCH 1, ATK 2, HP 4.
   ALONTECH. « SIRENA minions and villains cannot be attacked by the player
   Alontech Hybrid is engaged with. »
`65014` (5/5) Alontech Seawolf (Attachment) — VEHICLE. Attach to the main
   scheme. « Forced Interrupt: When the player phase begins, deal 1 damage
   to each player. Hero Action: Place 1 threat on the main scheme and
   discard an identity-specific card from your hand → discard this card. »
`65015` Triumph Probation (Obligation) — Give to the Pearl Pangan player.
   « Search your hand, deck, discard and play area for Wave's Swords and
   Wave's Crown and place them facedown under this card. Wave loses the
   TRIUMPH DIVISION trait. Alter Ego Action: Exhaust Pearl Pangan → add
   Wave's Sword and Wave's Crown to your hand and remove Triumph Probation
   from the game. »

**3 ressources personnalisées** (HeroSpecificResources, texte imprimé
identique aux ressources de base — max 1 par deck, aucune règle spéciale) :
`65017` Energy, `65018` Genius, `65019` Strength — reskins purs, cartes
`Resource` ordinaires avec l'icône correspondante, `desc.MaxPerDeck = "1"`.

**Le mot-clé maison : « Rising Tide area »** (règles complètes de
`WaveInsert.png`, lues à l'image) :

> Pearl Pangan/Wave has a unique area... At the start of the game, this area
> is empty, and cards can only be placed inside... by an effect that
> explicitly places them in this area... When a card is placed..., it is
> placed face-up, and can be flipped face-down by effects that flip cards...
> face-down. Cards... cannot be affected by effects that do not explicitly
> target the Rising Tide area.
> At the end of the player phase, before players draw up to their hand size,
> place all cards in the Rising Tide area in their owner's discard pile.
> Q: Can I look at face-down cards... using effects such as Jessica Drew's
> Alter-Ego ability? A: No, the Rising Tide area is an area, rather than a
> deck.
> Q: If a card asks me to discard a card I control, can I discard an ally in
> my Rising Tide area? A: No. Cards... cannot be affected by effects that do
> not explicitly target the Rising Tide area.

## ⚠ Décision : PAS de fiche dans `docs/reference/mots-cles/`

Le critère établi par l'audit du catalogue (voir le README de ce dossier,
section « Packs passés en revue ») est : mot-clé = terme imprimé EN GRAS sur
une carte. « Rising Tide area » n'apparaît **jamais en gras** sur aucune des
24 cartes lues (vérifié à l'image directe) — c'est une ZONE, comme la
Réserve du pack `brawn`, dont le nom n'est lui non plus jamais en gras et
qui a été explicitement écartée de ce catalogue pour la même raison.
**Même traitement que la Réserve** : documentée au §9 de
`GUIDE-CREATION-CONTENU.md` (« Divergences volontaires à préserver »), pas
ici.

## Recherche moteur faite (avant d'écrire une ligne de code)

Le mécanisme de face visible/cachée PAR CARTE existe déjà nativement :
`Card.state.is_face_up` (booléen par carte, indépendant de la zone),
`Card.Flip(effect)` le bascule tout seul quand `back_faces == []` (le cas de
toute carte joueur normale, qui n'a qu'une face). `Card.Render()` envoie déjà
`down_card_ids = ['player']` (dos générique carte joueur) pour toute carte
face cachée appartenant à un joueur, hors de tout code neuf. Donc :
**aucun mécanisme de rendu à inventer**, seulement une ZONE neuve + des
capacités qui appellent `Flip()`.

Point OUVERT, à trancher en écrivant l'identité : une carte face cachée
dans Rising Tide area est-elle visible à SON PROPRIÉTAIRE ? `Card.IsVisible`
n'a que 3 cas structurels (face visible / en main + propriétaire / zone
« comme en main » + propriétaire) ; aucun ne couvre une zone hors-jeu NON
« comme en main ». Par défaut, donc, **invisible même à son propriétaire**
(comme un deck), sauf action explicite. Coût si c'est le mauvais choix : le
joueur ne voit pas sa propre carte retournée — à corriger si signalé.

Hameçon de fin de phase trouvé : `Message.WhenPlayerEndPhase` (envoyé dans
`PlayerPhase.EndPhase()`, `src/game/player/element/player_phase.py:86`,
juste AVANT `MayDiscardHandCardsAndDrawUpToMax` qui fait la pioche jusqu'à
la main) — colle exactement à « before players draw up to their hand
size ». Pas encore de fabrique `AbilityFactory` dessus (à ajouter,
`turn_phase.py`, calqué sur `WhenPlayerPhaseEnd`).

Hameçon « décharger une carte pour payer un coût » trouvé :
`Message.AfterCardsBeSpendAsResource(faces, for_effect, player)`
(`sender_card.py:95`) — la liste COMPLÈTE des cartes dépensées pour UN effet
donné. Pas de fabrique générique (seulement
`AbilityFactory.AfterYouSpendThisCard`, filtrée sur UNE carte) : `Ability()`
construite à la main dans le script de Wave, filtrée sur les cartes dont la
zone d'origine était la main — pattern déjà utilisé ailleurs dans le dépôt
sans fabrique dédiée (`aa001b.py`, `ar012.py`...).

## Plan d'exécution

- [x] A. Moteur : nouvelle zone `DeckType.RisingTideArea` (`deck_type.py`),
      `player.rising_tide` (`player.py`), exposition au descripteur
      (`descriptor/world.py`, `to_descriptor.py`), fabrique
      `AbilityFactory.WhenPlayerEndPhase` (`turn_phase.py`), zone enregistrée
      dans `RunPuzzle.ZONES_JOUEUR` (`puzzle.py`). **Purge de fin de phase
      cablee en plus** (22/9/2026, apres relecture) : `PlayerPhase.EndPhase()`
      (`player_phase.py`) vide `player.rising_tide` dans la defausse AVANT
      `MayDiscardHandCardsAndDrawUpToMax`, pour CHAQUE joueur (regle
      universelle de la zone, comme `EnforceReserveLimit` pour la Reserve —
      pas une capacite de carte).
- [x] B. Plateau : emplacement `rising-tide` dans `zones.ts`
      (`t('Ta marée montante')`, corrigé le 22/9/2026 après un premier essai
      en anglais brut qui faisait échouer `dico-en.test.ts` — entrée ajoutée
      à `dico-en.ts`), rendu (`Board.tsx`, `board.css`), glisser-déposer
      (`PILE_PAR_ZONE` dans `glisser-manuel.ts`, `ZONES_MANUELLES` +
      `libellePile()` dans `MenuTriche.tsx`). `npm run typecheck` et
      `npm test` (175 fichiers, 1957 tests) verts au 22/9/2026.
- [x] C. Cartes dans `data/cards.json` : identité (2 faces) + 9 signatures
      uniques (15 copies) + 5 némésis + obligation + 3 ressources = 19
      entrées, tranche `65001`-`65019`. Chargement vérifié via
      `CardsDB.papers`.
- [x] D. Scripts (`src/cards/pack/wave/wave/*.py` + `wave_nemesis/*.py`) :
      16 fichiers (65001a, 65001b, 65002-65010, 65011-65015) + le fichier
      d'aide partagé `wave/__init__.py`. **Tous chargés sans erreur** via
      `CardsDB.FindAbilities` (harnais `.game-src-par9`, bootstrap
      `from engine import Engine` puis `Ver.Initialize()` puis
      `CardsDB.Initialize()` — l'ordre exact qui evite l'import circulaire
      rencontre en testant directement `cards.database`).
      Bug trouvé et corrigé en repassant sur `65001a.py` :
      `message.player` → `message.to_player` (l'attribut réel de
      `TriggerNonePlayerMessage`). Fausse piste de traduction trouvée et
      corrigée : `t(...)` n'existe PAS dans ce dépôt (les `prompt=` sont du
      texte brut) — supprimé de tous les fichiers `wave/*.py` par script,
      avec une casse de regex (`Exhaust("This")` mutilé en `Exhaus"This")`)
      recorrigée à la main dans 65009/65010.
- [x] E. `deck/starter/wave.json` (identité + 15 copies signature listées
      RÉPÉTÉES par copie — convention confirmée sur `cable.json`,
      `adam_warlock.json`, etc., pas des id uniques — + obligation + set
      némésis avec Alontech Hybrid x2, `player_deck` VIDE). `data/
      sets_info.json` complété (entrée "175. Custom (Wave)").
      `data/identites.json` PAS mis à jour : fichier généré par un outil
      (`outils/annuaire-identites.py`, introuvable dans ce checkout) —
      seulement utile au repérage d'illustrations (étape I), laissé pour la
      pose des images.
- [x] F. `GUIDE-CREATION-CONTENU.md` §9 : deux entrées ajoutées (zone Rising
      Tide area + pack `wave`), calquées sur les entrées Réserve/`brawn`.
- [x] G. Gabarits `PROCESSUS-CARTE.md` × 16 — **FAIT le 22/09/2026 (nuit)** :
      `.planning/todos/2026-09-22-wave-gabarits-processus-carte.md`. Aucune
      carte n'est « terminée » au sens strict (étapes 4 et 8 manquantes sur
      les 16, quelques réserves nommées carte par carte) — voir le bilan de
      ce fichier.
- [~] H. Tests moteur + `tools/test_capacites.py` + preuve par substitution.
      **DÉMARRÉ ET VERT le 22/09/2026, en vraie partie (pas seulement
      statique)** : trois cas ajoutés à `tools/test_capacites.py`
      (`.game-src-par9`, filtre `"wave"`/`"65001b"`/`"Pearl's Lolo"`,
      3/3 verts) :
        1. **65001b Champion Swimmer** — pose le dessus du deck FACE VISIBLE
           en Rising Tide area. Premiere preuve d'ECRITURE reelle dans la
           zone (`PlacerFaceVisibleDansRisingTide`).
        2. **Purge de fin de phase** (regle moteur ajoutee dans
           `PlayerPhase.EndPhase()`, voir A) — **preuve par substitution
           faite** : code commenté → ROUGE (« Rising Tide area contient
           encore 1 carte(s) » — mesuré), code restauré → VERT. C'est la
           preuve la plus importante de ce lot : ce code moteur n'avait
           JAMAIS tourné avant ce cas.
        3. **65008 Pearl's Lolo** — retourne une carte face visible en
           Rising Tide (reste dans la zone, passe face cachée) et soigne 3.
           Valide `CoutRetournerUneCarteRisingTide` (`CostFunc.Custom`),
           partagé par 65009 Wave's Swords et l'esprit de 65010 Wave's
           Crown — confiance élevée que ces deux-là fonctionnent aussi.
      **Bug réel trouvé et corrigé en écrivant ces cas** (PAS seulement un
      problème de harnais) : `CartesDansRisingTide` (`wave/__init__.py`) et
      `65002.py` (Sea Hunter) appelaient `.face` sur le résultat de
      `Deck.GetAll()`, qui rend déjà des `CardFace` (pas des `Card`) —
      `AttributeError` certaine au premier déclenchement réel. Aucun des
      tests précédents (chargement `CardsDB.FindAbilities`) ne pouvait
      l'attraper : `GetAbilities()` ne fait qu'enregistrer les fermetures,
      il ne les APPELLE jamais. Exactement l'avertissement du §9 de
      `PROCESSUS-CARTE.md` (« une gate qui répond OK n'est pas une preuve »).
      **Piège de harnais découvert et documenté** (dans les cas eux-mêmes,
      pour que personne ne le repaie) : `Puzzle.ChangeForm('<id>')` ne
      retrouve QUE la face **actuellement active** par son id (jamais la
      face inactive d'une identité à deux faces) puis la fait basculer vers
      l'AUTRE forme — appeler `ChangeForm` avec l'id de la forme qu'on VEUT
      atteindre (au lieu de celui de la forme courante) fabrique une carte
      orpheline sans planter au moment du `ChangeForm`, puis fait planter le
      `Puzzle.Action` suivant (`AssertionError` dans `GetControlByPlayer`).
      Confirmé IDENTIQUE sur `kate_bishop`/`human_torch` (pas spécifique à
      Wave) : aucun cas existant du dépôt n'enchaînait `ChangeForm` puis
      `Action` sur le MÊME id, donc jamais découvert avant. Wave, comme les
      autres héros, **commence la partie en forme alter-ego** (65001b Pearl
      Pangan) — aucun `ChangeForm` n'est donc nécessaire pour Champion
      Swimmer ou Pearl's Lolo (tous deux `AlterEgoAction`/action sur la face
      alter-ego).
      **TERMINÉ le 22/09/2026 (nuit) : les 16 cartes ont chacune leur cas
      réel, toutes vertes.** Cases ajoutés après les 3 premiers ci-dessus,
      filtre `"650"` sur `tools/test_capacites.py` (`.game-src-par9`) :
        4. **65001a Storm Surge** — une carte défaussée pour payer un coût
           part en Rising Tide area face visible.
        5. **65003 Crashing Wave** — 1 dégât de base + 2 par carte
           retournée (jusqu'à 3), mesuré à 7 dégâts avec 3 cartes posées.
        6. **65004 Marine Patrol** — 2 menace de base + choix « max 1
           chacune » sur 2 cartes retournées (menace ET pioche consommées,
           jamais deux fois la même branche).
        7. **65005 Instinctive Flow** — 3 cartes retournées → les TROIS
           branches (dégâts/menace/étourdissement) parties une fois chacune.
        8. **65007 Tide Wall** — prévention plafonnée à 3, 1 carte posée par
           point RÉELLEMENT prévenu (mesuré avec un ATK boosté aléatoire :
           preuve écrite pour être robuste au nombre exact).
        9. **65006 Ocean's Fury** — déclencheur différé (retire la dernière
           menace → pioche + retourne une carte), ET témoin d'épuisement
           « Max 1 per round » (une 2e copie, tentée directement via
           `PlayCardsLikeInTurn`, reste sans effet).
        10. **65002 Sea Hunter** — retourne une carte, rejoue un événement
            de la défausse en payant son coût imprimé ; measure une chaîne
            complète (Sea Hunter attaque → Storm Surge → Crashing Wave
            rejoué → sa propre branche de retournement), 4 dégâts au total.
        11. **65011 Alontech's Greatest Achievement** — preuve par REFUS :
            avec 1 seule icône, Crashing Wave (coût 1+1) reste injouable.
        12. **65012 The Reyna Sirena** — 1 dégât de coût additionnel pour
            jouer un événement engagé avec elle.
        13. **65013 Alontech Hybrid** — le vilain engagé avec elle ne peut
            plus être attaqué par ce joueur (`Puzzle.Attack` refusé,
            0 dégât).
        14. **65014 Alontech Seawolf** — les TROIS capacités en un cas :
            attachement à la manigance principale, interrupt forcée de
            début de phase (1 dégât), action héros à double coût qui se
            défausse elle-même.
        15. **65015 Triumph Probation** — cycle complet : recherche
            multi-zones + glissement, perte du trait TRIUMPH DIVISION,
            récupération complète (main + retrait du jeu + inclinaison).

      **Trois bugs réels supplémentaires trouvés ET corrigés en écrivant
      ces cas** (au-delà du `.face` déjà noté) :
        - **65001a Storm Surge** : la redirection de défausse utilisait
          `until_resolve_effect=effect`, qui désarme l'abilité dès que LA
          RÉPONSE ELLE-MÊME termine de résoudre — c'est-à-dire AVANT que
          `World.DiscardResourcesArea()` (deux lignes plus loin dans
          `player_action.py`) n'envoie la vraie défausse. La redirection
          n'avait donc jamais le temps de s'armer. Corrigé en
          `until_round_end=True`, calqué sur le vrai modèle
          (`RecyclerVersLaReserve`, pack brawn) que le premier jet avait
          mal recopié.
        - **65012 The Reyna Sirena** et **65014 Alontech Seawolf** : les
          deux utilisaient `Utility.DealDamageToCharacterYouControl`, qui
          OFFRE UN CHOIX parmi tous les personnages contrôlés (alliés
          compris). Or « that player must take 1 damage » / « deal 1
          damage to each player » vise TOUJOURS l'identité du joueur,
          jamais un allié — ce n'est pas la même chose que « a character
          you control ». Corrigé en `this.DealDamage([joueur.GetIdentity()],
          1, effect)`, direct, sans choix.
        - **65015 Triumph Probation** : `hero_face.GainTraits(-1, [...],
          effect)` avec l'`effect` DE L'OBLIGATION levait une exception
          AVALÉE EN SILENCE par le moteur (`list.remove(x): x not in
          list`). `CardFace.GainTraitInternal` (game/card/face/model/
          trait.py) attribue chaque trait au GRANTOR (`by_effect.this`),
          jamais à la face modifiée — un trait IMPRIMÉ est enregistré par
          `ResetTrait` sous LA FACE ELLE-MÊME, retirer une entrée exige
          donc un effet dont `.this` EST cette face. Corrigé avec
          `GameRule(hero_face)` (game/effect/rule.py) au lieu de `effect`.
          Aucune carte du dépôt ne semble faire « X perd le trait Y »
          avant celle-ci — mécanique neuve, piège neuf.

      **Deux pièges de harnais supplémentaires documentés** (dans les cas
      eux-mêmes) : (a) `Puzzle.Reveal`, pas `Puzzle.Deal`, pour donner une
      obligation « Give to the X player » — `Puzzle.Deal` ne déclenche PAS
      `WhenObligationGiveToPlayer` (aucun précédent du dépôt ne l'utilise
      pour une obligation ; `Puzzle.Reveal` est le modèle confirmé, ok019).
      (b) `Search.PlayerCard`/`SearchForCard` avec `may=True` pose un choix
      interactif qui a besoin de `"accepter_choix": True` pour ne pas être
      décliné par défaut — sans lui, une recherche qui devrait trouver une
      carte unique rend `None` silencieusement.

      **Étape 8 bis (test plateau) FAITE depuis, pour la zone elle-même**
      — voir plus bas. **Étape 8 (autoplay ciblé) toujours hors de portée
      de ce cas-par-cas.**
- [~] I. Images — **16/19 posées le 22/09/2026 (nuit).** Les scans
      téléchargés plus tôt dans la session (scratchpad, PNG 1500×2150)
      pour les 9 signatures hors identité, les 3 ressources et les 4
      cartes némésis (pas l'obligation) ont été redimensionnés à 300×434
      (taille standard du dépôt, vérifiée contre `01001a.jpg`/`01002.jpg`)
      et convertis en JPEG qualité 90, posés sous `assets/pics/<card_id>.jpg` :
      65002-65014, 65017-65019. Deux cartes vérifiées à l'image après
      pose (65002, 65011) : texte lisible, mise en page correcte, conforme
      au script. **Restent 65001a (Wave), 65001b (Pearl Pangan) et 65015
      (Triumph Probation)** : leurs scans n'ont jamais été téléchargés
      (identité et obligation, jamais récupérés du dossier Drive) — le lien
      du dossier ne figure dans aucun fichier de session retrouvable,
      il faudra le redemander pour finir cette étape.

**Étape 8 bis, test plateau — FAIT le 22/09/2026 (nuit).**
`ui-app/src/board/rising-tide-area.test.ts` (modèle
`attachement-en-chaine.test.ts`, la leçon Contingency Plan de Superior
Spider-Man) : 5 cas, tous verts au premier essai. Prouve que la Rising Tide
area dessine réellement ce que le moteur y place — une carte posée y
apparaît dans l'emplacement `'rising-tide'`, face visible montre sa vraie
face, face cachée-et-invisible-pour-ce-siège reste un dos générique
(jamais `peeking`, contrairement à la Réserve du pack `brawn` qui porte
`dansLaMain: true`). Suite complète du client (176 fichiers, 1962 cas)
toujours verte après ajout. Ce test couvre le mécanisme PARTAGÉ par
(quasiment) toutes les cartes du pack ; il ne revérifie pas individuellement
le rendu propre à 65010 (sa pile glissée) ni 65014 (son attachement), deux
mécanismes empruntés tels quels à `black_cat`/l'officiel `04135` et déjà
couverts ailleurs dans le dépôt.

**Étape 8, autoplay ciblé — FAIT le 22/09/2026 (nuit).**
`tools/autoplay.py .game-src-par9 --deck wave --vilains rhino --difficultes
normal --profils equilibre --parties 8` : **8/8 parties, 0 incident**, grep
exhaustif des 8 journaux (`NameError|AttributeError|TypeError|KeyError|
AssertionError|ValueError|Traceback`) confirmé à zéro partout. Le journal
détaillé (`/tmp/autoplay-wave-8.json`) montre le pilote déclencher
naturellement une bonne partie du pack en jeu réel simulé : `Champion_Swimmer`,
`Storm_Surge`, `Tuck_under_Wave's_Crown`, `Place_in_your_Rising_Tide_area`,
`Flip_up_to_2/3_..._facedown`, `Defense` (Tide Wall), etc.
⚠ **Taux de victoire non représentatif** (0 %, `player_deck` intentionnellement
vide — règle du 06/09/2026, aucune decklist fournie par l'autrice) : un deck
de 15 cartes signature seules perd vite, structurellement, quel que soit le
pack. **Témoin dans la même fournée** : `--deck brawn` (même situation, aspect
retiré le 12/09/2026), **7/8 incidents** (parties bloquées) dans les mêmes
conditions — Wave (0/8) est donc, si quoi que ce soit, PLUS stable que ce
témoin sous cette configuration, pas moins. La mesure qui compte ici est la
stabilité (0 traceback), pas le score.

Statut au 22/09/2026 (nuit) : A-H fait, **les 16 cartes du pack ont chacune
un cas réel vert dans `tools/test_capacites.py`**, avec substitution prouvée
sur la règle moteur la plus risquée (purge de fin de phase) et témoin
d'épuisement sur l'unique limite « Max 1 per round » du pack (Ocean's Fury).
Six bugs réels trouvés et corrigés en écrivant ces cas, aucun n'aurait été
visible par le chargement statique seul — exactement l'avertissement du §9
de PROCESSUS-CARTE.md. G (gabarits PROCESSUS-CARTE × 16) fait, détail complet
dans `.planning/todos/2026-09-22-wave-gabarits-processus-carte.md`. Les
étapes 8 (autoplay) et 8 bis (test plateau) sont faites.

**Étape I (images) — FAIT le 22/09/2026.** Les 3 scans manquants
(65001a Wave, 65001b Pearl Pangan, 65015 Triumph Probation) étaient dans le
zip `Wave (Pearl Pangan)-20260922T153452Z-1-001.zip` déposé par l'autrice sur
le Bureau : `Wave.png`, `Pangan.png` et `Nemesis/Probation.png`, tous les
trois 1500×2150, texte vérifié identique aux scripts déjà écrits. Convertis
en 300×434 JPEG et posés dans `assets/pics/` (16/16 cartes du pack ont
maintenant leur image). Les 16 sous-dossiers `HeroCards`/`Nemesis` du Drive
partagé étaient vides au moment de la recherche (contenu déplacé ou jamais
synchronisé côté Drive) : c'est le zip, pas Drive, qui a fourni les 3
derniers scans.

**Quatre réserves nommées refermées le 22/09/2026 (20/20 cas verts,
16 nominaux + 4 témoins)** — détail complet dans le fichier de gabarits :
témoin d'épuisement pour 65001b (« Limit once per phase ») et 65010
(« max 2 »), témoin d'isolation temporelle pour 65011 (« premier événement
du tour seulement » — a débusqué un bug de MISE EN PLACE du témoin lui-même,
pas de la carte : `ne_pas_depenser` indispensable), branche « SIRENA
minions » isolée pour 65013, et étape 8 bis dédiée pour 65015
(`triumph-probation-cartes-dessous.test.ts`, 4/4 verts).

**Correction, même jour : la substitution formelle N'ÉTAIT PAS
optionnelle.** Signalé par l'utilisateur (« tu dis preuve fonctionnelle,
le MD dit obligatoire ») — relecture de l'étape 7 de `PROCESSUS-CARTE.md` :
« Preuve par substitution, obligatoire » et « Aucune carte n'est terminée
tant qu'il reste une capacité sans preuve par substitution » ne souffrent
aucune exception pour les cartes sans bug déjà trouvé. Refait au complet
via `tools/substituer_pack.py .game-src-par9 <port> 650` (procédure sûre
pour pack non commité : sauvegarde + empreinte md5 avant/après) :
**16/16 cartes ont désormais au moins un cas qui tombe réellement au rouge
sans son module**. Deux incidents pendant l'opération, tous deux corrigés
et re-vérifiés :
  - Deux exécutions au premier plan tuées par un timeout ont laissé deux
    modules stubbés (`65006.py`, `65001b.py`) — restaurés depuis la
    sauvegarde prise en tout début d'opération, diff confirmé identique.
    Toute exécution ultérieure de `substituer_pack.py` doit tourner en
    tâche de fond suivie, jamais au premier plan sous un timeout court.
  - **La substitution a débusqué un vrai bug (#5)** sur 65013 : les deux
    cas passaient au vert AVEC ET SANS le module (`Puzzle.Attack('01094')`
    fait attaquer Rhino, pas l'inverse — la restriction n'était jamais
    exercée). Corrigé, repassé en substitution : rouge sans module, vert
    avec.

**13 des 16 cartes cochent maintenant « OUI » sans réserve restante.** Les
3 qui restent « NON » ont chacune une réserve précise et mineure, sans
rapport avec la substitution (désormais faite partout) : 65008 (cible du
soin non re-vérifiée sur scan haute résolution), 65011 (étape 8 bis
probablement sans objet mais non vérifiée), 65012 (Boost non testé, limite
de harnais connue). Détail complet dans le fichier de gabarits.

## Les 3 dernières réserves fermées — 23/09/2026

- **65008 Pearl's Lolo** : scan haute résolution revérifié
  (`Wave (Pearl Pangan)-20260922T153452Z-1-001.zip`,
  `HeroCards/13_lolo.png`). Le texte imprimé est bien « heal 3 damage. »,
  sans aucun qualificatif de cible — rien n'était caché sur le scan basse
  résolution. La lecture « any character », déjà retenue par analogie
  avec `av001b` Flash Thompson, est confirmée comme le choix le plus
  fidèle sur une carte dont le texte est simplement moins précis que son
  modèle.
- **65011 Alontech's Greatest Achievement** : étape 8 bis vérifiée SANS
  OBJET. Relecture complète du script : ses trois capacités (hausse de
  coût, marquage interne, remise à zéro) ne touchent que des variables
  Python internes, jamais une zone, un compteur ou un statut visible. Rien
  à tester en rendu plateau pour cette carte précisément — fermée par
  constat.
- **65012 The Reyna Sirena** : la « limite de harnais » supposée
  (`Puzzle.Boost` incompatible avec `WhenCardBecomeBoost`) était une
  fausse piste — précédent retrouvé et confirmé ailleurs dans le dépôt
  (`ho015` Kingpin, `jj019` Purple Man, tous deux des sbires avec capacité
  Boost testés avec succès via `Puzzle.Boost`). Cas ajouté dans
  `test_capacites.py` (« 65012 The Reyna Sirena — Boost : le joueur est
  etourdi »), preuve par substitution FORMELLE faite (rouge sans le
  `Faces.GiveStatus`, vert avec, restauré et reconfirmé).

**Suite complète relancée après les trois fermetures : 21/21 cas verts**
(`test_capacites.py`, filtre `"650"`). **Autoplay reconfirmé** :
`tools/autoplay.py .game-src-par8 --deck wave --vilains rhino --difficultes
normal --profils equilibre --parties 8` → 8/8 parties, 0 incident (colonne
« ! » du rapport). Aucun script de carte n'a été modifié pour fermer ces
trois réserves (seul `test_capacites.py` a gagné un cas) : `git status`
confirme `Fusion/marvel-lcg-src/src/cards/pack/wave/` intact.

**Statut final : 16/16 cartes du pack Wave terminées « OUI » sans réserve
restante, au sens strict de PROCESSUS-CARTE.md.**
