# Zeus (Mozilla) — relevé du matériel, avant toute ligne de code

**Relevé le 11/09/2026**, depuis le Drive de l'utilisateur (`Zeus`, auteur
`pavelklaban`, signature des cartes « MC Custom Content By: Mozilla »).

**23 cartes physiques, 17 entrées distinctes.** Identité recto verso, 15 cartes
de set héros numérotées 1/15 à 15/15, 1 obligation hors numérotation, et un set
némésis complet numéroté 1/5 à 5/5.

## ⚠ Comment ce relevé a été fait, et ce qu'il faut revérifier

Les textes viennent de **deux sources de qualité inégale** :

- **Lues à l'œil sur l'image** (fiables, icônes comprises) : les 5 némésis,
  `8/15` Olympian Might, et l'obligation. L'utilisateur les a collées
  directement.
- **Lues par OCR du Drive** (mots fiables, **icônes et chiffres douteux**) :
  l'identité et les 14 autres cartes du set héros.

⚠ **L'OCR NE REND PAS LES ICÔNES DE RESSOURCES.** Il écrit « Requirement (2) »
là où la carte montre « Requirement (⚡) », et « (222) » pour trois éclairs.
Toute icône citée ci-dessous vient donc d'une déduction, sauf sur les cartes
lues à l'œil. **À reconfirmer sur les scans avant la moindre entrée dans
`data/cards.json`.**

## ⚠ LA SEULE AMBIGUÏTÉ QUI RESTE, ET ELLE EST AU CŒUR DU PACK

La capacité d'identité, *Skyfather's Tempest*, est rendue par l'OCR ainsi :

> « After you spend both **and** resources to pay for an event, resolve the
> "Special" ability on that event and remove 1 threat from a scheme. »

