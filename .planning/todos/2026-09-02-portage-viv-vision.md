# Portage Viv Vision (set 147, préfixe `vv`) — journal

Pack fan-made de **Rainy**, vague 0 du deuxième arrivage. Zip
`Viv Vision-20260902T074028Z-1-001.zip`, 21 images, **12 card_id**.
Dossier de préparation : `2026-09-02-prep-vague0-viv-vision.md`.

## 1. Les quatre arbitrages de l'utilisateur (02/09/2026)

Posés un par un, en multichoix, **avant** d'écrire la première ligne de script,
comme l'exige l'étape 3 du `PROCESSUS-CARTE`.

| Question | Décision |
|---|---|
| Q1 — mot-clé maison `breakthrough`, défini nulle part | **Miroir d'`overkill` pour la menace** : l'excès se reporte sur une AUTRE manigance, au choix du joueur. Confirmé après coup par la définition communautaire (voir §2). |
| Q2 — aucune carte némésis dans le zip | **Modulaire officiel Zzzax** (Ironheart, `29036`-`29040`), ce que Rainy recommande d'après la critique BGG du pack. |
| Q3 — aucune decklist d'aspect fournie | **Protection**. |
| Q4 — sous-dossier « Vivian alt cards » | **Écarté**, version de base seule. |

## 2. Ce que la préparation annonçait, et ce que les scans disent

Trois écarts relevés en relisant les 12 scans un par un.

- **`breakthrough` n'est pas « 0 occurrence »** dans `data/cards.json` : trois
  cartes s'appellent *Breakthrough* (`40125` traîtrise Juggernaut, `jj003` et
  `61005` événements Jessica Jones). Aucune ne définit un mot-clé, le fond de
  la remarque tient, la lettre non.
- **Sparky the Dog porte une étoile VERTE**, donc `RES = "G"` (wild), et non
  une ressource physique comme annoncé. Vérifié par comparaison du coin
  inférieur gauche avec les autres cartes du même pack (leçon Lockjaw).
  Conséquence en jeu : Sparky n'est **pas** repêchable par le Recharge de
  `vv001b`, qui exige une énergie IMPRIMÉE.
- **Les « Vivian alt cards » ne sont pas de l'art alternatif.** L'illustration
  est identique ; c'est le TEXTE qui change : identité renommée « Vivian »,
  trait CIVILIAN ajouté à l'alter-ego, et limite « once per POWER per round »
  au lieu de « once per round », soit trois activations au lieu d'une. C'est
  une variante de RÈGLES, écartée sur décision de l'utilisateur.

**Définition retenue de `breakthrough`**, transmise par l'utilisateur depuis la
*Marvel Champions Home Brew Master List* : « When this attack defeats an enemy
or this thwart clears a scheme, excess damage or threat removal is
dealt/removed from another eligible target. » Recherche faite avant de
l'obtenir : absente de Hall of Heroes, des règles MarvelCDB, du thread BGG du
pack et de la feuille Google publique du Master List. Fiche complète :
`docs/reference/mots-cles/breakthrough.md`.

## 3. Deux fichiers moteur PARTAGÉS touchés

La règle de portée du §6bis du `GUIDE-CREATION-CONTENU` s'applique donc : les
105 decks et la batterie complète de `test_capacites.py` sont dus, pas
seulement le pack.

- `src/game/card/face/model/face_action.py` : `TemporaryGain` et
  `GainUntilRoundEnd` ne passaient pas `stalwart` à `Gain`, qui l'accepte
  pourtant (`face_gain.py:23`, appliqué en `face_gain.py:141`). **Troisième
  occurrence du même oubli**, après `retaliate` (4/8/2026) et `villainous`
  (1/9/2026). `vv004` Phase Up est le PREMIER stalwart temporaire du dépôt :
  les ~30 autres cartes qui l'accordent le font par attachement permanent,
  d'où l'angle mort.
- `src/game/card/factory.py` : `vv005` Solar Beam ajoutée à la liste blanche
  des événements à deux capacités `Play`, juste après son homonyme officiel
  `26008` qui y figure déjà pour la même raison.

## 4. L'écart assumé du pack : `vv003` Just a Phase

La carte imprime « **Hero Interrupt** : quand votre héros effectue une menée de
base, +3 CTR, ignorez patrol et l'icône de crise, et cette menée gagne
breakthrough ».

