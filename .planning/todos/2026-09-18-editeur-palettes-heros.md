# Un éditeur de palettes, réservé au compte auteur

**Demande de l'utilisateur, 18/09/2026** : « pour chaque personnage, on a une
couleur en bas à droite de l'écran, et certaines ne sont pas correctes. Un mode
disponible que pour moi, où je peux mettre le hex principal, secondaire et
tertiaire de chaque personnage. »

## Ce qui existe déjà

- `data/palettes-heros.json` : trois couleurs RVB par identifiant de carte,
  **générées** par `outils/palettes-heros.py` à partir du CONTOUR des cartes
  signature. Le fichier dit lui-même de ne pas l'éditer à la main.
- `ui-app/src/board/halo-heros.ts` les lit pour teinter le fond du plateau.
- Les comptes existent dans le SITE, pas dans le moteur :
  `site/orchestrateur.py`, base `narwhal.db`, table `comptes` (pseudo, e-mail),
  sessions de trois mois. Le moteur, lui, n'a qu'un laissez-passer de table.

## Décisions de cadrage

| Question | Décision |
|---|---|
| Qui y a accès | Le compte auteur du site, identifié par son pseudo |
| Ce que ça produit | Un fichier de CORRECTIONS dans le dépôt, à côté des palettes générées |
| Emplacement | Une page à part, tous les personnages en liste, correction à la chaîne |

## Le point dur, et il n'est pas celui qu'on croit

Ce n'est pas l'éditeur, c'est **faire savoir au plateau que le visiteur est
l'auteur**. L'identité vit dans le site, le plateau est servi par le moteur, et
rien ne relie aujourd'hui les deux pour cet usage. À cadrer avant d'écrire quoi
que ce soit : c'est là que se décide si l'idée tient en une journée ou en trois.

## Deux points à ne pas perdre de vue

1. **Les corrections doivent survivre à la régénération.** Le générateur
   réécrit `palettes-heros.json` ; les corrections vont donc dans un fichier
   séparé, lu par-dessus. Sinon chaque passe du générateur efface le travail.
2. **Juger sur un échantillon est précisément ce qui a produit les couleurs
   fausses.** L'utilisateur a choisi la page en liste en connaissance de cause.
   Atténuation retenue : l'échantillon de chaque personnage doit reproduire le
   VRAI rendu du fond de plateau, pas un aplat de couleur.

## Statut

Cadrée le 18/09/2026, **non commencée**. En attente derrière le mode manuel.
