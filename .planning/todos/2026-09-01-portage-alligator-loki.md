# Portage du pack ALLIGATOR LOKI — journal de validation

Set 140, préfixe `al`, 24 `card_id` (al001a/b + al002-al023). Auteur
**Ripper3**. Aspect du deck de départ : **Agressivité** (choix de
l'utilisateur, 01/09/2026). Pack porté le 01/09/2026, en une traite, sur la
consigne « de A à Z, entièrement jouable ».

Gabarit `PROCESSUS-CARTE.md` par carte, comme l'exige la Gate finale de
`PROCESSUS-HEROS.md`.

---

## 0. Ce que le pack apporte, au-delà du héros

### Le héros devient un attachement (extension du moteur)

Lock Jaws attache **le héros lui-même** à un ennemi. Le moteur ne connaît
que des cartes attachées à des unités, jamais une identité attachée. Trois
modèles étaient possibles ; l'utilisateur a tranché pour **« étendre le
moteur : le héros devient l'attachement »**, sans déplacer physiquement la
carte du héros (« ça marche de mettre la carte héros ou pas ? » → non, seul
un lien logique + un marqueur visuel).

- `identity.py` : `Hero.attached_enemy`, `AttachHeroTo(face, effect)` (émet
  `WhenCardWouldAttachTo` / `AfterCardAttachTo` avec le héros en `trigger`),
  `DetachHero(effect)` (`AfterCardDetachFrom`), `GetHeldEnemy()`,
  `GetInfoDict` → `attached_to_enemy` (0/1).
- `base/enemy.py` : `GetHoldingHeroPlayerNumber()` (numéro du joueur, 0 =
  personne) → `GetInfoDict` → `held_by_hero`.
- Pack `cards/pack/alligator_loki/__init__.py` : `EstAccrocheA`,
  `AccrocherLeHeros`, `DetacherLeHeros(effect, joueur, *, force=False)` qui
  ouvre À LA MAIN la fenêtre « would detach » d'Unbreakable Grip (le moteur
  n'a pas de message « would detach »).
- Le malus continu « attached enemy gets -1 SCH / -1 ATK » se rafraîchit
  par `change_on_event=OnEvent.AttachedMove("This")` : sans cela, la liste
  des cibles n'était pas recalculée à l'accrochage et l'ennemi gardait ses
  chiffres imprimés (constaté aux cas 919/921, corrigé).

### Un type de carte neuf : `PlayerMinion`

Throg (al002) est un **sbire de joueur** : joué depuis la main contre son
coût, engagé avec son propriétaire, défaussé dans la pile du joueur
(`owner_original` = le joueur). Fichier `card_type/minion_player.py`,
`CanPlayThisMinionCard` dans `ability/factory/play.py`.

Piège moteur : `Minion` est un type **final** (`IsType` compare le type
exact), donc `has_guard.py:32 assert Minion.IsType(self)` plantait à
l'entrée en jeu de Throg. Extension générale dans `card_face.py` :
l'attribut de classe `also_final_types` permet à une sous-classe de se
réclamer d'un type final (`PlayerMinion.also_final_types = (Minion,)`).

### Le marqueur visuel (ui-app)

Exigence de l'utilisateur : « on doit clairement pouvoir voir à quel
ennemi on est attaché ». `card-model.ts` lit `info.held_by_hero` →
`mordu`, `info.attached_to_enemy` → `accroche` ; `ScanCard.tsx` marque les deux
cartes liées en VERT (`#22e07a`, la couleur du contour de l'illustration) :
halo sur le cadre des deux, pastille « Accroché » dans le bandeau du héros,
et sur l'ennemi **l'alligator lui-même**.

L'illustration a été fournie par l'utilisateur le 02/09/2026, et son
placement arbitré en trois questions : **accroché au bord droit**, tête en
bas (l'image l'est déjà, aucune rotation), haut de 1,15 largeur de carte,
débordant d'environ un tiers de sa largeur pour se lire comme accroché A la
carte et non posé DESSUS ; **halo vert, sans pastille texte** côté ennemi ;
**pastille + halo, sans seconde image** côté héros.

Deux contraintes ont dicté le montage :
- `.scan-frame` rogne son contenu (`overflow: hidden`) : le marqueur vit
  donc dans `.scan-visuel` (qui reçoit `position: relative`), la couche qui
  porte aussi le zoom au survol.
- le serveur du jeu ne sert que `.html/.js/.css` (liste blanche de
  `web_server.py`, un `.png` renvoie silencieusement « no image ») :
  l'image doit être INLINÉE. `assetsInlineLimit: () => true` s'en charge, et
  `npm run verifier-sortie` échouerait si un fichier image sortait. Le PNG a
  donc été rogné et ramené à 189x600 (1,1 Mo -> 21 ko) pour que le data URI
  reste raisonnable.

Tests : `morsure.test.ts` (modèle, 4 cas) et `ScanCard.morsure.test.tsx`
(rendu, 4 cas, assertions sur les CLASSES et non sur le texte, qui dépend de
la langue). Suite complète 481/481, `tsc` propre.

### Le harnais comptait DEF deux fois (`Puzzle.Defend`)

Constaté par substitution sur le cas « défense de base » d'al001a, resté
vert sans module : Shocker ATK 2 contre DEF 1 faisait 0 dégât.
`Puzzle._DeclareDefender` appelait `BasicDefense` sans lever
`has_declare_defender` ; le moteur reposait sa question, le pilote
défendait encore avec le même héros, et `can_attack.py` additionne les
`defense_messages`. Corrigé : `message.DeclareDefender` + inclinaison du
défenseur s'il était prêt. **Fichier moteur partagé** → batterie complète
(§4).

### `WhenPlayerSelectHero` n'est pas un Setup

Le Setup d'al001b cherchait Throg dans un deck qui n'existait pas encore :
cette fabrique tourne au choix du héros, AVANT la création du deck du
joueur (journal : « activates » ligne 5, « PlayerDeck<40> was created »
ligne 6). Le bon crochet est `AbilityFactory.WhenCardSetup("This", op)`.

### Emplacement des modules = `set_name`

`CardsDB.FindAbilities` cherche le module dans
`cards.pack.<pack>.<CleanName(set_name)>`. Time Out (al017) a
`set_name = "Alligator Loki"` (obligation du héros) et vivait dans
`alligator_loki_nemesis/` : aucune capacité en jeu. Déplacé dans
`alligator_loki/`, commentaire « EMPLACEMENT DU MODULE » dans le fichier.

### Le `set_aside` du fichier de deck n'existe pas pour le moteur

Vu en autoplay (graine 7) : Time Out révélée, mais aucune Frogjolnir
mélangée. `HeroDescriptor` (`scene/replay/hero.py`) n'a pas de champ
`set_aside` et `SelectIdentity` (`player_setup.py:213`) a la génération en
commentaire ; seul le chemin PUZZLE (`server_new_game.py:93`) verse un
set_aside, et c'est celui du harnais (`Puzzle.CreatePlayerAdditionalDeck`),
d'où un cas vert pour une carte absente en vraie partie. Correction :
`AbilityFactory.BeginGameWithSetAside(["al022"])` sur al001b (modèle
bt001b, 09001b, 46001b), et les deux cas qui créaient al022 à la main ne le
font plus. **Agatha Harkness avait le même défaut**, corrigé le 02/09/2026
(aa001b, témoin 0/2 sans la ligne). **Audit des 29 decks de départ à
`set_aside` non vide** : tous les autres créent bien leurs cartes (par
constante ou par `SetupPutIntoPlay`), et SP//dr est câblé dans le moteur
(`player_setup.py:197`). Il n'y avait que ces deux trous.

### Un Interrupt nu pose une question à chaque déclenchement

Throg (al002) filtrait « attacks Throg » DANS l'opération : le moteur posait
quand même la question « Throg ? » à chaque attaque du héros, Rhino compris,
pour ne rien faire ; le garde-fou anti-répétition de l'autoplay finissait
par bloquer la partie (graine 5, verdict « bloquée »). La condition va dans
la fabrique : `attack_targets="This"`.

### Homonymes

- **Throg** ×4 : al002 (sbire de joueur), al019 (sbire némésis), 25014
  (allié Agressivité de Valkyrie), lj019 (allié de Lockjaw). Recherches par
  `card_ids`, jamais par nom, sauf al019 « any OTHER Throg » et al018
  « can attack only Throg » qui visent bien le nom. L'allié 25014 est
  volontairement ÉCARTÉ du deck de départ (il brouillerait al018/al019).
- **Loki** : al010 support PERSONA vs vilain 21160-21164 et sbire 06028.
- **Honey Badger** : 43003 et wx003, même nom → `IsName`.
- **Lightning Bolt** : al020/al021 liées par `ability_link` à 02044.

---

## 1. Étapes de `PROCESSUS-HEROS.md`

| Étape | État | Preuve |
|---|---|---|
| 1. `data/cards.json` | ✅ | pack `alligator_loki`, 24 card_id ; checksum recalculé |
| 2. Scripts | ✅ | 16 modules (al004-006 → al003, al008 → al007, al015-016 → al014, al020-021 → 02044 par `ability_link` ; al022/al019 côté némésis) ; `test_cards` **5021 ok / 0 err** |
| 3. Deck de départ | ✅ | `deck/starter/alligator_loki.json`, Agressivité, `set_aside` = al022 Frogjolnir, al023 hors deck (Team-Up injouable en solo) |
| 4. `data/nemesis/alligator_loki_nemesis.json` | ✅ | al018, al019, al020, al021 |
| 5. `data/sets_info.json` | ✅ | « 140. Custom (Alligator Loki) » |
| 6. Images | ✅ | 24 png dans `assets/pics/` |
| 7. Biographie | ✅ | entrée `al001a` dans `heros-info.js` (FR + EN) |
| 8. Texte français | ✅ | 24 entrées dans `textes-fr-fanmade.ts` |
| 9. Validation carte par carte | ✅ | §2 : **32/32 cas verts**, 16/16 cartes rouges par substitution (4 cas verts expliqués) |
| 10. Signature d'un autre héros | ✅ | `tools/prefixes_fanmade.json` entrée `al` ; aucune carte étrangère dans le deck (Throg 25014 écarté sciemment) |

---

## 2. Gabarits par carte

Preuve : `BILAN : 32/32 cas passes` (`/tmp/capacites-al.json`, cas 919-950
du harnais) ; substitutions par `tools/substituer_pack.py` :
**16/16 cartes** avec au moins un cas rouge sans leur module.

Toutes les cartes ci-dessous ont leur **carte de référence (étape 2)**,
leur **bloc texte-contre-code (5)** dans l'en-tête du module, leurs
**nombres (6)**, leur **cas sujet (7)** et l'**autoplay (8)** du §3.

### al001a * Alligator Loki (héros) — Carte terminée : OUI
Références ho005/an002 (malus continu par `CardFinder(check_effect_fn)`),
19005/dd010 (Interrupt sur pouvoir de base), bt004
(`AfterEnemyActivationEnd`, l'ennemi est `message.trigger`, pas `.this`).
Mots-pièges : « ATTACHED enemy » (identité d'objet, pas le nom), « BASIC
attack or defense » (Chomp! n'est pas un pouvoir de base), « Interrupt »
nu (le joueur peut refuser de mordre), « after attached enemy ACTIVATES »
(attaque OU manigance). **Arbitrage** : la Forced Response passe par la
fenêtre de la Grip (`DetacherLeHeros` sans `force`) : un effet de
remplacement s'applique à un effet forcé, c'est la raison d'être de la
carte. **Arbitrage défense** : l'accrochage en défense a lieu PENDANT
l'activation de l'ennemi ; la Forced Response détache donc aussitôt. Lock
Jaws en défense vaut une réduction de dégâts, pas une prise durable. Cas :
4 (attaque, défense, activation qui lâche, autre ennemi qui ne lâche pas),
rouges 3/4 : le cas « défense » reste vert sans module (0 dégât par DEF 1
contre ATK 2… voir §0, corrigé dans le harnais, puis 0 dégât par Lock Jaws
seul ; sans module il ferait 1 dégât, la nouvelle passe le prouvera).

### al001b * Alligator Loki (alter-ego) — Carte terminée : OUI
`BeginGameWithSetAside(["al022"])` (voir §0), Setup an001b/mw001b via
`WhenCardSetup` (voir §0), Nap Time =
`AfterUnitChangeForm(to_this_form=True)` (12016) + `BasicRecover` sans
inclinaison. « Find Throg » → al002 par `card_ids`. Détachement avec
`force=True` : Nap Time se résout après le passage en alter-ego, la Grip
(« HERO Interrupt ») ne peut plus parler. Rouges 2/2.

### al002 * Throg (sbire de joueur) — Carte terminée : OUI
Type neuf `PlayerMinion` (§0). `Patrol` = base automatique (fiche
mots-clés) : Throg empêche SON propriétaire de contrer le complot
principal, c'est un coût. Overkill donné à l'attaque en cours par
`message.property` (dd004/01053), déclenchement restreint par
`attack_targets="This"` (voir §0). En autoplay le héros attaque parfois son
propre Throg et Lock Jaws s'y accroche : Throg est un sbire, donc « that
enemy », c'est cohérent avec la combo overkill de la carte. « When Defeated » (jj013) → -3 menaces
puis remélange dans le deck du joueur Alligator Loki (an014). Rouge 1/1 :
overkill 1 sur Rhino, menace -3, Throg dans le deck.

### al003 / al004 / al005 / al006 Chomp! — Carte terminée : OUI
al004-006 par `ability_link` vers al003. Références dd004/01053 (attaque
d'événement), gp002 (« if this attack defeats »). Mots-pièges : « THAT
enemy » (6 dégâts seulement si accroché à la cible), « OTHERWISE, you may
attach » (facultatif, seulement si l'ennemi survit), « ready Alligator
Loki » (le héros). Cas : 3 (4 dégâts + accrochage facultatif, 6 dégâts
accroché, redressement sur défaite), rouges 3/3. Coût 2 : main
`["01090","01088"]` dans les cas.

### al007 / al008 See You Later! — Carte terminée : OUI
al008 → al007. 01085 (contre d'événement), ag005 (bascule alter-ego).
Ordre strict des trois phrases ; « you MAY shuffle Throg » facultatif
(`MayChooseOneAbility`), la bascule obligatoire. Rouge 1/1.

### al009 Alligator Antics — Carte terminée : OUI
bw021 (find + put into play), 45134 (attachement posé depuis hors jeu),
`Search.SearchForCard(include_player_deck="All")`. **Arbitrage « quel
Throg ? »** : les deux (al002, al019), le joueur choisit ; c'est un
détournement (donner l'attachement de rencontre à un Throg inoffensif).
**Arbitrage « attachment that CAN be attached to a minion »** : le moteur ne
lit pas la cible d'un attachement hors jeu ; tout `Attachment` accepté par
`CanAttachTo(throg)` est proposé, le joueur lit la carte comme sur table.
Cas : 2 (redressement + Throg en jeu sans attachement compatible ;
Frogjolnir trouvé et posé, AERIAL). Rouges 2/2. Piège du harnais :
`CreateEncounterDeck` AJOUTE au deck de Rhino, qui garde ses propres
attachements → `"cibles": ["al022"]`.

### al010 * Loki — Carte terminée : OUI
10008 (bonus continu d'un support), ma006 (`trait=`). « Alligator Loki
GAINS the trait » sur les DEUX faces (`Identity`), « while in hero form
+1 THW » sur `Hero` seul ; [wild] = `Resources("G")`. Rouge 1/1.

### al011 * Butterfly Swamp — Carte terminée : OUI
10008 (+1 REC en alter-ego, `card_type=AlterEgo`), 01092 (action payée par
inclinaison), 01067 (pioche). Mélange D'ABORD, pioche ENSUITE ; sans carte
PREPARATION en défausse la flèche est payée et on pioche quand même.
Rouge 1/1.

### al012 Gator Aid — Carte terminée : OUI
bw003 (« uses a basic power » = ATK/THW/DEF), bt008 (`GainATKForThisAttack`
& co), capacité temporaire sur `message.end_event` pour « after this use »
+ `MayChooseFace` pour le déplacement facultatif. Inclinée, elle ne se
déclenche plus (la flèche est un coût). Rouge 1/1.

### al013 Unbreakable Grip — Carte terminée : OUI
ma006 (+1 ATK en forme héros). **La seconde capacité vit dans
`DetacherLeHeros` (pack `__init__`)** : aucun message « would detach »
n'existe, la fenêtre est ouverte à la main, la Grip prête et en jeu y est
proposée (Interrupt nu, facultatif). Cas : 3 (+1 ATK ; activation de
l'ennemi tenu → Grip inclinée, héros toujours accroché ; Grip déjà
inclinée → détachement). Rouges 2/3 : le troisième est un CONTRE-CAS
(absence d'effet), vert sans module par construction. Cible Rhino dans
les deux cas d'activation : ATK 2+1 tuerait Shocker.

### al014 / al015 / al016 Lurking — Carte terminée : OUI
al015-016 → al014. an006 (`CostFunc.Discard("This")`), bw024 (attaque de
base sans inclinaison), 19029/16117 (+1 ATK pour cette attaque),
`AfterCardEnterPlay(HeroResponse, Minion)`. « Max 1 per player » =
`MaxPerUnit` de `desc`. « A minion » sans « engaged with you » : un sbire
entré chez un autre joueur déclenche aussi. Rouge 1/1.

### al017 Time Out (obligation) — Carte terminée : OUI
32055 (`WhenThisObligationGiveToYou`), aa017 (malus continu), 56023
(`CostFunc.Exhaust("YourIdentity")`), ab016 (`ShuffleAllTo` deck de
rencontre). « -2 ATK WHILE IN HERO FORM » → cible `Hero`. « Remove from
the game ». Module dans `alligator_loki/` (voir §0). Cas : 2 (Frogjolnir
mélangée + -2 ATK ; retrait de la partie), rouges 2/2.

### al018 Throg and Loki (complot némésis) — Carte terminée : OUI
40168a (« X can attack only Y » par nom), an015
(`Search.EncounterCard(include_discard_pile=True)`), an011
(`WhenThisRevealed` sur `SchemeSide2`). Hazard 1 lu dans `desc`. La
restriction ne vise que l'attaque : contrer et défendre restent libres.
Cas : 2, rouges 2/2.

### al019 * Throg (sbire némésis) — Carte terminée : OUI
22028 Gamora (« discard any other X »), 09029/dz014 (`PlaceCardHere`
face cachée), 50104a (`Rand.RandomChoice`), 33027 (`ReturnToHand` au
propriétaire). « ANY other Throg » = al002 aussi, par NOM (c'est le sens de
la carte). Placement APRÈS l'entrée en jeu (`PlaceCardHere` refuse hors
plateau). « When Defeated » seulement : défaussé autrement, il ne rend
rien. Cas : 2, rouges 1/2 : « vaincu, la carte revient en main » reste
vert sans module car sans le module rien n'est placé sous lui… et
`main_contient` la trouve toujours en main. Cas de DONNÉES assumé ; la
capacité est prouvée par le premier cas (carte placée, al002 défaussé).

### al020 / al021 Lightning Bolt — Carte terminée : OUI
`ability_link` vers 02044 Power Drain, texte identique. Cas : 1 (deck
`'01101','01099','01099'` → 2 boosts → 2 dégâts indirects, + Rhino),
vert. Pas de substitution possible (aucun module propre).

### al022 * Frogjolnir (attachement némésis) — Carte terminée : OUI
42027 Harpoon's Harpoon (`AttachToFaceWhenPutIntoPlay` +
`if_cannot_operation`), 45164 (`DoActivate` contre vous),
`GiveKeywordToAttached(Minion, trait="AERIAL")`, `AfterUnitAttackYou`.
Ordre `attachment.py:14-22` : attache d'abord, « When Revealed » ensuite,
donc « Then, Throg activates » en `WhenThisRevealed`. Vit dans le
`set_aside` du deck de départ, Time Out la mélange. Cas : 2 (Throg absent :
trouvé, révélé, armé, AERIAL, activation ; Forced Response +1 indirect).
Rouges 2/2. Héros INCLINÉ dans les deux cas, sinon le pilote défend et
Lock Jaws retire 1.

### al023 Little Rascals (Team-Up) — Carte terminée : OUI
12020/51025 (`.SetTarget("TeamUp")`, clé `TeamUp` de `desc`, fiche
`mots-cles/teamup.md` complétée), `Faces.GiveStatus` ×2. **Arbitrage « if
you cannot »** : on tente les deux statuts ; si l'un des deux n'a pas pu
être posé, redressement. Cas : 3 (sonné + désorienté ; vilain déjà sonné →
redressement ; sans Honey Badger, injouable). Rouges 2/3 : le troisième
est un contre-cas (injouabilité portée par `desc`, pas par le module).
Hors deck de départ (injouable en solo).

---

## 3. Autoplay ciblé (étape 8)

8 parties contre Rhino (normal, équilibré), le 01/09/2026, trois passes :

| Passe | V | D | %V | rounds | incidents |
|---|---|---|---|---|---|
| 1 (avant correctifs) | 0 | 7 | 0 % | 4,4 | **1 bloquée** (Throg, §0) |
| 2 (Throg corrigé) | 0 | 8 | 0 % | 4,8 | 0, mais Frogjolnir jamais mélangée (§0) |
| 3 (al001b corrigé) | 0 | 8 | 0 % | 4,4 | 0 |

- **Grep des 8 journaux** (`Traceback|NameError|AttributeError|TypeError|
  KeyError|AssertionError`) : **0**.
- Le 0 % est la norme du bot contre Rhino (Agatha, Harry Osborn, Venompool
  témoin : 0 % aussi).
- Vu en jeu réel : Lock Jaws (58 accrochages / 34 détachements), Chomp!,
  Throg al002 (joué, attaqué avec overkill), Unbreakable Grip, Gator Aid,
  Lurking, Alligator Antics, See You Later!, Butterfly Swamp, Loki, Time Out
  (révélée puis retirée par l'action alter-ego), Throg and Loki, Frogjolnir
  mélangée dans le deck de rencontre (3 parties) et défaussée par Looking
  for Trouble (1). Jamais vus : Nap Time (le bot ne repasse pas en
  alter-ego), Frogjolnir révélée, Throg al019 en jeu, Little Rascals (hors
  deck). Leurs preuves sont les cas du §2.

---

## 4. Batteries finales

- `test_capacites` filtré `al0` : **32/32**.
- Substitutions : **16/16 cartes** rouges, 4 cas verts expliqués au §2.
- `test_cards` : **5021 ok / 0 err**.
- ui-app : `tsc --noEmit` propre, `morsure.test.ts` + `pv-max.test.ts`
  10/10.
- Batterie complète (fichiers PARTAGÉS touchés : `card_face.py`,
  `identity.py`, `base/enemy.py`, `card_type/__init__.py`, `paper.py`,
  `play.py`, `puzzle.py`, le harnais) : **945/951** (`/tmp/capacites-full.json`).
  Les 6 rouges : sg006, sg007, sg009, sg013 (préexistants, cf.
  `2026-08-31-cas-rouges-sg-ss.md`) et lj024, mf010, dont l'attendu avait
  été passé de 3 à 4 par un remplacement trop large dans le commit 3f2819d
  (le nom des cas dit « 3 dégâts », le moteur en fait 3) : attendu remis à
  3, les deux repassent. **0 régression** des 24 cas `Puzzle.Defend`.
- `tools/audit_cartes.py` : 0 discordance pour le pack, 0 module en erreur.
- Passe finale après les correctifs du §3 : `al0` **32/32**, `test_cards`
  **5021 ok / 0 err**.

---

## 5. Ce que ces contrôles ne peuvent pas voir — reste à faire

- **Une vraie partie jouée à la main** (gate finale) : non faite.
- **Le marqueur à l'œil, en vraie partie** : le rendu n'a été vérifié que sur
  une page de démonstration reprenant le CSS réel, jamais sur le plateau.
- **ui-app déployée** (`deployer.sh`, 01/09/2026) ; survol de la biographie
  et du marqueur en vraie partie : à faire à l'œil.

- **Little Rascals en multijoueur réel** avec X-23 : prouvée par cas,
  jamais vue en partie.
