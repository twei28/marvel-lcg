# Portage de Red Sonja

Demande de l'utilisateur, 22/09/2026 : « crée le héros red Sonia qu'ils a
dans le zip ». Zip trouvé à la racine du dépôt :
`Red Sonja (08-26)-20260922T153645Z-1-001.zip` (auteur : RyCoRan, template
CommCody103, 34 images 1500×2150, extraites dans le scratchpad de session).

## Tranche d'identifiants retenue

`rs001`-`rs019`, vérifiée libre sur toute la collection (`grep card_id`
`data/cards.json`, aucune carte `rs*` existante avant ce portage).

## Ce qui a été lu (texte exact des scans, transcrit image par image)

**Identité**
- `rs001a` * Red Sonja (Hero) : THW 1, ATK 2, DEF 2, HP 10, HS 5. Traits
  ADVENTURER. « She-Devil — Action: Exhaust a WEAPON upgrade you control →
  play an event from your hand, reducing its resource cost by 1. »
- `rs001b` * Sonja of Hyrkania (AlterEgo) : REC 3, HP 10, HS 6. Traits
  ADVENTURER. Ability 1 (règle de deckbuilding, imprimée hors « Action »):
  « During deck-building you may include up to 6 events from aspects other
  than your chosen aspect. » Ability 2 : « Day of the Sword — Action: Search
  your deck for the Hyrkanium Blade upgrade and add it to your hand. »
- Art alternatif disponible : `Sonja Hero (alt art).png` (mêmes texte/stats
  que `rs001a`, template CommCody103) — mécanisme `ARTS_HEROS` (`app.js`),
  PAS un second deck. Non posé dans cette passe (voir plan).

**15 signatures, 12 cartes uniques** (RED SONJA 1/15 à 15/15, recompté :
1+2+2+2+1+1+1+1+1+1+1+1 = 15)
1. `rs002` * Conan (Ally) — Cost 3, THW 1(*), ATK 1(*), HP 3. ADVENTURER.
   « Interrupt: When you use one of Conan's basic powers, exhaust a WEAPON
   upgrade you control → Conan gets +X to that power for this use, where X
   is equal to that card's printed cost. »
2-3. `rs003` Savage Steel (Event) ×2 — Cost 3. ATTACK. « Hero Action
   (attack): Deal 6 damage to an enemy. For each point of excess damage
   dealt by this attack, reduce the cost of the next event you play this
   phase by 1. »
4-5. `rs004` Scarlet Huntress (Event) ×2 — Cost 3. THWART. « Hero Action
   (thwart): Remove 6 threat from a scheme. For each point of excess threat
   removed by this thwart, reduce the cost of the next event you play this
   phase by 1. »
6-7. `rs005` Devil's Defiance (Event) ×2 — Cost 1. DEFENSE. « Hero Interrupt
   (defense): When an enemy attacks, prevent all damage from that attack.
   After this attack, give Red Sonja a tough status card. »
8. `rs006` Hyrkanian Fury (Event) — Cost 2. ATTACK. « Hero Action (attack):
   Deal 4 damage to an enemy. If you used your "She Devil" ability to reduce
   the cost of this card, stun that enemy. »
9. `rs007` Red Reckoning (Event) — Cost 2. THWART. « Hero Action (thwart):
   Remove 4 threat from a scheme. If you used your "She Devil" ability to
   reduce the cost of this card, confuse an enemy. »
10. `rs008` Savage She-Devil (Event) — Cost 4. ATTACK. THWART. « Hero Action
   (attack/thwart): Deal 5 damage to an enemy. Remove 5 threat from a
   scheme. If you used your "She-Devil" ability to reduce the cost of this
   card, this action ignores the guard and patrol keywords and any crisis
   icons in play. »
11. `rs009` * Queen of Sogaria (Player Side Scheme) — Cost 5, Victory 0.
   « Only Red Sonja can remove threat from this scheme. She may use her
   basic ATK, DEF or THW to do so. While Queen of Sogaria is in the victory
   display, Red Sonja gains: "Response: After you exhaust Hyrkanium Blade,
   draw 1 card. (Limit once per round.)" »
12. `rs010` She Devil with a Sword (Resource) — PREPARATION? non, type
   RESOURCE pur (icônes wild+énergie, `RES` double sur la carte : icône
   verte wild ET jaune énergie visibles en bas à gauche — à vérifier à
   l'image avant script, la carte affiche DEUX icônes de ressource
   superposées, cas rare). « Hero Response: After you spend this card, ready
   a weapon upgrade you control. »
13. `rs011` Crimson Shadow (Upgrade) — Cost 2. PREPARATION. SKILL.
   « Red Sonja gets +1 THW. Uses (2 stealth counters). Hero Response: After
   a minion enters play, remove 1 stealth counter from here → cancel that
   minion's "When Revealed" effect. »
14. `rs012` * Bloodmoon Battleaxe (Upgrade) — Cost 2. WEAPON. Restricted.
   « Response: After you play an event, exhaust Bloodmoon Battleaxe → deal 2
   damage to an enemy. »
15. `rs013` * Hyrkanium Blade (Upgrade) — Cost 2. WEAPON. « Red Sonja's basic
   attacks gain piercing. Response: After you defeat a side scheme or
   minion, ready Hyrkanium Blade. (Limit once per round.) »

**Obligation**
`rs014` A Warrior's Burden (Obligation) — Give to the Sonja of Hyrkania
   player. « Choose: • Exhaust your identity and discard Hyrkanium Blade →
   remove A Warrior's Burden from the game. • Search the encounter deck and
   discard pile for 2 minions and reveal them → discard this card. »
   (Coquille du scan : « Sonia of Hyrkania » — corrigé en « Sonja of
   Hyrkania », nom exact de `rs001b`.)

**Némésis (5 cartes, RED SONJA NEMESIS 1/5 à 5/5)**
`rs015` (1/5) Queen of the Frozen Wastes (Side Scheme) — icône boost 2
   (silhouette). « Players cannot ready WEAPON upgrades. »
