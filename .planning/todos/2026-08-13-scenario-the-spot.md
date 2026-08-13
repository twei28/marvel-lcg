# TODO / SPEC — Le scénario « The Spot » (fan-made, DesignHacker)

**Statut :** relevé COMMENCÉ le 13/08/2026 — 7 cartes sur 25 lues.
🚧 **Le mot-clé `ThreatLevel` existe maintenant dans le moteur** (§8), sur
décision de l'utilisateur (« pour de vrai, pas approximé »). Aucune carte du set
n'est encore entrée dans le jeu.
**Origine :** demande utilisateur (« un scénario complet d'abord »), pour éprouver
la chaîne d'import de contenu fan-made avant de s'attaquer à une campagne.
**Source :** `THE SPOT (3.0)-20260813T091111Z-1-001.zip`, à la racine du dossier
projet, téléchargé le 13/08. 37 Mo.
**Prérequis :** `2026-08-12-nommage-contenu-fanmade.md` (le préfixe de 2 lettres).

---

## 1. L'inventaire, compté et non supposé

29 fichiers, dont 2 encarts de boîte. **25 cartes**, numérotées 1 à 25 par le
pack lui-même, plus 2 dos de cartes recto-verso.

⚠️ **Les 29 images sont TOUTES distinctes** (contrôle md5). Les cartes qui
partagent un nom — « …Comes Around! » ×3, « Distributed Presence » ×3,
« Oddballs » ×2, « Target Spotted » ×2 — ne sont donc PAS des exemplaires d'une
même carte : ce sont des cartes différentes, ou la même avec des illustrations
différentes. **Impossible de trancher sans les lire.** C'est exactement le genre
de supposition qui coûte un lot entier.

Les fichiers sont **nommés**, donc les titres sont connus sans déchiffrage. Les
images font 1488 × 2079 (portrait) ou 2079 × 1488 (paysage), ~1,2 Mo chacune ;
le jeu range ses illustrations en **300 × 435 / 435 × 300**, ~25 Ko. Un
redimensionnement à l'import est donc obligatoire (dette du 12/08).

## 2. Le nommage retenu

Préfixe **`sp`**, libre (les 20 préfixes déclarés sont `ab ag ah av bw cd dt gp
ht iw jj lj mf mk mw ra sg sr th vr`). Numéro de set **119**, premier libre après
118 (Determination). Code de scénario `the_spot`.

Le préfixe se déclare dans `tools/prefixes_fanmade.json` **au moment où les
premières cartes entrent**, pas avant : un vérificateur qui naît rouge n'apprend
qu'à ignorer le rouge.

## 3. LE RELEVÉ (7 cartes sur 25, lues en pleine page)

### 1A — Heightened Threat (MainScheme)

> **Contents**: The Spot I & II *(The Spot III & IV for expert mode)*, The Spot
> and Standard encounter sets. One modular encounter set *(recommended: Sinister
> Syndicate)*.
> **Setup**: Find the What Goes Around… environment and put side A into play
> *(side B instead for expert mode)*. The first player seeks a Spot card with the
> Threat Level keyword and reveals it. Shuffle.

### 1B — Heightened Threat (MainScheme, 12 menaces par joueur, +1 par joueur)

> **Forced Interrupt**: When you would remove any amount of threat from here or a
> Spot side scheme, move that threat to the card with the highest Threat Level
> instead. *(Threat Level is the number in the red icon. If the side scheme you
> removed threat from has the highest Threat Level number in play, remove that
> threat.)*
> **If this stage is completed, the players lose the game.**

### 2 à 5 — The Spot (Villain, 4 stades)

Traits **CRIMINAL. SCIENTIST.** Tous portent, en première ligne :
« Threat Level 1. Characters may thwart against The Spot. »

| # | Stade | PV | SCH | ATK | Le reste du texte |
|---|---|----|-----|-----|---|
| 2 | I   | 12 | 1 | 1 | Hinder 1. Retaliate 1 par tranche de 5 menaces ici, max **3**. |
| 3 | II  | 15 | 2 | 2 | Hinder 3. **Steady**. Retaliate 1 par 5 menaces ici, max **3**. |
| 4 | III | 18 | 1 | 2 | Hinder 3. Retaliate 1 par 5 menaces ici, max **4**. |
| 5 | IV  | 20 | 2 | 3 | Hinder 5. **Stalwart**. Retaliate 1 par 5 menaces ici, max **4**. |

⚠️ Les PV sont **par joueur** (icône joueur), comme d'habitude.

### 6A / 6B — What Goes Around… (Environment, recto-verso)

**6A, mode standard :**
> **Forced Interrupt**: When a card that belongs to The Spot encounter set (ie. a
> « Spot card ») is revealed, place 1 threat on the main scheme.
> **Hero Action**: Discard a card from hand → move up to 3 threat from one Spot
> card with the Threat Level keyword to a different Spot card with the Threat
> Level keyword.

**6B, mode expert :**
> **Forced Interrupt**: When a Spot card is revealed **or turned faceup as a boost
> card**, place 1 threat on the main scheme *(limit 1 threat per Spot card per
> phase)*.
> **Hero Action** : identique à 6A.

## 4. CE QUE LE MOTEUR N'A PAS, mesuré

Le scénario entier repose sur un mot-clé neuf. Trois constats, chacun vérifié
dans les sources :

1. **`ThreatLevel` n'existe nulle part** : `grep -rn "ThreatLevel\|Threat Level\|
   threat_level" src/` rend **zéro**. C'est un mot-clé à créer, avec son icône
   rouge, sa valeur par carte, et la comparaison « la plus haute en jeu ».
2. **La menace appartient aux MANIGANCES.** `PlaceThreatInternal` vit sur
   `Scheme` (`card/face/base/scheme.py`), et `PlaceThreatOnSchemes` n'accepte que
   des manigances. Or ici **le vilain porte de la menace** (« 5 threat here » sur
   The Spot) et **on peut manigancer contre lui** (« Characters may thwart against
   The Spot »). `ThwartInternal` prend `schemes: List['Scheme2']` : un vilain n'en
   est pas un.
3. **La brèche existe pourtant** : `can_hinder.py:58` pose déjà des jetons nommés
   `'threat'` sur une carte quelconque via `PlaceTokensInternal`, et
   `GetCounters('threat')` sait les relire. C'est par là qu'une approximation
   passerait, si approximation il doit y avoir.

**Ce qui est vert, en revanche** : `Hinder`, `Steady`, `Stalwart`, `Retaliate`
sont des attributs de `desc` que le moteur connaît déjà, et le type
`Environment` existe avec sa zone de jeu.

## 5. À TRANCHER AVANT D'ÉCRIRE UNE CARTE

**Le mot-clé Threat Level est-il implémenté pour de vrai, ou approximé ?** Les
deux chemins mènent à des travaux très différents :

* **Pour de vrai** : un attribut de `desc` (`ThreatLevel`), la menace autorisée
  sur un vilain, le maniganceage contre un vilain, et le déroutement de menace du
  complot principal vers la carte au plus haut niveau. C'est du MOTEUR, pas du
  contenu — l'inverse de ce qu'un import fan-made est censé être.
* **Approximé** : compteurs `'threat'` posés à la main par les modules, et l'écart
  écrit dans le code comme pour Red Dagger ou In the Wings. Le scénario se joue,
  mais sa mécanique centrale est déformée.

## 6. CE QUI RESTE À LIRE (18 cartes)

7 · Rocket Racer — 8 · Puma — 9 · Anywhere and Everywhere — 10 · Chameleon —
11 · Penchant for Pilfery — 12 · Living Laser — 13 · Spotty Pasts —
14 · Warp Hole — 15 · The Hypernova — 16, 17, 18 · …Comes Around! —
19, 20, 21 · Distributed Presence — 22, 23 · Oddballs — 24, 25 · Target Spotted.

Copies lisibles (900 px) déjà préparées : elles se refabriquent en une commande
depuis le zip, voir le journal de session.

## 7. Comment on saura que c'est fait

Le scénario apparaît dans l'écran de préparation, ses 25 cartes se génèrent, une
partie est menée de bout en bout par `autoplay.py` sans réponse illégale, et la
mécanique du Threat Level fait en jeu ce que le texte annonce — mesuré, pas
déduit, comme pour Merc Squad.


---

## 8. LE MOT-CLÉ EXISTE (13/08/2026)

Décision de l'utilisateur : **implémenté pour de vrai**, pas approximé.

**Premier morceau, livré** : `HasThreatLevel`, écrit sur le patron exact de
`HasHinder`, l'autre mot-clé chiffré du jeu. Une différence, écrite dans le
code : `Hinder` POSE des jetons quand la carte entre en jeu, `ThreatLevel` ne
pose rien — c'est un nombre qui sert à comparer des cartes entre elles. D'où
`HasAttribute` seul, sans `CanPlaceToken`.

`"ThreatLevel"` est déclaré parmi les clés de `desc` connues, et **`Villain` le
porte**. ⚠️ Il n'est posé QUE sur le vilain : les 4 stades de The Spot le portent,
c'est mesuré. Les manigances annexes le portent probablement aussi, mais elles
n'ont pas encore été lues, **et on n'ajoute pas un attribut à une classe de base
sur une supposition** — surtout pas à `Scheme2`, qui toucherait toutes les
manigances du jeu.

**Prouvé par substitution** (`tools/sonde_threat_level.py`) : le MÊME vilain
officiel rend `printed_threat_level = 0` sans le mot-clé et `2` avec. Sans le
témoin dans la même mesure, une sonde qui rend 0 partout ne se distingue pas
d'une sonde cassée. `test_cards` reste à 4331 ok / 0 erreur, et une partie
ordinaire rend le même résultat qu'avant.

⚠️ La sonde lit la valeur **imprimée**. Le mot-clé calculé (`threat_level`)
demande une carte EN JEU : une face fabriquée seule n'a pas de `card`, et y
toucher fait tomber `GetBuff`.

### Ce qui reste au moteur, mesuré et non deviné

1. **La menace sur un vilain.** `CanHinder` n'est PAS sur `Villain`, seulement sur
   `Scheme2` et `Obligation`. Or les 4 stades de The Spot portent `Hinder 1/3/5`,
   et leur texte lit « 5 threat here ». Mettre `Hinder` dans le `desc` d'un vilain
   aujourd'hui **empêcherait la carte de se générer** (la leçon du 13/08 sur les
   attributs de `desc` réservés à certains types).
2. **Manigancer contre un vilain.** `ThwartInternal` prend `schemes:
   List['Scheme2']` ; un vilain n'en est pas un. « Characters may thwart against
   The Spot » n'a donc aucun crochet.
3. **Le déroutement de menace** du complot principal vers la carte au plus haut
   Threat Level. C'est du texte de carte (1B), mais il lui faut deux crochets :
   une fenêtre « quand on retirerait de la menace d'ici » et une opération
   « déplacer de la menace d'une carte à une autre ».
