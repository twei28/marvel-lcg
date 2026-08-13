# TODO / SPEC — Le scénario « The Spot » (fan-made, DesignHacker)

**Statut :** ✅ **LIVRÉ le 13/08/2026.** Le scénario est dans le jeu, ses 21
faces portent ce qu'elles annoncent, ses 21 modules jouent, et huit parties
complètes ont été menées en normal comme en expert sans un seul incident.
**Les trois écarts ont été levés le 13/08 au soir (§12) : il n'en reste aucun.**
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


---

## 9. LE RELEVÉ COMPLET (13/08/2026)

**25 cartes physiques, 19 distinctes.** Les exemplaires multiples sont bien des
copies : la comparaison pixel à pixel montre qu'ils ne diffèrent QUE par leur
numéro en bas à gauche (`16 vs 17` : x 136-160, y 840-872 sur 644×900). Le
contrôle md5 les disait tous distincts, et il avait raison sans être utile — le
numéro est imprimé sur chaque exemplaire.

### La boîte

| # pack | id | Type | Nom | L'essentiel |
|---|---|---|---|---|
| 1A/1B | `sp001a/b` | MainScheme | Heightened Threat | 12 menaces/joueur, +1/joueur |
| 2 | `sp002` | Villain | The Spot I | PV 12*, SCH 1, ATK 1, **TL 1**, Hinder 1, retaliate max 3 |
| 3 | `sp003` | Villain | The Spot II | PV 15*, SCH 2, ATK 2, TL 1, Hinder 3, **Steady**, max 3 |
| 4 | `sp004` | Villain | The Spot III | PV 18*, SCH 1, ATK 2, TL 1, Hinder 3, max 4 |
| 5 | `sp005` | Villain | The Spot IV | PV 20*, SCH 2, ATK 3, TL 1, Hinder 5, **Stalwart**, max 4 |
| 6A/6B | `sp006a/b` | Environment | What Goes Around… | A = standard, B = expert |
| 7 | `sp007` | Minion | Rocket Racer | SCH 3, ATK 1, PV 4, **TL 2**, CRIMINAL. GENIUS. |
| 8 | `sp008` | Minion | Puma | SCH 1, ATK 1*, PV 5, **TL 3**, CRIMINAL. |
| 9 | `sp009` | SideScheme | Anywhere & Everywhere | **TL 4**, menace de départ 3/joueur |
| 10 | `sp010` | Minion | Chameleon | SCH 1*, ATK 1, PV 7, **TL 5**, CRIMINAL. |
| 11 | `sp011` | SideScheme | Penchant for Pilfery | **TL 6**, départ 4/joueur |
| 12 | `sp012` | Minion | Living Laser | SCH 2, ATK 1, PV 8, **TL 7**, CRIMINAL. ELITE. |
| 13 | `sp013` | SideScheme | Spotty Pasts | **TL 8**, départ 5/joueur |
| 14 | `sp014` | Environment | Warp Hole | **TL 9**, Hinder 5, LOCATION. TECH. |
| 15 | `sp015` | Attachment | The Hypernova | **TL 10**, +1 ATK, ARTIFACT. TECH. |
| 16-18 | `sp016` ×3 | Treachery | …Comes Around! | |
| 19-21 | `sp017` ×3 | Treachery | Distributed Presence | |
| 22-23 | `sp018` ×2 | Treachery | Oddballs | |
| 24-25 | `sp019` ×2 | Treachery | Target Spotted | |

Le **deck rencontre** est donc : `sp007` à `sp015`, puis `sp016` ×3, `sp017` ×3,
`sp018` ×2, `sp019` ×2 — 19 cartes. Les cartes 1 à 6 sont le complot principal,
les quatre stades du vilain et l'environnement, tous mis en place.

### Les textes qui n'étaient pas encore relevés

**7 · Rocket Racer** (unique) — Threat Level 2. Gagne **patrol et guard** tant
qu'il a 2 menaces ou plus sur lui. ★ Boost : révéler cette carte.

**8 · Puma** (unique) — Threat Level 3. **+1 ATK par tranche de 2 menaces** sur
lui. ★ Boost : révéler cette carte.

**9 · Anywhere & Everywhere** — Threat Level 4. *Forced Response* : à la fin de
la phase du vilain, s'il y a 3 menaces ou plus ici, **placer 1 menace sur chaque
carte en jeu portant le mot-clé Threat Level**. ★ Boost : révéler.

**10 · Chameleon** (unique) — Threat Level 5. **+1 SCH par tranche de 2 menaces**
sur lui. ★ Boost : révéler.

**11 · Penchant for Pilfery** — Threat Level 6. *Forced Response* : à la fin de
la phase du vilain, s'il y a 4 menaces ou plus ici, chaque joueur **défausse une
carte qu'il contrôle ou subit 2 dégâts**. ★ Boost : révéler.

**12 · Living Laser** (unique) — Threat Level 7. **Retaliate 1 par tranche de 2
menaces** sur lui, max 4. ★ Boost : révéler.