`rs016` (2/5) Ice Queen (Minion) — SCH 2, ATK 2, HP 5. ELITE. MYSTIC.
   « When Defeated: The defeating player discards cards from the top of the
   encounter deck and reveals the first minion discarded this way. » Boost :
   Put this minion into play engaged with you. (Désignée « Red Sonja's
   nemesis minion » dans le texte imprimé.)
`rs017` (3/5) Yeti Warrior (Minion) — SCH 0, ATK 3(*), HP 6. CREATURE.
   Guard. Toughness. Boost : Yeti Warrior's attacks gain overkill.
`rs018` (4/5) She-Devil Shackled! (Attachment) — Uses (3 fetter counters).
   « When Revealed: Attach to your identity and exhaust each WEAPON upgrade
   you control. Forced Interrupt: When a WEAPON upgrade you control would
   ready, spend 1 resource of any type. If you do, remove 1 fetter counter
   from here (and ready that upgrade). Otherwise, that upgrade does not
   ready. »
`rs019` (5/5) Frozen Fury (Treachery) — Boost icônes ×2. « When Revealed:
   For each upgrade you control (to a maximum of 3), choose: • Take 1
   indirect damage. • Place 1 threat on the main scheme. »

## Hors scope de cette passe : dossier `Extras` et 3 ressources reskins

