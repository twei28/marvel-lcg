# Pack Howard the Duck — fiches PROCESSUS-CARTE.md, une par card_id

Gabarit suivi : `PROCESSUS-HEROS.md` / `PROCESSUS-CARTE.md`. **28 card_id** au
total (`hd001a` à `hd027`, la face `a`/`b` de Howard comptant pour deux
identifiants distincts). Source : pack fan-made **RyCoRan** (« Marvel Champions
Custom Project », zip `Howard the Duck (05-23 Final)`) — 2 faces héros,
15 cartes signature + 1 permanente Setup, 3 ressources re-skinnées, 1 obligation
et 6 cartes némésis. Set 128, préfixe `hd`. Personnage : Howard, canard
anthropomorphe de Duckworld échoué à Cleveland.

Les étapes 1 et 3-6 de PROCESSUS-HEROS (cards.json, deck de départ, nemesis
json, sets_info.json, préfixe déclaré, traits DUCK/ELDER/VAMPIRE ajoutés au
moteur, images) ont été faites lors d'une session antérieure et validées par
l'utilisateur. Cette session a couvert l'étape 2 (scripts) et les étapes 7 à 10
(biographie, texte FR, validation carte par carte, autoplay, gate finale).

## Mécanique centrale

Howard tourne autour des **manigances annexes**. Il joue lui-même ses trois
manigances-joueur (`hd010` Trapped, `hd011` In a World, `hd012` He Never Made,
toutes `Victory: "0"`), les vainc, et une fois dans la **zone de victoire**
elles lui donnent un bonus permanent (+1 ATQ / +1 DEF / +1 CTR).

**Deux portées différentes**, à ne jamais confondre (piège `each` du tableau de
PROCESSUS-CARTE, documenté en tête de
`src/cards/pack/howard_the_duck/howard_the_duck/__init__.py`) :

| Texte imprimé | Portée | Aide |
|---|---|---|
| « for each **side scheme** in the victory display » (`hd005`/`hd006`, `hd007`/`hd008`) | TOUTES les manigances annexes, y compris celles du vilain | `NombreDeManigancesEnVictoire` |
| « for each **Howard the Duck** side scheme in the victory display » (`hd002`) | ses trois manigances-joueur seulement (`set_name` « Howard the Duck », distinct de « Howard the Duck Nemesis ») | `NombreDeManigancesHowardEnVictoire` |

Lecture confirmée par `hd021` (Waddle it Be?), qui remélange « all Howard the
Duck side schemes » de la zone de victoire **dans votre deck** : seules des
cartes joueur peuvent y aller.

Modèle officiel de tout le bloc : le pack **Cable** (`next_evol/cable`), même
archétype — `40003`/`40004`/`40005`/`40011` pour le décompte
(`Worlds.VictoryDisplay(effect).FindCardSize(CardFinder(card_type=SchemeSide2))`)
et `40006` Technovirus Purge pour le bonus permanent accordé depuis la zone de
victoire (`works_in_the_victory_display=True`).

## Cinq arbitrages tranchés par l'utilisateur le 30/08/2026 (documentés, non rediscutés)

1. **Icônes némésis** : `hd022` Duck and Cover! porte **Hazard** (carte penchée
   nue) ; `hd026` A Fowl Plot porte **Acceleration** (pointe + barre de
   soulignement). Vérifié par découpe d'image côte à côte, avec `ag011` comme
   témoin. Encadré ajouté dans `docs/reference/mots-cles/hazard.md` et
   `acceleration.md`. Les deux sont des mots-clés automatiques lus dans `desc` :
   aucun code.
2. **`hd024` Hellcow** = sbire némésis **alternatif**, à utiliser **à la place**
   du Collector (`hd023`) quand on affronte le scénario du Collector — celui-ci
   est un vilain officiel du pack `gmw` (cartes 16070-16081), il ne peut pas
   être des deux côtés de la table. Hellcow existe donc dans le jeu, est
   scriptée et testée, mais reste **hors du `nemesis_set`** standard (5 cartes :
   hd022, hd023, hd025, hd026, hd027).
3. **Manigances-joueur** (`hd010`, `hd011`, `hd012`) : case de coût **vide** sur
   le scan, **coût 1** tranché par l'utilisateur.
4. **Aspect Justice** pour le deck de départ (aucune decklist fournie par
   l'auteur). Voir `metadata.aspect_note` de `deck/starter/howard_the_duck.json`.
5. **Ressources `hd018`/`hd019`/`hd020`** : re-skins cosmétiques exacts des
   ressources basiques officielles, encodés en `full_link` vers `01088`/`01089`/
   `01090`. Aucun script (le `full_link` clone les règles).

## Deux choix tranchés par Claude, faute d'interlocuteur (session en arrière-plan)

1. **`hd027` Duck Hunt, branche identité civile** : « divide and place threat
   from this activation among them instead ». Le pipeline de manigance du moteur
   n'accepte **qu'une seule** manigance cible
   (`Message.GettingEnemySchemeTarget`, `can_scheme.py:68-72`) : impossible d'y
   répartir la menace. Rendu retenu : une interruption **temporaire**
   `WhenSchemeWouldPlaceThreat(MainScheme)` enregistrée juste avant l'activation
   (modèle exact `aos/nick_fury/50035b.py` Stealth), qui annule le placement sur
   le complot principal puis répartit la menace **point par point** entre les
   manigances annexes via un `ChooseAbilities` répété (modèle `ok008` Spear
   Thrust, qui divise déjà ses dégâts ainsi). C'est le joueur visé qui répartit.
2. **`hd009` Quack and Burn, seconde cible** : le couple `SetTarget` +
   `SetTarget2` (modèle `il009` Vision AI) a été **écarté après essai**. Il
   fonctionne quand les deux cibles sont résolues automatiquement, mais le
   pilote générique de `test_capacites` ne renvoie qu'une liste de cibles par
   question : `effect.targets2` restait vide et la moitié « retrait de menace »
   n'était jamais exercée (cas rouge du 30/08/2026). La seconde cible passe donc
   par un `ChooseAbilities` imbriqué, qui pose une question distincte et reste
   testable.

## Outils exécutés depuis `.game-src`

- `tools/test_cards.py` : **4613 ok / 0 err** (25 modules `hd*` ajoutés ;
  référence avant ce pack : 4588 ok pour scarlet_spider, aucune régression).
- `tools/verifier_prefixes.py` : OK — 5168 cartes, 26 préfixes déclarés,
  834 cartes fan-made, **aucun doublon, aucun préfixe non déclaré, aucun numéro
  emprunté**.
- `tools/verifier_coherence_cartes.py` : **0 carte joueur sans classe d'aspect,
  0 obligation sans destinataire, 0 image manquante** pour `howard_the_duck`.
  Aucune collision de nom impliquant Howard n'apparaît dans le rapport — mais
  une collision réelle existe et a été traitée : « **Collector** » (`hd023`)
  porte le même nom que le vilain officiel `gmw` 16070-16081. C'est une
  collision **de noms**, jamais de `card_id`, et **aucun script du pack ne
  cherche « Collector » par son nom** : aucune conséquence technique. C'est
  aussi la raison d'être de `hd024` Hellcow (arbitrage n°2).
- Deck de départ (`tools/verifier_tous_les_decks.py`, `DECK_NOM=howard_the_duck`) :
  partie montée avec succès, identité `hd001a`, main 5, deck restant 32, et
  `hd017` **bien en jeu dès la mise en place** (journal : « Nexus of all
  Realities entered play » puis « Howard Duckson equipped Nexus of all
  Realities »).
- Script anti-fuite « jamais une carte signature d'un autre héros dans un deck »
  (PROCESSUS-HEROS §10) : **0 résultat**, sur les 93 decks de départ du dépôt,
  `howard_the_duck` inclus.
- `tools/test_capacites.py` : **30 cas dédiés au pack `howard_the_duck`,
  30/30 verts** (indices 531-560). Un cas par capacité distincte, un cas partagé
  pour chaque lot de cartes physiquement dupliquées (Mallard Magic x2, Quack
  Attack x2, Fowl Play x2), et deux cas pour chaque carte à branche « if you
  cannot » (hd023, hd025, hd027).
- `tools/autoplay.py` : **8 parties contre `rhino`, profil `equilibre`**.
  Grep exhaustif `NameError|AttributeError|TypeError|KeyError|AssertionError`
  sur les 8 journaux : **0 partout** ; grep élargi `traceback|exception` :
  **0 partout aussi**. 0/8 victoires, **7,1 rounds tenus en moyenne**,
  4 parties terminées par « All players were eliminated », 3 par « The Main
  Scheme was Completed », **1 bloquée** (analyse ci-dessous, aucune carte de
  Howard en cause).
  **Couverture des cartes du pack dans les journaux** : `hd001a` à `hd021`
  présentes dans **8/8** parties (sauf `hd004` et `hd008`, deuxièmes
  exemplaires, 7/8) ; les 5 cartes du set némésis (`hd022`, `hd023`, `hd025`,
  `hd026`, `hd027`) dans 1/8 (aléa du tirage) ; `hd024` Hellcow absente, ce qui
  est normal — elle est hors du `nemesis_set` (arbitrage n°2).
  **Témoin `okoye`** (héros déjà audité à 100 %, même scénario, même profil,
  8 parties) : 0/8 victoires, **0 bloquée**, 4,1 rounds tenus en moyenne, 6/8
  terminées par complot achevé et 2/8 par élimination, 0 traceback.
  **Lecture de l'écart** : Howard tient plus longtemps que le témoin
  (7,1 rounds contre 4,1) — Private Eye prévient de la menace à chaque round et
  le kit est très défensif — mais meurt plus souvent (4/8 éliminations contre
  2/8), ce qui colle à un héros ATQ 1 qui peine à tuer le vilain. Aucun de ces
  écarts n'est anormal.

  **La partie bloquée, analysée précisément** : le message est
  `Hero_Action(id=66, cibles_legales=[1], plage=[1, 1])`, et le journal montre
  six fois de suite
  `<E> (66) [(45,01093) Tenacity] (Hero Action) [01093] WhenPlayerInTurn failed`.
  `01093` **Tenacity est une carte Basic OFFICIELLE**, pas une carte de Howard :
  le pilote d'autoplay reproposait indéfiniment son Hero Action (« dépensez une
  ressource [physical] et défaussez cette carte → redressez votre héros »), qui
  échoue faute de ressource physique payable, sans que le plateau bouge — le
  garde-fou anti-boucle finit par déclarer la partie bloquée. **Le même
  phénomène apparaît chez le témoin** (`okoye`, partie 5, 2 occurrences de
  `Tenacity ... failed`), qui s'en est simplement sorti avant le seuil. C'est
  donc une faiblesse du pilote générique face à une carte officielle, aggravée
  par un deck Justice pauvre en ressources physiques — **aucune carte `hd*`
  n'est impliquée, et il n'y a aucun traceback**.