Deux icônes ont disparu entre « both » et « and ». Or c'est la condition de
déclenchement de TOUT le pack : quatre cartes s'y réfèrent explicitement
(`11/15` The Aegis, `12/15` Thunderbolt, `13/15` Skyfather, et l'obligation).
**Il faut voir cette carte.**

## Le cœur du pack : l'énergie ⚡ et les capacités « Spécial »

Deux mécaniques imbriquées, et le set némésis attaque précisément les deux.

**Les « Spécial ».** Sept cartes du set héros en portent un. Ce sont des
capacités qui ne se déclenchent PAS en jouant la carte : `Skyfather's Tempest`
les résout depuis la main, Hera en résout un à son entrée, et `13/15` Skyfather
en DONNE un aux événements qui n'en ont pas.

**L'énergie ⚡.** Les événements d'attaque portent un `Requirement` en éclairs,
l'obligation en réclame un pour partir, `Mount Olympus` et `Thunderbolt` en
génèrent.

**Et le némésis vise ces deux points**, ce qui est du beau travail d'auteur :
Nyx punit les cartes à éclair imprimé, *The Mother of Night* les confisque,
*Shroud of the Nightmother* interdit purement de les dépenser, et *Total
Eclipse* punit les événements à « Spécial ».

## Les 17 entrées

### Identité

- **`* Zeus`** (Hero) — OLYMPUS. CTR 2, ATQ 2, DEF 2. Main 4 / 15 PV.
  *Skyfather's Tempest* — **Réponse** : après avoir dépensé ⟨**deux icônes à
  confirmer**⟩ pour payer un événement, résolvez la capacité « Spécial » de cet
  événement et retirez 1 menace d'une manigance.
- **`* Zeus Panhellenios`** (AlterEgo) — OLYMPUS. REC 5. Main 6 / 15 PV.
  *God of Lightning* — **Action** : cherchez l'amélioration Thunderbolt dans
  votre deck et votre défausse et ajoutez-la à votre main. *(1 max par round.)*

### Set héros, 15 cartes

| # | Carte | Type | Texte |
|---|---|---|---|
| 1 | **Hera** | Allié, coût 2, CTR 2, ATQ 2, OLYMPUS | **Réponse** : après l'entrée en jeu de Hera, choisissez une carte de votre main portant un « Spécial » imprimé et résolvez-le |
| 2-5 | **Thunder Strike** ×4 | Événement, coût 2, ATTACK SUPERPOWER | Requirement (⚡). **Action de héros** *(attaque)* : 5 dégâts, Perçant. **Spécial** : étourdir un ennemi |
| 6-7 | **Precognition** ×2 | Événement, coût 2, SUPERPOWER THWART | **Action de héros** *(contre)* : retirer 4 menaces. **Spécial** : désorienter un ennemi |
| 8-9 | **Olympian Might** ×2 | Événement, coût 3, ATTACK SUPERPOWER | Requirement (⚡⚡). **Action de héros** *(attaque)* : 7 dégâts, et si l'ennemi est vaincu, redressez Zeus. **Spécial** : gagnez une carte de statut Robuste |
| 10 | **Wrath of Olympus** | Événement, coût 5, ATTACK SUPERPOWER | Requirement (⚡⚡⚡). **Action de héros** *(attaque)* : 10 dégâts, Déferlement. **Spécial** : 2 dégâts à chaque ennemi, 2 menaces retirées de chaque manigance |
| 11 | **The Aegis** | Amélioration, coût 1, ARMOR OLYMPUS | **Réponse** : après avoir résolu *Skyfather's Tempest*, posez 1 compteur d'égide ici. **Interruption de héros** *(défense)* : retirez 2 compteurs pour empêcher 3 dégâts |
| 12 | **Thunderbolt** | Amélioration, OLYMPUS WEAPON | **Ressource de héros** : inclinez pour générer une ressource. **Réponse de héros** : après avoir résolu *Skyfather's Tempest*, redressez Thunderbolt |
| 13 | **Skyfather** | Amélioration, coût 2, OLYMPUS TITLE | Chaque événement que vous possédez sans « Spécial » imprimé en gagne un : « **Spécial** : 2 dégâts à un ennemi ». **Réponse** : après *Skyfather's Tempest*, +1 taille de main jusqu'à la fin de la phase |
| 14 | **Hephaestus** | Soutien, coût 1, OLYMPUS PERSONA | **Action d'alter ego** : inclinez pour remélanger 1 Thunder Strike de votre défausse dans votre deck et piochez 1 carte |
| 15 | **Mount Olympus** | Soutien, coût 1, LOCATION OLYMPUS | **Ressource** : inclinez et dépensez une ressource pour en générer une autre ⟨**icônes à confirmer**⟩ |

### Obligation

- **`Alcohol Problems`** (Obligation, set `ZEUS`, boost 2) — *Donnez-la au
  joueur Zeus Panhellenios.* Zeus ne peut pas résoudre son *Skyfather's
  Tempest*. **Action d'alter ego** : inclinez votre identité et dépensez une
  ressource ⚡ pour retirer Alcohol Problems de la partie.

### Set némésis, 5 cartes

| # | Carte | Type | Texte |
|---|---|---|---|
| 1/5 | **`* Nyx`** | Sbire, 6 PV, MNG 2*, ATQ 1*, boost 3, ELITE OLYMPUS | Stable. Vilain. ★ **Interruption forcée** : quand Nyx s'active contre vous, défaussez le dessus de votre deck ; si cette carte porte une icône ⚡ imprimée, Nyx gagne 1 carte de boost |
| 2/5 | **The Mother of Night** | Manigance annexe, 1 menace, boost 3, icône d'aléa | **Une fois révélée** : chaque joueur cherche dans son deck et sa défausse 2 cartes à icône ⚡ imprimée et les pose face cachée dessous. +1 menace ici par carte posée. **Une fois déjouée** : rendez chaque carte à la défausse de son propriétaire |
| 3/5 | **Shroud of the Nightmother** | Attachement, boost 2, CONDITION | Attachez-la à votre identité. Vous ne pouvez plus dépenser de ressources ⚡ pour payer des cartes. **Action d'alter ego** : dépensez 2 ressources de n'importe quel type pour la défausser |
| 4/5, 5/5 | **Total Eclipse** ×2 | Traîtrise | **Une fois révélée** : défaussez les 3 cartes du dessus de votre deck. 1 dégât indirect par événement défaussé. Si un événement à « Spécial » imprimé est défaussé, vous êtes étourdi. ★ **Boost** : donnez une carte de boost supplémentaire à l'ennemi qui s'active |

## Mots-clés rencontrés, fiches à ouvrir avant d'écrire

`requirement`, `piercing`, `overkill`, `steady`, `villainous`, `hazard`,
`toughness`, `stunned`, `confused`. **Toutes ont déjà leur fiche** dans
`docs/reference/mots-cles/`. Aucun mot-clé maison, contrairement à Sentinel et
son `DESTROY`.

## Nommage, déjà vérifié

Relevé fait, pas supposé, sur `cards.json` :

- ⚠⚠ **`Precognition` EXISTE DÉJÀ** : `40004`, pack `next_evol`. Les cartes
  `6/15` et `7/15` de Zeus portent exactement ce nom. C'est le même piège que
  `spider_woman` et que `* Mockingbird`, qui a mordu DEUX FOIS aujourd'hui, une
  fois dans le moteur et une fois dans le constructeur de deck. Le `card_id`
  fan-made préfixé règle la collision côté données ; ce qu'il faut surveiller,
  ce sont les règles et les recherches **par NOM**.
- `Thunderbolt` : pas de collision exacte, mais `50131b` *Thunderbolt Backup* et
  `57021` *The Thunderbolts* existent. Une recherche par sous-chaîne les
  attraperait.
- `Zeus` : `59010` *Son of Zeus* (pack `hercules`) contient le mot. Même
  remarque.
- **Libres** : Hera, Hephaestus, Nyx, Mount Olympus, The Aegis, Skyfather,
  Total Eclipse, Alcohol Problems.
- ⚠ **`Hercules` existe déjà** comme héros officiel, et la citation de `8/15` le
  mentionne. Sans conséquence, mais à ne pas confondre.
- Préfixe **`ze` libre**, vérifié dans `tools/prefixes_fanmade.json`.

## Ce qu'il faut avant de commencer

1. **Voir la carte d'identité Zeus** pour lire les deux icônes de *Skyfather's
   Tempest*. Bloquant : quatre cartes et l'obligation en dépendent.
2. **Les images en local.** Le connecteur Drive ne rend que du texte, et je ne
   peux pas télécharger 23 PNG sans saturer ma mémoire de travail. Il les faut
   sur le poste pour `assets/pics/` **et** pour reconfirmer les icônes que
   l'OCR a mangées.
3. Réserver un préfixe (`ze` est libre) et un numéro de set (171, après
   Spider-Woman en 169 et Mockingbird pressenti en 170).