Vérifié image par image : **aucune de ces 10 cartes n'est du contenu
nouveau.** Sept portent le pied de page officiel « MARVEL CHAMPIONS » (pas
« MC Custom Content ») : ce sont des réimpressions ART SEULEMENT de cartes
déjà existantes dans le catalogue sous leur nom d'origine — `Army of One`
et `Innate Aggression` sont des cartes OFFICIELLES telles quelles ;
`Bloodfang Dagger` = reskin de `Pulse Grenade`, `Hyrkanian Longbow` = reskin
de `Plasma Pistol` (sous-titre imprimé sur la carte) ; `Draw Your Steel!` et
`Savage Strike` reskins d'événements d'aspect existants (texte non
re-vérifié contre le catalogue, mais mécaniquement banal). Seule
`Savage Alliance` (Team-Up Red Sonja/Conan) est un texte inédit, mais le
mot-clé Team-Up officiel suppose DEUX IDENTITÉS HÉROS en partie multijoueur,
pas un héros et son propre allié signature — portée non standard, laissée
de côté. Les 3 « Sonja (R) - Energy/Genius/Strength » sont les ressources
génériques `Max 1 per deck` déjà automatiques dans tout deck, juste
réillustrées. **Décision (cohérente avec la règle du 06/09/2026 sur
`player_deck`) : aucune de ces 10 cartes n'est créée.** `player_deck` du
héros reste VIDE : aucune vraie decklist n'a été fournie par l'auteur (un
sac de reskins n'en est pas une).

`Sonja Hero (alt art).png` (identique à `rs001a`) : identité alternative
purement cosmétique, à déclarer plus tard via `ARTS_HEROS` si demandé —
pas de biographie séparée (règle étape 7 de PROCESSUS-HEROS).

## Recherche moteur faite avant d'écrire les scripts

- Réduction de coût pour jouer une carte : `AbilityFactoryResources.
  ReduceCostToPlayFaceWhen(which_card, update_cost_fn, which_player,
  which_effect=...)` et `UpdateCostOfCardInternal`
  (`src/game/ability/factory/resources.py:642,690`). Permet de cibler UNE
  carte précise (`which_effect`) au moment où le joueur la joue depuis la
  main suite à l'Action de `rs001a`/`rs009` (Queen of Sogaria).
- Reste à chercher avant script : fabrique pour « play an event from your
  hand » déclenché par une Action (comparable à `Sea Hunter`/`PlayCardsLikeInTurn`
  du pack Wave, mais ici c'est un jeu NORMAL depuis la main, pas « comme si »
  — donc plutôt un simple `AskChooseFace` + `PlayerAction.PlayCard`), et le
  drapeau « if you used your She-Devil ability to reduce the cost of this
  card » (état à poser sur LA CARTE au moment où `rs001a` réduit son coût,
  relu par `rs006`/`rs007`/`rs008` à leur propre résolution) — candidat :
  état temporaire posé via `Effect` sur `message.check_effect.this` dans le
  `update_cost_fn` de `ReduceCostToPlayFaceWhen`, relu par une condition
  côté carte.

## Plan d'exécution

- [x] Lecture des 34 scans, transcription ci-dessus.
- [ ] A. `data/cards.json` : 19 entrées (`rs001a/b`, `rs002`-`rs013`,
      `rs014`, `rs015`-`rs019`).
- [ ] B. Scripts `src/cards/pack/red_sonja/{red_sonja,red_sonja_nemesis}/*.py`.
- [ ] C. `deck/starter/red_sonja.json` (15 copies listées, obligation,
      nemesis_set avec doublon si besoin, `player_deck` VIDE — voir note
      ci-dessus).
- [ ] D. `data/sets_info.json` : entrée pack + héros.
- [ ] E. `data/nemesis/red_sonja_nemesis.json` (facultatif, cf.
      PROCESSUS-HEROS étape 4).
- [ ] F. Images : conversion des scans 1500×2150 en 300×434 JPEG,
      `assets/pics/rs0XX.jpg`.
- [ ] G. Biographie `heros-info.js` (copie vivante), indexée `rs001a`.
- [ ] H. Textes FR `ui-app/src/board/textes-fr-fanmade.ts`.
- [ ] I. `tools/test_capacites.py` : un cas par carte, preuve par
      substitution (`tools/substituer_pack.py`).
- [ ] J. `tools/verifier_tous_les_decks.py` (gate finale).
- [ ] K. Autoplay ciblé + grep tracebacks.
- [ ] L. Test plateau (étape 8 bis) si une carte dessine quelque chose
      (Crimson Shadow : compteurs stealth ; She-Devil Shackled! : compteurs
      fetter, attaché à l'identité ; upgrades exhaustées visibles).
- [ ] M. Gabarits `PROCESSUS-CARTE.md` par carte (fichier séparé, comme
      Wave : `.planning/todos/2026-09-22-red-sonja-gabarits-processus-carte.md`).
- [ ] N. Partie complète jouée avec le héros (gate finale de
      PROCESSUS-HEROS, hors de portée d'un outil — à signaler si non faite).

## RES (icône de ressource) vérifiée carte par carte, contre l'icône réelle

Vérifiée à l'image pour chaque carte signature (icône en bas à gauche, pas
la couleur du badge de coût qui est neutre noir/blanc dans ce template) :
`rs002` Conan R, `rs003` Savage Steel R, `rs004` Scarlet Huntress B,
`rs005` Devil's Defiance Y, `rs006` Hyrkanian Fury R, `rs007` Red Reckoning
G, `rs008` Savage She-Devil Y, `rs009` Queen of Sogaria B (badge de coût
coloré « 7 », convention différente pour `PlayerSideScheme`, cf. modèle
`40006` Technovirus Purge), `rs010` She Devil with a Sword GY (double icône
empilée = ressource qui compte comme LES DEUX types, convention confirmée
par grep sur `data/cards.json` : `Resources.FromText` additionne chaque
lettre, cf. `45010 Stored Energy RY`), `rs011` Crimson Shadow B, `rs012`
Bloodmoon Battleaxe Y, `rs013` Hyrkanium Blade R.

`rs017` Yeti Warrior : ATK imprimé « 3★ » — vérifié dans
`src/game/card/face/attribute/can_attack.py:48` que l'astérisque sur ATK
encode `printed_attack_consequential_damage` (dégât conséquent, règle
officielle), PAS un ajout de la valeur de Boost. Aucun badge Boost
numérique visible sur la carte → `Boost: "0"` correct malgré l'astérisque.

## ⚠⚠ PIÈGE ÉVITÉ, 22/09/2026 : ne jamais `json.dump` le fichier entier sans
l'indent d'origine

Premier essai d'écriture des 20 cartes dans `data/cards.json` : script
Python `json.load` + `json.dump(..., indent=4)` → **diff de 196 544 lignes**
(98 738 insertions/97 806 suppressions) au lieu des ~900 attendues, parce que
le fichier d'origine est sérialisé avec `indent=1` (1 espace par niveau, pas
4) et que `json.dump` réécrit TOUT le fichier avec le nouvel indent dès
qu'on le repasse une fois par `json.load`/`json.dump`. Aucune donnée
perdue (le contenu JSON est identique, seul le texte change), mais un tel
diff aurait pollué toute review future. **Corrigé en re-sérialisant avec
`indent=1` explicite** (vérifié contre `git show HEAD:...` : le fichier
d'origine encode déjà les tirets cadratins en UTF-8 littéral, donc
`ensure_ascii=False` était le bon choix dès le départ, seul l'indent était
faux). Diff final : 934 insertions, 2 suppressions (les 20 cartes + la
ligne `checksum`, déjà différente de HEAD avant cette session). **Leçon
pour toute future édition programmatique de `cards.json` ou
`sets_info.json` : `json.dump(..., ensure_ascii=False, indent=1)`,
jamais l'indent par défaut d'un script improvisé.**

## Étape A — FAITE : `data/cards.json`, clé `red_sonja`, 20 entrées

`rs001a`/`rs001b` (identité), `rs002`-`rs013` (12 cartes signature
uniques), `rs014` (obligation), `rs015`-`rs019` (némésis). Chargement
vérifié via `json.load` direct (pas encore testé via `CardsDB.papers` du
moteur — à faire à l'étape B/scripts).

Statut au 22/09/2026 : étape A faite. Reste B (scripts), C (deck), D
(sets_info), E (nemesis json, facultatif), F (images), G (bio), H (textes
FR), I (tests+substitution), J (verifier_tous_les_decks), K (autoplay),
L (test plateau), M (gabarits), N (partie complète).

## Tâche en attente, après ce portage : refonte du gabarit de pages du site

Demande de l'utilisateur en cours de portage (22-23/09/2026) : le gabarit
`PAGE` commun de `site/orchestrateur.py` (CSS partagé par `/entrer`,
`/admin`, `/signalements`, `/suivi`, `/reinitialisation`, `/arret`,
`/hors-ligne.html`...) est trop brut (« ça fait très moche »). Décisions
déjà prises par questions multichoix :
- Périmètre : le GABARIT COMMUN (une seule passe qui améliore toutes les
  pages qui l'utilisent), pas page par page.
- `/signalements` est accessible à TOUS les comptes (pas seulement admin,
  vérifié par un agent de recherche : garde `if not pseudo`, pas de check
  `ADMIN`) — donc concerné, contrairement à `/admin` et `/suivi` qui restent
  réservés à `ADMIN`.
- Direction visuelle : fond sombre conservé mais soigné, aligné sur
  l'identité visuelle des pages de sélection de perso du jeu (`ui-app`,
  écrans de préparation) plutôt qu'un style néo/Marvel générique.
- Ordonnancement : finir Red Sonja d'ABORD, puis enchaîner directement sur
  cette refonte SANS repasser par l'utilisateur entre les deux.

## Étape B — FAITE : 20 scripts (`src/cards/pack/red_sonja/{red_sonja,red_sonja_nemesis}/*.py`)

`rs001a`, `rs001b`, `rs002`-`rs013`, `rs014`, `rs015`-`rs019` + deux
`__init__.py` (helpers partagés `JouerEvenementReduitParSheDevil`,
`AUtiliseSheDevil`, `DegatsExcedentairesDeCetteAttaque`,
`MenaceExcedentaireDeCeContre`). Deux compteurs maison ajoutés au moteur
(`src/game/card/face/card_face.py`, `COUNTER` Literal) : `stealth` (rs011),
`fetter` (rs018) — sans eux la construction du deck plante (même piège que
`foe`/throg documenté dans le fichier).

⚠⚠ ARBITRAGE UTILISATEUR (22/09/2026, posé AVANT le script) : `rs011`
Crimson Shadow imprime « Hero Response » pour annuler un « When Revealed »
d'un sbire — mécaniquement impossible en Response (trop tard). Codé en
**Interrupt fonctionnel**, écart assumé et documenté en tête du fichier.

Recherche moteur notable (patterns non couverts par RECETTES-MOTEUR avant
ce portage, à y ajouter si un futur portage en a besoin) :
- `AbilityFactoryResources.ReduceCostToPlayFaceWhen`/`PlayCardsLikeInTurn(
  update_resources_cost=N)` pour « reduce the cost of X by N » (par
  opposition à `ignore_resources_cost` qui annule tout).
- `Worlds.UpdateNextCardPlayCost(joueur, -N, effect, finder=..., in_this=
  "Phase")` pour « reduce the cost of the next event you play this phase ».
- `AfterUnitDefeatedUnit(is_from_attack=True, has_excess_damage=True)` +
  `message.excess_damage` pour l'« excess damage » officiel (`ar005`) ;
  AUCUN équivalent natif pour un « excess threat » côté contre — calcul
  direct (`CardFace.threat` lu AVANT `RemoveThreatFromSchemes`).
- `CostFunc.Exhaust(trait="WEAPON")` pour « exhaust a WEAPON upgrade you
  control » (`an003`).
- `AbilityFactory.WhenUnitUseBasicPower` + `message.GainValue(x, effect)`
  pour un allié qui gagne +X à son propre pouvoir de base.
- `AbilityFactory.AfterYouSpendThisCard` (resources.py:508) EXISTE (contrairement
  à ce que suggérait un commentaire du pack `wave`) pour une ressource qui
  réagit à sa propre dépense.
- `AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity")` pour un
  attachement némésis qui s'attache à l'identité du joueur touché.
- `joueur.AskSpendResourcesInternal(Cost("1"), effect)` rend `None` si le
  paiement échoue/est refusé — modèle `si014`/`ah014` pour « spend N
  resources of any type. If you do, ... Otherwise ... ».
- Marqueur « cette carte a été jouée via l'Action She-Devil » : PAS de
  mécanisme natif pour « une capacité sait qu'une AUTRE capacité a réduit
  SON coût » — résolu par un attribut Python brut posé sur l'objet `Card`
  lui-même (`rs_reduit_par_she_devil`), jamais un dict global côté module
  (fuite entre parties possible sur un process multi-tables). Point le plus
  original de ce portage, **à vérifier en priorité par un cas réel**.

## Étape A bis — cards.json corrigé après relecture des scripts

Deux champs `desc` oubliés à l'écriture initiale, ajoutés après coup (même
discipline de re-sérialisation `indent=1`) : `rs011.desc.Uses = "2,stealth"`,
`rs017.desc.Guard = "1"` + `rs017.desc.Toughness = "1"`, `rs018.desc.Uses =
"3,fetter"`.

## Étape J (gate `verifier_tous_les_decks.py`) — FAITE, VERTE, 23/09/2026

```
DECK_NOM=red_sonja python3.10 tools/verifier_tous_les_decks.py .game-src-par9 41000
RESULTAT: {'deck': 'red_sonja', 'ok': True, 'message': 'identite rs001b, main 6, deck 9'}
```

Le deck monte une VRAIE partie (setup complet : identité, 15 cartes
signature, obligation, set némésis) sans assertion de construction, sans
traceback. C'est la gate qui a fait planter `lady_sif` malgré 22 cas verts
(leçon du §9 de PROCESSUS-CARTE) — elle est donc la première preuve
sérieuse que le pack est structurellement sain. ⚠ Interpréteur correct sur
cette machine : `~/marvel-work/python/bin/python3.10` (`python3.10` nu
renvoie « Permission denied », `python3` système marche aussi mais n'est
pas la version documentée du projet).

**Reste à faire (non fait à ce stade, honnêtement à charge du prochain
passage) :**
- Étape F (images) : scans disponibles dans le scratchpad de session,
  jamais redimensionnés/posés dans `assets/pics/`.
- Étape G (bio `heros-info.js`, copie vivante).
- Étape H (textes FR `textes-fr-fanmade.ts`).
- Étape I (cas `test_capacites.py` + preuve par substitution) : AUCUN cas
  écrit. Priorité absolue si repris : le marqueur She-Devil
  (`rs001a`+`rs006`/`rs007`/`rs008`), le plus original et le moins couvert
  par un précédent du dépôt.
- Étape K (autoplay ciblé), L (test plateau pour rs011/rs018, qui posent
  des compteurs visibles), M (gabarits PROCESSUS-CARTE par carte), N
  (partie complète jouée à la main) : NON FAITES.
- Le dossier `Extras` du zip et l'art alternatif du héros restent hors
  scope (décision documentée plus haut).

Statut au 23/09/2026 : **A, A bis, B, C, D, J faits.** Pack chargé, deck
vert. E (nemesis json) volontairement sauté (facultatif). F, G, H, I, K, L,
M, N restent à faire — carte par carte, aucune n'est « terminée » au sens
strict de PROCESSUS-CARTE.

## Étape F (images) — FAITE, 23/09/2026

20/20 images posées dans `assets/pics/<card_id>.jpg`, redimensionnées
depuis les scans du scratchpad. 18 cartes JOUEUR/PERSONNAGE en 300×434
portrait (standard, vérifié contre `01001a.jpg`).

⚠ **Piège rencontré et corrigé sur les DEUX manigances (`rs009` Queen of
Sogaria, `rs015` Queen of the Frozen Wastes)** : leurs scans sources sont en
paysage (2150×1500, contenu lisible SANS rotation — vérifié en les affichant
brutes). Un premier essai les a forcées en 300×434 portrait avec rotation
manuelle (`rotate(-90)` puis `rotate(90)`, les deux essais rendant le texte
illisible/de travers). Corrigé après avoir vérifié le format de stockage
RÉEL d'une manigance secondaire OFFICIELLE (`01107.jpg` Breakin' & Takin' :
**435×300, paysage, telle quelle**) : les manigances gardent leur
orientation paysage native, contrairement aux cartes personnage. Les deux
fichiers refaits en 435×300 sans rotation, vérifiés visuellement lisibles.
⚠ **Contre-exemple trouvé dans le dépôt, à ne pas imiter** : `65011.jpg`
(Wave, side scheme némésis) est stocké en 300×434 portrait — soit une
erreur du portage Wave jamais remarquée (son scan source était peut-être
déjà portrait), soit un cas différent ; en cas de doute sur un futur
portage, vérifier contre une manigance OFFICIELLE comme `01107.jpg`, pas
contre un autre pack fan-made.

