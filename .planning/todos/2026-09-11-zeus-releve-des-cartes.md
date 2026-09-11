# Zeus (Mozilla) — relevé du matériel, avant toute ligne de code

**Relevé le 11/09/2026**, depuis le Drive de l'utilisateur (`Zeus`, auteur
`pavelklaban`, signature des cartes « MC Custom Content By: Mozilla »).

**23 cartes physiques, 17 entrées distinctes.** Identité recto verso, 15 cartes
de set héros numérotées 1/15 à 15/15, 1 obligation hors numérotation, et un set
némésis complet numéroté 1/5 à 5/5.

## ⚠ Comment ce relevé a été fait, et ce qu'il faut revérifier

Les textes viennent de **deux sources de qualité inégale** :

- **Lues à l'œil sur l'image** (fiables, icônes comprises) : **les 23 cartes**.
  L'utilisateur les a toutes collées dans le fil le 11/09/2026, le set héros
  d'abord, puis le set némésis et l'obligation.
- **Lues par OCR du Drive** (mots fiables, **icônes et chiffres douteux**) :
  première passe, aujourd'hui remplacée par la lecture à l'œil.

⚠ **L'OCR NE REND PAS LES ICÔNES DE RESSOURCES.** Il écrit « Requirement (2) »
là où la carte montre « Requirement (⚡) », et « (222) » pour trois éclairs.
C'est pour cette raison que le relevé a été refait image par image : la colonne
« Ressource imprimée » ci-dessous est lue sur la pastille de coin, pas déduite.

## ⚠⚠ CE PACK INVENTE UN CINQUIÈME TYPE DE RESSOURCE

Résolu le 11/09/2026 avec l'utilisateur, carte par carte, sur les images.
**La première version de ce relevé se trompait sur toutes les icônes** : elle
lisait « énergie » partout où elle voyait un éclair. Il y a en réalité DEUX
icônes distinctes, et le pack repose entièrement sur leur différence.

**Vocabulaire à employer partout désormais**, arrêté avec l'utilisateur :

- **énergie** : la ressource officielle jaune du jeu de base. `Y` côté moteur.
- **éclair** : une ressource **maison**, inventée par l'auteur, qui n'existe que
  dans ce pack. **Aucune contrepartie dans le moteur.**

### Où chaque icône apparaît, relevé exhaustif

| Endroit | Énergie | Éclair |
|---|---|---|
| Ressource imprimée, Thunder Strike ×4 | | **oui** |
| Ressource imprimée, Wrath of Olympus et Thunderbolt | **oui** | |
| *Skyfather's Tempest* (identité) | **oui** | **oui**, il faut les DEUX |
| `Requirement` de Thunder Strike (×1), Olympian Might (×2), Wrath of Olympus (×3) | **oui** | |
| Mount Olympus, ressource dépensée | **oui** | |
| Mount Olympus, ressource générée | | **oui** |
| Thunderbolt, ressource générée | **oui** | |
| Alcohol Problems, ressource dépensée | | **oui** |
| Nyx, The Mother of Night, Shroud of the Nightmother | **oui** | |

### Ce que ça dit du dessin du pack

**L'éclair est rare et interne.** Deux sources seulement : les **quatre**
Thunder Strike, qui le portent imprimé, et **Mount Olympus**, qui convertit une
énergie en éclair. Rien d'autre n'en produit, et aucune carte d'aspect n'en
portera jamais.

**Le Tempest est un puzzle à deux ingrédients.** Il faut payer un même
événement avec au moins une énergie ET au moins un éclair. L'énergie vient de
partout, l'éclair des deux seules sources ci-dessus. C'est la tension du pack.

**Le némésis ne vise PAS l'éclair, il vise l'énergie.** C'est plus vicieux que
ce que croyait la première version : Shroud of the Nightmother interdit de
dépenser de l'énergie, donc éteint le Tempest, les trois `Requirement` et Mount
Olympus d'un seul coup. Nyx et The Mother of Night frappent les cartes à
énergie imprimée, qui sont légion dans n'importe quel aspect.

⚠ **L'obligation, elle, coûte un éclair.** Alcohol Problems bloque le Tempest
et réclame la ressource la plus rare du deck pour partir. Combinée au Shroud,
elle est presque verrouillée, puisque Mount Olympus a besoin d'énergie pour
fabriquer l'éclair.

## ⚠⚠ CONSÉQUENCE MOTEUR : ce pack n'est PAS un pack ordinaire

Le moteur code **quatre** couleurs en dur, et rien n'y est extensible :

