# Noir et blanc — le cadre de couleur autour de la carte

Spécifié le 08/08/2026, par questions au joueur. **Rien n'a encore été codé.**
Ce document complète [2026-08-08-effets-meteo-design.md](2026-08-08-effets-meteo-design.md)
et ne concerne QUE l'effet `noir`.

## Le besoin, dans les mots du joueur

> « Je veux que la couleur de la carte soit autour de la carte, et pas dans un
> carré au-dessus. »

## Diagnostic — mesuré dans le jeu, pas déduit

Aperçu forcé sur « Noir et blanc », partie Sharon Carter, fenêtre 1900×900.

| Constat | Mesure |
|---|---|
| `.plateau` porte bien `est-delave` | oui |
| `.scan-visuel` est désaturé | `filter: grayscale(1)` |
| Cartes portant une classe `aspect-*` | **6 sur 16** |
| Liseré sur ces 6 cartes | `outline: 4px solid #a878e8`, `outline-offset: 3px` |
| Coins de ces mêmes cartes | `border-radius: **0px**` |
| Coins d'une carte ordinaire | `border-radius: 8px` |

Trois choses en découlent, et ce sont les trois à corriger.

**1. Le « carré », c'est la règle censée l'éviter.** `board.css` pose
`border-radius: inherit` sur `.plateau.est-delave .scan-card[class*='aspect-']`.
`inherit` prend la valeur du PARENT (`.plateau-unite`, à 0), pas la valeur
propre de l'élément (8 px). La règle écrite pour que le liseré épouse les coins
arrondis **carre les coins** de très exactement les cartes qu'elle décore. Avec
en plus `outline-offset: 3px`, on obtient un rectangle à angles vifs flottant à
3 px d'un scan arrondi : un carré posé autour de la carte.

**2. Dix cartes sur seize n'ont aucune couleur.** L'aspect vient de `desc.Class`
du catalogue, que seules les cartes de joueur possèdent. Méchant, manigances,
sbires et cartes Rencontre ne portent jamais de classe `aspect-*` : le sélecteur
ne les atteint pas, elles restent grises et nues.

**3. Une notion de camp existe déjà** et personne ne s'en sert ici : les cartes
portent `camp-player` / `camp-encounter`, avec `--camp-ring` (vert
`rgba(60,205,120,.85)` / rouge `rgba(228,66,66,.85)`) déjà définis dans
`ScanCard.css`. C'est la source à réutiliser pour le point 2.

## Décisions

Prises une à une avec le joueur le 08/08/2026.

| Question | Décision |
|---|---|
| Quelle couleur | **La couleur d'aspect** (palette existante, inchangée) |
| Quelle forme | **Un cadre qui épouse la carte** — collé au bord, coins arrondis du scan |
| Épaisseur | **Fine, 2 px** |
| De quel côté du bord | **Par-dessus le bord du scan** (vers l'intérieur) |
| Cartes sans aspect | **La couleur de leur camp** (rouge Rencontre) |
| Cartes face cachée | **Aucun cadre** |
| Pastilles (PV, menace, compteurs, étiquette) | **Tout devient gris** |
| Quels effets | **« Noir et blanc » seulement** |

### Ce que ça donne, dit en une phrase

Sous l'effet, la table entière est grise — illustrations, pastilles, chiffres,
halos d'état. La **seule** couleur qui subsiste est un filet de 2 px collé au
bord de chaque carte face visible : sa couleur d'aspect si elle en a une, sinon
la couleur de son camp. Une carte face cachée n'a rien.

## Travail à faire

### 1. Le cadre lui-même

Dans `ui-app/src/board/board.css`, section « Plateau délavé ».

* **Supprimer** `border-radius: inherit` — c'est lui le carré. L'élément a déjà
  ses 8 px ; il n'y a rien à réaffirmer.
* **Remplacer** `outline: 4px … / outline-offset: 3px` par un trait de **2 px
  posé vers l'intérieur**. `box-shadow: inset 0 0 0 2px var(--lisere-aspect)`
  suit le `border-radius` de l'élément et ne déborde jamais — c'est ce qui
  permet de tenir la décision « par-dessus le bord » sans toucher à
  l'espacement du plateau.
  *Attention* : les cartes portent déjà des `box-shadow` pour leurs halos
  (`--camp-ring`, `--state-glow`, voir `ScanCard.css:158`). Écrire une ombre ici
  ÉCRASE les leurs si on ne compose pas. Sous cet effet les halos passent au
  gris de toute façon (décision « tout devient gris »), donc les écraser est
  acceptable — mais il faut le faire exprès et l'écrire.

### 2. Les cartes sans aspect

Faire retomber `--lisere-aspect` sur la couleur du camp quand aucune classe
`aspect-*` n'est présente. Deux voies, à trancher par qui code :

* poser la valeur par défaut sur `.scan-card` (`--lisere-aspect: <camp>`) et
  laisser les règles `aspect-*` la surcharger — le plus simple, une seule règle
  de dessin ;
* ou élargir le sélecteur à `.scan-card` et gérer le camp à part.

La première évite de dupliquer la règle de dessin, et supprime au passage le
sélecteur `[class*='aspect-']`, qui est fragile.

### 3. Les cartes face cachée

Elles portent `is-facedown` et **jamais** de classe `aspect-*` (`ScanCard.tsx:337`
refuse déjà de la poser : « son aspect n'est pas connu du joueur »). Avec le
repli sur le camp, elles hériteraient donc du rouge Rencontre — ce que la
décision refuse. Il faut une exclusion explicite sur `.is-facedown`.
**C'est le piège de ce chantier** : le repli du point 2 crée le défaut du
point 3, et un dos de carte teinté en rouge donnerait une information que le
moteur cache volontairement.

### 4. Le gris total

Vérifier que `filter: grayscale(1)` sur `.scan-visuel` couvre bien pastilles et
étiquettes. Mesuré : `.top-strip` et `.kind-pill` sont bien DANS `.scan-visuel`,
donc déjà gris. Rien à faire — mais à vérifier après coup, parce que le cadre
du point 1 doit rester en dehors de ce filtre.

## Vérification

1. `cd ui-app && npx tsc --noEmit && npx vitest run`.
2. `bash ui-app/deployer.sh`, puis recharger le plateau.
3. Ouvrir Options → « Aperçu météo » → onze clics jusqu'à « Noir et blanc ».
4. Dans la console, sur une carte de main et sur le Méchant :
   ```js
   const c = document.querySelector('.scan-card[data-card-id]')
   getComputedStyle(c).borderRadius   // doit valoir 8px, PAS 0px
   getComputedStyle(c).boxShadow      // doit contenir un inset de 2px
   ```
5. À l'œil, les quatre cas qui comptent : une carte d'aspect (filet coloré),
   une carte Rencontre (filet rouge), une carte face cachée (**aucun** filet),
   et la main où les cartes se chevauchent (aucun filet ne doit mordre sur la
   voisine).
6. Fenêtre étroite : la scène est mise à l'échelle, le filet de 2 px l'est
   aussi. Vérifier qu'il reste visible et ne devient pas un cheveu.

## Ce qui n'est PAS demandé

* Toucher au Sépia ou aux autres ambiances — la décision est « Noir et blanc
  seulement ».
* Garder les PV ou la menace en couleur — la décision est « tout devient gris »,
  et elle a été posée explicitement contre l'option inverse.
* Changer la palette d'aspect. Les cinq couleurs officielles et les deux choisies
  (héros `#a878e8`, basique `#aab3bd`) restent telles quelles.
