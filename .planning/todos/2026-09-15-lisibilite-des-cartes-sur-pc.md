# Les cartes sont moins lisibles sur PC que sur téléphone

**Question de l'utilisateur, 15/09/2026** : « en plus petit, sur téléphone, je
trouve que les cartes sont lisibles, et pas du tout sur l'écran. C'est dû à
quoi ? »

## La réponse, mesurée

Deux causes qui se cumulent, aucune n'est un défaut.

**1. Le PC montre tout, le téléphone montre trois cartes.** En tête de
`board.css` : « la table est mise à l'échelle de la fenêtre. Rien ne défile,
jamais. On voit tout. » L'échelle vaut `min(largeur/1920, hauteur/940)`, donc
1,00 pile sur un 1920×1080 : la carte fait 127 px. Le téléphone, lui, pose
`--card-w: clamp(140px, ...)` et **fait défiler**.

**2. La densité d'écran.** Un téléphone a 3 pixels réels par pixel CSS : la même
carte y est dessinée avec 420 vrais pixels contre 127 sur un écran de PC
ordinaire. Trois fois plus de détail, et tenu à 25 cm au lieu de 60.

| Écran | Échelle | Plafond image | Carte |
|---|---|---|---|
| 1920×1080, densité 1 | 1,00 | 1,94 | 127 px |
| 2560×1440, densité 1 | 1,33 | 1,94 | 169 px |
| 1920×1080, densité 2 | 1,00 | **1,00** | 127 px (254 réels) |

⚠ **Régénérer les vignettes plus grandes ne servirait à rien sur un 1920×1080** :
le plafond dû à l'image est à 1,94 et on est à 1,00. Ce levier ne vaut que sur
un écran à forte densité, où le plafond tombe pile à 1,00 et bloque tout.

## La piste essayée, et abandonnée

Idée de l'utilisateur : supprimer la rangée dédiée à la MAIN (une des quatre de
la grille), puisqu'elle ne sert que quand on l'ouvre, et la faire chevaucher la
rangée des héros.

**Maquetté sur le vrai plateau**, à partir d'un état de partie enregistré
(`board.html?etat=...`, aucune partie créée ni détruite), en 1920×1080, et
mesuré :

- carte : **127 → 165 px**, soit +30 % ;
- main : 229 px de hauteur rendus à la table.

⚠ **Abandonné par l'utilisateur, et sa raison est juste** : les colonnes
latérales sont FIGÉES (300 px à gauche, 384 px à droite,
`grid-template-columns`). Grossir les cartes du centre ne les touche pas : on
gagne au milieu et on creuse les côtés, la table se déséquilibre.

Autre défaut relevé sur la maquette : la colonne de gauche déborde par le haut
dès que les rangées grandissent, parce qu'elle empile deux cartes par rangée.

## Ce qui resterait, si le sujet revient

- Rendre les colonnes latérales élastiques plutôt que figées, AVANT de toucher
  à la hauteur. Sans ça, toute tentative se heurtera au même mur.
- Ou renoncer au « rien ne défile » sur PC, ce qui est un changement de
  principe, pas un réglage.
- Ou considérer que la table sert à SITUER et l'agrandissement au survol à LIRE.

## Statut

**Question répondue, piste abandonnée le 15/09/2026** sur décision de
l'utilisateur. Rien n'a été modifié dans le code.