## Étape I (test_capacites.py + substitution) — DÉMARRÉE, mécanique la plus
## risquée du pack PROUVÉE, 23/09/2026

Deux cas ajoutés (`tools/test_capacites.py`, filtre `"rs006"` sur
`.game-src-par*`, interpréteur `~/marvel-work/python/bin/python3.10` —
`python3.10` nu refuse, `python3` système marche aussi) :
1. `rs001a She-Devil — joue rs006 Hyrkanian Fury a cout reduit,
   etourdissement applique` : la chaîne complète (Action → choix d'un
   événement en main → coût réduit → marqueur → effet conditionnel de la
   carte jouée) mesurée en une fois.
2. `rs006 Hyrkanian Fury joue normalement (sans She-Devil) — TEMOIN` :
   contre-cas, le même événement joué sans passer par She-Devil ne doit
   jamais étourdir.

**Deux bugs réels trouvés ET corrigés en écrivant ces cas** (aucun n'aurait
été vu par le chargement statique — §9 de PROCESSUS-CARTE) :

1. **`Puzzle.ChangeForm('rs001a')` en mise en place fabriquait une carte
   orpheline** (`AssertionError` dans `GetControlByPlayer`, au tout premier
   essai). Piège déjà documenté dans le journal Wave : `ChangeForm` prend
   l'id de la face ACTUELLEMENT ACTIVE (`rs001b`, alter-ego, forme de
   départ de tout héros) et la fait basculer vers l'autre — jamais l'id de
   la forme VOULUE. Corrigé en `Puzzle.ChangeForm('rs001b')`.

