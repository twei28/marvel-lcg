# Texte français par-dessus le bloc anglais — étudié, ABANDONNÉ

Étudié et tranché le 07/08/2026. **Rien n'a été codé, et rien ne doit l'être.**

## Décision

On garde le mécanisme actuel : le texte français s'affiche dans un bloc SOUS
l'agrandissement de la carte (`ApercuMarvelcdb`, `board/Board.tsx`). On ne le
superpose PAS au bloc de texte anglais de la carte.

Ce document existe pour que la question ne soit pas rouverte sans les mesures
qui l'ont fait fermer.

## Pourquoi c'était tentant

Le besoin est réel : on lit la carte à un endroit et sa traduction à un autre.

Et le terrain semblait favorable :

| | Cartes |
|---|---|
| Catalogue complet (`cards.json` + `cards_custom.json`) | 4 748 |
| Avec un scan français (`assets/pics-fr/`) | 4 210 |
| **Sans scan français** | **538** |
| …dont le texte français est **déjà écrit** | **485** |
| …sans aucun texte français | 53 |
| …dont celles qui ont vraiment du texte à traduire | 26 (surtout les défis `24xx`) |

Le texte existait donc déjà pour 90 % du périmètre : ce n'était pas un travail
de traduction, seulement de présentation. Et le projet a un précédent de
superposition calibrée sur les scans
(`ui-app/outils/calibrer-stat-bubbles.py` → `components/stat-bubbles/positions.ts`).

## Ce qui l'a tué

Poser un pavé sur le bloc de texte suppose de savoir OÙ il est. L'hypothèse de
travail était : « les cartes fan-made sortent des générateurs officiels, leurs
blocs tombent au même endroit, donc un rectangle par famille de carte suffit ».

**Cette hypothèse est fausse.** Vérifié image par image :

* `60017` (Daredevil's Billy Club, Upgrade) est une carte GÉNÉRÉE : aucune
  illustration, texte sur fond crème, zone de texte de ~29 % à ~98 % de la
  hauteur, aux trois quarts vide.
* `60018` (The Man Without Fear, Upgrade) est un VRAI SCAN professionnel :
  illustration, encadré blanc, ligne de traits, règles, citation en italique —
  encadré vers 60-90 % de la hauteur.

Même famille, géométries sans rapport. La famille de carte n'est pas une clé
utilisable.

Et le lot est plus hétéroclite encore :

* **117 des 485 cartes n'ont aucune image locale** — servies depuis un autre
  dossier configuré (`image_folders` de `launch.json`) ou téléchargées à la
  volée depuis `image_servers`. On ne peut même pas les calibrer hors ligne.
* Les 368 restantes se répartissent sur **au moins six formats** : 1500×2150,
  450×645, 300×426, 727×1040, 1451×2080, 450×630.

Un pavé mal calé ne se signale pas : il recouvrirait l'illustration ou laisserait
l'anglais dépasser, sans erreur ni avertissement. C'est le pire mode de panne.

## Les issues envisagées, et pourquoi elles n'ont pas été retenues

* **Calibrage progressif à la demande** (tracer le rectangle quand on croise une
  carte non calibrée) — faisable, mais c'est un mode d'édition à construire et à
  maintenir pour un confort marginal.
* **Détection automatique de l'encadré** par analyse d'image — un encadré de
  texte est bien moins contrasté qu'une bulle de statistique colorée ; les
  échecs seraient silencieux et il faudrait un recours de toute façon.
* **Un pavé sur une zone large et sûre** (moitié basse de la carte) — ne rate
  jamais sa cible, mais masque l'illustration des vrais scans.

Aucune ne rendait le résultat plus lisible que le bloc actuel, qui lui marche
sur les 485 cartes sans le moindre risque de décalage.

## Ce qui reste vrai et utile

* Les 26 cartes qui ont du texte imprimé sans traduction française sont
  identifiables (presque toutes des défis `24xx`) : les traduire à la main dans
  `board/textes-fr-fanmade.ts` améliorerait le bloc existant, sans toucher à
  quoi que ce soit d'autre.
* Le pont `board/marvelcdb.ts` pointe sur **fr**.marvelcdb.com et sait déjà
  rendre le texte officiel français. Il est coupé par défaut, volontairement,
  pour que le jeu tourne hors ligne.