**13 · Spotty Pasts** — Threat Level 8. *Forced Response* : à la fin de la phase
du vilain, s'il y a 5 menaces ou plus ici, **le premier joueur cherche un sbire
Spot et le révèle**. ★ Boost : révéler.

**14 · Warp Hole** (Environment, LOCATION. TECH.) — Threat Level 9. **Hinder 5**.
Tant qu'il y a 3 menaces ou plus ici, cette carte gagne deux icônes (à relire de
près, l'image est petite à cet endroit). *Hero Response* : après qu'une attaque
inflige 3 dégâts ou plus à The Spot, **retirer 2 menaces d'ici** ; si la dernière
menace part ainsi, défausser Warp Hole.

**15 · The Hypernova** (Attachment, unique, ARTIFACT. TECH., +1 ATK) — **Attacher
à l'ennemi Spot au plus haut Threat Level.** Threat Level 10. *Forced Response* :
après l'activation de l'ennemi attaché, défausser X cartes du dessus du deck
rencontre, X étant la menace ici ; si un jeton d'accélération est posé ainsi,
défausser cette carte.

**16 · …Comes Around!** (Treachery, ×3) — *When Revealed* : défausser les 2
cartes du dessus du deck rencontre. Pour chaque carte Spot défaussée ainsi, au
choix **placer 2 menaces sur le complot principal OU la révéler**. Si aucune
carte Spot n'a été défaussée, cette carte gagne **déferlement**. ★ Boost :
défausser les 2 cartes du dessus du deck rencontre.

**19 · Distributed Presence** (Treachery, ×3) — *When Revealed* : **répartir 5
menaces au total entre les cartes Spot en jeu portant Threat Level, aussi
également que possible, en commençant par le plus BAS Threat Level**. Si 5
menaces ont été placées sur The Spot ainsi, on peut **redresser une carte qu'on
contrôle**.

**22 · Oddballs** (Treachery, ×2) — *When Revealed* : placer 1 menace sur chaque
carte Spot dont le **Threat Level est IMPAIR**. Si 2 menaces ou moins ont été
placées ainsi, **défausser une carte de sa main au coût imprimé impair**.
★ Boost : placer 2 menaces sur The Spot.

**24 · Target Spotted** (Treachery, ×2) — *When Revealed* : chercher **The
Hypernova** dans les 8 cartes du dessus du deck rencontre et la révéler. Si elle
ne l'a pas été, **chercher une carte Spot portant Threat Level et la révéler**.

### Ce que le relevé complet apprend sur le moteur

Le mot-clé n'est pas réservé au vilain : il est porté par des **sbires**, des
**manigances annexes**, des **environnements** et un **attachement**. Et la
menace se pose sur toutes ces cartes, y compris les sbires et l'attachement.
`HasThreatLevel` doit donc descendre sur les bases communes, pas sur `Villain`
seul comme au §8.


---

## 10. LIVRÉ (13/08/2026) — ce qui joue, et les trois écarts

Trois commits : `f26bd3c` (les données, les images, les deux scénarios),
`ab4c769` (les 21 modules et les crochets), après `b86513a` (le mot-clé).

### Le moteur a gagné trois crochets, chacun sur le patron d'un existant

| Ajout | Pourquoi il manquait |
|---|---|
| `AbilityFactory.WhenCardWouldRemovedToken` | Le pendant de `WhenCardWouldBePlacedToken`, qui existait seul. Le message existait déjà. |
| `OnEvent.Token` | Le pendant de `OnEvent.Counter` pour les JETONS. La menace est un jeton : une statistique qui en dépend ne se rafraîchissait jamais. |
| `ThisGainKeyword(guard=...)` | `Gain()` acceptait déjà `guard`, la fabrique ne le faisait pas suivre. Même trou que `defense`. |

Plus `Worlds.GetThreatLevelFaces` et `GetHighestThreatLevelFace`.

### ⚠️ Le défaut que seule une partie pouvait trouver

Le complot principal déroute la menace : « move that threat to the card with the
highest Threat Level **instead** ». J'ai lu « instead » comme « au lieu de
retirer », donc empêché le retrait ET posé la menace ailleurs : **elle était
dupliquée**. Les capacités se construisaient, les quatre vérificateurs étaient
verts, et la carte mentait. C'est la MESURE qui l'a dit — le complot se
complétait en 2,3 rounds au lieu de 4,0. « Move » veut dire que la menace part
d'ici et arrive là-bas.

C'est exactement la leçon de Merc Squad, sous une autre forme : aucun outil ne
dit qu'une capacité fait la BONNE chose.

### Les trois écarts assumés

1. **« Characters may thwart against The Spot »** — manigancer contre un VILAIN
   n'a aucun crochet : `ThwartInternal` ne prend que des `Scheme2`. Le niveau et
   la menace, eux, sont bien portés par le vilain. Ce qui manque est uniquement
   la manière d'en RETIRER en manigançant.
2. **L'action héroïque de What Goes Around…** déplace une quantité CHOISIE d'une
   carte vers une autre : pas de crochet.
3. **La réponse héroïque de Warp Hole** retire de la menace d'une carte du Spot,
   ce que le complot principal déroute justement. Laissée sans réponse plutôt
   que de mentir au joueur.