`src/game/element/rbyg.py` définit `ResRBYG(r, b, y, g)` avec
`RBYG: TypeAlias = Literal["R", "B", "Y", "G"]`. Chaque opération
(`__add__`, `__sub__`, `__mul__`, `FromText`, `GetColor`, `OnlyHasColor`,
`GetTypeKindsInternal`, `IsSameType`, `IsDifferentType`, `CanPayThisCost`)
énumère les quatre champs à la main. `Resources.RES_TEXT` et
`Resources.RBYG_LIST` les listent à nouveau, et le constructeur de `Resources`
n'accepte qu'un `Literal` fermé de combinaisons.

**Mesuré, pas supposé** : `rbyg`/`RBYG` apparaît **121 fois dans 22 fichiers**,
dont 16 fichiers de moteur. S'y ajoutent le format de `data/cards.json`, le
pool de ressources du joueur, l'écran de paiement et le rendu du plateau.

**Ce n'est donc pas un portage de cartes, c'est un chantier moteur.** Il faut
trancher avant d'écrire la première ligne :

1. **Ajouter une vraie cinquième couleur** au moteur. Coûteux, touche le cœur
   du système de paiement, mais rend le pack à 100 %.
2. **Modéliser l'éclair autrement** qu'en couleur de ressource : un compteur,
   un jeton, une carte-ressource spéciale. Moins invasif, mais il faut vérifier
   que « dépenser un éclair pour payer un événement » reste exprimable.
3. **Renoncer** à ce pack tant que le point 1 n'est pas fait.

✅ **Choix fait le 11/09/2026 : option 1**, la vraie cinquième couleur, livrée le jour même (voir la fiche `docs/reference/mots-cles/eclair.md`).

## Les 17 entrées

### Identité

- **`* Zeus`** (Hero) — OLYMPUS. CTR 2, ATQ 2, DEF 2. Main 4 / 15 PV.
  *Skyfather's Tempest* — **Réponse** : après avoir dépensé **à la fois une
  énergie et un éclair** pour payer un même événement, résolvez la capacité
  « Spécial » de cet événement et retirez 1 menace d'une manigance.
- **`* Zeus Panhellenios`** (AlterEgo) — OLYMPUS. REC 5. Main 6 / 15 PV.
  *God of Lightning* — **Action** : cherchez l'amélioration Thunderbolt dans
  votre deck et votre défausse et ajoutez-la à votre main. *(1 max par round.)*

### Set héros, 15 cartes

| # | Carte | Type | Ressource imprimée | Texte |
|---|---|---|---|---|
| 1 | **Hera** | Allié, coût 2, CTR 2, ATQ 2, OLYMPUS | joker | **Réponse** : après l'entrée en jeu de Hera, choisissez une carte de votre main portant un « Spécial » imprimé et résolvez-le |
| 2-5 | **Thunder Strike** ×4 | Événement, coût 2, ATTACK SUPERPOWER | **éclair** | Requirement (1 énergie). **Action de héros** *(attaque)* : 5 dégâts, Perçant. **Spécial** : étourdir un ennemi |
| 6-7 | **Precognition** ×2 | Événement, coût 2, SUPERPOWER THWART | mental | **Action de héros** *(contre)* : retirer 4 menaces. **Spécial** : désorienter un ennemi |
| 8-9 | **Olympian Might** ×2 | Événement, coût 3, ATTACK SUPERPOWER | physique | Requirement (2 énergies). **Action de héros** *(attaque)* : 7 dégâts, et si l'ennemi est vaincu, redressez Zeus. **Spécial** : gagnez une carte de statut Robuste |
| 10 | **Wrath of Olympus** | Événement, coût 5, ATTACK SUPERPOWER | énergie | Requirement (3 énergies). **Action de héros** *(attaque)* : 10 dégâts, Déferlement. **Spécial** : 2 dégâts à chaque ennemi, 2 menaces retirées de chaque manigance |
| 11 | **The Aegis** | Amélioration, coût 1, ARMOR OLYMPUS | physique | **Réponse** : après avoir résolu *Skyfather's Tempest*, posez 1 compteur d'égide ici. **Interruption de héros** *(défense)* : retirez 2 compteurs pour empêcher 3 dégâts |
| 12 | **Thunderbolt** | Amélioration, OLYMPUS WEAPON | énergie | **Ressource de héros** : inclinez pour générer **une énergie**. **Réponse de héros** : après avoir résolu *Skyfather's Tempest*, redressez Thunderbolt |
| 13 | **Skyfather** | Amélioration, coût 2, OLYMPUS TITLE | joker | Chaque événement que vous possédez sans « Spécial » imprimé en gagne un : « **Spécial** : 2 dégâts à un ennemi ». **Réponse** : après *Skyfather's Tempest*, +1 taille de main jusqu'à la fin de la phase |
| 14 | **Hephaestus** | Soutien, coût 1, OLYMPUS PERSONA | mental | **Action d'alter ego** : inclinez pour remélanger 1 Thunder Strike de votre défausse dans votre deck et piochez 1 carte |
| 15 | **Mount Olympus** | Soutien, coût 1, LOCATION OLYMPUS | physique | **Ressource** : inclinez et dépensez **une énergie** pour générer **un éclair** |