Le moteur vérifie **`patrol` au choix de la cible**, pas à la résolution :
`can_be_thwart_schemes` est posé sur le filtre du sélecteur (`ability.py:970`)
et appelle `MainScheme.CanBeThwartBy` (`scheme_main.py:204`). La fenêtre
d'interruption, elle, ne s'ouvre qu'après, dans `ThwartInternal`
(`can_thwart.py:103`). Une interruption fidèle au mot imprimé n'aurait donc
**jamais** pu lever patrol : avec un sbire Patrol engagé, le complot principal
n'apparaît même pas dans la liste des cibles. `crisis`, lui, est vérifié à la
résolution (`scheme_main.py:151`) et aurait fonctionné en interruption.

**Décision de l'utilisateur** : rendre la carte comme `61023` Grapnel Launcher,
la seule carte du dépôt qui ignore patrol — elle EXÉCUTE la menée elle-même.
`BasicThwart` produit une vraie menée de base, donc tout ce qui réagit à une
menée de base continue de se déclencher. L'épuisement du héros est ajouté en
coût, parce que `61023` imprime « without exhausting » et pas `vv003`.

**Perte assumée, la seule** : en interruption, la carte aurait pu bonifier une
menée de base offerte par une AUTRE carte. En action, elle ne bonifie que la
sienne. Aucune carte du kit de Viv n'offre ce cas.

Conséquence sur le texte : `data/cards.json` garde le texte IMPRIMÉ (règle du
processus), mais `textes-fr-fanmade.ts` décrit ce que la carte fait RÉELLEMENT,
pour ne pas promettre au joueur un déclencheur qu'il ne verra jamais.

## 5. Deux pièges payés dans le harnais de test

- **Le pilote compte les ressources en QUANTITÉ, pas en couleur.** `01088`
  Energy porte « YY » : elle couvre à elle seule un coût de 2, le pilote
  s'arrête là, et un `Requirement ([energy][mental])` n'est alors PAS
  satisfait — la carte est jouée, défaussée, et son effet échoue **en
  silence** (`<E> ... failed`). Les cas de `vv002` et `vv008` emploient donc
  `01082` Indomitable (Y) et `01081` Armored Vest (B), une icône chacune.
  `payer_avec` ne suffit pas : la troncature se fait sur le poids.
- **Deux capacités `Play` sur la même carte** : le moteur les nomme « Play »
  et « Play_1 ». Sans `choisir_option: "Play_1"`, le pilote prend toujours la
  première — le cas « menée » de `vv005` testait en réalité la branche attaque.

## 6. Gabarits PROCESSUS-CARTE, une fois par carte

Étapes communes à toutes : **étape 1** entrée dans `data/cards.json` (pack
`viv_vision`, en queue de fichier, checksums recalculés) ; **étape 4** image
`assets/pics/<card_id>.jpg` déposée depuis le zip. ⚠ Sur ces scans, `0.1` est
l'**alter-ego** et `0.2` le **héros**, l'inverse de l'ordre habituel.

### vv001a : ★ Viv Vision (face héros)

- [x] Étape 2 : `01068` ★ Vision (allié Core), texte quasi identique ; `ag001b`
      pour `SetName` + `LimitOncePerRound`. **Pas** `26001a`, sans rapport.