2. **`update_resources_cost` de `PlayCardsLikeInTurn` (player_action.py:937)
   attend une valeur NÉGATIVE pour réduire le coût**, jamais positive — le
   nom du paramètre suggère le contraire. `update_resources_cost=1` (signe
   positif, lecture naïve de « reduce by 1 ») AUGMENTAIT le coût de 1 au
   lieu de le réduire (mesuré via `TRACE_OPTIONS=1` : coût passé de 2 à 3,
   pas de 2 à 1). Confirmé en relisant TOUS les autres appels du dépôt à ce
   paramètre (`ant/12024.py`, `magneto/49017.py`, `sm/27054.py`,
   `vision/26036.py`, `bp/black_panther_shuri/51001b.py`, `jj/jessica_jones
   /61008.py`, `tt/enchantress/55012.py`) : **tous passent une valeur
   négative**, sans exception. Corrigé en `update_resources_cost=-1`.
   Documenté dans `red_sonja/__init__.py` pour que personne d'autre ne le
   repaie (candidat à ajouter dans `RECETTES-MOTEUR.md` si un futur portage
   utilise ce paramètre).

   Un premier réflexe a été d'écrire cet écart comme un bug MOTEUR (double
   négation dans `ReduceCostToPlayThis` → `ReduceCostToPlayFaceWhen` →
   `UpdateCostOfCardInternal`) : faux — la composition est correcte pour un
   appelant qui respecte la convention négative ; c'est l'appel de ce
   portage qui l'enfreignait. Vérifié avant de toucher au moteur
   (`[[corriger-le-moteur-plutot-qu-assumer-un-ecart]]`).

**Preuve par substitution FORMELLE faite sur le cas nominal** (23/09/2026) :
la ligne `if AUtiliseSheDevil(this):` de `rs006.py` neutralisée
(`if False and ...`) → cas 1 tombe ROUGE (« 01094 ne porte pas le statut
Stunned »), module restauré → repasse VERT. `verifier_tous_les_decks.py`
re-confirmé vert après restauration (`identite rs001b, main 6, deck 9`).

**Reste à faire, honnêtement à charge du prochain passage** : 18 cartes sur
20 n'ont encore AUCUN cas dédié (seuls rs006 et indirectement rs001a/rs013
via le montage sont exercés). Priorité suivante suggérée : rs007/rs008
(même marqueur She-Devil, branches distinctes), rs009/rs018 (mécaniques les
plus complexes restantes : granted-ability conditionnée à la vitrine de
victoire, et interruption de redressement avec compteurs). Étapes K
(autoplay), L (test plateau pour rs011 « stealth » et rs018 « fetter », qui
posent des compteurs visibles), M (gabarits PROCESSUS-CARTE), N (partie
complète) toujours NON FAITES.

Statut au 23/09/2026 (fin de session) : **A, A bis, B, C, D, F, G, H, J
faits. I démarrée (2/20 cartes avec cas réel + substitution formelle,
mécanique la plus originale du pack prouvée). K, L, M, N restent à faire.**
Aucune carte n'est « terminée » au sens strict de PROCESSUS-CARTE (qui
exige TOUTES les étapes, y compris autoplay et partie réelle) — à annoncer
clairement, pas à maquiller.

## Reprise du 23/09/2026 (après-midi) : étape I, les 18 cartes restantes