⚠ Les quatre Thunder Strike sont les SEULES cartes du pack à imprimer l'éclair.
Toutes les autres pastilles sont des ressources officielles ordinaires.

### Obligation

- **`Alcohol Problems`** (Obligation, set `ZEUS`, boost 2) — *Donnez-la au
  joueur Zeus Panhellenios.* Zeus ne peut pas résoudre son *Skyfather's
  Tempest*. **Action d'alter ego** : inclinez votre identité et dépensez une
  **éclair** pour retirer Alcohol Problems de la partie. ⚠ C'est la seule
  carte hors identité à réclamer un éclair, et elle bloque justement le
  *Skyfather's Tempest* tant qu'elle est là.

### Set némésis, 5 cartes

| # | Carte | Type | Texte |
|---|---|---|---|
| 1/5 | **`* Nyx`** | Sbire, 6 PV, MNG 2*, ATQ 1*, boost 3, ELITE OLYMPUS | Stable. Vilain. ★ **Interruption forcée** : quand Nyx s'active contre vous, défaussez le dessus de votre deck ; si cette carte porte une **énergie** imprimée, Nyx gagne 1 carte de boost |
| 2/5 | **The Mother of Night** | Manigance annexe, 1 menace, boost 3, icône d'aléa | **Une fois révélée** : chaque joueur cherche dans son deck et sa défausse 2 cartes à **énergie** imprimée et les pose face cachée dessous. +1 menace ici par carte posée. **Une fois déjouée** : rendez chaque carte à la défausse de son propriétaire |
| 3/5 | **Shroud of the Nightmother** | Attachement, boost 2, CONDITION | Attachez-la à votre identité. Vous ne pouvez plus dépenser d'**énergie** pour payer des cartes. ⚠ Éteint d'un coup le *Tempest*, les trois `Requirement` et Mount Olympus. **Action d'alter ego** : dépensez 2 ressources de n'importe quel type pour la défausser |
| 4/5, 5/5 | **Total Eclipse** ×2 | Traîtrise | **Une fois révélée** : défaussez les 3 cartes du dessus de votre deck. 1 dégât indirect par événement défaussé. Si un événement à « Spécial » imprimé est défaussé, vous êtes étourdi. ★ **Boost** : donnez une carte de boost supplémentaire à l'ennemi qui s'active |

## Mots-clés rencontrés, fiches à ouvrir avant d'écrire

`requirement`, `piercing`, `overkill`, `steady`, `villainous`, `hazard`,
`toughness`, `stunned`, `confused`. **Toutes ont déjà leur fiche** dans
`docs/reference/mots-cles/`.

⚠ **Mais il y a bien du maison ici** : l'**éclair** est une ressource inventée
par l'auteur, au même titre que le `DESTROY` de Sentinel. Elle mérite sa fiche
dans `docs/reference/mots-cles/`, et surtout une décision moteur (voir plus
haut) avant la moindre ligne de code.

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

1. ✅ **Fait le 11/09/2026** : toutes les icônes sont lues et confirmées avec
   l'utilisateur, carte par carte. Le relevé de texte est complet.
2. ✅ **Fait le 11/09/2026** : l'éclair est une cinquième couleur du moteur,
   lettre `L`. Fiche `docs/reference/mots-cles/eclair.md`, spec et plan dans
   `docs/superpowers/`. Thunder Strike portera `"RES": "L"`, et le Tempest
   se lit `Cost("YL")` sur le paiement de l'événement.
3. ✅ **Livré le 11/09/2026** : pack écrit, 35/35 cas, substitution 17/17,
   autoplay sans traceback. Gabarits dans
   `2026-09-11-zeus-gabarits-processus-carte.md`. ✅ Les 4 scans némésis sont installés (dossier « Encounter Cards » du Drive :
   le connecteur n'y voyait qu'Alcohol Problems, la vue embarquée
   `embeddedfolderview?id=` donne les identifiants des autres). Reste la vérification en partie réelle du boost supplémentaire
   de Nyx, que le harnais ne sait pas mesurer.
3 bis. **Les images en local.** ✅ 13 scans rapatriés depuis le Drive en direct (`curl` sur le lien partagé) et uniformisés à 615 px. Le connecteur Drive ne rend que du texte, mais
   le lien de téléchargement direct suffit. Il les faut sur le
   poste pour `assets/pics/`. L'utilisateur est à distance et les a collées
   dans le fil : elles sont lues, mais pas déposées sur le disque.
4. Réserver un préfixe (`ze` est libre) et un numéro de set (171, après
   Spider-Woman en 169 et Mockingbird pressenti en 170).
