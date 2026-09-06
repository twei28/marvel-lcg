# PROCESSUS-CARTE.md — les 16 gabarits du pack SUNFIRE (set 163, `sf`)

Gate de `PROCESSUS-HEROS.md` : un gabarit rempli par carte. Rédigés le
06/09/2026. Auteur du pack : **Rainy**, zip « Sunfire ».

⚠ **Aucun aspect n'a été arbitré, et c'est voulu.** Consigne utilisateur du
06/09/2026 : on n'invente plus de deck d'aspect pour un héros homebrew. Le
`player_deck` est **vide**, le joueur choisit ou construit le sien au
lancement. Détail et raison : `PROCESSUS-HEROS.md` étape 3.

**Preuves communes**, citées une fois :

- **Étape 7, cas** : `test_capacites.py … sf0` → **31/31**, en passe parallèle
  (`PARALLELES=4`) **et** en passe séquentielle.
- **Étape 7, substitution** : `substituer_pack.py … sf0` → **16/16 cartes** ont
  au moins un cas qui tombe au rouge sans leur module.

  | Carte | rouges | Carte | rouges | Carte | rouges |
  |---|---|---|---|---|---|
  | sf001a | 2/3 | sf006 | 1/1 | sf011 | 2/3 |
  | sf001b | 3/3 | sf007 | 2/2 | sf012 | 1/1 |
  | sf002 | 1/1 | sf008 | 1/2 | sf013 | 1/2 |
  | sf003 | 2/2 | sf009 | 2/2 | sf014 | 2/2 |
  | sf004 | 1/1 | sf010 | 2/2 | sf015 | 2/2 |
  | sf005 | 2/2 | | | | |

  ⚠ `sf014` est à **1/2**, pas 2/2 : la table a dû être refaite, voir §6.

  **Les cinq cas restés verts sont tous des contre-cas d'ABSENCE, des lignes de
  base, ou mesurent une AUTRE carte** : `sf001a` (l'attaque d'un allié ne pose
  rien), `sf008` (aucun bonus de DEF en forme civile), `sf011` (sans le complot,
  le sbire frappe à 2), `sf013` (un sbire sans Perforation ne passe pas le
  Tenace), `sf014` (« mais la brûlure, elle, passe » — ce cas mesure les dégâts
  de `sf009`, pas le module de la katana, et reste donc vert sans elle).
  Listés carte par carte plus bas, jamais masqués.
- **Étape 1** : pack `sunfire` en queue de `cards.json`, set
  `163. Custom (Sunfire)`, préfixe `sf` déclaré, `verifier_prefixes` OK.
- **Étape 4, image** : `assets/pics/sf0*.jpg` pour les 16, découpées du zip par
  `tools/importer_images_sunfire.py`.
- `test_cards` : **5320 ok / 0 erreur** (5304 avant le pack, soit **+16**).
- `verifier_desc_mots_cles sunfire` / `verifier_noms_modules` /
  `verifier_cartes_en_jeu sunfire` / `verifier_appels_modules sunfire` : OK.
- **Étape 3** : `deck/starter/sunfire.json`, et le deck **monte une partie**
  (`DECK_NOM=sunfire` → « identite sf001a, main 6, deck 9 »).
- **Étape 10** : signatures étrangères sur les **125 decks** → **0 écart**.
- **Étape 7 (héros)** : biographie `sf001a` dans `heros-info.js`
  (`node --check` OK).
- **Étape 8 (héros)** : les 16 textes français dans `textes-fr-fanmade.ts`,
  **déployés**.

---

## PAS DE GATE DE PORTÉE : AUCUN FICHIER MOTEUR PARTAGÉ TOUCHÉ

Rien hors de `src/cards/pack/sunfire/` n'a été modifié côté moteur. Aucun
mot-clé nouveau, aucun compteur nouveau, aucune fabrique nouvelle. Les traits
`HAND` et `NINJA` sont neufs au dépôt mais un trait ne se déclare nulle part.

---

## LA MÉCANIQUE : LA BRIQUE 6, ÉCRITE DE BOUT EN BOUT

