
---

## 7. Textes français, images, biographie, réplique de recrutement, crédits

### 7.1 Le texte français de chaque carte fan-made — **obligatoire à chaque pack**

Un pack livré sans ce texte laisse **toutes ses cartes sans tooltip français, et rien ne le signale**. Le plateau
cherche le français d'une carte dans cet ordre : (1) un scan français ; (2) le texte officiel (généré, ne jamais
l'éditer) ; (3) **`ui-app/src/board/textes-fr-fanmade.ts`**, écrit à la main ; (4) marvelcdb en ligne (sans effet
sur du fan-made). Pour une carte fan-made, la ligne (3) est le seul français que le joueur verra dessus.

**Ta livraison** : `integration/textes-fr/<pack>.fragment.txt`, **une entrée par `card_id`, y compris pour les
exemplaires en double** (recopie le même texte), au format exact du fichier :

```
  // <pack> — <Nom de la carte> (<Type>)
  '<card_id>': "texte français avec <b>balises</b>, [star], [[TRAIT]]…",
```

Les entrées réelles de Lockjaw (la face héros et la face alter ego) :

{{TEXTESFR:lj001|2}}

Les entrées d'Iron Fist (héros officiel récent : il a aussi ses textes dans ce fichier) :

{{TEXTESFR:64001|2}}

{{SECTION:docs/kit-campagne-ia/KIT-CAMPAGNE-COMPLET.md|**Vocabulaire officiel|### 10.4|2}}

Le vérificateur refuse les tournures interdites de ce tableau (« Robustesse », « Inébranlable », « statut Robuste »,
« Résistance. », « étourdi »), signale tout `card_id` sans texte, et tout texte pour un `card_id` absent.

### 7.2 Les images

Tu **ne produis pas** d'image. L'utilisateur te donne les images des cartes du héros ; tu t'en sers pour **lire**
les cartes (c'est la source de vérité de tout ce qui est imprimé) et tu livres `images.md` : un tableau
`card_id → fichier source`.

* Dans le jeu : **`assets/pics/<card_id>.<jpg|png|webp>`** — l'extension est obligatoire, le nom est le `card_id`
  (`lj001a.png`). Une face d'identité a **une image par face** ; une carte `full_link` n'a pas d'image propre.
* Tailles mesurées : cartes de héros maison **615 × 882** (png, jpg ou webp) ; cartes officielles récentes
  **300 × ~430**, parfois **600 × 860** (les cartes custom existent aussi en 600 × 840). Les **complots annexes de rencontre** sont **en paysage** (882 × 615) :
  l'image est stockée **couchée** telle quelle, le serveur la redresse à la lecture (`TryRotateImage`). N'ajuste rien : Claude
  uniformise les scans (`outils/uniformiser-scans.py`) et calibre les bulles de statistiques d'après l'image.
* **Lecture des planches** : si l'utilisateur te donne des planches de plusieurs cartes, ne transcris pas plus de
  **quatre cartes par lecture** : au-delà, le texte d'encart n'est plus fiable. Une carte lue à moitié se pose en
  question (§1.3), pas en supposition.
* `images.md` : une ligne par `card_id` (faces comprises), le fichier source et la taille si tu la connais :

```
| card_id | fichier | taille |
|---|---|---|
| lj001a | lockjaw-hero.png | 615x882 |
| lj001b | lockjaw-alter-ego.png | 615x882 |
```

### 7.3 La biographie (survol du héros dans le lanceur)

Le lanceur affiche, au survol de la tuile du héros, une fiche qui décrit le **personnage** (jamais sa mécanique
de jeu). Elle est indexée par le **`card_id` de la face héros** et jamais par le nom (`01001a` Peter Parker et
`27030a` Miles Morales s'appellent tous deux « Spider-Man »).

{{SECTION:docs/reference/PROCESSUS-HEROS.md|## Étape 7 : Biographie|## Étape 8|2}}

L'entrée réelle de Lockjaw (modèle de forme ; tu livres **seulement ta part** dans
`public/js/prepare/heros-info.fragment.js`) :

{{ENTREE:Fusion/marvel-lcg-src/public/js/prepare/heros-info.js|lj001a}}

Les clés autorisées : `bio` et `bioEn` (**obligatoires**), `civil`, `civilEn`, `base`, `baseEn`, `equipes`,
`equipesEn`, `ennemis`, `ennemisEn`, `apparition`. Le vérificateur refuse toute autre clé en avertissement, et
une biographie qui parle de mécanique de jeu (« Action », « Response »…). **Ne remplis que ce que tu sais ;
n'invente pas une équipe ou une némésis.** Sans entrée, le héros retombe silencieusement sur l'ancien affichage :
rien ne casse, la fiche manque.

### 7.4 La réplique de recrutement (facultative, à proposer)

Au recrutement, une phrase s'affiche sur la carte. Plusieurs par héros, tirées au sort sans répéter la dernière.
Elle est indexée par l'**identifiant de deck** (le nom du fichier `deck/starter/<id>.json`), **jamais par le nom**
(« Spider-Man » désigne quatre decks). Un héros sans réplique retombe sur l'onomatopée propre à son id dans `ONOMATOPEES` (`app.js`), puis sur
« BAM ! ». Les répliques sont des **répliques** (comics, films), gardées en anglais avec leur casse et leur
ponctuation : **ne les traduis pas** ; les onomatopées de pouvoirs restent dans le style « MOT ! ». **Ne les
invente pas** : si tu n'en connais pas de véritable, demande à l'utilisateur (c'est lui qui établit la liste).
Tu livres **une seule ligne** dans `public/js/prepare/repliques-heros.fragment.js` :

{{LIGNE:Fusion/marvel-lcg-src/public/js/prepare/repliques-heros.js|    lockjaw: [|javascript}}

{{LIGNE:Fusion/marvel-lcg-src/public/js/prepare/repliques-heros.js|    ant_man: [|javascript}}

### 7.5 Les crédits

* **Héros maison** : la clé `custom` (nom de l'auteur) sur **toutes** les cartes du héros, **identités comprises**.
  C'est ce qui fait afficher « Lockjaw (Nugget) » dans la grille (`public/js/prepare/auteur.js`) et le
  remerciement du filtre fan-made. `metadata.author` du deck porte le même nom.
* `CREDITS.md` de ta livraison : l'auteur et ses liens (`metadata.url`), le dossier source, les remerciements que
  l'auteur demande, et le nom de toute personne qui a fourni des scans. Rien d'autre.
* **Héros officiel** : pas de `custom`, pas de crédits d'auteur.

### 7.6 Ce que tu n'écris pas dans cette chaîne

Les positions de bulles de statistiques, la palette du héros, l'annuaire d'identités, les arts alternatifs
cosmétiques, la page « nouveautés » : tout cela est généré ou rédigé par Claude à partir des images et du
déroulé. Demande-le dans `BESOINS-MOTEUR.md` si ton héros a une particularité (une identité alternative à
l'art différent, par exemple).
