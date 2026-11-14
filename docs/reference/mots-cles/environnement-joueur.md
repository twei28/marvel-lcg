# Environnement de joueur (PLAYER ENVIRONMENT) et trait PLANET

**Texte imprimé / définition** : pack maison Silver Surfer (3ᵉ version, ni le `sv`
officiel ni le « Silver Surfer (Neptune) » déjà en file d'attente), reçu par
images le 04/11/2026.
- Type de carte imprimé **« PLAYER ENVIRONMENT »**, trait **PLANET** sur les 5
  cartes du « planet deck » (Zenn-La, Sakaar, Newhaven, Xandar, Ego) + 1 carte
  du deck de héros (Black Hole, Singularity).
- Chaque carte PLANET porte un effet **Arrive** et/ou **Depart** : « Arrive :
  <effet sur le personnage arrivant> », « Depart : <effet sur le personnage
  partant> ».
- Règle de clarification donnée par l'auteur (hors carte, message du
  04/11/2026) :
  > Characters at a PLANET cannot attack or defend and lose guard / patrol.
  > There are a few ways to send enemies to planets and it can be very
  > beneficial. Enemies do not gain the arrive and depart bonuses to
  > planets.
- Carte Silver Surfer (face Héros) : « Characters at a PLANET cannot attack or
  scheme and lose guard and patrol. » (texte imprimé, légèrement différent de
  la clarification : scheme au lieu de defend — à vérifier carte par carte,
  cf. piège ci-dessous) + capacité **Surf — Action : I depart a PLANET.**
- Mise en place propre à ce héros (note de l'auteur) : Silver Surfer et son
  Cosmic Surfboard commencent en jeu ; le planet deck est mélangé et mis de
  côté face cachée ; l'allié lié Ego the Living Planet est mis de côté.

**Mécanisme moteur** : **à créer en totalité**, aucun équivalent exact dans le
dépôt au 04/11/2026. Ce qui s'en rapproche le plus, sans la couvrir :
- `lieu.md` / `territoire.md` (Punisher MC×DC 2026) : seule mention connue
  d'un trait **PLANET** dans le dépôt, mais ce sont des environnements
  d'ÉTAPE DE VILAIN (Skrull Empire, `skrull_menace/skrull_empire/sk086.py`
  à `sk097.py`) — aucun déplacement de personnage, juste un texte imprimé
  rendu vierge. Aucun rapport mécanique avec ce pack-ci.
- `horde-metazombies.md` : `player.additional_deck`, un deck tiers PAR
  JOUEUR distinct de la main/deck/défausse — candidat pour le « planet
  deck » lui-même (mélangé, mis de côté, révélé par l'action du Cosmic
  Surfboard).
- `World.CreateGameArea()` / `GameArea.AddPlayer()` / `GameArea.AddCard()`
  (cité par `territoire.md`) : modèle le plus proche d'une « poche » de jeu
  séparée où ranger les personnages « à la planète », mais conçu pour des
  zones de COMBAT (Kang, Civil War), pas pour une carte-zone individuelle
  que le joueur choisit librement.
- `PlaceCardHere` / `AttachTo` (modèle `su001b` Master Planner, cité par
  PROCESSUS-CARTE §8 bis) : alternative plus légère — le personnage glisse
  SOUS la carte PLANET comme une pièce attachée, au lieu d'une vraie zone de
  jeu. Risque déjà documenté : une carte glissée à deux étages peut devenir
  invisible au plateau (`enUnites`) si l'affichage n'est pas adapté.

**Ce qu'il faut concevoir avant la première carte** (liste, pas encore
tranchée) :
1. Où vit une carte PLANET une fois « en jeu » : une zone par JOUEUR (Black
   Hole est dans le deck de héros, donc personnelle) ou une zone PARTAGÉE
   (plusieurs joueurs pourraient envoyer leurs personnages à la même
   planète, cf. Black Hole : « choose a player », « the villain and each
   minion engaged with that player arrive here »ippery — un seul exemplaire
   de Black Hole peut donc accueillir le vilain ET des sbires).
2. Comment un personnage « à une planète » reste un personnage normal
   (dégâts, PV, capacités) tout en étant exclu de l'attaque/défense/
   engagement/manigance normaux, et retrouve son état en departant.
3. Comment une Response/Interrupt du type « After <X> arrives/departs a
   PLANET » (Nova Frankie Raye, Cosmic Blast, Lightspeed Entrance, Tactical
   Navigation, Ride Along) s'accroche à un message moteur dédié — aucun
   équivalent `AfterUnitArrive`/`AfterUnitDepart` n'existe.