`sf009` **Burning** est une **amélioration JOUEUR attachée à un ENNEMI**, qui
revient dans la **réserve** au lieu de partir en défausse. C'est la brique 6 du
plan de portage, et ce pack la pousse plus loin que `blink` ou `yondu` : **six
exemplaires en circulation permanente**.

| Carte | Ce qu'elle fait de Burning |
|---|---|
| `sf001b` Shiro Yoshida | en met **6 de côté** à la mise en place |
| `sf001a` Burning Aura | en pose une à **chaque attaque ET chaque défense de base** |
| `sf002` Atomic Fire | en pose sur le vilain **et** chaque sbire engagé, puis frappe tout ce qui brûle |
| `sf003` Burning Hands | en pose une en repli |
| `sf005` Solar Blast | en pose une en repli, **sur l'ennemi frappé** |
| `sf004` Hot Pursuit | **redresse Sunfire** quand une est posée |
| `sf006` Atomic Samurai | **alourdit** ses dégâts de 1 |
| `sf007` Sunfire's Mask | fait **piocher** quand un ennemi brûlé meurt |
| `sf009` elle-même | brûle, puis **se remet de côté** |

**Huit cartes sur seize.**

### ⚠⚠ « Permanent » n'est pas un obstacle, c'est le mécanisme

`HasPermanent.OnWhenCardLeavePlay` (`has_permanent.py:34`) refuse la sortie de
jeu d'une carte Permanente **sauf si l'effet qui la sort vient du MÊME
`set_name`** :

```python
elif self.paper.set_name != by_effect.this.paper.set_name:
    return False
```

Burning porte `set_name = "Sunfire"` : **aucune carte du vilain ne peut
l'arracher, et toutes les cartes de Sunfire le peuvent**, à commencer par
elle-même. C'est exactement ce que le mot-clé veut dire sur cette carte, et le
moteur le rend **nativement**. Rien à contourner, aucun écart à assumer.

⚠ Corollaire : un helper appelé depuis une carte d'un autre set échouerait en
silence. Tout le pack passe donc par `RemettreDeCote`, et tout le pack pose ses
brûlures par `AttacherUneBrulure` — parce que `sf004` Hot Pursuit écoute
`AfterCardAttachTo`, que **seul `AttachTo2` émet**.

---

## CE QUE LES GATES ONT TROUVÉ

Quatre défauts, tous trouvés par les cas de test, **aucun** par la lecture.

### 1. ⚠⚠ Un nom de carte unique s'écrit SANS l'étoile, et l'oubli tue en silence

Le « ✦ » imprimé devant un nom unique **n'appartient pas au nom** :
`cards/paper.py:45-46` fait `is_unique = name.startswith("* ")` puis
`name = name.lstrip("* ")`. Un `CardFinder(name="* Silver Samurai")` ne trouve
donc **jamais rien, et en silence**.

Ici le prix est double : **`sf012` Silver Samurai et `sf014` Silver Samurai's
Katana se cherchent l'une l'autre** (le samouraï convoque sa katana, la katana
convoque son porteur). Avec l'étoile, **les deux cartes étaient mortes**.

Ni `test_cards`, ni `verifier_appels_modules`, ni `verifier_noms_modules` ne le
voient. **Payé quatre fois** au dépôt : `howard_the_duck`, `ms_america`,
`patriot`, puis ici. Ajouté à `RECETTES-MOTEUR.md` §6 à cette occasion.

### 2. `Find.Find` ne voit PAS le set némésis mis de côté

Sa liste de zones (`find.py:118-133`) couvre le deck de rencontre, sa défausse,
le terrain, le deck du joueur, sa main, sa défausse et `set_aside` — mais **pas
`player.set_aside_nemesis_sets`**, la pile où `player_setup.py:230` range les
cinq cartes némésis à la mise en place.

`sf012` et `sf014` ne s'y trouvaient donc pas non plus. D'où le helper
`TrouverCarteDuSet`, qui essaie le chemin normal **puis** la pile némésis à la
main.

### 3. `SetTarget("Players")` rend une FACE, pas un objet `Player`

