# À FAIRE : relever qui est sur l'image de chaque carte

**Constat de l'utilisateur, 13/09/2026**, en regardant la carte Muse :
« c'est vraiment l'image sur la carte qui fait foi ».

Il a raison, et la carte est formelle. Texte exact de **Muse (3/7)** :

> **Forced Interrupt**: When a player plays a card that has **their identity's
> picture on it**, Muse activates against that player.

Quatre des six cartes du set le disent (1/7, 3/7, 4/7, 6/7). Ce n'est pas
« une carte signature », c'est l'illustration.

## Pourquoi ce n'était pas fait

**Le moteur ne voit pas les images.** Il connaît le nom, le type, la classe,
les traits et le texte d'une carte ; rien de ce qu'elle montre. Aucun champ de
`cards.json` ne le dit, et MarvelCDB ne le fournit pas.

Le 13/09 au matin, l'arbitrage retenu était donc « les cartes signature »
(`card_class="IdentitySpecific"`), en écartant explicitement « vraiment
l'illustration », qui « demanderait de relever à l'œil ce que montrent des
milliers d'images ». C'est exactement ce qu'on décide de faire, mais avec un
outil pour que ce soit tenable.

## Ce qui est décidé

| Point | Décision |
|---|---|
| **Périmètre** | **Tout le catalogue**, 4324 cartes. Cartes joueur, rencontres, vilains : `Supply Run` et `Art Imitates Death` portent sur n'importe quelle carte. |
| **Où vit l'outil** | Une **page du jeu réservée à l'administrateur**, atteignable depuis `/admin`. Le relevé est un arbitrage : deux avis différents donneraient une liste incohérente. |
| **Combien de personnages par carte** | **Autant qu'on veut**, cases à cocher. `Art Imitates Death` dit « chaque personnage dont l'image était sur cette carte » : au pluriel. |
| **Liste proposée** | **Les identités du jeu** : héros officiels et fan-made avec leur alter ego, vilains, sbires uniques. Ce sont les seuls personnages que les cartes de Muse désignent. |
| **Carte sans identité** | **Un seul bouton « Aucune identité »** : lieu, civil, objet, explosion, même réponse. La nuance ne changerait rien en jeu. |
| **Carte qu'on ne sait pas trancher** | Un bouton **« Je verrai plus tard »**, distinct : elle retourne dans le tas au lieu d'être classée. |
| **Ordre** | **Les plus utiles d'abord** : cartes signature, puis cartes joueur, puis rencontres, puis le reste. Muse devient juste dès les premières centaines, même si le relevé s'arrête en chemin. |
| **Stockage** | **`data/images_cartes.json`**, versionné, à côté du catalogue. Il se relit dans git, survit à une réinstallation, et le harnais peut écrire des tests dessus. |

## Le repli, et il compte

⚠ **Une carte non relevée garde l'approximation actuelle** (carte signature).
Le relevé n'est donc jamais bloquant : on peut s'arrêter, reprendre, et le jeu
reste jouable à chaque instant. C'est ce qui permet d'attaquer 4324 cartes sans
promettre de les finir.

## Reste à préciser au moment de faire

- La forme exacte de `images_cartes.json` : `{ "<card_id>": ["<id identité>"] }`
  avec une liste vide pour « aucune identité », et l'absence de clé pour
  « pas encore relevée ». Deux états distincts, à ne pas confondre.
- La route d'écriture côté moteur, sur le modèle de `save_legacy`.
- Comment `EstUneCarteSignature` (pack `muse`) consulte le relevé, et comment
  `Art Imitates Death` et `Supply Run` s'en servent pour désigner leurs cibles.
- Le compteur d'avancement : combien de cartes relevées sur 4324.

## Statut

Décisions prises, **non commencé**.