Feu vert de l'utilisateur (« tu peux continuer sonja ») après le déploiement
de la refonte du site. 24 cas ajoutés à `tools/test_capacites.py` (un ou deux
par carte restante, plus témoins d'épuisement/plafond) pour rs002 à rs019.
Plusieurs allers-retours contre le moteur réel (`.game-src-par7`/`-par8`,
`~/marvel-work/python/bin/python3.10`), quatre **vrais bugs** trouvés en
écrivant ces cas — aucun n'aurait été vu par le chargement statique :

1. **rs003/rs004 (`DegatsExcedentairesDeCetteAttaque`, `__init__.py`)** :
   `RegisterTemp(unregister_after_exec=True, until_resolve_effect=...)` sur
   une capacité `AfterUnitDefeatedUnit` (donc `is_delay_ability`) levait
   `AssertionError` (`face_effect.py:110`) DES QUE l'écouteur recevait
   vraiment un message — c'est-à-dire dès qu'un ennemi était réellement
   vaincu par l'attaque. Aucun cas antérieur n'avait fait mourir une cible
   via cette fonction. Corrigé : `unregister_after_exec=False` (le seul
   réglage légal pour ce type de capacité, le démontage passe par
   `until_resolve_effect` seul).
2. **rs009 (Queen of Sogaria)** : la Réponse « while in the victory display,
   Red Sonja gains... » était posée sur rs009 elle-même — une carte dans la
   vitrine est `is_out_of_play=True`, donc AUCUNE de ses propres capacités
   ne s'enregistre jamais, condition ou pas. Corrigée en la déplaçant sur
   l'identité (`rs001a.py` ET `rs001b.py`, les deux faces — `CardFace.
   GetAbilities()` n'est jamais partagé entre elles), fonction commune
   `CapaciteQueenDeSogariaEnVitrine` (`__init__.py`). Documenté en détail
   dans `RECETTES-MOTEUR.md` §3bis (nouveau).
3. **rs014 (A Warrior's Burden), branche 1** : `CostFunc.Discard(name=
   "Hyrkanium Blade")` sans `from_where` cherchait la carte EN JEU
   (`from_where=["Default"]` résout via `get_InPlay`, `selector_where.py:197`),
   jamais en main — la branche était donc TOUJOURS impayable, jamais
   proposée, sans le moindre message. Corrigé : `from_where=
   ["YourHandCards"]`. Documenté dans `RECETTES-MOTEUR.md` §5.
4. **rs016 (Ice Queen)** : `effect.GetInitiator()` PLANTE (`AssertionError`)
   au lieu de rendre `None` quand l'initiateur de la défaite n'est pas un
   joueur (ici, un coup non attribué à un joueur) — la garde `isinstance(
   joueur, Player)` du code appelant n'a alors jamais la moindre chance de
   s'exécuter, l'exception part avant. Corrigé avec l'accesseur dédié et
   SANS assertion de `Message.WhenUnitBeDefeated` :
   `message.GetKillerPlayer()` (rend `None` proprement).

**Trois pièges de harnais, propres à ce pack, documentés pour la suite** :
- **La forme de départ est ALTER-EGO** (`rs001b`, main 6), jamais Hero —
  toute carte « Hero Action »/« Hero Interrupt »/« Hero Response » jouée ou
  déclenchée HORS du montage She-Devil (qui bascule lui-même via
  `Puzzle.Action('rs001a', ...)`) exige `Puzzle.ChangeForm('rs001b')` en
  mise en place. Oublié sur les premiers jets de rs003/rs004/rs005/rs008/
  rs010/rs011/rs012/rs013/rs016 — corrigé partout.
- **`Puzzle.Damage(card, val)` sans `source` peut fabriquer un DOUBLON
  détaché** plutôt que de toucher l'instance déjà en jeu (constaté sur
  rs013 : la carte visée par un pré-dégât séparé n'encaissait jamais rien,
  aucune erreur, juste silence). Remplacé partout par de VRAIES attaques
  répétées (`Puzzle.Attack('rs001a')` + `Puzzle.Ready('rs001a')` entre
  deux), qui ont en prime l'avantage d'attribuer correctement le tueur
  (voir bug #4 ci-dessus).
- **Les vilains sont `Stalwart`** (`can_status.py`) : `canbe_confused=True`
  n'offre donc jamais Rhino comme cible légale — un sbire (`01101`) sert de
  cible pour toute carte qui inflige Confused/Stunned/Tough à un ennemi
  choisi.

**Réserve nommée, non résolue dans cette passe** : `rs007` Red Reckoning,
branche She-Devil active (« confuse an enemy »). Le `joueur.ChooseAbilities`
IMBRIQUÉ à l'intérieur du corps de l'Action, lui-même appelé depuis le
`PlayCardsLikeInTurn(forced=True)` de She-Devil, empêche SYSTÉMATIQUEMENT
rs007 d'être choisi/joué par ce montage (jamais dans la défausse, aucune
exception levée) — alors que la MÊME carte jouée normalement fonctionne
(cas témoin, vert), et qu'une AUTRE carte contre SANS choix imbriqué
(rs004) traverse le même montage She-Devil sans problème. Cause exacte non
identifiée dans le temps de cette passe (harnais ou moteur) : seul le cas
témoin (sans She-Devil, prouvant l'absence de confusion) est vert pour
rs007 ; la partie conditionnelle « confuse » reste NON PROUVÉE. À charge du
prochain passage.

**Réserve déjà connue, inchangée** : `rs008` Savage She-Devil, branche
« ignores guard/patrol/crisis si She-Devil » — non testée (nécessiterait de
vérifier l'enforcement exact du mot-clé Guard côté moteur).

## Clôture de la reprise du 23/09/2026 : I, J, K, L, M

**Étape I — 31/31 cas verts, 19/20 cartes prouvées par substitution
formelle.** Après la première fournée (24/26 cas verts) et plusieurs
corrections ciblées (formes alter-ego/héros, `Puzzle.Damage` sans source,
cibles Stalwart, ordre de mise en place), TOUS les cas de comportement sont
verts. La preuve par substitution (`tools/substituer_pack.py`, procédure
sûre avec sauvegarde + empreinte md5, confirmée identique après coup) a
ensuite trouvé 4 trous que le simple vert des cas ne montrait pas :
- `rs001b` (Sonja of Hyrkania) n'avait AUCUN cas — « Day of the Sword »
  jamais exercée. Cas neuf ajouté (`Puzzle.PutIntoDeck` pour garantir
  Hyrkanium Blade dans le deck, pas déjà en main par le tirage de départ).
  Substitution : rouge confirmé.
- `rs009` (Queen of Sogaria) : les deux cas existants, déplacés sur
  l'identité lors de la correction du bug de la vitrine de victoire, ne
  couvraient plus DU TOUT `ThreatCannotBeRemovedFromWhile` (le seul
  contenu restant sur `rs009.py` lui-même). Cas neuf ajouté (Conan, un
  allié, tente de contrer la manigance : la menace ne bouge pas).
  Substitution : rouge confirmé.
- `rs007` : le seul cas restant (le témoin sans She-Devil) ne prouvait
  qu'une ABSENCE (« pas de Confused ») — vraie AVEC ou SANS le module.
  Renforcé avec `menace` (valeur exacte après -4) et `defausse` : les deux
  tombent bien sans le module. Substitution : 1/1 rouge, **carte
  pleinement prouvée par substitution** (la branche confuse reste une
  réserve à part, voir plus haut — pas un problème de preuve mais
  d'atteignabilité du harnais).
- `rs004` : **RÉSERVE NON RÉSOLUE.** Même diagnostic que rs007 au départ
  (le cas ne prouvait rien de positif sur la réduction de coût si le module
  disparaît), mais la fermeture n'a PAS tenu : `ne_pas_depenser:
  ["rs007"]` devrait empêcher cette carte de servir de ressource pour
  payer rs004 lui-même, et ne le fait pas de façon fiable — constaté de
  façon REPRODUCTIBLE (3 relances identiques, même résultat, donc pas un
  hasard de tirage). Le MÊME mécanisme protège correctement rs006 dans le
  cas symétrique de rs003 (`ne_pas_depenser: ["rs006"]`), sans le même
  succès ici — écart non expliqué dans le temps de cette passe. La preuve
  POSITIVE du cas nominal (le contre lui-même, `hors_jeu` sur 01107) reste
  solide et vérifiée ; c'est spécifiquement la preuve par ABSENCE DE
  MODULE qui reste trouée (substitution : 0/1, la carte reste vert même
  stubbée).

**Deux bugs réels supplémentaires trouvés pendant la substitution et la
vérification des decks (étape J)**, en plus des quatre déjà listés plus
haut :
- **`RECETTES-MOTEUR.md` mis à jour** avec deux nouvelles entrées : §3bis
  (« while X is in the victory display, Y gains... » — la bonne cible est
  l'identité, jamais la carte source) et un ajout au §5 (`CostFunc.
  Discard` sans `from_where` cherche en jeu, jamais en main).
- Une fausse alerte notée pour mémoire : `verifier_tous_les_decks.py`
  (étape J) a d'abord affiché un `AssertionError` sur `rs006` dans
  `CardFactory.CreateFace` (liste blanche des capacités « Play ») —
  disparue après un simple nettoyage du `__pycache__` de `.game-src-par7`
  (bytecode compilé stale d'avant les derniers correctifs de
  `__init__.py`/`rs001a.py`/`rs001b.py`). Confirmé stable sur deux relances
  propres : `{"deck": "red_sonja", "ok": true, "message": "identite
  rs001b, main 6, deck 9"}`. **Étape J : FAITE, verte.**

**Étape K — autoplay ciblé : FAIT le 23/09/2026.**
`tools/autoplay.py .game-src-par7 --deck red_sonja --vilains rhino
--difficultes normal --profils equilibre --parties 8` → **8/8 parties, 0
traceback** (grep exhaustif des 8 journaux sur
`NameError|AttributeError|TypeError|KeyError|AssertionError|Traceback`,
confirmé à zéro partout). 0 % de victoires, **non représentatif** : comme
pour Wave, `player_deck` est intentionnellement vide (aucune decklist
d'aspect fournie par l'auteur), un deck de 15 cartes signature seules perd
structurellement. Les 8 parties se terminent toutes par « The Main Scheme
was Completed », pas par un plantage.

**Étape L — plateau : portée volontairement limitée, FAITE.** rs011
(compteurs `stealth`) et rs018 (compteurs `fetter`) reposent sur le
mécanisme GÉNÉRIQUE `Uses (N X counters)` du moteur, déjà exercé en
production par d'autres packs — pas re-testé ici (même logique que Wave,
qui n'a testé QUE sa zone maison neuve). **Ce qui EST neuf et a été
trouvé en écrivant le gabarit** : `ui-app/src/board/compteurs-fr.ts`
n'avait AUCUNE entrée pour `stealth` ni `fetter` — un joueur en français
aurait vu le mot anglais brut sur la carte. Corrigé (`stealth` →
« discrétion », `fetter` → « entrave ») et testé
(`compteurs-fr.test.ts`, 2 cas neufs, 5/5 verts). Hors de portée : capture
d'écran, session jouée à la main dans un navigateur.

**Étape M — gabarits PROCESSUS-CARTE : FAITE**, fichier séparé
`.planning/todos/2026-09-23-red-sonja-gabarits-processus-carte.md` (comme
Wave), un gabarit par carte × 20.

**Étape N — partie complète jouée à la main : HORS SCOPE**, gate sortie du
backlog du projet le 15/09/2026 (mémoire `[[parties-humaines-hors-
backlog]]`), non faite et non à faire dans cette passe.

## Statut au 23/09/2026 (avant fermeture des 3 dernières réserves)

**A, A bis, B, C, D, F, G, H, I, J, K, L, M faites. E (nemesis json)
volontairement sautée (facultative). N hors scope (sortie du backlog).**

**17/20 cartes « terminées » sans réserve au sens strict de PROCESSUS-CARTE**
(rs001a, rs001b, rs002, rs003, rs005, rs006, rs009, rs010, rs011, rs012,
rs013, rs014, rs015, rs016, rs017, rs018, rs019).

**3/20 avec une réserve nommée et documentée, pas maquillée** :
- `rs004` Scarlet Huntress — preuve par substitution trouée (voir détail
  ci-dessus), preuve positive solide.
- `rs007` Red Reckoning — branche She-Devil/confuse inatteignable par le
  harnais, cause non identifiée ; partie inconditionnelle prouvée, témoin
  pleinement prouvé par substitution.
- `rs008` Savage She-Devil — branche « ignores guard/patrol/crisis »,
  jamais testée ; partie inconditionnelle prouvée.

Six bugs réels du moteur/du pack trouvés et corrigés au cours de cette
passe (aucun n'aurait été vu par le chargement statique, exactement
l'avertissement du §9 de PROCESSUS-CARTE) : voir le détail complet plus
haut dans ce journal et dans `RECETTES-MOTEUR.md` §3bis et §5.

## Fermeture des 3 dernières réserves — 23/09/2026 (soir)

Feu vert de l'utilisateur (« tu finis tout tu ne t'arretes pas avant que les
deux heros soient parfait et jouables et sans erreurs »). **Les trois
réserves partageaient en réalité DEUX causes racines communes**, aucune
liée à une carte buguée :

**Cause racine 1 — vrai bug de harnais dans `ne_pas_depenser`
(`tools/test_capacites.py`)**, trouvé en creusant `rs004`. Le filtre
ajoutait, EN PLUS des vrais ids d'effets payants, l'id de l'OBJET CARTE
lui-même à la liste des interdits — déjà documenté comme inopérant par un
commentaire voisin (« les clés de `payment` ne sont jamais des ids d'objet
carte »), mais en réalité DANGEREUX par coïncidence : l'id objet de `rs007`
coïncidait EXACTEMENT, dans cette mise en place précise, avec l'id de
l'effet payant d'une carte totalement différente (`01089` Genius). Le
filtre excluait donc Genius en plus de rs007, sans rapport, et `rs004`
tombait injouable faute de paiement complet. **Corrigé : seuls les vrais
ids d'effets payants filtrent désormais** (`effet.object_id`, via
`is_paying`), l'ajout de l'id objet est retiré. Documenté en détail dans
`RECETTES-MOTEUR.md` §7sexdecies bis, avec le nom exact des cas concernés.
Six autres cas `ne_pas_depenser` d'autres packs (`vr006`, `bw004+bw005`,
`vz027`, `hc001a`, `65011`, `ip013`, `yd005`) revérifiés un par un après
coup : tous verts, aucune régression (le correctif ne peut que RETIRER un
faux positif d'exclusion, jamais en introduire un).

**Cause racine 2 — cible illégale dans les cas eux-mêmes**, pas dans les
cartes : « remove threat from a scheme » n'offre jamais le complot
PRINCIPAL comme cible légale à round 1, phase Joueur, avant toute phase
Vilain (il n'a encore reçu aucune menace). Les anciens essais visaient
`01097b` (complot principal) pour la seconde carte du montage : jamais
légal, d'où `jouable = False` sans le moindre message. Corrigé partout en
visant une manigance ANNEXE à la place (`01107`/`01108`, `StartingThreat`
non nul).

**`rs004` Scarlet Huntress — FERMÉE, OUI sans réserve.** Cas existant
corrigé : `payer_avec` couvre maintenant réellement le coût (harnais
réparé), cible du second contre = `01108` Crowd Control (pas le complot
principal). Preuve par substitution refaite et concluante (rouge sans le
module : `rs007` reste en main, injouable faute de coût réduit).

**`rs007` Red Reckoning — FERMÉE, OUI sans réserve.** Nouveau cas dédié
(« via She-Devil, branche confuse an enemy ») : She-Devil (rs001a) joue
rs007 à coût réduit, contre une manigance annexe (`01107`), PUIS un second
ASK distinct (« Confuse_an_enemy », `all_legal_targets=[Rhino, 01101]`)
confirme la branche conditionnelle réellement exercée — confusion posée sur
`01101` (un sbire, jamais Rhino : Stalwart bloque `canbe_confused`). Preuve
par substitution concluante (rouge sans le module : `01101` ne porte pas
Confused). L'ancien diagnostic (« ChooseAbilities imbriqué systématiquement
inatteignable ») ne résistait pas à l'épreuve : c'était la cible illégale du
CONTRE (cause racine 2) qui empêchait toute la carte d'être jouable avant
même d'atteindre la branche confuse.

**`rs008` Savage She-Devil — FERMÉE, OUI sans réserve.** Nouveau cas dédié
(« via She-Devil, ignore Guard ») : un sbire Guard (`01101` Hydra
Mercenary, engagé automatiquement à sa mise en jeu) bloque normalement
l'attaque du VILLAIN (`Minion.SetGuardPatrolEffectedBy`) — sans She-Devil,
Rhino ne serait pas une cible légale. Avec She-Devil,
`all_legal_targets=[Rhino, 01101]` confirme que Rhino REDEVIENT légal, et
les 5 dégâts tombent bien sur lui. Preuve par substitution concluante
(rouge sans le module : 0 dégât sur Rhino, cible retombée illégale).

**Suite complète re-vérifiée verte après les trois fermetures** :
`test_capacites.py` filtre `"rs0"`, **30/30 cas passés** (20 cartes, 2 cas
supplémentaires pour rs007 et rs008, plus les témoins d'épuisement/plafond
déjà en place). Autoplay ciblé rejoué : `tools/autoplay.py .game-src-par7
--deck red_sonja --vilains rhino --difficultes normal --profils equilibre
--parties 8` → **8/8 parties, 0 incident**, même profil qu'avant
(0 % de victoires, non représentatif — `player_deck` intentionnellement
vide, voir plus haut).

## Statut final au 23/09/2026 (soir)

**20/20 cartes « terminées » sans réserve au sens strict de
PROCESSUS-CARTE.** A, A bis, B, C, D, F, G, H, I, J, K, L, M faites. E
(nemesis json) volontairement sautée (facultative, décision documentée plus
haut). N (partie complète jouée à la main) hors scope, gate sortie du
backlog du projet le 15/09/2026 (mémoire `[[parties-humaines-hors-
backlog]]`) — **le pack est jouable et sans erreur connue au sens de tout
ce qu'un outil peut vérifier**, sans qu'une partie humaine complète ait été
jouée (décision de portée déjà actée, pas une omission).

Huit bugs réels trouvés et corrigés sur l'ensemble de cette passe (six
listés plus haut + le bug de harnais `ne_pas_depenser` + aucun bug de carte
supplémentaire pour fermer rs007/rs008, qui n'avaient besoin que de cas
mieux ciblés) : aucun n'aurait été vu par le chargement statique, exactement
l'avertissement du §9 de PROCESSUS-CARTE. Détail complet dans
`RECETTES-MOTEUR.md` §3bis, §5 et §7sexdecies bis.