`sf002` Atomic Fire faisait `Player.IsType(cible)` sur la cible rendue par le
sélecteur : « AttributeError: 'Hero' object has no attribute 'IsPlayer' »
(`player.py:303`), **avalée par le moteur**. La carte était simplement inerte —
0 dégât, aucune brûlure — et seul le traceback du journal le disait.

⚠ Le dépôt a d'ailleurs un littéral dédié pour cette phrase exacte,
`SetTarget("VillainAndEngagedSamePlayerMinion")` (`04006`, `ho004`), qui met le
choix du joueur **dans** le sélecteur. Le module garde sa boucle explicite, déjà
écrite et testée, mais le littéral est signalé ici pour une éventuelle reprise.

### 4. Deux noms de paramètres et une fabrique inexistants

- `is_basic_power` **n'existe pas** sur `WhenUnitWouldAttack` : c'est
  `is_basic_attack` (`do_attack.py:38`), alors que la fabrique de défense dit
  bien `is_basic_defense`. Les deux ne nomment pas le paramètre pareil.
- `WhenCardPutIntoPlay` **n'existe pas comme fabrique** (le message existe, pas
  la fabrique). C'est `AfterCardEnterPlay`.
- `Cost("*")` **n'existe pas** : « 1 ressource de n'importe quel type » s'écrit
  `Cost("1")`, les lettres imposant une COULEUR et les chiffres un NOMBRE
  (`element/cost.py:35-41`).
- `message.UpdateDamage` existe, mais sur un **autre** message
  (`sender_damage.py:932`) et ne compte que les dégâts **excédentaires** :
  alourdir des dégâts en cours, c'est `IncreaseDamage` (modèle `dt094`).

Les deux premiers ont été attrapés par `test_cards`, les deux autres par la
lecture du moteur avant écriture.

### 5. Deux pièges du harnais, payés dans les cas

- **`Puzzle.Damage` passe par `FindOrCreateFace`**, qui fouille le deck AVANT
  le terrain. Avec `01110` Hydra Bomber, présent en **deux exemplaires** dans le
  deck de Rhino, la commande frappait une copie face cachée et celui du terrain
  restait intact. Le cas emploie donc `01131` * Tiger Shark, **étranger au
  scénario**.
- **L'icône Amplify du complot compte.** Le cas de `sf011` attendait 4 dégâts et
  en a lu 5 : `Hand Ambush` porte Amplify, qui ajoute 1 icône à chaque carte de
  bonus retournée (`ResolveAmplify`, `can_boost.py:71`). C'est le cas qui l'a
  rappelé, pas la lecture.

### 6. ⚠⚠ UN FICHIER SOURCE EST RESTÉ EN STUB, ET J'AI MESURÉ DU VIDE

La **première** exécution de `substituer_pack.py`, lancée au premier plan, a été
**coupée par la limite de 10 minutes de l'outil** en plein milieu. Elle a laissé
`sf014.py` réduit à `GetAbilities -> []`.

Conséquences, toutes constatées :

- les exécutions suivantes de `test_capacites` mesuraient un module **vide**
  sans que rien ne le signale — le seul cas rouge était celui de `sf014`, ce qui
  ressemblait à une régression ;
- **trois corrections ont été écrites pour chasser un fantôme** avant que je ne
  pense à lire le fichier ;
- la première table de substitution était fausse (`sf014` y était donné à 2/2).

`substituer_pack.py` prévient pourtant en toutes lettres : « ⚠ Le stub est posé
sur le FICHIER SOURCE puis restauré : ne pas interrompre brutalement ; en cas de
doute, `git status` doit rester propre à la fin ». Un pack **non encore commité**
échappe justement à ce contrôle-là.

**Procédure retenue et appliquée pour la seconde exécution** : copier les 16
sources dans le brouillon **avant**, relancer, puis comparer l'empreinte
`md5sum` de l'ensemble à la sauvegarde. Résultat : identique, aucun stub. C'est
cette seconde table qui figure ci-dessus.

