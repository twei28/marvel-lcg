# Les mots-clés du moteur Marvel Champions : toutes les fiches

Compagnon de `KIT-CHATGPT-CREATION.md`. Rassemble les 60 fiches de `docs/reference/mots-cles/` (état du 08/10/2026), une par mot-clé.

**Comment t'en servir.** Dès qu'une carte porte un mot-clé (en gras sur le texte imprimé, ou dans `desc`), ouvre sa fiche ici AVANT d'écrire la carte. Chaque fiche donne : la définition imprimée, le mécanisme moteur (souvent : aucun script, le moteur le lit dans `desc`), une carte exemple, les pièges connus. Un mot-clé absent de ce fichier n'est pas géré : pose la question à l'utilisateur, puis écris `# A_FAIRE_CLAUDE:` au lieu d'inventer.

Les chemins de fichiers cités (`src/...`, `cards.json`) sont ceux du dépôt : tu ne peux pas les ouvrir, ils servent seulement à Claude lors de l'intégration.

⚠ **`Elite` n'est PAS un mot-clé** : c'est un TRAIT, déclaré dans `traits` (`"traits": ["ELITE"]`), jamais dans `desc`, sans mécanique moteur.

## Sommaire

**Mots-clés officiels**

- [Toughness](#toughness)
- [Guard](#guard)
- [Quickstrike](#quickstrike)
- [Retaliate](#retaliate)
- [Restricted](#restricted)
- [Permanent](#permanent)
- [Surge](#surge)
- [Villainous](#villainous)
- [Hazard](#hazard)
- [Crisis](#crisis)
- [Acceleration](#acceleration)
- [Amplify](#amplify)
- [Steady](#steady)
- [Stalwart](#stalwart)
- [Peril](#peril)
- [Incite](#incite)
- [Patrol](#patrol)
- [Hinder](#hinder)
- [Vulnerable](#vulnerable)
- [TeamUp](#teamup)
- [Alliance](#alliance)
- [Temporary](#temporary)
- [Piercing](#piercing)
- [Overkill](#overkill)
- [Ranged](#ranged)
- [Boost (icônes) et Boost ★ (effet)](#boost)
- [Special et l'étoile ★ d'une capacité permanente](#special)
- [Teamwork (TRAIT)](#teamwork)
- [Uses](#uses)
- [Setup](#setup)
- [Forced Action](#forced-action)
- [Victory X (dont X négatif)](#victory)
- [Requirement](#requirement)

**Mots-clés maison** (packs fan-made)

- [Éclair (ressource maison, `L`)](#eclair)
- [Seek (mot-clé maison, Rainy)](#seek)
- [Track (mot-clé maison, Rainy)](#track)
- [Acceleration (capacité d'identité, Rainy) — homonyme de l'icône](#acceleration-2099)
- [Drain X](#drain-x)
- [Traitor](#traitor)
- [Companion](#companion)
- [Squirrel](#squirrel)
- [Destroy (mot-clé maison, pack `sentinel`)](#destroy)
- [Exposed (carte d'état maison, pack `sentinel`)](#exposed)
- [Investigate X](#investigate-x)
- [Setlist](#setlist)
- [REGISTERED](#registered)
- [Weakness (mot-clé maison, ekAugust — aspect Venomized)](#weakness)
- [Showtime!](#showtime)
- [Armored (maison, pack `superior_iron_man`)](#armored)
- [Fragile](#fragile)
- [Legion](#legion)
- [Plotting](#plotting)
- [Breakthrough](#breakthrough)
- [Summon — MOT-CLÉ MAISON](#summon)
- [Multiverse](#multiverse)
- [Agile X — MOT-CLÉ MAISON](#agile)
- [Reckless (mot-clé maison, aspect Determination)](#reckless)
- [Alias (mot-clé maison, aspect Determination)](#alias)
- [Fleeting (mot-clé maison, aspect Determination)](#fleeting)

---

# Partie 1 : mots-clés officiels

<a id="toughness"></a>

## Toughness

**Texte imprimé / définition** : « Toughness. *(This character enters play with
a tough status card.)* » Un personnage avec ce mot-clé entre en jeu avec une
carte de statut « Tough ». C'est tout : le mot-clé ne dit rien de plus, ni
limite par round, ni clause sur la menace. Le compteur `Toughness` (`1`, `2`,
...) est réinitialisé à sa valeur imprimée à chaque reset des mots-clés.

**Mécanisme moteur** : clé `desc.Toughness` sur la carte, lue nativement
par le moteur. `HasToughness`
(`src/game/card/face/attribute/has_toughness.py`) enregistre l'attribut
`Toughness` -> `printed_toughness`, pose le statut « Tough » à l'entrée en
jeu (`OnWhenCardEnterPlay`, via `Faces.GiveStatus([self], "Tough",
Toughness(self))`) et restaure la valeur imprimée à chaque `OnResetKeywords`
via `GainToughness`. La classe `Toughness(GameRule)` de
`src/game/effect/rule.py` sert de justification (raison) à l'attribution du
statut.

Ce que fait ensuite la carte de statut relève d'elle, pas du mot-clé : le
statut est géré par `CanStatus`
(`src/game/card/face/attribute/can_status.py`, `tough`/`tough_max`/`IsTough`/
`DiscardTough`), et sa capacité vit dans `src/cards/pack/status/tough.py`. Elle
écoute `WhenUnitWouldTakeDamage` sur `"AttachedCharacter"` : elle appelle
`message.SetBeInstead(effect)` (les dégâts n'ont pas lieu) puis
`unit.DiscardTough(effect, rule=1)` (une carte Tough est défaussée), sauf si la
source porte `property.ignore_tough`. **Aucun script requis** pour ce mot-clé :
c'est une des « bases automatiques » du guide, à ne pas recoder inutilement
dans le `.py` de la carte.

**Carte exemple** : `01076` : * Luke Cage (`desc` contient `"Toughness":
"1"`), lu directement depuis `desc`, aucun script requis. Aucun fichier
`01076.py` trouvé dans `src/cards/pack` : cette carte n'a pas de capacité
imprimée distincte nécessitant un script.

**Pièges connus** :
- Le mot-clé ne fait qu'UNE chose : donner une carte de statut Tough à l'entrée
  en jeu. Toute la mécanique d'absorption appartient au statut, et se déclenche
  sur n'importe quels dégâts (`WhenUnitWouldTakeDamage`), qu'ils viennent d'une
  attaque ou d'une capacité de carte. Il n'y a **ni limite « une fois par
  round », ni clause sur la menace**.
- Une source peut ignorer le statut via `property.ignore_tough` (les dégâts
  perforants passent aussi outre : `can_attack.py` défausse alors tous les Tough
  via `DiscardTough(..., rule="All")` quand `IsPiercing()`).
- Distinguer le mot-clé `desc.Toughness` (état de départ) du statut Tough
  lui-même, qu'une autre carte peut donner ou retirer en cours de partie :
  `GainStatus` refuse d'en ajouter au-delà de `tough_max`.
- Ne pas confondre avec Guard, Retaliate ou Patrol, qui portent sur le ciblage
  ou sur le combat.
- Si une future carte cumule Toughness avec une capacité imprimée distincte,
  vérifier via `find` si un script existe pour cette carte : le script devra
  porter uniquement cette capacité annexe, jamais le mot-clé Toughness
  lui-même.

**Variantes maison** : aucune recensée pour l'instant.

---

<a id="guard"></a>

## Guard

**Texte imprimé / définition** : « Guard. *(While this minion is engaged with
you, you cannot attack the villain.)* » Tant qu'un sbire Guard est engagé avec
un joueur, CE joueur ne peut pas attaquer le vilain. C'est un compteur
(`Guard 1`, `Guard 2`, ...), réinitialisé à sa valeur imprimée à chaque reset
des mots-clés.

**Mécanisme moteur** : clé `desc.Guard` sur la carte, lue nativement par
le moteur. `HasGuard` (`src/game/card/face/attribute/has_guard.py`)
enregistre l'attribut `Guard` -> `printed_guard`, restaure la valeur à
chaque `OnResetKeywords` via `GainGuard`, qui appelle aussi
`ClearGuardPatrolEffectTargets` / `SetGuardPatrolEffectedBy`
(`src/game/card/face/card_type/minion.py`) : ce dernier marque les VILAINS de
la zone de jeu comme « affectés par » ce sbire, ce qui est l'indication visible
côté UI. L'interdiction elle-même est appliquée par
`Villain.CanBeAttackBy()` (`src/game/card/face/base/villain.py`), qui renvoie
`False` dès qu'un sbire engagé avec le joueur initiateur répond `IsGuard()`,
sauf si l'effet ignore le mot-clé (`effect.IsIgnoreKeyword('Guard', effect)`).
`Villain.GetGuardFaces()` renvoie la liste des sbires responsables du blocage.
`GainGuard` pose un `assert Minion.IsType(self)` : Guard est réservé aux
sbires. **Aucun script requis** pour ce mot-clé.

**Carte exemple** : `01101` : Hydra Mercenary (`desc` contient `"Guard":
"1"`), lu directement depuis `desc`, aucun script requis. Aucun fichier
`01101.py` trouvé dans `src/cards/pack` : cette carte n'a pas de capacité
imprimée distincte nécessitant un script.

**Pièges connus** :
- Guard bloque **uniquement l'attaque du vilain**. Les autres sbires restent
  attaquables, y compris le sbire Guard lui-même, qui est justement la façon
  normale de lever le blocage.
- Guard ne touche PAS le thwart : c'est Patrol qui interdit de contrecarrer le
  complot principal. Les deux passent par la même plomberie
  (`SetGuardPatrolEffectedBy`) mais ne bloquent pas la même chose ; ne pas
  confondre les deux fiches.
- La restriction est **par joueur** : un sbire Guard engagé avec un autre
  joueur ne vous empêche pas d'attaquer le vilain.
- Certains effets contournent le blocage via
  `effect.IsIgnoreKeyword('Guard', effect)` ; vérifier ce point avant de
  conclure à un bug de ciblage.
- Si une future carte cumule Guard avec une capacité imprimée annexe (par
  exemple une réaction au combat), vérifier via `find` si un script existe pour
  cette carte : le script devra porter uniquement cette capacité annexe, jamais
  le mot-clé Guard lui-même.

**Variantes maison** : aucune recensée pour l'instant.

---

<a id="quickstrike"></a>

## Quickstrike

**Texte imprimé / définition** : « Quickstrike. *(After this minion engages
your hero, it attacks.)* » Dès qu'un sbire Quickstrike s'engage avec un héros,
il attaque immédiatement. Ce n'est **pas** une règle d'ordre de résolution des
dégâts, c'est une attaque supplémentaire déclenchée par l'engagement. C'est un
compteur (`Quickstrike 1`, `Quickstrike 2`, ...), réinitialisé à sa valeur
imprimée à chaque reset des mots-clés.

**Mécanisme moteur** : clé `desc.Quickstrike` sur la carte, lue nativement
par le moteur. `HasQuickstrike`
(`src/game/card/face/attribute/can_quickstrike.py`) enregistre l'attribut
`Quickstrike` -> `printed_quickstrike`, restaure la valeur à chaque
`OnResetKeywords` via `GainQuickstrike`, et expose `IsQuickstrike()`. La
sous-classe `CanQuickstrike` fournit `ResolveQuickstrike(player)` : si la carte
est en jeu, si `IsQuickstrike()` et si `player.IsHero()`, elle fabrique l'effet
`Quickstrike(self)` (`src/game/effect/rule.py`) et déclenche
`DoAttackYou(player, effect)` pour un `Enemy`, ou `BasicAttack` pour les autres
porteurs de `CanAttack`. L'appel se fait dans `Minion.OnEngagePlayer`
(`src/game/card/face/card_type/minion.py`), juste après
`Message.WhenMinionEngagePlayer` et avant `Message.AfterMinionEngagePlayer`.
**Aucun script requis** pour ce mot-clé.

**Carte exemple** : `01167` : * Vulture (`desc` contient `"Quickstrike":
"1"`), lu directement depuis `desc`, aucun script requis. Aucun fichier
`01167.py` trouvé dans `src/cards/pack` : cette carte porte aussi
`Nemesis: Spider-Man`, un autre mot-clé, sans que cela nécessite de script
propre (le nemesis est également géré nativement).

**Pièges connus** :
- Quickstrike n'a **rien à voir avec un ordre de résolution des dégâts** face à
  Retaliate. C'est une attaque déclenchée à l'engagement, point.
- Le déclenchement est conditionné à `player.IsHero()` : un sbire qui s'engage
  avec un joueur en alter-ego n'attaque pas.
- Il se déclenche à l'**engagement**, pas à chaque activation. Un sbire déjà
  engagé qui le reste ne rejoue pas son Quickstrike. En revanche un sbire mis
  en jeu directement engagé y passe : `Minion.OnWhenCardEnterPlay` appelle
  `OnEngagePlayer` quand `card.area.flags.is_engaged` est vrai.
- Ne pas coder l'attaque à la main dans le `.py` d'une carte Quickstrike : le
  moteur l'orchestre depuis le compteur `desc`. Si une future carte cumule
  Quickstrike avec une capacité imprimée annexe, vérifier via `find` si un
  script existe pour cette carte : le script devra porter uniquement cette
  capacité annexe, jamais le mot-clé Quickstrike lui-même.

**Variantes maison** : aucune recensée pour l'instant.

---

<a id="retaliate"></a>

## Retaliate

**Texte imprimé / définition** : « Retaliate 1. *(After this character is
attacked, deal 1 damage to the attacking character.)* » Après qu'un personnage
Retaliate a été attaqué, l'attaquant subit un nombre de dégâts égal à la valeur
de Retaliate. C'est un compteur (`Retaliate 1`, `Retaliate 2`, ...),
réinitialisé à sa valeur imprimée à chaque reset des mots-clés.

**Mécanisme moteur** : clé `desc.Retaliate` sur la carte, lue nativement
par le moteur. `HasRetaliate`
(`src/game/card/face/attribute/can_retaliate.py`) enregistre l'attribut
`Retaliate` -> `printed_retaliate`, restaure la valeur à chaque
`OnResetKeywords` via `GainRetaliate`, et fournit
`ResolveRetaliate(atk_message)` qui applique les dégâts en retour en
s'appuyant sur la classe `Retaliate(GameRule)` de
`src/game/effect/rule.py` comme justification de l'effet. Trois conditions y
sont vérifiées avant le `attacker.TakeDamage(...)` : l'attaquant existe et
n'est pas vaincu, l'attaque n'est pas à distance (`atk_message.IsRanged()`) et
le défenseur n'est pas vaincu, et l'attaque n'ignore pas le mot-clé
(`atk_message.IsIgnoreRetaliate()`). Sinon un `Message.AfterIgnoreKeywordOnCard`
est émis à la place. L'appel vient de `can_attack.py` et de
`src/game/effect/effect_invoke.py`. **Aucun script requis** pour ce mot-clé.

**Carte exemple** : `01040a` : * Black Panther (`desc` contient
`"Retaliate": "1"`), lu directement depuis `desc`, aucun script requis.
Aucun fichier `01040a.py` trouvé dans `src/cards/pack` : cette face de
carte n'a pas de capacité imprimée distincte nécessitant un script.

**Pièges connus** : trois cas où Retaliate ne se déclenche pas, tous lisibles
dans `ResolveRetaliate` : attaque **à distance** (`IsRanged()`), défenseur ou
attaquant **déjà vaincu** au moment de la résolution, et attaque qui **ignore
Retaliate** (`IsIgnoreRetaliate()`). Aucun rapport en revanche avec Quickstrike :
ce mot-clé n'est pas une règle d'ordre de résolution des dégâts, c'est une
attaque déclenchée quand un sbire s'engage avec un héros (voir sa fiche), et il
n'a aucune interaction particulière avec Retaliate. Si une future carte
cumule Retaliate avec une capacité imprimée annexe (déclencheur sur les
dégâts infligés, par exemple), vérifier via `find` si un script existe
pour cette carte : le script devra porter uniquement cette capacité
annexe, jamais le mot-clé Retaliate lui-même. La carte `03009` (Captain
America's Shield) illustre ce piège concret ailleurs dans le catalogue :
elle a un script (`AbilityFactory.GiveKeywordToAttached`), mais ce script
code sa capacité d'ATTACHEMENT (donner Defense 1 et Retaliate 1 à
Captain America), pas le mot-clé Retaliate en tant que tel.

**Variantes maison** : aucune recensée pour l'instant.

---

<a id="restricted"></a>

## Restricted

**Texte imprimé / définition** : « Restricted. » Un héros ne peut pas
avoir plus de deux cartes Restricted en jeu sous son contrôle en même
temps (limite globale, toutes cartes Restricted confondues, pas par
carte). C'est un compteur (`Restricted 1` en général), réinitialisé à sa
valeur imprimée à chaque reset des mots-clés.

**Mécanisme moteur** : clé `desc.Restricted` sur la carte, lue nativement
par le moteur. `HasRestricted`
(`src/game/card/face/attribute/has_restricted.py`) enregistre l'attribut
`Restricted` -> `printed_restricted`, et vérifie la limite via
`CheckRestrictedLimit`, qui délègue à
`player.limit_restricted.CheckLimit` (voir
`src/game/player/limit_monitor/restricted_limit.py`). Le contrôle
s'applique à l'entrée en jeu (`OnWouldEnterPlay`, peut empêcher la carte
d'entrer en jeu si la limite est dépassée), à la sortie de jeu et au
retournement d'une carte (recalcul de la limite). **Aucun script requis**
pour la restriction elle-même : c'est une des « bases automatiques » du
guide, à ne pas recoder inutilement dans le `.py` de la carte.

**Carte exemple** : `03009` : * Captain America's Shield (`desc` contient
`"Restricted": "1"`), lu directement depuis `desc` pour la limite
Restricted elle-même. Un fichier `03009.py` existe bien
(`src/cards/pack/cap/captain_america/03009.py`), mais son contenu
(`AbilityFactory.GiveKeywordToAttached(CardFinder(name="Captain
America"), defense=1, retaliate=1)`) code la capacité imprimée
d'attachement de la carte (donner Defense 1 et Retaliate 1 à Captain
America), pas le mot-clé Restricted. Le script ne doit pas et ne recode
pas la limite Restricted.

**Pièges connus** : ne pas ajouter de logique de comptage Restricted dans
le `.py` d'une carte : c'est entièrement pris en charge par le moteur via
`limit_restricted`. Le cas `03009` est un exemple concret et vérifié où le
script existant sert exclusivement à une autre capacité imprimée que le
mot-clé lui-même ; toute nouvelle fiche/carte Restricted doit vérifier de
la même façon (via `find`) si un script présent code autre chose que la
restriction.

**Variantes maison** : aucune recensée pour l'instant.

---

<a id="permanent"></a>

## Permanent

**Texte imprimé / définition** : « Permanent. » Une carte avec ce mot-clé
ne peut pas quitter le jeu par les moyens normaux (défausse, retrait,
retour en main, etc.) tant que l'effet qui tenterait de le faire ne
provient pas du même set qu'elle. C'est un indicateur booléen (`Permanent
1`), réinitialisé à sa valeur imprimée à chaque reset des mots-clés.

**Mécanisme moteur** : clé `desc.Permanent` sur la carte, lue nativement
par le moteur. `HasPermanent`
(`src/game/card/face/attribute/has_permanent.py`) enregistre l'attribut
`Permanent` -> `printed_permanent` (bool). Dans `OnWhenCardLeavePlay`, si
`self.permanent` est vrai et que l'effet qui retire la carte
(`by_effect.this.paper.set_name`) appartient à un set différent de celui
de la carte, la sortie de jeu est bloquée (`return False`) ; quelques
exceptions nommées (Flight/Super Strength/Telepathy, Weather/Storm, Power
Stone, Milano) sont codées en dur dans ce fichier moteur, pas dans les
scripts de cartes. **Aucun script requis** pour le mot-clé Permanent
lui-même : c'est une des « bases automatiques » du guide, à ne pas
recoder inutilement dans le `.py` de la carte.

**Carte exemple** : `04159a` : Basic Thwart Upgrade (`desc` contient
`"Permanent": "1"`), lu directement depuis `desc` pour l'aspect
« impossible à retirer » lui-même. Un fichier `04159a.py` existe bien
(`src/cards/pack/trors/hydra_campaign/04159a.py`), mais son contenu
(`AbilityFactory.GiveKeywordToAttached("You", health=2)` et
`AbilityFactory.GiveKeywordToAttached(Hero, thwart=1)`) code la capacité
imprimée de la carte (donner +2 HP à vous et +1 THW aux héros), pas le
mot-clé Permanent. Le script ne doit pas et ne recode pas le blocage de
sortie de jeu.

**Pièges connus** : ne pas coder de garde-fou « empêcher la défausse »
dans le `.py` d'une carte Permanent : c'est géré nativement par
`HasPermanent.OnWhenCardLeavePlay`. Le cas `04159a` est un exemple concret
et vérifié où le script existant sert exclusivement à une autre capacité
imprimée que le mot-clé lui-même. Attention également aux exceptions
codées en dur par nom de set/carte dans `has_permanent.py` : elles ne sont
pas généralisables, toute nouvelle carte Permanent avec un comportement
similaire nécessiterait une modification du moteur, pas un script de
carte isolé.

**Variantes maison** : aucune recensée pour l'instant.

---

<a id="surge"></a>

## Surge

**Texte imprimé / définition** : « Surge. » Quand une carte Rencontre avec ce mot-clé est révélée, une carte Rencontre supplémentaire est piochée immédiatement. Le compteur `Surge` (`1`, `2`, ...) fixe le nombre de pioches supplémentaires déclenchées.

**Mécanisme moteur** : clé `desc.Surge` sur la carte, lue nativement par le moteur. `HasSurge` et `CanSurge` (`src/game/card/face/attribute/can_surge.py`) enregistrent l'attribut `Surge` -> `printed_surge`, restaurent la valeur à chaque `OnResetKeywords` via `GainSurge`. Quand Surge se déclenche, `ResolveSurge()` déale une ou plusieurs cartes Rencontre via `player.DealEncounterCards()`. La classe `Surge(GameRule)` dans `src/game/effect/rule.py` sert de justification. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `01121` : Weapons Runner (`desc` contient `"Surge": "1"`), lu directement depuis `desc`, aucun script requis. Un fichier `01121.py` existe dans `src/cards/pack` : ce script gère une capacité imprimée annexe (entrée en jeu comme boost), pas le mot-clé Surge.

**Pièges connus** : Surge s'ajoute à la pioche standard des cartes Rencontre, il n'est pas une variante de celle-ci ; il faut compter la perte de contrôle engendrée par la pioche supplémentaire. Si une future carte cumule Surge avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Surge lui-même.

**Variantes maison** : aucune recensée pour l'instant.

---

<a id="villainous"></a>

## Villainous

**Texte imprimé / définition** : « Villainous. *(When this minion activates,
give it a boost card.)* » Un sbire Villainous reçoit une carte de boost à
chacune de ses activations, exactement comme le vilain. Cela n'a **aucun
rapport avec les règles d'engagement**. C'est un compteur (`Villainous 1`,
`Villainous 2`, ...), réinitialisé à sa valeur imprimée à chaque reset des
mots-clés.

**Mécanisme moteur** : clé `desc.Villainous` sur la carte, lue nativement par
le moteur. `HasVillainous`
(`src/game/card/face/attribute/has_villainous.py`) enregistre l'attribut
`Villainous` -> `printed_villainous`, restaure la valeur à chaque
`OnResetKeywords` via `GainVillainous`, et hérite de `CanBoost` pour surcharger
`GetBoostCardNum()`, qui retourne 1 si `IsVillainous()` et 0 sinon. Ce
`GetBoostCardNum()` est consulté à chaque activation : par `can_attack.py`
(appel à `GiveFacedownBoostCardsInternal(GetBoostCardNum(...) +
additional_boost_card, ...)`) pour une attaque, et par `can_scheme.py` pour un
plan. C'est la même surcharge que celle de `Villain.GetBoostCardNum()`
(`src/game/card/face/base/villain.py`), qui renvoie 1 sans condition : un sbire
Villainous se comporte donc, pour le boost, comme le vilain. **Aucun script
requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `11041` : * Deathunt 9000 (`desc` contient `"Villainous":
"1"`, plus `"Toughness": "1"`), lu directement depuis `desc`, aucun script
requis pour le mot-clé. Le fichier `11041.py` existe et code la capacité
imprimée `[star] Boost` (« Give this enemy a tough status card and another
boost card », via `AbilityFactory.WhenCardBecomeBoost`), pas le mot-clé
Villainous.

**Pièges connus** :
- Villainous ne modifie **pas** les règles d'engagement. C'est une source de
  carte de boost à l'activation, rien d'autre.
- Ne pas confondre avec `desc.Boost` (`HasBoostIcon`,
  `src/game/card/face/attribute/has_boost_icon.py`, attribut
  `printed_boost`) : cette clé-là compte les icônes de boost imprimées sur la
  carte quand ELLE sert de boost à quelqu'un d'autre. `11041` n'a d'ailleurs
  aucune clé `Boost`, contrairement à `01101` ou `16119`.
- Mot-clé de sbire uniquement.
- Si une future carte cumule Villainous avec une capacité imprimée distincte
  (c'est le cas de `11041`), vérifier via `find` si un script existe : le script
  devra porter uniquement cette capacité annexe, jamais le mot-clé Villainous
  lui-même.

**Variantes maison** : aucune recensée pour l'instant.


### Variante : un HÉROS qui gagne Villainous (dd001a Doctor Doom, hc010 Outer Demons)

Depuis le 01/09/2026, `Hero` hérite de `HasVillainous` : un héros villainous
reçoit une carte boost à chaque **attaque de base** (`can_attack.py:264`),
ses icônes s'ajoutent à l'ATQ, et `ResolveBoostCards` envoie les messages
`WhenBoostCardTurnedFaceUp` (une carte peut donc y réagir : hc010 annule
l'effet Boost et soigne 1). Deux façons de l'accorder :

- temporaire : `hero.GainUntilRoundEnd(effect, villainous=1)` (dd001a) ;
- continu, par une amélioration : `*GiveKeywordToAttached(CardFinder(name=…),
  villainous=1)` (hc010, paramètre ajouté le 11/09/2026 à `asset.py` et
  `asset_helper.py`).

⚠ **Attaque seulement.** Le contre de base ne distribue pas de boost
(`can_thwart.py` n'a pas l'équivalent). Écart assumé sur les deux packs, noté
dans leurs gabarits. Les effets [star] Boost des cartes de rencontre ne se
déclenchent que sur une activation d'ENNEMI : pour un héros, seule l'icône
compte.

---

<a id="hazard"></a>

## Hazard

**Texte imprimé / définition** : « Hazard. » Rappel imprimé sur les cartes qui le portent (ex. `01107`) : « Hazard Icon: Deal +1 encounter card during the villain phase. » Le compteur `Hazard` (`1`, `2`, ...) fixe le nombre d'icônes Hazard portées par la carte.

**Mécanisme moteur** : clé `desc.Hazard` sur la carte, lue nativement par le moteur. `HasHazard` (`src/game/card/face/attribute/has_hazard.py`) enregistre l'attribut `Hazard` -> `printed_hazard`, restaure la valeur à chaque `OnResetKeywords` via `GainHazard`. `Worlds.GetHazardIcons`/`GetIconsNum` (`src/game/operate/worlds.py`) comptent les icônes Hazard en jeu ; ce total pilote le nombre de cartes Rencontre supplémentaires tirées pendant la phase vilain. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `01107` : Breakin' & Takin' (`desc` contient `"Hazard": "1"`), lu directement depuis `desc`, aucun script requis. Un fichier `01107.py` existe dans `src/cards/pack` : ce script gère une capacité imprimée annexe (placement de threat à la révélation), pas le mot-clé Hazard.

**Pièges connus** : ne pas confondre avec Acceleration, qui agit au début de la phase vilain en posant du threat plutôt qu'en tirant des cartes.

> **Distinguer les deux ICÔNES imprimées** (relevé le 30/08/2026 sur le pack
> `howard_the_duck`, tranché par l'utilisateur ; les deux se ressemblent
> beaucoup et une lecture au jugé les confond) :
> - **Aléa / Hazard** : une carte à jouer **penchée**, portant une croix, et
>   **rien en dessous**. Exemple : `hd022` Duck and Cover!
> - **Acceleration** : la même croix, mais la forme porte une **pointe/flèche
>   vers le haut à droite** ET une **barre épaisse de soulignement** en
>   dessous. Exemples : `hd026` A Fowl Plot, `ag011` Assassination Plot.
>
> Méthode de vérification employée : découper la bande basse du cadre de
> texte des cartes à comparer, agrandir ×2, et les mettre côte à côte (une
> carte du dépôt dont le `desc` déclare déjà le mot-clé sert de témoin —
> ici `ag011`, qui déclare `Acceleration`). Une manigance sans aucune icône
> (`hd025` Duck, Duck, Doom!) sert de contrôle négatif : elle prouve que
> l'icône n'est pas un décor du gabarit. Les cartes Hazard peuvent cumuler plusieurs icônes Hazard (compteur > 1), chaque icône déclenchant une pioche supplémentaire. Si une future carte cumule Hazard avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Hazard lui-même.

> ### ✅ TROISIÈME MÉTHODE, PLUS SÛRE QUE L'ŒIL (09/09/2026)
>
> La comparaison de bandes découpées reste valable, mais il existe désormais
> plus direct : **l'icône est un glyphe de `public/fonts/ChampionsIcons.ttf`**,
> la police officielle, et `public/css/marvel/icon.css` dit lequel.
>
> - `H` → `.icon-hazard` : une carte penchée, un plus évidé sur son bord
>   gauche, **rien en dessous**.
> - `A` → `.icon-acceleration` : la même carte, mais une **pointe en haut à
>   droite** et une **barre épaisse dessous**.
>
> Méthode : rendre les deux glyphes avec Pillow à la même taille, les poser
> côte à côte du scan agrandi, et regarder. Aucune ambiguïté ne survit à cette
> comparaison. C'est ainsi qu'a été tranchée `vz031` First Contact, dont
> l'icône était restée « non identifiée » à son premier portage — elle porte
> **Hazard 1**, ce qui équilibre une amélioration à 2 qui donne +1 aux trois
> pouvoirs. Précédent exact : `27191` Symbiote Suit, la carte basique citée
> par la decklist du même auteur, qui déclare aussi `"Hazard": "1"` sans que
> son texte ne mentionne le mot.
>
> ⚠ **Le `desc` est la SEULE trace** : le texte de ces cartes ne dit pas
> « Hazard », seule l'icône le dit. `verifier_desc_mots_cles.py` ne peut donc
> pas l'attraper, et un oubli reste invisible. Le cas
> « vz031 First Contact » de `test_capacites.py` mesure l'icône en jeu par la
> clé `icones`, ajoutée pour cela.

**Variantes maison** : aucune recensée pour l'instant.

---

<a id="crisis"></a>

## Crisis

**Texte imprimé / définition** : « Crisis. » Un schéma annexe avec ce mot-clé force une réponse immédiate du joueur : il doit être vaincu avant que le threat puisse être retiré du schéma principal. Le compteur `Crisis` (`1`, `2`, ...) fixe le nombre de charges de crise.

**Mécanisme moteur** : clé `desc.Crisis` sur la carte, lue nativement par le moteur. `CanCrisis` (`src/game/card/face/attribute/has_crisis.py`) enregistre l'attribut `Crisis` -> `printed_crisis`, restaure la valeur à chaque `OnResetKeywords` via `GainCrisis`. Quand un schéma Crisis entre en jeu, `SetCrisisEffectedBy()` marque le complot principal comme affecté (`scheme.card.ui.SetEffectedBy(diff, GameRule(self))`). Le blocage réel se joue dans `CardFace.RemoveThreatFromSchemes` (`src/game/card/face/card_face.py`) : sa signature porte un paramètre `ignore_crisis` que le moteur enregistre via une règle temporaire (`AbilityFactory.UnitIgnoreKeywordIcons(..., crisis=True)`) quand une carte veut explicitement passer outre. C'est donc un vrai contrôle côté moteur, intégré à la fonction de retrait de menace elle-même, pas une simple restriction d'affichage. **Aucun script requis** pour ce mot-clé lui-même : c'est une des « bases automatiques » du guide.

**Carte exemple** : `01108` : Crowd Control (`desc` contient `"Crisis": "1"`), lu directement depuis `desc`, aucun script requis. Aucun fichier `01108.py` trouvé dans `src/cards/pack` : cette carte ne porte que le mot-clé Crisis, sans capacité imprimée annexe.

**Pièges connus** : Crisis bloque le retrait de menace sur le complot principal au niveau de `RemoveThreatFromSchemes` lui-même, pas via une règle de perte de PV. Une carte qui veut explicitement l'ignorer doit passer `ignore_crisis=True` à cet appel. Ne pas confondre avec Peril, qui agit de manière similaire mais sur un autre déclencheur. Si une future carte cumule Crisis avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Crisis lui-même.

### ⚠ MISE À JOUR DU 11/09/2026 : la Crise verrouille désormais la CIBLE

La description ci-dessus était exacte mais **incomplète**, et cette lacune a
coûté une partie à un joueur. Jusqu'à cette date, la Crise ne bloquait qu'**à
la résolution** : le complot principal restait proposé comme cible d'un
contre, le joueur y jouait sa carte, et `RemoveThreatInternal` rendait 0. La
carte partait en défausse sans rien faire, sans un mot. Le joueur a annulé et
rejoué le même coup trois fois avant de signaler le problème.

Or ses deux sœurs verrouillent **au ciblage** :

| Mot-clé | Où il verrouille |
|---|---|
| Garde | `Villain.CanBeAttackBy` (`base/villain.py`) |
| Patrouille | `MainScheme.CanBeThwartBy` (`card_type/scheme_main.py`) |
| **Crise** | **`MainScheme.CanBeThwartBy`, depuis le 11/09/2026** |

Le complot principal n'est donc plus offert à un contre tant qu'une icône de
crise est en jeu. La condition est **identique** à celle de la résolution
(`Worlds.GetCrisisFaces(...)` et `IsIgnoreKeyword('Crisis', ...)`), sans
`IsPlayerInitiator()` : une divergence entre ce que le moteur propose et ce
qu'il résout serait pire que le trou d'origine.

#### Conséquence pour une carte qui ignore la Crise

`ignore_crisis=True` passé à `RemoveThreatFromSchemes` n'agit qu'à la
résolution, donc **trop tard pour le ciblage**. Une carte qui est un
**contre** (`SetLabel('thwart')`) doit en plus le **déclarer** sur sa
capacité :

```python
.SetIgnoreKeyword('Crisis')
```

C'est ce que lit `IsIgnoreKeyword` au moment du calcul des cibles légales.
Les cartes qui retirent de la menace par une **Action** (et non un contre) ne
sont pas concernées : elles ne passent pas par `CanBeThwartBy`.

⚠ **Gate dédiée** : `tools/verifier_ignore_crise.py` échoue si un contre
ignore la Crise sans la déclarer. Calibrée en retirant la ligne de `90119`.

#### Les deux cartes alignées ce jour-là

- **`90119` Search and Rescue** (pack `rescue_rainy`) : le seul vrai contre du
  dépôt à ignorer la Crise. Les six autres cartes à `ignore_crisis=True` sont
  des Actions.
- **`15012` Crisis Averted** (pack `scw`) : le cas limite. Elle n'ignore la
  Crise **que si elle a été payée avec une ressource mentale**, or le paiement
  vient APRÈS le ciblage (`effect_checker` : `check_target` puis `check_pay`).
  Son ignorance est donc déclarée avec **`paid_with="B"`** (voir ci-dessous) :
  vraie tant que rien n'est payé (la carte reste ciblable), tranchée à la
  résolution selon les ressources réellement dépensées. Payée sans mental
  sous une Crise, elle ne retire donc rien : c'est le texte de la carte, et
  le plateau **demande confirmation** avant d'envoyer un tel paiement.
  ⚠ Cette carte avait été **ratée par un grep** sur `ignore_crisis=True` :
  elle passe par une variable locale. C'est la gate qui l'a trouvée.
- **`hc006` On the Prowl** (pack `hellcat`) : même famille, variante « using
  **only** [mental] » : `paid_with="B", only=True` (`OnlyHasColor`), sur
  `'Crisis'` et `'Patrol'`. ⚠ La première gate ne la voyait pas
  (`ignore_crisis=mental`, une variable) ; corrigée le 11/09/2026 au soir.

#### L'ignorance qui dépend du paiement : `paid_with` (11/09/2026 au soir)

```python
.SetIgnoreKeyword('Crisis', paid_with="B")              # au moins une mentale (15012)
.SetIgnoreKeyword('Crisis', 'Patrol', paid_with="B", only=True)  # rien d'autre (hc006)
```

`Ability.SetIgnoreKeyword` construit la condition (rien de payé, ou la
couleur ; joker compris) **et** la garde dans `AbilityIgnore.paid_with` /
`paid_only`. Au rendu d'une option (`Effect.Render`, `get_warning`), si la
cible est un complot principal verrouillé par ce mot-clé, le descripteur
porte `target_payment[*].warning = {"keyword", "paid_with", "mode"}`. Le
plateau (`ask.ts`, `coupSansEffet`) compare les lettres du paiement choisi et
ouvre une **confirmation** (`ConfirmationJeu`, Continuer / Annuler, FR et EN)
si aucune ne convient ; il ne connaît ni la carte ni la règle. Décision
utilisateur du 11/09/2026 : prévenir au moment de payer, par une modale, le
moteur calcule.

⚠ **Ne jamais écrire cette condition à la main** (`condition=lambda effect:
effect.GetPaidResources()...`) : la règle serait la même, mais le rendu ne
saurait rien, et le joueur perdrait sa carte sans un mot. La gate
`verifier_ignore_crise.py` refuse cette forme dès que la lambda lit le
paiement (`br002`, dont la condition ne lit pas le paiement, reste libre).
Harnais : trois cas « MODALE » (15012 sous Crise, témoin sans Crise, témoin
fort payé sans mental) plus un cas hc006 en mode `only`.

#### Côté plateau

Le complot principal porte une pastille rouge « Crise » tant qu'une manigance
annexe à Crise est en jeu, et l'aperçu au survol nomme la manigance
responsable (`zones.ts`, `avecCrise` ; `ScanCard`, `pastille-crise`).

**Variantes maison** : aucune recensée pour l'instant.

---

<a id="acceleration"></a>

## Acceleration

**Texte imprimé / définition** : « Acceleration. » Rappel imprimé sur les cartes qui le portent (ex. `01109`) : « Acceleration Icon: Place +1 threat on the main scheme at the start of the villain phase. » Le compteur `Acceleration` (`1`, `2`, ...) fixe le nombre d'icônes Acceleration portées par la carte.

**Mécanisme moteur** : clé `desc.Acceleration` sur la carte, lue nativement par le moteur. `HasAccelerationIcon` (`src/game/card/face/attribute/has_acceleration_icon.py`) enregistre l'attribut `Acceleration` -> `printed_acceleration_icon`, restaure la valeur à chaque `OnResetKeywords` via `GainAccelerationIcon`. `Worlds.GetIconsNum` (`src/game/operate/worlds.py`) compte les icônes Acceleration en jeu ; ce total pilote le threat posé sur le complot principal au début de la phase vilain. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `01109` : Bomb Scare (`desc` contient `"Acceleration": "1"`), lu directement depuis `desc`, aucun script requis. Un fichier `01109.py` existe dans `src/cards/pack` : ce script gère une capacité imprimée annexe (placement de threat à la révélation), pas le mot-clé Acceleration.

**Pièges connus** : ne pas confondre avec Hazard, qui agit pendant la phase vilain en tirant des cartes Rencontre supplémentaires plutôt qu'en posant du threat.

> **Distinguer les deux ICÔNES imprimées** : voir l'encadré de `hazard.md`,
> qui donne la différence visuelle exacte (Acceleration = pointe vers le haut
> **+ barre de soulignement** ; Aléa = carte penchée **nue**) et la méthode de
> découpe employée le 30/08/2026 pour la trancher. `ag011` Assassination Plot
> est le témoin de référence du dépôt pour l'icône Acceleration : son `desc`
> déclare `Acceleration` et son scan porte bien la forme à pointe + barre. Les cartes Acceleration peuvent cumuler plusieurs icônes (compteur > 1), chaque icône plaçant un threat supplémentaire. Si une future carte cumule Acceleration avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Acceleration lui-même.

**Variantes maison** : aucune, mais ⚠ **un homonyme existe, et il est
désormais porté** : voir la fiche dédiée **`acceleration-2099.md`**. Le pack
fan-made **Spider-Man 2099** (Rainy) appelle « *Acceleration* » une CAPACITÉ
D'IDENTITÉ (défausser depuis le dessus du deck jusqu'à un événement, le jouer,
puis remettre les autres cartes sous le deck), sans aucun rapport avec l'icône
décrite ici. Six cartes du pack testent « si tu as joué cette carte via ta
capacité *Acceleration* ». `desc.Acceleration` et `HasAccelerationIcon` ne
sont **pas** employés par ce pack : ce sont deux notions différentes sous le
même mot.

⚠ **Et `sm013` Future in Crisis porte les DEUX** : c'est une obligation du
pack Spider-Man 2099 qui déclare bien `desc.Acceleration` (l'icône, celle de
cette fiche) alors que le héros du même pack porte la capacité homonyme.
Vérifié par comparaison d'image contre `ag011` le 08/09/2026.

---

<a id="amplify"></a>

## Amplify

**Texte imprimé / définition** : « Amplify. » Quand une carte boost est retournée face-up pendant l'activation d'un ennemi, ajouter un icône boost supplémentaire pour chaque schéma annexe en jeu avec ce mot-clé. Le compteur `Amplify` (`1`, `2`, ...) fixe le nombre d'icônes Amplify portées par la carte.

**Mécanisme moteur** : clé `desc.Amplify` sur la carte, lue nativement par le moteur. `HasAmplify` (`src/game/card/face/attribute/has_amplify.py`) enregistre l'attribut `Amplify` -> `printed_amplify`, restaure la valeur à chaque `OnResetKeywords` via `GainAmplify`. Quand une carte boost est révélée durant l'activation d'un ennemi, `ResolveAmplify()` compte les icônes Amplify en jeu et ajoute autant d'icônes boost via `face.GainBoostIcons()`. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `16054` : Vendetta (`desc` contient `"Amplify": "1"`), lu directement depuis `desc`, aucun script requis. Aucun fichier `16054.py` trouvé dans `src/cards/pack` : cette carte ne porte que le mot-clé Amplify, sans capacité imprimée annexe.

**Pièges connus** : Amplify s'ajoute aux icônes boost d'une carte révélée, il ne remplace pas les icônes existants. Les cartes Amplify peuvent cumuler plusieurs icônes (compteur > 1), chaque icône ajoutant un boost supplémentaire à la carte révélée. Amplify s'applique uniquement au moment de la révélation d'un boost ; c'est un modificateur d'activation d'ennemi, pas une propriété permanente de la carte boost. Si une future carte cumule Amplify avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Amplify lui-même.

**Variantes maison** : aucune recensée pour l'instant.

---

<a id="steady"></a>

## Steady

**Texte imprimé / définition** : « Steady. » Un personnage avec ce mot-clé peut avoir jusqu'à deux compteurs Stun supplémentaires et deux compteurs Confuse supplémentaires. Ce personnage n'est étourdi que s'il a déjà deux compteurs Stun (au lieu de un), et n'est confus que s'il a déjà deux compteurs Confuse (au lieu de un). Quand l'effet d'un statut de ce type résout (en remplacement de l'activation), tous les compteurs du type en question sont retirés.

**Mécanisme moteur** : clé `desc.Steady` sur la carte, lue nativement par le moteur. `HasSteady` (`src/game/card/face/attribute/has_steady.py`) enregistre l'attribut `Steady` -> `printed_steady`, stocke le compteur `Steady` via la clé `desc`, et restaure sa valeur à chaque `OnResetKeywords` via `GainSteady`. La classe `Steady(GameRule)` dans `src/game/effect/rule.py` sert de justification (raison) à l'attribution du compteur. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide, à ne pas recoder inutilement dans le `.py` de la carte.

**Carte exemple** : `27074` : * Venom (`desc` contient `"Steady": "1"`), lu directement depuis `desc`, aucun script requis. Un fichier `27074.py` existe dans `src/cards/pack` : ce script gère des capacités imprimées annexes, pas le mot-clé Steady.

**Pièges connus** : Steady ne s'applique que aux statuts Stun et Confuse ; ne pas confondre avec les autres mot-clés de protection. Si une future carte cumule Steady avec une capacité imprimée distincte, vérifier via `find` si un script existe pour cette carte : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Steady lui-même.

**Variantes maison** : aucune recensée pour l'instant.

---

<a id="stalwart"></a>

## Stalwart

**Texte imprimé / définition** : « Stalwart. » Un personnage avec ce mot-clé ne peut pas être étourdi ni confus. Le compteur `Stalwart` (`1`, `2`, ...) fixe le nombre de chargés Stalwart disponibles.

**Mécanisme moteur** : clé `desc.Stalwart` sur la carte, lue nativement par le moteur. `HasStalwart` (`src/game/card/face/attribute/has_stalwart.py`) enregistre l'attribut `Stalwart` -> `printed_stalwart`, restaure la valeur à chaque `OnResetKeywords` via `GainStalwart` et discard tout compteur Stun ou Confuse existant quand le mot-clé est gagné. La classe `Stalwart(GameRule)` dans `src/game/effect/rule.py` sert de justification. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `16133` : Kree Lieutenant (`desc` contient `"Stalwart": "1"`), lu directement depuis `desc`, aucun script requis. Le script `16133.py` existe et code une capacité d'icône de boost supplémentaire (« When this card becomes a boost, gain 3 boost icons »), pas le mot-clé lui-même : le moteur lit `Stalwart` nativement dans `desc`, aucun module n'est nécessaire pour lui.

**Pièges connus** : ne pas confondre avec d'autres mot-clés de protection (Guard, Retaliate, Toughness). Si une future carte cumule Stalwart avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Stalwart lui-même.

**Variantes maison** : aucune recensée pour l'instant.

---

<a id="peril"></a>

## Peril

**Texte imprimé / définition** : « Peril. » Pendant qu'un joueur résout une carte Rencontre avec ce mot-clé, ce joueur ne peut consulter aucun autre joueur, et les autres joueurs ne peuvent jouer aucune carte ni déclencher d'abilité. Le compteur `Peril` (`1`, `2`, ...) fixe le nombre de charges Peril disponibles.

**Mécanisme moteur** : clé `desc.Peril` sur la carte, lue nativement par le moteur. `HasPeril` (`src/game/card/face/attribute/has_peril.py`) enregistre l'attribut `Peril` -> `printed_peril`, restaure la valeur à chaque `OnResetKeywords` via `GainPeril`. L'isolement du joueur et l'interdiction pour les autres de jouer sont appliqués par le moteur lors de la résolution de la carte. La classe `Peril(GameRule)` dans `src/game/effect/rule.py` sert de justification. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `16145` : Blind Side (`desc` contient `"Peril": "1"`), lu directement depuis `desc`, aucun script requis. Le script `16145.py` existe et code la capacité de révélation (« When revealed, choose one: exhaust the Milano or pay RR. If you don't, stun the first player »), pas le mot-clé lui-même : le moteur lit `Peril` nativement dans `desc`, aucun module n'est nécessaire pour lui.

**Pièges connus** : Peril isole complètement le joueur qui résout la carte, y compris de la consultation tactique (le joueur ne peut pas demander l'avis des autres). Si une future carte cumule Peril avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Peril lui-même.

**Variantes maison** : aucune recensée pour l'instant.

---

<a id="incite"></a>

## Incite

**Texte imprimé / définition** : « Incite X. » Quand une carte Rencontre avec ce mot-clé est révélée, placez X points de menace sur le complot principal. (X est la valeur indiquée à côté du mot-clé Incite.)

**Mécanisme moteur** : clé `desc.Incite` sur la carte, lue nativement par le moteur. `HasIncite` / `CanIncite` (`src/game/card/face/attribute/can_incite.py`) enregistre l'attribut `Incite` -> `printed_incite`, restaure la valeur à chaque `OnResetKeywords` via `GainIncite`. Quand la carte est révélée, `ResolveIncite()` place le nombre de menaces spécifié sur le complot principal via `Worlds.FindMainScheme()` et `PlaceThreatInternal()`. La classe `Incite(GameRule)` dans `src/game/effect/rule.py` sert de justification. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `04056` : Hydra Regular (`desc` contient `"Incite": "1"`), lu directement depuis `desc`, aucun script requis. Aucun fichier `04056.py` trouvé dans `src/cards/pack` : toutes les capacités imprimées de cette carte sont couvertes par les compteurs `desc` automatiques du moteur, sans script dédié.

**Pièges connus** : Incite place la menace sur le **complot principal** uniquement, jamais sur les complots secondaires. Si le complot principal n'existe pas, l'effet ne s'applique pas. Si une future carte cumule Incite avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Incite lui-même.

**Variantes maison** : aucune recensée pour l'instant.

---

<a id="patrol"></a>

## Patrol

**Texte imprimé / définition** : « Patrol. *(While this minion is engaged with
you, you cannot thwart the main scheme.)* » Tant qu'un sbire Patrol est engagé
avec un joueur, CE joueur ne peut pas contrecarrer le complot principal. C'est
un compteur (`Patrol 1`, `Patrol 2`, ...), réinitialisé à sa valeur imprimée à
chaque reset des mots-clés.

**Mécanisme moteur** : clé `desc.Patrol` sur la carte (réservée aux sbires,
`GainPatrol` pose un `assert Minion.IsType(self)`), lue nativement par le
moteur. `HasPatrol` (`src/game/card/face/attribute/has_patrol.py`) enregistre
l'attribut `Patrol` -> `printed_patrol` et restaure la valeur à chaque
`OnResetKeywords` via `GainPatrol`, qui appelle
`ClearGuardPatrolEffectTargets` / `SetGuardPatrolEffectedBy`
(`src/game/card/face/card_type/minion.py`) : ce dernier marque les COMPLOTS
PRINCIPAUX de la zone de jeu comme « affectés par » ce sbire, ce qui est
l'indication visible côté UI. L'interdiction elle-même est appliquée par
`MainScheme.CanBeThwartBy()`
(`src/game/card/face/card_type/scheme_main.py`) : si la carte visée est bien le
complot principal et que `MainScheme.GetPatrolFaces(effect)` n'est pas vide, la
méthode renvoie `False`, sauf si l'effet ignore le mot-clé
(`effect.IsIgnoreKeyword('Patrol', effect)`) ou si l'initiateur n'est pas un
joueur (`effect.IsPlayerInitiator()`). **Aucun script requis** pour ce mot-clé :
c'est une des « bases automatiques » du guide.

**Carte exemple** : `16119` : Badoon Lieutenant (`desc` contient `"Patrol":
"1"`), lu directement depuis `desc`, aucun script requis. Le script `16119.py`
existe et code la capacité de boost imprimée (« If this activation is a scheme,
this card gets +2 boost icons for this activation »), pas le mot-clé lui-même :
le moteur lit `Patrol` nativement dans `desc`, aucun module n'est nécessaire
pour lui.

**Pièges connus** :
- Patrol n'a **rien à voir avec les règles d'engagement**. Il ne rend pas le
  sbire engageable par n'importe quel joueur, il interdit un thwart.
- Seul le **complot principal** est bloqué : les complots annexes restent
  contrecarrables, et le sbire lui-même reste attaquable, ce qui est la façon
  normale de lever le blocage.
- La restriction est **par joueur** : un sbire Patrol engagé avec un autre
  joueur ne vous empêche pas de contrecarrer.
- Un effet dont l'initiateur n'est pas un joueur n'est pas bloqué, et certains
  effets contournent le blocage via `IsIgnoreKeyword('Patrol', ...)`.
- Patrol ne s'applique qu'aux sbires, jamais aux autres types de cartes.
- Patrol partage avec Guard la plomberie `SetGuardPatrolEffectedBy`, mais les
  deux ne bloquent pas la même chose (complot principal pour Patrol, vilain
  pour Guard) ; ne pas confondre les deux fiches.
- Si une future carte cumule Patrol avec une capacité imprimée distincte,
  vérifier via `find` si un script existe : le script devra porter uniquement
  cette capacité annexe, jamais le mot-clé Patrol lui-même.

**Variantes maison** : aucune recensée pour l'instant.

---

<a id="hinder"></a>

## Hinder

**Texte imprimé / définition** : « Hinder X. » Quand une carte Rencontre avec ce mot-clé entre en jeu, placez X points de menace sur cette carte. (X est la valeur indiquée à côté du mot-clé Hinder.)

**Mécanisme moteur** : clé `desc.Hinder` sur la carte, lue nativement par le moteur. `HasHinder` / `CanHinder` (`src/game/card/face/attribute/can_hinder.py`) enregistre l'attribut `Hinder` -> `printed_hinder`, restaure la valeur à chaque `OnResetKeywords` via `GainHinder`. Quand la carte entre en jeu (`OnWouldEnterPlay`) ou après un retournement (`OnAfterFlip`), `ResolveHinder()` place le nombre de menaces spécifié sur la carte elle-même via `PlaceTokensInternal()`. La classe `ResetKeyword(...)` dans `src/game/effect/rule.py` sert de justification. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `16066` : Blockade (`desc` contient `"Hinder": "2*"`), lu directement depuis `desc`, aucun script requis. Le script `16066.py` existe et code une capacité annexe d'exhaustion pour retirer de la menace (« Exhaust the Milano to remove 3 threat from this scheme »), pas le mot-clé lui-même : le moteur lit `Hinder` nativement dans `desc`, aucun module n'est nécessaire pour lui.

**Pièges connus** : Hinder place la menace **sur la carte elle-même**, jamais sur le complot principal ou les autres cartes. Le `2*` en `desc` indique une menace **par joueur**. Si une future carte cumule Hinder avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Hinder lui-même.

**Variantes maison** : aucune recensée pour l'instant.

---

<a id="vulnerable"></a>

## Vulnerable

**Texte imprimé / définition** : « Vulnerable. » Un personnage avec ce mot-clé est défaussé s'il est ou devient étourdi ou confus. Le compteur `Vulnerable` (`1`, `2`, ...) fixe le nombre de chargés Vulnerable disponibles.

**Mécanisme moteur** : clé `desc.Vulnerable` sur la carte, lue nativement par le moteur. `HasVulnerable` (`src/game/card/face/attribute/has_vulnerable.py`) enregistre l'attribut `Vulnerable` -> `printed_vulnerable`, restaure la valeur à chaque `OnResetKeywords` via `GainVulnerable`. Quand le personnage reçoit un statut Stun ou Confuse, le moteur vérifie `IsVulnerable()` et le défausse si le mot-clé est actif. La classe `Vulnerable(GameRule)` dans `src/game/effect/rule.py` sert de justification. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `50083` : A.I.M. Scientist (`desc` contient `"Vulnerable": "1"`), lu directement depuis `desc`, aucun script requis. Le script `50083.py` existe et code une restriction d'attaque (« While the engaged player is engaged with another minion, A.I.M. Scientist cannot be attacked »), pas le mot-clé lui-même : le moteur lit `Vulnerable` nativement dans `desc`, aucun module n'est nécessaire pour lui.

**Pièges connus** : Vulnerable ne s'applique qu'au statuts Stun et Confuse, jamais aux autres formes de dégâts ou d'effets. Un personnage Vulnerable n'est pas défaussé par une simple menace ou un dégât normal, seulement s'il est ou devient Stun/Confus. Si une future carte cumule Vulnerable avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Vulnerable lui-même.

**Variantes maison** : aucune recensée pour l'instant.

---

<a id="teamup"></a>

## TeamUp

**Texte imprimé / définition** : « Team-Up (Héros A and Héros B). » Cette carte suppose que les deux héros nommés ont des identités héros en jeu **simultanément**. Le mot-clé n'offre généralement pas une capacité distincte, il s'agit plutôt d'une **restriction d'usage** : la carte ne fonctionne que si les deux identités héros sont présentes.

**Mécanisme moteur** : clé `desc.TeamUp` sur la carte (ou une condition portée par le script), lue nativement par le moteur. La condition de présence est vérifiée quand on tente de jouer ou déclencher la carte, via la cible `SetTarget("TeamUp")`.

> ⚠️ **CORRIGÉ le 01/09/2026.** Cette fiche affirmait que « la clé `desc` suppose deux **identités héros** en jeu, pas seulement des alliés » et qu'un script était donc obligatoire dès qu'un des noms désigne un allié. **C'est faux.** `HasTeamUp.GetTeamUpUnits()`
> (`src/game/card/face/attribute/has_teamup.py:21`) balaie
> `Worlds.GetOnFieldFriendlyCharacters()`, qui rend
> `[player.GetIdentity()] + player.allies.Get()` (`worlds.py:289`) : les
> **ALLIÉS COMPTENT**. Le commentaire du moteur le dit d'ailleurs en toutes
> lettres, « both of the named characters (identity or ally) are in play ».
> La clé `desc.TeamUp` suffit donc, même quand un des deux noms est un allié.
> Vérifié en écrivant `al023` Little Rascals (Alligator Loki + Honey Badger,
> qui n'existe QUE comme allié : 43003 et wx003).

**Carte exemple** : `jj022` : Power Couple (`desc` ne contient pas TeamUp, la condition est portée par le `.py` correspondant). Ce script gère la condition `couple_present()` qui vérifie que Jessica Jones est l'identité actuelle et que Luke Cage (son allié signature) est en jeu. Un fichier `jj022.py` existe dans `src/cards/pack` : ce script gère la capacité complète avec sa condition de présence.

**Pièges connus** : le vrai piège n'est pas l'allié, c'est le **DECKBUILDING**. Un allié de classe `Hero` appartient à un seul héros : `43003` Honey Badger est une carte signature de X-23, donc un deck d'Alligator Loki ne peut PAS l'inclure. `al023` Little Rascals reste ainsi injouable en solo et ne s'ouvre qu'en multijoueur, aux côtés d'un joueur X-23 ou Wolverine/X-23 qui met son allié en jeu. C'est le fonctionnement voulu d'un Team-Up, pas un défaut.

`jj022` Power Couple porte sa condition en script pour une autre raison : sa carte n'imprime pas la clé `desc.TeamUp` (voir `docs/reference/GUIDE-CREATION-CONTENU.md` section 9, entrée `jessica_jones`).

**Variantes maison** : aucune recensée pour l'instant.

**Note historique** : Le brief du plan mentionnait la card_id `73022` pour Power Couple, mais cet identifiant est périmé (ancien schéma de numérotation). La carte réelle utilise l'identifiant `jj022` du pack jessica_jones et correspond exactement à la description du guide (section 9).


### Pièges vus au portage de Hellcat (11/09/2026)

- **Le chargeur EXIGE `.SetTarget("TeamUp")`** sur chaque capacité d'un
  événement à `desc.TeamUp` (`cards/database.py:223`, assert en debug) : les
  deux personnages nommés deviennent les cibles. Sans lui la partie meurt au
  setup (« AssertionError: origin_card_id='hc020' »). Modèle 14018 Order and
  Chaos ; hc020 Green Hell, hc021 Hell-Iron.
- **« Team-Up (any 2 of A, B, C, D) »** (hc022 Divas) n'est pas exprimable
  par `desc.TeamUp` (deux groupes « A;B », les DEUX exigés). On omet la clé
  et on code la condition à la main (`conditions=` sur l'action : au moins
  deux des personnages nommés en jeu côté joueur). Le deckbuilder n'applique
  alors aucune restriction Team-Up à cette carte : écart noté.

---

<a id="alliance"></a>

## Alliance

**Texte imprimé / définition** : « Alliance. *(The players can pay this card's
costs as a group.)* » Les joueurs peuvent financer le coût de la carte
collectivement, chacun depuis sa propre main. Le mot-clé ne fait que cela : il
ouvre le paiement, il ne dit rien de l'effet, qui reste celui du texte imprimé
en dessous.

**Mécanisme moteur** : clé `desc.Alliance` sur la carte, lue nativement par le
moteur, exactement comme Toughness, Guard, Patrol ou Retaliate. `HasAlliance`
(`src/game/card/face/attribute/has_alliance.py`) enregistre l'attribut
`Alliance` -> `alliance` en **booléen** ; il est mêlé au type `Event`
(`src/game/card/face/card_type/event.py` : `class Event(HasTeamUp, HasAlliance,
ClassCard, FinalType)`), donc réservé aux événements. Le drapeau est consulté à
deux endroits :

- `src/game/ability/factory/resources.py` (deux occurrences, dans les contrôles
  de paiement) : `if Event.IsType(message.paying_for_effect.this): if
  message.paying_for_effect.this.alliance: return True` ;
- `src/game/event/manager.py` : sur un `Message.WhenPlayerPayingResources`, le
  joueur à contrôler devient `message.to_player` quand l'événement payé porte
  `alliance`.

**Aucun script requis** pour le mot-clé lui-même : c'est une des « bases
automatiques » du guide.

**Carte exemple** : `25036` : Cosmic Alliance, pack `valk` (`desc` contient
`"Alliance": "1"`), lu directement depuis `desc`. Un fichier `25036.py` existe
bien, mais il ne code que la **Hero Action** imprimée (« Choose an AVENGER
character and a GUARDIAN character → ready each of those characters », via
`AbilityFactory.WhenInYourPlayTurn` + `Faces.ReadyAll`), jamais le mot-clé.
Même schéma pour `26035` (Joining Forces, pack `vision`) et `40053` (Team
Investigation, pack `next_evol`, dont le `.py` ne porte que le
`RemoveThreatFromSchemes`).

Le catalogue compte **16 cartes** avec `desc.Alliance` (23032, 23034, 25033,
25036, 26035, 40053, 42031, 44046, 47028, 47029, 48031, 48032, 53019, dt061,
dt115, wd136). Seules quatre d'entre elles impriment le rappel entre
parenthèses (`25036`, `26035`, `40053`, `42031`) ; sur les autres, « Alliance. »
est écrit seul, sans rappel, comme le note le commentaire en tête de
`dt061.py`. Le comportement moteur est identique dans les deux cas.

**Pièges connus** :
- Alliance ne s'applique qu'au **financement des coûts**, jamais aux autres
  mécaniques (dégâts, menace, etc.). L'autre joueur peut contribuer à payer,
  mais le propriétaire de la carte reste maître de l'effet.
- Le drapeau est **booléen et réservé aux événements** (`Event` hérite de
  `HasAlliance`). Le poser sur un autre type de carte n'aurait aucun effet.
- **Ne pas confondre avec Coordinated Effort (`58032`, pack `wonder_man`)** :
  cette carte ne porte PAS le mot-clé Alliance imprimé, et son `desc` n'a pas
  de clé `Alliance`. Son texte est « Attach to an encounter card in play. Max 1
  per encounter card. While paying costs on attached card, any player may help
  pay those costs. » C'est un mécanisme distinct, proche dans l'esprit
  (« laisser un autre joueur aider à payer ») mais géré par le crochet
  `CheckAnyPlayerMayHelpPay()` de
  `src/game/ability/factory/resources.py`, un **CORRECTIF maison** (voir §9 du
  guide) qui teste la présence d'un attachement nommé « Coordinated Effort ».
  Ce crochet est appelé en `or` juste après le test natif `.alliance`, ce qui
  explique la ressemblance de comportement sans qu'il s'agisse du même
  mot-clé. Le script `58032.py` ne code d'ailleurs que la restriction
  d'attachement (`CanPlayThisUpgradeCard(CardFinder(card_type=EncounterCard))`).
- Si une future carte cumule Alliance avec une capacité imprimée distincte
  (c'est le cas des trois cartes ci-dessus), vérifier via `find` si un script
  existe : le script devra porter uniquement cette capacité annexe, jamais le
  mot-clé Alliance lui-même.

**Variantes maison** : **Forces Combined** (`cd003`, pack `cloak_dagger`) est le
second usager du crochet `CheckAnyPlayerMayHelpPay`, et pas du mot-clé Alliance
(son `desc` ne contient que `Class` et `Permanent`). Son texte imprimé est
« Interrupt: When you would spend resources on a card or ability, exhaust
Forces Combined → you may spend resources from both of your hands for that card
or ability. » Le crochet parcourt les cartes contrôlées et renvoie vrai dès
qu'une carte nommée « Forces Combined » est en jeu et **prête** ; l'inclinaison
elle-même est portée par la capacité de `cd003.py`, pas par le contrôle. C'est
un écart documenté au §9 du guide, cohérent avec la mécanique des deux
identités liées Cloak & Dagger (`linked_identity`).

**Note historique** : le brief du plan mentionnait la card_id `70003` pour
Forces Combined, mais cet identifiant est périmé (ancien schéma de
numérotation). La carte réelle utilise l'identifiant `cd003` du pack
`cloak_dagger`.

---

<a id="temporary"></a>

## Temporary

**Texte imprimé / définition** : « Temporary. *(Discard this card at the end
of the round.)* » Une carte avec ce mot-clé est défaussée du jeu à la fin du
round.

**Mécanisme moteur** : clé `desc.Temporary` sur la carte, lue nativement par
le moteur. `HasTemporary` (`src/game/card/face/attribute/has_temporary.py`)
enregistre l'attribut `Temporary` -> `printed_temporary` et restaure la valeur
à chaque `OnResetKeywords` via `GainTemporary`. La défausse de fin de round
est faite par `ProcessTemporary()`
(`src/game/world/world_action.py`) : `Worlds.FindCardsOnField(by_effect,
is_temporary=True)` puis `Faces.DiscardAll(...)`. Le filtre `is_temporary`
vit dans `CardFinder` (`src/game/card/card_finder/checker.py`). **Aucun
script requis** pour ce mot-clé : c'est une des « bases automatiques » du
guide. ⚠ Ne pas se fier à `ResolvedTemporaryDiscard` dans
`has_temporary.py` : ce chemin-là est commenté, le vrai mécanisme est
`ProcessTemporary`.

**Carte exemple** : `59016` : Lion of Olympus (`desc` contient
`"Temporary": "1"`), lu directement depuis `desc`, aucun script requis pour le
mot-clé. `33005`-`33007` (Cyclops) et `60052` (Daredevil) pareil.

**Pièges connus** :
- La défausse a lieu à la FIN DU ROUND, pas à la fin du tour du joueur.
  `rg008` (* Red Guardian's Shield) imprime en plus un retour en main à la fin
  du TOUR : c'est une capacité distincte, scriptée, qui court-circuite en
  pratique la défausse de fin de round.
- Une carte Temporary attachée à un ennemi part avec la fin du round même si
  l'ennemi survit (cf. `33005` Exploit Weakness).

**Variantes maison** : `ho012` (« That Had to Hurt », pack `harry_osborn`)
cumule Temporary avec « Hero form only », « Max 1 per enemy » et une Response :
seul le surplus est scripté, jamais le mot-clé.

---

<a id="piercing"></a>

## Piercing

**Texte imprimé / définition** : « Piercing. *(This attack discards a tough
status card instead of being blocked by it.)* » Une attaque perçante défausse
les cartes de statut Robustesse (tough) de la cible au lieu d'être absorbée
par elles.

**Mécanisme moteur** : propriété booléenne `piercing` de la dataclass des
propriétés d'attaque (`src/game/card/face/attribute/can_attack.py`, commentée
« discard tough » ; le pendant `lost_piercing` sert aux retraits). Deux
chemins pour l'accorder :
- statiquement, via `piercing=True` des fabriques d'attaque
  (`src/game/ability/factory/do_attack.py`, ex. `ab008` du pack `albert`) ;
- dynamiquement via `message.GainPiercing(effect)` sur le message d'attaque
  (`src/game/message/sender/sender_damage.py`, `sender.py`) — chemin des
  textes « this attack gains piercing ».
Les conditions « if this attack has piercing » se testent via
`with_piercing` (`src/game/ability/factory/damage.py`,
`WhenRecalculateAttackDamage`).

**Carte exemple** : `ab008` (pack `albert`) : attaque déclarée avec
`piercing=True` dans la fabrique.

**Pièges connus** :
- Piercing ne retire la Robustesse que dans le cadre d'une ATTAQUE. Un effet
  de dégâts directs hors attaque reste bloqué par tough.
- Un événement qui « gains piercing » selon une condition doit brancher la
  condition sur le paiement ou l'état AU MOMENT de l'attaque, pas à celui du
  jeu de la carte (même piège que « if this attack has ranged or piercing »,
  listé dans PROCESSUS-CARTE.md comme non rendable fidèlement sur certains
  événements).

**Variantes maison** : `ho016` (* Bullseye, pack `harry_osborn`) : « [star]
Bullseye's attack gains piercing and overkill » — capacité étoile (Expert)
posée par `GainPiercing`/`GainOverKill` sur l'attaque en cours.

---

<a id="overkill"></a>

## Overkill

**Texte imprimé / définition** : « Overkill. *(Excess damage from this attack
is dealt to the villain / to the enemy's side.)* » Les dégâts excédentaires
d'une attaque qui abat sa cible sont reportés : sur le vilain si c'est un
joueur qui attaque un sbire, sur l'identité du joueur si c'est un ennemi qui
abat un allié.

**Mécanisme moteur** : propriété booléenne `overkill` de la dataclass des
propriétés d'attaque (`src/game/card/face/attribute/can_attack.py`). Elle se
donne de deux façons :
- statiquement, via les paramètres `overkill=True` des fabriques d'attaque
  (`AbilityFactory.DoAttack` et parents, `src/game/ability/factory/do_attack.py`) ;
- dynamiquement, en cours d'attaque, via `message.GainOverKill(effect)` sur le
  message d'attaque (`src/game/message/sender/sender_damage.py` et
  `sender.py`) — c'est le chemin des textes « this attack gains overkill ».
Le report des dégâts est calculé dans la résolution des dégâts d'attaque
(`include_overkill` dans `src/game/ability/factory/damage.py`).

**Carte exemple** : `an013` (* Hel-Wolf) : « [star] Boost: This attack gains
overkill » rendu par `attaque.GainOverKill(effect)` dans le handler
`WhenCardBecomeBoost`, sur le modèle de `01099` (attaché à Rhino). Côté
joueur : `01053` Relentless Assault (« this attack gains overkill » selon le
paiement).

**Pièges connus** :
- Overkill ne s'applique qu'aux dégâts D'ATTAQUE : un effet « deal X damage »
  hors attaque ne reporte jamais rien.
- Sur un texte de boost, l'attaque visée est `message.would_atk_message` du
  message `WhenCardBecomeBoost` : la récupérer avec `getattr(..., None)` car
  la carte peut être révélée hors attaque (plan du vilain).

**Variantes maison** : `ho016` (* Bullseye, pack `harry_osborn`) : « [star]
Bullseye's attack gains piercing and overkill » — capacité étoile (Expert),
pas un boost.

---

<a id="ranged"></a>

## Ranged

**Texte imprimé / définition** : « Ranged. *(This attack ignores retaliate.)* »
Une attaque à distance ignore la Riposte du défenseur. Le mot-clé se porte sur
l'ATTAQUE, jamais sur le personnage : un personnage « gains ranged » veut dire
« ses attaques gagnent ranged ».

**Mécanisme moteur** : propriété booléenne `ranged` de la dataclass
`AttackProperty` (`src/game/card/face/attribute/can_attack.py`, commentée
« ignore retaliate »). Elle n'est lue qu'à un seul endroit :
`src/game/card/face/attribute/can_retaliate.py` court-circuite `ResolveRetaliate`
si `atk_message.IsRanged()`. Trois chemins pour l'accorder :
- **permanent, sur les attaques d'un personnage** :
  `AbilityFactory.UnitAttackGainKeyword("This", ranged=True)`
  (`src/game/ability/factory/do_attack.py`) ;
- **ponctuel, sur une attaque que l'on déclenche soi-même** :
  `property=AttackProperty(ranged=True)` passé à `DealDamage` ;
- **ponctuel, sur l'attaque en cours** : `message.GainRanged(effect)`
  (`src/game/message/sender/sender_damage.py`).

⚠ **Aucune clé `desc`.** Contrairement à Guard, Patrol ou Retaliate, `Ranged`
n'existe pas dans la liste blanche `CardFace.KEY` : écrire `"Ranged": "1"` dans
`data/cards.json` fait planter le chargement de la carte. Ranged est toujours
scripté.

**Carte exemple** : `50107b` (* M.O.D.O.K., pack `aos`) :
`UnitAttackGainKeyword("This", overkill=True, ranged=True)`, permanent.
Ponctuel : `ag003` (pack `agent_13`), `AttackProperty(ranged=True)`.

**Pièges connus** :
- **Le sens s'inverse selon le message visé.** `ag005` (pack `agent_13`)
  documente le cas : appeler `message.GainRanged(effect)` sur le message de
  l'ATTAQUE ENNEMIE donne ranged à l'ennemi, l'exact contraire du texte
  « votre attaque gagne ranged ». Pour une attaque que la carte déclenche,
  passer `AttackProperty(ranged=True)` à `DealDamage`.
- Ranged n'annule que la Riposte. Il ne traverse ni la Robustesse (c'est
  [[piercing]]) ni le blocage d'un allié.
- Un `[star]` du genre « X's attacks gain ranged » est un effet PERMANENT de
  l'attachement ou du personnage : `UnitAttackGainKeyword`, pas une réponse.

**Variantes maison** : `gb014` (Vicious Tendrils, pack `gorr`) : attachement
posé sur le vilain qui donne à la fois `retaliate 1` (base automatique, sur le
porteur) et, par capacité étoilée, `ranged` aux attaques de Gorr — les deux
mots-clés se contredisent pour l'adversaire, ce qui est l'intention de la carte.

---

<a id="boost"></a>

## Boost (icônes) et Boost ★ (effet)

**Texte imprimé / définition** : deux choses distinctes, que la même fiche
couvre parce qu'elles se lisent au même endroit sur la carte.
1. Les **icônes de boost**, en bas à droite d'une carte de rencontre : chaque
   icône ajoute 1 à l'attaque ou à la manigance du vilain quand la carte est
   retournée comme carte de boost.
2. L'**effet Boost ★**, une ligne « [star] **Boost** : … » sous un trait
   horizontal, qui se résout quand la carte est retournée comme carte de boost.

**Mécanisme moteur** :
- **Icônes = base automatique.** Clé `desc.Boost`, en CHAÎNE :
  `"Boost": "2"`. Enregistrée par
  `src/game/card/face/attribute/has_boost_icon.py` (`RegisterAttribute("Boost",
  "printed_boost")`), comptée à la révélation par `CountBoostIconsInternal`.
  Portée par `EncounterNonVillainCard` (traîtrise, complot annexe, attachement,
  environnement) et par `Enemy` (vilain, sbire). `"Boost": "0"` est légitime.
- **Effet ★ = script obligatoire.** Aucune clé `desc`. Deux endroits :
  - dans `data/cards.json`, uniquement le TEXTE imprimé, dans le champ racine
    `text`, séparé du reste par `\n<hr />\n` puis
    `[star] <b>Boost</b>: <effet>` ;
  - dans le module, une capacité
    `AbilityFactory.WhenCardBecomeBoost("This", operation)`
    (`src/game/ability/factory/boost.py`, type `AbilityType.Boost`).
- Le moteur ne lit PAS le texte : `has_boost_icon.py` calcule `boost_star` en
  cherchant une capacité de type `AbilityType.Boost`. Écrire la ligne
  « [star] Boost » sans écrire l'`Ability` ne crée aucune étoile.

**Carte exemple** : `01099` (Charge, pack `core`) pour les icônes seules
(`{"Boost": "2", "ATK+": "3"}`, aucun script). `an013` (* Hel-Wolf, pack
`angela`) pour le gabarit complet : `desc.Boost = "2"`, une capacité étoilée
permanente ET un `WhenCardBecomeBoost`.

**Pièges connus** :
- L'attaque en cours, pendant un effet de boost, se lit
  `message.would_atk_message` — à récupérer avec `getattr(..., None)`, elle
  n'existe pas si le boost sert une manigance.
- Ne pas confondre le `[star]` d'un effet Boost (sous le trait) et le `[star]`
  d'une capacité permanente (au-dessus) : le second est un
  `AbilityType.NonKeywordStar`, voir [[special]].
- Les icônes de boost d'un SBIRE comptent quand ce sbire est retourné comme
  carte de boost, pas quand il est en jeu.

**Variantes maison** : `gb010` (Necro-Raven, pack `gorr`) : le ★ Boost met le
sbire en jeu engagé avec le joueur au lieu de l'envoyer à la défausse, et se
cumule avec la Réponse Obligatoire d'entrée en jeu de la carte.

---

<a id="special"></a>

## Special et l'étoile ★ d'une capacité permanente

**Texte imprimé / définition** : deux notions que le mot « Special » confond.
1. Le **`[star]` en tête d'une ligne de texte** d'une carte de rencontre : une
   capacité PERMANENTE, toujours active tant que la carte est en jeu (par
   exemple « ★ Black Berserker gets +X hit points »).
2. La **capacité « Special » nommée**, rare, qu'une AUTRE carte vient résoudre
   explicitement.

**Mécanisme moteur** :
- **Cas 1, le ★ permanent** : type `AbilityType.NonKeywordStar`
  (`src/game/ability/ability_type.py`, valeur interne `"ConstantStar"`,
  priorité `TimingPriority.Constant`). Rien dans `desc` : seule la ligne
  `[star] <effet>` dans le champ racine `text` de `data/cards.json`, plus la
  capacité dans le module. Le pendant sans étoile est `AbilityType.NonKeyword`.
- **Cas 2, la capacité nommée** : `AbilityFactory.WhenResolveSpecialAbility`
  (`src/game/ability/factory/resolve.py`, type `AbilityType.Special`). Le
  moteur la cherche par `self.effect.Find(type=AbilityType.Special)`
  (`src/game/card/face/card_face.py`) quand une carte demande de résoudre une
  capacité spéciale.

**Carte exemple** : cas 1 : `01132` (* Melter, pack `core`),
`WhenUnitAttackYou(AbilityType.NonKeywordStar, "This", ...)` ; copie commentée
dans `an013` (pack `angela`). Cas 2 : `ab007` (pack `albert`).

**Pièges connus** :
- **Convention du projet** : une capacité `[star]` SANS la mention « In expert
  mode » est codée TOUJOURS active (cf. `RECETTES-MOTEUR.md`). Réserver
  `expert_mode_only=True` aux textes qui le disent.
- Le ★ d'un effet **Boost** (sous le trait horizontal, « [star] Boost: … ») est
  autre chose : c'est un `AbilityType.Boost`, voir [[boost]].
- `NonKeywordStar` sur un effet continu ne se rafraîchit pas tout seul quand la
  quantité qu'il lit change : un « +X PV où X = nombre d'attachements » doit
  passer par une fabrique qui recalcule, ou déclarer son événement de
  rafraîchissement.

**Résoudre un Special HORS de la table** (pack `zeus`, 11/09/2026) : Hera
résout le Special d'une carte EN MAIN, *Skyfather's Tempest* celui d'un
événement PENDANT son paiement. `ResolveSpecialAbility` ne trouve alors aucun
effet enregistré. Recette dans `RECETTES-MOTEUR.md` §4 : déclarer le Special
avec `.NoOutOfPlayLimit()`, et l'enregistrer en temporaire juste avant de le
résoudre (`ResoudreLeSpecialDe`, `cards/pack/zeus/zeus/__init__.py`). Lire
« a printed Special » avec `face.ability.Find(type=AbilityType.Special)` (les
capacités DÉCLARÉES), jamais `face.effect.Find` (les effets enregistrés, qui
dépendent de la zone).

**Variantes maison** : `gb009` (Black Berserker, pack `gorr`) : `[star]` qui
donne des PV proportionnels au nombre d'attachements NECROVERSE en jeu, plafonné
à 4 — la valeur bouge en cours de partie, l'étoile doit donc être recalculée et
non figée à l'entrée en jeu.

---

<a id="teamwork"></a>

## Teamwork (TRAIT)

**Texte imprimé / définition** : `Teamwork ([[TRAIT]])`. Après qu'un sbire
portant Teamwork entre en jeu et s'engage avec un joueur, s'il y a **au moins
un AUTRE sbire en jeu qui porte le trait cité**, le sbire qui vient d'arriver
**s'active** contre le joueur avec lequel il est engagé (il attaque ou
manigance immédiatement, comme en phase du vilain).

Le mot-clé transforme donc une arrivée de sbire en attaque immédiate dès que
la bande est constituée. Le trait entre parenthèses n'est pas forcément celui
du sbire lui-même, même si dans les 31 cartes officielles qui le portent,
c'est toujours le cas.

**Mécanisme moteur** : **entièrement natif, aucun script à écrire.** Il se
déclare dans `desc` :

```json
"desc": { "HP": "5", "ATK": "3*", "SCH": "1", "Teamwork": "ASGARD" }
```

`src/game/card/face/attribute/can_teamwork.py` fait le reste :
`RegisterAttribute("Teamwork", "printed_teamwork", str)` lit la valeur, puis
`CanTeamwork.OnAfterCardEnterPlay` cherche un autre sbire du terrain qui
porte le trait (`minion.HasTrait(*self.teamwork)`) et déclenche
`minion.DoActivate(minion.GetEngagedPlayer(), Teamwork(minion))`.

**Carte exemple** : `32159` * Fabian Cortez (set Acolytes) : `"Teamwork":
"ACOLYTE"` dans `desc`, et son `.py` ne contient QUE sa capacité
« When Defeated » — pas une ligne pour Teamwork. Voir aussi `38029` Donald
Pierce et `38030` Skullbuster (set Reavers), même montage.

**Pièges connus** :

- ⚠ **Ne jamais l'écrire en script.** C'est la même famille de pièges que
  `Toughness` et `Restricted` : une base lue directement dans `desc`. Un
  module qui la recoderait ferait s'activer le sbire DEUX fois.
- ⚠ **Le trait cité doit exister dans l'énum `TRAITS`**
  (`src/game/card/face/card_face.py`). `CheckPrintedValue` lève un `assert
  IsTrait(self.printed_teamwork)` : un trait maison non déclaré fait tomber
  la carte à la construction, pas en jeu.
- ⚠ **Le déclencheur est l'ENTRÉE EN JEU, pas l'engagement.** Un sbire déjà
  en jeu quand un second arrive ne se réveille pas de lui-même sous la règle
  actuelle : c'est le NOUVEAU venu qui s'active.
- ⚠ **Deux règles cohabitent dans le moteur**, selon `world.rule.v16_teamwork`
  (`src/game/world/world_rule.py:38`, **`False` par défaut**) :
  - règle par défaut (pré-1.6) : **tous** les sbires dont le `teamwork`
    correspond s'activent, pas seulement celui qui arrive ;
  - `v16_teamwork = True` : **seul** le sbire qui vient d'entrer s'active.
  Un test qui compte les dégâts doit donc savoir sous quelle règle il tourne.
- Le sbire qui arrive s'active contre **son** joueur engagé, pas contre le
  premier joueur.

**Variantes maison** : aucune à ce jour. Le pack `lady_sif` (Rainy, set 150)
est le premier contenu maison à l'imprimer, sur `ls015` Skurge —
`Teamwork (ASGARD)` — et il a exigé l'ajout du trait `TEMPTATION` à l'énum
pour ses deux attachements, mais pas d'`ASGARD`, déjà présent.

---

<a id="uses"></a>

## Uses

**Texte imprimé / définition** : « Uses (N <nom> counters). » La carte entre
en jeu avec N pions du type nommé. Quand le **dernier** pion est retiré, la
carte quitte le jeu : c'est la règle du mot-clé, pas un effet de la carte.
Rien n'est imprimé pour cette sortie, et c'est précisément pour ça qu'on
oublie de la vérifier.

Le nom du pion est libre (`doubt`, `emergency`, `pheromone`, `charge`,
`unworthy`, `foe`…) et n'a aucune sémantique : deux cartes qui portent le même
nom de pion ne se parlent pas pour autant.

**Mécanisme moteur** : clé `desc.Uses` valant `"<N>,<nom_du_pion>"`, lue
nativement par `HasUses`
(`src/game/card/face/attribute/has_uses.py`). **Aucun script requis**, ni pour
poser les N pions, ni pour faire sortir la carte. Deux points d'ancrage :

- `OnWhenCardEnterPlay` (ligne 20) pose les N pions à l'entrée en jeu ;
- `RemoveCountersInternal` (ligne 46) surveille chaque retrait : dès que
  `GetAllCounters() <= 0`, la carte part.

⚠ Le nom du pion doit passer `IsCounter()` (`game/element/utility.py`) :
`has_uses.py:15` pose un `assert` sec. Un nom absent de l'énumération fait
tomber la construction de la carte, pas la partie.

Le retrait d'un pion s'écrit soit en effet
(`Faces.RemoveCountersOn([this], 1, '<nom>', effect)`, modèle `53029`), soit
en **coût** (`CostFunc.Counter("This", 1, '<nom>')`, modèle `61033a`).

**Carte exemple** : `61033a` : Suggestion ([energy]) — lu directement depuis
`desc` pour les pions et la sortie de jeu ; le script ne code que la capacité
imprimée :

```python
AbilityFactory.WhenInYourPlayTurn(AbilityType.ForcedAction, suggestion)
.SetCostFunc(CostFunc.Exhaust("This")).SetCostFunc(CostFunc.Counter("This", 1, 'pheromone')),
```

**Pièges connus** :

- **Ne pas coder la sortie de jeu.** Le réflexe est d'ajouter un
  `WhenTheLastCounterIsRemovedFromHere` qui défausse la carte : il ferait
  double emploi avec `RemoveCountersInternal` et défausserait deux fois. Cette
  fabrique ne sert que pour un effet EN PLUS de la sortie (modèle `wd057`, qui
  retourne Curt Connors).
- ⚠ **`GetAllCounters()`, pas le compteur nommé.** La sortie se déclenche
  quand la carte n'a **plus aucun pion, tous types confondus**. Une carte à
  `Uses` sur laquelle un autre effet pose un pion d'un type différent ne part
  donc pas tant que ce pion-là reste. Aucune carte du dépôt n'est dans ce cas
  aujourd'hui, mais le montage est possible et le comportement surprendrait.
- ⚠ **`Victory 0` ne va PAS dans la pile de victoire.** `has_uses.py:54` teste
  `if self.victory:` : `Victory 0` vaut l'entier `0`, donc faux, et la carte
  est **défaussée**. Les règles imprimées, elles, envoient une carte
  « Victory 0 » dans la pile de victoire (pour 0 point). L'écart est sans
  conséquence tant qu'aucune carte ne COMPTE les cartes de la pile de
  victoire — et le commentaire `# Hack` du moteur cite justement `51031`, une
  carte à `Victory 0`, ce qui laisse penser que l'intention était l'inverse.
  Cinq cartes livrées sont concernées : `51031`, `53029`, `59004`, `br012` et
  `tg011`. À rouvrir le jour où une carte lira la pile de victoire.
- **La carte doit être EN JEU** (`self.IsInPlay()`), sinon le retrait de pion
  ne déclenche rien. Retirer un pion d'une carte en défausse est inerte.

**Variantes maison** : aucune. Les packs maison qui emploient `Uses`
(`br012` Unworthy, `sr013` Bad Publicity, `tg011` Trouble in Central Park)
suivent tous la règle officielle sans l'étendre.

---

<a id="setup"></a>

## Setup

**Texte imprimé / définition** : « Setup. » Une carte de rencontre avec ce
mot-clé est mise en jeu pendant la mise en place du scénario (étape
« Set Up »), avant que le deck rencontre soit mélangé, au lieu d'attendre
d'être révélée. Ses capacités « When Revealed » ne jouent pas ; un texte
« Setup: ... » sur la carte décrit ce qu'elle fait à ce moment.

**Mécanisme moteur** : clé `desc.Setup` (`"Setup": "1"`) lue nativement.
`HasSetup` (`src/game/card/face/attribute/has_setup.py`) enregistre
`printed_setup` ; `world.py:552` ramasse toutes les faces des decks avec
`printed_setup > 0` et appelle `ProcessSetup`, qui fait `PutIntoPlay` sous
le contrôle du premier joueur. **Aucun script requis** pour la mise en jeu
elle-même. Le texte « Setup: ... » de la carte, lui, se code avec
`AbilityFactory.AfterGameSetup(op)` : il part au pas « Resolve Character
Setup Abilities », donc APRÈS la mise en place du complot principal et des
œuvres d'Art Museum Heist.

**Carte exemple** : `60112` : Disturbed Psyche (pack `fne`, set Typhoid
Mary), `desc` contient `"Setup": "1"`, et son texte « Setup: Randomly
choose which side of Typhoid Mary is face up » est codé par
`AbilityFactory.AfterGameSetup(mise_en_place)` avec
`Rand.RandomChoice([True, False], effect)` puis `vilain.card.Flip(effect)`.
`60113a` Establish Trust (complot annexe Permanent + Setup) entre en jeu par
le seul `desc`, sans une ligne de script.

**Pièges connus** :
- `AbilityFactory.WhenCardSetup` n'est JAMAIS envoyé à une carte mise en jeu
  par le mot-clé (mesuré le 18/09/2026 : le Setup de Disturbed Psyche restait
  muet). C'est `AfterGameSetup` qu'il faut.
- Sous le harnais (graine 42), `Rand.RandomChoice` est déterministe : la
  partie de test commence toujours sur Bloody Mary (`60110b`). Les cas qui
  veulent l'autre face font `Puzzle.Flip('60110b')`.
- Un vilain que le Setup retourne doit avoir ses DEUX faces déclarées dans le
  scénario (`"villain": ["60110a,60110b"]`), sinon `card.Flip` le met face
  cachée (RECETTES-MOTEUR §7quater).

**Variantes maison** : aucune recensée pour l'instant.

---

<a id="forced-action"></a>

## Forced Action

**Texte imprimé / définition** : « Forced Action: <coût> → <effet>. » Ce
n'est pas un mot-clé au sens des règles mais un TYPE de capacité (comme
Hero Action ou Forced Response) : une action que le joueur DOIT effectuer
pendant sa phase de joueur tant qu'elle est possible ; la phase ne peut pas
se terminer avant. Le joueur choisit seulement le moment.

**Mécanisme moteur** : `AbilityType.ForcedAction` (`ability_type.py:56`,
« the player phase cannot end until all possible forced actions among all
players have been performed »). Se code avec
`AbilityFactory.WhenInYourPlayTurn(AbilityType.ForcedAction, op)` et les
coûts en `SetCostFunc` (`CostFunc.Exhaust("This")`, `CostFunc.Counter(...)`).
Tant que le coût est payable, l'action reste proposée et la fin de phase est
bloquée ; quand il ne l'est plus (carte inclinée, pions épuisés), l'action
disparaît et la phase peut finir.

**Carte exemple** : `ls016` : Hypnotic Suggestion (pack `lady_sif`),
`WhenInYourPlayTurn(AbilityType.ForcedAction, hypnotic_suggestion)
.SetCostFunc(CostFunc.Exhaust("This"))`. Dans `fne`, les trois obligations
de Purple Man (`60105` « Fight. », `60106` « Protect. », `60107` « Serve. »)
passent par `ObligationCommandee` (purple_man/__init__.py) : même
fabrique, avec `CostFunc.Exhaust("This")` ET `CostFunc.Counter("This", 1,
'command')`.

**Pièges connus** :
- Deux `SetCostFunc` s'additionnent : incliner ET retirer un pion, jamais
  l'un des deux (piège `wd005`).
- Sous le harnais, on déclenche par `Puzzle.Action(id, 'ForcedAction')`
  (modèles `ls017`, `tg011`) avec une main sans carte jouable
  (`main_exclusive: ["01088"]`), sinon le pilote joue d'abord ses cartes et
  fausse la mesure (RECETTES-MOTEUR §7ter).
- Une Forced Action sur une carte à `Uses (N ... counters)` s'éteint avec le
  dernier pion : la sortie de la carte est native (voir `uses.md`), ne pas la
  recoder.

**Variantes maison** : aucune recensée pour l'instant.

---

<a id="victory"></a>

## Victory X (dont X négatif)

**Texte imprimé / définition** : « Victory X » (RRG) : quand cette carte est
vaincue (sbire, complot annexe) ou, pour une carte joueur qui le porte, quand
elle quitte le jeu de cette façon, elle est placée dans la **pile de victoire**
au lieu de sa défausse, et compte X points dans le score final. X peut être
**négatif** : la carte va quand même dans la pile de victoire, mais elle
retire des points. Fear No Evil imprime « Victory -1 » sur l'alliée de
campagne * Typhoid Mary / * Bloody Mary (`60210a,60210b`) : la vaincre coûte
un point ET laisse une trace, le livret vérifie « Mary Defeated? » en fin de
partie en regardant la pile de victoire.

**Mécanisme moteur** : base native, lue dans `desc.Victory` (`HasVictory`,
`src/game/card/face/attribute/has_victory.py`). `OnBeDefeated` envoie la face
dans la pile de victoire (`Faces.AddToVictoryDisplay`) dès que
`printed_victory` n'est pas `None` : **le signe ne change rien au déplacement**,
`0` et `-1` y vont comme `2`. Le nombre n'est relu que par le score. Un vilain
ne s'y déplace pas tant qu'un stade suivant porte le même nom. Aucun script
requis pour le mot-clé lui-même.

**Carte exemple** : `60210a` : * Typhoid Mary (alliée de campagne, Victory -1),
lu directement depuis `desc` (`"Victory": "-1"`), aucun script requis pour
l'aller dans la pile de victoire ; c'est `CollectFNE` (`cards/pack/fne/campaign.py`)
qui relit ensuite `card.area.flags.is_victory_display` pour cocher « Mary
Defeated? ». Autre exemple : `60024` * De-escalation (Cops, Victory 0).

**Pièges connus** :
- Écrire `"Victory": "0"` n'est PAS neutre : la carte va dans la pile de
  victoire (c'est voulu pour De-escalation, dont le texte le demande).
- Une carte qui QUITTE le jeu autrement que vaincue (défaussée par un effet,
  retirée du jeu) ne passe pas par `OnBeDefeated` : elle ne va pas dans la
  pile de victoire. Pour Typhoid Mary, « defeated » est donc bien la seule
  voie qui coche « Mary Defeated? ».
- Le harnais lit la pile par `card.area.flags.is_victory_display` (clé
  `victoire` de `pileFondue` côté plateau : « Pile de victoire »).

**Variantes maison** : aucune.

---

<a id="requirement"></a>

## Requirement

**Texte imprimé / définition** : « Requirement ([mental]). *(While paying for
this card, spend the listed resources.)* » Pour jouer la carte, le paiement
doit **comporter** les ressources listées, en plus d'en couvrir le coût. Ce
n'est pas un coût supplémentaire : les ressources listées sont **incluses**
dans le coût, elles en contraignent seulement la couleur.

Exemple : Web Binding (`27006`) coûte 2 avec `Requirement ([mental])`. Il faut
donc payer 2 ressources dont **au moins une** mentale, pas 3.

**Mécanisme moteur** : clé `desc.Requirement`, une chaîne de couleurs au même
format que `RES` (`"B"`, `"R"`, `"BB"`, `"YBR"`…). Lue nativement par
`HasCost.RegisterAttribute("Requirement", parse2)`
(`src/game/card/face/attribute/has_cost.py:24`), puis exposée par
`GetPrintedCostWithRequirement()`. **Aucun script requis** : c'est une des
« bases automatiques » du guide, au même titre que `Toughness` ou `Restricted`.

Le script d'une carte à Requirement ne le mentionne donc jamais. Vérifié sur
`27006.py` (Web Binding), qui ne code que son Hero Interrupt.

**Cartes exemples** (toutes officielles) :

| Carte | `desc.Requirement` | Imprimé |
|---|---|---|
| `27006` Web Binding | `"B"` | Requirement ([mental]) |
| `28013` No Quarter | `"R"` | Requirement ([physical]) |
| `29020` R&D Facility | `"BB"` | Requirement ([mental][mental]) |
| `27049` * Spider-Man | `"YBR"` | Requirement ([energy][mental][physical]) |

**Pièges connus** :

- **Ce n'est pas un coût en plus.** Lire « Requirement ([mental]) » sur une
  carte à 2 comme « 2 + 1 mental » est faux : c'est « 2, dont au moins 1
  mental ».
- **Ne pas le confondre avec « If you paid for this card using a [X]
  resource »**, qui est une CONDITION D'EFFET, pas une condition de jeu : la
  carte se joue dans tous les cas, seul le bonus dépend de la couleur payée.
  Le pack `doctor_doom` porte les deux tournures, parfois à une carte d'écart
  (`dd003` Doombot a un Requirement ; `dd004` « This World Is Mine! » a la
  condition d'effet).
- La chaîne se répète pour exiger plusieurs fois la même couleur (`"BB"` = deux
  mentales), exactement comme `RES`.

**Variantes maison** : aucune. Le pack fan-made `doctor_doom` (`dd003`
Doombot, `Requirement ([mental])`) l'emploie tel quel.

---

# Partie 2 : mots-clés maison

<a id="eclair"></a>

## Éclair (ressource maison, `L`)

**Texte imprimé / définition** : le pack fan-made Zeus (Mozilla) imprime sur
ses quatre Thunder Strike une icône de ressource qui n'existe pas dans le jeu
officiel, un éclair droit. Ce n'est PAS l'énergie : Zeus exige de payer un
même événement « avec une énergie ET un éclair » (*Skyfather's Tempest*).
Vocabulaire fixé le 11/09/2026 : **énergie** = la ressource officielle jaune ;
**éclair** = celle-ci.

**Mécanisme moteur** : cinquième couleur à part entière, lettre `L`, ajoutée
le 11/09/2026 (`src/game/element/rbyg.py`, champ `l`). Elle se déclare comme
les autres : `"RES": "L"` dans `desc`, `Cost("YL")` pour un coût typé, jeton
`[[lightning]]` dans les narrations, `GetColor("L")` pour la compter.
- Un joker (`G`) vaut aussi un éclair (défaut `convert_green_res=True`).
- Un éclair paie tout coût générique, et ne paie PAS un coût typé d'une autre
  couleur : « Requirement (énergie) » le refuse.
- Plateau : `ui-app/src/board/icones-ressources.tsx`, entrée `lightning`,
  rendue en SVG bleu électrique. Deckbuilder : classe `icon-lightning`.
- Gate : `ui-app/src/board/noms-ressources.test.ts` relit la table du moteur
  et celle du plateau et exige les cinq lettres des deux côtés.
- Test : `tools/test_couleur_eclair.py` (26 cas, sans partie ni port).

**Carte exemple** : aucune livrée à ce jour ; le pack Zeus suivra
`PROCESSUS-HEROS.md`. Le relevé complet est dans
`.planning/todos/2026-09-11-zeus-releve-des-cartes.md`. Spec et plan dans
`docs/superpowers/specs/2026-09-11-cinquieme-couleur-de-ressource-design.md`
et `docs/superpowers/plans/2026-09-11-cinquieme-couleur-de-ressource.md`.

**Pièges connus** :
- **Ne pas lire l'éclair comme une énergie.** La première version du relevé
  Zeus l'a fait sur toutes les cartes ; le set némésis, lui, vise bien
  l'ÉNERGIE officielle, pas l'éclair.
- `DeclareResourceType()` propose désormais `L` à toute carte qui fait nommer
  un type (Psylocke, Iron Lad, Mojo). C'est la règle : un type existe pour
  tout le monde. Passer `l=False` si une carte doit s'en tenir aux quatre
  officiels.
- Les jetons à un crochet `[energy]` des textes français ne sont pas rendus
  en icône aujourd'hui (ils s'affichent tels quels dans l'aperçu) ;
  `[lightning]` suivra le même sort. Hors périmètre de la couleur.

**Variantes maison** : c'est la variante. Aucune autre ressource maison dans
le projet.

---

<a id="seek"></a>

## Seek (mot-clé maison, Rainy)

**Texte imprimé / définition** : « Seek a minion from the encounter deck »,
« seek an event from your deck ».

> ### ✅ DÉFINITION DE L'AUTEUR, TROUVÉE LE 08/09/2026
>
> L'insert du pack **Spider-Man 2099** la donne noir sur blanc :
>
> > **New Keyword: Seek.** The seek keyword is a shorthand term for an ability
> > that **discards cards from the top of a deck until a certain type of card
> > is discarded**. For example, "Seek an event from your deck." is shorthand
> > for "Discard cards from the top of your deck until you discard an event."
>
> ⚠ **Ce n'est PAS une recherche.** La version retenue au dépôt jusqu'à cette
> date — « chercher la carte dans la zone, la prendre, mélanger » — ne
> défaussait rien : elle donnait le même résultat visible (on obtient la
> carte) en cachant tout le coût réel (le deck se vide, la défausse se
> remplit, et les cartes traversées sont perdues pour ce tour). Sur
> Spider-Man 2099 la différence n'est même pas subtile : `sm002` Ghost Rider
> se déclenche « after Ghost Rider is **discarded** by your *Acceleration*
> ability », donc la lecture « recherche » rendrait la carte inerte.
>
> **Arbitrage utilisateur du 08/09/2026 : corriger partout.**

**Mécanisme moteur** : deux primitives natives, une par zone, et elles
existaient déjà — c'est bien la lecture qui était fausse, pas l'outillage.

- Deck du **joueur** : `Player.DiscardDeckUntil(effect, card_type=Event,
  return_other_faces=autres)` (`player_action.py:1028`). Rend la carte
  trouvée, remplit `autres` avec les cartes traversées.
- Deck **rencontre** : `Worlds.DiscardEncounterCardsUntil(effect,
  card_type=Minion, return_other_faces=autres)` (`worlds.py:540`), même
  contrat. Modèles officiels : `01116b`, `01117a`, `45147b`, `ag013`.
- Les deux passent par `Deck.DiscardUntil` (`deck.py:443`), qui **défausse
  aussi la carte trouvée** avant de la rendre. Une carte « mise en jeu »
  ensuite part donc de la **défausse**, pas du deck.
- Le remélange en fin de deck est géré par `DiscardUntil` lui-même
  (`deck.py:483`).

**Carte exemple** : `sm001a` * Spider-Man (Spider-Man 2099), la carte qui
porte la définition de l'auteur dans son propre pack.

**Pièges connus** :

- ⚠ **Sans `include_encounter_discard_pile`, la défausse n'est pas fouillée**
  — et avec la vraie définition, la question ne se pose plus : on ne fouille
  rien, on défausse depuis le dessus.
- ⚠ La carte trouvée arrive dans la **défausse**. La remettre en jeu ou en
  main est une étape SÉPARÉE (`Faces.AddToHand`, `PutIntoPlay`), qu'il faut
  écrire.
- ⚠ Un deck vide rend `None` : toute carte qui « seek » doit prévoir la
  branche sans trouvaille.

**Ne relèvent PAS de ce mot-clé** (vérifié texte en main le 08/09/2026) :

| Carte | Texte imprimé | Pourquoi |
|---|---|---|
| `56007` Hunted | « **search** the encounter deck and discard pile » | carte **officielle**, le mot « seek » n'y figure pas |
| `br011` Hammer Time | « **Search** the encounter deck for a minion » | Rainy écrit « search » ici, pas « seek » |

**Cartes réellement concernées par la correction du 08/09/2026** : `br005`
Star Jump (« Seek a minion from the encounter deck »), `br009` Oathbrother
(« seek an event from your deck »), `ar001a` * Ares (« Seek a minion from the
encounter deck »).

**Variantes maison** : « Find a Beta Ray Bill card » (`br005`, troisième
puce) est un autre verbe, et **celui-là est bien une recherche** : il n'est
pas touché par la correction.

---

<a id="track"></a>

## Track (mot-clé maison, Rainy)

**Texte imprimé / définition** : l'insert du pack **Superior Spider-Man** la
donne, et sans ambiguïté :

> **New Keyword: Track.** The track keyword is a shorthand term meaning
> **"move 1 threat from a scheme to a minion in play."** A minion may have any
> number of threat on them and they do not need to be engaged with you in order
> to be tracked. While there are no innate effects of a minion having threat on
> them, some card effects may interact with threat on a minion. **When a minion
> with threat on it is defeated, all threat on that minion is returned to the
> supply.**

⚠ **C'est un DÉPLACEMENT, pas un retrait.** La menace quitte la manigance et
arrive sur le sbire : elle n'est pas détruite. C'est exactement le piège
`instead` de PROCESSUS-CARTE §5 (leçon The Spot) — coder « retirer 1 menace »
sans rien poser sur le sbire rendrait le pack entier faux, et ferait de
`track` un simple contre gratuit.

**Q/R de l'insert** : « Can I track a minion while I am engaged with a minion
that has the patrol keyword? » → **Non depuis le complot PRINCIPAL** (patrol,
ou une icône crisis en jeu, l'interdisent), **oui depuis un complot annexe**.
Le retrait passe donc par les mêmes règles que n'importe quel retrait de
menace : `RemoveThreatFromSchemes`, sans `ignore_crisis`.

**Mécanisme moteur** : aucune primitive dédiée, deux gestes enchaînés.

- Le retrait : `this.RemoveThreatFromSchemes(cibles, 1, effect)` — et il faut
  lire son RETOUR, car il peut ne rien retirer (manigance vide, patrol, crisis).
  Ne poser sur le sbire que ce qui a réellement été retiré.
- La pose : `Faces.PlaceCountersOn([sbire], n, 'threat', effect)`.
  ⚠ Le compteur `threat` a été **AJOUTÉ à l'énum `COUNTER`** le 08/09/2026
  (`card_face.py`) : la menace posée sur un SBIRE n'a aucune existence native
  dans le moteur, contrairement à celle d'une manigance.
- Le nettoyage à la mort du sbire est **gratuit** : les compteurs disparaissent
  avec la carte. Rien à coder pour la dernière phrase de la définition.

**Carte exemple** : `su010` Facial Recognition Uplink (« After a minion enters
play, track it ») ; `su008` Mechanical Arms (« When you make a basic attack
against a minion, track that minion ») ; `su002` Spiderlings (« track a minion
INSTEAD of removing threat »).

**Pièges connus** :

- ⚠ « **a minion in play** » : n'importe quel sbire, y compris celui d'un autre
  joueur, et **sans obligation d'être engagé** — l'insert le dit. Ne pas
  restreindre le sélecteur aux sbires engagés.
- ⚠ « **from a scheme** » : principal OU annexe, au choix du joueur. Ne pas
  coder « du complot principal ».
- ⚠ Sans sbire en jeu, ou sans menace sur aucune manigance, `track` ne fait
  rien. Toute carte qui l'emploie en COÛT doit donc doubler son `CostFunc`
  d'un `conditions=[...]` (RECETTES §5).
- ⚠ `su015` Goblin Protocol dit « Threat on tracked minions counts towards the
  main scheme's target threat » : c'est le seul endroit où la menace d'un
  sbire agit, et cela demande de lire les compteurs de TOUS les sbires en jeu.

**Variantes maison** : aucune. `su011` Spider-Bot offre « track a minion **or**
remove 1 threat from a scheme », deux branches distinctes — la seconde n'est
PAS un track (rien n'est posé sur un sbire).

---

<a id="acceleration-2099"></a>

## Acceleration (capacité d'identité, Rainy) — homonyme de l'icône

⚠ **Ce n'est PAS le mot-clé `acceleration.md`.** Deux notions portent le même
mot. L'icône officielle pose de la menace au début de la phase vilain et se
déclare dans `desc.Acceleration` ; la capacité décrite ici est une **capacité
imprimée d'identité**, propre au pack fan-made **Spider-Man 2099** (Rainy),
et n'a aucun rapport. Ne jamais réutiliser `desc.Acceleration` ni
`HasAccelerationIcon` pour elle.

**Texte imprimé / définition** : sur `sm001a` * Spider-Man (face héros) :

> *Acceleration* — [star] **Response**: After your hero uses a basic power,
> seek an event from your deck. You may play that event. Place each other
> card you discarded this way on the bottom of your deck in the order you
> discarded them. *(Limit once per phase.)*

Six cartes du pack testent ensuite « **if you played this card using your
*Acceleration* ability** » ou « after you resolve your *Acceleration*
ability ». Le nom de la capacité est donc un **marqueur** que les autres
cartes lisent, pas seulement de la saveur.

**Mécanisme moteur** :

- Le « seek » est `Player.DiscardDeckUntil(effect, card_type=Event,
  return_other_faces=autres)` (voir `seek.md`) : il DÉFAUSSE depuis le dessus
  du deck jusqu'à défausser un événement.
- « You may play that event » : `Player.PlayCardsLikeInTurn([face], effect)`
  — la carte est dans la défausse, donc `is_like_in_hand` est posé par la
  fonction elle-même (`player_action.py:904`). ⚠ `if_not_play_discard_it`
  vaut `True` par défaut : c'est bien ce qu'on veut, l'événement non joué
  reste défaussé, puis part sous le deck comme les autres.
- « on the bottom of your deck in the order you discarded them » :
  `Faces.MoveAllToDeck(autres, deck, "Bottom", effect)` — la position est un
  **argument positionnel** (RECETTES §2), et l'ordre est celui de la liste
  rendue par `return_other_faces`, qui est déjà l'ordre de défausse.
- **Le marqueur.** Aucune primitive moteur ne dit « cette carte a été jouée
  par telle capacité ». Le pack pose donc son propre témoin sur le joueur au
  moment de l'appel à `PlayCardsLikeInTurn`, et les six cartes le lisent
  dans leur `conditions`. Helper commun du pack :
  `src/cards/pack/spider_man_2099/spider_man_2099/__init__.py`.

**Carte exemple** : `sm001a` * Spider-Man (l'identité qui porte la capacité) ;
`sm003` Accelerated Decoy pour la lecture du marqueur (« do both instead »).

**Pièges connus** :

- ⚠ **« After your hero uses a basic power »** est
  `AfterUnitUseBasicPower(type, "You", op, powers=["ATK","THW","DEF"])`
  (RECETTES §1, modèles `14001a`, `tt001a`). La **récupération** n'est pas un
  pouvoir de base au sens de ce message : elle a son propre
  `AfterUnitMakeRecovery`, et elle n'existe qu'en alter-ego, où cette face
  n'est pas en jeu.
- ⚠ **« Limit once per phase »** exige un témoin d'épuisement
  (PROCESSUS-CARTE 7 bis) : deux pouvoirs de base dans la MÊME phase, et un
  chiffre mesuré au second (taille du deck inchangée).
- ⚠ `sm008` Accelerated Vision donne « one additional time per phase (but
  still once per trigger) » : la limite ne peut donc pas être un simple
  `LimitOncePerPhase()` du moteur, qui ne sait pas compter jusqu'à deux. Le
  pack compte lui-même, par phase, dans le même helper que le marqueur.
- ⚠ Si le deck est épuisé sans trouver d'événement, l'insert tranche :
  mélanger la défausse en un deck neuf, puis placer dessous les cartes
  défaussées par la capacité. `DiscardUntil` gère déjà le remélange
  (`deck.py:483`) ; ce qui reste à la charge de la carte, c'est l'ordre final.

**Variantes maison** : `sm011` Spinnerets et `sm012` Web Cape se branchent
« after you resolve your *Acceleration* ability », c'est-à-dire **même quand
aucun événement n'a été joué** ; `sm010` Hyper-Agility, elle, exige
explicitement « **without playing an event** ». Trois portées différentes du
même déclencheur : les lire mot à mot.

---

<a id="drain-x"></a>

## Drain X

> ## ✅ LE MOT-CLÉ EST DÉFINI PAR ÉCRIT DEPUIS LE 31/08/2026
>
> L'insert du pack `venompool` (« Venompool Insert.png », CptScorp, Cycle 2)
> le définit noir sur blanc, et c'est **mot pour mot** la lecture retenue à
> l'aveugle le 4/8/2026 pour `agent_anti_venom` :
>
> > « When an ability instructs you to drain X from an enemy, deal X damage
> > to that enemy, then heal X damage from your identity. »
>
> La convention n'est donc plus une supposition arbitrée faute de mieux :
> elle a une source imprimée, et les deux packs la rendent à l'identique.
> La question systématique à l'utilisateur, exigée par la version précédente
> de cette fiche avant tout nouvel appel à `Drain()`, **n'a plus lieu d'être**
> tant qu'une carte reprend le mot-clé sans le modifier.

> ## ⚠ DEUX DÉFINITIONS COEXISTENT DEPUIS LE 29/09/2026
>
> Le glossaire fan-made de MC4DB dit :
>
> > « When this keyword is triggered by a character, deal X damage to that
> > character's target. Then, **if the target took that damage**, heal X
> > damage from the character who triggered drain. »
>
> Règle de priorité fixée par l'utilisateur : texte imprimé > MC4DB > fiche.
> - `venompool` **imprime** sa définition (insert ci-dessus, soin
>   inconditionnel sur l'identité) : il la garde. Divergence assumée avec
>   MC4DB, notée ici, pas dans le script.
> - `agent_anti_venom` n'imprime rien : son helper suit MC4DB, le soin n'a
>   lieu que si l'ennemi a **subi** les dégâts (un Tough les absorbe : pas de
>   soin). Cas « av009 ... vilain TOUGH », rouge avec l'ancien helper.
> - « the character who triggered drain » : sur les quatre cartes du dépôt,
>   c'est toujours l'identité (aucun allié ne déclenche un drain). Sans
>   effet aujourd'hui, à relire si un allié imprime le mot.
> - « a subi » se lit sur les **points de vie** (ou la défaite) de la cible,
>   pas sur le retour de `DealDamage`, qui compte les dégâts INFLIGÉS avant
>   prévention et rendait 1 face à un Tough.

**Texte imprimé / définition** : mot-clé maison, apparu dans le pack
`agent_anti_venom` — Unlikely Allies (« Drain 2 from an enemy ») et Bear
Arms (« drain 1 from the villain ») — où il n'était **défini nulle part**
(aucun insert dans les trois dossiers Drive du pack, rien trouvé en ligne).
Le pack `venompool` a fourni la définition imprimée (encadré ci-dessus) :
X dégâts à l'ennemi ciblé, puis X soins sur l'identité du joueur qui résout
l'effet, et sur elle seule (pas sur l'allié qui déclenche l'effet s'il est
distinct du héros).

**Mécanisme moteur** : centralisé dans `Drain()` du `__init__.py` du set
`agent_anti_venom` (`Fusion/marvel-lcg-src/src/cards/pack/agent_anti_venom/agent_anti_venom/__init__.py`) :

```python
def Drain(source: 'CardFace', targets: Sequence['CardFace'], value: int, effect: 'Effect') -> None:
    if not targets:
        return
    avant = {cible: cible.health for cible in targets if hasattr(cible, "health")}
    source.DealDamage(targets, value, effect)
    subis = any(cible.health < sante or cible.IsDefeated() or not cible.IsInPlay()
                for cible, sante in avant.items())
    if not subis:
        return
    identity = GetAgentAntiVenom(effect)
    if identity is not None:
        source.HealthUnits([identity], value, effect)
```

`GetAgentAntiVenom(effect)` remonte l'identité du joueur qui résout l'effet
via `effect.GetInitiator().GetIdentity()`, quelle que soit sa face (Hero ou
Alter-Ego) : c'est ce qui garantit que les soins vont bien sur Agent
Anti-Venom lui-même, jamais sur la carte source de l'effet (Bear Arms,
Unlikely Allies). Chaque carte appelle `Drain(source, targets, X, effect)`
avec son propre `X` : pas de champ `desc` dédié, la valeur est en dur dans
le script de chaque carte.

**Carte exemple** : `av009` (Bear Arms), extrait de
`Fusion/marvel-lcg-src/src/cards/pack/agent_anti_venom/agent_anti_venom/av009.py` :

```python
def bear_arms_drain(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
    this = effect.this.CastTo(Upgrade)
    Drain(this, effect.targets, 1, effect)
```

`av007` (Unlikely Allies) appelle la même fonction avec `value=2`, dans une
des quatre branches ouvertes selon l'icône de ressource imprimée de la
carte défaussée (« [physical] - Drain 2 from an enemy. ») :

```python
def _drain(initiator: 'Player', source: 'CardFace', effect: 'Effect') -> 'Ability':
    return AbilityFactory.ForChoiceAbility(
        "Drain 2 from an enemy",
        lambda targets:
            Drain(source, targets, 2, effect)
    ).SetTarget(Enemy)
```

**Pièges connus** : chaque pack garde son **propre** helper `Drain()`, et
depuis le 29/09/2026 les deux corps DIFFÈRENT (soin conditionnel côté
`agent_anti_venom`, inconditionnel côté `venompool`, voir l'encadré). Deux
raisons de ne pas les fusionner : l'identité soignée n'est pas la même, et un
pack custom ne doit pas dépendre d'un autre pack custom (un joueur peut très
bien avoir installé l'un sans l'autre). Autre piège
local, propre à Bear Arms : le « next attack gains ranged » de sa première
capacité n'a pas de mécanisme « prochaine attaque » dans le moteur ; il est
simulé par une capacité temporaire `UnitAttackGainKeyword` posée sur
l'identité et retirée dès sa première exécution (`unregister_after_exec`),
sans lien direct avec `Drain()`.

**Variantes maison** : le pack `venompool` (CptScorp, set 129) reprend le
mot-clé sans le modifier, sur deux cartes — `vp009` Klyntar Suit (« drain 1
from the attacking enemy », Response après avoir subi des dégâts d'une
attaque) et `vp010` True Form (« Drain 1 from that enemy », Interrupt sur
une attaque de base). Helper local dans
`Fusion/marvel-lcg-src/src/cards/pack/venompool/venompool/__init__.py`.

---

<a id="traitor"></a>

## Traitor

**Texte imprimé / définition** : mot-clé maison du pack nemesis
`agent_anti_venom` (« Agent Anti-Venom Nemesis »), défini en toutes lettres
sur les deux cartes qui le posent, contrairement à `drain X`. Texte exact
lu dans `cards.json` sur The Made Men (`av014`) et * Infected Scorpion
(`av015`) : « gains traitor *(treat that ally as a minion engaged with its
owner. It has 1 SCH, a blank printed text box, and does not take
consequential damage.)* ».

**Mécanisme moteur** : rendu par `TreatAsMinion`
(`game/ability/factory/treat.py`), une fonction déjà présente dans le
moteur. Manipulated Mind (27171) et « Lost » Child (47027) n'appellent
PAS cette fonction nue : elles utilisent
`AbilityFactory.TreatAttachedCardAsMinion(Ally, "Minion", ...)`
(`treat.py`, méthode statique de la classe `AbilityFactoryTreat`, le même
fichier que `TreatAsMinion`), un helper apparenté mais
distinct, câblé sur l'attachement de la carte (`AttachTo2` dans leur
`WhenThisRevealed`, converti automatiquement via
`AfterCardGainUpgrade`). Ici le déclencheur du pack `agent_anti_venom`
est une capacité de carte (Forced Interrupt), pas un attachement posé
sur l'allié : `GainTraitor` appelle donc directement la fonction nue
`TreatAsMinion`, hors du chemin `TreatAttachedCardAsMinion` /
attachement. Ce n'est pas un cas inédit dans le dépôt : Spider-Woman :
Veranke (`mw026.py`, pack `madame_web`) appelle elle aussi `TreatAsMinion`
directement, sans attachement, depuis un Forced Interrupt sur
`WhenUnitWouldBeDefeated`. Extrait de
`Fusion/marvel-lcg-src/src/cards/pack/agent_anti_venom/agent_anti_venom_nemesis/__init__.py` :

```python
from game.ability.factory.treat import TreatAsMinion

TRAITOR_TEMPLATE = "Traitor Minion"


def _sch_a_un(minion: Any, ally: Any, effect: 'Effect') -> None:
    minion.printed_scheme = 1


def GainTraitor(ally: 'CardFace', effect: 'Effect') -> bool:
    """Transforme un allie en sbire engage avec son proprietaire."""
    player = ally.CastTo(Ally).GetControlByPlayer()
    if player is None:
        return False
    return TreatAsMinion(ally, TRAITOR_TEMPLATE, player, effect, process=_sch_a_un)
```

`GainTraitor` s'appuie sur la carte-gabarit `aav_traitor_minion`
(« Traitor Minion ») pour la conversion, et force le SCH à 1 via le
callback `process=_sch_a_un` (le gabarit ne porte pas nativement ce SCH).
Le commentaire du fichier précise l'import : `TreatAsMinion` est une
fonction de module, pas une méthode d'`AbilityFactory`, donc non
réexportée par le `from game.ability.factory import *` de
`cards/pack/__init__.py` ; il faut l'importer explicitement.

**Carte exemple** : `av015` (* Infected Scorpion), extrait de
`Fusion/marvel-lcg-src/src/cards/pack/agent_anti_venom/agent_anti_venom_nemesis/av015.py` :

```python
def infected_scorpion(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
    this = effect.this.CastTo(Minion)
    Unused(this)

    cible = message.target
    if cible is None or not Ally.IsType(cible):
        return

    def prevenir(effect2: 'Effect', message2: 'Message.WhenUnitWouldTakeDamage') -> None:
        message2.PreventDamage("All", effect2)

    cible.effect.RegisterTemp(
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Temp0,
            "This",
            prevenir,
            is_from_attack=message.would_atk_message,
        ),
        unregister_after_exec=True,
    )

    GainTraitor(cible, effect)
```

`av014` (The Made Men, side scheme nemesis) appelle la même `GainTraitor`
sur l'allié au plus haut ATK imprimé de chaque joueur, après chaque
schéma/attaque de Maniac.

**Pièges connus** : ne pas confondre `TreatAsMinion` (fonction nue de
`treat.py`, appelée directement depuis une capacité) avec
`AbilityFactory.TreatAttachedCardAsMinion` (`treat.py`), le helper
utilisé par Manipulated Mind et « Lost » Child, qui suppose lui un
attachement posé sur l'allié et se déclenche via `AfterCardGainUpgrade`.
Une implémentation qui chercherait `traitor` uniquement du côté
`TreatAttachedCardAsMinion` / attachement raterait le cas `agent_anti_venom`,
puisqu'ici aucun attachement n'est posé sur l'allié : il faut appeler la
fonction nue `TreatAsMinion` directement depuis la capacité de la carte
source (Forced Interrupt ou Forced Response), comme le fait `GainTraitor`
et comme le fait aussi `mw026.py` pour Spider-Woman : Veranke. Piège annexe propre à
Infected Scorpion : la capacité écoute `WhenUnitWouldAttackUnit`, pas
`WhenUnitWouldAttack` (à ce dernier moment l'attaque vise encore le
joueur, le défenseur n'est pas désigné, et `attacked_targets` ne contient
jamais d'allié).

**Variantes maison** : `TreatAsAlly` de Totally Awesome Hulk
(`tah_hellbender_ally`, pack `totally_awesome_hulk`) est le même genre de
montage (« traiter une carte comme si »), à inspecter si un futur pack a
besoin d'un « traiter comme » différent de `traitor`.

---

<a id="companion"></a>

## Companion

**Texte imprimé / définition** : mot-clé maison du pack `lockjaw` (héros
custom **Lockjaw**, « Nugget », Marvel Champions Custom Project Cycle I),
porté par plusieurs alliés du deck signature. Texte exact lu dans
`cards.json` sur * Hairball (`lj021`) : « Companion. *(This ally does not
count towards the ally limit, and it cannot be used to defend against
attacks.)* ». Le texte entre parenthèses est celui qui définit le mot-clé,
imprimé identiquement sur chaque carte qui le porte.

**Mécanisme moteur** : composé dans `Companion()`
(`Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw/__init__.py`) à
partir de deux fabriques génériques déjà présentes dans le moteur, sans
mot-clé dédié :

```python
def Companion() -> List['Ability']:
    """« Companion » : hors limite d'alliés, et ne peut pas défendre.

    Mot-clé maison du pack, sans équivalent dans le moteur : il se compose de
    deux règles déjà existantes.
    """
    return [
        *AbilityFactory.ThisNotCountAllyLimit(),
        *AbilityFactory.UnitCannotDefend(
            "This",
            None,
            cannot_trigger_defense_ability=True,
        ),
    ]
```

`ThisNotCountAllyLimit()` (`AbilityFactoryFriend`,
`game/ability/factory/friend.py`) écoute `Message.CheckIfAllyCountLimit` et
appelle `message.SetNotCountAlly(effect)` dès que l'allié vérifié est bien
« This » : c'est la règle générique derrière tout allié qui ne compte pas
dans la limite (le moteur ne connaît que cette fabrique, pas un concept
« Companion »).

`UnitCannotDefend("This", None, cannot_trigger_defense_ability=True)`
(`AbilityFactoryDoAttack`, `game/ability/factory/do_attack.py`) écoute
`Message.CheckIfUnitCanDefendAgainstAttack` et appelle
`message.SetCannotDefend(effect)`. Le deuxième paramètre positionnel
(`who_attacker`) est `None` : lu dans `Condition.CheckWhichCard`
(`game/ability/condition/card_type.py`, fonction interne
`invoke_check_card`), un `check_rule` à `None` renvoie toujours `True`,
donc la restriction ne porte que sur l'unité (« This »), pas sur
l'attaquant : Hairball ne peut défendre contre aucun ennemi, pas seulement
certains. `cannot_trigger_defense_ability=True` ajoute en plus
l'incapacité à déclencher une capacité de défense propre à la carte (pas
seulement l'action de défense de base) ; ce paramètre est aussi ce qui
distingue `UnitCannotDefend` de sa variante `UnitCannotMakeBasicDefense`
(même fichier), qui appelle `UnitCannotDefend` avec
`cannot_trigger_defense_ability=False` pour ne bloquer que la défense de
base.

**Carte exemple** : `lj021` (* Hairball), extrait de
`Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw/lj021.py` :

```python
def GetAbilities() -> Sequence['Ability']:

    def amortir(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage(1, effect)

    return [
        *Companion(),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            Friend,
            amortir,
            is_from_attack=True,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
```

D'autres alliés du pack portent le même `*Companion()` en tête de leurs
capacités : Zabu (`lj018`), Throg (`lj019`), Redwing (`lj020`) et Lockheed
(`lj022`), tous confirmés par grep sur le dossier
`Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw/`.

**Pièges connus** : aucun signalé au 29/08/2026.

**Variantes maison** : **Squirrel** (pack `squirrel_girl`, fonction
`Ecureuil()` dans
`Fusion/marvel-lcg-src/src/cards/pack/squirrel_girl/squirrel_girl/__init__.py`)
reprend le même montage `ThisNotCountAllyLimit()` +
`UnitCannotDefend("This", None, cannot_trigger_defense_ability=True)`, mais
n'est pas une simple copie augmentée d'une capacité de dépense : elle
ajoute aussi `AbilityFactory.UnitCannotHaveUpgradeAttached("This")` (l'allié
ne peut pas recevoir d'amélioration), la capacité de dépense étant portée
séparément par le reste du pack et non par `Ecureuil()` elle-même. Voir
`squirrel.md` pour le détail.

---

<a id="squirrel"></a>

## Squirrel

**Texte imprimé / définition** : mot-clé maison du pack `squirrel_girl`
(héroïne custom **Squirrel Girl**), porté par les six alliés du « deck
écureuil ». Texte exact lu dans `cards.json` sur * Tippy-Toe (`sg002`) :
« Squirrel. *(Does not count against your ally limit. Cannot defend.
Cannot have upgrades attached. Cannot be chosen or strengthened by
non-Squirrel Girl player cards. When it leaves play, put it into the
Squirrel discard pile. Can be spent for Squirrel Aid.)* ». Contrairement à
Companion, ce texte ne se réduit pas à deux règles : il en couvre cinq, et
seules les trois premières sont portées par la fonction du mot-clé
elle-même (voir plus bas).

**Mécanisme moteur** : composé dans `Ecureuil()`
(`Fusion/marvel-lcg-src/src/cards/pack/squirrel_girl/squirrel_girl/__init__.py`,
lignes 283-299), commune aux six cartes du deck écureuil :

```python
def Ecureuil() -> List['Ability']:
    return [
        *AbilityFactory.ThisNotCountAllyLimit(),
        *AbilityFactory.UnitCannotDefend(
            "This",
            None,
            cannot_trigger_defense_ability=True,
        ),
        *AbilityFactory.UnitCannotHaveUpgradeAttached("This"),
    ]
```

Les deux premières fabriques sont identiques à celles de `Companion()` (voir
`companion.md`) : `ThisNotCountAllyLimit()` pour « ne compte pas dans la
limite d'alliés », `UnitCannotDefend("This", None,
cannot_trigger_defense_ability=True)` pour « ne peut pas défendre ».
`UnitCannotHaveUpgradeAttached("This")`
(`game/ability/factory/ability_factory.py`, lignes 287-314) ajoute « ne peut
pas recevoir d'amélioration » : elle écoute `Message.CheckIfFaceCanAttachTo`
pour refuser l'attache dès l'intention (`SetCannotAttachTo`), et
`Message.WhenCardWouldAttachTo` en filet de sécurité, qui défausse
l'amélioration à la place de l'attacher (`SetBeInstead` +
`Faces.DiscardAll`) si elle passait quand même.

Ces trois fabriques ne couvrent que 3 des 5 clauses du texte imprimé. Les
deux autres sont portées ailleurs, pas par `Ecureuil()` :

- « *Cannot be chosen or strengthened by non-Squirrel Girl player cards* »
  passe par deux points d'accroche posés carte par carte dans
  `PreparerEcureuil(face, joueur)` (lignes 134-159), appelée une fois par
  écureuil au setup : `face.refuse_target_fn` et `face.refuse_gain_fn` sont
  réglés sur `_EstSourceEtrangere`, qui renvoie vrai si la source de l'effet
  est une carte joueur hors du set. Ce ne sont pas des capacités
  interceptables : `refuse_target_fn` est lu en direct par
  `GetAllLegalTargets` (le seul entonnoir de sélection de cibles) et
  `refuse_gain_fn` par `Gain`, qui est `@final`.
- « *When it leaves play, put it into the Squirrel discard pile* » passe
  aussi par `PreparerEcureuil`, qui enregistre sur chaque écureuil un
  `WhenCardWouldMoveToArea` (`AbilityType.Temp0`) : dès que le mouvement
  visé est vers `discard_pile` ou `player_deck`, il est redirigé vers
  `additional_discard_pile` / `additional_deck` du joueur
  (`message.ChangeToArea(...)`).
- « *Can be spent for Squirrel Aid* » passe par `CapaciteDepenseIdentite()`
  (lignes 235-280), une capacité `Resource` (« Discard a SQUIRREL ally you
  control → 1 [wild] », `for_card=FinderCarteSquirrelGirl()`) posée sur les
  deux faces d'**identité** (`sg001a` et `sg001b`, appel confirmé aux lignes
  47 et 30 de leurs fichiers respectifs), et non sur les six écureuils. Le
  docstring de la fonction explique pourquoi : le moteur recense les
  sources de paiement une seule fois, avant toute dépense, et chaque
  capacité ne compte que pour une source. Poser la capacité sur les six
  écureuils offrirait six sources qu'il serait ensuite impossible de
  limiter (refuser une source déjà recensée fait échouer l'assertion
  `len(resources_effects) == 1` de `ProcessPayingEffect`). Avec une source
  unique sur l'identité, la limite « 1 seul écureuil par carte jouée » du
  matériel d'origine devient structurelle : le joueur choisit toujours quel
  écureuil part, via le coût (`CostFunc.Custom` ciblant un allié `SQUIRREL`
  qu'il contrôle).

**Carte exemple** : `sg002` (* Tippy-Toe), extrait de
`Fusion/marvel-lcg-src/src/cards/pack/squirrel_girl/squirrel_deck/sg002.py` :

```python
return [
    *Ecureuil(),
    AbilityFactory.AfterCardEnterPlay(
        AbilityType.Response,
        "This",
        reordonner,
        conditions=[PasDeDiscorde],
    ),
]
```

Les six écureuils (`sg002` à `sg007`) portent tous `*Ecureuil()` en tête de
leurs capacités, confirmé par lecture du dossier
`Fusion/marvel-lcg-src/src/cards/pack/squirrel_girl/squirrel_deck/`. Notes
sur l'identifiant : les card_id du pack suivent le format `sgNNN` (`sg001a`,
`sg001b`, `sg002`…`sg022`), pas le format numérique `750NN` mentionné dans
une version antérieure du plan de doc ; une recherche `grep "\"750"` sur
`cards.json` ne renvoie donc rien pour ce pack, il faut chercher par
`"card_id": "sg0` ou par le nom des cartes.

**Pièges connus** :

- Les cartes du deck écureuil sont hors jeu : elles ne se désignent PAS par
  `SetTarget(Select.From(faces=...))` (le sélecteur ne les restreint pas),
  mais par `player.MayChooseFace(faces, effect, not_move=True)`. Vu à
  l'œuvre dans `AppelerEcureuil` (interruption de Network of Trees,
  `sg012`) et dans `sg002.reordonner` (Tippy-Toe reclasse le dessus du deck
  écureuil).
- Poser `CapaciteDepenseIdentite()` sur chaque écureuil au lieu de
  l'identité casserait la limite « 1 écureuil par carte jouée » : voir
  l'explication détaillée ci-dessus (assertion `ProcessPayingEffect`).
- `Puzzle.PutIntoPlay` crée une copie NEUVE de la carte, qui n'a reçu aucune
  règle de setup (ni `PreparerEcureuil`, ni le montage du deck écureuil) :
  tout cas de test portant sur les règles d'un écureuil doit le faire
  APPELER par le jeu (`AppelerEcureuil`), pas le poser directement en jeu.

**Variantes maison** : **Companion** (pack `lockjaw`, voir `companion.md`)
partage la même base `ThisNotCountAllyLimit()` +
`UnitCannotDefend("This", None, cannot_trigger_defense_ability=True)`, sans
la troisième fabrique (`UnitCannotHaveUpgradeAttached`) ni la mécanique de
dépense.

---

<a id="destroy"></a>

## Destroy (mot-clé maison, pack `sentinel`)

**Texte imprimé / définition** (insert du pack, `Insert.jpg`) : « When you are
instructed to **destroy** a Component upgrade, take 2 unpreventable damage and
flip that Component from its **Intact** side to its **Destroyed** side. A
Component that is already on its Destroyed side cannot be destroyed. »

Traduction retenue : « Quand on vous demande de **détruire** une amélioration
Component, subissez **2 dégâts imblocables** et retournez ce Component de sa
face **Intacte** à sa face **Détruite**. Un Component déjà sur sa face Détruite
ne peut pas être détruit. »

**Mécanisme moteur** : aucune primitive. Le mot-clé est un **raccourci de
texte**, pas une règle du moteur : il se déroule en deux opérations que le
moteur connaît déjà. **L'ordre du code est l'inverse de celui du texte**, et ce
n'est pas un détail (voir le troisième piège ci-dessous).

1. **Retourner le Component**, `Faces.FlipAllTo([component], face_up=None, effect)`
   (`src/game/operate/faces.py:144`), comme la Battle Board de `night_thrasher`
   (`nt003a` / `nt003b`) et la Spider Armor d'`armored_spidey` (`as002a`).
2. **2 dégâts imblocables à l'identité**, avec
   `DamageProperty(damage=2, ignore_tough=True, unpreventable=True)` — c'est le
   héros qui subit, pas le Component.

⚠ **`DamageProperty.unpreventable` n'existait pas avant ce pack** (ajouté le
12/09/2026). Les deux seules cartes officielles qui emploient le mot
(`62001a` Luke Cage, `62028` Internal Injury) se contentaient d'`ignore_tough`,
qui ne ferme qu'**une porte sur trois** : la carte Coriace. Une prévention
chiffrée (`08032` Defensive Stance) ou un remplacement pur et simple
(`49006` Magnetic Bubble, et surtout `st001a` lui-même) passaient au travers.
Le drapeau est honoré par `Message.WhenUnitWouldTakeDamage`, dans
`PreventDamage` **et** dans `SetBeInstead`. Les deux cartes officielles ont été
mises à jour au passage.

Le pack centralise les deux opérations dans **`Detruire()`** du `__init__.py` du
set : neuf cartes emploient le mot-clé, aucune ne doit pouvoir en diverger.

**Carte exemple** : `st001a` Sentinel — « Interrupt: When you would take any
amount of damage, destroy a COMPONENT upgrade instead. » Le mot-clé est ici la
substitution elle-même : les dégâts de l'attaque sont remplacés par 2 dégâts
imblocables plus le retournement. Voir aussi `st006` Exterminate, `st007`
Hardwire Access, `st008` Rocket Punch et `st009` Threat Suppression, dont le
coût additionnel est « inclinez **ou détruisez** » un Component nommé.

**Pièges connus** :

- **« Un Component déjà Détruit ne peut pas être détruit »** : la cible légale
  est une amélioration portant les traits `COMPONENT` **et** `INTACT`. Le
  moteur ne le déduit pas : chaque appel filtre sur le trait `INTACT`.
- **Les 2 dégâts ne sont pas préventibles, et c'est vital.** Sur `st001a`,
  l'interruption remplace des dégâts par d'autres dégâts. **Mesuré le
  12/09/2026, sans le drapeau** : une attaque de sbire à 2 dégâts retournait les
  QUATRE pièces d'un coup, chaque destruction relançant l'interruption. Et dans
  une version antérieure, où les dégâts tombaient AVANT le retournement, la
  boucle ne s'arrêtait jamais — trois parties d'autoplay bloquées sur la même
  question reposée à l'identique.
- **Retourner d'abord, blesser ensuite.** L'insert énonce l'inverse, mais c'est
  le seul ordre qui termine : si les dégâts partent en premier, la pièce visée
  est encore INTACT au moment où une relance cherche une cible.
- **C'est le HÉROS qui subit les 2 dégâts**, jamais le Component : une
  amélioration n'a pas de points de vie.
- **Détruire n'est pas défausser.** Le Component reste en jeu, retourné. Une
  carte qui défausse une amélioration (`st015` Mark VII-A, second volet) fait
  autre chose.
- **Le coût additionnel « inclinez OU détruisez »** est un choix du joueur
  **dans le coût**, pas dans l'effet : le moteur doit proposer les deux, et
  « détruire » reste possible quand la carte est déjà inclinée. C'est ce qui
  permet de rejouer un événement dans le même tour, en payant de sa carrosserie.

---

<a id="exposed"></a>

## Exposed (carte d'état maison, pack `sentinel`)

**Texte imprimé** (`Exposed Status.png`) : « The next time this character is
attacked, discard all Exposed status cards from it. That attack deals 1
additional damage for each Exposed status card discarded this way. »

Traduction retenue : « La prochaine fois que ce personnage est attaqué,
défaussez toutes ses cartes d'état Exposé. Cette attaque inflige 1 dégât de
plus par carte d'état Exposé défaussée ainsi. »

**Ce que c'est** : une **quatrième carte d'état**, à côté de Coriace, Sonné et
Désorienté. Le moteur n'en connaissait que trois.

**Mécanisme moteur** : l'état est une vraie carte, comme les trois autres.

| Endroit | Ce qu'il a fallu |
|---|---|
| `data/cards.json`, pack `status` | une carte `{"card_id": "exposed", "type": "Status", "name": "Exposed"}`, jumelle des trois autres |
| `CardFace.STATUS` (`src/game/card/face/card_face.py`) | `"Exposed"` ajouté au `Literal` |
| `StatusCard.symbol_name` (`card_type/card_status.py`) | l'entrée `"Exposed": Symbol.exposed` |
| `Symbol` (`src/game/render/symbol.py`) | `exposed` |
| `Status.exposed` (`card/face/component/status.py`) | la propriété de comptage, jumelle de `confused`/`stunned`/`tough` |
| `CanStatus.exposed` et `HasStatus` (`attribute/can_status.py`) | sans quoi `HasStatus("Exposed")` tombait sur `assert False`, et `has_status="Any"` ignorait le quatrième état |
| `Puzzle.Expose` (`game/puzzle/puzzle.py`) | poser l'état dans un cas de test, comme `Puzzle.Tough` |
| `src/cards/pack/status/exposed.py` | la capacité de la carte, `AbilityType.Status` sur `"AttachedCharacter"`, modèle `tough.py` |

Un état se pose par `face.GainStatus("Exposed", effect)`
(`attribute/can_status.py:67`) et se retire par `LoseState`. **Exposé
s'empile** : contrairement à Coriace, `GainStatus` ne lui oppose aucun plafond
(`tough_max`), ce qui est voulu — « 1 dégât de plus **par carte** ».

**Carte exemple** : `st002a` Head (Intact) — « Hero Action: Exhaust Head
(Intact) → expose 2 enemies. » Voir aussi `st006` Exterminate (expose 2
ennemis après ses 7 dégâts), `st013` Targeting Protocol, et les deux cartes qui
**comptent** les Exposé en jeu : `st007` Hardwire Access et `st013`.

**Pièges connus** :

- **« Est attaqué » n'est pas « subit des dégâts ».** L'état se déclenche sur
  l'attaque, pas sur la source de dégâts : une carte qui inflige des dégâts
  sans attaquer ne le consomme pas.
- **Tout part d'un coup, et les dégâts se cumulent** : deux Exposé sur la même
  cible font +2, et les deux cartes s'en vont ensemble.
- **Les Exposé du plateau se comptent partout**, pas seulement sur la cible :
  `st007` et `st013` lisent « the number of Exposed status cards **in play** ».
- **Un état posé sur un ennemi vaincu part avec lui** : le décompte peut
  changer entre le moment où le joueur choisit sa carte et celui où elle se
  résout.
- **Le plateau les dessine déjà, mais PAS gratuitement.** `Board.tsx` sépare
  bien les cartes `kind === 'status'` des améliorations, et `etats.ts` a un repli
  générique qui aurait affiché un « E ». Trois endroits devaient quand même être
  mis à jour, sans quoi le quatrième état était muet ou anglais :
  `ETATS` dans `etats.ts` (nom français « Exposé », classe propre),
  `Statut` / `STATUTS` / `libelleStatut` dans `effets-statuts.ts` (sans quoi
  **aucun badge** n'annonçait la pose ni le retrait), et le type
  `CardEffectDelta` dans `ScanCard.tsx`. Plus le scan
  (`assets/textures/exposed.webp`, à côté de `tough.webp`).
- **Le décompte « in play » se lit sur les PERSONNAGES** :
  `Worlds.GetOnFieldCharacters` puis `components.status.exposed`. Le helper
  `ExposedEnJeu` du pack `sentinel` est le seul endroit qui le fait.

---

<a id="investigate-x"></a>

## Investigate X

**Texte imprimé / définition** : mot-clé maison du pack `jessica_jones`
(héroïne custom **Jessica Jones**, par « ekAugust »), porté par quatre des
cinq manigances secondaires du set de rencontre « On the Job ». Texte exact
lu dans `cards.json` sur * Chase Down a Lead (`jj013`) : « Investigate 2.
*(When revealed, move 2 threat from the main scheme to here.)* ». Le
gabarit `X[per_hero]` existe aussi : sur * Hang Back and Watch (`jj014`),
« Investigate 2[per_hero]. *(When revealed, move 2[per_hero] threat from
the main scheme to here.)* ».

**Mécanisme moteur** : composé dans `Investigate(value, *, per_hero=False)`
(`Fusion/marvel-lcg-src/src/cards/pack/jessica_jones/on_the_job/__init__.py`,
lignes 16-36), commune aux cartes du set qui portent le mot-clé :

```python
def Investigate(value: int, *, per_hero: bool=False) -> 'Ability':

    def investigate(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        amount = value
        if per_hero:
            amount *= Worlds.GetPlayerNumIcon(effect)

        main = Worlds.FindMainScheme(this)
        if main is None:
            return

        moved = this.RemoveThreatFromSchemes([main], amount, effect)
        if moved:
            this.PlaceThreatOnSchemes([this], moved, effect)

    return AbilityFactory.WhenThisRevealed(
        None,
        investigate,
    )
```

Aucune fabrique moteur ne porte ce mot-clé nativement : c'est un script
carte par carte, posé en tête de `GetAbilities()` de chaque carte
concernée. `AbilityFactory.WhenThisRevealed(None, investigate)`
(`game/ability/factory/reveal.py`, ligne 118) est la fabrique générique
« When Revealed » du moteur, sans condition ici (`None`). Le calcul en
deux temps suit le texte imprimé au mot près : `RemoveThreatFromSchemes`
retire d'abord `amount` de menace sur la manigance principale trouvée par
`Worlds.FindMainScheme` (`game/operate/worlds.py`, ligne 101), et renvoie
`moved`, la quantité réellement retirée ; seule cette quantité (jamais la
valeur demandée telle quelle) est ensuite posée sur la carte elle-même via
`this.PlaceThreatOnSchemes([this], moved, effect)`. `RemoveThreatFromSchemes`
et `PlaceThreatOnSchemes` sont deux méthodes génériques de `CardFace`
(`game/card/face/card_face.py`, lignes 641 et 567), pas des fabriques
propres au mot-clé : une manigance principale à 0 menace (ou déjà vidée par
un `RemoveThreatFromSchemes` précédent dans la même résolution) ne donne
donc rien, conformément au commentaire du fichier source (« une manigance
principale à 0 de menace ne doit rien donner »).

Le multiplicateur `per_hero` (`jj014`, `jj015`) multiplie `value` par
`Worlds.GetPlayerNumIcon(effect)` avant le retrait ; il ne change rien au
reste du mécanisme.

**Carte exemple** : `jj013` (* Chase Down a Lead), extrait de
`Fusion/marvel-lcg-src/src/cards/pack/jessica_jones/on_the_job/jj013.py` :

```python
return [
    Investigate(2),

    AbilityFactory.WhenSchemeBeDefeated(
        AbilityType.WhenDefeated,
        "This",
        when_defeated,
    ),
]
```

Trois autres manigances du set portent aussi `Investigate(...)` en tête de
leurs capacités, confirmé par grep sur le dossier
`Fusion/marvel-lcg-src/src/cards/pack/jessica_jones/on_the_job/` : `jj014`
(* Hang Back and Watch, `Investigate(2, per_hero=True)`), `jj015` (* Pore
Over the Evidence, `Investigate(1, per_hero=True)`) et `jj016` (* Sneak
Into the Crime Scene, `Investigate(2)`). La cinquième carte du set, `jj012`
(* Always a Bigger Conspiracy), ne porte pas le mot-clé : son texte imprimé
n'a pas de clause « When revealed », confirmé par lecture de son fichier
source et de son `text` dans `cards.json`, qui ne mentionnent aucun
« Investigate ».

**Pièges connus** : aucune fabrique moteur ne porte ce mot-clé nativement,
ne pas chercher du côté d'`AbilityFactory` standard. Le set de rencontre
« On the Job » lui-même (`data/encounter_sets/on_the_job.json`, cartes
`jj012` à `jj016`) est ajouté au deck Rencontre via
`message.encounter_set_names` dans `Message.WhenGameBeginSetup`,
enregistré en `RegisterTemp` depuis `WhenPlayerSelectHero` : ce point
d'accroche est nécessaire car `World.Begin` a déjà créé puis mélangé le
deck Rencontre à l'étape suivante, un `ShuffleAllTo` plus tardif arriverait
trop tard. Ce mécanisme d'ajout du set n'est pas propre au mot-clé
Investigate, mais conditionne l'apparition en jeu des cartes qui le
portent.

**Variantes maison** : aucune connue au 29/08/2026.

---

<a id="setlist"></a>

## Setlist

**Texte imprimé / définition** : « Setlist » désigne, dans le pack maison
`dazzler` (héroïne custom **Dazzler**, contenu de « Lord Havok »), la zone
de jeu créée par l'upgrade permanent **Live Concert** (`dz017a`) où
s'accumulent les événements de trait [[SONG]] joués. Le mot « Setlist »
n'apparaît pas littéralement dans le texte imprimé de `dz017a` : « Response:
After you resolve a [[SONG]] event attach it here, placed in a row to the
side of this card (to a maximum of 4). Once placed here, it cannot be
swapped with a new card. Hero Action: Flip this card to its Showtime! side
and reveal it. » « Setlist » est le nom donné par le pack, et repris dans le
code (commentaire de tête du fichier central : « Tout le set tourne autour
d'une zone, la SETLIST »), à cette zone à 4 emplacements, plutôt qu'un
mot-clé imprimé verbatim sur une carte.

**Mécanisme moteur** : composé dans
`Fusion/marvel-lcg-src/src/cards/pack/dazzler/dazzler/__init__.py`. Ce
fichier n'existe ni dans ce worktree ni dans l'historique git de ce dépôt
(vérifié lors de cette tâche : absent de `master` et de toutes les branches
accessibles via `git log --all`). Son contenu ci-dessous a été lu
directement par l'agent coordinateur dans le checkout original
`/mnt/c/Users/arnau/Desktop/Marvel LCG/` (hors
du périmètre de ce worktree) et transmis verbatim ; il n'a pas été relu de
façon indépendante par l'agent qui rédige cette fiche.

```python
def Concert(effect, joueur=None):
    """Live Concert en jeu, quelle que soit sa face (Live Concert / Showtime!),
    chez le joueur courant."""
    # cherche par nom, les deux faces de la meme carte physique

def Setlist(effect, joueur=None) -> list:
    """Les [[SONG]] actuellement dans la Setlist (zone PlaceCardArea de
    Live Concert), dans l'ordre de pose."""
    concert = Concert(effect, joueur)
    if concert is None: return []
    zone = concert.GetPlacedCardArea()
    if zone is None: return []
    return list(zone.Get(True))

def SetlistALaPlace(effect) -> bool:
    """« to a maximum of 4 » : la Setlist accepte-t-elle une carte de plus ?"""
    return len(Setlist(effect)) < 4  # PLACES_SETLIST = 4
```

`Setlist()` s'appuie sur `Concert()` pour retrouver Live Concert en jeu
(quelle que soit sa face, Live Concert ou Showtime!, chez le joueur
courant, recherché par nom), puis lit sa `PlaceCardArea` (zone de cartes
attachées) via `GetPlacedCardArea()` et rend la liste des cartes qui s'y
trouvent (`zone.Get(True)`), dans l'ordre de pose. Si Live Concert n'est
pas en jeu, ou si sa zone est absente, `Setlist()` rend une liste vide.

La pose dans la zone est gérée par `dz017a` lui-même, pas par la fonction
`Setlist()` : sa capacité Response (`ranger_dans_la_setlist`, voir Carte
exemple) attache l'événement [[SONG]] résolu via
`this.PlaceCardHere([chanson], True, effect)` (face visible), sous
condition `SetlistALaPlace(effect)` (`len(Setlist(effect)) < 4`), la limite
de 4 emplacements imprimée sur la carte (« to a maximum of 4 »). La limite
est donc imposée côté condition de pose, pas par une limite native de
`PlaceCardArea`.

La sortie de la Setlist se fait par le retournement de Live Concert sur sa
face Showtime! (`dz017b`) : mécanisme traité par le mot-clé Showtime! (voir
`showtime.md`), pas par Setlist lui-même.

**Carte exemple** : `dz017a` (Live Concert, upgrade permanent recto),
extrait de `dz017a.py`, transmis par le coordinateur :

```python
def GetAbilities():
    def ranger_dans_la_setlist(effect, message):
        this = effect.this.CastTo(Upgrade)
        chanson = message.played_face
        if chanson is None: return
        this.PlaceCardHere([chanson], True, effect)  # FACE VISIBLE

    def lever_le_rideau(effect, message):
        joueur = effect.GetInitiator()
        Faces.FlipAllTo(effect.targets, None, effect)
        for face in effect.targets:
            montree = face.card.face
            if montree is not None and montree.IsInPlay():
                montree.Reveal(joueur, effect, is_by_flipping=True)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response, "You",
            CardFinder(card_type=Event, trait=TRAIT_SONG),
            ranger_dans_la_setlist,
            conditions=[lambda effect, message: SetlistALaPlace(effect)],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction, lever_le_rideau,
            conditions=[lambda effect, message: not AngoisseEnJeu(effect)],
        ).SetTarget("This"),
    ]
```

`AngoisseEnJeu`, condition de la Hero Action de retournement, n'a pas été
expliquée par le coordinateur ni lue par l'agent rédacteur : ne pas
supposer son comportement, à vérifier sur pièce avant de s'appuyer dessus.

**Pièges connus** : « Setlist » n'est pas un texte imprimé verbatim sur les
cartes, contrairement à « Showtime! » qui l'est : c'est le nom donné par le
pack et par le code à la zone `PlaceCardArea` de Live Concert. Ne pas
chercher le mot « Setlist » dans `cards.json` en espérant une
correspondance de texte de carte. La limite de 4 emplacements est une
condition de script (`SetlistALaPlace`), pas une propriété native de la
zone : une carte hypothétique qui poserait directement dans cette zone sans
passer par cette condition ne serait pas bornée par ce mécanisme (aucune
autre carte du pack ne le fait, d'après le fichier central transmis).

**Variantes maison** : aucune connue au 29/08/2026, hors le pack `dazzler`
lui-même.

---

<a id="registered"></a>

## REGISTERED

**Texte imprimé / définition** : pack `iron_patriot` (Neptune, set 142).
Norman Osborn joue avec un SECOND DECK de 20 sbires, le **deck REGISTERED**. Sa
manigance permanente en révèle le dessus ; le sbire entre en jeu **engagé avec
lui**, résout ses effets de révélation, puis le joueur peut dépenser un nombre
de ressources égal à ses **icônes de [boost]** pour en prendre le contrôle et le
traiter comme un **allié REGISTERED**. Insert, mot pour mot :

> « When you reveal a minion from the REGISTERED deck, it enters play as a
> minion first and resolves any revealed effects. After this, you may spend
> resources equal to the number of boost icons on that minion's card to take
> control of it as a REGISTERED ally. If you do not, it remains in play as a
> minion engaged with you. »

⚠ **Ce n'est pas un mot-clé au sens du jeu, c'est un TRAIT** — comme `ELITE`.
Il se déclare dans `traits`, jamais dans `desc`, et le moteur ne lui associe
aucune mécanique native. La fiche existe parce que le pack construit tout un
système autour de lui, et que trois pièges moteur ont coûté une journée.

**Mécanisme moteur** : rien de neuf, tout existait.

| Besoin du pack | Ce qui existe déjà |
|---|---|
| un second deck et sa défausse | `player.additional_deck` / `additional_discard_pile` (`player.py:97`) |
| le remplir au montage | `AbilityFactory.BeginGameWithSetAside` + `WhenPlayerSelectHero` (modèle `09001b` Stephen Strange) |
| révéler le dessus | `Deck.RevealTopCard` → `face.Reveal` (`face_on_event.py:245`) |
| sbire → allié, CTR = MNG imprimée | `Faces.TreatAsAlly` (`faces.py:340`), qui recopie déjà `printed_scheme` dans `printed_thwart` |
| la capacité « Special » | `AbilityFactory.WhenResolveSpecialAbility` pour la déclarer, `face.ResolveSpecialAbility` pour la résoudre |

**Carte exemple** : `ip002a` : * Registration Act, et le helper partagé
`src/cards/pack/iron_patriot/iron_patriot/__init__.py`.

**Pièges connus** — les quatre ont été MESURÉS le 09-10/09/2026 :

1. **`Faces.TreatAsAlly` ÉCHANGE LA FACE, et n'emporte rien avec elle.** Le
   gabarit `registered_ally` n'a aucune capacité et un seul trait. Sans
   correctif, le « Special » qu'on vient de PAYER disparaissait à la seconde
   où on l'obtenait, et Bullseye cessait d'être ASSASSIN. Il faut donc :
   - **recharger le module du sbire** pour obtenir des `Ability` NEUVES —
     celles déjà en place sont liées à leur papier (`face_ability.py:18`) et le
     moteur refuse de les reposer ailleurs (`card.py:316`) ;
   - **recopier les traits imprimés** ;
   - **rallumer les bonus continus** : la famille `WhileValid`
     (`ThisGainKeyword`...) se suspend à `WhenCardEnterPlay` (`on_while.py:177`)
     et n'est jamais calculée si on l'inscrit APRÈS l'entrée en jeu.
   Les mots-clés lus dans `desc` (Garde, Patrouille, Riposte, Vulnérable…), eux,
   tombent avec la face — et c'est voulu : un allié ne garde pas la garde.
2. **Convertir PENDANT le « When Revealed » casse la révélation.** Le sbire
   n'est alors plus engagé, et `minion.py:41` l'exige
   (`assert self.card.world.is_game_over, f"{self.engaged_player=}"`). On se
   pose une fenêtre plus tard, sur `AfterCardRevealedEnd`.
3. **Le prix est en ICÔNES DE BOOST, pas en coût de ressource.** Aucune carte
   qui réduit un coût ne touche le deck REGISTERED ; une carte qui change les
   icônes, si (`ip008` Director of Security). Lire par
   `CountBoostIconsInternal`, jamais `printed_boost`.
4. **La défausse se sépare en deux, contre l'intuition.** Insert : un ALLIÉ
   REGISTERED vaincu part dans la défausse du deck REGISTERED, un SBIRE du deck
   REGISTERED resté sbire part dans la défausse de RENCONTRE. Le test est
   `HasTrait("REGISTERED")` au moment de la défaite.

**Variantes maison** : aucune à ce jour. À ne pas confondre avec le trait
`CONTROLLED` (packs `rogue`, `phoenix`), qui prend aussi le contrôle d'un sbire
mais lui **interdit** d'utiliser ses capacités — l'insert d'Iron Patriot oppose
explicitement les deux.

---

<a id="weakness"></a>

## Weakness (mot-clé maison, ekAugust — aspect Venomized)

**Texte imprimé / définition** : « Weakness. *(Begins the game in your deck and
is discarded into your discard pile.)* »

L'insert du pack **Venomized** la donne en entier :

> **New Keyword: Weakness.** Cards with the "weakness" keyword begin the game
> shuffled into your deck and **do not count toward your deck size**. Cards
> that feature the "weakness" keyword are **encounter cards**, which will have
> a negative effect on your game **when they are drawn into your hand**. They
> can be **discarded like any other card** and they are **discarded into your
> discard pile**.

**Règle de construction de deck** (insert, section « Venomized Weakness Set ») :
après avoir bâti son deck, si l'on y a mis des cartes Venomized *(black)*, on
ajoute au hasard des cartes du set « Venomized Weakness », selon le **coût
total en ressources** de ces cartes Venomized :

| Coût total des cartes Venomized | Cartes Weakness à ajouter |
|---|---|
| 1 à 20 | 1 |
| 21 à 40 | 2 |

Les doublons sont possibles (tirage aléatoire, pas une sélection).

**Mécanisme moteur** : **AUCUN CODE**. C'est le résultat qui compte ici, et il
a été mesuré, pas supposé.

Le mot-clé se ramène à trois faits, dont deux sont natifs :

1. **Une carte de type `Treachery` peut vivre dans le deck du joueur.**
   `PlayerSetup.SelectIdentity` passe la liste `player_deck` telle quelle à
   `CardFactory.GenerateCards` (`player_setup.py:260`) : aucun filtre de type.
2. **Elle se pioche normalement en main**, et son
   `AbilityFactory.AfterCardEnterHand` part. Le déclencheur est celui de
   `bk002` * Sabretooth (pack `blink`), seul autre usage de cette fenêtre au
   dépôt.
3. **Elle se défausse comme n'importe quelle carte en main**, dans la défausse
   **du joueur**, à la fin de la phase du joueur. C'est le comportement natif
   d'une carte du deck joueur : rien à écrire.

> ### ✅ MESURÉ LE 09/09/2026, PAS SUPPOSÉ
>
> Deux cas de `tools/test_capacites.py` montent un deck joueur ne contenant
> que la carte, piochent, et lisent l'état :
>
> - `vz036 Flash Fire — MESURE du mot-cle WEAKNESS` : la carte arrive **en
>   main** et l'identité prend **1 dégât indirect**.
> - `vz037 Sensory Overload` : la carte arrive en main et le complot principal
>   passe de **3 à 4 menaces**.
>
> **Calibrage (§9 de `PROCESSUS-CARTE.md`)** : les deux modules retirés, les
> deux cas tombent — « degats sur 01001b = 0 (attendu 1) » et « menace sur
> 01097b = 3 (attendu 4) ». **2/2 avec, 0/2 sans.**

**Carte exemple** : `vz036` Flash Fire.

```python
def GetAbilities() -> Sequence['Ability']:

    def flash_fire(effect: 'Effect', message: 'Message.AfterCardEnterHand') -> None:
        this = effect.this
        joueur = this.GetControlByOrOwner()
        if not Player.IsType(joueur):
            return
        joueur.GetIdentity().TakeIndirectDamage(this, 1, effect)

    return [
        AbilityFactory.AfterCardEnterHand(
            AbilityType.ForcedResponse,
            "This",
            flash_fire,
        ),
    ]
```

**Pièges connus** :

- ⚠ **`which_card="This"` pose `CanWorkOnlyInHand()` tout seul**
  (`card_move.py`, fin de `AfterCardEnterHand`). L'ajouter à la main branche
  la capacité deux fois.
- ⚠ **« enters your hand » n'est pas « after you draw »** : une carte rendue
  en main par un autre effet déclenche aussi. Leçon déjà écrite dans `bk002`.
- ⚠ **La parenthèse « You may discard this card from your hand at the end of
  the player phase like any other card » ne se code pas.** C'est déjà le
  comportement de toute carte en main. La recoder ajouterait une règle en
  double.
- ⚠ **Ce n'est pas une Obligation.** Une obligation part dans le deck
  **rencontre** et se révèle par la phase du vilain ; une weakness vit dans le
  deck **joueur** et frappe à la pioche. Les deux sont des cartes de rencontre,
  et c'est tout ce qu'elles partagent.
- ✅ **La règle de deck-building EST automatisée** (09/09/2026). Ne plus écrire
  les cartes Weakness à la main dans un `player_deck` : elles y seraient en
  double. C'est le moteur qui les ajoute au montage de la partie.

**Règle de construction, automatisée des deux côtés :**

| Où | Quoi | Verrou |
|---|---|---|
| `PlayerSetup.CartesImposeesParLesAspects` (`src/game/player/element/player_setup.py`) | AJOUTE les cartes au deck, tirage semé, avant le mélange | `tools/test_aspect_determination.py` (bornes 1, 20, 21, 40, au-delà, et le témoin « aucun Venomized ») |
| `cartesImposees` (`public/js/deckbuilder/regles.js`) | ANNONCE le nombre dans l'éditeur | `outils/verifier-regles-deck.mjs` |

⚠ **La table des tranches est écrite DEUX FOIS**, une par côté. Si elle change,
elle change aux deux endroits. C'est précisément pourquoi les deux verrous
existent : la première version JS oubliait de multiplier le coût par le nombre
d'exemplaires, et la seconde tranche n'était jamais atteinte.

⚠ **Le tableau de l'auteur s'arrête à 40.** Au-delà, les deux implémentations
gardent la dernière tranche (2 cartes) plutôt que d'extrapoler « une de plus
par tranche de 20 », qui serait une règle inventée. Un deck de 50 cartes peut
dépasser 40 de coût cumulé : le cas est atteignable, et le choix est figé par
un cas de test pour qu'un changement d'avis soit un geste conscient.

⚠ **Un coût « X » vaut 0** des deux côtés : X se décide en jouant la carte, pas
en construisant le deck, et l'auteur parle du coût imprimé.

⚠ **Le tirage passe par `Random.RandomChoice`**, le générateur semé du moteur,
jamais par `random` : une partie rejouée à la même graine doit tirer les mêmes
faiblesses, sinon les rejeux et le multijoueur divergent. Tirage AVEC remise,
le texte autorisant les doublons.

**Mesure de bout en bout** : deck « Spider-Man (Venomized) », 39 cartes
choisies → `PlayerDeck<41> was created`. Témoin `spider_man`, 40 choisies →
`PlayerDeck<40>`. La règle n'ajoute rien à un deck qui n'emploie pas l'aspect.

**Variantes maison** : aucune à ce jour. Le set « Venomized Weakness » ne
compte que deux cartes, `vz036` Flash Fire et `vz037` Sensory Overload.

---

<a id="showtime"></a>

## Showtime!

**Texte imprimé / définition** : mot-clé maison du pack `dazzler` (héroïne
custom **Dazzler**, contenu de « Lord Havok »), imprimé littéralement comme
titre de seconde capacité sur les événements de trait [[SONG]] du pack,
après leur « Hero Action ». Texte exact transmis pour `dz003` (* A Little
Girl's Dream) : « Hero Action: Reduce the resource cost of the next ally or
event you play this round by 3. Showtime!: Confuse a non-[[ELITE]] enemy. »

**Mécanisme moteur** : composé dans le même fichier central
`Fusion/marvel-lcg-src/src/cards/pack/dazzler/dazzler/__init__.py`, absent
de ce worktree et de l'historique git de ce dépôt (vérifié lors de cette
tâche). Contenu ci-dessous lu directement par l'agent coordinateur dans le
checkout original `/mnt/c/Users/arnau/Desktop/Marvel LCG/` et
transmis verbatim ; non relu de façon
indépendante par l'agent qui rédige cette fiche.

```python
def Showtime(operation: Any) -> 'Ability':
    """La seconde capacite d'un [[SONG]], celle qui n'agit que dans la Setlist.

    Elle n'est jamais declenchee par un message : `jamais` la verrouille, et
    seule `ResoudreShowtime` sait l'atteindre. `NoOutOfPlayLimit` est
    indispensable : la carte vit dans la Setlist, que le moteur ne compte pas
    comme « en jeu ».
    """
    def jamais(effect: 'Effect', message: 'Message2') -> bool:
        return False

    return Ability(
        AbilityType.Special,
        Message.WhenCardRevealed,
        [jamais],
        operation,
    ).SetName(NOM_SHOWTIME).NoOutOfPlayLimit()


def ResoudreShowtime(faces, player, effect) -> int:
    """Resout le « Showtime! » de chaque carte donnee. Rend le nombre resolu."""
    return Faces.ResolveAbility(faces, player, AbilityType.Special, effect)
```

`Showtime(operation)` construit une `Ability` nominalement accrochée au
message `Message.WhenCardRevealed`, mais dont l'unique condition, `jamais`,
renvoie toujours `False` : elle ne peut donc jamais se déclencher d'elle-même
par ce message. Le commentaire de tête du fichier central explique le
choix : le moteur sait déjà résoudre une capacité d'un type donné sur une
autre carte via `Faces.ResolveAbility(faces, player, ability_type, effect)`
(déjà utilisée par des cartes officielles citées dans ce commentaire :
Quatre Cavaliers `45090`, Celestial Tech `45158`) ; il fallait donc un type
de capacité libre, qu'aucune autre carte du jeu n'utilise.
`AbilityType.Special` répond à ce besoin : déclaré, doté de ses flags
(`ui_display_name`, donc son nom s'affiche), absent de `TYPE_PRIORITY` (qui
a un défaut) mais non utilisé par aucune autre carte du jeu selon le même
commentaire, donc réquisitionnable sans modification du moteur commun.
`.NoOutOfPlayLimit()` est nécessaire parce que la carte, une fois dans la
Setlist (zone `PlaceCardArea` de Live Concert, voir `setlist.md`), n'est
plus comptée « en jeu » par le moteur, ce qui bloquerait sinon la
résolution d'une capacité à limite d'utilisation par tour/partie.

`ResoudreShowtime(faces, player, effect)` est l'unique point d'entrée
capable de déclencher effectivement ces capacités : il appelle
`Faces.ResolveAbility(faces, player, AbilityType.Special, effect)` sur la
liste de cartes passée, et rend le nombre de capacités résolues. Le
commentaire de tête du fichier central décrit le point d'appel prévu pour
l'ensemble de la Setlist : la Hero Action de Live Concert retourne la carte
sur sa face Showtime! (`dz017b`), dont le texte imprimé transmis dit
« When Revealed: Resolve the "Showtime!" ability on each card in the
Setlist, in any order. Then, discard all cards from the Setlist. If 4 cards
were discarded this way, you may either... ». Le script `dz017b.py`
lui-même (l'appel effectif attendu, du type
`ResoudreShowtime(Setlist(...), ...)`) ne m'a pas été transmis : seuls le
commentaire de conception du fichier central et le texte imprimé de la
carte confirment ce point d'entrée, pas une lecture directe de
`dz017b.py`. À vérifier sur pièce avant de s'appuyer dessus pour une
fiche future.

**Carte exemple** : `dz003` (* A Little Girl's Dream, Event, trait SONG),
script complet transmis par le coordinateur :

```python
from . import *

def GetAbilities():
    def reve(effect, message):
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        if joueur is None: return
        Worlds.UpdateNextCardPlayCost(
            joueur, -3, effect,
            finder=CardFinder(card_type=Ally | Event),
            in_this="Phase",
        )

    def showtime(effect, message):
        this = effect.this.CastTo(Event)
        Faces.GiveStatus(CiblesShowtime(effect), "Confused", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, reve).SetPlay().SetLabel(),
        Showtime(showtime).SetTarget(Enemy, non_trait="ELITE", canbe_confused=True, range=(0, 1)),
    ]
```

La capacité Showtime! est construite par `Showtime(showtime)`, ciblée sur
un ennemi non-[[ELITE]] confusable (`.SetTarget(Enemy, non_trait="ELITE",
canbe_confused=True, range=(0, 1))`), et son opération applique le statut
Confused via `Faces.GiveStatus(CiblesShowtime(effect), "Confused",
effect)`.

**Pièges connus** : `CiblesShowtime` (helper cité dans le brief de tâche
mais dont le corps ne m'a pas été transmis) existe précisément parce que le
chemin normal du moteur, `CardFace.ResolveAbility` (appelé en interne par
`Faces.ResolveAbility`), prend automatiquement la première cible légale
sans rien demander au joueur : pour une capacité Showtime! avec cible comme
celle de `dz003`, ce comportement par défaut empêcherait un vrai choix.
`CiblesShowtime` sert à forcer ce choix. Toute future carte Showtime! avec
cible doit passer par ce helper plutôt que reconstruire un ciblage manuel,
sous peine de retomber dans ce défaut moteur (ciblage automatique, sans
choix). Deuxième piège : ne pas chercher `AbilityType.Special` en lui
prêtant un sens générique dans le moteur, c'est un type autrement inutilisé
par le jeu, réquisitionné spécifiquement par ce pack pour verrouiller
Showtime! contre tout déclenchement accidentel via
`Message.WhenCardRevealed`. Enfin, le mécanisme d'appel final sur
l'ensemble de la Setlist (`dz017b.py`) n'a pas été lu, seulement inféré du
texte imprimé et du commentaire de conception : à confirmer avant de
documenter le retournement de Live Concert lui-même dans une fiche future.

**Variantes maison** : aucune connue au 29/08/2026, hors le pack `dazzler`
lui-même. `dz003` est la seule carte Showtime! avec ciblage lue en détail ;
le pack en compte d'autres (40 cartes au total d'après la mémoire de
session du projet) qui portent vraisemblablement des opérations
`Showtime()` différentes, non vérifiées ici.

---

<a id="armored"></a>

## Armored (maison, pack `superior_iron_man`)

**Texte imprimé / définition** : « Armored 2. Guard. Patrol. » sur le minion némésis Tony Stark A.I. (si016). Guard et Patrol sont officiels (fiches dédiées). « Armored » n'existe NULLE PART ailleurs : ni dans le moteur, ni sur aucune des 4600+ cartes officielles déjà portées, ni dans le matériel fourni par l'auteur (pas de règles jointes au pack). Ce n'est pas un mot-clé officiel de Marvel Champions : c'est un mot-clé maison de l'auteur (Merlin), non défini.

**Définition** (glossaire fan-made de MC4DB, adoptée le 29/09/2026) :

> « When a character with this keyword would take any amount of damage
> **from an attack**, prevent X of that damage. »

⚠ **Ce qui a changé le 29/09/2026.** L'arbitrage du 29/08/2026 (question posée avant d'écrire le script, carte de référence absente, aucune règle jointe) prévenait 2 dégâts de **chaque** instance, attaque ou non. MC4DB limite aux dégâts **d'une attaque** : une trahison ou une capacité qui blesse ce minion passe en entier. Le script porte désormais `is_from_attack=True`. La carte n'imprime rien qui contredise le glossaire.

**Mécanisme moteur** : pas de clé `desc` dédiée (contrairement à Guard/Patrol/Toughness) — codé directement dans `si016.py` via un Forced Interrupt sur `Message.WhenUnitWouldTakeDamage`, modèle `Armored Rhino Suit` (`core/rhino/01098.py`) :

```python
def armored_2(effect, message):
    message.PreventDamage(2, effect)

AbilityFactory.WhenUnitWouldTakeDamage(
    AbilityType.ForcedInterrupt,
    "This",
    armored_2,
    is_from_attack=True,
)
```

**Carte exemple** : `si016` : Tony Stark A.I., seule carte du jeu à porter ce mot-clé.

**Pièges connus** :
- Ne pas confondre avec Toughness (une seule utilisation puis la carte de statut est défaussée) : Armored se recharge à chaque attaque, sans compteur ni statut.
- **Hors attaque, rien n'est prévenu** : cas « des degats HORS attaque passent en entier » (3 dégâts directs, 3 subis), rouge avec l'ancien script. Il reste vert sous substitution (témoin d'absence d'effet) ; c'est le cas « une ATTAQUE de base du heros ne le blesse pas » qui prouve le module.
- Réservé à cette seule carte : si un autre pack imprime un jour « Armored X », vérifier d'abord si l'interprétation retenue ici convient avant de la recopier telle quelle — ce n'est pas un mot-clé officiel avec une définition stable, juste l'arbitrage pris pour CETTE carte.

**Variantes maison** : aucune autre recensée pour l'instant.

---

<a id="fragile"></a>

## Fragile

**Texte imprimé / définition** : « Fragile. (Attacks against this character
gain overkill.) »

**Mécanisme moteur** : mot-clé maison, déjà défini dans le pack
`determination` (aspect fan-made, `src/cards/pack/determination/__init__.py`,
fonction `Fragile()`) avant même le pack `okoye`. Le crochet lui-même est
**officiel** : la carte 33032 (Marked) fait exactement ceci pour un sbire —
`message.GainOverKill(effect)` sur la fenêtre `WhenUnitWouldAttackUnit`. Il
suffit de changer la cible : `"This"` au lieu du sbire attaché par Marked.

```python
def Fragile() -> 'Ability':
    def fragile(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        message.GainOverKill(effect)

    return AbilityFactory.WhenUnitWouldAttackUnit(
        AbilityType.NonKeyword,
        None,
        "This",
        fragile,
    )
```

Le pack `okoye` réutilise CE mécanisme tel quel (`src/cards/pack/okoye/okoye/__init__.py`,
fonction `Fragile()`), avec une différence : Midnight Angel Armor (ok012/ok013)
retire ce mot-clé au personnage attaché (« loses the fragile keyword »). Le
moteur n'a pas de primitive générique pour désactiver une ability imprimée sur
une AUTRE carte : la condition est donc intégrée directement dans le handler
(pas d'overkill accordé si Midnight Angel Armor est attachée), ce qui produit
le même résultat observable que « perdre Fragile » sans modifier le mécanisme
partagé avec `determination`.

**Carte exemple** : `ok017` (jeton Dora Milaje) et `ok018` (jeton Midnight
Angel), les deux seuls porteurs du mot-clé dans ce pack — `GetAbilities()`
retourne simplement `[Fragile(), Legion()]`.

**Pièges connus** :
- `WhenUnitWouldAttackUnit` (et pas `WhenUnitWouldAttack`) est indispensable :
  la première fenêtre ne contient jamais de cible allié tant que le
  défenseur n'est pas choisi (voir §10 du guide, piège « la fenêtre du
  défenseur »).
- Overkill se réévalue par attaque, pas de façon permanente sur la carte :
  aucun état à nettoyer en fin de partie.

**Variantes maison** : `okoye` ajoute une clause de retrait conditionnelle
(Midnight Angel Armor) qui n'existe pas dans `determination`. Toute nouvelle
carte du pack `okoye` qui retirerait Fragile pour une autre raison devra
étendre cette même condition plutôt que d'écrire un second mécanisme.

---

<a id="legion"></a>

## Legion

**Texte imprimé / définition** : « Legion. (2 allies with the legion keyword
count as 1 ally toward your ally limit.) »

**Mécanisme moteur** : mot-clé maison, introduit par le pack `okoye`. Aucune
primitive « N comptent comme 1 » n'existe dans le moteur : la seule brique
disponible est `Message.CheckIfAllyCountLimit` / `message.SetNotCountAlly()`,
exposée via `AbilityFactory.ThisNotCountAllyLimit` (`friend.py`), qui marque
un allié comme NE COMPTANT JAMAIS (utilisée par `aoa/missions.py` pour un
allié qui échappe totalement à la limite).

`AllyLimit.CheckLimit` (`src/game/player/limit_monitor/ally_limit.py`) envoie
un message `CheckIfAllyCountLimit` à chaque allié en jeu du joueur et somme
ceux qui ne sont pas marqués « not_count » pour obtenir `curr_ally` ; c'est ce
total qui est comparé à `ally_limit`.

Implémentation retenue (`src/cards/pack/okoye/okoye/__init__.py`, fonction
`Legion()`) : classer les alliés portant Legion par ordre de création stable
(`card.object_id`), puis marquer **un allié sur deux** (index impair) comme
« ne comptant pas ». N alliés Legion valent alors `ceil(N/2)` au lieu de N,
ce qui correspond exactement à « 2 comptent comme 1 » (2→1, 3→2, 4→2, 5→3...).

```python
def Legion() -> 'Ability':
    def est_le_second_du_couple(effect, message) -> bool:
        joueur = effect.this.GetControlByPlayer()
        if joueur is None:
            return False
        allies_legion = sorted(
            (a for a in joueur.allies.Get() if EstAllieLegion(a)),
            key=lambda a: a.card.object_id,
        )
        if effect.this not in allies_legion:
            return False
        return allies_legion.index(effect.this) % 2 == 1

    return AbilityFactory.ThisNotCountAllyLimit(conditions=[est_le_second_du_couple])[0]
```

**Carte exemple** : `ok017` (jeton Dora Milaje) et `ok018` (jeton Midnight
Angel), les deux seuls porteurs du mot-clé dans ce pack (les deux « Created
Ally » générés par Adored Ones et Angelic Warfare).

**Pièges connus** :
- Le classement se recalcule à chaque appel (stateless), à partir des alliés
  **actuellement en jeu** du joueur — pas d'état persistant à synchroniser
  quand un allié Legion est défait ou rejoué.
- Edge case connu et non bloquant : `AllyLimit.CheckLimit` envoie aussi le
  message aux `gain_faces` (alliés sur le point d'entrer en jeu, pas encore
  dans `player.allies.Get()`). Pour un tel allié, `effect.this not in
  allies_legion` renvoie `False` tant qu'il n'est pas encore effectivement en
  jeu : il compte normalement au moment précis de la vérification d'entrée,
  avant de rejoindre la paire au recalcul suivant. N'a pas d'effet observable
  différent en pratique (la limite est de toute façon revérifiée après
  l'ajout), mais à garder en tête si un cas de test semble incohérent d'un
  point de vue « avant/après » très précis.
- Ne pas confondre avec `jetons`/`compteurs` (§8 du guide) : Legion ne pose
  aucun jeton, c'est un filtre de comptage pur.

**Variantes maison** : aucune autre carte du pack `okoye` ne porte Legion
que les deux jetons ci-dessus ; toute nouvelle carte Legion future devra
utiliser `EstAllieLegion()` (même fichier) pour rester dans le même groupe de
pairage plutôt que de créer un second groupe indépendant.

---

<a id="plotting"></a>

## Plotting

**Texte imprimé / définition** : « Plotting. (After this minion engages your
identity, it schemes.) »

**Mécanisme moteur** : pas un compteur `desc` (contrairement à
Quickstrike/Incite/Surge) : déclenché par `AbilityFactory.AfterMinionEngagePlayer`
(`src/game/ability/factory/minion.py`) ciblant `"This"` contre `"You"`, qui
appelle `this.CastTo(Minion).BasicSchemes(effect)` — une action SCH de base
contre le complot principal, sans cible explicite à fournir (symétrique de
`BasicAttacks`, voir `can_scheme.py:166`).

**Carte exemple** : `ok021` (`* Malice`, pack `okoye`) porte le même
mécanisme (« Malice schemes » après un déclencheur différent), sans le
nommer par un mot-clé — `this.CastTo(Minion).BasicSchemes(effect)` dans
`src/cards/pack/okoye/okoye_nemesis/ok021.py`.

**Pièges connus** : le trigger est `AfterMinionEngagePlayer`, pas
`AfterMinionEngageYou`/attaque — bien vérifier qu'il se déclenche à
l'engagement, pas à l'activation suivante du sbire.

**Variantes maison** : `ss019` (`* Bella Donna`, pack `scarlet_spider`,
CptScorp) est la première carte à nommer ce mécanisme « Plotting » avec
texte de rappel entre parenthèses, façon mot-clé officiel. `vp015` (`* Guzz`,
pack `venompool`, même auteur) le reprend à l'identique, à un mot près dans
le rappel : « After this minion engages **you**, it schemes » au lieu de
« engages **your identity** ». Même mécanisme, même déclencheur
`AfterMinionEngagePlayer` : la différence est rédactionnelle, pas mécanique.

---

<a id="breakthrough"></a>

## Breakthrough

**Texte imprimé / définition** : « This thwart gains breakthrough. »
Mot-clé MAISON, imprimé dans le pack `viv_vision` (Rainy) sur `vv003` Just a
Phase et **sur aucune autre carte du pack** : le zip ne contient aucun insert
de règles.

**Définition** (glossaire fan-made de MC4DB, adoptée le 29/09/2026) :

> « Excess threat removed from this side scheme is removed from **the main
> scheme**. »

⚠ **Ce qui a changé le 29/09/2026.** La fiche suivait jusque-là la « Marvel
Champions Home Brew Master List » transmise par l'utilisateur le 02/09/2026
(« another eligible target », au choix du joueur), jamais recoupée depuis le
dépôt. MC4DB, seul glossaire public consulté qui définit le mot, impose la
manigance PRINCIPALE. Le script `vv003` ne propose donc plus de choix : l'excès
part sur `Worlds.GetMainSchemes(effect)[0]`. Si la menée visait la principale
elle-même, l'excès est perdu (rien d'autre n'est nommé). La lecture « l'excès
va toujours sur la principale », écartée le 02/09, est donc celle qui vaut.

Exemple : Viv (THW 1) joue Just a Phase, monte à 4 THW et vise une manigance
annexe qui ne porte que 2 menaces. Les 2 menaces partent, la manigance tombe,
et les **2 restantes** partent sur la manigance principale, même si une autre
annexe est en jeu (cas « avec DEUX annexes », rouge avec l'ancien script).

⚠ MC4DB ne parle que de MENACE : le volet « dégâts » de l'ancienne définition
(« this attack gains breakthrough ») n'a de source que la masterlist. Aucune
carte du dépôt ne l'imprime ; s'il en arrive une, la question se repose.

**Mécanisme moteur — volet ATTAQUE** : c'est `overkill`, tel quel. Le moteur
sait déjà le faire, et sa fiche `overkill.md` donne les deux chemins
(`overkill=True` sur la fabrique d'attaque, ou `message.GainOverKill(effect)`
en cours d'attaque pour les textes « this attack gains… »). Une carte qui
imprimerait « this attack gains breakthrough » n'a donc **rien à coder à la
main** : elle se rend par `GainOverKill`. Aucune carte du dépôt n'est dans ce
cas au 02/09/2026 ; `vv003` n'imprime que le volet menée.

**Mécanisme moteur — volet MENÉE** : rien de natif, contrairement à `overkill`.
Le report se calcule à la main sur le message
`Message.AfterUnitThwartScheme`, envoyé juste après `RemoveThreatInternal`
(`src/game/card/face/attribute/can_thwart.py:148-150`), donc **pendant** que
les bonus de menée de la carte sont encore actifs :

- valeur voulue : `message.would_thw_scheme_message.property.GetThwart(unit)`
  (`ThwartProperty.GetThwart`, `can_thwart.py:4`) ;
- valeur réellement retirée : `message.remove_threat` (plafonnée par la menace
  présente sur la manigance) ;
- excès = voulu − retiré, reporté par
  `RemoveThreatFromSchemes` sur une cible choisie via `ChooseAbilities` +
  `ForChoiceAbility(...).SetTarget(Scheme2, exclude=[...], has_threat=True)`.

L'abonnement se pose en `RegisterTemp` depuis l'Interruption de la carte, sur
le modèle de `20013` Making an Entrance qui pose exactement le même genre
d'effet de suite (`AfterUnitThwartAndRemoveLastThreat` + condition
`message in thw_message.would_thw_messages`).

**Carte exemple** : `vv003` (Just a Phase), pack `viv_vision`.

**Pièges connus** :

- **Seule une vraie MENÉE reporte.** Comme `overkill` ne reporte que des dégâts
  d'attaque, le volet menée de `breakthrough` ne reporte que ce qui a été
  retiré PAR une menée (« removed from this side scheme »). Un « remove N threat » qui n'est pas une menée (le Hero
  Action de `vv005` Solar Beam, par exemple) ne reporte jamais rien, même si la
  manigance tombe.
- **Lire l'excès sur `AfterUnitThwartScheme`, pas sur `AfterUnitThwartEnd`.**
  Le bonus de +3 THW est posé par `GainTHWForThisThwart`, qui passe par
  `GainForThisActive` : à la fin de la menée il peut déjà avoir expiré, et
  `property.GetThwart(unit)` rendrait alors la valeur de base. Le message par
  manigance est envoyé DANS la boucle, avant toute expiration.
- **Menée répartie** (`property.is_divided`) : la valeur par manigance vaut 1,
  et le multiplicateur `schemes_dict[target]` ne se lit pas depuis le message.
  Le cas ne se présente pas sur `vv003` (Interruption sur une menée DE BASE,
  donc une seule manigance), mais toute réutilisation du mot-clé sur une carte
  à cibles multiples devra revoir le calcul.
- **Une manigance vaincue disparaît.** Si la menée abat la manigance visée,
  l'excès existe toujours : ne pas conditionner le report à la survie de la
  cible.
- **Pas de choix à proposer.** La cible du report est la principale, imposée :
  un `ChooseAbilities` (ancien montage) ouvrait une question que le glossaire
  ne pose pas.

**Variantes maison** : aucune autre dans le dépôt pour l'instant. La définition
communautaire prévient elle-même que certains auteurs la retouchent pour un
héros donné : si un pack imprime sa propre formulation, c'est elle qui gagne
sur cette fiche, et la fiche se corrige en conséquence.

---

<a id="summon"></a>

## Summon — MOT-CLÉ MAISON

**Texte imprimé / définition** : « **Summon** the Tahlei upgrade and add it to
your hand. », « **Summon** the Yaka Arrow upgrade and add it to your hand. »,
« **Summon** the Sword-Gun-Arm attachment and attach it to Sav'rkk. »,
« Otherwise, **summon** Sav'rkk and reveal him. »

**L'auteur ne le définit JAMAIS.** Le mot apparaît six fois dans le pack
`yondu` (set 154, BLUEHG + DESIGNHACKER) et **nulle part ailleurs dans le
jeu** : aucune carte officielle ne l'imprime, et les deux seules occurrences
du dépôt (`bw019` Rising Tide, `gb010` Necro-Raven) sont du texte
d'ambiance, pas une mécanique.

**Définition** (glossaire fan-made de MC4DB, adoptée le 29/09/2026 ; elle
englobe l'arbitrage du 03/09/2026) :

> « Search the deck, discard pile, or **anywhere in or out of play** for a
> specific card, then shuffle the deck if it was searched in this way. Summon
> predates the official Find keyword, which covers almost the same ground:
> both reach every game area where the named card could be. »

⚠ **Ce qui a changé le 29/09/2026.** L'arbitrage du 03/09/2026 (deck ET
défausse) était un sous-ensemble : les helpers fouillent désormais aussi la
main, la mise de côté et la zone « retiré de la partie » (cas « depuis la zone
RETIREE DE LA PARTIE », rouge avant, côté héros comme côté rencontre). Le
TERRAIN n'est pas fouillé : chaque carte du pack qui convoque une carte
pouvant déjà être en jeu le dit elle-même (« if ... is not in play »), et
`yd004` interdit la duplication en toutes lettres.

**Pourquoi la défausse compte.** Le matériel l'impose : Tahlei
(14/15) et Yaka Arrow (15/15) **sont des cartes du deck de 15**, comptées
comme telles sur la decklist de l'auteur. Restreindre `summon` au seul deck
rendrait une Yaka Arrow défaussée définitivement perdue — or l'obligation
`Banished` la défausse explicitement, et **neuf cartes du pack** ne lisent
qu'elle. Le pack se bloquerait sur son propre texte.

**Mécanisme moteur** : **aucune primitive dédiée, mais rien à inventer** —
c'est `Search.SearchForCards`, qui expose toutes les zones :

```python
faces = Search.SearchForCards(
    effect, joueur,
    include_player_deck=True,
    include_player_discard_pile=True,
    include_player_hand_cards=True,
    include_set_aside=True,
    include_removed_area=True,
    name="Yaka Arrow",
    card_type=Upgrade,
)
if faces and faces[0] not in joueur.hand_cards.Get():
    joueur.GainCard(faces[0], effect)
```

Le « (Shuffle.) » est le comportement PAR DÉFAUT de `Search`, il ne se code
pas. Modèles : `an001b` * Aldrif Odinsdottir, `ok001b` * Okoye, `ls005`
To Arms! (deck + défausse), `mw001b` * Cassandra Webb.

Côté rencontre, `Search.SearchForCards(..., include_encounter_deck=True,
include_encounter_discard_pile=True, include_set_aside=True,
include_removed_area=True)` (`ConvoquerRencontre`, set `yondu_nemesis`) —
modèle `ag013` Hallucination pour le motif « chercher puis attacher ».

**Carte exemple** : `yd001b` * Yondu Udonta — voir le `.py` correspondant, qui
porte le commentaire complet.

**Pièges connus** :

- ⚠ **« Summon … **and add it to your hand** » n'est PAS « put it into play ».**
  La carte va en MAIN et devra être jouée, coût compris. Trois cartes du pack
  l'écrivent ainsi ; `yd015` Sav'rkk et `yd016` Sword-Gun-Arm, elles, disent
  « and reveal him » / « and attach it », donc directement en jeu. Lire le
  verbe qui suit, jamais le seul mot `summon`.
- ⚠ **Ne pas oublier la défausse.** C'est la moitié de la définition, et
  celle sans laquelle le pack se bloque. Un cas de test qui ne monte que le
  deck passera au vert dans les deux montages : le contre-cas obligatoire
  place la carte cherchée **dans la défausse**.
- ⚠ **Si la carte est déjà en jeu, `summon` ne doit rien faire.** `yd004`
  Whistle While You Work l'écrit noir sur blanc (« If the Yaka Arrow upgrade
  is **not in play**, summon it … **instead** »), et les autres cartes le
  supposent. Chercher une carte déjà sur le terrain la dupliquerait.

**Variantes maison** : aucune autre à ce jour. La définition ci-dessus est
celle du glossaire MC4DB ; un futur pack qui imprimerait sa propre parenthèse
l'emporterait sur elle (texte imprimé > MC4DB > fiche).

---

<a id="multiverse"></a>

## Multiverse

**Texte imprimé / définition** : le mot `Multiverse.` apparaît seul, en tête du
bloc de texte d'un **allié signature**, sans aucune parenthèse explicative.
Aucun des trois packs qui l'emploient ne le définit.

**Définition retenue** (glossaire fan-made de MC4DB, adoptée le 29/09/2026 ;
elle remplace l'arbitrage du 05/09/2026) :

> « Identity-specific cards with the multiverse keyword are optional
> **replacements** for the given card of the corresponding card number.
> During deckbuilding, you may choose to replace the identity-specific card
> sharing its card number with an identity-specific card with the multiverse
> keyword. Doing so satisfies your deckbuilding requirements. During a
> campaign, this choice cannot be unmade. »

Autrement dit : une carte Multiverse est **une autre version d'un numéro de
set déjà occupé**. Au deckbuilding, le joueur prend **l'une OU l'autre**,
jamais les deux. Choisir la version Multiverse satisfait l'obligation
d'emporter les cartes signature. En campagne, on ne revient pas dessus.

⚠ **Ce qui a changé le 29/09/2026.** La fiche disait jusque-là que le mot-clé
« n'interdit pas de les mettre toutes les deux dans le deck, seulement d'en
avoir deux en jeu ». C'était faux : trois decks de départ emportaient les deux
versions (16 signatures pour 15 numéros). Ils ne gardent plus que l'originale.

Les paires du dépôt, déclarées par la clé **`multiverse_of`** de `cards.json`
sur la carte Multiverse (même nom de clé que MC4DB) :

| Carte Multiverse | Remplace (même numéro de set) | Pack |
|---|---|---|
| `ra002` `* Odinson` | `ra003` `* Roz Solomon` | `rainy` (Thor, Jane Foster) |
| `bc003` `* Spider-Man` (AVENGER) | `bc002` `* Spider-Man` (SYMBIOTE, WEB-WARRIOR) | `blackcat` |
| `bw003` `* Ironheart` | `bw002` `* Silk` | `brawn` |

⚠ La paire `brawn` est **déduite**, pas lue : l'auteur n'imprime pas les
numéros dans `cards.json`, et le deck de départ de l'auteur emporte Silk sans
Ironheart. Les deux autres paires viennent des noms de fichiers du zip
(« 1 Spider-Man (black) / (red) ») et du deck de Rainy (16 entrées).

**Mécanisme moteur** : **AUCUN, zéro ligne de code**, comme avant. Le
remplacement est une règle de DECKBUILDING : elle vit dans les decks de départ
(une seule version) et dans l'éditeur, `validerDeck` de
`public/js/deckbuilder/regles.js`, qui refuse un deck contenant une carte
Multiverse ET la carte que désigne son `multiverse_of` (signatures du héros
comprises, donc aussi pour Stan Lee). Verrou :
`outils/verifier-regles-deck.mjs` (quatre cas). `PlayerSetup` n'a rien à
vérifier : un deck de départ ne porte plus qu'une version, et l'unicité native
(l'étoile `*`) reste le filet en jeu.

**Carte exemple** : `ra002` `* Odinson`. Son module ne fait rien pour le
mot-clé ; le commentaire qu'il porte sur « une seule version par deck » est
désormais exact au sens strict.

**Pièges connus** :

- ⚠ **`MULTIVERSE` est aussi un TRAIT**, et les deux notions n'ont rien à voir.
  `wd029` Multiverse Recruit (pack `web_of_deceit`) porte
  `"traits": ["MULTIVERSE"]` ; Blink (Earth-295) emploie le même mot comme
  trait. Un trait va dans `traits`, ce mot-clé-ci va dans `multiverse_of`.
- ⚠ **Ne pas croire que les deux versions sont deux illustrations d'une même
  carte.** `bc002` et `bc003` ont des statistiques, des traits et des
  capacités DIFFÉRENTS : ce sont deux `card_id` distincts qui se disputent un
  numéro.
- ⚠ **Un nouveau pack qui imprime `Multiverse`** doit recevoir sa clé
  `multiverse_of`, sans quoi l'éditeur laissera passer les deux versions.
- ⚠ **Campagne** : « this choice cannot be unmade » n'est appliqué nulle part
  (le carnet de campagne ne mémorise pas le choix). Écart connu, sans cas.

**Variantes maison** : aucune. Trois packs, trois auteurs (`rainy`, `brawn`,
`blackcat`), même écriture nue et même absence de définition.

---

<a id="agile"></a>

## Agile X — MOT-CLÉ MAISON

**Texte imprimé / définition** : « gains agile 1 *(reduce damage from attacks
with boost cards by 1)*. » Le personnage qui porte Agile X subit X dégâts de
moins de la part d'une attaque **accompagnée d'au moins une carte de boost**.
La parenthèse est imprimée sur la carte elle-même : la définition vient de
l'auteur, elle n'a rien été arbitrée.

⚠ **Divergence assumée avec le glossaire MC4DB (29/09/2026).** MC4DB définit
Agile X ainsi : « Reduce damage taken from **undefended** villain and
**villainous** minion attacks by X (default is 1) ». La carte, elle, imprime
sa propre parenthèse (« attacks with boost cards »), et la règle de priorité
fixée par l'utilisateur est : texte imprimé > MC4DB > fiche. On garde donc le
texte de DESIGNHACKER. Différences concrètes : MC4DB ne réduirait pas une
attaque DÉFENDUE, et ne réduirait que les attaques du vilain et des sbires
Villainous ; la carte réduit toute attaque à cartes de boost, défendue ou non.
Un futur pack qui imprimerait « agile » NU (sans parenthèse) suivrait MC4DB.

**Origine** : `nt003a` Battle Board, face `VEHICLE` (pack maison
`night_thrasher`, set 153, auteur DESIGNHACKER). Premier et seul porteur
connu au 03/09/2026.

**Ce que le mot-clé vise vraiment** : les attaques d'**activation d'ennemi**.
Une attaque de vilain ou de sbire reçoit toujours des cartes de boost ; une
attaque portée par un effet de carte (une traîtrise, une capacité) n'en reçoit
aucune. Agile ne protège donc que de la phase du vilain, jamais d'un effet
ponctuel — c'est ce qui l'empêche d'être une réduction de dégâts générale.

**Mécanisme moteur** : **aucune primitive native, il faut le scripter.**
Le moteur ne conserve la liste des cartes de boost d'une attaque que dans les
messages d'APRÈS-COUP : `Message.AfterUnitAttackUnit.boost_faces`
(`sender_damage.py:510`) et `AfterEnemyActivationEnd.HasThisBoost`
(`sender_enemy.py:149`). Au moment où les dégâts tomberaient — la seule
fenêtre où l'on peut encore les réduire — les cartes de boost ont déjà été
défaussées à l'étape (d) de `can_boost.py`.

Le montage retenu inverse donc la lecture : au lieu de demander « cette
attaque avait-elle des cartes de boost ? », on s'accroche au moment où **une
carte de boost est retournée face visible pendant une attaque**, et on
enregistre à cet instant une réduction TEMPORAIRE bornée à cette attaque.

```python
AbilityFactory.WhenBoostCardTurnedFaceUp(
    AbilityType.NonKeyword,
    None,
    poser_la_reduction,
    while_attack=True,
)
```

puis, dans l'opération, un `RegisterTemp` d'un
`ReduceCharacterTakeDamageBy(<porteur>, X)` lié à l'attaque en cours
(`is_from_attack=message.would_message`), avec un garde-fou pour ne
l'enregistrer qu'une fois par attaque : une activation retourne plusieurs
cartes de boost, et sans ce garde-fou la réduction se cumulerait autant de
fois qu'il y a de cartes.

**Carte exemple** : `nt003a` Battle Board (face `VEHICLE`) — voir le
`.py` correspondant, qui porte le commentaire complet du montage.

**Pièges connus** :

- ⚠ **Ne pas le rendre par un `ReduceCharacterTakeDamageBy` permanent.** Ce
  serait une réduction de TOUS les dégâts d'attaque, boost ou pas : la carte
  deviendrait deux fois meilleure qu'imprimée, et rien dans les tests ne le
  verrait — un cas qui compte les dégâts d'une attaque de vilain passe au vert
  dans les deux montages, puisqu'une attaque de vilain a toujours du boost.
  **Le contre-cas obligatoire est une attaque SANS carte de boost** (dégâts
  infligés par un effet de carte), où la réduction ne doit PAS s'appliquer.
  ⚠ **Et le harnais ne sait pas en produire** : une activation d'ennemi reçoit
  toujours des cartes de boost. Le contre-cas réellement monté (`nt003a`,
  « agile ne touche PAS aux dégâts hors attaque ») passe donc par des dégâts
  qui ne viennent d'aucune attaque — il prouve que la réduction n'est pas
  permanente, mais il reste vert sous substitution. C'est la seule gate du
  pack `night_thrasher` restée entrouverte, et elle est signalée comme telle
  dans son journal de portage.
- ⚠ **Une carte de boost par attaque ne suffit pas à borner la réduction** :
  le message est envoyé pour CHAQUE carte retournée. Sans garde-fou, une
  activation à trois cartes de boost réduirait de 3.
- ⚠ Agile réduit les DÉGÂTS, pas les icônes de boost. Ne pas le confondre avec
  `as015` Scarlet Spider (pack `armored_spidey`), qui réduit le nombre
  d'icônes : l'un agit sur ce que l'attaque inflige, l'autre sur ce qu'elle
  vaut.
- ⚠ Comme tout mot-clé chiffré, la valeur se réinitialise à chaque reset des
  mots-clés : elle doit être donnée par une capacité continue, pas posée une
  fois pour toutes.

**Variantes maison** : aucune autre à ce jour. À relire si un futur pack
imprime « agile » sans la parenthèse explicative — la définition ci-dessus
vient de la carte de DESIGNHACKER, pas d'une règle officielle.

---

<a id="reckless"></a>

## Reckless (mot-clé maison, aspect Determination)

**Texte imprimé / définition** : « Reckless. *(After this character enters
play, place 1 threat on each scheme.)* » (rappel imprimé sur `dt001`, `dt092`
et `dt100` ; `dt099` porte le mot nu).

Définition MC4DB (règle `fanmade`, `rules?locale=en`, 29/09/2026) : « When
this character enters play, place 1 threat on each scheme in play. » Même
mécanique ; seule la fenêtre diffère en mots (« when » contre « after »),
sans effet observable : le moteur n'offre qu'`AfterCardEnterPlay` pour ce
moment, et rien ne s'intercale entre l'entrée en jeu et la menace posée.

**Mécanisme moteur** : aucun crochet natif. Le mot-clé est une aptitude
écrite UNE fois, `Reckless()` dans
`src/cards/pack/determination/__init__.py`, et posée par chaque carte qui le
porte (`Reckless()` en tête de sa liste d'aptitudes) :

```python
def Reckless() -> 'Ability':
    def reckless(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        this.PlaceThreatOnSchemes("EachScheme", 1, effect)

    return AbilityFactory.AfterCardEnterPlay(
        AbilityType.ForcedResponse,
        "This",
        reckless
    )
```

`"EachScheme"` couvre la manigance principale ET toutes les annexes en jeu,
ce que disent les deux définitions (« each scheme », « each scheme in play »).

**Carte exemple** : `dt001` * Cable : `return [Reckless(), ...]`, puis son
Interrupt d'attaque. Autres porteurs : `dt092` * X-23, `dt099` * Marrow,
`dt100` * Archangel (qui cumule Alias et Retaliate 2).

**Pièges connus** :
- `CastTo(Ally)` : les quatre porteurs sont des alliés. Un futur porteur
  d'un autre type (soutien-personnage, héros) devra passer par
  `CastTo(Unit)` ou équivalent, sinon l'aptitude tombe.
- Le mot-clé n'est PAS lu dans `desc` (aucune clé `Reckless` dans
  `cards.json`) : une carte qui l'imprime sans appeler `Reckless()` est
  inerte. Vérifier le `.py` à chaque nouvelle carte, `verifier_desc_mots_cles`
  ne le voit pas.
- Réponse forcée : le joueur ne choisit ni de l'ignorer ni l'ordre avec une
  autre « after enters play » de la même carte (ex. `dt100` n'en a pas,
  `dt105` Venompool n'est pas Reckless). Aucun cas de conflit aujourd'hui.

**Variantes maison** : aucune. Le mot n'existe pas dans le jeu officiel ;
« Reckless Aggression » (`server_get.py`) est un nom de paquet d'aspect
préfait, sans rapport.

---

<a id="alias"></a>

## Alias (mot-clé maison, aspect Determination)

**Texte imprimé / définition** : « Alias. *(If you control a card with a
matching subtitle, discard it and play this card for free.)* » (rappel
imprimé sur `dt100` ; `dt105`, `dt106`, `dt107` portent le mot nu).

Définition MC4DB (règle `fanmade`, 29/09/2026) : « If you control a card
with a matching subtitle, discard it and play this card for free. Ignore
Unique Rule when deckbuilding. » Première phrase identique. La seconde n'a
pas d'équivalent chez nous, voir « Pièges connus ».

**Mécanisme moteur** : aucun crochet natif. Deux aptitudes écrites UNE fois,
`Alias()` dans `src/cards/pack/determination/__init__.py`, posées par
`*Alias()` dans chaque carte qui le porte :

- `AbilityFactory.ReduceCostToPlayThis(lambda effect: effect.this.printed_cost,
  conditions=[controle_un_homonyme])` : le coût tombe à zéro tant que le
  joueur contrôle une AUTRE carte dont `paper.subtitle` est égal au sien ;
- `AbilityFactory.AfterCardEnterPlay(AbilityType.ForcedResponse, "This",
  defausser_l_homonyme)` : à l'entrée en jeu, le premier homonyme contrôlé
  est défaussé (`Faces.DiscardAll(homonymes[:1], effect)`).

Les deux sont liées par le texte (« on joue gratuitement PARCE QU'on
défausse ») mais indépendantes dans le code : si l'homonyme quitte le jeu
entre le paiement et l'entrée en jeu, la carte est quand même gratuite.

**Carte exemple** : `dt100` * Archangel : `return [Reckless(), *Alias(),
...]`. Autres porteurs : `dt105` * Venompool, `dt106` * Captain Universe,
`dt107` * Zenpool.

**Pièges connus** :
- ⚠ **DEUX DÉFAUTS L'ONT RENDU INERTE JUSQU'AU 29/09/2026**, corrigés le
  même jour (gabarit
  `.planning/todos/2026-09-29-fleeting-alias-gabarits-processus-carte.md`) :
  1. les quatre porteurs avaient un `subtitle` VIDE dans `cards.json`, et les
     deux aptitudes rendent la main dès que le sous-titre est vide. Les
     sous-titres imprimés, lus sur les scans : Archangel = « Warren
     Worthington III » (homonymes `33019`, `41003` Angel) ; Venompool,
     Captain Universe (version Deadpool) et Zenpool = « Wade Wilson »
     (homonymes `40024`, `dt016` Deadpool) ;
  2. `ReduceCostToPlayThis(lambda effect: effect.this.printed_cost)` rendait
     l'objet `Cost` : la fabrique multiplie (`base_val * fn(effect)`), d'où
     un `TypeError` avalé par le moteur, visible seulement dans
     `/tmp/capacites_*.log`. Il faut `.val`. Une réduction de coût qui « ne
     part jamais » sans message : lire ce journal avant de chercher ailleurs.
  Preuve : cinq cas `[dt]` de `tools/test_capacites.py` (quatre sujets + un
  témoin sans homonyme), rouges avant, verts après.
- « Ignore Unique Rule when deckbuilding » (MC4DB) : la règle d'unicité
  officielle ne s'applique qu'EN JEU (deux cartes uniques de même nom), pas
  au deckbuilding, et Archangel/Angel, Zenpool/Deadpool n'ont pas le même
  nom. L'éditeur (`public/js/deckbuilder/regles.js`) ne connaît d'ailleurs
  aucune règle d'unicité : il ne plafonne que le nombre d'exemplaires par
  titre (`maxParDeck`). Rien à respecter, rien à corriger.
- Le mot-clé n'est pas lu dans `desc` : une carte qui l'imprime sans
  `*Alias()` est inerte, et `verifier_desc_mots_cles` ne le voit pas.

**Variantes maison** : aucune. « Alias » est aussi un mot du jeu officiel
(l'ALIAS d'une identité, en règle) : ne pas confondre, ce mot-clé-ci ne
parle que du sous-titre imprimé sous le nom d'un allié.

---

<a id="fleeting"></a>

## Fleeting (mot-clé maison, aspect Determination)

**Texte imprimé / définition** : « Fleeting. *(This card must be discarded
from play at the end of the phase.)* » (`dt087` "Get 'Em, Boom-Boom!", seul
porteur du dépôt).

Définition MC4DB (règle `fanmade`, 29/09/2026) : « After the phase ends,
discard this card. » Même sens.

**Mécanisme moteur** : aucun crochet natif, le moteur ne lit aucun mot-clé
dans le texte. Aptitude écrite UNE fois, `Fleeting()` dans
`src/cards/pack/determination/__init__.py` (depuis le 29/09/2026 ; avant
cela le mot-clé n'était implémenté nulle part et `dt087` restait attachée
jusqu'à la défaite de l'ennemi) :

- `AbilityFactory.WhenPhaseEnd(AbilityType.ForcedResponse, None,
  DiscardThisCard, conditions=[en_jeu])` : `phase_name=None` = la PREMIÈRE
  fin de phase qui suit l'entrée en jeu, quelle que soit la phase ; la
  condition `IsInPlay()` évite de défausser une carte encore en main.
- La défausse passe par `Faces.DiscardAll`, donc par la fenêtre
  `WhenCardWouldDiscard` (`card.py:635`) : l'Interrupt de départ de `dt087`
  part bien au moment où Fleeting la défausse.

Modèle : `44032` The Merc with the Mouth (`WhenPlayerPhaseEnd` +
`DiscardThisCard`). Preuve : cas `dt087 ... [dt] — Fleeting` de
`tools/test_capacites.py` (vérificateur `dt087_fleeting_fin_de_phase`, qui
envoie lui-même `Message.WhenPhaseEnd`, l'API Puzzle n'avançant aucune
phase), vu rouge puis vert ; gabarit dans
`.planning/todos/2026-09-29-fleeting-alias-gabarits-processus-carte.md`.

**Carte exemple** : `dt087` "Get 'Em, Boom-Boom!" : `Fleeting()` +
`AfterUnitTookDamage` (Hero Response, s'attache à un ennemi) +
`WhenCardWouldDiscard` (1 dégât à chaque ennemi).

**Pièges connus** :
- « At the end of the phase » : la phase où la carte est ENTRÉE en jeu
  (elle arrive en phase vilain, après des dégâts subis), pas la fin du round.
  Un montage sur `AfterRoundEnd` serait faux.
- La carte n'a pas de mise en jeu ordinaire (pas de `CanPlayThisUpgradeCard`,
  voir son commentaire) : l'aptitude Fleeting ne doit pas en ajouter une.

**Variantes maison** : aucune ; mot-clé absent du jeu officiel.

---