## Bugs réels trouvés et corrigés (preuve par substitution rouge/vert)

### 1. `hd017` n'entrait jamais en jeu : la mise en place manquait sur l'identité

**Symptôme** : le cas `hd017` restait rouge (« aucun événement en main : le
second Interrupt n'a rien cherché »), et `hd017` n'apparaissait **nulle part**
dans le journal de partie.

**Cause** : la carte comptait sur son seul `desc.Setup` et sur la clé
`set_aside` du deck de départ, ce qui ne suffit ni l'un ni l'autre.
- `World.GameSetup` ne met en jeu les cartes `Setup` qu'en parcourant
  `player_deck`, `set_aside_nemesis_sets`, les decks de rencontre et
  `world.additional_decks` (`world.py:531-539`) — jamais le set aside du joueur
  (`player.set_aside_deck` est un alias de `additional_discard_pile`,
  `player.py:100`).
- La clé `set_aside` d'un deck de départ est **purement documentaire** :
  `SceneLoader.NewScene` ne la lit pas (`loader.py:98-108` ne construit le
  `HeroDescriptor` qu'avec `hero`, `hero_deck`, `obligations`, `nemesis_set`,
  `player_deck`) ; seul le chemin « puzzle » s'en sert
  (`server_new_game.py:109/122`).

**Correctif retenu — la voie idiomatique du dépôt** : c'est l'IDENTITÉ qui met
la carte en jeu. `hd001b` (Howard Duckson) porte désormais
`AbilityFactory.SetupPutIntoPlay(["hd017"])`, qui génère la carte depuis son
`card_id` sans qu'elle ait besoin d'être dans un deck (`setup.py:6-31`). C'est
ce que font les 20 autres héros à `set_aside` non vide — Wolverine
(`35001b` → `"35002"`), Vision (`26001b` → `"26002a,26002b"`), Spider-Man Rainy
(`sr001b` → `"sr012"`), Storm, Doctor Strange... `hd017` reste donc **hors du
`hero_deck`** (15 cartes signature) et la clé `set_aside` du deck garde sa
valeur documentaire, avec un `metadata.setup_note` qui explique le mécanisme.

Une première correction, écartée : mettre `hd017` dans le `hero_deck` (16 cartes)
pour que `ProcessSetup` la trouve. Cela **fonctionne** (cas vert), mais s'écarte
des 20 précédents du dépôt et gonfle le deck signature d'une carte qui n'est
jamais tirée. Rejetée au profit de la voie majoritaire.

**Rouge/vert** : cas `hd017 Nexus of all Realities — Interrupt`, rouge avant
(aucun événement cherché, `hd017` absente du journal), vert après (l'allié
vaincu déclenche bien la recherche).

**Pas de bug ailleurs** : les 21 decks de départ à `set_aside` non vide ont été
passés au crible, aucun n'a de carte orpheline — `sr012` (Impact Webbing) sort
bien au setup grâce au `SetupPutIntoPlay` de `sr001b`. Une première rédaction de
ce document annonçait à tort un « défaut latent » sur `spider_man_rainy` :
affirmation fausse, retirée.

### 2. `hd026` A Fowl Plot — plantage moteur en défaussant une carte PERMANENTE

**Symptôme** : `AssertionError` en pleine partie, trois fois sur huit dans
l'autoplay (parties 1, 4 et 5) :

```
File ".../cards/pack/howard_the_duck/howard_the_duck_nemesis/hd026.py", line 42
    defaussees = Faces.DiscardAll([cible], effect)
File ".../game/card/face/card_face.py", line 473, in do_discard
    assert controller.is_eliminated
AssertionError
```

**Cause** : « Discard an upgrade you control » proposait `hd017` Nexus of all
Realities, amélioration **permanente**, donc incapable de quitter le jeu. Le
moteur garde-fou (`card_face.py:463-473`) n'autorise la défausse d'une carte
permanente que si son contrôleur est éliminé.

**Correctif** : filtre `CardFinder(canbe_discard=True)` sur
`GetControlCardsByType` (`checker.py:169-171` écarte exactement les cartes
permanentes et les identités). C'est aussi la règle : une carte permanente ne se
défausse pas, et la branche « If no cards were discarded this way » doit alors
s'appliquer. Même filtre ajouté par prudence sur `hd023` (« discard an ally or
support »), bien qu'aucun soutien permanent n'existe dans ce kit.

**Rouge/vert** : rouge = 3 tracebacks sur 8 parties d'autoplay, reproductibles ;
vert = 0 traceback sur 8 parties après correctif.

### 3. `hd009` Quack and Burn — la moitié « retrait de menace » ne partait jamais

**Symptôme** : cas rouge, « menace sur 01097b = 0 (attendu 3) ». Le journal
montrait `Quack and Burn activates, targets [Rhino]` — une seule liste de cibles.

**Cause** : `SetTarget2` n'est pas alimenté par le pilote générique du harnais,
et la clause `if effect.targets2` restait donc toujours fausse. Ce n'est pas
qu'une limite de test : un joueur humain aurait bien deux sélections, mais rien
ne le prouvait, et le montage restait fragile.

**Correctif** : la seconde cible passe par un `ChooseAbilities` imbriqué
(modèle `ok008`/`hd003`), qui pose une question distincte.

**Rouge/vert** : rouge avec `SetTarget2` (menace inchangée), vert après
(3 dégâts = ATQ imprimée de Man-Thing, et la menace baisse bien de 2 = CTR de
Howard).

### 4. Piège de nommage évité avant qu'il ne morde : le `*` d'unicité

`cards/paper.py:45-46` retire le préfixe `"* "` d'un nom unique
(`is_unique = name.startswith("* ")` puis `name = name.lstrip("* ")`). Un
`CardFinder(name="* Howard the Duck")` n'aurait **jamais** rien trouvé, en
silence — et quatre cartes du pack (`hd002`, `hd010`, `hd011`, `hd012`, `hd015`)
en dépendent. Constantes corrigées dans le `__init__.py` du set avant le premier
test.

## Trois limites du harnais, documentées et non masquées

1. **Interférence d'une carte d'aspect** : `01061` Great Responsibility (Justice,
   présente dans le deck de Howard) est elle aussi une interruption « quand une
   menace serait placée » — laissée en main, le pilote la joue et redirige TOUTE
   la menace en dégâts, ce qui faussait deux cas. Réglé en vidant la main
   (`main_exclusive`) et en posant la menace **après** ce vidage.