### 7. Deux `assert` du moteur sur le même trajet, trouvés par l'autoplay seul

`JoueurDeCetteCarte` du set némésis appelait `Minion.GetEngagedPlayer()`, qui
**lève un `AssertionError`** quand le sbire n'est pas engagé et que sa zone n'a
pas de joueur propriétaire (`minion.py:145-149`) — c'est exactement le cas de
`sf013` Hand Ninja au moment où son étoile Boost le met en jeu **depuis la zone
de bonus du vilain**. Le moteur **avale** l'exception : la carte ne fait rien.

Le premier correctif est passé par `card.area.GetOwnerPlayer()`… qui porte
**lui aussi** un assert (`assert isinstance(owner, Player)`, `deck/deck.py:73`),
et qui saute sur la même zone. Il a fallu un second autoplay pour le voir, le
premier ayant été masqué par l'autre. La version finale passe par
`GetOwner()` et filtre avec `EstJoueur`, un helper local qui remplace
`Player.IsType` partout dans le set — ce dernier faisant `x.IsPlayer()` et
explosant sur autre chose qu'un joueur.

⚠ **Aucun des 31 cas ne voyait ces deux défauts**, parce qu'aucun ne mettait le
ninja en jeu depuis la zone de bonus. C'est la raison d'être de l'étape
autoplay, et c'est la deuxième fois en trois packs qu'elle rattrape ce que les
cas laissent passer (après `bc010`).

---

## MOTS-CLÉS RENCONTRÉS

| Mot-clé | Carte | État |
|---|---|---|
| `permanent` | sf009 | fiche existante — ⚠ **et c'est le mécanisme du pack**, voir plus haut |
| `requirement` | sf003 | fiche existante, base automatique `desc.Requirement = "Y"`, AUCUN SCRIPT |
| `quickstrike` | sf012 | fiche existante, base automatique |
| `retaliate` | sf012 | fiche existante, base automatique |
| `amplify` | sf011 | fiche existante, base automatique, AUCUN SCRIPT |
| `piercing` | sf013 | fiche existante, `UnitAttackGainKeyword("This", piercing=True)` |
| `surge` | sf015 | fiche existante — **gagné**, pas imprimé : `ThisCardGainSurge` |
| `boost` | sf013, sf015 | fiche existante — l'étoile n'existe que si `WhenCardBecomeBoost` est écrite |
| `special` | sf001a, sf013 | fiche existante, les `[star]` codés toujours actifs |

**Aucune fiche n'a eu à être créée.**

⚠ L'icône **Amplify** de `sf011` a été identifiée **par comparaison d'image**
avec `16054` Vendetta, carte officielle dont le `desc` déclare
`"Amplify": "1"` : les deux dessins sont **superposables**. Comparée aussi à
`01107` (hazard, un « + » sur carte inclinée) et `01109` (acceleration, un
« + » sur maison soulignée), qui sont **différentes**. Jamais nommée à vue —
leçon Lockjaw.

⚠ `ELITE` est un **TRAIT**, pas un mot-clé (`sf012`).

---

## HOMONYMES ET NOMS

- ⚠ **« * Sunfire » est DÉJÀ `35014`**, un ALLIÉ du pack `wolverine`. Aucune
  carte du pack ne cherche le héros par son nom : toutes passent par le TYPE ou
  par `"YourHero"`.
- ⚠ **« Hot Pursuit » est DÉJÀ `24058`**, une manigance annexe du set State of
  Emergency. Le texte français s'écrit sur le `card_id`.
- ⚠ **Les deux faces portent le même numéro « 0.1 » dans le zip**, contrairement
  aux autres packs de Rainy qui numérotent « 0.1 » et « 0.2 ». Ce n'est donc pas
  le numéro qui tranche mais le **libellé imprimé** HERO / ALTER-EGO.
- ⚠ **`sf010` Shame porte le bandeau SUNFIRE**, pas « … NEMESIS » : son module
  vit dans `sunfire/sunfire/`. Piège `bt019` payé une **onzième** fois, et la
  **huitième** fois où il est vu AVANT d'écrire.