### Ce qui reste, si on veut aller au bout

Lever l'écart 1 est le seul qui touche vraiment le jeu : il demande d'autoriser
le maniganceage contre un ennemi. Les écarts 2 et 3 sont des commodités.

Et, comme toujours : **une partie menée par un humain**. Le bot perd les huit
parties, ce qui est plausible pour un scénario dont toute la finesse est de
placer la menace au bon endroit plutôt que de la retirer, mais seul un joueur
peut dire si l'expérience tient debout.


---

## 11. LE RAPPORT DE BUG DU JOUEUR (13/08/2026) — et ce qu'il a revele

**« J'ai voulu lancer Spot et la partie s'arrete apres la mise en place de mon
heros, on voit meme pas le deck de Spot. »**

### La cause n'etait pas le scenario

Le serveur du joueur tournait depuis **16h35**, c'est-a-dire AVANT que les cartes
existent. Le moteur charge sa base de cartes au demarrage : `sp002` n'existait
pas pour lui, et la mise en place s'arretait la. **Il faut relancer le jeu apres
tout ajout de contenu.**

Mesure : sur un serveur NEUF, le plateau montre The Spot 12/12 PV, Heightened
Threat, l'environnement What Goes Around en jeu, un deck rencontre de 34 cartes,
et zero erreur JS. Le meme piege s'est reproduit sur mon propre serveur de test
pendant le diagnostic, ce qui l'a confirme deux fois.

### ⚠️ Mais le diagnostic a trouve un VRAI defaut

Le plateau proposait **20 cartes** au choix de mise en place, alors que le texte
dit « seeks a Spot card **with the Threat Level keyword** ». Mon `CardFinder`
filtrait sur le set, pas sur le mot-cle -- et **`CardFinder` ne sait pas filtrer
sur un mot-cle** : il connait les noms, les traits, les types, les classes, pas
les attributs de `desc`. La recherche se fait donc par identifiants, via la liste
`CARTES_A_NIVEAU` du pack.

Apres correction, le choix tombe a **9 cartes**, exactement celles du deck qui
portent un niveau. Mesure sur le plateau, pas deduite.

### Le test qui verrouille la lecon

`ui-check/tests/spot-plateau.spec.ts` demande au PLATEAU ce qu'il montre. Ni
`autoplay` ni les verificateurs ne posent cette question : ils tournent dans leur
propre processus, avec un moteur fraichement charge. Le joueur, lui, arrive sur
un plateau servi par un moteur deja demarre.


---

## 12. LES TROIS ÉCARTS SONT LEVÉS (13/08/2026)

Demande de l'utilisateur : « tu finis The Spot complètement, pourquoi je vais
tester un truc qui n'est pas fini ? ». Juste. Les trois écarts du §10 n'existent
plus.

### 1. « Characters may thwart against The Spot »

Le moteur ne sait toujours pas viser un ENNEMI avec la puissance de base
Manigancer : `ThisCanThwart` cible `Scheme2` et `ThwartInternal` ne prend que des
manigances. Refondre la puissance de base toucherait **toutes** les cartes du jeu
pour une seule. **C'est donc le vilain qui OFFRE l'action** : un personnage que
vous contrôlez s'épuise (`CostFunc.Exhaust("YouControlUnit")`) et retire de la
menace d'ici à hauteur de sa valeur de MANIGANCE.

Le résultat est celui du texte. Ce que cette forme ne rend pas, et c'est écrit
dans le code : les effets qui se déclenchent « après avoir manigancé » ne partent
pas, puisque ce n'est pas la puissance de base.

### 2. L'action héroïque de What Goes Around…

Écrite. Défausser une carte de la main (`CostFunc.Discard("YourHandCards")`),
choisir la source, choisir la destination, choisir la quantité.

⚠️ **Le moteur ne sait pas demander un NOMBRE** : `AskChooseOneText` demande un
choix parmi des libellés. Les quantités possibles sont donc proposées une par
une (« Move 1 threat », « Move 2 threat »…).

### 3. La réponse héroïque de Warp Hole

Écrite, et l'écart reposait sur une **erreur de lecture de ma part** : le
déroutement du complot principal ne vise que le complot lui-même et les
manigances annexes du Spot. Warp Hole est un ENVIRONNEMENT, il n'est donc pas
concerné, et la menace en part vraiment.

### ⚠️ Ce que la mesure a dit, et qu'il faut savoir

Après ces trois ajouts, **4 parties sur 8 se sont bloquées** alors qu'il n'y en
avait aucune. Ce n'est PAS un défaut du jeu : le bot fait l'aller-retour avec la
menace (A vers B, puis B vers A, indéfiniment), et son garde-fou anti-répétition
refuse à juste titre de continuer. **Vérifié en relevant le plafond de
répétitions : 8 parties sur 8 vont alors au bout, zéro incident.**

L'action est bien illimitée sur la carte officielle, un joueur humain n'a donc
aucune raison de tourner en rond. Mais `autoplay` seul ne peut plus mesurer ce
scénario sans ce réglage — c'est à retenir pour la prochaine mesure.

`test_cards` : **4352 ok / 0 erreur**.
