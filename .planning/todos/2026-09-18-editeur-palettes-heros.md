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

## Ce qui a été fait, le 19/09/2026

**Le point dur n'en était pas un : le moteur sait déjà qui est l'auteur.**
`_est_administrateur` (server_get.py) existait pour le relevé des
illustrations : l'orchestrateur ne renseigne `site_admin_url` que pour la
table de l'administrateur, et le siège 0 est celui du titulaire du compte.
L'éditeur vit donc entièrement dans le jeu, comme `/releve-images.html`, sans
rien ajouter entre le site et le moteur.

| Pièce | Fichier | Preuve |
|---|---|---|
| Règles pures (hex, groupement, fond) | `public/js/palettes/couleurs.js` | `node --test tools/tests-lanceur/palettes-couleurs.test.mjs` (11) |
| Page en liste | `public/palettes-heros.html`, `public/js/palettes/app.js`, `public/css/palettes-heros.css` | — |
| Bouton (compte auteur) | `public/js/prepare/lien-admin.js` | — |
| Corrections par-dessus le généré | `src/cards/palettes_heros.py` | `RELEASE=1 python3.10 tools/test_palettes_heros.py` (13) |
| Écriture réservée, atomique | `/save_palette_heros` (server_get.py) | même garde que `/save_images_cartes` |
| L'aperçu montre le VRAI fond | `ui-app/src/board/halo-heros-accord.test.ts` | vitest (5) |

Les deux points à ne pas perdre de vue ont été tenus :

1. **Les corrections survivent à la régénération** : elles vivent dans
   `data/palettes-heros-corrections.json`, jamais touché par
   `outils/palettes-heros.py`, et posé par-dessus à la lecture. Elles
   survivent aussi au DÉPLOIEMENT : `deployer.ps1` exclut ce fichier de
   l'archive envoyée et le rapatrie dans le dépôt après coup, puisque c'est
   sur le serveur qu'on corrige.
2. **L'échantillon reproduit le vrai rendu** : la bande diagonale du plateau,
   sur le fond sombre du plateau, et une gate compare les deux formules pour
   qu'elles ne dérivent pas.

## Statut

**Fait le 19/09/2026.** Reste à faire côté joueur : ouvrir la page depuis sa table et
corriger les couleurs qui tombent à côté.