4. L'ennemi (minion/vilain) envoyé à une planète NE déclenche PAS les bonus
   d'arrivée/départ réservés aux personnages du joueur (clarification de
   l'auteur) : le crochet doit distinguer le camp du personnage qui arrive.

**Carte exemple** : aucune encore scriptée — pack en phase de lecture/
conception (04/11/2026).

**Pièges connus** :
- Texte de la carte Héros (« cannot attack or **scheme**... ») contre
  clarification de l'auteur (« cannot attack or **defend**... ») : à poser
  comme question carte par carte au moment du script de `sv0XX` (la carte
  Héros) plutôt que trancher ici (règle « en cas de doute », PROCESSUS-CARTE
  §3).
- Confondre le trait PLANET de ce pack avec celui, homonyme, de Skrull
  Empire (`lieu.md`) : aucun rapport, deux mécaniques distinctes.
- « Ego engages Silver Surfer » (planet deck 5/5) : Ego est un `Minion` qui,
  une fois révélé DANS le planet deck, doit s'engager normalement contre le
  joueur — donc Ego vit À LA FOIS comme carte du planet deck (zone hors
  jeu) ET comme sbire normal une fois révélé : vérifier à quel moment il
  quitte la zone « planet deck » pour la zone de jeu normale.
- « Ego the Living Planet » (allié lié, Linked) : mis de côté au Setup,
  entre en jeu seulement quand Ego (le minion) est vaincu — modèle
  `Linked` déjà couvert par `linked.md`, mais le déclencheur « vaincu dans
  le planet deck » doit être vérifié contre ce mot-clé.

**Variantes maison** : brique neuve, à concevoir avec l'utilisateur avant
d'écrire la première ligne de script (voir §9 de `PROCESSUS-CARTE.md`, « en
cas de doute, demander » — mécanique maison non couverte par le moteur).

## Conception retenue (04/11/2026, après investigation moteur)

Décisions utilisateur : « lose guard and patrol » ne concerne que les
ennemis envoyés à une planète (Garde/Patrouille sont des capacités réservées
aux sbires dans le moteur, aucun allié/héros n'en a) ; un ennemi envoyé à une
planète reste engagé mais inerte (pas de nouveau code d'engagement).

**Prefixe** : `pc` (set 253, `tools/prefixes_fanmade.json`), pack
`silver_surfer_power_cosmic`.

⚠ **Correction d'une fausse piste** (investigation initiale par agent,
corrigée en relisant `src/game/deck/deck_type.py` soi-même) : `PlaceCardArea`
(mécanisme `PlaceCardHere`, modèle `su001b` Master Planner) porte
`is_out_of_play = True` et **PAS** `is_in_play = True` — une carte posée là
est donc HORS JEU au sens du moteur (`Card.IsOnField()` lit
`area.flags.is_in_play`). **Inadapté** pour un personnage vivant (PV,
dégâts, capacités) qu'on veut garder pleinement fonctionnel pendant son
séjour à une planète (Ego « each character here takes damage equal to my
ATK », Black Hole « take 3 damage », Zenn-La « Heal the arriving character
2 » exigent tous un personnage bel et bien EN JEU). Toujours vérifier les
flags dans `deck_type.py` directement, jamais sur la seule foi d'un rapport
d'agent.

**Mécanisme retenu, deux zones neuves, toutes deux `is_in_play = True`** :
1. **La carte PLANET elle-même** : pas de nouvelle `DeckType` — réemploi de
   `DeckType.EnvironmentArea` (déjà `is_in_play=True, is_face_up=True`,
   normalement lié au MONDE pour les environnements de manigance) mais
   instancié PAR JOUEUR : `Deck2(joueur, DeckType.EnvironmentArea, CardFace)`,
   mis en cache paresseux sur l'objet `Player` (modèle `HordeDeck` de
   `the_hunger_core/commun.py`, qui fait déjà exactement ça pour un deck tiers
   non prévu nativement par `Player`).
2. **Les personnages « à » une planète donnée** : nouvelle `DeckType`
   `PlanetGuestsArea` (`is_in_play=True, is_face_up=True`, calquée sur
   `UpgradesArea`/`AlliesArea`), instanciée PAR CARTE PLANET EN JEU (pas par
   joueur ni par monde) : `Deck2(planete.card, DeckType.PlanetGuestsArea,
   CardFace)`, mise en cache paresseuse sur l'objet `Card` de la planète. Un
   personnage qui y est déplacé (`Faces.MoveAllTo`) sort mécaniquement de
   `player.allies`/`area_hero`/zone d'engagement d'origine — donc déjà hors
   des listes d'attaque/manigance/défense normales — tout en restant
   `IsOnField()==True`.