- ✅ « Shiro Yoshida », « Burning », « Atomic Fire », « Burning Hands »,
  « Solar Blast », « Atomic Samurai », « Sunfire's Mask », « Sunfire's Suit »,
  « Shame », « Hand Ambush », « Silver Samurai », « Hand Ninja », « Silver
  Samurai's Katana » et « Tachyon Whip » n'ont **aucun homonyme** au dépôt.

---

## ÉCARTS ASSUMÉS

- **`sf013` et `sf015`, l'astérisque dans `ATK`** : sur un SBIRE, le `*` de
  `desc.ATK` alimente `printed_attack_consequential_damage`, un champ que seul
  `ally.py` lit. Il est donc **inerte** ici, et le dépôt l'écrit quand même pour
  marquer la capacité Special (`57056`, `58026`, `59043`). On suit la
  convention.
- **`sf015`, « After you use a basic power, take 2 damage »** : les quatre
  pouvoirs de base sont visés, récupération comprise — mais la récupération
  exige la forme civile, elle-même **interdite par la phrase précédente de la
  même carte**. Les trois pouvoirs de héros sont donc les seuls atteignables.
  C'est une conséquence du texte, pas une restriction ajoutée.
- **`sf010`, « The number of cards in your hand cannot exceed your hand size »** :
  cette phrase n'a **aucun équivalent** au dépôt (vérifié sur les 5933 cartes).
  Elle est rendue par une Réponse forcée sur `Message.AfterCardsMoved` filtrée
  sur la main, faute de tout message « après avoir pioché » (seul
  `WhenPlayerWouldDrawCard` existe, et il part **avant** la pioche). Le montage
  couvre en prime toutes les autres façons de remplir sa main, ce que « any
  cards » demande.
- **`sf002`, la boucle explicite plutôt que
  `SetTarget("VillainAndEngagedSamePlayerMinion")`** : voir §3 ci-dessus. Même
  résultat, code déjà testé, littéral signalé pour une reprise éventuelle.

---

## CE QUE CES BLOCS NE PEUVENT PAS VOIR

⚠ **Aucune partie n'a été jouée par un humain dans le navigateur.**

⚠ **Le deck de départ n'a AUCUNE carte d'aspect.** L'autoplay joue donc un deck
de 15 cartes signature seulement, ce qui n'est **pas** une partie normale : le
pilote manque de ressources et de cartes. Les chiffres sont à lire comme un test
de non-blocage, pas comme une mesure d'équilibre.

**Autoplay, 8 parties contre Rhino, profil équilibré** (troisième exécution, la
seule faite sur le code réparé — les deux premières tournaient sur un `sf014`
vide et sur les deux `assert` du §7) :

| Deck | parties | sans verdict | tracebacks |
|---|---|---|---|
| `sunfire` | 8 | **2** (1 bloquée, 1 minuteur) | 1 |
| `spider_man` (témoin) | **5 seulement**, exécution interrompue | 0 | — |

⚠ **La comparaison au témoin est INCOMPLÈTE** : son exécution a été arrêtée à 5
parties sur 8. Je ne peux donc **pas** affirmer que Sunfire est au niveau du
témoin, et je ne l'affirme pas.

⚠ **Le traceback restant n'est PAS dans le pack** : c'est
`controller.py:274`, le garde-fou anti-répétition du **pilote**. La question qui
le coince est l'Interruption de `sf006` Atomic Samurai, proposée **une fois par
brûlure** en fin de phase — jusqu'à six fois d'affilée. La carte imprime
« **Interrupt** », pas « Forced Interrupt » : elle est facultative par le texte,
et la transformer en obligatoire pour arranger le pilote serait un écart. C'est
une limite du harnais, pas un défaut de la carte.

⚠ **Deux causes possibles du blocage n'ont PAS été départagées** : le deck sans
aucune carte d'aspect, ou la fréquence de cette Interruption. Il faudrait une
fournée avec un deck d'aspect complet pour trancher, ce qui sort du cadre de ce
portage.

## Gabarits, carte par carte