2. **Paiement à plusieurs sources** : le pilote générique ne compose pas un
   paiement quand la carte à financer coûte 2 et qu'aucune source ne couvre le
   montant à elle seule. Vérifié avec un **témoin officiel** (`40007`
   Graymalkin, posé à côté de l'Agence) : lui non plus n'était pas retenu. Le
   cas `hd014` vise donc un événement à coût 1 (`01086` First Aid), financé par
   la seule Agence — preuve par insuffisance sans ambiguïté.
3. **Défense automatique** : Howard a DEF 2 contre l'ATQ 2 de Rhino, il défend
   et ne subit rien, donc l'interruption de `hd005` n'avait aucune fenêtre. Le
   cas utilise une source de dégâts déterministe (`Puzzle.Damage`, 3 points) à
   la place.

---

### hd001a : Howard the Duck (face héros)

- [x] Étape 2 : cartes de référence :
      Private Eye → `bkw/08017.py` (Counterintelligence), même couple
      `AbilityFactory.WhenThreatWouldBePlacedOn(...)` + `message.PreventThreat`
      (deux écarts voulus par le texte : portée `None` = « a scheme », pas
      `MainScheme` ; valeur 1, pas 3).
      Response → `AbilityFactory.AfterCardEnterPlay(Response, SchemeSide2)`
      (fabrique de `ok002` Aneka / `bp/51014` Manifold) + `Faces.ReadyAll`
      (modèle `il015`/`ok014`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : **`a scheme`**
      (n'importe quelle manigance, `which_scheme=None`, pas seulement le complot
      principal) ; **`a side scheme`** (`SchemeSide2` = joueur ET rencontre) ;
      **Interrupt vs Response** (deux fabriques distinctes, pas un `if`) ;
      **`Limit once per round`** sur **les deux** capacités (`.LimitOncePerRound()`
      deux fois — piège « un second Interrupt/Response annoncé »). `Interrupt` nu
      et non `HeroInterrupt` : le texte n'écrit pas « Hero », et la face Héros
      n'est de toute façon en jeu qu'en forme héros. Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : HP 9, ATQ 1, CTR 2, DEF 2, MNG 5 (desc et
      carte identiques) ; « prevent 1 » → `PreventThreat(1, effect)`.
      Résultat : conforme.
- [x] Étape 7 : deux cas, un par capacité :
      - `hd001a Howard the Duck — Private Eye` : 3 menaces posées par
        `Puzzle.PlaceThreat` (qui passe bien par `PlaceThreatInternal`, donc par
        le message interrompu) → **2** réellement placées. Vert.
      - `hd001a Howard the Duck — Response` : Howard incliné, `hd025` mise en
        jeu (sans révéler, pour n'exercer que l'entrée en jeu) → Howard
        redressé. Vert du premier coup.
- [x] Étape 8 : autoplay ciblé : `hd001a` présente dans **8/8** parties,
      `Private_Eye` activé plusieurs fois par partie dans les journaux
      (jusqu'à 5 fois dans une seule partie), 0 traceback.

Carte terminée : OUI

### hd001b : Howard Duckson (face alter-ego)

- [x] Étape 2 : cartes de référence : **mise en place du pack** →
      `wolv/wolverine/35001b.py` (Logan) et `spider_man_rainy/sr001b.py`, même
      `AbilityFactory.SetupPutIntoPlay([<card_id>])` porté par l'identité pour
      mettre `hd017` en jeu à la mise en place (voir bug n°1) ;
      **Deducktive Reasoning** → `next_evol/cable/40004.py` (Precognition),
      même triplet `initiator.LookAtDeck("EncounterDeck", n, effect)` +
      `initiator.MayChooseFace(..., not_move=True)` +
      `initiator.PlaceOnTopInAnyOrder(...)`. Seule différence imprimée :
      Precognition **défausse** la carte choisie, Howard la met **sous** le deck
      → `Faces.MoveAllToDeck([choisie], deck, "Bottom", effect)` (modèle
      `msm/ms_marvel/05006.py` et `sm/mysterio/__init__.py`, les deux seuls
      usages du mode "Bottom" du dépôt).
- [x] Étape 5 : mots-pièges : **`the top 3 cards`** (nombre FIXE, contrairement à
      Precognition dont le nombre dépend de la zone de victoire) ; **`put 1 on
      the bottom`** (une seule, et au FOND, pas défaussée) ; **`the others back
      in any order`** (les 2 restantes remises sur le DESSUS) ; **`Limit once per
      round`**. Résultat : conforme.
- [x] Étape 6 : nombres : 3 regardées, 1 au fond, 2 remises ; HP 9, REC 3,
      MNG 6. Résultat : conforme.
- [x] Étape 7 : cas `hd001b Howard Duckson — Deducktive Reasoning` : `hd024`
      remontée sur le DESSUS du deck de rencontre (`Puzzle.PutIntoDeck`), le
      pilote prend toujours le premier item offert → vérification que `hd024`
      est bien **au fond** du deck de rencontre et plus sur le dessus. Vert du
      premier coup.
- [x] Étape 8 : `hd001b` présente dans **8/8** parties,
      `Deducktive_Reasoning` observé jusqu'à 2 fois par round d'identité
      civile, 0 traceback.

Carte terminée : OUI

### hd002 : Man-Thing (allié, coût 4)

- [x] Étape 2 : carte de référence : `phoenix/34021.py` (Storm) pour
      `AbilityFactory.ReduceCostToPlayThis(<fn>)` — la fonction rend le MONTANT
      de la réduction (`resources.py:586-637`).
- [x] Étape 5 : mots-pièges : **`Toughness`** = mot-clé automatique lu dans
      `desc.Toughness`, **aucun module** (base automatique explicitement listée
      par PROCESSUS-CARTE étape 5) ; **`for each Howard the Duck side scheme`**
      = portée RESTREINTE (`set_name="Howard the Duck"`), pas toutes les
      manigances annexes de la zone de victoire — c'est la moitié du piège
      `each` de ce pack ; **`Reduce the cost to play`** (réduction de coût, pas
      un gain de ressource). Résultat : conforme.
- [x] Étape 6 : nombres : coût 4, HP 5, ATQ `3**`, CTR `1*`, Toughness 1 ;
      réduction de 1 par manigance. Note : `3**` est parsé par le moteur en
      ATQ imprimée 3 + 2 dégâts conséquents (`can_attack.py:47-53`), encodage
      standard partagé par 12 alliés officiels. Résultat : conforme.
- [x] Étape 7 : cas `hd002 Man-Thing — coût réduit` : **preuve par
      insuffisance** (même technique que `il001b`) — trois Haymaker en main
      = 3 ressources EXACTEMENT, le coût imprimé 4 est impayable, seul le coût
      réduit à 3 (`hd010` envoyée en zone de victoire) rend Man-Thing jouable.
      Vert. La `Toughness` est prouvée indirectement par le cas `hd017`, où
      Man-Thing exige DEUX coups de dégâts pour être vaincu.
- [x] Étape 8 : `hd002` présente dans **8/8** parties, jouée et attaquant
      (3 dégâts constatés sur Rhino, 2 dégâts conséquents sur lui-même),
      0 traceback.

Carte terminée : OUI

### hd003, hd004 : Mallard Magic (2 exemplaires physiques, RES mental / énergie)

- [x] Étape 2 : cartes de référence : `ok019` Funeral Rites / `ok004` Adored
      Ones pour `initiator.ChooseAbilities` à 2 branches ;
      `core/spider_man/32008.py` (Steel Fist) pour
      `Faces.GiveStatus(targets, "Stunned"/"Confused", effect)` ; `ok008` Spear
      Thrust pour le `ChooseAbilities` imbriqué de la seconde cible.
- [x] Étape 5 : mots-pièges : **`Choose:`** = UNE seule ability `.SetPlay()`
      (obligatoire — `game/card/factory.py:95-121` n'accepte qu'un
      `play_count == 1` par événement hors liste blanche codée en dur, et un
      second `.SetPlay()` ferait planter la création de partie du héros) ;
      **`deal 5 damage to it`** = LA MÊME cible que le stun (piège `that <nom>`,
      un seul `SetTarget(Enemy)` réutilisé) ; **`Confuse an enemy AND remove 4
      threat from a scheme`** = deux cibles INDÉPENDANTES. Résultat : conforme.
- [x] Étape 6 : nombres : coût 3, 5 dégâts (branche 1), 4 menaces (branche 2).
      Résultat : conforme.
- [x] Étape 7 : cas `hd003 Mallard Magic — branche 1` (partagé pour les 2
      exemplaires, code identique) : Rhino sonné ET 5 dégâts constatés. Vert.
      **La branche 2 n'a pas de cas dédié** : le pilote générique prend toujours
      la première option d'un `ChooseAbilities` libre, même limite déjà
      documentée sur `il017`/`ok019`/`ss011`/`ss017`.
- [x] Étape 8 : `hd003` présente dans **8/8** parties, `hd004` dans 7/8,
      jouées (`Play:Event`), 0 traceback.

Carte terminée : OUI (les 2 exemplaires ; branche 2 non couverte par un cas
dédié, même limite que toute carte « Choose » à 2 branches libres du dépôt)

### hd005, hd006 : Quack Attack (2 exemplaires physiques, RES physique / énergie)

- [x] Étape 2 : cartes de référence : `next_evol/cable/40012.py` (Telekinetic
      Force Field) pour `AbilityFactory.WhenUnitWouldTakeDamage(HeroInterrupt,
      <qui>, ...)` + `message.PreventDamage(<n>, effect)` ;
      `next_evol/cable/40011.py` (Plasma Rifle) pour le décompte
      `Worlds.VictoryDisplay(...).FindCardSize(CardFinder(card_type=SchemeSide2))`.
- [x] Étape 5 : mots-pièges : **`When YOU would take damage`** = `"You"`
      (l'identité du joueur), pas tout `Friend` comme Force Field ;
      **`any amount of damage`** = aucun filtre supplémentaire (ni
      `is_from_attack`, ni `is_consequential_damage`) ; **`prevent 2 of that
      damage`** = 2, pas "All" ; **`for each side scheme in the victory
      display`** = portée LARGE (toutes les manigances annexes, celles du vilain
      comprises) — l'autre moitié du piège `each` de ce pack. La cible ennemie
      est choisie à la résolution et non par un `SetTarget` statique : à
      0 manigance en victoire il n'y a aucun dégât, donc aucune cible à demander.
      Résultat : conforme.
- [x] Étape 6 : nombres : coût 1, 2 dégâts prévenus, 1 dégât par manigance.
      Résultat : conforme.
- [x] Étape 7 : cas `hd005 Quack Attack — Hero Interrupt` (partagé pour les 2
      exemplaires, code identique) : source de dégâts déterministe
      (`Puzzle.Damage`, 3 points) → 3 - 2 prévenus = **1 dégât** encaissé, et la
      carte se retrouve en défausse (preuve qu'elle a bien été jouée en
      interruption). Vert. **La moitié « 1 dégât par manigance en victoire »
      n'est pas exercée par ce cas** (aucune manigance en zone de victoire au
      moment du déclenchement) : le décompte lui-même est le même appel que celui
      prouvé sur `hd002` et `hd007`.
- [x] Étape 8 : `hd005` et `hd006` présentes dans **8/8** parties, 0 traceback.

Carte terminée : OUI (les 2 exemplaires ; prévention prouvée en direct, moitié
« dégâts par manigance » prouvée par le même décompte sur d'autres cartes mais
pas dans ce cas précis)

### hd007, hd008 : Fowl Play (2 exemplaires physiques, RES mental / physique)

- [x] Étape 2 : cartes de référence : `cw/tigra/56009.py` (Feline Senses) et
      `ironheart/29005.py` (Fly Over) pour
      `RemoveThreatFromSchemes(..., if_this_remove_last_threat=<fn>)`, crochet
      dédié du moteur ; `ok014` Royal Protector pour `initiator.GetHero()` +
      `Faces.ReadyAll` ; `player_action.py:230` (`MayChooseOneAbility`) pour un
      choix OPTIONNEL à 2 branches.
- [x] Étape 5 : mots-pièges : **`If you defeat a SIDE scheme in this way`** —
      le crochet du moteur ne filtre pas le type de manigance, la restriction
      `SchemeSide2` est vérifiée à la main sur la cible ; **`you MAY ready your
      hero OR remove...`** = choix optionnel (`MayChooseOneAbility`, qui ajoute
      « Cancel »), pas un `ChooseAbilities` forcé comme une obligation ;
      **`ready your HERO`** = l'identité en forme héros (`GetHero()`), pas la
      carte jouée ; **`for each side scheme in the victory display`** = portée
      LARGE. Résultat : conforme.
- [x] Étape 6 : nombres : coût 2, 3 menaces retirées, 1 menace par manigance en
      victoire. Résultat : conforme.
- [x] Étape 7 : cas `hd007 Fowl Play` (partagé pour les 2 exemplaires, code
      identique) : `hd010` (3 menaces) mise en jeu, Howard **incliné avant**,
      Fowl Play jouée sur elle → `hd010` hors jeu ET Howard redressé (première
      option = « Ready your hero »). Le redressement prouve que la branche bonus
      a réellement tourné. Vert. **La seconde branche du bonus (retrait de
      menace) n'a pas de cas dédié**, même limite de pilote que ci-dessus.
- [x] Étape 8 : `hd007` présente dans **8/8** parties, `hd008` dans 7/8,
      0 traceback.

Carte terminée : OUI (les 2 exemplaires ; seconde branche du bonus non couverte
par un cas dédié)

### hd009 : Quack and Burn

- [x] Étape 2 : cartes de référence : `ok001b` Vanguard Leader / `ss001b` Spider
      Link pour `Search.PlayerCard(..., name=...)` + `initiator.GainCard` ;
      `next_evol/cable/40009.py` (Askani'son) pour la lecture
      `initiator.GetHero().thwart` ; `ss022` Forced Contract pour la leçon
      `printed_attack` (la valeur `.attack` d'une face qui n'est pas en jeu rend
      0) ; `ok008` Spear Thrust pour le `ChooseAbilities` imbriqué.
- [x] Étape 5 : mots-pièges : **`Man-Thing's ATK`** = valeur DYNAMIQUE, lue
      sur la carte (effective si Man-Thing est en jeu, imprimée sinon), jamais
      une constante 3 ; **`Howard the Duck's THW`** = la face HÉROS, stat
      calculée (fiable, elle n'est lue que quand cette face est active) ;
      **`Find Man-Thing`** = recherche par NOM (précédent `kb003` pour
      « Hawkeye ») ; **`and remove threat`** = coût/effet à plusieurs parties,
      aucune oubliée (piège `and remove`). Résultat : conforme.
- [x] Étape 6 : nombres : coût 2 ; dégâts = 3 (ATQ imprimée de Man-Thing) ;
      menace = 2 (CTR de Howard). Résultat : conforme.
- [x] Étape 7 : cas `hd009 Quack and Burn` : Man-Thing ajouté à la main depuis
      le deck, **3 dégâts** sur Rhino et menace du complot principal descendue
      de 2. Rouge avec `SetTarget2` (bug n°3 ci-dessus, menace inchangée), vert
      après restructuration. Note de lecture : la menace finale attendue est 2 et
      non 3, parce que les 5 menaces posées passent par `PlaceThreatInternal`,
      donc par Private Eye (`hd001a`, en jeu en forme héros) qui en prévient 1.
- [x] Étape 8 : `hd009` présente dans **8/8** parties, 0 traceback.

Carte terminée : OUI

### hd010 : Trapped (manigance annexe joueur, coût 1, Victory 0)

- [x] Étape 2 : cartes de référence : `next_evol/cable/40006.py` (Technovirus
      Purge) pour le bonus permanent depuis la zone de victoire
      (`GiveKeywordToInPlayWhenApplyThis(..., works_in_the_victory_display=True)`,
      garde-fou `environment_helper.py:85`) ; `jubilee/47003.py` (Shopping Spree)
      pour `WhenSchemeBeDefeated(WhenDefeated, "This", has_defeating_player=True)`
      + `Search.PlayerCard` ; `next_evol/cable/40002.py` (Bodyslide) pour
      `Players.ForEachPlayer`.
- [x] Étape 5 : mots-pièges : **`Victory 0`** = lu par le moteur dans
      `desc.Victory` (`has_victory.py:25`), aucun code ; **`EACH player may
      search ... and add it to their HAND`** vs **`THE PLAYER WHO DEFEATED this
      scheme, may put THAT ally into play`** = deux portées différentes dans la
      même capacité (piège `each` ET piège `that <nom>` : « that ally » est bien
      LA MÊME carte que celle que ce joueur vient d'ajouter, conservée par
      joueur) ; **`may`** deux fois = `Search.PlayerCard(may=True)` puis
      `MayChooseOneAbility`. Résultat : conforme.
- [x] Étape 6 : nombres : coût 1, menace de départ `3*`, Victory 0, +1 ATQ.
      Résultat : conforme.
- [x] Étape 7 : cas `hd010 Trapped — When Defeated` : la manigance est vaincue
      par une **vraie action de joueur** (`hd007` jouée), seul moyen d'avoir un
      `defeating_player` ; Man-Thing déposé en défausse → recherché, ajouté à la
      main, puis mis en jeu. Vert. Le bonus « +1 ATQ depuis la zone de victoire »
      est prouvé indirectement par le cas `hd002` (la réduction de coût ne
      s'applique que si `hd010` est bien arrivée en zone de victoire).
- [x] Étape 8 : `hd010` présente dans **8/8** parties, jouée puis déjouée,
      0 traceback.

Carte terminée : OUI

### hd011 : In a World (manigance annexe joueur, coût 1, Victory 0)

- [x] Étape 2 : cartes de référence : identiques à `hd010` ; plus
      `trors/04017.py` (Ready for Action) / `ok006` pour
      `Faces.GiveStatus(<faces>, "Tough", effect)` et `il002` Stature pour
      `this.HealthUnits([identite], 2, effect)`.
- [x] Étape 5 : mots-pièges : **`Give EACH PLAYER a tough status card`** = le
      statut se pose sur l'IDENTITÉ de chaque joueur (seule carte qui puisse le
      porter) ; **`THE PLAYER WHO DEFEATED this scheme, MAY heal 2`** = portée
      restreinte au seul vainqueur, et optionnelle. Résultat : conforme.
- [x] Étape 6 : nombres : coût 1, menace `3*`, Victory 0, +1 DEF, 2 dégâts
      soignés. Résultat : conforme.
- [x] Étape 7 : cas `hd011 In a World — When Defeated` : identité blessée de 3
      avant, `hd011` vaincue par `hd007` → identité **Tenace** ET dégâts
      ramenés à 1 (3 - 2). Les deux portées vérifiées d'un coup. Vert du premier
      coup.
- [x] Étape 8 : `hd011` présente dans **8/8** parties, 0 traceback.

Carte terminée : OUI

### hd012 : He Never Made (manigance annexe joueur, coût 1, Victory 0)

- [x] Étape 2 : cartes de référence : identiques à `hd010` ; plus `ok001b`/
      `kb002` pour `Faces.ShuffleAllTo(..., player.player_deck, effect)` et
      `ok006` pour le « up to 3 » (`range`).
- [x] Étape 5 : mots-pièges : **`up to 3 cards`** = `AskChooseFaces(..., (0, 3),
      forced=False)` ; **`add 1 of those cards to their hand INSTEAD`** = piège
      `instead` — la carte ne part PAS dans le deck puis en main, elle va en main
      AU LIEU d'aller dans le deck : elle est retirée de la liste **avant** le
      `ShuffleAllTo` ; **`those cards`** = les cartes que CE joueur vient de
      choisir (piège `that <nom>`), pas la défausse entière ; **`EACH player`**
      vs **`THE PLAYER WHO DEFEATED`** = deux portées. Résultat : conforme.
- [x] Étape 6 : nombres : coût 1, menace `3*`, Victory 0, +1 CTR, jusqu'à 3
      cartes, 1 gardée. Résultat : conforme.
- [x] Étape 7 : cas `hd012 He Never Made — When Defeated` : défausse semée de
      3 cartes connues (`01051`, `01088`, `01089`), `accepter_choix` force le
      pilote à prendre le MAXIMUM (sans cette clé un choix « up to 3 » se résout
      à 0 et la capacité paraît morte) → les 3 cartes ont quitté la défausse et
      exactement 1 se trouve en main. Vert du premier coup.
- [x] Étape 8 : `hd012` présente dans **8/8** parties, 0 traceback.

Carte terminée : OUI

### hd013 : Beverly Switzler (soutien, coût 1)

- [x] Étape 2 : cartes de référence : `ok011` Upanga pour
      `WhenInYourPlayTurn(AlterEgoAction, ...)` + `CostFunc.Exhaust("This")` ;
      `il009` Vision AI pour `Faces.ReturnToHand` ; `il002` pour
      `this.HealthUnits`.
- [x] Étape 5 : mots-pièges : **`the BOTTOMMOST Howard the Duck card`** — la
      cible native `from_where=["YourDiscardPileBottommost"]` ne prend QUE la
      carte du fond, sans filtre de set : inutilisable ici. Recherche faite à la
      main sur `player.discard_pile.Get()`, qui rend la défausse du FOND vers le
      dessus (`deck.py:381-387`, exactement ce que consulte
      `get_YourDiscardPileBottommost`, `selector_where.py:114`). Le filtre est le
      **SET** (`set_name="Howard the Duck"`), pas le trait ni le nom.
      **`Heal 1 damage from your identity`** = seconde opération de la même
      capacité, jamais oubliée (piège `and remove`). Résultat : conforme.
- [x] Étape 6 : nombres : coût 1, 1 dégât soigné. Résultat : conforme.
- [x] Étape 7 : cas `hd013 Beverly Switzler` : `01087` Haymaker déposée **sous**
      `hd005` dans la défausse — c'est elle la vraie carte du fond, mais elle
      n'est pas une carte Howard : si le filtre de set était absent, c'est elle
      qui remonterait. Résultat : `hd005` en main, dégâts de l'identité ramenés
      de 2 à 1, Beverly inclinée. Vert du premier coup.
- [x] Étape 8 : `hd013` présente dans **8/8** parties, jouée
      (`Play:Support`), 0 traceback.

Carte terminée : OUI

### hd014 : Ducktective Agency (soutien, coût 2)

- [x] Étape 2 : cartes de référence : `ncrawler/nightcrawler/48005.py`
      (Prehensile Tail) pour `CanGenerateResources(AbilityType.Resource,
      Resources("B"), for_card=CardFinder(card_type=Event))` +
      `CostFunc.Exhaust("This")` ; `AfterUnitDefeatedScheme` (`scheme.py:203`),
      famille de `40001a` Cable ; `ok014` pour `Faces.ReadyAll`.
- [x] Étape 5 : mots-pièges : **`for an event`** = `for_card`, seul mécanisme du
      moteur pour restreindre une ressource (une ressource non filtrée se
      dépenserait sur n'importe quoi) ; **`[mental]`** = `"B"` ; **`After YOU
      remove the last threat from A SCHEME`** = portée LARGE sur la manigance
      (`None`, pas seulement les annexes) et RESTREINTE sur l'auteur (`"You"`) —
      contraste voulu avec `hd015`, qui restreint la manigance aux annexes.
      Résultat : conforme.
- [x] Étape 6 : nombres : coût 2, 1 ressource générée. Résultat : conforme.
- [x] Étape 7 : deux cas, un par capacité :
      - `hd014 — capacité Resource` : **preuve par insuffisance** — la main ne
        contient QUE First Aid (`01086`, événement officiel à coût 1) et aucune
        carte-ressource ; la seule source de paiement possible est l'Agence.
        Résultat : First Aid en défausse (jouée), Agence **inclinée**, identité
        soignée de 2 (3 dégâts → 1). Vert après reconstruction du cas (voir la
        limite de harnais n°2 : un événement à coût 2 ne convenait pas, vérifié
        avec le témoin officiel `40007` Graymalkin).
      - `hd014 — Hero Response` : l'Agence est **inclinée avant** (donc elle ne
        peut pas non plus servir à payer) ; `hd010` vaincue par `hd007` →
        l'Agence est redressée. Son redressement ne peut venir que de la
        Response. Vert du premier coup.
- [x] Étape 8 : `hd014` présente dans **8/8** parties, 0 traceback.

Carte terminée : OUI

### hd015 : Duckpool Suit (amélioration, coût 2)

- [x] Étape 2 : cartes de référence : `ok014` Royal Protector et `ss015`/`ss016`
      pour `GiveKeywordToInPlayWhenApplyThis` sur une amélioration **sans ligne
      « Attach to... »** (portée directement par le joueur) ;
      `AfterUnitDefeatedScheme(HeroResponse, "You", SchemeSide2, ...)` +
      `CostFunc.Exhaust("This")`.
- [x] Étape 5 : mots-pièges : **`YOU get +3 hit points`** vise l'identité quelle
      que soit sa face (`"You"`) ; **`HOWARD THE DUCK gets +1 ATK`** vise la face
      HÉROS nommément — deux portées différentes sur la même carte (même
      distinction que `ok014`) ; **`After you defeat A SIDE SCHEME`** =
      `SchemeSide2`, restreint aux annexes (contraste voulu avec `hd014`) ;
      **`exhaust Duckpool Suit`** = coût. Résultat : conforme.
- [x] Étape 6 : nombres : coût 2, +3 PV, +1 ATQ, 1 dégât. Résultat : conforme.
- [x] Étape 7 : deux cas :
      - `hd015 — +3 PV et +1 ATQ` : carte posée, `health +3` et `attack +1`
        constatés sur l'identité. Vert du premier coup.
      - `hd015 — Hero Response` : `hd010` vaincue par `hd007` → Duckpool Suit
        **inclinée** et 1 dégât sur Rhino. Vert du premier coup.
- [x] Étape 8 : `hd015` présente dans **8/8** parties, jouée
      (`Play:Upgrade`), 0 traceback.

Carte terminée : OUI

### hd016 : Iron Suit (amélioration, coût 2)

- [x] Étape 2 : cartes de référence : `aos/nick_fury/50046.py` (Secret Agent),
      modèle EXACT du couple `this.RemoveThreatFromSchemes(targets, 1, effect)`
      (qui rend le nombre RÉELLEMENT retiré) + `Faces.PlaceTokensOn([this],
      <ce nombre>, 'threat', effect)` ; `aos/nick_fury/50043.py` (Eyepatch
      Camera) pour `initiator.DeclareNumber` borné par ce que la carte porte ;
      `ok004`/`ok019` pour le `ChooseAbilities` à 2 branches.
- [x] Étape 5 : mots-pièges : **`move 1 threat from a scheme TO HERE`** — la
      menace posée sur une carte JOUEUR est un **JETON** `'threat'`, pas un
      compteur (deux stocks distincts, rappel explicite dans
      `test_capacites.py`, clé `jetons`). `Scheme2.MoveThreat` (`scheme.py:155`)
      est écarté : sa destination doit être une manigance, jamais une
      amélioration. **`remove X threat from here`** = coût payé avant l'effet.
      **`deal X damage to a MINION or remove X threat from a scheme`** = portées
      ASYMÉTRIQUES : la branche dégâts vise un SBIRE (`Minion`, le vilain n'est
      pas une cible légale), la branche menace vise n'importe quelle manigance.
      Résultat : conforme.
- [x] Étape 6 : nombres : coût 2, 1 menace déplacée, X borné par les jetons
      portés. Résultat : conforme.
- [x] Étape 7 : deux cas, un par capacité :
      - `hd016 — Action` : complot principal à 5 menaces → 4, **1 jeton
        `threat`** sur Iron Suit, carte inclinée. Vert du premier coup.
      - `hd016 — Hero Action` : 3 jetons posés, le pilote prend le premier item
        de `DeclareNumber` (X = 1) et la première branche (dégâts) → 1 dégât sur
        Hydra Bomber et **2 jetons restants** (preuve que seul le montant déclaré
        est dépensé, pas tout le stock). Vert du premier coup.
        **La branche « retirer X menace d'une manigance » n'a pas de cas
        dédié** (même limite de pilote), et la valeur X > 1 non plus (même limite
        déjà documentée sur `il002`/`ss004`).
- [x] Étape 8 : `hd016` présente dans **8/8** parties, avec un déplacement de
      menace observé dans le journal (« Iron Suit reçoit 1 pion threat »),
      0 traceback.

Carte terminée : OUI (les deux capacités prouvées ; la branche « menace » du
second choix et les valeurs X > 1 restent hors de portée du pilote générique)

### hd017 : Nexus of all Realities (amélioration, Setup. Permanent.)

- [x] Étape 2 : cartes de référence : `AbilityFactory.WhenCardLeavePlay(Interrupt,
      ("YouControl", CardFinder(card_type=Ally)), ...)` (`card_move.py:208`, la
      carte est encore manipulable à ce stade) ; tuple `("YouControl", ...)` déjà
      utilisé par `ok010`/`ok014` pour rendre « an ally YOU control » ;
      `ok001b`/`ss001b` pour `Search.PlayerCard` + `GainCard`.
- [x] Étape 5 : mots-pièges : **`Setup`/`Permanent`** = lus dans `desc`, aucune
      ability sur CETTE carte — mais `desc.Setup` seul ne suffit pas à la mettre
      en jeu (voir bug n°1) : la mise en place est portée par l'identité
      `hd001b` ; **`search your DECK`** (pas la défausse :
      `include_discard_pile=False`) ; **`an ally YOU control`** (piège `you
      control`) ; **un second Interrupt annoncé** — vérifié qu'il a bien un
      module, ce qui a mis au jour le bug n°1 (la carte n'entrait jamais en
      jeu). Résultat : conforme, **sauf le premier Interrupt**, ci-dessous.
- [x] Étape 6 : nombres : aucun nombre imprimé (1 carte cherchée).
      Résultat : conforme.
- [x] Étape 7 : cas `hd017 Nexus of all Realities — Interrupt` : la main est
      vidée puis rechargée d'une SEULE carte ressource (aucun événement), donc
      tout événement présent en fin de cas vient de la recherche ; Man-Thing mis
      en jeu puis tué en **deux** coups (Ténacité absorbe le premier, même piège
      que `il019` Kang). Rouge avant le correctif du deck (bug n°1), vert après.
- [x] Étape 8 : `hd017` en jeu dès la mise en place de **8/8** parties depuis
      le correctif, activation observée dans le journal (« Nexus of all
      Realities activates » après la mise sous `hd025` de Jessica Jones),
      0 traceback.

Carte terminée : OUI pour le second Interrupt et pour la mise en place.
**Le PREMIER Interrupt imprimé (« When a character enters play, choose a play
area that character is played to ») est délibérément NON CODÉ** — voir la
section « à vérifier en partie réelle » en fin de document.

### hd018, hd019, hd020 : Energy, Genius, Strength (ressources re-skinnées)

- [x] Étape 2 : **aucun script requis** — ces trois cartes sont des `full_link`
      vers `01088`/`01089`/`01090` dans `data/cards.json`. Le mécanisme clone
      intégralement les règles de la carte officielle : type, `RES`,
      `MaxPerDeck`, classe et comportement. Écrire un module leur serait non
      seulement inutile mais nuisible (il masquerait le clone).
- [x] Étape 5 : texte-contre-code : le seul texte imprimé est « Max 1 per
      deck. », rendu par `desc.MaxPerDeck` de la carte liée.
      Résultat : conforme.
- [x] Étape 6 : nombres : `MaxPerDeck` 1, `RES` `YY`/`BB`/`RR` — hérités des
      cartes officielles, jamais ressaisis. Résultat : conforme.
- [x] Étape 7 : pas de capacité, donc pas de cas sujet. Elles sont néanmoins
      **exercées en direct** : `hd019` Genius apparaît dans la main de départ de
      plusieurs cas et sert de carburant, et `hd018`/`hd020` figurent dans le
      deck monté par `verifier_tous_les_decks.py`.
- [x] Étape 8 : les trois apparaissent dans **8/8** parties d'autoplay
      (journaux de défausse et de paiement), 0 traceback.

Carte terminée : OUI (les 3 ; aucun script requis, clone de `01088`/`01089`/
`01090`)

### hd021 : Waddle it Be? (obligation)

- [x] Étape 2 : cartes de référence : `ok019` Funeral Rites et `ss017`
      Murderer's Guilt, même structure
      `AbilityFactory.WhenThisObligationGiveToYou` +
      `YouMayFlipToYourAlterEgoForm` + `player.ChooseAbilities` à 2 branches ;
      `ok001b`/`kb002` pour `Faces.ShuffleAllTo` ; `ok019` pour
      `ThisCardGainSurge`.
- [x] Étape 5 : mots-pièges : **`Give to the Howard Duckson player`** =
      `desc.GiveTo` ; **`Choose`** (pas « you may choose ») = choix FORCÉ,
      `ChooseAbilities` et non `MayChooseOneAbility` ; **`Exhaust Howard
      Duckson`** = la face ALTER-EGO nommément
      (`GetIdentity().GetAlterEgoFace()`, comme `ok019`), pas l'identité tout
      court ; **`all Howard the Duck side schemes`** = portée restreinte au set
      « Howard the Duck » (la phrase les remélange DANS VOTRE DECK, ce qu'une
      carte rencontre ne peut pas faire) ; **`If no schemes were removed this
      way`** = condition sur le retrait RÉEL ; **`Discard this obligation`**
      appartient à la SEULE branche 2 (la branche 1 la retire du jeu — piège
      « portée d'une phrase ambiguë », tranché comme sur `ok019`).
      Résultat : conforme.
- [x] Étape 6 : nombres : Boost 2. Résultat : conforme.
- [x] Étape 7 : cas `hd021 Waddle it Be? — branche 1` : obligation révélée →
      **retirée de la partie**, alter-ego incliné. Vert du premier coup.
      **La branche 2 n'a pas de cas dédié** (le pilote prend toujours la première
      option), même limite déjà documentée sur `il017`/`ok019`/`ss017`.
- [x] Étape 8 : `hd021` présente dans **8/8** parties (obligation du héros,
      mise de côté au setup puis révélée par le deck de rencontre),
      0 traceback.

Carte terminée : OUI (branche 1 prouvée ; branche 2 non couverte par un cas
dédié, même limite que toute obligation « Choose » à 2 branches du dépôt)

### hd022 : Duck and Cover! (manigance annexe némésis, Hazard 1)

- [x] Étape 2 : carte de référence : `core/captain_marvel_nemesis/01179.py`
      (Yon-Rogg's Treason) pour `player.hand_cards.FindCards(has_printed_res=
      <lettre>)` + `Faces.DiscardAll` ; `ok020` Malevolent Mimic pour
      `this.PlaceThreatOnSchemes([this], ...)` ; `Players.ForEachPlayer`.
- [x] Étape 5 : mots-pièges : **icône Hazard** (mot-clé automatique
      `desc.Hazard`, aucun code ; icône vérifiée par découpe d'image, carte
      penchée NUE sans barre de soulignement, témoin `ag011` — à ne pas
      confondre avec l'Accélération de `hd026`) ; **`a PRINTED [mental]`** =
      `has_printed_res="B"`, qui ne convertit PAS le joker
      (`convert_green_res = False`, `finder.py:102`) — une carte à ressource
      wild n'est donc pas défaussée ; **`MUST discard`** = défausse forcée, pas
      un `AskDiscardFaces`, et TOUTES les cartes concernées ; **`EACH player`** ;
      **`1 ADDITIONAL threat HERE for each card discarded THIS WAY`** = compté
      sur les défausses réellement faites, tous joueurs confondus, et posé sur
      SOI-MÊME. Résultat : conforme.
- [x] Étape 6 : nombres : menace de départ `2*`, Boost 3, Hazard 1, +1 menace par
      carte. Résultat : conforme.
- [x] Étape 7 : cas `hd022 Duck and Cover! — When Revealed` : deux Genius
      (`01089`, RES `BB`) en main → main vidée et menace = 2 (départ) + 2
      (défaussées) = **4**. Cas joué en forme d'identité civile **à dessein**,
      pour que Private Eye (`hd001a`, hors jeu en civil) n'interfère pas avec la
      menace posée. Vert du premier coup.
- [x] Étape 8 : `hd022` révélée dans 1 partie sur 8 de l'autoplay (set némésis,
      aléa du tirage), 0 traceback.

Carte terminée : OUI

### hd023 : Collector (sbire némésis, Villainous)

- [x] Étape 2 : cartes de référence : `ss007` Spider-pathy pour
      `Search.EncounterCard(..., card_type=EncounterSideScheme)` +
      `face.PutIntoPlay` ; `kb008`/`ok023` pour le choix fait à la main par le
      joueur visé (`AskChooseFace`) — la carte est une carte RENCONTRÉE, son
      ability n'a pas de sélecteur propre au joueur ciblé.
- [x] Étape 5 : mots-pièges : **`Villainous`** = mot-clé automatique lu dans
      `desc.Villainous`, aucun code (précédent `ok021` pour « Steady ») ;
      **`an ally OR support YOU control`** = deux types autorisés ET restriction
      de contrôle (piège `you control` : la cible ne doit jamais pouvoir viser
      une carte du vilain) ; **`If you CANNOT`** (et non « if you choose not
      to ») = vérifié AVANT de proposer le choix, pas après un refus ;
      **`the topmost scheme from the encounter deck`** = recherche, pas un nom
      précis. Filtre `canbe_discard=True` ajouté après le bug n°2.
      Résultat : conforme.
- [x] Étape 6 : nombres : HP 5, SCH 3, ATQ 1, Boost 2, Villainous 1.
      Résultat : conforme.
- [x] Étape 7 : deux cas, un par branche :
      - `hd023 — When Revealed` : Man-Thing seul allié en jeu → défaussé.
        Vert du premier coup.
      - `hd023 — branche de repli` : aucun allié ni soutien, `hd025` remontée sur
        le dessus du deck de rencontre → `hd025` en jeu. Vert du premier coup.
- [x] Étape 8 : `hd023` révélée dans 1 partie sur 8 de l'autoplay (set némésis,
      aléa du tirage), 0 traceback.

Carte terminée : OUI

### hd024 : Hellcow (sbire némésis ALTERNATIF, Quickstrike)

- [x] Étape 2 : cartes de référence : `ss021` Undead Hand Ninja et
      `lockjaw/lj015.py` (Annihilus), modèle EXACT de
      `WhenUnitWouldBeDefeated("This")` + `message.SetBeInstead(effect)` +
      `Faces.ShuffleAllTo([this], "EncounterDeck", effect)` ;
      `determination/dt078.py` (Cumbersome Enhancements) pour
      `WhenPhaseBegin(ForcedInterrupt, "Villain", ...)` (`turn_phase.py:129`) ;
      `albert/ab012.py` pour `this.HealthUnits([this], 1, effect)`.
- [x] Étape 5 : mots-pièges : **`Quickstrike`** = mot-clé automatique lu dans
      `desc.Quickstrike`, aucun code (précédent `ss020` Harvester) ;
      **`Forced Interrupt`** (phase) vs **`Interrupt`** (défaite) = deux types
      d'ability distincts, le texte imprimé ne dit « Forced » que sur le premier
      — écart avec `ss021`, qui écrit « Forced Interrupt » sur sa clause de
      défaite ; **`shuffle her into the encounter deck INSTEAD`** = piège
      `instead`, la défaite n'a jamais lieu et la carte PART du terrain pour
      ARRIVER dans le deck, elle n'est pas dupliquée. Résultat : conforme.
- [x] Étape 6 : nombres : HP 6, SCH 1, ATQ 2, Boost 2, Quickstrike 1, 1 dégât
      soigné. Résultat : conforme.
- [x] Étape 7 : cas `hd024 Hellcow — Interrupt` : mise en jeu, 99 dégâts → hors
      jeu ET **présente dans le deck de rencontre** (remélangée, pas défaussée).
      Vert du premier coup.
      **Le Forced Interrupt « au début de la phase du méchant, soigner 1 » n'a
      pas de cas dédié** : le harnais `test_capacites` s'arrête au tour du
      joueur et ne peut pas atteindre le début de la phase du méchant sans
      terminer le cas. Le montage est celui, mot pour mot, de
      `determination/dt078.py`, déjà éprouvé. **À vérifier en partie réelle.**
- [x] Étape 8 : `hd024` est **hors du `nemesis_set` standard** (arbitrage n°2) :
      elle n'est donc jamais tirée par l'autoplay. Elle a en revanche servi de
      carte-témoin dans le cas `hd001b` (remontée sur le dessus du deck de
      rencontre), où elle s'est comportée normalement.

Carte terminée : OUI (Interrupt de défaite prouvé en direct ; soin de début de
phase du méchant non exercé par le harnais, mécanisme identique à un modèle
officiel déjà éprouvé)

### hd025 : Duck, Duck, Doom! (manigance annexe némésis)

- [x] Étape 2 : carte de référence : `aos/aim_abduction/50081.py` (Abduct
      Superhumans), modèle EXACT de `this.TuckCardUnderHere(ally, effect)` puis
      `this.GetPlacedCardArea().Get()` au When Defeated. 50081 remet les alliés
      EN JEU, `hd025` les rend EN MAIN → `Faces.ReturnToHand(faces, "Owner",
      effect)` (`faces.py:306`, mode "Owner" prévu pour cela).
- [x] Étape 5 : mots-pièges : **`an ally YOU control`** (piège `you control`) ;
      **`If you CANNOT`** = aucun allié du tout, vérifié AVANT le choix ;
      **`confuse YOUR identity`** = l'identité du joueur visé ; **`the ally
      BENEATH HERE`** = la zone rangée de CETTE carte, pas un allié quelconque
      (piège `that <nom>`). Résultat : conforme.
- [x] Étape 6 : nombres : menace de départ `2*`, Boost 2. Résultat : conforme.
- [x] Étape 7 : deux cas, un par branche :
      - `hd025 — rangement puis retour` : Man-Thing en jeu → rangé sous la carte
        (hors jeu), puis `hd025` déjouée → Man-Thing **en main**. Vert du premier
        coup.
      - `hd025 — branche de repli` : aucun allié → identité civile (`hd001b`)
        **Désorientée**. Vert du premier coup.
- [x] Étape 8 : `hd025` révélée dans 1 partie sur 8 du lot final ; dans un lot
      antérieur (via `01190` Shadow of the Past) le rangement d'allié ET la
      branche « confuse » ont tous deux été observés dans les journaux.
      0 traceback.

Carte terminée : OUI

### hd026 : A Fowl Plot (manigance annexe némésis, Acceleration 1)

- [x] Étape 2 : cartes de référence : `hd023` pour
      `GetControlCardsByType` + `AskChooseFace` ; `card_face.py:574` (littéral
      `"MainScheme"` prévu par `PlaceThreatOnSchemes`) ; `core/01061.py` (Great
      Responsibility) pour `identite.TakeDamage(this, 1, effect)`.
- [x] Étape 5 : mots-pièges : **icône Acceleration** (mot-clé automatique
      `desc.Acceleration`, aucun code ; icône vérifiée par découpe d'image,
      pointe + BARRE DE SOULIGNEMENT, témoin `ag011` — à ne pas confondre avec
      le Hazard de `hd022`) ; **`an upgrade YOU control`** (piège `you control`,
      plus le filtre `canbe_discard` du bug n°2) ; **`If NO CARDS were discarded
      this way`** = condition sur la défausse RÉELLEMENT effectuée
      (`Faces.DiscardAll` rend la liste des cartes effectivement parties), pas
      sur la simple présence d'une amélioration en jeu ; **`place 1 threat on
      the main scheme AND take 1 damage`** = deux opérations dans la même
      branche, aucune oubliée (piège `and remove`). Résultat : conforme.
- [x] Étape 6 : nombres : menace `2*`, Boost 3, Acceleration 1, 1 menace,
      1 dégât. Résultat : conforme.
- [x] Étape 7 : cas `hd026 A Fowl Plot — When Revealed` : `hd016` Iron Suit mise
      en jeu et désignée explicitement par `cibles` (pour éviter que le pilote ne
      tombe sur `hd017`, permanente) → Iron Suit défaussée. Vert.
      **La branche de repli (1 menace + 1 dégât) n'a pas de cas dédié** : le
      joueur contrôle TOUJOURS au moins `hd017`, permanente, donc la branche ne
      peut être atteinte qu'en partie où aucune amélioration défaussable n'est en
      jeu. Elle a en revanche été exercée **en autoplay** avant le correctif du
      bug n°2 (c'est précisément le chemin qui plantait), et le correctif la rend
      désormais atteignable proprement.
- [x] Étape 8 : `hd026` révélée dans 3 parties sur 8 d'un premier lot
      d'autoplay ; **c'est elle qui a livré le bug n°2** (3 tracebacks
      reproductibles). Après correctif : révélée dans 1 partie sur 8 du lot
      final (aléa du tirage), 0 traceback.

Carte terminée : OUI (branche « défausser » prouvée en direct ; branche de repli
observée en autoplay, sans cas dédié faute de position atteignable dans le
harnais)

### hd027 : Duck Hunt (trahison némésis)

- [x] Étape 2 : cartes de référence : `core/rhino/01106.py` (Stampede) et
      `ok023` War Drumming pour la structure
      `AbilityFactory.WhenThisRevealed("Alter-Ego"|"Hero", ...)` — DEUX abilities
      distinctes, pas un `if` sur la forme ; `ok021` Malice pour
      `villain.CastTo(Enemy).BasicSchemes(effect)` (`can_scheme.py:166`) ;
      `aos/nick_fury/50035b.py` (Stealth) pour l'interruption TEMPORAIRE
      `WhenSchemeWouldPlaceThreat` enregistrée avant l'activation ; `ok008` Spear
      Thrust pour la répartition point par point ; `ok006`/`trors 04017` pour
      `Faces.GiveStatus`, `il002`/`ab012` pour `HealthUnits`.
- [x] Étape 5 : mots-pièges : **`The villain schemes`** = manigance de base hors
      activation normale, avec ses cartes boost ; **`divide and place threat from
      this activation among them INSTEAD`** = piège `instead`, la menace PART du
      complot principal (annulée par `PreventThreat("All")`) pour ARRIVER sur les
      annexes, elle n'est pas dupliquée ; **`If there are side schemes in play`**
      = condition vérifiée AVANT, sinon la manigance se résout normalement ;
      **`Give the villain a tough status card. If you CANNOT`** = vérifié par
      `HasStatus("Tough")` AVANT, pas après un échec silencieux ; **`heal 3
      damage from IT`** = le vilain lui-même (piège `that <nom>`).
      Résultat : conforme.
- [x] Étape 6 : nombres : Boost 2, 3 dégâts soignés. Résultat : conforme.
- [x] Étape 7 : trois cas, un par branche :
      - `hd027 — When Revealed (Hero)` : Rhino reçoit le statut **Tenace**.
        Vert du premier coup.
      - `hd027 — When Revealed (Hero), « If you cannot »` : Rhino déjà Tenace et
        blessé de 5 → soigné de 3 (dégâts ramenés à 2). Vert du premier coup.
      - `hd027 — When Revealed (Alter-Ego)` : `hd010` en jeu, complot principal
        remis à 0 → le journal trace « The Break-In! would place 1 (Scheme) »
        puis « **Trapped** would place 1 » : le complot principal reste à **0**
        et la manigance annexe monte. Vert du premier coup.
- [x] Étape 8 : `hd027` révélée dans 1 partie sur 8 de l'autoplay et
      remélangée dans le deck de rencontre sans incident, 0 traceback.

Carte terminée : OUI

---

## Note technique : la clé `set_aside` d'un deck de départ est documentaire

Rappel, parce que le piège est silencieux : le champ `set_aside` d'un
`deck/starter/*.json` n'est lu QUE par le chemin « puzzle »
(`server_new_game.py:109/122`). `SceneLoader.NewScene` construit son
`HeroDescriptor` sans lui (`loader.py:98-108`), et `player_setup.py:213` porte
la ligne commentée `# CardFactory.GenerateCards(set_aside, ...)`. De son côté,
`World.GameSetup` ne cherche les cartes `Setup` que dans `player_deck`,
`set_aside_nemesis_sets`, les decks de rencontre et `world.additional_decks`
(`world.py:531-539`).

**Le vrai mécanisme est sur l'identité** : `AbilityFactory.SetupPutIntoPlay
(["<card_id>", ...])` (`setup.py:6-31`) appelle `CardFactory.GenerateCards`, qui
fabrique la carte depuis son `card_id` sans qu'elle appartienne à aucun deck,
puis la met en jeu sous le contrôle du joueur. Les 21 decks de départ à
`set_aside` non vide ont été vérifiés un par un : **aucune carte orpheline**,
tous passent par ce crochet (ou par un deck annexe créé par script, comme le
deck Invocation de Doctor Strange ou le deck Sense de Daredevil). Écrire
`set_aside` sans `SetupPutIntoPlay` produit une carte muette.

## Gate finale de `PROCESSUS-HEROS.md`

- [x] **Étapes 1 à 8 complètes**
      1. `data/cards.json` : 28 card_id, checksums recalculés — fait (session
         antérieure).
      2. Scripts : 25 modules (`hd001a`-`hd017`, `hd021`-`hd027`), plus les 3
         `full_link` sans script — fait cette session.
      3. `deck/starter/howard_the_duck.json` : aspect Justice, 15 cartes
         signature, `set_aside: ["hd017"]` documentaire, obligation, set némésis
         de 5 cartes, 25 cartes d'aspect — fait, corrigé cette session.
      4. `data/nemesis/howard_the_duck_nemesis.json` — fait.
      5. `data/sets_info.json`, entrée « 128. Custom (Howard the Duck) » — fait.
      6. Images : les 28 `assets/pics/hd*.png` présentes
         (`verifier_coherence_cartes.py` : 0 image manquante).
      7. **Biographie** : entrée `"hd001a"` dans
         `public/js/prepare/heros-info.js` (`bio`, `bioEn`, `civil`, `base`,
         `apparition`). **Preuve au survol dans le wizard NON faite** — elle
         exige le navigateur, voir ci-dessous.
      8. **Texte français** : 28 entrées dans
         `ui-app/src/board/textes-fr-fanmade.ts`, une par card_id du pack, les
         3 ressources `full_link` incluses (« Maximum 1 par deck. »).
- [x] **Un `PROCESSUS-CARTE.md` rempli et « Carte terminée : OUI » pour chaque
      carte du pack** : `hd001a`, `hd001b`, `hd002`, `hd003`, `hd004`, `hd005`,
      `hd006`, `hd007`, `hd008`, `hd009`, `hd010`, `hd011`, `hd012`, `hd013`,
      `hd014`, `hd015`, `hd016`, `hd017`, `hd018`, `hd019`, `hd020`, `hd021`,
      `hd022`, `hd023`, `hd024`, `hd025`, `hd026`, `hd027` — **28/28 OUI**.
- [ ] **Une partie complète jouée avec le héros** : **NON FAIT**. Un agent ne
      peut pas jouer une partie dans le navigateur. Ce point reste à la charge
      d'un humain.

**La gate finale est donc INCOMPLÈTE** : deux points exigent le navigateur (la
preuve de la biographie au survol, et la partie réelle). Tout le reste est fait
et prouvé.

## Ce que ces blocs ne peuvent pas voir

**Aucune partie n'a été jouée par un humain dans le navigateur.** Un agent ne
peut pas jouer une vraie partie dans l'interface web : ce point de la gate finale
de `PROCESSUS-HEROS.md` reste **explicitement NON FAIT**, à réaliser par un
humain. La validation s'arrête à `test_cards`, `verifier_*`, `test_capacites`
(30 cas verts) et `autoplay` (8 parties, 0 traceback, comparable au témoin
`okoye`).

**La preuve de la biographie n'a pas non plus été faite** : l'étape 7 de
`PROCESSUS-HEROS.md` exige de confirmer AU SURVOL du héros dans le wizard que le
panneau affiche bien le texte attendu, et pas seulement le grand visuel. L'entrée
`"hd001a"` est écrite dans `public/js/prepare/heros-info.js` au format exact des
entrées `ok001a`/`il001a`/`ss001a` voisines, mais **seul un humain peut le voir
à l'écran**. Un héros sans entrée retombe silencieusement sur l'ancien affichage :
rien ne casserait, mais la fiche manquerait.

Points précis à vérifier en priorité lors de cette partie réelle :

1. **`hd017` (Nexus of all Realities), PREMIER Interrupt** : « When a character
   enters play, choose a play area that character is played to. » **Ce qui
   manque, précisément** : la possibilité d'envoyer un personnage dans l'aire de
   jeu d'un AUTRE joueur au moment où il entre en jeu. Le moteur n'expose aucun
   crochet pour cela — `Message.WhenCardEnterPlay` (`sender_card.py:995`) ne
   porte aucune destination modifiable, et `Message.WhenCardPutIntoPlay`
   (`sender_card.py:388`) porte bien un `target_game_area` mais déclaré `Final`,
   donc figé avant que l'interruption ne puisse s'exprimer. **En solo — le seul
   mode où ce héros a été validé — il n'existe qu'une seule aire de jeu : le
   choix est vide de conséquence, et ne rien coder produit exactement le même
   état du monde que le texte imprimé.** À vérifier en MULTIJOUEUR, où la clause
   a un effet réel. Précédents de clause imprimée laissée sans code, assumée et
   documentée : `ok023` (« gains villainous for this attack ») et `kb003`
   (« cannot place arrow counters »).
2. **`hd024` (Hellcow), Forced Interrupt de début de phase du méchant** :
   vérifier qu'elle se soigne bien de 1 à chaque phase du méchant. Le harnais
   `test_capacites` s'arrête au tour du joueur et ne peut pas atteindre ce
   moment ; le montage est celui, mot pour mot, de `determination/dt078.py`.
   Hellcow étant un sbire **alternatif** hors du `nemesis_set`, il faut la
   substituer à la main au Collector pour l'exercer.
3. **`hd016` (Iron Suit), seconde branche et X > 1** : jouer la Hero Action avec
   plusieurs jetons de menace sur la carte, choisir X > 1 et la branche « retirer
   X menace d'une manigance ». Le pilote générique du harnais prend toujours le
   premier item offert (X = 1, première branche).
4. **Toutes les branches « Choose » libres** (`hd003`/`hd004` branche 2,
   `hd007`/`hd008` branche « retrait de menace », `hd021` branche 2) : même
   limite structurelle que tous les packs déjà validés du dépôt.