3. **Le planet deck personnel** : `DeckType.AdditionalDeck` (déjà
   `is_out_of_play=True, is_set_aside=True` : convient tel quel pour un paquet
   mélangé et mis de côté), instancié PAR JOUEUR, modèle `HordeDeck` encore
   (pas `player.additional_deck` tout court, pour éviter toute collision avec
   un autre mécanisme qui s'en servirait).
4. **Retour au départ (Depart)** : retenir la zone d'origine du personnage
   AVANT de le déplacer (`personnage.card.area`), pour le restituer telle
   quelle (`area_hero` pour le héros, `player.allies` pour un allié, zone
   d'engagement pour un ennemi) plutôt que de deviner.

**Déjà posé côté moteur (04/11/2026)**, testé seulement par import Python, PAS
encore par le harnais `test_capacites.py` (aucune preuve de partie réelle à
ce stade, à faire avant la première carte « terminée ») :
- `src/game/message/sender/sender_player.py` : `AfterCharacterArrivePlanet`,
  `AfterCharacterDepartPlanet` (modèle exact `AfterPlayerResolveFlow`).
- `src/game/ability/factory/setup.py` : fabriques miroirs
  `AbilityFactory.AfterCharacterArrivePlanet` / `...DepartPlanet`.

## Revirement du 05/11/2026 : pas de nouvelle carte d'état générique

Correctif après une fausse route (une carte d'état maison « At Planet »,
calquée sur Stunned/Confused, avait été posée dans le moteur ET retirée le
jour même) : « Characters at a PLANET cannot attack or scheme... » est
**le texte imprimé sur la carte Silver Surfer elle-même** (`pc001a`), pas
une règle générale du jeu. Pas besoin d'un mécanisme moteur générique
attaché à chaque personnage : une seule capacité passive sur la carte
Héros, qui lit le marqueur « sur quelle planète » (déjà prévu, voir plus
bas) pour n'importe quel personnage, ami ou ennemi, suffit. Décision
utilisateur du 05/11 (voir `archives/travail-heros-termines/import-silver-surfer-power-cosmic/
QUESTIONS-AUTEUR.md`, Q1) : blocage attaque + manigance SEULEMENT, texte
imprimé suivi à la lettre — pas de blocage de la défense (une clarification
hors-carte le suggérait, mais le texte imprimé n'en parle pas).

## Revirement du 04/11/2026 (soir) : PAS de déplacement de carte, un marqueur

Décision utilisateur, après avoir fait remarquer que déplacer la carte
HÉROS elle-même est risqué (trop de mécanismes du moteur supposent qu'elle
reste en `area_hero` : jouer des cartes, flip Héros/Alter-Ego, l'action Surf
imprimée dessus). Plutôt que de traiter le Héros à part, décision : **aucune
carte ne bouge jamais, ni le Héros ni les alliés ni un ennemi.** « Être à une
planète » devient un simple MARQUEUR posé sur la carte (quelle planète,
quel `CardFace`), pas un déplacement de zone.

Conséquence : la partie « gratuite » de l'ancien plan (sortir des listes
d'attaque/manigance en sortant physiquement de `player.allies`/`area_hero`)
disparaît. Il faut maintenant trouver et modifier, un par un, les VRAIS
points du moteur qui dressent la liste des personnages pouvant
attaquer/manigancer/défendre/être engagés, et leur ajouter le filtre
« sauf si marqué à une planète ». C'est plus de fichiers moteur touchés que
le plan précédent, mais zéro risque sur le Héros ou l'affichage plateau.

## État au 05/11/2026 (soir) : première carte prouvée en jeu réel

`pc001a`/`pc001b` (identité Héros/Alter-Ego) écrites, compilées, et
**prouvées par `test_capacites`** (pas seulement lues) :
- `tools/test_capacites.py`, pack « pc » : 2 cas (blocage + témoin sans
  marqueur), tous deux VERTS avec le code en place.
- **Preuve par substitution faite** : le bloc `AbilitésBlocagePlanet()`
  retiré de `pc001a.py` → le cas de blocage devient ROUGE (Rhino encaisse 1
  dégât au lieu de 0) ; remis → vert à nouveau.
- **Diagnostic calibré AVANT de juger** : un premier jet attendait que
  Silver Surfer reste PRÊT après une attaque bloquée. Vérifié contre le
  Stunned **officiel** du moteur (`Puzzle.AddStatus('pc001a', 'Stunned')` +
  attaque) : lui aussi laisse l'attaquant ÉPUISÉ après une attaque empêchée
  — le coût (l'inclinaison) est payé AVANT que `ForcedInterrupt`+
  `SetBeInstead` n'intervienne. Attente corrigée en conséquence (ne vérifier
  que les dégâts, pas l'inclinaison) : c'est le comportement normal du
  moteur, pas un défaut de ce pack.

**Mécanisme final retenu** (voir `src/cards/pack/silver_surfer_power_cosmic/
__init__.py`) :
- `EstÀUnePlanète(personnage)` : lit un simple attribut Python
  (`personnage.card.pc_planete_actuelle`), pas de nouvelle zone/`DeckType`.
- `ArriverA`/`Departir` : posent/retirent ce marqueur et envoient les
  messages `AfterCharacterArrivePlanet`/`AfterCharacterDepartPlanet`.
- `AbilitésBlocagePlanet()` : capacité PARTAGÉE entre `pc001a.py` et
  `pc001b.py` (texte imprimé identique sur les deux faces) — bloque
  attaque et manigance de N'IMPORTE QUEL personnage marqué (`CardFinder()`
  large, pas seulement Silver Surfer : Black Hole pourra y envoyer le
  méchant/des sbires), via `AbilityType.ForcedInterrupt` + `SetBeInstead`
  (modèle `sk185`/`sk283`, skrull_menace). PAS de blocage de la défense
  (décision utilisateur du 05/11, texte imprimé suivi à la lettre).
- `Puzzle.ArriveAtPlanet(card, planet_card)` ajouté à `puzzle.py` : outil de
  test uniquement, appelle `ArriverA` directement (modèle `AddStatus`).

**Affichage plateau (étape 8 bis PROCESSUS-CARTE)** : décision utilisateur
04/11/2026 — pas de jeton, juste une infobulle (tooltip) au survol du
personnage marqué, qui affiche le nom ET l'image de la carte PLANET. **PAS
ENCORE FAIT** côté `ui-app/` : reste à faire avant de considérer `pc001a`/
`pc001b` complètement terminées (gate PROCESSUS-CARTE §8 bis).

**Reste à faire pour le pack entier** : les ~28 autres cartes (Cosmic
Surfboard, planet deck, nemesis, etc.), chacune selon `PROCESSUS-CARTE.md`
en entier.

## État au 05/11/2026 (nuit) : pc002 Cosmic Surfboard + pc003 Zenn-La

Trois cartes de plus écrites, compilées, et **prouvées en jeu réel** (10 cas
`test_capacites` verts au total pour `pc`, preuve par substitution faite
pour chacune) :
- `pc002` Cosmic Surfboard : entrée en jeu au Setup (native, `desc.Setup`,
  dans `player_deck` via `hero_deck`), Forced Interrupt fin de round (tous
  les ennemis à une planète partent), Action « choisir une PLANET → Silver
  Surfer y arrive » (`.SetTarget(card_type=Support, trait="PLANET")`).
- `pc003` Zenn-La : Arrive (soigne 2), Depart (+1 au PROCHAIN pouvoir de
  base, `WhenUnitUseBasicPower` + `RegisterTemp(unregister_after_exec=True)`
  — témoin d'épuisement fait : une 2e attaque après la 1re ne garde pas le
  bonus).
- **Piège trouvé et corrigé** : Zenn-La porte `desc.Setup` (texte imprimé),
  mais ne vit JAMAIS dans `player.player_deck` (elle vit dans le planet deck
  personnel, hors deck) — le scan natif des cartes Setup (`world.py:596-607`)
  ne l'aurait donc JAMAIS trouvée. Posée explicitement par
  `AbilityFactory.SetupPutIntoPlay(["pc003"])` sur pc001b (Alter-Ego), modèle
  des cartes « mises de côté par le héros lui-même » (PROCESSUS-HEROS étape
  3). Cosmic Surfboard, lui, est dans `hero_deck` → `player_deck`, donc son
  propre `desc.Setup` natif suffit, pas de code en plus.
- Nouveaux outils de test ajoutés à `puzzle.py` (test uniquement, pas des
  cartes) : `Puzzle.ArriveAtPlanet(carte, planète)`,
  `Puzzle.DepartFromPlanet(carte)`.

**Reste explicitement incomplet** : « Shuffle the planet deck and set it
aside facedown » (Sakaar, Newhaven, Xandar, Ego — ces 4 cartes n'existent
pas encore, donc rien à mélanger) ; affichage plateau (tooltip, étape 8 bis)
toujours pas fait pour aucune carte du pack.
