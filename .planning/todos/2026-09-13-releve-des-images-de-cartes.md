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
| **Périmètre** | **Tout le catalogue**. ⚠ Le chiffre de 4324 cartes écrit ici le 13/09 était faux : le catalogue en compte **6153**, qui ne portent que **5746 illustrations distinctes** (`pic_id` et `full_link` en partagent). Corrigé au moment de faire. || **Où vit l'outil** | Une **page du jeu réservée à l'administrateur**, atteignable depuis `/admin`. Le relevé est un arbitrage : deux avis différents donneraient une liste incohérente. |
| **Combien de personnages par carte** | **Autant qu'on veut**, cases à cocher. `Art Imitates Death` dit « chaque personnage dont l'image était sur cette carte » : au pluriel. |
| **Liste proposée** | **Les identités du jeu** : héros officiels et fan-made avec leur alter ego, vilains, sbires uniques. Ce sont les seuls personnages que les cartes de Muse désignent. |
| **Carte sans identité** | **Un seul bouton « Aucune identité »** : lieu, civil, objet, explosion, même réponse. La nuance ne changerait rien en jeu. |
| **Carte qu'on ne sait pas trancher** | Un bouton **« Je verrai plus tard »**, distinct : elle retourne dans le tas au lieu d'être classée. |
| **Ordre** | **Les plus utiles d'abord** : cartes signature, puis cartes joueur, puis rencontres, puis le reste. Muse devient juste dès les premières centaines, même si le relevé s'arrête en chemin. |
| **Stockage** | **`data/images_cartes.json`**, versionné, à côté du catalogue. Il se relit dans git, survit à une réinstallation, et le harnais peut écrire des tests dessus. |

## Le repli, et il compte

⚠ **Une carte non relevée garde l'approximation actuelle** (carte signature).
Le relevé n'est donc jamais bloquant : on peut s'arrêter, reprendre, et le jeu
reste jouable à chaque instant. C'est ce qui permet d'attaquer 5746
illustrations sans promettre de les finir.

⚠ **Vérifié, pas supposé** : les 12 cas Muse de `test_capacites.py` sont
repassés verts avec un relevé vide, donc l'ancien comportement est intact tant
que rien n'est relevé.

## Ce qui a été tranché en faisant

- **La clé est l'IMAGE, pas la carte.** `{ "<id image>": ["<id personne>"] }`,
  l'id image étant `pic_id`, sinon la carte d'origine d'une réimpression,
  sinon la carte elle-même. Même résolution côté moteur, côté page et côté
  outil d'import. Sans cela, une réimpression aurait pu contredire son original.
- **Une personne n'est pas une carte.** D'où `data/identites.json`, généré par
  `outils/annuaire-identites.py` : Rhino est quatre cartes, Spider-Man douze
  faces. ⚠ Le regroupement se fait sur le **couple héros + alter ego**, jamais
  sur le seul nom de code : « Spider-Man » seul fondait Peter Parker, Miles
  Morales et Miguel O'Hara en une personne.
- **`EstUneCarteSignature` n'est plus la règle, c'est le repli.** La règle est
  `PorteLImageDe(face, joueur)`, et elle est *discrète* : elle ne retombe sur
  l'approximation que pour une image **jamais regardée**. Une image relevée
  sans personne dessus répond non, même sur une carte signature, sinon relever
  une carte n'aurait aucun effet.
- **`mu005` Grim Inspiration garde `CartesSignatureDe`** : c'est la seule carte
  du set dont le texte imprimé dit vraiment « an identity-specific card ».
- **Un lot peut venir d'une IA qui voit les images.** Prompt et CSV dans
  `.planning/releve-images/`, versement par `outils/importer-releve-images.py`,
  qui refuse le lot entier si un seul identifiant est inventé.

## Statut

**Fait** (commit `1596c595`). Le relevé lui-même est à zéro : c'est le travail
de saisie qui commence, il n'est jamais bloquant.

Reste ouvert : personne n'a encore relevé une seule carte, donc le chemin
« relevé non vide » n'a été prouvé que par `outils/test_releve_images.py` et
par la spec Playwright, jamais en partie réelle. Le jour où le premier lot est
versé, rejouer les 12 cas Muse de `test_capacites.py` pour voir ce qui change.