- [x] Étape 5 : mots-pièges vérifiés : « YOU get » (identité, pas la face —
      `ignore_flip=True` par défaut), « a chosen BASIC power » (les TROIS :
      THW/ATK/DEF, là où 01068 n'en offre que deux), « until the end of the
      ROUND » (`GainUntilRoundEnd`, pas `GainUntilPhaseEnd`), « Limit once per
      round ». Résultat : conforme.
- [x] Étape 6 : THW 1 / ATK 1 / DEF 1, HS 5, PV 10, +2, limite 1/round —
      identiques sur le scan, dans `desc` et dans le script. Résultat : conforme.
- [x] Étape 7 : 1 cas, `vv001a Density Manipulation`. Substitution : voir §7.
- [ ] Étape 8 : autoplay — voir §8.

### vv001b : ★ Viv Vision (face alter-ego)

- [x] Étape 2 : `ag001b` ★ Sharon Carter (même auteur), même forme exacte
      (Action limitée 1/round qui choisit dans une pile et repose sur un deck) ;
      `al007` pour la lecture de sa propre défausse.
- [x] Étape 5 : « a PRINTED [energy] resource » (couleur imprimée, wild NON
      converti — `checker.py:436`), « in YOUR discard pile » (écart avec
      ag001b, qui vise la défausse de rencontre), « ON TOP of your deck »
      (argument positionnel, pas `to_top=`), « Choose » sans « you may ».
      Résultat : conforme.
- [x] Étape 6 : REC 3, HS 6, PV 10, limite 1/round. Résultat : conforme.
- [x] Étape 7 : 2 cas — le cas nominal et un **contre-cas** prouvant qu'une
      carte wild n'est PAS repêchable. Substitution : voir §7.
- [ ] Étape 8 : voir §8.

### vv002 : Hologram Projection

- [x] Étape 2 : `27006` Web Binding (annulation d'activation, et elle porte
      elle aussi un Requirement) ; `01083`/`05015` pour la pose de statut.
- [x] Étape 5 : « an ENEMY » (vilain ET sbires, aucun filtre de type),
      « cancel THAT activation » (`SetBeInstead`, pas une interdiction
      durable), « confuse THAT enemy » (`message.trigger`, jamais un choix).
      `Requirement` : **aucun script**, base automatique. Résultat : conforme.
- [x] Étape 6 : coût 2, Requirement [energy][mental] = `"YB"`. Aucun autre
      nombre imprimé. Résultat : conforme.
- [x] Étape 7 : 1 cas. Substitution : voir §7.
- [ ] Étape 8 : voir §8.

### vv003 : Just a Phase

- [x] Étape 2 : `61023` Grapnel Launcher (seule carte du dépôt qui ignore
      patrol) ; `20013` Making an Entrance (effet de suite branché sur la
      menée) ; `08013` Stealth Strike (choix d'une seconde manigance).
- [x] Étape 5 : « THEY get +3 THW » (le héros, `additional_value=3`), « for
      THAT thwart » (borné à cette menée par construction), « ignore patrol
      AND crisis » (les deux, et `.SetLabel('thwart')` n'est pas cosmétique :
      `IsIgnoreKeyword` refuse 'Patrol' hors `is_like_thwart`,
      `effect.py:491`), « ANOTHER eligible target » (`exclude=` + `has_threat`).
      **Écart de déclencheur documenté au §4.** Résultat : conforme au §4 près.
- [x] Étape 6 : coût 1, +3. Résultat : conforme.
- [x] Étape 7 : 2 cas — le breakthrough (excès reporté) et l'icône de crise
      ignorée. Substitution : voir §7.
- [ ] Étape 8 : voir §8.

### vv004 : Phase Up

- [x] Étape 2 : `03005` Shield Block (et **non** `01003` Backflip, qui filtre
      sur l'attaque) ; `dd001a` pour un mot-clé accordé jusqu'à la fin du round.
- [x] Étape 5 : « ANY AMOUNT of damage » (pas de `is_from_attack`, c'est tout
      l'écart avec Backflip), « PREVENT ALL » (`"All"`, pas un chiffre), « YOU
      gain stalwart » (l'identité, via `message.trigger`), « until the end of
      the ROUND ». Ordre imprimé respecté. Résultat : conforme.
- [x] Étape 6 : coût 1, Requirement [energy]. Résultat : conforme.
- [x] Étape 7 : 1 cas, avec sonde dédiée (`etat_attendu` ne sait pas lire
      `stalwart`, absent de la table `IMPRIME`). Substitution : voir §7.
- [ ] Étape 8 : voir §8.

### vv005 : Solar Beam

- [x] Étape 2 : `26008` Solar Beam, son homonyme OFFICIEL (même structure à
      deux `Play`) ; `ag003`/`41030` pour le ranged ponctuel.
- [x] Étape 5 : « THIS ATTACK gains ranged » (branche attaque seule,
      `AttackProperty(ranged=True)` et jamais `message.GainRanged`, qui
      donnerait ranged à l'ennemi), « to AN enemy » / « FROM A scheme » (une
      cible chacune), deux `Hero Action` (sous-type dédié). Résultat : conforme.
- [x] Étape 6 : coût 2, 5 dégâts, 4 menaces, Requirement [energy]. Résultat :
      conforme.
- [x] Étape 7 : 2 cas, un par branche. Substitution : voir §7.
- [ ] Étape 8 : voir §8.

### vv006 : Superdense Strike

- [x] Étape 2 : `56017` Savage Strike (modèle exact du couple bonus+mot-clé sur
      sa propre attaque de base). **Pas** l'homonyme officiel `26009`.
- [x] Étape 5 : « AGAINST AN ENEMY » (codé, d'où l'appel direct à
      `WhenUnitWouldAttack` : `WhenUnitMakeAttack` n'expose pas
      `attack_targets`, paramètre commenté en `do_attack.py:84`), « for THAT
      attack », « THAT ATTACK gains piercing » (sur l'attaque, pas le
      personnage), « Give YOUR HERO a tough status card » (troisième phrase
      sans flèche : un effet, pas un coût). Aucun Requirement imprimé sur
      cette carte : aucun n'a été inventé. Résultat : conforme.
- [x] Étape 6 : coût 2, +4. Résultat : conforme.
- [x] Étape 7 : 1 cas, qui prouve AUSSI le piercing (Rhino reçoit une carte
      Tenace au préalable). Substitution : voir §7.
- [ ] Étape 8 : voir §8.

### vv007 : ★ Sparky the Dog

- [x] Étape 2 : `18015` First Hit (déclencheur « minion initiates an attack ») ;
      `sr010` (lecture de `message.attacker`) ; `aa003` Ebony (Alter-Ego Action
      payée par épuisement) ; `sd013` (déclaration explicite de
      `CanPlayThisSupportCard`).
- [x] Étape 5 : « a MINION » (jamais le vilain), **pas de « against you »**
      imprimé donc pas de `against_player="You"`, « to THAT minion », la flèche
      qui fait de l'épuisement un coût, « from YOUR IDENTITY ». Résultat :
      conforme. **Ressource corrigée : `RES = "G"`, voir §2.**
- [x] Étape 6 : coût 1, 2 dégâts, soin 1. Résultat : conforme.
- [x] Étape 7 : 2 cas, un par capacité. Substitution : voir §7.
- [ ] Étape 8 : voir §8.

### vv008 : Computer Mind

- [x] Étape 2 : `AfterPlayerPlayedCard` (`play.py:310`) ; `ho006` pour la
      famille « réagir à la carte qu'on vient de jouer » ; la fiche
      `mots-cles/requirement.md` pour la lecture de `face.requirement`.
      **Aucune autre carte du dépôt ne LIT le mot-clé Requirement** : les ~30
      qui l'impriment ne comptent jamais les ressources exigées d'une autre
      carte. D'où la lecture directe de `face.requirement.val`.
- [x] Étape 5 : « a card that HAS THE REQUIREMENT KEYWORD » (`requirement.val
      > 0`, et non « coûte des ressources »), « for each REQUIRED RESOURCE »
      (le nombre d'icônes exigées, jamais le coût), « that card »
      (`message.played_face`), « AFTER you play » (jamais `WhenPlayerPlayCard`),
      « YOU play » (filtre `"You"`), `Response` nu et non `Hero Response`
      (donc jouable aussi en alter-ego). Résultat : conforme.
- [x] Étape 6 : coût 1, « 1 card for each ». Résultat : conforme.
- [x] Étape 7 : 1 cas, qui prouve le « **for each** » et pas seulement le
      déclenchement : `vv002` exige deux ressources, donc DEUX cartes piochées.
      Substitution : voir §7.
- [ ] Étape 8 : voir §8.

### vv009 : Insubstantial Flight

- [x] Étape 2 : `ho011` ★ Goblin Glider (même carte à un déclencheur près) ;
      `vr010` Regeneration (même auteur) pour la forme de la réponse.
      **Aucune fabrique n'enveloppe `Message.AfterCardExhausted` et aucune
      carte du dépôt ne s'y abonnait** : l'`Ability` est construite à la main,
      montage établi (`cd008`, `aa001b`, `dt009`, `gb001`).
- [x] Étape 5 : « YOU gain the [[AERIAL]] trait » (l'identité, donc
      `GiveKeywordToAttached("You", ...)`), « After your HERO exhausts »
      (filtre `"YourHero"`), « exhausts » sans complément (n'importe quel
      épuisement, aucun filtre sur le pouvoir), la flèche qui plafonne à une
      fois par round, « ready YOUR HERO » (`message.trigger`). Pas de boucle :
      redresser n'émet pas `AfterCardExhausted`. Résultat : conforme.
- [x] Étape 6 : coût 2, Requirement [energy]. Aucun autre nombre. Résultat :
      conforme.
- [x] Étape 7 : 2 cas, un par capacité. Substitution : voir §7.
- [ ] Étape 8 : voir §8.

### vv010 : ★ Viv's Solar Gem

- [x] Étape 2 : `sd015` Never Ending Spark (la même carte à un déclencheur
      près) ; `29030` pour « after the villain phase ends ».
- [x] Étape 5 : `Resource:` **nu** et non `Hero Resource:` (générable aussi en
      alter-ego), `Response:` **nu** (le redressement joue quelle que soit la
      forme, ce qui compte : la fin de phase du vilain trouve souvent Viv en
      civil), « generate A [energy] resource » (une seule), aucune restriction
      de financement donc pas de `for_card=`, « ready Viv's Solar Gem »
      (elle-même). Résultat : conforme.
- [x] Étape 6 : coût 2. Aucun autre nombre. Résultat : conforme.
- [x] Étape 7 : 2 cas — le financement réel d'un coût, et le redressement,
      celui-ci par sonde in-process (l'API Puzzle n'avance aucune phase).
      Substitution : voir §7.
- [ ] Étape 8 : voir §8.

### vv011 : Grounded

- [x] Étape 2 : `36030` Claustrophobia (obligation de Storm) — **même texte,
      mot pour mot**, aux noms propres près. **Pas** `12025` Care for Cassie,
      qui imprime « you MAY flip » et un choix à deux branches.
- [x] Étape 5 : « FLIP » sans « you may » (obligatoire), « cannot change form »
      (interdiction PERMANENTE, `PlayersCannotChangeForms`, et non « until your
      next turn ends » comme 12025), « Exhaust YOUR ALTER-EGO »
      (`CostFunc.Exhaust("YourIdentity")`), « REMOVE FROM THE GAME » et non
      « discard ». `desc.GiveTo` = « Viv Vision », résolu par
      `IsName(..., check_all_face=True)` qui ignore l'étoile d'unicité.
      Résultat : conforme.
- [x] Étape 6 : Boost 2 (deux icônes rouges lues sur le scan). Résultat :
      conforme.
- [x] Étape 7 : 2 cas, un par capacité. Substitution : voir §7.
- [ ] Étape 8 : voir §8.

## 7. Étape 7 — résultat de la batterie et des substitutions

`tools/test_capacites.py` filtré sur `vv0` : **20 cas, tous verts**.

Preuve par substitution (`tools/substituer_pack.py`), 12 cartes sur 12 :

| Carte | Rouges | Commentaire |
|---|---|---|
| `vv001a` | 1/1 | — |
| `vv001b` | **1/2** | le cas vert est le **contre-cas** « une carte wild n'est PAS repêchable » : il vérifie une ABSENCE d'effet, il reste donc vert sans module par construction. Assumé, comme `vp014`/`vp015`/`ho017` avant lui. |
| `vv002` | 1/1 | — |
| `vv003` | 2/2 | plus une **substitution fine** décrite ci-dessous |
| `vv004` | 1/1 | — |
| `vv005` | 2/2 | une par branche `Play` |
| `vv006` | 1/1 | — |
| `vv007` | 2/2 | — |
| `vv008` | 1/1 | — |
| `vv009` | 2/2 | — |
| `vv010` | 2/2 | — |
| `vv011` | **2/2** | après correction d'un FAUX VERT, voir ci-dessous |

**Le faux vert de `vv011`, trouvé par la substitution.** Le cas de bascule
écrivait `"attendu": {"face": "vv001b", ...}`. Or **`face` n'est pas une clé de
`etat_attendu`** : elle appartient à un autre vérificateur, donc la ligne ne
vérifiait RIEN. Seul `en_jeu: ["vv011"]` était testé, et il reste vrai sans le
module — le cas passait au vert sur une carte muette. La clé qui teste vraiment
la forme est `forme` (`test_capacites.py:15244`). Corrigé : le cas est
désormais **2/2 au rouge** sous substitution. C'est exactement ce que la preuve
par substitution est là pour attraper, et aucun autre outil ne l'aurait vu.

**Substitution fine sur `vv003`**, pour prouver la clause qui justifie tout
l'écart du §4. Retirer le module entier prouve la carte, pas le mot-clé : on a
donc remplacé `.SetIgnoreKeyword('Crisis', 'Patrol')` par
`.SetIgnoreKeyword('Crisis')` seul, et relancé. Résultat : le cas patrol tombe
au **ROUGE** (« menace sur 01097b = 5, attendu 1 » : le complot principal
n'était plus sélectionnable), les deux autres restent verts. La levée de
`patrol` est donc prouvée pour elle-même.

## 8. Étape 8 — autoplay

`tools/autoplay.py`, 8 parties, Rhino / normal / profil équilibré, contre le
héros **témoin** `spider_man` dans les mêmes conditions.

| Deck | Parties | Victoires | Rounds moyens | Incidents |
|---|---|---|---|---|
| `viv_vision` | 8 | 0 | 5,1 | **0** |
| `spider_man` (témoin) | 8 | 0 | 5,6 | **1** (une partie bloquée) |

**Grep exhaustif** (`NameError|AttributeError|TypeError|KeyError|AssertionError|
Traceback`) sur les 16 journaux : **0 partout**.

Le taux de victoire nul est une propriété du **pilote**, pas du pack : le
témoin officiel fait exactement pareil, et lui bloque une partie sur huit là
où Viv n'en bloque aucune.

**Lecture ligne à ligne** des journaux qui touchent les cartes neuves. Tout ce
qu'on voulait voir s'y trouve : la bascule de forme, `vv008` Computer Mind
équipée, `vv007` Sparky posé puis incliné, la *Density Manipulation* de
`vv001a` activée, `vv005` Solar Beam qui frappe Rhino. Et surtout, partie 1,
**le mot-clé `breakthrough` en situation réelle** :

```
120: Just a Phase activates, targets [The Break-In!]
123: The Break-In! perd 1 pion(s) « threat »
127: Bomb Scare  perd 3 pion(s) « threat »
131: Bomb Scare  was discarded
```

La menée de 4 vide le complot principal (qui ne portait qu'une menace) et
**les 3 restantes se reportent sur une autre manigance, qui tombe**. C'est la
définition du mot-clé, exercée par le jeu lui-même et non par un cas de test.

Écart de pilotage relevé, sans gravité : l'heuristique dépense volontiers un
`vv005` Solar Beam comme simple ressource énergie. C'est un défaut connu du
pilote, pas de la carte.

## 8bis. Règle de portée — les 112 decks

Deux fichiers moteur PARTAGÉS ont été touchés (§3), donc la passe complète est
due, pas seulement le deck du pack.

`tools/verifier_tous_les_decks.py`, passe complète : **110/112 decks montent
une partie**, dont `viv_vision` (« identite vv001a, main 6, deck 34 », soit
exactement la forme du témoin `spider_man »).

Les deux échecs sont **PRÉEXISTANTS, pas des régressions**. Vérifié en
remettant les deux fichiers moteur à leur état d'origine
(`git checkout`, `__pycache__` purgé) et en relançant les deux decks seuls :
les deux échouent **avec le message identique**, sans mes correctifs.

| Deck | Message | Nature |
|---|---|---|
| `sp_dr` | `setup : AssertionError: self=[(01,31002a) Peni Parker]` | préexistant |
| `doctor_doom` | `setup : AssertionError: face.paper.card_id='dd003'` | préexistant — `dd003` Doombot est un **Ally** à deux capacités `Play`, et la liste blanche de `factory.py` ne couvre les doublons que pour les `Event` et pour le seul allié `45031`. |

## 8ter. Règle de portée — la batterie complète

`tools/test_capacites.py` sans filtre, `PARALLELES=4` : **1012/1017 cas
passés**. Les 5 rouges, un par un :

- **4 cas du pack `squirrel_girl`** (`sg006`, `sg007`, `sg009`, `sg013`).
  **Préexistants** : les quatre se reproduisent avec le message identique
  après avoir remis les deux fichiers moteur à leur état d'origine.
- **1 cas du pack, `vv008`** : `AssertionError: ip='127.0.0.1', port=41010`.
  C'est le **faux échec de port** que le §7 de `RECETTES-MOTEUR` documente,
  et cette fois la cause est nommée : le **jeu lui-même tournait**
  (`launcher_fast.py`, pid 502942) et occupait 41010. Rejoué à ce port exact,
  le cas rend `{"ok": true, "message": "2 cartes piochees et Computer Mind
  incline"}`, et il est vert 3/3 en série. Aucun défaut de carte.

⚠ **Leçon à retenir pour les prochains portages** : la règle « jamais deux
harnais en parallèle » ne suffit pas — **le jeu lancé compte comme un
occupant de port**. Vérifier `pgrep -af launcher_fast.py` avant une passe
complète, au même titre que `pgrep -af test_capacites`.

Autres vérifications statiques, toutes vertes : `test_cards.py` (5069 OK,
0 erreur), `verifier_api_cartes.py` (5668 fichiers, 4 en faute, **aucune du
pack** — voir §10), `verifier_prefixes.py`.

## 9. Reste dû

- `PROCESSUS-HEROS` gate finale : une partie complète jouée par un humain dans
  le navigateur. Aucun outil du projet ne la remplace.
- Vérification au survol du héros dans le wizard que la biographie de
  `vv001a` s'affiche (preuve exigée par l'étape 7 de `PROCESSUS-HEROS`).

## 10. Trouvailles hors pack

Deux ont été CORRIGÉES le 02/09/2026, sur demande de l'utilisateur, dans un
commit séparé de celui du portage. La troisième reste ouverte.

- `GainUntilRoundEnd` n'expose pas `recover`, que `TemporaryGain` accepte
  pourtant (`face_action.py`, paramètre déclaré juste au-dessus).
  `verifier_api_cartes.py` le signale sur **`wd159` et `wd160`** « Web Swing! »
  (pack `web_of_deceit`), qui appellent
  `GainUntilRoundEnd(effect, attack=1, thwart=1, defense=1, recover=1)`.
  L'appel lève `TypeError`, avalé par le moteur.
  **Effet réel, à ne pas surestimer** : `Faces.ReadyAll` s'exécute AVANT la
  ligne fautive, donc le héros EST redressé ; c'est le « +1 à chaque pouvoir
  de base » qui n'arrive jamais. La carte est à moitié morte, en silence.
  Même famille que le correctif `stalwart` du §3.
  ✅ **CORRIGÉ** : `recover` ajouté à `GainUntilRoundEnd`.
  `verifier_api_cartes.py` passe de 4 fautes à 2.
- ❌ **NON corrigé, et pourquoi.**
  `AbilityFactory.UnitIgnoreKeywordIcons` déclare un paramètre
  `while_use_basic_thw` qu'elle **n'utilise jamais** (`play.py:448`). Une seule
  carte le passe, `21191` ★ Fandral : son « quand Fandral utilise son CTR de
  base, ignorez les icônes de crise » ignore donc la crise **en permanence**,
  pas seulement pendant sa menée de base.
  Ce n'est **pas** une ligne à ajouter : le moteur n'expose nulle part, depuis
  l'effet reçu par `CheckIfEffectIsIgnoreKeyWord`, de quoi reconnaître une
  menée DE BASE. Il faudrait créer ce crochet. Et la carte est officielle,
  sans aucun cas de test pour rattraper une erreur. Laissé ouvert
  délibérément.
- **`doctor_doom` et `sp_dr` ne montent aucune partie** (voir §8bis), et c'est
  antérieur à ce portage. `dd003` Doombot est un allié à deux capacités
  `Play` : la liste blanche de `factory.py` traite ce cas pour les `Event`
  (une douzaine d'entrées) mais, côté `Ally`, ne connaît que `45031`. Ajouter
  `dd003` à côté d'elle est tout ce qu'il manquait.
  ✅ **CORRIGÉ** : le deck `doctor_doom` monte à nouveau
  (« identite dd001a, main 6, deck 34 »), et la passe complète passe de
  110/112 à **111/112**. Seul `sp_dr` reste rouge.
- `ui-app/src/board/mots-cles.ts` n'a pas d'entrée `Requirement`, alors que la
  clé existe dans `desc` : les ~30 cartes qui portent ce mot-clé, dont 5 de ce
  pack, n'affichent aucune infobulle pour lui. `Breakthrough` y a été ajouté
  (sans quoi le joueur lisait un mot inconnu) ; `Requirement` ne l'a pas été,
  parce que cela change l'affichage de cartes officielles hors de ce portage.