### sf001a : * Sunfire (face héros)
- [x] Étape 2 : `yd001a` « D'ast Whistlin' » (pack yondu), le héros dont la
      capacité se déclenche sur les mouvements d'une amélioration attachée à un
      ennemi ; `WhenUnitWouldAttack` + `WhenUnitDefendAgainstAttack` pour les
      deux fenêtres.
- [x] Étape 5 : ⚠ « makes a BASIC attack or BASIC defense » → **deux** fenêtres,
      et elles ne nomment pas la même carte : la **cible** d'un côté,
      l'**attaquant** de l'autre. D'où deux opérations. ⚠ INTERRUPT, donc la
      brûlure est posée **avant** que le pouvoir ne se résolve.
- [x] Étape 6 : **PV 11, CTR 2, ATQ 1★, DEF 2★, main 5.** Les étoiles marquent
      le Special, pas des dégâts consécutifs (précédents `58001a`, `61001a`).
      Aucune limite imprimée.
- [x] Étape 7 : 3 cas, **rouges 2/3** — le vert est le contre-cas « l'attaque
      d'un allié ne pose rien », qui mesure une ABSENCE.
- [x] Étape 7 bis : limite imprimée **NON**.

**Carte terminée : OUI**

### sf001b : * Shiro Yoshida (face alter-ego)
- [x] Étape 2 : `09001b` / `bt001b` / `al001b` pour
      `BeginGameWithSetAside` ; `aa001a` pour `DiscardDeckTopCards`, qui **rend**
      la liste des cartes défaussées.
- [x] Étape 5 : ⚠ « begins the game with 6 Burning upgrades set aside » n'est
      **pas** le champ `set_aside` du deck, que le moteur ne lit pas en vraie
      partie. ⚠ Pas de flèche dans Hot-Headed : défausser cinq cartes est
      l'effet, pas un coût.
- [x] Étape 6 : PV 11, REC 4, main 6. Limite une fois par ROUND.
- [x] Étape 7 : 3 cas, **rouges 3/3**.
- [x] Étape 7 bis : limite imprimée **OUI**. Témoin par `declencher_tolerant`,
      chiffre mesuré : `taille_main: 2`.

**Carte terminée : OUI**

### sf002 : Atomic Fire — **OUI**
(1 cas, rouge 1/1 ; ⚠ **deux portées différentes dans la même carte**, la
première sur le joueur choisi, la seconde sur tout le terrain. Voir §3 de « ce
que les gates ont trouvé » pour l'AttributeError avalée.)

### sf003 : Burning Hands — **OUI**
(2 cas, rouges 2/2 ; ⚠ « Choose an attachment … » **sans** « attached to that
enemy » : tout le terrain, c'est la différence imprimée avec `sf005`.
⚠ « OTHERWISE » n'est pas un choix.)

### sf004 : Hot Pursuit — **OUI**
(1 cas, rouge 1/1 ; ⚠ la fenêtre `AfterCardAttachTo` n'est émise que par
`AttachTo2` : c'est pour ça que **tout** le pack passe par
`AttacherUneBrulure`.)

### sf005 : Solar Blast — **OUI**
(2 cas, rouges 2/2 ; ⚠ le second est **le seul endroit où la différence avec
`sf003` est mesurée** : un attachement sur un AUTRE ennemi n'est pas arraché.
⚠ La cible du contre-cas est `01131` * Tiger Shark et ses 6 PV, parce que Hand
Ninja n'en a que 2 et mourait des 3 dégâts, si bien que le repli ne trouvait
plus d'ennemi où poser la brûlure.)

### sf006 : * Atomic Samurai — **OUI**
(1 cas, rouge 1/1 ; ⚠ « from the TRIGGERED ABILITY of Burning » et non « from
Burning » : le filtre porte sur la SOURCE des dégâts. C'est l'écart 1 → 2 avec
le cas de `sf009` qui mesure la carte, pas un chiffre isolé.)

### sf007 : * Sunfire's Mask — **OUI**
(2 cas, rouges 2/2 ; ⚠ « **YOU** get +2 hit points » → le littéral `"You"`, donc
les deux faces, à l'inverse de `sf008` qui dit « **SUNFIRE** gets +1 DEF ». Les
deux écritures cohabitent dans le même pack, et le contre-cas en forme civile
**confirme** le bonus au lieu de l'infirmer — c'est la preuve que le littéral
employé est le bon.)

### sf008 : Sunfire's Suit — **OUI**
(2 cas, **rouge 1/2** ; le vert est le contre-cas en forme civile, qui mesure
une ABSENCE. Il prouve qu'**aucun** bonus de DEF ne fuit, exigence de RECETTES §3 née du défaut `an002`. ⚠ Pas unique,
vérifié par découpe d'image du bandeau vertical à côté de `sf006` et `sf007`,
qui portent une étoile.)

### sf009 : Burning — **OUI**
(2 cas, rouges 2/2 ; **la carte qui porte le pack**. Le premier passe par une
**vérification dédiée** qui envoie `WhenPhaseEnd` et `AfterPhaseEnd` à la main,
`Puzzle.BeginVillainPhase()` n'ouvrant que la phase du vilain. Le second prouve
la seconde Réponse forcée, sans laquelle une brûlure posée sur un sbire vaincu
serait perdue et la réserve se viderait en six sbires.)

### sf010 : Shame — **OUI**
(2 cas, rouges 2/2 ; ⚠ obligation qui **reste en jeu**, modèle `04165` Martial
Law. ⚠ « **REMOVE** from the game » et non « discard » : `04165`, la carte
modèle, dit « discard » — ne pas la recopier sans la relire.)

### sf011 : Hand Ambush — **OUI**
(3 cas, rouges 2/3 ; le vert est la LIGNE DE BASE « sans le complot, le sbire
frappe à 2 », qui donne son sens aux 5 dégâts du cas nominal. ⚠ Un sbire ne
reçoit normalement **aucune** carte de bonus : c'est ce qui rend le chiffre
lisible. ⚠ « place it ON TOP of the encounter deck » : le sbire revient, et
c'est le piège du set.)

### sf012 : * Silver Samurai — **OUI**
(1 cas, rouge 1/1 ; ⚠ voir §1 et §2 de « ce que les gates ont trouvé » : cette
carte et `sf014` se cherchent l'une l'autre, et **deux** pièges les tuaient
ensemble. ⚠ « IF IT IS NOT IN PLAY » désigne **la katana**, pas le samouraï.)

### sf013 : Hand Ninja — **OUI**
(2 cas, **rouge 1/2** ; le vert est la LIGNE DE BASE — `01101` Hydra Mercenary a
la même ATQ 1 et aucune Perforation, et son **zéro** donne son sens au dégât du
premier. ⚠ Deux capacités mesurées d'un coup : le ninja s'active tout seul en
entrant, et son attaque traverse le Tenace.)

### sf014 : * Silver Samurai's Katana — **OUI**
(2 cas, **rouge 1/2** — le vert est « mais la brûlure, elle, passe », qui mesure
`sf009` et non cette carte ; ⚠ le second est **essentiel** : « cannot take damage FROM
ATTACKS » ne protège **pas** des dégâts de Burning, qui viennent d'une Réponse
forcée. C'est la réponse du pack à ce sbire, et sans ce cas le filtre
`is_from_attack` pourrait être absent sans que rien ne le voie. ⚠ La réserve
tombe à 4 et non à 5 : le samouraï a Coup Rapide, il attaque dès son entrée,
Sunfire défend, et Burning Aura pose une **seconde** brûlure.)

### sf015 : Tachyon Whip — **OUI**
(2 cas, rouges 2/2 ; ⚠ `"YourHero"` ne résout **pas** depuis une carte de
rencontre — `Select.GetYou(effect)` ne rend rien pour une carte qui n'appartient
à aucun joueur, et la Réponse ne partait jamais. Même leçon que `bk009` Portal.
On filtre sur l'HÔTE. ⚠ « cannot change to ALTER-EGO form » : la direction est
imprimée, un filtre absent bloquerait les deux sens.)

**16 cartes terminées sur 16.**
